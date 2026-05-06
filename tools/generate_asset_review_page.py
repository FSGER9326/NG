#!/usr/bin/env python3
"""Generate a local HTML review page for NG asset review gates.

The generated page is intentionally local-only. It helps reviewers inspect
promoted PNGs beside their review-gate checks and pending outcome notes before
moving any asset from `cleaned` to `accepted`.

Example:
    python tools/generate_asset_review_page.py \
      --review data/asset_reviews/wolfpine_first_cleaned_review_2026_05_06.json \
      --out build/wolfpine_first_cleaned_review.html
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REVIEW = ROOT / "data" / "asset_reviews" / "wolfpine_first_cleaned_review_2026_05_06.json"
DEFAULT_OUT = ROOT / "build" / "asset_reviews" / "wolfpine_first_cleaned_review_2026_05_06.html"
OUTCOME_ROOT = ROOT / "data" / "asset_review_outcomes"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def repo_relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def safe_text(value: Any) -> str:
    return html.escape(str(value) if value is not None else "")


def list_items(items: Any) -> str:
    if not isinstance(items, list) or not items:
        return "<p class='muted'>None recorded.</p>"
    return "<ul>" + "".join(f"<li>{safe_text(item)}</li>" for item in items) + "</ul>"


def load_outcomes_for_review(review_path: Path) -> dict[str, dict[str, Any]]:
    if not OUTCOME_ROOT.exists():
        return {}
    review_rel = repo_relative(review_path)
    outcomes: dict[str, dict[str, Any]] = {}
    for path in sorted(OUTCOME_ROOT.glob("*.json")):
        try:
            data = load_json(path)
        except json.JSONDecodeError:
            continue
        if data.get("review_gate") != review_rel:
            continue
        for asset in data.get("assets", []):
            if isinstance(asset, dict) and isinstance(asset.get("asset_id"), str):
                outcomes[asset["asset_id"]] = asset
    return outcomes


def asset_card(asset: dict[str, Any], outcome: dict[str, Any] | None) -> str:
    asset_id = str(asset.get("asset_id", "unknown_asset"))
    intended_file = str(asset.get("intended_file", ""))
    image_path = ROOT / intended_file
    image_exists = image_path.exists()
    image_src = repo_relative(image_path) if image_exists else ""
    outcome_value = outcome.get("outcome") if outcome else "no outcome"
    checks_passed = outcome.get("checks_passed") if outcome else False

    image_html = (
        f"<img src='../../{html.escape(image_src)}' alt='{safe_text(asset_id)}'>"
        if image_exists
        else "<div class='missing'>PNG not found in local checkout yet</div>"
    )

    return f"""
    <section class='card'>
      <div class='preview'>{image_html}</div>
      <div class='details'>
        <h2>{safe_text(asset_id)}</h2>
        <p><strong>Path:</strong> <code>{safe_text(intended_file)}</code></p>
        <p><strong>SHA256:</strong> <code>{safe_text(asset.get('expected_sha256'))}</code></p>
        <p><strong>Recommended layer:</strong> {safe_text(asset.get('recommended_layer'))}</p>
        <p><strong>Recommended use:</strong> {safe_text(asset.get('recommended_use'))}</p>
        <p><strong>Outcome:</strong> <span class='badge'>{safe_text(outcome_value)}</span>
           <strong>Checks passed:</strong> <span class='badge'>{safe_text(checks_passed)}</span></p>
        <h3>Specific review checks</h3>
        {list_items(asset.get('specific_review_checks'))}
        <h3>Accepted only if</h3>
        {list_items(asset.get('accepted_only_if'))}
        <h3>Recorded issues</h3>
        {list_items(outcome.get('issues') if outcome else [])}
        <h3>Recorded follow-ups</h3>
        {list_items(outcome.get('followups') if outcome else [])}
      </div>
    </section>
    """


def build_page(review_path: Path) -> str:
    data = load_json(review_path)
    outcomes = load_outcomes_for_review(review_path)
    assets = [asset for asset in data.get("assets", []) if isinstance(asset, dict)]

    cards = "\n".join(asset_card(asset, outcomes.get(asset.get("asset_id"))) for asset in assets)
    return f"""<!doctype html>
<html lang='en'>
<head>
<meta charset='utf-8'>
<title>{safe_text(data.get('name', 'Asset Review'))}</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 2rem; background: #1f211f; color: #eee5d0; }}
  header {{ max-width: 1100px; margin-bottom: 2rem; }}
  .muted {{ color: #b8ad97; }}
  code {{ background: #2d302d; padding: 0.1rem 0.25rem; border-radius: 0.25rem; }}
  .card {{ display: grid; grid-template-columns: 320px 1fr; gap: 1.5rem; max-width: 1200px; margin: 0 0 1.5rem; padding: 1rem; background: #292c29; border: 1px solid #474236; border-radius: 0.75rem; }}
  .preview {{ min-height: 240px; display: flex; align-items: center; justify-content: center; background: #777; border-radius: 0.5rem; background-image: linear-gradient(45deg, #555 25%, transparent 25%), linear-gradient(-45deg, #555 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #555 75%), linear-gradient(-45deg, transparent 75%, #555 75%); background-size: 24px 24px; background-position: 0 0, 0 12px, 12px -12px, -12px 0px; }}
  img {{ max-width: 300px; max-height: 300px; object-fit: contain; filter: drop-shadow(0 12px 16px rgba(0,0,0,.45)); }}
  .missing {{ color: #f2d28a; padding: 1rem; text-align: center; }}
  .badge {{ display: inline-block; margin: 0 .5rem .25rem 0; padding: .15rem .5rem; background: #3b3f3a; border: 1px solid #665f4d; border-radius: 999px; }}
  h1, h2, h3 {{ color: #f4d899; }}
  li {{ margin: .25rem 0; }}
</style>
</head>
<body>
<header>
  <h1>{safe_text(data.get('name'))}</h1>
  <p>{safe_text(data.get('purpose'))}</p>
  <p><strong>Review gate:</strong> <code>{safe_text(repo_relative(review_path))}</code></p>
  <p><strong>Target area:</strong> {safe_text(data.get('target_area'))}</p>
  <h2>Global review checks</h2>
  {list_items(data.get('global_review_checks'))}
</header>
{cards}
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", default=str(DEFAULT_REVIEW), help="Asset review gate JSON path")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output HTML path")
    args = parser.parse_args()

    review_path = Path(args.review).expanduser()
    if not review_path.is_absolute():
        review_path = ROOT / review_path
    out_path = Path(args.out).expanduser()
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    if not review_path.exists():
        raise SystemExit(f"Review gate not found: {review_path}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_page(review_path), encoding="utf-8")
    print(f"Wrote {repo_relative(out_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
