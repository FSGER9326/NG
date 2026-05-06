# NG Art Baseline v1 (Automation-Friendly)

This baseline is a hard style contract for generated and imported assets.

## Camera and composition

- pseudo-isometric 3/4 camera
- fixed light direction from top-left
- no perspective drift between assets in same kit
- silhouettes must read at gameplay zoom

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
