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

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {"account": "C220103", "value": 0.04 * generic.costs.cas22, "enabled": True,
     "cost_basis": "noak", "provenance": "derived", "source": "helion-website-technology.md §Magnets; contrary-research-helion.md §Magnet Materials",
     "rationale": "Helion uses pulsed resistive electromagnets ('regular aluminum magnets') rather than HTS-REBCO superconducting coils. The library default for C220103 assumes HTS magnet costs (~$50-150M for tokamak-scale coils). Resistive coils are 1-2 orders of magnitude cheaper per unit field strength-volume (aluminum and copper conductor, no cryogenics, no REBCO tape), but require continuous cooling and have I²R losses. At 40 T peak field and ~50 MJ stored energy, rough estimate: 50-100 tonnes aluminum/copper conductor at $2,500-9,000/tonne = $250K-$1M material; winding, insulation, structural support, and cooling systems add 10-50× material cost → $5-20M for coil subsystem at FOAK. This is ~10-20% of typical HTS coil costs for similar stored energy. To achieve absolute cost of $5-10M (midpoint $7.5M) at native scale where generic CAS22 ≈ $188M, override multiplier = $7.5M / $188M ≈ 0.04 (4% of generic CAS22 subtotal). This yields resistive magnet cost consistent with bottom-up material and fabrication estimates."},

    {"account": "C220102", "value": 0.2, "enabled": True,
     "cost_basis": "noak", "provenance": "derived", "source": "analysis.md §4 (Archetype Fit), lines 230-237; analogue cost proxies for borated concrete/polyethylene vs. D-T steel/lithium blankets",
     "rationale": "Helion's D-He3 fuel produces ~20× lower neutron flux than D-T (neutrons from side D-D reactions only, not primary fusion channel). The library default for C220102 assumes D-T tokamak radiation shielding: thick steel/lithium blankets and massive biological shields totaling $10-50M for 500 MWe, scaling to ~$2-10M for 50 MWe. Helion's lower neutron flux permits lighter shielding: borated polyethylene panels or borated concrete rather than thick steel/lithium blankets. Analysis estimates ~$50-100K for borated polyethylene/concrete shielding (industrial shielding panel costs at $50-200/m², ~500-1000 m² for vessel surface area → $25-200K material + installation). This is ~1-2% of D-T shielding costs. However, the library default likely includes biological shields, access labyrinths, and other fixed structures that scale with building volume, not neutron flux. Conservative override: 20% of library default (~$0.2M at 50 MWe scale) to account for lighter material but similar installation complexity. This brings C220102 from ~$1-2M (library default) to ~$0.2M."},

    {"account": "C220104", "value": 25.0, "enabled": True,
     "cost_basis": "noak", "provenance": "derived", "source": "helion-website-technology.md §Capacitor Bank; [industry capacitor cost proxies]",
     "rationale": "Helion's capacitor bank ('>50 MJ total energy storage,' 'thousands of high-voltage pulsed capacitors') serves as the primary pulsed driver for FRC formation, acceleration, and compression. The library default for C220104 is laser driver or accelerator costs ($/J of driver energy), which are typically $100-500/J for ICF lasers or heavy-ion beamlines. Capacitors cost ~$0.05-$0.50/J at industrial volume (pulsed power applications). At 50 MJ, cost is $2.5M-$25M depending on voltage, ripple current, and cycle life. Adding IGBTs for switching (~$0.10-$0.50/W, 50 MW → $5-25M) gives combined capacitor-IGBT cost of $10-50M. Using midpoint $25M for FOAK. This is $/J basis: $25M / 50 MJ = $500/J, but this is total system cost, not driver-energy basis. Library expects $/J of *driver energy delivered to plasma*, not stored energy. If capacitor-to-plasma efficiency is 80%, then 50 MJ stored → 40 MJ delivered → $25M / 40 MJ = $625/J delivered. Using $25M as absolute override rather than $/J, since the library's $/J metric is laser/accelerator-specific and doesn't map cleanly to capacitor banks. Override: $25M capital cost for capacitor-IGBT system."},

    {"account": "C220107", "value": 0.0, "enabled": True,
     "cost_basis": "noak", "provenance": "derived", "source": "helion-website-technology.md §Capacitor Bank (capacitors already costed in C220104)",
     "rationale": "C220107 is 'power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored)'. For Helion, the capacitor bank is the pulsed power source and is already costed in C220104 (primary driver). The resistive magnets are powered by the same capacitor bank (capacitors discharge through coils to generate magnetic field for compression). There is no separate 'magnet power supply' distinct from the driver capacitor bank. To avoid double-counting, set C220107 = 0. This is an analyst-derived accounting decision based on the dual-function of the capacitor bank (driver + magnet power supply), not a company-stated cost figure. The source citation supports the technical rationale (capacitor bank serves both functions), but the zero value is analyst-determined to prevent double-counting within the model's cost structure."},

    {"account": "C220109", "value": 0.08 * generic.costs.cas22, "enabled": True,
     "cost_basis": "noak", "provenance": "derived", "source": "helion-website-technology.md §Energy Capture; Helion 2021 press release (95% round-trip efficiency); [analogue: electrostatic DEC costs for mirrors]",
     "rationale": "Helion uses direct inductive energy conversion: expanding magnetized plasma induces current in surrounding coils, converting charged particle energy to electricity without a thermal cycle. The library default for C220109 assumes electrostatic direct energy converters (bias grids, collector plates) used in magnetic mirror concepts. Helion's inductive approach is fundamentally different: the same coils used for compression also serve as energy recovery coils (dual-function), and the conversion mechanism is Faraday induction, not electrostatic potential. Capital cost for inductive DEC is primarily the power electronics (IGBTs, transformers, grid interface) to convert pulsed AC (from coil flux change) to grid-quality DC or 60 Hz AC. Estimated at $10-20M for 50 MWe (power electronics are ~$0.20-$0.40/W for utility-scale converters, midpoint $15M). To achieve absolute cost of $10-20M (midpoint $15M) at native scale where generic CAS22 ≈ $188M, override multiplier = $15M / $188M ≈ 0.08 (8% of generic CAS22 subtotal). The coils themselves are already costed in C220103; this override captures only the power electronics and grid interface for energy recovery."},

    {"account": "CAS23", "value": 0.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct", "source": "helion-website-technology.md §Energy Capture; contrary-research-helion.md §Energy Recovery",
     "rationale": "Helion uses direct inductive energy conversion with no steam cycle ('No steam cycle required,' '85-95% direct electricity capture efficiency without steam turbines'). CAS23 is 'Turbine plant equipment (thermal cycle)' — steam/gas turbines, condensers, heat exchangers, cooling towers. For Helion, this account is $0 (not applicable). The charged particles from D-He3 fusion transfer energy to the magnetic field via plasma expansion, and the field induces current in coils; there is no intermediate thermal working fluid. This is a major differentiator from D-T concepts (which use steam Rankine or sCO2 Brayton cycles) and eliminates ~$50-150M in turbine-generator-BOP costs for a 50 MWe plant (rough scaling from larger plants). The library will compute CAS23 from thermal power and efficiency assumptions; override to zero."},
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
