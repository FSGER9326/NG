# Character Creation and NPC Reaction System

## Goal

Character creation should produce believable low-fantasy protagonists whose ancestry, background, class, and traits fit together thematically. The system should also expose durable tags for passive skill checks, dialogue gates, NPC reactions, faction prejudice, companion banter, and quest alternate paths.

The canonical machine-readable data lives in:

```text
data/character_creation/character_creation.json
```

Starter portrait metadata lives in:

```text
data/character_creation/portraits.json
```

## Creator pillars

The character creator is built from four layers:

1. **Ancestry** — inherited body, culture, and social visibility.
2. **Background** — lived history before the game begins.
3. **Class** — current adventuring discipline and combat/social role.
4. **Trait** — a defining personal quality, scar, habit, talent, or limitation.

Each layer contributes:

- `tags`
- optional `attributes` modifiers
- optional `skills` modifiers
- optional `requires_any_tags`
- optional `blocked_by_tags`

## Current profile fields

The built player profile currently carries:

```text
name
ancestry
ancestry_id
background
background_id
class
class_id
trait
trait_id
origin
archetype
portrait_id
portrait
tags
attributes
skills
compatibility_warnings
```

`origin` and `archetype` are legacy aliases for older content/scenarios. New content should prefer `background`, `background_id`, `class`, and `class_id` where possible.

## Portrait metadata

Portrait support is currently text-first. The builder assigns a starter `portrait_id` and display `portrait` name from the selected background. This gives save/load and future UI a durable field before final portrait art exists.

Current starter mapping:

```text
Border Drifter -> portrait_weathered_drifter_01
Failed Squire -> portrait_disgraced_squire_01
Village Outcast -> portrait_village_outcast_01
Caravan Guard -> portrait_caravan_guard_01
Other backgrounds -> portrait_weathered_drifter_01 fallback
```

This is not yet a full manual portrait-selection UI. The next UI step is to expose portrait choices explicitly and let the player override the background-derived default.

## Tags

Tags are string IDs, grouped by prefix. They are intentionally readable and data-friendly.

Examples:

```text
ancestry.elf
age.young
appearance.fair
frame.slender
background.veteran
combat.veteran
education.formal
class.mage
magic.arcane
social.noble
reputation.dangerous
trait.scholar
```

Tags should be stable once used by content. Dialogue and quests should check tags rather than checking a displayed class or background name directly.

## Thematic compatibility

Compatibility is enforced through tag requirements and blocks.

Examples:

- A **War Veteran** should not casually take **Scholarly** unless future content adds a special exception. The current data blocks `trait_scholarly` from `background.veteran` and `combat.veteran`.
- A **Fair Young Elf** should not take **Brawny** because the ancestry contributes `age.young`, `appearance.fair`, and `frame.slender`, while `trait_brawny` blocks those tags.
- A **Mage Apprentice** should not pair with heavy-labor body fantasy by default because `class_mage_apprentice` contributes `combat.fragile` and blocks `labor.heavy` and `combat.veteran`.
- A **Scarred Veteran** requires some martial or veteran credibility and blocks `age.young` and `social.sheltered`.
- **Delicate Bearing** requires refined, fair, slender, noble, or sheltered tags and blocks heavy labor, brawny frames, and veteran combat tags.

This keeps the creator from producing incoherent combinations while still allowing unusual builds through future hand-authored exceptions.

## Compatibility explanation behavior

The compatibility engine now checks each selected layer against the tags that came before it. This matters because a trait should not satisfy its own requirement simply by adding its own tags.

Example:

```text
Fair Young Elf + Cloister Novice + Mage Apprentice + Brawny
```

The creator should not merely say that `Brawny` conflicts with `frame.slender`. It should explain the conflict in readable terms such as:

```text
Brawny conflicts with elf ancestry, young character, slender frame, mage training, fragile arcane training, sheltered upbringing.
```

