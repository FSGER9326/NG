#!/usr/bin/env python3
"""Promote reviewed asset candidates from a handoff ZIP into NG kit paths.

This tool is intentionally local-first: it copies selected PNGs from a reviewed
handoff package into canonical `assets/kits/...` paths and updates the relevant
asset-kit manifest statuses/production notes. It avoids marking anything
`accepted` unless the requested file is actually present after extraction.

Example:
    python tools/promote_asset_candidates.py \
        --zip ng_wolfpine_production_batch_2026_05_06.zip \
        --plan assets/kits/wolfpine_village/FIRST_BINARY_PROMOTION_2026_05_06.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
VALID_STATUSES = {
    "planned",
    "generated_candidate",
    "external_candidate",
    "cleaned",
    "accepted",
    "rejected",
}
REQUIRED_PLAN_FIELDS = {"asset_id", "manifest", "source_in_zip", "intended_file", "status"}
OPTIONAL_ASSET_FIELDS = {
    "production_batch",
    "source_file",
    "candidate_file",
    "sha256",
    "production_notes",
}


def repo_path(root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Unsafe repository path: {value}")
    return root / path


def rel(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_plan_entry(entry: Any, index: int) -> dict[str, Any]:
    if not isinstance(entry, dict):
        raise ValueError(f"Plan asset #{index} must be an object")

    missing = sorted(REQUIRED_PLAN_FIELDS - set(entry.keys()))
    if missing:
        raise ValueError(f"Plan asset #{index} missing fields: {', '.join(missing)}")

    for field in REQUIRED_PLAN_FIELDS:
        if not isinstance(entry[field], str) or not entry[field].strip():
            raise ValueError(f"Plan asset #{index} field {field} must be a non-empty string")

    if entry["status"] not in VALID_STATUSES:
        raise ValueError(f"Plan asset {entry['asset_id']}: invalid status {entry['status']!r}")

    return entry


def load_plan(plan_path: Path) -> dict[str, Any]:
    data = load_json(plan_path)
    if not isinstance(data, dict):
        raise ValueError("Promotion plan must be a JSON object")
    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ValueError("Promotion plan must contain a non-empty assets list")
    data["assets"] = [validate_plan_entry(entry, index) for index, entry in enumerate(assets, start=1)]
    return data


def copy_from_zip(zip_path: Path, source_in_zip: str, target: Path, dry_run: bool) -> str:
    if Path(source_in_zip).is_absolute() or ".." in Path(source_in_zip).parts:
        raise ValueError(f"Unsafe ZIP source path: {source_in_zip}")

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        if source_in_zip not in names:
            raise FileNotFoundError(f"ZIP member not found: {source_in_zip}")
        if dry_run:
            with archive.open(source_in_zip) as handle:
                digest = hashlib.sha256(handle.read()).hexdigest()
            return digest

        target.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(source_in_zip) as source, target.open("wb") as destination:
            shutil.copyfileobj(source, destination)

    return sha256_file(target)


def update_manifest(root: Path, manifest_path: Path, entry: dict[str, Any], actual_sha256: str, dry_run: bool) -> bool:
    data = load_json(manifest_path)
    assets = data.get("assets")
    if not isinstance(assets, list):
        raise ValueError(f"{rel(root, manifest_path)}: assets must be a list")

    asset_id = entry["asset_id"]
    target_asset = None
    for asset in assets:
        if isinstance(asset, dict) and asset.get("id") == asset_id:
            target_asset = asset
            break

    if target_asset is None:
        raise ValueError(f"{rel(root, manifest_path)}: asset id not found: {asset_id}")

    intended_file = entry["intended_file"]
    if target_asset.get("intended_file") != intended_file:
        raise ValueError(
            f"{rel(root, manifest_path)} asset {asset_id}: intended_file mismatch; "
            f"manifest has {target_asset.get('intended_file')!r}, plan has {intended_file!r}"
        )

    if entry["status"] == "accepted" and not repo_path(root, intended_file).exists() and not dry_run:
        raise ValueError(f"Refusing to mark accepted before file exists: {intended_file}")

    target_asset["status"] = entry["status"]
    target_asset["sha256"] = actual_sha256
    for field in OPTIONAL_ASSET_FIELDS:
        if field in entry and isinstance(entry[field], str) and entry[field].strip():
            target_asset[field] = entry[field]

    if not dry_run:
        write_json(manifest_path, data)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", required=True, dest="zip_path", help="Candidate handoff ZIP path")
    parser.add_argument("--plan", required=True, dest="plan_path", help="Promotion plan JSON path")
    parser.add_argument("--dry-run", action="store_true", help="Validate and report without writing files")
    parser.add_argument(
        "--repo-root",
        default=str(DEFAULT_ROOT),
        help="Repository root to update. Defaults to the project root; tests may point this at a temporary mini-repo.",
    )
    args = parser.parse_args()

    root = Path(args.repo_root).expanduser().resolve()
    zip_path = Path(args.zip_path).expanduser().resolve()
    plan_path = repo_path(root, args.plan_path) if not Path(args.plan_path).is_absolute() else Path(args.plan_path)

    if not root.exists():
        print(f"Repository root does not exist: {root}", file=sys.stderr)
        return 1
    if not zip_path.exists():
        print(f"Candidate ZIP does not exist: {zip_path}", file=sys.stderr)
        return 1
    if not plan_path.exists():
        print(f"Promotion plan does not exist: {plan_path}", file=sys.stderr)
        return 1

    try:
        plan = load_plan(plan_path)
        print(f"Promoting asset candidates from {zip_path}")
        print(f"Using plan {rel(root, plan_path) if plan_path.is_relative_to(root) else plan_path}")

        for entry in plan["assets"]:
            intended_file = repo_path(root, entry["intended_file"])
            actual_sha256 = copy_from_zip(zip_path, entry["source_in_zip"], intended_file, args.dry_run)
            expected_sha256 = entry.get("sha256")
            if isinstance(expected_sha256, str) and expected_sha256 and expected_sha256 != actual_sha256:
                raise ValueError(
                    f"{entry['asset_id']}: SHA256 mismatch; plan has {expected_sha256}, ZIP produced {actual_sha256}"
                )
            update_manifest(root, repo_path(root, entry["manifest"]), entry, actual_sha256, args.dry_run)
            action = "Would promote" if args.dry_run else "Promoted"
            print(f"{action} {entry['asset_id']} -> {entry['intended_file']} [{entry['status']}]")

    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"Asset promotion failed: {exc}", file=sys.stderr)
        return 1

    print("Asset promotion complete." if not args.dry_run else "Dry run passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
