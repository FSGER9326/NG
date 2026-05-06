# Wolfpine Village Pipeline Spec

## Objective

Create Wolfpine assets at least equal to Infernus references, with a parity-plus quality target.

## Stages

1. **Plan**
   - Select batch scope from roadmap.
   - Confirm required module families and target variant counts.
2. **Generate**
   - Produce one SVG candidate per target asset ID.
   - Follow `SVG_TECH_ART_BIBLE.md` exactly.
3. **Review**
   - Score candidates using `SVG_SCORECARD.md`.
   - Reject or regenerate below-threshold candidates.
4. **Validate**
   - Run modular seam and adjacency checks for structural assets.
   - Validate gameplay readability at target scene scale.
5. **Promote**
   - Update the production manifest after acceptance only.
   - Record qa score, family, orientation, and compatibility metadata.
6. **PR**
   - Open a PR with artifacts, scorecard summary, and validation evidence.

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

## Batch Ordering

1. Foundation modulars (walls/floors/stairs/ramps).
2. Structural enrichers (arches/buttresses/columns/shadows).
3. Hero facades.
4. Hotspot props.
5. Decals/clutter/occluders.

## Canonical Promotion Rule

Only promote assets after scorecard pass, validation pass, and manifest update.
