#!/usr/bin/env python3
"""Validate Wolfpine generated batch scorecards and evidence links."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
GENERATED_ROOT = ROOT / "assets" / "generated"

CATEGORY_WEIGHTS: dict[str, int] = {
    "camera consistency": 20,
    "silhouette readability at target scale": 20,
    "modular seam compatibility": 15,
    "lighting/shadow coherence": 15,
    "material/palette consistency": 10,
    "gameplay affordance clarity": 10,
    "cleanup/alpha integrity": 10,
}

HEADER_ALIASES: dict[str, tuple[str, ...]] = {
    "asset_id": ("asset", "asset id", "asset_id", "candidate", "candidate id"),
    "weighted_total": ("weighted total", "total", "weighted score", "score"),
    "seam_evidence": ("seam evidence", "seam test", "modular seam evidence", "seam path"),
    "scale_evidence": ("scale evidence", "scale check", "scale path", "readability evidence"),
    "promoted": ("promoted", "promotion", "promote"),
    "manifest_ref": ("manifest", "manifest ref", "manifest path", "manifest reference"),
}

MARKDOWN_LINK_RE = re.compile(r"^\s*\[[^\]]+\]\(([^)]+)\)\s*$")
URL_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def parse_markdown_table(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    rows: list[dict[str, str]] = []

    for idx in range(len(lines) - 1):
        header_line = lines[idx].strip()
        separator_line = lines[idx + 1].strip()
        if not (header_line.startswith("|") and header_line.endswith("|")):
            continue
        if "|" not in separator_line or "-" not in separator_line:
            continue

        headers = [cell.strip() for cell in header_line.strip("|").split("|")]
        for row in lines[idx + 2 :]:
            row = row.strip()
            if not row.startswith("|"):
                break
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            if len(cells) != len(headers):
                continue
            if all(not c for c in cells):
                continue
            rows.append(dict(zip(headers, cells, strict=False)))
        if rows:
            return rows
    return rows


def resolve_header_key(row: dict[str, str], logical_key: str) -> str | None:
    aliases = HEADER_ALIASES[logical_key]
    for key in row:
        nk = normalize(key)
        if nk in aliases:
            return key
    return None


def parse_float(value: str) -> float | None:
    stripped = value.strip().replace("%", "")
    try:
        return float(stripped)
    except ValueError:
        return None


def extract_evidence_target(value: str) -> str:
    """Return the path/URL target from a scorecard evidence cell.

    Accepts plain relative paths and markdown links. URLs are considered valid
    external evidence references, but blank cells are always invalid.
    """

    stripped = value.strip()
    if not stripped:
        return ""

    match = MARKDOWN_LINK_RE.match(stripped)
    if match:
        stripped = match.group(1).strip()

    # Drop optional markdown title from `[x](path "title")`.
    if " " in stripped and not URL_SCHEME_RE.match(stripped):
        stripped = stripped.split(" ", 1)[0].strip()

    return stripped


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def check_path_exists(base_dir: Path, value: str) -> bool:
    target = extract_evidence_target(value)
    if not target:
        return False

    if is_url(target):
        return True

    candidate = Path(target)
    if candidate.is_absolute():
        return candidate.exists()
    if ".." in candidate.parts:
        return False
    return (base_dir / candidate).exists() or (ROOT / candidate).exists()


def validate_batch(batch_dir: Path) -> list[str]:
    errors: list[str] = []
    required_files = ["README.md", "scorecard_review.md"]

    for name in required_files:
        required_path = batch_dir / name
        if not required_path.exists():
            errors.append(f"[{batch_dir.name}] [batch] Missing required file: {rel(required_path)}")

    asset_files = [p for p in batch_dir.iterdir() if p.is_file() and p.name not in required_files]
    if not asset_files:
        errors.append(f"[{batch_dir.name}] [batch] No asset files found in {rel(batch_dir)}")

    scorecard_path = batch_dir / "scorecard_review.md"
    if not scorecard_path.exists():
        return errors

    rows = parse_markdown_table(scorecard_path)
    if not rows:
        errors.append(f"[{batch_dir.name}] [scorecard] Could not parse markdown table from {rel(scorecard_path)}")
        return errors

    first = rows[0]
    required_cols = ["asset_id", "weighted_total", "seam_evidence", "scale_evidence"]
    resolved = {k: resolve_header_key(first, k) for k in required_cols + ["promoted", "manifest_ref"]}
    missing = [k for k in required_cols if resolved[k] is None]
    if missing:
        errors.append(f"[{batch_dir.name}] [scorecard] Missing required columns: {', '.join(missing)}")
        return errors

    category_cols: dict[str, str] = {}
    for category in CATEGORY_WEIGHTS:
        for key in first:
            if normalize(key) == category:
                category_cols[category] = key
                break
    if len(category_cols) != len(CATEGORY_WEIGHTS):
        missing_categories = [c for c in CATEGORY_WEIGHTS if c not in category_cols]
        errors.append(
            f"[{batch_dir.name}] [scorecard] Missing category columns: {', '.join(missing_categories)}"
        )
        return errors

    for row in rows:
        asset_id = row.get(resolved["asset_id"] or "", "").strip() or "UNKNOWN_ASSET"
        row_errors_prefix = f"[{batch_dir.name}] [{asset_id}]"

        cat_values: dict[str, float] = {}
        for category, header in category_cols.items():
            raw = row.get(header, "")
            value = parse_float(raw)
            if value is None:
                errors.append(f"{row_errors_prefix} Category '{category}' must be numeric, got: {raw!r}")
                continue
            cat_values[category] = value
            if value < 70:
                errors.append(f"{row_errors_prefix} Category '{category}' below floor: {value:.2f} < 70")

        raw_total = row.get(resolved["weighted_total"] or "", "")
        total = parse_float(raw_total)
        if total is None:
            errors.append(f"{row_errors_prefix} Weighted total must be numeric, got: {raw_total!r}")
            continue

        computed = sum(cat_values.get(cat, 0.0) * wt / 100 for cat, wt in CATEGORY_WEIGHTS.items())
        if len(cat_values) == len(CATEGORY_WEIGHTS) and abs(computed - total) > 0.25:
            errors.append(
                f"{row_errors_prefix} Weighted total mismatch: listed {total:.2f}, computed {computed:.2f}"
            )

        if total < 85:
            errors.append(f"{row_errors_prefix} Threshold failure: weighted total {total:.2f} < 85")

        seam = row.get(resolved["seam_evidence"] or "", "")
        if not check_path_exists(batch_dir, seam):
            errors.append(f"{row_errors_prefix} Missing seam-test evidence path/link: {seam!r}")

        scale = row.get(resolved["scale_evidence"] or "", "")
        if not check_path_exists(batch_dir, scale):
            errors.append(f"{row_errors_prefix} Missing scale-check evidence path/link: {scale!r}")

        promoted_flag = row.get(resolved["promoted"] or "", "").strip().lower()
        if promoted_flag in {"yes", "true", "promoted", "1"}:
            manifest_ref = row.get(resolved["manifest_ref"] or "", "").strip()
            if not manifest_ref:
                errors.append(f"{row_errors_prefix} Promoted asset missing manifest reference")
            elif not check_path_exists(batch_dir, manifest_ref):
                errors.append(f"{row_errors_prefix} Manifest reference does not exist: {manifest_ref!r}")

    return errors


def iter_batch_dirs(batch_ids: list[str]) -> list[Path]:
    if batch_ids:
        return [GENERATED_ROOT / batch_id for batch_id in batch_ids]
    if not GENERATED_ROOT.exists():
        return []
    return sorted(path for path in GENERATED_ROOT.iterdir() if path.is_dir())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_id", nargs="*", help="Batch IDs under assets/generated to validate")
    args = parser.parse_args()

    batches = iter_batch_dirs(args.batch_id)
    if not batches:
        print("No generated batches found to validate.")
        return 1

    errors: list[str] = []
    checked = 0
    for batch_dir in batches:
        if not batch_dir.exists() or not batch_dir.is_dir():
            errors.append(f"[{batch_dir.name}] [batch] Batch directory missing: {rel(batch_dir)}")
            continue
        checked += 1
        errors.extend(validate_batch(batch_dir))

    if errors:
        print("Wolfpine pipeline validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Wolfpine pipeline validation passed for {checked} batch(es).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
