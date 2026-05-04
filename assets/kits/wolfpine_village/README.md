# Wolfpine Village Asset Kit

This folder is the canonical reusable asset kit for Wolfpine-style settlement art.

The goal is to build future village scenes from reusable, documented parts instead of generating every area from scratch. Final area art should still be exported as low-spec 2D background/foreground plates, but those plates should be assembled from trusted NG kit assets wherever possible.

## Style target

- Classic pre-rendered / painted pseudo-isometric CRPG look.
- Closer to Baldur's Gate 2 / Pillars-style settlement art than pixel art.
- Warm late-afternoon or soft overcast village exterior lighting.
- Natural greens and earth colors, not horror-dark for village exteriors.
- Grounded low-fantasy frontier materials: timber, plaster, old stone, mossy slate, mud, cobble, pine vegetation.

## Folder intent

```text
assets/kits/wolfpine_village/
  buildings/      Large and semi-modular facades.
  architecture/   Doors, windows, stairs, roof patches, fence sections.
  props/          Distinct focal or interactable objects.
  clutter/        Small repeatable dressing pieces.
  vegetation/     Trees, shrubs, weeds, roots, grass.
  decals/         Mud, moss, puddles, wheel ruts, soot, cracks, shadows.
  occluders/      Foreground depth pieces such as branches, roof edges, wall tops.
  source/         Optional notes for source files kept outside the repo.
```

Large raw external downloads should not be committed here. Commit only curated, normalized, project-ready assets and lightweight metadata.

## Source of truth

The metadata manifest lives at:

```text
data/asset_kits/wolfpine_village_starter.json
```

The village area art brief and layout constraints live at:

```text
areas/wolfpine_village/ART_BRIEF.md
areas/wolfpine_village/layout_constraints.json
```

## Promotion rule

A generated or external piece becomes a canonical NG kit asset only when it passes these checks:

- It matches the Wolfpine camera angle.
- It matches the Wolfpine palette and lighting family.
- It has clean edges or a clear intended plate boundary.
- It has a readable gameplay function.
- It does not contain impossible architecture.
- It has metadata in the starter manifest or a future kit manifest.
- Its license/source/generation notes are known.

## Do not use raw generated scene cutouts as canonical assets by default

Cutting useful pieces out of full generated scenes is allowed for salvage, but intentional isolated asset generation is preferred. Scene cutouts often have incomplete hidden sides, baked scene-specific shadows, and awkward edges.
