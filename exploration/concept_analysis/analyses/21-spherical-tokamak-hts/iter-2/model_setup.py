"""1costingfe model: Spherical Tokamak HTS (Tokamak Energy) (Tokamak Energy).

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
from costingfe.validation import CostingInput, default_availability
from lib.model_setup_helpers import (
    generic_reference, run_native_and_1gw, print_cas_breakdown,
    enabled_overrides,
)

# 1. Specification — design-point inputs only, at native scale.
#    Geometry / physics / power. NO library-default re-passing.
spec = dict(
    R0=5.0,          # tokamak-energy-st-e1-dpp2025-abstract.md §Abstract (major radius)
    plasma_t=2.17,   # inferred: R0/A = 5.0/2.3 (minor radius a)
    elon=2.8,        # estimated: typical ST elongation; MAST-U κ~2.5–3.0, pulsed-ST paper cites κ=3
    B=5.25,          # tokamak-energy-st-e1-dpp2025-abstract.md §Abstract (on-axis toroidal field)
    p_input=50.0,    # estimated: ~20 MW RF for CS recharge + ECRH for CD/heating; total wallplug ~40–60 MW
    # p_ecrh not set separately — total p_input covers all auxiliary heating (ECRH-only flat-top)
    # Ip ~14 MA estimated but not a spec key
    # Pfus ~1500 MW estimated but library back-solves from P_native + p_input
)
P_native = 450.0     # MWe — tokamak-energy-st-e1-dpp2025-abstract.md §Abstract (lower bound of 450–750 MW range)

# 2. Model.
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#
# Section 5b concludes: 0 enabled overrides. The dossier provides architectural
# descriptions and materials science characterization (WC cermet shielding,
# Demo4 HTS magnets, ECRH heating) but publishes no cost figures, mass
# estimates, or unit prices for any CAS account. All accounts ride the library
# default for the TOKAMAK archetype.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)

# ── F-1: Sensitivity sweeps for low-confidence spec inputs ───────────────
# p_input (50 MW, low confidence, range 40–60 MW) and elon (2.8, low
# confidence, range 2.5–3.0) are the two lowest-confidence spec keys
# feeding directly into the cost model. Sweep each individually at native
# scale to bound the LCOE impact of acknowledged parameter uncertainty.
# plasma_t (2.17 m, medium confidence) is a deterministic derivation from
# R0/A and is not independently swept.
_avail = default_availability(model.concept)
_life = CostingInput.model_fields["lifetime_yr"].default
_enabled = enabled_overrides(overrides)

print("\np_input sweep (native 450 MWe; estimated 40–60 MW wallplug auxiliary):")
for _pi in [40.0, 45.0, 50.0, 55.0, 60.0]:
    _r = model.forward(
        net_electric_mw=P_native, n_mod=1,
        availability=_avail, lifetime_yr=_life, noak=True,
        cost_overrides=_enabled,
        override_reference_mw=P_native,
        **{**spec, "p_input": _pi},
    )
    _mark = "  <- spec" if _pi == 50.0 else ""
    print(f"  p_input={_pi:.0f} MW: LCOE={_r.costs.lcoe:.1f} $/MWh{_mark}")

print("\nelon sweep (native 450 MWe; typical ST range κ=2.5–3.0):")
for _k in [2.5, 2.6, 2.8, 3.0]:
    _r = model.forward(
        net_electric_mw=P_native, n_mod=1,
        availability=_avail, lifetime_yr=_life, noak=True,
        cost_overrides=_enabled,
        override_reference_mw=P_native,
        **{**spec, "elon": _k},
    )
    _mark = "  <- spec" if _k == 2.8 else ""
    print(f"  elon={_k:.1f}: LCOE={_r.costs.lcoe:.1f} $/MWh{_mark}")
