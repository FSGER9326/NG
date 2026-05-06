# Wolfpine Village Modular Stress Tests

This document defines **deterministic validation templates** for seam and alignment testing across the Wolfpine Village modular kit.

These tests are intended to catch mesh, pivot, UV, and lighting integration issues **before** production map assembly.

## Scope and scene placement

Create non-production validation scenes in Godot under:

- `game/scenes/area/validation/wolfpine_village/`

Recommended naming pattern:

- `wv_test_01_straight_runs.tscn`
- `wv_test_02_corners.tscn`
- `wv_test_03_elevation_transitions.tscn`
- `wv_test_04_arch_buttress_wall.tscn`
- `wv_test_05_shadow_overlap.tscn`

Keep these scenes out of shipping area load paths; they are for deterministic regression checks only.

---

## Template 01: Straight runs (repeated walls/floors)

### Required pieces

- 1x standard floor tile module (base unit).
- 1x straight wall segment module (matching tile width).
- Optional: 1x trim/cap module used in production straight runs.

Instantiate as:

- Floor: 1x8 strip and 8x8 patch.
- Wall: 1x8 linear run attached to one side of the floor strip.
- Repeat all modules with identical transform increments (no hand nudging).

### Expected visual result

- Seam lines are either invisible or uniformly tight along the entire repeated run.
- No cumulative positional or rotational drift from first to last segment.
- UV continuity appears stable (no sudden scale/rotation flips between neighbors).
- Trim/cap elements sit flush without z-fighting.

### Fail conditions

- **Gaps:** visible daylight between adjacent repeats at any distance.
- **Tangent artifacts:** normal-map seam pops or specular breaks at joins.
- **Angle drift:** end segment no longer axis-aligned after repeated placement.
- **Lighting contradictions:** repeated units alternate brightness due to mismatched normals/lightmap setup.

---

## Template 02: Inside/outside corners

### Required pieces

- 1x inside-corner wall module.
- 1x outside-corner wall module.
- 2x straight wall segments.
- Floor tiles sufficient for a 4x4 corner test pad.
- Optional: corner trim/post pieces.

Instantiate as:

- Build one inside corner using two straight approaches.
- Build one outside corner using two straight approaches.
- Duplicate each setup in mirrored orientation to test handedness.

### Expected visual result

- Corner vertices close cleanly with no wedge openings.
- Straight-to-corner transitions preserve wall thickness and silhouette.
- Mirrored variants match quality of non-mirrored variants.
- Corner trim/posts align to both connected walls without overlap clipping.

### Fail conditions

- **Gaps:** V-shaped openings at corner apex or wall-foot intersections.
- **Tangent artifacts:** hard shading discontinuity at corner transition.
- **Angle drift:** corner deviates from intended 90° (or declared design angle).
- **Lighting contradictions:** one branch of corner receives inconsistent bounce/occlusion relative to matching geometry.

---

## Template 03: Elevation transitions (stairs ↔ ramps ↔ floor upper/lower)

### Required pieces

- 1x lower floor tile set.
- 1x upper floor tile set at fixed elevation delta.
- 1x stair module matching the delta.
- 1x ramp module matching the same delta.
- 1x transition lip/landing module (if used by kit).
- Optional: side walls/railings that accompany stair/ramp pieces.

Instantiate as:

- Lane A: lower floor → stairs → upper floor.
- Lane B: lower floor → ramp → upper floor.
- Lane C: stairs directly adjacent to ramp to compare side-by-side slope integration.

### Expected visual result

- Both stair and ramp terminate exactly flush with lower/upper floors.
- Elevation delta is identical across stair and ramp solutions.
- No vertical step, hovering, or sink at transition boundaries.
- Side walls/railings follow slope and landings without offset.

### Fail conditions

- **Gaps:** cracks at top/bottom landings or side junctions.
- **Tangent artifacts:** shading pops across slope-to-flat transitions.
- **Angle drift:** ramp/stair pitch mismatches expected rise-over-run and fails to meet floor plane.
- **Lighting contradictions:** upper/lower floor receives incompatible shadowing where geometry is continuous.

---

## Template 04: Arch + buttress + wall joins

### Required pieces

- 1x arch opening module.
- 2x supporting wall modules (left/right).
- 1x buttress module (or pair, if symmetric).
- Optional: capstone/keystone/trim modules.

Instantiate as:

- Compose a canonical gateway: wall → arch opening → wall.
- Attach buttress modules at intended snap points.
- Duplicate at least once with a longer wall extension on one side to test asymmetry.

### Expected visual result

- Arch feet seat perfectly on wall supports.
- Buttress contact surfaces remain flush with host wall across full height.
- Decorative caps line up without penetration or floating.
- Silhouette remains structurally coherent from near and far camera distances.

### Fail conditions

- **Gaps:** separation at arch spring points, buttress roots, or cap joins.
- **Tangent artifacts:** curvature shading breaks where arch meets straight wall.
- **Angle drift:** buttress leans/off-axes relative to wall normal.
- **Lighting contradictions:** contact points appear overlit or unnaturally dark compared with adjacent continuous surfaces.

---

## Template 05: Shadow overlap stacking

### Required pieces

- 3+ stackable/overlapping silhouette pieces (e.g., eaves, beams, trim ledges, overhangs).
- 1x wall backdrop and 1x floor receiver plane.
- At least one directional light and one fill/ambient setup representative of production.

Instantiate as:

- Build layered overlaps with progressively deeper offsets.
- Include one case with near-coplanar overlap to stress z precision.
- Capture identical arrangement at multiple light angles (e.g., low, mid, high sun).

### Expected visual result

- Contact shadows are stable and physically plausible across angles.
- Overlapping pieces do not produce flicker, moiré, or unstable penumbra jumps.
- Receiver surfaces show smooth gradient transitions without abrupt discontinuities.

### Fail conditions

- **Gaps:** visible light leaks where pieces should occlude.
- **Tangent artifacts:** shimmer/flicker from unstable normals or near-coplanar interference.
- **Angle drift:** stacked pieces reveal misalignment under grazing-light silhouettes.
- **Lighting contradictions:** shadow direction, softness, or intensity conflicts with scene light rig.

---

## Determinism and execution notes

- Use fixed transforms, fixed light rig presets, and fixed camera bookmarks for all runs.
- Do not hand-adjust piece placement between reruns; only replace source assets.
- Keep one test scene per template plus optional `_variant_*` scenes for mirrored or stress extremes.
- Treat these scenes as regression baselines for manual review and screenshot diffs.
