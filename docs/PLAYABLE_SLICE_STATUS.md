# Playable Slice Status

Last updated: 2026-05-06

This document is the human-readable source of truth for what is currently playable in the NG Wolfpine vertical slice. Keep it updated when work changes routes, areas, quests, dialogue, scenario coverage, asset state, or known blockers.

`repo-context.txt` is generated context for agents. This file is the planning/status layer for humans and future agents.

## Update rule

Update this file in the same PR when any of these change:

- playable areas, exits, or route graph
- quest stages, dialogue choices, flags, or companion recruitment
- runtime scenario coverage
- validators that protect playability
- asset-pipeline milestones or blockers
- current recommended next work

If a PR touches gameplay/content but does not need a status update, explain why in the PR checklist.

## Current playable slice

The current vertical slice is the Wolfpine opening sequence:

1. Start on `wolfpine_road`.
2. Investigate caravan clues and side-quest hooks.
3. Recruit Brannoc from companion dialogue.
4. Travel to `wolfpine_village`.
5. Explore the village hub, inn, blacksmith, and chapel yard.
6. Report evidence to Captain Renna.
7. Resolve the first missing-caravan report or continue through the deeper evidence-web path.

## Playable area graph

```text
wolfpine_road
  -> wolfpine_village

wolfpine_village
  -> wolfpine_road
  -> wolfpine_inn_common_room
  -> wolfpine_blacksmith
  -> wolfpine_chapel_yard

wolfpine_inn_common_room
  -> wolfpine_village

wolfpine_blacksmith
  -> wolfpine_village

wolfpine_chapel_yard
  -> wolfpine_village
```

CI runs `tools/validate_area_routes.py`, so exit hotspots must point to existing areas and defined entry points.

## Runtime scenario coverage

The Godot scenario suite currently covers these playable flows:

| Scenario | Coverage |
|---|---|
| `wolfpine_road_caravan_clue_flow` | Main missing-caravan clue chain on Wolfpine Road and travel into Wolfpine Village. |
| `wolfpine_renna_evidence_report_flow` | Gather road evidence, report carter body / erased name / smuggler mark to Captain Renna, and advance the evidence-web report. |
| `wolfpine_renna_first_report_resolution` | Find first road clue, report it to Renna, and resolve the first investigation report. |
| `wolfpine_brannoc_recruitment` | Recruit Brannoc from Wolfpine Road companion dialogue and set recruitment state. |
| `wolfpine_dog_road_quest_flow` | Follow wounded-dog trail, end the vigil, and cross-link the carter-body clue into the main quest. |
| `wolfpine_village_interior_exits` | Travel Village -> Inn -> Village and Village -> Blacksmith -> Village. |
| `wolfpine_interior_clue_flow` | Inspect clue hotspots inside the inn and blacksmith and return to the village. |
| `wolfpine_chapel_yard_quest_flow` | Travel to chapel yard, advance `soot_prayer_cloth`, set flags, and return to village. |
| `wolfpine_black_bread_village_flow` | Start/advance `black_bread_tithe` via market stall and notice board, plus mill pressure hints. |

Character creation, save/load, portrait metadata, asset pipelines, and other systems have their own validators/scenarios, but this table tracks the core playable Wolfpine slice.

## Quest and interaction state

### Main quest: `missing_caravan`

Covered playable beats:

- road shrine clue: `found_wreck`
- ledger niche clue: `found_erased_name`
- cut-bark mark clue: `found_smuggler_mark`
- dog-vigil carter body clue: `found_carter_body`
- Captain Renna report states:
  - `reported_clue`
  - `reported_carter_body`
  - `reported_erased_name`
  - `reported_smuggler_mark`
  - `evidence_web_reported`
  - `resolved`

### Side quest: `dog_knew_road`

Covered playable beats:

- `found_blood_marker`
- `buried_master`
- `dog_vigil_ended` completion flag
- cross-link into `missing_caravan.found_carter_body`

