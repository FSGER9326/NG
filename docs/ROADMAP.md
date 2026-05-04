# NG Roadmap

## Current goal

Build a low-spec, pseudo-isometric, party-based CRPG that is easy for AI tools to inspect, edit, validate, and extend.

## Milestone 0.1 — Repository skeleton

- [x] README
- [x] Godot project config
- [x] Main scene
- [x] Bootstrap data loader
- [x] Starter JSON content
- [x] Validation script
- [x] Art bible
- [x] Game design document

## Milestone 0.2 — Area prototype

- [x] Area scene controller
- [x] Background loading placeholder
- [x] Actor placement from JSON
- [x] Click-to-move prototype
- [x] Hotspot inspection
- [x] Real area transition support

## Milestone 0.3 — Dialogue and quest prototype

- [x] Dialogue UI prototype
- [x] Dialogue node navigation
- [x] Quest start effect stored in game state
- [x] Quest stage update stored in game state
- [x] Basic flag-setting effect
- [x] Reusable dialogue flag and quest-stage checks
- [x] Dialogue condition validation
- [x] Skill check format

## Milestone 0.4 — Frontend shell

- [x] Main menu shell
- [x] New Game starts character creator
- [x] Character creator first pass: name, origin, archetype
- [x] Start Journey launches current area prototype
- [x] Save/Load menu placeholders
- [x] Save game format
- [x] Load game flow
- [ ] Character stats and portrait selection

## Milestone 0.5 — Combat prototype

- [ ] Combat scene
- [ ] Party and enemy placement
- [ ] Turn queue
- [ ] AP spending
- [ ] Melee attack
- [ ] Victory/defeat result

## Milestone 0.6 — First playable module

- [ ] Wolfpine Road playable
- [x] Wolfpine Village stub
- [x] Wolfpine Village art brief and layout constraints
- [ ] Wolfpine Village final background plate
- [ ] Collapsed Crypt stub
- [ ] One companion recruitable
- [ ] One quest completable

## Current first playable test paths

### Boot and new-game path

1. Launch the game in Godot.
2. Main menu should appear.
3. Choose `New Game`.
4. Character creator should appear.
5. Enter a name, choose origin/archetype, and choose `Start Journey`.
6. Wolfpine Road prototype should load.

### Basic quest path

1. Start a new game.
2. Click `@ captain_renna`.
3. Choose the work dialogue option.
4. Quest tracker should show `missing_caravan: accepted`.
5. Click `Old Road Shrine`.
6. Quest tracker should show `missing_caravan: found_wreck`.

### Flag-gated dialogue path

1. Click `Old Road Shrine`.
2. Click `@ captain_renna`.
3. The dialogue choice `I found fresh wagon ruts by the old shrine.` should be visible.
4. Choose it.
5. Quest tracker should show `missing_caravan: reported_clue`.

### Skill-gated dialogue path

1. Start a new game.
2. Click `@ captain_renna`.
3. The perception-gated dialogue choice `You look like you expected the caravan to vanish.` should be visible with the starter party's perception value.
4. Choosing it should open Renna's pressure-read branch.

### Save/load path

1. Start a new game from the main menu.
2. Create a character profile.
3. Load Wolfpine Road.
4. Accept `missing_caravan` from Captain Renna.
5. Save the game.
6. Load the game.
7. Confirm the profile, current area, and quest stage are restored.

### Area transition path

1. Start a new game.
2. Click `North Road` on Wolfpine Road.
3. Wolfpine Village should load.

## Art-generation path for Wolfpine Village

1. Use `areas/wolfpine_village/layout_constraints.json` as the source of truth for walkable zones, required paths, doors, stairs, hotspots, and NPC zones.
2. Use `areas/wolfpine_village/ART_BRIEF.md` for the visual target and rejection checklist.
3. Generate or kitbash the village from the layout, not the other way around.
4. Reject final art with hidden doors, stairs to windows, blocked paths, disconnected roads, or horror-dark village lighting.
5. After final art is accepted, create matching background, occlusion, walkmask/collision, hotspot, and actor overlays.

## Next target

Stabilize the menu/new-game/area-transition/save-load flow, then add character stats and portrait selection. For art, the next target is a Wolfpine Village background plate generated from the checked art brief and layout constraints.

## Always update this file when scope changes.
