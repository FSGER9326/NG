# Getting Started

This page explains what the game currently is, what the prototype can do, and how to understand what is on screen.

## Current prototype

The current build starts in **Wolfpine Road**.

This is not yet a finished area. It is a playable test slice for:

- loading an area
- moving the party marker
- clicking NPCs
- opening dialogue
- making dialogue choices
- starting a quest
- inspecting a hotspot
- updating quest state

## What you see on screen

### Party marker

The party is currently represented by:

```text
◆ party
```

This is a placeholder. Later it should become a small party sprite or party leader marker.

### NPC markers

NPCs and enemies currently appear as clickable labels such as:

```text
@ captain_renna
@ border_bandit
```

These are placeholders. Later they should become actual sprites with names shown only on hover, selection, or debug mode.

### Hotspots

Hotspots are clickable interactions on the map.

Current examples:

- **Old Road Shrine** — inspect hotspot
- **North Road** — exit stub

Later, hotspots should usually be invisible until highlighted by cursor/inspection mode.

### Dialogue panel

Dialogue appears in a framed panel with:

- speaker name
- dialogue text
- clickable choices

The current dialogue format is simple JSON. Later it may move to Ink or a richer custom dialogue format.

### Quest tracker

The quest tracker shows current quest state.

Example:

```text
Quests:
- missing_caravan: accepted
```

This is an early debug-style tracker, not the final journal UI.

## Current playable test path

1. Click `@ captain_renna`.
2. Choose **I am looking for work.**
3. The quest tracker should show:

```text
missing_caravan: accepted
```

4. Click **Old Road Shrine**.
5. The quest tracker should show:

```text
missing_caravan: found_wreck
```

## How to think about the prototype

The current build is a skeleton with early presentation. Its job is to prove that the RPG can remember choices and update the world. The final game should hide most of the debug labels behind proper art, sprites, UI, and area design.
