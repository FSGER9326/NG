#!/usr/bin/env python3
"""Validate NG project data.

Dependency-free Python validation for JSON data, common references, dialogue links,
area actor placements, encounter IDs, quest-stage references, dialogue conditions,
and scripted test scenarios.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
JSON_ROOTS = [ROOT / "data", ROOT / "areas", ROOT / "dialogue", ROOT / "tests"]

REFERENCE_KEYS = {
    "background",
    "occlusion",
    "walkmask",
    "hotspots",
    "actors",
    "portrait",
    "dialogue",
    "sprite",
    "icon",
}

CONDITION_TYPES = {"flag", "quest_stage", "skill_check", "not", "all", "any"}
SKILLS = {"perception", "survival", "resolve", "lore", "stealth"}
MENU_BUTTONS = {"new_game", "start_journey"}
SCREENS = {"main_menu", "character_creator", "game"}
ORIGINS = {"Border Drifter", "Failed Squire", "Village Outcast", "Caravan Guard"}
ARCHETYPES = {"Mercenary", "Scout", "Hedge Knight", "Cunning Speaker"}


class ProjectIndex:
    def __init__(self) -> None:
        self.ids: dict[str, Path] = {}
        self.actors: set[str] = set()
        self.quests: dict[str, set[str]] = {}
        self.encounters: set[str] = set()
        self.factions: set[str] = set()
        self.areas: set[str] = set()
        self.hotspots: set[str] = set()
        self.dialogue_choice_texts: set[str] = set()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def walk_json_files() -> list[Path]:
    files: list[Path] = []
    for root in JSON_ROOTS:
        if root.exists():
            files.extend(sorted(root.rglob("*.json")))
    return files


def collect_ids(path: Path, data: Any, index: ProjectIndex, errors: list[str]) -> None:
    if isinstance(data, dict):
        item_id = data.get("id")
        if isinstance(item_id, str):
            if item_id in index.ids:
                errors.append(f"Duplicate id '{item_id}' in {path.relative_to(ROOT)} and {index.ids[item_id].relative_to(ROOT)}")
            else:
                index.ids[item_id] = path

            kind = data.get("kind")
            if kind in {"npc", "companion", "enemy"}:
                index.actors.add(item_id)
            if "encounters" in path.parts:
                index.encounters.add(item_id)
            if path.name == "area.json" and "areas" in path.parts:
                index.areas.add(item_id)

        if path.match("*/data/quests/**/*.json") and isinstance(item_id, str):
            stages = data.get("stages", {})
            if isinstance(stages, dict):
                index.quests[item_id] = set(stages.keys())

        if path.name == "hotspots.json" and "areas" in path.parts:
            for hotspot in data.get("hotspots", []):
                if isinstance(hotspot, dict) and isinstance(hotspot.get("id"), str):
                    index.hotspots.add(hotspot["id"])

        if "dialogue" in path.parts:
            collect_dialogue_choice_texts(data, index)

        faction_list = data.get("factions")
        if isinstance(faction_list, list):
            for faction in faction_list:
                if isinstance(faction, dict) and isinstance(faction.get("id"), str):
                    index.factions.add(faction["id"])

        for value in data.values():
            collect_ids(path, value, index, errors)
    elif isinstance(data, list):
        for value in data:
            collect_ids(path, value, index, errors)


def collect_dialogue_choice_texts(data: Any, index: ProjectIndex) -> None:
    if not isinstance(data, dict):
        return
    nodes = data.get("nodes")
    if not isinstance(nodes, dict):
        return
    for node in nodes.values():
        if not isinstance(node, dict):
            continue
        for choice in node.get("choices", []):
            if isinstance(choice, dict) and isinstance(choice.get("text"), str):
                index.dialogue_choice_texts.add(choice["text"])


def check_references(path: Path, data: Any, errors: list[str]) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in REFERENCE_KEYS and isinstance(value, str):
                ref = to_repo_path(value)
                if value and not ref.exists():
                    errors.append(f"Missing referenced file in {path.relative_to(ROOT)}: {key} -> {value}")
            check_references(path, value, errors)
    elif isinstance(data, list):
        for value in data:
            check_references(path, value, errors)


def check_dialogue(path: Path, data: Any, index: ProjectIndex, errors: list[str]) -> None:
    if "dialogue" not in path.parts or not isinstance(data, dict):
        return
    nodes = data.get("nodes")
    if not isinstance(nodes, dict):
        return
    node_ids = set(nodes.keys())
    start_node = data.get("start_node")
    if isinstance(start_node, str) and start_node not in node_ids:
        errors.append(f"Dialogue start_node missing in {path.relative_to(ROOT)}: {start_node}")
    for node_id, node in nodes.items():
        if not isinstance(node, dict):
            errors.append(f"Dialogue node is not an object in {path.relative_to(ROOT)}: {node_id}")
            continue
        check_conditions(path, node.get("conditions", []), index, errors, f"node {node_id}")
        for choice in node.get("choices", []):
            if not isinstance(choice, dict):
                continue
            next_node = choice.get("next")
            if isinstance(next_node, str) and next_node != "end" and next_node not in node_ids:
                errors.append(f"Dialogue missing next node in {path.relative_to(ROOT)}: {node_id} -> {next_node}")
            check_conditions(path, choice.get("conditions", []), index, errors, f"choice '{choice.get('text', '')}' in node {node_id}")
        check_effects(path, node.get("effects", []), index, errors)


def check_area_actor_placements(path: Path, data: Any, index: ProjectIndex, errors: list[str]) -> None:
    if path.name != "actors.json" or "areas" not in path.parts or not isinstance(data, dict):
        return
    for actor in data.get("actors", []):
        if not isinstance(actor, dict):
            continue
        actor_id = actor.get("actor_id")
        if isinstance(actor_id, str) and actor_id not in index.actors:
            errors.append(f"Area references missing actor in {path.relative_to(ROOT)}: {actor_id}")
        encounter_id = actor.get("encounter_id")
        if isinstance(encounter_id, str) and encounter_id not in index.encounters:
            errors.append(f"Area references missing encounter in {path.relative_to(ROOT)}: {encounter_id}")


def check_effects(path: Path, effects: Any, index: ProjectIndex, errors: list[str]) -> None:
    if not isinstance(effects, list):
        return
    for effect in effects:
        if not isinstance(effect, dict):
            continue
        effect_type = effect.get("type")
        if effect_type in {"start_quest", "set_quest_stage"}:
            quest_id = effect.get("quest_id")
            if not isinstance(quest_id, str) or quest_id not in index.quests:
                errors.append(f"Effect references missing quest in {path.relative_to(ROOT)}: {quest_id}")
                continue
            stage = effect.get("stage")
            if isinstance(stage, str) and stage not in index.quests[quest_id]:
                errors.append(f"Effect references missing quest stage in {path.relative_to(ROOT)}: {quest_id}.{stage}")
        elif effect_type == "set_flag":
            if not isinstance(effect.get("flag_id"), str) or not effect.get("flag_id"):
                errors.append(f"set_flag effect missing flag_id in {path.relative_to(ROOT)}")


def check_conditions(path: Path, conditions: Any, index: ProjectIndex, errors: list[str], context: str) -> None:
    if conditions in (None, []):
        return
    if not isinstance(conditions, list):
        errors.append(f"Conditions must be a list in {path.relative_to(ROOT)} at {context}")
        return
    for condition in conditions:
        check_condition(path, condition, index, errors, context)


def check_condition(path: Path, condition: Any, index: ProjectIndex, errors: list[str], context: str) -> None:
    if not isinstance(condition, dict):
        errors.append(f"Condition must be object in {path.relative_to(ROOT)} at {context}")
        return
    condition_type = condition.get("type")
    if condition_type not in CONDITION_TYPES:
        errors.append(f"Unknown condition type in {path.relative_to(ROOT)} at {context}: {condition_type}")
        return
    if condition_type == "flag":
        if not isinstance(condition.get("flag_id"), str) or not condition.get("flag_id"):
            errors.append(f"flag condition missing flag_id in {path.relative_to(ROOT)} at {context}")
        if "value" in condition and not isinstance(condition.get("value"), bool):
            errors.append(f"flag condition value must be boolean in {path.relative_to(ROOT)} at {context}")
    elif condition_type == "quest_stage":
        quest_id = condition.get("quest_id")
        stage = condition.get("stage")
        if not isinstance(quest_id, str) or quest_id not in index.quests:
            errors.append(f"quest_stage condition references missing quest in {path.relative_to(ROOT)} at {context}: {quest_id}")
        elif not isinstance(stage, str) or stage not in index.quests[quest_id]:
            errors.append(f"quest_stage condition references missing stage in {path.relative_to(ROOT)} at {context}: {quest_id}.{stage}")
    elif condition_type == "skill_check":
        skill_id = condition.get("skill_id")
        difficulty = condition.get("difficulty")
        if not isinstance(skill_id, str) or not skill_id:
            errors.append(f"skill_check condition missing skill_id in {path.relative_to(ROOT)} at {context}")
        elif skill_id not in SKILLS:
            errors.append(f"skill_check condition references unknown skill in {path.relative_to(ROOT)} at {context}: {skill_id}")
        if not isinstance(difficulty, int) or difficulty < 0:
            errors.append(f"skill_check condition difficulty must be a non-negative integer in {path.relative_to(ROOT)} at {context}")
    elif condition_type == "not":
        check_condition(path, condition.get("condition"), index, errors, f"{context} > not")
    elif condition_type in {"all", "any"}:
        nested = condition.get("conditions")
        if not isinstance(nested, list) or not nested:
            errors.append(f"{condition_type} condition needs non-empty conditions list in {path.relative_to(ROOT)} at {context}")
        else:
            check_conditions(path, nested, index, errors, f"{context} > {condition_type}")


def check_quest_references(path: Path, data: Any, index: ProjectIndex, errors: list[str]) -> None:
    if not isinstance(data, dict):
        return
    check_effects(path, data.get("victory_effects", []), index, errors)
    check_effects(path, data.get("effects", []), index, errors)


def check_scenario(path: Path, data: Any, index: ProjectIndex, errors: list[str]) -> None:
    if "tests" not in path.parts or "scenarios" not in path.parts or not isinstance(data, dict):
        return
    root_scene = data.get("root_scene", "area")
    if not isinstance(root_scene, str):
        errors.append(f"Scenario root_scene must be string in {path.relative_to(ROOT)}")
    steps = data.get("steps")
    if not isinstance(steps, list):
        errors.append(f"Scenario missing steps list in {path.relative_to(ROOT)}")
        return
    for step_index, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            errors.append(f"Scenario step is not object in {path.relative_to(ROOT)} step {step_index}")
            continue
        step_type = step.get("type")
        if not isinstance(step_type, str):
            errors.append(f"Scenario step missing type in {path.relative_to(ROOT)} step {step_index}")
            continue
        check_scenario_step(path, step, step_type, step_index, index, errors)


def check_scenario_step(path: Path, step: dict[str, Any], step_type: str, step_index: int, index: ProjectIndex, errors: list[str]) -> None:
    match step_type:
        case "load_area" | "assert_area":
            area_id = step.get("area_id")
            if not isinstance(area_id, str) or area_id not in index.areas:
                errors.append(f"Scenario {step_type} references missing area in {path.relative_to(ROOT)} step {step_index}: {area_id}")
        case "click_actor":
            actor_id = step.get("actor_id")
            if not isinstance(actor_id, str) or actor_id not in index.actors:
                errors.append(f"Scenario references missing actor in {path.relative_to(ROOT)} step {step_index}: {actor_id}")
        case "choose_dialogue":
            text = step.get("text")
            if not isinstance(text, str) or text not in index.dialogue_choice_texts:
                errors.append(f"Scenario references missing dialogue choice in {path.relative_to(ROOT)} step {step_index}: {text}")
        case "click_hotspot":
            hotspot_id = step.get("hotspot_id")
            if not isinstance(hotspot_id, str) or hotspot_id not in index.hotspots:
                errors.append(f"Scenario references missing hotspot in {path.relative_to(ROOT)} step {step_index}: {hotspot_id}")
        case "assert_quest_stage":
            quest_id = step.get("quest_id")
            stage = step.get("stage")
            if not isinstance(quest_id, str) or quest_id not in index.quests:
                errors.append(f"Scenario references missing quest in {path.relative_to(ROOT)} step {step_index}: {quest_id}")
            elif not isinstance(stage, str) or stage not in index.quests[quest_id]:
                errors.append(f"Scenario references missing quest stage in {path.relative_to(ROOT)} step {step_index}: {quest_id}.{stage}")
        case "assert_flag":
            if not isinstance(step.get("flag_id"), str) or not step.get("flag_id"):
                errors.append(f"Scenario assert_flag missing flag_id in {path.relative_to(ROOT)} step {step_index}")
        case "assert_screen":
            if step.get("screen") not in SCREENS:
                errors.append(f"Scenario assert_screen has unknown screen in {path.relative_to(ROOT)} step {step_index}: {step.get('screen')}")
        case "press_menu":
            if step.get("button") not in MENU_BUTTONS:
                errors.append(f"Scenario press_menu has unknown button in {path.relative_to(ROOT)} step {step_index}: {step.get('button')}")
        case "set_character_name":
            if not isinstance(step.get("name"), str):
                errors.append(f"Scenario set_character_name missing name in {path.relative_to(ROOT)} step {step_index}")
        case "select_origin":
            if step.get("origin") not in ORIGINS:
                errors.append(f"Scenario select_origin has unknown origin in {path.relative_to(ROOT)} step {step_index}: {step.get('origin')}")
        case "select_archetype":
            if step.get("archetype") not in ARCHETYPES:
                errors.append(f"Scenario select_archetype has unknown archetype in {path.relative_to(ROOT)} step {step_index}: {step.get('archetype')}")
        case "assert_player_profile":
            for field in ["name", "origin", "archetype"]:
                if field in step and not isinstance(step.get(field), str):
                    errors.append(f"Scenario assert_player_profile field {field} must be string in {path.relative_to(ROOT)} step {step_index}")
        case _:
            errors.append(f"Scenario has unknown step type in {path.relative_to(ROOT)} step {step_index}: {step_type}")


def to_repo_path(value: str) -> Path:
    if value.startswith("res://"):
        return ROOT / value.removeprefix("res://")
    return ROOT / value


def main() -> int:
    errors: list[str] = []
    index = ProjectIndex()
    parsed_files: dict[Path, Any] = {}
    files = walk_json_files()

    if not files:
        errors.append("No JSON files found under data/, areas/, dialogue/, or tests/.")

    for path in files:
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")
            continue
        parsed_files[path] = data
        collect_ids(path, data, index, errors)

    for path, data in parsed_files.items():
        check_references(path, data, errors)
        check_dialogue(path, data, index, errors)
        check_area_actor_placements(path, data, index, errors)
        check_quest_references(path, data, index, errors)
        check_scenario(path, data, index, errors)

    if errors:
        print("NG validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "NG validation passed: "
        f"{len(files)} JSON files, {len(index.ids)} IDs, "
        f"{len(index.actors)} actors, {len(index.quests)} quests, "
        f"{len(index.hotspots)} hotspots."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
