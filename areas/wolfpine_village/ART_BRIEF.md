# Wolfpine Village Art Brief

## Purpose

Wolfpine Village is the first settlement hub after Wolfpine Road. It should prove that NG can support classic CRPG village areas with functional architecture, readable navigation, and reusable art-generation constraints.

This brief must be used before generating, kitbashing, painting over, or importing any final village background art.

## Gameplay purpose

- Receive the player from `wolfpine_road` through the south road entry.
- Provide a central village square for dialogue, quest updates, and future vendors.
- Visually introduce Wolfpine as a poor but inhabited border village, not a ruin or horror scene.
- Reserve clear access to future interiors: inn, blacksmith, storehouse, chapel path.
- Leave enough central space for party movement and possible future scripted encounters.

## Required composition

Canvas target: 1280x720.
Camera: fixed pseudo-isometric 3/4 classic CRPG view.

Required visible areas:

1. South road entry in the lower-left / lower side.
2. Central well and gathering square.
3. The Pine Hearth inn with a visible ground-level door.
4. Blacksmith forge with a visible ground-level door and readable forge identity.
5. Market stall that does not block the main path.
6. Notice board near the square.
7. North / chapel path exit in the upper-right.
8. Storehouse or guarded supply building as a future hook.

## Visual mood

Closer to Baldur's Gate 2 / Pillars-style classic CRPG settlement art than grim horror.

- Warm late-afternoon or soft overcast daylight.
- Natural greens, moss, grass, and flowers are allowed.
- Timber, stone, plaster, slate roof, clay roof, mud, and cobblestone should dominate.
- The village should feel poor, damp, and tense, but still lived-in.
- Use warm window/lantern accents sparingly.
- Keep interiors/crypts darker than the village exterior.

Avoid:

- Excessive darkness.
- Horror-only lighting.
- Pixel-art texture treatment.
- Cartoonish clean fantasy colors.
- Overly heroic high-fantasy architecture.
- Empty generated scenery without functional doors or paths.

## Wolfpine architecture kit

### Roofs

- Mossy gray slate for older buildings.
- Muted red-brown clay tile for the inn and market-facing structures.
- Sagging timber shingles for poorer cottages.

### Walls

- Whitewashed or tan plaster with exposed dark timber.
- Old stone lower foundations.
- Damp moss and dirt near ground contact.

### Doors

- Arched or heavy rectangular dark wood.
- Iron hinges and simple latches.
- Ground-level only unless an explicit platform and stair exist.
- Important doors may have a lantern, sign, or worn threshold.

### Windows

- Small leaded glass or shuttered windows.
- Windows must read as windows, not doors.
- Second-floor windows must clearly sit above ground level.

### Street and terrain

- Uneven cobblestone around the square.
- Mud and wagon ruts along road edges.
- Grass and weeds between stones.
- Rocks and old pine roots near the edges.

### Props

- Barrels, crates, sacks, firewood, buckets, covered baskets.
- Market cloth, dried fish, onions, tallow candles.
- Forge anvil, woodpile, coal, tools.
- Guard seals and damp notices on the board.

Props should add life and detail, but never block required routes or doors.

## Hard architectural constraints

The final art must obey `areas/wolfpine_village/layout_constraints.json`.

Mandatory rules:

- Every important building must have at least one visible ground-level door.
- Doors must touch or face a valid walkable zone.
- Stairs must connect valid elevations; no stairs to windows.
- Required paths must remain visually clear.
- The market stall must not block south road to well movement.
- Foreground roofs, trees, and awnings must not hide required hotspots.
- The chapel path and south road exits must be readable as exits.
- The well, notice board, inn door, blacksmith door, market stall, chapel path, and south road exit must all remain reachable.

## Suggested final art prompt

Classic pre-rendered isometric CRPG village square, fixed 3/4 pseudo-isometric camera, warm late-afternoon frontier settlement, detailed timber-frame houses with old stone foundations, mossy slate roofs, muted clay tiles, uneven cobblestone square, central stone well, market stall, blacksmith forge, inn, notice board, chapel path beyond pines, lived-in low-fantasy border village, natural greens and earth colors, warm windows and lantern accents, dense handcrafted detail, readable walkable paths, every important building has a visible ground-level door connected to the path, no stairs to windows, no blocked doors, no text, no UI.

## Negative prompt / rejection notes

Reject generated art if it has:

- Stairs ending at windows, walls, roofs, or nothing.
- Buildings with no ground-level doors.
- Doors hidden behind barrels, stalls, fences, trees, or roofs.
- Roads that stop without connecting.
- Windows that look like entry doors.
- Market stalls blocking the only main route.
- Inconsistent camera perspective.
- Pixel-art rendering when a painted/pre-rendered CRPG look was requested.
- Overly grim horror lighting for the village exterior.

## Review checklist

Before accepting final art:

- [ ] South road entry is visible and open.
- [ ] Path from south road to central well is clear.
- [ ] Path from well to inn door is clear.
- [ ] Path from well to blacksmith door is clear.
- [ ] Path from well to chapel path is clear.
- [ ] Inn has a visible ground-level door.
- [ ] Blacksmith has a visible ground-level door.
- [ ] Storehouse has a believable door even if not interactive yet.
- [ ] No stair leads to a window or dead roof edge.
- [ ] Notice board, well, market stall, doors, and exits are reachable.
- [ ] Foreground layers do not hide critical hotspots.
- [ ] There is room for at least four party members to gather near the well.
- [ ] Color and lighting are closer to classic CRPG settlement art than horror.
