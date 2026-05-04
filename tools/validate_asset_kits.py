#!/usr/bin/env python3
"""Validate NG asset-kit manifests.

This validator checks lightweight structure and production-readiness rules for
JSON manifests under data/asset_kits/.

Usage:
    python tools/validate_asset_kits.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSET_KIT_ROOT = ROOT / "data" / "asset_kits"

TOP_LEVEL_REQUIRED = {
    "id",
    "name",
    "style_family",
    "version",
    "purpose",
    "camera",
    "lighting",
    "source_policy",
    "global_acceptance_checks",
    "assets",
}

ASSET_REQUIRED = {
    "id",
    "display_name",
    "category",
    "subcategory",
    "asset_type",
    "priority",
    "status",
    "intended_file",
    "scale_class",
    "tags",
    "placement_rules",
    "acceptance_checks",
}

VALID_STATUSES = {
    "planned",
    "generated_candidate",
    "external_candidate",
    "cleaned",
    "accepted",
    "rejected",
}

VALID_ASSET_TYPES = {
    "canonical_modular",
    "canonical_semi_modular",
    "scene_specific",
    "generated_reference",
    "external_source",
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


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def manifest_files() -> list[Path]:
    if not ASSET_KIT_ROOT.exists():
        return []
    return sorted(path for path in ASSET_KIT_ROOT.glob("*.json") if path.is_file())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def check_string_list(path: Path, asset_id: str, field: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{rel(path)} asset {asset_id}: {field} must be a list")
        return
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{rel(path)} asset {asset_id}: {field} must contain only non-empty strings")


def check_manifest(path: Path, data: Any, errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append(f"{rel(path)}: manifest must be a JSON object")
        return

    missing = sorted(TOP_LEVEL_REQUIRED - set(data.keys()))
    if missing:
        errors.append(f"{rel(path)}: missing required top-level fields: {', '.join(missing)}")

    kit_id = data.get("id")
    if not isinstance(kit_id, str) or not kit_id.strip():
        errors.append(f"{rel(path)}: id must be a non-empty string")

    version = data.get("version")
    if not isinstance(version, int) or version < 1:
        errors.append(f"{rel(path)}: version must be a positive integer")

    global_checks = data.get("global_acceptance_checks")
    if not isinstance(global_checks, list) or not global_checks:
        errors.append(f"{rel(path)}: global_acceptance_checks must be a non-empty list")

    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append(f"{rel(path)}: assets must be a non-empty list")
        return

    seen_ids: set[str] = set()
    seen_priorities: set[int] = set()

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

        category = asset.get("category")
        if category not in VALID_CATEGORIES:
            errors.append(f"{rel(path)} asset {asset_id}: invalid category {category!r}")

        status = asset.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{rel(path)} asset {asset_id}: invalid status {status!r}")

        asset_type = asset.get("asset_type")
        if asset_type not in VALID_ASSET_TYPES:
            errors.append(f"{rel(path)} asset {asset_id}: invalid asset_type {asset_type!r}")

        priority = asset.get("priority")
        if not isinstance(priority, int) or priority < 1:
            errors.append(f"{rel(path)} asset {asset_id}: priority must be a positive integer")
        elif priority in seen_priorities:
            errors.append(f"{rel(path)} asset {asset_id}: duplicate priority {priority}")
        else:
            seen_priorities.add(priority)

        intended_file = asset.get("intended_file")
        if not isinstance(intended_file, str) or not intended_file.startswith("assets/kits/"):
            errors.append(f"{rel(path)} asset {asset_id}: intended_file must start with assets/kits/")
        elif ".." in Path(intended_file).parts:
            errors.append(f"{rel(path)} asset {asset_id}: intended_file must not contain '..'")

        check_string_list(path, asset_id, "tags", asset.get("tags"), errors)
        check_string_list(path, asset_id, "placement_rules", asset.get("placement_rules"), errors)
        check_string_list(path, asset_id, "acceptance_checks", asset.get("acceptance_checks"), errors)

        if status == "accepted":
            if not isinstance(intended_file, str) or not (ROOT / intended_file).exists():
                errors.append(f"{rel(path)} asset {asset_id}: accepted asset file does not exist: {intended_file}")


def main() -> int:
    errors: list[str] = []
    files = manifest_files()

    if not files:
        errors.append("No asset-kit manifests found under data/asset_kits/.")

    for path in files:
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {rel(path)}: {exc}")
            continue
        check_manifest(path, data, errors)

    if errors:
        print("Asset kit validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Asset kit validation passed: {len(files)} manifest(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
