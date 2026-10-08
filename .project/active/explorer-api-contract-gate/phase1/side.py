"""One side of a Phase 1 replay pair: observe a tree with the real core, then record or check.

Run in its own process, `python -I -B side.py ...`, because the explorer's module
caches (`_load_model_module`, the `lib` helper import, `exploration.*`) live per
process. With -I nothing is on sys.path but the venv, so this script inserts the
code root (the extract whose server is imported) and the worktree's website_contract
directory (whose contract.py is under test).

    side.py record --code-root CR --tree T --pin SHA --out OUT [options]
    side.py check  --code-root CR --tree T --contract C --out OUT [options]

    options: --omit-list P (fallback mode), --skip-compute, --dump D (raw responses),
             --findings-only (compute the findings route only, without the server)

The output JSON always carries timings and the server's reads: every file under the
tree it opened for reading, and every directory it listed, from importing the server to
the last response. Record adds the contract text; check adds the failure keys and, for
each shape-type key, the pinned and observed kinds. A side that can't load or observe
writes its traceback instead and exits 1.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import sys
import time
import traceback
from pathlib import Path

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
    import contract as c

    contract = c.parse(args.contract.read_text()) if args.mode == "check" else None
    if args.findings_only:
        observation = observe_findings(c, args.tree, result)
        schema = c.Schema(frozenset(), {}, {})  # the findings response is an untyped dict
    else:
        observation, schema = observe_served(c, args, contract, result)
    result["templates"] = {
        template: {
            "count": len(responses),
            "total_seconds": sum(r.seconds for r in responses),
            "slowest_seconds": max((r.seconds for r in responses), default=0.0),
            "statuses": sorted({r.status for r in responses}),
        }
        for template, responses in observation.items()
    }
    result["compute_calls"] = [
        {"template": t, "instance": r.instance, "status": r.status, "seconds": r.seconds}
        for t in COMPUTE
        for r in observation.get(t, [])
    ]
    if args.dump is not None:
        args.dump.write_text(
            json.dumps(
                {t: [[r.instance, r.status, r.body] for r in rs] for t, rs in observation.items()}
            )
        )

    if args.mode == "record":
        tools = [f"{name}=={importlib.metadata.version(name)}" for name in ("httpx", "pytest")]
        result["contract"] = c.render(c.record(observation, schema, args.pin, tools, js={}))
        return
    result["failures"] = c.check(observation, contract)
    shapes = c.observed_shapes(observation, contract)
    details = {}
    for key in result["failures"]:
        rule, method, route, *rest = key.split(" ")
        if rule in ("shape", "unpopulated"):
            where = (f"{method} {route}", rest[0])
            details[key] = {"pinned": sorted(contract.shapes[where]), "now": sorted(shapes[where])}
    result["details"] = details


def observe_served(c, args: argparse.Namespace, contract, result: dict) -> tuple[dict, object]:
    """Serve the tree and observe it, auditing what the server reads; return it and the schema."""
    opened, listed = audit_reads()

    import exploration.concept_explorer.server as server

    if not Path(server.__file__).resolve().is_relative_to(args.code_root.resolve()):
        raise RuntimeError(f"imported {server.__file__}, not the code root's server")
    if args.omit_list is not None:
        import exploration.concept_explorer.models as models

        models._OMIT_LIST_PATH = args.omit_list
    skip = COMPUTE if args.skip_compute else ()
    schema = None
    start = time.perf_counter()
    with c.serve(args.tree / "exploration" / "concept_explorer") as client:
        result["startup_seconds"] = time.perf_counter() - start
        observe_start = time.perf_counter()
        if args.mode == "record":
            schema = c.classify(client.get("/openapi.json").json())
            concept_ids = c.manifest_concept_ids(client)
        else:
            concept_ids = list(contract.concepts)
        observation = c.observe(client, concept_ids, skip)
        result["observe_seconds"] = time.perf_counter() - observe_start
    result["reads"] = under(args.tree, opened)
    result["listed"] = under(args.tree, listed)
    return observation, schema


def observe_findings(c, tree: Path, result: dict) -> dict:
    """The findings route's responses for every served concept, without starting the server.

    For a tree whose server can't start (the 2026-06-08..15 Latin-1 registry) but whose change
    reaches only findings. Calls the tree's own findings.py exactly as its route does
    (server.py api_get_findings): live analyses root, archive root when it is a directory.
    """
    import yaml

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
        responses.append(c.Response(concept_id, 200, body, 0.0))
    result["concept_ids"] = concept_ids
    return {c.FINDINGS: responses}


if __name__ == "__main__":
    sys.exit(main())
