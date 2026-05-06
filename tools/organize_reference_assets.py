#!/usr/bin/env python3
"""Organize external reference PNG assets into a single category folder.

This is intended for local/private reference packs. It does not transform image
content. It only copies or moves files into predictable category folders and
writes an index JSON that art agents can use for reference lookup.
"""

from __future__ import annotations

import argparse
import json
import shutil
import struct
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

DEFAULT_DEST = Path("reference_assets/organized/pvgames/infernus_free")

CATEGORY_USE = {
    "animated_light_sources": "Animation strip timing, glow readability, and flame/light effect style.",
    "architectural_adorns": "Readable architectural ornament density without muddy silhouettes.",
    "archways": "Portal/threshold construction, negative space, and modular facade framing.",
    "bridges": "Walkable connector silhouettes and modular path joins.",
    "building_parts": "Architectural pieces that need manual category review.",
    "buttresses": "Support-piece proportions, grounding, and shadow logic.",
    "columns": "Vertical structure readability, material banding, and repeated modular variants.",
    "columns_pillars": "Standalone vertical silhouette, base/capital definition, and prop scale.",
    "decor_props": "Small prop readability, thematic accents, and detail density.",
    "doors_gates": "Walkable entrance readability and threshold framing.",
    "floor_ground_tiles": "Ground material texture and tile seam discipline.",
    "floor_tiles": "Interior/structure tile alignment and repeatable pattern treatment.",
    "lava_fire_fx": "Effect readability and glow/color restraint.",
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
    return {
        "width": width,
        "height": height,
        "bit_depth": data[24],
        "color_type": data[25],
        "rgba_png": data[25] == 6,
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


def unique_dest(dest_dir: Path, source: Path) -> Path:
    candidate = dest_dir / source.name
    if not candidate.exists():
        return candidate
    stem = source.stem
    suffix = source.suffix
    index = 2
    while True:
        candidate = dest_dir / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def build_summary(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        grouped[entry["category"]].append(entry)

    summary = []
    for category, items in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        dims = Counter(f"{item['width']}x{item['height']}" for item in items)
        summary.append({
            "category": category,
            "count": len(items),
            "reference_use": CATEGORY_USE.get(category, "Reference quality comparison."),
            "common_dimensions": [
                {"size": size, "count": count}
                for size, count in dims.most_common(8)
            ],
            "examples": [item["organized_path"] for item in items[:12]],
        })
    return summary


def organize(source_root: Path, dest_root: Path, mode: str, dry_run: bool) -> dict[str, Any]:
    source_root = source_root.resolve()
    dest_root = dest_root.resolve()
    entries: list[dict[str, Any]] = []

    for source in sorted(source_root.rglob("*.png")):
        if dest_root in source.resolve().parents:
            continue
        rel_source = source.relative_to(source_root).as_posix()
        info = png_info(source)
        category = classify(source.relative_to(source_root))
        category_dir = dest_root / category
        dest = unique_dest(category_dir, source)

        entries.append({
            "source_path": rel_source,
            "organized_path": dest.relative_to(dest_root).as_posix(),
            "category": category,
            **info,
            "reference_only": True,
        })

        if not dry_run:
            category_dir.mkdir(parents=True, exist_ok=True)
            if mode == "move":
                shutil.move(str(source), str(dest))
            else:
                shutil.copy2(source, dest)

    return {
        "version": 1,
        "source_root": source_root.as_posix(),
        "organized_root": dest_root.as_posix(),
        "mode": mode,
        "dry_run": dry_run,
        "total_png_files": len(entries),
        "all_pngs_are_rgba": all(entry["rgba_png"] for entry in entries),
        "total_size_bytes": sum(entry["size_bytes"] for entry in entries),
        "category_summary": build_summary(entries),
        "entries": entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize reference PNG assets by category")
    parser.add_argument("source", type=Path, help="Folder containing reference PNGs")
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST, help="Canonical organized reference folder")
    parser.add_argument("--mode", choices=["copy", "move"], default="copy", help="Copy or move files into organized folders")
    parser.add_argument("--dry-run", action="store_true", help="Write index only; do not copy/move files")
    parser.add_argument("--index", type=Path, default=None, help="Output index path; defaults to <dest>/reference_index.json")
    args = parser.parse_args()

    if not args.source.exists():
        raise SystemExit(f"Source folder does not exist: {args.source}")

    index_path = args.index or args.dest / "reference_index.json"
    catalog = organize(args.source, args.dest, args.mode, args.dry_run)
    if not args.dry_run:
        args.dest.mkdir(parents=True, exist_ok=True)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")

    print(f"Organized/categorized {catalog['total_png_files']} PNG files")
    print(f"Index: {index_path}")
    print(f"Destination: {args.dest}")


if __name__ == "__main__":
    main()
