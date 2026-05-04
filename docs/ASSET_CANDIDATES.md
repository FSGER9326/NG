# NG Asset Candidates

This file tracks asset sources worth using for NG. The goal is to reduce dependence on generating every UI/icon/sound asset from scratch while keeping licensing clean.

## Current decision

Use a staged asset approach:

1. **In-repo generated placeholders** for immediate UI/icons/portraits.
2. **CC0/free asset packs** for generic UI, icons, SFX, fonts, and prototype sprites.
3. **Custom/AI-assisted pseudo-isometric area plates** for final world backgrounds.
4. **Manual license review before importing any external asset into the repo.**

## Priority sources

### Kenney

Best use:

- UI panels/buttons/icons
- placeholder cursors
- simple SFX
- generic prototype icons
- possible sprite/object placeholders

Why useful:

- Large coherent asset collection.
- Good for quick prototype UI and icons.
- Generally safest source to start with when we need free reusable game assets.

License notes:

- Treat as preferred only when the specific pack/source page confirms CC0/public-domain style licensing.
- Still record source URL and pack name in `assets/ledger/assets.json` when imported.

### OpenGameArt

Best use:

- individual fantasy icons
- ambient SFX/music
- possible pixel props/tiles

License notes:

- Must review each asset individually.
- Prefer CC0 or OGA-BY.
- Avoid GPL, CC-BY-SA, and ambiguous licenses unless we explicitly choose to accept their obligations.
- Record attribution if required.

### FreeGameAssets

Best use:

- discovery/indexing only.
- Use it to find sources, not as an automatic import target.

License notes:

- Verify the license at the original source before importing anything.

### itch.io free packs

Best use:

- UI/icon packs
- small SFX packs
- maybe portrait/sprite prototypes

License notes:

- License differs per pack.
- Avoid packs with unclear, non-commercial, or no-derivatives terms.

## What not to import yet

- Large raw art dumps.
- Mixed-style asset megabundles without a clear purpose.
- Anything requiring attribution until the credits/attribution system exists.
- Anything that visually locks NG into a cartoony style.

## Near-term asset needs

### UI

- parchment/dark panel texture or flat style
- choice buttons
- quest tracker panel
- item slot background
- dialogue speaker frame
- cursor/interaction markers

### Icons

- sword
- shrine/inspect
- quest marker
- exit/road marker
- inventory bag
- dialogue marker

### Portraits

- Captain Renna
- Brannoc
- generic bandit

### Audio later

- button hover/click
- quest accepted
- page turn
- rain/wind ambience
- distant crows

## Import rule

Every external asset must have a ledger entry before it is used by data files.
