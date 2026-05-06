#!/usr/bin/env python3
"""Validate generated asset promotion candidates.

This validator is intentionally strict about technical production requirements
that are easy to automate: PNG mode, alpha, canvas size, naming, and manifest
completeness. It does not replace human art review or in-engine scale testing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

try:
    from PIL import Image
except ImportError:  # pragma: no cover - dependency boundary
    Image = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = (ROOT / "assets" / "generated",)
ALLOWED_CANVAS_SIZES = {(512, 512), (1024, 1024), (2048, 2048)}
SAFE_FILE_RE = re.compile(r"^[a-z0-9][a-z0-9_\-]*\.(png|jpg|jpeg|json|svg)$")
SAFE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_\-]*$")
REQUIRED_MANIFEST_FIELDS = {
    "id",
    "type",
    "source_kind",
    "license_status",
    "usage",
    "file",
    "canvas",
    "pivot",
    "qa_status",
}
ALLOWED_QA_STATUSES = {"source", "candidate", "approved_first_playable", "final", "rejected"}
ALLOWED_SOURCE_KINDS = {"generated", "generated_from_reference", "third_party_derivative", "manual_paintover"}
ALLOWED_LICENSE_STATUS = {"project_generated", "third_party_reviewed", "requires_review"}

STRUCTURAL_SVG_MARKERS = (
    "NG-PRIMITIVE-BASE:",
    "NG-PRIMITIVE-SHADOW:",
    "NG-PRIMITIVE-EDGE:",
)
STRUCTURAL_SVG_MARKER_RE = {
    marker: re.compile(rf"{re.escape(marker)}\s*[A-Za-z0-9][A-Za-z0-9_-]*")
    for marker in STRUCTURAL_SVG_MARKERS
}
SVG_STRUCTURAL_CLASS_MARKER = "NG-SVG-CLASS: structural"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated NG art assets")
    parser.add_argument(
        "paths",
        nargs="*",
        help="Asset directories or manifest files to validate. Defaults to assets/generated if present.",
    )
    args = parser.parse_args()

    if Image is None:
        print("Pillow is required: python -m pip install pillow", file=sys.stderr)
        return 2

    targets = _resolve_targets(args.paths)
    if not targets:
        print("No generated asset manifests found. Nothing to validate.")
        return 0

    errors: list[str] = []
    for manifest_path in targets:
        _validate_manifest(manifest_path, errors)

    if errors:
        print("Generated asset validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Generated asset validation passed: {len(targets)} manifest(s)")
    return 0


def _resolve_targets(paths: list[str]) -> list[Path]:
    if paths:
        raw_targets = [Path(path) for path in paths]
    else:
        raw_targets = [path for path in DEFAULT_ROOTS if path.exists()]

    manifests: list[Path] = []
    for target in raw_targets:
        if not target.is_absolute():
            target = ROOT / target
        if target.is_file() and target.name == "manifest.json":
            manifests.append(target)
        elif target.is_dir():
            manifests.extend(sorted(target.rglob("manifest.json")))
    return sorted(set(manifests))


def _validate_manifest(manifest_path: Path, errors: list[str]) -> None:
    rel_manifest = _rel(manifest_path)
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{rel_manifest}: invalid JSON: {exc}")
        return

    entries = manifest.get("assets", manifest)
    if isinstance(entries, dict):
        entries = [entries]
    if not isinstance(entries, list) or not entries:
        errors.append(f"{rel_manifest}: manifest must be an object or non-empty assets list")
        return

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"{rel_manifest}: assets[{index}] must be an object")
            continue
        _validate_entry(manifest_path.parent, rel_manifest, index, entry, errors)


def _validate_entry(base_dir: Path, rel_manifest: str, index: int, entry: dict[str, Any], errors: list[str]) -> None:
    prefix = f"{rel_manifest}:assets[{index}]"
    missing = sorted(REQUIRED_MANIFEST_FIELDS - set(entry.keys()))
    if missing:
        errors.append(f"{prefix}: missing fields: {', '.join(missing)}")

    asset_id = str(entry.get("id", ""))
    if not SAFE_ID_RE.match(asset_id):
        errors.append(f"{prefix}: unsafe id: {asset_id!r}")

    source_kind = str(entry.get("source_kind", ""))
    if source_kind not in ALLOWED_SOURCE_KINDS:
        errors.append(f"{prefix}: source_kind must be one of {sorted(ALLOWED_SOURCE_KINDS)}")

    license_status = str(entry.get("license_status", ""))
    if license_status not in ALLOWED_LICENSE_STATUS:
        errors.append(f"{prefix}: license_status must be one of {sorted(ALLOWED_LICENSE_STATUS)}")

    qa_status = str(entry.get("qa_status", ""))
    if qa_status not in ALLOWED_QA_STATUSES:
        errors.append(f"{prefix}: qa_status must be one of {sorted(ALLOWED_QA_STATUSES)}")

    file_name = str(entry.get("file", ""))
    file_path = Path(file_name)
    if not SAFE_FILE_RE.match(file_path.name):
        errors.append(f"{prefix}: asset file name must be lowercase snake/kebab case PNG/JPG/JSON: {file_name!r}")
    if file_path.is_absolute() or ".." in file_path.parts:
        errors.append(f"{prefix}: asset file path must stay inside manifest directory: {file_name!r}")
        return

    canvas = entry.get("canvas")
    if not _is_int_pair(canvas):
        errors.append(f"{prefix}: canvas must be [width, height]")
    else:
        canvas_tuple = (int(canvas[0]), int(canvas[1]))
        if canvas_tuple not in ALLOWED_CANVAS_SIZES:
            errors.append(f"{prefix}: canvas {canvas_tuple} not allowed; expected one of {sorted(ALLOWED_CANVAS_SIZES)}")

    pivot = entry.get("pivot")
    if not _is_int_pair(pivot):
        errors.append(f"{prefix}: pivot must be [x, y]")

    asset_path = base_dir / file_path
    if not asset_path.exists():
        errors.append(f"{prefix}: asset file missing: {_rel(asset_path)}")
        return

    if asset_path.suffix.lower() == ".png":
        _validate_png(asset_path, prefix, entry, errors)
    elif asset_path.suffix.lower() == ".svg":
        _validate_svg(asset_path, prefix, errors)

    mask_name = entry.get("mask")
    if mask_name:
        mask_path = base_dir / str(mask_name)
        if not mask_path.exists():
            errors.append(f"{prefix}: mask file missing: {_rel(mask_path)}")

    preview_name = entry.get("preview")
    if preview_name:
        preview_path = base_dir / str(preview_name)
        if not preview_path.exists():
            errors.append(f"{prefix}: preview file missing: {_rel(preview_path)}")


def _validate_png(asset_path: Path, prefix: str, entry: dict[str, Any], errors: list[str]) -> None:
    with Image.open(asset_path) as image:
        if image.mode != "RGBA":
            errors.append(f"{prefix}: PNG must be RGBA, got {image.mode}: {_rel(asset_path)}")
            return
        if image.size not in ALLOWED_CANVAS_SIZES:
            errors.append(f"{prefix}: PNG canvas {image.size} not allowed: {_rel(asset_path)}")
        declared_canvas = entry.get("canvas")
        if _is_int_pair(declared_canvas) and image.size != (int(declared_canvas[0]), int(declared_canvas[1])):
            errors.append(f"{prefix}: manifest canvas {declared_canvas} does not match PNG size {image.size}")

        alpha = image.getchannel("A")
        alpha_min, alpha_max = alpha.getextrema()
        if alpha_min == 255:
            errors.append(f"{prefix}: PNG has no transparent pixels: {_rel(asset_path)}")
        if alpha_max == 0:
            errors.append(f"{prefix}: PNG is fully transparent: {_rel(asset_path)}")
        transparent_count = _count_alpha_pixels(alpha, lambda value: value == 0)
        semi_count = _count_alpha_pixels(alpha, lambda value: 0 < value < 255)
        total = image.size[0] * image.size[1]
        if transparent_count / total < 0.15:
            errors.append(f"{prefix}: PNG has too little transparent padding ({transparent_count / total:.1%})")
        if semi_count / total > 0.30:
            errors.append(f"{prefix}: PNG has unusually high semi-transparent area ({semi_count / total:.1%}); check halo/shadow mask")

        rgba = image.load()
        corner_points = [
            (0, 0),
            (image.size[0] - 1, 0),
            (0, image.size[1] - 1),
            (image.size[0] - 1, image.size[1] - 1),
        ]
        if any(rgba[x, y][3] != 0 for x, y in corner_points):
            errors.append(f"{prefix}: PNG corners should be fully transparent: {_rel(asset_path)}")




def _validate_svg(asset_path: Path, prefix: str, errors: list[str]) -> None:
    contents = asset_path.read_text(encoding="utf-8")

    # Structural classes must include explicit primitive traceability markers.
    if SVG_STRUCTURAL_CLASS_MARKER not in contents:
        return

    for marker, marker_re in STRUCTURAL_SVG_MARKER_RE.items():
        if not marker_re.search(contents):
            errors.append(
                f"{prefix}: structural SVG missing non-empty marker '{marker}' in metadata/comments: {_rel(asset_path)}"
            )

def _count_alpha_pixels(alpha_image: Any, predicate: Callable[[int], bool]) -> int:
    histogram = alpha_image.histogram()
    return sum(count for value, count in enumerate(histogram) if predicate(value))


def _is_int_pair(value: Any) -> bool:
    return isinstance(value, list) and len(value) == 2 and all(isinstance(item, int) for item in value)


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
