#!/usr/bin/env python3
"""Export prompt cards from an NG asset-generation batch manifest.

Usage:
    python tools/export_asset_batch_prompts.py data/asset_batches/wolfpine_village_batch_01.json

Output:
    debug/asset_batch_prompts/<batch_id>/<asset_id>.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "debug" / "asset_batch_prompts"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Batch manifest must be a JSON object: {path}")
    return data


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    return []


def as_text_list(value: Any) -> list[str]:
    return [item for item in as_list(value) if isinstance(item, str)]


def safe_name(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"_", "-"} else "_" for char in value).strip("_")


def build_prompt_card(batch: dict[str, Any], asset: dict[str, Any]) -> str:
    batch_id = str(batch.get("id", "unknown_batch"))
    batch_name = str(batch.get("name", batch_id))
    target_kit = str(batch.get("target_kit", "unknown_kit"))
    target_area = str(batch.get("target_area", "unknown_area"))
    global_prompt_lock = str(batch.get("global_prompt_lock", ""))
    global_negative_prompt = str(batch.get("global_negative_prompt", ""))
    batch_acceptance_checks = as_text_list(batch.get("batch_acceptance_checks"))

    asset_id = str(asset.get("asset_id", "unknown_asset"))
    target_file = str(asset.get("target_file", ""))
    candidate_status = str(asset.get("candidate_status", "not_started"))
    prompt_addon = str(asset.get("generation_prompt_addon", ""))
    review_checks = as_text_list(asset.get("review_checks"))

    review = "\n".join(f"- [ ] {check}" for check in review_checks) or "- [ ] No review checks recorded."
    batch_acceptance = "\n".join(f"- [ ] {check}" for check in batch_acceptance_checks) or "- [ ] No batch acceptance checks recorded."

    return f"""# Batch Asset Prompt: {asset_id}

## Batch

- Batch: `{batch_id}`
- Name: {batch_name}
- Target kit: `{target_kit}`
- Target area: `{target_area}`
- Candidate status: `{candidate_status}`
- Target file: `{target_file}`

## Generation prompt

```text
Create one reusable canonical asset for the NG CRPG project.

{global_prompt_lock}

Asset ID: {asset_id}
Target file: {target_file}

Asset-specific requirements:
{prompt_addon}

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- suitable for assembly into a 1280x720 Wolfpine Village background plate
```

## Negative prompt

```text
{global_negative_prompt}
```

## Review gate

{review}

## Batch acceptance reminders

{batch_acceptance}

## Cleanup checklist

- [ ] Crop with margin.
- [ ] Clean background or mask.
- [ ] Add/normalize alpha if needed.
- [ ] Match Wolfpine color grade.
- [ ] Normalize contact shadow.
- [ ] Save candidate to target file or record rejected candidate notes.
- [ ] Record source/license/generation notes before production use.
"""


def export_prompts(batch_path: Path, output_root: Path) -> list[Path]:
    batch = load_json(batch_path)
    batch_id = str(batch.get("id", batch_path.stem))
    output_dir = output_root / safe_name(batch_id)
    output_dir.mkdir(parents=True, exist_ok=True)

    exported: list[Path] = []
    for asset in as_list(batch.get("assets")):
        if not isinstance(asset, dict):
            continue
        asset_id = str(asset.get("asset_id", "unknown_asset"))
        output_path = output_dir / f"{safe_name(asset_id)}.md"
        output_path.write_text(build_prompt_card(batch, asset), encoding="utf-8")
        exported.append(output_path)
    return exported


def main() -> int:
    parser = argparse.ArgumentParser(description="Export prompt cards from an NG asset batch manifest.")
    parser.add_argument("batch", type=Path, help="Path to asset batch manifest JSON.")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT, help="Output root directory.")
    args = parser.parse_args()

    batch_path = args.batch
    if not batch_path.is_absolute():
        batch_path = ROOT / batch_path
    output_root = args.output_root
    if not output_root.is_absolute():
        output_root = ROOT / output_root

    exported = export_prompts(batch_path, output_root)
    print(f"Exported {len(exported)} batch prompt cards to {output_root}")
    for path in exported:
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
