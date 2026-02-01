"""Diagnostic Script: Classification Trace (Component 4 / FR-3)

Traces default_value through _classify_entry_points() and build_pipeline_context()
to confirm which strategy fires and whether the default survives to JSON generation.

Runs twice: once with the default path filter (broken) and once with a patched filter.
Uses "design.sysml" as the corrected filter to avoid library OperatorExpression crash.
"""
import sys
import logging
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, "/home/reid/1cfe/sysml-codegen/src")
sys.path.insert(0, "/home/reid/1cfe/agentic-mbse/src")

from sysml_codegen.generation.initialization import build_pipeline_context
from sysml_codegen.analysis.parameter_groups import extract_design_attributes as _orig_extract

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

MODEL_PATHS = [
    Path("/home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/"),
]

print("=" * 70)
print("DIAGNOSTIC: Classification Trace (FR-3)")
print("=" * 70)


def print_graph_details(ctx, label):
    """Print entry points and their classification from a PipelineContext."""
    graph = ctx.computation_graph
    print(f"\n--- {label} ---")

    # Design attributes extracted
    total_design = sum(len(v) for v in ctx.design_attributes.values())
    print(f"  Design attributes extracted: {total_design}")
    for fpath, attrs in ctx.design_attributes.items():
        for a in attrs:
            print(f"    DESIGN_ATTR qname: {a.qualified_name} = {a.default_value!r}")

    # Entry points from graph
    print(f"\n  Entry points in ComputationGraph:")
    if hasattr(graph, "entry_point_groups"):
        for group in graph.entry_point_groups:
            print(f"\n    Group: {group.name} ({group.class_name})")
            for ep in group.parameters:
                print(f"      EP qname: {ep.qualified_name}")
                print(f"        type: {ep.entry_type}")
                print(f"        default_value: {ep.default_value!r}")
                print(f"        simple_name: {ep.simple_name}")
                print(f"        param_group: {ep.param_group!r}")
    else:
        print("    (no entry_point_groups attribute)")

    # QName mismatch analysis
    if total_design > 0 and hasattr(graph, "entry_point_groups"):
        design_qnames = set()
        for attrs in ctx.design_attributes.values():
            for a in attrs:
                design_qnames.add(a.qualified_name)
        ep_qnames = set()
        for g in graph.entry_point_groups:
            for ep in g.parameters:
                ep_qnames.add(ep.qualified_name)

        print(f"\n  --- Qualified Name Mismatch Analysis ---")
        print(f"  Design attr QNames: {sorted(design_qnames)}")
        print(f"  Entry point QNames: {sorted(ep_qnames)}")
        matching = design_qnames & ep_qnames
        design_only = design_qnames - ep_qnames
        ep_only = ep_qnames - design_qnames
        print(f"  Matching:     {sorted(matching) if matching else 'NONE'}")
        print(f"  Design only:  {sorted(design_only) if design_only else 'NONE'}")
        print(f"  EP only:      {sorted(ep_only) if ep_only else 'NONE'}")
        if not matching and design_qnames and ep_qnames:
            print(f"\n  >>> CRITICAL: Zero QName overlap between design attrs and entry points!")
            print(f"  >>> Strategy 1 (DESIGN_ATTRIBUTE) can NEVER match even with correct path filter!")
            print(f"  >>> Design attrs use parent part qnames (spike_design.length)")
            print(f"  >>> Entry points use calc usage qnames (spike_design.area_calc.length)")


# ---- Run 1: Default path filter (broken) ----
print("\n" + "=" * 70)
print("RUN 1: Default path filter ('models/designs') - EXPECT BROKEN")
print("=" * 70)

try:
    ctx_default = build_pipeline_context(MODEL_PATHS)
    print_graph_details(ctx_default, "Default filter results")
except Exception as e:
    print(f"  ERROR during build_pipeline_context: {e}")
    ctx_default = None

# ---- Run 2: Patched path filter using "design.sysml" ----
print("\n" + "=" * 70)
print("RUN 2: Patched path filter ('design.sysml') - EXPECT DESIGN ATTRS")
print("=" * 70)

import sysml_codegen.generation.initialization as init_module

def patched_extract(model, design_path_filter="models/designs"):
    """Override with design.sysml-specific filter."""
    return _orig_extract(model, design_path_filter="design.sysml")

try:
    with patch.object(init_module, "extract_design_attributes", side_effect=patched_extract):
        ctx_patched = build_pipeline_context(MODEL_PATHS)
    print_graph_details(ctx_patched, "Patched filter results")
except Exception as e:
    print(f"  ERROR during build_pipeline_context (patched): {e}")
    import traceback
    traceback.print_exc()
    ctx_patched = None

# ---- Comparison ----
print("\n" + "=" * 70)
print("COMPARISON")
print("=" * 70)

