# SVG Tech Art Bible (Wolfpine)

## Projection lock

- Fixed pseudo-isometric 3/4 view for all assets.
- No front-facing orthographic shortcuts for modular classes.

## Lighting lock

- Key light from upper-left.
- Contact/cast shadow direction down-right or slightly back-right.
- Maintain consistent value hierarchy: top plane > key-facing side > opposite side.

## Material language

- Dark timber, old stone, weathered plaster, moss, mud/cobble accents.
- Use restrained roughness overlays; avoid clean flat shapes.

## Anti-flatness rules

Required for medium+ assets:
- At least 3 major value bands.
- Localized wear/chip detail on structural edges.
- Subtle texture variation on broad surfaces.

## Complexity budget

- Prefer geometric shading + texture overlays over heavy filter stacks.
- Keep filter usage minimal and purposeful.
- Reject candidate if visual gain is minor but complexity is high.

## Readability

- Asset silhouette must remain legible at gameplay scale.
- Doors cannot be confused with windows.
- Path-facing interaction side must be clear.

## Modular seam discipline

- Join boundaries must align cleanly across compatible families.
- Elevation transitions must not create visual gaps.
