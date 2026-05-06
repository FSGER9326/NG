# Wolfpine Village Quality Scorecard

This scorecard is **required for every candidate asset before promotion** into the Wolfpine Village production set.

## Purpose

Use this scorecard to gate candidate assets for visual quality, gameplay readability, and kit compatibility before updating manifests and ledgers.

This is the canonical promotion scorecard for Wolfpine. SVG-specific notes may add technical constraints, but promotion uses the weighted criteria below.

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
3. **Attach evidence**:
   - seam or modular validation evidence,
   - gameplay-scale readability evidence,
   - optional preview/capture links for visual review.
4. **Apply gate decision**:
   - `<85.0` or any category `<70`: reject / send back for revision.
   - `85.0–91.9` with all categories `>=70`: eligible for `candidate_validated`.
   - `>=92.0` with all categories `>=70`: eligible for hero designation after lead review.
5. **Promote only after validation**:
   - update `assets/kits/wolfpine_village/production_manifest_2026_05_06.json`,
   - keep status transitions compatible with `planned -> generated_candidate/external_candidate -> cleaned -> candidate_validated -> accepted`,
   - register accepted assets in `assets/ledger/assets.json` only after all gates pass.

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
Gate result: Reject | Candidate Validated | Accept | Hero Eligible
Evidence:
- Seam/modular:
- Scale/readability:
Notes:
```

## Manifest Status + Validator Enforcement

When this scorecard is used to promote kit assets, reviewers must enforce these manifest lifecycle rules:

- Required fields present: `id`, `candidate_file` or `file`, `module_family`, `orientation`, `join_compatibility`, `qa_score`, and lifecycle status.
- Allowed asset lifecycle:
  `planned -> generated_candidate/external_candidate -> cleaned -> candidate_validated -> accepted`
- Disallowed transitions:
  - direct generated candidate -> accepted without scorecard evidence,
  - accepted status without seam/readability evidence,
  - untracked file paths or missing provenance.

A transition to `accepted` must include both:

1. Completed scorecard evidence using this document's weighted review.
2. Seam/readability evidence confirming modular join behavior and target-scale clarity.

Without both evidence items, validators must fail promotion.
