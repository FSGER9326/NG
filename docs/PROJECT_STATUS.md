# NG Project Status

This file is the main handoff point for future chats and AI agents.

## Current project identity

- Repo: `FSGER9326/NG`
- Working title: **NG / New Game**
- Narrative working title: **No Gods in the Pines**
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
- a rich but modular campaign story built from local crimes, faction pressure, and old-law mythic consequences

## Story target

The campaign premise now lives in `docs/STORY_BIBLE.md`.

Core story direction:

- A small party of dangerous nobodies enters the starving Wolfpine March.
- The first practical problem is a missing supply caravan on Wolfpine Road.
- The larger mystery is the failing **Road Peace**, an old compact that keeps roads, shrines, ledgers, ranger paths, saint relics, and corpse law functioning.
- The tone should be mundane and epic at once: hunger, tolls, crime, village panic, paladin oaths, ranger rites, saint lies, old debts, and violence with consequences.
- Paladins, rangers, criminals, priests, soldiers, and villagers should be grounded people with useful virtues, private sins, and believable limits rather than simple archetypes.

## Current technical state

The repo currently contains:

- Godot project config
- main scene that boots into a main menu
- main menu shell
- New Game flow into a character creator
- character creator UI: name, ancestry, background/origin, class/archetype, trait
- data-driven character creation rules in `data/character_creation/character_creation.json`
- text-first portrait metadata in `data/character_creation/portraits.json`
- character profile builder with tags, attributes, skills, portrait defaults, and compatibility warnings
- creator compatibility UI that shows readable theme conflicts and blocks incoherent builds from starting
- reusable NPC reaction authoring rules in `data/reactions/npc_reaction_rules.json`
- player profile/tag/attribute storage in `GameState`
- player-tag and attribute dialogue conditions for NPC reactions and passive checks
- Renna caravan-guard reaction branch gated by `background.caravan_guard`
- Renna arcane-suspicion reaction branch gated by `magic.arcane`
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
- reusable quest seed bank: `docs/QUEST_SEEDS.md`
- starter NPC: `captain_renna`
- starter companion: `brannoc`
- starter enemy: `border_bandit`
- starter item: `border_iron_sword`
- starter quest: `missing_caravan`
- narrative story bible: `docs/STORY_BIBLE.md`
- story implementation backlog: `docs/STORY_IMPLEMENTATION_BACKLOG.md`
- validation script: `tools/validate_project.py`
- character creation validation script: `tools/validate_character_creation.py`
- portrait metadata validation script: `tools/validate_portraits.py`
- quest seed bank validation script: `tools/validate_quest_seeds.py`
- GDScript helper contract validation script: `tools/validate_gdscript_helpers.py`
- asset-kit validation script: `tools/validate_asset_kits.py`
- asset prompt exporter: `tools/export_asset_prompts.py`
- debug/scenario runner: `tools/run_scenario_test.gd`
- local debug bundle scripts
- GitHub validation workflow, including character creation, portrait metadata, quest seed bank, GDScript helper contracts, and asset-kit manifest validation

## Current testable build target

Opening the project in Godot and pressing Play should show the main menu.

Expected boot behavior:

- Main menu appears.
- `New Game` opens the character creator.
- Character creator allows name/ancestry/background/class/trait selection.
- `Start Journey` builds a tagged player profile and loads the Wolfpine Road prototype when the selected build is thematically coherent.
- Incoherent builds remain on the character creator screen with visible compatibility warnings.

Expected character creation behavior:

- Character creation data is loaded from `data/character_creation/character_creation.json`.
- Ancestry, background, class, and trait choices contribute tags, attributes, and skills through `CharacterProfileBuilder`.
- Portrait metadata is loaded from `data/character_creation/portraits.json` for text-first portrait IDs, names, summaries, and tags.
- `tools/validate_character_creation.py` cross-checks `CharacterProfileBuilder` default portrait IDs and any explicit background `portrait_id` values against `portraits.json`.
- `PortraitCatalog` is available for the upcoming text-first portrait selector UI and is protected by `tools/validate_gdscript_helpers.py`.
- Old scenario fields `origin` and `archetype` remain mapped to `background` and `class` for compatibility.
- Invalid or incoherent combinations are represented through tag requirements/blocks in data.
- The creator previews compatibility warnings and blocks Start Journey when the built profile has compatibility warnings.
- Unavailable traits are explained with readable theme labels rather than only raw trait names.
- Example blocked build: `Fair Young Elf` + `Mage Apprentice` + `Brawny`.
- Example recovery path: change `Brawny` to `Arcane Sensitive`, then Start Journey succeeds and adds `magic.arcane` / `trait.arcane_sensitive` tags.
- Manual portrait selection is not implemented yet; issue #13 tracks exposing the existing text-first portrait metadata in the creator UI without requiring final portrait art.

Expected Wolfpine Road behavior:

