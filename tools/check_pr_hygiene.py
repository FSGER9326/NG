#!/usr/bin/env python3
"""Check PR scope hygiene for NG.

This script is intentionally conservative. It does not replace human review;
it catches common project-management mistakes that caused earlier branch drift:
large mixed-scope PRs, runtime/content coupling, and docs-only PRs that touch
more than durable handoff docs.
"""

from __future__ import annotations

import sys
from pathlib import Path

CATEGORY_PREFIXES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("ci", (".github/",)),
    ("docs", ("docs/", "README.md")),
    ("runtime", ("game/",)),
    ("data", ("data/", "dialogue/")),
    ("areas", ("areas/",)),
    ("scenarios", ("tests/scenarios/",)),
    ("tools", ("tools/",)),
    ("assets", ("assets/",)),
)

WARNING_ONLY_CATEGORIES = {"docs", "ci"}
MAX_CHANGED_FILES = 12
MAX_CORE_CATEGORIES = 3


def load_changed_files(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"Changed-file list does not exist: {path}")
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def categorize(path: str) -> str:
    for category, prefixes in CATEGORY_PREFIXES:
        if any(path == prefix.rstrip("/") or path.startswith(prefix) for prefix in prefixes):
            return category
    return "other"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: tools/check_pr_hygiene.py changed_files.txt")
        return 2

    changed_files = load_changed_files(Path(sys.argv[1]))
    categories = {categorize(path) for path in changed_files}
    core_categories = categories - WARNING_ONLY_CATEGORIES
    errors: list[str] = []
    warnings: list[str] = []

    if not changed_files:
        print("No changed files found. Nothing to check.")
        return 0

    if len(changed_files) > MAX_CHANGED_FILES:
        warnings.append(
            f"This PR changes {len(changed_files)} files. Prefer smaller PRs unless this is an intentional cleanup."
        )

    if len(core_categories) > MAX_CORE_CATEGORIES:
        errors.append(
            "This PR mixes too many core categories: "
            + ", ".join(sorted(core_categories))
            + ". Split unrelated runtime/content/tooling changes."
        )

    if "runtime" in categories and ({"data", "areas", "assets"} & categories) and "scenarios" not in categories:
        warnings.append(
            "Runtime changes combined with content/data/assets should usually include scenario coverage."
        )

    if "assets" in categories and "docs" not in categories:
        warnings.append(
            "Asset changes should usually update or reference asset policy/metadata docs."
        )

    if "data" in categories and "scenarios" not in categories and "tools" not in categories:
        warnings.append(
            "Data/content changes should usually include scenario coverage or validation updates."
        )

    if "areas" in categories and "scenarios" not in categories and "tools" not in categories:
        warnings.append(
            "Area changes should usually include scenario coverage or validation updates."
        )

    if "docs" in categories and "docs/PROJECT_STATUS.md" not in changed_files and "docs/ROADMAP.md" not in changed_files:
        if any(path.startswith(("data/", "areas/", "game/", "assets/")) for path in changed_files):
            warnings.append(
                "Behavior/content changes should consider updating PROJECT_STATUS.md or ROADMAP.md."
            )

    print("NG PR hygiene check")
    print("Changed files:")
    for path in changed_files:
        print(f"  - {path} [{categorize(path)}]")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("\nPR hygiene check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
