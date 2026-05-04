# NG — New Game RPG

**NG** is a low-spec, pseudo-isometric, party-based RPG project designed to be built and maintained through text-first files.

The project target is an original dark low-fantasy CRPG inspired by the *function* of classic Infinity Engine games: dense 2D areas, party companions, tactical combat, branching dialogue, faction consequences, and a content pipeline that can grow without rewriting the engine.

## Core principles

- **AI-maintainable:** important systems live in plain text files that can be inspected, patched, validated, and reviewed through GitHub.
- **Low-spec first:** the game should be designed around 2D backgrounds, small animated sprites, baked lighting, and minimal runtime effects.
- **Data-driven content:** actors, items, quests, areas, factions, encounters, and dialogue should be extendable through files.
- **Original art identity:** pseudo-isometric, detailed, painterly/pixel-like low fantasy, without copying assets or exact proprietary styles.
- **Safe asset workflow:** generated/imported assets must be tracked with metadata and source notes.

## Initial technical stack

- **Engine:** Godot 4.x, 2D, Compatibility renderer
- **Code:** GDScript
- **Scenes:** text `.tscn`
- **Data:** JSON
- **Dialogue:** Ink later; JSON stubs first
- **Maps:** large 2D background plates + walkmasks/occlusion/hotspot metadata
- **Validation:** Python scripts

## Repository layout

```text
game/       Godot scenes and scripts
data/       JSON game data and schemas
areas/      Area definitions and art metadata
dialogue/   Dialogue files and stubs
assets/     Sprites, portraits, icons, UI, VFX metadata
tools/      Validation and asset pipeline scripts
docs/       Design docs, art bible, content pipeline, roadmap
tests/      Validation fixtures and sample saves
```

## First milestone

Vertical Slice 0.1: **Wolfpine Road**

- one playable area
- one NPC
- one companion stub
- one quest
- one item
- one enemy
- one dialogue stub
- one combat encounter stub
- project validation script

## Validate repository data

From the repository root:

```bash
python tools/validate_project.py
```

The validator checks JSON parsing, duplicate IDs, and referenced files where practical.

## Current status

Project skeleton initialized. No playable build yet.
