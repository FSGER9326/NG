#!/usr/bin/env python3
"""Validate NG asset promotion plans.

Promotion plans describe how reviewed candidate PNGs from a local handoff ZIP
should be copied into canonical kit paths and how their manifest entries should
be updated. This validator checks the plan structure and cross-checks every
planned asset against its target asset-kit manifest without requiring the ZIP or
PNG files to be present in the repository.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSET_KIT_ROOT = ROOT / "assets" / "kits"
VALID_STATUSES = {
    "planned",
    "generated_candidate",
    "external_candidate",
    "cleaned",
    "accepted",
    "rejected",
}
REQUIRED_PLAN_FIELDS = {"id", "description", "source_zip", "status_policy", "assets"}
REQUIRED_ASSET_FIELDS = {"asset_id", "manifest", "source_in_zip", "intended_file", "status"}
OPTIONAL_STRING_FIELDS = {
    "production_batch",
    "source_file",
    "candidate_file",
    "sha256",
    "production_notes",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Unsafe repository path: {value}")
    return ROOT / path


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def plan_files() -> list[Path]:
    if not ASSET_KIT_ROOT.exists():
        return []
    return sorted(ASSET_KIT_ROOT.glob("*/FIRST_BINARY_PROMOTION_*.json"))


def check_non_empty_string(errors: list[str], path: Path, context: str, field: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{rel(path)} {context}: {field} must be a non-empty string")


def check_safe_relative_path(errors: list[str], path: Path, context: str, field: str, value: Any) -> None:
    check_non_empty_string(errors, path, context, field, value)
    if isinstance(value, str):
        value_path = Path(value)
        if value_path.is_absolute() or ".." in value_path.parts:
            errors.append(f"{rel(path)} {context}: {field} must be a safe relative path")


def manifest_asset_index(manifest_path: Path, errors: list[str], plan_path: Path) -> dict[str, dict[str, Any]]:
    if not manifest_path.exists():
        errors.append(f"{rel(plan_path)}: referenced manifest does not exist: {rel(manifest_path)}")
        return {}

    try:
        data = load_json(manifest_path)
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in referenced manifest {rel(manifest_path)}: {exc}")
        return {}

    assets = data.get("assets")
    if not isinstance(assets, list):
        errors.append(f"{rel(manifest_path)}: assets must be a list")
        return {}

    index: dict[str, dict[str, Any]] = {}
    for asset in assets:
        if isinstance(asset, dict) and isinstance(asset.get("id"), str):
            index[asset["id"]] = asset
    return index


def check_plan(path: Path, data: Any, errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append(f"{rel(path)}: promotion plan must be a JSON object")
        return

    missing = sorted(REQUIRED_PLAN_FIELDS - set(data.keys()))
    if missing:
        errors.append(f"{rel(path)}: missing fields: {', '.join(missing)}")

    for field in ("id", "description", "source_zip", "status_policy"):
        check_non_empty_string(errors, path, "plan", field, data.get(field))

    source_zip = data.get("source_zip")
    if isinstance(source_zip, str):
        if Path(source_zip).is_absolute() or ".." in Path(source_zip).parts:
            errors.append(f"{rel(path)} plan: source_zip must be a safe relative filename/path")
        if not source_zip.endswith(".zip"):
            errors.append(f"{rel(path)} plan: source_zip should end with .zip")

    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append(f"{rel(path)}: assets must be a non-empty list")
        return

    seen_ids: set[str] = set()
    seen_intended_files: set[str] = set()
    manifest_cache: dict[Path, dict[str, dict[str, Any]]] = {}

    for index, entry in enumerate(assets, start=1):
        context = f"asset #{index}"
        if not isinstance(entry, dict):
            errors.append(f"{rel(path)} {context}: must be an object")
            continue

        missing_entry = sorted(REQUIRED_ASSET_FIELDS - set(entry.keys()))
        if missing_entry:
            errors.append(f"{rel(path)} {context}: missing fields: {', '.join(missing_entry)}")

        asset_id = entry.get("asset_id")
        if isinstance(asset_id, str) and asset_id.strip():
            context = f"asset {asset_id}"
            if asset_id in seen_ids:
                errors.append(f"{rel(path)} {context}: duplicate asset_id")
            seen_ids.add(asset_id)
        else:
            check_non_empty_string(errors, path, context, "asset_id", asset_id)
            asset_id = f"#{index}"

        for field in ("manifest", "source_in_zip", "intended_file"):
            check_safe_relative_path(errors, path, context, field, entry.get(field))

        status = entry.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{rel(path)} {context}: invalid status {status!r}")
        if status == "accepted":
            errors.append(f"{rel(path)} {context}: promotion plans should not pre-mark assets as accepted")

        for field in OPTIONAL_STRING_FIELDS:
            if field in entry and (not isinstance(entry[field], str) or not entry[field].strip()):
                errors.append(f"{rel(path)} {context}: {field} must be a non-empty string when present")

        sha256 = entry.get("sha256")
        if sha256 is not None and (not isinstance(sha256, str) or not SHA256_RE.fullmatch(sha256)):
            errors.append(f"{rel(path)} {context}: sha256 must be 64 lowercase hex characters")

        intended_file = entry.get("intended_file")
        if isinstance(intended_file, str):
            if not intended_file.startswith("assets/kits/"):
                errors.append(f"{rel(path)} {context}: intended_file must start with assets/kits/")
            if not intended_file.endswith(".png"):
                errors.append(f"{rel(path)} {context}: intended_file must end with .png")
            if intended_file in seen_intended_files:
                errors.append(f"{rel(path)} {context}: duplicate intended_file {intended_file}")
            seen_intended_files.add(intended_file)

        source_in_zip = entry.get("source_in_zip")
        if isinstance(source_in_zip, str) and not source_in_zip.endswith(".png"):
            errors.append(f"{rel(path)} {context}: source_in_zip must end with .png")

        manifest_value = entry.get("manifest")
        if not isinstance(manifest_value, str) or not isinstance(asset_id, str):
            continue
        try:
            manifest_path = repo_path(manifest_value)
        except ValueError as exc:
            errors.append(f"{rel(path)} {context}: {exc}")
            continue

        if manifest_path not in manifest_cache:
            manifest_cache[manifest_path] = manifest_asset_index(manifest_path, errors, path)
        manifest_assets = manifest_cache[manifest_path]
        manifest_asset = manifest_assets.get(asset_id)
        if manifest_asset is None:
            errors.append(f"{rel(path)} {context}: asset_id not found in {rel(manifest_path)}")
            continue

        if isinstance(intended_file, str) and manifest_asset.get("intended_file") != intended_file:
            errors.append(
                f"{rel(path)} {context}: intended_file does not match {rel(manifest_path)} "
                f"({manifest_asset.get('intended_file')!r})"
            )


def main() -> int:
    errors: list[str] = []
    files = plan_files()

    for path in files:
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {rel(path)}: {exc}")
            continue
        check_plan(path, data, errors)

    if errors:
        print("Asset promotion plan validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Asset promotion plan validation passed: {len(files)} plan(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
