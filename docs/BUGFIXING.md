# NG Bugfixing Guide

## Goal

Make bugs diagnosable from files and automated checks as much as possible, so the user does not always need to run the game and send screenshots.

## Best bugfixing strategy

1. Keep systems small and data-driven.
2. Validate all JSON and references before runtime.
3. Add deterministic sample test data.
4. Add debug logs to clear text files later.
5. Keep save files readable JSON during early development.
6. Use placeholder assets with metadata so missing art does not break prototypes.

## Validation command

Run from repo root:

```bash
python tools/validate_project.py
```

The script currently checks:

- JSON syntax
- duplicate IDs
- common referenced files

## Future validation checks to add

- Dialogue `next` node references exist.
- Quest stages referenced by dialogue effects exist.
- Actor IDs placed in areas exist.
- Encounter IDs referenced in areas exist.
- Item IDs in inventory/loadouts exist.
- Faction IDs referenced by actors/quests exist.
- Required placeholder assets exist.

## Debug-friendly formats

Use JSON for:

- save games during early development
- game state dumps
- party state
- quest state
- faction reputation
- loaded area state

Use text logs for:

- boot sequence
- data-load failures
- dialogue effects
- quest stage changes
- combat turn history

## Recommended local debug files later

These should be generated locally and ignored by Git:

```text
logs/latest_boot.log
logs/latest_area_load.log
logs/latest_combat.log
logs/latest_dialogue.log
saves/debug_save.json
```

## Screenshot minimization

Screenshots are useful for UI/art/layout bugs, but most logic bugs should be reproducible from:

- exact Git commit
- save JSON
- debug log
- validation output

## Bug report template

```text
Repo commit:
What I expected:
What happened:
Steps to reproduce:
Relevant save/log:
Relevant screenshot if visual:
```

## AI agent rule

When fixing a bug, first check whether validation could have caught it. If yes, update validation too.
