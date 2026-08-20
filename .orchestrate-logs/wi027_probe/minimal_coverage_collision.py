"""Minimal, license-free demonstration of the Gate B mechanism.

The whole Gate B collision reduces to ONE function: collect_uncovered_params,
which extend_graph_with_constraints re-runs over the WHOLE graph at capture time
(constraint_lowering.py:1348-1350). This script builds the smallest graph that
carries the demo's essential shape:

  * one PRE-EXISTING cost-rollup module ('lcoe_calc') whose input 'total_capital'
    is a cross-part sum codegen cannot wire, so it is a fallback entry point with
    NO value at capture (default_value=None) -- exactly the 3 keys the demo's
    bridge fills only at GENERATION time.

We show:
  (A) at capture (placeholder NOT yet filled)  -> the check reports 1 violation
  (B) after the bridge fills it at generation  -> the check reports 0 violations

(A) is the state extend_graph_with_constraints sees when constraints are present,
so it raises. (B) is the state the generation-time V11 gate (cli/__init__.py:277,
which the bridge satisfies) sees. Same key, two different times.
"""
from pathlib import Path
from sysml_codegen.resolution.models import (
    ComputationGraph, PipelineModule, ModuleInput, ModuleOutput,
    InputSource, ParameterGroup, EntryPoint, EntryPointType, ModuleKind,
)
from sysml_codegen.resolution.graph_builder import collect_uncovered_params

KEY = "plant__lcoe_calc__total_capital"       # a cross-part rollup sum (unwirable)

# one pre-existing module reading the rollup key from an entry point
lcoe = PipelineModule(
    name="plant__lcoe_calc",
    module_type="LCOE",
    inputs=[ModuleInput(param_name="total_capital", python_type="float",
                        source=InputSource(source_type="entry_point",
                                           param_group="plant_params",
                                           qualified_name=KEY))],
    outputs=[ModuleOutput(field_name="root", python_type="float", channel_name="lcoe")],
    execution_order=0, module_kind=ModuleKind.CALCULATION,
)

def make_graph(placeholder_filled: bool) -> ComputationGraph:
    ep = EntryPoint(qualified_name=KEY, simple_name="total_capital",
                    entry_type=EntryPointType.LIBRARY_DEFAULT,
                    default_value=(1.0 if placeholder_filled else None),
                    param_group="plant_params")
    grp = ParameterGroup(name="plant_params", class_name="PlantParams",
                         source_file=Path("plant.sysml"), parameters=[ep])
    return ComputationGraph(
        modules=[lcoe], entry_point_groups=[grp],
        execution_order=["plant__lcoe_calc"],
        fallback_entry_points={KEY},   # it fell through Step-4 (unwirable cross-part sum)
    )

print("(A) capture time  -- placeholder NOT filled (what extend_graph_with_constraints sees):")
viol_A = collect_uncovered_params(make_graph(False))
print(f"    uncovered = {[v.missing_key for v in viol_A]}")
print(f"    -> extend_graph_with_constraints would RAISE: "
      f"'V11 coverage violations in extended graph' ({len(viol_A)} offender)")

print("(B) generation time -- bridge filled the placeholder (what the V11 gate sees):")
viol_B = collect_uncovered_params(make_graph(True))
print(f"    uncovered = {[v.missing_key for v in viol_B]}")
print(f"    -> generation-time V11 gate PASSES ({len(viol_B)} offenders)")

print()
print("Same key, same graph shape. The ONLY difference is WHEN the value is")
print("filled. The capture-time check demands it at capture; the bridge supplies")
print("it at generation. With asserts stripped, the capture-time check never runs")
print("(pipeline_builder.py:1001 guards it on `if concrete_constraints:`), so the")
print("key rides through to the generation gate the bridge satisfies. Un-stripping")
print("the asserts turns the capture-time check on -> collision.")
