# Wolfpine Evidence Status Addendum

This addendum records the first-playable Wolfpine evidence work merged after the previous `PROJECT_STATUS.md` snapshot.

## Merged gameplay/content changes

The following PRs are now merged into `main`:

- PR #46 — `Add Wolfpine Road evidence clue hotspots`
- PR #48 — `Add Brannoc reactions for Wolfpine evidence clues`
- PR #49 — `Add Renna reports for Wolfpine evidence clues`

## Current Wolfpine Road evidence loop

Wolfpine Road now supports a broader Missing Caravan investigation loop:

- `old_shrine` still provides the initial shrine/rut/toll-disc evidence.
- `shrine_ledger_niche` adds a hidden ledger clue with an erased passenger name.
- `cut_bark_smuggler_mark` adds a Blackfen/smuggler-route mark near the wagon ruts.
- `dog_vigil_hollow` now feeds back into the main Missing Caravan quest with the hidden dead carter clue.

## Missing Caravan quest stages now covered

The quest includes evidence-find and report stages for:

- `found_erased_name`
- `found_smuggler_mark`
- `found_carter_body`
- `reported_carter_body`
- `reported_erased_name`
- `reported_smuggler_mark`
- `evidence_web_reported`

## Dialogue and companion state

Captain Renna now has gated report branches for:

- the dead carter found by following the wounded dog
- the erased passenger name from the shrine ledger
- the cut-bark smuggler mark
- the combined evidence-web synthesis, once all three clue reports are known

Brannoc now has companion reaction branches for:

- the hidden dead carter
- the erased ledger name
- the smuggler mark

These branches use concrete flags instead of a generic approval meter, matching the current companion-story direction.

## Scenario coverage added

The new scenario coverage includes:

```text
tests/scenarios/wolfpine_evidence_clues.json
tests/scenarios/brannoc_new_caravan_clue_reactions.json
tests/scenarios/wolfpine_report_carter_body_to_renna.json
tests/scenarios/wolfpine_evidence_web_to_renna.json
```

These scenarios validate the new hotspot clues, quest stages, flags, Brannoc reactions, Renna reports, and combined evidence-web report path.

## Validation status

The merged PRs passed GitHub validation before merge:

- Validate NG data
- PR hygiene
- Godot smoke and scenario test

## Follow-up recommendations

Next content work should move from Wolfpine Road evidence into one of these small, testable slices:

1. Wolfpine Village NPC pressure around the erased name or Blackfen route signs.
2. A small suspect/interview branch that uses `wolfpine_evidence_web_reported`.
3. A consequence branch for how much truth Renna is willing to reveal publicly.
4. A docs/status consolidation pass that folds this addendum back into `PROJECT_STATUS.md` when a local patch/edit workflow is available.
