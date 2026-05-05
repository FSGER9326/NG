#!/usr/bin/env python3
"""Validate small GDScript helper contracts used by text-first systems."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTRAIT_CATALOG_PATH = ROOT / "game" / "scripts" / "character" / "portrait_catalog.gd"

REQUIRED_PORTRAIT_CATALOG_SNIPPETS = {
    "class_name PortraitCatalog",
    "static func get_portraits",
    "static func find_by_id",
    "static func find_by_name",
    "static func get_default_portrait",
    "static func get_display_name",
    "static func get_summary",
    "static func apply_to_profile",
    "portrait_id",
    "portrait",
}


def main() -> int:
    errors: list[str] = []
    if not PORTRAIT_CATALOG_PATH.exists():
        print(f"Missing GDScript helper: {PORTRAIT_CATALOG_PATH.relative_to(ROOT)}")
        return 1

    content = PORTRAIT_CATALOG_PATH.read_text(encoding="utf-8")
    for snippet in sorted(REQUIRED_PORTRAIT_CATALOG_SNIPPETS):
        if snippet not in content:
            errors.append(f"portrait_catalog.gd missing expected contract snippet: {snippet}")

    if errors:
        print("NG GDScript helper validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("NG GDScript helper validation passed: PortraitCatalog contract present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
