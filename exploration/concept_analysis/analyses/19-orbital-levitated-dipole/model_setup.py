"""1costingfe model: Orbital Levitated Dipole (Zephyr Energy) (Zephyr Fusion).

WARNING: PLACEHOLDER MODEL — NO DESIGN POINT DISCLOSED
=======================================================

Zephyr Fusion has not published any quantitative design point parameters.
This model uses MINIMAL PLACEHOLDER values to satisfy the three-forward
contract validator, but the results are NOT MEANINGFUL.

Analysis (analysis.md Section 5) confirms:
    "No design point exists for this concept. Zephyr Fusion has not published
    any quantitative plasma parameters, reactor dimensions, power output targets
    (beyond 'megawatt-class'), or engineering specifications."

Section 5b: overrides = [] (no company cost data disclosed)

PLACEHOLDER RATIONALE:
- spec: minimal dict to allow forward() to run (library will use all YAML defaults)
- P_native: 100 MWe (arbitrary "megawatt-class" guess, NOT company data)
- overrides: [] (empty registry per analysis)

These are NOT Zephyr's design values — they are the minimum required to bind
generic/native/result_1gw for validator compliance while documenting the blocker.

The analysis documents 20 data gaps, 7 blocking. Until Zephyr publishes a
design point, this output should NOT be used for cross-concept comparison.

Usage:
    uv run python model_setup.py              # print placeholder results
    uv run python model_setup.py | tee model_output.txt
"""
import sys
from pathlib import Path

_SCRIPTS = next(
    p / "scripts"
    for p in Path(__file__).resolve().parents
    if (p / "scripts" / "lib" / "model_setup_helpers.py").exists()
)
sys.path.insert(0, str(_SCRIPTS))

from costingfe import ConfinementConcept, CostModel, Fuel
from lib.model_setup_helpers import (
    generic_reference, run_native_and_1gw, print_cas_breakdown,
)

# Zephyr discloses no design point — see WARNING block above. Mirror of
# the data_grounded=False flag passed to print_cas_breakdown below.
# Read by the explorer extractor to suppress headline LCOE in cross-concept
# views (cost landscape, comparison summary). CAS breakdown still renders.
DATA_GROUNDED = False

# 1. Specification — PLACEHOLDER (no company data; library defaults used)
# The analysis states all parameters are "Unknown". To satisfy the contract,
# we pass an empty spec dict — the library will use all YAML defaults for DIPOLE.
# This is NOT a transcription of Zephyr's design; it's the minimum to run forward().
spec = dict()  # Empty: all fields from library YAML defaults

# PLACEHOLDER: arbitrary "megawatt-class" interpretation (NOT company data)
P_native = 100.0  # MWe — Zephyr claims "megawatt-class" but no specific value

# 2. Model — using inferred archetype/fuel (analysis: "D-He3 [inferred], low confidence")
# Note: library may not have Fuel.DHE3; using DT as proxy (analysis Section 7
# notes D-T vs D-He3 as a major delta, but no D-He3 YAML exists in library)
model = CostModel(concept=ConfinementConcept.DIPOLE, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, library defaults (mandatory line)
generic = generic_reference(model, spec, P_native)

# 3. Override registry — empty per analysis Section 5b
# "Zephyr Fusion has not disclosed any company-grounded quantities, unit costs,
# or published dollar figures for any cost account."
overrides = []

# 4. Overrides-on forwards via shared helper (native + 1 GWe projection)
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

# Print breakdown
print("=" * 78)
print("WARNING: PLACEHOLDER MODEL — NO DESIGN POINT DISCLOSED")
print("=" * 78)
print(f"This model uses P_native = {P_native} MWe (arbitrary 'megawatt-class' guess)")
print("and spec = {} (all library YAML defaults for DIPOLE + DT).")
print()
print("Zephyr Fusion has not published:")
print("  - Plasma parameters (beta, T, n, τₑ)")
print("  - Reactor geometry (R0, coil radius, field strength)")
print("  - Heating method/power, energy conversion pathway")
print("  - System mass, launch configuration, or cost breakdown")
print()
print("The output below is the library's default DIPOLE story at 100 MWe, NOT")
print("Zephyr's design. See analysis.md Section 5/6 for the 20 data gaps.")
print("=" * 78)
print()

print_cas_breakdown(generic, native, result_1gw, overrides, data_grounded=False)
# data_grounded=False: Zephyr Fusion has disclosed no quantitative reactor
# parameters (PLACEHOLDER MODEL header above). The spec dict is empty and
# P_native = 100 MWe is an arbitrary "megawatt-class" placeholder. Headline
# LCOE lines emit (NOT ENOUGH DATA FOR THIS CONCEPT); CAS22 breakdown below
# still prints so a reviewer can see what library DIPOLE defaults produced.
