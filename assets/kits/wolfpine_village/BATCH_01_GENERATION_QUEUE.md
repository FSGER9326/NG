# Wolfpine Village Batch 01 Generation Queue

## Purpose

Batch 01 produces the first high-value reusable environment assets needed to assemble and review the Wolfpine Village hub plate.

This batch focuses on large readable scene anchors first, then the central interaction props needed to judge scale, walkability, and classic CRPG readability.

## Source files

Use these files as hard references before generating:

```text
areas/wolfpine_village/ART_BRIEF.md
areas/wolfpine_village/layout_constraints.json
data/asset_kits/wolfpine_village_starter.json
assets/kits/wolfpine_village/GENERATION_SPECS.md
```

## Global prompt lock

```text
Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.
```

## Global negative prompt

```text
pixel art, front-facing flat perspective, inconsistent camera angle, unreadable silhouette, no contact shadow, modern materials, glossy heroic fantasy, horror-dark lighting, readable text, labels, signs with words, UI, impossible architecture, stairs to windows, blocked doors, full scene background, characters, monsters
```

## Batch assets

### 01 — `wolfpine_inn_facade_01`

Target file:

```text
assets/kits/wolfpine_village/buildings/wolfpine_inn_facade_01.png
```

Generation prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: The Pine Hearth Inn Facade
Asset ID: wolfpine_inn_facade_01
Category: buildings / facade
Style family: Wolfpine village
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement asset, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow
Materials: dark timber frame, tan weathered plaster, old stone lower foundation, mossy gray slate roof, muted clay roof accents, damp moss, mud at threshold
Requirements:
- isolated reusable building facade, not a full scene
- large two-story frontier inn silhouette
- one clearly visible ground-level main door facing lower-right / south-east
- small shuttered windows that cannot be mistaken for doors
- subtle warm window glow only, not horror lighting
- lived-in poor border village character
- enough margin around asset for cleanup and alpha masking
- no readable text, no sign lettering, no UI
```

Review gate:

- [ ] Door is ground-level and visible.
- [ ] Door is not blocked by barrels, stairs, rails, roof, or props.
- [ ] Windows cannot be mistaken for doors.
- [ ] Roof, walls, and foundation are structurally believable.
- [ ] Asset can fit near the `inn_front` zone from `layout_constraints.json`.

### 02 — `wolfpine_blacksmith_facade_01`

Target file:

```text
assets/kits/wolfpine_village/buildings/wolfpine_blacksmith_facade_01.png
```

Generation prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: Wolfpine Blacksmith Facade
Asset ID: wolfpine_blacksmith_facade_01
Category: buildings / facade
Style family: Wolfpine village
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement asset, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow, subtle forge warmth only
Materials: dark timber, old stone, weathered plaster, soot-stained chimney, woodpile, iron tools, muddy work threshold
Requirements:
- isolated reusable blacksmith facade, not a full scene
- clear ground-level door facing a walkable work yard
- chimney and forge identity readable without labels
- forge awning or side work bay may exist, but must not block the door
- anvil, tool silhouettes, coal, and firewood beside the approach, not across it
- no stairs to windows, no blocked threshold, no readable text
```

Review gate:

- [ ] Door remains visible and reachable.
- [ ] Forge identity reads at game scale.
- [ ] Tool clutter is beside the work area, not blocking the path.
- [ ] Perspective matches the inn facade and shared village ground plane.

### 03 — `wolfpine_storehouse_facade_01`

Target file:

```text
assets/kits/wolfpine_village/buildings/wolfpine_storehouse_facade_01.png
```

