# NG Current Checkpoint

Date: 2026-05-04
Branch for this cleanup: `cleanup/project-checkpoint-2026-05-04`
Source-of-truth repo: `FSGER9326/NG`
Default branch: `main`
Current `main` head during checkpoint: `4b6d722fd0f6d398b140328f27be8242829bd4e9` (`Add Caravan Guard Renna reaction scenario`)

## Why this checkpoint exists

The project had accumulated several parallel chats and pull requests, and the roadmap appeared to be behind the actual repository state. This file is a durable restart point before further feature/content advancement.

Use this file to quickly recover the real project state, then re-read:

1. `docs/PROJECT_STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/WORKFLOW.md`
4. `docs/BUGFIXING.md`
5. `docs/ASSET_POLICY.md`
6. `docs/STORY_BIBLE.md`
7. `docs/CHARACTER_CREATION.md`

## Current confirmed main-branch state

`main` is the stable branch and currently contains the menu/new-game/character-creator/Wolfpine Road prototype work described in `docs/PROJECT_STATUS.md`.

The latest confirmed `main` commit adds scenario coverage for the Caravan Guard Renna reaction path:

- `tests/scenarios/wolfpine_caravan_guard_renna_reaction.json`

This means `main` already has at least one scenario path that expects the older scenario inputs `Border Human`, `Caravan Guard`, `Scout`, and `Quick-Eyed`. There is also an open PR to normalize some scenario background fields to canonical IDs, so scenario field naming should be reviewed before adding more scenario fixtures.

## Open pull request queue

Triage these before advancing broad new content.

| PR | Branch | State | Mergeability at checkpoint | Purpose | Cleanup note |
| --- | --- | --- | --- | --- | --- |
| #6 | `feature/creator-compatibility-explanations` | draft | mergeable | Improves readable character-creator compatibility explanations and fixes compatibility evaluation ordering. | Draft. Validate and merge only after scenario/input ID consistency is settled. |
| #5 | `codex/locate-and-update-background-fields-in-tests` | open | mergeable | Normalizes selected scenario background fields to canonical IDs. | Likely should be reviewed before PR #6 and before new creator scenarios. |
| #4 | `content/chapel-yard-soot` | open | mergeable | Adds Chapel Yard area stub and `soot_prayer_cloth` quest hook. | Content expansion; keep parked until baseline cleanup is done. |
| #3 | `content/black-bread-tithe` | open | mergeable | Adds Wolfpine Village `black_bread_tithe` quest seed implementation. | Content expansion; keep parked until baseline cleanup is done. |
| #2 | `content/dog-knew-road` | open | mergeable | Adds Wolfpine Road wounded-dog side quest seed implementation. | Content expansion; keep parked until baseline cleanup is done. |
| #1 | `content/quest-seeds` | open | not mergeable | Adds reusable quest seed bank and status update. | Needs rebase/conflict resolution or replacement because later PRs already convert some seeds. |

## Roadmap correction

Treat `docs/ROADMAP.md` as directionally useful but not fully current until this checkpoint is merged and the PR queue is reconciled.

The real next priority is no longer simply "advance the next feature." It is:

1. Preserve `main` as the clean baseline.
2. Review and reconcile open PRs in dependency order.
3. Normalize scenario fixture conventions for character creation IDs.
4. Validate the current main build locally with:
   - `python tools/validate_project.py`
   - `python tools/validate_character_creation.py`
   - `python tools/validate_asset_kits.py`
5. Run or inspect the debug bundle/scenario logs before merging content PRs.
6. Only then resume roadmap feature advancement.

## Suggested PR triage order

1. PR #5 — scenario canonical background IDs.
2. PR #6 — creator compatibility explanation work, after rebasing if needed.
3. PR #1 — quest seed bank conflict resolution. Decide whether to rebase it or replace it with a smaller current seed-bank document that accounts for PRs #2-#4.
4. PRs #2, #3, #4 — content seed implementations, one at a time, with validation after each merge.

## Do not do yet

Until the queue is clean:

- Do not add more quest content.
- Do not generate or import final Wolfpine Village art.
- Do not start combat prototype work.
- Do not make broad rewrites to area loading, dialogue, or save/load.

## Safe cleanup work now

Allowed cleanup before feature advancement:

- Update status docs to reflect the open PR queue.
- Add validation notes or scenario naming conventions.
- Rebase/merge small PRs one at a time.
- Fix validation failures discovered by the current baseline.
- Keep all changes text-first and low-risk.
