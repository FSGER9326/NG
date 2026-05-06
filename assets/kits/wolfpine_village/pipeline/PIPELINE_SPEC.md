# Wolfpine Village Pipeline Spec

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
