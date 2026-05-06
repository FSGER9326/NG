# Wolfpine Village SVG Tech Art Bible

## Primitive library location

All reusable primitive building blocks for Wolfpine SVG production live under:

- `assets/kits/wolfpine_village/svg_primitives/base_motifs/`
- `assets/kits/wolfpine_village/svg_primitives/contact_shadows/`
- `assets/kits/wolfpine_village/svg_primitives/edge_wear/`

### Required primitive packs

- **Base motifs (mandatory for structural classes):** timber/plaster/stone motifs.
- **Contact shadows (mandatory for structural + grounded classes):** at least one contact-shadow primitive.
- **Edge wear overlays (mandatory for structural classes):** at least one edge-wear overlay.

## Asset classes and mandatory primitives

### Structural classes

Structural classes include facades, walls, fence segments, gates, doors, windows, and load-bearing architecture modules.

Mandatory primitives per asset:

1. One base motif from `base_motifs`.
2. One contact-shadow primitive from `contact_shadows`.
3. One edge-wear overlay from `edge_wear`.

### Grounded non-structural classes

Grounded classes include freestanding props touching terrain (wells, carts, stalls, signposts).

Mandatory primitives per asset:

1. One contact-shadow primitive.

Recommended (not mandatory):

- one base motif if the prop has broad flat faces,
- one edge-wear overlay if the silhouette contains long uninterrupted edges.

### Floating or decal classes

Floating, suspended, and decal-only classes are exempt from mandatory primitives, but should still include anti-flatness treatment where practical.

## Allowed overrides

Overrides are allowed only when all of the following are true:

1. The override is documented in SVG comments using `NG-OVERRIDE-REASON`.
2. The replacement remains materially equivalent (e.g., custom timber variant instead of stock timber motif).
3. The asset still satisfies anti-flatness minimums.

Allowed override examples:

- Swapping `base_timber_frame_v1` for a custom `base_timber_frame_dense_v2` defined locally.
- Replacing a soft contact shadow with a hard-edged threshold shadow for doors.
- Using custom stone chip wear tuned to hero props.

Not allowed:

- Removing contact grounding on grounded or structural assets.
- Removing edge wear entirely on structural assets without documented technical exception.

## Anti-flatness minimum requirements

For structural classes, all assets must satisfy:

1. **Material breakup:** at least one base motif pass.
2. **Grounding:** at least one contact-shadow pass near terrain-facing boundary.
3. **Edge variation:** at least one edge-wear overlay pass on exposed silhouette or major panel boundaries.
4. **Metadata traceability:** primitive references and class marker present in SVG comments/metadata.

Minimum metadata/comments markers for validator compliance on structural classes:

- `NG-SVG-CLASS: structural`
- `NG-PRIMITIVE-BASE: <id>`
- `NG-PRIMITIVE-SHADOW: <id>`
- `NG-PRIMITIVE-EDGE: <id>`

Optional marker:

- `NG-OVERRIDE-REASON: <short reason>`
