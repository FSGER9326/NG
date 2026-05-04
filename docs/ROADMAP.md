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
- [ ] Skill check format

## Milestone 0.4 — Frontend shell

- [x] Main menu shell
- [x] New Game starts character creator
- [x] Character creator first pass: name, origin, archetype
- [x] Start Journey launches current area prototype
- [x] Save/Load menu placeholders
- [ ] Save game format
- [ ] Load game flow
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

### Area transition path

1. Start a new game.
2. Click `North Road` on Wolfpine Road.
3. Wolfpine Village should load.

## Next target

Stabilize the menu/new-game/area-transition flow, then add save/load and a simple skill-check format.

## Always update this file when scope changes.
