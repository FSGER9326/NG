#!/usr/bin/env python3
"""Validate the text-first NG quest seed bank."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEST_SEEDS_PATH = ROOT / "docs" / "QUEST_SEEDS.md"
SEED_HEADING_RE = re.compile(r"^## \d+\. .+$", re.MULTILINE)
FIELD_RE = re.compile(r"^\*\*(ID|Use|Theme|Description|Stages|Branches|Flags|Lines):\*\*", re.MULTILINE)
ID_RE = re.compile(r"^\*\*ID:\*\* `([a-z0-9_]+)`", re.MULTILINE)

REQUIRED_FIELDS = {
    "ID",
    "Use",
    "Theme",
    "Description",
    "Stages",
    "Branches",
    "Flags",
    "Lines",
}


def split_seed_sections(content: str) -> list[str]:
    matches = list(SEED_HEADING_RE.finditer(content))
    sections: list[str] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else content.find("\n## Implementation notes", start)
        if end == -1:
            end = len(content)
        sections.append(content[start:end].strip())
    return sections


def main() -> int:
    errors: list[str] = []

    if not QUEST_SEEDS_PATH.exists():
        print(f"Missing quest seed bank: {QUEST_SEEDS_PATH.relative_to(ROOT)}")
        return 1

    content = QUEST_SEEDS_PATH.read_text(encoding="utf-8")
    sections = split_seed_sections(content)
    if not sections:
        errors.append("No numbered quest seed sections found")

    seen_ids: set[str] = set()
    for section in sections:
        heading = section.splitlines()[0]
        id_match = ID_RE.search(section)
        seed_id = id_match.group(1) if id_match else heading
        fields = set(FIELD_RE.findall(section))
        missing_fields = REQUIRED_FIELDS - fields
        if missing_fields:
            errors.append(f"{seed_id} missing fields: {', '.join(sorted(missing_fields))}")
        if not id_match:
            errors.append(f"{heading} missing machine-readable ID")
        elif seed_id in seen_ids:
            errors.append(f"Duplicate quest seed ID: {seed_id}")
        else:
            seen_ids.add(seed_id)
        if "_" not in seed_id:
            errors.append(f"Quest seed ID should use snake_case with underscores: {seed_id}")
        if "`not_started`" not in section:
            errors.append(f"{seed_id} stages should include `not_started`")
        if "**Flags:**" in section and "_" not in section.split("**Flags:**", 1)[1].split("\n", 1)[0]:
            errors.append(f"{seed_id} flags should include machine-readable snake_case names")

    if "## Implementation notes" not in content:
        errors.append("Quest seed bank missing Implementation notes section")
    if "Good first candidates" not in content:
        errors.append("Quest seed bank should identify good first JSON conversion candidates")

    if errors:
        print("NG quest seed validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"NG quest seed validation passed: {len(sections)} quest seeds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
