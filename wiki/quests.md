# Quests

This page explains current and planned quests.

## Missing Caravan

**Quest ID:** `missing_caravan`  
**Current status:** implemented as first prototype quest loop  
**First giver:** Captain Renna  
**First area:** Wolfpine Road

### Premise

A supply caravan vanished on the road to Wolfpine. The village blames bandits, the guards blame smugglers, and the old shrine watches in silence.

The missing supplies include food, lamp oil, arrow shafts, and medicine — enough to keep Wolfpine alive another month.

### Current implemented flow

1. Speak with Captain Renna.
2. Choose the work dialogue option.
3. Quest stage becomes:

```text
accepted
```

4. Inspect the Old Road Shrine.
5. Quest stage becomes:

```text
found_wreck
```

6. The flag `wolfpine_old_shrine_inspected` is set.

### Current stages

| Stage | Meaning |
|---|---|
| `not_started` | The player has not started the quest. |
| `accepted` | Captain Renna asked the party to search the road. |
| `found_wreck` | The party found evidence near the old shrine. |
| `accused_guards` | Future branch: the party suspects guards are involved. |
| `exposed_smugglers` | Future branch: the party exposes smuggler involvement. |
| `resolved` | Future branch: the quest is resolved. |

### Planned branches

The quest should eventually support several solutions:

#### Bandit solution

Track and defeat or negotiate with road bandits.

Possible outcomes:

- recover some supplies
- kill bandits
- spare hungry villagers-turned-bandits
- gain/lose reputation with Wolfpine Guard

#### Smuggler solution

Find signs that the caravan was redirected or betrayed.

Possible outcomes:

- expose a smuggler route
- cut a deal
- blackmail someone
- anger local powers

#### Guard corruption solution

Discover that some guards may have been involved or allowed the caravan to vanish.

Possible outcomes:

- accuse Wolfpine guards
- protect Captain Renna
- destabilize the village
- gain leverage over local authority

### Design purpose

`missing_caravan` is the first proof-of-concept quest. It should demonstrate:

- dialogue starts quests
- exploration updates quests
- clues set flags
- choices produce branches
- factions react later

## Future quest categories

### Main borderland quests

Large quests tied to Wolfpine, old imperial ruins, and regional factions.

### Companion quests

Personal quests for recruitable companions.

### Faction quests

Quests that improve or damage relationships with factions.

### Wilderness encounters

Small authored events along roads, forests, shrines, and ruins.
