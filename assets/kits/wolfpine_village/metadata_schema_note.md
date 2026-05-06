# Wolfpine Village Metadata Schema Note

This note defines the canonical allowed values for manifest metadata fields used by Wolfpine Village kit imports.

## Fields

- `module_family` (string)
  - Allowed values: `building_shell`, `architecture_trim`, `prop_set`, `clutter_set`, `pathing_piece`, `set_dressing`, `unassigned`
- `orientation` (string)
  - Allowed values: `iso_southwest`, `iso_southeast`, `iso_northwest`, `iso_northeast`, `omni`, `ui_flat`
- `edge_role` (string)
  - Allowed values: `front`, `side`, `corner`, `transition`
- `elevation_class` (string)
  - Allowed values: `lower`, `upper`, `ramp`, `stair`
- `join_compatibility` (array of strings)
  - Allowed value pattern: semantic join tags, e.g. `wolfpine_v1`, `road_edge_v1`, `stone_trim_v1`
  - Must contain at least one tag.
- `shadow_mode` (string)
  - Allowed values: `baked_soft`, `baked_hard`, `runtime_blob`, `runtime_projected`, `none`
- `tile_span` (object)
  - Required keys: `width`, `depth`, `height`
  - Value constraints: integer values `>= 1`
- `style_lock_version` (string)
  - Allowed values: `wolfpine_v1`, `wolfpine_v2_candidate`
- `qa_score` (number)
  - Allowed range: `0.0` to `1.0`
  - Recommended interpretation:
    - `< 0.60` needs revision
    - `0.60 - 0.84` usable candidate
    - `>= 0.85` production-ready

## Import Consistency Rules

1. All new kit manifest entries **must** include all fields above.
2. Avoid free-form alternatives for enum-like fields.
3. If a value is unknown during initial ingest, use:
   - `module_family: unassigned`
   - `qa_score: 0.0`
   - `join_compatibility: ["wolfpine_v1"]`
4. Update this file first when introducing new enumerations, then update manifests.
