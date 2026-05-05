#!/usr/bin/env python3
"""Validate NG text-first portrait metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PORTRAITS_PATH = ROOT / "data" / "character_creation" / "portraits.json"
CHARACTER_CREATION_PATH = ROOT / "data" / "character_creation" / "character_creation.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_tag_list(errors: list[str], context: str, value: Any) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{context}.tags must be a non-empty list")
        return
    for tag in value:
        if not isinstance(tag, str) or "." not in tag:
            errors.append(f"{context}.tags has malformed tag: {tag}")


def validate_background_portrait_refs(errors: list[str], portrait_ids: set[str]) -> None:
    if not CHARACTER_CREATION_PATH.exists():
        errors.append(f"Missing character creation data: {CHARACTER_CREATION_PATH.relative_to(ROOT)}")
        return
    data = load_json(CHARACTER_CREATION_PATH)
    if not isinstance(data, dict):
        errors.append("Character creation root must be an object")
        return
    backgrounds = data.get("backgrounds")
    if not isinstance(backgrounds, list):
        errors.append("Character creation data must contain a backgrounds list")
        return
    for index, background in enumerate(backgrounds, start=1):
        if not isinstance(background, dict):
            errors.append(f"background entry {index} must be an object")
            continue
        background_id = str(background.get("id", f"background entry {index}"))
        portrait_id = background.get("portrait_id")
        if portrait_id is None:
            continue
        if not isinstance(portrait_id, str) or not portrait_id:
            errors.append(f"{background_id}.portrait_id must be a non-empty string when present")
            continue
        if portrait_id not in portrait_ids:
            errors.append(f"{background_id}.portrait_id references unknown portrait: {portrait_id}")


def main() -> int:
    errors: list[str] = []
    if not PORTRAITS_PATH.exists():
        print(f"Missing portrait metadata: {PORTRAITS_PATH.relative_to(ROOT)}")
        return 1

    data = load_json(PORTRAITS_PATH)
    if not isinstance(data, dict):
        print("Portrait metadata root must be an object")
        return 1

    portraits = data.get("portraits")
    if not isinstance(portraits, list) or not portraits:
        print("Portrait metadata must contain a non-empty portraits list")
        return 1

    seen_ids: set[str] = set()
    for index, portrait in enumerate(portraits, start=1):
        if not isinstance(portrait, dict):
            errors.append(f"portrait entry {index} must be an object")
            continue
        portrait_id = portrait.get("id")
        context = str(portrait_id) if isinstance(portrait_id, str) and portrait_id else f"portrait entry {index}"
        if not isinstance(portrait_id, str) or not portrait_id:
            errors.append(f"portrait entry {index} missing id")
        elif portrait_id in seen_ids:
            errors.append(f"Duplicate portrait id: {portrait_id}")
        else:
            seen_ids.add(portrait_id)
        if isinstance(portrait_id, str) and not portrait_id.startswith("portrait_"):
            errors.append(f"Portrait id should use portrait_ prefix: {portrait_id}")
        for field in ("name", "summary"):
            if not isinstance(portrait.get(field), str) or not portrait.get(field):
                errors.append(f"{context} missing {field}")
        validate_tag_list(errors, context, portrait.get("tags"))

    validate_background_portrait_refs(errors, seen_ids)

    if errors:
        print("NG portrait validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"NG portrait validation passed: {len(portraits)} portraits.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
