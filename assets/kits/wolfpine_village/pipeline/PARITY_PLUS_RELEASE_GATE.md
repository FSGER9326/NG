# PARITY PLUS RELEASE GATE

## Purpose
Define objective release KPIs required to pass the Parity Plus gate for the Wolfpine Village pipeline.

## Objective Release KPIs

### 1) Modular Family Coverage Count
- **Requirement:** Each planned modular family for this kit must be represented in the parity matrix and have release-ready outputs.
- **Pass condition:** **100% family coverage** against the approved family list in the current scope baseline.
- **Report evidence:** Coverage table listing each family, status, and artifact links.

### 2) Minimum Approved Variants per High-Frequency Family
- **Requirement:** High-frequency families must have enough approved variants to avoid visible patterning under normal gameplay/editor composition.
- **Pass condition:** **Minimum 4 approved variants per high-frequency family**.
- **Report evidence:** Variant approval log with reviewer sign-off and version IDs.

### 3) Seam Pass Rate Target
- **Requirement:** Modules must pass seam integrity checks across all required adjacency pairings and orientation cases.
- **Pass condition:** **≥ 99% seam pass rate** in the final validation run.
- **Report evidence:** Validation output summary including total seam checks, passes, fails, and known exceptions (if any).

### 4) Readability Score Target
- **Requirement:** Layout/readability quality must meet the project readability rubric for navigation clarity and silhouette differentiation.
- **Pass condition:** **Readability score ≥ 8.5/10** averaged across the final review panel.
- **Report evidence:** Scoring sheet with individual reviewer scores and computed average.

### 5) Repetition Masking Checks in 3 Sample Compositions
- **Requirement:** Repetition masking must be evaluated in representative scenes.
- **Pass condition:** **3/3 sample compositions pass** masking checks with no critical repetition flags.
- **Report evidence:** Composition captures, checklist results, and reviewer notes for each sample.

## Hardening Label & Batch 2+ Production Constraint
- The pipeline **must not** be labeled **"fully hardened"** until all KPIs above are met.
- A **completion report is required** before assigning the "fully hardened" label.
- **Large-scale Batch 2+ production must not begin** until the completion report is approved and the gate is formally marked as passed.

## Required Completion Report (Gate Closeout)
The completion report must include:
1. KPI-by-KPI pass/fail summary.
2. Supporting evidence links for every KPI.
3. Open issues and explicit risk acceptance (if applicable).
4. Final approval signatures (content lead + pipeline/tech lead).
5. Date/time of gate decision and release tag/reference.
