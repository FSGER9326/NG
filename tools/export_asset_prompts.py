#!/usr/bin/env python3
"""Export per-asset prompt cards from an NG asset-kit manifest.

Usage:
    python tools/export_asset_prompts.py data/asset_kits/wolfpine_village_starter.json

Output:
    debug/asset_prompts/<kit_id>/<priority>_<asset_id>.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "debug" / "asset_prompts"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Manifest must be a JSON object: {path}")
    return data


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    return []


def as_text_list(value: Any) -> list[str]:
    return [item for item in as_list(value) if isinstance(item, str)]


def safe_name(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"_", "-"} else "_" for char in value).strip("_")


def build_prompt_card(manifest: dict[str, Any], asset: dict[str, Any]) -> str:
    kit_id = str(manifest.get("id", "unknown_kit"))
    style_family = str(manifest.get("style_family", "unknown"))
    camera = str(manifest.get("camera", "pseudo_isometric_3_4"))
    lighting = str(manifest.get("lighting", "late_afternoon_soft"))
    display_name = str(asset.get("display_name", asset.get("id", "Unnamed Asset")))
    asset_id = str(asset.get("id", "unknown_asset"))
    category = str(asset.get("category", "unknown"))
    subcategory = str(asset.get("subcategory", "unknown"))
    scale_class = str(asset.get("scale_class", "unknown"))
    intended_file = str(asset.get("intended_file", ""))
    tags = ", ".join(as_text_list(asset.get("tags")))
    placement_rules = as_text_list(asset.get("placement_rules"))
    acceptance_checks = as_text_list(asset.get("acceptance_checks"))
    global_checks = as_text_list(manifest.get("global_acceptance_checks"))

    placement = "\n".join(f"- {rule}" for rule in placement_rules) or "- None recorded."
    acceptance = "\n".join(f"- {check}" for check in acceptance_checks) or "- None recorded."
    global_acceptance = "\n".join(f"- {check}" for check in global_checks) or "- None recorded."

    return f"""# Asset Prompt: {display_name}

## Manifest

- Kit: `{kit_id}`
- Asset ID: `{asset_id}`
- Category: `{category}` / `{subcategory}`
- Style family: `{style_family}`
- Camera: `{camera}`
- Lighting: `{lighting}`
- Scale class: `{scale_class}`
- Intended file: `{intended_file}`
- Tags: {tags or "none"}

## Generation prompt

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: {display_name}
Asset ID: {asset_id}
Category: {category}
Style family: {style_family}
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement asset, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow
Materials: dark timber, old stone, weathered plaster, moss, mud, cobble, muted natural colors as appropriate
Requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent ground plane and contact shadow
- no text, no UI
- no modern objects
- suitable for assembly into a 1280x720 village background plate
- obey the placement rules and acceptance checks below
```

## Placement rules

{placement}

## Asset acceptance checks

{acceptance}

## Global acceptance checks

{global_acceptance}

## Cleanup checklist

- [ ] Crop with margin.
- [ ] Clean background or mask.
- [ ] Add/normalize alpha if needed.
- [ ] Match Wolfpine color grade.
- [ ] Normalize contact shadow.
- [ ] Save to intended kit path or record replacement path.
- [ ] Record source/license/generation notes.
"""


def export_prompts(manifest_path: Path, output_root: Path) -> list[Path]:
    manifest = load_json(manifest_path)
    kit_id = str(manifest.get("id", manifest_path.stem))
    output_dir = output_root / safe_name(kit_id)
    output_dir.mkdir(parents=True, exist_ok=True)

    exported: list[Path] = []
    for asset in as_list(manifest.get("assets")):
        if not isinstance(asset, dict):
            continue
        asset_id = str(asset.get("id", "unknown_asset"))
        priority = asset.get("priority", 999)
        try:
            priority_number = int(priority)
        except (TypeError, ValueError):
            priority_number = 999
        filename = f"{priority_number:02d}_{safe_name(asset_id)}.md"
        output_path = output_dir / filename
        output_path.write_text(build_prompt_card(manifest, asset), encoding="utf-8")
        exported.append(output_path)
    return exported


def main() -> int:
    parser = argparse.ArgumentParser(description="Export prompt cards from an NG asset-kit manifest.")
    parser.add_argument("manifest", type=Path, help="Path to asset-kit manifest JSON.")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT, help="Output root directory.")
    args = parser.parse_args()

    manifest_path = args.manifest
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    output_root = args.output_root
    if not output_root.is_absolute():
        output_root = ROOT / output_root

    exported = export_prompts(manifest_path, output_root)
    print(f"Exported {len(exported)} prompt cards to {output_root}")
    for path in exported:
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
