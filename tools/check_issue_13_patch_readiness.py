#!/usr/bin/env python3
"""Preflight check for the Issue #13 portrait selector patcher.

This script does not modify files. It checks whether the local checkout appears
ready for `tools/apply_issue_13_portrait_selection_patch.py`, and it fails fast
on obvious drift or partial application.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_GD = ROOT / "game" / "scripts" / "core" / "main.gd"
PATCHER = ROOT / "tools" / "apply_issue_13_portrait_selection_patch.py"
SCENARIO_PATH = ROOT / "tests" / "scenarios" / "character_creator_portrait_selection.json"

REQUIRED_FILES = [
    ROOT / "data" / "character_creation" / "portraits.json",
    ROOT / "game" / "scripts" / "character" / "portrait_catalog.gd",
    ROOT / "tools" / "validate_project.py",
    ROOT / "tools" / "validate_character_creation.py",
    ROOT / "tools" / "validate_portraits.py",
]

UNPATCHED_MARKERS = {
    "portrait preload insertion point": "const CharacterProfileBuilder = preload(\"res://game/scripts/character/character_profile_builder.gd\")\n\nconst CHARACTER_CREATION_PATH := \"res://data/character_creation/character_creation.json\"\n",
    "creator variable insertion point": "var archetype_options: OptionButton\nvar trait_options: OptionButton\nvar compatibility_warning_label: Label\nvar start_journey_button: Button\nvar character_creation_data: Dictionary = {}\n",
    "portrait data load insertion point": "\tcharacter_creation_data = data_loader.load_json_file(CHARACTER_CREATION_PATH)\n\tGameLog.info(\"BOOT\", \"Loaded bootstrap data\", {\"keys\": load_result.keys(), \"has_character_creation\": not character_creation_data.is_empty()})\n",
    "trait row insertion point": "\troot.add_child(_make_form_label(\"Trait\"))\n\ttrait_options = OptionButton.new()\n\ttrait_options.name = \"TraitOptions\"\n\t_populate_option_button(trait_options, character_creation_data.get(\"traits\", []), [\"Steady Under Fire\"])\n\t_select_option_by_text(trait_options, String(player_profile.get(\"trait\", \"Steady Under Fire\")), \"trait\")\n\ttrait_options.item_selected.connect(_on_creator_selection_changed)\n\troot.add_child(trait_options)\n\n\tcompatibility_warning_label = Label.new()\n",
    "start journey bind insertion point": "\tstart_journey_button.pressed.connect(_start_new_game_from_creator.bind(character_name_edit, ancestry_options, origin_options, archetype_options, trait_options))\n\tbuttons.add_child(start_journey_button)\n\t_refresh_trait_options(String(player_profile.get(\"trait\", \"Steady Under Fire\")))\n\t_update_creator_compatibility()\n",
    "start journey signature insertion point": "func _start_new_game_from_creator(name_edit: LineEdit, selected_ancestry_options: OptionButton, selected_origin_options: OptionButton, selected_archetype_options: OptionButton, selected_trait_options: OptionButton) -> void:\n",
    "profile portrait application insertion point": "\tvar built_profile := _build_player_profile(character_name, ancestry_name, background_name, class_name, trait_name)\n\tvar warnings: Array = built_profile.get(\"compatibility_warnings\", [])\n",
    "portrait signal insertion point": "func _on_creator_selection_changed(_selected_index: int = -1) -> void:\n\t_refresh_trait_options(_get_selected_option_text(trait_options))\n\t_update_creator_compatibility(_selected_index)\n\nfunc _refresh_trait_options",
    "debug start journey insertion point": "\t\t\tif button == \"start_journey\":\n\t\t\t\tif character_name_edit == null or ancestry_options == null or origin_options == null or archetype_options == null or trait_options == null:\n\t\t\t\t\tGameLog.error(\"ASSERT\", \"Cannot start journey; character creator controls are missing\")\n\t\t\t\t\treturn false\n\t\t\t\t_start_new_game_from_creator(character_name_edit, ancestry_options, origin_options, archetype_options, trait_options)\n",
    "debug select portrait insertion point": "\t\t\"select_trait\":\n\t\t\tvar trait_ok := _select_option_by_text(trait_options, String(action.get(\"trait\", \"\")), \"trait\")\n\t\t\t_update_creator_compatibility()\n\t\t\treturn trait_ok\n\t\t\"assert_trait_available\":\n",
    "profile assertion insertion point": "func _assert_player_profile(action: Dictionary) -> bool:\n\tfor key in [\"name\", \"ancestry\", \"origin\", \"archetype\", \"background\", \"class\", \"trait\"]:\n",
    "clear portrait controls insertion point": "\ttrait_options = null\n\tcompatibility_warning_label = null\n\tstart_journey_button = null\n",
}

PATCHED_MARKERS = [
    "PortraitCatalog",
    "PORTRAITS_PATH",
    "portrait_options",
    "portrait_summary_label",
    "select_portrait",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def has_any_patch_marker(content: str) -> bool:
    return any(marker in content for marker in PATCHED_MARKERS)


def has_all_patch_markers(content: str) -> bool:
    return all(marker in content for marker in PATCHED_MARKERS)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for path in [MAIN_GD, PATCHER, *REQUIRED_FILES]:
        if not path.exists():
            errors.append(f"Missing required file: {rel(path)}")

    if errors:
        print("Issue #13 patcher preflight failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    content = MAIN_GD.read_text(encoding="utf-8")

    if has_all_patch_markers(content):
        if SCENARIO_PATH.exists():
            print("Issue #13 portrait selector appears to be already applied.")
            print(f"Scenario present: {rel(SCENARIO_PATH)}")
            return 0
        print("Issue #13 portrait selector appears partially applied: runtime markers exist but scenario is missing.")
        return 1

    if has_any_patch_marker(content):
        print("Issue #13 portrait selector appears partially applied. Inspect main.gd before running the patcher.")
        return 1

    for label, marker in UNPATCHED_MARKERS.items():
        count = content.count(marker)
        if count != 1:
            errors.append(f"{label}: expected 1 match, found {count}")

    if SCENARIO_PATH.exists():
        warnings.append(f"Scenario already exists before runtime patch: {rel(SCENARIO_PATH)}")

    if errors:
        print("Issue #13 patcher preflight failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Issue #13 patcher preflight passed.")
    print("Safe next command:")
    print("  python tools/apply_issue_13_portrait_selection_patch.py")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
