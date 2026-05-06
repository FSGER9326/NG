# Wolfpine Village Production Roadmap

This roadmap defines three production waves for the Wolfpine Village kit and establishes dependencies, throughput targets, and review criteria. All wave gates must be evaluated against `QUALITY_SCORECARD.md` before promotion.

## Wave 1 — Foundation Modulars

### Scope
- Core walls
- Floors
- Stairs/ramps
- Corners
- Shadows

### Dependency graph
1. **Generation specs baselined** (`GENERATION_SPECS.md`).
2. **Palette + value range locked** for foundation material set.
3. **Core walls** complete first (anchor dimensions and trim language).
4. **Floors** and **corners** built from wall scale + snapping rules.
5. **Stairs/ramps** built after floor elevation increments are fixed.
6. **Shadows** authored last, after all foundation silhouettes are final.

### Target asset counts
- Core walls: **16**
- Floors: **10**
- Stairs/ramps: **8**
- Corners: **10**
- Shadows: **12**
- **Wave 1 total target: 56 assets**

### Definition of done
- All assets tile or snap without visible seam breaks in representative test layouts.
- Scale, pivot, and orientation conventions are consistent across the full wave.
- No missing directional variants where gameplay navigation requires reversibility.
- Foundation set supports at least one full “small block” village assembly without placeholders.

### Review gate (QUALITY_SCORECARD.md)
- Pass minimum thresholds in `QUALITY_SCORECARD.md` for:
  - Modularity / fit reliability
  - Readability at gameplay camera distances
  - Material/palette consistency
  - Technical hygiene (naming, pivots, export integrity)
- Gate decision: **Wave 2 cannot start until Wave 1 scorecard pass is recorded**.

---

## Wave 2 — Structural Enrichers

### Scope
- Arches
- Buttresses
- Columns/pillars
- Roof-gap variants
- Facade kits

### Dependency graph
1. **Wave 1 approved** and frozen as structural baseline.
2. **Columns/pillars** authored first (used as load-bearing motif).
3. **Arches** derived from validated column spacing.
4. **Buttresses** adapted to wall heights and corner geometries from Wave 1.
5. **Roof-gap variants** depend on final roofline breakpoints and stair landing heights.
6. **Facade kits** assembled last from all approved enrichers for combinatorial coverage.

### Target asset counts
- Arches: **12**
- Buttresses: **10**
- Columns/pillars: **12**
- Roof-gap variants: **8**
- Facade kits: **10**
- **Wave 2 total target: 52 assets**

### Definition of done
- Enricher modules add silhouette complexity without breaking Wave 1 snap logic.
- Each enricher family includes enough variants to avoid visible repetition in adjacent placements.
- Facade kits can be layered onto at least 80% of eligible Wave 1 wall spans.
- No collision or overlap regressions in canonical street and courtyard layout tests.

### Review gate (QUALITY_SCORECARD.md)
- Pass minimum thresholds in `QUALITY_SCORECARD.md` for:
  - Structural coherence with foundation set
  - Visual variety vs. repetition control
  - Composition quality in mid-density blockouts
  - Technical correctness in attachment/snap behavior
- Gate decision: **Wave 3 unlock requires signed scorecard pass for Wave 2**.

---

## Wave 3 — Hero + Dressing + Biome Polish

### Scope
- Signature facades
- Focal props
- Clutter/decals/occluders
- Palette harmonization pass

### Dependency graph
1. **Wave 1 + Wave 2 approved** and treated as locked production base.
2. **Signature facades** established first to define final visual identity and hierarchy.
3. **Focal props** produced to support key sightlines and landmark readability.
4. **Clutter/decals/occluders** distributed after major sightline and traversal checks.
5. **Palette harmonization pass** performed last across all three waves to resolve drift.

### Target asset counts
- Signature facades: **8**
- Focal props: **14**
- Clutter/decals/occluders: **28**
- Palette harmonization pass outputs: **1 global pass package**
- **Wave 3 total target: 50 deliverables**

### Definition of done
- At least three showcase compositions read as distinct districts while remaining stylistically unified.
- Hero assets establish clear focal hierarchy at long, mid, and close camera ranges.
- Dressing improves lived-in density without introducing navigation ambiguity.
- Palette harmonization eliminates cross-wave saturation/value mismatches and preserves biome intent.

### Review gate (QUALITY_SCORECARD.md)
- Pass minimum thresholds in `QUALITY_SCORECARD.md` for:
  - Hero readability and composition impact
  - Set-level cohesion across all waves
  - Biome authenticity and palette control
  - Final production readiness (packaging and integration quality)
- Gate decision: **Final promotion only after Wave 3 scorecard pass and full-kit sign-off**.
