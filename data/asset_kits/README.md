# Asset Kit Manifests

Asset kit manifests describe reusable art assets before they are generated, sourced, cleaned, or imported.

The goal is to make NG art production data-driven, reviewable, and repeatable. A kit manifest is not the final art; it is the source of truth for what assets should exist, where they should live, how they can be used, and what checks they must pass before becoming canonical project assets.

## Current manifests

```text
data/asset_kits/wolfpine_village_starter.json
```

## Manifest purpose

A manifest should answer:

- What reusable assets belong to this style family?
- What category and folder should each asset use?
- Which assets are highest priority?
- What placement rules prevent bad level design?
- What acceptance checks prevent unusable or inconsistent assets?
- What source/licensing policy applies?

## Required top-level fields

```json
{
  "id": "wolfpine_village_starter_kit",
  "name": "Wolfpine Village Starter Kit",
  "style_family": "wolfpine",
  "version": 1,
  "purpose": "...",
  "camera": "pseudo_isometric_3_4",
  "lighting": "late_afternoon_soft",
  "target_area": "wolfpine_village",
  "source_policy": {},
  "global_acceptance_checks": [],
  "assets": []
}
```

## Required per-asset fields

```json
{
  "id": "wolfpine_well_01",
  "display_name": "Stone Village Well",
  "category": "props",
  "subcategory": "village_core",
  "asset_type": "canonical_modular",
  "priority": 4,
  "status": "planned",
  "intended_file": "assets/kits/wolfpine_village/props/wolfpine_well_01.png",
  "scale_class": "medium_prop",
  "tags": ["well", "stone", "village"],
  "placement_rules": [],
  "acceptance_checks": []
}
```

## Status values

Use these status values:

- `planned`: defined but no production asset exists yet.
- `generated_candidate`: candidate image exists outside canonical kit or needs cleanup.
- `external_candidate`: external/CC0 source candidate exists but is not normalized.
- `cleaned`: asset was cleaned and normalized but not yet accepted.
- `accepted`: canonical asset is ready for scene assembly.
- `rejected`: candidate was rejected; notes should explain why.

## Asset type values

Use these values:

- `canonical_modular`: small or medium reusable piece.
- `canonical_semi_modular`: larger chunk or facade reusable with constraints.
- `scene_specific`: useful for one area or quest scene.
- `generated_reference`: reference only, not a production asset.
- `external_source`: raw external source material, normally not committed directly.

## Production rule

Do not mark an asset `accepted` until:

1. The final file exists at `intended_file` or a deliberate replacement path.
2. Source/license or generation notes are tracked.
3. It passes the manifest's global acceptance checks.
4. It passes its own per-asset acceptance checks.
5. It can be used without breaking area layout readability.

## Prompt export

Use this helper to create per-asset prompt cards from a manifest:

```bash
python tools/export_asset_prompts.py data/asset_kits/wolfpine_village_starter.json
```

The output goes to:

```text
debug/asset_prompts/<kit_id>/
```
