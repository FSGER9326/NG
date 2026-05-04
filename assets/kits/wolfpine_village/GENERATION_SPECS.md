# Wolfpine Village Asset Generation Specs

Use these specs when generating, kitbashing, or manually painting canonical Wolfpine Village assets.

The goal is not to mimic a specific commercial game. The target is an original classic pre-rendered / painted pseudo-isometric CRPG look, suitable for low-spec Godot 2D background-plate assembly.

## Global style lock

Use this visual lock for every asset in the kit:

```text
Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.
```

## Global negative constraints

Reject or regenerate any asset with:

- pixel-art rendering
- front-facing flat perspective
- inconsistent camera angle
- unreadable silhouette at game scale
- no contact shadow
- modern materials or objects
- overly glossy heroic fantasy look
- horror-dark lighting for village exterior assets
- text, labels, signs with readable words, or UI elements
- impossible architecture, especially stairs to windows or doors blocked by props

## Asset isolation rules

Preferred generation target:

- one asset per image
- clean background or simple neutral ground plane
- enough margin for cleanup
- no baked full-scene surroundings
- no characters unless the asset specifically needs a scale reference, and then remove the character before production use

## Lighting rules

- Light source: soft upper-left / late-afternoon daylight.
- Contact shadows should fall down/right or slightly back/right.
- Windows may have warm glow, but only when useful.
- Do not use strong blue crypt lighting for outdoor village assets.

## Scale conventions

Approximate production scale classes:

- `large_building`: 300-520 px wide in a 1280x720 area plate.
- `medium_prop`: 80-180 px wide.
- `small_prop`: 40-100 px wide.
- `small_clutter`: 24-70 px wide.
- `ground_decal`: variable, transparent edge preferred.
- `foreground_occluder`: large enough to frame but not obscure required hotspots.

