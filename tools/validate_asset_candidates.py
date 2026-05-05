#!/usr/bin/env python3
"""Validate NG asset candidate ledgers.

Candidate ledgers track generated/sourced art before promotion into canonical kit
paths. Validation keeps source notes, status, batch references, and target files
consistent.

Usage:
    python tools/validate_asset_candidates.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_ROOT = ROOT / "data" / "asset_candidates"
BATCH_ROOT = ROOT / "data" / "asset_batches"
KIT_ROOT = ROOT / "data" / "asset_kits"

TOP_LEVEL_REQUIRED = {
    "id",
    "name",
    "target_area",
    "target_kit",
    "purpose",
    "source_policy",
    "candidate_statuses",
    "required_candidate_fields",
    "candidates",
}

SOURCE_POLICY_REQUIRED = {
    "allowed_source_types",
    "disallowed_source_types",
    "notes",
}

CANDIDATE_REQUIRED = {
    "asset_id",
    "batch_id",
    "candidate_id",
    "status",
    "source_type",
    "source_notes",
    "candidate_file",
    "target_file",
    "cleanup_notes",
    "review_notes",
}

DEFAULT_ALLOWED_STATUSES = {
    "candidate_needed",
    "candidate_generated",
    "needs_cleanup",
    "needs_review",
    "accepted_for_kit",
    "rejected",
}

PROMOTION_STATUSES = {"accepted_for_kit"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def as_text_list(value: Any) -> list[str]:
    return [item for item in as_list(value) if isinstance(item, str)]


def ledger_files() -> list[Path]:
    if not CANDIDATE_ROOT.exists():
        return []
    return sorted(path for path in CANDIDATE_ROOT.glob("*.json") if path.is_file())


def load_batch_index() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not BATCH_ROOT.exists():
        return result
    for path in sorted(BATCH_ROOT.glob("*.json")):
        data = load_json(path)
        if isinstance(data, dict) and isinstance(data.get("id"), str):
            result[data["id"]] = data
    return result


def load_kit_index() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not KIT_ROOT.exists():
        return result
    for path in sorted(KIT_ROOT.glob("*.json")):
        data = load_json(path)
        if isinstance(data, dict) and isinstance(data.get("id"), str):
            result[data["id"]] = data
    return result


def kit_asset_index(kit: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for asset in as_list(kit.get("assets")):
        if isinstance(asset, dict) and isinstance(asset.get("id"), str):
            result[asset["id"]] = asset
    return result


def batch_asset_index(batches: dict[str, dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for batch_id, batch in batches.items():
        for asset in as_list(batch.get("assets")):
            if isinstance(asset, dict) and isinstance(asset.get("asset_id"), str):
                result[(batch_id, asset["asset_id"])] = asset
    return result


def check_text_list(path: Path, context: str, field: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{rel(path)} {context}: {field} must be a non-empty list")
        return
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{rel(path)} {context}: {field} entries must be non-empty strings")


def check_path_string(path: Path, context: str, field: str, value: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{rel(path)} {context}: {field} must be a non-empty string")
        return
    if not value.startswith(prefix):
        errors.append(f"{rel(path)} {context}: {field} must start with {prefix}")
    if ".." in Path(value).parts:
        errors.append(f"{rel(path)} {context}: {field} must not contain '..'")


def check_ledger(path: Path, data: Any, batches: dict[str, dict[str, Any]], kits: dict[str, dict[str, Any]], errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append(f"{rel(path)}: candidate ledger must be an object")
        return

    missing = sorted(TOP_LEVEL_REQUIRED - set(data.keys()))
    if missing:
        errors.append(f"{rel(path)}: missing required fields: {', '.join(missing)}")

    ledger_id = data.get("id")
    if not isinstance(ledger_id, str) or not ledger_id.strip():
        errors.append(f"{rel(path)}: id must be a non-empty string")

    for field in ("name", "target_area", "target_kit", "purpose"):
        if not isinstance(data.get(field), str) or not data.get(field).strip():
            errors.append(f"{rel(path)}: {field} must be a non-empty string")

    target_kit_id = data.get("target_kit")
    target_kit = kits.get(target_kit_id) if isinstance(target_kit_id, str) else None
    if target_kit is None:
        errors.append(f"{rel(path)}: target_kit references missing kit: {target_kit_id}")
        kit_assets: dict[str, dict[str, Any]] = {}
    else:
        kit_assets = kit_asset_index(target_kit)
        target_area = data.get("target_area")
        if target_kit.get("target_area") != target_area:
            errors.append(f"{rel(path)}: target_area {target_area!r} does not match kit target_area {target_kit.get('target_area')!r}")

    source_policy = data.get("source_policy")
    if not isinstance(source_policy, dict):
        errors.append(f"{rel(path)}: source_policy must be an object")
        allowed_source_types: set[str] = set()
        disallowed_source_types: set[str] = set()
    else:
        missing_policy = sorted(SOURCE_POLICY_REQUIRED - set(source_policy.keys()))
        if missing_policy:
            errors.append(f"{rel(path)}: source_policy missing fields: {', '.join(missing_policy)}")
        check_text_list(path, "source_policy", "allowed_source_types", source_policy.get("allowed_source_types"), errors)
        check_text_list(path, "source_policy", "disallowed_source_types", source_policy.get("disallowed_source_types"), errors)
        if not isinstance(source_policy.get("notes"), str) or not source_policy.get("notes", "").strip():
            errors.append(f"{rel(path)}: source_policy.notes must be non-empty")
        allowed_source_types = set(as_text_list(source_policy.get("allowed_source_types")))
        disallowed_source_types = set(as_text_list(source_policy.get("disallowed_source_types")))
        overlap = allowed_source_types & disallowed_source_types
        if overlap:
            errors.append(f"{rel(path)}: source types cannot be both allowed and disallowed: {', '.join(sorted(overlap))}")

    statuses = set(as_text_list(data.get("candidate_statuses")))
    if not statuses:
        errors.append(f"{rel(path)}: candidate_statuses must be a non-empty string list")
        statuses = DEFAULT_ALLOWED_STATUSES
    missing_default_statuses = DEFAULT_ALLOWED_STATUSES - statuses
    if missing_default_statuses:
        errors.append(f"{rel(path)}: candidate_statuses missing expected statuses: {', '.join(sorted(missing_default_statuses))}")

    required_candidate_fields = set(as_text_list(data.get("required_candidate_fields")))
    missing_required = CANDIDATE_REQUIRED - required_candidate_fields
    if missing_required:
        errors.append(f"{rel(path)}: required_candidate_fields missing: {', '.join(sorted(missing_required))}")

    candidates = data.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        errors.append(f"{rel(path)}: candidates must be a non-empty list")
        return

    batch_assets = batch_asset_index(batches)
    seen_candidate_ids: set[str] = set()
    for index, candidate in enumerate(candidates, start=1):
        if not isinstance(candidate, dict):
            errors.append(f"{rel(path)} candidate #{index}: must be an object")
            continue
        check_candidate(path, index, candidate, statuses, allowed_source_types, disallowed_source_types, batch_assets, kit_assets, seen_candidate_ids, errors)


def check_candidate(
    path: Path,
    index: int,
    candidate: dict[str, Any],
    statuses: set[str],
    allowed_source_types: set[str],
    disallowed_source_types: set[str],
    batch_assets: dict[tuple[str, str], dict[str, Any]],
    kit_assets: dict[str, dict[str, Any]],
    seen_candidate_ids: set[str],
    errors: list[str],
) -> None:
    candidate_id = candidate.get("candidate_id", f"#{index}")
    context = f"candidate {candidate_id}"
    if not isinstance(candidate_id, str) or not candidate_id.strip():
        errors.append(f"{rel(path)} candidate #{index}: candidate_id must be a non-empty string")
        candidate_id = f"#{index}"
    elif candidate_id in seen_candidate_ids:
        errors.append(f"{rel(path)}: duplicate candidate_id: {candidate_id}")
    else:
        seen_candidate_ids.add(candidate_id)

    missing = sorted(CANDIDATE_REQUIRED - set(candidate.keys()))
    if missing:
        errors.append(f"{rel(path)} {context}: missing fields: {', '.join(missing)}")

    asset_id = candidate.get("asset_id")
    batch_id = candidate.get("batch_id")
    if not isinstance(asset_id, str) or not asset_id.strip():
        errors.append(f"{rel(path)} {context}: asset_id must be a non-empty string")
        asset_id = ""
    if not isinstance(batch_id, str) or not batch_id.strip():
        errors.append(f"{rel(path)} {context}: batch_id must be a non-empty string")
        batch_id = ""

    batch_asset = batch_assets.get((batch_id, asset_id))
    if batch_asset is None:
        errors.append(f"{rel(path)} {context}: asset_id {asset_id!r} not found in batch {batch_id!r}")

    kit_asset = kit_assets.get(asset_id)
    if kit_assets and kit_asset is None:
        errors.append(f"{rel(path)} {context}: asset_id {asset_id!r} not found in target kit")

    status = candidate.get("status")
    if status not in statuses:
        errors.append(f"{rel(path)} {context}: invalid status {status!r}")

    source_type = candidate.get("source_type")
    if source_type not in allowed_source_types:
        errors.append(f"{rel(path)} {context}: source_type must be one of allowed source types: {source_type!r}")
    if source_type in disallowed_source_types:
        errors.append(f"{rel(path)} {context}: source_type is disallowed: {source_type!r}")

    source_notes = candidate.get("source_notes")
    if not isinstance(source_notes, str) or len(source_notes.strip()) < 20:
        errors.append(f"{rel(path)} {context}: source_notes must be detailed enough for review")

    check_path_string(path, context, "candidate_file", candidate.get("candidate_file"), "assets/kits/", errors)
    check_path_string(path, context, "target_file", candidate.get("target_file"), "assets/kits/", errors)

    target_file = candidate.get("target_file")
    candidate_file = candidate.get("candidate_file")
    if batch_asset is not None and target_file != batch_asset.get("target_file"):
        errors.append(f"{rel(path)} {context}: target_file must match batch target_file {batch_asset.get('target_file')!r}")
    if kit_asset is not None and target_file != kit_asset.get("intended_file"):
        errors.append(f"{rel(path)} {context}: target_file must match kit intended_file {kit_asset.get('intended_file')!r}")
    if isinstance(candidate_file, str) and isinstance(target_file, str) and candidate_file == target_file:
        errors.append(f"{rel(path)} {context}: candidate_file must be separate from target_file until promotion")

    check_text_list(path, context, "cleanup_notes", candidate.get("cleanup_notes"), errors)
    check_text_list(path, context, "review_notes", candidate.get("review_notes"), errors)

    if status in PROMOTION_STATUSES:
        if not isinstance(candidate_file, str) or not (ROOT / candidate_file).exists():
            errors.append(f"{rel(path)} {context}: accepted candidate_file does not exist: {candidate_file}")
        if not isinstance(target_file, str) or not (ROOT / target_file).exists():
            errors.append(f"{rel(path)} {context}: accepted target_file does not exist: {target_file}")


def main() -> int:
    errors: list[str] = []
    files = ledger_files()
    if not files:
        errors.append("No asset candidate ledgers found under data/asset_candidates/.")

    try:
        batches = load_batch_index()
        kits = load_kit_index()
    except json.JSONDecodeError as exc:
        print(f"Asset candidate validation failed: invalid referenced JSON: {exc}")
        return 1

    for path in files:
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {rel(path)}: {exc}")
            continue
        check_ledger(path, data, batches, kits, errors)

    if errors:
        print("Asset candidate validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Asset candidate validation passed: {len(files)} candidate ledger(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
