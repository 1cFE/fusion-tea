"""1costingfe model: Planar-Coil Stellarator (Thea Energy).

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
#    Geometry / physics / power. NO library-default re-passing.
spec = dict(
    R0=8.0,              # major radius [m] — thea-energy-helios-arxiv-2512-08027.md §2 Table 1
    plasma_t=1.8,        # minor radius [m] — thea-energy-helios-arxiv-2512-08027.md §2 Table 1
                         # (paper states a=1.8 m; A=4.5 gives R0/A=1.78, paper rounds to 1.8)
    B=6.0,               # on-axis magnetic field [T] — thea-energy-helios-arxiv-2512-08027.md §2 Table 1
                         # (B_peak=20 T on conductor is informational only)
    elon=1.0,            # elongation — QA stellarator cross-section roughly circular (analysis §5)
    plasma_volume=500.0, # plasma volume [m³] — thea-energy-helios-arxiv-2512-08027.md §2 Table 1
    p_input=2.5,         # auxiliary heating wallplug [MW] — thea-energy-helios-arxiv-2512-08027.md §4.4
                         # 1 MW ECRH + overhead during ignited operation (2.5 MW budgeted).
                         # NOT fusion power (958 MW is informational — library back-solves p_fus).
    # eta_th=0.402 — not a spec key; library-owned via PowerCycle ENUM (Rankine ~40%).
    # fusion_power_MW=958 — informational only; p_fus is never a spec key.
    # capacity_factor=0.88 — library-owned availability; not a spec key.
)
P_native = 390.0         # MWe — copied from the analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Analysis Section 5b found ZERO enabled overrides. Helios is an exceptionally
#    detailed engineering/physics design paper but contains no published cost data
#    whatsoever — no capital cost breakdown, no $/kW, no LCOE analysis. All costing
#    relies entirely on library defaults computed from the design point parameters.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
