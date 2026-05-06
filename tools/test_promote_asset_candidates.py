#!/usr/bin/env python3
"""Smoke-test the local asset candidate promotion tool.

This test creates a tiny synthetic ZIP and promotion plan at runtime, then runs
`tools/promote_asset_candidates.py --dry-run` against an existing Wolfpine
manifest entry. It proves the dry-run path verifies ZIP membership, SHA256,
manifest lookup, and intended-file matching without writing PNGs or mutating the
manifest.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMOTE_TOOL = ROOT / "tools" / "promote_asset_candidates.py"
STARTER_MANIFEST = "data/asset_kits/wolfpine_village_starter.json"
SOURCE_IN_ZIP = "props/wolfpine_well_01.png"
INTENDED_FILE = "assets/kits/wolfpine_village/props/wolfpine_well_01.png"


def main() -> int:
    payload = b"synthetic-ng-wolfpine-png-placeholder\n"
    payload_sha256 = hashlib.sha256(payload).hexdigest()

    with tempfile.TemporaryDirectory(prefix="ng_asset_promotion_test_") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        zip_path = temp_dir / "synthetic_candidates.zip"
        plan_path = temp_dir / "synthetic_promotion_plan.json"

        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.writestr(SOURCE_IN_ZIP, payload)

        plan = {
            "id": "synthetic_asset_promotion_dry_run",
            "description": "Runtime smoke test plan for promote_asset_candidates.py dry-run behavior.",
            "source_zip": zip_path.name,
            "status_policy": "Smoke test uses cleaned status only and must not write files.",
            "assets": [
                {
                    "asset_id": "wolfpine_well_01",
                    "manifest": STARTER_MANIFEST,
                    "source_in_zip": SOURCE_IN_ZIP,
                    "intended_file": INTENDED_FILE,
                    "status": "cleaned",
                    "production_batch": "synthetic_test_batch",
                    "source_file": "synthetic_source.png",
                    "candidate_file": SOURCE_IN_ZIP,
                    "sha256": payload_sha256,
                    "production_notes": "Synthetic dry-run smoke test entry; not a real production asset."
                }
            ]
        }
        plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")

        before_manifest = (ROOT / STARTER_MANIFEST).read_text(encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(PROMOTE_TOOL),
                "--zip",
                str(zip_path),
                "--plan",
                str(plan_path),
                "--dry-run",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        after_manifest = (ROOT / STARTER_MANIFEST).read_text(encoding="utf-8")

    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        return result.returncode

    if "Dry run passed." not in result.stdout:
        print(result.stdout, end="")
        print("Expected dry-run success message was not printed.", file=sys.stderr)
        return 1

    if before_manifest != after_manifest:
        print("Dry run mutated the starter manifest.", file=sys.stderr)
        return 1

    print("Promotion tool dry-run smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
