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
- testable scenario-driven content paths

## Current technical state

The repo currently contains:

- Godot project config
- main scene that boots into a main menu
- main menu shell
- New Game flow into a simple character creator
- first-pass character creator UI: name, background/origin, class/archetype
- data-driven character creation rules in `data/character_creation/character_creation.json`
- character profile builder with tags, attributes, skills, and compatibility warnings
- player profile/tag/attribute storage in `GameState`
- player-tag and attribute dialogue conditions for NPC reactions and passive checks
- Renna caravan-guard reaction branch gated by `background.caravan_guard`
- Start Journey flow into the Wolfpine Road area prototype
- JSON data loader
- game-state stub with flags, quest stages, party IDs, faction reputation, player profile, tags, attributes, and skills
- quest-system stub
- `AreaController` scene/script prototype and active runtime area controller
- reusable dialogue condition evaluator
- starter area: `wolfpine_road`
- transition destination stub: `wolfpine_village`
- Wolfpine Village art brief and layout constraints for BG2/Pillars-like village generation
- Wolfpine Village starter asset kit README, metadata manifest, generation specs, prompt exporter, and validator
- starter NPC: `captain_renna`
- starter companion: `brannoc`
- starter enemy: `border_bandit`
- starter item: `border_iron_sword`
- starter quest: `missing_caravan`
- validation script: `tools/validate_project.py`
- character creation validation script: `tools/validate_character_creation.py`
- asset-kit validation script: `tools/validate_asset_kits.py`
- asset prompt exporter: `tools/export_asset_prompts.py`
- debug/scenario runner: `tools/run_scenario_test.gd`
- local debug bundle scripts
- GitHub validation workflow, including asset-kit manifest validation

## Current testable build target

Opening the project in Godot and pressing Play should show the main menu.

Expected boot behavior:

- Main menu appears.
- `New Game` opens the character creator.
- Character creator allows name/background/class selection through the old origin/archetype scenario controls.
- `Start Journey` builds a tagged player profile and loads the Wolfpine Road prototype.

Expected character creation behavior:

- Character creation data is loaded from `data/character_creation/character_creation.json`.
- Background and class choices contribute tags, attributes, and skills through `CharacterProfileBuilder`.
- The current UI defaults ancestry to `Border Human` and trait to `Steady Under Fire` until ancestry/trait UI is added.
- Old scenario fields `origin` and `archetype` remain mapped to `background` and `class` for compatibility.
- Invalid or incoherent combinations are represented through tag requirements/blocks in data, with full UI enforcement planned next.

Expected Wolfpine Road behavior:

- A dark placeholder background appears.
- The Wolfpine Road title/debug label appears.
- A visible `◆ party` marker appears.
- Clicking the ground moves the party marker directly toward the clicked point.
- Hotspot buttons appear for the old shrine and north road.
- Actor buttons appear for `captain_renna` and `border_bandit`.
- Clicking the old shrine updates debug text, sets a flag, and advances `missing_caravan` to `found_wreck`.
- Clicking the north road transitions to `wolfpine_village`.
- Clicking `captain_renna` opens a JSON-driven dialogue panel.
- Dialogue choices can move between nodes.
- Dialogue effects can start quests, set quest stages, and set flags.
- Dialogue choices can be gated by reusable flag/quest-stage/skill/player-tag/attribute conditions.
- A Caravan Guard player can access Renna's caravan-road reaction branch.

Expected Wolfpine Village planning state:

- `areas/wolfpine_village/ART_BRIEF.md` defines the first village's visual target, composition, architecture kit, prompt, and rejection checklist.
- `areas/wolfpine_village/layout_constraints.json` defines walkable zones, required paths, buildings, doors, stairs, hotspot access, NPC zones, and forbidden art mistakes.
- `assets/kits/wolfpine_village/README.md` defines the canonical kit folder policy and promotion rule.
- `assets/kits/wolfpine_village/GENERATION_SPECS.md` defines prompt and acceptance specs for the first 15 reusable assets.
- `data/asset_kits/wolfpine_village_starter.json` is the machine-readable starter manifest for those assets.
- `tools/export_asset_prompts.py` can export per-asset prompt cards from the manifest.
- `tools/validate_asset_kits.py` validates asset-kit manifests and is wired into CI.
- Village exterior art should be closer to classic BG2/Pillars-style settlement plates than horror-dark wilderness art.
- Final village art should be generated from the constraints and kit, not used as the source of truth for paths and architecture.

## Automated scenario coverage

Scenario files live under:

```text
tests/scenarios/
```

Important current scenarios:

```text
tests/scenarios/main_menu_new_game.json
tests/scenarios/character_tags_renna_caravan_guard.json
tests/scenarios/wolfpine_missing_caravan.json
tests/scenarios/wolfpine_shrine_before_renna.json
tests/scenarios/wolfpine_report_shrine_to_renna.json
tests/scenarios/wolfpine_road_to_village.json
```

These are intended to test:

- main menu to character creator to new game
- tagged player profile creation from background/class choices
- player-tag based Renna NPC reaction
- Renna quest acceptance
- shrine inspection quest update
- shrine-before-Renna quest regression protection
- flag-gated Renna dialogue
- Wolfpine Road to Wolfpine Village transition

## Validation

Run from repo root:

```bash
python tools/validate_project.py
python tools/validate_character_creation.py
python tools/validate_asset_kits.py
```

The validators currently check:

- JSON syntax
- duplicate IDs
- common referenced files
- dialogue next-node references
- dialogue conditions, including skill, attribute, player-tag, and party-member checks
- quest and quest-stage references
- area actor placements
- scenario step references
- main-menu scenario step shapes
- character creation option IDs, tags, modifiers, and compatibility references
- asset-kit manifest structure and accepted asset file references

## Debug bundle

Run from repo root on Windows:

```bat
tools\collect_debug_bundle.bat
```

Expected output:

```text
debug\NG_debug_latest.zip
```

Upload that zip for AI-assisted bug analysis.

## Current priority

Bring the testable build to a clean local pass:

1. Pull latest repo state.
2. Run `tools\collect_debug_bundle.bat`.
3. Inspect `validation.log` and `scenario.log`.
4. Fix any GDScript runtime errors found in the menu/new-game/area/dialogue paths.
5. Expand the character creator UI to expose ancestry and trait selection, then enforce compatibility blocks in the UI.
6. Continue toward save/load hardening and broader passive skill/tag-check content after the boot path is stable.
7. Use `areas/wolfpine_village/ART_BRIEF.md`, `layout_constraints.json`, and the Wolfpine Village asset kit before generating final Wolfpine Village art.
8. Generate prompt cards with `python tools/export_asset_prompts.py data/asset_kits/wolfpine_village_starter.json` before producing the first canonical asset candidates.

## Working rule

If a future AI chat loses context, read this file first, then:

1. `docs/ROADMAP.md`
2. `docs/WORKFLOW.md`
3. `docs/BUGFIXING.md`
4. `docs/ASSET_POLICY.md`
5. `docs/GAME_DESIGN.md`
6. `docs/ART_BIBLE.md`
7. `docs/CHARACTER_CREATION.md`
