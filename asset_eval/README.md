# Asset Evaluation Intake

This folder is for evaluating free third-party assets before anything is promoted into the game.

## Rules

- Do not commit raw downloaded third-party packs.
- Download into `asset_eval/downloads/` only.
- Extract into `asset_eval/extracted/` only.
- Promote selected assets into `assets/vendor/<source_or_pack>/` only after review.
- Every promoted pack must include a source URL, license file or license note, and a manifest entry.
- Prefer CC0 and permissive licenses for first-playable placeholder assets.
- Avoid importing large frameworks or complete visual styles that fight the NG art direction.

## Local workflow

List candidates:

```bash
python tools/asset_eval_download.py --list
```

Download candidates that have a direct URL:

```bash
python tools/asset_eval_download.py --download
```

List one candidate:

```bash
python tools/asset_eval_download.py --id kenney_ui_audio --list
```

Validate the manifest:

```bash
python tools/validate_asset_eval_manifest.py
```

## Manual-download candidates

Most asset pages, especially Kenney and itch.io pages, require human review or a browser download step. For those:

1. Open the `source_page_url` from `asset_candidates.json`.
2. Confirm the license on the page.
3. Download to `asset_eval/downloads/`.
4. Add or update a local receipt/notes file.
5. Fill out `asset_eval/REVIEW_WORKSHEET.md`.

## Evaluation criteria

Score each candidate against:

- License clarity
- File size and repo suitability
- Godot import suitability
- Low-spec compatibility
- Match with NG's grounded low-fantasy tone
- Usefulness for first playable
- Whether the asset is placeholder-only or possible final material

## Promotion criteria

An asset can move from evaluation into `assets/vendor/` only when:

- license is clear and acceptable
- source URL is recorded
- file size is reasonable
- asset is actually used by a first-playable feature or a near-term prototype
- a small manifest documents usage and restrictions
