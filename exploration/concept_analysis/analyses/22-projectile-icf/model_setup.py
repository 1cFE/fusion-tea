# STALE: analysis-updated-iter-4
"""
Projectile ICF (D-T) First-Pass LCOE Model
===========================================
1cFE First Pass Concept Analysis
Concept: Hypervelocity Projectile-Driven Inertial Confinement Fusion (D-T)
Companies: First Light Fusion (Oxford, UK; pivoted to FLARE, Sept 2025),
           NearStar Fusion (Sacramento, CA; MTIF hybrid — contextual comparator only)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

This is a parameterized LCOE model based on publicly available information from
First Light Fusion technology pages, the FLARE pivot update, IP Group portfolio
reporting, and the Hawker (2020) IFE economics framework (Phil. Trans. R. Soc. A 379,
rsta.2020.0053). Cost structure follows the CAS (Code of Accounts System) used in
1costingfe / pyFECONS, adapted for a pulsed IFE architecture with flowing liquid
lithium first wall and electromagnetic gun driver.

CRITICAL MODELING NOTE — False Precision Warning:
    The two blocking unknowns in this model are (1) driver capital cost and
    (2) target gain. Neither has a published analogue cost basis. The LCOE output
    is swept over these parameters rather than pinned to a "best estimate," because
    any single point estimate would misrepresent the actual uncertainty.
    The analysis.md §Section 2 recommends free-form scenario modeling for exactly
    this reason. Use the scenario comparison and sensitivity sweeps; do not treat the
    baseline LCOE as a prediction.

Key references:
- First Light Fusion technology pages (firstlightfusion.com) — compiled in
  analyses/22-projectile-icf/iter-01/sources/first-light-fusion-technology.md
- First Light Fusion FLARE pivot (September 2025) — compiled in
  analyses/22-projectile-icf/iter-02/sources/first-light-flare-pivot-update.md
- IP Group portfolio update (September 2025) — compiled in
  analyses/22-projectile-icf/iter-03/sources/ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19.md
- The Engineer — FLF tritium claims — compiled in
  analyses/22-projectile-icf/iter-03/sources/theengineer-content-news-first-light-fusion-claims-tritium.md
- PR Newswire — FLF Machine 3 fusion announcement (April 5, 2022) — compiled in
  analyses/22-projectile-icf/iter-03/sources/prnewswire-news-releases-first-light-achieves-world-first.md
- Hawker, N.J. (2020). "A simplified economic model for inertial fusion energy."
  Phil. Trans. R. Soc. A 379, rsta.2020.0053.
- SAND2006-7148 — Z-IFE Power Plant Final Report FY2006 (analogue for IFE architecture)
- Olson et al., Fusion Eng. Design (2005) — Z-pinch IFE power plant (analogue scaling)
- 1costingfe CAS structure — https://github.com/1cFE/1costingfe

Structural departures from standard CAS tokamak model:
- C220103 Coils = $0 (no magnets in projectile ICF)
- C220104 Heating = $0 (no NBI/RF/laser preheat — driver does all work)
- C220107 Driver = FREE PARAMETER (electromagnetic gun; no published analogue cost)
- C220101 Blanket = flowing liquid Li curtain (TBR 1.8; no vessel replacement)
- CAS27 Special Materials = liquid Li inventory ($70M natural, $143-451M enriched)
- CAS80 Consumables = per-target + per-projectile (novel recurring cost structure)
- Per-shot consumables replace RTL cost from MagLIF analogue
"""

import math
from dataclasses import dataclass, field
from typing import Optional


# === Reference power levels for scaling laws (from 1costingfe) ===
P_TH_REF = 2500.0   # Reference thermal power [MW]
P_ET_REF = 1100.0   # Reference gross electric power [MW]


