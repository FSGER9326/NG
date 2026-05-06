#!/usr/bin/env python3
"""Validate Wolfpine PR readiness markers in changed batch markdown docs."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_DOC_PREFIX = "assets/kits/wolfpine_village/"
BATCH_DOC_NAME_HINTS = ("BATCH", "PROMOTION", "REVIEW")

REQUIRED_MARKERS = (
    "- [x] validator command passed",
    "- [x] scorecard evidence complete",
    "- [x] required validation scenes referenced",
    "- [x] seam compatibility checked",
    "- [x] elevation transition checked",
    "- [x] gameplay-scale readability checked",
    "- [x] manifest status transitions valid",
    "- [x] unresolved blocked assets listed",
)


def run_capture(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"Command failed: {' '.join(command)}")
    return result.stdout


def changed_files(base_ref: str) -> list[Path]:
    out = run_capture(["git", "diff", "--name-only", "--diff-filter=d", f"{base_ref}...HEAD"])
    files: list[Path] = []
    for line in out.splitlines():
        line = line.strip()
        if line:
            files.append(Path(line))
    return files


def is_batch_doc(path: Path) -> bool:
    as_posix = path.as_posix()
    if not as_posix.startswith(BATCH_DOC_PREFIX):
        return False
    if path.suffix.lower() != ".md":
        return False
    name = path.name.upper()
    return any(hint in name for hint in BATCH_DOC_NAME_HINTS)


def marker_present(content: str, marker: str) -> bool:
    return marker in content or marker.replace("[x]", "[X]") in content


def validate_doc(path: Path) -> list[str]:
    content = (ROOT / path).read_text(encoding="utf-8")
    missing: list[str] = []
    for marker in REQUIRED_MARKERS:
        if not marker_present(content, marker):
            missing.append(marker)
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-ref", default="origin/main", help="Base ref for changed-file detection")
    parser.add_argument("--files", nargs="*", help="Explicit markdown files to validate")
    args = parser.parse_args()

    if args.files:
        candidates = [Path(p) for p in args.files]
    else:
        candidates = [p for p in changed_files(args.base_ref) if is_batch_doc(p)]

    if not candidates:
        print("No changed Wolfpine batch docs detected; nothing to validate.")
        return 0

    failures = 0
    for relative_path in candidates:
        absolute = ROOT / relative_path
        if not absolute.exists():
            # Explicit --files may include missing paths; auto-detected deletions are filtered before this point.
            print(f"FAIL: {relative_path} does not exist")
            failures += 1
            continue
        missing = validate_doc(relative_path)
        if missing:
            failures += 1
            print(f"FAIL: {relative_path} is missing required readiness markers:")
            for marker in missing:
                print(f"  - {marker}")
        else:
            print(f"PASS: {relative_path}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
