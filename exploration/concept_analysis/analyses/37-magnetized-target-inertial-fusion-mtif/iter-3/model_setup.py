"""1costingfe model: MTIF (Magneto-Inertial Fusion Technologies) (NearStar Fusion).

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
#    NearStar MTIF concept has extreme data opacity: the only published parameters
#    are rep_rate (1 Hz), projectile mass (50g), projectile velocity (10 km/s),
#    and fuel cycle (D-D). Critical gaps include target gain (Q), fusion yield,
#    driver efficiency, chamber geometry, and magnetic field strength. The analysis
#    (Section 5) documents that these few known values do NOT map to canonical
#    1costingFE spec keys for the MAG_TARGET archetype.
#
#    Known non-spec context (for reference, not model inputs):
#    - rep_rate_Hz: 1.0 (nearstar-mtif-technical-overview.md)
#    - projectile_mass_kg: 0.050 (nearstar-mtif-technical-overview.md)
#    - projectile_velocity_km_per_s: 10.0 (nearstar-mtif-technical-overview.md)
#    - driver_energy_MJ: >1.0 (stated, not spec key)
#    - fuel_cycle: D-D (captured in Fuel ENUM)
#    - fusion_yield_per_shot_MJ: [unknown] — BLOCKING gap
#    - target_gain_Q: [unknown] — BLOCKING gap
#
#    The MAG_TARGET archetype does not surface rep_rate, projectile parameters, or
#    driver_energy as spec kwargs. Without fusion yield, chamber geometry, or plasma
#    parameters, spec remains empty. The library will use pure MAG_TARGET YAML
#    defaults at the design-point scale.
spec = dict(
    # Empty — no canonical spec keys can be populated from available NearStar data.
    # Analysis Section 5 documents that the disclosed parameters (rep rate,
    # projectile mass/velocity) are not in the MAG_TARGET forward() signature.
)

P_native = 50  # MWe — from analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.MAG_TARGET, fuel=Fuel.DD)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Analysis Section 5b: "One enabled override. Expected band for Med archetype-fit
#    is 3–8. The count (1) is below the expected band but reflects the extreme opacity
#    of NearStar's public materials. Almost no quantitative cost, performance, or
#    engineering data has been disclosed beyond driver architecture basics."
#
#    PLAUSIBILITY CAVEAT: The 1 GWe LCOE output from this model (~56.6 $/MWh) should
#    NOT be interpreted as a credible estimate for NearStar's concept until target gain,
#    driver cost, and component lifetime are disclosed. This is a library-default
#    artifact that encodes MAG_TARGET archetype assumptions (low driver cost, high gain,
#    low O&M) not validated for a hypervelocity-projectile + D-D architecture with no
#    published yield, no experimental data, and undemonstrated railgun component lifetime
#    at 1 Hz. The model output is useful for identifying what WOULD need to be true for
#    LCOE competitiveness (e.g., target gain >X, railgun CAPEX <$Y, rail lifetime >Z
#    shots), but it is not a validated projection. Sensitivity analysis on target gain,
#    driver efficiency, or component lifetime would be needed to bound the LCOE range
#    under pessimistic vs. optimistic assumptions.
overrides = [

    {
        "account": "C220107",
        "value": 20.0,  # M$
        "enabled": True,
        "provenance": "derived",
        "source": "nearstar-mtif-technical-overview.md §Driver; Z-IFE and Navy railgun capacitor cost analogies",
        "rationale": (
            "Railgun driver energy >1 MJ kinetic per shot implies ~5–10 MJ electrical stored energy per shot "
            "(at 10–30% efficiency typical for railguns). At $4/J mid-range for industrial capacitors "
            "(between commodity $3/J and military-grade $5/J), a 5 MJ bank costs $20M. This is derived from "
            "railgun efficiency analogies and capacitor industry pricing, not from NearStar-published data. "
            "Enabled because: (1) the library's MAG_TARGET default is calibrated to Z-pinch pulsed-power "
            "systems (LTD or Marx banks, different cost structure than railgun capacitors), making railgun-specific "
            "analogy more credible for this concept; (2) NearStar's COTS claim (nearstar-mtif-technical-overview.md "
            "§Driver: 'commercial-off-the-shelf (COTS) technologies') supports mid-range capacitor pricing over "
            "high-end military specifications; (3) the $20M figure is conservative relative to NearStar's "
            "architectural claims — if COTS applies and capacitor cost approaches $1/J fusion target, cost could "
            "be $5M (factor of 4 lower), not higher. Uncertainty is ±factor of 2–3 but the $20M midpoint is "
            "better-grounded than a Z-pinch-based library default for a railgun application."
        ),
        "cost_basis": "noak",
    },

    {
        "account": "CAS21",
        "value": lambda: 0.70 * generic.costs.cas21,
        "enabled": False,
        "blocked_by": "1cFE/fusion-tea#2",
        "provenance": "derived",
        "source": "nearstar-energy-capture-research.md §Key finding",
        "rationale": (
            "NearStar markets a coal plant retrofit strategy: 'retrofit the heat source in traditional "
            "hydrocarbon (e.g., coal) power plants with a fusion power core to leverage existing turbines "
            "and power grid infrastructure.' If viable, this saves turbine building, switchyard, and auxiliary "
            "building capital costs — estimated 20–40% of greenfield CAS21. The 0.70 factor (30% reduction) "
            "is a midpoint estimate. Disabled because no actual retrofit case study, cost comparison, or site "
            "assessment is published. Savings depend on: coal plant remaining service life, state of turbine "
            "hall structural integrity, compatibility of pulsed fusion thermal output with existing steam cycle, "
            "and costs of modifications (new heat exchangers, control systems, safety upgrades)."
        ),
        "cost_basis": "noak",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
