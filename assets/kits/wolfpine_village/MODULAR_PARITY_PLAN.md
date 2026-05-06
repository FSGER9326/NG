# Wolfpine Modular Parity Plan (Baseline: `Building_Infernus_1`)

This planning document maps the detected Infernus baseline family groups in `Building_Infernus_1` to Wolfpine-equivalent modular families, then defines parity-plus production targets.

Primary objective:

1. Reach **functional parity** with the Infernus baseline.
2. Lock each family to Wolfpine style/readability constraints.
3. Exceed parity with additional hand variants once approved.

---

## Status legend

- `planned`: scoped with requirements, not yet actively produced.
- `in_progress`: asset generation, paintover, or cleanup underway.
- `approved`: passes style lock + gameplay readability checks.
- `rejected`: does not satisfy criteria and must be remade.

---

## Wolfpine style lock (applies to all families)

- **Camera + projection:** pseudo-isometric consistency with existing Wolfpine kit.
- **Material language:** timber framing, worn plaster, frontier stone, slate, moss, mud/cobble adjacency.
- **Lighting:** warm late-afternoon or soft overcast; avoid harsh noir contrast.
- **Palette:** natural greens/earths; avoid saturated fantasy primaries.
- **Edge quality:** clean silhouettes and alpha edges suitable for kit snapping/compositing.
- **Gameplay readability:** silhouettes must telegraph walk-blocking, traversal, and transition points at a glance.

Any family instance that violates style lock is marked `rejected` until corrected.

---

## Family parity definitions

### 1) `wall_front_*`
- **Minimum variant target:** 8
- **Orientation / handedness:** straight front spans + left/right end-cap variants.
- **Snap intent:** edge chain for primary facade runs.
- **Readability constraints:** clear walk-blocking at wall base; window/trim detail cannot obscure collision read.
- **Acceptance criteria (style lock):** consistent plaster/timber rhythm; no perspective drift across chained segments.

### 2) `wall_side_*`
- **Minimum variant target:** 8
- **Orientation / handedness:** left-facing and right-facing side planes.
- **Snap intent:** side edges and depth-return transitions from `wall_front_*`.
- **Readability constraints:** side depth must read as non-walkable structure, not background-only paint.
- **Acceptance criteria (style lock):** side grain/stone courses align to front families without seam popping.

### 3) `wall_wide_*`
- **Minimum variant target:** 6
- **Orientation / handedness:** neutral wide spans plus mirrored alternates where needed.
- **Snap intent:** long edge fills between corner anchors.
- **Readability constraints:** repeating motifs must preserve visual rhythm, avoid tiling artifacts.
- **Acceptance criteria (style lock):** large-span shading remains Wolfpine-soft, with controlled micro-variation.

### 4) `wall_large_*`
- **Minimum variant target:** 6
- **Orientation / handedness:** broad massing pieces with left/right terminals.
- **Snap intent:** major frontage blocks and structural landmarks.
- **Readability constraints:** must communicate “major obstruction” clearly.
- **Acceptance criteria (style lock):** macro forms match settlement scale and do not overpower neighboring kit pieces.

### 5) `wall_medium_*`
- **Minimum variant target:** 8
- **Orientation / handedness:** standard midsize segments with mirrored end conditions.
- **Snap intent:** default interchange wall family for most layouts.
- **Readability constraints:** silhouette contrast must stay legible behind props/clutter.
- **Acceptance criteria (style lock):** joins seamlessly with large/small families through shared trim heights.

### 6) `wall_small_*`
- **Minimum variant target:** 10
- **Orientation / handedness:** short filler segments, caps, and broken-length alternates.
- **Snap intent:** gap fill, micro-corners, door/window adjacency.
- **Readability constraints:** tiny segments must still indicate pass/block boundaries.
- **Acceptance criteria (style lock):** maintains full material fidelity despite short footprint.

### 7) `stairs_*`
- **Minimum variant target:** 6
- **Orientation / handedness:** ascent/descent readability for left and right placements.
- **Snap intent:** elevation transitions between floor tiers and exterior paths.
- **Readability constraints:** top and base landings must be obvious for traversal affordance.
- **Acceptance criteria (style lock):** step pitch and shadowing remain consistent across all stair lengths.

### 8) `stairs_inverted_*`
- **Minimum variant target:** 4
- **Orientation / handedness:** inverse-facing complements to `stairs_*`.
- **Snap intent:** reverse approach vectors and mirrored layouts.
- **Readability constraints:** inversion must not confuse up/down interpretation.
- **Acceptance criteria (style lock):** mirrored logic preserved without introducing lighting inversion artifacts.

### 9) `ramp_*`
- **Minimum variant target:** 4
- **Orientation / handedness:** left/right ramp direction with short/medium runs.
- **Snap intent:** smooth grade transitions where stairs are too abrupt.
- **Readability constraints:** slope direction readable from silhouette and plank/stone lines.
- **Acceptance criteria (style lock):** ramps integrate naturally with mud/cobble ground language.

### 10) `archway_*`
- **Minimum variant target:** 6
- **Orientation / handedness:** front and side arch faces; broken/intact options.
- **Snap intent:** threshold transitions and framed passage nodes.
- **Readability constraints:** opening void must be unmistakable as traversable (if intended).
- **Acceptance criteria (style lock):** arch curvature and keystone details fit frontier masonry vocabulary.

