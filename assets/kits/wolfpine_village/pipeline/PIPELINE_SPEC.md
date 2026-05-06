# Wolfpine Village Pipeline Spec

## Objective

Create Wolfpine assets at least equal to Infernus references, with a parity-plus quality target.

## Sources of Truth

Use these files in order:

1. `assets/kits/wolfpine_village/MODULAR_PARITY_PLAN.md` — family coverage and parity targets.
2. `assets/kits/wolfpine_village/PRODUCTION_ROADMAP.md` — wave ordering and release sequencing.
3. `assets/kits/wolfpine_village/SVG_TECH_ART_BIBLE.md` — canonical SVG primitive and anti-flatness rules.
4. `assets/kits/wolfpine_village/QUALITY_SCORECARD.md` — canonical promotion scorecard.
5. `assets/kits/wolfpine_village/pipeline/BATCH_STATE_MACHINE.md` — batch-level state and retry policy.

`pipeline/SVG_SCORECARD.md` is a preflight checklist only. It must not override `QUALITY_SCORECARD.md`.

## Stages

1. **Plan**
   - Select batch scope from roadmap.
   - Confirm required module families and target variant counts.
   - Initialize batch state as `planned`.
2. **Generate**
   - Produce one SVG candidate per target asset ID.
   - Follow `assets/kits/wolfpine_village/SVG_TECH_ART_BIBLE.md` exactly.
   - Record prompt/spec version and run identifier.
3. **Review**
   - Run SVG preflight if applicable.
   - Score candidates using `assets/kits/wolfpine_village/QUALITY_SCORECARD.md`.
   - Reject or regenerate below-threshold candidates.
4. **Validate**
   - Run modular seam and adjacency checks for structural assets.
   - Validate gameplay readability at target scene scale.
   - Store evidence paths or links in `scorecard_review.md` / `scorecard_review.json`.
5. **Promote**
   - Update the production manifest after acceptance only.
   - Record qa score, family, orientation, compatibility metadata, and evidence.
   - Use asset lifecycle states from `docs/ASSET_SESSION_PROTOCOL.md`.
6. **PR**
   - Open a PR with artifacts, scorecard summary, validation evidence, and validator output.

## Fixed Modular Validation Templates

Use the following template scenes for structural validation before promotion:

- `game/scenes/area/validation/wolfpine_village/wv_modular_straight_run.tscn`
- `game/scenes/area/validation/wolfpine_village/wv_modular_corner_cases.tscn`
- `game/scenes/area/validation/wolfpine_village/wv_modular_elevation_transitions.tscn`

## Pass Criteria

A structural asset only passes if it meets **all** criteria in all applicable templates:

1. No visible seams or gaps at joins.
2. Stair and ramp transitions remain readable in gameplay camera framing.
3. No shadow contradictions across neighboring connected pieces.
4. Evidence is recorded in the scorecard row as a repo path, markdown link, or approved external URL.

## Scorecard Requirement

Every scorecard entry for a structural asset must explicitly state which template scene(s) it passed in:

- `wv_modular_straight_run.tscn`
- `wv_modular_corner_cases.tscn`
- `wv_modular_elevation_transitions.tscn`

Entries missing template-scene references are incomplete and must not be marked as pass.

## Quality Gates

- Minimum passing score: **85/100**
- No category below: **70/100**
- Hero quality target: **92/100**

Mandatory fail conditions:

- Inconsistent camera/projection.
- Inconsistent lighting direction.
- Unreadable silhouette at gameplay scale.
- Broken modular seams or elevation transitions.
- Flat/vector-icon look that violates Wolfpine style lock.
- Missing or blank evidence fields for promoted or validation-gated rows.

## Batch Ordering

1. Foundation modulars (walls/floors/stairs/ramps).
2. Structural enrichers (arches/buttresses/columns/shadows).
3. Hero facades.
4. Hotspot props.
5. Decals/clutter/occluders.

## Promotion Rule

Only promote assets after scorecard pass, validation pass, manifest update, and validator pass.
