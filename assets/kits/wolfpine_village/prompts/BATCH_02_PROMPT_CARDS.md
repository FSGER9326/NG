# Wolfpine Village Batch 02 Prompt Cards

These are ready-to-copy generation cards for the second Wolfpine Village reusable asset batch.

Batch 02 focuses on modular architecture and clutter pieces that can repair generated facades, improve reuse, and dress village scenes without blocking required paths.

Source manifest:

```text
data/asset_batches/wolfpine_village_batch_02.json
```

Exporter:

```bash
python tools/export_asset_batch_prompts.py data/asset_batches/wolfpine_village_batch_02.json
```

## Shared style lock

Use this lock for every Batch 02 prompt:

```text
Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.
```

## Shared negative prompt

```text
pixel art, front-facing flat perspective, inconsistent camera angle, unreadable silhouette, no contact shadow, modern materials, glossy heroic fantasy, horror-dark lighting, readable text, labels, signs with words, UI, impossible architecture, stairs to windows, blocked doors, full scene background, characters, monsters
```

---

## `wolfpine_door_heavy_01`

Target:

```text
assets/kits/wolfpine_village/architecture/wolfpine_door_heavy_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_door_heavy_01
Target file: assets/kits/wolfpine_village/architecture/wolfpine_door_heavy_01.png

Asset-specific requirements:
Heavy dark wooden medieval frontier village door, iron strap hinges, small latch, damp lower edge, old timber planks, slight stone or mud threshold contact shadow, sized for ground-level inn or storehouse use, clearly a door and not a window, isolated architecture patch with transparent-ready margin.

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- suitable for repairing or reinforcing Wolfpine Village building facades
```

Review gate:

- [ ] Reads as a ground-level door, not a window.
- [ ] Perspective matches the village facades.
- [ ] Can be placed over a facade without looking pasted on.
- [ ] Has believable hinges/latch and grounded threshold shadow.

---

## `wolfpine_window_shuttered_01`

Target:

```text
assets/kits/wolfpine_village/architecture/wolfpine_window_shuttered_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_window_shuttered_01
Target file: assets/kits/wolfpine_village/architecture/wolfpine_window_shuttered_01.png

Asset-specific requirements:
Small shuttered village window for timber-and-plaster facade, dark wooden shutters, slightly uneven frame, optional faint warm interior glow, much smaller than a door, clearly non-walkable, isolated architecture patch with clean margin, Wolfpine damp moss and weathering.

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- suitable for repairing or reinforcing Wolfpine Village building facades
```

Review gate:

- [ ] Reads clearly as a window.
- [ ] Cannot be mistaken for a door or usable exit.
- [ ] Matches timber/plaster Wolfpine material language.
- [ ] Can repeat on facades without obvious pattern noise.

---

## `wolfpine_fence_segment_01`

Target:

```text
assets/kits/wolfpine_village/architecture/wolfpine_fence_segment_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_fence_segment_01
Target file: assets/kits/wolfpine_village/architecture/wolfpine_fence_segment_01.png

Asset-specific requirements:
Rough low timber fence segment for a poor frontier village, uneven dark wooden posts and rails, muddy base, moss and damp age, short modular length, repeatable edge piece for path framing, fixed pseudo-isometric angle, not a wall, not too visually heavy.

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- suitable for path-edge dressing without blocking required routes
```

Review gate:

- [ ] Repeats cleanly enough for path edges.
- [ ] Perspective matches the ground plane.
- [ ] Does not read as an impassable wall unless grouped densely.
- [ ] Works beside inn, forge, and village square edges.

---

## `wolfpine_firewood_stack_01`

Target:

```text
assets/kits/wolfpine_village/props/wolfpine_firewood_stack_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_firewood_stack_01
Target file: assets/kits/wolfpine_village/props/wolfpine_firewood_stack_01.png

Asset-specific requirements:
Small stacked firewood pile for a damp frontier village, split logs, simple rough stacking, dark wet bark, muted cut wood, light moss or mud at base, compact footprint, readable contact shadow, usable beside forge, inn service wall, or cottage.

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- small enough to dress buildings without blocking doors or hotspots
```

Review gate:

- [ ] Reads as firewood at small scale.
- [ ] Compact enough to sit beside buildings without blocking doors.
- [ ] Contact shadow grounds it to the pseudo-isometric plane.
- [ ] Works with blacksmith and cottage dressing.

---

## `wolfpine_barrel_01`

Target:

```text
assets/kits/wolfpine_village/clutter/wolfpine_barrel_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_barrel_01
Target file: assets/kits/wolfpine_village/clutter/wolfpine_barrel_01.png

Asset-specific requirements:
Weathered wooden barrel, damp dark staves, simple iron hoops, muddy base, pseudo-isometric view, small reusable clutter object, no labels or symbols, medieval frontier storage prop, clean silhouette and contact shadow, suitable for grouping near inn, storehouse, or market stall.

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- small enough for repeated controlled scene dressing
```

Review gate:

- [ ] Readable round barrel form in pseudo-isometric view.
- [ ] Small enough for repeated dressing.
- [ ] No readable markings or modern details.
- [ ] Can group with crates without visual clutter.

---

## `wolfpine_crate_01`

Target:

```text
assets/kits/wolfpine_village/clutter/wolfpine_crate_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_crate_01
Target file: assets/kits/wolfpine_village/clutter/wolfpine_crate_01.png

Asset-specific requirements:
Weathered wooden crate, rough plank construction, damp mossy edges, muddy contact shadow, pseudo-isometric view, medieval frontier storage prop, compact reusable clutter asset, no labels or text, can stack with sacks or barrels near storehouse and market edges.

Production requirements:
- isolated reusable asset, not a full scene
- clean readable silhouette
- consistent fixed pseudo-isometric 3/4 ground plane
- readable contact shadow from upper-left light
- enough margin for cleanup and alpha masking
- no text, no UI, no modern objects
- no characters baked into environment assets
- small enough for repeated controlled scene dressing
```

Review gate:

- [ ] Perspective matches the ground plane.
- [ ] Edges are readable but not pixel-sharp.
- [ ] No readable text or modern shipping marks.
- [ ] Works with barrel and storehouse clutter clusters.
