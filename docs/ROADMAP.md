# NG Roadmap

## Current goal

Build a low-spec, pseudo-isometric, party-based CRPG that is easy for AI tools to inspect, edit, validate, and extend.

## Milestone 0.1 — Repository skeleton

- [x] README
- [x] Godot project config
- [x] Main scene
- [x] Bootstrap data loader
- [x] Starter JSON content
- [x] Validation script
- [x] Art bible
- [x] Game design document
- [x] Story bible

## Milestone 0.2 — Area prototype

- [x] Area scene controller
- [x] Background loading placeholder
- [x] Actor placement from JSON
- [x] Click-to-move prototype
- [x] Hotspot inspection
- [x] Real area transition support

## Milestone 0.3 — Dialogue and quest prototype

- [x] Dialogue UI prototype
- [x] Dialogue node navigation
- [x] Quest start effect stored in game state
- [x] Quest stage update stored in game state
- [x] Basic flag-setting effect
- [x] Reusable dialogue flag and quest-stage checks
- [x] Dialogue condition validation
- [x] Skill check format
- [x] Player-tag and attribute-check dialogue gates
- [x] NPC reaction example driven by character creation tags

## Milestone 0.4 — Frontend shell and character creation

- [x] Main menu shell
- [x] New Game starts character creator
- [x] Character creator first pass: name, origin, archetype
- [x] Data-driven character creation rules for ancestry/background/class/trait
- [x] Tagged player profile builder
- [x] Character tags, attributes, and skills stored in game state
- [x] Start Journey launches current area prototype with player profile applied
- [x] Save/Load menu placeholders
- [x] Save game format
- [x] Load game flow
- [x] Expose ancestry selection in the creator UI
- [x] Expose trait selection in the creator UI
- [x] Enforce compatibility blocks and requirements in the creator UI
- [x] Add option filtering for incompatible traits in the creator UI
- [x] Add richer compatibility explanation text in the creator UI
- [ ] Character portrait selection — tracked in issue #13; metadata and CI validation are ready

## Milestone 0.5 — Combat prototype

- [ ] Combat scene
- [ ] Party and enemy placement
- [ ] Turn queue
- [ ] AP spending
- [ ] Melee attack
- [ ] Victory/defeat result

## Milestone 0.6 — First playable module

- [ ] Wolfpine Road playable
- [x] Wolfpine Village stub
- [x] Wolfpine Village art brief and layout constraints
- [ ] Wolfpine Village final background plate
- [ ] Collapsed Crypt stub
- [ ] One companion recruitable
- [ ] One quest completable
- [x] Missing Caravan evidence trail expanded with ledger, smuggler-mark, carter-body, Brannoc reaction, and Renna report paths
- [ ] Missing Caravan expanded from evidence trail into a completable story-bible Act I structure
- [x] Old Shrine expanded with early Road Peace clues, corpse-law evidence seeds, and evidence-web reporting
- [ ] Wolfpine Village populated with hunger, law, church, smuggler, and child-informant pressure
- [x] Brannoc upgraded with concrete companion reaction flags for the Wolfpine evidence trail
- [ ] Brannoc upgraded from starter companion data to a recruitable companion arc seed

## Milestone 0.7 — Narrative systems and content depth

- [ ] Add faction reputation IDs for Roadwardens, Grey Rangers, Ash Church, Blackfen Free Company, Sainted Lance, Baronial Houses, Rat Crown, and Borrowed
- [ ] Add story flags for mercy, execution, corpse-law, food allocation, relic custody, and public-truth decisions
- [x] Add companion reaction flags for Brannoc, then reuse the pattern for ranger and paladin companions
- [ ] Add at least one ranger NPC or companion seed grounded in realistic path law rather than generic nature mysticism
- [ ] Add at least one paladin NPC or companion seed grounded in legal witness protection, mercy, and oath pressure
- [ ] Add quest content tags from `docs/STORY_BIBLE.md` to future quest/dialogue data where useful
- [ ] Add validation for unknown faction IDs once faction data files exist
- [ ] Add scenario tests for at least one mercy consequence, one execution consequence, and one faction reputation consequence

## Current first playable test paths

### Boot and new-game path

1. Launch the game in Godot.
2. Main menu should appear.
3. Choose `New Game`.
4. Character creator should appear.
5. Enter a name, choose ancestry/background/class/trait, and choose `Start Journey`.
6. Wolfpine Road prototype should load with a tagged player profile.

### Character-tag NPC reaction path

