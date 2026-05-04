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
- [x] Area transition stub/debug output

## Milestone 0.3 — Dialogue and quest prototype

- [x] Dialogue UI prototype
- [x] Dialogue node navigation
- [x] Quest start effect debug handling
- [ ] Quest stage update stored in game state
- [ ] Flag checks
- [ ] Skill check format

## Milestone 0.4 — Combat prototype

- [ ] Combat scene
- [ ] Party and enemy placement
- [ ] Turn queue
- [ ] AP spending
- [ ] Melee attack
- [ ] Victory/defeat result

## Milestone 0.5 — First playable module

- [ ] Wolfpine Road playable
- [ ] Wolfpine Village stub
- [ ] Collapsed Crypt stub
- [ ] One companion recruitable
- [ ] One quest completable

## Next target

Test the current Godot state. If it launches, the next practical task is storing quest state in `GameState` and wiring dialogue effects into that state rather than only printing debug text.

## Always update this file when scope changes.
