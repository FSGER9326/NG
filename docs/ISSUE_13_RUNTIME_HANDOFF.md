# Issue #13 Runtime Handoff

Issue #13 is the next gameplay-facing implementation target:

```text
Expose text-first portrait selection in the character creator.
```

## Current support already on `main`

The following support pieces are already merged:

- `data/character_creation/portraits.json`
- `game/scripts/character/portrait_catalog.gd`
- `tools/validate_portraits.py`
- `tools/validate_character_creation.py` portrait-reference checks
- `tools/validate_gdscript_helpers.py` contract checks for `PortraitCatalog`
- `tools/validate_project.py` support for future portrait scenario fields:
  - `select_portrait`
  - `portrait`
  - `portrait_id`
- `tools/validate_issue_13_patcher.py` drift check for the exact-context patcher
- `tools/apply_issue_13_portrait_selection_patch.py`
- `docs/ISSUE_13_PORTRAIT_SELECTION_PATCH.md`

## Remaining runtime task

Run the local exact-context patcher on a fresh runtime branch:

```bash
python tools/apply_issue_13_portrait_selection_patch.py
```

Expected changed files after running the patcher:

```text
game/scripts/core/main.gd
tests/scenarios/character_creator_portrait_selection.json
```

## Intended runtime behavior

After the runtime patch:

- the character creator loads `data/character_creation/portraits.json`
- the creator shows a `Portrait` dropdown after `Trait`
- the creator shows a text summary for the selected portrait
- `Start Journey` applies the selected portrait with `PortraitCatalog.apply_to_profile()`
- the debug/scenario runner supports `select_portrait`
- `assert_player_profile` can check `portrait` and `portrait_id`

## Scenario target

The patcher creates:

```text
tests/scenarios/character_creator_portrait_selection.json
```

The scenario should verify:

- main menu opens the character creator
- a coherent character build can select the `Caravan Guard` portrait
- Start Journey loads `wolfpine_road`
- the final player profile contains:

```text
portrait: Caravan Guard
portrait_id: portrait_caravan_guard_01
```

## Validation after applying runtime patch

Run:

```bash
python tools/validate_project.py
python tools/validate_character_creation.py
python tools/validate_portraits.py
python tools/validate_quest_seeds.py
python tools/validate_gdscript_helpers.py
python tools/validate_issue_13_patcher.py
python tools/validate_asset_kits.py
```

Then run the Godot smoke/scenario workflow or the local debug bundle.

## Automatic drift protection

CI and the local update scripts now run:

```bash
python tools/validate_issue_13_patcher.py
```

Before the runtime patch lands, this validator checks that every exact replacement context in `tools/apply_issue_13_portrait_selection_patch.py` still appears exactly once in `game/scripts/core/main.gd`.

After the runtime patch lands, it accepts the already-applied state only when the matching portrait-selection scenario exists.

## Important caution

Do not manually overwrite `game/scripts/core/main.gd` through a blind full-file replacement. It is a large script, and the connector has not consistently exposed the file SHA for safe direct replacement.

Prefer the patcher, because it uses exact context replacements and refuses to run if the expected file shape has drifted.

## Asset policy

No image assets are required for Issue #13. This is text-first portrait metadata only.
