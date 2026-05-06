# Batch 00 Scorecard Review - 2026-05-06

Thresholds:

- Weighted total >= 85
- No category < 70

| Asset ID | Camera consistency | Silhouette readability at target scale | Modular seam compatibility | Lighting/shadow coherence | Material/palette consistency | Gameplay affordance clarity | Cleanup/alpha integrity | Weighted total | Seam evidence | Scale evidence | Promoted | Manifest ref |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| wolfpine_wall_front_medium_01 | 88 | 90 | 86 | 86 | 82 | 88 | 92 | 87.60 | game/scenes/area/validation/wolfpine_village/wv_modular_straight_run.tscn | game/scenes/area/validation/wolfpine_village/wv_test_00_batch0_quickcheck.tscn | no |  |
| wolfpine_wall_side_medium_01 | 87 | 86 | 87 | 85 | 81 | 86 | 93 | 86.40 | game/scenes/area/validation/wolfpine_village/wv_modular_corner_cases.tscn | game/scenes/area/validation/wolfpine_village/wv_test_00_batch0_quickcheck.tscn | no |  |
| wolfpine_floor_lower_01 | 86 | 88 | 85 | 84 | 80 | 88 | 95 | 86.45 | game/scenes/area/validation/wolfpine_village/wv_modular_straight_run.tscn | game/scenes/area/validation/wolfpine_village/wv_test_00_batch0_quickcheck.tscn | no |  |
| wolfpine_stairs_01 | 89 | 88 | 84 | 86 | 83 | 89 | 94 | 87.50 | game/scenes/area/validation/wolfpine_village/wv_modular_elevation_transitions.tscn | game/scenes/area/validation/wolfpine_village/wv_test_00_batch0_quickcheck.tscn | no |  |
| wolfpine_column_01 | 90 | 87 | 82 | 87 | 84 | 87 | 94 | 87.25 | game/scenes/area/validation/wolfpine_village/wv_modular_corner_cases.tscn | game/scenes/area/validation/wolfpine_village/wv_test_00_batch0_quickcheck.tscn | no |  |

## Promoted Modular Slice Notes

- `wolfpine_wall_front_a_00`, `wolfpine_wall_side_a_00`, `wolfpine_floor_lower_a_00`, `wolfpine_stairs_a_00`, and `wolfpine_contact_shadow_wall_side_a_00` passed the promotion gate in the production manifest.
- This pass favors consistent geometry and readability over texture complexity.
- Next iteration should increase subtle material breakup while preserving seam cleanliness.
