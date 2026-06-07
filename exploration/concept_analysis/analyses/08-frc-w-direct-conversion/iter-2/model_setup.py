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
#
#    Archetype-Fit: Low. ConfinementConcept.PULSED_FRC is the closest available
#    framework match for Helion's pulsed bilateral colliding-FRC architecture
#    (aluminium coils, inductive DEC, no HTS, no thermal cycle). The library
#    PULSED_FRC YAML is calibrated to a Helion-like device, so geometry and
#    power-balance defaults are more aligned than any other archetype would be.
#
#    Published design-point parameters mapped to canonical spec keys:
#      f_rep — ARPA-E presentation explicitly states "50 MW at 2 Hz"
#              (docslib-helion-arpa-e-presentation.md §Fusion Engine Design Point)
#
#    Parameters excluded from spec and why:
#      B=40 T  — plasma compression field; PULSED_FRC forward() does not accept B
#                (B is an MFE archetype key, not in the PULSED_FRC YAML).
#                b_center (coil-center field, 5 T default) is the relevant YAML
#                key but it refers to the coil surface field, not the 40 T plasma
#                compression field — they are distinct quantities.
#      n_e, T_e — plasma density and temperature; accepted by MFE archetypes for
#                radiation / confinement calculations but not part of the PULSED_FRC
#                forward() signature (strict-kwarg validator rejects them).
#      p_input  — not in the pulsed forward() signature (MFE-only); energy balance
#                uses q_eng + f_rep.
#      q_eng    — fusion gain is unpublished for Orion (Q_plasma > 1 not yet
#                demonstrated); YAML default 3.0 is the calibrated placeholder.
#      eta_pin, eta_dec — efficiency keys, YAML/ENUM-owned per rule 6.
#
#    Geometry note: standard torus spec keys (R0, plasma_t as minor radius, elon)
#    do not map to Helion's linear bilateral FRC. The PULSED_FRC YAML already
#    has R0=0.0 and plasma_t=0.5 (linear-machine calibrated defaults). Orion
#    device geometry (compression zone radius, half-length) is not published.
#    Leaving geometry fields at YAML defaults.
spec = dict(
    f_rep=2.0,   # Hz — ARPA-E: "50 MW at 2 Hz" (high confidence)
)
P_native = 50.0  # MWe — Microsoft PPA / ARPA-E design point

# 2. Model.
model = CostModel(concept=ConfinementConcept.PULSED_FRC, fuel=Fuel.DHE3)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
#     `generic` is the library's bare answer at P_native; relative overrides
#     below anchor to this reference. ALWAYS emit this line.
generic = generic_reference(model, spec, P_native)

