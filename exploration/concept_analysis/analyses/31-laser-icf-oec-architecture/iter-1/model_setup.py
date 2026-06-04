"""1costingfe model: Laser ICF OEC Architecture (BLF) (Blue Laser Fusion).

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
#    Sunahara et al. (2025) Optics Express paper provides laser physics and power
#    balance but minimal reactor geometry. Archetype-Fit: Low (IFE with hybrid
#    thermal + DEC conversion modeled as pure-thermal LASER_IFE archetype).
#
#    Mapping published design point (analysis.md §5) to canonical CostingInput
#    spec fields:
#
#    plasma_t (chamber radius): Paper §4.1 gives 8–10 m chamber radius (medium
#      confidence). Midpoint 9 m used. YAML default is 4.0 m — half the published
#      value — which would undersize all radial-build-dependent costs (blanket,
#      shield, structure, vessel volumes scale as r²). For a Low archetype-fit
#      concept the prompt requires populating spec with published values.
#
#    q_eng (engineering gain): Derivable from published power balance. P_grid =
#      2820 MWe, P_recirc = 600 MW (500 MW laser + 100 MW facility), so q_eng =
#      P_grid / P_recirc ≈ 4.7. YAML default is 4.0. Using the paper's power
#      balance rather than the default.
#
#    mn (neutron multiplier): Paper §4.2 states M_n = 1.10 from exothermic
#      6Li(n,α)T blanket reaction. YAML default is 1.1 — matches. Not overridden.
#
#    f_rep (repetition rate): Paper Table 2 states 10 Hz. YAML default is 10.0 Hz
#      — matches. Not overridden.
#
#    NOT in spec (blocked or not canonical):
#    - eta_pin (0.10 wallplug): Hard Rule 6 blocker. YAML default 0.10 matches
#      the paper's composite η_w* = 0.16 × 0.60 = 0.10. Documented, not passed.
#    - eta_th (0.44 thermal): Hard Rule 6 blocker. Library-owned via PowerCycle
#      ENUM. Paper's 0.44 includes 10% exothermic Li-6 boost over base 0.40.
#    - eta_dec (0.44 DEC): Hard Rule 6 blocker. DEC channel (30% of P_fus) not
#      expressible in LASER_IFE pulsed_conversion=thermal mode anyway.
#    - p_fus (8000 MW): Never a spec key (back-solved by library).
#    - E_driver (5 MJ laser energy): Not a CostingInput field; library back-solves
#      driver energy from q_eng + f_rep + eta_pin via inverse power balance.
#    - f_dec: Not in PULSED_REQUIRED; LASER_IFE uses pulsed_conversion=thermal.
#      BLF's 30% DEC channel is a modeling gap (no hybrid thermal+DEC mode exists).
spec = dict(
    plasma_t=9.0,   # chamber radius [m], midpoint of 8–10 m (paper §4.1, medium confidence)
    q_eng=4.7,      # P_grid/P_recirc = 2820/600 (paper Table 2 power balance)
)
P_native = 2820  # MWe — analysis.md Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Analysis §5b concludes zero enabled overrides. All 16 canonical accounts were
#    individually reviewed against Sunahara et al. (2025). The paper contains
#    detailed physics parameters and a power balance but zero dollar figures, unit
#    costs, material quantities with associated costs, or target fabrication cost
#    targets. Without any company-grounded cost data, there is no evidentiary basis
#    for a single override. The override-count rubric expects 6–12 for Low
#    archetype-fit, but that expectation assumes the dossier contains at least some
#    economic data — this is a data-availability problem, not an analysis problem.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
