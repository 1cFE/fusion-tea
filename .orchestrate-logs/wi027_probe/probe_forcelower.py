"""Does the bridge-force-lower path work? Capture is deferred (facts carried,
mode grandfathered_off, graph NOT lowered). Simulate the bridge: build the graph
from the deferred snapshot, fill the 3 capital-rollup placeholders, THEN run
lower_constraints + extend_graph_with_constraints on the covered graph. If V11
passes and constraint+aggregator modules appear, an in-scope bridge mechanism
exists. If it still aborts, no in-scope path exists and this must surface.
"""
from pathlib import Path
from sysml_codegen.snapshot.graph_rebuild import build_full_graph_from_snapshot
from sysml_codegen.analysis.part_instance_index import FrozenOccurrenceIndex
from sysml_codegen.analysis.constraint_lowering import (
    lower_constraints,
    extend_graph_with_constraints,
)
from sysml_codegen.resolution.graph_builder import collect_uncovered_params

SNAP = Path(".orchestrate-logs/wi027_probe/probeA_deferred.snapshot.json")
PLACEHOLDER = 1.0
BRIDGE_KEYS = {
    "stellarator_09__stellaris__contingency__direct_subtotal",
    "stellarator_09__stellaris__indirect__direct_cost",
    "stellarator_09__stellaris__lcoe_calc__total_capital",
}

graph, inputs = build_full_graph_from_snapshot(SNAP)
snap = inputs["snap"]
print("mode in snapshot:", snap["constraint_lowering_mode"])
print("facts usages:", len(snap["constraint_facts"].usages))
print("modules before lowering:", len(graph.modules))
print("uncovered BEFORE placeholder fill:", [u.missing_key.split('.')[-1] for u in collect_uncovered_params(graph)])

# --- bridge step: fill the 3 capital-rollup placeholders ---
bridged = []
for group in graph.entry_point_groups:
    for param in group.parameters:
        if param.qualified_name in BRIDGE_KEYS and param.default_value is None:
            param.default_value = PLACEHOLDER
            bridged.append(param.qualified_name)
print("bridged placeholders:", len(bridged))
print("uncovered AFTER placeholder fill:", [u.missing_key.split('.')[-1] for u in collect_uncovered_params(graph)])

# --- force-lower on the covered graph ---
try:
    concrete = lower_constraints(
        snap["constraint_facts"],
        occ_index=FrozenOccurrenceIndex(snap["part_occurrences"]),
        registry=inputs["registry"],
        design_attrs=inputs["design_attrs"],
        calc_usages=snap["calc_usages"],
        source_location_mode="snapshot",
        source_roots=[],
    )
    print("lower_constraints -> concrete count:", len(concrete))
    extended = extend_graph_with_constraints(graph, concrete, inputs["group_deriver"])
    print("extend_graph_with_constraints SUCCEEDED")
    kinds = {}
    for m in extended.modules:
        k = getattr(m, "module_kind", None)
        kinds[str(k)] = kinds.get(str(k), 0) + 1
    print("extended module kinds:", kinds)
    print("catalog on graph:", extended.constraint_catalog is not None)
    if extended.constraint_catalog is not None:
        cat = extended.constraint_catalog
        recs = getattr(cat, "records", None) or getattr(cat, "constraints", None)
        print("catalog record count:", len(recs) if recs is not None else "?")
except Exception as e:
    print("FORCE-LOWER FAILED:", type(e).__name__)
    print(str(e)[:700])