# 3. Override registry — eight entries, transcribed from analysis Section 5b.
#    All relative values use the modular-fleet frame per override-semantics policy.
#
#    C220101 and CAS27 are omitted: the PULSED_FRC/D-He3 library calibration already
#    prices both accounts at zero (no tritium-breeding blanket; no LiPb/FLiBe fill).
#    Overriding a zero-valued account has no effect on LCOE and is misleading.
overrides = [
    # C220102 — Radiation shield: 2.45 MeV DD neutrons vs 14.1 MeV D-T neutrons.
    # Helion: ~1 m solid borated polyethylene / borated concrete (hospital-class).
    # Shield mass, material cost, and installation are dramatically reduced.
    {"account": "C220102",
     "value": 0.25 * generic.cas22_detail["C220102"],
     "enabled": True,
     "cost_basis": "noak",
     "provenance": "derived",
     "source": "dossier.md §Neutron Management; helion-website-technology.md §Shielding",
     "rationale": (
         "Library C220102 prices a radiation shield sized to 14.1 MeV D-T neutron "
         "wall loading. D-He3 DD side-reaction neutrons are 2.45 MeV — far less "
         "penetrating. Helion states 'approximately one-meter solid barrier' of "
         "borated polyethylene and borated concrete, explicitly compared to hospital "
         "particle-beam shielding. At 2.45 MeV, penetration depth in concrete is "
         "roughly 1/5 that of 14.1 MeV neutrons, and the neutron energy fraction is "
         "~5% vs ~80% for D-T. Shield mass, material cost, and installation complexity "
         "are all dramatically reduced. 0.25 × library default for a fleet of this "
         "device at 1 GWe reflects the much lighter shielding requirement."
     )},

    # C220103 — Confinement magnets: pulsed aluminium coils, no HTS.
    # CEO Kirtley: "regular aluminum magnets". No REBCO, no cryostat, no cryogenic
    # plant. Driver capital is in C220107; this account is the coil winding only.
    {"account": "C220103",
     "value": 0.05 * generic.cas22_detail["C220103"],
     "enabled": True,
     "cost_basis": "noak",
     "provenance": "derived",
     "source": (
         "dossier.md §Magnet Type; helion-website-technology.md §Magnets; "
         "contrary-research-helion.md §Magnets"
     ),
     "rationale": (
         "Library C220103 prices HTS-REBCO confinement coils (conductor + winding + "
         "cryostat) at roughly $44k/kg-equivalent for REBCO tape. Helion uses pulsed "
         "aluminium electromagnetic coils ('regular aluminum magnets' per CEO Kirtley) "
         "driven by a capacitor bank. There is no REBCO, no cryostat, no cryogenic "
         "plant, and no quench protection system. Pulsed aluminium coils are wound from "
         "commodity conductor material with no exotic procurement. The per-module coil "
         "cost is a small fraction of HTS coil cost; the driver capital has moved "
         "entirely into C220107 (capacitor bank). For the library's modular-fleet "
         "default at 1 GWe (n_mod = 20 modules each contributing one coil set), "
         "0.05 × captures the aluminium coil winding cost without any superconductor, "
         "cryostat, or cryogenic infrastructure premium."
     )},

    # C220107 — Pulsed-power capacitor bank: the dominant driver cost.
    # SfA white paper NOAK target: <$0.50/J. At 50 MJ per module:
    # 50,000,000 J × $0.50/J = $25M per module (Class U).
    {"account": "C220107",
     "value": 25.0,
     "enabled": True,
     "cost_basis": "noak",
     "provenance": "derived",
     "source": (
         "helion-website-technology.md §Capacitor Bank; "
         "docslib-helion-arpa-e-presentation.md §Fusion Engine"
     ),
     "rationale": (
         "C220107 prices the pulsed-power capacitor bank at $/J stored. Helion stores "
         ">50 MJ per module at tens of kV. Unit cost: the SfA white paper (Science for "
         "America, May 2023) identifies that commercial viability requires capacitor "
         "cost to fall from the current ~$5/J to <$0.50/J through NOAK manufacturing "
         "learning, analogous to battery cost trajectories. Helion manufacturers some "
         "components in-house. At the NOAK target of $0.50/J and a 50 MJ bank: "
         "50,000,000 J × $0.50/J = $25M per module. This is Class U (per-module), so "
         "the 1 GWe fleet of n_mod = 20 modules costs $500M in total capacitor bank "
         "capital. The library's generic value for C220107 at $/J stored likely differs "
         "from this assumption; 25.0 M$ per module is the NOAK-derived estimate. The "
         "$0.50/J unit cost is from a sector analogue (SfA 2023), not a "
         "Helion-published figure — provenance is derived."
     )},

    # C220109 — Direct energy converter: $0 because DEC is physically integrated.
    # The same coils that compress the plasma recover energy via Faraday induction.
    # The DEC IS C220103 + C220107. Separate C220109 would double-count.
    {"account": "C220109",
     "value": 0.0,
     "enabled": True,
     "cost_basis": "noak",
     "provenance": "direct",
     "source": (
         "helion-website-technology.md §Energy Capture; "
         "contrary-research-helion.md §Energy"
     ),
     "rationale": (
         "Helion's inductive DEC is physically integrated into the pulsed "
         "electromagnetic coil system: the same coils that compress the plasma also "
         "recover energy from the expanding magnetised plasma via Faraday induction. "
         "There is no separate direct-energy-converter hardware — the DEC IS the coil "
         "system (C220103) and the capacitor bank (C220107). Pricing C220109 as a "
         "standalone account would double-count the coil and bank capital already "
         "captured above. The correct per-module charge for C220109 in a 1 GWe fleet "
         "of this device is $0. Company-published architecture confirms the integrated "
         "approach."
     )},

    # C220110 — Remote handling: ~hospital-accelerator class, not D-T hot-cell class.
    # Helion's 2.45 MeV DD neutron environment (5% of fusion energy) permits personnel
    # access with modest shielding; full rad-hardened manipulators not required.
    {"account": "C220110",
     "value": 0.20 * generic.cas22_detail["C220110"],
     "enabled": True,
     "cost_basis": "noak",
     "provenance": "derived",
     "source": (
         "dossier.md §Neutron Management; helion-website-technology.md §Shielding"
     ),
     "rationale": (
         "Library C220110 prices remote handling equipment sized for a high-neutron "
         "D-T environment (rad-hardened manipulators, hot cells, shielded transport "
         "casks). Helion's D-He3 fuel produces ~5% neutron energy at 2.45 MeV — a "
         "neutron environment comparable to hospital accelerator facilities, not a "
         "fission or D-T fusion plant. Personnel access to the machine with modest "
         "shielding is feasible; full remote-handling infrastructure is not required. "
         "The library's per-module remote handling cost for a 1 GWe fleet is ~5× what "
         "Helion needs. 0.20 × library default captures a basic maintenance "
         "infrastructure with minimal radiation hardening."
     )},

    # CAS23 — Turbine plant: $0. Helion uses inductive DEC with no steam cycle.
    # Company publications explicitly state "No steam cycle required."
    {"account": "CAS23",
     "value": 0.0,
     "enabled": True,
     "cost_basis": "noak",
     "provenance": "direct",
     "source": (
         "helion-website-technology.md §Energy Capture; "
         "contrary-research-helion.md §Energy"
     ),
     "rationale": (
         "Helion converts fusion energy directly to electricity via inductive DEC — "
         "expanding magnetised plasma induces current in the surrounding coils. There "
         "is no thermal cycle: no steam generator, no turbine, no condenser. Company "
         "publications explicitly state 'No steam cycle required.' CAS23 for a 1 GWe "
         "fleet of this device is $0. This is Class P (power-proportional); the "
         "library default scales with electrical output."
     )},

    # CAS24 — Electrical plant: 60% of library default.
    # Grid interconnect + power electronics retained; turbine-hall switchgear removed.
    {"account": "CAS24",
     "value": 0.60 * generic.costs.cas24,
     "enabled": True,
     "cost_basis": "noak",
     "provenance": "derived",
     "source": "helion-website-technology.md §Energy Capture",
     "rationale": (
         "CAS24 covers switchyard, transformers, and plant electrical distribution. "
         "Helion's direct electricity output still requires power conditioning (AC "
         "conversion from pulsed DC inductive output), step-up transformers, and grid "
         "interconnect hardware. However, without a turbine-generator interface, "
         "turbine-hall electrical plant, and large synchronous generator switchgear, "
         "CAS24 is materially reduced. 0.60 × the library's 1 GWe power-proportional "
         "default captures the grid interconnect and power electronics while removing "
         "the turbine-side electrical infrastructure. Class P."
     )},

    # CAS26 — Heat rejection: 10% of library default.
    # DEC recovers 85–95% of energy; waste heat is only from resistive losses,
    # DD neutron capture (~5%), and DEC inefficiency (~5–15%). Total heat rejection
    # is roughly 10–20% of a thermal-cycle plant at the same electrical output.
    {"account": "CAS26",
     "value": 0.10 * generic.costs.cas26,
     "enabled": True,
     "cost_basis": "noak",
     "provenance": "derived",
     "source": (
         "helion-website-technology.md §Energy Capture; "
         "contrary-research-helion.md §Energy"
     ),
     "rationale": (
         "CAS26 prices heat rejection (cooling towers, circulating water) sized for "
         "the waste heat from a thermal-cycle plant, which rejects roughly 55–60% of "
         "fusion thermal power. Helion's DEC recovers 85–95% of fusion energy as "
         "electricity; waste heat to reject is primarily from resistive losses in "
         "coils, neutron capture in the shield (~5% of fusion energy), and DEC "
         "inefficiency (~5–15% of fusion energy). Total heat rejection requirement is "
         "roughly 10–20% of a comparable thermal-cycle plant at the same electrical "
         "output. 0.10 × the library's 1 GWe power-proportional default reflects this "
         "dramatically reduced cooling burden. Class P."
     )},

]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
