# NG Dialogue System

## Goal

Keep dialogue, quest branching, and world-state reactions data-driven so future quests are easy to write, validate, test, and debug.

## Runtime files

Core dialogue runtime currently lives in:

```text
game/scripts/area/area_controller.gd
game/scripts/dialogue/dialogue_condition_evaluator.gd
```

The area controller handles:

- opening dialogue
- entering nodes
- showing visible choices
- applying effects
- scenario-test hooks

The condition evaluator handles reusable condition logic.

## Dialogue file shape

Dialogue files live under:

```text
dialogue/
```

Basic shape:

```json
{
  "id": "captain_renna_intro",
  "speaker": "captain_renna",
  "start_node": "start",
  "nodes": {
    "start": {
      "text": "Dialogue text.",
      "choices": []
    }
  }
}
```

## Choices

Choices use:

```json
{
  "text": "I am looking for work.",
  "next": "work_offer"
}
```

`next` can be another node ID or `end`.

## Effects

Effects change game state.

Supported effects:

### Start quest

```json
{
  "type": "start_quest",
  "quest_id": "missing_caravan",
  "stage": "accepted"
}
```

### Set quest stage

```json
{
  "type": "set_quest_stage",
  "quest_id": "missing_caravan",
  "stage": "found_wreck"
}
```

### Set flag

```json
{
  "type": "set_flag",
  "flag_id": "wolfpine_old_shrine_inspected",
  "value": true
}
```

## Conditions

Conditions control whether a node or choice is available.

Conditions can be placed on:

- dialogue nodes
- dialogue choices

Example choice gated by a flag:

```json
{
  "text": "I found fresh wagon ruts by the old shrine.",
  "next": "shrine_found_report",
  "conditions": [
    {
      "type": "flag",
      "flag_id": "wolfpine_old_shrine_inspected",
      "value": true
    }
  ]
}
```

## Supported condition types

### Flag condition

Passes when a flag matches the expected boolean value.

```json
{
  "type": "flag",
  "flag_id": "wolfpine_old_shrine_inspected",
  "value": true
}
```

### Quest-stage condition

Passes when a quest is at a specific stage.

```json
{
  "type": "quest_stage",
  "quest_id": "missing_caravan",
  "stage": "found_wreck"
}
```

### Not condition

Passes when the nested condition fails.

```json
{
  "type": "not",
  "condition": {
    "type": "flag",
    "flag_id": "wolfpine_old_shrine_inspected",
    "value": true
  }
}
```

### All condition

Passes when every nested condition passes.

```json
{
  "type": "all",
  "conditions": [
    {
      "type": "flag",
      "flag_id": "wolfpine_old_shrine_inspected",
      "value": true
    },
    {
      "type": "quest_stage",
      "quest_id": "missing_caravan",
      "stage": "found_wreck"
    }
  ]
}
```

### Any condition

Passes when at least one nested condition passes.

```json
{
  "type": "any",
  "conditions": [
    {
      "type": "quest_stage",
      "quest_id": "missing_caravan",
      "stage": "found_wreck"
    },
    {
      "type": "quest_stage",
      "quest_id": "missing_caravan",
      "stage": "reported_clue"
    }
  ]
}
```

## Validation

The validator checks dialogue conditions:

```bash
python tools/validate_project.py
```

It catches:

- unknown condition types
- non-list `conditions`
- missing `flag_id`
- non-boolean flag values
- missing quest IDs
- missing quest stages
- malformed `not`, `all`, and `any` conditions

## Scenario testing

Scenario tests live in:

```text
tests/scenarios/
```

Use scenarios to prove branching behavior. Current flag-gated dialogue coverage includes:

```text
tests/scenarios/wolfpine_report_shrine_to_renna.json
```

## Authoring rule

When adding a new quest branch:

1. Add dialogue conditions in JSON.
2. Add effects in JSON.
3. Add or update a scenario test.
4. Run validation.
5. Update the wiki if the branch teaches the player something important.
