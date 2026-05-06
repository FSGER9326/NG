#!/usr/bin/env python3
"""Validate Issue 13 text-first portrait selection runtime prerequisites.

Issue #13 is implemented in the active runtime extension
``game/scripts/core/main_runtime_v3.gd``. Older runtime paths remain as stable
shims so scenes, docs, and tooling can keep using the same entrypoint.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_MAIN_PATH = ROOT / "game" / "scripts" / "core" / "main.gd"
RUNTIME_SHIM_PATH = ROOT / "game" / "scripts" / "core" / "main_runtime.gd"
RUNTIME_V2_PATH = ROOT / "game" / "scripts" / "core" / "main_runtime_v2.gd"
PORTRAIT_RUNTIME_PATH = ROOT / "game" / "scripts" / "core" / "main_runtime_v3.gd"
MAIN_SCENE_PATH = ROOT / "game" / "scenes" / "main.tscn"
PORTRAIT_CATALOG_PATH = ROOT / "game" / "scripts" / "character" / "portrait_catalog.gd"
PORTRAIT_DATA_PATH = ROOT / "data" / "character_creation" / "portraits.json"
SCENARIO_PATH = ROOT / "tests" / "scenarios" / "character_creator_portrait_selection.json"

RUNTIME_V2_REQUIRED_SNIPPETS = {
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

PORTRAIT_RUNTIME_REQUIRED_SNIPPETS = {
    "const PortraitCatalog",
    "const PORTRAITS_PATH",
    "portrait_options",
    "portrait_summary_label",
    "portrait_data",
    "func _populate_portrait_options",
    "func _select_portrait_for_current_background",
    "func _get_selected_portrait",
    "func _update_portrait_summary",
    "select_portrait",
    "portrait_id",
}

SCENARIO_REQUIRED_SNIPPETS = {
    "character_creator_portrait_selection",
    "select_portrait",
    "Weathered Drifter",
    "portrait_weathered_drifter_01",
}


def main() -> int:
    errors: list[str] = []

    for path in [
        LEGACY_MAIN_PATH,
        RUNTIME_SHIM_PATH,
        RUNTIME_V2_PATH,
        PORTRAIT_RUNTIME_PATH,
        MAIN_SCENE_PATH,
        PORTRAIT_CATALOG_PATH,
        PORTRAIT_DATA_PATH,
        SCENARIO_PATH,
    ]:
        _require_file(path, errors)

    if errors:
        return _fail(errors)

    legacy_content = LEGACY_MAIN_PATH.read_text(encoding="utf-8")
    runtime_shim_content = RUNTIME_SHIM_PATH.read_text(encoding="utf-8")
    runtime_v2_content = RUNTIME_V2_PATH.read_text(encoding="utf-8")
    portrait_runtime_content = PORTRAIT_RUNTIME_PATH.read_text(encoding="utf-8")
    scene_content = MAIN_SCENE_PATH.read_text(encoding="utf-8")
    scenario_content = SCENARIO_PATH.read_text(encoding="utf-8")

    expected_legacy_shim = 'extends "res://game/scripts/core/main_runtime.gd"'
    if expected_legacy_shim not in legacy_content:
        errors.append("legacy main.gd should be a parse-safe shim extending main_runtime.gd")
    if "var class_name" in legacy_content or "func _build_player_profile" in legacy_content:
        errors.append("legacy main.gd must not contain the old full runtime body or reserved class_name local")

    expected_runtime_shim = 'extends preload("res://game/scripts/core/main_runtime_v3.gd")'
    if expected_runtime_shim not in runtime_shim_content:
        errors.append("main_runtime.gd should extend the active portrait runtime v3 with preload-based inheritance")
    if 'extends "res://game/scripts/core/main_runtime_v3.gd"' in runtime_shim_content:
        errors.append("main_runtime.gd must not use quoted-path inheritance for runtime v3")

    expected_portrait_runtime_base = 'extends preload("res://game/scripts/core/main_runtime_v2.gd")'
    if expected_portrait_runtime_base not in portrait_runtime_content:
        errors.append("main_runtime_v3.gd should extend main_runtime_v2.gd with preload-based inheritance")
    if 'extends "res://game/scripts/core/main_runtime_v2.gd"' in portrait_runtime_content:
        errors.append("main_runtime_v3.gd must not use quoted-path inheritance for runtime v2")

    if "res://game/scripts/core/main_runtime.gd" not in scene_content:
        errors.append("main.tscn should keep pointing at the stable main_runtime.gd shim")

    for snippet in sorted(RUNTIME_V2_REQUIRED_SNIPPETS):
        if snippet not in runtime_v2_content:
            errors.append(f"main_runtime_v2.gd missing runtime prerequisite: {snippet}")

    for snippet in sorted(PORTRAIT_RUNTIME_REQUIRED_SNIPPETS):
        if snippet not in portrait_runtime_content:
            errors.append(f"main_runtime_v3.gd missing portrait selection prerequisite: {snippet}")

    for snippet in sorted(SCENARIO_REQUIRED_SNIPPETS):
        if snippet not in scenario_content:
            errors.append(f"portrait selection scenario missing expected snippet: {snippet}")

    if "var class_name" in runtime_v2_content or "var class_name" in portrait_runtime_content:
        errors.append("runtime scripts must not contain a parse-breaking var class_name local")
    if "var trait :=" in runtime_v2_content or "for trait in" in runtime_v2_content:
        errors.append("main_runtime_v2.gd still contains a parse-breaking trait local/loop identifier")
    if "var trait :=" in portrait_runtime_content or "for trait in" in portrait_runtime_content:
        errors.append("main_runtime_v3.gd must not contain a parse-breaking trait local/loop identifier")

    if errors:
        return _fail(errors)

    print("Issue 13 validation passed: text-first portrait selection runtime and scenario are present.")
    return 0


def _require_file(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing expected file: {path.relative_to(ROOT)}")


def _fail(errors: list[str]) -> int:
    print("Issue 13 portrait selection validation failed:")
    for error in errors:
        print(f"  - {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
