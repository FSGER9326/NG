# Glossary

This glossary explains terms used in the NG wiki and current prototype.

## AP

Action Points. Planned combat resource used for movement, attacks, and abilities in turn-based combat.

## Area

A playable map or location. Current example: `wolfpine_road`.

## Area plate

A large painted or generated 2D background image used as the visible map. This is the planned BG2-like presentation layer.

## Actor

A placed character or creature in an area. Actors can be NPCs, companions, enemies, or party members.

## Background plate

Same as area plate: the main image layer of an authored area.

## Captain Renna

A Wolfpine Guard captain and current quest giver for `missing_caravan`.

## Companion

A recruitable party member with personality, stats, dialogue, and future approval/disapproval systems.

## Dialogue node

A single section of dialogue text plus player choices and optional effects.

## Effect

A gameplay action triggered by dialogue or hotspots.

Current effects:

- `start_quest`
- `set_quest_stage`
- `set_flag`

## Flag

A stored fact about the world or player actions.

Example:

```text
wolfpine_old_shrine_inspected
```

## Hotspot

A clickable interaction point in an area, such as a shrine, exit, door, container, or clue.

## Missing Caravan

The first prototype quest. The player can accept it from Captain Renna and find a clue at the Old Road Shrine.

## Old Faith

A planned early religious/cultural faction or influence tied to rural shrines, old stones, groves, and pre-current-rule traditions.

## Old Road Shrine

A roadside shrine in Wolfpine Road. It currently updates the `missing_caravan` quest when inspected.

## Quest stage

A named state within a quest.

Example stages for `missing_caravan`:

- `not_started`
- `accepted`
- `found_wreck`
- `resolved`

## Road Bandits

A current enemy faction placeholder. They represent deserters, hungry villagers, and thieves preying on unsafe roads.

## Walkmask

A future area-data layer defining where the party can and cannot walk.

## Wolfpine

The first planned village hub. It is starving and depends on supply caravans.

## Wolfpine Guard

The village guard faction. Captain Renna belongs to this faction.

## Wolfpine Road

The first playable prototype area. It contains Captain Renna, a road bandit placeholder, the Old Road Shrine, and a North Road exit stub.
