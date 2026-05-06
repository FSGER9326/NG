# Wolfpine Batch State Machine

This state machine governs **batch-level progression** for `assets/kits/wolfpine_village` generation and promotion loops.

## Canonical states

Every batch is always in exactly one state:

1. `planned`
2. `generated`
3. `reviewed`
4. `validated`
5. `promoted`
6. `blocked`

## Transition rules

```text
planned -> generated -> reviewed -> validated -> promoted
```

Allowed side transition:

```text
planned/generated/reviewed/validated -> blocked
```

Unblock rule:

```text
blocked -> planned
```

No other transitions are valid.

## State entry criteria

### `planned`
- Batch scope is fixed (asset families + target count).
- Prompt/spec baseline is pinned in repo docs.
- Retry counters for each asset family are initialized.

### `generated`
- Candidates are generated for all in-scope asset families.
- Generation metadata is recorded (prompt hash/version + run identifier).
- Failures are classified (see retry policy) before review starts.

### `reviewed`
- Human/agent quality review completed against the current kit constraints.
- Each failed candidate has a failure class.
- Assets passing review are explicitly listed for validation.

### `validated`
- Required validators pass for the batch.
- Manifest references and file paths are consistent.
- Retry-policy obligations (including mandatory prompt/spec patches) are satisfied.

### `promoted`
- Approved assets are moved to canonical kit paths.
- Manifest statuses and batch notes are updated in the same change.
- Promotion record includes source batch and validation evidence.

### `blocked`
- Batch cannot progress due to unresolved dependency, repeated failure loop, or missing decision.
- Block reason and unblocking action are written in batch notes.

## Retry policy (required)

### 1) Max retry count per asset family
- Track retries independently for each asset family (for example: `building_facade`, `door_module`, `market_prop`).
- Hard limit: **3 retries per asset family** inside one batch cycle.
- Exceeding the limit moves the batch to `blocked` until scope/spec is updated.

### 2) Failure classification taxonomy
Every failed attempt must be tagged with one primary class:

- `projection` — camera angle/perspective/isometric read mismatch.
- `lighting` — value direction, shadow logic, or contrast mismatch.
- `seam` — alpha edge/fringe/tiling or integration boundary artifact.
- `readability` — silhouette/gameplay read failure at target scale.

### 3) Repeated same-cause failure rule
If the **same asset family** receives the **same failure class** in **2 consecutive retries**, a prompt/spec patch is mandatory before any additional regeneration.

Mandatory patch requirements:
- Patch is committed to repo (`prompt`, `spec`, or both).
- Patch note states the repeated cause and intended corrective change.
- Next regeneration run references the patch commit/ID in batch notes.

Without this patch, further retries are invalid.

## Deterministic role handoff (WebGPT -> Codex)

To avoid non-deterministic loops, prompt adjustment and regeneration must follow this fixed order:

1. **WebGPT prompt-adjustment step**
   - Read latest failure log for the asset family.
   - Emit exactly one bounded prompt/spec delta addressing one primary failure class.
   - Write delta into repo-tracked spec/prompt notes before regeneration.

2. **Codex regeneration step**
   - Regenerate only the affected asset family with the patched prompt/spec.
   - Increment retry counter for that family.
   - Record run output and classification result.

3. **Gate decision**
   - If class resolved, continue toward `reviewed`/`validated`.
   - If same class repeats twice consecutively, enforce mandatory patch rule.
   - If retry max reached, transition batch to `blocked`.

This sequence is mandatory for each retry loop.
