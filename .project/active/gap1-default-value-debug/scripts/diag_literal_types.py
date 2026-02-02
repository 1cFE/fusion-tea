"""Diagnostic Script: Literal Type Matching (Component 2 / FR-1)

Empirically tests whether SysideAdapter.is_instance() matches literal expression
types identically to Python isinstance() for the chain spike model.

Tests all four literal types: LiteralRational, LiteralInteger, LiteralBoolean, LiteralString.
"""
import sys
from pathlib import Path

sys.path.insert(0, "/home/reid/1cfe/sysml-codegen/src")
sys.path.insert(0, "/home/reid/1cfe/agentic-mbse/src")

from agentic_mbse.sysml.syside_adapter import SysideAdapter

# Import syside directly for Python isinstance tests
try:
    import syside
    HAS_SYSIDE = True
except ImportError:
    HAS_SYSIDE = False
    print("WARNING: Could not import syside directly. Python isinstance tests will be skipped.")

MODEL_PATHS = [
    Path("/home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/"),
]

print("=" * 70)
print("DIAGNOSTIC: Literal Type Matching (FR-1)")
print("=" * 70)

# Load model
print("\n--- Loading model ---")
model, _facade = SysideAdapter.load_model(MODEL_PATHS)

# Find all AttributeUsage elements with feature_value_expression
print("\n--- Scanning AttributeUsage elements with default values ---")

literal_type_names = ["LiteralRational", "LiteralInteger", "LiteralBoolean", "LiteralString"]

for elem in SysideAdapter.elements_of_type(model, "AttributeUsage"):
    if not hasattr(elem, "feature_value_expression"):
        continue
    if not elem.feature_value_expression:
        continue

    expr = elem.feature_value_expression
    elem_name = getattr(elem, "name", "<unnamed>")

    # Try to get the qualified name for context
    try:
        owner = getattr(elem, "owner", None)
        owner_name = getattr(owner, "name", "?") if owner else "?"
    except Exception:
        owner_name = "?"

    print(f"\n  Attribute: {owner_name}.{elem_name}")
    print(f"    Python type(expr): {type(expr)}")
    print(f"    Python type(expr).__name__: {type(expr).__name__}")
    print(f"    repr(expr): {repr(expr)[:100]}")

    # Check for value attribute
    if hasattr(expr, "value"):
        print(f"    expr.value: {expr.value!r} (type: {type(expr.value).__name__})")
    else:
        print(f"    expr.value: NOT PRESENT")

    # Test each literal type with all three mechanisms
    print(f"    --- Type matching tests ---")
    for type_name in literal_type_names:
        # Mechanism 1: SysideAdapter.is_instance() (new code path)
        adapter_result = SysideAdapter.is_instance(expr, type_name)

        # Mechanism 2: Python isinstance() (old code path)
        if HAS_SYSIDE:
            syside_type = getattr(syside, type_name, None)
            if syside_type is not None:
                python_isinstance_result = isinstance(expr, syside_type)
            else:
                python_isinstance_result = "N/A (type not found in syside)"
        else:
            python_isinstance_result = "N/A (syside not imported)"

        # Mechanism 3: syside's elem.isinstance() method
        if hasattr(expr, "isinstance"):
            try:
                if HAS_SYSIDE:
                    syside_type = getattr(syside, type_name, None)
                    if syside_type:
                        syside_isinstance_result = expr.isinstance(syside_type)
                    else:
                        syside_isinstance_result = "N/A"
                else:
                    syside_isinstance_result = "N/A"
            except Exception as e:
                syside_isinstance_result = f"ERROR: {e}"
        else:
            syside_isinstance_result = "N/A (no isinstance method)"

        # Report if any mechanism matched
        any_match = adapter_result or (python_isinstance_result is True) or (syside_isinstance_result is True)
        marker = " <<<" if any_match else ""
        print(f"    {type_name}:{marker}")
        print(f"      Adapter.is_instance():    {adapter_result}")
        print(f"      Python isinstance():      {python_isinstance_result}")
        print(f"      syside .isinstance():     {syside_isinstance_result}")

        # Check for disagreements
        results = []
        if isinstance(adapter_result, bool):
            results.append(("adapter", adapter_result))
        if isinstance(python_isinstance_result, bool):
            results.append(("python", python_isinstance_result))
        if isinstance(syside_isinstance_result, bool):
            results.append(("syside", syside_isinstance_result))

        if len(results) >= 2:
            values = [r[1] for r in results]
            if len(set(values)) > 1:
                print(f"      >>> DISAGREEMENT DETECTED!")
                for name, val in results:
                    print(f"          {name}: {val}")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("If all three mechanisms agree for all literal types, Delta B is benign.")
print("If disagreements exist, the adapter indirection is a contributing factor.")
