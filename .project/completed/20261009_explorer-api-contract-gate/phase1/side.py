"""One side of a Phase 1 replay pair: observe a tree with the real core, then record or check.

Run in its own process, `python -I -B side.py ...`, because the explorer's module
caches (`_load_model_module`, the `lib` helper import, `exploration.*`) live per
process. With -I nothing is on sys.path but the venv, so this script inserts the
code root (the extract whose server is imported) and the worktree's website_contract
directory (whose modules are under test).

    side.py record --code-root CR --tree T --pin SHA --out OUT [options]
    side.py check  --code-root CR --tree T --contract C --out OUT [options]

    options: --omit-list P (fallback mode), --skip-compute, --dump D (raw responses),
             --findings-only (compute the findings route only, without the server)

The output JSON always carries timings and the server's reads: every file under the
tree it opened for reading, and every directory it listed, from importing the server to
the last response. Record adds the contract text; check adds the failure keys and, for
each shape-type key, the pinned and observed kinds. A side that can't load or observe
writes its traceback instead and exits 1.

Timings and --skip-compute live here, not in the gate: `HarnessClient` times each request
`observe` sends and, with --skip-compute, leaves compute unsent.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import re
import sys
import time
import traceback
from pathlib import Path
from typing import Any

WEBSITE_CONTRACT = (
    Path(__file__).resolve().parents[4] / "exploration" / "concept_explorer" / "website_contract"
)
NON_CONCEPT_FILES = {
    "manifest.json",
    "parameter_index.json",
    "concept_registry.json",
    "decision_tree.json",
}
COMPUTE = ("POST /api/compute:slider", "POST /api/compute:slider-range", "POST /api/compute:toggle")
COMPUTE_ROUTE = "/api/compute"


class _Unsent:
    """What `observe` gets for a compute request under --skip-compute. It records status 0,
    and the side then drops the compute templates, so nothing judges these responses."""

    status_code = 0
    headers: dict[str, str] = {}


class HarnessClient:
    """The TestClient as `observe` calls it, plus what only the replay needs: every request's
    method, route, body, status and seconds (`calls`), and compute left unsent on request."""

    def __init__(self, client: Any, skip_compute: bool) -> None:
        self._client = client
        self._skip_compute = skip_compute
        self.calls: list[dict] = []

    def get(self, url: str, **kwargs: Any) -> Any:
        return self._send("GET", url, kwargs)

    def post(self, url: str, **kwargs: Any) -> Any:
        if self._skip_compute and url == COMPUTE_ROUTE:
            return _Unsent()
        return self._send("POST", url, kwargs)

    def _send(self, method: str, url: str, kwargs: dict) -> Any:
        start = time.perf_counter()
        response = self._client.request(method, url, **kwargs)
        seconds = time.perf_counter() - start
        self.calls.append(
            {
                "route": f"{method} {_route_of(url)}",
                "body": kwargs.get("json"),
                "status": response.status_code,
                "seconds": seconds,
            }
        )
        return response


def _route_of(url: str) -> str:
    """'/api/concepts/04/findings' -> '/api/concepts/{}/findings', for timing by route."""
    return re.sub(r"^/api/(concepts|parameters)/[^/]+", r"/api/\1/{}", url)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("record", "check"))
    parser.add_argument("--code-root", type=Path, required=True)
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--pin")
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--omit-list", type=Path)
    parser.add_argument("--skip-compute", action="store_true")
    parser.add_argument("--dump", type=Path)
    parser.add_argument("--findings-only", action="store_true")
    args = parser.parse_args()
    result: dict = {"mode": args.mode, "code_root": str(args.code_root), "tree": str(args.tree)}
    try:
        run(args, result)
    except Exception:  # the replay records why a side couldn't run; it never retries or hides it
        result["error"] = traceback.format_exc()
        args.out.write_text(json.dumps(result, indent=1))
        return 1
    args.out.write_text(json.dumps(result, indent=1))
    return 0


def audit_reads() -> tuple[list[str], list[str]]:
    """Install an audit hook; return the lists it fills: paths opened for reading, dirs listed.

    The hook only appends raw paths (calling into os from a hook would re-enter it); the
    caller resolves them afterwards. A hook can't be removed, so this runs once per process.
    """
    opened: list[str] = []
    listed: list[str] = []
    write_flags = os.O_WRONLY | os.O_RDWR | os.O_CREAT

    def hook(event: str, hook_args: tuple) -> None:
        if event == "open":
            path, mode, flags = hook_args
            reading = (
                (not any(c in mode for c in "wax+"))
                if isinstance(mode, str)
                else not (flags & write_flags)
            )
            if reading and isinstance(path, str):
                opened.append(path)
        elif event in ("os.listdir", "os.scandir") and isinstance(hook_args[0], str):
            listed.append(hook_args[0])

    sys.addaudithook(hook)
    return opened, listed


def under(tree: Path, paths: list[str]) -> list[str]:
    """`paths` that lie inside `tree`, relative to it, sorted and unique."""
    root = tree.resolve()
    relative = set()
    for path in paths:
        absolute = Path(os.path.abspath(path))
        if absolute.is_relative_to(root):
            relative.add(absolute.relative_to(root).as_posix())
    return sorted(relative)


def run(args: argparse.Namespace, result: dict) -> None:
    sys.path[:0] = [str(args.code_root), str(WEBSITE_CONTRACT)]
    import contract_rules as rules
    from contract_text import parse, render

    contract = parse(args.contract.read_text()) if args.mode == "check" else None
    if args.findings_only:
        observation = observe_findings(args.tree, result)
        calls: list[dict] = []
        schema = rules.Schema(frozenset(), {}, {})  # the findings response is an untyped dict
    else:
        observation, calls, schema = observe_served(args, contract, result)
    result["templates"] = {
        template: {"count": len(responses), "statuses": sorted({r.status for r in responses})}
        for template, responses in observation.items()
    }
    result["routes"] = route_timings(calls)
    result["compute_calls"] = [
        {
            "concept_id": call["body"]["concept_id"],
            "apply_analyst_overrides": call["body"]["apply_analyst_overrides"],
            "status": call["status"],
            "seconds": call["seconds"],
        }
        for call in calls
        if call["route"] == f"POST {COMPUTE_ROUTE}"
    ]
    if args.dump is not None:
        args.dump.write_text(
            json.dumps(
                {t: [[r.instance, r.status, r.body] for r in rs] for t, rs in observation.items()}
            )
        )

    if args.mode == "record":
        tools = [f"{name}=={importlib.metadata.version(name)}" for name in ("httpx", "pytest")]
        result["contract"] = render(rules.record(observation, schema, args.pin, tools, js={}))
        return
    result["failures"] = rules.check(observation, contract)
    shapes = rules.observed_shapes(observation, contract)
    details = {}
    for key in result["failures"]:
        rule, method, route, *rest = key.split(" ")
        if rule in ("shape", "unpopulated"):
            where = (f"{method} {route}", rest[0])
            details[key] = {"pinned": sorted(contract.shapes[where]), "now": sorted(shapes[where])}
    result["details"] = details


def route_timings(calls: list[dict]) -> dict[str, dict]:
    """Per route: how many requests, their total seconds and the slowest one's."""
    timings: dict[str, dict] = {}
    for call in calls:
        entry = timings.setdefault(
            call["route"], {"count": 0, "total_seconds": 0.0, "slowest_seconds": 0.0}
        )
        entry["count"] += 1
        entry["total_seconds"] += call["seconds"]
        entry["slowest_seconds"] = max(entry["slowest_seconds"], call["seconds"])
    return timings


