# First-Pass Free Asset Evaluation

This report evaluates the free asset candidates listed in `asset_eval/asset_candidates.json` for NG's first playable.

The goal is not to pick final art immediately. The goal is to decide what is worth downloading locally into `asset_eval/downloads/`, extracting into `asset_eval/extracted/`, and reviewing with `asset_eval/REVIEW_WORKSHEET.md`.

## Evaluation assumptions

- NG targets a low-spec Godot 4 Compatibility renderer path.
- Final art direction is grounded low-fantasy, pseudo-isometric, readable, and not cartoon-bright.
- Raw third-party packs should not be committed until a subset is selected and documented.
- CC0 assets are preferred for early evaluation because they minimize attribution and redistribution overhead.
- Audio placeholders can become final more easily than mismatched visual packs.
- Large frameworks or asset-store plugins should not replace NG's current JSON/GDScript/data-driven systems.

## Summary recommendation

Download and evaluate in this order:

1. `kenney_ui_audio`
2. `kenney_interface_sounds`
3. `kenney_rpg_audio`
4. `kenney_ui_pack_rpg_expansion`
5. `kenney_ui_pack`
6. `kenney_game_icons`
7. `kenney_board_game_icons`
8. `kenney_roguelike_rpg_pack`
9. `itch_vexed_bit_bonanza`
10. Discovery pools only after a specific need is identified.

Do not import full packs into the game yet. Promote only small subsets that support current first-playable flows.

## Candidate evaluations

| Candidate | Decision | Fit | Use now | Final candidate | Notes |
|---|---|---:|---|---|---|
| `kenney_ui_audio` | Download first | 5/5 | UI clicks, hover, confirm, cancel | Yes | Small, CC0, directly improves play feel with low art-direction risk. |
| `kenney_interface_sounds` | Download first | 5/5 | Additional UI sound pool | Yes | Compare against `kenney_ui_audio`; keep only subtle, non-arcade sounds. |
| `kenney_rpg_audio` | Download first | 4/5 | Footsteps, weapon/foley placeholders | Maybe | Strong first-playable utility, especially for road/village feel. Needs taste review. |
| `kenney_ui_pack_rpg_expansion` | Download first | 4/5 | Quest/log/inventory panel placeholders | Maybe | Best visual UI candidate. Use selectively; avoid making NG look like generic bright RPG UI. |
| `kenney_ui_pack` | Download second | 3/5 | Basic panels/buttons/sliders | Placeholder mostly | Useful for speed, but broad/default UI style may clash with final tone. |
| `kenney_game_icons` | Download second | 3/5 | Debug prompts, inspect/exit markers, toolbar icons | Placeholder mostly | Useful but likely too generic for final CRPG icon identity. |
| `kenney_board_game_icons` | Download second | 3/5 | Quest-state, condition, map, abstract icons | Placeholder mostly | May contain readable symbols for scenario/debug UI. Needs subset review. |
| `kenney_roguelike_rpg_pack` | Download after UI/audio | 2/5 | Inventory/debug icons, temporary tokens | No | Very useful volume, but pixel/tile style does not match pseudo-isometric final art. |
| `kenney_impact_sounds` | Defer until combat | 3/5 | Combat/object impact placeholders | Maybe | Good candidate once combat prototype exists; not urgent for current flow. |
| `itch_vexed_bit_bonanza` | Download after Kenney pass | 2/5 | Tiny icons/debug markers | No | CC0 and tiny download, but 1-bit 10x10 style is placeholder-only for NG. |
| `itch_cc0_godot_pool` | Discovery only | variable | Find specific missing needs | variable | Review individual pages only. Do not bulk-download. |
| `godot_asset_library_pool` | Discovery only | variable | Tooling/addons only | No art | Use only for specific editor/debug/import needs. Avoid gameplay frameworks. |

## Best immediate downloads

### 1. UI audio and interface sounds

These are the safest first downloads because they are small, easy to evaluate, low-risk for art direction, and immediately improve perceived quality.

Evaluate for:

- menu open/close
- button hover/click
- dialogue choice confirm
- quest updated
- save/load confirm
- denied/blocked action

