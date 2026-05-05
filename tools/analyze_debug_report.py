#!/usr/bin/env python3
"""Summarize NG debug reports for quick remote triage.

Usage examples:

    python tools/analyze_debug_report.py
    python tools/analyze_debug_report.py debug/latest
    python tools/analyze_debug_report.py debug_reports/latest
    python tools/analyze_debug_report.py debug/NG_debug_latest.zip

The script is intentionally lightweight: it only reads text/JSON files already
produced by the local debug scripts and prints a concise issue summary.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable

DEFAULT_CANDIDATES = (
    Path("debug/latest"),
    Path("debug_reports/latest"),
)

IMPORTANT_FILES = (
    "validation.log",
    "scenario.log",
    "manual_play_stdout.log",
    "game.log",
    "actions.jsonl",
)

EXIT_CODE_FILES = (
    "validation_exit_code.txt",
    "test_exit_code.txt",
    "game_exit_code.txt",
)

ERROR_PATTERNS = (
    re.compile(r"\bERROR\b", re.IGNORECASE),
    re.compile(r"\bFAILED\b", re.IGNORECASE),
    re.compile(r"SCRIPT ERROR", re.IGNORECASE),
    re.compile(r"Parse Error", re.IGNORECASE),
    re.compile(r"Invalid get index", re.IGNORECASE),
    re.compile(r"Nonexistent function", re.IGNORECASE),
    re.compile(r"Cannot call method", re.IGNORECASE),
    re.compile(r"Traceback", re.IGNORECASE),
)

WARNING_PATTERNS = (
    re.compile(r"\bWARNING\b", re.IGNORECASE),
    re.compile(r"\bWARN\b", re.IGNORECASE),
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize an NG debug report")
    parser.add_argument(
        "path",
        nargs="?",
        help="Report directory or zip file. Defaults to debug/latest, then debug_reports/latest.",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=20,
        help="Maximum issue lines to print per file.",
    )
    args = parser.parse_args()

    try:
        with _resolve_report_path(args.path) as report_dir:
            summary = analyze_report(report_dir, max_lines=args.max_lines)
            print_summary(summary)
            return 1 if summary["high_priority_findings"] else 0
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(f"debug report analysis failed: {exc}", file=sys.stderr)
        return 2


class _ResolvedReport:
    def __init__(self, source: Path, temp_dir: tempfile.TemporaryDirectory[str] | None = None) -> None:
        self.source = source
        self.temp_dir = temp_dir

    def __enter__(self) -> Path:
        return self.source

    def __exit__(self, _exc_type, _exc, _tb) -> None:
        if self.temp_dir is not None:
            self.temp_dir.cleanup()


def _resolve_report_path(path_arg: str | None) -> _ResolvedReport:
    if path_arg:
        path = Path(path_arg)
    else:
        path = next((candidate for candidate in DEFAULT_CANDIDATES if candidate.exists()), DEFAULT_CANDIDATES[0])

    if path.is_file() and path.suffix.lower() == ".zip":
        temp_dir = tempfile.TemporaryDirectory(prefix="ng_debug_report_")
        with zipfile.ZipFile(path, "r") as archive:
            archive.extractall(temp_dir.name)
        extracted = Path(temp_dir.name)
        nested = _find_report_root(extracted)
        return _ResolvedReport(nested, temp_dir)

    if not path.exists():
        raise FileNotFoundError(f"report path not found: {path}")
    if not path.is_dir():
        raise ValueError(f"report path is not a directory or zip file: {path}")
    return _ResolvedReport(path)


def _find_report_root(root: Path) -> Path:
    for candidate in [root, *root.rglob("*")]:
        if candidate.is_dir() and any((candidate / name).exists() for name in IMPORTANT_FILES + EXIT_CODE_FILES):
            return candidate
    return root


def analyze_report(report_dir: Path, max_lines: int = 20) -> dict:
    summary: dict = {
        "report_dir": str(report_dir),
        "metadata": {},
        "exit_codes": {},
        "high_priority_findings": [],
        "warnings": [],
        "file_findings": {},
        "game_flow": {},
    }

    for name in ("git_commit.txt", "git_status.txt", "timestamp.txt", "report_type.txt", "run_id.txt"):
        path = report_dir / name
        if path.exists():
            summary["metadata"][name] = _read_text(path).strip()

    for name in EXIT_CODE_FILES:
        path = report_dir / name
        if not path.exists():
            continue
        value = _read_text(path).strip()
        summary["exit_codes"][name] = value
        if value not in ("", "0"):
            summary["high_priority_findings"].append(f"{name} is non-zero: {value}")

    for name in IMPORTANT_FILES:
        path = report_dir / name
        if not path.exists():
            continue
        findings = _scan_text_file(path, max_lines=max_lines)
        if findings["errors"] or findings["warnings"]:
            summary["file_findings"][name] = findings
            summary["high_priority_findings"].extend(f"{name}: {line}" for line in findings["errors"])
            summary["warnings"].extend(f"{name}: {line}" for line in findings["warnings"])

    actions_path = report_dir / "actions.jsonl"
    if actions_path.exists():
        summary["game_flow"] = _summarize_actions(actions_path)
        if summary["game_flow"].get("started_new_game") and not summary["game_flow"].get("area_runtime_loaded"):
            summary["high_priority_findings"].append(
                "actions.jsonl shows new game start, but no Area runtime load event was logged. "
                "Check scene instantiation, AreaScene readiness, or whether the game exited immediately after Start Journey."
            )

    for state_name in ("state_latest.json", "state_after_scenario.json"):
        path = report_dir / state_name
        if path.exists():
            state_issue = _summarize_state(path)
            if state_issue:
                summary["high_priority_findings"].append(f"{state_name}: {state_issue}")

    return summary


def _scan_text_file(path: Path, max_lines: int) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    for line_number, line in enumerate(_iter_lines(path), start=1):
        clean = line.rstrip()
        if len(errors) < max_lines and any(pattern.search(clean) for pattern in ERROR_PATTERNS):
            errors.append(f"L{line_number}: {clean}")
        elif len(warnings) < max_lines and any(pattern.search(clean) for pattern in WARNING_PATTERNS):
            warnings.append(f"L{line_number}: {clean}")
    return {"errors": errors, "warnings": warnings}


def _summarize_actions(path: Path) -> dict:
    result = {
        "event_count": 0,
        "started_new_game": False,
        "area_runtime_loaded": False,
        "last_event": None,
    }
    for line in _iter_lines(path):
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        result["event_count"] += 1
        result["last_event"] = event
        message = str(event.get("message", ""))
        event_type = str(event.get("type", ""))
        category = str(event.get("category", ""))
        if message == "Started new game" or (category == "GAME" and "Started new game" in message):
            result["started_new_game"] = True
        if category == "AREA" and "Area loaded" in message:
            result["area_runtime_loaded"] = True
        if event_type == "area_rendered" or event_type == "runtime_nodes_built":
            result["area_runtime_loaded"] = True
    return result


def _summarize_state(path: Path) -> str:
    try:
        data = json.loads(_read_text(path))
    except json.JSONDecodeError as exc:
        return f"invalid JSON state dump: {exc}"
    if isinstance(data, dict):
        if data.get("screen") == "game" and not data.get("has_current_area", True):
            return "screen is game, but has_current_area is false"
        if data.get("has_current_area") and not data.get("current_area_id"):
            return "current area exists, but current_area_id is empty"
    return ""


def print_summary(summary: dict) -> None:
    print("NG debug report analysis")
    print("========================")
    print(f"Report: {summary['report_dir']}")

    if summary["metadata"]:
        print("\nMetadata:")
        for key, value in summary["metadata"].items():
            compact = value.replace("\n", "; ")
            print(f"- {key}: {compact}")

    if summary["exit_codes"]:
        print("\nExit codes:")
        for key, value in summary["exit_codes"].items():
            status = "OK" if value in ("", "0") else "FAIL"
            print(f"- {key}: {value} ({status})")

    game_flow = summary.get("game_flow") or {}
    if game_flow:
        print("\nGame flow:")
        print(f"- events logged: {game_flow.get('event_count', 0)}")
        print(f"- started new game: {game_flow.get('started_new_game', False)}")
        print(f"- area runtime loaded: {game_flow.get('area_runtime_loaded', False)}")
        last_event = game_flow.get("last_event")
        if last_event:
            print(f"- last event: {last_event}")

    if summary["high_priority_findings"]:
        print("\nHigh-priority findings:")
        for item in _dedupe(summary["high_priority_findings"]):
            print(f"- {item}")
    else:
        print("\nHigh-priority findings: none detected")

    if summary["warnings"]:
        print("\nWarnings:")
        for item in _dedupe(summary["warnings"]):
            print(f"- {item}")


def _iter_lines(path: Path) -> Iterable[str]:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            yield from handle
    except OSError:
        return


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
