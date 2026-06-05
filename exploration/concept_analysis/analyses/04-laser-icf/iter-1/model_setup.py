"""1costingfe model: Laser ICF (HB11 Energy) (hb11).

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
#    From analysis.md Section 5 Design Point Parameters.
#    McKenzie et al. 2023 model (500 MWe scenario).
#
#    Archetype-Fit: Low — LASER_IFE is the closest available ConfinementConcept
#    but HB11's picosecond CPA + capacitor-coil p-B11 targets depart
#    significantly from the library's nanosecond DT-ICF archetype.
#
#    For laser IFE (PULSED family), the library uses q_eng to derive driver
#    energy via the pulsed inverse power balance. p_input is an MFE-only key
#    and is NOT passed here (the existing root model_setup.py passed it
#    incorrectly; the pulsed path ignores it).
#
#    eta_pin (laser wall-plug efficiency): McKenzie states 20%, library default
#    is 10%. eta_pin is ENUM-driven and cannot be overridden in spec per Rule 6.
#    Documenting the discrepancy only.
spec = dict(
    # Chamber geometry (spherical chamber for IFE)
    # Patent describes ≥1m diameter sphere; library default 4.0m is adequate
    # pending data. No HB11-specific chamber dimension published.
    plasma_t=4.0,  # Chamber radius [m] — library default

    # Blanket and shielding geometry — library defaults
    blanket_t=0.80,    # Blanket thickness [m]
    ht_shield_t=0.25,  # Shield thickness [m]

    # Auxiliary power loads
    p_trit=0.0,     # No tritium processing for p-B11 (aneutronic)
    p_cryo=0.0,     # No cryogenics: room-temp solid targets, no superconducting magnets
    p_target=1.0,   # Target factory power [MW] — library default
)

P_native = 500  # MWe — McKenzie et al. 2023 model scenario

# 2. Model.
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.PB11)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Archetype-Fit: Low → expected 6–12 enabled overrides. Analysis produced 9.
#    All overrides are analyst-derived (provenance: derived) from McKenzie et al.
#    2023 qualitative statements and patent architecture; no company-published
#    cost figures exist. The dominant theme is architectural elimination of
#    DT-specific subsystems (tritium blanket, shielding, pulsed power,
#    activated-component maintenance) that the p-B11 aneutronic fuel cycle
#    renders unnecessary.
overrides = [
    # C220101: Blanket — aneutronic, no tritium breeding
    {
        "account": "C220101",
        "value": 0.05 * generic.cas22_detail["C220101"],
        "enabled": True,
        "provenance": "derived",
        "source": (
            "link-10-1007-s10894-023-00349-9/output.md §Commercialisation; "
            "hb11-patent-reactor-design.md §Energy Conversion"
        ),
        "rationale": (
            "Aneutronic p-B11 reaction eliminates tritium-breeding blanket entirely. "
            "Neutron energy fraction ~0.1% from side reactions. No lithium blanket, "
            "no neutron multiplier, no tritium extraction. The 'first wall' is a "
            "stainless steel sphere (>=1m, 10mm wall). Retained at 5% of default "
            "to account for minimal energy-capture wall structure and alpha-particle "
            "thermal management. No company-published dollar figure; override is "
            "based on architectural elimination of the subsystem."
        ),
        "cost_basis": "noak",
    },
    # C220102: Radiation shield — negligible neutron wall loading
    {
        "account": "C220102",
        "value": 0.05 * generic.cas22_detail["C220102"],
        "enabled": True,
        "provenance": "derived",
        "source": "link-10-1007-s10894-023-00349-9/output.md §Commercialisation",
        "rationale": (
            "Neutron wall loading is negligible (~0.1% of fusion energy in side-"
            "reaction neutrons, 2 orders of magnitude below conventional fission "
            "per MW). Shield sizing scales to neutron wall loading. Retained at 5% "
            "to account for residual shielding against side-reaction neutrons and "
            "alpha-particle-induced activation (which McKenzie notes will need "
            "materials research)."
        ),
        "cost_basis": "noak",
    },
    # C220107: Pulsed-power capacitor bank — not present in HB11 design
    {
        "account": "C220107",
        "value": 0.0,
        "enabled": True,
        "provenance": "direct",
        "source": (
            "hb11-patent-reactor-design.md §Reactor Architecture; "
            "link-10-1007-s10894-023-00349-9/output.md §Commercialisation"
        ),
        "rationale": (
            "HB11 uses a laser driver, not a pulsed-power capacitor bank. No "
            "capacitor bank exists in this design. The driver cost is captured "
            "in C220104 (laser). Setting to zero eliminates double-counting."
        ),
        "cost_basis": "noak",
    },
    # C220108: Target factory — room-temperature consumable assemblies
    {
        "account": "C220108",
        "value": 100.0,
        "enabled": True,
        "provenance": "derived",
        "source": "link-10-1007-s10894-023-00349-9/output.md §Commercialisation",
        "rationale": (
            "McKenzie et al. 2023 state 'a target cost of several dollars per target "
            "is acceptable if a target gain of 200 can be achieved.' The target is a "
            "complex consumable assembly. Novel materials (borophene, white graphene) "
            "enable solution-based manufacturing. $100M is a placeholder for the "
            "target factory capital cost, analogous to other IFE target factory "
            "estimates. Highly uncertain — no published factory design or bottom-up "
            "cost estimate exists."
        ),
        "cost_basis": "noak",
    },
    # C220110: Remote handling — minimal activation environment
    {
        "account": "C220110",
        "value": 0.15 * generic.cas22_detail["C220110"],
        "enabled": True,
        "provenance": "derived",
        "source": "link-10-1007-s10894-023-00349-9/output.md §Commercialisation",
        "rationale": (
            "Negligible neutron activation eliminates the need for rad-hardened "
            "remote handling equipment. Maintenance can be performed with "
            "conventional equipment in a non-activated environment. Retained at "
            "15% for mechanical handling of consumable target assemblies, laser "
            "optics maintenance, and general reactor chamber access."
        ),
        "cost_basis": "noak",
    },
    # CAS21: Buildings — eliminated tritium/hot-cell infrastructure
    {
        "account": "CAS21",
        "value": 0.50 * generic.costs.cas21,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "link-10-1007-s10894-023-00349-9/output.md §Commercialisation; "
            "hb11-patent-reactor-design.md §Reactor Architecture"
        ),
        "rationale": (
            "Eliminated facilities: tritium processing building, hot cell for "
            "activated-component handling, heavy biological shielding structure, "
            "cryogenic target preparation facility. Retained: reactor building "
            "(simplified), turbine building (if thermal conversion), laser building, "
            "target fabrication facility, electrical building, control building. "
            "50% reduction reflects elimination of ~half the building scope of a "
            "DT IFE plant."
        ),
        "cost_basis": "noak",
    },
    # CAS27: Special materials — boron-11 commodity fuel, no tritium
    {
        "account": "CAS27",
        "value": 1.0,
        "enabled": True,
        "provenance": "derived",
        "source": "link-10-1007-s10894-023-00349-9/output.md §Introduction",
        "rationale": (
            "Initial reactor material inventory is solid hydrogen-boron fuel at "
            "room temperature. No cryogenic handling, no tritium, no lithium "
            "compounds, no FLiBe. Boron-11 is industrial commodity (~$1-5/kg). "
            "$1M placeholder covers initial fuel inventory and target assembly "
            "materials. Negligible relative to DT concepts requiring tritium "
            "($30k+/g startup inventory) and FLiBe."
        ),
        "cost_basis": "noak",
    },
    # CAS70: O&M — reduced activation-driven replacement
    {
        "account": "CAS70",
        "value": 0.50 * generic.costs.cas70,
        "enabled": True,
        "provenance": "derived",
        "source": "link-10-1007-s10894-023-00349-9/output.md §Commercialisation",
        "rationale": (
            "McKenzie et al.: 'significant operational costs of DT systems are "
            "primarily associated with the replacement of activated reactor "
            "components... For the HB11 system, these costs are reduced.' No "
            "neutron-driven component replacement (25-year lifetime assumed). "
            "Primary O&M cost is laser diode replacement ($1/W, 2.2 billion "
            "shot lifetime). 50% reduction from DT default reflects elimination "
            "of activated-component replacement program while retaining laser "
            "maintenance, target factory operations, and general plant O&M."
        ),
        "cost_basis": "noak",
    },
    # CAS80: Fuel cost — earth-abundant p-B11, no tritium
    {
        "account": "CAS80",
        "value": 0.5,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "link-10-1007-s10894-023-00349-9/output.md §Introduction; "
            "link-10-1007-s10894-023-00349-9/output.md §Commercialisation"
        ),
        "rationale": (
            "Raw fuel cost is negligible. Boron-11 is 80% of natural boron "
            "(industrial commodity). Hydrogen is ubiquitous. No tritium "
            "procurement. Annual boron consumption estimated at <10^6 tons "
            "against ~10^9 tons global reserves. $0.5M/yr placeholder. "
            "Target fabrication cost (the real fuel-cycle driver) is allocated "
            "to C220108."
        ),
        "cost_basis": "noak",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
