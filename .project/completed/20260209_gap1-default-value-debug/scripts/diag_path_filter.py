"""Diagnostic Script: Path Filter Verification (Component 1)

Tests whether the design_path_filter parameter in extract_design_attributes()
is the root cause for empty design_params.json in the chain spike model.

Hypothesis: The chain spike model lives at models/tests/codegen_chain_spike/design.sysml
which does NOT contain "models/designs" (the default filter). This causes all
design attributes to be filtered out.

NOTE: The "models/tests" filter also matches library.sysml (same directory),
whose output attributes have OperatorExpressions that crash _extract_default_value().
We use "design.sysml" as the most specific filter and also test "models/tests" with
error catching to document both the primary and secondary issues.
"""
import sys
import logging
from pathlib import Path

# Ensure both repos are importable
sys.path.insert(0, "/home/reid/1cfe/sysml-codegen/src")
sys.path.insert(0, "/home/reid/1cfe/agentic-mbse/src")

from sysml_codegen.analysis.parameter_groups import extract_design_attributes
from agentic_mbse.sysml.syside_adapter import SysideAdapter

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

MODEL_PATHS = [
    Path("/home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/"),
]

print("=" * 70)
print("DIAGNOSTIC: Path Filter Verification")
print("=" * 70)

# Step 1: Load model
print("\n--- Step 1: Loading chain spike model ---")
model, _facade = SysideAdapter.load_model(MODEL_PATHS)
print(f"Model loaded successfully")

# Step 2: Default filter ("models/designs") - expect EMPTY
print("\n--- Step 2: Default filter ('models/designs') ---")
result_default = extract_design_attributes(model, design_path_filter="models/designs")
total_default = sum(len(v) for v in result_default.values())
print(f"  Files matched: {len(result_default)}")
print(f"  Total attributes: {total_default}")
for fpath, attrs in result_default.items():
    for a in attrs:
        print(f"    {a.qualified_name} = {a.default_value!r}")

if total_default == 0:
    print("  >>> CONFIRMED: Default filter 'models/designs' yields ZERO attributes")
else:
    print("  >>> UNEXPECTED: Default filter returned attributes!")

# Step 3: Broad filter ("models/tests") - may crash on library output exprs
print("\n--- Step 3: Broad filter ('models/tests') ---")
try:
    result_tests = extract_design_attributes(model, design_path_filter="models/tests")
    total_tests = sum(len(v) for v in result_tests.values())
    print(f"  Files matched: {len(result_tests)}")
    print(f"  Total attributes: {total_tests}")
    for fpath, attrs in result_tests.items():
        print(f"  File: {fpath}")
        for a in attrs:
            print(f"    {a.qualified_name} = {a.default_value!r} (type: {a.sysml_type})")
except Exception as e:
    print(f"  >>> ERROR: {type(e).__name__}: {e}")
    print("  This is EXPECTED — 'models/tests' also matches library.sysml,")
    print("  whose output expressions (e.g., area = length * width) crash")
    print("  _extract_default_value() at the OperatorExpression → evaluate_true_static_expression path.")
    print("  This is a SECONDARY BUG: _extract_default_value() doesn't gracefully handle")
    print("  non-static OperatorExpressions that reference features.")
    total_tests = -1  # sentinel for crashed

# Step 4: Specific filter ("design.sysml") - should get only design attrs
print("\n--- Step 4: Specific filter ('design.sysml') ---")
try:
    result_design = extract_design_attributes(model, design_path_filter="design.sysml")
    total_design = sum(len(v) for v in result_design.values())
    print(f"  Files matched: {len(result_design)}")
    print(f"  Total attributes: {total_design}")
    for fpath, attrs in result_design.items():
        print(f"  File: {fpath}")
        for a in attrs:
            print(f"    {a.qualified_name} = {a.default_value!r} (type: {a.sysml_type})")
except Exception as e:
    print(f"  >>> ERROR: {type(e).__name__}: {e}")
    total_design = -1

# Step 5: Empty filter (no filtering) - all files, likely crashes on library exprs
print("\n--- Step 5: Empty filter ('') ---")
try:
    result_all = extract_design_attributes(model, design_path_filter="")
    total_all = sum(len(v) for v in result_all.values())
    print(f"  Files matched: {len(result_all)}")
    print(f"  Total attributes: {total_all}")
    for fpath, attrs in result_all.items():
        print(f"  File: {fpath}")
        for a in attrs:
            print(f"    {a.qualified_name} = {a.default_value!r} (type: {a.sysml_type})")
except Exception as e:
    print(f"  >>> ERROR: {type(e).__name__}: {e}")
    total_all = -1

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"  Default filter ('models/designs'): {total_default} attributes")
print(f"  Broad filter ('models/tests'):     {'CRASHED' if total_tests == -1 else total_tests} attributes")
print(f"  Specific filter ('design.sysml'):  {'CRASHED' if total_design == -1 else total_design} attributes")
print(f"  No filter (''):                    {'CRASHED' if total_all == -1 else total_all} attributes")

print("\nFINDINGS:")
if total_default == 0:
    print("  1. PRIMARY ROOT CAUSE CONFIRMED: Path filter mismatch.")
    print("     The chain spike design.sysml path does not contain 'models/designs'.")
    print("     extract_design_attributes() returns 0 attributes → empty JSON.")

actual_result = total_design if total_design > 0 else (total_tests if total_tests > 0 else 0)
if actual_result > 0:
    # Check which result to use
    use_result = result_design if total_design > 0 else (result_tests if total_tests > 0 else {})
    all_have_defaults = all(
        a.default_value is not None
        for attrs in use_result.values()
        for a in attrs
    )
    if all_have_defaults:
        print(f"  2. With corrected filter: {actual_result} attributes, ALL have non-None defaults.")
        print("     _extract_default_value() in parameter_groups.py works correctly for literals.")
    else:
        print(f"  2. WARNING: Some attributes have None default_value even with corrected filter!")
        print("     This indicates a secondary issue in _extract_default_value().")

if total_tests == -1:
    print("  3. SECONDARY BUG: _extract_default_value() crashes on OperatorExpressions")
    print("     that reference features (e.g., 'area = length * width' in library output attrs).")
    print("     evaluate_true_static_expression() raises ValueError for feature references.")
    print("     This would be hit if the path filter were broadened without also filtering")
    print("     out library output attributes.")
