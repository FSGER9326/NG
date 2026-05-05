#!/usr/bin/env python3
"""Export Markdown review sheets from NG asset candidate ledgers.

Candidate ledgers live under data/asset_candidates/ and track generated/sourced
art before promotion into canonical kit files. This tool turns those JSON records
into human-reviewable checklists.

Usage:
    python tools/export_asset_candidate_review_sheets.py data/asset_candidates/wolfpine_village_candidates.json
    python tools/export_asset_candidate_review_sheets.py data/asset_candidates/wolfpine_village_modular_candidates.json

Output:
    debug/asset_candidate_reviews/<ledger_id>/<candidate_id>.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "debug" / "asset_candidate_reviews"
BATCH_ROOT = ROOT / "data" / "asset_batches"
KIT_ROOT = ROOT / "data" / "asset_kits"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def as_text_list(value: Any) -> list[str]:
    return [item for item in as_list(value) if isinstance(item, str)]


def safe_name(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"_", "-"} else "_" for char in value).strip("_")


def load_batch_index() -> dict[tuple[str, str], dict[str, Any]]:
    result: dict[tuple[str, str], dict[str, Any]] = {}
    if not BATCH_ROOT.exists():
        return result
    for path in sorted(BATCH_ROOT.glob("*.json")):
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        batch_id = str(data.get("id", path.stem))
        for asset in as_list(data.get("assets")):
            if isinstance(asset, dict) and isinstance(asset.get("asset_id"), str):
                result[(batch_id, asset["asset_id"])] = asset
    return result


def load_kit_asset_index() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not KIT_ROOT.exists():
        return result
    for path in sorted(KIT_ROOT.glob("*.json")):
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        for asset in as_list(data.get("assets")):
            if isinstance(asset, dict) and isinstance(asset.get("id"), str):
                result[asset["id"]] = asset
    return result


def checklist(items: list[str], checked: bool = False) -> str:
    box = "x" if checked else " "
    if not items:
        return "- [ ] No checklist items recorded."
    return "\n".join(f"- [{box}] {item}" for item in items)


def bullet_list(items: list[str]) -> str:
    if not items:
        return "- None recorded."
    return "\n".join(f"- {item}" for item in items)


def build_review_sheet(
    ledger: dict[str, Any],
    candidate: dict[str, Any],
    batch_assets: dict[tuple[str, str], dict[str, Any]],
    kit_assets: dict[str, dict[str, Any]],
) -> str:
    ledger_id = str(ledger.get("id", "unknown_ledger"))
    target_area = str(ledger.get("target_area", "unknown_area"))
    target_kit = str(ledger.get("target_kit", "unknown_kit"))

    asset_id = str(candidate.get("asset_id", "unknown_asset"))
    batch_id = str(candidate.get("batch_id", "unknown_batch"))
    candidate_id = str(candidate.get("candidate_id", "unknown_candidate"))
    status = str(candidate.get("status", "unknown"))
    source_type = str(candidate.get("source_type", "unknown"))
    source_notes = str(candidate.get("source_notes", ""))
    candidate_file = str(candidate.get("candidate_file", ""))
    target_file = str(candidate.get("target_file", ""))
    cleanup_notes = as_text_list(candidate.get("cleanup_notes"))
    review_notes = as_text_list(candidate.get("review_notes"))

    batch_asset = batch_assets.get((batch_id, asset_id), {})
    kit_asset = kit_assets.get(asset_id, {})
    batch_review = as_text_list(batch_asset.get("review_checks"))
    kit_acceptance = as_text_list(kit_asset.get("acceptance_checks"))
    placement_rules = as_text_list(kit_asset.get("placement_rules"))
    tags = as_text_list(kit_asset.get("tags"))

    return f"""# Asset Candidate Review: {candidate_id}

## Candidate summary

- Ledger: `{ledger_id}`
- Area: `{target_area}`
- Target kit: `{target_kit}`
- Batch: `{batch_id}`
- Asset ID: `{asset_id}`
- Candidate status: `{status}`
- Source type: `{source_type}`
- Candidate file: `{candidate_file}`
- Target file: `{target_file}`

## Source / generation notes

```text
{source_notes}
```

## Required source review

- [ ] Source type is allowed by the asset policy.
- [ ] Tool/model/date/settings or external source/license details are recorded.
- [ ] Candidate is not copied from a commercial game, franchise, or unclear source.
- [ ] Candidate can be modified and used in the project.
- [ ] Candidate file is separate from the canonical target file until promotion.

## Cleanup checklist

{checklist(cleanup_notes)}

## Candidate rejection checks

{checklist(review_notes)}

## Batch review checks

{checklist(batch_review)}

## Kit acceptance checks

{checklist(kit_acceptance)}

## Placement / usage rules

{bullet_list(placement_rules)}

## Kit tags

{bullet_list(tags)}

## Promotion decision

- [ ] Reject candidate.
- [ ] Keep candidate for revision.
- [ ] Needs cleanup before review.
- [ ] Needs second candidate for comparison.
- [ ] Accept for kit promotion.

## Reviewer notes

```text

```
"""


def export_review_sheets(ledger_path: Path, output_root: Path) -> list[Path]:
    ledger = load_json(ledger_path)
    if not isinstance(ledger, dict):
        raise ValueError(f"Ledger must be a JSON object: {ledger_path}")

    ledger_id = str(ledger.get("id", ledger_path.stem))
    output_dir = output_root / safe_name(ledger_id)
    output_dir.mkdir(parents=True, exist_ok=True)

    batch_assets = load_batch_index()
    kit_assets = load_kit_asset_index()
    exported: list[Path] = []

    for candidate in as_list(ledger.get("candidates")):
        if not isinstance(candidate, dict):
            continue
        candidate_id = str(candidate.get("candidate_id", "unknown_candidate"))
        output_path = output_dir / f"{safe_name(candidate_id)}.md"
        output_path.write_text(build_review_sheet(ledger, candidate, batch_assets, kit_assets), encoding="utf-8")
        exported.append(output_path)

    return exported


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Markdown review sheets from an NG asset candidate ledger.")
    parser.add_argument("ledger", type=Path, help="Path to asset candidate ledger JSON.")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT, help="Output root directory.")
    args = parser.parse_args()

    ledger_path = args.ledger
    if not ledger_path.is_absolute():
        ledger_path = ROOT / ledger_path
    output_root = args.output_root
    if not output_root.is_absolute():
        output_root = ROOT / output_root

    exported = export_review_sheets(ledger_path, output_root)
    print(f"Exported {len(exported)} review sheet(s) to {output_root}")
    for path in exported:
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
