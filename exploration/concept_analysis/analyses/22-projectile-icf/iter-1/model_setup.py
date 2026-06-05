"""1costingfe model: Projectile ICF (First Light Fusion).

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
#    First Light projectile pilot plant (2022 pre-pivot ~150 MWe target).
#    Archetype-Fit: Low — HEAVY_ION (heavy-ion beam IFE) is the closest
#    available archetype but First Light's projectile approach is structurally
#    different: electromagnetic gun driver (not a heavy-ion accelerator), sub-Hz
#    rep rate (not 5-10 Hz), and liquid lithium curtain chamber (not FLiBe jets).
#
#    Data availability is Limited (Section 1). No published systems engineering
#    design, thermal-hydraulic layout, or energy balance exists for the 150 MWe
#    pilot plant. The only canonical spec key with a design-point-grounded value
#    differing from YAML defaults is f_rep.
#
#    Parameters NOT in spec (no canonical spec key or library-owned):
#    - target_gain (200-1000): no spec key; library uses q_eng for power balance
#    - driver_energy_MJ (~100 MJ stored): no spec key; library derives from q_eng
#    - projectile_speed (~60 km/s): no spec key
#    - eta_pin (~10-20% EM gun wall-plug): library-owned per Rule 6
#    - q_eng: YAML default 4.0; analysis estimates similar range from gain/efficiency
#      but no published Q_eng value. Accepting YAML default.
spec = dict(
    f_rep=0.033,  # prnewswire §Fusion Facts: "every 30 seconds" = 0.033 Hz
)
P_native = 150  # MWe — prnewswire §Next Steps: "~150 MW of electricity"

# 2. Model.
model = CostModel(concept=ConfinementConcept.HEAVY_ION, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — transcribed from analysis.md Section 5b.
#    4 enabled overrides. Expected band for Low archetype-fit: 6-12.
#    Discrepancy reflects severe data limitation — First Light published almost
#    no subsystem-level cost data before pivoting away from projectile ICF.
#    The 4 overrides represent the only accounts where company-grounded
#    quantitative evidence exists (Section 5b discrepancy note).
overrides = [
    # C220104: Primary pulsed driver — electromagnetic gun at $2/J stored
    {
        "account": "C220104",
        "value": 200.0,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "pmc-articles-pmc7658748.md §2. Model; "
            "ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md "
            "§Cost comparisons estimates"
        ),
        "rationale": (
            "Hawker (2020) published Machine 3 driver cost at $1.7/J stored. "
            "IP Group (2025) published FLARE demo at $2/J stored. "
            "Pilot design specifies 100 MJ stored energy (Machine 4 target). "
            "100 MJ x $2/J = $200M. Used $2/J as the more conservative (later, "
            "rep-rated) estimate. This is the electromagnetic gun + capacitor bank "
            "+ power supply cost. Library IFE driver default (heavy-ion accelerator "
            "at $12M/MW) is inapplicable to EM gun."
        ),
        "cost_basis": "noak",
    },
    # C220107: Pulsed-power capacitor bank — zeroed to avoid double-counting
    # with C220104 which already includes the capacitor bank as integral to
    # the electromagnetic launcher.
    {
        "account": "C220107",
        "value": 0.0,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md "
            "§Cost comparisons estimates"
        ),
        "rationale": (
            "The EM gun driver cost ($2/J for 100 MJ = $200M) already includes "
            "the capacitor bank as an integral part of the electromagnetic launcher "
            "system. Unlike laser IFE where the bank charges the laser and the laser "
            "is a separate cost item, here the bank IS the driver's energy store. "
            "Setting to zero avoids double-counting."
        ),
        "cost_basis": "noak",
    },
    # C220108: Target factory — annualized target manufacturing cost
    {
        "account": "C220108",
        "value": 5.6,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "pmc-articles-pmc7658748.md §2. Model; "
            "prnewswire-news-releases-first-light-achieves-world-first.md "
            "§A consumables business model"
        ),
        "rationale": (
            "Hawker (2020) establishes that target cost must be <10% of electricity "
            "revenue for economic viability. At 150 MWe, 85% CF, $50/MWh LCOE target: "
            "Annual revenue = 150,000 x 8760 x 0.85 x $50/1000 = $55.8M. "
            "10% ceiling = $5.58M/year annualized target factory + consumables cost. "
            "At 0.033 Hz x 8760 x 3600 x 0.85 = 0.99M shots/year. "
            "Max target cost = $5.58M / 0.99M = ~$5.6/target. "
            "Value represents annualized target factory cost in $M/year. "
            "Library default (high-rep-rate IFE target factory) is inapplicable at "
            "1M/year volume."
        ),
        "cost_basis": "noak",
    },
    # CAS27: Special materials — initial lithium inventory
    {
        "account": "CAS27",
        "value": 70.0,
        "enabled": True,
        "provenance": "direct",
        "source": (
            "ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md "
            "§Cost comparisons estimates"
        ),
        "rationale": (
            "IP Group press release directly states 'Natural lithium per reactor: $70M' "
            "in the cost comparison table. This represents the initial lithium inventory "
            "for the reactor chamber. Compares to '$143M-$451M for enriched lithium "
            "alternatives.' First Light uses natural lithium (no enrichment needed due "
            "to TBR 1.8 with natural Li). Library default for special materials does not "
            "account for the large liquid-metal inventory unique to this architecture."
        ),
        "cost_basis": "noak",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
