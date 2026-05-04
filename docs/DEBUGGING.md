# NG Debugging and Test Harness

## Goal

Make bug reports reproducible from text logs and scripted tests, so the user can run one command, upload the bundle, and let an AI assistant inspect what happened.

## User workflow

From the repository root, run:

```bat
tools\collect_debug_bundle.bat
```

This creates:

```text
debug\NG_debug_latest.zip
```

Upload that zip to ChatGPT for analysis.

## What the bundle contains

Expected files include:

```text
validation.log
scenario.log
game.log
actions.jsonl
state_initial.json
state_latest.json
state_after_scenario.json
git_commit.txt
git_status.txt
```

## Important files

### Human-readable log

```text
game.log
```

Example style:

```text
[0000.120] AREA: Loading area: wolfpine_road
[0000.240] DIALOGUE: Opened dialogue dialogue/npcs/captain_renna.json
[0000.310] QUEST: missing_caravan not_started -> accepted
```

### Machine-readable action log

```text
actions.jsonl
```

Each line is JSON. This is easier for AI/tools to parse.

### State dumps

```text
state_initial.json
state_latest.json
state_after_scenario.json
```

These contain current area, player position, quests, flags, actors, and hotspots.

## Scripted scenario tests

Scenario definitions live in:

```text
tests/scenarios/
```

Current scenario:

```text
tests/scenarios/wolfpine_missing_caravan.json
```

It verifies this flow:

1. Load Wolfpine Road.
2. Click Captain Renna.
3. Choose `I am looking for work.`
4. Assert `missing_caravan: accepted`.
5. Click Old Road Shrine.
6. Assert `missing_caravan: found_wreck`.
7. Assert `wolfpine_old_shrine_inspected == true`.

## GitHub Actions integration

The Godot smoke workflow now also runs the scripted Wolfpine scenario and uploads debug logs:

```text
.github/workflows/godot-smoke.yml
```

## Logging architecture

Core logger:

```text
game/scripts/core/game_log.gd
```

State dump helper:

```text
game/scripts/core/debug_state_dump.gd
```

Scenario runner:

```text
tools/run_scenario_test.gd
```

User scripts:

```text
tools/run_debug_tests.bat
tools/collect_debug_bundle.bat
```

## Logging rules for future development

Every important system should log through `GameLog`:

- area load
- actor placement
- hotspot placement
- player input
- dialogue open/node/choice
- quest stage changes
- flag changes
- faction reputation changes
- inventory changes later
- combat turn/action/hit/damage/death later
- save/load later

## Bugfixing rule

When a bug is fixed, ask:

> Could a validation check or scenario test have caught this?

If yes, add or update the test.
