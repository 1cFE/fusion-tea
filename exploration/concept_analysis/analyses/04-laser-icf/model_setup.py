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
#    For laser IFE, the library calculates fusion power from driver specs via
#    the pulsed IFE model. We pass:
#    - p_input: recirculating/driver power (MW)
#    - Geometry: plasma_t (chamber radius)
#    - Auxiliary loads as needed
#    The library defaults handle f_rep, eta_pin, q_eng, and thermal conversion.
spec = dict(
    # Driver recirculating power (McKenzie: 50 MW laser driver input)
    # McKenzie §Commercialisation: 50 MW input to drive laser system (accounting
    # unclear: likely includes laser wall-plug power plus auxiliaries for 1 Hz
    # operation; not derivable from 30 kJ/shot at 20% efficiency alone, which
    # yields 150 kW average laser output, implying additional auxiliary loads
    # or pulsed peak power infrastructure).
    p_input=50.0,  # MW

    # Chamber geometry (spherical chamber for IFE)
    # Default from pulsed_laser_ife.yaml is 4.0m; no HB11-specific chamber dimension
    # Patent describes ≥1m diameter sphere; using library default pending data
    plasma_t=4.0,  # Chamber radius [m]

    # Blanket and shielding geometry (library defaults adequate for aneutronic)
    blanket_t=0.80,   # Blanket thickness [m]
    ht_shield_t=0.25,  # Shield thickness [m]

    # Auxiliary power loads (library defaults from pulsed_laser_ife.yaml)
    # p_pump, p_house, p_cryo, p_target are already set; override if concept differs
    # HB11 is aneutronic (p-B11), so p_trit should be zero
    p_trit=0.0,  # No tritium processing for p-B11

    # Target factory power (IFE consumable targets)
    p_target=1.0,  # MW (library default adequate pending target factory data)
)

P_native = 500  # MWe — McKenzie et al. 2023 model scenario

