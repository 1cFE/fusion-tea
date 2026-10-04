"""Step 3: run scripts/study/indicators.py for every group of every unit, through a disclosed name-alias shim.

The stock tool refuses all three WI-100 packages with "constraint '<id>' has no matching module in the pipeline" for
the two UA-capacity checks (`main_UA_capacity_ok`, `reheat_UA_capacity_ok`): `_constraint_entry` looks a constraint's
module up by its constraint id, and codegen names these two modules with the id lower-cased
(`..._main_ua_capacity_ok_...`). Every other constraint's module name equals its id. This is a tool defect, not a
package or study condition (finding #1 of this record); the tool file is outside this record's write scope.

The shim changes one thing: after the stock `build_graph`, each ConstraintEvaluation module whose output channel is
`<constraint id>__evaluation` and whose name differs from that id is also registered under the id, and only when the
name is exactly the id lower-cased. `graph.modules` feeds only the per-constraint operand lookup; the reachability
trace reads `graph.deps` and `graph.producer`, which are untouched, so no trace result can change. Everything else is
the stock `indicators.main`. The aliases are written beside each report as indicators_<unit>.aliases.json.

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/run_indicators.py [unit ...]'
"""
from __future__ import annotations

import json

import record_common as rc
from scripts.study import indicators as ind

_stock_build_graph = ind.build_graph
ALIASES: dict[str, str] = {}


def build_graph(parsed):
    graph = _stock_build_graph(parsed)
    for name, module in list(graph.modules.items()):
        for port in module.outputs.values():
            if port.type != "ConstraintEvaluation" or not port.ref.endswith("__evaluation"):
                continue
            cid = port.ref[: -len("__evaluation")]
            if cid == name or cid in graph.modules:
                continue
            if cid.lower() != name:
                raise ind.IndicatorError(f"constraint {cid!r}: module {name!r} is not its id lower-cased")
            graph.modules[cid] = module
            ALIASES[cid] = name
    return graph


ind.build_graph = build_graph

if __name__ == "__main__":
    import sys

    for unit in (sys.argv[1:] or rc.UNITS):
        ALIASES.clear()
        package = f"exploration/stellarator_materials/units/{unit}/stellarator_materials_{unit}_tea"
        out = rc.RECORD / f"indicators_{unit}.json"
        if out.exists():
            raise FileExistsError(f"{out.name} exists; preserve evidence")
        code = ind.main(["--package", package, "--manifest", str(rc.manifest_path(unit)),
                         "--groups", str(rc.axes_path(unit)), "--out", str(out)])
        if code != 0:
            raise SystemExit(f"{unit}: indicators refused (exit {code})")
        rc.write_json({"unit": unit, "shim": "run_indicators.py", "shim_sha256": rc.sha256(__file__),
                       "stock_tool_sha256": rc.sha256(rc.REPO / "scripts/study/indicators.py"),
                       "aliases": dict(sorted(ALIASES.items()))}, rc.RECORD / f"indicators_{unit}.aliases.json")
        report = json.loads(out.read_text())
        print(unit, "aliases", sorted(ALIASES), {g["axis"]: (g["no_constraint_response"], len(g["constraints_reachable"]))
                                                 for g in report["groups"]})
