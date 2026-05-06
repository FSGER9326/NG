# PVGames Infernus Reference Guide

Use this guide to turn the PVGames Infernus Free pack into a practical quality reference for NG asset production.

This pack is not an NG style target. It is a craft benchmark: generated NG assets should be at least as clean, readable, modular, and production-ready, while staying original and matching NG's grounded low-fantasy Wolfpine direction.

## Canonical organized location

All usable reference work should point to one organized root:

```text
reference_assets/organized/pvgames/infernus_free/
```

Inside that folder, assets should be grouped by category:

```text
reference_assets/organized/pvgames/infernus_free/
  animated_light_sources/
  architectural_adorns/
  archways/
  buttresses/
  columns/
  columns_pillars/
  decor_props/
  floor_ground_tiles/
  floor_tiles/
  misc_root_tiles/
  pillars/
  ramps/
  rocks_stone/
  stairs/
  walls/
  walls_and_edges/
  reference_index.json
```

## Organizing newly added files

If the pack or additional reference files were added anywhere else, run:

```bash
python tools/organize_reference_assets.py <folder-containing-pngs> --dest reference_assets/organized/pvgames/infernus_free --mode move
```

Use `--mode copy` instead when you want to preserve the original folder. Use `--dry-run` to create an index without moving files.

The organizer:

- scans all PNGs recursively
- classifies them into practical reference categories
- moves or copies them into one canonical reference root
- writes `reference_index.json` with dimensions, RGBA status, byte size, source path, organized path, and category

## Raw/local source location

For local-only raw source copies, use:

```text
reference_assets/local/pvgames/infernus_free/
```

That path is intentionally ignored by Git. If a private fork intentionally tracks the assets, keep the same folder shape so the catalog and reference notes remain useful.

## Pack structure observed from upload

The uploaded `PVGames_Infernus_Free.zip` contains:

- 639 PNG files
- All parsed PNGs use RGBA color type
- Primary root: `Infernus_Tiles/`
- Major sub-kits:
  - `Infernus_Tiles/`
  - `Infernus_Tiles/Building_Infernus_1/`
  - `Infernus_Tiles/Building_Infernus_2/`

## Category map

Use these categories when selecting examples for generated-art QA.

| Category | Count | Use as reference for |
|---|---:|---|
| `misc_root_tiles` | 325 | Breadth of set dressing, environment pieces, decals, and props. |
| `walls` | 82 | Modular wall depth, side consistency, corner joins, facade rhythm. |
| `decor_props` | 54 | Small prop silhouette, readable thematic accents, detail density. |
| `walls_and_edges` | 26 | Wall-mounted decoration and boundary-piece readability. |
| `stairs` | 24 | Step direction, elevation clarity, movement affordance. |
| `rocks_stone` | 17 | Organic stone shape language and material treatment. |
| `ramps` | 16 | Slope direction and elevation-transition clarity. |
| `architectural_adorns` | 14 | Ornament density without muddy silhouettes. |
| `buttresses` | 14 | Grounded support pieces and contact shadow logic. |
| `columns` | 14 | Vertical modular structure, capitals/bases, repeated variants. |
| `floor_tiles` | 14 | Repeatable structural floor patterns and seams. |
| `archways` | 10 | Portal negative space and threshold framing. |
| `animated_light_sources` | 9 | Flame/glow readability and animation-strip discipline. |
| `columns_pillars` | 9 | Standalone vertical silhouettes and scale contrast. |
| `floor_ground_tiles` | 7 | Ground texture and tile seam discipline. |
| `pillars` | 4 | Large support silhouettes and occlusion potential. |

## Best reference examples by task

### Wolfpine village ground tiles

Compare generated tiles against:

- `Infernus_Tiles/Infernus_Ground.png`
- `Infernus_Tiles/Infernus_Hellscape_Ground_1.png`
- `Infernus_Tiles/Building_Infernus_1/Floor_Lower_1.png`
- `Infernus_Tiles/Building_Infernus_2/Floor_Lower_1.png`

Look for clean tile edges, controlled texture noise, readable material breakup, and repeat-friendly shapes.

### Wolfpine buildings and facades

Compare generated facades against:

- `Infernus_Tiles/Building_Infernus_1/Wall_Front_Large_1.png`
- `Infernus_Tiles/Building_Infernus_1/Wall_Large_1.png`
- `Infernus_Tiles/Building_Infernus_2/Wall_Front_Large_1.png`
- `Infernus_Tiles/Building_Infernus_2/Wall_Large_1.png`

Look for modular alignment, believable side planes, consistent shadow side, and clean joins.

### Doors, archways, and thresholds

Compare generated doors/thresholds against:

- `Infernus_Tiles/Building_Infernus_1/Archway_1.png`
- `Infernus_Tiles/Building_Infernus_1/Archway_2.png`
- `Infernus_Tiles/Building_Infernus_2/Archway_1.png`
- `Infernus_Tiles/Building_Infernus_2/Archway_2.png`

Look for clear negative space, readable walk-through intent, and strong foreground/background separation.

### Stairs and ramps

Compare generated elevation transitions against:

- `Infernus_Tiles/Building_Infernus_1/Stairs_1.png`
- `Infernus_Tiles/Building_Infernus_1/Stairs_Inverted_1.png`
- `Infernus_Tiles/Building_Infernus_2/Ramp_1.png`
- `Infernus_Tiles/Building_Infernus_2/Ramp_2.png`

Reject NG generated stairs if they do not clearly show where a character can walk.

### Props and set dressing

Compare generated props against:

- `Infernus_Tiles/Infernus_Bones1_1.png`
- `Infernus_Tiles/Infernus_Decor1_1.png`
- `Infernus_Tiles/Infernus_Altar_1.png`
- `Infernus_Tiles/Infernus_Hellscape_Rock_1.png`

Use them for silhouette clarity and material polish, not theme copying.

### Lighting and effects

Compare generated flames/glows against:

- `Infernus_Tiles/Anim_Infernus_Lightsources_1.png`
- `Infernus_Tiles/Anim_Infernus_Lightsources_2.png`
- `Infernus_Tiles/Anim_Infernus_Lightsources_3.png`

Use these for animation-strip and glow readability only. NG village lighting should remain grounded and less infernal.

## QA checklist for generated NG art

Before accepting any generated NG asset, compare it to the relevant PVGames category and answer:

- Is the silhouette readable at gameplay scale?
- Does the asset obey a clear pseudo-isometric angle?
- Does the light direction stay consistent across the kit?
- Are alpha edges clean, with no background residue or halo?
- Is material rendering at least as legible as the reference?
- Does the asset join or tile as predictably as the reference category?
- Does it preserve NG's grounded Wolfpine style instead of copying Infernus theming?

If any answer is no, keep the asset in candidate/rejected status.

## Catalog regeneration

When the reference files exist in the checkout, regenerate a full local catalog with:

```bash
python tools/catalog_reference_assets.py reference_assets/organized/pvgames/infernus_free --source-pack "PVGames Infernus Free" --out debug/pvgames_infernus_full_catalog.json
```

The committed compact catalog lives at:

```text
data/asset_registry/pvgames_infernus_reference_catalog.json
```

That catalog is intentionally summary-first so agents can use it without reading every binary file.
