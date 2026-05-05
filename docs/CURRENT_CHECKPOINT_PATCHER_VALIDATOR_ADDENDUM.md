# Current Checkpoint Addendum: Issue #13 Patcher Validator

Date: 2026-05-05
Applies after main commit: `49c32e55b8e12c3e4c20e857c6b25e913f2d485a`

This addendum supplements `docs/CURRENT_CHECKPOINT.md`, which was last refreshed before the Issue #13 patcher validator and related documentation merges.

## New merged work after the checkpoint

- PR #39 added `tools/validate_issue_13_patcher.py`.
- PR #39 wired the validator into:
  - `.github/workflows/validate.yml`
  - `tools/update_ng.bat`
  - `tools/update_ng.ps1`
- PR #40 documented the new validator in `docs/AUTOMATION.md`.
- PR #42 documented the new validator in `docs/ISSUE_13_RUNTIME_HANDOFF.md`.

## Current validation command set

Run from repo root:

```bash
python tools/validate_project.py
python tools/validate_character_creation.py
python tools/validate_portraits.py
python tools/validate_quest_seeds.py
python tools/validate_gdscript_helpers.py
python tools/validate_issue_13_patcher.py
python tools/validate_asset_kits.py
```

## What the new validator protects

`tools/validate_issue_13_patcher.py` verifies the safety of the Issue #13 portrait-selection patch workflow.

Before the runtime patch lands, it checks that every exact replacement context in:

```text
tools/apply_issue_13_portrait_selection_patch.py
```

still appears exactly once in:

```text
game/scripts/core/main.gd
```

After the runtime patch lands, it accepts the already-applied state only if the matching scenario exists:

```text
tests/scenarios/character_creator_portrait_selection.json
```

## Current Issue #13 next step

The remaining gameplay-facing task is still to run the patcher locally on a fresh runtime branch:

```bash
python tools/apply_issue_13_portrait_selection_patch.py
```

Expected changed files:

```text
game/scripts/core/main.gd
tests/scenarios/character_creator_portrait_selection.json
```

Then run the full validator set and the Godot smoke/scenario workflow before opening the final runtime PR.

## Important caution

Do not manually overwrite `game/scripts/core/main.gd` through a blind full-file replacement. Prefer the local patcher because it uses exact context replacements and now has drift validation in CI and local update scripts.
