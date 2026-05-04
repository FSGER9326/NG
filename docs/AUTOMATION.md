# NG Automation Guide

This file explains what is automatic in the NG repository and how to use it without needing to remember GitHub details.

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
```

Purpose:

- catches invalid JSON
- catches duplicate IDs
- catches missing common file references

### 2. Godot smoke test

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

Purpose:

- catches many Godot script/scene load errors without requiring the user to start the game manually

Why it is not on every push:

- it downloads Godot and is slower than data validation
- it should be used for PRs or when manually checking runtime breakage

### 3. Manual Windows prototype build

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

### 4. Local one-click update scripts

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

## What is not automatic yet

The repo does not yet automatically:

- update your local Godot project folder without you running a script
- import external assets
- make game-design decisions
- generate final art
- publish releases automatically

## Recommended normal user workflow

1. ChatGPT changes the repo.
2. Run `tools/update_ng.bat` locally.
3. Open Godot.
4. Test if needed.
5. If there is a bug, send the error text or screenshot.

## Recommended AI workflow

1. Read `docs/PROJECT_STATUS.md`.
2. Read `docs/ROADMAP.md`.
3. Make small text-first changes.
4. Update validation if a new data format is introduced.
5. Update wiki/docs if the player-facing game changes.
6. Let GitHub Actions validate the repo.

## Safety rules

- Do not store secrets in the repo.
- Do not auto-import assets without license review.
- Do not auto-push generated binary dumps.
- Keep `export_credentials.cfg` ignored.
- Keep `export_presets.cfg` tracked so CI can build.