# 2. Model.
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.PB11)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5d.
#    Per F-1, the Low archetype-fit grade requires 6-12 enabled overrides to account
#    for structural departures from the library's DT-ICF archetype assumptions. All
#    overrides are analyst-derived (provenance: derived) from McKenzie et al. 2023
#    qualitative statements; no company-published cost figures exist.
overrides = [
    # C220101: Blanket — aneutronic energy capture (no tritium breeding)
    {
        "enabled": True,
        "account": "C220101",
        "value": generic.cas22_detail["C220101"] * 0.70,
        "provenance": "derived",
        "source": "analysis.md §5d (McKenzie et al. 2023 §Commercialisation)",
        "rationale": (
            "Aneutronic p-B11 blanket avoids tritium breeding infrastructure and uses "
            "simpler energy capture design (no lithium ceramics, no tritium extraction "
            "loops). McKenzie states 'there will be no need for tritium breeding' and "
            "notes reduced system complexity. Energy conversion via thermal (36-40%) or "
            "direct (45-64%) pathways structurally different from DT breeding blankets. "
            "30% cost reduction vs. library's DT-ICF blanket model reflects elimination "
            "of breeding subsystems while retaining thermal management and structural "
            "support. Conservative estimate pending detailed blanket design."
        ),
        "cost_basis": "noak",
    },
    # C220102: Radiation shield — 100× reduction in neutron flux
    {
        "enabled": True,
        "account": "C220102",
        "value": generic.cas22_detail["C220102"] * 0.30,
        "provenance": "derived",
        "source": "analysis.md §5d (McKenzie et al. 2023 §Commercialisation)",
        "rationale": (
            "McKenzie states p-B11 produces '~ 0.1%' neutron energy from side reactions, "
            "with 'number of neutrons per MW of electrical power 2 orders of magnitude "
            "lower than conventional uranium fission reactor.' Library's DT-ICF shield "
            "assumes ~80% neutron energy fraction; p-B11's <0.1% fraction eliminates need "
            "for heavy neutron shielding (borated concrete, steel layers). Shielding still "
            "needed for residual neutrons and alpha-generated X-rays, but at much reduced "
            "thickness/mass. 70% cost reduction reflects 100× reduction in neutron flux. "
            "Conservative pending chamber geometry details."
        ),
        "cost_basis": "noak",
    },
    # C220104: Dual-laser driver — absolute NOAK estimate. Library default
    #          models a single ~14 MW long-pulse DPSSL derived from YAML f_rep
    #          and q_eng (and recently recalibrated to ~$205M/MJ via
    #          1cFE/1costingfe#21), but HB11's actual driver is structurally a
    #          two-system stack (ns capacitor-coil + ps PETAWATT CPA). The
    #          relative-multiplier approach was anchoring 1.75x against the
    #          wrong cost basis. Replaced with an absolute NOAK derivation
    #          below; library issue tracking the dual-laser split is not yet
    #          filed (per-concept workaround pending that fix).
    {
        "enabled": True,
        "account": "C220104",
        "value": 1000.0,
        "provenance": "derived",
        "source": (
            "McKenzie et al. 2023 §Commercialisation ($1/W diode target, "
            "50 MW driver wallplug) + Focused Energy NOAK class ($0.5-1/J "
            "for ps CPA systems) + LIFE-class facility overhead studies "
            "(grating compressor + spatial filter cost fractions)"
        ),
        "rationale": (
            "HB11's actual driver is structurally a TWO-system stack that the "
            "library does not model. NOAK derivation, midpoint of an $800M-$1.5B "
            "range:\n"
            "  (a) ns capacitor-coil ~100 J + ~5 MW long-pulse DPSSL pump ~ $250M "
            "[McKenzie $1/W diode x 50 MW x ~5x DPSSL system multiplier for "
            "diodes-to-system NOAK]\n"
            "  (b) ps PETAWATT CPA at 30 kJ x 1 Hz: ~$80M materials [Focused Energy "
            "NOAK ~$0.7/J for ps systems] + ~$250M grating compressor + spatial "
            "filters with sub-mm rms wavefront [LIFE-class facility studies, "
            "$200-300M for 30 kJ-class CPA]\n"
            "  (c) Vacuum beam transport + diagnostics + commissioning ~$120M "
            "[DPSSL plant overhead at NOAK, 5-10% of materials]\n"
            "  (d) Integration + plant infrastructure 1.3x materials ~$200M\n"
            "Total: $250M + $330M + $120M + $200M = ~$900M-$1.1B; midpoint $1.0B. "
            "Sensitivity range $800M-$1.5B reflects ps CPA NOAK $/J uncertainty "
            "and grating-compressor pricing tier. The library's single $/J knob "
            "(driver_laser_per_mj) cannot capture the ns/ps split structurally; "
            "this absolute override is the right shape until a library-side "
            "driver_laser_ps_per_mj field exists (issue not yet filed; cited as "
            "follow-up in PR #37 ARC investigation)."
        ),
        "cost_basis": "noak",
    },
    # C220108: Target factory — room-temperature electromagnet consumables
    {
        "enabled": True,
        "account": "C220108",
        "value": 157.5,  # M$ annualized: $5/target × 31.5M targets/year
        "provenance": "derived",
        "source": "analysis.md §5d (McKenzie et al. 2023 §Commercialisation)",
        "rationale": (
            "McKenzie: 'target cost of several dollars per target is acceptable if target "
            "gain of 200 can be achieved.' At 1 Hz (31.5M targets/year), assume mid-range "
            "$5/target for capacitor-coil magnetic field assembly (nickel plates, coil "
            "windings, polyethylene foam, quartz fiber, HB11 fuel cylinder). Room-temperature "
            "solid targets avoid DT cryogenics (major cost advantage), but integrated "
            "electromagnet per shot adds complexity vs. simple pellet. $5/target × 31.5M/year = "
            "$157.5M/year annualized consumable cost, comparable to ~15-20% of OPEX for "
            "500 MWe plant. Uncertainty range $1-10/target; baseline at mid-range pending "
            "target factory prototype."
        ),
        "cost_basis": "noak",
    },
    # CAS21: Buildings — no tritium infrastructure
    {
        "enabled": True,
        "account": "CAS21",
        "value": generic.costs.cas21 * 0.80,
        "provenance": "derived",
        "source": "analysis.md §5d (McKenzie et al. 2023 §Commercialisation)",
        "rationale": (
            "McKenzie: 'there will be no need for tritium breeding, storage, handling, "
            "extraction or atmospheric recovery, or a radioactive waste treatment facility.' "
            "Aneutronic operation eliminates tritium processing buildings, hot cells for "
            "blanket handling under tritium containment, atmospheric recovery systems, and "
            "radioactive waste storage structures. Reactor building and turbine hall remain "
            "(if thermal conversion), but support building footprint reduced. 20% cost "
            "reduction vs. library's DT-ICF building model reflects eliminated tritium "
            "infrastructure. Conservative estimate; larger reduction possible if direct "
            "conversion eliminates turbine building."
        ),
        "cost_basis": "noak",
    },
    # CAS27: Special materials — boron-11 inventory (no tritium)
    {
        "enabled": True,
        "account": "CAS27",
        "value": 0.1,  # M$ = $100k
        "provenance": "derived",
        "source": "analysis.md §5d (McKenzie et al. 2023 §Introduction, §Commercialisation)",
        "rationale": (
            "Special materials inventory for p-B11: initial boron-11 fuel load only (no "
            "lithium blanket, no tritium inventory). McKenzie: natural boron is 80% B-11, "
            "'world's largest known mine ~1.2 billion metric tons,' commodity cost ~$1-2/kg. "
            "At 0.001 kg boron per target (1 cm × 2 mm cylinder, density 2.34 g/cm³), startup "
            "inventory for 1 week operation at 1 Hz = 604,800 targets × 0.001 kg = ~600 kg "
            "boron = $600-1,200 material cost. Round to $100k including handling, storage, and "
            "buffer inventory. Negligible compared to DT's tritium inventory cost (~kg of "
            "tritium at $30k/g). Hydrogen (protons) sourced from water, effectively free."
        ),
        "cost_basis": "noak",
    },
    # CAS70: O&M — reduced activation-driven replacement
    {
        "enabled": True,
        "account": "CAS70",
        "value": generic.costs.cas70 * 0.85,
        "provenance": "derived",
        "source": "analysis.md §5d (McKenzie et al. 2023 §Commercialisation)",
        "rationale": (
            "McKenzie: 'Significant operational costs of DT systems primarily associated with "
            "replacement of activated reactor components exposed to high neutron fluxes. For "
            "HB11 system, these costs are reduced' due to 2-orders-magnitude lower neutron "
            "production. Reactor lifetime 'not limited by neutron irradiation' (25 years "
            "assumed). Reduced first-wall/blanket replacement frequency and no tritium "
            "handling O&M (extraction, purification, accountability). Diode replacement cost "
            "flagged as 'critical cost driver' ($1/W, 2.2B shot lifetime), but this is laser "
            "subsystem maintenance, not unique to p-B11. 15% O&M reduction vs. library DT-ICF "
            "model reflects lower activation-driven component replacement. Conservative "
            "pending validation of 25-year lifetime under alpha bombardment."
        ),
        "cost_basis": "noak",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
