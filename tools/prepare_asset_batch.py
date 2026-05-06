#!/usr/bin/env python3
"""Prepare deterministic batch scaffolding for asset production sessions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime, timezone


REQUIRED_REGISTRY_FILE = Path("data/asset_registry/scene_builder_registry.json")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_batch_file(batch_id: str) -> Path:
    candidate = Path("data/asset_registry/batches") / f"{batch_id}.json"
    if not candidate.exists():
        raise SystemExit(f"Batch file not found: {candidate}")
    return candidate


def ensure_registry_has_kit(registry: dict, kit_id: str) -> None:
    kits = registry.get("kits", [])
    found = any(k.get("kit_id") == kit_id for k in kits)
    if not found:
        raise SystemExit(f"kit_id '{kit_id}' not found in {REQUIRED_REGISTRY_FILE}")


def build_report_template(batch: dict) -> str:
    asset_lines = "\n".join(f"- {asset_id}" for asset_id in batch["asset_ids"])
    gates = "\n".join([
        "- Gate A (style/readability): pending",
        "- Gate B (legal/provenance): pending",
        "- Gate C (technical): pending",
        "- Gate D (manifest integrity): pending",
        "- Gate E (in-engine readiness): pending",
    ])
    validators = "\n".join(f"- `{cmd}`" for cmd in batch["required_validators"])

    return f"""# Batch QA Report: {batch['batch_id']}

## Scope

- kit_id: `{batch['kit_id']}`
- goal: `{batch['goal']}`
- generated_at_utc: `{datetime.now(timezone.utc).isoformat()}`

## Asset IDs

{asset_lines}

## Gate Status

{gates}

## Validator Commands

{validators}

## Notes

- Fill in pass/fail outcomes for each gate.
- Link any rejections with reason and remediation.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Create batch scaffold for asset production")
    parser.add_argument("batch_id", help="Batch id matching data/asset_registry/batches/<batch_id>.json")
    parser.add_argument("--out", default="debug/asset_batches", help="Output root folder")
    args = parser.parse_args()

    if not REQUIRED_REGISTRY_FILE.exists():
        raise SystemExit(f"Missing required registry file: {REQUIRED_REGISTRY_FILE}")

    registry = load_json(REQUIRED_REGISTRY_FILE)
    batch_file = find_batch_file(args.batch_id)
    batch = load_json(batch_file)

    ensure_registry_has_kit(registry, batch["kit_id"])

    out_root = Path(args.out) / args.batch_id
    prompts_dir = out_root / "prompts"
    qa_dir = out_root / "qa"
    candidates_dir = out_root / "candidates"

    prompts_dir.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)
    candidates_dir.mkdir(parents=True, exist_ok=True)

    (out_root / "batch.json").write_text(json.dumps(batch, indent=2) + "\n", encoding="utf-8")
    (qa_dir / "report.md").write_text(build_report_template(batch), encoding="utf-8")

    print(f"Prepared batch scaffold at: {out_root}")
    print(f"Asset count: {len(batch['asset_ids'])}")


if __name__ == "__main__":
    main()
