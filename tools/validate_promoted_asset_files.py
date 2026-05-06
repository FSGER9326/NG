#!/usr/bin/env python3
"""Validate promoted NG asset files exist and match recorded hashes.

Asset-kit manifests may track many future/planned pieces before PNGs exist in
the repository. This validator intentionally checks only assets that have moved
to a file-backed production state:

- `cleaned`
- `accepted`

For those statuses, the asset must have:

- an `intended_file` path,
- a committed file at that path,
- a 64-character lowercase SHA256 in the manifest,
- a file hash matching the manifest value.

This keeps planned/generated candidates flexible while making real promoted art
traceable and reproducible.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSET_KIT_MANIFEST_ROOT = ROOT / "data" / "asset_kits"
FILE_BACKED_STATUSES = {"cleaned", "accepted"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def asset_kit_files() -> list[Path]:
    if not ASSET_KIT_MANIFEST_ROOT.exists():
        return []
    return sorted(ASSET_KIT_MANIFEST_ROOT.glob("*.json"))


def check_asset(path: Path, asset: dict[str, Any], errors: list[str]) -> None:
    asset_id = asset.get("id", "<missing id>")
    status = asset.get("status")
    if status not in FILE_BACKED_STATUSES:
        return

    intended_file = asset.get("intended_file")
    if not isinstance(intended_file, str) or not intended_file.strip():
        errors.append(f"{rel(path)} asset {asset_id}: {status} assets must define intended_file")
        return

    intended_path = Path(intended_file)
    if intended_path.is_absolute() or ".." in intended_path.parts:
        errors.append(f"{rel(path)} asset {asset_id}: intended_file must be a safe relative path")
        return
    if not intended_file.startswith("assets/kits/"):
        errors.append(f"{rel(path)} asset {asset_id}: intended_file must start with assets/kits/")
    if not intended_file.endswith(".png"):
        errors.append(f"{rel(path)} asset {asset_id}: intended_file must end with .png")

    repo_file = ROOT / intended_path
    if not repo_file.exists():
        errors.append(f"{rel(path)} asset {asset_id}: {status} file is missing: {intended_file}")
        return
    if not repo_file.is_file():
        errors.append(f"{rel(path)} asset {asset_id}: intended_file is not a file: {intended_file}")
        return

    expected_sha256 = asset.get("sha256")
    if not isinstance(expected_sha256, str) or not SHA256_RE.fullmatch(expected_sha256):
        errors.append(f"{rel(path)} asset {asset_id}: {status} assets must record a 64-character lowercase sha256")
        return

    actual_sha256 = sha256_file(repo_file)
    if actual_sha256 != expected_sha256:
        errors.append(
            f"{rel(path)} asset {asset_id}: sha256 mismatch for {intended_file}; "
            f"manifest has {expected_sha256}, file is {actual_sha256}"
        )


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
        print("Promoted asset file validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Promoted asset file validation passed: {len(files)} manifest(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
