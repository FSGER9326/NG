# Issue #13 Portrait Selection Patch

This note documents the safe local patch path for implementing issue #13: exposing text-first portrait selection in the character creator.

## Why this exists

`game/scripts/core/main.gd` is currently large, and the connected GitHub update path is safest for small/new files. To avoid a risky full-file overwrite, the repo includes an exact-context patcher:

```bash
python tools/apply_issue_13_portrait_selection_patch.py
```

The patcher refuses to run if the expected `main.gd` context has drifted or if the portrait selector already appears to be applied.

## What the patcher changes

The patcher updates `game/scripts/core/main.gd` to:

- preload `PortraitCatalog`
- load `data/character_creation/portraits.json`
- add a `Portrait` dropdown to the character creator
- add a portrait summary label
- populate choices from text-first portrait metadata
- apply the selected portrait before `Start Journey`
- support scenario/debug action `select_portrait`
- allow `assert_player_profile` to check `portrait_id` and `portrait`

The patcher also creates:

```text
tests/scenarios/character_creator_portrait_selection.json
```

The scenario checks that a coherent build can select the `Caravan Guard` portrait, start the game, load Wolfpine Road, and persist both:

```text
portrait: Caravan Guard
portrait_id: portrait_caravan_guard_01
```

## After running the patcher

Review the diff before committing. The expected changed files are:

```text
game/scripts/core/main.gd
tests/scenarios/character_creator_portrait_selection.json
```

Do not add final portrait art for this issue. This remains text-first metadata only.

## Validation after patch

Run from repo root:

```bash
python tools/validate_project.py
python tools/validate_character_creation.py
python tools/validate_portraits.py
python tools/validate_quest_seeds.py
python tools/validate_gdscript_helpers.py
python tools/validate_asset_kits.py
```

Then run the Godot scenario workflow or local debug bundle if available.

## Asset policy

No image assets are required for issue #13. This is text-first portrait metadata only.
