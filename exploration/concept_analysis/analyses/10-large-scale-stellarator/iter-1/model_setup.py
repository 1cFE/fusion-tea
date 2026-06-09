"""1costingfe model: Large-Scale Stellarator (Gauss Fusion).

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
    R0=18.0,              # helias-reactor-context.md §Table II (HSR4/18)
    plasma_t=1.7,         # analyst-patch-spec-anchors.md; derived from HSR4/18 cross-section
    plasma_volume=1500.0, # gauss-fusion-technical-summary.md §GIGA Power Plant
    B=6.0,                # gauss-fusion-technical-summary.md §GIGA Power Plant (on-axis)
    elon=1.6,             # analyst-patch-spec-anchors.md; averaged over toroidally varying bean/triangular cross-sections
    p_input=75.0,         # analyst-patch-spec-anchors.md; ECRH for startup/profile control (50-100 MW band)
)
P_native = 1000.0  # MWe — gauss-fusion-technical-summary.md (3 GW thermal → 1 GW electric)

# 2. Model.
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
#     `generic` is the library's overrides-off forward at P_native. It is BOTH the
#     writing frame for relative overrides AND the reference the framework rescales
#     against at projection time (see `_scale_overrides` in
#     1costingfe/src/costingfe/model.py). Under the headline invariant, a relative
#     override lands on `M x (the library's 1 GWe fleet cost for that account)`
#     regardless of class — the framework rescales your native-frame anchor to the
#     fleet frame by the per-account ratio fleet_cost/native_cost, so you never
#     compute that ratio yourself. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = []
# Section 5b explicitly states: zero overrides proposed. Gauss Fusion disclosed
# a top-level €15-18B total cost estimate but no CAS-level breakdown. The HELIAS
# heritage studies claimed "20% reactor core cost reduction" vs HSR5/22 and magnet
# costs "far below ITER-type tokamak" based on lower field (10 T NbTi), but GIGA
# targets 12-13 T peak field requiring Nb₃Sn or REBCO — both more expensive than
# NbTi per kA-m. Without published magnet procurement costs, blanket fabrication
# costs, or building cost estimates grounded in GIGA-specific design, no override
# value can be defensibly anchored to company data.

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
