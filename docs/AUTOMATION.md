# NG Automation Guide

This file explains what is automatic in the NG repository and how to use it without needing to remember GitHub details.

## Operating model

The user should not need to manage GitHub directly during normal development.

ChatGPT/AI agents should manage repository mechanics:

- read the durable handoff docs first
- create small branches instead of pushing broad changes to `main`
- open or update focused pull requests
- keep status docs current when priorities change
- watch validation results and report only meaningful decisions/results back to the user
- avoid mixing unrelated runtime, content, asset, and roadmap work in one PR

`main` should be treated as the stable baseline. Work should land through small PRs after validation.

## Current automation layers

### 1. Data validation on push and pull request

File:

```text
.github/workflows/validate.yml
```

Runs automatically when:

- code is pushed to `main`
- a pull request targets `main`
- manually triggered from GitHub Actions

What it does:

```bash
python tools/validate_project.py
python tools/validate_character_creation.py
python tools/validate_asset_kits.py
```

Purpose:

- catches invalid JSON
- catches duplicate IDs
- catches missing common file references
- catches character creation option/tag/modifier drift
- catches asset kit manifest drift

### 2. Godot smoke and scenario test

File:

```text
.github/workflows/godot-smoke.yml
```

Runs when:

- a pull request targets `main`
- manually triggered from GitHub Actions

What it does:

- downloads Godot 4.3 Linux
- opens the project headlessly
- loads `game/scenes/main.tscn`
- loads and instantiates `game/scenes/area/area_scene.tscn`
- calls `load_area("wolfpine_road")`
- runs every JSON scenario under `tests/scenarios/*.json`
- uploads `debug/latest/` as the `NG-godot-debug-logs` artifact

Purpose:

- catches many Godot script/scene load errors without requiring the user to start the game manually
- catches scenario regressions before merge
- produces logs for AI-assisted diagnosis

Why it is not on every push:

- it downloads Godot and is slower than data validation
- it should be used for PRs or when manually checking runtime breakage

### 3. PR scope hygiene check

File:

```text
tools/check_pr_hygiene.py
```

Purpose:

- lists changed files by project category
- warns about oversized PRs
- fails mixed-scope PRs that touch too many core categories at once
- warns when runtime/content/area/data changes are missing scenario or validation coverage
- warns when asset changes lack docs/metadata context

Recommended workflow file:

```text
.github/workflows/pr-hygiene.yml
```

If the workflow file is not present yet, run the checker manually from a branch diff:

```bash
git diff --name-only origin/main...HEAD > changed_files.txt
python tools/check_pr_hygiene.py changed_files.txt
```

### 4. Pull request template

File:

```text
.github/pull_request_template.md
```

Purpose:

- forces every PR to state change type, scope, validation, and handoff note
- makes future chats easier to recover
- reduces vague or multi-purpose branches

### 5. Manual Windows prototype build

File:

```text
.github/workflows/build-windows.yml
```

Runs when:

- manually triggered from GitHub Actions

What it does:

- downloads Godot 4.3 Linux
- downloads Godot export templates
- runs data validation
- exports a Windows build using `export_presets.cfg`
- uploads an artifact named `NG-windows-prototype`

Purpose:

- creates a downloadable Windows prototype build without requiring local Godot export setup

### 6. Local one-click update scripts

Files:

```text
tools/update_ng.bat
tools/update_ng.ps1
```

What they do:

- pull the latest repo changes with Git
- run `python tools/validate_project.py`
- show an error if the local folder has conflicts or validation fails

Best use:

- double-click `tools/update_ng.bat` after ChatGPT pushes changes
- then open Godot and test normally

## Recommended branch and PR rules

Use branches by intent:

```text
cleanup/*
ci/*
fix/*
feature/*
content/*
docs/*
assets/*
```

Preferred PR sizes:

- docs/status cleanup: small and merge early
- CI/validation: one workflow or validator at a time
- content data: one quest, one area stub, or one dialogue cluster at a time
- runtime code: one system behavior at a time, with scenario coverage if possible
- assets: one coherent kit or metadata change at a time, no large dumps

## Recommended PR triage order during cleanup

When the repo has several open PRs, triage in this order:

1. CI/validation fixes that make future checks more reliable.
2. Scenario fixture/schema normalization.
3. Runtime bugfixes needed for smoke/scenario pass.
4. Docs/status checkpoint updates.
5. Content PRs, one at a time.
6. Asset imports or generation work only after asset policy/metadata is ready.

## What is not automatic yet

The repo does not yet automatically:

- update your local Godot project folder without you running a script
- import external assets
- make game-design decisions
- generate final art
- publish releases automatically
- enforce GitHub branch protection settings from inside the repo

## Recommended normal user workflow

1. Ask ChatGPT for the next project goal in plain language.
2. ChatGPT manages GitHub branches, PRs, docs, and validation.
3. Run `tools/update_ng.bat` locally only when you want to test the latest merged build.
4. Open Godot and test if needed.
5. If there is a bug, send the error text, screenshot, or debug bundle.

## Recommended AI workflow

1. Read `docs/CURRENT_CHECKPOINT.md` if present.
2. Read `docs/PROJECT_STATUS.md`.
3. Read `docs/ROADMAP.md`.
4. Read `docs/WORKFLOW.md`.
5. Read `docs/BUGFIXING.md`.
6. Inspect open PRs before starting new work.
7. Make small text-first changes on a branch.
8. Update validation if a new data format is introduced.
9. Update status/roadmap docs if behavior, priority, or scope changes.
10. Let GitHub Actions validate the repo.
11. Report changed files, validation status, and the next recommended action.

## Safety rules

- Do not store secrets in the repo.
- Do not auto-import assets without license review.
- Do not auto-push generated binary dumps.
- Keep `export_credentials.cfg` ignored.
- Keep `export_presets.cfg` tracked so CI can build.
