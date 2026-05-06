#!/usr/bin/env python3
"""Validate reference asset layout for NG.

Default mode checks a changed-file list, so it can safely block new PRs from
adding root-level reference clutter even while older uploaded folders are still
being cleaned up.

Use --audit-repo to scan the current checkout and report existing layout debt.
Audit mode exits successfully by default unless --strict is also passed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

CANONICAL_REFERENCE_ROOT = Path("reference_assets/organized/pvgames/infernus_free")

DISALLOWED_ROOT_NAMES = {
    "Building_Infernus_1",
    "Building_Infernus_2",
    "Infernus tiles 1",
    "Infernus tiles 2",
    "Infernus tiles 3",
    "Infernus tiles 4",
    "Infernus tiles 5",
}

DISALLOWED_ROOT_PREFIXES = (
    "PVGames",
    "Pvgames",
    "pvgames",
    "Infernus_",
    "Infernus ",
    "Infernus-",
)

REFERENCE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".bmp",
    ".tga",
    ".psd",
    ".aseprite",
}

ALLOWED_REFERENCE_PREFIXES = (
    "reference_assets/organized/",
    "reference_assets/local/",
    "assets/generated/",
    "assets/kits/",
    "assets/ledger/",
    "asset_eval/",
    "debug_reports/",
)


def normalize(path: str) -> str:
    return path.strip().replace("\\", "/")


def load_changed_files(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"Changed-file list does not exist: {path}")
    return [normalize(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def root_segment(path: str) -> str:
    return path.split("/", 1)[0]


def is_reference_file(path: str) -> bool:
    return Path(path).suffix.lower() in REFERENCE_EXTENSIONS


def is_allowed_reference_path(path: str) -> bool:
    return path.startswith(ALLOWED_REFERENCE_PREFIXES)


def root_name_is_disallowed(root: str) -> bool:
    return root in DISALLOWED_ROOT_NAMES or any(root.startswith(prefix) for prefix in DISALLOWED_ROOT_PREFIXES)


def validate_changed_files(changed_files: list[str]) -> list[str]:
    errors: list[str] = []
    for path in changed_files:
        root = root_segment(path)
        if root_name_is_disallowed(root):
            errors.append(
                f"Reference asset path is at repo root: {path}. Move it under {CANONICAL_REFERENCE_ROOT}/."
            )
            continue
        if is_reference_file(path) and not is_allowed_reference_path(path):
            errors.append(
                f"Binary/reference file is outside an approved asset root: {path}. Use {CANONICAL_REFERENCE_ROOT}/ or assets/generated/."
            )
    return errors


def audit_repo(repo_root: Path) -> list[str]:
    findings: list[str] = []
    for child in sorted(repo_root.iterdir(), key=lambda item: item.name.lower()):
        if not child.is_dir():
            continue
        if root_name_is_disallowed(child.name):
            findings.append(
                f"Root-level reference folder found: {child.name}/. Move it under {CANONICAL_REFERENCE_ROOT}/."
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate NG reference asset layout")
    parser.add_argument("changed_files", nargs="?", type=Path, help="Changed-file list from PR hygiene workflow")
    parser.add_argument("--audit-repo", action="store_true", help="Scan the current checkout for existing root-level reference folders")
    parser.add_argument("--strict", action="store_true", help="Fail audit mode when existing root-level reference folders are found")
    args = parser.parse_args()

    if args.audit_repo:
        findings = audit_repo(Path.cwd())
        print("NG reference asset layout audit")
        if findings:
            print("Findings:")
            for finding in findings:
                print(f"  - {finding}")
            if args.strict:
                return 1
            print("Audit completed with findings. Re-run with --strict to fail on these.")
            return 0
        print("No root-level reference folders found.")
        return 0

    if args.changed_files is None:
        print("Usage: tools/validate_reference_asset_layout.py changed_files.txt", file=sys.stderr)
        return 2

    changed_files = load_changed_files(args.changed_files)
    errors = validate_changed_files(changed_files)
    print("NG reference asset layout check")
    if errors:
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Reference asset layout check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
