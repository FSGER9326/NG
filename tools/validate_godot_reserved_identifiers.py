#!/usr/bin/env python3
"""Fail fast on GDScript local identifiers that collide with Godot 4.6 keywords.

The manual play logs exposed parse errors caused by local variables named
``class_name`` and ``trait``. Godot treats these as language-level identifiers
in recent versions, so they should not be used after ``var`` or as loop targets.

This validator intentionally focuses on the high-risk declaration forms that
have broken the project, instead of trying to fully parse GDScript.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Keep this set deliberately conservative. Add names only after they cause or
# strongly risk parser collisions in the supported Godot version.
RESERVED_LOCAL_NAMES = {
    "class_name",
    "trait",
}

DECLARE_PATTERNS = (
    re.compile(r"^\s*var\s+([A-Za-z_][A-Za-z0-9_]*)\b"),
    re.compile(r"^\s*for\s+([A-Za-z_][A-Za-z0-9_]*)\s+in\b"),
)

IGNORED_DIR_PARTS = {
    ".git",
    ".godot",
    "debug_reports",
    "debug",
}


def main() -> int:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.gd")):
        if any(part in IGNORED_DIR_PARTS for part in path.parts):
            continue
        _scan_file(path, errors)

    if errors:
        print("Godot reserved identifier validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Godot reserved identifier validation passed.")
    return 0


def _scan_file(path: Path, errors: list[str]) -> None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: could not decode as UTF-8: {exc}")
        return

    for line_number, line in enumerate(lines, start=1):
        stripped = _strip_line_comment(line)
        for pattern in DECLARE_PATTERNS:
            match = pattern.search(stripped)
            if match is None:
                continue
            identifier = match.group(1)
            if identifier in RESERVED_LOCAL_NAMES:
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number}: reserved local identifier '{identifier}' in: {line.strip()}"
                )


def _strip_line_comment(line: str) -> str:
    # Good enough for declarations: ignore anything after a # comment marker.
    # GDScript strings containing # before a declaration are not relevant here.
    return line.split("#", 1)[0]


if __name__ == "__main__":
    raise SystemExit(main())