def observe_served(
    args: argparse.Namespace, contract, result: dict
) -> tuple[dict, list[dict], object]:
    """Serve the tree and observe it, auditing what the server reads.

    Returns the observation (compute templates dropped under --skip-compute), every
    request's timing, and the schema when recording."""
    import contract_rules as rules
    import frontend_requests as fr

    opened, listed = audit_reads()

    import exploration.concept_explorer.server as server

    if not Path(server.__file__).resolve().is_relative_to(args.code_root.resolve()):
        raise RuntimeError(f"imported {server.__file__}, not the code root's server")
    if args.omit_list is not None:
        import exploration.concept_explorer.models as models

        models._OMIT_LIST_PATH = args.omit_list
    schema = None
    start = time.perf_counter()
    with fr.serve(args.tree / "exploration" / "concept_explorer") as client:
        result["startup_seconds"] = time.perf_counter() - start
        observe_start = time.perf_counter()
        if args.mode == "record":
            schema = rules.classify(client.get("/openapi.json").json())
            concept_ids = fr.manifest_concept_ids(client)
        else:
            concept_ids = list(contract.concepts)
        harness_client = HarnessClient(client, args.skip_compute)
        observation = fr.observe(harness_client, concept_ids)
        result["observe_seconds"] = time.perf_counter() - observe_start
    if args.skip_compute:
        for template in COMPUTE:
            del observation[template]
    result["reads"] = under(args.tree, opened)
    result["listed"] = under(args.tree, listed)
    return observation, harness_client.calls, schema


def observe_findings(tree: Path, result: dict) -> dict:
    """The findings route's responses for every served concept, without starting the server.

    For a tree whose server can't start (the 2026-06-08..15 Latin-1 registry) but whose change
    reaches only findings. Calls the tree's own findings.py exactly as its route does
    (server.py api_get_findings): live analyses root, archive root when it is a directory.
    """
    import yaml
    from frontend_requests import FINDINGS, Response

    from exploration.concept_explorer.findings import build_findings

    explorer = tree / "exploration" / "concept_explorer"
    omit_path = explorer / "omit_list.yaml"
    omitted = (
        {str(k) for k in (yaml.safe_load(omit_path.read_text()) or {})}
        if omit_path.exists()
        else set()
    )
    concept_ids = sorted(
        json.loads(path.read_text())["concept_id"]
        for path in (explorer / "data").glob("*.json")
        if path.name not in NON_CONCEPT_FILES and path.stem not in omitted
    )
    archive_root = tree / "archive" / "concept_analysis_pre_rework"
    responses = []
    for concept_id in concept_ids:
        payload = build_findings(
            concept_id,
            explorer.parent / "concept_analysis" / "analyses",
            archive_root=archive_root if archive_root.is_dir() else None,
        )
        body = {
            "exec_summary_html": payload.exec_summary_html,
            "analysis_html": payload.analysis_html,
            "analysis_from_archive": payload.analysis_from_archive,
        }
        responses.append(Response(concept_id, None, 200, body, allow_origin=None))
    result["concept_ids"] = concept_ids
    return {FINDINGS: responses}


if __name__ == "__main__":
    sys.exit(main())
