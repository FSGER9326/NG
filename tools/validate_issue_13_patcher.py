#!/usr/bin/env python3
"""Validate the Issue #13 portrait-selection patcher.

This validator does not modify files. It checks that the exact-context patcher
still matches the current `game/scripts/core/main.gd` shape before the runtime
patch lands. After the runtime patch lands, it accepts the already-applied state
when the matching portrait-selection scenario exists.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAIN_GD = ROOT / "game" / "scripts" / "core" / "main.gd"
PATCHER = ROOT / "tools" / "apply_issue_13_portrait_selection_patch.py"
SCENARIO = ROOT / "tests" / "scenarios" / "character_creator_portrait_selection.json"


class PatcherParseError(RuntimeError):
    pass


def _literal_arg(call: ast.Call, index: int) -> Any:
    try:
        return ast.literal_eval(call.args[index])
    except (IndexError, ValueError, TypeError) as exc:
        raise PatcherParseError(f"Could not read literal argument {index} for replace_once call") from exc


def _extract_replace_contexts() -> list[tuple[str, str]]:
    tree = ast.parse(PATCHER.read_text(encoding="utf-8"), filename=str(PATCHER))
    contexts: list[tuple[str, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "replace_once":
            continue
        before = _literal_arg(node, 1)
        label = _literal_arg(node, 3)
        if not isinstance(before, str) or not isinstance(label, str):
            raise PatcherParseError("replace_once before/label arguments must be string literals")
        contexts.append((label, before))
    if not contexts:
        raise PatcherParseError("No replace_once contexts found in Issue #13 patcher")
    return contexts


def _is_runtime_patch_applied(content: str) -> bool:
    return "PortraitCatalog" in content and "portrait_options" in content and "select_portrait" in content


def main() -> int:
    errors: list[str] = []
    if not MAIN_GD.exists():
        errors.append(f"Missing file: {MAIN_GD.relative_to(ROOT)}")
    if not PATCHER.exists():
        errors.append(f"Missing file: {PATCHER.relative_to(ROOT)}")
    if errors:
        print("Issue #13 patcher validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    main_content = MAIN_GD.read_text(encoding="utf-8")
    if _is_runtime_patch_applied(main_content):
        if not SCENARIO.exists():
            print("Issue #13 patcher validation failed:")
            print(f"  - Runtime patch appears applied, but scenario is missing: {SCENARIO.relative_to(ROOT)}")
            return 1
        print("Issue #13 patcher validation passed: runtime patch already applied and scenario exists.")
        return 0

    try:
        contexts = _extract_replace_contexts()
    except PatcherParseError as exc:
        print("Issue #13 patcher validation failed:")
        print(f"  - {exc}")
        return 1

    for label, before in contexts:
        count = main_content.count(before)
        if count != 1:
            errors.append(f"Context '{label}' expected 1 match in {MAIN_GD.relative_to(ROOT)}, found {count}")

    if errors:
        print("Issue #13 patcher validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Issue #13 patcher validation passed: {len(contexts)} exact contexts match current main.gd.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
