# Generated Asset Production Pipeline

This document defines how generated art moves from prompt output to production-grade NG game asset.

Generated art is not considered production-ready until it passes both:

1. **Visual/art QA**: readable, consistent, useful in NG's grounded low-fantasy style.
2. **Technical/Godot QA**: true alpha, correct canvas, naming, manifest, import, scale, and scene test.

## Core rule

A good-looking generated image is only a **source plate**. A production asset is a **validated, documented, Godot-ready sprite**.

## Asset lifecycle

```text
source prompt / reference
→ generated source image
→ source archive
→ alpha and cleanup pass
→ normalized production candidate
→ manifest + QA preview
→ in-engine placement test
→ promoted asset PR
→ accepted game asset
```

## Folder layout

```text
asset_eval/
  generated_sources/        # local/ignored source generations and experiments
  processed_candidates/     # local/ignored processed PNGs for review
  reviews/                  # local review notes, screenshots, contact sheets

assets/
  vendor/                   # third-party reviewed packs only
  generated/
    outdoor_props/
      roadside_shrine/
        manifest.json
        roadside_shrine.png
        roadside_shrine.preview.jpg
        roadside_shrine.mask.png
```

Do not commit raw exploratory generations unless they are intentionally documented as source/reference material.

## Stage 1 — Concept source

A generated source image can enter evaluation when it has:

- clear intended use
- known generation prompt or source note
- no direct copy of a restricted third-party asset
- no baked text/logo/watermark
- plausible fit with NG's tone

For NG outdoor props, source prompts should target:

- grounded low-fantasy realism
- 2.5D / pseudo-isometric angle
- muted stone/wood/grass palette
- clean silhouette
- no characters unless specifically needed
- no large scenic background

## Stage 2 — Visual QA gate

Reject or regenerate if any are true:

- style is too cartoonish, sci-fi, modern, or glossy
- silhouette is unclear at 50% display scale
- object function is ambiguous
- details look melted, nonsensical, or structurally impossible
- lore symbols are random or misleading
- prop cannot plausibly exist in Wolfpine / Road Peace / low-fantasy setting

Accept for cleanup only if:

- object identity is readable in one glance
- perspective is compatible with current area art
- lighting direction is not extreme
- asset can be used as prop, landmark, or background component
- expected gameplay use is known

## Stage 3 — Technical cleanup

Minimum production candidate requirements:

| Requirement | Target |
|---|---|
| File format | PNG |
| Color mode | RGBA |
| Alpha | real transparency, not baked checkerboard |
| Canvas | 1024x1024 for large props; 512x512 for small props; 2048x2048 source optional |
| Background | fully transparent outside asset |
| Halo | no visible pale/dark fringe on light, dark, and midtone backgrounds |
| Shadow | subtle compact contact shadow only, or no shadow if scene will supply one |
| Origin/pivot | documented in manifest |
| Scale | tested against player/NPC markers |
| File size | reasonable for low-spec target |

Cleanup steps:

1. Remove baked background.
2. Generate true alpha mask.
3. Contract/feather mask carefully to remove halo.
4. Decontaminate edge colors away from white/checkerboard.
5. Crop to object bounds with padding.
6. Place on standard canvas.
7. Normalize scale and pivot.
8. Export production candidate PNG.
9. Generate mask and preview sheet.

## Stage 4 — Automated QA

Every promoted generated asset should include a manifest entry and pass a technical validator.

Required manifest fields:

```json
{
  "id": "roadside_shrine",
  "type": "generated_prop",
  "source_kind": "generated",
  "source_prompt_summary": "weathered roadside shrine, grounded low fantasy, pseudo-isometric",
  "license_status": "project_generated",
  "usage": "Wolfpine Road / old shrine landmark",
  "file": "roadside_shrine.png",
  "canvas": [1024, 1024],
  "pivot": [512, 820],
  "contact_bounds": [330, 760, 700, 910],
  "qa_status": "candidate",
  "notes": "Needs in-engine scale check before final."
}
```

Automated checks should confirm:

- file exists
- PNG is RGBA
- canvas size is allowed
- alpha has both transparent and opaque pixels
- no baked checkerboard pattern in transparent region
- edge halo estimate is below threshold
- manifest fields exist
- file names are lowercase snake_case
- preview/mask exists when required

## Stage 5 — In-engine QA gate

Before final promotion, place the asset in a test scene or target area and check:

- reads at normal zoom
- scale versus player/NPC marker is correct
- click/hotspot bounds can be defined cleanly
- no edge halo over dark grass, dirt, and stone backgrounds
- visual style does not clash with existing Wolfpine art
- prop does not block readability of UI/dialogue overlays
- performance remains acceptable on low-spec target

Use at least three backgrounds for halo checks:

```text
#1b2119 dark grass
#40352b dirt/mud
#68645a stone/road
```

## Stage 6 — Promotion PR

A generated asset promotion PR should include only the minimal set needed.

Required:

- final PNG asset
- manifest entry
- preview sheet or screenshot
- source/prompt note
- in-engine screenshot if used in area
- no raw exploratory files unless justified

Avoid:

- committing every generation attempt
- committing baked-background files
- committing private third-party source tiles
- importing large unused variants

## Production status labels

Use these labels in manifests and PRs:

| Status | Meaning |
|---|---|
| `source` | raw generation or source plate; not game-ready |
| `candidate` | processed RGBA asset; needs in-engine test |
| `approved_first_playable` | accepted for first playable; may still be replaced later |
| `final` | accepted as final asset for current art direction |
| `rejected` | kept only as notes/reference, not imported |

## Generated outdoor prop checklist

- [ ] Source image selected for a concrete NG use
- [ ] True RGBA PNG produced
- [ ] Canvas normalized to 1024x1024 or 512x512
- [ ] Alpha mask checked on dark/mid/light backgrounds
- [ ] Edge halo cleaned
- [ ] Scale checked against player marker
- [ ] Pivot/contact metadata recorded
- [ ] Manifest written
- [ ] Preview sheet generated
- [ ] In-engine screenshot captured
- [ ] Raw/source files kept out of public asset folders

## Practical recommendation for the current outdoor props

The current generated outdoor assets should be processed in this order:

1. `village_well` — best standalone production candidate.
2. `roadside_shrine` — best narrative landmark candidate.
3. `stone_wall_fence` — usable boundary prop, but should eventually split into wall/fence modules.
4. `ruined_archway` — strong landmark, use sparingly and scale-test carefully.

For each, create:

```text
<asset_id>.png
<asset_id>.mask.png
<asset_id>.preview.jpg
manifest.json entry
```

Do not call them final until they pass the in-engine halo and scale check.
