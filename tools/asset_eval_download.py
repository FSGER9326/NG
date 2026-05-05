#!/usr/bin/env python3
"""Download/stage third-party assets for local evaluation only.

This script reads ``asset_eval/asset_candidates.json`` and downloads only
candidates with a ``direct_download_url``. Candidates marked manual/page review
are listed with their source pages so a human can review license and download
terms first.

Raw third-party downloads should stay under ``asset_eval/downloads`` and should
not be committed to the repository.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "asset_eval" / "asset_candidates.json"
SAFE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_\-]*$")


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage free asset candidates for local evaluation")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Path to asset candidate manifest")
    parser.add_argument("--id", dest="candidate_ids", action="append", default=[], help="Candidate ID to download/list. Can be used multiple times.")
    parser.add_argument("--list", action="store_true", help="List candidates and exit")
    parser.add_argument("--download", action="store_true", help="Download candidates with direct_download_url")
    parser.add_argument("--force", action="store_true", help="Overwrite existing downloads")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    manifest = _read_manifest(manifest_path)
    candidates = manifest.get("candidates", [])
    if not isinstance(candidates, list):
        print("asset manifest error: candidates must be a list", file=sys.stderr)
        return 2

    selected = _select_candidates(candidates, args.candidate_ids)
    if args.list or not args.download:
        _print_candidates(selected)
        if not args.download:
            return 0

    download_dir = ROOT / str(manifest.get("local_download_dir", "asset_eval/downloads"))
    download_dir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for candidate in selected:
        failures += _download_candidate(candidate, download_dir, force=args.force)
    return 1 if failures else 0


def _read_manifest(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"asset manifest not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"asset manifest is invalid JSON: {path}: {exc}")


def _select_candidates(candidates: list[Any], ids: list[str]) -> list[dict[str, Any]]:
    normalized = [candidate for candidate in candidates if isinstance(candidate, dict)]
    if not ids:
        return normalized
    wanted = set(ids)
    selected = [candidate for candidate in normalized if str(candidate.get("id", "")) in wanted]
    found = {str(candidate.get("id", "")) for candidate in selected}
    missing = sorted(wanted - found)
    if missing:
        raise SystemExit(f"unknown asset candidate id(s): {', '.join(missing)}")
    return selected


def _print_candidates(candidates: list[dict[str, Any]]) -> None:
    print("Asset evaluation candidates")
    print("===========================")
    for candidate in candidates:
        candidate_id = str(candidate.get("id", ""))
        name = str(candidate.get("name", ""))
        license_id = str(candidate.get("license", "unknown"))
        priority = candidate.get("priority", "")
        mode = str(candidate.get("download_mode", ""))
        direct = str(candidate.get("direct_download_url", ""))
        source_page = str(candidate.get("source_page_url", ""))
        print(f"- {candidate_id}: {name} [{license_id}] priority={priority} mode={mode}")
        if direct:
            print(f"  direct: {direct}")
        elif source_page:
            print(f"  review/download page: {source_page}")


def _download_candidate(candidate: dict[str, Any], download_dir: Path, force: bool = False) -> int:
    candidate_id = str(candidate.get("id", "")).strip()
    if not SAFE_ID_PATTERN.match(candidate_id):
        print(f"skip invalid candidate id: {candidate_id!r}", file=sys.stderr)
        return 1

    url = str(candidate.get("direct_download_url", "")).strip()
    if not url:
        print(f"manual review required: {candidate_id} -> {candidate.get('source_page_url', '')}")
        return 0

    extension = _guess_extension(url)
    target = download_dir / f"{candidate_id}{extension}"
    if target.exists() and not force:
        print(f"already downloaded: {target}")
        return 0

    print(f"downloading {candidate_id}: {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "NG asset evaluation downloader"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
    except urllib.error.URLError as exc:
        print(f"download failed for {candidate_id}: {exc}", file=sys.stderr)
        return 1

    target.write_bytes(data)
    _write_receipt(candidate, target)
    print(f"saved: {target} ({len(data)} bytes)")
    return 0


def _guess_extension(url: str) -> str:
    lower = url.lower().split("?", 1)[0]
    for extension in (".zip", ".7z", ".tar.gz", ".tgz", ".png", ".ogg", ".wav"):
        if lower.endswith(extension):
            return extension
    return ".download"


def _write_receipt(candidate: dict[str, Any], target: Path) -> None:
    receipt = {
        "candidate_id": candidate.get("id", ""),
        "name": candidate.get("name", ""),
        "source": candidate.get("source", ""),
        "source_page_url": candidate.get("source_page_url", ""),
        "direct_download_url": candidate.get("direct_download_url", ""),
        "license": candidate.get("license", "unknown"),
        "downloaded_file": target.name,
    }
    target.with_suffix(target.suffix + ".receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
