# Wolfpine Village First Priority Asset Prompts

These are the tracked prompt cards for the first production candidates from `data/asset_kits/wolfpine_village_starter.json`.

Use these before generating or sourcing art. After a candidate is produced, evaluate it against the acceptance checks here, then update the manifest status only after cleanup and source/license notes are recorded.

## Global style lock

Use this common style lock for all five first-priority assets:

```text
Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.
```

## Global negative constraints

Reject/regenerate if the result has:

- pixel-art rendering
- flat front-facing perspective
- inconsistent camera angle
- unreadable silhouette at game scale
- no contact shadow
- modern materials or objects
- glossy heroic-fantasy look
- horror-dark lighting for village exterior assets
- readable text or UI
- impossible architecture
- stairs to windows
- doors blocked by props

---

## 1. `wolfpine_inn_facade_01` — The Pine Hearth Inn Facade

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: The Pine Hearth Inn Facade
Asset ID: wolfpine_inn_facade_01
Category: buildings
Style family: Wolfpine village
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement asset, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow
Materials: dark timber, old stone, weathered plaster, moss, mud, cobble, muted natural colors

Create a larger two-story frontier inn facade called The Pine Hearth in concept only, but with no readable text. Timber frame, tan plaster, old stone lower foundation, mossy slate and muted clay roof elements, one clearly visible ground-level main door facing the viewer's lower-right side, small shuttered windows, subtle warm window glow, lived-in but poor border village character.

Requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent ground plane and contact shadow
- no text, no UI
- no modern objects
- suitable for assembly into a 1280x720 village background plate
- at least one clearly visible ground-level door
- windows clearly read as windows, not doors
- door approach remains free of blocking props
```

Acceptance checks:

- [ ] Ground-level door is readable.
- [ ] Door is not blocked by barrels, railings, stairs, or props.
- [ ] Windows cannot be mistaken for doors.
- [ ] Roof and foundation are structurally believable.
- [ ] Facade can be reused in more than one village scene.

---

## 2. `wolfpine_blacksmith_facade_01` — Wolfpine Blacksmith Facade

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: Wolfpine Blacksmith Facade
Asset ID: wolfpine_blacksmith_facade_01
Category: buildings
Style family: Wolfpine village
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement asset, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow
Materials: dark timber, old stone, weathered plaster, soot-stained chimney, muted natural colors

Create a practical blacksmith forge facade, timber and stone, low-fantasy frontier construction, clear ground-level door, chimney, forge awning or side work bay, anvil/workbench/tool silhouettes placed beside the approach but not blocking the door, soot staining near chimney, subtle warm forge accent light.

Requirements:
- isolated reusable asset, not a full scene
- clear ground-level door
- forge clutter beside the work area, not across the path
- no text, no UI
- no modern objects
- suitable for assembly into a 1280x720 village background plate
```

Acceptance checks:

- [ ] Door remains visible and reachable.
- [ ] Forge identity is readable without labels.
- [ ] Tool clutter sits beside the work area, not across the only path.
- [ ] No stairs or platforms lead to invalid windows.

---

## 3. `wolfpine_storehouse_facade_01` — Guarded Storehouse Facade

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: Guarded Storehouse Facade
Asset ID: wolfpine_storehouse_facade_01
Category: buildings
Style family: Wolfpine village
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement asset, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow
Materials: heavy timber, old stone foundation, reinforced plank doors, muted natural colors

Create a sturdy guarded village storehouse facade, heavy timber, old stone foundation, practical double door or reinforced plank door, sacks and crates near the side wall, poor frontier settlement mood, believable storage architecture, no noble decoration.

Requirements:
- isolated reusable asset, not a full scene
- visible main door
- storage identity visible from silhouette and side props
- side clutter must not block the door
- no text, no UI
- no modern objects
- suitable for assembly into a 1280x720 village background plate
```

Acceptance checks:

- [ ] Main door is visible.
- [ ] Clutter does not hide or block the door.
- [ ] Building reads as storage, not an inn or cottage.
- [ ] Building has believable foundation and roof support.

---

## 4. `wolfpine_well_01` — Stone Village Well

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: Stone Village Well
Asset ID: wolfpine_well_01
Category: props
Style family: Wolfpine village
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement prop, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow
Materials: damp old stone, moss, dark timber, rope, bucket, muted natural colors

Create a weathered stone village well, low circular stone rim, simple timber crossbeam or small roof only if it does not dominate the silhouette, rope and bucket, moss and damp stone, readable from pseudo-isometric view, suitable as a central village square hotspot.

Requirements:
- isolated reusable asset, not a full scene
- approachable from multiple sides
- compact enough for a central square
- no text, no UI
- no modern objects
- suitable for assembly into a 1280x720 village background plate
```

Acceptance checks:

- [ ] Reads as a well at small game scale.
- [ ] Allows approach from multiple sides.
- [ ] Crossbeam/roof does not obscure too much ground.
- [ ] Has usable contact shadow.

---

## 5. `wolfpine_market_stall_01` — Village Market Stall

```text
Create one reusable canonical asset for the NG CRPG project.

Asset: Village Market Stall
Asset ID: wolfpine_market_stall_01
Category: props
Style family: Wolfpine village
Camera: fixed pseudo-isometric 3/4 classic CRPG view
Look: original painted/pre-rendered classic CRPG settlement prop, not pixel-art
Lighting: soft warm late-afternoon daylight from upper-left, readable contact shadow
Materials: rough wood, muted cloth awning, baskets, onions, dried fish, tallow candles, cloth bundles, muted natural colors

Create a small frontier market stall with muted cloth awning, rough wooden counter, onions, dried fish, tallow candles, baskets, cloth bundles, low-fantasy village goods, customer-facing side clearly open, no readable text.

Requirements:
- isolated reusable asset, not a full scene
- clear front/customer side
- compact enough to place along a path edge
- awning does not hide critical interaction points
- no text, no UI
- no modern objects
- suitable for assembly into a 1280x720 village background plate
```

Acceptance checks:

- [ ] Has a clear front/customer side.
- [ ] Not too wide to place along a path edge.
- [ ] Goods add detail without noisy clutter.
- [ ] Footprint is easy to block in collision.

## Candidate cleanup checklist

For every generated candidate:

- [ ] Crop with margin.
- [ ] Clean background or mask.
- [ ] Add/normalize alpha if needed.
- [ ] Match Wolfpine color grade.
- [ ] Normalize contact shadow.
- [ ] Save to the manifest's intended path or record a replacement path.
- [ ] Record source/license/generation notes.
- [ ] Update `data/asset_kits/wolfpine_village_starter.json` status only after review.
