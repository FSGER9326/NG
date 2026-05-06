# NG Asset Session Protocol (Idiot-Proof)

This protocol is the required operating procedure for generating and promoting NG assets.

If followed exactly, every accepted asset should be production-ready, traceable, and reusable.

---

## 0) Non-negotiable principles

1. **Repo is truth**: no asset is considered real until tracked in repo files.
2. **Manifest-first**: do not generate "randomly"; generate against planned manifest entries.
3. **Gate-based**: an asset only moves forward by passing all gates.
4. **No silent exceptions**: failed checks must be logged as fail/reject with reason.
5. **Small batches**: batch size is intentionally limited to keep quality and consistency high.

---

## 1) Session bootstrap (every new Codex/GPT session)

Before any generation or editing work:

1. Read in order:
   - `docs/PROJECT_STATUS.md`
   - `docs/ROADMAP.md`
   - `docs/WORKFLOW.md`
   - `docs/ART_BIBLE.md`
   - `docs/ASSET_POLICY.md`
   - `docs/ASSET_PRODUCTION.md`
   - `docs/GENERATED_ASSET_PIPELINE.md`
2. Run project and asset validators once.
3. Report current branch + git status.
4. Identify exactly one target asset kit and one batch.

If any step is skipped, **stop** and do not produce assets.

---

## 2) Asset state machine (must be explicit)

Every asset in a kit must stay in one of these states:

```text
planned -> generated_candidate/external_candidate -> cleaned -> candidate_validated -> accepted
```

Additional terminal/side states:

- `rejected` (failed quality, style, legality, or technical gates)
- `blocked` (missing dependency/info)

No asset may jump states.

---

## 3) Batch contract (hard limits)

A single production batch must satisfy all of the below:

- 5 to 12 assets maximum
- one kit/theme only
- one quality target only (e.g., candidate_validated or accepted)
- one PR only

Required batch files:

- batch plan markdown
- manifest updates
- produced files
- QA notes
- validator outputs summary

---

## 4) Canonical directory and naming rules

1. Naming: lowercase `snake_case` only.
2. IDs must be stable once created.
3. Intended file path in manifest must match actual file path.
4. No exploratory dump files inside canonical `assets/` production paths.

---

## 5) Mandatory quality gates

An asset can only be marked `accepted` if it passes **all** gates below.

### Gate A — Style and gameplay readability

- correct pseudo-isometric perspective for NG
- clear silhouette at gameplay scale
- coherent with current kit style and palette
- no unreadable clutter, text, logos, watermark artifacts

### Gate B — Legal and provenance

- source kind is explicit (`generated`, `external`, `handmade`)
- source note/prompt summary recorded
- license status recorded and compatible
- no copy-like resemblance to a restricted third-party identity

### Gate C — Technical image quality

- PNG + RGBA
- true transparency where required
- no obvious edge halo/fringe
- approved canvas size class
- pivot/contact bounds documented when relevant

### Gate D — Manifest integrity

- required fields present
- status transition valid
- file exists
- naming conventions pass

### Gate E — In-engine readiness

- scale reads correctly against player/NPC references
- placement does not break area readability
- no obvious visual clash with area context

If any gate fails, asset returns to previous state or moves to `rejected`.

---

## 6) Absolute do-not-accept checklist

Do not accept any asset that has one or more of:

- uncertain or incompatible license
- wrong camera angle
- muddy silhouette
- baked background/checkerboard artifacts
- unresolved alpha halo
- missing manifest linkage
- missing provenance note
- mismatched filename vs manifest `intended_file`

---

## 7) Session output format (required)

At end of each asset session, provide a concise report with:

1. **Batch scope** (kit + asset IDs)
2. **State changes** per asset
3. **Gate results** per asset (A/B/C/D/E pass/fail)
4. **Validator commands + outcomes**
5. **Remaining risks**
6. **Next smallest batch** recommendation

---

## 8) Enforcement commands (run every batch)

From repo root:

```bash
python tools/validate_asset_kits.py
python tools/validate_asset_production_batches.py
python tools/validate_asset_reviews.py
python tools/validate_asset_review_outcomes.py
python tools/validate_generated_assets.py
python tools/validate_promoted_png_files.py
python tools/validate_promoted_png_headers.py
python tools/validate_project.py
```

If a command fails, do not mark affected assets `accepted`.

---

## 9) Golden prompts and prompt drift control

To keep a growing library consistent:

1. Maintain one approved prompt template per asset class.
2. Allow only one controlled variable change at a time.
3. Record prompt deltas in batch notes.
4. Reject generations that drift from established kit look.

---

## 10) Library growth strategy for creative freedom

To maximize long-term flexibility, grow in this order:

1. **Foundation primitives**: terrain, walls, structural modules
2. **Core functional props**: doors, stairs, wells, market pieces
3. **Variant layers**: damaged, poor, noble, seasonal, faction variants
4. **Biome extension packs**: snow, marsh, highland, urban district
5. **Narrative overlays**: banners, clues, event-state variants

This yields combinatorial reuse instead of one-off scene art.

---

## 11) Handoff contract for any future session

Use this handoff block exactly:

```text
Read docs/WORKFLOW.md, docs/ASSET_POLICY.md, docs/ASSET_PRODUCTION.md, docs/GENERATED_ASSET_PIPELINE.md, and docs/ASSET_SESSION_PROTOCOL.md first. Operate manifest-first. Use strict gate-based promotion. Do not mark assets accepted unless all gates pass and validators succeed. Produce only one small batch with explicit state transitions and QA report.
```

---

## 12) Definition of done for an accepted asset

An asset is done only when all are true:

- asset file exists at intended path
- manifest status is `accepted`
- provenance/license notes are present
- technical checks and validators pass
- in-engine readiness check passed
- batch report recorded

If any item is missing, the asset is not done.

---

## 13) Agent registration for fast autonomous scene building

Yes: in addition to process docs, agents need machine-readable registration.

Canonical registry file:

```text
data/asset_registry/scene_builder_registry.json
```

This registry should declare, per kit:

- manifests to read first
- prompt/spec source files
- scene targets
- required validator commands
- hard scene-building rules (accepted-only assets, layout constraints, no untracked paths)

Agent rule: before building or modifying a scene, load the registry entry for that kit and follow it as the execution contract.

