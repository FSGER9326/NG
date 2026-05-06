#!/usr/bin/env python3
"""Prepare a local PR branch for the first Wolfpine binary promotion.

Run this from a local checkout with the first-promotion ZIP available. It creates
or reuses a branch, runs the checked-in promotion wrapper with `--commit`, then
optionally pushes the branch and prints a GitHub CLI PR command.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BRANCH = "assets/promote-wolfpine-first-cleaned-pngs"
DEFAULT_BASE = "main"
WRAPPER = "tools/promote_wolfpine_first_binary_slice.py"
PR_TITLE = "Promote first Wolfpine cleaned PNG assets"

PR_BODY = """## Type of change

- [x] Asset pipeline
- [x] Art/assets

## Summary

Promotes the first five Wolfpine PNGs from the reviewed promotion bundle into canonical kit paths as `cleaned` assets.

Promoted files:

- `assets/kits/wolfpine_village/props/wolfpine_well_01.png`
- `assets/kits/wolfpine_village/props/wolfpine_notice_board_01.png`
- `assets/kits/wolfpine_village/architecture/wolfpine_door_heavy_01.png`
- `assets/kits/wolfpine_village/architecture/wolfpine_window_shuttered_01.png`
- `assets/kits/wolfpine_village/props/wolfpine_firewood_stack_01.png`

Also updates `data/asset_kits/wolfpine_village_starter.json`.

These assets remain `cleaned`, not `accepted`. Acceptance still requires Godot visual/layout review and an accepted review outcome.
"""


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(command))
    result = subprocess.run(command, cwd=ROOT, text=True, check=False)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {' '.join(command)}")
    return result


def output(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"Command failed: {' '.join(command)}")
    return result.stdout.strip()


def ensure_clean(allow_dirty: bool) -> None:
    status = output(["git", "status", "--short"])
    if status and not allow_dirty:
        print(status)
        raise RuntimeError("Working tree is not clean. Commit/stash changes or pass --allow-dirty.")


def checkout_branch(branch: str, base: str, reuse_branch: bool) -> None:
    existing = output(["git", "branch", "--list", branch])
    if existing:
        if not reuse_branch:
            raise RuntimeError(f"Branch already exists: {branch}. Pass --reuse-branch to use it.")
        run(["git", "checkout", branch])
        return
    run(["git", "checkout", base])
    run(["git", "pull", "--ff-only", "origin", base])
    run(["git", "checkout", "-b", branch])


def print_pr_command(branch: str, base: str) -> None:
    body = PR_BODY.replace("'", "'\\''")
    print("\nPush and open the PR with:")
    print(f"git push -u origin {branch}")
    print(f"gh pr create --base {base} --head {branch} --title '{PR_TITLE}' --body '{body}'")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", required=True, help="Path to the optimized first-promotion ZIP.")
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--reuse-branch", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    zip_path = Path(args.zip).expanduser().resolve()
    if not zip_path.exists():
        print(f"ZIP does not exist: {zip_path}", file=sys.stderr)
        return 1

    try:
        ensure_clean(args.allow_dirty)
        checkout_branch(args.branch, args.base, args.reuse_branch)
        run([sys.executable, WRAPPER, "--zip", str(zip_path), "--commit"])
        if args.push:
            run(["git", "push", "-u", "origin", args.branch])
        print_pr_command(args.branch, args.base)
    except RuntimeError as exc:
        print(f"Failed to prepare Wolfpine binary promotion PR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