## Generation prompt template

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: [ASSET DISPLAY NAME]
Asset ID: [ASSET ID]
Category: [CATEGORY]
Style family: Wolfpine village
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement asset, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow
Materials: dark timber, old stone, weathered plaster, moss, mud, cobble, muted natural colors as appropriate
Requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent ground plane and contact shadow
- no text, no UI
- no modern objects
- suitable for assembly into a 1280x720 village background plate
- obey the asset-specific rules below
```

## Priority asset specs

### 1. `wolfpine_inn_facade_01`

Purpose: main village social building and future interior transition.

Prompt add-on:

```text
A larger two-story frontier inn facade called The Pine Hearth in concept only, but with no readable text. Timber frame, tan plaster, old stone lower foundation, mossy slate and muted clay roof elements, one clearly visible ground-level main door facing the viewer's lower-right side, small shuttered windows, subtle warm window glow, lived-in but poor border village character.
```

Acceptance:

- Must have a visible ground-level door.
- Door must not be blocked by barrels, railings, stairs, or props.
- Windows must not look like doors.
- Roof and foundation must feel structurally possible.

### 2. `wolfpine_blacksmith_facade_01`

Purpose: blacksmith building / forge anchor for the village square.

Prompt add-on:

```text
A practical blacksmith forge facade, timber and stone, low-fantasy frontier construction, clear ground-level door, chimney, forge awning or side work bay, anvil/workbench/tool silhouettes placed beside the approach but not blocking the door, soot staining near chimney, warm forge accent light kept subtle.
```

Acceptance:

- Door remains visible and reachable.
- Forge identity is readable without labels.
- Tool clutter sits beside the work area, not across the only path.

### 3. `wolfpine_storehouse_facade_01`

Purpose: guarded supplies / famine pressure visual hook.

Prompt add-on:

```text
A sturdy guarded village storehouse facade, heavy timber, old stone foundation, practical double door or reinforced plank door, sacks and crates near the side wall, poor frontier settlement mood, believable storage architecture, no noble decoration.
```

Acceptance:

- Main door must be visible.
- Clutter must not hide or block the door.
- Should read as storage, not an inn or cottage.

### 4. `wolfpine_well_01`

Purpose: central square hotspot and party gathering focal point.

Prompt add-on:

```text
A weathered stone village well, low circular stone rim, simple timber crossbeam or small roof only if it does not dominate the silhouette, rope and bucket, moss and damp stone, readable from pseudo-isometric view, suitable as a central village square hotspot.
```

Acceptance:

- Must read as a well at small game scale.
- Should allow approach from multiple sides.
- Crossbeam/roof cannot obscure too much of the ground.

### 5. `wolfpine_market_stall_01`

Purpose: market identity and future merchant anchor.

Prompt add-on:

```text
A small frontier market stall with muted cloth awning, rough wooden counter, onions, dried fish, tallow candles, baskets, cloth bundles, low-fantasy village goods, customer-facing side clearly open, no readable text.
```

Acceptance:

- Must have a clear front/customer side.
- Should not be too wide to place along a path edge.
- Goods should add detail without noisy clutter.

### 6. `wolfpine_notice_board_01`

Purpose: quest board / village information hotspot.

Prompt add-on:

```text
A damp wooden village notice board on two posts, parchment scraps and guard seals visible as shapes only, no readable text, weathered timber, mud at base, suitable for a quest/news hotspot in a village square.
```

Acceptance:

- No readable words.
- Reads as notice board, not signpost or door.
- Has clear interaction side.

### 7. `wolfpine_door_heavy_01`

Purpose: reusable heavy door for inn/storehouse facades.

Prompt add-on:

```text
A heavy dark wooden medieval frontier door, iron hinges and latch, slightly arched or reinforced rectangular frame, worn threshold, pseudo-isometric angle matching a timber-and-plaster building facade, no surrounding full building.
```

Acceptance:

- Clearly reads as door.
- Larger than window assets.
- Perspective must align with facades.

### 8. `wolfpine_window_shuttered_01`

Purpose: reusable village facade window.

Prompt add-on:

```text
A small shuttered timber village window with weathered wood frame, optional muted warm interior glow, sized clearly smaller than a door, suitable for plaster-and-timber buildings, pseudo-isometric facade angle, no full building.
```

Acceptance:

- Clearly reads as window.
- Cannot be confused with entry.
- Works on inn/cottage/storehouse variants.

### 9. `wolfpine_fence_segment_01`

Purpose: village boundary and path framing.

Prompt add-on:

```text
A rough timber fence segment, low frontier construction, uneven posts, weathered wood, moss and mud at the base, pseudo-isometric ground alignment, suitable for repeating along path edges.
```

Acceptance:

- Repeatable without obvious seams.
- Low enough not to hide important scene information.
- Ground alignment is clear.

### 10. `wolfpine_firewood_stack_01`

Purpose: forge/cottage clutter and warmth.

Prompt add-on:

```text
A stacked pile of split firewood beside a village building, rough logs, small chopping block optional, grounded contact shadow, low-fantasy practical prop, pseudo-isometric angle.
```

Acceptance:

- Reads at small scale.
- Does not look like a wall or barrier unless intentionally dense.
- Works beside cottages and blacksmith.

### 11. `wolfpine_barrel_01`

Purpose: repeated storage clutter.

Prompt add-on:

```text
A single weathered wooden barrel with iron bands, medieval village storage prop, pseudo-isometric view, muted colors, grounded contact shadow, no modern markings.
```

Acceptance:

- Small, reusable, clean silhouette.
- Can be grouped with crates/sacks.
- No label or text.

### 12. `wolfpine_crate_01`

Purpose: repeated storage clutter.

Prompt add-on:

```text
A weathered wooden crate, medieval frontier village storage prop, rough planks, muted brown wood, pseudo-isometric view, grounded contact shadow, no markings or readable text.
```

Acceptance:

- Perspective matches ground plane.
- Works alone or stacked.
- Not too clean or modern.

### 13. `wolfpine_grass_clump_01`

Purpose: edge blending and ground variation.

Prompt add-on:

```text
A small irregular clump of natural green weeds and grass for a damp frontier village path edge, painterly pre-rendered look, soft transparent-friendly edges, pseudo-isometric ground view.
```

Acceptance:

- Natural muted green, not neon.
- Soft enough to blend with paths.
- Repeatable without obvious pattern.

### 14. `wolfpine_mud_rut_decal_01`

Purpose: road direction and ground blending.

Prompt add-on:

```text
A muddy wheel-rut ground decal for a medieval village road, damp brown mud, shallow wagon tracks, painterly texture, transparent-friendly feathered edges, pseudo-isometric ground alignment.
```

Acceptance:

- Supports path direction.
- Does not look like a hard-edged sticker.
- Can overlay dirt/cobble/grass edges.

### 15. `wolfpine_branch_occluder_01`

Purpose: foreground depth framing.

Prompt add-on:

```text
A foreground pine branch and needle cluster used as a soft occluder for a pseudo-isometric CRPG scene edge, muted green pine needles, dark branch, slightly larger and softer than normal props, no trunk or full tree, no background scene.
```

Acceptance:

- Clearly foreground layer material.
- Must not cover required doors or hotspots when used.
- Should frame scene edges without visual clutter.

## Production note

After generation, assets should be normalized through the same cleanup pass:

1. Crop with margin.
2. Clean background or mask.
3. Add/normalize alpha if needed.
4. Match Wolfpine color grade.
5. Normalize contact shadow.
6. Save to intended kit path.
7. Record final source/license/generation notes in the manifest or a dedicated asset ledger.
