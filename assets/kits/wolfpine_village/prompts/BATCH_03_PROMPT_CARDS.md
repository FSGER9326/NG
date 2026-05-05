# Wolfpine Village Batch 03 Prompt Cards

These are ready-to-copy generation cards for the third Wolfpine Village reusable asset batch.

Batch 03 focuses on finishing assets: ground blending, road decals, and controlled foreground depth. These assets should improve final scene cohesion without hiding doors, exits, hotspots, or walkable paths.

Source manifest:

```text
data/asset_batches/wolfpine_village_batch_03.json
```

Exporter:

```bash
python tools/export_asset_batch_prompts.py data/asset_batches/wolfpine_village_batch_03.json
```

## Shared style lock

Use this lock for every Batch 03 prompt:

```text
Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.
```

## Shared negative prompt

```text
pixel art, front-facing flat perspective, inconsistent camera angle, unreadable silhouette, no contact shadow, modern materials, glossy heroic fantasy, horror-dark lighting, readable text, labels, signs with words, UI, impossible architecture, stairs to windows, blocked doors, full scene background, characters, monsters, hard rectangular decal edge, neon green vegetation, foreground object covering doors, foreground object covering exits
```

---

## `wolfpine_grass_clump_01`

Target:

```text
assets/kits/wolfpine_village/vegetation/wolfpine_grass_clump_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_grass_clump_01
Target file: assets/kits/wolfpine_village/vegetation/wolfpine_grass_clump_01.png

Asset-specific requirements:
Small village-edge grass and weed clump for damp low-fantasy settlement paths, muted natural greens, muddy root base, soft irregular silhouette, transparent-ready isolated asset, low contrast, repeatable without obvious pattern, for blending path edges and wall bases rather than blocking movement.

Production requirements:
- isolated reusable asset, not a full scene
- transparent-ready soft edges
- low profile, not a collision object by default
- repeatable without obvious seams or cloned patterning
- no flowers or saturated fantasy colors
- no characters, creatures, UI, or text
- suitable for blending mud, cobble, wall bases, and road edges in a 1280x720 Wolfpine Village plate
```

Review gate:

- [ ] Blends with mud and cobble edges.
- [ ] Not too contrasty at game scale.
- [ ] Can repeat without obvious pattern.
- [ ] Does not imply collision unless densely clustered.

---

## `wolfpine_mud_rut_decal_01`

Target:

```text
assets/kits/wolfpine_village/decals/wolfpine_mud_rut_decal_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_mud_rut_decal_01
Target file: assets/kits/wolfpine_village/decals/wolfpine_mud_rut_decal_01.png

Asset-specific requirements:
Transparent-ready muddy wheel rut ground decal for wagon-worn village road, damp brown mud, subtle puddle sheen, irregular soft edges, pseudo-isometric ground-plane alignment, decal-like top-down painted texture that supports path direction without obscuring walkability, no hard rectangular boundary.

Production requirements:
- isolated reusable ground decal, not a full scene
- transparent-ready irregular soft edge
- aligned to the pseudo-isometric village ground plane
- subtle enough to sit under gameplay markers and actors
- no hard rectangular crop line
- no text, no UI, no modern tire marks
- usable over dirt, mud, and cobble road bases
```

Review gate:

- [ ] Works over cobble, dirt, and road bases.
- [ ] Does not look like a hard-edged sticker.
- [ ] Supports path direction visually.
- [ ] Does not obscure walkability readability.

---

## `wolfpine_branch_occluder_01`

Target:

```text
assets/kits/wolfpine_village/occluders/wolfpine_branch_occluder_01.png
```

Prompt:

```text
Create one reusable canonical asset for the NG CRPG project.

Original classic pre-rendered pseudo-isometric CRPG asset, fixed 3/4 isometric camera, painted/pre-rendered look, not pixel-art, grounded low-fantasy frontier village, muted natural earth colors, warm late-afternoon or soft overcast daylight, readable contact shadow, dark timber, old stone, weathered plaster, moss, mud, cobble, no UI, no text.

Asset ID: wolfpine_branch_occluder_01
Target file: assets/kits/wolfpine_village/occluders/wolfpine_branch_occluder_01.png

Asset-specific requirements:
Foreground pine branch occluder for classic CRPG village scene edge framing, dark green pine needles, rough branch bark, slightly softer focus than gameplay objects, transparent-ready isolated foreground element, asymmetrical edge silhouette, subtle warm daylight rim, meant for screen corners and upper foreground only.

Production requirements:
- isolated reusable foreground occluder, not a ground prop
- transparent-ready silhouette with natural gaps between needles and branches
- slightly softer focus than buildings and props
- suitable for top or side screen-edge framing
- must not be dense enough to hide required doors, exits, characters, or hotspots
- no text, no UI, no creatures, no full tree trunk
```

Review gate:

- [ ] Looks like a foreground element, not a ground prop.
- [ ] Soft enough to avoid distracting from gameplay.
- [ ] Does not cover important interaction points.
- [ ] Can frame scene edges and add depth without hiding doors or exits.
