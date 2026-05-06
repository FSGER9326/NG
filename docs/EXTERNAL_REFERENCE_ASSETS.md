# External Reference Assets

External reference assets are allowed as a visual benchmark, but only when their license allows the intended project use and the original assets are not redistributed through this repository.

## PVGames Infernus Free

- Provider: Pioneer Valley Games / PVGames
- Pack: `PVGames_Infernus_Free.zip`
- Local-only unpack path: `reference_assets/local/pvgames/infernus_free/`
- Repo policy: do not commit the original PNG resources, edited copies, or unpacked pack contents.
- Allowed repo artifacts: documentation, metadata, local path instructions, quality-bar notes.

The pack readme permits use and editing in commercial and non-commercial projects, but it does not permit freely distributing the resources or edited resource files. Treat it as a local-only reference pack.

## How agents should use this reference

1. Keep the PVGames files outside version control under `reference_assets/local/pvgames/infernus_free/`.
2. Use the pack only as a quality benchmark for rendering craft, perspective discipline, silhouette clarity, alpha cleanup, material detail, and modular tile consistency.
3. Do not copy, trace, recolor, upscale, or derive NG assets directly from these files.
4. Generated NG assets must be original, project-specific, and tracked through the normal manifest, QA, and validator flow.
5. If a future pack has a different license, add a separate registry entry before using it.

## Quality benchmark notes

Generated or cleaned NG art should aim to meet or exceed this reference level in:

- crisp pseudo-isometric construction
- consistent top-left lighting and shadow logic
- clean transparent edges without halos
- readable silhouettes at gameplay scale
- modular parts that align predictably
- material rendering for stone, wood, metal, cloth, dirt, and vegetation
- coherent kit-wide palette and detail density
