# Core Mechanics

This page explains the current and planned mechanics of NG.

## Current implemented mechanics

### Area loading

The game currently loads an area from JSON data.

Current area:

```text
wolfpine_road
```

The area data points to:

- hotspots
- actor placements
- entry points
- description
- presentation data later

### Party movement

The party currently appears as a placeholder marker:

```text
◆ party
```

Clicking the ground moves the marker directly toward the clicked position.

Current limitations:

- no pathfinding yet
- no walkmask collision yet
- no party formation yet
- no sprite animation yet

### Hotspots

Hotspots are clickable map interactions.

Current hotspot types:

| Type | Meaning |
|---|---|
| `inspect` | Shows descriptive text and can trigger effects. |
| `exit` | Shows target area debug text. Later this will move the party between areas. |

Hotspots can have effects.

Example effect types:

```text
set_quest_stage
set_flag
```

### Dialogue

Dialogue is currently stored in JSON.

Dialogue nodes contain:

- text
- choices
- next-node links
- optional effects

Current dialogue effects include:

| Effect | Meaning |
|---|---|
| `start_quest` | Starts a quest and sets its first active stage. |
| `set_quest_stage` | Updates a quest to a new stage. |
| `set_flag` | Stores a world/player flag. |

### Quest state

Quest state is stored in `GameState` and displayed in the quest tracker.

Example:

```text
Quests:
- missing_caravan: accepted
```

Quest stages currently visible in the first quest:

| Stage | Meaning |
|---|---|
| `not_started` | The player has not accepted or discovered the quest. |
| `accepted` | Captain Renna asked the party to investigate. |
| `found_wreck` | The old shrine/wagon-rut clue has been found. |

### Flags

Flags remember facts about the world.

Current example:

```text
wolfpine_old_shrine_inspected
```

This is set when the player inspects the Old Road Shrine.

## Planned mechanics

### Skill checks

Planned dialogue and exploration checks may use skills such as:

- survival
- resolve
- lore
- intimidation
- deception
- perception
- athletics

### Faction reputation

The game is planned to track faction relationships.

Possible early factions:

- Wolfpine Guard
- Road Bandits
- Old Faith
- Smugglers
- Border Lords

### Companions

Companions are planned to have:

- unique dialogue
- approval/disapproval
- personal quests
- interjections
- possible conflicts with factions or other companions

### Combat

Combat is planned as turn-based AP combat first.

Planned systems:

- party and enemy placement
- action points
- melee attacks
- ranged attacks
- abilities
- status effects
- victory/defeat results

Real-time-with-pause is not a first milestone.

### Journal

The current quest tracker is temporary. A future journal should show:

- active quests
- completed quests
- known clues
- faction notes
- companion notes
