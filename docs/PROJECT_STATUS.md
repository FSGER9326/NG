# NG Project Status

This file is the main handoff point for future chats and AI agents.

## Current project identity

- Repo: `FSGER9326/NG`
- Working title: **NG / New Game**
- Genre: low-spec pseudo-isometric party CRPG
- Engine target: Godot 4.x, 2D, Compatibility renderer
- Main implementation style: text-first, data-driven, AI-maintainable

## Design target

Original dark low-fantasy CRPG with:

- detailed pseudo-isometric 2D areas
- party companions
- branching dialogue
- quest consequences
- faction reputation
- turn-based AP combat first
- extendable content files

## Current technical state

The repo currently contains:

- Godot project config
- main scene
- bootstrap script
- JSON data loader
- game-state stub
- quest-system stub
- starter area: `wolfpine_road`
- starter NPC: `captain_renna`
- starter companion: `brannoc`
- starter enemy: `border_bandit`
- starter item: `border_iron_sword`
- starter quest: `missing_caravan`
- validation script: `tools/validate_project.py`

## Current priority

Milestone 0.2: make the area prototype real.

Next useful tasks:

1. Add `AreaController` scene/script.
2. Render placeholder area background.
3. Load area actors from JSON.
4. Add simple clickable hotspots.
5. Add dialogue panel that can read JSON dialogue.
6. Run and fix `python tools/validate_project.py` after each data change.

## Working rule

If a future AI chat loses context, read this file first, then `docs/ROADMAP.md`, `docs/GAME_DESIGN.md`, and `docs/WORKFLOW.md`.
