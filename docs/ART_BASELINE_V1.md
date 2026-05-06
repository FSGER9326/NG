# NG Art Baseline v1 (Automation-Friendly)

This baseline is a hard style contract for generated and imported assets.

## Camera and composition

- pseudo-isometric 3/4 camera
- fixed light direction from top-left
- no perspective drift between assets in same kit
- silhouettes must read at gameplay zoom

## Reference quality bar

PVGames Infernus Free is the current external visual reference for minimum production craft.

Generated or cleaned NG art should meet or exceed that reference level for:

- crisp pseudo-isometric construction
- disciplined modular alignment
- believable material rendering
- readable gameplay-scale silhouettes
- clean transparent edges without halos
- consistent top-left lighting and shadow logic
- coherent kit-wide palette and detail density

Important: PVGames resource files are local-only references. Do not commit, copy, trace, recolor, upscale, or derive NG assets directly from them. Use them as a quality bar only.

See `docs/EXTERNAL_REFERENCE_ASSETS.md` for local setup and license handling.

## Tile and canvas standards

- base iso ground tile: `128x64`
- half transitions: `64x32` when required
- small prop canvas: `512x512`
- medium prop canvas: `1024x1024`
- large facade/module canvas: `2048x2048`

## Material and palette rules

- grounded low-fantasy materials: wood, stone, leather, iron
- muted earth-first palette
- saturated accents reserved for gameplay-significant objects
- avoid glossy modern highlights

## Production acceptance floor

An asset cannot be accepted unless all are true:

1. true RGBA PNG
2. no baked background
3. no obvious edge halo
4. manifest record exists
5. source/provenance note exists
6. in-engine readability confirmed
7. quality is at least comparable to the approved external reference bar

## Variant strategy for scale

For reusable core props, target this variant set:

- `clean`
- `worn`
- `damaged`
- `faction_a`
- `faction_b`
- `season_wet`
- `season_dry`

## Batch size guidance

- preferred batch size: 8 to 12 assets
- one kit per batch
- one PR per batch
