# NG Bugfixing Guide

## Goal

Make bugs diagnosable from files and automated checks as much as possible, so the user does not always need to run the game and send screenshots.

## Best bugfixing strategy

1. Keep systems small and data-driven.
2. Validate all JSON and references before runtime.
3. Add deterministic sample test data.
4. Log every important gameplay action through `GameLog`.
5. Keep state dumps readable JSON during early development.
6. Use placeholder assets with metadata so missing art does not break prototypes.
7. Add scenario tests for every bug-prone quest/mechanic path.

## Validation command

Run from repo root:

```bash
python tools/validate_project.py
```

The script currently checks:

- JSON syntax
- duplicate IDs
- common referenced files

## Debug bundle command

Run from repo root:

```bat
tools\collect_debug_bundle.bat
```

This creates:

```text
debug\NG_debug_latest.zip
```

Upload that zip to ChatGPT for analysis.

## Debug harness docs

Full details are in:

```text
docs/DEBUGGING.md
```

## Important generated debug files

```text
debug/latest/validation.log
debug/latest/scenario.log
debug/latest/game.log
debug/latest/actions.jsonl
debug/latest/state_initial.json
debug/latest/state_latest.json
debug/latest/state_after_scenario.json
```

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

Use text/JSONL logs for:

- boot sequence
- data-load failures
- area loading
- input actions
- dialogue open/node/choice
- quest stage changes
- flag changes
- combat turn history later

## Screenshot minimization

Screenshots are useful for UI/art/layout bugs, but most logic bugs should be reproducible from:

- exact Git commit
- validation output
- game log
- action JSONL
- scenario result
- state dump

## Bug report template

```text
Repo commit:
What I expected:
What happened:
Steps to reproduce:
Relevant save/log/debug bundle:
Relevant screenshot if visual:
```

## AI agent rule

When fixing a bug, first check whether validation or a scenario test could have caught it. If yes, update validation or add a scenario test too.
