#!/usr/bin/env python3
"""Run controlled Meshy API batches for NG source assets.

This script deliberately treats Meshy output as source material. It downloads
GLB files and metadata into asset_sources/raw/meshy/, then delegates final
2.5D sprite rendering to the existing Blender renderer.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
API_BASE = "https://api.meshy.ai"
TEXT_TO_3D_ENDPOINT = "/openapi/v2/text-to-3d"
BALANCE_ENDPOINT = "/openapi/v1/balance"
DEFAULT_BLENDER = Path("C:/Program Files/Blender Foundation/Blender 5.1/blender.exe")
DEFAULT_RAW_ROOT = ROOT / "asset_sources" / "raw" / "meshy"
DEFAULT_RENDER_ROOT = ROOT / "assets" / "generated"
TERMINAL_STATUSES = {"SUCCEEDED", "FAILED", "CANCELED"}


@dataclass(frozen=True)
class AssetSpec:
    asset_id: str
    prompt: str
    texture_prompt: str
    category: str
    priority: int
    should_remesh: bool
    target_polycount: int
    pose_mode: str


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True, help="Meshy batch JSON config.")
    parser.add_argument("--state", type=Path, help="State JSON path. Defaults under asset_sources/raw/meshy/<batch_id>.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--render-root", type=Path, default=DEFAULT_RENDER_ROOT)
    parser.add_argument("--api-key", help="API key. Prefer MESHY_API_KEY environment variable.")
    parser.add_argument("--max-active", type=int, default=0, help="Override config max_active task submissions.")
    parser.add_argument("--poll-seconds", type=int, default=20)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("plan", help="Print batch cost estimate and resolved output paths.")
    subparsers.add_parser("balance", help="Show Meshy credit balance.")
    subparsers.add_parser("submit-previews", help="Submit text-to-3D preview tasks.")
    subparsers.add_parser("watch-previews", help="Poll preview task status until done or one poll pass if --once.")
    subparsers.add_parser("submit-refines", help="Submit refine tasks for succeeded preview tasks.")
    subparsers.add_parser("watch-refines", help="Poll refine tasks until done and download models.")
    subparsers.add_parser("download", help="Download succeeded refined models and thumbnails.")
    render_parser = subparsers.add_parser("render", help="Render downloaded GLBs into 2.5D sprites with Blender.")
    render_parser.add_argument("--blender", type=Path, default=DEFAULT_BLENDER)
    render_parser.add_argument("--angles", type=int, default=8)
    render_parser.add_argument("--resolution", type=int, default=512)
    render_parser.add_argument("--samples", type=int, default=24)
    render_parser.add_argument("--style", choices=["preserve", "toon", "flat"], default="preserve")
    for subparser in subparsers.choices.values():
        if subparser.prog.endswith(("watch-previews", "watch-refines")):
            subparser.add_argument("--once", action="store_true")

    args = parser.parse_args()
    config = load_config(args.config)
    batch_id = str(config["batch_id"])
    raw_dir = args.raw_root / batch_id
    state_path = args.state or raw_dir / "state.json"
    state = load_state(state_path, config)

    if args.command == "plan":
        print_plan(config, state_path, raw_dir, args.render_root / batch_id)
        return 0

    api_key = args.api_key or os.environ.get("MESHY_API_KEY", "")
    if args.command != "render" and not api_key:
        raise SystemExit("MESHY_API_KEY is not set. Set it only locally; do not commit secrets.")

    client = MeshyClient(api_key) if api_key else None

    if args.command == "balance":
        assert client is not None
        print(json.dumps(client.get(BALANCE_ENDPOINT), indent=2))
        return 0
    if args.command == "submit-previews":
        assert client is not None
        submit_previews(client, config, state, state_path, max_active(args, config))
        return 0
    if args.command == "watch-previews":
        assert client is not None
        watch_tasks(client, state, state_path, "preview", args.poll_seconds, args.once)
        return 0
    if args.command == "submit-refines":
        assert client is not None
        submit_refines(client, config, state, state_path, max_active(args, config))
        return 0
    if args.command == "watch-refines":
        assert client is not None
        watch_tasks(client, state, state_path, "refine", args.poll_seconds, args.once)
        download_succeeded(client, state, state_path, raw_dir)
        return 0
    if args.command == "download":
        assert client is not None
        download_succeeded(client, state, state_path, raw_dir)
        return 0
    if args.command == "render":
        render_downloaded(args, batch_id, raw_dir, args.render_root / batch_id)
        return 0
    raise SystemExit(f"Unhandled command: {args.command}")


class MeshyClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get(self, path: str) -> dict[str, Any]:
        return self.request("GET", path)

    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", path, payload)

    def request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        body = None
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(API_BASE + path, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Meshy {method} {path} failed: HTTP {exc.code}: {detail}") from exc

    def download(self, url: str, out_path: Path) -> None:
        request = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.api_key}"})
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(request, timeout=180) as response:
            out_path.write_bytes(response.read())


def load_config(path: Path) -> dict[str, Any]:
    config = json.loads((ROOT / path if not path.is_absolute() else path).read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("Config must be a JSON object.")
    if "batch_id" not in config or "assets" not in config:
        raise ValueError("Config must define batch_id and assets.")
    return config


def load_state(path: Path, config: dict[str, Any]) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "batch_id": config["batch_id"],
        "config": rel(ROOT / config.get("_config_path", "")) if config.get("_config_path") else "",
        "tasks": {},
        "downloads": {},
    }


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def asset_specs(config: dict[str, Any]) -> list[AssetSpec]:
    defaults = config.get("defaults", {})
    specs = []
    for entry in config.get("assets", []):
        specs.append(
            AssetSpec(
                asset_id=entry["id"],
                prompt=entry["prompt"],
                texture_prompt=entry.get("texture_prompt", defaults.get("texture_prompt", "")),
                category=entry.get("category", ""),
                priority=int(entry.get("priority", 100)),
                should_remesh=bool(entry.get("should_remesh", defaults.get("should_remesh", True))),
                target_polycount=int(entry.get("target_polycount", defaults.get("target_polycount", 30000))),
                pose_mode=entry.get("pose_mode", defaults.get("pose_mode", "")),
            )
        )
    return sorted(specs, key=lambda item: (item.priority, item.asset_id))


def max_active(args: argparse.Namespace, config: dict[str, Any]) -> int:
    value = args.max_active or int(config.get("max_active", 6))
    return max(1, value)


def print_plan(config: dict[str, Any], state_path: Path, raw_dir: Path, render_dir: Path) -> None:
    specs = asset_specs(config)
    preview_credits = 20 * len(specs)
    refine_credits = 10 * len(specs)
    print(f"Batch: {config['batch_id']}")
    print(f"Assets: {len(specs)}")
    print(f"Preview estimate: {preview_credits} credits")
    print(f"Refine-all estimate: +{refine_credits} credits")
    print(f"Raw output: {rel(raw_dir)}")
    print(f"State: {rel(state_path)}")
    print(f"Render output: {rel(render_dir)}")
    for spec in specs:
        print(f"  - {spec.asset_id}: {spec.category}")


def submit_previews(
    client: MeshyClient,
    config: dict[str, Any],
    state: dict[str, Any],
    state_path: Path,
    active_limit: int,
) -> None:
    submitted = 0
    for spec in asset_specs(config):
        record = state["tasks"].setdefault(spec.asset_id, {})
        if record.get("preview_task_id"):
            continue
        if pending_count(state, "preview") >= active_limit:
            break
        payload: dict[str, Any] = {
            "mode": "preview",
            "prompt": prompt_with_lock(config, spec.prompt),
            "ai_model": config.get("ai_model", "latest"),
            "target_formats": ["glb"],
            "should_remesh": spec.should_remesh,
            "target_polycount": spec.target_polycount,
        }
        if spec.pose_mode:
            payload["pose_mode"] = spec.pose_mode
        response = client.post(TEXT_TO_3D_ENDPOINT, payload)
        record["preview_task_id"] = response["result"]
        record["preview_status"] = "PENDING"
        record["prompt"] = payload["prompt"]
        record["category"] = spec.category
        submitted += 1
        print(f"submitted preview {spec.asset_id}: {response['result']}")
        save_state(state_path, state)
    print(f"Submitted {submitted} preview task(s).")


def submit_refines(
    client: MeshyClient,
    config: dict[str, Any],
    state: dict[str, Any],
    state_path: Path,
    active_limit: int,
) -> None:
    specs_by_id = {spec.asset_id: spec for spec in asset_specs(config)}
    submitted = 0
    for asset_id, record in sorted(state["tasks"].items()):
        spec = specs_by_id.get(asset_id)
        if not spec or record.get("refine_task_id"):
            continue
        if record.get("preview_status") != "SUCCEEDED":
            continue
        if pending_count(state, "refine") >= active_limit:
            break
        payload: dict[str, Any] = {
            "mode": "refine",
            "preview_task_id": record["preview_task_id"],
            "ai_model": config.get("ai_model", "latest"),
            "target_formats": ["glb"],
            "enable_pbr": bool(config.get("enable_pbr", False)),
            "remove_lighting": bool(config.get("remove_lighting", True)),
            "auto_size": True,
            "origin_at": "bottom",
        }
        if spec.texture_prompt:
            payload["texture_prompt"] = spec.texture_prompt
        response = client.post(TEXT_TO_3D_ENDPOINT, payload)
        record["refine_task_id"] = response["result"]
        record["refine_status"] = "PENDING"
        record["texture_prompt"] = spec.texture_prompt
        submitted += 1
        print(f"submitted refine {asset_id}: {response['result']}")
        save_state(state_path, state)
    print(f"Submitted {submitted} refine task(s).")


def watch_tasks(
    client: MeshyClient,
    state: dict[str, Any],
    state_path: Path,
    stage: str,
    poll_seconds: int,
    once: bool,
) -> None:
    while True:
        changed = False
        remaining = []
        for asset_id, record in sorted(state["tasks"].items()):
            task_id = record.get(f"{stage}_task_id")
            if not task_id:
                continue
            status_key = f"{stage}_status"
            if record.get(status_key) in TERMINAL_STATUSES:
                continue
            task = client.get(f"{TEXT_TO_3D_ENDPOINT}/{urllib.parse.quote(task_id)}")
            status = task.get("status", "UNKNOWN")
            record[status_key] = status
            record[f"{stage}_task"] = task
            changed = True
            if status not in TERMINAL_STATUSES:
                remaining.append(asset_id)
            print(f"{stage} {asset_id}: {status} {task.get('progress', '')}")
        if changed:
            save_state(state_path, state)
        if once or not remaining:
            break
        time.sleep(poll_seconds)


def download_succeeded(client: MeshyClient, state: dict[str, Any], state_path: Path, raw_dir: Path) -> None:
    model_dir = raw_dir / "models"
    meta_dir = raw_dir / "metadata"
    thumb_dir = raw_dir / "thumbnails"
    downloaded = 0
    for asset_id, record in sorted(state["tasks"].items()):
        if record.get("refine_status") != "SUCCEEDED":
            continue
        if state["downloads"].get(asset_id, {}).get("model"):
            continue
        task = record.get("refine_task") or {}
        model_url = (task.get("model_urls") or {}).get("glb")
        if not model_url:
            print(f"skip {asset_id}: no GLB URL in task result")
            continue
        model_path = model_dir / f"{asset_id}.glb"
        client.download(model_url, model_path)
        (meta_dir / f"{asset_id}.json").parent.mkdir(parents=True, exist_ok=True)
        (meta_dir / f"{asset_id}.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        thumb_url = task.get("thumbnail_url")
        thumb_path = ""
        if thumb_url:
            thumb_file = thumb_dir / f"{asset_id}.png"
            client.download(thumb_url, thumb_file)
            thumb_path = rel(thumb_file)
        state["downloads"][asset_id] = {
            "model": rel(model_path),
            "metadata": rel(meta_dir / f"{asset_id}.json"),
            "thumbnail": thumb_path,
        }
        downloaded += 1
        print(f"downloaded {asset_id}: {rel(model_path)}")
        save_state(state_path, state)
    print(f"Downloaded {downloaded} model(s).")


def render_downloaded(args: argparse.Namespace, batch_id: str, raw_dir: Path, render_dir: Path) -> None:
    model_dir = raw_dir / "models"
    if not model_dir.exists() or not any(model_dir.glob("*.glb")):
        raise SystemExit(f"No downloaded GLB files found in {rel(model_dir)}.")
    blender = args.blender
    if not blender.exists():
        raise SystemExit(f"Blender executable not found: {blender}")
    command = [
        str(blender),
        "--background",
        "--python",
        str(ROOT / "tools" / "render_3d_asset_pack_to_sprites.py"),
        "--",
        "--input-dir",
        str(model_dir),
        "--out-dir",
        str(render_dir),
        "--angles",
        str(args.angles),
        "--resolution",
        str(args.resolution),
        "--samples",
        str(args.samples),
        "--style",
        args.style,
    ]
    subprocess.run(command, cwd=ROOT, check=True)
    print(f"Rendered Meshy batch {batch_id} to {rel(render_dir)}")


def pending_count(state: dict[str, Any], stage: str) -> int:
    status_key = f"{stage}_status"
    task_key = f"{stage}_task_id"
    return sum(
        1
        for record in state["tasks"].values()
        if record.get(task_key) and record.get(status_key) not in TERMINAL_STATUSES
    )


def prompt_with_lock(config: dict[str, Any], prompt: str) -> str:
    style_lock = str(config.get("style_lock", "")).strip()
    if not style_lock:
        return prompt
    return f"{prompt.strip()}\n\nStyle lock: {style_lock}"


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
