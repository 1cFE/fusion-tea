"""1costingfe model: FRC w/ Direct Conversion (Helion Energy).

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
#    Note: Helion's pulsed colliding-FRC concept has limited published geometry.
#    The chamber is described as "~2× Polaris" with Polaris at "~60 ft length"
#    (helion-prototype-generations.md), implying Orion ~30-40 m length, ~2-3 m
#    diameter, but detailed R0, plasma_t, elon, and other tokamak-geometry
#    parameters are not applicable or not disclosed. The library may have
#    PULSED_FRC-specific geometry defaults; we provide only what's sourced.
#
#    IMPORTANT: eta_dec and eta_th are ENUM-owned (PowerCycle / PulsedConversion)
#    and MUST NOT appear in spec. PULSED_FRC defaults to PulsedConversion.INDUCTIVE_DEC,
#    which carries its own efficiency. To express Helion's claimed 85-95% efficiency,
#    we would need to add a new PulsedConversion variant in costingfe upstream, not
#    override here. The library default INDUCTIVE_DEC efficiency is used as-is.
spec = dict(
    # Pulsed operation parameters (sourced from analysis Section 5)
    q_eng=4.0,  # engineering Q (P_fus / P_input) — inferred from need for net gain after recirculating power
    f_rep=1.5,  # Hz — midpoint of 1-2 Hz range (docslib-helion-arpa-e-presentation.md §Power: "50 MW at 2 Hz"; helion-website-technology.md: "possibly 2 Hz to 10 Hz")
    # Compression field and energy storage (sourced)
    # B0 not directly a forward() parameter for PULSED_FRC; library may derive from stored energy
    # e_stored_mj not in spec dict; library computes from q_eng, f_rep, power
    # No R0, plasma_t, elon — not applicable to pulsed linear FRC
    # No f_dec — for PULSED concepts, the PulsedConversion ENUM determines conversion path
)
P_native = 50.0  # MWe — Microsoft PPA target (helion-prototype-generations.md §Orion; contrary-research-helion.md §Power Output)

# 2. Model.
model = CostModel(concept=ConfinementConcept.PULSED_FRC, fuel=Fuel.DHE3)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry.
#
# 2026-06-17: stripped four overrides that were fighting the PULSED_FRC library
# design rather than augmenting it:
#   - C220103 (resistive coils @ 4% of CAS22)
#   - C220104 (capacitor bank @ $25M absolute)
#   - C220107 ($0 to avoid double-counting after moving cap bank to C220104)
#   - C220109 (DEC power electronics @ 8% of CAS22 absolute)
#
# PULSED_FRC was authored specifically for Helion (cas22.py:71 sets n_coils=0;
# cas22.py:545-547 routes the capacitor bank through C220107 at $/J_stored;
# cas22.py:601-608 computes C220109 INDUCTIVE_DEC as a markup on C220107). The
# stripped overrides moved the cap bank to C220104 at a $25M absolute value and
# zeroed C220107 to avoid double-counting — but the "double-counting" was created
# by the move itself. They also broke the C220109 ↔ C220107 physical coupling
# the library was designed to model. Net effect was an understated cap-bank cost
# at all scales and an LCOE projection systematically too low at 1 GWe.
#
# The two remaining overrides are architectural facts, not cost re-routing:
#   - C220102 (D-He3 lower neutron flux → lighter shielding)
#   - CAS23 (direct inductive conversion, no steam cycle)
overrides = [
    {"account": "C220102", "value": 0.2, "enabled": True,
     "cost_basis": "noak", "provenance": "derived", "source": "analysis.md §4 (Archetype Fit), lines 230-237; analogue cost proxies for borated concrete/polyethylene vs. D-T steel/lithium blankets",
     "rationale": "Helion's D-He3 fuel produces ~20× lower neutron flux than D-T (neutrons from side D-D reactions only, not primary fusion channel). The library default for C220102 assumes D-T tokamak radiation shielding: thick steel/lithium blankets and massive biological shields totaling $10-50M for 500 MWe, scaling to ~$2-10M for 50 MWe. Helion's lower neutron flux permits lighter shielding: borated polyethylene panels or borated concrete rather than thick steel/lithium blankets. Analysis estimates ~$50-100K for borated polyethylene/concrete shielding (industrial shielding panel costs at $50-200/m², ~500-1000 m² for vessel surface area → $25-200K material + installation). This is ~1-2% of D-T shielding costs. However, the library default likely includes biological shields, access labyrinths, and other fixed structures that scale with building volume, not neutron flux. Conservative override: 20% of library default (~$0.2M at 50 MWe scale) to account for lighter material but similar installation complexity. This brings C220102 from ~$1-2M (library default) to ~$0.2M."},

    {"account": "CAS23", "value": 0.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct", "source": "helion-website-technology.md §Energy Capture; contrary-research-helion.md §Energy Recovery",
     "rationale": "Helion uses direct inductive energy conversion with no steam cycle ('No steam cycle required,' '85-95% direct electricity capture efficiency without steam turbines'). CAS23 is 'Turbine plant equipment (thermal cycle)' — steam/gas turbines, condensers, heat exchangers, cooling towers. For Helion, this account is $0 (not applicable). The charged particles from D-He3 fusion transfer energy to the magnetic field via plasma expansion, and the field induces current in coils; there is no intermediate thermal working fluid. This is a major differentiator from D-T concepts (which use steam Rankine or sCO2 Brayton cycles) and eliminates ~$50-150M in turbine-generator-BOP costs for a 50 MWe plant (rough scaling from larger plants). The library will compute CAS23 from thermal power and efficiency assumptions; override to zero."},
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
