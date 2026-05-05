#!/usr/bin/env python3
"""Export an SVG placement preview for an NG asset placement plan.

This creates a lightweight visual map that helps review whether generated asset
candidates can fit the intended Wolfpine Village layout before final plate work.

Usage:
    python tools/export_asset_placement_preview.py areas/wolfpine_village/batch_01_asset_placement_plan.json

Output:
    debug/asset_placement_previews/<area_id>_<batch_id>.svg
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "debug" / "asset_placement_previews"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def point_to_str(point: Any) -> str:
    if isinstance(point, list) and len(point) >= 2:
        return f"{float(point[0]):.1f},{float(point[1]):.1f}"
    return "0,0"


def polygon_points(points: Any) -> str:
    return " ".join(point_to_str(point) for point in as_list(points))


def centroid(points: Any) -> tuple[float, float]:
    valid: list[tuple[float, float]] = []
    for point in as_list(points):
        if isinstance(point, list) and len(point) >= 2:
            valid.append((float(point[0]), float(point[1])))
    if not valid:
        return (0.0, 0.0)
    return (sum(point[0] for point in valid) / len(valid), sum(point[1] for point in valid) / len(valid))


def svg_text(x: float, y: float, text: str, class_name: str = "label") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{class_name}">{html.escape(text)}</text>'


def svg_polygon(points: Any, class_name: str, title: str) -> str:
    return f'<polygon points="{polygon_points(points)}" class="{class_name}"><title>{html.escape(title)}</title></polygon>'


def svg_circle(point: Any, radius: int, class_name: str, title: str) -> str:
    if not isinstance(point, list) or len(point) < 2:
        return ""
    return f'<circle cx="{float(point[0]):.1f}" cy="{float(point[1]):.1f}" r="{radius}" class="{class_name}"><title>{html.escape(title)}</title></circle>'


def build_svg(plan: dict[str, Any], layout: dict[str, Any]) -> str:
    canvas_size = plan.get("canvas_size", layout.get("canvas_size", [1280, 720]))
    width = int(canvas_size[0])
    height = int(canvas_size[1])
    area_id = str(plan.get("area_id", "unknown_area"))
    batch_id = str(plan.get("batch_id", "unknown_batch"))

    parts: list[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    parts.append("""
<style>
  .background { fill: #20251f; }
  .grid { stroke: #3a4038; stroke-width: 1; opacity: 0.35; }
  .walkable { fill: #6f8a54; opacity: 0.34; stroke: #b8d28e; stroke-width: 2; }
  .building { fill: #75553c; opacity: 0.34; stroke: #d3b083; stroke-width: 2; }
  .placement { fill: #5488a8; opacity: 0.42; stroke: #9fd7ff; stroke-width: 2; }
  .door { fill: #f1c56c; stroke: #3a260e; stroke-width: 2; }
  .anchor { fill: #f28f5b; stroke: #31140b; stroke-width: 2; }
  .hotspot { fill: #c879d8; stroke: #33133d; stroke-width: 2; }
  .label { fill: #f5ead2; font-family: sans-serif; font-size: 13px; paint-order: stroke; stroke: #131611; stroke-width: 3px; stroke-linejoin: round; }
  .small { fill: #f5ead2; font-family: sans-serif; font-size: 11px; paint-order: stroke; stroke: #131611; stroke-width: 3px; stroke-linejoin: round; }
  .title { fill: #f5ead2; font-family: sans-serif; font-size: 20px; font-weight: bold; paint-order: stroke; stroke: #131611; stroke-width: 4px; stroke-linejoin: round; }
</style>
""")
    parts.append(f'<rect width="{width}" height="{height}" class="background"/>')

    for x in range(0, width + 1, 80):
        parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" class="grid"/>')
    for y in range(0, height + 1, 80):
        parts.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" class="grid"/>')

    parts.append(svg_text(24, 34, f"{area_id} / {batch_id}", "title"))

    for zone in as_list(layout.get("walkable_zones")):
        if not isinstance(zone, dict):
            continue
        zone_id = str(zone.get("zone_id", "walkable"))
        points = zone.get("points", [])
        parts.append(svg_polygon(points, "walkable", f"walkable: {zone_id}"))
        x, y = centroid(points)
        parts.append(svg_text(x - 32, y, zone_id, "small"))

    for building in as_list(layout.get("buildings")):
        if not isinstance(building, dict):
            continue
        building_id = str(building.get("building_id", "building"))
        footprint = building.get("footprint", [])
        parts.append(svg_polygon(footprint, "building", f"building: {building_id}"))
        x, y = centroid(footprint)
        parts.append(svg_text(x - 38, y, building_id, "small"))

    for placement in as_list(plan.get("placements")):
        if not isinstance(placement, dict):
            continue
        asset_id = str(placement.get("asset_id", "asset"))
        footprint = placement.get("expected_footprint", [])
        anchor = placement.get("anchor_point", [])
        parts.append(svg_polygon(footprint, "placement", f"placement: {asset_id}"))
        parts.append(svg_circle(anchor, 7, "anchor", f"anchor: {asset_id}"))
        x, y = centroid(footprint)
        parts.append(svg_text(x - 52, y + 18, asset_id, "small"))

    for door in as_list(layout.get("doors")):
        if not isinstance(door, dict):
            continue
        door_id = str(door.get("door_id", "door"))
        position = door.get("position", [])
        parts.append(svg_circle(position, 6, "door", f"door: {door_id}"))
        if isinstance(position, list) and len(position) >= 2:
            parts.append(svg_text(float(position[0]) + 8, float(position[1]) - 8, door_id, "small"))

    for hotspot in as_list(layout.get("hotspot_access")):
        if not isinstance(hotspot, dict):
            continue
        hotspot_id = str(hotspot.get("hotspot_id", "hotspot"))
        matching = [placement for placement in as_list(plan.get("placements")) if isinstance(placement, dict) and placement.get("hotspot_id") == hotspot_id]
        for placement in matching:
            anchor = placement.get("anchor_point", [])
            parts.append(svg_circle(anchor, 11, "hotspot", f"hotspot: {hotspot_id}"))

    parts.append("</svg>")
    return "\n".join(parts)


def export_preview(plan_path: Path, output_root: Path) -> Path:
    plan = load_json(plan_path)
    area_id = str(plan.get("area_id", "unknown_area"))
    batch_id = str(plan.get("batch_id", "unknown_batch"))
    layout_path = ROOT / "areas" / area_id / "layout_constraints.json"
    layout = load_json(layout_path)

    output_root.mkdir(parents=True, exist_ok=True)
    output_path = output_root / f"{area_id}_{batch_id}.svg"
    output_path.write_text(build_svg(plan, layout), encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export an SVG asset placement preview.")
    parser.add_argument("placement_plan", type=Path, help="Path to asset placement plan JSON.")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT, help="Output root directory.")
    args = parser.parse_args()

    plan_path = args.placement_plan
    if not plan_path.is_absolute():
        plan_path = ROOT / plan_path
    output_root = args.output_root
    if not output_root.is_absolute():
        output_root = ROOT / output_root

    output_path = export_preview(plan_path, output_root)
    print(output_path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
