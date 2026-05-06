# SVG Scorecard

This file is a quick SVG authoring checklist. The canonical Wolfpine promotion scorecard is:

```text
assets/kits/wolfpine_village/QUALITY_SCORECARD.md
```

Use the promotion scorecard for all `candidate_validated` and `accepted` decisions. Use this SVG checklist only to catch SVG-specific technical failures before a candidate enters formal promotion review.

## SVG Preflight Categories

Score each category 0-100 and treat any category below 70 as a regeneration signal:

1. Projection fidelity
2. Lighting/shadow coherence
3. Silhouette readability at gameplay scale
4. Material richness without clutter
5. Modular seam compatibility
6. SVG technical cleanliness/complexity budget
7. Primitive-marker compliance for structural SVGs

## Required Promotion Mapping

Before promotion review, convert SVG preflight observations into the canonical seven-category scorecard:

| SVG preflight concern | Canonical promotion category |
|---|---|
| Projection fidelity | Camera consistency |
| Silhouette readability | Silhouette readability at target scale |
| Modular seam compatibility | Modular seam compatibility |
| Lighting/shadow coherence | Lighting/shadow coherence |
| Material richness | Material/palette consistency |
| Path/traversal readability | Gameplay affordance clarity |
| SVG cleanliness, alpha/export hygiene, primitive markers | Cleanup/alpha integrity |

## Review template

```md
Asset ID:
Reviewer:
Date:
SVG preflight:
- Projection:
- Lighting:
- Readability:
- Material richness:
- Seam compatibility:
- Technical cleanliness:
- Primitive-marker compliance:
Result: PASS TO PROMOTION REVIEW / REGENERATE
Notes:
```
