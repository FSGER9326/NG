#!/usr/bin/env python3
"""Validate an asset handoff ZIP against a promotion plan.

This is a local preflight check for binary art handoffs. It verifies that every
`source_in_zip` member listed in a promotion plan exists in the ZIP and that its
SHA256 matches the plan. It does not write files or update manifests.

Example:
    python tools/validate_asset_handoff_zip.py \
        --zip ng_wolfpine_first_promotion_optimized.zip \
        --plan assets/kits/wolfpine_village/FIRST_BINARY_PROMOTION_2026_05_06.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Unsafe repository path: {value}")
    return ROOT / path


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_zip_member(archive: zipfile.ZipFile, member: str) -> str:
    digest = hashlib.sha256()
    with archive.open(member) as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_member_path(value: Any, asset_id: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{asset_id}: source_in_zip must be a non-empty string")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{asset_id}: source_in_zip must be a safe relative ZIP path")
    if not value.endswith(".png"):
        raise ValueError(f"{asset_id}: source_in_zip must end with .png")
    return value


def validate_plan_asset(asset: Any, index: int) -> dict[str, str]:
    if not isinstance(asset, dict):
        raise ValueError(f"Plan asset #{index} must be an object")
    asset_id = asset.get("asset_id")
    if not isinstance(asset_id, str) or not asset_id.strip():
        raise ValueError(f"Plan asset #{index}: asset_id must be a non-empty string")
    source_in_zip = validate_member_path(asset.get("source_in_zip"), asset_id)
    expected_sha256 = asset.get("sha256")
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64 or expected_sha256.lower() != expected_sha256:
        raise ValueError(f"{asset_id}: sha256 must be 64 lowercase hex characters")
    int(expected_sha256, 16)
    return {
        "asset_id": asset_id,
        "source_in_zip": source_in_zip,
        "sha256": expected_sha256,
    }


def validate(zip_path: Path, plan_path: Path) -> list[str]:
    plan = load_json(plan_path)
    assets = plan.get("assets") if isinstance(plan, dict) else None
    if not isinstance(assets, list) or not assets:
        raise ValueError("Promotion plan must contain a non-empty assets list")

    expected_assets = [validate_plan_asset(asset, index) for index, asset in enumerate(assets, start=1)]
    messages: list[str] = []

    with zipfile.ZipFile(zip_path) as archive:
        zip_names = set(archive.namelist())
        expected_names = {asset["source_in_zip"] for asset in expected_assets}
        missing = sorted(expected_names - zip_names)
        if missing:
            raise ValueError("ZIP is missing expected member(s): " + ", ".join(missing))

        for asset in expected_assets:
            actual_sha256 = sha256_zip_member(archive, asset["source_in_zip"])
            if actual_sha256 != asset["sha256"]:
                raise ValueError(
                    f"{asset['asset_id']}: sha256 mismatch for {asset['source_in_zip']}; "
                    f"plan has {asset['sha256']}, ZIP has {actual_sha256}"
                )
            messages.append(f"{asset['asset_id']}: {asset['source_in_zip']} {actual_sha256}")

    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", required=True, dest="zip_path", help="Local handoff ZIP to validate")
    parser.add_argument("--plan", required=True, dest="plan_path", help="Promotion plan JSON path")
    args = parser.parse_args()

    zip_path = Path(args.zip_path).expanduser().resolve()
    plan_path = repo_path(args.plan_path) if not Path(args.plan_path).is_absolute() else Path(args.plan_path)

    if not zip_path.exists():
        print(f"Handoff ZIP does not exist: {zip_path}", file=sys.stderr)
        return 1
    if not plan_path.exists():
        print(f"Promotion plan does not exist: {plan_path}", file=sys.stderr)
        return 1

    try:
        messages = validate(zip_path, plan_path)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"Asset handoff ZIP validation failed: {exc}", file=sys.stderr)
        return 1

    for message in messages:
        print(message)
    print(f"Asset handoff ZIP validation passed: {len(messages)} asset(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
