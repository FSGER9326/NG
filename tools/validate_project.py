#!/usr/bin/env python3
"""Validate NG project data.

This script is intentionally dependency-free so it can run on any basic Python 3 install.
It checks JSON parsing, duplicate IDs, and common file references used by the starter content pipeline.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
JSON_ROOTS = [ROOT / "data", ROOT / "areas", ROOT / "dialogue"]

REFERENCE_KEYS = {
    "background",
    "occlusion",
    "walkmask",
    "hotspots",
    "actors",
    "portrait",
    "dialogue",
    "sprite",
    "icon",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def walk_json_files() -> list[Path]:
    files: list[Path] = []
    for root in JSON_ROOTS:
        if root.exists():
            files.extend(sorted(root.rglob("*.json")))
    return files


def collect_ids(path: Path, data: Any, ids: dict[str, Path], errors: list[str]) -> None:
    if isinstance(data, dict):
        item_id = data.get("id")
        if isinstance(item_id, str):
            if item_id in ids:
                errors.append(f"Duplicate id '{item_id}' in {path.relative_to(ROOT)} and {ids[item_id].relative_to(ROOT)}")
            else:
                ids[item_id] = path
        for value in data.values():
            collect_ids(path, value, ids, errors)
    elif isinstance(data, list):
        for value in data:
            collect_ids(path, value, ids, errors)


def check_references(path: Path, data: Any, errors: list[str]) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in REFERENCE_KEYS and isinstance(value, str):
                if value.startswith("res://"):
                    ref = ROOT / value.removeprefix("res://")
                else:
                    ref = ROOT / value
                if not ref.exists():
                    errors.append(f"Missing referenced file in {path.relative_to(ROOT)}: {key} -> {value}")
            check_references(path, value, errors)
    elif isinstance(data, list):
        for value in data:
            check_references(path, value, errors)


def main() -> int:
    errors: list[str] = []
    ids: dict[str, Path] = {}
    files = walk_json_files()

    if not files:
        errors.append("No JSON files found under data/, areas/, or dialogue/.")

    for path in files:
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")
            continue
        collect_ids(path, data, ids, errors)
        check_references(path, data, errors)

    if errors:
        print("NG validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"NG validation passed: {len(files)} JSON files, {len(ids)} IDs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
