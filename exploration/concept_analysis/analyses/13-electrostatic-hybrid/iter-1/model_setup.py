"""1costingfe model: Electrostatic Hybrid (Orbitron) (Avalanche Energy).

CRITICAL BLOCKER: This concept cannot be meaningfully modeled at its actual
design-point scale (5 kWe) due to 1costingFE power balance convergence floors
at ~1 MWe. The analysis (Section 5b) states: "The 1costingFE library cannot
model below ~1 MWe due to power balance convergence floors. Any P_native < 1 MWe
is rejected with rec_frac > 1 errors regardless of parameter choices."

Per the analyst-patch source (analyst-patch-pb11-fuel-critical.md), the library
must be run at P_native=1.0 MWe as a workaround, even though the actual design
point is 5 kWe (0.005 MWe). This script uses the 1.0 MWe workaround to produce
a runnable model, but the result does NOT represent the actual 5 kWe device.

Usage:
    uv run python model_setup.py              # print results (at 1 MWe workaround scale)
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
#    From analysis Section 5 table. The geometry/physics parameters are from
#    the actual 5 kWe design point, but P_native is set to 1.0 MWe (workaround)
#    instead of the actual 0.005 MWe to avoid convergence failure.
spec = dict(
    # Geometry (from CWFest 2023 blog: 12 cm diameter device = 6 cm radius)
    # plasma_t is the minor radius for dipole-class devices (ORBITRON maps to DIPOLE archetype)
    plasma_t=0.06,      # m — avalanche-cwfest2023-blog.md §Fusion rate scaling

    # Magnetic field (target for superconducting upgrade; current prototypes at 0.05 T)
    B=0.3,              # T — avalanche-cwfest2023-blog.md §Fusion rate scaling

    # Auxiliary heating wallplug (scaled to 1 MWe workaround scale)
    # At the actual 5 kWe scale, p_input would be ~5 kW (0.005 MW) per CWFest
    # scaling (1 kW recirculating for 1 kW fusion at Q~1). At 1 MWe workaround
    # scale, p_input is scaled linearly: 1.0 MWe / 0.005 MWe × 0.005 MW = 1.0 MW.
    # This is a placeholder — the actual device physics at 1 MWe is unknown.
    p_input=1.0,        # MW — scaled from 5 kW estimate to 1 MWe workaround scale
)

# Note: chamber_length is not a canonical CostingInput field and has been omitted.
# The analysis estimated 0.2-0.5 m based on "desktop-scale" but this parameter
# is not used by the ORBITRON/DIPOLE archetype cost model.

# Native power — WORKAROUND VALUE, not the actual design point
# Actual design point: 0.005 MWe (5 kWe)
# Workaround value: 1.0 MWe (to avoid convergence failure)
# Per analyst-patch-pb11-fuel-critical.md: "the library must be run at
# P_native = 1.0 MWe as a workaround, even though the actual design point
# is 5 kWe (0.005 MWe)."
P_native = 1.0  # MWe — WORKAROUND (actual design point is 0.005 MWe)

print("="*80)
print("CRITICAL NOTICE: P_native Workaround in Effect")
print("="*80)
print(f"Actual design point:    0.005 MWe (5 kWe)")
print(f"Workaround P_native:    {P_native} MWe")
print("")
print("The library cannot model below ~1 MWe due to power balance convergence.")
print("This script uses P_native=1.0 MWe to produce a runnable model, but the")
print("result does NOT represent the actual 5 kWe device economics.")
print("="*80)
print("")

# Additional context not in spec (documentation only):
# - Cathode voltage: 300 kV (avalanche-300kv-press-release.md)
# - Field gradient: 6.0 MV/m (avalanche-fusionwerx-grant.md)
# - Q_plasma: ~2-5 inferred (must be >1 for net power; CWFest targets Q~1)
# - Fusion power (scaled estimate at actual 5 kWe scale): ~25 kWt
# - Neutron rate (at actual 5 kWe scale): ~10^12 n/s
# - eta_th: assumed 20-30% (no steam turbine exists at 5 kWe scale)
# - Tritium breeding: N/A (no space for breeding blanket at 12 cm diameter)
# - Chamber length: estimated 0.2-0.5 m (not a canonical spec key)

# 2. Model.
model = CostModel(concept=ConfinementConcept.ORBITRON, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
#     Using P_native=1.0 MWe workaround instead of actual 0.005 MWe.
generic = generic_reference(model, spec, P_native)

# 3. Override registry — empty per analysis Section 5b.
#    Analysis states: "Given these blockers, no overrides are proposed. The
#    concept cannot be meaningfully costed at the specified scale and fuel with
#    current library capabilities."
#
#    Note: Even if overrides were discovered at the 1 MWe workaround scale,
#    they would not apply to the actual 5 kWe device due to the scale mismatch.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)

print("")
print("="*80)
print("REMINDER: These results use P_native=1.0 MWe (workaround), not the actual")
print("0.005 MWe (5 kWe) design point. The LCOE estimate does NOT represent the")
print("actual Orbitron economics at its specified scale.")
print("="*80)
