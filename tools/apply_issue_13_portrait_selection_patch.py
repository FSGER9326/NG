#!/usr/bin/env python3
"""Apply the Issue #13 text-first portrait selector patch.

This is a local safety patcher for `game/scripts/core/main.gd`. The GitHub
connector can require full-file replacement for this large script, so this tool
uses exact context replacements and stops if the current file shape has drifted.

Run from repo root:

    python tools/apply_issue_13_portrait_selection_patch.py

Then review the diff, run validators/scenarios, and open a focused PR.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_GD = ROOT / "game" / "scripts" / "core" / "main.gd"
SCENARIO_PATH = ROOT / "tests" / "scenarios" / "character_creator_portrait_selection.json"

PORTRAIT_SELECTION_SCENARIO = """{
  "id": "character_creator_portrait_selection",
  "name": "Character Creator Portrait Selection",
  "root_scene": "main",
  "description": "Verifies that the text-first portrait selector can choose portrait metadata and persist the selected portrait into the player profile when starting the game.",
  "steps": [
    {
      "type": "assert_screen",
      "screen": "main_menu"
    },
    {
      "type": "press_menu",
      "button": "new_game"
    },
    {
      "type": "assert_screen",
      "screen": "character_creator"
    },
    {
      "type": "set_character_name",
      "name": "Portrait Tester"
    },
    {
      "type": "select_ancestry",
      "ancestry": "Border Human"
    },
    {
      "type": "select_origin",
      "origin": "Caravan Guard"
    },
    {
      "type": "select_archetype",
      "archetype": "Scout"
    },
    {
      "type": "select_trait",
      "trait": "Quick-Eyed"
    },
    {
      "type": "select_portrait",
      "portrait": "Caravan Guard"
    },
    {
      "type": "press_menu",
      "button": "start_journey"
    },
    {
      "type": "assert_screen",
      "screen": "game"
    },
    {
      "type": "assert_area",
      "area_id": "wolfpine_road"
    },
    {
      "type": "assert_player_profile",
      "name": "Portrait Tester",
      "background": "Caravan Guard",
      "class": "Scout",
      "trait": "Quick-Eyed",
      "portrait": "Caravan Guard",
      "portrait_id": "portrait_caravan_guard_01"
    },
    {
      "type": "assert_player_profile",
      "tag": "background.caravan_guard"
    }
  ]
}
"""


def replace_once(content: str, before: str, after: str, label: str) -> str:
    count = content.count(before)
    if count != 1:
        raise SystemExit(f"Refusing to patch {label}: expected 1 match, found {count}.")
    return content.replace(before, after, 1)


def write_portrait_selection_scenario() -> None:
    if SCENARIO_PATH.exists():
        existing = SCENARIO_PATH.read_text(encoding="utf-8")
        if existing == PORTRAIT_SELECTION_SCENARIO:
            print(f"Scenario already present: {SCENARIO_PATH.relative_to(ROOT)}")
            return
        raise SystemExit(f"Refusing to overwrite existing scenario: {SCENARIO_PATH.relative_to(ROOT)}")
    SCENARIO_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCENARIO_PATH.write_text(PORTRAIT_SELECTION_SCENARIO, encoding="utf-8")
    print(f"Created scenario: {SCENARIO_PATH.relative_to(ROOT)}")


def main() -> int:
    content = MAIN_GD.read_text(encoding="utf-8")
    if "PortraitCatalog" in content or "portrait_options" in content:
        raise SystemExit("Issue #13 portrait selector appears to be already applied.")

    content = replace_once(
        content,
        "const CharacterProfileBuilder = preload(\"res://game/scripts/character/character_profile_builder.gd\")\n\nconst CHARACTER_CREATION_PATH := \"res://data/character_creation/character_creation.json\"\n",
        "const CharacterProfileBuilder = preload(\"res://game/scripts/character/character_profile_builder.gd\")\nconst PortraitCatalog = preload(\"res://game/scripts/character/portrait_catalog.gd\")\n\nconst CHARACTER_CREATION_PATH := \"res://data/character_creation/character_creation.json\"\nconst PORTRAITS_PATH := \"res://data/character_creation/portraits.json\"\n",
        "preloads and paths",
    )

    content = replace_once(
        content,
        "var archetype_options: OptionButton\nvar trait_options: OptionButton\nvar compatibility_warning_label: Label\nvar start_journey_button: Button\nvar character_creation_data: Dictionary = {}\n",
        "var archetype_options: OptionButton\nvar trait_options: OptionButton\nvar portrait_options: OptionButton\nvar portrait_summary_label: Label\nvar compatibility_warning_label: Label\nvar start_journey_button: Button\nvar character_creation_data: Dictionary = {}\nvar portrait_data: Dictionary = {}\n",
        "creator variables",
    )

    content = replace_once(
        content,
        "\tcharacter_creation_data = data_loader.load_json_file(CHARACTER_CREATION_PATH)\n\tGameLog.info(\"BOOT\", \"Loaded bootstrap data\", {\"keys\": load_result.keys(), \"has_character_creation\": not character_creation_data.is_empty()})\n",
        "\tcharacter_creation_data = data_loader.load_json_file(CHARACTER_CREATION_PATH)\n\tportrait_data = data_loader.load_json_file(PORTRAITS_PATH)\n\tGameLog.info(\"BOOT\", \"Loaded bootstrap data\", {\"keys\": load_result.keys(), \"has_character_creation\": not character_creation_data.is_empty(), \"has_portraits\": not portrait_data.is_empty()})\n",
        "portrait data load",
    )

    content = replace_once(
        content,
        "\troot.add_child(_make_form_label(\"Trait\"))\n\ttrait_options = OptionButton.new()\n\ttrait_options.name = \"TraitOptions\"\n\t_populate_option_button(trait_options, character_creation_data.get(\"traits\", []), [\"Steady Under Fire\"])\n\t_select_option_by_text(trait_options, String(player_profile.get(\"trait\", \"Steady Under Fire\")), \"trait\")\n\ttrait_options.item_selected.connect(_on_creator_selection_changed)\n\troot.add_child(trait_options)\n\n\tcompatibility_warning_label = Label.new()\n",
        "\troot.add_child(_make_form_label(\"Trait\"))\n\ttrait_options = OptionButton.new()\n\ttrait_options.name = \"TraitOptions\"\n\t_populate_option_button(trait_options, character_creation_data.get(\"traits\", []), [\"Steady Under Fire\"])\n\t_select_option_by_text(trait_options, String(player_profile.get(\"trait\", \"Steady Under Fire\")), \"trait\")\n\ttrait_options.item_selected.connect(_on_creator_selection_changed)\n\troot.add_child(trait_options)\n\n\troot.add_child(_make_form_label(\"Portrait\"))\n\tportrait_options = OptionButton.new()\n\tportrait_options.name = \"PortraitOptions\"\n\t_populate_portrait_options()\n\t_select_portrait_by_name(String(player_profile.get(\"portrait\", \"\")))\n\tportrait_options.item_selected.connect(_on_portrait_selection_changed)\n\troot.add_child(portrait_options)\n\n\tportrait_summary_label = Label.new()\n\tportrait_summary_label.name = \"PortraitSummary\"\n\tportrait_summary_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART\n\tportrait_summary_label.custom_minimum_size = Vector2(620, 48)\n\tCrpgTheme.apply_label(portrait_summary_label)\n\troot.add_child(portrait_summary_label)\n\n\tcompatibility_warning_label = Label.new()\n",
        "portrait controls",
    )

    content = replace_once(
        content,
        "\tstart_journey_button.pressed.connect(_start_new_game_from_creator.bind(character_name_edit, ancestry_options, origin_options, archetype_options, trait_options))\n\tbuttons.add_child(start_journey_button)\n\t_refresh_trait_options(String(player_profile.get(\"trait\", \"Steady Under Fire\")))\n\t_update_creator_compatibility()\n",
        "\tstart_journey_button.pressed.connect(_start_new_game_from_creator.bind(character_name_edit, ancestry_options, origin_options, archetype_options, trait_options, portrait_options))\n\tbuttons.add_child(start_journey_button)\n\t_refresh_trait_options(String(player_profile.get(\"trait\", \"Steady Under Fire\")))\n\t_update_portrait_summary()\n\t_update_creator_compatibility()\n",
        "start journey bind",
    )

    content = replace_once(
        content,
        "func _start_new_game_from_creator(name_edit: LineEdit, selected_ancestry_options: OptionButton, selected_origin_options: OptionButton, selected_archetype_options: OptionButton, selected_trait_options: OptionButton) -> void:\n",
        "func _start_new_game_from_creator(name_edit: LineEdit, selected_ancestry_options: OptionButton, selected_origin_options: OptionButton, selected_archetype_options: OptionButton, selected_trait_options: OptionButton, selected_portrait_options: OptionButton) -> void:\n",
        "start journey signature",
    )

    content = replace_once(
        content,
        "\tvar built_profile := _build_player_profile(character_name, ancestry_name, background_name, class_name, trait_name)\n\tvar warnings: Array = built_profile.get(\"compatibility_warnings\", [])\n",
        "\tvar built_profile := _build_player_profile(character_name, ancestry_name, background_name, class_name, trait_name)\n\tif selected_portrait_options != null and selected_portrait_options.get_item_count() > 0:\n\t\tbuilt_profile = PortraitCatalog.apply_to_profile(built_profile, _get_selected_portrait())\n\tvar warnings: Array = built_profile.get(\"compatibility_warnings\", [])\n",
        "profile portrait application",
    )

    content = replace_once(
        content,
        "func _on_creator_selection_changed(_selected_index: int = -1) -> void:\n\t_refresh_trait_options(_get_selected_option_text(trait_options))\n\t_update_creator_compatibility(_selected_index)\n\nfunc _refresh_trait_options",
        "func _on_creator_selection_changed(_selected_index: int = -1) -> void:\n\t_refresh_trait_options(_get_selected_option_text(trait_options))\n\t_update_portrait_summary()\n\t_update_creator_compatibility(_selected_index)\n\nfunc _on_portrait_selection_changed(_selected_index: int = -1) -> void:\n\t_update_portrait_summary()\n\nfunc _refresh_trait_options",
        "portrait selection signal",
    )

    content = replace_once(
        content,
        "func _get_unavailable_trait_explanations() -> Array[String]:\n\tvar result: Array[String] = []\n\tif character_creation_data.is_empty():\n\t\treturn result\n\tvar traits: Array = character_creation_data.get(\"traits\", [])\n\tif traits.is_empty():\n\t\treturn result\n\tvar base_tags := _collect_creator_base_tags()\n\tfor trait in traits:\n\t\tif typeof(trait) != TYPE_DICTIONARY:\n\t\t\tcontinue\n\t\tvar reasons := CharacterProfileBuilder.get_item_unavailable_reasons(base_tags, trait)\n\t\tif not reasons.is_empty():\n\t\t\tresult.append(\" \".join(reasons))\n\treturn result\n\nfunc _start_game",
        "func _get_unavailable_trait_explanations() -> Array[String]:\n\tvar result: Array[String] = []\n\tif character_creation_data.is_empty():\n\t\treturn result\n\tvar traits: Array = character_creation_data.get(\"traits\", [])\n\tif traits.is_empty():\n\t\treturn result\n\tvar base_tags := _collect_creator_base_tags()\n\tfor trait in traits:\n\t\tif typeof(trait) != TYPE_DICTIONARY:\n\t\t\tcontinue\n\t\tvar reasons := CharacterProfileBuilder.get_item_unavailable_reasons(base_tags, trait)\n\t\tif not reasons.is_empty():\n\t\t\tresult.append(\" \".join(reasons))\n\treturn result\n\nfunc _populate_portrait_options() -> void:\n\tif portrait_options == null:\n\t\treturn\n\tportrait_options.clear()\n\tvar portraits := PortraitCatalog.get_portraits(portrait_data)\n\tif portraits.is_empty():\n\t\tportrait_options.add_item(\"Weathered Drifter\")\n\t\tportrait_options.select(0)\n\t\treturn\n\tfor portrait in portraits:\n\t\tportrait_options.add_item(PortraitCatalog.get_display_name(portrait))\n\tportrait_options.select(0)\n\nfunc _select_portrait_by_name(portrait_name: String) -> bool:\n\tif portrait_options == null:\n\t\treturn false\n\tif portrait_name.is_empty():\n\t\treturn false\n\treturn _select_option_by_text(portrait_options, portrait_name, \"portrait\")\n\nfunc _get_selected_portrait() -> Dictionary:\n\tif portrait_options == null or portrait_options.get_item_count() == 0:\n\t\treturn PortraitCatalog.get_default_portrait(portrait_data)\n\tvar portrait_name := portrait_options.get_item_text(portrait_options.selected)\n\tvar portrait := PortraitCatalog.find_by_name(portrait_data, portrait_name)\n\tif portrait.is_empty():\n\t\treturn PortraitCatalog.get_default_portrait(portrait_data)\n\treturn portrait\n\nfunc _update_portrait_summary() -> void:\n\tif portrait_summary_label == null:\n\t\treturn\n\tvar portrait := _get_selected_portrait()\n\tif portrait.is_empty():\n\t\tportrait_summary_label.text = \"Portrait: Weathered Drifter\\nNo portrait metadata loaded.\"\n\t\treturn\n\tportrait_summary_label.text = \"%s\\n%s\" % [PortraitCatalog.get_display_name(portrait), PortraitCatalog.get_summary(portrait)]\n\nfunc _start_game",
        "portrait helpers",
    )

    content = replace_once(
        content,
        "\t\t\tif button == \"start_journey\":\n\t\t\t\tif character_name_edit == null or ancestry_options == null or origin_options == null or archetype_options == null or trait_options == null:\n\t\t\t\t\tGameLog.error(\"ASSERT\", \"Cannot start journey; character creator controls are missing\")\n\t\t\t\t\treturn false\n\t\t\t\t_start_new_game_from_creator(character_name_edit, ancestry_options, origin_options, archetype_options, trait_options)\n",
        "\t\t\tif button == \"start_journey\":\n\t\t\t\tif character_name_edit == null or ancestry_options == null or origin_options == null or archetype_options == null or trait_options == null or portrait_options == null:\n\t\t\t\t\tGameLog.error(\"ASSERT\", \"Cannot start journey; character creator controls are missing\")\n\t\t\t\t\treturn false\n\t\t\t\t_start_new_game_from_creator(character_name_edit, ancestry_options, origin_options, archetype_options, trait_options, portrait_options)\n",
        "debug start journey",
    )

    content = replace_once(
        content,
        "\t\t\"select_trait\":\n\t\t\tvar trait_ok := _select_option_by_text(trait_options, String(action.get(\"trait\", \"\")), \"trait\")\n\t\t\t_update_creator_compatibility()\n\t\t\treturn trait_ok\n\t\t\"assert_trait_available\":\n",
        "\t\t\"select_trait\":\n\t\t\tvar trait_ok := _select_option_by_text(trait_options, String(action.get(\"trait\", \"\")), \"trait\")\n\t\t\t_update_creator_compatibility()\n\t\t\treturn trait_ok\n\t\t\"select_portrait\":\n\t\t\tvar portrait_ok := _select_option_by_text(portrait_options, String(action.get(\"portrait\", \"\")), \"portrait\")\n\t\t\t_update_portrait_summary()\n\t\t\treturn portrait_ok\n\t\t\"assert_trait_available\":\n",
        "debug select portrait",
    )

    content = replace_once(
        content,
        "func _assert_player_profile(action: Dictionary) -> bool:\n\tfor key in [\"name\", \"ancestry\", \"origin\", \"archetype\", \"background\", \"class\", \"trait\"]:\n",
        "func _assert_player_profile(action: Dictionary) -> bool:\n\tfor key in [\"name\", \"ancestry\", \"origin\", \"archetype\", \"background\", \"class\", \"trait\", \"portrait_id\", \"portrait\"]:\n",
        "profile assertions",
    )

    content = replace_once(
        content,
        "\ttrait_options = null\n\tcompatibility_warning_label = null\n\tstart_journey_button = null\n",
        "\ttrait_options = null\n\tportrait_options = null\n\tportrait_summary_label = null\n\tcompatibility_warning_label = null\n\tstart_journey_button = null\n",
        "clear portrait controls",
    )

    MAIN_GD.write_text(content, encoding="utf-8")
    write_portrait_selection_scenario()
    print(f"Applied Issue #13 portrait selector patch to {MAIN_GD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
