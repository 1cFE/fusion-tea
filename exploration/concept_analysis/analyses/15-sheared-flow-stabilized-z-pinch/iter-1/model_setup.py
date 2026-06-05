"""1costingfe model: Sheared-Flow Z-Pinch (Zap Energy) (Zap Energy).

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
#    Zap Energy SFS Z-pinch is a pulsed, self-confined, magnet-free concept
#    with a LiPb liquid-metal blanket. No magnets, no cryogenics, no
#    manufactured targets (plasma forms from gas injection).
#
#    The MIF pulsed-thermal inverse path takes q_eng and f_rep as primary
#    inputs and back-solves for p_fus and e_driver_mj from the target P_net.
#    p_input, eta_p, f_dec are NOT in the MIF forward() signature.
#
#    Published Q > 10 is Q_sci (P_fus/P_input), not q_eng. q_eng is not
#    published; the YAML default of 3.0 is used (not re-passed).
#
#    fusion_power_MW ≈ 190 MW (19 MJ × 10 Hz) — informational only,
#    library back-solves from q_eng + P_native via the inverse balance.
spec = dict(
    f_rep=10.0,       # Hz — engineering-paradigms-paper-summary.md §III; 10 Hz commercial target
    blanket_t=1.0,    # m — engineering-paradigms-paper-summary.md §V: "on the order of a meter or more"
)
P_native = 50  # MWe — century-demo-system.md §Module description; analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.STAGED_ZPINCH, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — transcribed from analysis Section 5b.
#    The analysis found zero evidence-backed overrides: no published cost
#    figures, unit prices, or quantified bills of material for any subsystem.
#    The library defaults for the pulsed-electrical-drive archetype are the
#    best available baseline. Archetype-Fit: High (0 overrides within band).
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
