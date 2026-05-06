#!/usr/bin/env python3
"""Validate NG asset review gate files.

Asset review files are data-driven visual/layout gates used after candidate art is
promoted to `cleaned` and before any asset can be moved to `accepted`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSET_REVIEW_ROOT = ROOT / "data" / "asset_reviews"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_TOP_LEVEL = {
    "id",
    "name",
    "purpose",
    "target_area",
    "source_bundle",
    "required_manifest",
    "required_status_before_review",
    "allowed_status_after_review",
    "review_context",
    "global_review_checks",
    "assets",
    "review_outcomes",
}
REQUIRED_ASSET_FIELDS = {
    "asset_id",
    "intended_file",
    "expected_sha256",
    "recommended_layer",
    "recommended_use",
    "specific_review_checks",
    "accepted_only_if",
}
VALID_REVIEW_STATUSES = {"cleaned", "accepted", "rejected"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def review_files() -> list[Path]:
    if not ASSET_REVIEW_ROOT.exists():
        return []
    return sorted(ASSET_REVIEW_ROOT.glob("*.json"))


def check_string(errors: list[str], path: Path, context: str, field: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{rel(path)} {context}: {field} must be a non-empty string")


def check_string_list(errors: list[str], path: Path, context: str, field: str, value: Any, *, min_items: int = 1) -> None:
    if not isinstance(value, list) or len(value) < min_items:
        errors.append(f"{rel(path)} {context}: {field} must be a list with at least {min_items} item(s)")
        return
    for index, item in enumerate(value, start=1):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{rel(path)} {context}: {field}[{index}] must be a non-empty string")


def check_safe_path(errors: list[str], path: Path, context: str, field: str, value: Any) -> None:
    check_string(errors, path, context, field, value)
    if not isinstance(value, str):
        return
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        errors.append(f"{rel(path)} {context}: {field} must be a safe relative path")


def asset_index_from_manifest(manifest_path: Path, errors: list[str], review_path: Path) -> dict[str, dict[str, Any]]:
    if not manifest_path.exists():
        errors.append(f"{rel(review_path)}: required_manifest does not exist: {rel(manifest_path)}")
        return {}
    try:
        data = load_json(manifest_path)
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in required manifest {rel(manifest_path)}: {exc}")
        return {}
    assets = data.get("assets") if isinstance(data, dict) else None
    if not isinstance(assets, list):
        errors.append(f"{rel(manifest_path)}: assets must be a list")
        return {}
    return {asset["id"]: asset for asset in assets if isinstance(asset, dict) and isinstance(asset.get("id"), str)}


def check_review(path: Path, data: Any, errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append(f"{rel(path)}: review file must be a JSON object")
        return

    missing = sorted(REQUIRED_TOP_LEVEL - set(data.keys()))
    if missing:
        errors.append(f"{rel(path)}: missing top-level fields: {', '.join(missing)}")

    for field in ("id", "name", "purpose", "target_area", "source_bundle", "required_status_before_review"):
        check_string(errors, path, "review", field, data.get(field))
    check_safe_path(errors, path, "review", "required_manifest", data.get("required_manifest"))
    if isinstance(data.get("source_bundle"), str) and not data["source_bundle"].endswith(".zip"):
        errors.append(f"{rel(path)} review: source_bundle should end with .zip")

    if data.get("required_status_before_review") != "cleaned":
        errors.append(f"{rel(path)} review: required_status_before_review must currently be 'cleaned'")

    allowed_statuses = data.get("allowed_status_after_review")
    if not isinstance(allowed_statuses, list) or not allowed_statuses:
        errors.append(f"{rel(path)} review: allowed_status_after_review must be a non-empty list")
    else:
        for status in allowed_statuses:
            if status not in VALID_REVIEW_STATUSES:
                errors.append(f"{rel(path)} review: invalid allowed status {status!r}")

    review_context = data.get("review_context")
    if not isinstance(review_context, dict):
        errors.append(f"{rel(path)} review: review_context must be an object")
    else:
        for field in ("camera", "renderer_target", "style_family"):
            check_string(errors, path, "review_context", field, review_context.get(field))
        check_string_list(errors, path, "review_context", "backgrounds", review_context.get("backgrounds"))
        check_string_list(errors, path, "review_context", "scale_checks", review_context.get("scale_checks"))

    check_string_list(errors, path, "review", "global_review_checks", data.get("global_review_checks"), min_items=3)

    review_outcomes = data.get("review_outcomes")
    if not isinstance(review_outcomes, dict):
        errors.append(f"{rel(path)} review: review_outcomes must be an object")
    else:
        for status in VALID_REVIEW_STATUSES:
            check_string(errors, path, "review_outcomes", status, review_outcomes.get(status))

    manifest_assets: dict[str, dict[str, Any]] = {}
    if isinstance(data.get("required_manifest"), str):
        try:
            manifest_assets = asset_index_from_manifest(ROOT / data["required_manifest"], errors, path)
        except ValueError:
            manifest_assets = {}

    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append(f"{rel(path)} review: assets must be a non-empty list")
        return

    seen_ids: set[str] = set()
    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            errors.append(f"{rel(path)} asset #{index}: must be an object")
            continue
        asset_id = asset.get("asset_id")
        context = f"asset {asset_id}" if isinstance(asset_id, str) and asset_id else f"asset #{index}"
        missing_asset = sorted(REQUIRED_ASSET_FIELDS - set(asset.keys()))
        if missing_asset:
            errors.append(f"{rel(path)} {context}: missing fields: {', '.join(missing_asset)}")
        check_string(errors, path, context, "asset_id", asset_id)
        if isinstance(asset_id, str):
            if asset_id in seen_ids:
                errors.append(f"{rel(path)} {context}: duplicate asset_id")
            seen_ids.add(asset_id)
            manifest_asset = manifest_assets.get(asset_id)
            if manifest_assets and manifest_asset is None:
                errors.append(f"{rel(path)} {context}: asset_id not found in required_manifest")
            elif manifest_asset is not None and asset.get("intended_file") != manifest_asset.get("intended_file"):
                errors.append(f"{rel(path)} {context}: intended_file does not match required_manifest")
        check_safe_path(errors, path, context, "intended_file", asset.get("intended_file"))
        if isinstance(asset.get("intended_file"), str) and not asset["intended_file"].endswith(".png"):
            errors.append(f"{rel(path)} {context}: intended_file must end with .png")
        expected_sha = asset.get("expected_sha256")
        if not isinstance(expected_sha, str) or not SHA256_RE.fullmatch(expected_sha):
            errors.append(f"{rel(path)} {context}: expected_sha256 must be 64 lowercase hex characters")
        check_string(errors, path, context, "recommended_layer", asset.get("recommended_layer"))
        check_string(errors, path, context, "recommended_use", asset.get("recommended_use"))
        check_string_list(errors, path, context, "specific_review_checks", asset.get("specific_review_checks"), min_items=3)
        check_string_list(errors, path, context, "accepted_only_if", asset.get("accepted_only_if"), min_items=1)


def main() -> int:
    errors: list[str] = []
    files = review_files()
    for path in files:
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {rel(path)}: {exc}")
            continue
        check_review(path, data, errors)

    if errors:
        print("Asset review validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"Asset review validation passed: {len(files)} review file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
