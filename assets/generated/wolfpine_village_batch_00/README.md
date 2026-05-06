# Wolfpine Village Batch 00

This batch applies the Wolfpine generation specs, SVG technical art bible, and prompt templates to produce canonical modular foundation assets.

## Included SVG candidates

- `wolfpine_wall_front_medium_01.svg`
- `wolfpine_wall_side_medium_01.svg`
- `wolfpine_floor_lower_01.svg`
- `wolfpine_stairs_01.svg`
- `wolfpine_column_01.svg`

## Included promoted slice

- `wolfpine_wall_front_a_00`
- `wolfpine_wall_side_a_00`
- `wolfpine_floor_lower_a_00`
- `wolfpine_stairs_a_00`
- `wolfpine_contact_shadow_wall_side_a_00`

## Acceptance flow used

1. Generated isolated canonical candidates for each family.
2. Ran scorecard review and rejected or regenerated below-threshold candidates.
3. Normalized crop, alpha, and contact-shadow alignment.
4. Recorded metadata: `module_family`, `orientation`, `join_compatibility`, and `qa_score`.
5. Promoted into the production manifest only after acceptance.

## Modular test proof

- wall_front + wall_side seam compatibility: **pass**
- floor_lower + stairs transition compatibility: **pass**

These assets are intended as canonical candidates and promoted slice entries. Future iterations should continue validating scorecard thresholds, seam checks, and gameplay readability before full promotion.
