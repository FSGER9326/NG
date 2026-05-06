#!/usr/bin/env python3
"""Catalog external reference asset folders for quality-bar use.

This tool does not copy or transform assets. It records file paths, PNG dimensions,
and coarse categories so art agents can quickly find reference examples without
browsing hundreds of files manually.
"""

from __future__ import annotations

import argparse
import json
import struct
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

CATEGORY_USE = {
    "animated_light_sources": "Animation strip timing, glow readability, and flame/light effect style.",
    "architectural_adorns": "Readable architectural ornament density without muddy silhouettes.",
    "archways": "Portal/threshold construction, negative space, and modular facade framing.",
    "buttresses": "Support-piece proportions, grounding, and shadow logic.",
    "columns": "Vertical structure readability, material banding, and repeated modular variants.",
    "columns_pillars": "Standalone vertical silhouette, base/capital definition, and prop scale.",
    "decor_props": "Small prop readability, thematic accents, and detail density.",
    "floor_ground_tiles": "Ground material texture and tile seam discipline.",
    "floor_tiles": "Interior/structure tile alignment and repeatable pattern treatment.",
    "misc_root_tiles": "General kit breadth: set dressing, environment pieces, decals, and props.",
    "pillars": "Large support silhouette, occlusion potential, and scale contrast.",
    "ramps": "Readable elevation transitions and slope direction clarity.",
    "rocks_stone": "Organic stone silhouettes, material texture, and variant shape language.",
    "stairs": "Step direction readability, elevation clarity, and path affordance.",
    "walls": "Wall modularity, facade depth, shadow side consistency, and corner joins.",
    "walls_and_edges": "Boundary decoration, wall-mounted detail, and readable side-facing assets.",
}


def png_info(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if data[:8] != PNG_SIGNATURE or data[12:16] != b"IHDR":
        raise ValueError(f"Not a readable PNG IHDR: {path}")
    width, height = struct.unpack(">II", data[16:24])
    bit_depth = data[24]
    color_type = data[25]
    return {
        "width": width,
        "height": height,
        "bit_depth": bit_depth,
        "color_type": color_type,
        "rgba_png": color_type == 6,
        "size_bytes": path.stat().st_size,
    }


def classify(path: Path) -> str:
    stem = path.stem.lower()
    folder = path.parent.as_posix().lower()
    if stem.startswith("anim_"):
        return "animated_light_sources"
    if "building_infernus" in folder:
        first = path.stem.split("_")[0].lower()
        return {
            "adorn": "architectural_adorns",
            "archway": "archways",
            "buttress": "buttresses",
            "column": "columns",
            "floor": "floor_tiles",
            "pillar": "pillars",
            "ramp": "ramps",
            "stairs": "stairs",
            "wall": "walls",
        }.get(first, "building_parts")

    name = stem.replace("infernus_", "")
    if "wall" in name:
        return "walls_and_edges"
    if any(token in name for token in ["floor", "ground", "tile", "road"]):
        return "floor_ground_tiles"
    if any(token in name for token in ["lava", "magma", "fire"]):
        return "lava_fire_fx"
    if any(token in name for token in ["rock", "stone", "boulder"]):
        return "rocks_stone"
    if "stairs" in name:
        return "stairs"
    if "ramp" in name:
        return "ramps"
    if "bridge" in name:
        return "bridges"
    if "pillar" in name or "column" in name:
        return "columns_pillars"
    if "arch" in name:
        return "archways"
    if "door" in name or "gate" in name:
        return "doors_gates"
    if any(token in name for token in ["decor", "adorn", "statue", "skull", "bone"]):
        return "decor_props"
    return "misc_root_tiles"


def build_catalog(root: Path, source_pack: str) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.png")):
        rel = path.relative_to(root).as_posix()
        info = png_info(path)
        category = classify(path.relative_to(root))
        records.append({
            "path": rel,
            "category": category,
            **info,
            "reference_only": True,
        })

    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_category[record["category"]].append(record)

    category_summary = []
    for category, items in sorted(by_category.items(), key=lambda item: (-len(item[1]), item[0])):
        dims = Counter(f"{item['width']}x{item['height']}" for item in items)
        category_summary.append({
            "category": category,
            "count": len(items),
            "reference_use": CATEGORY_USE.get(category, "Reference quality comparison."),
            "common_dimensions": [
                {"size": size, "count": count}
                for size, count in dims.most_common(8)
            ],
            "examples": [item["path"] for item in items[:12]],
        })

    return {
        "version": 1,
        "source_pack": source_pack,
        "root": root.as_posix(),
        "total_png_files": len(records),
        "all_pngs_are_rgba": all(record["rgba_png"] for record in records),
        "total_size_bytes": sum(record["size_bytes"] for record in records),
        "category_summary": category_summary,
        "quality_dimensions_to_compare": [
            "silhouette_readability",
            "isometric_alignment",
            "modular_join_consistency",
            "material_rendering",
            "lighting_direction",
            "shadow_contact",
            "edge_alpha_cleanliness",
            "variant_family_cohesion",
            "gameplay_scale_readability",
        ],
        "entries": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Catalog reference PNG assets")
    parser.add_argument("root", type=Path, help="Reference asset root to scan")
    parser.add_argument("--source-pack", default="external_reference_pack", help="Human-readable source pack name")
    parser.add_argument("--out", type=Path, default=Path("debug/reference_asset_catalog.json"), help="Output JSON file")
    args = parser.parse_args()

    if not args.root.exists():
        raise SystemExit(f"Reference root does not exist: {args.root}")

    catalog = build_catalog(args.root, args.source_pack)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {catalog['total_png_files']} PNG records to {args.out}")


if __name__ == "__main__":
    main()
