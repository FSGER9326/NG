#!/usr/bin/env python3
"""Validate NG asset-generation batch manifests.

Batch manifests live under data/asset_batches/ and turn an asset-kit manifest
into concrete production queues with prompts, review checks, and candidate status.

Usage:
    python tools/validate_asset_batches.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSET_BATCH_ROOT = ROOT / "data" / "asset_batches"
ASSET_KIT_ROOT = ROOT / "data" / "asset_kits"

TOP_LEVEL_REQUIRED = {
    "id",
    "name",
    "target_kit",
    "target_area",
    "status",
    "purpose",
    "source_files",
    "global_prompt_lock",
    "global_negative_prompt",
    "batch_acceptance_checks",
    "assets",
}

ASSET_REQUIRED = {
    "asset_id",
    "target_file",
    "candidate_status",
    "generation_prompt_addon",
    "review_checks",
}

VALID_BATCH_STATUSES = {
    "planned",
    "generating",
    "reviewing",
    "accepted",
    "blocked",
}

VALID_CANDIDATE_STATUSES = {
    "not_started",
    "generated_candidate",
    "needs_cleanup",
    "accepted",
    "rejected",
    "blocked",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def batch_files() -> list[Path]:
    if not ASSET_BATCH_ROOT.exists():
        return []
    return sorted(path for path in ASSET_BATCH_ROOT.glob("*.json") if path.is_file())


def kit_manifests() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not ASSET_KIT_ROOT.exists():
        return result
    for path in sorted(ASSET_KIT_ROOT.glob("*.json")):
        if not path.is_file():
            continue
        data = load_json(path)
        if isinstance(data, dict) and isinstance(data.get("id"), str):
            result[data["id"]] = data
    return result


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    return []


def check_string_list(path: Path, context: str, field: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{rel(path)} {context}: {field} must be a non-empty list")
        return
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{rel(path)} {context}: {field} must contain only non-empty strings")


def kit_asset_index(kit: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for asset in as_list(kit.get("assets")):
        if isinstance(asset, dict) and isinstance(asset.get("id"), str):
            result[asset["id"]] = asset
    return result


def check_batch(path: Path, data: Any, kits: dict[str, dict[str, Any]], errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append(f"{rel(path)}: batch manifest must be a JSON object")
        return

    missing = sorted(TOP_LEVEL_REQUIRED - set(data.keys()))
    if missing:
        errors.append(f"{rel(path)}: missing required top-level fields: {', '.join(missing)}")

    batch_id = data.get("id")
    if not isinstance(batch_id, str) or not batch_id.strip():
        errors.append(f"{rel(path)}: id must be a non-empty string")

    status = data.get("status")
    if status not in VALID_BATCH_STATUSES:
        errors.append(f"{rel(path)}: invalid status {status!r}")

    target_kit_id = data.get("target_kit")
    target_kit = kits.get(target_kit_id) if isinstance(target_kit_id, str) else None
    if target_kit is None:
        errors.append(f"{rel(path)}: target_kit references missing kit: {target_kit_id}")
        kit_assets: dict[str, dict[str, Any]] = {}
    else:
        kit_assets = kit_asset_index(target_kit)

    target_area = data.get("target_area")
    if not isinstance(target_area, str) or not target_area.strip():
        errors.append(f"{rel(path)}: target_area must be a non-empty string")

    for field in ("purpose", "global_prompt_lock", "global_negative_prompt"):
        if not isinstance(data.get(field), str) or not data.get(field).strip():
            errors.append(f"{rel(path)}: {field} must be a non-empty string")

    check_string_list(path, "batch", "source_files", data.get("source_files"), errors)
    for source_file in as_list(data.get("source_files")):
        if isinstance(source_file, str) and not (ROOT / source_file).exists():
            errors.append(f"{rel(path)}: source_file does not exist: {source_file}")

    check_string_list(path, "batch", "batch_acceptance_checks", data.get("batch_acceptance_checks"), errors)

    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append(f"{rel(path)}: assets must be a non-empty list")
        return

    seen_asset_ids: set[str] = set()
    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            errors.append(f"{rel(path)} asset #{index}: must be an object")
            continue
        check_batch_asset(path, index, asset, kit_assets, seen_asset_ids, errors)


def check_batch_asset(
    path: Path,
    index: int,
    asset: dict[str, Any],
    kit_assets: dict[str, dict[str, Any]],
    seen_asset_ids: set[str],
    errors: list[str],
) -> None:
    asset_id = asset.get("asset_id", f"#{index}")
    if not isinstance(asset_id, str) or not asset_id.strip():
        errors.append(f"{rel(path)} asset #{index}: asset_id must be a non-empty string")
        asset_id = f"#{index}"
    elif asset_id in seen_asset_ids:
        errors.append(f"{rel(path)}: duplicate batch asset_id: {asset_id}")
    else:
        seen_asset_ids.add(asset_id)

    missing = sorted(ASSET_REQUIRED - set(asset.keys()))
    if missing:
        errors.append(f"{rel(path)} asset {asset_id}: missing fields: {', '.join(missing)}")

    kit_asset = kit_assets.get(asset_id)
    if kit_assets and kit_asset is None:
        errors.append(f"{rel(path)} asset {asset_id}: not found in target kit manifest")

    target_file = asset.get("target_file")
    if not isinstance(target_file, str) or not target_file.startswith("assets/kits/"):
        errors.append(f"{rel(path)} asset {asset_id}: target_file must start with assets/kits/")
    elif ".." in Path(target_file).parts:
        errors.append(f"{rel(path)} asset {asset_id}: target_file must not contain '..'")

    if kit_asset is not None:
        intended_file = kit_asset.get("intended_file")
        if target_file != intended_file:
            errors.append(f"{rel(path)} asset {asset_id}: target_file must match kit intended_file {intended_file!r}")

    candidate_status = asset.get("candidate_status")
    if candidate_status not in VALID_CANDIDATE_STATUSES:
        errors.append(f"{rel(path)} asset {asset_id}: invalid candidate_status {candidate_status!r}")

    generation_prompt_addon = asset.get("generation_prompt_addon")
    if not isinstance(generation_prompt_addon, str) or len(generation_prompt_addon.strip()) < 40:
        errors.append(f"{rel(path)} asset {asset_id}: generation_prompt_addon must be a useful non-empty prompt")

    check_string_list(path, f"asset {asset_id}", "review_checks", asset.get("review_checks"), errors)

    if candidate_status == "accepted":
        if not isinstance(target_file, str) or not (ROOT / target_file).exists():
            errors.append(f"{rel(path)} asset {asset_id}: accepted target_file does not exist: {target_file}")


def main() -> int:
    errors: list[str] = []
    files = batch_files()

    if not files:
        errors.append("No asset batch manifests found under data/asset_batches/.")

    try:
        kits = kit_manifests()
    except json.JSONDecodeError as exc:
        print(f"Asset batch validation failed: invalid asset kit JSON: {exc}")
        return 1

    for path in files:
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {rel(path)}: {exc}")
            continue
        check_batch(path, data, kits, errors)

    if errors:
        print("Asset batch validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Asset batch validation passed: {len(files)} batch manifest(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
