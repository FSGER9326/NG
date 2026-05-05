#!/usr/bin/env python3
"""Validate the local asset evaluation candidate manifest."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "asset_eval" / "asset_candidates.json"
SAFE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_\-]*$")
KNOWN_DOWNLOAD_MODES = {
    "manual_or_page",
    "manual_review_required",
    "direct",
}
KNOWN_LICENSES = {
    "CC0-1.0",
    "MIT",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "Apache-2.0",
    "mixed_cc0_pool",
    "mixed_open_source_pool",
    "custom",
    "unknown",
}

REQUIRED_FIELDS = {
    "id",
    "name",
    "source",
    "source_page_url",
    "license",
    "category",
    "expected_use",
    "download_mode",
    "priority",
    "final_art_candidate",
}


def main() -> int:
    errors: list[str] = []
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"asset eval manifest missing: {MANIFEST.relative_to(ROOT)}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"asset eval manifest invalid JSON: {exc}")
        return 1

    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if manifest.get("local_download_dir") != "asset_eval/downloads":
        errors.append("local_download_dir should be asset_eval/downloads")
    if manifest.get("local_extract_dir") != "asset_eval/extracted":
        errors.append("local_extract_dir should be asset_eval/extracted")

    candidates = manifest.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        errors.append("candidates must be a non-empty list")
    else:
        _validate_candidates(candidates, errors)

    if errors:
        print("Asset evaluation manifest validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Asset evaluation manifest validation passed: {len(candidates)} candidates")
    return 0


def _validate_candidates(candidates: list[Any], errors: list[str]) -> None:
    seen_ids: set[str] = set()
    for index, item in enumerate(candidates):
        prefix = f"candidate[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(REQUIRED_FIELDS - set(item.keys()))
        if missing:
            errors.append(f"{prefix} missing required fields: {', '.join(missing)}")
        candidate_id = str(item.get("id", ""))
        if not SAFE_ID_PATTERN.match(candidate_id):
            errors.append(f"{prefix} has unsafe id: {candidate_id!r}")
        if candidate_id in seen_ids:
            errors.append(f"duplicate candidate id: {candidate_id}")
        seen_ids.add(candidate_id)

        source_page_url = str(item.get("source_page_url", ""))
        if not source_page_url.startswith("https://"):
            errors.append(f"{candidate_id}: source_page_url must be https://")

        license_id = str(item.get("license", ""))
        if license_id not in KNOWN_LICENSES:
            errors.append(f"{candidate_id}: unexpected license id: {license_id}")

        mode = str(item.get("download_mode", ""))
        if mode not in KNOWN_DOWNLOAD_MODES:
            errors.append(f"{candidate_id}: unexpected download_mode: {mode}")
        direct_url = str(item.get("direct_download_url", ""))
        if mode == "direct" and not direct_url.startswith("https://"):
            errors.append(f"{candidate_id}: direct mode requires https direct_download_url")
        if direct_url and not direct_url.startswith("https://"):
            errors.append(f"{candidate_id}: direct_download_url must be https:// when present")

        priority = item.get("priority")
        if not isinstance(priority, int) or priority < 1 or priority > 5:
            errors.append(f"{candidate_id}: priority must be an integer from 1 to 5")
        if not isinstance(item.get("final_art_candidate"), bool):
            errors.append(f"{candidate_id}: final_art_candidate must be boolean")


if __name__ == "__main__":
    raise SystemExit(main())
