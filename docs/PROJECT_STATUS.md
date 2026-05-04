# NG Project Status

This file is the main handoff point for future chats and AI agents.

## Current project identity

- Repo: `FSGER9326/NG`
- Working title: **NG / New Game**
- Genre: low-spec pseudo-isometric party CRPG
- Engine target: Godot 4.x, 2D, Compatibility renderer
- Main implementation style: text-first, data-driven, AI-maintainable

## Design target

Original dark low-fantasy CRPG with:

- detailed pseudo-isometric 2D areas
- party companions
- branching dialogue
- quest consequences
- faction reputation
- turn-based AP combat first
- extendable content files

## Current technical state

The repo currently contains:

- Godot project config
- main scene wired to instantiate the area prototype
- bootstrap script
- JSON data loader
- game-state stub
- quest-system stub
- `AreaController` scene/script prototype
- starter area: `wolfpine_road`
- starter NPC: `captain_renna`
- starter companion: `brannoc`
- starter enemy: `border_bandit`
- starter item: `border_iron_sword`
- starter quest: `missing_caravan`
- validation script: `tools/validate_project.py`
- GitHub Action: `.github/workflows/validate.yml`

## First testable state

Opening the project in Godot and pressing Play should now instantiate the Wolfpine Road prototype.

Expected behavior:

- A dark placeholder background appears.
- The Wolfpine Road title/debug label appears.
- Hotspot buttons appear for the old shrine and north road.
- Actor markers appear for `captain_renna` and `border_bandit`.
- Clicking the old shrine updates debug text with inspection text.
- Clicking the north road updates debug text with the target area stub.

## Current priority

Finish Milestone 0.2 and move into Milestone 0.3.

Next useful tasks:

1. Test the current Godot launch state.
2. Fix any Godot/GDScript syntax/runtime errors found on launch.
3. Add click-to-move placeholder behavior.
4. Add simple dialogue panel that can read JSON dialogue.
5. Apply dialogue effects to start/update quests.
6. Keep improving `tools/validate_project.py` whenever a bug could have been caught by validation.

## Validation

Run from repo root:

```bash
python tools/validate_project.py
```

GitHub Actions now also runs validation on push and PR.

## Working rule

If a future AI chat loses context, read this file first, then `docs/ROADMAP.md`, `docs/GAME_DESIGN.md`, `docs/WORKFLOW.md`, `docs/BUGFIXING.md`, and `docs/ASSET_POLICY.md`.