### Side quest: `soot_prayer_cloth`

Covered playable beats:

- `found_unburned_cloth`
- `revealed_mark`
- chapel-yard return route

### Side quest: `black_bread_tithe`

Covered playable beats:

- `checked_market`
- `found_guard_tithe`
- related mill pressure flags

### Companion: Brannoc

Covered playable beat:

- Wolfpine Road recruitment dialogue sets `brannoc_recruited`.

Note: runtime supports `assert_party_member`, but `tools/validate_project.py` did not support that scenario assertion when `wolfpine_brannoc_recruitment` was added. The scenario currently asserts the recruitment flag. A focused follow-up can add static validator support for `assert_party_member` and strengthen the scenario.

## Validators protecting playability

Key validation/scenario protections currently in CI:

- `tools/validate_project.py`
- `tools/validate_area_routes.py`
- `tools/validate_character_creation.py`
- `tools/validate_gdscript_helpers.py`
- `tools/validate_asset_kits.py`
- `tools/validate_promoted_asset_files.py`
- `tools/validate_asset_production_batches.py`
- `tools/validate_asset_promotion_plans.py`
- `tools/validate_asset_reviews.py`
- `tools/validate_asset_review_outcomes.py`
- Godot smoke/scenario workflow
- Runtime parse guards
- PR hygiene

## Asset pipeline status

The first Wolfpine PNG assets are prepared but not yet committed to main as binary files.

Prepared first-promotion assets:

- `wolfpine_well_01`
- `wolfpine_notice_board_01`
- `wolfpine_door_heavy_01`
- `wolfpine_window_shuttered_01`
- `wolfpine_firewood_stack_01`

Current asset lifecycle support:

```text
generated/planned
-> promotion bundle
-> cleaned manifest status
-> pending review outcome
-> visual/layout review gate
-> accepted only with accepted review outcome
```

Important files:

- `tools/prepare_wolfpine_first_binary_pr.py`
- `data/asset_reviews/wolfpine_first_cleaned_review_2026_05_06.json`
- `data/asset_review_outcomes/wolfpine_first_cleaned_review_pending_2026_05_06.json`

Known blocker: the ChatGPT GitHub connector could not reliably stream the uploaded/local PNG bytes into Git blobs. The safe path is still to run the local helper from a normal checkout with the optimized ZIP, then push the binary promotion PR.

## Known gaps before a stronger playable demo

Highest-value remaining work:

1. Commit the first five Wolfpine PNG binaries from the local apply bundle as `cleaned` assets.
2. Add static validator support for `assert_party_member`, then strengthen the Brannoc scenario to assert actual party membership.
3. Add a small journal/quest-log UX check so players can see active and completed quest state clearly in the prototype.
4. Add at least one NPC/vendor or village resident interaction beyond Captain Renna and Brannoc.
5. Add a black-bread resolution path, not only investigation stages.
6. Add a chapel-yard resolution/report path for `soot_prayer_cloth`.
7. Replace placeholder area backgrounds/walkmasks/occlusion notes with reviewed production art and collision/occlusion data.
8. Add a lightweight playable-demo checklist for manual smoke testing outside CI.

## Recent playable-state milestone history

- Added Wolfpine inn and blacksmith interiors and route scenario coverage.
- Added area route validation for exit targets and entry points.
- Added chapel-yard side-quest scenario coverage.
- Added Wolfpine Road main-caravan clue scenario coverage.
- Added Captain Renna evidence-report and first-report resolution scenarios.
- Added Brannoc recruitment scenario.
- Added wounded-dog side-quest scenario.
- Added inn/blacksmith interior clue scenario.
- Added black-bread village investigation scenario.

## Maintenance notes

When adding future playable work:

1. Add or update a runtime scenario if the change affects player-facing flow.
2. Add or update validators if the issue could recur in data.
3. Update this document with the new playable coverage and remaining gap changes.
4. Keep changes small and data-driven where possible.
