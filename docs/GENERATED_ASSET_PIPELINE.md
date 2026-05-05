# Generated Art Asset Production Pipeline

This pipeline defines how generated or kitbashed art becomes production-grade NG game art.

It exists because a good-looking generated image is not automatically a shippable asset. An asset is production-grade only when it passes source, legal, technical, visual, integration, and in-engine QA gates.

## Principles

- Keep raw/generated source files out of production folders until accepted.
- Preserve source prompts, references, licenses, and transformation notes.
- Prefer small, isolated, low-risk props before large background plates.
- Keep final game files Godot-friendly, low-spec, and compatible with the Godot 4 Compatibility renderer target.
- Treat generated art as source material until it passes objective checks.
- Do not ship assets that still depend on an untracked source pack, unclear license, or unclean background removal.

## Folder lifecycle

```text
asset_eval/
  downloads/               # local only; raw third-party packs
  extracted/               # local only; extracted third-party packs
  generated_sources/       # local only; raw generated outputs and prompts
  production_candidates/   # local only or review-only processed candidates

assets/
  vendor/                  # accepted third-party subsets with manifests/licenses
  generated/               # accepted generated or heavily processed assets
    outdoor_props/
    ui/
    icons/
    backgrounds/
```

Raw downloads and generated sources should stay local unless they are needed for review and safe to commit. Production folders should contain only selected files with license/source metadata.

## Pipeline stages

### Stage 0 — Need definition

Before generating or importing anything, define the in-game need:

- asset id
- area or feature that needs it
- player-facing purpose
- prop/background/icon/audio category
- approximate size in game
- target mood and readability
- whether it is final art, temporary art, or test-only

Example:

```json
{
  "asset_id": "wolfpine_village_well_01",
  "category": "outdoor_prop",
  "needed_for": "wolfpine_village",
  "purpose": "village center landmark and possible inspect hotspot",
  "target_canvas": [1024, 1024],
  "target_format": "RGBA PNG",
  "production_goal": "first_playable_candidate"
}
```

### Stage 1 — Source and rights gate

Every candidate needs a recorded source trail:

- generation date
- model/tool used, if known
- prompt or edit instructions
- reference images used
- third-party source pack names, if any
- license notes for every source image/pack
- whether the output may be redistributed in a public repo

Reject or keep local-only if:

- source license is unknown
- edited third-party art cannot be redistributed
- output is mostly a direct copy of a protected source asset
- no source URL or license file exists for a third-party pack

### Stage 2 — Generation/art direction pass

Generated output must satisfy visual direction before technical cleanup:

- readable silhouette at expected in-game scale
- grounded low-fantasy tone
- no anachronistic or sci-fi details
- no accidental text/symbols unless approved
- consistent 2.5D/pseudo-isometric camera where relevant
- consistent material language with the area
- no obvious AI artifacts in focal details

Reject or regenerate if:

- perspective conflicts with existing area art
- subject is fused into an unusable mini-diorama when a modular prop is needed
- details are illegible or nonsensical
- style overpowers NG's grounded tone

### Stage 3 — Technical cleanup

A production candidate must be converted into game-ready files.

Required for prop sprites:

- PNG format
- true RGBA alpha
- transparent background outside the asset
- no baked checkerboard
- no white/gray fringe halos on dark or colored backgrounds
- standard canvas size, usually 1024x1024 for large props or 512x512 for small props
- centered composition
- safe margins, usually 24-64 px depending on asset size
- consistent contact point/pivot metadata
- compact contact shadow only, or separate shadow if needed

Required for background plates:

- target resolution documented
- no unintended transparency unless used by the scene system
- walkable floor readability
- hotspot/occlusion planning notes
- foreground/background layer plan if actors pass behind objects

Recommended cleanup steps:

```text
1. Remove any baked background/checkerboard.
2. Build or refine alpha mask.
3. Defringe edges against dark, grass, dirt, and UI-checker backgrounds.
4. Crop to visible bounds with padding.
5. Normalize to target canvas.
6. Place contact point consistently near the lower center of the asset.
7. Save PNG with RGBA.
8. Create QA previews on black, mid-gray, grass/dirt, and checker backgrounds.
9. Record metadata in a manifest.
```

### Stage 4 — Objective QC gate

A generated prop is not production-grade until these checks pass:

