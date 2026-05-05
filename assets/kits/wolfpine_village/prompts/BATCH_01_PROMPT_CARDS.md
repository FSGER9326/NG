# Wolfpine Village Batch 01 Prompt Cards

These are ready-to-copy generation cards for the first Wolfpine Village reusable asset batch.

Source manifest:

```text
data/asset_batches/wolfpine_village_batch_01.json
```

Exporter:

```bash
python tools/export_asset_batch_prompts.py data/asset_batches/wolfpine_village_batch_01.json
```

## Shared style lock

Use this lock for every Batch 01 prompt:

```text
Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.
```

## Shared negative prompt

```text
pixel art, front-facing flat perspective, inconsistent camera angle, unreadable silhouette, no contact shadow, modern materials, glossy heroic fantasy, horror-dark lighting, readable text, labels, signs with words, UI, impossible architecture, stairs to windows, blocked doors, full scene background, characters, monsters
```

---

## `wolfpine_inn_facade_01`

Target:

```text
assets/kits/wolfpine_village/buildings/wolfpine_inn_facade_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_inn_facade_01
Target file: assets/kits/wolfpine_village/buildings/wolfpine_inn_facade_01.png

Asset-specific requirements:
Large two-story frontier inn facade, timber frame, tan weathered plaster, old stone lower foundation, mossy gray slate roof, muted clay roof accents, one clearly visible ground-level main door facing lower-right or south-east, small shuttered windows, subtle warm window glow, lived-in poor border village character, no readable sign text.

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- suitable for assembly into a 1280x720 Wolfpine Village background plate
```

Review gate:

- [ ] Door is ground-level and visible.
- [ ] Door is not blocked by barrels, stairs, rails, roof, or props.
- [ ] Windows cannot be mistaken for doors.
- [ ] Roof, walls, and foundation are structurally believable.
- [ ] Asset can fit near the `inn_front` zone from `layout_constraints.json`.

---

## `wolfpine_blacksmith_facade_01`

Target:

```text
assets/kits/wolfpine_village/buildings/wolfpine_blacksmith_facade_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_blacksmith_facade_01
Target file: assets/kits/wolfpine_village/buildings/wolfpine_blacksmith_facade_01.png

Asset-specific requirements:
Practical blacksmith forge facade, timber and stone, clear ground-level door facing a walkable work yard, chimney and forge identity readable without labels, forge awning or side work bay, anvil and tool silhouettes beside the approach, soot-stained chimney, subtle forge warmth, no blocked threshold.

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- suitable for assembly into a 1280x720 Wolfpine Village background plate
```

Review gate:

- [ ] Door remains visible and reachable.
- [ ] Forge identity reads at game scale.
- [ ] Tool clutter is beside the work area, not blocking the path.
- [ ] Perspective matches the inn facade and shared village ground plane.

---

## `wolfpine_storehouse_facade_01`

Target:

```text
assets/kits/wolfpine_village/buildings/wolfpine_storehouse_facade_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_storehouse_facade_01
Target file: assets/kits/wolfpine_village/buildings/wolfpine_storehouse_facade_01.png

Asset-specific requirements:
Sturdy guarded village storehouse facade, heavy timber, old stone foundation, reinforced plank door with iron strap hinges, damp moss, muddy threshold, sacks and crates near the side wall, practical supply building, no noble decoration, no people baked into the asset.

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- suitable for assembly into a 1280x720 Wolfpine Village background plate
```

Review gate:

- [ ] Main door exists and makes architectural sense.
- [ ] Clutter does not block the door.
- [ ] Reads as storage or supplies, not inn or cottage.
- [ ] Fits the storehouse footprint and approach from `layout_constraints.json`.

---

## `wolfpine_well_01`

Target:

```text
assets/kits/wolfpine_village/props/wolfpine_well_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_well_01
Target file: assets/kits/wolfpine_village/props/wolfpine_well_01.png

Asset-specific requirements:
Weathered stone village well, low circular damp stone rim, moss, rope and bucket, simple dark timber crossbeam or very small roof that does not dominate, readable from pseudo-isometric view, central village square hotspot and party-gathering focal object.

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- suitable for assembly into a 1280x720 Wolfpine Village background plate
```

Review gate:

- [ ] Reads as a well at small scale.
- [ ] Does not become a large occluder.
- [ ] Contact shadow anchors it to the ground.
- [ ] Works as the central square focal point.

---

## `wolfpine_market_stall_01`

Target:

```text
assets/kits/wolfpine_village/props/wolfpine_market_stall_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_market_stall_01
Target file: assets/kits/wolfpine_village/props/wolfpine_market_stall_01.png

Asset-specific requirements:
Small frontier market stall, muted cloth awning, rough wooden counter, baskets, onions, dried fish, tallow candles, cloth bundles, customer-facing side clearly open, narrow enough to sit along a path edge, no readable labels or text.

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- suitable for assembly into a 1280x720 Wolfpine Village background plate
```

Review gate:

- [ ] Clear front or customer side.
- [ ] Does not block south road to well route when placed on edge.
- [ ] Goods are readable without visual noise.
- [ ] Footprint is easy to block in collision.

---

## `wolfpine_notice_board_01`

Target:

```text
assets/kits/wolfpine_village/props/wolfpine_notice_board_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_notice_board_01
Target file: assets/kits/wolfpine_village/props/wolfpine_notice_board_01.png

Asset-specific requirements:
Damp wooden village notice board on two posts, weathered dark timber, parchment scraps and wax or guard-seal shapes visible but no readable words, mud at base, clear interaction side, should read as a quest board rather than a door or signpost.

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- suitable for assembly into a 1280x720 Wolfpine Village background plate
```

Review gate:

- [ ] No readable words.
- [ ] Reads as a notice board at game scale.
- [ ] Interaction side is clear.
- [ ] Good hotspot silhouette.
