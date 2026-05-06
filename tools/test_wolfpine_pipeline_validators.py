#!/usr/bin/env python3
"""Regression checks for Wolfpine asset pipeline validators.

These are dependency-light tests for validator edge cases that caused review
comments: blank evidence bypasses, markdown evidence links, top-level JSON
scorecards, and malformed scorecard rows.
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_tool(path: str):
    spec = importlib.util.spec_from_file_location(Path(path).stem, REPO_ROOT / path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_wolfpine_evidence_paths() -> None:
    tool = load_tool("tools/validate_wolfpine_pipeline.py")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        batch_dir = root / "assets" / "generated" / "wolfpine_test"
        evidence = batch_dir / "evidence" / "seam.png"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("placeholder", encoding="utf-8")

        old_root = tool.ROOT
        try:
            tool.ROOT = root
            assert not tool.check_path_exists(batch_dir, "")
            assert not tool.check_path_exists(batch_dir, "   ")
            assert tool.check_path_exists(batch_dir, "evidence/seam.png")
            assert tool.check_path_exists(batch_dir, "[seam evidence](evidence/seam.png)")
            assert tool.check_path_exists(batch_dir, "https://example.com/evidence/seam.png")
            assert not tool.check_path_exists(batch_dir, "../outside.png")
        finally:
            tool.ROOT = old_root


def test_generated_asset_review_json_shapes() -> None:
    tool = load_tool("tools/validate_generated_assets.py")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        review_path = root / "scorecard_review.json"

        valid_review = {
            "asset_id": "wolfpine_crate_01",
            "weighted_total": "88.5",
            "result": "PASS",
            "seam_test_scene_path": "game/scenes/area/validation/wolfpine_village/wv_modular_corner_cases.tscn",
            "scale_check_note": "Readable at target scale.",
            "reviewer": "pipeline-test",
            "review_date": "2026-05-06",
            "camera_score": "88",
        }

        review_path.write_text(json.dumps([valid_review]), encoding="utf-8")
        errors: list[str] = []
        tool._validate_scorecard_review_json(
            review_path,
            "assets/generated/wolfpine_test/manifest.json",
            {"wolfpine_crate_01"},
            errors,
        )
        assert errors == []

        review_path.write_text(json.dumps(["not an object", valid_review]), encoding="utf-8")
        errors = []
        tool._validate_scorecard_review_json(
            review_path,
            "assets/generated/wolfpine_test/manifest.json",
            {"wolfpine_crate_01"},
            errors,
        )
        assert any("review row must be an object" in error for error in errors)
        assert not any("AttributeError" in error for error in errors)


def main() -> int:
    test_wolfpine_evidence_paths()
    test_generated_asset_review_json_shapes()
    print("Wolfpine pipeline validator regression tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
