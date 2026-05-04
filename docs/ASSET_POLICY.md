# NG Asset Policy

## Goal

Use free, legal, reusable assets where possible so the project does not depend on generating every icon, UI panel, sound, or placeholder from scratch.

## Preferred asset licenses

Best:

- CC0 / public domain
- MIT / permissive code assets
- Explicitly free for commercial and modification use

Accept only with care:

- CC-BY, if attribution tracking is added
- GPL assets only if we intentionally accept copyleft implications for that asset/code path

Avoid:

- unclear license
- non-commercial only
- no-derivatives
- ripped game assets
- AI outputs that copy an existing game, artist, or franchise identity too closely

## Asset ledger

Every imported or generated asset should eventually have a metadata entry.

Suggested format:

```json
{
  "id": "asset_id",
  "file": "assets/path/file.png",
  "type": "ui_icon",
  "source": "kenney",
  "source_url": "",
  "license": "CC0",
  "modified": true,
  "notes": "Cropped and recolored for NG UI." 
}
```

## Recommended free asset sources

- Kenney assets for CC0 UI/icons/placeholders.
- OpenGameArt, but license must be checked per asset.
- itch.io asset packs, but license must be checked per pack.
- FreeGameAssets, but license must be checked per asset.

## Modification pipeline

Imported free assets should usually be modified to fit NG:

1. Download asset.
2. Record source and license.
3. Resize/crop/recolor as needed.
4. Convert to project naming convention.
5. Add metadata.
6. Keep originals out of the repo if too large.

## Naming convention

```text
assets/ui/panel_dark_stone_01.png
assets/icons/items/sword_border_iron_01.png
assets/icons/abilities/strike_heavy_01.png
assets/portraits/captain_renna_01.png
```

## Important rule

Do not import assets just because they are free. Prefer a small coherent set over a huge inconsistent asset dump.
