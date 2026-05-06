#!/usr/bin/env python3
"""Run the first Wolfpine binary asset promotion from a local handoff ZIP.

This is a convenience wrapper around `tools/promote_asset_candidates.py` for the
first reviewed Wolfpine PNG slice. It performs the safe production sequence:

1. verify the handoff ZIP exists,
2. run promotion dry-run,
3. run promotion write-mode,
4. run relevant validators,
5. show changed files,
6. optionally create a local git commit.

It intentionally keeps promoted assets at `cleaned`; visual review in Godot is
still required before any later `accepted` promotion.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "assets" / "kits" / "wolfpine_village" / "FIRST_BINARY_PROMOTION_2026_05_06.json"
DEFAULT_ZIP = "ng_wolfpine_first_promotion_optimized.zip"
COMMIT_MESSAGE = "Promote first Wolfpine cleaned PNG assets"

VALIDATION_COMMANDS = [
    [sys.executable, "tools/validate_project.py"],
    [sys.executable, "tools/validate_asset_kits.py"],
    [sys.executable, "tools/validate_promoted_asset_files.py"],
    [sys.executable, "tools/validate_asset_production_batches.py"],
    [sys.executable, "tools/validate_asset_promotion_plans.py"],
    [sys.executable, "tools/test_promote_asset_candidates.py"],
]

EXPECTED_PROMOTED_PATHS = [
    "assets/kits/wolfpine_village/props/wolfpine_well_01.png",
    "assets/kits/wolfpine_village/props/wolfpine_notice_board_01.png",
    "assets/kits/wolfpine_village/architecture/wolfpine_door_heavy_01.png",
    "assets/kits/wolfpine_village/architecture/wolfpine_window_shuttered_01.png",
    "assets/kits/wolfpine_village/props/wolfpine_firewood_stack_01.png",
    "data/asset_kits/wolfpine_village_starter.json",
]


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(command))
    result = subprocess.run(command, cwd=ROOT, text=True, check=False)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {' '.join(command)}")
    return result


def ensure_clean_enough_for_promotion(force: bool) -> None:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("Could not inspect git status before promotion")
    if result.stdout.strip() and not force:
        print(result.stdout, end="")
        raise RuntimeError("Working tree has existing changes. Re-run with --allow-dirty to proceed anyway.")


def run_promotion(zip_path: Path) -> None:
    promotion_base = [
        sys.executable,
        "tools/promote_asset_candidates.py",
        "--zip",
        str(zip_path),
        "--plan",
        str(PLAN.relative_to(ROOT)),
    ]
    run([*promotion_base, "--dry-run"])
    run(promotion_base)


def run_validators() -> None:
    for command in VALIDATION_COMMANDS:
        run(command)


def show_changed_files() -> None:
    run(["git", "status", "--short"], check=False)
    run(["git", "diff", "--stat"], check=False)


def check_expected_files_exist() -> None:
    missing = [path for path in EXPECTED_PROMOTED_PATHS if not (ROOT / path).exists()]
    if missing:
        raise RuntimeError("Promotion did not create/update expected paths:\n  - " + "\n  - ".join(missing))


def create_commit() -> None:
    for path in EXPECTED_PROMOTED_PATHS:
        run(["git", "add", path])
    run(["git", "commit", "-m", COMMIT_MESSAGE])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--zip",
        default=DEFAULT_ZIP,
        help="Path to ng_wolfpine_first_promotion_optimized.zip. Defaults to a file beside the repo checkout.",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow running when the working tree already has changes.",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Create a local git commit after successful promotion and validation.",
    )
    args = parser.parse_args()

    zip_path = Path(args.zip).expanduser()
    if not zip_path.is_absolute():
        zip_path = ROOT / zip_path
    zip_path = zip_path.resolve()

    if not zip_path.exists():
        print(f"Handoff ZIP not found: {zip_path}", file=sys.stderr)
        print("Place ng_wolfpine_first_promotion_optimized.zip beside the repo checkout or pass --zip /path/to/file.zip.", file=sys.stderr)
        return 1
    if not PLAN.exists():
        print(f"Promotion plan not found: {PLAN}", file=sys.stderr)
        return 1

    try:
        ensure_clean_enough_for_promotion(args.allow_dirty)
        run_promotion(zip_path)
        check_expected_files_exist()
        run_validators()
        show_changed_files()
        if args.commit:
            create_commit()
            print("Created local commit for first Wolfpine cleaned PNG promotion.")
        else:
            print("Promotion completed and validated. Review the changed files, then commit them when ready.")
    except RuntimeError as exc:
        print(f"Wolfpine binary promotion failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
