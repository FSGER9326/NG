# NG Save System

## Goal

Keep the early save format simple, readable, JSON-based, and useful for debugging.

The first implementation is a single-slot prototype used to verify persistence before building a full save/load UI.

## Runtime files

```text
game/scripts/core/save_system.gd
game/scripts/core/main.gd
game/scripts/core/game_state.gd
```

## Save location

```text
user://ng_save_slot_1.json
```

## Save version

Current version: `1`

## Current saved state

The first save/load implementation stores:

- player profile
- current area ID
- player marker position
- flags
- faction reputation
- party member IDs
- party skills
- active quest IDs
- quest stages

It restores:

- player profile
- current area
- player marker position
- `GameState`
- mirrored `QuestSystem.quest_states`
- quest tracker display

## Menu behavior

The main menu shows `Load Game` and enables it only if the single save file exists.

`Save Game` is not a full menu flow yet; save is currently available through debug/scenario action and the internal `_save_game()` path.

## Scenario coverage

Current save/load scenario:

```text
tests/scenarios/main_menu_save_load.json
```

It verifies character creation, starting Wolfpine Road, accepting `missing_caravan`, saving, loading, restored profile, restored current area, and restored quest stage.

## Known limitations

- Single save slot only.
- No save browser UI.
- No timestamps.
- No inventory/equipment format yet.
- No combat-state save format yet.
- No version migration beyond a warning.
- Save/load should be rechecked after character stats and inventory exist.

## Authoring rule

When adding new persistent state:

1. Add it to `GameState.to_debug_dict()` or the relevant save export path.
2. Add import/apply logic.
3. Add scenario coverage if the state affects gameplay.
4. Update this document.