### 11) `column_*`
- **Minimum variant target:** 6
- **Orientation / handedness:** cylindrical/square column forms with front/side visibility variants.
- **Snap intent:** structural repeats in porches, halls, and facade accents.
- **Readability constraints:** should read as narrow blockers/supports without swallowing path readability.
- **Acceptance criteria (style lock):** wear patterns and base/cap profiles align with Wolfpine masonry set.

### 12) `pillar_*`
- **Minimum variant target:** 6
- **Orientation / handedness:** heavier pillar alternatives, left/right edge-ready versions.
- **Snap intent:** corner reinforcement and gate framing.
- **Readability constraints:** must distinguish from `column_*` by mass and role.
- **Acceptance criteria (style lock):** bulkier geometry still retains coherent light direction and scale.

### 13) `buttress_*`
- **Minimum variant target:** 4
- **Orientation / handedness:** left-leaning and right-leaning support forms.
- **Snap intent:** wall-depth reinforcement at long spans/corners.
- **Readability constraints:** should imply structural support, not accidental debris.
- **Acceptance criteria (style lock):** attachment seams into walls are clean and perspective-correct.

### 14) `floor_upper_*`
- **Minimum variant target:** 6
- **Orientation / handedness:** upper-plane tiles/segments with edge/corner/topcap variants.
- **Snap intent:** elevated walkable surfaces.
- **Readability constraints:** walkable top plane must be clearly differentiated from vertical faces.
- **Acceptance criteria (style lock):** plank/stone texel density harmonized with lower floor families.

### 15) `floor_lower_*`
- **Minimum variant target:** 6
- **Orientation / handedness:** lower-plane segments with adjacency to walls and transitions.
- **Snap intent:** base-level walk surfaces and foundation interfaces.
- **Readability constraints:** avoid confusion with decorative decals; pathing plane must remain clear.
- **Acceptance criteria (style lock):** values/chroma support character readability over the floor.

### 16) Explicit shadow companions
- **Minimum variant target:** 1:1 companion for each non-trivial structural variant (target 80%+ coverage before approval pass).
- **Orientation / handedness:** shadow direction locked to Wolfpine light rig; mirrored shadows only when geometry mirror is valid.
- **Snap intent:** grounding for walls/stairs/arches/columns where baked contact is required.
- **Readability constraints:** shadows cannot fake collision where none exists; must reinforce, not contradict traversal.
- **Acceptance criteria (style lock):** soft-edged, palette-consistent shadows with controlled opacity and no halo edges.

---

## Completion matrix (parity tracking)

> Update `state`, `owner`, and `notes` during production reviews. Once baseline parity is `approved`, teams may append `*_plus` variants to exceed parity.

| Family | Min Variants | Orientation / Handedness Required | Primary Snap Intent | Current State | Owner | Notes |
|---|---:|---|---|---|---|---|
| wall_front_* | 8 | Front span + L/R end-caps | Edge chain | planned | unassigned | Baseline parity target from Infernus frontage set. |
| wall_side_* | 8 | Left-facing + right-facing | Edge/depth return | planned | unassigned | Must bridge cleanly with wall_front_* corners. |
| wall_wide_* | 6 | Wide neutral + mirror-safe alts | Long edge fill | planned | unassigned | Prioritize anti-tiling detail passes. |
| wall_large_* | 6 | Large mass + L/R terminals | Landmark frontage | planned | unassigned | Use for hero building outlines. |
| wall_medium_* | 8 | Mid spans + mirrored ends | Default wall interchange | planned | unassigned | Core production volume family. |
| wall_small_* | 10 | Short fillers + micro-caps | Gap/transition fill | planned | unassigned | Needed for kit closure quality. |
| stairs_* | 6 | L/R readable ascent-descent | Elevation transition | planned | unassigned | Include clear landing silhouettes. |
| stairs_inverted_* | 4 | Inverse-facing stair set | Mirrored transition | planned | unassigned | Validate against pathing overlays. |
| ramp_* | 4 | L/R slope direction | Grade transition | planned | unassigned | Keep slope readability high. |
| archway_* | 6 | Front/side arch + condition alts | Threshold/portal | planned | unassigned | Include traversable and blocked variants. |
| column_* | 6 | Front/side visibility forms | Structural repeat | planned | unassigned | Distinguish from pillar massing. |
| pillar_* | 6 | Heavy support + edge-ready L/R | Corner/gate framing | planned | unassigned | Reserve for major anchors. |
| buttress_* | 4 | Left-lean + right-lean | Wall reinforcement | planned | unassigned | Pair with large/wide wall sets. |
| floor_upper_* | 6 | Upper plane edge/corner variants | Elevated walk plane | planned | unassigned | Maintain crisp walkability cues. |
| floor_lower_* | 6 | Lower plane adjacency variants | Base walk plane | planned | unassigned | Harmonize with ground decals. |
| shadow companions | 80%+ of structural set | Light-rig locked, mirror-safe only | Contact grounding | planned | unassigned | Required before family can reach approved. |

---

## Approval gate (family-level)

A family can only move to `approved` when all are true:

1. Minimum variant target is met or exceeded.
2. Required orientation/handedness set is complete.
3. Snap intent validated in at least one production mock assembly.
4. Gameplay readability review passes (traversal/blocking/transition clarity).
5. Wolfpine style lock review passes.
6. Required shadow companions are present and consistent.

If any gate fails, set family state to `rejected` (or revert to `in_progress` after remediation scope) and add corrective notes.
