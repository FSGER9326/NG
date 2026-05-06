# Wolfpine Autonomous Asset Creation Pipeline

This pipeline is the operational source of truth for autonomous SVG-first asset production in Codex Web + Web ChatGPT workflows.

## Why this exists

Codex Web PR flows are reliable for text files. SVG assets are text-based and can be committed via PR. Binary formats (PNG/JPG) may require external artifact storage, but this pipeline is designed to produce high-quality canonical assets using SVG-first production.

## Pipeline files

- `PIPELINE_SPEC.md` — full end-to-end production flow and gates.
- `ROLE_HANDOFF.md` — exact Codex/WebGPT ownership and handoff checklist.
- `SVG_TECH_ART_BIBLE.md` — non-negotiable visual and technical constraints.
- `SVG_SCORECARD.md` — objective acceptance scoring.
- `BATCH_SCHEDULE_W1_W3.md` — day-by-day execution plan.
- `PR_TEMPLATE.md` — standard PR body for autonomous art batches.

## Execution rule

No asset is canonical unless all of the following are true:
1. SVG tech art constraints are met.
2. Scorecard threshold is met.
3. Adjacency validation is passed for relevant modular classes.
4. Metadata is updated in the production manifest.
