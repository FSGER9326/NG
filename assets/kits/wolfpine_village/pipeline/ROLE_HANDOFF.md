# Codex + WebGPT Role Handoff Protocol

## Primary role split

### WebGPT
- Research references, style risk patterns, and prompt refinements.
- Propose concise prompt deltas when failures repeat.
- Flag consistency drifts across a batch.

### Codex
- Generate or edit SVG assets in repo.
- Apply scorecard, enforce gates, and update manifest/docs.
- Prepare validation scene references and PR content.

## Handoff checklist (per asset)

1. **WebGPT prep**
   - Provide prompt block and failure-avoidance notes.
2. **Codex generation**
   - Create candidate SVG in batch folder.
3. **Codex QA**
   - Fill scorecard line-item scores.
4. **Codex validation**
   - Confirm seam/transition compatibility where applicable.
5. **Codex promotion**
   - Update manifest metadata and batch summary.
6. **WebGPT review pass**
   - Suggest micro-adjustments for next candidate if needed.

## Escalation

If two consecutive candidates fail the same criterion:
- Pause generation for that family.
- Patch prompt/spec before continuing.