The engine keeps a small tag-label table in `CharacterProfileBuilder` so common tags are shown as readable phrases. Unknown tags fall back to a cleaned label, replacing `.` and `_` with spaces.

Rules for compatibility text:

- Prefer readable world-facing reasons over raw tag IDs.
- Keep reasons short enough to fit in the creator panel.
- Explain what blocked the option, not only that it is blocked.
- Do not hard-code one-off class/background pair logic in the UI.
- Add new tag labels to `CharacterProfileBuilder.TAG_LABELS` when new tags become player-facing.

## Attributes

Current starter attributes:

```text
might
finesse
resolve
wits
presence
occult
```

Attributes are broad role-playing signals. They should not replace skills; they should support passive checks, combat formulas, and reaction tone.

## Skills

Current starter skills:

```text
perception
survival
resolve
lore
stealth
athletics
medicine
streetwise
arcana
command
```

Dialogue and interaction checks should prefer skills where possible because they are easier to reason about and tune.

## NPC reactions

NPCs should react to tags in layered ways:

### Respect reactions

Soldiers, guards, caravan hands, and hard-bitten villagers may respect:

```text
combat.veteran
training.martial
background.caravan_guard
class.warden
reputation.reliable
```

Example use:

```json
{
  "type": "player_tag",
  "tag": "combat.veteran",
  "value": true
}
```

### Suspicion reactions

Guards, priests, merchants, and frightened villagers may distrust:

```text
magic.arcane
occult.marked
social.underworld
reputation.untrustworthy
reputation.dangerous
```

### Kinship reactions

Commoners, laborers, outcasts, and road folk may open up to:

```text
social.common
hardship.poverty
background.outcast
survival.road
region.border
```

### Class prejudice

Low-fantasy NPCs should not treat all classes neutrally. A starving village might value a surgeon, distrust a mage, and measure a hedge knight against old grievances.

Examples:

- `class.surgeon` can unlock medical triage, corpse-reading, and plague dialogue.
- `class.mage` can unlock occult reads but increase suspicion.
- `class.hedge_knight` can unlock formal challenge and oath dialogue.
- `class.speaker` can unlock manipulation or de-escalation.
- `class.scout` can unlock tracking and ambush detection.

## Dialogue condition patterns

### Passive skill check

```json
{
  "type": "skill_check",
  "skill_id": "perception",
  "difficulty": 2
}
```

### Player tag check

```json
{
  "type": "player_tag",
  "tag": "background.caravan_guard",
  "value": true
}
```

### Any of several reactions

```json
{
  "type": "any",
  "conditions": [
    {"type": "player_tag", "tag": "combat.veteran", "value": true},
    {"type": "player_tag", "tag": "background.caravan_guard", "value": true},
    {"type": "skill_check", "skill_id": "command", "difficulty": 2}
  ]
}
```

### Attribute check

```json
{
  "type": "attribute_check",
  "attribute_id": "presence",
  "difficulty": 3
}
```

## Reaction writing guidelines

NPC reaction text should be specific but not overwhelming. Prefer one or two short lines that imply recognition.

Good examples:

- `combat.veteran`: “Renna notices how you stand out of the rain without turning your back to the road.”
- `magic.arcane`: “Her hand tightens near the iron charm at her belt when she notices the witchlight in your eyes.”
- `social.noble`: “She gives your cloak-pin a longer look than your face.”
- `background.caravan_guard`: “A guard who has walked beside wagons knows where drivers lie and where ambushers wait.”

Avoid reactions that reduce the whole character to one label. A tag should color the moment, not replace the scene.

## Implementation notes

The first implementation should stay text-first:

- Keep all creator content in JSON.
- Keep compatibility rules in JSON through tags.
- Keep runtime checks in small GDScript helpers.
- Add validation when new condition types are added.
- Keep portrait IDs text-first until final portrait assets are ready.
- Do not block character creation on portrait art availability.
