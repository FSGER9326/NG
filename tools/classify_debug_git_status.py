#!/usr/bin/env python3
"""Classify git-status noise inside NG debug reports.

The one-click report scripts intentionally regenerate files under
``debug_reports/latest`` and archive each run under ``debug_reports/runs``.
When those reports are captured mid-regeneration or alongside local Godot
executables, ``git_status.txt`` can look alarming even though the game failure
is elsewhere.

This helper reads a report's ``git_status.txt`` and separates expected report
churn from actionable workspace changes.
"""

from __future__ import annotations

import argparse
from pathlib import Path

EXPECTED_REPORT_PREFIXES = (
    "debug_reports/latest/",
    "debug_reports/runs/",
    "debug/latest/",
    "debug/",
)

EXPECTED_LOCAL_PATTERNS = (
    "Godot_v",
    "Godot.exe",
    "Godot_console.exe",
    "Godot_*_console.exe",
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify a debug report git_status.txt file")
    parser.add_argument(
        "path",
        nargs="?",
        default="debug_reports/latest",
        help="Debug report directory or git_status.txt path. Defaults to debug_reports/latest.",
    )
    args = parser.parse_args()

    status_path = _resolve_status_path(Path(args.path))
    if not status_path.exists():
        print(f"No git_status.txt found at {status_path}")
        return 2

    expected_report: list[str] = []
    expected_local: list[str] = []
    actionable: list[str] = []

    for raw_line in status_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        path = _status_path(line)
        if _is_expected_report_path(path):
            expected_report.append(line)
        elif _is_expected_local_path(path):
            expected_local.append(line)
        else:
            actionable.append(line)

    print("Debug git status classification")
    print("===============================")
    print(f"Source: {status_path}")
    _print_group("Expected report churn", expected_report)
    _print_group("Expected local tools", expected_local)
    _print_group("Actionable workspace changes", actionable)

    if actionable:
        return 1
    return 0


def _resolve_status_path(path: Path) -> Path:
    if path.name == "git_status.txt":
        return path
    return path / "git_status.txt"


def _status_path(line: str) -> str:
    # Git porcelain lines are typically "XY path" or "?? path".
    # Rename entries can contain "old -> new"; for classification, the right
    # side is usually the path that matters.
    value = line[3:].strip() if len(line) > 3 else line.strip()
    if " -> " in value:
        value = value.split(" -> ", 1)[1].strip()
    return value.replace("\\", "/")


def _is_expected_report_path(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in EXPECTED_REPORT_PREFIXES)


def _is_expected_local_path(path: str) -> bool:
    name = Path(path).name
    if name.startswith("Godot_v") and name.endswith(".exe"):
        return True
    return name in EXPECTED_LOCAL_PATTERNS


def _print_group(title: str, lines: list[str]) -> None:
    print(f"\n{title}: {len(lines)}")
    for line in lines[:40]:
        print(f"- {line}")
    if len(lines) > 40:
        print(f"- ... {len(lines) - 40} more")


if __name__ == "__main__":
    raise SystemExit(main())
