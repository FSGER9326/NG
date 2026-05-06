# Wolfpine First Binary Promotion Review — 2026-05-06

This review note is the bridge between the local optimized PNG handoff and the canonical Wolfpine asset kit.

The binary handoff package is intentionally not committed by this document. To promote it, run the checked-in promotion tool against the local ZIP and commit the resulting PNG files plus `data/asset_kits/wolfpine_village_starter.json` updates.

## Source package

```text
ng_wolfpine_first_promotion_optimized.zip
```

The ZIP should contain exactly these five PNGs:

| Asset ID | ZIP member | Canonical path | Expected SHA256 | Planned status |
|---|---|---|---|---|
| `wolfpine_well_01` | `props/wolfpine_well_01.png` | `assets/kits/wolfpine_village/props/wolfpine_well_01.png` | `ac46b5af0fb013cdfb0b113a2b9684380cb0b56ab7c129d1ba3a698d5cee3185` | `cleaned` |
| `wolfpine_notice_board_01` | `props/wolfpine_notice_board_01.png` | `assets/kits/wolfpine_village/props/wolfpine_notice_board_01.png` | `c056d94f5add4e62473a0c36f00614520f15b45870829b6cb4a7e5522cf7c62a` | `cleaned` |
| `wolfpine_door_heavy_01` | `architecture/wolfpine_door_heavy_01.png` | `assets/kits/wolfpine_village/architecture/wolfpine_door_heavy_01.png` | `d1ded59dcd520c2f09c1d959cb938efb5762371205fec7b2a3265fcdd359dcbf` | `cleaned` |
| `wolfpine_window_shuttered_01` | `architecture/wolfpine_window_shuttered_01.png` | `assets/kits/wolfpine_village/architecture/wolfpine_window_shuttered_01.png` | `0873dcc7e217bd3233053829296b202d6467c9848f3ab4d039660d414d9c3de4` | `cleaned` |
| `wolfpine_firewood_stack_01` | `props/wolfpine_firewood_stack_01.png` | `assets/kits/wolfpine_village/props/wolfpine_firewood_stack_01.png` | `fe424f6ba6bdc7b3a70b624ca301c91cd722fbdd9dd095dc00310cac93abc2e9` | `cleaned` |

## Required local commands

Run from the repository root with the ZIP placed beside the checkout or pass an absolute ZIP path.

```bash
python tools/promote_asset_candidates.py \
  --zip ng_wolfpine_first_promotion_optimized.zip \
  --plan assets/kits/wolfpine_village/FIRST_BINARY_PROMOTION_2026_05_06.json \
  --dry-run
```

If the dry run passes, run:

```bash
python tools/promote_asset_candidates.py \
  --zip ng_wolfpine_first_promotion_optimized.zip \
  --plan assets/kits/wolfpine_village/FIRST_BINARY_PROMOTION_2026_05_06.json
```

Then run the normal validation suite:

```bash
python tools/validate_asset_kits.py
python tools/validate_asset_production_batches.py
python tools/validate_asset_promotion_plans.py
python tools/test_promote_asset_candidates.py
```

## Review checklist before `accepted`

Do not mark these assets `accepted` immediately after promotion. Keep them at `cleaned` until visual review confirms:

- Alpha edges look clean on light, dark, and game-like backgrounds.
- Contact shadows do not conflict with the Wolfpine village plate lighting.
- Asset scale is usable at the intended Godot viewport size.
- `wolfpine_well_01` can sit near the square without blocking actor approach.
- `wolfpine_notice_board_01` reads as a quest board and contains no readable real text.
- `wolfpine_door_heavy_01` reads as a ground-level door, not a window.
- `wolfpine_window_shuttered_01` cannot be mistaken for a door or interactable entrance.
- `wolfpine_firewood_stack_01` works beside both cottage and blacksmith facades without blocking doors.

## Acceptance rule

After local promotion, these are still `cleaned` assets. A later PR may move any individual asset to `accepted` only when:

1. the PNG exists at the canonical path,
2. manifest status and SHA256 match the committed file,
3. the asset has been checked in the Godot scene/layout context,
4. the relevant validators pass,
5. source/generation notes remain present.
