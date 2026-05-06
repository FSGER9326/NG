#!/usr/bin/env python3
"""Validate NG asset production batch manifests.

Production batch manifests are lightweight handoff records for generated,
external, or hand-painted candidate art before the files are promoted into a
canonical asset kit manifest.

They intentionally do not require candidate PNGs to exist in the repository;
that allows large art handoff packages to be reviewed before selected assets are
committed and marked `accepted` in data/asset_kits/*.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets" / "kits"

VALID_STATUSES = {
    "planned",
    "generated_candidate",
    "external_candidate",
    "cleaned",
    "accepted",
    "rejected",
}

VALID_CATEGORIES = {
    "buildings",
    "architecture",
    "props",
    "clutter",
    "vegetation",
    "decals",
    "occluders",
}

TOP_LEVEL_REQUIRED = {
    "batch",
    "style",
    "source_type",
    "external_imports",
    "cleanup_pipeline",
    "canonical_acceptance_note",
    "assets",
}

ASSET_REQUIRED = {
    "id",
    "display_name",
    "category",
    "source_file",
    "status",
    "candidate_file",
    "sha256",
    "production_notes",
}

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def production_manifest_files() -> list[Path]:
    if not ASSET_ROOT.exists():
        return []
    return sorted(ASSET_ROOT.glob("*/production_manifest_*.json"))


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def check_non_empty_string(path: Path, field: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{rel(path)}: {field} must be a non-empty string")


def check_relative_file(path: Path, asset_id: str, field: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{rel(path)} asset {asset_id}: {field} must be a non-empty string")
        return
    value_path = Path(value)
    if value_path.is_absolute() or ".." in value_path.parts:
        errors.append(f"{rel(path)} asset {asset_id}: {field} must be a safe relative path")


def check_string_list(path: Path, field: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{rel(path)}: {field} must be a list")
        return
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{rel(path)}: {field} must contain only non-empty strings")


def check_manifest(path: Path, data: Any, errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append(f"{rel(path)}: manifest must be a JSON object")
        return

    missing = sorted(TOP_LEVEL_REQUIRED - set(data.keys()))
    if missing:
        errors.append(f"{rel(path)}: missing required top-level fields: {', '.join(missing)}")

    check_non_empty_string(path, "batch", data.get("batch"), errors)
    check_non_empty_string(path, "style", data.get("style"), errors)
    check_non_empty_string(path, "source_type", data.get("source_type"), errors)
    check_non_empty_string(path, "canonical_acceptance_note", data.get("canonical_acceptance_note"), errors)

    external_imports = data.get("external_imports")
    if not isinstance(external_imports, list):
        errors.append(f"{rel(path)}: external_imports must be a list")

    check_string_list(path, "cleanup_pipeline", data.get("cleanup_pipeline"), errors)

    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append(f"{rel(path)}: assets must be a non-empty list")
        return

    seen_ids: set[str] = set()
    seen_candidate_files: set[str] = set()

    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            errors.append(f"{rel(path)} asset #{index}: must be an object")
            continue

        asset_id = asset.get("id", f"#{index}")
        if not isinstance(asset_id, str) or not asset_id.strip():
            errors.append(f"{rel(path)} asset #{index}: id must be a non-empty string")
            asset_id = f"#{index}"
        elif asset_id in seen_ids:
            errors.append(f"{rel(path)}: duplicate asset id: {asset_id}")
        else:
            seen_ids.add(asset_id)

        missing_asset_fields = sorted(ASSET_REQUIRED - set(asset.keys()))
        if missing_asset_fields:
            errors.append(f"{rel(path)} asset {asset_id}: missing fields: {', '.join(missing_asset_fields)}")

        for field in ("display_name", "production_notes"):
            if not isinstance(asset.get(field), str) or not asset.get(field, "").strip():
                errors.append(f"{rel(path)} asset {asset_id}: {field} must be a non-empty string")

        category = asset.get("category")
        if category not in VALID_CATEGORIES:
            errors.append(f"{rel(path)} asset {asset_id}: invalid category {category!r}")

        status = asset.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{rel(path)} asset {asset_id}: invalid status {status!r}")

        check_relative_file(path, asset_id, "source_file", asset.get("source_file"), errors)
        check_relative_file(path, asset_id, "candidate_file", asset.get("candidate_file"), errors)

        candidate_file = asset.get("candidate_file")
        if isinstance(candidate_file, str):
            if candidate_file in seen_candidate_files:
                errors.append(f"{rel(path)} asset {asset_id}: duplicate candidate_file {candidate_file}")
            else:
                seen_candidate_files.add(candidate_file)

        sha256 = asset.get("sha256")
        if not isinstance(sha256, str) or not SHA256_RE.fullmatch(sha256):
            errors.append(f"{rel(path)} asset {asset_id}: sha256 must be 64 lowercase hex characters")


def main() -> int:
    errors: list[str] = []
    files = production_manifest_files()

    for path in files:
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {rel(path)}: {exc}")
            continue
        check_manifest(path, data, errors)

    if errors:
        print("Asset production batch validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Asset production batch validation passed: {len(files)} manifest(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