| Check | Requirement |
|---|---|
| File format | `.png` |
| Color mode | RGBA |
| Alpha | true transparency outside asset |
| Canvas | standard size, usually 1024x1024 or 512x512 |
| Background | no white, checkerboard, or prompt background baked into transparent area |
| Edge quality | no visible halo at 100%, 75%, 50% scale on dark and grass backgrounds |
| Bounds | asset is not clipped; has safe margin |
| Scale | tested against player/NPC marker |
| Pivot | contact/pivot documented |
| Compression | no obvious compression artifacts |
| Source | prompt/source/license recorded |
| Integration | loads in Godot without missing-resource errors |

Recommended thresholds for automated checks:

- image must be RGBA
- visible alpha pixels must exist
- canvas must match manifest target canvas
- visible bounds must have margin >= 8 px on every side
- asset must not be almost fully opaque canvas-filling unless it is a background plate
- manifest must include id, category, source type, intended use, license/source notes, and production status

### Stage 5 — In-engine placement QA

Place the asset in a test scene or target area before acceptance.

Check at common scales:

- 100%
- 75%
- 50%

Check against:

- player marker
- NPC marker
- road/grass/dirt backgrounds
- darker night/interior lighting if relevant
- camera zoom or viewport scale used by NG

Reject or reprocess if:

- edge halo is visible
- contact point floats
- asset scale is inconsistent
- detail becomes mush at intended size
- prop blocks navigation/readability
- baked shadow conflicts with scene lighting

### Stage 6 — Promotion into repo

Only selected, reviewed files should move into `assets/`.

Every promoted generated asset needs:

```text
assets/generated/outdoor_props/<asset_id>.png
assets/generated/outdoor_props/<asset_id>.manifest.json
```

For third-party subsets:

```text
assets/vendor/<source>/<pack>/manifest.json
assets/vendor/<source>/<pack>/LICENSE.txt
assets/vendor/<source>/<pack>/<selected_file>.png
```

Promote tiny subsets first. Do not commit large raw packs or every generated variation.

### Stage 7 — Data-driven integration

Use data manifests instead of hardcoded paths where possible.

Example:

```json
{
  "id": "wolfpine_village_well_01",
  "path": "res://assets/generated/outdoor_props/wolfpine_village_well_01.png",
  "category": "outdoor_prop",
  "pivot": [512, 900],
  "visual_scale": 0.75,
  "hotspot_id": "village_well",
  "status": "production_candidate"
}
```

### Stage 8 — Final acceptance

Mark an asset as final only after:

- technical QC passes
- in-engine placement QA passes
- source/license review passes
- visual direction review passes
- no known scale/halo issues remain
- it is used by an area, UI, scenario, or near-term first-playable feature

Statuses:

| Status | Meaning |
|---|---|
| `source_only` | raw generation/download; not game-ready |
| `concept` | visual reference only |
| `processed_candidate` | RGBA/cropped/normalized, pending in-engine QA |
| `production_candidate` | technically valid and ready for test integration |
| `accepted_first_playable` | usable in first playable |
| `final` | approved final asset |
| `rejected` | do not use |

## Generated outdoor prop checklist

Use this checklist for shrine/well/wall/arch assets:

- [ ] asset is needed by a specific area or feature
- [ ] source prompt and references are recorded
- [ ] no direct copying of restricted source art
- [ ] PNG is RGBA
- [ ] canvas is 1024x1024
- [ ] background is true transparent alpha
- [ ] no checkerboard or white backdrop remains
- [ ] alpha edge checked on black/mid-gray/grass backgrounds
- [ ] no obvious white or gray halo
- [ ] contact shadow is compact and not scene-specific
- [ ] prop is not clipped
- [ ] visible bounds leave safe margin
- [ ] pivot/contact point recorded
- [ ] scale tested against actor marker
- [ ] imported into Godot without warnings
- [ ] used by a test scene or target area before final acceptance

## Practical recommendation for current NG assets

For the generated outdoor set, use this order:

1. village well — strongest functional prop candidate
2. roadside shrine — strongest narrative prop candidate
3. ruined archway — strong landmark, use sparingly
4. stone wall/fence — useful but should later split into wall and fence modules

Before committing any generated outdoor prop as final:

- run technical QC
- create dark-background previews
- place in Wolfpine Road/Village test scene
- scale against player/NPC markers
- store manifest with `production_candidate`, not `final`, until in-engine review passes

## Non-goals

This pipeline does not require a full art department workflow. It is intentionally lightweight for first-playable production. It also does not make AI/generation licensing claims by itself; every source still needs explicit review under `docs/ASSET_POLICY.md`.
