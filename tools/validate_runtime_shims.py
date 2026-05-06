#!/usr/bin/env python3
"""Validate runtime shim files used by the Godot entrypoint.

This catches the local-play failure mode where a shim exists but Godot cannot
resolve the target script path. The check is intentionally text-first and does
not require Godot to be installed.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SHIMS = {
    "game/scripts/core/main.gd": {
        "target": "res://game/scripts/core/main_runtime.gd",
        "allowed_forms": (
            'extends "res://game/scripts/core/main_runtime.gd"',
            'extends preload("res://game/scripts/core/main_runtime.gd")',
        ),
    },
    "game/scripts/core/main_runtime.gd": {
        "target": "res://game/scripts/core/main_runtime_v3.gd",
        "allowed_forms": (
            'extends preload("res://game/scripts/core/main_runtime_v3.gd")',
        ),
        "rejected_forms": (
            'extends "res://game/scripts/core/main_runtime_v3.gd"',
            'extends "res://game/scripts/core/main_runtime_v2.gd"',
        ),
    },
    "game/scripts/core/main_runtime_v3.gd": {
        "target": "res://game/scripts/core/main_runtime_v2.gd",
        "allowed_forms": (
            'extends preload("res://game/scripts/core/main_runtime_v2.gd")',
        ),
        "rejected_forms": (
            'extends "res://game/scripts/core/main_runtime_v2.gd"',
        ),
    },
}

MAIN_SCENE = ROOT / "game" / "scenes" / "main.tscn"
EXPECTED_MAIN_SCENE_SCRIPT = "res://game/scripts/core/main_runtime.gd"


def main() -> int:
    errors: list[str] = []

    if not MAIN_SCENE.exists():
        errors.append("missing main scene: game/scenes/main.tscn")
    else:
        scene_content = MAIN_SCENE.read_text(encoding="utf-8")
        if EXPECTED_MAIN_SCENE_SCRIPT not in scene_content:
            errors.append(
                "main.tscn should point at the stable runtime shim "
                f"{EXPECTED_MAIN_SCENE_SCRIPT}"
            )

    for relative_path, spec in SHIMS.items():
        shim_path = ROOT / relative_path
        if not shim_path.exists():
            errors.append(f"missing runtime shim: {relative_path}")
            continue
        content = shim_path.read_text(encoding="utf-8").strip().splitlines()[0]
        allowed_forms: tuple[str, ...] = spec["allowed_forms"]
        if content not in allowed_forms:
            errors.append(
                f"{relative_path} has unexpected shim content: {content!r}; "
                f"expected one of {allowed_forms!r}"
            )
        for rejected in spec.get("rejected_forms", ()):
            if rejected in content:
                errors.append(f"{relative_path} uses rejected shim form: {rejected}")
        target = str(spec["target"])
        if not target.startswith("res://"):
            errors.append(f"{relative_path} target is not a res:// path: {target}")
            continue
        target_path = ROOT / target.removeprefix("res://")
        if not target_path.exists():
            errors.append(f"{relative_path} target does not exist: {target}")

    if errors:
        print("Runtime shim validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Runtime shim validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
