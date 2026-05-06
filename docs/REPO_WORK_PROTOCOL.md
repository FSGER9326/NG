# Repository Work Protocol

This protocol defines how AI-assisted work should proceed in this repository.

The goal is to keep GitHub work fast, reviewable, and resistant to connector or branch-state errors.

## Source of truth

For code-related, implementation, debugging, architecture, validation, or repository-planning work, read `repo-context.txt` first when it exists.

If `repo-context.txt` is missing, unavailable, stale, or clearly incomplete, fall back to direct repository reads.

## Preflight before writes

Before any GitHub write action, produce a concise preflight:

```text
PR mode:
Objective:
Planned file ledger:
- path — add/update/delete — reason — category
Hygiene risk:
Validation plan:
Write budget:
Stop condition:
```

Do not write until the file ledger is internally consistent.

If the user says `keep working`, proceed after the preflight unless approval is explicitly required.

## PR modes

Choose exactly one primary mode for a PR.

### Content PR

Allowed:

```text
data/
dialogue/
areas/
tests/scenarios/
```

Avoid unless explicitly required:

```text
assets/
game/scripts/
tools/
.github/
docs/
```

### Runtime PR

Allowed:

```text
game/scripts/
tests/scenarios/
tools/validators when required
```

Avoid:

```text
assets/
large content expansion
docs cleanup
```

### Tooling PR

Allowed:

```text
tools/
.github/
docs/ when documenting the tool or process
```

Avoid:

```text
game content
dialogue
assets
```

### Docs PR

Allowed:

```text
docs/
wiki/
README-style files
```

Avoid:

```text
runtime changes
content changes
assets
```

### Asset PR

Allowed:

```text
assets/
asset manifests
asset pipeline docs
asset validators
```

Avoid:

```text
quest changes
dialogue changes
runtime changes
```

## Write budget

Default target:

```text
one branch
one coherent PR
one corrective CI fix at most
one merge
```

For file writes:

- Prefer four or fewer file writes.
- If more than four files are needed, show a file ledger first.
- If more than eight files are needed, split into separate PRs unless explicitly approved.

## Dirty branch escape hatch

If two write, update, or delete attempts fail on the same branch or file:

1. Stop repairing that branch.
2. Create a fresh branch from `main`.
3. Reapply only the intended final file set.
4. Open a clean PR.
5. Close or abandon the dirty PR if needed.

Do not keep retrying stale SHA or delete operations indefinitely.

## Finish current loop first

If an open PR exists from the current work block, do not start a new feature until the PR is handled:

- merge if green
- apply one narrow fix if CI exposes a clear blocker
- close or abandon if dirty
- report the blocker if it cannot be fixed safely

## No opportunistic extras

Only add files required for the stated PR objective and validation.

Do not add opportunistic placeholders, assets, docs cleanup, refactors, or tooling while working on a content/runtime PR.

Examples:

- Do not add `assets/` files to a content PR.
- Do not update roadmap/status docs inside a runtime PR unless the runtime PR is explicitly a handoff PR.
- Do not add generated assets without manifests and asset-policy coverage.

## Validation expectations

Use CI as the final gate.

Common local/CI checks include:

```bash
python tools/validate_project.py
python tools/validate_character_creation.py
python tools/validate_portraits.py
python tools/validate_quest_seeds.py
python tools/validate_gdscript_helpers.py
python tools/validate_asset_kits.py
python tools/validate_runtime_shims.py
python tools/validate_generated_assets.py
```

Scenario changes should include focused scenario coverage when possible.

## Long work block ledger

End long work blocks with:

```text
Done:
Validated:
Merged/PR:
Blocked/Remaining:
Next:
```
