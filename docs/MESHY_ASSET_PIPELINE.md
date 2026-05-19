# Meshy Asset Pipeline

This document defines how NG should use Meshy API output for the enhanced classic pre-rendered pseudo-isometric CRPG art target.

## Core rule

Meshy output is source material, not final game art.

For NG, the efficient path is:

```text
Meshy single-object 3D source
-> local GLB archive and metadata
-> Blender orthographic 2.5D render pass
-> transparent PNG frames or sheets
-> manifest, scorecard, and in-engine review
-> promoted kit asset
```

## Why this route

Meshy is strongest when it produces one clear 3D object from a focused prompt or from 2-4 clean views of the same object. It is weak as a way to generate a whole 2D area, a multi-object prop sheet, or precise tile modules in one call.

Use batches for throughput, not multi-object prompts.

## Meshy lane selection

Use Text-to-3D preview for:

- barrels, crates, sacks, firewood, rubble
- simple village or dungeon props
- fast silhouette exploration

Use Image-to-3D or Multi-Image-to-3D for:

- hero props with important proportions
- carts, wells, market stalls, shrine arches
- humanoids or creatures that need controlled front/side/back form

Use Retexture for:

- wet/dry variants
- faction variants
- damaged/aged variants
- palette harmonization after a mesh is good

Use Rigging and Animation only for:

- clear biped humanoids in A-pose or T-pose
- textured models below the face-count limit
- assets that will be rendered into 8-direction action sheets

Do not use Meshy for:

- exact wall/floor/stair snap modules
- full area plates
- multi-object sheets
- readable signs or text-bearing props
- precise mechanical parts

## Prompt contract

Base style lock:

```text
single complete reusable game prop, original enhanced classic pre-rendered pseudo-isometric CRPG asset, grounded low-fantasy frontier village, muted earth palette, old timber, worn stone, iron, moss, mud, soft upper-left daylight, clean silhouette, centered object, no scene background, no characters, no UI, no readable text, not pixel art, not cartoon, not glossy heroic fantasy
```

Prompt shape:

```text
A single [object type], [3-6 concrete physical details], practical low-fantasy [location/category] prop, centered, full object visible.
```

Keep prompts physical. Avoid abstract mood, magic effects, smoke, sparks, tiny hair/fibers, scene descriptions, and multiple asset lists.

## Credit discipline

Default probe batch:

```powershell
python tools\meshy_batch.py --config data\asset_pipeline\meshy_wolfpine_probe.json plan
```

Expected Meshy-6 costs from the current API pricing:

- Text-to-3D preview: 20 credits per asset
- Text-to-3D refine: 10 credits per asset
- Remesh: 5 credits when used separately
- Retexture: 10 credits
- Auto-rig: 5 credits
- Animation: 3 credits

For the six-asset probe:

```text
preview all: 120 credits
refine all: +60 credits
```

Refine only assets whose preview mesh has a useful silhouette.

## Commands

Set the key only in the local shell:

```powershell
$env:MESHY_API_KEY = "msy_..."
```

Check credit balance:

```powershell
python tools\meshy_batch.py --config data\asset_pipeline\meshy_wolfpine_probe.json balance
```

Submit preview tasks:

```powershell
python tools\meshy_batch.py --config data\asset_pipeline\meshy_wolfpine_probe.json submit-previews
```

Watch preview tasks:

```powershell
python tools\meshy_batch.py --config data\asset_pipeline\meshy_wolfpine_probe.json watch-previews
```

Submit texture/refine tasks:

```powershell
python tools\meshy_batch.py --config data\asset_pipeline\meshy_wolfpine_probe.json submit-refines
```

Watch, download, and archive refined GLBs:

```powershell
python tools\meshy_batch.py --config data\asset_pipeline\meshy_wolfpine_probe.json watch-refines
```

Render downloaded GLBs through Blender:

```powershell
python tools\meshy_batch.py --config data\asset_pipeline\meshy_wolfpine_probe.json render
```

Raw Meshy downloads go under:

```text
asset_sources/raw/meshy/
```

That path is ignored. Do not commit raw Meshy sources unless a promotion task explicitly calls for a reviewed source archive.

Rendered candidates go under:

```text
assets/generated/meshy_wolfpine_probe_01/
```

## Local toolchain

Required:

- Python 3.12
- Blender 5.1
- Pillow
- requests/http client support
- ImageMagick
- Oxipng
- Godot 4.3 for local visual QA

Useful:

- `gltf-transform` for GLB inspection and optimization
- GIMP or Krita for manual alpha/paintover cleanup
- Tiled for scene assembly review

## Review gate

Before promotion, every Meshy-derived candidate needs:

- source prompt and task metadata
- downloaded GLB retained locally
- Blender 2.5D PNG render
- true RGBA transparency
- scale check against player/NPC marker
- contact shadow and halo review
- scorecard result
- target-area or kit-context review
