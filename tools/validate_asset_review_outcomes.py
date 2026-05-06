#!/usr/bin/env python3
"""Validate NG asset review outcome files and accepted-asset gating.

Review gates define what must be checked before an asset can move from
`cleaned` to `accepted`. Review outcome files record the actual decision.

This validator supports two modes:

1. Validate any JSON files present in `data/asset_review_outcomes/*.json`.
2. Ensure every asset currently marked `accepted` in `data/asset_kits/*.json`
   has a matching review outcome with `outcome: accepted`.

If there are no accepted assets and no outcome files yet, the validator passes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSET_KIT_ROOT = ROOT / "data" / "asset_kits"
ASSET_REVIEW_ROOT = ROOT / "data" / "asset_reviews"
ASSET_REVIEW_OUTCOME_ROOT = ROOT / "data" / "asset_review_outcomes"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
VALID_OUTCOMES = {"cleaned", "accepted", "rejected"}
REQUIRED_TOP_LEVEL = {
    "id",
    "review_gate",
    "reviewed_at",
    "reviewer",
    "target_manifest",
    "assets",
}
REQUIRED_ASSET_FIELDS = {
    "asset_id",
    "intended_file",
    "expected_sha256",
    "outcome",
    "summary",
    "checks_passed",
    "issues",
    "followups",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def safe_repo_path(value: str) -> Path | None:
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    return ROOT / candidate


def check_string(errors: list[str], path: Path, context: str, field: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{rel(path)} {context}: {field} must be a non-empty string")


def check_string_list(errors: list[str], path: Path, context: str, field: str, value: Any) -> None:
    if not isinstance(value, list):
        errors.append(f"{rel(path)} {context}: {field} must be a list")
        return
    for index, item in enumerate(value, start=1):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{rel(path)} {context}: {field}[{index}] must be a non-empty string")


def asset_kit_files() -> list[Path]:
    if not ASSET_KIT_ROOT.exists():
        return []
    return sorted(ASSET_KIT_ROOT.glob("*.json"))


def outcome_files() -> list[Path]:
    if not ASSET_REVIEW_OUTCOME_ROOT.exists():
        return []
    return sorted(ASSET_REVIEW_OUTCOME_ROOT.glob("*.json"))


def accepted_assets_from_manifests(errors: list[str]) -> dict[str, dict[str, str]]:
    accepted: dict[str, dict[str, str]] = {}
    for manifest_path in asset_kit_files():
        try:
            data = load_json(manifest_path)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {rel(manifest_path)}: {exc}")
            continue
        assets = data.get("assets") if isinstance(data, dict) else None
        if not isinstance(assets, list):
            continue
        for asset in assets:
            if not isinstance(asset, dict) or asset.get("status") != "accepted":
                continue
            asset_id = asset.get("id")
            intended_file = asset.get("intended_file")
            sha256 = asset.get("sha256")
            if not isinstance(asset_id, str) or not isinstance(intended_file, str):
                continue
            accepted[asset_id] = {
                "manifest": rel(manifest_path),
                "intended_file": intended_file,
                "sha256": sha256 if isinstance(sha256, str) else "",
            }
    return accepted


def review_gate_assets(review_gate_path: Path, errors: list[str], outcome_path: Path) -> dict[str, dict[str, Any]]:
    if not review_gate_path.exists():
        errors.append(f"{rel(outcome_path)}: review_gate does not exist: {rel(review_gate_path)}")
        return {}
    try:
        data = load_json(review_gate_path)
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in review gate {rel(review_gate_path)}: {exc}")
        return {}
    assets = data.get("assets") if isinstance(data, dict) else None
    if not isinstance(assets, list):
        errors.append(f"{rel(review_gate_path)}: assets must be a list")
        return {}
    return {asset["asset_id"]: asset for asset in assets if isinstance(asset, dict) and isinstance(asset.get("asset_id"), str)}


def check_outcome_file(path: Path, data: Any, errors: list[str]) -> dict[str, str]:
    accepted_outcomes: dict[str, str] = {}
    if not isinstance(data, dict):
        errors.append(f"{rel(path)}: outcome file must be a JSON object")
        return accepted_outcomes

    missing = sorted(REQUIRED_TOP_LEVEL - set(data.keys()))
    if missing:
        errors.append(f"{rel(path)}: missing top-level fields: {', '.join(missing)}")

    for field in ("id", "review_gate", "reviewed_at", "reviewer", "target_manifest"):
        check_string(errors, path, "outcome", field, data.get(field))

    review_assets: dict[str, dict[str, Any]] = {}
    review_gate_value = data.get("review_gate")
    if isinstance(review_gate_value, str):
        review_gate_path = safe_repo_path(review_gate_value)
        if review_gate_path is None:
            errors.append(f"{rel(path)} outcome: review_gate must be a safe relative path")
        else:
            if not review_gate_value.startswith("data/asset_reviews/"):
                errors.append(f"{rel(path)} outcome: review_gate must be under data/asset_reviews/")
            review_assets = review_gate_assets(review_gate_path, errors, path)

    target_manifest_value = data.get("target_manifest")
    if isinstance(target_manifest_value, str):
        target_manifest_path = safe_repo_path(target_manifest_value)
        if target_manifest_path is None:
            errors.append(f"{rel(path)} outcome: target_manifest must be a safe relative path")
        elif not target_manifest_path.exists():
            errors.append(f"{rel(path)} outcome: target_manifest does not exist: {target_manifest_value}")

    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append(f"{rel(path)} outcome: assets must be a non-empty list")
        return accepted_outcomes

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
            gate_asset = review_assets.get(asset_id)
            if review_assets and gate_asset is None:
                errors.append(f"{rel(path)} {context}: asset_id not present in review_gate")
            elif gate_asset is not None:
                if asset.get("intended_file") != gate_asset.get("intended_file"):
                    errors.append(f"{rel(path)} {context}: intended_file does not match review_gate")
                if asset.get("expected_sha256") != gate_asset.get("expected_sha256"):
                    errors.append(f"{rel(path)} {context}: expected_sha256 does not match review_gate")
        intended_file = asset.get("intended_file")
        if not isinstance(intended_file, str) or not intended_file.endswith(".png"):
            errors.append(f"{rel(path)} {context}: intended_file must be a .png path")
        expected_sha = asset.get("expected_sha256")
        if not isinstance(expected_sha, str) or not SHA256_RE.fullmatch(expected_sha):
            errors.append(f"{rel(path)} {context}: expected_sha256 must be 64 lowercase hex characters")
        outcome = asset.get("outcome")
        if outcome not in VALID_OUTCOMES:
            errors.append(f"{rel(path)} {context}: invalid outcome {outcome!r}")
        if outcome == "accepted" and isinstance(asset_id, str):
            accepted_outcomes[asset_id] = rel(path)
        check_string(errors, path, context, "summary", asset.get("summary"))
        checks_passed = asset.get("checks_passed")
        if not isinstance(checks_passed, bool):
            errors.append(f"{rel(path)} {context}: checks_passed must be boolean")
        if outcome == "accepted" and checks_passed is not True:
            errors.append(f"{rel(path)} {context}: accepted outcome requires checks_passed true")
        check_string_list(errors, path, context, "issues", asset.get("issues"))
        check_string_list(errors, path, context, "followups", asset.get("followups"))
    return accepted_outcomes


def main() -> int:
    errors: list[str] = []
    accepted_assets = accepted_assets_from_manifests(errors)
    accepted_outcomes: dict[str, str] = {}

    for path in outcome_files():
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {rel(path)}: {exc}")
            continue
        accepted_outcomes.update(check_outcome_file(path, data, errors))

    for asset_id, manifest_info in sorted(accepted_assets.items()):
        if asset_id not in accepted_outcomes:
            errors.append(
                f"{manifest_info['manifest']} asset {asset_id}: accepted asset requires "
                "a matching accepted review outcome in data/asset_review_outcomes/"
            )

    if errors:
        print("Asset review outcome validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(
        f"Asset review outcome validation passed: {len(outcome_files())} outcome file(s), "
        f"{len(accepted_assets)} accepted asset(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