Generation prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: Guarded Storehouse Facade
Asset ID: wolfpine_storehouse_facade_01
Category: buildings / facade
Style family: Wolfpine village
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement asset, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow
Materials: heavy timber, old stone foundation, reinforced plank door, iron strap hinges, damp moss, muddy threshold, sacks and crates near side wall
Requirements:
- isolated reusable storehouse facade, not a full scene
- practical guarded supply building, not noble housing
- one visible reinforced ground-level door
- side clutter may show famine pressure but must not hide the door
- no guards or people baked into the asset
- no readable text, no UI
```

Review gate:

- [ ] Main door exists and makes architectural sense.
- [ ] Clutter does not block the door.
- [ ] Reads as storage/supplies, not inn/cottage.
- [ ] Fits the `storehouse` footprint and approach from `layout_constraints.json`.

### 04 — `wolfpine_well_01`

Target file:

```text
assets/kits/wolfpine_village/props/wolfpine_well_01.png
```

Generation prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: Stone Village Well
Asset ID: wolfpine_well_01
Category: props / village_core
Style family: Wolfpine village
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement prop, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow
Materials: damp old stone, moss, rope, bucket, simple dark timber crossbeam
Requirements:
- isolated reusable village well, not a full scene
- low circular stone rim readable from pseudo-isometric view
- timber crossbeam or small roof must not dominate or hide ground contact
- usable as central hotspot and party-gathering focal object
- approach space visually open on at least two sides
- no readable text, no UI
```

Review gate:

- [ ] Reads as a well at small scale.
- [ ] Does not become a large occluder.
- [ ] Contact shadow anchors it to the ground.
- [ ] Works as the central square focal point.

### 05 — `wolfpine_market_stall_01`

Target file:

```text
assets/kits/wolfpine_village/props/wolfpine_market_stall_01.png
```

Generation prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: Village Market Stall
Asset ID: wolfpine_market_stall_01
Category: props / market
Style family: Wolfpine village
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement prop, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow
Materials: rough wooden counter, muted cloth awning, baskets, onions, dried fish, tallow candles, cloth bundles
Requirements:
- isolated reusable market stall, not a full scene
- customer-facing side clearly open
- narrow enough to sit along a path edge without blocking the main route
- goods add lived-in detail without noisy clutter
- no readable text, no labels, no UI
```

Review gate:

- [ ] Clear front/customer side.
- [ ] Does not block south road to well route when placed on edge.
- [ ] Goods are readable without visual noise.
- [ ] Footprint is easy to block in collision.

### 06 — `wolfpine_notice_board_01`

Target file:

```text
assets/kits/wolfpine_village/props/wolfpine_notice_board_01.png
```

Generation prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: Damp Village Notice Board
Asset ID: wolfpine_notice_board_01
Category: props / quest_board
Style family: Wolfpine village
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement prop, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow
Materials: weathered dark timber, damp parchment scraps, wax or guard-seal shapes, mud at base
Requirements:
- isolated reusable notice board on two posts
- parchment and seal shapes visible but no readable words
- clear interaction side
- should read as a board, not a door or signpost
- no readable text, no labels, no UI
```

Review gate:

- [ ] No readable words.
- [ ] Reads as a notice board at game scale.
- [ ] Interaction side is clear.
- [ ] Good hotspot silhouette.

## Batch acceptance

Batch 01 is usable when:

- [ ] All six assets have candidate PNGs or documented candidate references.
- [ ] Each candidate passes its review gate.
- [ ] Any generated source notes are recorded in the asset manifest or a follow-up ledger.
- [ ] Candidates are placed into the intended kit folders or explicitly marked as rejected.
- [ ] At least one quick composition mockup can place inn, blacksmith, storehouse, well, market stall, and notice board without violating `layout_constraints.json`.

## Next batch

Batch 02 should focus on reusable assembly pieces:

```text
wolfpine_door_heavy_01
wolfpine_window_shuttered_01
wolfpine_fence_segment_01
wolfpine_firewood_stack_01
wolfpine_barrel_01
wolfpine_crate_01
```

Batch 03 should focus on ground/depth finishing:

```text
wolfpine_grass_clump_01
wolfpine_mud_rut_decal_01
wolfpine_branch_occluder_01
```