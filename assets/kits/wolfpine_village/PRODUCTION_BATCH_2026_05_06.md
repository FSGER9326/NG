# Wolfpine Production Candidate Batch — 2026-05-06

This batch records the first cleaned production pass for the modernized Infinity Engine / dark fantasy isometric Wolfpine asset direction.

The binary PNGs for this batch were cleaned locally into a handoff package. They are **not marked `accepted` in the canonical manifest yet** because accepted assets must exist at their intended repo paths and still need an in-Godot visual/layout review.

## Pipeline stage

- Source type: project-directed generated isolated candidates.
- External imported assets: none.
- License/source note: original project-directed generated candidates; no OpenGameArt or other third-party binaries were committed in this batch.
- Cleanup performed: alpha/background masking, crop with margin, minor color/contrast normalization, contact-shadow/grounding preserved where useful.
- Style target: modernized Infinity Engine, dark fantasy, fixed pseudo-isometric 3/4, painterly/pre-rendered look.

## Candidate table

| Asset ID | Status | Candidate file in handoff package | SHA256 prefix | Review notes |
|---|---:|---|---:|---|
| `wolfpine_inn_facade_01` | `cleaned` | `buildings/wolfpine_inn_facade_01.png` | `a0744f45423e` | Good production candidate: strong door/readability, usable roof/foundation; needs final hand alpha pass before accepted. |
| `wolfpine_blacksmith_facade_01` | `cleaned` | `buildings/wolfpine_blacksmith_facade_01.png` | `7390ad82efcf` | Strong production candidate: forge identity, chimney, door, work area; crop/alpha normalized. |
| `wolfpine_storehouse_facade_01` | `generated_candidate` | `buildings/wolfpine_storehouse_facade_01.png` | `beab18f5ac4a` | Good massing but not yet a perfect storehouse; needs door/guarded-supply paint pass before accepted. |
| `wolfpine_well_01` | `cleaned` | `props/wolfpine_well_01.png` | `15d967cd7dea` | Production-ready candidate: readable, grounded, fits square hotspot. |
| `wolfpine_market_stall_01` | `cleaned` | `props/wolfpine_market_stall_01.png` | `0f555abb8096` | Production-ready candidate for empty/low-stock market stall; needs optional food-clutter variant later. |
| `wolfpine_notice_board_01` | `cleaned` | `props/wolfpine_notice_board_01.png` | `708cbd891a37` | Production-ready candidate; no readable text, strong interaction silhouette. |
| `wolfpine_door_heavy_01` | `cleaned` | `architecture/wolfpine_door_heavy_01.png` | `fe9a1c40b5e0` | Production-ready modular door candidate; strong material read, ground threshold, lantern. |
| `wolfpine_window_shuttered_01` | `cleaned` | `architecture/wolfpine_window_shuttered_01.png` | `e95ace7a07ed` | Production-ready modular window candidate; clearly not a door. |
| `wolfpine_fence_segment_01` | `cleaned` | `architecture/wolfpine_fence_segment_01.png` | `0197e9e0ae3a` | Usable path-edge fence candidate; needs trimmed/no-ground variant for modular repetition. |
| `wolfpine_firewood_stack_01` | `cleaned` | `props/wolfpine_firewood_stack_01.png` | `56a515b3e13a` | Production-ready candidate; readable at scale, forge/cottage compatible. |
| `wolfpine_supply_pile_01` | `generated_candidate` | `clutter/wolfpine_supply_pile_01.png` | `5ea9db463db3` | Useful supplemental clutter; not in starter manifest yet. Split into barrel/crate/sack variants before canonical use. |
| `wolfpine_cart_loaded_01` | `generated_candidate` | `props/wolfpine_cart_loaded_01.png` | `d0df1ebe14cb` | Useful supplemental village/road prop; should become a new manifest entry if retained. |
| `wolfpine_chapel_gate_arch_01` | `generated_candidate` | `architecture/wolfpine_chapel_gate_arch_01.png` | `8d5848721040` | Strong chapel-path marker; should become a new manifest entry for chapel transition dressing. |
| `wolfpine_blacksmith_workbench_01` | `generated_candidate` | `props/wolfpine_blacksmith_workbench_01.png` | `48b6924f1e57` | Good forge dressing; should be split/normalized as separate tool bench/anvil props. |

## Recommended promotion order

1. `wolfpine_well_01`
2. `wolfpine_notice_board_01`
3. `wolfpine_door_heavy_01`
4. `wolfpine_window_shuttered_01`
5. `wolfpine_firewood_stack_01`
6. `wolfpine_market_stall_01`
7. `wolfpine_blacksmith_facade_01`
8. `wolfpine_inn_facade_01`
9. `wolfpine_fence_segment_01`
10. `wolfpine_storehouse_facade_01`

The supplemental candidates (`wolfpine_supply_pile_01`, `wolfpine_cart_loaded_01`, `wolfpine_chapel_gate_arch_01`, `wolfpine_blacksmith_workbench_01`) should either become new manifest entries or be split into smaller canonical pieces before acceptance.

## Acceptance blockers before marking `accepted`

- Commit the actual cleaned PNGs at their intended `assets/kits/wolfpine_village/...` paths.
- Review alpha edges over a neutral and dark game background.
- Check contact shadows do not conflict with the final village plate lighting.
- Load or mock-place the first-priority assets against `areas/wolfpine_village/layout_constraints.json`.
- Keep doors, routes, and hotspots readable: well, notice board, inn door, blacksmith door, market stall, chapel path, south road exit.

## Rejection notes from this pass

- Generic pixel-art sheets from earlier attempts are rejected for Wolfpine production use.
- Scene-sheet/collage outputs are rejected for canonical kit use.
- Full-frame 3D diorama candidates can be retained only when the object reads as a reusable isolated asset after cleanup.

## Next production step

Commit the cleaned PNG handoff package into the matching kit folders, then update `data/asset_kits/wolfpine_village_starter.json` from `planned` to `cleaned` or `accepted` only for assets whose files exist and pass review.
