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
#    Geometry / physics / power. NO library-default re-passing.
#    Note: eta_th is ENUM-owned (PowerCycle) and cannot be specified here.
#    The design point assumes thermal cycle (steam) per 2025 website.
spec = dict(
    # Laser driver parameters
    laser_pulse_energy_kJ=30.0,       # Patent US10410752B2 line 326 example; McKenzie §Pathways to Increase Fusion Gain (30 PW × 1 ps)
    rep_rate_hz=1.0,                  # Patent line 326 "one reaction per second"; McKenzie assumes 1 Hz

    # Target and fuel
    target_gain=200.0,                # McKenzie §Commercialisation: range 100-300, using midpoint for baseline

    # Power balance
    p_input=50.0,                     # McKenzie §Commercialisation: 50 MWe to drive laser (10% recirculating fraction)
)
P_native = 500.0         # MWe — McKenzie et al. 2023 §Commercialisation

# 2. Model.
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.PB11)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {"account": "C220104", "value": 0.0, "enabled": False,
     "cost_basis": "noak", "provenance": "derived", "source": "McKenzie et al. 2023 §Commercialisation; Patent US10410752B2",
     "rationale": "HB11 uses dual laser drivers: (1) ns pulse (>100 J) to generate kilotesla magnetic field via capacitor-coil target, (2) ps petawatt CPA pulse (~30 kJ) for proton fast ignition. The 500 MWe plant requires 50 MW input to a 20% efficient laser producing 10 MW average output. McKenzie assumes diode cost $1/W and lifetime 2.2 billion shots, but no total driver capital cost is published. D-T laser ICF analogues (Xcimer $60-120/J NOAK, Inertia $700-1000/J) suggest order $2-30M per 30 kJ laser unit, but p-B11's dual-laser architecture and DPSSL technology requirements differ structurally from D-T DPSSL or KrF systems. Cannot propose justified override without company-grounded cost data. Library default for pulsed driver ($/J of driver energy) is retained with low confidence.",
     "blocked_by": "1cFE/1costingfe#2"},

    {"account": "C220108", "value": 27.0, "enabled": False,
     "cost_basis": "noak", "provenance": "derived", "source": "McKenzie et al. 2023 §Commercialisation",
     "rationale": "HB11 replaces the D-T ICF cryogenic target factory with room-temperature solid-state p-B11 targets consumed at 1 Hz. At 85% capacity factor, annual consumption is 27 million targets. McKenzie states 'a target cost of several dollars per target is acceptable if a target gain of 200 can be achieved.' Assuming $1/target (lower bound of 'several dollars'), annual cost is $27M. This is an annualized OPEX, not capital cost — the 1costingFE schema treats C220108 as target factory capital for IFE. Reinterpret C220108 as annual target production cost for p-B11 and include in CAS70 O&M instead. Override disabled pending schema clarification. If target cost is $3-5, annual cost is $80-135M, or $20-33/MWh — significant fuel cost relative to D-T.",
     "blocked_by": "1cFE/1costingfe#3"},

    {"account": "CAS23", "value": 0.0, "enabled": False,
     "cost_basis": "noak", "provenance": "direct", "source": "HB11 2025 website (hb11.energy/our-technology); McKenzie et al. 2023 §Commercialisation",
     "rationale": "The 2018 patent and 2020 public messaging described direct electrostatic conversion of alpha-particle energy at -1.4 MV, eliminating thermal cycle (CAS23 turbine plant = $0). The 2025 website states 'The energy released drives a conventional steam cycle generator' (repeated twice). McKenzie assumes generator conversion efficiency ε ∈ [36-40%], consistent with steam cycle. If steam cycle is actual architecture, CAS23 is non-zero (library default applies). If direct conversion is pursued (45-64% efficiency per McKenzie estimates), CAS23 = 0. Design point frontmatter specifies 'Thermal (steam)' (medium confidence), suggesting CAS23 override to $0 is not justified. Energy conversion architecture contradiction is unresolved — propose no override pending clarification from company or independent engineering study.",
     "blocked_by": "1cFE/1costingfe#4"},

    {"account": "CAS27", "value": 0.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct", "source": "McKenzie et al. 2023 §Introduction, §Commercialisation",
     "rationale": "p-B11 aneutronic fuel eliminates tritium breeding blanket. No lithium inventory, no beryllium neutron multiplier, no tritium handling or recovery systems. Side reactions produce ~0.1% neutron energy, but McKenzie states 'the number of neutrons produced per MW of electrical power would be 2 orders of magnitude lower than in conventional uranium fission reactor' and neutron effects are 'not expected to be a concern.' CAS27 special materials (tritium inventory, Li-6 enrichment, breeding blanket fill) are structurally inapplicable. Override CAS27 to $0. The boron fuel itself is consumed annually (~tons/year at <$10/kg for natural boron) — include in CAS80 fuel cost instead."},

    {"account": "CAS70", "value": 0.85 * generic.costs.cas70, "enabled": True,
     "cost_basis": "noak", "provenance": "derived", "source": "McKenzie et al. 2023 §Commercialisation",
     "rationale": "McKenzie states 'Significant operational costs of DT systems are primarily associated with the replacement of the activated reactor components exposed to high neutron fluxes. For the HB11 system, these costs are reduced for several reasons including that there will be no need for tritium breeding, storage, handling, extraction or atmospheric recovery, or a radioactive waste treatment facility.' Aneutronic operation (side reactions <0.1% neutrons) eliminates tritium fuel cycle OPEX, hot-cell blanket replacement, and radioactive waste handling — major D-T cost drivers. However, HB11 substitutes laser diode replacement ($5M/year at $1/W × 50 MW / 10 yr) and consumable target cost ($27-135M/year). Net OPEX effect is unclear — propose 15% reduction (0.85× library CAS70) for tritium elimination, but flag high uncertainty. Diode and target costs may offset savings."},

    {"account": "CAS80", "value": 50.0, "enabled": False,
     "cost_basis": "noak", "provenance": "derived", "source": "McKenzie et al. 2023 §Commercialisation; natural boron market price ~$5/kg",
     "rationale": "McKenzie estimates global boron supply needs for p-B11 energetics at <10⁶ tons/year (comparable to uranium fission tonnage), 1000× less than global boron reserves. For a 500 MWe plant, annual boron consumption is [estimated: 500 MWe × 8760 hr/yr × 0.85 CF / (8.7 MeV/reaction × 3 α/reaction × 1.6e-13 J/MeV × NA reactions/mol) / (11 g/mol B-11) ≈ 10,000 kg/yr]. At natural boron price ~$5/kg (industrial grade), fuel cost is $50k/yr or $0.01/MWh — negligible. If isotopic enrichment (80% → 99% B-11) is required, enrichment cost could dominate, but McKenzie notes this must be weighed against side-reaction neutron concerns. No enrichment cost data available. Propose CAS80 override disabled pending fuel cycle detail. Library default (D-T fuel cost) is structurally inapplicable but may approximate order-of-magnitude if targets are considered 'fuel' rather than blanket materials.",
     "blocked_by": "1cFE/1costingfe#5"},
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
