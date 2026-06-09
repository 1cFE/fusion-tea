"""1costingfe model: FRC w/ Direct Conversion (Helion Energy) (Helion Energy).

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
#
#    CRITICAL: Helion's pulsed FRC architecture has limited published geometry.
#    The concept uses PULSED_FRC archetype, which is a linear cylindrical device,
#    NOT a toroidal configuration. Therefore, tokamak-style geometry parameters
#    (R0, plasma_t, elon) are NOT applicable and are OMITTED per
#    analyst-patch-spec-anchors.md §What NOT to set.
#
#    Power-conversion efficiencies (eta_dec, eta_th, eta_pin, etc.) are ENUM-owned
#    and MUST NOT appear in spec (see Hard Rule 6 and the archetype-specific blocklist).
#    The library's PULSED_FRC + INDUCTIVE_DEC selection automatically handles the
#    conversion path; Helion's claimed 85-95% efficiency is a library-level property,
#    not settable via spec until upstream costingfe adds a higher-eta variant.
spec = dict(
    q_eng=4.0,      # analyst-patch-spec-anchors.md — inferred engineering Q from net-gain requirement
    f_rep=1.5,      # analyst-patch-spec-anchors.md — midpoint of 1-2 Hz range from ARPA-E + website
)
P_native = 50.0     # MWe — analysis.md Design Point block; Microsoft PPA target 2028

# 2. Model.
model = CostModel(concept=ConfinementConcept.PULSED_FRC, fuel=Fuel.DHE3)

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
overrides = [
    {
        "account": "CAS23",
        "value": 0.0,
        "enabled": True,
        "provenance": "direct",
        "source": "helion-website-technology.md §Energy Capture",
        "rationale": (
            "Direct inductive energy conversion via Faraday's law eliminates the steam cycle entirely. "
            "No turbines, condensers, steam generators, or heat exchangers are required. The library's "
            "thermal cycle cost (CAS23) does not apply to this concept. This is a direct architectural "
            "fact, not a cost estimate — the subsystem does not exist."
        ),
        "cost_basis": "noak",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
