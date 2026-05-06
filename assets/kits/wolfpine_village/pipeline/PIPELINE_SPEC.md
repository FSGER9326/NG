# Pipeline Spec: Parity+ SVG Production

## Objective

Create Wolfpine assets at least equal to Infernus references, with a parity-plus quality target.

## Stages

1. **Plan**
   - Select batch scope from roadmap.
   - Confirm required module families and target variant counts.
2. **Generate**
   - Produce one SVG candidate per target asset ID.
   - Follow `SVG_TECH_ART_BIBLE.md` exactly.
3. **Review**
   - Score candidates using `SVG_SCORECARD.md`.
   - Reject/regenerate below-threshold candidates.
4. **Validate**
   - Run modular seam/adjacency checks for structural assets.
   - Validate gameplay readability at target scene scale.
5. **Promote**
   - Update production manifest after acceptance only.
   - Record qa score, family, orientation, compatibility metadata.
6. **PR**
   - Open PR with artifacts, scorecard summary, and validation evidence.

## Quality gates

- Minimum passing score: **85/100**
- No category below: **70/100**
- Hero quality target: **92/100**

Mandatory fail conditions:
- Inconsistent camera/projection.
- Inconsistent lighting direction.
- Unreadable silhouette at gameplay scale.
- Broken modular seams or elevation transitions.
- Flat/vector-icon look that violates Wolfpine style lock.

## Batch ordering

1. Foundation modulars (walls/floors/stairs/ramps).
2. Structural enrichers (arches/buttresses/columns/shadows).
3. Hero facades.
4. Hotspot props.
5. Decals/clutter/occluders.

## Canonical promotion rule

Only promote assets after scorecard pass + validation pass + manifest update.
