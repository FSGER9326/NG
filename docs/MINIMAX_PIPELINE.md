# MiniMax Production Asset Pipeline

## Purpose

Use MiniMax through `MiniMax-AI/MiniMax-MCP` as a local/AI-tool asset-generation pipeline for NG, especially for:

- temporary and final NPC voice lines
- narration prototypes
- ambient voice barks
- generated concept images for portraits/items/UI references
- possible short promotional/video material later

MiniMax should **not** be a required runtime dependency for the shipped Godot game at this stage.

## Why not call MiniMax directly from the game?

The game target is low-spec, offline-friendly, and easy to debug. Runtime API calls would add:

- API key handling risk
- network dependency
- token/cost unpredictability
- platform/privacy concerns
- harder reproduction of bugs
- possible latency during play

Instead, use MiniMax during production to generate assets, then commit only reviewed output files and metadata.

## Intended architecture

```text
MiniMax account/token plan
        ↓
MiniMax-MCP configured locally in an MCP-capable client
        ↓
Generated audio/image/video files saved locally
        ↓
Reviewed/trimmed/renamed project assets
        ↓
assets/generated/minimax/...
        ↓
assets/ledger/assets.json attribution/source records
        ↓
Godot loads normal local files
```

## Secret handling

Never commit MiniMax credentials.

Allowed local-only locations:

```text
.env
local_config.json
secrets/
api_keys/
```

These are already ignored by `.gitignore`.

Do not put API keys in:

```text
project.godot
export_presets.cfg
docs/
assets/ledger/assets.json
*.tscn
*.gd
```

## MiniMax-MCP setup pattern

MiniMax-MCP expects environment variables such as:

```text
MINIMAX_API_KEY
MINIMAX_API_HOST
MINIMAX_MCP_BASE_PATH
MINIMAX_API_RESOURCE_MODE
```

Use the API host that matches the account region:

```text
Global:   https://api.minimax.io
Mainland: https://api.minimaxi.com
```

Recommended local output path for NG:

```text
<repo>/asset_sources/minimax_output
```

Keep raw/generated work files out of the committed game until reviewed.

## Recommended MCP client config shape

Use this only in your local MCP-capable client config, not in the repo:

```json
{
  "mcpServers": {
    "MiniMax": {
      "command": "uvx",
      "args": ["minimax-mcp", "-y"],
      "env": {
        "MINIMAX_API_KEY": "YOUR_LOCAL_KEY_ONLY",
        "MINIMAX_MCP_BASE_PATH": "C:/path/to/NG/asset_sources/minimax_output",
        "MINIMAX_API_HOST": "https://api.minimax.io",
        "MINIMAX_API_RESOURCE_MODE": "local"
      }
    }
  }
}
```

## Output folders

Raw local output, not committed by default:

```text
asset_sources/minimax_output/
asset_sources/raw/
asset_sources/tmp/
```

Reviewed project assets, may be committed:

```text
assets/generated/minimax/audio/dialogue/
assets/generated/minimax/audio/barks/
assets/generated/minimax/images/portraits/
assets/generated/minimax/images/items/
assets/generated/minimax/video/
```

## Voice asset naming

Use stable, searchable names:

```text
assets/generated/minimax/audio/dialogue/captain_renna_missing_caravan_001.ogg
assets/generated/minimax/audio/dialogue/captain_renna_shrine_report_001.ogg
assets/generated/minimax/audio/barks/brannoc_selection_001.ogg
```

Prefer `.ogg` for Godot runtime use.

## Image asset naming

```text
assets/generated/minimax/images/portraits/captain_renna_concept_001.png
assets/generated/minimax/images/items/border_iron_sword_concept_001.png
```

Generated images should be treated as source/reference until reviewed for style consistency.

## Asset ledger entries

Every committed MiniMax-derived asset should have an entry in:

```text
assets/ledger/assets.json
```

Suggested entry:

```json
{
  "id": "voice_captain_renna_shrine_report_001",
  "file": "assets/generated/minimax/audio/dialogue/captain_renna_shrine_report_001.ogg",
  "type": "voice_line",
  "source": "minimax",
  "source_url": "https://github.com/MiniMax-AI/MiniMax-MCP",
  "license": "generated_output_review_required",
  "modified": true,
  "notes": "Generated locally through MiniMax-MCP, trimmed/converted for NG. Requires project-owner review before final release."
}
```

## Dialogue integration plan

Dialogue JSON should reference local voice files only after they exist and are reviewed.

Future dialogue line shape:

```json
{
  "text": "Renna's expression tightens...",
  "voice": "assets/generated/minimax/audio/dialogue/captain_renna_shrine_report_001.ogg"
}
```

Do not block gameplay on missing voice files. Missing voice should only log a warning.

## Production rule

MiniMax may be part of **production workflow**.

MiniMax is not part of **runtime gameplay** unless a future explicit online-mode feature is designed, secured, budgeted, and tested.

## Next implementation steps

1. Add optional `voice` fields to dialogue nodes.
2. Add validation for existing voice-file references when present.
3. Add a tiny Godot audio playback helper for dialogue voice files.
4. Add a reviewed sample placeholder voice entry once an actual file exists.
5. Keep all credentials local-only.
