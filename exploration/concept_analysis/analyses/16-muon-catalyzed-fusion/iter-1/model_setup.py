"""
Muon-Catalyzed Fusion (D-T) First-Pass LCOE Model
===================================================
1cFE First Pass Concept Analysis
Concept: Muon-Catalyzed Fusion (μCF) with D-T fuel
Company: Acceleron Fusion (US; founded 2008, spun off 2022)

This is a parameterized LCOE model for a muon-catalyzed fusion power plant
based on: Acceleron Fusion's ARPA-E BETHE presentation (July 2025), the
Wikipedia article on μCF physics, and the Phase 1a analysis
(analyses/16-muon-catalyzed-fusion/analysis.md).

μCF is architecturally unlike any standard fusion concept. A superconducting
proton accelerator produces muons that catalyze D-T reactions in a
material-containment target — no plasma, no HTS magnets, no pulsed driver.
The energy balance is dominated by the ratio of fusion energy produced to
electrical energy consumed per muon (Q_sci).

CRITICAL PHYSICS CONSTRAINT (LCOE-DEFINING):
    Q_sci = N_fus × E_fus / E_mu_elec
    Commercial viability requires: Q_sci × M_blanket × eta_th > 1 + (P_aux / P_beam)

At Acceleron's stated targets (200 fusions/muon, 2.5 GeV/muon):
    Q_sci ≈ 1.41 → P_et / P_beam ≈ 0.77 (energy sink at any aux load)

The baseline scenario in this model uses E_mu = 1.2 GeV — an aspirational
breakthrough roughly 2× beyond Acceleron's 2.5 GeV stated target — to produce
a positive net power output. Even at these aspirational parameters, LCOE is
~$800/MWh, approximately 32× Acceleron's $0.025/kWh ($25/MWh) target. The
dominant driver is accelerator capital cost.

Economy-of-scale cross-concept scaling (α = 0.6):
    scaled_lcoe = native_lcoe × (P_native / 1000 MWe)^(1 - α)
Applied post-hoc to native physics-derived power.

Key references:
    Newburg, S. (2025) "Muon Catalyzed Fusion," ARPA-E BETHE Program
    Presentation, July 2025. Acceleron Fusion.
    [iter-01/sources/acceleron-arpa-e-presentation-2025.md]

    Wikipedia, Muon-Catalyzed Fusion (Physics Reference)
    [iter-01/sources/muon-catalyzed-fusion-physics.md]

    1costingfe costing_constants.yaml — CAS scaling laws and unit costs
    [~/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml]

    analysis.md — Phase D1+ analysis with quantitative parameters
    [analyses/16-muon-catalyzed-fusion/analysis.md]

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass, field

# ============================================================================
# Physical constants
# ============================================================================
E_FUSION_MEV  = 17.6                          # D-T fusion energy [MeV]
E_FUSION_J    = 17.6e6 * 1.602e-19            # D-T fusion energy [J]
GEV_TO_J      = 1.0e9 * 1.602e-19             # Conversion: 1 GeV → Joules
AMU_KG        = 1.66053906660e-27             # 1 atomic mass unit [kg]

# ============================================================================
# Reference power levels for 1costingfe scaling laws
# ============================================================================
P_TH_REF  = 2500.0   # Reference thermal power [MW]
P_ET_REF  = 1100.0   # Reference gross electric power [MW]
P_NET_REF = 1000.0   # Reference net electric power [MW]


@dataclass
class MuCFPlantParams:
    """
    Parameterized Muon-Catalyzed Fusion (D-T) power plant model.

    Architecture overview:
    ┌──────────────────────────────────────────────────────┐
    │  Proton linac  →  active-target muon source          │
    │       ↓                                              │
    │  μ + D-T → He-4 + n  (catalysis, N_fus times/muon)  │
    │       ↓                                              │
    │  Neutrons → breeding blanket → thermal energy        │
    │  Alphas   → local target heating → thermal energy    │
    │       ↓                                              │
    │  sCO₂ Brayton cycle → gross electric                 │
    │       ↓                                              │
    │  Net electric = Gross - Recirculating (accelerator + aux) │
    └──────────────────────────────────────────────────────┘

    Key structural differences from 1costingfe standard models:
    • C220103 (Coils):          ZERO — no plasma confinement
    • C220104 (Heating):        ZERO — accelerator IS the driver
    • C220107 (Power Supplies): OVERRIDE — superconducting linac capital
    • C220108 (Target Factory): ZERO — continuous operation, no per-shot targets

    Uncertainty tiers used in docstrings:
    • (no tag)             — well-established physics or engineering constant
    • MODERATE UNCERTAINTY — reasonable estimate from documented analogues
    • HIGH UNCERTAINTY     — speculative or poorly constrained
    • PHYSICS CEILING      — fundamental quantum mechanical hard limit
    """

    # =========================================================================
    # ACCELERATOR & MUON SOURCE
    # =========================================================================

    acc_beam_power_MW: float = 100.0
    """Wall-plug electrical power consumed by accelerator system [MW].
    This is the dominant recirculating load. Acceleron targets ~100 MWe net
    with 47% recirc, implying ~89 MW beam; 100 MW used as round baseline.
    Source: analysis.md §S5, §S2 (energy balance discussion).
    Ref: acceleron-arpa-e-presentation-2025.md §Muon source.
    HIGH UNCERTAINTY — no plant-scale accelerator design published."""

    E_mu_elec_GeV: float = 1.2
    """Electrical energy consumed per muon produced [GeV_electrical].
    Conventional accelerators: ~6 GeV/muon [muon-catalyzed-fusion-physics.md
    §Problems facing practical exploitation]. Acceleron active-target target:
    2.5–3 GeV [acceleron-arpa-e-presentation-2025.md §Cost contour].
    Baseline 1.2 GeV requires breakthrough 2× beyond stated target — used
    to produce net-positive output for LCOE corridor estimation.
    Source: analysis.md §S2 (energy balance challenge), §S5 (parameter table).
    HIGH UNCERTAINTY — PSI experimental results not yet published."""

    n_fus_per_muon: float = 240.0
    """D-T catalysis cycles per muon before permanent muon loss [dimensionless].
    Alpha-sticking (0.3–0.5%) limits max fusions/muon to ~200–350.
    Demonstrated record: 150 (Los Alamos LAMPF) [muon-catalyzed-fusion-
    physics.md §Problems facing practical exploitation].
    Acceleron stretch target: 300 [dossier.md §Summary].
    Baseline 240 sits just below the physics ceiling at 0.4% sticking (= 250).
    Source: analysis.md §S2, §S5.
    HIGH UNCERTAINTY — PHYSICS CEILING (100 / alpha_sticking_pct)."""

    alpha_sticking_pct: float = 0.4
    """Alpha-sticking probability per fusion event [%].
    Probability that the muon permanently attaches to the alpha particle,
    ending the catalysis chain. Jackson (1957): ~1%; revised measurements:
    0.3–0.5% [muon-catalyzed-fusion-physics.md §Problems facing practical
    exploitation]. Physics ceiling on n_fus_per_muon = 100 / alpha_sticking_pct.
    Source: analysis.md §S2.
    PHYSICS CEILING — not a freely adjustable engineering parameter."""

    # =========================================================================
    # ENERGY CAPTURE
    # =========================================================================

    M_blanket: float = 1.10
    """Blanket energy multiplication (neutrons captured in Li breeding blanket,
    including exothermic Li-6 + n → T + He-4 reaction, ~4.8 MeV additional).
    Source: 1costingfe costing_constants.yaml (standard D-T value).
    Ref: Standard fusion engineering reference."""

    eta_th: float = 0.50
    """Thermal-to-electric conversion efficiency [fraction].
    sCO₂ Brayton cycle at ~700°C (mid-range of stated 500–1000°C).
    High-efficiency sCO₂ Brayton: ~45–52% demonstrated at 600–800°C.
    Source: Inferred from acceleron-company-overview.md §Advantages (500–1000°C)
    and Brayton cycle engineering.
    MODERATE UNCERTAINTY — Acceleron has not published a specific thermal
    efficiency value."""

    # =========================================================================
    # PLANT CONFIGURATION
    # =========================================================================

    n_mod: int = 1
    """Number of fusion modules per plant.
    Single-module design for 100 MWe class plant.
    Source: acceleron-company-overview.md §Advantages. ASSUMED."""

    plant_availability: float = 0.85
    """Plant capacity factor / availability [fraction].
    Particle physics CW accelerators (SNS, ESS): 85–95% availability.
    Power generation requires commercial-grade scheduling not yet characterized.
    Source: analysis.md §S5 (Gap #11). MODERATE UNCERTAINTY."""

    plant_lifetime_years: float = 40.0
    """Plant economic lifetime [years].
    Source: 1costingfe default. Standard fusion plant assumption."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds 10% contingency on direct costs.
    Source: 1costingfe CAS29 convention."""

    # =========================================================================
    # CAPITAL — ACCELERATOR SYSTEM (C220107 OVERRIDE)
    # =========================================================================

    acc_capital_M: float = 2000.0
    """Capital cost of superconducting proton accelerator + active-target muon
    source system [$M]. Maps to C220107 (Power Supplies) — CONCEPT OVERRIDE.
    THIS IS THE DOMINANT CAPITAL COST AND LARGEST SINGLE UNCERTAINTY.
    Analogues: SNS (ORNL) $1.4B, 1 GeV, 1.4 MW beam; ESS (Sweden) ~€2B, 2 GeV.
    Power generation requires CW operation at >> 1 MW beam. Acceleron's
    active-target design has no published cost estimate at any scale.
    $2000M is a rough FOAK estimate for a novel 100 MW CW GeV-class linac.
    Source: analysis.md §S2 (Accelerator cost challenge), §S5 (Gap #2).
    Ref: dossier.md §Driver Technology.
    HIGH UNCERTAINTY — range easily $500M–$10B+ depending on design maturity."""

    # =========================================================================
    # CHAMBER & BLANKET GEOMETRY
    # =========================================================================

    chamber_inner_radius_m: float = 1.0
    """Inner radius of material-containment fusion chamber [m].
    Non-plasma, high-density DT medium — far smaller than IFE/MFE chambers.
    Commercial-scale chamber architecture is undefined (analysis.md §S2, §S4).
    Source: ASSUMED — rough scale for compact material-containment system.
    HIGH UNCERTAINTY."""

    blanket_thickness_m: float = 0.80
    """Breeding blanket + first wall thickness [m].
    Type unspecified (FLiBe, LiPb, or solid ceramic all plausible).
    14.1 MeV neutron spectrum identical to plasma D-T requires full TBR blanket.
    Source: ASSUMED. Ref: analysis.md §S3 (Tritium Breeding Blanket).
    MODERATE UNCERTAINTY."""

    shield_thickness_m: float = 0.50
    """Neutron shielding thickness [m].
    Full 14.1 MeV shielding required — same neutron spectrum as plasma D-T.
    Source: ASSUMED. Ref: Standard D-T shielding requirement."""

    structure_thickness_m: float = 0.25
    """Primary structure thickness [m].
    Source: ASSUMED — analogy to compact accelerator-based facility.
    MODERATE UNCERTAINTY."""

    vessel_thickness_m: float = 0.08
    """Chamber containment vessel thickness [m].
    High-pressure DT environment (non-vacuum). May use metallic or ceramic
    containment rather than vacuum vessel.
    Source: ASSUMED. MODERATE UNCERTAINTY."""

    blanket_unit_cost: float = 0.60
    """Blanket/first-wall unit cost [M$/m³]. Full D-T breeding blanket.
    Source: 1costingfe costing_constants.yaml, blanket_unit_cost_dt."""

    # =========================================================================
    # AUXILIARY POWER (recirculating loads beyond accelerator)
    # =========================================================================

    p_cryo_MW: float = 8.0
    """Cryogenic system power [MW] for superconducting accelerator RF cavities.
    Much larger than IFE/MFE cryoplants — CW GeV linac requires continuous
    cryogenic operation at high heat load.
    Source: ASSUMED from SNS/ESS cryoplant operational analogues.
    MODERATE UNCERTAINTY."""

    p_trit_MW: float = 10.0
    """Tritium processing and handling power [MW].
    Source: 1costingfe ife_zpinch.yaml default for D-T systems."""

    p_house_MW: float = 4.0
    """Housekeeping / facility power [MW].
    Source: 1costingfe ife_zpinch.yaml default."""

    p_controls_MW: float = 2.0
    """Accelerator beam control, diagnostics, ML-optimization power [MW].
    Source: ASSUMED from particle physics accelerator operational analogues.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # FINANCIAL
    # =========================================================================

    interest_rate: float = 0.08
    """Real discount rate / WACC [fraction].
    Source: 1costingfe interest_rate default."""

    inflation_rate: float = 0.02
    """Inflation rate for O&M levelization [fraction].
    Source: 1costingfe default."""

    construction_time_years: float = 6.0
    """Construction period [years].
    Source: 1costingfe reference_construction_time."""

    om_rate_fraction: float = 0.025
    """Annual O&M as fraction of overnight capital.
    SNS O&M: ~$100M/yr on $1.4B ≈ 7%. Commercial plant target much lower.
    2.5% reflects expectation of industrial learning vs. scientific facility.
    Source: ASSUMED. MODERATE UNCERTAINTY — accelerator O&M poorly characterized
    for commercial power generation mission (analysis.md §S2, S5 Gap #5)."""

    core_lifetime_FPY: float = 5.0
    """Blanket/first-wall core lifetime [full-power-years before replacement].
    D-T 14.1 MeV neutrons: 5–10 FPY (~20 dpa/yr).
    Source: 1costingfe costing_constants.yaml, core_lifetime_dt."""

    # =========================================================================
    # FUEL & STARTUP COSTS
    # =========================================================================

    u_deuterium_per_kg: float = 2175.0
    """Deuterium unit cost [$/kg].
    Source: 1costingfe costing_constants.yaml, u_deuterium."""

    tritium_startup_M_ref: float = 40.0
    """Tritium startup inventory cost [$M] at 1 GWe reference.
    Startup: ~1 kg T at >$35,000/g. Scaled to plant size in CAS50.
    Source: 1costingfe costing_constants.yaml startup_fuel_dt."""

    # =========================================================================
    # REGULATORY
    # =========================================================================

    regulatory_multiplier: float = 1.5
    """Building cost multiplier for D-T nuclear facility regulatory overhead.
    Lower than Stewart & Shirvan 2.2× tokamak value: μCF has no plasma
    disruption or runaway electron hazards, simpler nuclear safety case.
    Source: ASSUMED — analysis.md §S7 (D-T regulatory environment).
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # COMPUTE METHODS
    # =========================================================================

    def _compute_power(self) -> dict:
        """Layer 1: Physics-based power balance from accelerator parameters.

        Energy flow (per module):
          Beam power [P_beam] → muon production → catalysis cycles [N_fus]
          → fusion power [P_fus] → thermal [P_th] → gross electric [P_et]
          → net electric [P_net] = P_et - P_beam - P_aux
        """
        r: dict = {}

        # --- Muon production rate ---
        E_mu_J = self.E_mu_elec_GeV * GEV_TO_J       # J per muon (electrical)
        r["E_mu_J"] = E_mu_J

        P_beam_W = self.acc_beam_power_MW * 1e6
        muon_rate = P_beam_W / E_mu_J                  # muons/s
        r["muon_rate_per_s"] = muon_rate

        # Physics ceiling check (alpha-sticking)
        n_fus_ceiling = 100.0 / self.alpha_sticking_pct
        r["n_fus_physics_ceiling"] = n_fus_ceiling
        r["ceiling_violated"] = (self.n_fus_per_muon > n_fus_ceiling)

        # --- Fusion power ---
        fusion_rate = muon_rate * self.n_fus_per_muon  # fusions/s
        r["fusion_rate_per_s"] = fusion_rate

        p_fus = fusion_rate * E_FUSION_J / 1e6          # MW
        r["p_fus"] = p_fus

        # Scientific Q: fusion thermal / accelerator electrical
        Q_sci = p_fus / self.acc_beam_power_MW
        r["Q_sci"] = Q_sci

        # D-T energy partition: 80% neutrons (14.1 MeV), 20% alphas (3.5 MeV)
        r["p_neutron"] = p_fus * 0.80
        r["p_alpha"]   = p_fus * 0.20

        # --- Thermal power ---
        # All fusion energy eventually thermalizes; blanket Li reaction adds ~10%
        p_th = p_fus * self.M_blanket
        r["p_th"] = p_th

        # --- Gross electric ---
        p_et = p_th * self.eta_th
        r["p_et"] = p_et

        # --- Recirculating power ---
        p_aux = (self.p_cryo_MW + self.p_trit_MW
                 + self.p_house_MW + self.p_controls_MW)
        r["p_aux"] = p_aux
        p_recirc = self.acc_beam_power_MW + p_aux
        r["p_recirc"] = p_recirc

        # --- Net electric ---
        p_net = p_et - p_recirc
        r["p_net"] = p_net

        # Multi-module plant totals
        r["p_net_plant"] = p_net * self.n_mod
        r["p_et_plant"]  = p_et * self.n_mod
        r["p_th_plant"]  = p_th * self.n_mod

        # --- Figures of merit ---
        r["Q_eng"] = p_fus / p_recirc if p_recirc > 0 else float('inf')
        r["recirc_fraction"] = p_recirc / p_et if p_et > 0 else float('inf')

        # Gross-to-driver ratio (viability indicator: must be > 1 for any net power)
        r["gross_to_driver_ratio"] = p_et / self.acc_beam_power_MW

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Chamber geometry volumes using spherical shells.
        Spherical geometry used for compact material-containment fusion chamber."""
        r: dict = {}

        ri = self.chamber_inner_radius_m

        def sphere_shell_vol(r_in: float, thickness: float) -> float:
            r_out = r_in + thickness
            return (4.0 / 3.0) * math.pi * (r_out**3 - r_in**3)

        r_b = ri + self.blanket_thickness_m
        r["blanket_vol_m3"]   = sphere_shell_vol(ri, self.blanket_thickness_m)

        r_s = r_b + self.shield_thickness_m
        r["shield_vol_m3"]    = sphere_shell_vol(r_b, self.shield_thickness_m)

        r_st = r_s + self.structure_thickness_m
        r["structure_vol_m3"] = sphere_shell_vol(r_s, self.structure_thickness_m)

        r["vessel_vol_m3"]    = sphere_shell_vol(r_st, self.vessel_thickness_m)

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts.

        μCF-specific overrides (marked [OVERRIDE]):
        • C220103: ZERO — no plasma confinement magnets
        • C220104: ZERO — accelerator is heating mechanism
        • C220107: Direct accelerator capital (not power-scaled formula)
        • C220108: ZERO — continuous process, no target fabrication

        All other sub-accounts use 1costingfe power-scaling laws.
        """
        r: dict = {}

        p_th  = max(power["p_th"], 1.0)
        p_et  = max(power["p_et"], 1.0)
        # Use abs() so CAS22 geometry/cost calculations work even for negative-Q scenarios
        p_net_safe = max(abs(power["p_net"]) * self.n_mod, 1.0)

        # C220101: First Wall + Blanket (volume × unit_cost × power-scale)
        # Source: 1costingfe blanket_unit_cost_dt = 0.60 M$/m³
        r["C220101"] = (self.blanket_unit_cost
                        * geom["blanket_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220102: Shield (HT + LT + Bioshield)
        # Source: 1costingfe shield_unit_cost = 0.74 M$/m³
        r["C220102"] = (0.74
                        * geom["shield_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: Coils — ZERO [OVERRIDE: no plasma confinement magnets]
        # μCF key structural advantage: eliminates largest MFE capital item.
        r["C220103"] = 0.0

        # C220104: Supplementary Heating — ZERO [OVERRIDE]
        # Accelerator beam produces muons directly; no separate plasma heating.
        r["C220104"] = 0.0

        # C220105: Primary Structure
        # Source: 1costingfe structure_unit_cost = 0.15 M$/m³
        r["C220105"] = (0.15
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: Chamber Containment Vessel
        # Reduced from 1costingfe vessel_unit_cost=0.72 because non-vacuum system.
        # Source: DEFAULT from 1costingfe, reduced 0.72→0.40 for non-vacuum.
        r["C220106"] = (0.40
                        * geom["vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # C220107: Power Supplies — OVERRIDE with accelerator capital cost
        # Superconducting proton linac + active-target muon source.
        # DOMINANT COST ITEM. Direct estimate, not power-scaled formula.
        # Source: analysis.md §S2 Gap #2; SNS/ESS analogues; HIGH UNCERTAINTY.
        r["C220107"] = self.acc_capital_M

        # C220108: Target Factory — ZERO [OVERRIDE]
        # μCF is a continuous process; no per-shot target fabrication required.
        # Compare: IFE target_factory_base = 244 M$ — inapplicable here.
        r["C220108"] = 0.0

        # C220109: Direct Energy Converter — not applicable
        r["C220109"] = 0.0

        # C220110: Remote Handling (D-T neutron damage requires full RH suite)
        # Source: 1costingfe remote_handling_dt_base = 150 M$ at 1 GWe, ^0.6 scaling
        r["C220110"] = 150.0 * (p_net_safe / P_NET_REF) ** 0.6

        # C220111: Installation labor
        # Source: 1costingfe installation_frac = 0.14
        reactor_sub = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"])
        r["C220111"] = 0.14 * reactor_sub

        # C220112: Isotope Separation — 0 (handled in CAS80 fuel costs)
        r["C220112"] = 0.0

        r["CAS22_per_module"] = reactor_sub + r["C220111"] + r["C220112"]

        # --- Plant-wide accounts ---
        p_th_total  = power["p_th"] * self.n_mod
        p_net_total = abs(power["p_net"]) * self.n_mod  # abs for negative-Q safety

        # C220200: Coolant Systems (Brayton cycle primary + intermediate loops)
        # Source: 1costingfe CAS22 plant-wide formulas
        C220201 = 166.0 * (p_net_total / 1000.0)
        C220202 = 40.6  * (p_th_total  / 3500.0) ** 0.55
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling + Cryoplant (enlarged for SC linac)
        # Source: 1costingfe CAS22 formula (C220301 + C220302)
        C220301 = 1.1e-3 * p_th_total
        C220302 = 200.0 * (max(self.p_cryo_MW, 0.01) / 30.0) ** 0.7
        r["C220300"] = C220301 + C220302

        # C220400: Radioactive Waste Management
        # Source: 1costingfe formula
        r["C220400"] = 1.96 * (p_th_total / 1000.0)

        # C220500: Tritium Fuel Handling & Storage
        # Source: 1costingfe fuel_handling_dt_base = 120 M$ at 1 GWe, ^0.7 scaling
        r["C220500"] = 120.0 * (p_net_total / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        # Source: 1costingfe formula
        r["C220600"] = 11.5 * (p_net_total / 1000.0) ** 0.8

        # C220700: Instrumentation & Control (accelerator controls add cost)
        # Source: 1costingfe formula, not scaled up — accelerator controls in C220107
        r["C220700"] = 85.0 * (p_th_total / 3500.0) ** 0.65

        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        r["CAS22"] = r["CAS22_per_module"] * self.n_mod + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: CAS10-60 capital cost build-up."""
        r: dict = {}

        p_et = max(power["p_et"], 1.0)
        p_net = power["p_net"]
        p_net_safe = max(abs(p_net) * self.n_mod, 1.0)   # safe for negative-Q

        # === CAS10: Pre-construction ===
        land_cost     = 0.25 * p_net_safe * 10_000 / 1e6   # $0.25 acres/MWe × $10k/acre
        licensing     = 5.0 if not self.noak else 2.5       # D-T licensing
        # Source: 1costingfe CAS10 constants
        r["CAS10"] = (3.0      # site_permits
                      + (4.0 if self.noak else 20.0)        # plant_studies
                      + 2.0    # plant_permits
                      + 1.0    # plant_reports
                      + 1.0    # other_precon
                      + land_cost
                      + licensing)

        # === CAS21: Buildings ===
        # D-T facility building costs (M$ at P_ET_REF = 1100 MW gross electric)
        # Source: 1costingfe building_costs dt column; accelerator hall replaces
        # reactor hall (ASSUMED); hot cell reduced vs. tokamak (no PFCs).
        building_items_M = {
            "site_improvements":   85.0,
            "accelerator_hall":   120.0,   # ASSUMED: replaces tokamak reactor building
            "turbine_building":    58.0,
            "hot_cell":            60.0,   # Reduced: no extreme-flux PFC handling
            "reactor_auxiliaries": 29.0,
            "fuel_storage":         9.0,
            "control_room":        14.0,
            "security":             3.5,
            "ventilation_hvac":    17.0,
            "administration":       9.0,
            "maintenance":         17.0,
            "heat_exchanger":      17.0,
            "power_supply_bldg":   17.0,   # HV building for accelerator power
            "cryogenics":          14.0,
            "misc":                 5.0,
        }
        total_bldg_ref = sum(building_items_M.values())    # M$ at P_ET_REF
        cas21_raw = total_bldg_ref * p_et / P_ET_REF       # scaled to actual P_et
        # Apply D-T nuclear regulatory multiplier
        r["CAS21"] = cas21_raw * self.regulatory_multiplier
        r["CAS21_detail"] = {k: v * p_et / P_ET_REF * self.regulatory_multiplier
                             for k, v in building_items_M.items()}

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment (sCO₂ Brayton) ===
        # Brayton turbomachinery slightly more expensive per MW than steam Rankine.
        # Source: DEFAULT 1costingfe turbine_per_mw (Rankine) × 1.26 for Brayton
        r["CAS23"] = self.n_mod * p_et * 0.25   # M$/MW

        # === CAS24: Electric Plant Equipment ===
        # Source: 1costingfe costing_constants.yaml electric_per_mw
        r["CAS24"] = self.n_mod * p_et * 0.08418

        # === CAS25: Misc Plant Equipment ===
        # Source: 1costingfe costing_constants.yaml misc_per_mw
        r["CAS25"] = self.n_mod * p_et * 0.05124

        # === CAS26: Heat Rejection ===
        # Source: 1costingfe heat_rej_per_mw (Rankine reference, similar for Brayton)
        r["CAS26"] = self.n_mod * p_et * 0.03416

        # === CAS27: Special Materials (Li-6 enrichment + initial tritium inventory) ===
        # Source: 1costingfe special_materials_dt = 15 M$ at 1 GWe, ^0.5 scaling
        r["CAS27"] = 15.0 * (p_net_safe / P_NET_REF) ** 0.5

        # === CAS28: Digital Twin ===
        # Source: 1costingfe digital_twin = 5 M$
        r["CAS28"] = 5.0

        # === CAS29: Contingency ===
        # Source: 1costingfe contingency_rate_foak = 0.10, noak = 0.0
        cas20_sub = sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                        "CAS25", "CAS26", "CAS27", "CAS28"])
        r["CAS29"] = (0.0 if self.noak else 0.10) * cas20_sub

        # === CAS20: Total Direct Costs ===
        r["CAS20"] = cas20_sub + r["CAS29"]

        # === CAS30: Indirect Costs ===
        # Source: 1costingfe indirect_fraction=0.20, reference_construction_time=6
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / 6.0)

        # === CAS40: Owner's Costs ===
        # Source: 1costingfe owner_cost_dt = 39 M$ at 1 GWe, ^0.5 scaling
        r["CAS40"] = 39.0 * (p_net_safe / P_NET_REF) ** 0.5

        # === CAS50: Supplementary Costs ===
        # Tritium startup inventory (dominant for D-T)
        startup_fuel  = self.tritium_startup_M_ref * (p_net_safe / P_NET_REF) ** 0.5
        # Source: 1costingfe spare_parts_frac_dt = 0.03 (activated component spares)
        spare_parts   = 0.03 * sum(r[k] for k in ["CAS22", "CAS23", "CAS24",
                                                    "CAS25", "CAS26", "CAS27", "CAS28"])
        # Source: 1costingfe shipping_frac=0.015, tax_frac=0.01, insurance=0.015
        shipping      = 0.015 * r["CAS20"]
        taxes         = 0.010 * r["CAS20"]
        insurance     = 0.015 * (r["CAS20"] + r["CAS30"])
        # Source: 1costingfe decom_provision_dt = 127 M$ at 1 GWe, ^0.5 scaling
        decom         = 127.0 * (p_net_safe / P_NET_REF) ** 0.5
        r["CAS50"] = startup_fuel + spare_parts + shipping + taxes + insurance + decom

        # === Overnight Capital ===
        r["overnight_capital"] = (r["CAS10"] + r["CAS20"]
                                  + r["CAS30"] + r["CAS40"] + r["CAS50"])

        # === CAS60: Interest During Construction ===
        i = self.interest_rate
        T = self.construction_time_years
        f_idc = ((1 + i)**T - 1) / (i * T) - 1 if (i > 0 and T > 0) else 0.0
        r["f_IDC"] = f_idc
        r["CAS60"] = f_idc * r["overnight_capital"]

        # === Total Capital ===
        r["total_capital"] = r["overnight_capital"] + r["CAS60"]

        p_net_total = power["p_net"] * self.n_mod
        if p_net_total > 0:
            r["specific_capital_USD_per_kWe"] = (r["total_capital"] * 1e6
                                                   / (p_net_total * 1e3))
        else:
            r["specific_capital_USD_per_kWe"] = float('inf')

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70-90 annualized costs and LCOE."""
        r: dict = {}

        p_net_total = power["p_net"] * self.n_mod

        # Capital Recovery Factor
        i   = self.interest_rate
        n   = self.plant_lifetime_years
        crf = i * (1 + i)**n / ((1 + i)**n - 1)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]

        # === CAS71: Levelized Annual O&M ===
        annual_om_base = self.om_rate_fraction * costs["overnight_capital"]
        g  = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g)**Tc
        if abs(i - g) > 1e-10:
            pv_om = A1 * (1 - ((1 + g) / (1 + i))**n) / (i - g)
        else:
            pv_om = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_om

        # === CAS72: Scheduled Replacement (blanket / first wall) ===
        eff_yr_per_rep = self.core_lifetime_FPY / self.plant_availability
        n_rep = max(0, int(math.ceil(n / eff_yr_per_rep)) - 1)
        rep_cost = cas22["C220101"] * self.n_mod
        pv_rep = sum(
            rep_cost / (1 + i)**(k * eff_yr_per_rep)
            for k in range(1, n_rep + 1)
            if k * eff_yr_per_rep < n
        )
        r["CAS72"] = crf * pv_rep
        r["n_blanket_replacements"] = n_rep

        r["CAS70"] = r["CAS71"] + r["CAS72"]

        # === CAS80: Fuel & Consumables (D-T; ongoing T self-bred) ===
        # Deuterium consumption: 1 D atom per D-T fusion, M_D = 2 amu
        M_D_kg = 2 * AMU_KG
        seconds_per_year = 8760 * 3600 * self.plant_availability
        annual_D_kg = power["fusion_rate_per_s"] * M_D_kg * seconds_per_year
        r["CAS80"] = annual_D_kg * self.u_deuterium_per_kg / 1e6   # M$/yr
        r["CAS80_deuterium"] = r["CAS80"]

        # === LCOE ===
        ann_rev = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = ann_rev

        if p_net_total > 0:
            ann_energy_MWh = 8760 * p_net_total * self.plant_availability
            r["annual_energy_MWh"] = ann_energy_MWh
            lcoe = ann_rev * 1e6 / ann_energy_MWh
            r["lcoe_USD_per_MWh"]  = lcoe
            r["lcoe_cents_per_kWh"] = lcoe / 10.0
        else:
            r["annual_energy_MWh"]  = 0.0
            r["lcoe_USD_per_MWh"]   = float('inf')
            r["lcoe_cents_per_kWh"] = float('inf')

        if ann_rev > 0:
            r["capital_fraction"] = r["CAS90"] / ann_rev
            r["om_fraction"]      = r["CAS70"] / ann_rev
            r["fuel_fraction"]    = r["CAS80"] / ann_rev

        return r

    def compute(self) -> dict:
        """Compute CAS-structured LCOE from physics first principles.

        Returns dict with sub-dicts:
            power:     physics-derived power balance
            geometry:  chamber volumes
            cas22:     CAS22 sub-accounts
            costs:     CAS10–60 capital costs
            economics: CAS70–90 annualized costs + LCOE
        """
        power = self._compute_power()
        geom  = self._compute_geometry(power)
        cas22 = self._compute_cas22(power, geom)
        costs = self._compute_costs(power, cas22)
        econ  = self._compute_economics(power, costs, cas22)
        return {
            "power":     power,
            "geometry":  geom,
            "cas22":     cas22,
            "costs":     costs,
            "economics": econ,
        }


# ============================================================================
# Module-level interface for concept explorer
# ============================================================================
params  = MuCFPlantParams()
results = params.compute()

_ALPHA    = 0.6   # economy-of-scale exponent (standard cross-concept scaling)
_p_native = results["power"].get("p_net_plant", results["power"]["p_net"])

if _p_native > 0:
    _factor    = (_p_native / 1000.0) ** (1.0 - _ALPHA)
    _overnight = results["costs"]["overnight_capital"] * 1e3 / _p_native
    scaled_headline = {
        "p_net_mw":        1000.0,
        "lcoe_per_mwh":    results["economics"]["lcoe_USD_per_MWh"] * _factor,
        "overnight_per_kw": _overnight * _factor,
    }
else:
    # Energy sink at baseline parameters — scaled values are undefined
    scaled_headline = {
        "p_net_mw":        1000.0,
        "lcoe_per_mwh":    float('inf'),
        "overnight_per_kw": float('inf'),
    }


# ============================================================================
# Output functions
# ============================================================================

def print_results(p: MuCFPlantParams, r: dict) -> None:
    """Pretty-print the full LCOE model results with CAS-structured accounting."""
    pw    = r["power"]
    cas22 = r["cas22"]
    costs = r["costs"]
    econ  = r["economics"]

    print("=" * 72)
    print("Muon-Catalyzed Fusion (D-T) LCOE Model — Acceleron Fusion")
    print("1cFE CAS-Structured Free-Form Model")
    print("=" * 72)

    # Viability warning
    if pw["p_net"] <= 0:
        print()
        print("  *** ENERGY SINK: Net electric is NEGATIVE at these parameters. ***")
        print("  *** Q_sci × M × η_th < 1 + P_aux/P_beam — no net power output. ***")
        print("  *** LCOE is undefined. Accelerator consumes more than plant generates. ***")
        print()

    # --- Key Physics Inputs ---
    print(f"\n--- Key Physics Parameters ---")
    print(f"  Muon energy cost (E_mu):     {p.E_mu_elec_GeV:.1f} GeV_electrical/muon")
    print(f"  Fusions per muon (N_fus):    {p.n_fus_per_muon:.0f}")
    print(f"  Alpha-sticking ceiling:      {pw['n_fus_physics_ceiling']:.0f} fusions/muon (at {p.alpha_sticking_pct:.2f}% sticking)")
    if pw["ceiling_violated"]:
        print(f"  *** WARNING: N_fus > physics ceiling! ***")
    print(f"  Scientific Q (Q_sci):        {pw['Q_sci']:.3f}  (≥1 required for thermal gain)")
    print(f"  Gross/driver ratio:          {pw['gross_to_driver_ratio']:.3f}  (>1 required for any net power)")
    print(f"  Blanket multiplication M:    {p.M_blanket:.2f}")
    print(f"  Thermal efficiency η_th:     {p.eta_th:.1%}")
    print(f"  Accelerator beam power:      {p.acc_beam_power_MW:.0f} MW")
    print(f"  Plant availability:          {p.plant_availability:.0%}")
    print(f"  Modules:                     {p.n_mod}")

    # --- Power Balance ---
    print(f"\n--- Power Balance (per module) ---")
    print(f"  Muon rate:                   {pw['muon_rate_per_s']:.2e} muons/s")
    print(f"  Fusion rate:                 {pw['fusion_rate_per_s']:.2e} fusions/s")
    print(f"  Fusion power (P_fus):        {pw['p_fus']:>8.1f} MW")
    print(f"    Neutron power (80%):       {pw['p_neutron']:>8.1f} MW (14.1 MeV → blanket)")
    print(f"    Alpha power (20%):         {pw['p_alpha']:>8.1f} MW (3.5 MeV → local heat)")
    print(f"  Thermal power (P_th):        {pw['p_th']:>8.1f} MW  (× M={p.M_blanket})")
    print(f"  Gross electric (P_et):       {pw['p_et']:>8.1f} MWe (× η={p.eta_th:.1%})")
    print(f"  Recirculating power:")
    print(f"    Accelerator beam:          {p.acc_beam_power_MW:>8.1f} MW")
    print(f"    Auxiliaries (cryo+trit+house+ctrl): {pw['p_aux']:>5.1f} MW")
    print(f"    Total recirculating:       {pw['p_recirc']:>8.1f} MW")
    print(f"  Net electric (P_net):        {pw['p_net']:>8.1f} MWe ← {'NEGATIVE (energy sink)' if pw['p_net']<=0 else 'positive'}")
    print(f"  Plant net electric:          {pw['p_net_plant']:>8.1f} MWe")
    print(f"  Engineering Q (Q_eng):       {pw['Q_eng']:>8.3f}")
    print(f"  Recirculating fraction (ε):  {pw['recirc_fraction']:>8.1%}  "
          f"(Acceleron claims: 47%)")

    # --- CAS22 ---
    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    cas22_labels = {
        "C220101": ("Blanket + First Wall",    ""),
        "C220102": ("Shield (14 MeV neutrons)", ""),
        "C220103": ("Coils",                   "[ZERO — no confinement magnets]"),
        "C220104": ("Supplementary Heating",   "[ZERO — accelerator is driver]"),
        "C220105": ("Primary Structure",       ""),
        "C220106": ("Chamber Containment",     ""),
        "C220107": ("Accelerator System",      "[OVERRIDE — dominant cost]"),
        "C220108": ("Target Factory",          "[ZERO — continuous process]"),
        "C220110": ("Remote Handling",         ""),
        "C220111": ("Installation Labor",      ""),
    }
    for code, (label, note) in cas22_labels.items():
        val = cas22.get(code, 0.0)
        if val != 0.0 or note:
            print(f"    {code} {label:<32s} ${val:>8.1f}M  {note}")
    print(f"    {'─' * 58}")
    print(f"    Per-module subtotal:                    ${cas22['CAS22_per_module']:>8.1f}M × {p.n_mod}")

    pw_labels = {
        "C220200": "Coolant Systems (Brayton loops)",
        "C220300": "Aux Cooling + Cryoplant (SC linac)",
        "C220400": "Rad Waste Management",
        "C220500": "Tritium Fuel Handling & Storage",
        "C220600": "Other Equipment",
        "C220700": "I&C",
    }
    print(f"  Plant-wide accounts:")
    for code, label in pw_labels.items():
        val = cas22[code]
        if val > 0.01:
            print(f"    {code} {label:<36s} ${val:>8.1f}M")
    print(f"    {'─' * 58}")
    print(f"    Plant-wide subtotal:                    ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                              ${cas22['CAS22']:>8.1f}M")

    # --- Capital Costs ---
    print(f"\n--- Capital Costs (CAS10–60) ---")
    print(f"  CAS10 Pre-construction:                   ${costs['CAS10']:>8.1f}M")
    print(f"  CAS21 Buildings (×{p.regulatory_multiplier:.1f}× reg. mult.):      ${costs['CAS21']:>8.1f}M")
    print(f"  CAS22 Reactor Plant Equipment:            ${costs['CAS22']:>8.1f}M")
    print(f"  CAS23 Turbine Plant (Brayton):            ${costs['CAS23']:>8.1f}M")
    print(f"  CAS24 Electric Plant:                     ${costs['CAS24']:>8.1f}M")
    print(f"  CAS25 Misc Plant:                         ${costs['CAS25']:>8.1f}M")
    print(f"  CAS26 Heat Rejection:                     ${costs['CAS26']:>8.1f}M")
    print(f"  CAS27 Special Materials (Li-6 + T):       ${costs['CAS27']:>8.1f}M")
    print(f"  CAS28 Digital Twin:                       ${costs['CAS28']:>8.1f}M")
    print(f"  CAS29 Contingency:                        ${costs['CAS29']:>8.1f}M")
    print(f"  {'─' * 60}")
    print(f"  CAS20 Direct Costs:                       ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30 Indirect Costs:                     ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40 Owner's Costs:                      ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50 Supplementary (incl. T startup):    ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 60}")
    print(f"  Overnight Capital:                        ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60 IDC (f={costs['f_IDC']:.3f}):                ${costs['CAS60']:>8.1f}M")
    print(f"  {'═' * 60}")
    print(f"  Total Capital:                            ${costs['total_capital']:>8.1f}M")
    if pw["p_net"] > 0:
        print(f"  Specific Capital:                   ${costs['specific_capital_USD_per_kWe']:>10,.0f} $/kWe")
        print(f"  (Fission NOAK reference:              ~$7,000–10,000 $/kWe)")

    # --- Annual Costs ---
    print(f"\n--- Annual Costs (CAS70–90) ---")
    print(f"  CAS90 Capital charge (CRF={econ['CRF']:.4f}):    ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71 O&M (levelized, {p.om_rate_fraction:.1%}/yr):     ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72 Blanket replacements ({econ['n_blanket_replacements']} over life): ${econ['CAS72']:>8.1f}M/yr")
    print(f"  CAS70 Total O&M:                          ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80 Fuel (deuterium, T self-bred):      ${econ['CAS80']:>8.4f}M/yr")

    # --- LCOE ---
    print(f"\n--- LCOE ---")
    if pw["p_net"] > 0:
        print(f"  Annual energy production:     {econ['annual_energy_MWh']:>12,.0f} MWh/yr")
        print(f"  Annual revenue requirement:   ${econ['annual_revenue_req']:>8.1f}M/yr")
        print(f"  ╔══════════════════════════════════════════════════╗")
        print(f"  ║  LCOE = {econ['lcoe_cents_per_kWh']:>7.1f} ¢/kWh                          ║")
        print(f"  ║       = {econ['lcoe_USD_per_MWh']:>7.1f} $/MWh                         ║")
        print(f"  ║  Acceleron target: 2.5 ¢/kWh ($25/MWh)          ║")
        print(f"  ║  Gap vs. target:   {econ['lcoe_cents_per_kWh']/2.5:>6.1f}×                          ║")
        print(f"  ╚══════════════════════════════════════════════════╝")
        print(f"  Capital (CAS90):             {econ.get('capital_fraction', 0):.1%}")
        print(f"  O&M    (CAS70):              {econ.get('om_fraction', 0):.1%}")
        print(f"  Fuel   (CAS80):              {econ.get('fuel_fraction', 0):.2%}")

        if _p_native > 0:
            _f = (_p_native / 1000.0) ** (1.0 - _ALPHA)
            print(f"\n--- Scaled to 1000 MWe Reference (α=0.6) ---")
            print(f"  Scale factor:    ({_p_native:.0f}/1000)^{1-_ALPHA:.1f} = {_f:.3f}")
            print(f"  Scaled LCOE:     {econ['lcoe_USD_per_MWh'] * _f:.1f} $/MWh"
                  f"  ({econ['lcoe_cents_per_kWh'] * _f:.2f} ¢/kWh)")
    else:
        print(f"  LCOE: UNDEFINED — net electric is negative.")
        print(f"  Plant is an energy sink. LCOE is infinite.")
        print(f"  Required: Q_sci × M × η > 1 + P_aux/P_beam")
        q_need = (1.0 + p.p_aux / p.acc_beam_power_MW if p.acc_beam_power_MW > 0 else 2.0)
        n_need = q_need * p.E_mu_elec_GeV * 1000.0 / E_FUSION_MEV
        print(f"  At E_mu={p.E_mu_elec_GeV:.1f} GeV, need N_fus ≥ {n_need:.0f} fusions/muon")
        print(f"  (Physics ceiling at {p.alpha_sticking_pct:.2f}% sticking: {pw['n_fus_physics_ceiling']:.0f})")


def sensitivity_sweep(base_params: MuCFPlantParams,
                      param_name: str,
                      values: list,
                      label: str = "") -> list[dict]:
    """Sweep a single parameter and return LCOE and net power for each value."""
    out = []
    for val in values:
        p = MuCFPlantParams(**{**base_params.__dict__, param_name: val})
        r = p.compute()
        pw = r["power"]
        out.append({
            "param_value":    float(val),
            "lcoe_cents_kWh": r["economics"]["lcoe_cents_per_kWh"],
            "lcoe_USD_MWh":   r["economics"]["lcoe_USD_per_MWh"],
            "net_electric_MW": pw["p_net"],
            "Q_sci":          pw["Q_sci"],
            "recirc_fraction": pw["recirc_fraction"],
        })
    return out


def _print_sweep(sweep_results: list[dict], label: str,
                 param_unit: str = "") -> None:
    """Print a sensitivity sweep table."""
    print(f"\n  {label}:")
    print(f"  {'Value':>12}  {'Q_sci':>7}  {'P_net':>8}  {'ε':>6}  {'LCOE':>14}")
    print(f"  {'─'*12}  {'─'*7}  {'─'*8}  {'─'*6}  {'─'*14}")
    for row in sweep_results:
        v    = row["param_value"]
        q    = row["Q_sci"]
        pn   = row["net_electric_MW"]
        eps  = row["recirc_fraction"]
        lcoe = row["lcoe_cents_kWh"]
        if pn <= 0:
            lcoe_str = "SINK (neg)"
            eps_str  = " >100%"
        elif lcoe == float('inf'):
            lcoe_str = "     inf"
            eps_str  = f"{eps:>5.0%}"
        else:
            lcoe_str = f"{lcoe:>7.1f} ¢/kWh"
            eps_str  = f"{eps:>5.0%}"
        print(f"  {v:>10.3g}{param_unit}  {q:>7.3f}  {pn:>7.1f}MW  "
              f"{eps_str}  {lcoe_str}")


def main() -> None:
    # =========================================================================
    # BASELINE SCENARIO
    # =========================================================================
    print("\n" + "#" * 72)
    print("# μCF BASELINE: Aspirational Breakthrough (E_mu=1.2 GeV, N_fus=240)")
    print("# NOTE: Requires ~2× improvement beyond Acceleron's 2.5 GeV target.")
    print("# Even at this aspirational level, LCOE >> Acceleron's $0.025/kWh target.")
    print("#" * 72)

    baseline = MuCFPlantParams()
    base_r   = baseline.compute()
    print_results(baseline, base_r)

    # =========================================================================
    # SENSITIVITY SWEEPS
    # =========================================================================
    print("\n" + "=" * 72)
    print("SENSITIVITY ANALYSIS — Single-Parameter Sweeps from Baseline")
    print("=" * 72)
    print("  Baseline LCOE:", end=" ")
    bl = base_r["economics"]["lcoe_cents_per_kWh"]
    print(f"{bl:.1f} ¢/kWh" if bl < 1e6 else "SINK")
    print()

    # 1. Muon energy cost (the most important physics parameter)
    sw1 = sensitivity_sweep(
        baseline, "E_mu_elec_GeV",
        [0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 6.0],
    )
    _print_sweep(sw1, "Muon energy cost E_mu [GeV_electrical/muon] (↓ better)", " GeV")

    # 2. Fusions per muon (physics-ceiling constrained)
    sw2 = sensitivity_sweep(
        baseline, "n_fus_per_muon",
        [100, 150, 200, 240, 280, 320, 400],
    )
    _print_sweep(sw2, "Fusions per muon N_fus (↑ better, ceiling ~250 at 0.4% sticking)", "")

    # 3. Accelerator capital cost (dominant financial uncertainty)
    sw3 = sensitivity_sweep(
        baseline, "acc_capital_M",
        [200, 500, 1000, 2000, 4000, 8000],
    )
    _print_sweep(sw3, "Accelerator capital cost [$M] (↓ better)", " M$")

    # 4. Thermal efficiency
    sw4 = sensitivity_sweep(
        baseline, "eta_th",
        [0.35, 0.40, 0.45, 0.50, 0.55, 0.60],
    )
    _print_sweep(sw4, "Thermal efficiency η_th [fraction] (↑ better)", "")

    # 5. Accelerator beam power (scales both recirc and output)
    sw5 = sensitivity_sweep(
        baseline, "acc_beam_power_MW",
        [50, 75, 100, 150, 200, 300],
    )
    _print_sweep(sw5, "Accelerator beam power P_beam [MW] (sets plant scale)", " MW")

    # =========================================================================
    # SCENARIO COMPARISON TABLE
    # =========================================================================
    print("\n\n" + "=" * 72)
    print("SCENARIO COMPARISON")
    print("=" * 72)
    print(f"{'Scenario':<28} {'E_mu':>7} {'N_fus':>6} {'Q_sci':>7} "
          f"{'P_net':>8} {'ε':>6} {'LCOE':>14}")
    print("-" * 78)

    scenarios = {
        "Current physics (LAMPF)": MuCFPlantParams(
            E_mu_elec_GeV=6.0,
            n_fus_per_muon=150,
            alpha_sticking_pct=1.0,   # Jackson 1957 estimate
            acc_beam_power_MW=100,
        ),
        "Acceleron target": MuCFPlantParams(
            E_mu_elec_GeV=2.5,
            n_fus_per_muon=200,
            alpha_sticking_pct=0.4,
            acc_beam_power_MW=100,
        ),
        "Acceleron stretch target": MuCFPlantParams(
            E_mu_elec_GeV=2.5,
            n_fus_per_muon=300,        # Near physics ceiling at 0.35% sticking
            alpha_sticking_pct=0.33,   # 0.33% gives ceiling ~303
            acc_beam_power_MW=100,
        ),
        "Baseline (breakthrough)": MuCFPlantParams(),   # 1.2 GeV, 240 fusions
        "Optimistic breakthrough": MuCFPlantParams(
            E_mu_elec_GeV=0.8,
            n_fus_per_muon=240,
            alpha_sticking_pct=0.4,
            acc_beam_power_MW=100,
            acc_capital_M=1000.0,     # ~2× cheaper accelerator at this lower energy
            eta_th=0.52,
        ),
    }

    for name, sc_params in scenarios.items():
        sc_r  = sc_params.compute()
        pw    = sc_r["power"]
        econ  = sc_r["economics"]
        q     = pw["Q_sci"]
        pn    = pw["p_net"]
        eps   = pw["recirc_fraction"]
        lcoe  = econ["lcoe_cents_per_kWh"]

        if pn <= 0:
            lcoe_str = "     SINK"
            eps_str  = " >100%"
        elif lcoe >= 1e6:
            lcoe_str = "   inf  "
            eps_str  = f"{eps:5.0%}"
        else:
            lcoe_str = f"{lcoe:7.1f} ¢/kWh"
            eps_str  = f"{eps:5.0%}"

        print(f"{name:<28} {sc_params.E_mu_elec_GeV:>5.1f}G {sc_params.n_fus_per_muon:>6.0f} "
              f"{q:>7.3f} {pn:>7.1f}MW {eps_str}  {lcoe_str}")

    # =========================================================================
    # KEY BINDING CONSTRAINTS
    # =========================================================================
    print("\n\n" + "=" * 72)
    print("KEY BINDING CONSTRAINTS (in order of LCOE impact)")
    print("=" * 72)

    print("""
  1. ENERGY BALANCE — THE FUNDAMENTAL VIABILITY GATE

     Commercial μCF requires: Q_sci × M_blanket × η_th > 1 + P_aux/P_beam

     At Acceleron's stated targets (E_mu=2.5 GeV, N_fus=200):
       Q_sci = 200 × 17.6 MeV / 2500 MeV = 1.41
       Gross/driver = 1.41 × 1.10 × 0.50 = 0.78  → ENERGY SINK

     The Kelly, Hart & Rose (2021) estimate (150 fusions/muon, 18% acc eff,
     60% thermal conversion) found only 14% net-to-input ratio. Even at
     Acceleron's targets the concept produces net negative electricity.

     What Acceleron needs (for 47% recirc with η_th=0.50, M=1.10):
       Q_sci ≥ 1/(0.47 × 1.10 × 0.50) = 3.87 → N_fus ≥ 550 at 2.5 GeV
       OR: E_mu ≤ 0.8 GeV at N_fus = 240 (this model's baseline requires 1.2 GeV)

     STATUS: Not demonstrated. No experimental result approaches this threshold.
     Resolution: Brookhaven National Laboratory breakeven test (~2030 target).

  2. ACCELERATOR CAPITAL COST — DOMINANT LCOE COMPONENT

     At baseline (E_mu=1.2 GeV, N_fus=240, P_beam=100 MW, P_net≈70 MWe):
       Accelerator: $2,000M of ~$3,100M overnight capital (65%)
       Specific capital: ~$44,000+/kWe (vs. fission NOAK ~$7,000–10,000/kWe)

     SNS (ORNL, 1 GeV, 1.4 MW beam): $1,400M → $1B/MW_beam
     Commercial target would need $<50M/MW_beam — a 20× cost reduction.
     This requires industrial-scale manufacturing never achieved for GeV linacs.

     To hit $25/MWh at 70 MWe with current physics: acc_capital ≤ ~$50M
     (current estimate: $2,000M → 40× gap in accelerator cost alone)

     STATUS: No published cost model for the MCF-relevant accelerator regime.
     Resolution: Acceleron's active-target design may reduce cost vs. science-
     grade linacs, but magnitude of reduction is completely unknown.

  3. ALPHA-STICKING PHYSICS CEILING — HARD LIMIT ON N_FUS

     Fusions per muon is bounded by alpha-sticking probability:
       Max N_fus = 100 / α_sticking
       At α = 0.4% (recent measurements): max N_fus ≈ 250
       At α = 0.3% (optimistic): max N_fus ≈ 333

     Acceleron's 300 fusions/muon target requires α < 0.33%, at the edge
     of experimental measurements. This is a quantum mechanical limit, not
     an engineering design variable. Sticking probability cannot be improved
     by reactor design — it is set by D-T fusion kinematics.

     Combined constraints 1–3 define a narrow operating window that may
     require simultaneous achievement of: E_mu ≤ 1.5 GeV (undemonstrated),
     N_fus ≥ 250 (near physics ceiling), and accelerator cost <$200M/GW.
""")

    print("NOTE: All estimates carry VERY HIGH UNCERTAINTY. This model is intended")
    print("for first-pass corridor mapping only. The dominant uncertainty is the")
    print("physics energy balance — the concept may not be commercially viable at")
    print("any capital cost if the fundamental Q_sci constraint cannot be met.")
    print("Cost accounts follow 1costingfe CAS structure with concept-specific overrides.")
    print("Accelerator costs use particle-physics facility analogues — highly speculative.")


if __name__ == "__main__":
    main()
