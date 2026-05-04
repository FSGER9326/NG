#!/usr/bin/env python3
"""Validate NG project data.

Dependency-free Python validation for JSON data, common references, dialogue links,
area actor placements, encounter IDs, and quest-stage references.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
JSON_ROOTS = [ROOT / "data", ROOT / "areas", ROOT / "dialogue"]

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


class ProjectIndex:
    def __init__(self) -> None:
        self.ids: dict[str, Path] = {}
        self.actors: set[str] = set()
        self.quests: dict[str, set[str]] = {}
        self.encounters: set[str] = set()
        self.factions: set[str] = set()


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

        if path.match("*/data/quests/**/*.json") and isinstance(item_id, str):
            stages = data.get("stages", {})
            if isinstance(stages, dict):
                index.quests[item_id] = set(stages.keys())

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
    if not path.parts or "dialogue" not in path.parts or not isinstance(data, dict):
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
        for choice in node.get("choices", []):
            if not isinstance(choice, dict):
                continue
            next_node = choice.get("next")
            if isinstance(next_node, str) and next_node != "end" and next_node not in node_ids:
                errors.append(f"Dialogue missing next node in {path.relative_to(ROOT)}: {node_id} -> {next_node}")
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


def check_quest_references(path: Path, data: Any, index: ProjectIndex, errors: list[str]) -> None:
    if not isinstance(data, dict):
        return
    check_effects(path, data.get("victory_effects", []), index, errors)
    check_effects(path, data.get("effects", []), index, errors)


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
        errors.append("No JSON files found under data/, areas/, or dialogue/.")

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

    if errors:
        print("NG validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "NG validation passed: "
        f"{len(files)} JSON files, {len(index.ids)} IDs, "
        f"{len(index.actors)} actors, {len(index.quests)} quests."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
