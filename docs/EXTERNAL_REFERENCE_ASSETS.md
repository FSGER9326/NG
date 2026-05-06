# External Reference Assets

External reference assets are visual benchmarks for generated and cleaned NG art.

## Canonical reference root

All committed external reference packs must live under one root:

```text
reference_assets/organized/
```

Do not keep reference-pack folders at the repository root.

## PVGames Infernus Free

- Provider: Pioneer Valley Games / PVGames
- Pack: `PVGames_Infernus_Free.zip`
- Canonical organized path: `reference_assets/organized/pvgames/infernus_free/`
- Optional raw staging path: `reference_assets/local/pvgames/infernus_free/`
- Required index file once organized: `reference_assets/organized/pvgames/infernus_free/reference_index.json`

The pack readme permits use and editing in commercial and non-commercial projects; verify redistribution scope before publishing any public repository containing the resources.

## Required folder shape

PVGames files should be grouped into category folders below the canonical path:

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

## Root folders to move

If any of these folders exist at repo root, move them into the canonical path:

```text
Building_Infernus_1/
Building_Infernus_2/
Infernus tiles 1/
Infernus tiles 2/
Infernus tiles 3/
Infernus tiles 4/
Infernus tiles 5/
```

Use the organizer:

```bash
python tools/organize_reference_assets.py . --dest reference_assets/organized/pvgames/infernus_free --mode move
```

Or move only the known root folders:

```bash
python tools/organize_reference_assets.py "Building_Infernus_1" --dest reference_assets/organized/pvgames/infernus_free --mode move
python tools/organize_reference_assets.py "Building_Infernus_2" --dest reference_assets/organized/pvgames/infernus_free --mode move
python tools/organize_reference_assets.py "Infernus tiles 1" --dest reference_assets/organized/pvgames/infernus_free --mode move
python tools/organize_reference_assets.py "Infernus tiles 2" --dest reference_assets/organized/pvgames/infernus_free --mode move
python tools/organize_reference_assets.py "Infernus tiles 3" --dest reference_assets/organized/pvgames/infernus_free --mode move
python tools/organize_reference_assets.py "Infernus tiles 4" --dest reference_assets/organized/pvgames/infernus_free --mode move
python tools/organize_reference_assets.py "Infernus tiles 5" --dest reference_assets/organized/pvgames/infernus_free --mode move
```

## How agents should use this reference

1. Look for PVGames reference material only under `reference_assets/organized/pvgames/infernus_free/`.
2. Use the pack as a quality benchmark for rendering craft, perspective discipline, silhouette clarity, alpha cleanup, material detail, and modular tile consistency.
3. Do not copy, trace, recolor, upscale, or derive NG assets directly from these files.
4. Generated NG assets must be original, project-specific, and tracked through the normal manifest, QA, and validator flow.
5. If a future pack has a different license, add a separate registry entry before using it.

## Quality benchmark notes

Generated or cleaned NG art should aim to meet or exceed this reference level in:

- crisp pseudo-isometric construction
- consistent top-left lighting and shadow logic
- clean transparent edges without halos
- readable silhouettes at gameplay scale
- modular parts that align predictably
- material rendering for stone, wood, metal, cloth, dirt, and vegetation
- coherent kit-wide palette and detail density
