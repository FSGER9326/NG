# Wolfpine Village Quality Scorecard

This scorecard is **required for every candidate asset before promotion** into the Wolfpine Village production set.

## Purpose

Use this scorecard to gate candidate assets for visual quality, gameplay readability, and kit compatibility before updating manifests and ledgers.

## Weighted Criteria (100 points total)

| Category | Weight | What to evaluate |
|---|---:|---|
| Camera consistency | 20 | Perspective, horizon behavior, and camera-angle alignment with the kit standard in `GENERATION_SPECS.md`. |
| Silhouette readability at target scale | 20 | Recognizability and shape clarity at intended in-game display size. |
| Modular seam compatibility | 15 | Edge matching, tile joins, and snap behavior with existing modular neighbors. |
| Lighting/shadow coherence | 15 | Directionality, softness/hardness, and grounding shadows relative to scene baseline. |
| Material/palette consistency | 10 | Surface response and color-family alignment with Wolfpine palette constraints. |
| Gameplay affordance clarity | 10 | Visual communication of traversable/blocking/interactive intent. |
| Cleanup/alpha integrity | 10 | Fringing, haloing, matte contamination, transparency artifacts, and crop cleanliness. |

Scoring formula:

- Each category is scored from **0–100**.
- Weighted total = `sum(category_score * category_weight / 100)`.
- Maximum weighted total = **100**.

## Required Thresholds

A candidate must satisfy **all** gating checks:

1. **Per-category floor:** no category below **70/100**.
2. **Promotion threshold:** weighted total must be **85.0+** to be promotable.
3. **Hero asset threshold:** weighted total must be **92.0+** to be tagged as **hero asset**.

If any category is below the floor, the candidate is **blocked**, even if total score exceeds 85.

## Reviewer Workflow (Required)

1. **Confirm spec compliance context** in `assets/kits/wolfpine_village/GENERATION_SPECS.md` (camera, scale, palette, and kit constraints).
2. **Score candidate with this scorecard** and record per-category values plus weighted total in review notes.
3. **Apply gate decision**:
   - `<85.0` or any category `<70`: reject / send back for revision.
   - `85.0–91.9` with all categories `>=70`: promote as standard production asset.
   - `>=92.0` with all categories `>=70`: eligible for hero designation.
4. **Update production tracking** in `assets/kits/wolfpine_village/production_manifest_2026_05_06.json` with decision status and score summary.
5. **Register promoted asset** in `assets/ledger/assets.json` only after passing the thresholds above.

## Suggested Review Record Template

```md
Candidate: <asset_id_or_filename>
Reviewer: <name>
Date: <YYYY-MM-DD>

Scores (0-100):
- Camera consistency (20):
- Silhouette readability at target scale (20):
- Modular seam compatibility (15):
- Lighting/shadow coherence (15):
- Material/palette consistency (10):
- Gameplay affordance clarity (10):
- Cleanup/alpha integrity (10):

Weighted total:
Gate result: Reject | Promote | Promote + Hero Eligible
Notes:
```
