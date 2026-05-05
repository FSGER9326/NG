#!/usr/bin/env python3
"""Validate NG asset placement plans.

Placement plans connect generated/kit assets to area layout constraints. They are
used before final background plates are assembled, so they should stay aligned
with layout zones, doors, paths, hotspots, and batch manifests.

Usage:
    python tools/validate_asset_placement_plans.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AREAS_ROOT = ROOT / "areas"
BATCH_ROOT = ROOT / "data" / "asset_batches"
KIT_ROOT = ROOT / "data" / "asset_kits"

PLAN_SUFFIX = "_asset_placement_plan.json"

PLAN_REQUIRED = {
    "id",
    "area_id",
    "batch_id",
    "canvas_size",
    "purpose",
    "source_files",
    "global_rules",
    "placements",
}

PLACEMENT_REQUIRED = {
    "asset_id",
    "asset_role",
    "target_zone",
    "target_layer",
    "intended_file",
    "anchor_point",
    "expected_footprint",
    "must_not_block_paths",
    "nearby_walkable_zones",
    "review_notes",
}

VALID_LAYERS = {
    "background_buildings",
    "props_interactive",
    "props_noninteractive",
    "foreground_occluders",
    "ground_decals",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def as_text_list(value: Any) -> list[str]:
    return [item for item in as_list(value) if isinstance(item, str)]


def placement_plan_files() -> list[Path]:
    if not AREAS_ROOT.exists():
        return []
    return sorted(path for path in AREAS_ROOT.rglob(f"*{PLAN_SUFFIX}") if path.is_file())


def load_batch_index() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not BATCH_ROOT.exists():
        return result
    for path in sorted(BATCH_ROOT.glob("*.json")):
        data = load_json(path)
        if isinstance(data, dict) and isinstance(data.get("id"), str):
            result[data["id"]] = data
    return result


def load_kit_asset_index() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not KIT_ROOT.exists():
        return result
    for path in sorted(KIT_ROOT.glob("*.json")):
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        for asset in as_list(data.get("assets")):
            if isinstance(asset, dict) and isinstance(asset.get("id"), str):
                result[asset["id"]] = asset
    return result


def load_layout(area_id: str) -> tuple[Path | None, dict[str, Any] | None]:
    layout_path = AREAS_ROOT / area_id / "layout_constraints.json"
    if not layout_path.exists():
        return None, None
    data = load_json(layout_path)
    if not isinstance(data, dict):
        return layout_path, None
    return layout_path, data


def point_is_valid(point: Any, canvas_size: list[int]) -> bool:
    if not isinstance(point, list) or len(point) != 2:
        return False
    if not all(isinstance(value, int | float) for value in point):
        return False
    width, height = canvas_size
    return 0 <= float(point[0]) <= width and 0 <= float(point[1]) <= height


def polygon_is_valid(points: Any, canvas_size: list[int], min_points: int = 3) -> bool:
    if not isinstance(points, list) or len(points) < min_points:
        return False
    return all(point_is_valid(point, canvas_size) for point in points)


def collect_layout_ids(layout: dict[str, Any]) -> dict[str, set[str]]:
    walkable_zones: set[str] = set()
    buildings: set[str] = set()
    doors: set[str] = set()
    paths: set[str] = set()
    hotspots: set[str] = set()
    npc_zones: set[str] = set()

    for zone in as_list(layout.get("walkable_zones")):
        if isinstance(zone, dict) and isinstance(zone.get("zone_id"), str):
            walkable_zones.add(zone["zone_id"])
    for building in as_list(layout.get("buildings")):
        if isinstance(building, dict) and isinstance(building.get("building_id"), str):
            buildings.add(building["building_id"])
    for door in as_list(layout.get("doors")):
        if isinstance(door, dict):
            if isinstance(door.get("door_id"), str):
                doors.add(door["door_id"])
            if isinstance(door.get("hotspot_id"), str):
                hotspots.add(door["hotspot_id"])
    for path in as_list(layout.get("required_paths")):
        if isinstance(path, dict) and isinstance(path.get("path_id"), str):
            paths.add(path["path_id"])
    for hotspot in as_list(layout.get("hotspot_access")):
        if isinstance(hotspot, dict) and isinstance(hotspot.get("hotspot_id"), str):
            hotspots.add(hotspot["hotspot_id"])
    for npc_zone in as_list(layout.get("npc_zones")):
        if isinstance(npc_zone, dict) and isinstance(npc_zone.get("zone_id"), str):
            npc_zones.add(npc_zone["zone_id"])

    return {
        "walkable_zones": walkable_zones,
        "buildings": buildings,
        "doors": doors,
        "paths": paths,
        "hotspots": hotspots,
        "npc_zones": npc_zones,
    }


def batch_asset_index(batch: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for asset in as_list(batch.get("assets")):
        if isinstance(asset, dict) and isinstance(asset.get("asset_id"), str):
            result[asset["asset_id"]] = asset
    return result


def check_text_list(path: Path, context: str, field: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{rel(path)} {context}: {field} must be a non-empty list")
        return
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{rel(path)} {context}: {field} entries must be non-empty strings")


def check_plan(path: Path, data: Any, batches: dict[str, dict[str, Any]], kit_assets: dict[str, dict[str, Any]], errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append(f"{rel(path)}: placement plan must be an object")
        return

    missing = sorted(PLAN_REQUIRED - set(data.keys()))
    if missing:
        errors.append(f"{rel(path)}: missing required fields: {', '.join(missing)}")

    plan_id = data.get("id")
    if not isinstance(plan_id, str) or not plan_id.strip():
        errors.append(f"{rel(path)}: id must be a non-empty string")

    area_id = data.get("area_id")
    if not isinstance(area_id, str) or not area_id.strip():
        errors.append(f"{rel(path)}: area_id must be a non-empty string")
        return

    layout_path, layout = load_layout(area_id)
    if layout_path is None:
        errors.append(f"{rel(path)}: missing layout constraints for area: {area_id}")
        return
    if layout is None:
        errors.append(f"{rel(path)}: layout constraints must be an object: {rel(layout_path)}")
        return

    canvas_size = data.get("canvas_size")
    if not isinstance(canvas_size, list) or len(canvas_size) != 2 or not all(isinstance(value, int) and value > 0 for value in canvas_size):
        errors.append(f"{rel(path)}: canvas_size must be [positive_int, positive_int]")
        canvas_size = [1280, 720]

    layout_canvas_size = layout.get("canvas_size")
    if layout_canvas_size != canvas_size:
        errors.append(f"{rel(path)}: canvas_size must match layout_constraints.json canvas_size {layout_canvas_size}")

    batch_id = data.get("batch_id")
    batch = batches.get(batch_id) if isinstance(batch_id, str) else None
    if batch is None:
        errors.append(f"{rel(path)}: batch_id references missing asset batch: {batch_id}")
        batch_assets: dict[str, dict[str, Any]] = {}
    else:
        batch_assets = batch_asset_index(batch)
        if batch.get("target_area") != area_id:
            errors.append(f"{rel(path)}: batch target_area {batch.get('target_area')!r} does not match plan area_id {area_id!r}")

    check_text_list(path, "plan", "source_files", data.get("source_files"), errors)
    for source_file in as_text_list(data.get("source_files")):
        if not (ROOT / source_file).exists():
            errors.append(f"{rel(path)}: source_file does not exist: {source_file}")

    check_text_list(path, "plan", "global_rules", data.get("global_rules"), errors)

    placements = data.get("placements")
    if not isinstance(placements, list) or not placements:
        errors.append(f"{rel(path)}: placements must be a non-empty list")
        return

    layout_ids = collect_layout_ids(layout)
    seen_assets: set[str] = set()
    for index, placement in enumerate(placements, start=1):
        if not isinstance(placement, dict):
            errors.append(f"{rel(path)} placement #{index}: must be an object")
            continue
        check_placement(path, index, placement, canvas_size, layout_ids, batch_assets, kit_assets, seen_assets, errors)


def check_placement(
    path: Path,
    index: int,
    placement: dict[str, Any],
    canvas_size: list[int],
    layout_ids: dict[str, set[str]],
    batch_assets: dict[str, dict[str, Any]],
    kit_assets: dict[str, dict[str, Any]],
    seen_assets: set[str],
    errors: list[str],
) -> None:
    asset_id = placement.get("asset_id", f"#{index}")
    if not isinstance(asset_id, str) or not asset_id.strip():
        errors.append(f"{rel(path)} placement #{index}: asset_id must be a non-empty string")
        asset_id = f"#{index}"
    elif asset_id in seen_assets:
        errors.append(f"{rel(path)}: duplicate placement asset_id: {asset_id}")
    else:
        seen_assets.add(asset_id)

    missing = sorted(PLACEMENT_REQUIRED - set(placement.keys()))
    if missing:
        errors.append(f"{rel(path)} placement {asset_id}: missing fields: {', '.join(missing)}")

    if batch_assets and asset_id not in batch_assets:
        errors.append(f"{rel(path)} placement {asset_id}: asset_id not found in batch manifest")
    if kit_assets and asset_id not in kit_assets:
        errors.append(f"{rel(path)} placement {asset_id}: asset_id not found in asset kit manifests")

    intended_file = placement.get("intended_file")
    if not isinstance(intended_file, str) or not intended_file.startswith("assets/kits/"):
        errors.append(f"{rel(path)} placement {asset_id}: intended_file must start with assets/kits/")
    else:
        batch_asset = batch_assets.get(asset_id)
        if batch_asset is not None and intended_file != batch_asset.get("target_file"):
            errors.append(f"{rel(path)} placement {asset_id}: intended_file must match batch target_file")
        kit_asset = kit_assets.get(asset_id)
        if kit_asset is not None and intended_file != kit_asset.get("intended_file"):
            errors.append(f"{rel(path)} placement {asset_id}: intended_file must match kit intended_file")

    target_layer = placement.get("target_layer")
    if target_layer not in VALID_LAYERS:
        errors.append(f"{rel(path)} placement {asset_id}: invalid target_layer {target_layer!r}")

    target_zone = placement.get("target_zone")
    valid_target_zones = layout_ids["walkable_zones"] | layout_ids["buildings"] | layout_ids["npc_zones"]
    if not isinstance(target_zone, str) or target_zone not in valid_target_zones:
        errors.append(f"{rel(path)} placement {asset_id}: unknown target_zone {target_zone!r}")

    if not point_is_valid(placement.get("anchor_point"), canvas_size):
        errors.append(f"{rel(path)} placement {asset_id}: anchor_point must be inside canvas")

    if not polygon_is_valid(placement.get("expected_footprint"), canvas_size):
        errors.append(f"{rel(path)} placement {asset_id}: expected_footprint must be a polygon inside canvas")

    for door_id in as_text_list(placement.get("required_visible_doors")):
        if door_id not in layout_ids["doors"]:
            errors.append(f"{rel(path)} placement {asset_id}: unknown required_visible_door {door_id}")

    hotspot_id = placement.get("hotspot_id")
    if hotspot_id is not None and (not isinstance(hotspot_id, str) or hotspot_id not in layout_ids["hotspots"]):
        errors.append(f"{rel(path)} placement {asset_id}: unknown hotspot_id {hotspot_id!r}")

    for path_id in as_text_list(placement.get("must_not_block_paths")):
        if path_id not in layout_ids["paths"]:
            errors.append(f"{rel(path)} placement {asset_id}: unknown must_not_block_path {path_id}")

    nearby_zones = placement.get("nearby_walkable_zones")
    check_text_list(path, f"placement {asset_id}", "nearby_walkable_zones", nearby_zones, errors)
    for zone_id in as_text_list(nearby_zones):
        if zone_id not in layout_ids["walkable_zones"]:
            errors.append(f"{rel(path)} placement {asset_id}: nearby_walkable_zone is not walkable: {zone_id}")

    check_text_list(path, f"placement {asset_id}", "review_notes", placement.get("review_notes"), errors)


def main() -> int:
    errors: list[str] = []
    files = placement_plan_files()
    if not files:
        errors.append("No asset placement plans found under areas/.")

    try:
        batches = load_batch_index()
        kit_assets = load_kit_asset_index()
    except json.JSONDecodeError as exc:
        print(f"Asset placement validation failed: invalid referenced JSON: {exc}")
        return 1

    for path in files:
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {rel(path)}: {exc}")
            continue
        check_plan(path, data, batches, kit_assets, errors)

    if errors:
        print("Asset placement validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Asset placement validation passed: {len(files)} placement plan(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
