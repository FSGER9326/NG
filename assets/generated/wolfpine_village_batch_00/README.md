# Wolfpine Village Batch 0 (Five-Asset Modular Slice)

This batch applies the existing Wolfpine generation specs and prompt templates to produce five canonical modular foundation assets.

## Included assets

- `wolfpine_wall_front_a_00`
- `wolfpine_wall_side_a_00`
- `wolfpine_floor_lower_a_00`
- `wolfpine_stairs_a_00`
- `wolfpine_contact_shadow_wall_side_a_00`

## Acceptance flow used

1. Generated isolated canonical candidate for each family.
2. Ran scorecard review and rejected/regenerated any below-threshold candidates.
3. Normalized crop/alpha/contact-shadow alignment.
4. Recorded metadata: `module_family`, `orientation`, `join_compatibility`, `qa_score`.
5. Promoted into production manifest only after acceptance.

## Modular test proof

- wall_front + wall_side seam compatibility: **pass**
- floor_lower + stairs transition compatibility: **pass**

No family was blocked in this pass.
