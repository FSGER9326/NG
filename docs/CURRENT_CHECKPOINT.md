# NG Current Checkpoint

Date: 2026-05-05
Source-of-truth repo: `FSGER9326/NG`
Default branch: `main`
Current `main` head during checkpoint: `0de7bac31fb3e4e7379d46ef21d27d0a605397d4`

## Why this checkpoint exists

This file is the durable restart point for future chats and AI agents. It replaces the stale cleanup checkpoint branch from 2026-05-04, whose PR queue and main-branch head are no longer current.

Read this file first, then read:

1. `docs/PROJECT_STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/WORKFLOW.md`
4. `docs/BUGFIXING.md`
5. `docs/ASSET_POLICY.md`
6. `docs/STORY_BIBLE.md`
7. `docs/CHARACTER_CREATION.md`

## Current confirmed main-branch state

`main` is the stable baseline. Recent branch-integration work has already brought in the useful content and validation work from the old branch queue:

- `docs/QUEST_SEEDS.md`
- `data/quests/side/dog_knew_road.json`
- `data/quests/side/black_bread_tithe.json`
- `data/quests/side/soot_prayer_cloth.json`
- `areas/wolfpine_chapel_yard/*`
- `tests/scenarios/wolfpine_wounded_dog_tracks.json`
- `tests/scenarios/wolfpine_black_bread_tithe.json`
- `tests/scenarios/wolfpine_chapel_yard_soot.json`
- `game/scripts/character/portrait_catalog.gd`
- `tools/validate_portraits.py`
- `tools/validate_character_creation.py`
- `tools/validate_quest_seeds.py`
- `tools/validate_gdscript_helpers.py`
- `tools/validate_asset_kits.py`
- CI and local update scripts that run the current validator set

## Branch integration status

During the latest branch audit:

- Old content branches for Dog That Knew the Road, Black Bread Tithe, and Soot on the Prayer Cloth were confirmed already present on `main` through later squash merges.
- The aggregate `content/cleanup-quests` branch was confirmed to contain the same content already present on `main`.
- The workflow guardrail branch was confirmed already represented on `main` by `tools/check_pr_hygiene.py` and `.github/workflows/pr_hygiene.yml`.
- `ci/validate-background-portrait-refs` was integrated by PR #27 and merged as `0de7bac31fb3e4e7379d46ef21d27d0a605397d4`.
- The old Codex branch that changes scenario `background` assertions to internal background IDs should not be merged as-is. Current profiles keep `background` as the readable name and expose the internal ID separately as `background_id`.

## Current validation command set

Run from repo root:

```bash
python tools/validate_project.py
python tools/validate_character_creation.py
python tools/validate_portraits.py
python tools/validate_quest_seeds.py
python tools/validate_gdscript_helpers.py
python tools/validate_asset_kits.py
```

The Windows local update scripts also run this validator set after pulling latest changes:

```text
tools/update_ng.bat
tools/update_ng.ps1
```

## Current primary goal

The next meaningful gameplay-facing task is still issue #13:

```text
Expose text-first portrait selection in character creator
```

Current support work for issue #13 is ready:

- portrait metadata exists in `data/character_creation/portraits.json`
- portrait metadata is validated
- character creation and portrait validators cross-check portrait references
- `PortraitCatalog` exists and is protected by `tools/validate_gdscript_helpers.py`

Remaining issue #13 implementation scope:

1. Load portrait metadata in `game/scripts/core/main.gd`.
2. Add a portrait dropdown and summary label to the character creator.
3. Populate portrait choices from `data/character_creation/portraits.json`.
4. Use `PortraitCatalog.apply_to_profile()` before Start Journey.
5. Add scenario/debug coverage for `select_portrait` and `portrait_id` / `portrait` assertions.
6. Add `tests/scenarios/character_creator_portrait_selection.json`.

## Important caution

`game/scripts/core/main.gd` is a large file. The GitHub connector currently exposes full-file replacement for existing text files, so do not overwrite it casually. Prefer one of these approaches:

1. Use a local patch workflow with exact context hunks.
2. Use Git blob/tree primitives only if the exact current blob/tree data is available and the patch is mechanically verified.
3. Keep changes small and test through scenario coverage.

## Branch cleanup recommendation

Many old branches remain after squash merges. Do not assume a diverged branch contains unmerged work just because it is `ahead_by > 0`; many are squash-merged equivalents. Before integrating any branch:

1. Compare it with `main`.
2. Check whether the changed files already exist on `main`.
3. Inspect semantic drift before opening a PR.
4. Prefer recreating useful stale docs on a fresh branch instead of merging outdated handoff text.

## Do not do yet

- Do not merge the Codex background-ID scenario branch as-is.
- Do not import final portrait art for issue #13.
- Do not start combat prototype work until the current menu/new-game/portrait-creator path is stable.
- Do not make broad rewrites to area loading, dialogue, or save/load while branch cleanup is still in progress.
