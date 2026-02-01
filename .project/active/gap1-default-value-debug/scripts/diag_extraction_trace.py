"""Diagnostic Script: Extraction Pipeline Trace (Component 3 / FR-2)

Traces default_value through each stage of extraction for the chain spike model.
Shows both the library extraction path (extractor.py) and design attribute path
(parameter_groups.py).
"""
import sys
import logging
from pathlib import Path

sys.path.insert(0, "/home/reid/1cfe/sysml-codegen/src")
sys.path.insert(0, "/home/reid/1cfe/agentic-mbse/src")

from sysml_codegen.extraction.extractor import SysMLDataExtractor
from sysml_codegen.analysis.parameter_groups import extract_design_attributes

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

MODEL_PATHS = [
    Path("/home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/"),
]

print("=" * 70)
print("DIAGNOSTIC: Extraction Pipeline Trace (FR-2)")
print("=" * 70)

# ---- Path 1: Library extraction (extractor.py) ----
print("\n--- Path 1: Library Extraction (extractor.py) ---")
print("This path extracts calc def input/output attributes.")
print("For chain spike, library inputs have NO defaults, so expect all None.\n")

extractor = SysMLDataExtractor(MODEL_PATHS)
if not extractor.load_models():
    print("ERROR: Failed to load models!")
    sys.exit(1)

calc_defs = extractor.extract_calculation_definitions()
print(f"Found {len(calc_defs)} calculation definitions:\n")

for calc_def in calc_defs:
    print(f"  CalcDef: {calc_def.name} ({calc_def.qualified_name})")
    print(f"    Source: {calc_def.source_file}:{calc_def.source_line}")
    for attr in calc_def.input_attributes:
        print(f"    INPUT  {attr.name}: {attr.sysml_type} = {attr.default_value!r}")
    for attr in calc_def.output_attributes:
        print(f"    OUTPUT {attr.name}: {attr.sysml_type} = {attr.default_value!r}")
    print()

# ---- Path 2: Design attribute extraction (parameter_groups.py) ----
print("\n--- Path 2: Design Attribute Extraction (parameter_groups.py) ---")

# 2a: With default filter
print("\n  2a: With default filter ('models/designs'):")
design_attrs_default = extract_design_attributes(extractor.model, design_path_filter="models/designs")
total_default = sum(len(v) for v in design_attrs_default.values())
print(f"      Result: {total_default} attributes")
for fpath, attrs in design_attrs_default.items():
    for a in attrs:
        print(f"        {a.qualified_name} = {a.default_value!r}")

# 2b: With specific filter ('design.sysml') - targets only design file
print("\n  2b: With specific filter ('design.sysml'):")
try:
    design_attrs_fixed = extract_design_attributes(extractor.model, design_path_filter="design.sysml")
    total_fixed = sum(len(v) for v in design_attrs_fixed.values())
    print(f"      Result: {total_fixed} attributes")
    for fpath, attrs in design_attrs_fixed.items():
        for a in attrs:
            print(f"        {a.qualified_name} = {a.default_value!r}")
except Exception as e:
    print(f"      ERROR: {e}")
    design_attrs_fixed = {}
    total_fixed = 0

# 2c: With broad filter ('models/tests') - includes library, may crash
print("\n  2c: With broad filter ('models/tests') — includes library outputs:")
try:
    design_attrs_broad = extract_design_attributes(extractor.model, design_path_filter="models/tests")
    total_broad = sum(len(v) for v in design_attrs_broad.values())
    print(f"      Result: {total_broad} attributes")
    for fpath, attrs in design_attrs_broad.items():
        print(f"      File: {fpath}")
        for a in attrs:
            print(f"        {a.qualified_name} = {a.default_value!r}")
except Exception as e:
    print(f"      CRASHED: {type(e).__name__}: {e}")
    print("      (Library output attrs have OperatorExpressions that reference features)")
    design_attrs_broad = {}
    total_broad = -1

# ---- Side-by-side comparison ----
print("\n--- Side-by-Side Comparison ---")
print(f"{'Attribute':<60} {'Library':<12} {'Design(def)':<14} {'Design(fix)':<14}")
print("-" * 100)

# Collect all attribute names from all paths
all_attrs = {}

for calc_def in calc_defs:
    for attr in calc_def.input_attributes:
        key = f"{calc_def.name}.{attr.name}"
        all_attrs.setdefault(key, {})["library"] = attr.default_value

for attrs in design_attrs_default.values():
    for a in attrs:
        key = a.qualified_name
        all_attrs.setdefault(key, {})["design_default"] = a.default_value

for attrs in design_attrs_fixed.values():
    for a in attrs:
        key = a.qualified_name
        all_attrs.setdefault(key, {})["design_fixed"] = a.default_value

for name, sources in sorted(all_attrs.items()):
    lib = sources.get("library", "-")
    des_def = sources.get("design_default", "-")
    des_fix = sources.get("design_fixed", "-")
    print(f"  {name:<58} {str(lib):<12} {str(des_def):<14} {str(des_fix):<14}")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Library path: {sum(1 for cd in calc_defs for a in cd.input_attributes if a.default_value is not None)} / "
      f"{sum(len(cd.input_attributes) for cd in calc_defs)} inputs have defaults")
print(f"Design path (default filter): {total_default} attributes extracted")
print(f"Design path (specific filter): {total_fixed} attributes extracted")
print(f"Design path (broad filter):    {'CRASHED' if total_broad == -1 else total_broad} attributes extracted")

# Check if ALL design attrs have non-None defaults when using fixed filter
if total_fixed > 0:
    none_count = sum(
        1 for attrs in design_attrs_fixed.values()
        for a in attrs if a.default_value is None
    )
    if none_count > 0:
        print(f"\nWARNING: {none_count} attributes have None default even with corrected filter!")
        print("This indicates _extract_default_value() in parameter_groups.py also has issues.")
    else:
        print(f"\nAll {total_fixed} design attributes have non-None defaults with corrected filter.")
        print("The path filter is the ONLY issue for this model.")
