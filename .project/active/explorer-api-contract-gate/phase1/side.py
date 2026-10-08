"""One side of a Phase 1 replay pair: observe a tree with the real core, then record or check.

Run in its own process, `python -I -B side.py ...`, because the explorer's module
caches (`_load_model_module`, the `lib` helper import, `exploration.*`) live per
process. With -I nothing is on sys.path but the venv, so this script inserts the
code root (the extract whose server is imported) and the worktree's website_contract
directory (whose contract.py is under test).

    side.py record --code-root CR --tree T --pin SHA --out OUT [options]
    side.py check  --code-root CR --tree T --contract C --out OUT [options]

    options: --omit-list P (fallback mode), --skip-compute, --dump D (raw responses)

The output JSON always carries timings. Record adds the contract text; check adds the
failure keys and, for each shape-type key, the pinned and observed kinds. A side that
can't load or observe writes its traceback instead and exits 1.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import sys
import time
import traceback
from pathlib import Path

WEBSITE_CONTRACT = (
    Path(__file__).resolve().parents[4] / "exploration" / "concept_explorer" / "website_contract"
)
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


def run(args: argparse.Namespace, result: dict) -> None:
    sys.path[:0] = [str(args.code_root), str(WEBSITE_CONTRACT)]
    import contract as c

    import exploration.concept_explorer.server as server

    if not Path(server.__file__).resolve().is_relative_to(args.code_root.resolve()):
        raise RuntimeError(f"imported {server.__file__}, not the code root's server")
    if args.omit_list is not None:
        import exploration.concept_explorer.models as models

        models._OMIT_LIST_PATH = args.omit_list
    skip = COMPUTE if args.skip_compute else ()
    contract = c.parse(args.contract.read_text()) if args.mode == "check" else None

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


if __name__ == "__main__":
    sys.exit(main())
