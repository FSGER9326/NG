# NG Asset Production Workflow

This document explains how to turn generated, sourced, or hand-painted art into reusable NG assets without losing consistency, licensing clarity, or gameplay readability.

## Core rule

Do not put raw generated scene cutouts or external downloads directly into the canonical kit.

Canonical kit assets must be:

- reviewed
- cleaned
- normalized
- tracked in metadata
- validated where possible
- usable without breaking area layout readability

## Production states

Asset manifests use these statuses:

```text
planned -> generated_candidate/external_candidate -> cleaned -> accepted
```

Use `rejected` for failed candidates and keep notes when useful.

## Step 1 — Start from a manifest

Every reusable asset should begin as an entry in a manifest under:

```text
data/asset_kits/
```

Current starter manifest:

```text
data/asset_kits/wolfpine_village_starter.json
```

Before producing art, check:

- asset ID
- intended file path
- category
- placement rules
- acceptance checks
- priority

## Step 2 — Export or read the prompt card

Use the prompt exporter:

```bash
python tools/export_asset_prompts.py data/asset_kits/wolfpine_village_starter.json
```

The output is written to:

```text
debug/asset_prompts/<kit_id>/
```

Tracked first-priority prompts also live at:

```text
assets/kits/wolfpine_village/FIRST_PRIORITY_PROMPTS.md
```

## Step 3 — Generate, source, or paint a candidate

Preferred sources:

1. intentional isolated generation for the specific asset
2. hand-painted project art
3. CC0 or permissive external source modified into NG style
4. selective salvage from a generated full-scene concept only when the result is clean and useful

Avoid:

- unclear license assets
- non-commercial assets
- raw full-scene cutouts as default production method
- generated images with commercial-game-identical identity
- assets that only work in one exact scene unless intentionally marked `scene_specific`

## Step 4 — Candidate review

Review against:

- global manifest acceptance checks
- per-asset acceptance checks
- `assets/kits/wolfpine_village/GENERATION_SPECS.md`
- area constraints if the asset is used in a specific area

For Wolfpine Village, also check:

```text
areas/wolfpine_village/ART_BRIEF.md
areas/wolfpine_village/layout_constraints.json
```

Reject candidates with:

- pixel-art style when painted/pre-rendered style is required
- wrong camera angle
- unclear silhouette
- no contact shadow
- impossible architecture
- doors hidden by props
- stairs to windows
- overly horror-dark village exterior lighting
- readable text or UI elements

## Step 5 — Cleanup and normalization

Before a candidate can become canonical:

1. Crop with margin.
2. Remove or mask background.
3. Add/normalize alpha if needed.
4. Normalize color grade to the kit family.
5. Normalize contact shadow.
6. Check scale class.
7. Check file naming.
8. Save to the manifest's `intended_file` or update the manifest with a deliberate replacement path.

## Step 6 — Source and license notes

Before marking accepted, record enough information to identify the source.

For generated assets, record:

- generation model/tool if known
- prompt card or source prompt file
- manual edits made
- whether it is original project-directed output

For external assets, record:

- source name
- source URL
- license
- modifications
- attribution requirement if any

Use the asset policy in:

```text
docs/ASSET_POLICY.md
```

## Step 7 — Manifest update

Only after cleanup and source notes are recorded, update the manifest status.

Example:

```json
{
  "id": "wolfpine_well_01",
  "status": "accepted",
  "intended_file": "assets/kits/wolfpine_village/props/wolfpine_well_01.png"
}
```

Do not mark an asset `accepted` if its file does not exist. The asset-kit validator will fail this.

## Step 8 — Validate

Run:

```bash
python tools/validate_asset_kits.py
python tools/validate_project.py
```

CI also runs both validators.

## Step 9 — Scene assembly

When assembling an area:

1. Start from the area's layout constraints.
2. Place accepted kit assets only where their placement rules allow.
3. Add decals and occluders to unify the plate.
4. Export final `background`, `occlusion`, and `walkmask`/collision data.
5. Confirm doors, hotspots, exits, and NPC zones remain readable and reachable.

For Wolfpine Village, final art must obey:

```text
areas/wolfpine_village/layout_constraints.json
```

## First recommended production batch

Start with these assets:

1. `wolfpine_inn_facade_01`
2. `wolfpine_blacksmith_facade_01`
3. `wolfpine_storehouse_facade_01`
4. `wolfpine_well_01`
5. `wolfpine_market_stall_01`

These support the first village background plate more than small clutter does.