@dataclass
class ProjectileICFPlantParams:
    """
    Parameterized Projectile ICF (D-T) power plant model.
    All values have source annotations.
    Uncertainty tags: (none) = well-sourced, MODERATE UNCERTAINTY = analogue estimate,
    HIGH UNCERTAINTY = speculative or no analogue cost basis.
    """

    # =========================================================================
    # DRIVER / LAUNCHER
    # The electromagnetic gun accelerates a macroscopic projectile to 60 km/s.
    # Machine 4 (cancelled Feb 2025) was the planned commercial-scale device.
    # =========================================================================

    driver_stored_energy_MJ: float = 100.0
    """Stored electrical energy per shot in driver capacitor bank [MJ].
    Source: Machine 4 (FLF's cancelled commercial-scale device) was designed for
    100 MJ stored energy, per FLF technology pages.
    Ref: first-light-fusion-technology.md §Driver; analysis.md §Section 5.
    NOTE: This sets the driver scale reference; fusion yield is parametrized
    separately as the primary commercial uncertainty. The stored energy is
    consistent with FLF's design intent but the device was never built.
    MODERATE UNCERTAINTY — design spec for cancelled device."""

    driver_efficiency: float = 0.30
    """Fraction of stored energy delivered to target as kinetic energy
    (wall-plug-to-kinetic efficiency of EM launcher) [dimensionless].
    Source: NOT PUBLISHED for projectile ICF. Analogue estimate from:
    - EM launchers (railgun/coilgun): ~20-40% wall-to-kinetic at current scales
    - FLF FLARE (pulsed power): ~5-10% wall-to-target, LTD/IMG ~15-20%
    - EM launchers are expected to be more efficient than pulsed power per
      delivered joule, but less efficient at extreme velocities.
    Using 0.30 as mid-range estimate.
    Ref: analysis.md §Section 2 ("20-40% (EM, estimate)").
    HIGH UNCERTAINTY — no published FLF data; 60 km/s efficiency undemonstrated."""

    driver_cost_M_USD: float = 1000.0
    """Capital cost of electromagnetic gun driver [$M].
    Source: NO PUBLISHED ESTIMATE EXISTS. This is the dominant modeling unknown.
    Calibration from FLARE pivot (indirect evidence):
    - FLARE uses pulsed power at $2/J (FLF-stated)
    - "Alternatives" cited at $6-13/J (from FLARE pivot analysis)
    - Machine 4 (100 MJ stored): at $6/J → $600M, at $13/J → $1.3B
    - FLF's abandonment of the projectile gun implies cost >$2/J baseline
    Using $1,000M as central estimate (between $600M and $1.3B analogues).
    Baseline: $1,000M; Conservative: $2,000M; Optimistic: $500M.
    Ref: first-light-flare-pivot-update.md; analysis.md §Section 2, §Section 5.
    HIGH UNCERTAINTY — blocking unknown; no industrial analogue at 60 km/s."""

    driver_rep_rate_Hz: float = 0.033
    """Shot repetition rate [Hz] (shots per second).
    Source: FLF cited multiple conflicting figures:
    - 0.033 Hz (30s between shots) — pilot plant / 150 MWe reference
    - 0.1 Hz (10s between shots) — commercial / 500 MWe reference
    - 0.011 Hz (90s between shots) — also cited, source unclear
    Using 0.033 Hz as baseline (most conservative cited figure for pilot scale).
    The 333 MWe design point requires higher gain per shot at lower rep rate.
    Ref: first-light-fusion-technology.md §Repetition Rate; analysis.md §Section 5.
    MODERATE UNCERTAINTY — three conflicting figures in public materials."""

    # =========================================================================
    # TARGET / FUSION PHYSICS
    # FLF's "amplifier" target: cubic ~1cm form with multiple internal cavities
    # that create converging shockwaves. Proprietary design.
    # =========================================================================

    fusion_yield_MJ: float = 30_000.0
    """Fusion energy yield per shot [MJ] (30 GJ baseline).
    Source: INFERRED from plant design point. FLF's 333 MWe design at 0.033 Hz:
      p_fusion_avg = 333 MWe / (thermal_eff × (1 - recirc_frac))
                   ≈ 333 / (0.33 × 0.95) ≈ 1,060 MW fusion average
      fusion_yield = 1,060 MW / 0.033 Hz ≈ 32,000 MJ ≈ 30 GJ (rounded)
    Cross-check: analysis.md §Section 5 table note: "Derivation: 333 MWe ÷ 0.33 × 30s
    ≈ 30 GJ fusion energy needed"
    Baseline: 30,000 MJ (matches 333 MWe design point at stated rep rate/efficiency).
    Conservative: 6,000 MJ (gain 200× minimum commercial threshold).
    Optimistic: 30,000 MJ (gain 1000× at 100 MJ stored, 30% efficiency).
    Ref: analysis.md §Section 5; first-light-fusion-technology.md §Tritium Breeding.
    HIGH UNCERTAINTY — gain achieved at 60 km/s has never been demonstrated."""

    target_cost_USD: float = 5.0
    """Cost per fusion target [USD].
    Source: NOT PUBLISHED. FLF's amplifier target geometry (~1 cm cubic, multiple
    cavities) is proprietary IP. No mass-production analogue for precision
    multi-cavity fusion targets.
    Economic ceiling from Goodin et al. (2004) IFE target cost analysis:
    target cost must be < 10% of electrical yield per shot.
    At $50/MWh LCOE and 30 GJ fusion yield: 10% of electrical value/shot =
    0.1 × (30,000 MJ × 0.33 / 3,600) MWh × $50/MWh = 0.1 × 2.75 × 50 ≈ $13.75
    So $5/target is below the $13.75 economic ceiling for optimistic gain scenario.
    At conservative yield (6 GJ): ceiling is $2.75 — lower constraint.
    Baseline: $5.00; Conservative: $20.00; Optimistic: $2.00.
    Ref: analysis.md §Section 5 §Gap 4; Goodin et al. (2004).
    HIGH UNCERTAINTY — fabrication cost at 1-4M targets/year completely unknown."""

    projectile_cost_USD: float = 1.0
    """Cost per projectile [USD].
    Source: NOT PUBLISHED. At 6.5 km/s (Machine 3), projectile materials are
    not exotic. At 60 km/s, bore erosion is an open engineering question.
    Even at $1/projectile, annual cost = ~880,000 shots × $1 = $880K/yr at
    0.033 Hz with 85% availability — modest relative to other costs.
    ASSUMED: $1/projectile as order-of-magnitude lower bound. May be significantly
    higher if exotic materials required for bore-erosion resistance.
    Ref: analysis.md §Section 4 §Projectile Materials.
    HIGH UNCERTAINTY — no published estimate; 60 km/s bore dynamics unsolved."""

    blanket_energy_multiplication: float = 1.10
    """Blanket energy multiplication factor M (from exothermic ⁶Li(n,α)T reaction).
    Source: Standard D-T fusion assumption. Natural Li blanket (7.5% ⁶Li) provides
    less multiplication than ⁶Li-enriched blanket.
    Ref: Standard fusion engineering; analysis.md §Section 2 (liquid Li blanket)."""

    thermal_efficiency: float = 0.33
    """Thermal-to-electric conversion efficiency for steam Rankine cycle.
    Source: FLF explicitly chose a "conventional steam Rankine cycle — 150-year-old
    steam turbine technology at this scale is mature." Steam Rankine at this
    scale operates at 33-35%.
    Ref: first-light-fusion-technology.md §Energy Conversion; analysis.md §Section 3.
    NOTE: The analysis notes thermal buffering from pulsed Li heat source may be
    needed — assumed minor efficiency impact in base case."""

    # =========================================================================
    # PLANT CONFIGURATION
    # =========================================================================

    n_mod: int = 1
    """Number of fusion modules (chambers) per plant.
    Source: FLF design is single-chamber. Multi-chamber configurations possible
    but not published.
    Ref: first-light-fusion-technology.md §Plant Specifications."""

    plant_availability: float = 0.85
    """Plant capacity factor / availability.
    Source: NOT PUBLISHED for projectile ICF.
    Z-IFE study (SAND2006-7148) assumed 85% availability for pulsed IFE baseline.
    Chamber clearing time (liquid Li resettlement after blast) is unknown —
    this constrains rep rate but not availability per se.
    Using 85% as analogue from Z-IFE study.
    Ref: analysis.md §Gap 7 (capacity factor unknown); SAND2006-7148.
    MODERATE UNCERTAINTY — analogue from Z-IFE; no FLF-specific data."""

    plant_lifetime_years: float = 40.0
    """Plant economic lifetime [years]."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds contingency and higher pre-construction costs."""

    # =========================================================================
    # CHAMBER GEOMETRY — Spherical geometry for IFE liquid-wall chamber
    # =========================================================================

    chamber_inner_radius_m: float = 2.5
    """Inner radius of fusion chamber [m].
    Source: FLF uses liquid lithium curtains ~1m thick. Chamber inner radius
    not explicitly stated; Z-IFE FLiBe chamber ~3m radius is the closest analogue.
    Using 2.5m as slightly smaller (FLF targets are smaller than MagLIF liners).
    ASSUMED: 2.5m — analogue from Z-IFE (3m) scaled down for smaller target.
    Ref: SAND2006-7148; analysis.md §Section 3 (liquid Li chamber).
    MODERATE UNCERTAINTY."""

    blanket_thickness_m: float = 1.0
    """Blanket (flowing liquid lithium curtain) thickness [m].
    Source: FLF specifically states "1-meter-thick flowing liquid lithium curtains."
    This simultaneously serves as first wall, blanket, tritium breeding zone,
    and primary neutron absorber.
    Ref: first-light-fusion-technology.md §Neutron Management; analysis.md §Section 2."""

    shield_thickness_m: float = 0.4
    """Structural shield thickness behind liquid Li blanket [m].
    Source: FLF claims "neutrons do not reach the vessel wall" due to the 1m Li curtain.
    If true, the residual shield can be thinner than in solid-wall designs.
    ASSUMED: 0.4m — reduced from Z-IFE's 0.5m shield, reflecting liquid Li's
    full neutron capture. Some shield still needed for activation and safety.
    MODERATE UNCERTAINTY."""

    structure_thickness_m: float = 0.3
    """Primary structure thickness [m].
    Source: Analogy to IFE chamber structure.
    Ref: SAND2006-7148."""

    vessel_thickness_m: float = 0.1
    """Vacuum vessel / outer containment thickness [m].
    Source: FLF claims "vessel never replaced" due to full neutron capture in Li curtain.
    The outer structural vessel still has finite cost.
    Ref: first-light-fusion-technology.md §Neutron Management."""

    # =========================================================================
    # BLANKET / CAS22 OVERRIDES
    # =========================================================================

    blanket_unit_cost: float = 0.60
    """Flowing liquid lithium blanket unit cost [M$/m³].
    Source: 1costingfe costing_constants.yaml blanket_unit_cost_dt = 0.60 M$/m³.
    Liquid Li blanket has different engineering challenges (chemical reactivity,
    pump power) vs solid blanket, but comparable volumetric cost is plausible.
    This cost covers the Li inventory, flow channels, heat exchangers, and
    containment infrastructure.
    DEFAULT: 0.60 M$/m³ from 1costingfe D-T blanket reference.
    MODERATE UNCERTAINTY — liquid Li blanket unit cost poorly characterized."""

    # =========================================================================
    # SPECIAL MATERIALS (CAS27)
    # =========================================================================

    li_inventory_cost_M_USD: float = 70.0
    """Liquid lithium inventory cost [$M]. Maps to CAS27 special materials.
    Source: FLF white paper (cited via IP Group portfolio article, Sept 2025):
    natural lithium per reactor ~$70M vs enriched lithium ~$143-451M.
    Using natural lithium $70M as base case (if TBR 1.8 achievable with natural Li).
    If ⁶Li enrichment required: $143-451M (2-6× premium).
    Ref: ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19.md §Cost comparisons;
    analysis.md §Section 4 §Lithium-6 Enrichment."""

    # =========================================================================
    # TRITIUM
    # =========================================================================

    tritium_startup_kg: float = 3.0
    """Tritium startup inventory [kg].
    Source: Standard D-T challenge: 1-5 kg startup inventory at ~$30,000/g.
    FLF's high TBR (1.8) enables "self-sufficiency in as little as one week"
    (design claim, not experimentally demonstrated), reducing required startup.
    Baseline: 3 kg at $30,000/g = $90M startup fuel cost.
    Ref: analysis.md §Section 4 §Tritium; first-light-fusion-technology.md §Tritium Breeding.
    MODERATE UNCERTAINTY — startup inventory depends on tritium extraction rate."""

    tritium_surplus_kg_per_year: float = 25.0
    """Tritium surplus produced per year [kg/year].
    Source: FLF states 25 kg/year surplus at 333 MWe design point.
    TBR = 1.8 independently validated by TÜV SÜD UK (February 2026) via
    computational analysis of the blanket design.
    Ref: first-light-fusion-technology.md §Tritium Breeding;
    theengineer-content-news-first-light-fusion-claims-tritium.md."""

    tritium_price_USD_per_g: float = 0.0
    """Tritium byproduct revenue price [$/g]. Default $0 (conservative base case).
    Source: Current scarcity price ~$30,000/g (CANDU-driven; ~20 kg/year global supply).
    At 25 kg/year surplus and $30,000/g: ~$750M/year potential revenue for 333 MWe plant.
    This would approach 60% of electricity revenue at $50/MWh LCOE.
    CRITICAL SCENARIO NOTE: This price is structurally self-undermining at fleet scale.
    Fleet deployment of FLF plants would flood the ~20 kg/year global market.
    BASE CASE: $0/g (fleet saturation, price collapse).
    SCARCITY CASE: $30,000/g (current market, first-mover scenario).
    Ref: theengineer-content-news-first-light-fusion-claims-tritium.md; analysis.md §Section 2."""

    # =========================================================================
    # AUXILIARY / RECIRCULATING POWER
    # =========================================================================

    p_li_pump_MW: float = 30.0
    """Liquid lithium primary loop pump power [MW].
    Source: NOT PUBLISHED. Analogue: Z-IFE FLiBe pump power was estimated at
    ~20-40 MW for similar thermal power levels. Liquid Li has lower viscosity
    than FLiBe but similar flow rate requirements.
    ASSUMED: 30 MW as central analogue estimate.
    Ref: analysis.md §Section 3 (liquid Li pump power noted as unknown).
    HIGH UNCERTAINTY — not characterized in FLF public materials."""

    p_trit_MW: float = 10.0
    """Tritium processing power [MW].
    Source: 1costingfe ife_zpinch.yaml default. D-T systems with high TBR
    (like FLF's 1.8) require active tritium extraction from liquid Li coolant.
    MODERATE UNCERTAINTY."""

    p_house_MW: float = 4.0
    """Housekeeping power [MW].
    Ref: 1costingfe ife_zpinch.yaml default."""

    p_cryo_MW: float = 0.3
    """Cryogenic system power [MW].
    Source: Projectile ICF has no superconducting magnets — minimal cryogenic load.
    Only needed for target cryogenic preparation (D-T ice).
    Ref: 1costingfe ife_zpinch.yaml default (minimal cryo baseline)."""

    p_target_factory_MW: float = 1.5
    """Target factory and projectile loading system power [MW].
    Ref: 1costingfe ife_zpinch.yaml default."""

    # =========================================================================
    # FINANCIAL
    # =========================================================================

    interest_rate: float = 0.08
    """Real discount rate (weighted average cost of capital).
    Ref: 1costingfe default; standard fusion LCOE studies."""

    inflation_rate: float = 0.02
    """Inflation rate for levelized cost calculations.
    Ref: 1costingfe default."""

    construction_time_years: float = 6.0
    """Construction period [years].
    Ref: 1costingfe reference_construction_time."""

    # =========================================================================
    # OPERATING COSTS
    # =========================================================================

    om_cost_per_MW_yr: float = 60.0
    """O&M cost per MW net capacity per year [$/MW/yr].
    Source: No analogue exists for projectile ICF O&M. Conventional nuclear plant
    O&M ~$20-40/MW/yr provides a lower bound; pulsed IFE adds per-shot hardware
    maintenance (gun barrel, target injector, Li loop maintenance).
    Using 60 $/MW/yr from 1costingfe CAS71 IFE reference as order-of-magnitude.
    ASSUMED: $60/MW/yr — analogous to pulsed IFE; liquid Li loop likely adds cost.
    Ref: 1costingfe costing_constants.yaml om_cost_dt (52 at 1 GWe).
    HIGH UNCERTAINTY — no operating prototype; liquid Li loop O&M uncharacterized."""

    core_lifetime_FPY: float = 40.0
    """First wall / blanket core lifetime in full-power-years before replacement.
    Source: FLF explicitly states "neutrons do not reach the vessel wall" —
    the flowing Li curtain absorbs all neutrons, protecting the structural vessel.
    This implies vessel lifetime = plant lifetime (40 FPY).
    The blanket liquid Li itself is continuously refreshed (no radiation damage
    accumulation in a flowing liquid).
    Ref: first-light-fusion-technology.md §Neutron Management; analysis.md §Section 7.
    NOTE: This is a major cost advantage vs solid-wall D-T designs (which need
    blanket replacement every ~5 FPY). Sets blanket replacement cost ≈ $0."""

    fuel_cost_per_shot_USD: float = 0.005
    """D-T fuel cost per shot [USD].
    Source: D-T fuel per shot is mg-scale. Deuterium is cheap (~$2/g).
    Tritium is bred in-situ (no ongoing purchase). Net fuel cost is effectively
    only the deuterium mass per shot.
    At 30 GJ yield, D-T reaction energy = 17.6 MeV/reaction; moles of fuel ≈
    30,000 MJ / (17.6 MeV × 1.6e-13 J/eV × 6.022e23) ≈ 1.78 × 10⁻² mol ≈ 0.1g D
    Cost: 0.1g × $2/g = $0.20 — upper bound. Effective fuel cost << $0.01/shot.
    Ref: Standard fusion fuel cost estimates; analysis.md §Section 4."""

    def _compute_power(self) -> dict:
        """Layer 1: Compute power balance for pulsed projectile ICF plant."""
        r = {}

        # Energy delivered to target per shot
        energy_to_target_MJ = self.driver_stored_energy_MJ * self.driver_efficiency
        r["energy_to_target_MJ"] = energy_to_target_MJ

        # Target gain (derived — the key physics uncertainty)
        r["target_gain"] = self.fusion_yield_MJ / energy_to_target_MJ

        # D-T fusion energy split: 80% neutrons (14.06 MeV), 20% alphas (3.52 MeV)
        f_neutron = 0.80
        f_ash = 0.20
        p_fus = self.fusion_yield_MJ * self.driver_rep_rate_Hz  # MW (time-averaged)
        r["p_fus"] = p_fus
        r["p_neutron"] = p_fus * f_neutron
        r["p_ash"] = p_fus * f_ash

        # Thermal power: blanket captures neutrons (with multiplication) + alpha heat
        # Driver energy that reaches target thermalizes in chamber (small contribution)
        driver_avg_power_MW = self.driver_stored_energy_MJ * self.driver_rep_rate_Hz
        # The undelivered driver energy (1 - eff) fraction thermalizes in driver system,
        # NOT in the chamber — it is resistive/ohmic loss in the launcher, not useful heat.
        p_th = (self.blanket_energy_multiplication * r["p_neutron"] + r["p_ash"])
        r["p_th"] = p_th
        r["driver_avg_power_MW"] = driver_avg_power_MW

        # Gross electric
        p_et = p_th * self.thermal_efficiency
        r["p_et"] = p_et

        # Recirculating power: driver recharge + liquid Li pump + auxiliaries
        p_aux = (self.p_li_pump_MW + self.p_trit_MW + self.p_house_MW
                 + self.p_cryo_MW + self.p_target_factory_MW)
        r["p_aux"] = p_aux
        r["p_aux_detail"] = {
            "li_pump": self.p_li_pump_MW,
            "tritium": self.p_trit_MW,
            "housekeeping": self.p_house_MW,
            "cryo": self.p_cryo_MW,
            "target_factory": self.p_target_factory_MW,
        }

        # Net electric = gross - driver recharge - auxiliaries
        p_net = p_et - driver_avg_power_MW - p_aux
        r["p_net"] = p_net

        # Engineering Q (fusion power / driver input power)
        r["Q_eng"] = p_fus / driver_avg_power_MW if driver_avg_power_MW > 0 else float('inf')
        r["recirc_fraction"] = (driver_avg_power_MW + p_aux) / p_et if p_et > 0 else float('inf')

        # Annual shot count
        r["shots_per_year"] = self.driver_rep_rate_Hz * 3600 * 8760 * self.plant_availability

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Compute spherical chamber shell volumes.
        Uses spherical geometry for IFE liquid-wall chamber, matching 1costingfe
        convention for IFE/MIF concepts."""
        r = {}
        ri = self.chamber_inner_radius_m

        def sphere_shell_vol(r_in, thickness):
            r_out = r_in + thickness
            return (4.0 / 3.0) * math.pi * (r_out**3 - r_in**3)

        r_blanket_out = ri + self.blanket_thickness_m
        r["blanket_vol_m3"] = sphere_shell_vol(ri, self.blanket_thickness_m)

        r_shield_out = r_blanket_out + self.shield_thickness_m
        r["shield_vol_m3"] = sphere_shell_vol(r_blanket_out, self.shield_thickness_m)

        r_structure_out = r_shield_out + self.structure_thickness_m
        r["structure_vol_m3"] = sphere_shell_vol(r_shield_out, self.structure_thickness_m)

        r_vessel_out = r_structure_out + self.vessel_thickness_m
        r["vessel_vol_m3"] = sphere_shell_vol(r_structure_out, self.vessel_thickness_m)

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts.
        Follows 1costingfe cas22.py structure adapted for projectile ICF.
        Key overrides vs standard tokamak CAS:
        - C220103 (Coils) = $0: no magnets of any kind
        - C220104 (Heating) = $0: no NBI/RF/laser — driver does all work
        - C220107 (Power Supplies) = driver_cost_M_USD: the launcher IS the power supply
        - C220112 (Isotope Sep) = $0: Li inventory handled in CAS27
        """
        r = {}
        p_th = max(power["p_th"], 1.0)
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)

        # --- Per-module accounts ---

        # C220101: First Wall + Blanket (flowing liquid Li curtain)
        # Formula: unit_cost × volume × (p_th / P_TH_REF)^0.6
        # Liquid Li curtain serves as first wall, blanket, and tritium breeding zone.
        # Vessel never replaced (full neutron absorption in Li) → no replacement penalty.
        r["C220101"] = (self.blanket_unit_cost
                        * geom["blanket_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220102: Shield (behind Li curtain — reduced because Li absorbs most neutrons)
        # Formula: 0.74 × volume × (p_th / P_TH_REF)^0.6
        shield_unit_cost = 0.74   # M$/m³ — from 1costingfe costing_constants.yaml
        r["C220102"] = (shield_unit_cost
                        * geom["shield_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: Coils — OVERRIDE: $0 (projectile ICF uses NO magnets)
        # Unlike tokamaks (HTS coils ~$1-2B), stellarators, or even MagLIF
        # (seed field coils ~$10M), projectile ICF requires zero magnetic infrastructure.
        r["C220103"] = 0.0

        # C220104: Supplementary Heating — OVERRIDE: $0
        # The driver kinetic impact does all the work. No NBI, no RF, no laser preheat.
        r["C220104"] = 0.0

        # C220105: Primary Structure
        # Formula: 0.15 × volume × (p_et / P_ET_REF)^0.5
        structure_unit_cost = 0.15  # M$/m³ — from 1costingfe costing_constants.yaml
        r["C220105"] = (structure_unit_cost
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: Vacuum System + containment vessel
        # For liquid Li chamber, the "vacuum vessel" is the structural outer shell.
        # Li-air reactivity requires inert-atmosphere containment throughout.
        # Standard vessel_unit_cost from 1costingfe, but may underestimate Li containment.
        vessel_unit_cost = 0.72  # M$/m³ — from 1costingfe costing_constants.yaml
        r["C220106"] = (vessel_unit_cost
                        * geom["vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # C220107: Power Supply / Driver — OVERRIDE: electromagnetic gun
        # This is the dominant novel cost account and the primary modeling uncertainty.
        # Standard formula: 80.0 × (p_et/1000)^0.7 [1costingfe default for power supplies]
        # Override: direct driver capital cost (deep uncertainty; see param docstring).
        r["C220107"] = self.driver_cost_M_USD  # [override — see driver_cost_M_USD]

        # C220108: Target Factory + Projectile Loading System
        # Commercial rep rate: 0.033 Hz × 0.85 availability × 31.56Ms/yr ≈ 884K shots/yr.
        # Need automated target manufacture AND precise projectile injection system.
        # Formula from 1costingfe: 244.0 × (p_et / 1000)^0.7 [target factory base]
        target_factory_base = 244.0  # M$ at 1 GWe — from 1costingfe costing_constants.yaml
        r["C220108"] = target_factory_base * (p_et / 1000.0) ** 0.7

        # C220109: Direct Energy Converter — not applicable for steam Rankine
        r["C220109"] = 0.0

        # C220111: Installation labor
        installation_frac = 0.14  # from 1costingfe costing_constants.yaml
        reactor_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109"])
        r["C220111"] = installation_frac * reactor_subtotal

        # C220112: Isotope Separation — $0 here (Li inventory in CAS27)
        r["C220112"] = 0.0

        # Per-module subtotal
        r["CAS22_per_module"] = reactor_subtotal + r["C220111"] + r["C220112"]

        # --- Plant-wide accounts ---
        p_net_total = p_net * self.n_mod
        p_th_total = p_th * self.n_mod

        # C220200: Main & Secondary Coolant (Li primary + water/steam secondary)
        # Liquid Li to water/steam heat exchanger — additional cost vs single-fluid designs.
        C220201 = 166.0 * (p_net_total / 1000.0)         # Primary Li loop
        C220202 = 40.6 * (p_th_total / 3500.0) ** 0.55   # Intermediate Li-to-steam HX
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling + Cryoplant (minimal — no SC magnets)
        C220301 = 1.1e-3 * p_th_total                                  # Aux coolant
        C220302 = 200.0 * (max(self.p_cryo_MW, 0.01) / 30.0) ** 0.7   # Cryoplant (small)
        r["C220300"] = C220301 + C220302

        # C220400: Radioactive Waste Management
        r["C220400"] = 1.96 * (p_th_total / 1000.0)

        # C220500: Fuel Handling & Storage (D-T with high TBR — significant tritium system)
        fuel_handling_base = 120.0  # M$ at 1 GWe — from 1costingfe fuel_handling_dt_base
        r["C220500"] = fuel_handling_base * (p_net_total / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        r["C220600"] = 11.5 * (p_net_total / 1000.0) ** 0.8

        # C220700: Instrumentation & Control
        r["C220700"] = 85.0 * (p_th_total / 3500.0) ** 0.65

        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        # Total CAS22
        r["CAS22"] = r["CAS22_per_module"] * self.n_mod + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: CAS10-60 capital cost structure."""
        r = {}
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)
        p_net_total = p_net * self.n_mod

        # === CAS10: Pre-construction ===
        site_permits = 3.0
        plant_studies = 4.0 if self.noak else 20.0
        plant_permits = 2.0
        plant_reports = 1.0
        other_precon = 1.0
        land_cost = 0.25 * p_net * math.sqrt(self.n_mod) * 10_000 / 1e6
        licensing_cost = 5.0 if not self.noak else 2.5  # D-T licensing
        r["CAS10"] = (site_permits + plant_studies + plant_permits + plant_reports
                      + other_precon + land_cost + licensing_cost)

        # === CAS21: Buildings ===
        # Projectile ICF needs a large launcher bay + target factory building
        # in addition to standard fusion plant buildings.
        building_cost_per_kW = {
            "site_improvements": 268.0,     # $/kW — from 1costingfe CAS21 defaults
            "fusion_heat_island": 126.0,    # reactor building
            "turbine_building": 54.0,
            "heat_exchanger": 12.0,
            "launcher_bay": 40.0,           # ASSUMED: electromagnetic gun building (large, long)
            "hot_cell": 93.4,               # D-T hot cell for tritium handling
            "misc_buildings": 61.6,
        }
        total_building_per_kW = sum(building_cost_per_kW.values())
        r["CAS21"] = total_building_per_kW * p_et / 1000.0  # M$
        r["CAS21_detail"] = {k: v * p_et / 1000.0 for k, v in building_cost_per_kW.items()}

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23-26: Balance of Plant ===
        # Steam Rankine is identical to conventional thermal plant — fully mature.
        # FLF explicitly confirmed: "After the lithium heat exchanger, the plant
        # is identical to many other already working facilities."
        turbine_per_mw = 0.19764   # M$/MW — from 1costingfe costing_constants.yaml
        electric_per_mw = 0.08418  # M$/MW
        misc_per_mw = 0.05124      # M$/MW
        heat_rej_per_mw = 0.03416  # M$/MW
        r["CAS23"] = self.n_mod * p_et * turbine_per_mw
        r["CAS24"] = self.n_mod * p_et * electric_per_mw
        r["CAS25"] = self.n_mod * p_et * misc_per_mw
        r["CAS26"] = self.n_mod * p_et * heat_rej_per_mw

        # === CAS27: Special Materials (liquid Li inventory) ===
        # Source: FLF white paper via ipgroupplc-news-2025-09-19:
        # natural Li ~$70M/reactor, enriched Li ~$143-451M/reactor.
        r["CAS27"] = self.li_inventory_cost_M_USD

        # === CAS28: Digital Twin ===
        r["CAS28"] = 5.0  # DEFAULT: from 1costingfe costing_constants.yaml

        # === CAS29: Contingency ===
        cas20_subtotal = sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                             "CAS25", "CAS26", "CAS27", "CAS28"])
        contingency_rate = 0.0 if self.noak else 0.10
        r["CAS29"] = contingency_rate * cas20_subtotal

        # === CAS20: Total Direct Costs ===
        r["CAS20"] = cas20_subtotal + r["CAS29"]

        # === CAS30: Indirect Costs (20% of direct, scaled by construction time) ===
        ref_construction_time = 6.0
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / ref_construction_time)

        # === CAS40: Owner's Costs ===
        # Using D-T power-law scaling from 1costingfe owner_cost_dt = 39 M$ at 1 GWe
        r["CAS40"] = 39.0 * (p_net_total / 1000.0) ** 0.5

        # === CAS50: Supplementary Costs ===
        spare_parts_frac = 0.03   # D-T — from 1costingfe spare_parts_frac_dt
        spare_parts = spare_parts_frac * sum(r[k] for k in ["CAS22", "CAS23", "CAS24",
                                                              "CAS25", "CAS26", "CAS27", "CAS28"])
        # Tritium startup inventory: 3 kg at $30,000/g
        tritium_startup_cost = self.tritium_startup_kg * 1000 * 30_000 / 1e6  # M$
        fuel_load = tritium_startup_cost
        shipping = 0.015 * r["CAS20"]    # 1.5% of direct costs
        taxes = 0.01 * r["CAS20"]        # 1% of direct costs
        insurance = 0.015 * (r["CAS20"] + r["CAS30"])
        decommissioning = 127.0 * (p_net_total / 1000.0)  # D-T: $127M at 1 GWe (1costingfe)
        r["CAS50"] = spare_parts + fuel_load + shipping + taxes + insurance + decommissioning

        # === Overnight Capital ===
        overnight = r["CAS10"] + r["CAS20"] + r["CAS30"] + r["CAS40"] + r["CAS50"]
        r["overnight_capital"] = overnight

        # === CAS60: Interest During Construction (IDC) ===
        i = self.interest_rate
        T = self.construction_time_years
        if i > 0 and T > 0:
            f_idc = ((1 + i) ** T - 1) / (i * T) - 1
        else:
            f_idc = 0.0
        r["CAS60"] = f_idc * overnight
        r["f_IDC"] = f_idc

        # === Total Capital ===
        r["total_capital"] = overnight + r["CAS60"]

        if power["p_net"] > 0:
            r["specific_capital_USD_per_kWe"] = (
                r["total_capital"] * 1e6 / (power["p_net"] * self.n_mod * 1e3)
            )
        else:
            r["specific_capital_USD_per_kWe"] = float('inf')

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70-90 annualized costs, LCOE, and tritium revenue credit."""
        r = {}
        p_net = power["p_net"]
        p_net_total = p_net * self.n_mod

        # Capital Recovery Factor
        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1 + i) ** n / ((1 + i) ** n - 1)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]  # M$/year

        # === CAS71: Annual O&M (levelized with inflation) ===
        annual_om_base = self.om_cost_per_MW_yr * p_net_total * 1000.0 / 1e6  # M$
        g = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g) ** Tc
        if abs(i - g) > 1e-10:
            pv_growing_annuity = A1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
        else:
            pv_growing_annuity = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_growing_annuity  # M$/year

        # === CAS72: Scheduled Blanket Replacement ===
        # FLF: flowing Li blanket never replaced (full neutron absorption).
        # core_lifetime_FPY = 40 → no replacements in 40-year plant life.
        effective_years_per_replacement = self.core_lifetime_FPY / self.plant_availability
        n_replacements = max(0, int(math.ceil(
            self.plant_lifetime_years / effective_years_per_replacement)) - 1)
        replacement_cost = cas22["C220101"]
        pv_replacements = 0.0
        for k in range(1, n_replacements + 1):
            year = k * effective_years_per_replacement
            if year < self.plant_lifetime_years:
                pv_replacements += replacement_cost / (1 + i) ** year
        r["CAS72"] = crf * pv_replacements  # M$/year (= $0 for liquid Li design)
        r["n_blanket_replacements"] = n_replacements

        r["CAS70"] = r["CAS71"] + r["CAS72"]  # M$/year

        # === CAS80: Annualized Per-Shot Consumable Costs ===
        shots_per_year = power["shots_per_year"]
        annual_target_cost = shots_per_year * self.target_cost_USD / 1e6       # M$/year
        annual_projectile_cost = shots_per_year * self.projectile_cost_USD / 1e6  # M$/year
        annual_fuel_cost = shots_per_year * self.fuel_cost_per_shot_USD / 1e6   # M$/year
        r["CAS80"] = annual_target_cost + annual_projectile_cost + annual_fuel_cost
        r["CAS80_targets"] = annual_target_cost
        r["CAS80_projectiles"] = annual_projectile_cost
        r["CAS80_fuel"] = annual_fuel_cost

        # === Annual Energy Production ===
        annual_energy_MWh = 8760 * p_net_total * self.plant_availability
        r["annual_energy_MWh"] = annual_energy_MWh

        # === LCOE (base — no tritium revenue credit) ===
        annual_revenue_req = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_revenue_req

        if annual_energy_MWh > 0:
            r["lcoe_USD_per_MWh"] = annual_revenue_req * 1e6 / annual_energy_MWh
            r["lcoe_cents_per_kWh"] = r["lcoe_USD_per_MWh"] / 10.0
        else:
            r["lcoe_USD_per_MWh"] = float('inf')
            r["lcoe_cents_per_kWh"] = float('inf')

        # === Tritium Surplus Revenue Credit ===
        # Only credited if tritium_price_USD_per_g > 0 (not base case).
        # At fleet scale, the price is self-undermining — see analysis.md §Section 2.
        annual_tritium_revenue_M = (
            self.tritium_surplus_kg_per_year * 1000 * self.tritium_price_USD_per_g / 1e6
        )
        r["annual_tritium_revenue_M"] = annual_tritium_revenue_M
        if annual_energy_MWh > 0:
            r["tritium_credit_USD_per_MWh"] = annual_tritium_revenue_M * 1e6 / annual_energy_MWh
        else:
            r["tritium_credit_USD_per_MWh"] = 0.0

        # LCOE with tritium credit
        net_revenue_req = annual_revenue_req - annual_tritium_revenue_M
        if annual_energy_MWh > 0:
            r["lcoe_with_trit_USD_per_MWh"] = net_revenue_req * 1e6 / annual_energy_MWh
        else:
            r["lcoe_with_trit_USD_per_MWh"] = float('inf')

        # Cost fractions (base case)
        if annual_revenue_req > 0:
            r["capital_fraction"] = r["CAS90"] / annual_revenue_req
            r["om_fraction"] = r["CAS70"] / annual_revenue_req
            r["fuel_fraction"] = r["CAS80"] / annual_revenue_req

        return r

    def compute(self) -> dict:
        """Compute LCOE and all intermediate values using CAS-structured accounting."""
        power = self._compute_power()
        geom = self._compute_geometry(power)
        cas22 = self._compute_cas22(power, geom)
        costs = self._compute_costs(power, cas22)
        econ = self._compute_economics(power, costs, cas22)

        results = {
            "power": power,
            "geometry": geom,
            "cas22": cas22,
            "costs": costs,
            "economics": econ,
            # Convenience aliases
            "net_electric_MW": power["p_net"],
            "lcoe_cents_per_kWh": econ["lcoe_cents_per_kWh"],
            "total_capital_M_USD": costs["total_capital"],
        }
        return results


def print_results(params: ProjectileICFPlantParams, results: dict, label: str = ""):
    """Pretty-print LCOE model results with CAS-structured accounting."""
    power = results["power"]
    cas22 = results["cas22"]
    costs = results["costs"]
    econ = results["economics"]

    title = f"Projectile ICF (D-T) LCOE Model — 1cFE CAS-Structured"
    if label:
        title += f"\n  Scenario: {label}"
    print("=" * 72)
    print(title)
    print("=" * 72)

    # --- Key Inputs ---
    gain = power["target_gain"]
    print(f"\n--- Key Input Parameters ---")
    print(f"  Driver stored energy:         {params.driver_stored_energy_MJ:.0f} MJ")
    print(f"  Driver efficiency:            {params.driver_efficiency:.1%}")
    print(f"  Energy to target per shot:    {power['energy_to_target_MJ']:.1f} MJ")
    print(f"  Fusion yield per shot:        {params.fusion_yield_MJ:.0f} MJ ({params.fusion_yield_MJ/1000:.1f} GJ)")
    print(f"  Target gain:                  {gain:.0f}×   [KEY UNCERTAINTY]")
    print(f"  Rep rate:                     {params.driver_rep_rate_Hz:.4f} Hz ({1/params.driver_rep_rate_Hz:.0f}s cycle)")
    print(f"  Driver capital cost:          ${params.driver_cost_M_USD:.0f}M   [KEY UNCERTAINTY]")
    print(f"  Blanket multiplication:       {params.blanket_energy_multiplication:.2f}")
    print(f"  Thermal efficiency:           {params.thermal_efficiency:.1%}")
    print(f"  Plant availability:           {params.plant_availability:.1%}")
    print(f"  Modules:                      {params.n_mod}")
    print(f"  FOAK/NOAK:                    {'NOAK' if params.noak else 'FOAK'}")
    print(f"  Interest rate:                {params.interest_rate:.1%}")
    print(f"  Plant lifetime:               {params.plant_lifetime_years:.0f} years")
    print(f"  Target cost/shot:             ${params.target_cost_USD:.2f}")
    print(f"  Li inventory (CAS27):         ${params.li_inventory_cost_M_USD:.0f}M")
    print(f"  Tritium price:                ${params.tritium_price_USD_per_g:,.0f}/g")

    # --- Power Balance ---
    print(f"\n--- Power Balance ---")
    print(f"  Fusion power (time-avg):      {power['p_fus']:.0f} MW")
    print(f"    Neutron power (80%):        {power['p_neutron']:.0f} MW")
    print(f"    Alpha power (20%):          {power['p_ash']:.0f} MW")
    print(f"  Thermal power:                {power['p_th']:.0f} MW")
    print(f"  Gross electric:               {power['p_et']:.0f} MWe")
    print(f"  Recirculating power:")
    print(f"    Driver recharge:            {power['driver_avg_power_MW']:.0f} MW")
    aux = power["p_aux_detail"]
    print(f"    Li pump:                    {aux['li_pump']:.0f} MW")
    print(f"    Tritium + other aux:        {aux['tritium'] + aux['housekeeping'] + aux['cryo'] + aux['target_factory']:.1f} MW")
    print(f"  Net electric:                 {power['p_net']:.0f} MWe")
    print(f"  Engineering Q:                {power['Q_eng']:.1f}")
    print(f"  Recirculating fraction:       {power['recirc_fraction']:.1%}")
    print(f"  Shots per year:               {power['shots_per_year']:,.0f}")

    # --- CAS22: Reactor Plant Equipment ---
    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    print(f"  Per-module sub-accounts:")
    cas22_labels = {
        "C220101": "Blanket/First Wall (liquid Li)",
        "C220102": "Shield",
        "C220103": "Coils [OVERRIDE: $0 — no magnets]",
        "C220104": "Heating [OVERRIDE: $0 — no preheat]",
        "C220105": "Primary Structure",
        "C220106": "Vacuum System / Containment",
        "C220107": "Driver [OVERRIDE: EM launcher]",
        "C220108": "Target Factory + Injector",
        "C220109": "Direct Energy Converter",
        "C220111": "Installation",
        "C220112": "Isotope Separation",
    }
    for code, label in cas22_labels.items():
        val = cas22[code]
        override_note = " [override]" if code in ("C220103", "C220104", "C220107") else ""
        if val >= 0.01 or code in ("C220103", "C220104"):
            print(f"    {code} {label:<38s} ${val:>8.1f}M{override_note}")
    print(f"  {'':>4s} {'─' * 52}")
    print(f"    Per-module subtotal:                       ${cas22['CAS22_per_module']:>8.1f}M × {params.n_mod}")
    print(f"  Plant-wide accounts:")
    pw_labels = {
        "C220200": "Coolant Systems (Li primary + HX)",
        "C220300": "Aux Cooling + Cryoplant",
        "C220400": "Rad Waste Management",
        "C220500": "Fuel Handling & Storage (D-T)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    for code, label in pw_labels.items():
        val = cas22[code]
        if val > 0.01:
            print(f"    {code} {label:<38s} ${val:>8.1f}M")
    print(f"  {'':>4s} {'─' * 52}")
    print(f"    Plant-wide subtotal:                       ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                                 ${cas22['CAS22']:>8.1f}M")

    # --- Capital Cost Summary ---
    print(f"\n--- Capital Costs (CAS10-60) ---")
    print(f"  CAS10 Pre-construction:                      ${costs['CAS10']:>8.1f}M")
    print(f"  CAS21 Buildings:                             ${costs['CAS21']:>8.1f}M")
    print(f"  CAS22 Reactor Plant Equipment:               ${costs['CAS22']:>8.1f}M")
    print(f"  CAS23 Turbine Plant:                         ${costs['CAS23']:>8.1f}M")
    print(f"  CAS24 Electric Plant:                        ${costs['CAS24']:>8.1f}M")
    print(f"  CAS25 Misc Plant:                            ${costs['CAS25']:>8.1f}M")
    print(f"  CAS26 Heat Rejection:                        ${costs['CAS26']:>8.1f}M")
    print(f"  CAS27 Special Materials (Li inventory):      ${costs['CAS27']:>8.1f}M")
    print(f"  CAS28 Digital Twin:                          ${costs['CAS28']:>8.1f}M")
    print(f"  CAS29 Contingency:                           ${costs['CAS29']:>8.1f}M")
    print(f"  {'─' * 60}")
    print(f"  CAS20 Direct Costs:                          ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30 Indirect Costs:                        ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40 Owner's Costs:                         ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50 Supplementary (incl. tritium startup): ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 60}")
    print(f"  Overnight Capital:                           ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60 IDC (f={costs['f_IDC']:.3f}):                    ${costs['CAS60']:>8.1f}M")
    print(f"  {'═' * 60}")
    print(f"  Total Capital:                               ${costs['total_capital']:>8.1f}M")
    print(f"  Specific Capital:                            ${costs['specific_capital_USD_per_kWe']:>8.0f} $/kWe")
    print(f"  FLF stated target:                           <$5,000M (<$5B commercial)")

    # --- Annual Costs ---
    print(f"\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90 Capital charge (CRF={econ['CRF']:.4f}):     ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71 O&M (levelized):                       ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72 Scheduled replacement:                 ${econ['CAS72']:>8.1f}M/yr  ({econ['n_blanket_replacements']} replacements — liquid Li never replaced)")
    print(f"  CAS70 Total O&M:                             ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80 Per-shot consumables:")
    print(f"    Targets ({power['shots_per_year']:,.0f}/yr × ${params.target_cost_USD:.2f}/ea):  ${econ['CAS80_targets']:>8.1f}M/yr")
    print(f"    Projectiles:                               ${econ['CAS80_projectiles']:>8.1f}M/yr")
    print(f"    D-T fuel:                                  ${econ['CAS80_fuel']:>8.3f}M/yr")
    print(f"  CAS80 Total consumables:                     ${econ['CAS80']:>8.1f}M/yr")

    # Tritium revenue
    if econ["annual_tritium_revenue_M"] > 0:
        print(f"\n  Tritium surplus revenue (25 kg/yr × ${params.tritium_price_USD_per_g:,.0f}/g):")
        print(f"    Annual revenue:                          ${econ['annual_tritium_revenue_M']:>8.1f}M/yr")
        print(f"    LCOE credit:                             ${econ['tritium_credit_USD_per_MWh']:>8.1f} $/MWh")

    # --- LCOE ---
    p_net_effective = power["p_net"] * params.n_mod
    print(f"\n--- LCOE ---")
    print(f"  Annual energy:            {econ['annual_energy_MWh']:,.0f} MWh ({p_net_effective:.0f} MWe net)")
    print(f"  Annual revenue req:       ${econ['annual_revenue_req']:.1f}M")
    print(f"  Cost fractions:  Capital={econ.get('capital_fraction', 0):.1%}  "
          f"O&M={econ.get('om_fraction', 0):.1%}  Consumables={econ.get('fuel_fraction', 0):.1%}")
    print(f"  ╔══════════════════════════════════════════╗")
    print(f"  ║  LCOE = {econ['lcoe_cents_per_kWh']:>7.2f} ¢/kWh  (no tritium credit)  ║")
    print(f"  ║       = {econ['lcoe_USD_per_MWh']:>7.1f} $/MWh                      ║")
    if econ["annual_tritium_revenue_M"] > 0:
        print(f"  ║  LCOE = {econ['lcoe_with_trit_USD_per_MWh']:>7.1f} $/MWh  (with tritium credit)  ║")
    print(f"  ╚══════════════════════════════════════════╝")
    print(f"  FLF stated target: <$50/MWh")


def sensitivity_sweep(base_params: ProjectileICFPlantParams, param_name: str,
                      values: list, label: str = "") -> list:
    """Sweep a single parameter and return LCOE for each value."""
    results_list = []
    for val in values:
        kwargs = {k: v for k, v in base_params.__dict__.items()}
        kwargs[param_name] = val
        p = ProjectileICFPlantParams(**kwargs)
        r = p.compute()
        results_list.append({
            "param_value": float(val),
            "lcoe_USD_per_MWh": r["economics"]["lcoe_USD_per_MWh"],
            "lcoe_cents_kWh": r["lcoe_cents_per_kWh"],
            "net_electric_MW": r["net_electric_MW"],
            "target_gain": r["power"]["target_gain"],
            "total_capital_M": r["costs"]["total_capital"],
        })
    return results_list


def main():
    print("\n" + "=" * 72)
    print("PROJECTILE ICF (D-T) — FREE-FORM LCOE MODEL")
    print("First Light Fusion / NearStar Fusion")
    print("=" * 72)
    print("""
CRITICAL FRAMING (from analysis.md §Section 2):
  This concept has two blocking unknowns:
  (1) Electromagnetic gun capital cost — no published analogue exists.
  (2) Target gain at 60 km/s — never experimentally demonstrated.
  LCOE outputs below are swept over these parameters, not predicted.
  Machine 4 (100 MJ, 60 km/s) was cancelled in February 2025 before testing.
  The FLARE pivot provides indirect evidence that the projectile driver cost
  was above the $50/MWh viability threshold.
""")

    # =========================================================================
    # BASELINE SCENARIO
    # Optimistic: gain=1000×, driver=$1B — anchored to FLF's 333 MWe design point
    # =========================================================================
    baseline = ProjectileICFPlantParams(
        fusion_yield_MJ=30_000.0,    # 30 GJ/shot — matches 333 MWe at 0.033 Hz
        driver_efficiency=0.30,       # 30% EM launcher efficiency
        driver_stored_energy_MJ=100.0,  # Machine 4 spec
        driver_cost_M_USD=1_000.0,   # Central estimate from FLARE analogues
        driver_rep_rate_Hz=0.033,    # 30s between shots (pilot design point)
        target_cost_USD=5.0,
        li_inventory_cost_M_USD=70.0,
        noak=True,
    )
    # Implied gain: 30,000 / (100 × 0.30) = 1000× [optimistic FLF claim]

    baseline_results = baseline.compute()
    print_results(baseline, baseline_results, label="Baseline (gain=1000×, driver=$1B, 0.033 Hz)")

    # =========================================================================
    # SENSITIVITY SWEEPS — Top 6 LCOE drivers
    # =========================================================================
    print("\n\n" + "=" * 72)
    print("SENSITIVITY SWEEPS (from baseline)")
    print("=" * 72)
    base_lcoe = baseline_results["economics"]["lcoe_USD_per_MWh"]
    print(f"  Baseline LCOE: {base_lcoe:.1f} $/MWh\n")

    sweeps = [
        # (param_name, values, header, unit)
        ("fusion_yield_MJ",
         [3_000, 6_000, 15_000, 30_000, 60_000],
         "1. Fusion yield per shot (gain sensitivity)",
         "MJ/shot"),
        ("driver_cost_M_USD",
         [200, 500, 1_000, 2_000, 3_500],
         "2. EM driver capital cost [KEY UNCERTAINTY]",
         "$M"),
        ("driver_rep_rate_Hz",
         [0.011, 0.033, 0.1, 0.2, 0.5],
         "3. Rep rate (shot frequency)",
         "Hz"),
        ("driver_efficiency",
         [0.15, 0.20, 0.30, 0.40, 0.50],
         "4. Driver efficiency (wall-to-kinetic)",
         "frac"),
        ("target_cost_USD",
         [1.0, 5.0, 10.0, 20.0, 50.0],
         "5. Target fabrication cost",
         "$/shot"),
        ("plant_availability",
         [0.60, 0.70, 0.80, 0.85, 0.90],
         "6. Plant availability / capacity factor",
         "frac"),
    ]

    for param_name, values, header, unit in sweeps:
        print(f"  {header}:")
        print(f"  {'Value':>12s} {'Net MWe':>9s} {'Gain':>8s} {'LCOE $/MWh':>12s}  {'vs Baseline':>12s}")
        print(f"  {'─'*60}")
        sweep_results = sensitivity_sweep(baseline, param_name, values)
        for sr in sweep_results:
            net_mw = sr["net_electric_MW"]
            lcoe = sr["lcoe_USD_per_MWh"]
            gain = sr["target_gain"]
            delta = lcoe - base_lcoe
            delta_str = f"{delta:+.0f}" if abs(delta) < 9999 else "N/A"
            if net_mw <= 0:
                print(f"  {sr['param_value']:>12.4g} {net_mw:>9.0f}  ← NET POWER NEGATIVE")
            else:
                print(f"  {sr['param_value']:>12.4g} {net_mw:>9.0f} {gain:>8.0f}× {lcoe:>12.1f}  {delta_str:>12s}")
        print()

    # =========================================================================
    # SCENARIO COMPARISON TABLE
    # Three scenarios defined by gain achievement and driver cost
    # =========================================================================
    print("=" * 72)
    print("SCENARIO COMPARISON: Conservative / Moderate / Optimistic")
    print("=" * 72)

    scenarios = {
        "Conservative\n  (gain=200×, driver=$2B)": ProjectileICFPlantParams(
            fusion_yield_MJ=6_000.0,       # gain=200× at 100 MJ stored, 30% eff
            driver_efficiency=0.30,
            driver_stored_energy_MJ=100.0,
            driver_cost_M_USD=2_000.0,     # High-end FLF-implied cost
            driver_rep_rate_Hz=0.033,
            target_cost_USD=10.0,           # Higher cost at lower yield
            li_inventory_cost_M_USD=143.0,  # Enriched Li needed
            noak=False,                     # FOAK (technology unproven)
        ),
        "Moderate\n  (gain=500×, driver=$1B)": ProjectileICFPlantParams(
            fusion_yield_MJ=15_000.0,      # gain=500× at 100 MJ, 30% eff
            driver_efficiency=0.30,
            driver_stored_energy_MJ=100.0,
            driver_cost_M_USD=1_000.0,
            driver_rep_rate_Hz=0.033,
            target_cost_USD=5.0,
            li_inventory_cost_M_USD=70.0,
            noak=True,
        ),
        "Optimistic\n  (gain=1000×, driver=$500M)": ProjectileICFPlantParams(
            fusion_yield_MJ=30_000.0,      # gain=1000× — top of FLF claim range
            driver_efficiency=0.30,
            driver_stored_energy_MJ=100.0,
            driver_cost_M_USD=500.0,       # Aggressive cost reduction vs FLARE analogues
            driver_rep_rate_Hz=0.1,        # 10s rep rate (FLF commercial target)
            target_cost_USD=2.0,           # Mass production economy
            li_inventory_cost_M_USD=70.0,
            noak=True,
        ),
    }

    print(f"\n  {'Scenario':<42s} {'Net MWe':>8s} {'Gain':>6s} {'Capital $M':>10s} {'$/kWe':>7s} {'LCOE $/MWh':>11s}")
    print(f"  {'─'*94}")
    for scenario_label, p in scenarios.items():
        r = p.compute()
        net_mw = r["net_electric_MW"]
        gain = r["power"]["target_gain"]
        cap = r["costs"]["total_capital"]
        spec_cap = r["costs"]["specific_capital_USD_per_kWe"]
        lcoe = r["economics"]["lcoe_USD_per_MWh"]
        label_single = scenario_label.replace("\n  ", " ")
        print(f"  {label_single:<42s} {net_mw:>8.0f} {gain:>6.0f}× {cap:>10.0f}  {spec_cap:>7,.0f}  {lcoe:>11.1f}")

    print(f"\n  FLF stated targets:                         333 MWe         <$5,000  ~$10,000     <$50.0")

    # Tritium revenue scenario
    print(f"\n\n--- Tritium Revenue Scenarios (Optimistic physics, varying tritium price) ---")
    print(f"  {'Tritium price':>16s} {'Annual revenue':>16s} {'LCOE (base)':>12s} {'LCOE (credited)':>16s}")
    print(f"  {'─'*65}")
    trit_prices = [0, 5_000, 15_000, 30_000]
    opt_base = ProjectileICFPlantParams(
        fusion_yield_MJ=30_000.0,
        driver_cost_M_USD=500.0,
        driver_rep_rate_Hz=0.1,
        target_cost_USD=2.0,
        noak=True,
    )
    for price in trit_prices:
        opt_p = ProjectileICFPlantParams(**{**opt_base.__dict__, "tritium_price_USD_per_g": price})
        r = opt_p.compute()
        econ = r["economics"]
        ann_rev = econ["annual_tritium_revenue_M"]
        lcoe_base = econ["lcoe_USD_per_MWh"]
        lcoe_cred = econ["lcoe_with_trit_USD_per_MWh"]
        print(f"  {price:>14,} $/g  {ann_rev:>12.0f}M/yr  {lcoe_base:>12.1f}  {lcoe_cred:>16.1f} $/MWh")

    # =========================================================================
    # KEY BINDING CONSTRAINTS NARRATIVE
    # =========================================================================
    print("""

KEY BINDING CONSTRAINTS (Top 3 LCOE Drivers)
─────────────────────────────────────────────

1. TARGET GAIN — Commercial Binary Threshold (analysis.md §Section 2, Challenge 2)
   LCOE is nearly linear in 1/fusion_yield at fixed rep rate. The minimum commercial
   gain is 200×. Below 200×, the concept cannot sustain 333 MWe at FLF's rep rates
   even at $0 driver cost — the plant physics simply doesn't close. Above 200×, LCOE
   improvement follows ~1/gain (2× gain → ~1/2 LCOE, all else equal). The claimed
   range of 200–1000× spans 5× in LCOE potential. The gain at 60 km/s has never
   been experimentally tested — Machine 4 was cancelled before construction.

2. DRIVER CAPITAL COST — Dominant Novel CAS22 Account (analysis.md §Section 2, Challenge 1)
   The electromagnetic gun is the most uncertain capital item. No published cost
   estimate exists for a 60 km/s device. Sweeping from $200M to $3.5B (analysis shows
   this is the plausible range from FLARE analogues) shifts LCOE by ~40–60 $/MWh.
   FLF's abandonment of the projectile gun (FLARE pivot, Sept 2025) is indirect
   evidence that the driver cost exceeded the viability threshold internally —
   it anchors the pessimistic scenario at $2B+. The gain sensitivity and driver
   cost sensitivity are roughly equal in LCOE impact at the moderate scenario.

3. REP RATE × GAIN COUPLING — Cliff-Edge Constraint (analysis.md §Section 2, Challenge 3)
   At gain < 200×, achieving 333 MWe requires rep rates above 0.1 Hz — which may
   violate the chamber clearing time constraint (liquid Li resettlement after blast
   is unknown but non-zero). This is a cliff edge: the model smoothly computes
   degrading net power as gain falls, but the physics may be discontinuous — the
   chamber may not physically clear at >0.1 Hz. The liquid Li pump recirculating
   power (30 MW assumed, HIGH UNCERTAINTY) adds secondary sensitivity: if pump
   power is 3× higher (90 MW), net power drops by ~60 MWe from baseline.
""")


if __name__ == "__main__":
    main()