1. Start a new game.
2. Create a Caravan Guard / Scout.
3. Confirm the player has `background.caravan_guard`.
4. Click `@ captain_renna`.
5. The dialogue choice `I have walked caravan roads. Tell me where yours broke pattern.` should be visible.
6. Choosing it should open Renna's caravan-road reaction branch.

### Character compatibility path

1. Start a new game.
2. Choose Fair Young Elf / Cloister Novice / Mage Apprentice.
3. The creator should mark Brawny unavailable in the trait list.
4. The creator warning text should explain that Brawny conflicts with readable themes such as elf ancestry, slender frame, mage training, fragile arcane training, and sheltered upbringing.
5. Choose a coherent trait such as Arcane Sensitive to proceed.

### Character portrait metadata path

1. Run `python tools/validate_portraits.py`.
2. Confirm `data/character_creation/portraits.json` has unique text-first portrait IDs, names, summaries, and tags.
3. Implement issue #13 to expose these metadata choices in the creator UI without requiring final portrait art.

### Basic quest path

1. Start a new game.
2. Click `@ captain_renna`.
3. Choose the work dialogue option.
4. Quest tracker should show `missing_caravan: accepted`.
5. Click `Old Road Shrine`.
6. Quest tracker should show `missing_caravan: found_wreck`.

### Flag-gated dialogue path

1. Click `Old Road Shrine`.
2. Click `@ captain_renna`.
3. The dialogue choice `I found fresh wagon ruts by the old shrine.` should be visible.
4. Choose it.
5. Quest tracker should show `missing_caravan: reported_clue`.

### Wolfpine evidence report path

1. Start a new game and load Wolfpine Road.
2. Inspect `shrine_ledger_niche`, `cut_bark_smuggler_mark`, `wounded_dog_tracks`, and `dog_vigil_hollow`.
3. Confirm Missing Caravan can reach `found_erased_name`, `found_smuggler_mark`, and `found_carter_body`.
4. Click `@ brannoc` and confirm he has clue reactions for the dead carter, erased name, and smuggler mark.
5. Click `@ captain_renna` and report the carter body, erased name, and smuggler mark.
6. Confirm Renna exposes `The evidence does not point to one thief. It points to a handoff.` and can set `missing_caravan: evidence_web_reported`.

### Skill-gated dialogue path

1. Start a new game.
2. Click `@ captain_renna`.
3. The perception-gated dialogue choice `You look like you expected the caravan to vanish.` should be visible with the starter party's perception value.
4. Choosing it should open Renna's pressure-read branch.

### Save/load path

1. Start a new game from the main menu.
2. Create a character profile.
3. Load Wolfpine Road.
4. Accept `missing_caravan` from Captain Renna.
5. Save the game.
6. Load the game.
7. Confirm the profile, current area, and quest stage are restored.

### Area transition path

1. Start a new game.
2. Click `North Road` on Wolfpine Road.
3. Wolfpine Village should load.

## Narrative expansion path for Wolfpine first playable

1. Use `docs/STORY_BIBLE.md` as the source of truth for tone, campaign premise, factions, companion seeds, and the Missing Caravan story direction.
2. Expand ordinary stakes first: food, lamp oil, tolls, dead animals, missing names, local panic, and practical crime.
3. Add faction pressure second: Roadwardens, Ash Church, smugglers, rangers, and village officials should each have partial truths and useful sins.
4. Add old-law clues third: Road Peace, corpse law, saint relics, mile-stones, shrine damage, and impossible toll evidence.
5. Preserve modularity by keeping each clue, dialogue branch, quest stage, and consequence testable through flags and scenario files.

## Art-generation path for Wolfpine Village

1. Use `areas/wolfpine_village/layout_constraints.json` as the source of truth for walkable zones, required paths, doors, stairs, hotspots, and NPC zones.
2. Use `areas/wolfpine_village/ART_BRIEF.md` for the visual target and rejection checklist.
3. Generate or kitbash the village from the layout, not the other way around.
4. Reject final art with hidden doors, stairs to windows, blocked paths, disconnected roads, or horror-dark village lighting.
5. After final art is accepted, create matching background, occlusion, walkmask/collision, hotspot, and actor overlays.

## Next target

Stabilize the menu/new-game/area-transition/save-load flow, then implement issue #13 to expose text-first portrait selection in the character creator UI. For narrative content, the next small slice should move the merged Wolfpine Road evidence web into Wolfpine Village suspect pressure, public-truth consequences, or a small completable Missing Caravan resolution branch. For art, the next target is a Wolfpine Village background plate generated from the checked art brief and layout constraints.

## Always update this file when scope changes.