Reject sounds that feel:

- arcade-like
- sci-fi
- too loud
- too comedic
- too modern or mobile-game-like

Promote only 5-12 sounds at first.

### 2. RPG audio

Evaluate for:

- dirt/road footsteps
- wood footsteps for village interiors later
- leather/cloth movement
- low-key weapon draw/hit placeholders
- object pickup/inspect

Keep sounds subtle. The first playable needs ambience and interaction feel more than dramatic combat stings.

### 3. RPG UI expansion

Evaluate for:

- dialogue panel frame ideas
- quest journal panel placeholders
- inventory/card panel placeholders
- small sliders/tabs/buttons

Do not commit a full UI skin. Promote only a minimal subset if it improves readability.

## Placeholder-only visual packs

The pixel packs are useful for testing but should not define NG's look:

- `kenney_roguelike_rpg_pack`
- `itch_vexed_bit_bonanza`
- most icon packs until reviewed

Good uses:

- temporary inventory icons
- debug minimap or test-grid tokens
- hidden object hotspot stand-ins
- internal test UI markers

Bad uses:

- final Wolfpine art
- final portraits
- final area backgrounds
- final companion sprites

## Discovery pool policy

### itch.io CC0/Godot pool

Use only when a concrete need exists, for example:

- rain loop
- forest ambience
- specific UI icon missing from Kenney
- small CC0 prop set for internal blockout

Every page must be reviewed individually. Do not trust the pool-level license alone.

### Godot Asset Library pool

Use only for tools/addons with a concrete need, for example:

- import helper
- editor organization helper
- debug overlay helper
- license/asset manifest helper

Avoid:

- full quest frameworks
- dialogue frameworks that replace current JSON dialogue
- save-system frameworks
- visual frameworks that require renderer changes
- GPL/copyleft plugins unless deliberately approved

## Recommended promotion plan

### Phase A — local evaluation only

Download:

```text
kenney_ui_audio
kenney_interface_sounds
kenney_rpg_audio
kenney_ui_pack_rpg_expansion
kenney_ui_pack
```

Fill out `asset_eval/REVIEW_WORKSHEET.md` for each pack.

### Phase B — promote tiny subsets

Create a later PR with only selected files, for example:

```text
assets/vendor/kenney_ui_audio/manifest.json
assets/vendor/kenney_ui_audio/LICENSE.txt
assets/vendor/kenney_ui_audio/ui/click_01.ogg
assets/vendor/kenney_ui_audio/ui/confirm_01.ogg
assets/vendor/kenney_rpg_audio/manifest.json
assets/vendor/kenney_rpg_audio/LICENSE.txt
assets/vendor/kenney_rpg_audio/foley/footstep_dirt_01.ogg
```

### Phase C — integrate into game

Only after promotion:

- add audio import settings if needed
- wire UI click/confirm sounds into menus/dialogue
- add simple `data/audio_cues.json` if a data-driven layer is needed
- scenario/smoke-check that the game still launches without missing resources

## Current decision matrix

| Area | Best candidate | Why |
|---|---|---|
| Menu feel | `kenney_ui_audio` | Small, CC0, immediate value. |
| Dialogue interaction | `kenney_interface_sounds` | More UI variation for choice/confirm/back. |
| Road/village tactile feel | `kenney_rpg_audio` | Footsteps/foley fit first playable better than visual packs. |
| Placeholder quest UI | `kenney_ui_pack_rpg_expansion` | RPG-specific panels and controls. |
| Debug/hotspot icons | `kenney_game_icons` or `kenney_board_game_icons` | Useful for development readability. |
| Inventory placeholders | `kenney_roguelike_rpg_pack` | Large icon/tile volume, but placeholder-only. |
| Final Wolfpine art | none of these | Use custom/generated art guided by layout and art brief. |
| Final portraits | none of these | Keep portrait metadata text-first until art direction is locked. |

## Verdict

The best immediate value is audio plus a small RPG UI subset. The visual packs are useful for prototyping but should remain placeholder-only unless a subset is heavily restyled or used for internal/debug UI.

Do not bulk-promote assets. Download broadly for local evaluation, then promote narrowly.
