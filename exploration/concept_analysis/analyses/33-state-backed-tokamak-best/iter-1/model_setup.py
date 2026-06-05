"""1costingfe model: State-Backed Tokamak (Neo / ASIPP-class) (Neo Fusion).

Usage:
    uv run python model_setup.py              # print results
    uv run python model_setup.py | tee model_output.txt
"""
import sys
from pathlib import Path

# Make the shared three-forward helper importable regardless of where this file
# lives (concept dir or iter-N/ dir): walk up to the scripts/ root.
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

# 1. Specification — design-point inputs only, at native scale.
#    ARIES-ACT1 reference case (Kessel et al., Fusion Sci. Tech. 67:1, 2015)
#
#    Note: The library's TOKAMAK archetype accepts only geometry and power
#    inputs, not intermediate plasma physics parameters. Fields like delta
#    (triangularity), plasma_current, beta_n, and h_factor are documented
#    in the analysis but not costing model inputs - they're physics
#    calculations internal to the tokamak systems code that produced ACT1.
spec = dict(
    R0=6.25,       # major radius (m), osti-servlets-purl-1178069.md Table I
    plasma_t=1.91, # minor radius (m), inferred from A = R0/a = 3.27 (Table I)
    elon=2.0,      # elongation κ, Table I
    B=6.0,         # on-axis magnetic field (T), Table I
    p_input=42.7,  # H/CD auxiliary heating wallplug power (MW), Table I
    # Physics parameters from Table I not in spec (library doesn't consume):
    #   delta = 0.63 (triangularity)
    #   plasma_current = 10.9 MA
    #   beta_n = 4.75 (total normalized beta)
    #   h_factor = 1.65 (H98 confinement multiplier)
    # Fusion power (1813 MW per Table I) is back-solved by library from
    # p_input + geometry via inverse power balance, not a spec input.
)
P_native = 1000  # MWe net electric — design point specification

# 2. Model.
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — ARIES-ACT1 is a paper study with no company-grounded
#    cost data. The library default (ARIES-class tokamak calibration) already
#    represents this design point's cost structure. No overrides justified.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
