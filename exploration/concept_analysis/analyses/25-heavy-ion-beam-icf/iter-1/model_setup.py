"""1costingfe model: Heavy-Ion Beam ICF (Intensity Energy).

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
#    HYLIFE-II baseline (LLNL OSTI 7021072, 1990s).
#
#    The analysis identified key pulsed IFE parameters but no geometry/plasma
#    parameters that map to canonical spec keys. The YAML defaults capture
#    typical heavy-ion beam ICF chamber geometry (spherical chamber, plasma_t=4m).
#
#    Design point provides: 6 Hz rep rate, 5 MJ driver energy, 350 MJ yield,
#    driver efficiency 30-40%, target gain ~70. Only f_rep maps directly to
#    canonical spec keys; the rest are derived via q_eng.
spec = dict(
    f_rep=6.0,         # hif-technology-overview.md §HYLIFE-II: 6 Hz baseline rep rate
    # q_eng derived from power balance: Q_target ~70, eta_driver ~35% (midpoint of 30-40%)
    # q_eng = P_net / P_driver_electric ≈ 4.0 (library default is appropriate)
    # eta_pin = 0.35 would be the driver efficiency, but per Rule 6 power-conversion
    # efficiencies are library-owned; YAML default eta_pin=0.25 is conservative
    # mn = 1.1 is library default (standard DT blanket multiplication)
)
P_native = 940.0       # MWe — hif-technology-overview.md §HYLIFE-II baseline

# Note: Driver energy (5 MJ), yield (350 MJ), and target gain (~70) are provided
# in the design point but do not map to canonical spec keys. The library derives
# these from q_eng, f_rep, and P_native via the inverse power balance.
#
# The analysis states driver efficiency 30-40% (hif-technology-overview.md §Driver
# Technology), which would suggest eta_pin=0.35, but power-conversion efficiencies
# are library-owned per Rule 6. YAML default eta_pin=0.25 remains.
#
# Chamber geometry (FLiBe liquid wall, thick jets) and materials (Li₂BeF₄ blanket)
# do not have corresponding spec keys in the pulsed IFE archetype.

# 2. Model.
model = CostModel(concept=ConfinementConcept.HEAVY_ION, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — Section 5b states "No override candidates proposed."
#    The archetype-fit grade is High, expecting 0-4 enabled overrides.
#    All quantitative data derives from 1990s-era national lab studies (HYLIFE-II,
#    HIBALL) with no company-grounded cost data. Without accountable provenance,
#    no departures from library defaults are justified.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