- A dark placeholder background appears.
- The Wolfpine Road title/debug label appears.
- A visible `◆ party` marker appears.
- Clicking the ground moves the party marker directly toward the clicked point.
- Hotspot buttons appear for the old shrine and north road.
- Actor buttons appear for `captain_renna`, `brannoc`, and `border_bandit`.
- Clicking the old shrine updates debug text, sets `wolfpine_old_shrine_inspected`, sets dead-mule/toll-disc/Road-Peace flags, and advances `missing_caravan` to `found_wreck`.
- Clicking the north road transitions to `wolfpine_village`.
- Clicking `captain_renna` opens a JSON-driven dialogue panel.
- Clicking `brannoc` opens companion dialogue, including a toll-disc reaction branch if the old shrine clue was found.
- Dialogue choices can move between nodes.
- Dialogue effects can start quests, set quest stages, set flags, and add party members.
- Dialogue choices can be gated by reusable flag/quest-stage/skill/player-tag/attribute conditions.
- A Caravan Guard player can access Renna's caravan-road reaction branch.
- A magic-tagged player can access Renna's arcane-suspicion reaction branch.
- If the toll-disc clue was found, Renna exposes a gated branch: `Someone pressed a toll disc into a dead mule's eye.` This sets `missing_caravan` to `found_shrine_clue` and `wolfpine_renna_knows_toll_disc`.
- If the toll-disc clue was found, Brannoc exposes a gated branch: `You saw the mule at the shrine. The toll disc in its eye.` This sets `brannoc_guilt_hint_1` as the first seed of his caravan-survivor guilt arc.

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

Expected story planning state:

- `docs/STORY_BIBLE.md` defines the campaign premise, tone pillars, expandable story layers, Road Peace mystery, major factions, antagonists, companion concepts, and first playable module story target.
- `docs/STORY_IMPLEMENTATION_BACKLOG.md` converts the story bible into small first-playable content tasks, flags, quest stages, scenario ideas, and writing constraints.
- `docs/QUEST_SEEDS.md` provides reusable text-first side quest seeds; convert them into runtime JSON only after choosing one small implementation target and adding scenario coverage.
- Future quest work should start from ordinary pressure first, then connect to faction pressure and the old-law layer.
- Future companion work should prefer concrete moral flags and story consequences over a single generic approval meter.
- Future Wolfpine Road and Wolfpine Village dialogue should support the missing-caravan mystery, Renna's hard choices, Brannoc's guilt, ranger/paladin realism, local hunger, and early Road Peace failure signs.

## Automated scenario coverage

Scenario files live under:

```text
tests/scenarios/
```

Important current scenarios:

```text
tests/scenarios/main_menu_new_game.json
tests/scenarios/character_creator_ancestry_trait_tags.json
tests/scenarios/character_creator_incompatible_combo.json
tests/scenarios/character_creator_recover_from_incompatible_combo.json
tests/scenarios/character_tags_renna_caravan_guard.json
tests/scenarios/character_tags_renna_arcane_suspicion.json
tests/scenarios/wolfpine_missing_caravan.json
tests/scenarios/wolfpine_shrine_before_renna.json
tests/scenarios/wolfpine_report_shrine_to_renna.json
tests/scenarios/wolfpine_shrine_toll_disc.json
tests/scenarios/brannoc_toll_disc_reaction.json
tests/scenarios/wolfpine_road_to_village.json
```

These are intended to test:

- main menu to character creator to new game
- ancestry/background/class/trait tagged player profile creation
- creator compatibility blocking for incoherent builds
- recovery from an incoherent build by changing to a compatible trait
- player-tag based Renna caravan-guard NPC reaction
- player-tag based Renna arcane-suspicion NPC reaction
- Renna quest acceptance
- shrine inspection quest update
- shrine-before-Renna quest regression protection
- flag-gated Renna dialogue
- toll-disc Road Peace clue flags and Renna's toll-disc branch
- Brannoc's toll-disc reaction and first guilt-arc hint flag
- Wolfpine Road to Wolfpine Village transition

## Validation

Run from repo root:

```bash
python tools/validate_project.py
python tools/validate_character_creation.py
python tools/validate_portraits.py
python tools/validate_quest_seeds.py
python tools/validate_gdscript_helpers.py
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
- character creation option IDs, tags, modifiers, compatibility references, default portrait IDs, and background portrait references
- text-first portrait metadata IDs, names, summaries, and tags
- quest seed bank structure, seed IDs, required fields, flags, stages, and implementation notes
- GDScript helper contracts such as `PortraitCatalog`
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
5. Implement issue #13 to expose text-first portrait selection in the character creator UI without requiring final portrait art.
6. Continue toward save/load hardening and broader passive skill/tag-check content after the boot path is stable.
7. Expand Wolfpine Road and Wolfpine Village content using `docs/STORY_BIBLE.md`, especially the missing caravan, Road Peace, Renna, Brannoc, hunger pressure, and early old-shrine clues.
8. Use `docs/QUEST_SEEDS.md` only as a seed bank until one entry is selected for JSON conversion with matching scenario coverage.
9. Use `areas/wolfpine_village/ART_BRIEF.md`, `layout_constraints.json`, and the Wolfpine Village asset kit before generating final Wolfpine Village art.
10. Generate prompt cards with `python tools/export_asset_prompts.py data/asset_kits/wolfpine_village_starter.json` before producing the first canonical asset candidates.

## Working rule

If a future AI chat loses context, read this file first, then:

1. `docs/ROADMAP.md`
2. `docs/WORKFLOW.md`
3. `docs/BUGFIXING.md`
4. `docs/ASSET_POLICY.md`
5. `docs/GAME_DESIGN.md`
6. `docs/STORY_BIBLE.md`
7. `docs/ART_BIBLE.md`
8. `docs/CHARACTER_CREATION.md`
