# NG Presentation Plan

## Goal

Move the current playable prototype from a debug board toward an original BG2-like pseudo-isometric CRPG presentation.

This does not mean copying Baldur's Gate 2 assets or exact proprietary style. It means using the same functional presentation ideas:

- dense 2D area plates
- pseudo-isometric camera language
- invisible walkable/blocked areas
- small readable party/NPC sprites
- framed dialogue and quest UI
- portrait-driven conversations
- authored hotspots and area transitions

## Current presentation state

Implemented:

- code-drawn pseudo-isometric Wolfpine Road placeholder
- dark CRPG-style runtime UI theme helper
- framed dialogue panel
- framed quest tracker panel
- styled buttons and labels
- asset candidate assessment
- initial asset ledger

Still placeholder/debug:

- actor buttons still show `@ actor_id`
- party is still `◆ party`
- hotspots are visible buttons
- no portraits yet
- no inventory UI yet
- no real area background PNG yet
- no walkmask/occlusion mask yet

## Visual direction

Original low-fantasy frontier CRPG:

- rain-dark border roads
- pine forests
- old imperial stones
- moss, mud, bronze, iron, parchment
- muted greens/browns/gray-blue shadows
- warm lantern and candle accents
- grounded silhouettes, not glossy heroic fantasy

## Layering model

Each authored area should eventually use:

```text
background.png     painted/pseudo-isometric base area plate
walkmask.png       white/black or polygon data for walkable space
occlusion.png      foreground objects drawn above actors
hotspots.json      inspect/use/talk/exit triggers
actors.json        NPC/enemy/party placement
ambient.json       optional sound/weather/light cues
```

## Transition path from current prototype

### Step 1 — Better placeholders

- Replace flat actor buttons with small portrait/sprite markers.
- Keep invisible data IDs internally.
- Make hotspots optional debug overlays.
- Add a debug toggle later.

### Step 2 — First real UI pass

- Add dialogue portrait slot.
- Add speaker nameplate.
- Add quest tracker frame.
- Add bottom command/log bar.
- Add simple party portrait strip.

### Step 3 — First area art pass

- Generate or assemble a Wolfpine Road background plate.
- Downscale and clean it for low-spec use.
- Add matching walkmask and occlusion stub.
- Keep the code-drawn isometric map as fallback/debug.

### Step 4 — First sprites

- Party marker becomes a small standing adventurer sprite.
- Captain Renna becomes a small guard-captain sprite.
- Border bandit becomes a small enemy sprite.
- Keep labels hidden unless debug overlay is enabled.

### Step 5 — Asset import discipline

- Use Kenney/OpenGameArt/itch/free sources only after license review.
- Record every imported or generated asset in `assets/ledger/assets.json`.
- Prefer small coherent sets over large mixed-style dumps.

## Next recommended presentation task

Create a party/NPC marker system:

- `Sprite2D` or `TextureRect` markers with generated/project-owned SVG or PNG placeholders.
- actor name label on hover/selection, not always visible.
- visible debug mode can still show IDs.

This will make the game feel less like a form UI while keeping the current data-driven interaction system.
