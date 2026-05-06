#!/usr/bin/env python3
"""Smoke-test the local asset candidate promotion tool.

The test creates tiny synthetic ZIPs and promotion plans at runtime. It verifies
both supported safety modes:

1. `--dry-run` against the real checkout does not mutate the real manifest.
2. write mode against a temporary mini-repo copies the file and updates manifest
   metadata without touching the checked-out project.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROMOTE_TOOL = ROOT / "tools" / "promote_asset_candidates.py"
STARTER_MANIFEST = "data/asset_kits/wolfpine_village_starter.json"
SOURCE_IN_ZIP = "props/wolfpine_well_01.png"
INTENDED_FILE = "assets/kits/wolfpine_village/props/wolfpine_well_01.png"
ASSET_ID = "wolfpine_well_01"


def make_zip(zip_path: Path, payload: bytes) -> str:
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr(SOURCE_IN_ZIP, payload)
    return hashlib.sha256(payload).hexdigest()


def make_plan(plan_path: Path, payload_sha256: str, description: str) -> None:
    plan = {
        "id": "synthetic_asset_promotion_test",
        "description": description,
        "source_zip": plan_path.with_suffix(".zip").name,
        "status_policy": "Synthetic test uses cleaned status only.",
        "assets": [
            {
                "asset_id": ASSET_ID,
                "manifest": STARTER_MANIFEST,
                "source_in_zip": SOURCE_IN_ZIP,
                "intended_file": INTENDED_FILE,
                "status": "cleaned",
                "production_batch": "synthetic_test_batch",
                "source_file": "synthetic_source.png",
                "candidate_file": SOURCE_IN_ZIP,
                "sha256": payload_sha256,
                "production_notes": "Synthetic promotion smoke test entry; not a real production asset."
            }
        ]
    }
    plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")


def run_promoter(zip_path: Path, plan_path: Path, repo_root: Path | None = None, dry_run: bool = False) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(PROMOTE_TOOL), "--zip", str(zip_path), "--plan", str(plan_path)]
    if repo_root is not None:
        command.extend(["--repo-root", str(repo_root)])
    if dry_run:
        command.append("--dry-run")
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)


def assert_success(result: subprocess.CompletedProcess[str]) -> None:
    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        raise AssertionError(f"promotion command failed with exit code {result.returncode}")


def run_dry_run_test() -> None:
    payload = b"synthetic-ng-wolfpine-png-placeholder-dry-run\n"

    with tempfile.TemporaryDirectory(prefix="ng_asset_promotion_dry_run_") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        zip_path = temp_dir / "synthetic_candidates.zip"
        plan_path = temp_dir / "synthetic_promotion_plan.json"
        payload_sha256 = make_zip(zip_path, payload)
        make_plan(plan_path, payload_sha256, "Runtime smoke test plan for dry-run behavior.")

        before_manifest = (ROOT / STARTER_MANIFEST).read_text(encoding="utf-8")
        result = run_promoter(zip_path, plan_path, dry_run=True)
        after_manifest = (ROOT / STARTER_MANIFEST).read_text(encoding="utf-8")

    assert_success(result)
    if "Dry run passed." not in result.stdout:
        print(result.stdout, end="")
        raise AssertionError("Expected dry-run success message was not printed.")
    if before_manifest != after_manifest:
        raise AssertionError("Dry run mutated the starter manifest.")


def make_minimal_repo(temp_root: Path) -> None:
    manifest_source = ROOT / STARTER_MANIFEST
    manifest_target = temp_root / STARTER_MANIFEST
    manifest_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(manifest_source, manifest_target)


def run_write_mode_test() -> None:
    payload = b"synthetic-ng-wolfpine-png-placeholder-write-mode\n"

    with tempfile.TemporaryDirectory(prefix="ng_asset_promotion_write_") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        repo_root = temp_dir / "mini_repo"
        repo_root.mkdir()
        make_minimal_repo(repo_root)

        zip_path = temp_dir / "synthetic_candidates.zip"
        plan_path = temp_dir / "synthetic_promotion_plan.json"
        payload_sha256 = make_zip(zip_path, payload)
        make_plan(plan_path, payload_sha256, "Runtime smoke test plan for write-mode behavior.")

        result = run_promoter(zip_path, plan_path, repo_root=repo_root, dry_run=False)
        promoted_file = repo_root / INTENDED_FILE
        promoted_file_exists = promoted_file.exists()
        promoted_file_payload = promoted_file.read_bytes() if promoted_file_exists else b""
        manifest_data: dict[str, Any] = json.loads((repo_root / STARTER_MANIFEST).read_text(encoding="utf-8"))

    assert_success(result)
    if "Asset promotion complete." not in result.stdout:
        print(result.stdout, end="")
        raise AssertionError("Expected write-mode success message was not printed.")
    if not promoted_file_exists:
        raise AssertionError("Promoted file was not written inside the temporary mini-repo.")
    if promoted_file_payload != payload:
        raise AssertionError("Promoted file payload does not match ZIP source.")

    matching_assets = [asset for asset in manifest_data["assets"] if asset.get("id") == ASSET_ID]
    if len(matching_assets) != 1:
        raise AssertionError(f"Expected exactly one manifest asset for {ASSET_ID}")
    asset = matching_assets[0]
    if asset.get("status") != "cleaned":
        raise AssertionError(f"Expected status cleaned, got {asset.get('status')!r}")
    if asset.get("sha256") != payload_sha256:
        raise AssertionError("Manifest sha256 was not updated to promoted payload hash.")
    if asset.get("production_batch") != "synthetic_test_batch":
        raise AssertionError("Manifest production metadata was not updated.")


def main() -> int:
    try:
        run_dry_run_test()
        run_write_mode_test()
    except AssertionError as exc:
        print(f"Promotion tool smoke test failed: {exc}", file=sys.stderr)
        return 1

    print("Promotion tool dry-run and write-mode smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
