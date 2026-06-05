"""1costingfe model: Dense Plasma Focus (LPP Fusion) (LPPFusion).

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
#    LPPFusion Focus Fusion commercial generator: a pulsed dense plasma focus
#    device with p-B11 fuel. Extremely compact (~3 tonnes, ~30 m³), no external
#    magnets, no cryogenics, no tritium, no manufactured targets. The plasma
#    self-confines via its own current-generated magnetic fields for ~10 ns.
#
#    Archetype-Fit: Low — DENSE_PLASMA_FOCUS is the library enum but was
#    calibrated with generic DPF defaults (5 Hz rep rate, DT-scale geometry).
#    Focus Fusion is radically smaller and faster (200 Hz, ~cm electrodes).
#
#    The pulsed-thermal inverse path takes q_eng and f_rep and back-solves
#    p_fus and e_driver_mj from the target P_net.
#
#    q_eng is not directly published. The YAML default of 3.0 is accepted.
#    Lerner claims ~60 kJ fusion yield per pulse with ~25 kJ net electricity,
#    but these are undemonstrated paper-concept numbers.
#
#    Published fusion power per pulse: ~60 kJ × 200 Hz = 12 MW (gross fusion).
#    Library back-solves from q_eng + P_native via the inverse balance.
#
#    Parameters NOT in spec (no canonical spec key or intentionally omitted):
#    - eta_th: library-owned per Rule 6. Design point has no thermal cycle
#      (eta_th=0); library carries per-archetype default.
#    - eta_pin: library-owned per Rule 6. YAML default = 0.20.
#    - eta_dec: library-owned per Rule 6. YAML default = 0.85.
#    - p_fus: never a spec key; library back-solves.
spec = dict(
    f_rep=200.0,      # Hz — lerner-2023-jfe-paper.md §Energy Capture: "about 200 times a second"
    mn=1.0,           # aneutronic p-B11; negligible neutron energy (< 1% from side reactions)
    p_trit=0.0,       # no tritium processing (p-B11 fuel)
    p_cryo=0.0,       # no cryogenics (no superconducting magnets, no cryoplant)
    p_coils=0.0,      # no external magnets — plasma is self-confined
    p_target=0.0,     # no manufactured targets — plasma forms from gas fill at electrode tip
    blanket_t=0.10,   # m — aneutronic p-B11 needs minimal shielding, not a breeding blanket
    ht_shield_t=0.05, # m — thin biological shield for secondary x-rays and minor neutrons
    structure_t=0.05, # m — minimal: device is ~3 tonnes total
    vessel_t=0.05,    # m — FF-2B vacuum chamber is ~10 cm radius; commercial comparable
)
P_native = 5.0  # MWe — lerner-2023-jfe-paper.md §Energy Capture; analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.DENSE_PLASMA_FOCUS, fuel=Fuel.PB11)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — transcribed from analysis.md Section 5b.
#    7 enabled overrides, reflecting the radical structural difference between
#    Focus Fusion's 5 MWe, ~3 tonne, aneutronic, direct-conversion device and
#    any conventional fusion plant architecture.
overrides = [
    # CAS21: Buildings — the entire device is ~3 tonnes, ~30 m³, fits in a 4m×4m room.
    {
        "account": "CAS21",
        "value": 0.05 * generic.costs.cas21,
        "enabled": True,
        "provenance": "derived",
        "source": "lerner-2023-jfe-paper.md §Energy Capture",
        "rationale": (
            "The entire device is ~3 tonnes, ~30 m³, fits in a 4m×4m room. No reactor "
            "building, no hot cell, no heavy-lift crane bay. At 5 MWe with aneutronic fuel "
            "and no tritium handling, the building requirement is a small industrial "
            "enclosure, not a nuclear-grade reactor building. 5% of the generic CAS21 "
            "is an order-of-magnitude estimate reflecting the ~100× reduction in "
            "building volume vs. a conventional fusion plant. No company-published "
            "building cost exists; this is analyst-derived."
        ),
        "cost_basis": "noak",
    },
    # CAS23: Turbine plant equipment — zero; no thermal cycle.
    {
        "account": "CAS23",
        "value": 0.0,
        "enabled": True,
        "provenance": "direct",
        "source": "lerner-2023-jfe-paper.md §Energy Capture",
        "rationale": (
            "No thermal cycle. All energy conversion is direct (ion beam decelerator + "
            "x-ray photoelectric). No steam turbine, no sCO2 cycle, no thermal BOP. "
            "CAS23 is structurally zero for this design point."
        ),
        "cost_basis": "noak",
    },
    # CAS24: Electric plant equipment — small industrial/distributed scale.
    {
        "account": "CAS24",
        "value": 0.10 * generic.costs.cas24,
        "enabled": True,
        "provenance": "derived",
        "source": "lerner-2023-jfe-paper.md §Cost and Transition",
        "rationale": (
            "At 5 MWe, the switchyard, transformers, and plant distribution are "
            "at small industrial/distributed generation scale, not utility scale. "
            "10% of generic CAS24 reflects the ~200× power reduction and "
            "correspondingly smaller electrical infrastructure. No company figure."
        ),
        "cost_basis": "noak",
    },
    # CAS26: Heat rejection — no thermal cycle; minimal electrode/electronics cooling.
    {
        "account": "CAS26",
        "value": 0.05 * generic.costs.cas26,
        "enabled": True,
        "provenance": "derived",
        "source": "lerner-2023-jfe-paper.md §Energy Capture — Cooling",
        "rationale": (
            "No thermal cycle, so no condenser or cooling tower for a turbine island. "
            "Cooling requirements limited to: electrode tip cooling (~10 kW/cm² at "
            "anode tip, using compressed helium), capacitor bank thermal management, "
            "and electronics cooling. Total heat rejection is a small fraction of "
            "the 5 MWe output. 5% of generic CAS26 is an order-of-magnitude "
            "estimate. No company figure."
        ),
        "cost_basis": "noak",
    },
    # CAS27: Special materials — no tritium, no FLiBe, no lithium blanket.
    {
        "account": "CAS27",
        "value": 0.10 * generic.costs.cas27,
        "enabled": True,
        "provenance": "derived",
        "source": "lppfusion-proton-boron-p11b-fuel-arrives/output.md",
        "rationale": (
            "No tritium inventory, no FLiBe, no lithium blanket fill. Initial "
            "inventory consists of beryllium electrodes (small mass, commercial "
            "Be is ~$800/kg) and initial decaborane fuel charge. Laboratory-"
            "scale isotopically pure decaborane costs $600/gram, but mass "
            "production is claimed to reduce this 'many hundred-fold.' At even "
            "$1/gram (optimistic mass production), 5 kg = $5,000. Total initial "
            "materials inventory is negligible vs. conventional fusion concepts. "
            "10% of generic CAS27 is conservative. No company-published figure."
        ),
        "cost_basis": "noak",
    },
    # CAS70: O&M — dominated by monthly electrode replacement, reduced staffing.
    {
        "account": "CAS70",
        "value": 0.25 * generic.costs.cas70,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "lerner-2023-jfe-paper.md §Cost and Transition; §Energy Capture"
        ),
        "rationale": (
            "O&M dominated by monthly electrode replacement (small beryllium "
            "components), capacitor bank maintenance, and staffing. No tritium "
            "handling, no remote maintenance, no large component changeouts. "
            "Device simplicity and small size should reduce staffing vs. conventional "
            "fusion plants. 25% of generic CAS70 reflects reduced complexity "
            "partially offset by high-frequency electrode replacement. No company "
            "O&M cost breakdown exists."
        ),
        "cost_basis": "noak",
    },
    # CAS80: Annualized fuel cost — decaborane at ~5 kg/year.
    # $30,000/year = 0.03 M$/year (analysis §5b derives from 5000 g × $6/g).
    {
        "account": "CAS80",
        "value": 0.03,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "lppfusion-proton-boron-p11b-fuel-arrives/output.md; "
            "lerner-2023-jfe-paper.md §Cost and Transition"
        ),
        "rationale": (
            "Fuel is decaborane at ~5 kg/year. Laboratory cost is ~$600/gram "
            "($3M/year) but requires mass production for commercial viability. "
            "Assuming 100-fold cost reduction to ~$6/gram: 5,000 g × $6/g = "
            "$30,000/year = 0.03 M$/year. Even at this level, fuel cost is "
            "negligible relative to capital amortization. Natural boron is "
            "abundant; isotopic enrichment to 99.9% B-11 is the cost driver."
        ),
        "cost_basis": "noak",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
