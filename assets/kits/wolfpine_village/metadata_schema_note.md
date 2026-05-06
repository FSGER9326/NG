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

## Canonical Asset Lifecycle

Wolfpine kit manifests use the existing asset lifecycle vocabulary:

```text
planned -> generated_candidate/external_candidate -> cleaned -> candidate_validated -> accepted
```

Side/terminal states:

- `rejected` — failed quality, style, legal/provenance, or technical gates.
- `blocked` — cannot progress until a dependency or decision is resolved.

Do **not** use `candidate`, `validated`, or `canonical` as replacement manifest statuses unless a separate migration updates all current manifests and validators in the same PR.

## SVG Candidate Fields for Promotion

Before an SVG asset can move to `candidate_validated` or `accepted`, manifest or batch evidence must include:

- `id`
- `candidate_file` or `file`
  - May point to `.svg` for SVG-first assets.
  - May point to `.png` for rendered, cleaned, or paintover assets.
- `module_family`
- `orientation`
- `join_compatibility`
- `qa_score`
- lifecycle status compatible with the canonical asset lifecycle above.

## Promotion Gate Requirements

Validation checks must block `accepted` promotion unless both evidence types are present:

- **Scorecard evidence:** a completed quality scorecard record with category scores and weighted total.
- **Seam/readability evidence:** modular seam compatibility evidence and gameplay-scale readability evidence. These may be local repo paths, Godot validation scenes, captures, notes, or explicit review artifacts.

If either evidence type is missing, validators must reject the promotion request.
