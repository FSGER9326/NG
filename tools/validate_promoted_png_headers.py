#!/usr/bin/env python3
"""Validate promoted NG asset PNG headers.

This validator checks file-backed asset-kit entries only: assets marked
`cleaned` or `accepted`. It confirms the committed file is a real PNG with a
valid IHDR header and reasonable dimensions for the low-spec Godot 4 pipeline.

The full SHA/file-existence check lives in `validate_promoted_asset_files.py`;
this script adds lightweight binary sanity checks without third-party image
libraries.
"""

from __future__ import annotations

import json
import struct
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSET_KIT_MANIFEST_ROOT = ROOT / "data" / "asset_kits"
FILE_BACKED_STATUSES = {"cleaned", "accepted"}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MIN_DIMENSION = 8
MAX_DIMENSION = 4096


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def asset_kit_files() -> list[Path]:
    if not ASSET_KIT_MANIFEST_ROOT.exists():
        return []
    return sorted(ASSET_KIT_MANIFEST_ROOT.glob("*.json"))


def read_png_header(path: Path) -> tuple[int, int, int, int]:
    """Return width, height, bit depth, and color type from a PNG IHDR chunk."""
    with path.open("rb") as handle:
        signature = handle.read(8)
        if signature != PNG_SIGNATURE:
            raise ValueError("missing PNG signature")

        raw_length = handle.read(4)
        chunk_type = handle.read(4)
        if len(raw_length) != 4 or len(chunk_type) != 4:
            raise ValueError("truncated PNG header")

        length = struct.unpack(">I", raw_length)[0]
        if chunk_type != b"IHDR":
            raise ValueError("first PNG chunk is not IHDR")
        if length != 13:
            raise ValueError(f"unexpected IHDR length {length}")

        ihdr = handle.read(length)
        if len(ihdr) != length:
            raise ValueError("truncated IHDR data")

    width, height, bit_depth, color_type = struct.unpack(">IIBB", ihdr[:10])
    return width, height, bit_depth, color_type


def check_asset(manifest_path: Path, asset: dict[str, Any], errors: list[str]) -> None:
    asset_id = asset.get("id", "<missing id>")
    status = asset.get("status")
    if status not in FILE_BACKED_STATUSES:
        return

    intended_file = asset.get("intended_file")
    if not isinstance(intended_file, str) or not intended_file.strip():
        errors.append(f"{rel(manifest_path)} asset {asset_id}: {status} asset must define intended_file")
        return

    intended_path = Path(intended_file)
    if intended_path.is_absolute() or ".." in intended_path.parts:
        errors.append(f"{rel(manifest_path)} asset {asset_id}: intended_file must be a safe relative path")
        return

    repo_file = ROOT / intended_path
    if not repo_file.exists():
        # The file-existence validator reports this more specifically; skip duplicate header errors.
        return

    try:
        width, height, bit_depth, color_type = read_png_header(repo_file)
    except (OSError, ValueError, struct.error) as exc:
        errors.append(f"{rel(manifest_path)} asset {asset_id}: invalid PNG header for {intended_file}: {exc}")
        return

    if not (MIN_DIMENSION <= width <= MAX_DIMENSION):
        errors.append(
            f"{rel(manifest_path)} asset {asset_id}: PNG width {width} outside "
            f"allowed range {MIN_DIMENSION}-{MAX_DIMENSION}: {intended_file}"
        )
    if not (MIN_DIMENSION <= height <= MAX_DIMENSION):
        errors.append(
            f"{rel(manifest_path)} asset {asset_id}: PNG height {height} outside "
            f"allowed range {MIN_DIMENSION}-{MAX_DIMENSION}: {intended_file}"
        )
    if bit_depth not in {8, 16}:
        errors.append(f"{rel(manifest_path)} asset {asset_id}: unsupported PNG bit depth {bit_depth}: {intended_file}")
    if color_type not in {2, 3, 4, 6}:
        errors.append(f"{rel(manifest_path)} asset {asset_id}: unsupported PNG color type {color_type}: {intended_file}")


def check_manifest(path: Path, errors: list[str]) -> None:
    try:
        data = load_json(path)
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {rel(path)}: {exc}")
        return

    assets = data.get("assets") if isinstance(data, dict) else None
    if not isinstance(assets, list):
        errors.append(f"{rel(path)}: assets must be a list")
        return

    for asset in assets:
        if not isinstance(asset, dict):
            errors.append(f"{rel(path)}: asset entries must be objects")
            continue
        check_asset(path, asset, errors)


def main() -> int:
    errors: list[str] = []
    files = asset_kit_files()
    for path in files:
        check_manifest(path, errors)

    if errors:
        print("Promoted PNG header validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Promoted PNG header validation passed: {len(files)} manifest(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
