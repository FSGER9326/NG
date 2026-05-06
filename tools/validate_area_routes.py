#!/usr/bin/env python3
"""Validate playable area route continuity.

This catches broken clickable exits before they reach runtime. Every hotspot with
`type: exit` must point at an existing area and an entry point defined by that
area's `area.json`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AREAS_ROOT = ROOT / "areas"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def area_files() -> list[Path]:
    if not AREAS_ROOT.exists():
        return []
    return sorted(AREAS_ROOT.glob("*/area.json"))


def build_area_index(errors: list[str]) -> dict[str, dict[str, Any]]:
    areas: dict[str, dict[str, Any]] = {}
    for path in area_files():
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {rel(path)}: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel(path)}: area file must be an object")
            continue
        area_id = data.get("id")
        if not isinstance(area_id, str) or not area_id:
            errors.append(f"{rel(path)}: area id must be a non-empty string")
            continue
        if area_id in areas:
            errors.append(f"Duplicate area id {area_id!r} in {rel(path)} and {rel(areas[area_id]['_path'])}")
            continue
        data["_path"] = path
        areas[area_id] = data
    return areas


def check_hotspot_routes(area_id: str, area_data: dict[str, Any], areas: dict[str, dict[str, Any]], errors: list[str]) -> None:
    hotspots_ref = area_data.get("hotspots")
    area_path = area_data.get("_path")
    if not isinstance(area_path, Path):
        return
    if not isinstance(hotspots_ref, str) or not hotspots_ref:
        errors.append(f"{rel(area_path)}: hotspots must reference a hotspot JSON file")
        return
    hotspots_path = ROOT / hotspots_ref
    if not hotspots_path.exists():
        errors.append(f"{rel(area_path)}: hotspots file is missing: {hotspots_ref}")
        return

    try:
        hotspots_data = load_json(hotspots_path)
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {rel(hotspots_path)}: {exc}")
        return
    hotspots = hotspots_data.get("hotspots") if isinstance(hotspots_data, dict) else None
    if not isinstance(hotspots, list):
        errors.append(f"{rel(hotspots_path)}: hotspots must be a list")
        return

    for hotspot in hotspots:
        if not isinstance(hotspot, dict) or hotspot.get("type") != "exit":
            continue
        hotspot_id = hotspot.get("id", "<missing id>")
        target_area = hotspot.get("target_area")
        target_entry = hotspot.get("target_entry")
        context = f"{rel(hotspots_path)} exit {hotspot_id}"
        if not isinstance(target_area, str) or not target_area:
            errors.append(f"{context}: target_area must be a non-empty string")
            continue
        if target_area not in areas:
            errors.append(f"{context}: target_area does not exist: {target_area}")
            continue
        if not isinstance(target_entry, str) or not target_entry:
            errors.append(f"{context}: target_entry must be a non-empty string")
            continue
        target_entries = areas[target_area].get("entry_points")
        if not isinstance(target_entries, dict):
            errors.append(f"{rel(areas[target_area]['_path'])}: entry_points must be an object")
            continue
        if target_entry not in target_entries:
            errors.append(f"{context}: target_entry {target_entry!r} is not defined by area {target_area}")


def main() -> int:
    errors: list[str] = []
    areas = build_area_index(errors)
    for area_id, area_data in sorted(areas.items()):
        check_hotspot_routes(area_id, area_data, areas, errors)

    if errors:
        print("Area route validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"Area route validation passed: {len(areas)} area(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
