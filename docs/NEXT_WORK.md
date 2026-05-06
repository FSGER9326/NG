# Next Work Queue

This file is a durable handoff queue for future NG work sessions.

Future chats should read this after `repo-context.txt` and `docs/PROJECT_STATUS.md` when deciding what to do next.

## Current first-playable target

Build a compact first-playable vertical slice:

```text
Main Menu
→ Character Creator
→ Wolfpine Road
→ Missing Caravan evidence
→ Wolfpine Village pressure
→ witness/dialogue follow-up
→ one meaningful resolution
→ save/load survives it
```

## Active repo-work protocol

Follow `docs/REPO_WORK_PROTOCOL.md` for all GitHub work.

Key rules:

- Read context first.
- Preflight before writes.
- Pick one PR mode: content, runtime, tooling, docs, or asset.
- Keep PR scope coherent.
- Avoid mixing assets into content PRs.
- Use a hard write budget.
- Use the dirty-branch escape hatch after two failed write/update/delete attempts.
- Finish the current PR loop before starting a new feature.

## Immediate cleanup / carryover

### 1. Finish or replace Miller Tovin witness work

There is/was a dirty branch or PR for Miller Tovin that mixed an `assets/` placeholder into a content PR.

Preferred clean path:

```text
Create clean content-only branch from main.
Add only:
- data/actors/npcs/miller_tovin.json
- dialogue/npcs/miller_tovin.json
- areas/wolfpine_village/actors.json
- tests/scenarios/wolfpine_miller_tovin_witness.json
Do not add assets/ files.
Reuse an existing placeholder portrait until a separate asset PR exists.
Open clean PR.
Close/abandon dirty PR if needed.
Run CI.
Merge if green.
```

### 2. Update stale project status / roadmap

After recent merged work, durable docs should reflect:

- manual portrait selection is implemented
- character creator profile preview is implemented
- `main_runtime_v3.gd` is the active portrait/profile-preview runtime extension
- issue #13 is no longer the next active implementation target

Do this as a separate docs PR.

### 3. Make Missing Caravan completable

Add one first-playable resolution path after road + village evidence.

Target branch type: content PR.

Possible gated Renna branch:

```text
I know how the caravan lie reached Wolfpine.
```

Possible conditions:

```text
wolfpine_village_pressure_reported = true
wolfpine_miller_names_mara_vell = true
```

Possible effects:

```text
missing_caravan -> resolved
wolfpine_caravan_resolved = true
one consequence flag for quiet/public resolution
```

Add scenario coverage.

### 4. Make Brannoc recruitable

Target branch type: runtime/content depending on existing effect support.

Desired result:

- explicit Brannoc recruitment dialogue
- `brannoc_recruited` flag
- Brannoc added to party
- scenario coverage

### 5. Harden save/load over the first-playable loop

After Missing Caravan completion and Brannoc recruitment exist, add a scenario that saves and loads:

- player profile
- portrait_id
- current area
- quest stage
- first-playable flags
- recruited party member

### 6. Minimal combat prototype

Only after the investigation loop is playable and durable.

Keep the first combat shell small:

- combat screen/shell
- one party marker
- one enemy
- basic turn/AP loop
- attack
- victory
- return to area
- scenario coverage

## Avoid next

Do not prioritize:

- large asset imports
- final art lock-in
- broad runtime rewrites
- unrelated documentation cleanup
- new quest branches without scenario coverage

## Long work block ledger format

End each deep work block with:

```text
Done:
Validated:
Merged/PR:
Blocked/Remaining:
Next:
```
