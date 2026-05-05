#!/usr/bin/env python3
"""Validate NG character creation data.

Checks ancestry/background/class/trait records for stable ids, tag shape,
modifier shape, thematic compatibility references, and starter portrait metadata.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data" / "character_creation"
DATA_PATH = DATA_ROOT / "character_creation.json"
PORTRAITS_PATH = DATA_ROOT / "portraits.json"
SECTIONS = ("ancestries", "backgrounds", "classes", "traits")
ATTRIBUTE_IDS = {"might", "finesse", "resolve", "wits", "presence", "occult"}
SKILL_IDS = {
    "perception",
    "survival",
    "resolve",
    "lore",
    "stealth",
    "athletics",
    "medicine",
    "streetwise",
    "arcana",
    "command",
}
REQUIRED_STARTER_PORTRAIT_IDS = {
    "portrait_weathered_drifter_01",
    "portrait_disgraced_squire_01",
    "portrait_village_outcast_01",
    "portrait_caravan_guard_01",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_stat_map(errors: list[str], context: str, value: Any, allowed: set[str]) -> None:
    if value in ({}, None):
        return
    if not isinstance(value, dict):
        errors.append(f"{context} must be an object")
        return
    for key, amount in value.items():
        if key not in allowed:
            errors.append(f"{context} uses unknown id: {key}")
        if not isinstance(amount, int):
            errors.append(f"{context}.{key} must be an integer")


def validate_tags(errors: list[str], context: str, tags: Any, known_tags: set[str] | None = None) -> None:
    if not isinstance(tags, list) or not tags:
        errors.append(f"{context} must have non-empty tags")
        return
    for tag in tags:
        if not isinstance(tag, str) or "." not in tag:
            errors.append(f"{context} has malformed tag: {tag}")
        elif known_tags is not None:
            known_tags.add(tag)


def validate_item(errors: list[str], section: str, item: Any, seen_ids: set[str], known_tags: set[str]) -> None:
    if not isinstance(item, dict):
        errors.append(f"{section} entry must be an object")
        return

    item_id = item.get("id")
    if not isinstance(item_id, str) or not item_id:
        errors.append(f"{section} entry missing id")
        item_id = f"missing_id_{section}"
    elif item_id in seen_ids:
        errors.append(f"Duplicate character creation id: {item_id}")
    else:
        seen_ids.add(item_id)

    for field in ("name", "summary"):
        if not isinstance(item.get(field), str) or not item.get(field):
            errors.append(f"{item_id} missing {field}")

    validate_tags(errors, item_id, item.get("tags"), known_tags)

    explicit_portrait_id = item.get("portrait_id")
    if explicit_portrait_id is not None:
        if not isinstance(explicit_portrait_id, str) or not explicit_portrait_id.startswith("portrait_"):
            errors.append(f"{item_id}.portrait_id must use portrait_ id prefix")

    modifiers = item.get("modifiers", {})
    if modifiers and not isinstance(modifiers, dict):
        errors.append(f"{item_id}.modifiers must be an object")
    elif isinstance(modifiers, dict):
        validate_stat_map(errors, f"{item_id}.modifiers.attributes", modifiers.get("attributes", {}), ATTRIBUTE_IDS)
        validate_stat_map(errors, f"{item_id}.modifiers.skills", modifiers.get("skills", {}), SKILL_IDS)

    for field in ("requires_any_tags", "blocked_by_tags"):
        value = item.get(field, [])
        if value and not isinstance(value, list):
            errors.append(f"{item_id}.{field} must be a list")
            continue
        for tag in value:
            if not isinstance(tag, str) or "." not in tag:
                errors.append(f"{item_id}.{field} has malformed tag: {tag}")


def validate_portraits(errors: list[str], known_tags: set[str]) -> set[str]:
    if not PORTRAITS_PATH.exists():
        errors.append(f"Missing portrait metadata: {PORTRAITS_PATH.relative_to(ROOT)}")
        return set()

    try:
        data = load_json(PORTRAITS_PATH)
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {PORTRAITS_PATH.relative_to(ROOT)}: {exc}")
        return set()

    if not isinstance(data, dict):
        errors.append("Portrait metadata root must be an object")
        return set()

    for field in ("id", "name", "description"):
        if not isinstance(data.get(field), str) or not data.get(field):
            errors.append(f"portrait metadata missing {field}")

    portraits = data.get("portraits")
    if not isinstance(portraits, list) or not portraits:
        errors.append("portraits must be a non-empty list")
        return set()

    seen_ids: set[str] = set()
    for index, portrait in enumerate(portraits, start=1):
        context = f"portrait {index}"
        if not isinstance(portrait, dict):
            errors.append(f"{context} must be an object")
            continue
        portrait_id = portrait.get("id")
        if not isinstance(portrait_id, str) or not portrait_id:
            errors.append(f"{context} missing id")
            portrait_id = context
        elif not portrait_id.startswith("portrait_"):
            errors.append(f"{portrait_id} should use portrait_ id prefix")
        elif portrait_id in seen_ids:
            errors.append(f"Duplicate portrait id: {portrait_id}")
        else:
            seen_ids.add(portrait_id)

        for field in ("name", "summary"):
            if not isinstance(portrait.get(field), str) or not portrait.get(field):
                errors.append(f"{portrait_id} missing {field}")

        validate_tags(errors, portrait_id, portrait.get("tags"))
        for tag in portrait.get("tags", []):
            if isinstance(tag, str) and tag not in known_tags and not tag.startswith(("portrait.", "mood.")):
                errors.append(f"{portrait_id} uses non-portrait tag not produced by character creation data: {tag}")

    missing_required = REQUIRED_STARTER_PORTRAIT_IDS - seen_ids
    for portrait_id in sorted(missing_required):
        errors.append(f"Missing required starter portrait id used by CharacterProfileBuilder: {portrait_id}")

    return seen_ids


def validate_background_portrait_refs(errors: list[str], data: dict[str, Any], portrait_ids: set[str]) -> None:
    backgrounds = data.get("backgrounds", [])
    if not isinstance(backgrounds, list):
        return
    for background in backgrounds:
        if not isinstance(background, dict):
            continue
        background_id = str(background.get("id", "unknown"))
        portrait_id = background.get("portrait_id")
        if portrait_id is None:
            errors.append(f"{background_id} missing required portrait_id")
            continue
        if not isinstance(portrait_id, str) or not portrait_id.startswith("portrait_"):
            errors.append(f"{background_id}.portrait_id must use portrait_ id prefix")
        elif portrait_id not in portrait_ids:
            errors.append(f"{background_id}.portrait_id references missing portrait: {portrait_id}")


def main() -> int:
    errors: list[str] = []
    if not DATA_PATH.exists():
        print(f"Missing character creation data: {DATA_PATH.relative_to(ROOT)}")
        return 1

    try:
        data = load_json(DATA_PATH)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {DATA_PATH.relative_to(ROOT)}: {exc}")
        return 1

    if not isinstance(data, dict):
        print("Character creation data root must be an object")
        return 1

    validate_stat_map(errors, "base_attributes", data.get("base_attributes", {}), ATTRIBUTE_IDS)
    validate_stat_map(errors, "base_skills", data.get("base_skills", {}), SKILL_IDS)

    seen_ids: set[str] = set()
    known_tags: set[str] = set()
    for section in SECTIONS:
        items = data.get(section)
        if not isinstance(items, list) or not items:
            errors.append(f"{section} must be a non-empty list")
            continue
        for item in items:
            validate_item(errors, section, item, seen_ids, known_tags)

    portrait_ids = validate_portraits(errors, known_tags)
    validate_background_portrait_refs(errors, data, portrait_ids)

    # Second pass: compatibility tags should either be produced somewhere now or use an accepted future-facing prefix.
    future_prefixes = ("occult.", "morale.", "diplomacy.", "medicine.", "armor.", "stealth.", "survival.")
    for section in SECTIONS:
        for item in data.get(section, []):
            if not isinstance(item, dict):
                continue
            item_id = str(item.get("id", "unknown"))
            for field in ("requires_any_tags", "blocked_by_tags"):
                for tag in item.get(field, []):
                    if isinstance(tag, str) and tag not in known_tags and not tag.startswith(future_prefixes):
                        errors.append(f"{item_id}.{field} references tag no current option produces: {tag}")

    if errors:
        print("NG character creation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "NG character creation validation passed: "
        f"{sum(len(data.get(section, [])) for section in SECTIONS)} options, "
        f"{len(known_tags)} produced tags, {len(portrait_ids)} portraits."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
