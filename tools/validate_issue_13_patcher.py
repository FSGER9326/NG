#!/usr/bin/env python3
"""Validate Issue 13 portrait patcher prerequisites.

The active game runtime is now split so old Godot parser-sensitive files can
remain as stable compatibility shims while the parse-safe implementation lives
in ``game/scripts/core/main_runtime_v2.gd``.

This validator protects that layout instead of requiring the old full runtime
body to remain at the legacy ``main.gd`` or ``main_runtime.gd`` paths.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCHER_PATH = ROOT / "tools" / "apply_issue_13_portrait_selection_patch.py"
LEGACY_MAIN_PATH = ROOT / "game" / "scripts" / "core" / "main.gd"
RUNTIME_SHIM_PATH = ROOT / "game" / "scripts" / "core" / "main_runtime.gd"
RUNTIME_MAIN_PATH = ROOT / "game" / "scripts" / "core" / "main_runtime_v2.gd"
MAIN_SCENE_PATH = ROOT / "game" / "scenes" / "main.tscn"
PORTRAIT_CATALOG_PATH = ROOT / "game" / "scripts" / "character" / "portrait_catalog.gd"
PORTRAIT_DATA_PATH = ROOT / "data" / "character_creation" / "portraits.json"

RUNTIME_REQUIRED_SNIPPETS = {
    "const CharacterProfileBuilder",
    "func _show_character_creator",
    "func _start_new_game_from_creator",
    "func _build_player_profile",
    "func _start_game",
    "character_creation_data",
    "player_profile",
    "archetype_options",
    "trait_options",
}

PATCHER_REQUIRED_SNIPPETS = {
    "portrait",
    "PortraitCatalog",
    "character_creation",
    "main.gd",
}


def main() -> int:
    errors: list[str] = []

    _require_file(PATCHER_PATH, errors)
    _require_file(LEGACY_MAIN_PATH, errors)
    _require_file(RUNTIME_SHIM_PATH, errors)
    _require_file(RUNTIME_MAIN_PATH, errors)
    _require_file(MAIN_SCENE_PATH, errors)
    _require_file(PORTRAIT_CATALOG_PATH, errors)
    _require_file(PORTRAIT_DATA_PATH, errors)

    if errors:
        return _fail(errors)

    legacy_content = LEGACY_MAIN_PATH.read_text(encoding="utf-8")
    runtime_shim_content = RUNTIME_SHIM_PATH.read_text(encoding="utf-8")
    runtime_content = RUNTIME_MAIN_PATH.read_text(encoding="utf-8")
    scene_content = MAIN_SCENE_PATH.read_text(encoding="utf-8")
    patcher_content = PATCHER_PATH.read_text(encoding="utf-8")

    expected_legacy_shim = 'extends "res://game/scripts/core/main_runtime.gd"'
    if expected_legacy_shim not in legacy_content:
        errors.append("legacy main.gd should be a parse-safe shim extending main_runtime.gd")
    if "var class_name" in legacy_content or "func _build_player_profile" in legacy_content:
        errors.append("legacy main.gd must not contain the old full runtime body or reserved class_name local")

    expected_runtime_shim = 'extends "res://game/scripts/core/main_runtime_v2.gd"'
    if expected_runtime_shim not in runtime_shim_content:
        errors.append("main_runtime.gd should be a parse-safe shim extending main_runtime_v2.gd")
    if "var trait" in runtime_shim_content or "func _build_player_profile" in runtime_shim_content:
        errors.append("main_runtime.gd must not contain the old full runtime body or reserved trait local")

    if "res://game/scripts/core/main_runtime.gd" not in scene_content:
        errors.append("main.tscn should keep pointing at the stable main_runtime.gd shim")

    for snippet in sorted(RUNTIME_REQUIRED_SNIPPETS):
        if snippet not in runtime_content:
            errors.append(f"main_runtime_v2.gd missing Issue 13 runtime prerequisite: {snippet}")

    for snippet in sorted(PATCHER_REQUIRED_SNIPPETS):
        if snippet not in patcher_content:
            errors.append(f"Issue 13 portrait patcher missing expected snippet: {snippet}")

    if "var class_name" in runtime_content:
        errors.append("main_runtime_v2.gd still contains a parse-breaking var class_name local")
    if "var trait :=" in runtime_content or "for trait in" in runtime_content:
        errors.append("main_runtime_v2.gd still contains a parse-breaking trait local/loop identifier")

    if errors:
        return _fail(errors)

    print("Issue 13 patcher validation passed: runtime v2 layout and portrait patch prerequisites are present.")
    return 0


def _require_file(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing expected file: {path.relative_to(ROOT)}")


def _fail(errors: list[str]) -> int:
    print("Issue 13 patcher validation failed:")
    for error in errors:
        print(f"  - {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
