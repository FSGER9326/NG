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

## Current first playable loop

Opening the project in Godot and pressing Play should instantiate the Wolfpine Road prototype.

Expected behavior:

- A dark placeholder background appears.
- The Wolfpine Road title/debug label appears.
- A visible `◆ party` marker appears.
- Clicking the ground moves the party marker directly toward the clicked point.
- Hotspot buttons appear for the old shrine and north road.
- Actor buttons appear for `captain_renna` and `border_bandit`.
- Clicking the old shrine updates debug text with inspection text.
- Clicking the north road updates debug text with the target area stub.
- Clicking `captain_renna` opens a simple JSON-driven dialogue panel.
- Dialogue choices can move between nodes.
- Dialogue quest effects currently print debug output but are not yet stored in `GameState`.

## Current priority

Test the current Godot launch state and fix any runtime errors.

Next useful tasks:

1. Test player click-to-move.
2. Test Captain Renna dialogue.
3. Fix any GDScript runtime errors found on launch/click.
4. Store quest state in `GameState` / `QuestSystem` instead of only printing debug text.
5. Add flag checks and simple skill-check format to dialogue JSON.
6. Keep improving `tools/validate_project.py` whenever a bug could have been caught by validation.

## Validation

Run from repo root:

```bash
python tools/validate_project.py
```

GitHub Actions also runs validation on push and PR.

## Working rule

If a future AI chat loses context, read this file first, then `docs/ROADMAP.md`, `docs/GAME_DESIGN.md`, `docs/WORKFLOW.md`, `docs/BUGFIXING.md`, and `docs/ASSET_POLICY.md`.