def collect_eps(graph):
    eps = {}
    if hasattr(graph, "entry_point_groups"):
        for g in graph.entry_point_groups:
            for ep in g.parameters:
                eps[ep.qualified_name] = ep
    return eps

if ctx_default and ctx_patched:
    eps_default = collect_eps(ctx_default.computation_graph)
    eps_patched = collect_eps(ctx_patched.computation_graph)

    all_qnames = sorted(set(eps_default.keys()) | set(eps_patched.keys()))

    print(f"\n{'Qualified Name':<60} {'Type(broken)':<22} {'Def(broken)':<14} {'Type(fixed)':<22} {'Def(fixed)':<14}")
    print("-" * 132)
    for qname in all_qnames:
        ep_d = eps_default.get(qname)
        ep_p = eps_patched.get(qname)
        type_d = str(ep_d.entry_type).split(".")[-1] if ep_d else "N/A"
        type_p = str(ep_p.entry_type).split(".")[-1] if ep_p else "N/A"
        val_d = ep_d.default_value if ep_d else "N/A"
        val_p = ep_p.default_value if ep_p else "N/A"
        changed = " <<<" if val_d != val_p or type_d != type_p else ""
        print(f"  {qname:<58} {type_d:<22} {str(val_d):<14} {type_p:<22} {str(val_p):<14}{changed}")

    # Check if the fix produces valid JSON data
    print(f"\n  Would JSON be populated with fix?")
    for qname in all_qnames:
        ep = eps_patched.get(qname)
        if ep and ep.default_value is not None:
            print(f"    {qname}: {ep.default_value} (float)")
        else:
            print(f"    {qname}: STILL None - secondary issue exists!")

elif ctx_default:
    print("  Only default run succeeded.")
    eps_default = collect_eps(ctx_default.computation_graph)
    print(f"\n  Default run entry points:")
    for qname, ep in sorted(eps_default.items()):
        print(f"    {qname}: type={ep.entry_type}, default={ep.default_value!r}")
elif ctx_patched:
    print("  Only patched run succeeded.")
else:
    print("  Both runs failed.")

# ---- Safety Net Analysis ----
print("\n" + "=" * 70)
print("SAFETY NET ANALYSIS (_group_entry_points_via_deriver)")
print("=" * 70)

if ctx_patched:
    # Check if the deriver's default values differ from classification
    deriver = ctx_patched.group_deriver
    if hasattr(deriver, '_attr_index'):
        print(f"  Deriver _attr_index has {len(deriver._attr_index)} entries")
        for key, val in sorted(deriver._attr_index.items()):
            print(f"    {key}: {val}")
    else:
        print("  Deriver has no _attr_index attribute")

    # Check get_default_value for each EP
    eps_patched = collect_eps(ctx_patched.computation_graph)
    for qname in sorted(eps_patched.keys()):
        if hasattr(deriver, 'get_default_value'):
            try:
                dv = deriver.get_default_value(qname)
                print(f"  deriver.get_default_value({qname}): {dv!r}")
            except Exception as e:
                print(f"  deriver.get_default_value({qname}): ERROR: {e}")

if ctx_default:
    deriver_d = ctx_default.group_deriver
    print(f"\n  Default run deriver:")
    if hasattr(deriver_d, '_attr_index'):
        print(f"    _attr_index has {len(deriver_d._attr_index)} entries")
        for key, val in sorted(deriver_d._attr_index.items()):
            print(f"      {key}: {val}")
    else:
        print("    No _attr_index attribute")

# ---- Conclusion ----
print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)
if ctx_default and ctx_patched:
    eps_d = collect_eps(ctx_default.computation_graph)
    eps_p = collect_eps(ctx_patched.computation_graph)
    all_none_default = all(ep.default_value is None for ep in eps_d.values())
    all_have_patched = all(ep.default_value is not None for ep in eps_p.values())
    some_have_patched = any(ep.default_value is not None for ep in eps_p.values())

    if all_none_default and all_have_patched:
        print("  CONFIRMED: Path filter fix fully resolves the issue.")
    elif all_none_default and some_have_patched:
        print("  PARTIAL: Path filter fix helps but doesn't resolve all entry points.")
    elif all_none_default and not some_have_patched:
        print("  DEEPER ISSUE: Even with path filter fix, defaults are still None.")
        print("  This likely means qualified name mismatch prevents Strategy 1 matching.")
        print("  The safety net (_group_entry_points_via_deriver) also fails.")
    else:
        print("  UNEXPECTED: Default run had some non-None values. Investigate.")
elif ctx_default:
    eps_d = collect_eps(ctx_default.computation_graph)
    all_none = all(ep.default_value is None for ep in eps_d.values())
    print(f"  Default run: {'all None' if all_none else 'some non-None'} defaults.")
    print("  Patched run failed - investigate errors above.")
