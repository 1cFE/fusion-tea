"""
Laser ICF Liquid-Jet Target (Cortex Fusion Systems) First-Pass LCOE Model
==========================================================================
1cFE First Pass Concept Analysis
Concept: Laser ICF Liquid-Jet Target — Plasmonic Nanoshell D-D Fusion
Company: Cortex Fusion Systems

This is a parameterized LCOE model for the "Nano-Sun" 1 MHz reactor scenario
from arXiv:2503.15531 (Kharzeev, Levitt, Trallero-Herrero, 2025). It computes
CAS-structured costs from first principles at the concept's native power scale
(~0.3 MWe).

╔═══════════════════════════════════════════════════════════════════════════════╗
║ CRITICAL: THIS IS NOT A CREDIBLE COST ESTIMATE                               ║
║                                                                               ║
║ The concept's core physics mechanism (plasmonic confinement of deuterons      ║
║ inside gold nanoshells) is UNVALIDATED. Zero fusion neutrons have been        ║
║ reported from this mechanism by any group. The claimed fusion rate (10^7/s    ║
║ per nanoshell) and Q factor (~100) rest on a single theoretical preprint      ║
║ with acknowledged gaps (ionization damping, deuteron escape).                 ║
║                                                                               ║
║ BLOCKING ISSUES:                                                              ║
║ • Physics mechanism unvalidated — zero experimental fusion events             ║
║ • No energy conversion system designed or proposed                            ║
║ • No reactor chamber, blanket, or shielding design                            ║
║ • Native power (0.3 MWe) is 3,000× below commercial scale                   ║
║ • Gold nanoshell manufacturing at 10^12/s does not exist                     ║
║                                                                               ║
║ This model exists ONLY for cross-concept comparison corridor purposes.        ║
║ All cost parameters are ASSUMED — the paper provides zero cost data.          ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Key references:
    arXiv:2503.15531 — Kharzeev, Levitt, Trallero-Herrero (2025),
    "Fusion in a Nanoshell: Harnessing Plasmonic Fields for Nuclear Reactions"
    [iter-01/sources/arxiv-2503-nanoshell-paper.md]

    Knight et al. (Cambridge, 2024), "Detailed Characterization of kHz-rate
    Laser-Driven Fusion at a Thin Liquid Sheet"
    [iter-01/sources/kHz-liquid-sheet-fusion-paper.md]

    1costingfe costing_constants.yaml — CAS scaling laws and unit costs
    [~/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml]

    analysis.md — Phase D1+ analysis with quantitative parameters
    [analyses/03-laser-icf-liquid-jet-target/analysis.md]

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass

# ============================================================================
# Physical constants
# ============================================================================
E_FUSION_DD_T_MEV = 4.03           # D-D → T + p fusion energy [MeV]
E_FUSION_DD_He3_MEV = 3.27         # D-D → He-3 + n fusion energy [MeV]
E_FUSION_DD_AVG_MEV = (E_FUSION_DD_T_MEV + E_FUSION_DD_He3_MEV) / 2.0  # ~3.65 MeV
E_FUSION_J = E_FUSION_DD_AVG_MEV * 1e6 * 1.602e-19  # Average D-D energy [J]
AMU_KG = 1.66053906660e-27         # 1 atomic mass unit [kg]
GOLD_DENSITY_KG_M3 = 19300.0       # Gold density [kg/m³]

# ============================================================================
# Reference power levels for 1costingfe scaling laws
# ============================================================================
P_TH_REF = 2500.0   # Reference thermal power [MW]
P_ET_REF = 1100.0    # Reference gross electric power [MW]
P_NET_REF = 1000.0   # Reference net electric power [MW]


@dataclass
class CortexFusionPlantParams:
    """
    Parameterized Laser ICF Liquid-Jet Target (Cortex Fusion) power plant model.

    Architecture overview (SPECULATIVE — no engineering design exists):
    ┌──────────────────────────────────────────────────────────────────┐
    │  Femtosecond laser (1 MHz, ~3 kW avg) → gold nanoshell colloid  │
    │       ↓                                                          │
    │  Plasmonic field enhancement (~100×) → deuteron acceleration     │
    │       ↓ [PHYSICS UNVALIDATED — zero fusion events demonstrated]  │
    │  [THEORETICAL] D-D fusion → 2.45 MeV neutrons + charged         │
    │       ↓                                                          │
    │  Neutrons → [UNDESIGNED blanket] → thermal energy               │
    │  Charged → local colloid heating → thermal energy                │
    │       ↓                                                          │
    │  [UNSPECIFIED thermal cycle] → gross electric                    │
    │       ↓                                                          │
    │  Net electric = Gross - Recirculating (laser + aux)              │
    └──────────────────────────────────────────────────────────────────┘

    Key structural differences from 1costingfe standard models:
    • C220103 (Coils):          ZERO — no magnetic confinement
    • C220104 (Heating):        ZERO — laser IS the driver
    • C220107 (Power Supplies): OVERRIDE — femtosecond laser capital
    • C220108 (Target Factory): OVERRIDE — nanoshell colloid preparation system

    Uncertainty tiers used in docstrings:
    • (no tag)             — well-established physics or engineering constant
    • MODERATE UNCERTAINTY — reasonable estimate from documented analogues
    • HIGH UNCERTAINTY     — speculative or poorly constrained
    • EXTREME UNCERTAINTY  — pure speculation, no credible basis
    • PHYSICS UNVALIDATED  — fundamental mechanism not demonstrated
    """

    # =========================================================================
    # LASER DRIVER
    # =========================================================================

    laser_avg_power_kW: float = 3.0
    """Average laser power [kW].
    Derived from rep rate × energy per pulse. The paper states P_laser ~ 3 kW.
    Source: arxiv-2503-nanoshell-paper.md §Released energy, Eq. 16.
    Ref: analysis.md §S5 (Laser average power).
    MODERATE UNCERTAINTY — value is self-consistent within the paper."""

    laser_rep_rate_MHz: float = 1.0
    """Laser repetition rate [MHz].
    Source: arxiv-2503-nanoshell-paper.md §Released energy, "laser repetition
    frequency of f = 1 MHz."
    Ref: analysis.md §S5.
    HIGH UNCERTAINTY — current commercial Yb lasers reach "hundreds of kHz";
    1 MHz at required intensity is beyond demonstrated capability."""

    laser_pulse_energy_mJ: float = 3.0
    """Laser energy per pulse [mJ]. Derived: P_laser / f = 3 kW / 1 MHz = 3 mJ.
    Source: analysis.md §S5 (inferred, not stated directly in paper).
    HIGH UNCERTAINTY — derived quantity."""

    laser_wallplug_efficiency: float = 0.30
    """Laser wall-plug efficiency [fraction].
    Industrial femtosecond Yb fiber lasers: 20-30% wall-plug efficiency.
    Source: ASSUMED from commercial laser specifications.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # NANOSHELL TARGET PHYSICS (UNVALIDATED)
    # =========================================================================

    nanoshells_per_pulse: float = 1.0e6
    """Number of gold nanoshells irradiated per laser pulse.
    Source: arxiv-2503-nanoshell-paper.md §Released energy, "N_s-p = 10^6".
    Ref: analysis.md §S5.
    HIGH UNCERTAINTY — assumed, not derived from laser focus geometry."""

    fusion_rate_per_shell_per_s: float = 1.0e7
    """Fusion reactions per nanoshell per second of irradiation [s^-1].
    This is the core physics claim. Theoretical estimate with major caveats:
    ionization damping not modeled, deuteron escape unquantified.
    Source: arxiv-2503-nanoshell-paper.md §Fusion probability, Eq. 11.
    Ref: analysis.md §S5.
    PHYSICS UNVALIDATED — zero fusions demonstrated from this mechanism."""

    fusion_power_MW: float = 1.0
    """Total fusion power [MW]. Paper states "P_fusion ~ 1 MW".
    Source: arxiv-2503-nanoshell-paper.md §Released energy, Eq. 14.
    Ref: analysis.md §S5.
    PHYSICS UNVALIDATED — depends on all nanoshell physics claims being correct."""

    # =========================================================================
    # ENERGY CAPTURE (NO SYSTEM DESIGNED)
    # =========================================================================

    kappa: float = 0.30
    """Thermal-to-electric conversion efficiency [fraction].
    The paper assumes κ ≈ 30% "conversion efficiency of γ quanta and neutron
    energy into electric power" without specifying ANY mechanism.
    D-D fusion from colloidal nanoshell suspension: no standard energy
    conversion pathway exists. Neutrons emitted isotropically from liquid
    colloid; how ~1 MW of mostly 2.45 MeV neutrons would be captured is
    completely unaddressed.
    Source: arxiv-2503-nanoshell-paper.md §Released energy, Eq. 16.
    Ref: analysis.md §S2 (Challenge 2: No energy conversion system).
    EXTREME UNCERTAINTY — no mechanism specified. 30% is paper's assumption."""

    M_blanket: float = 1.0
    """Blanket energy multiplication factor [dimensionless].
    D-D fusion: no breeding blanket needed (no tritium). Neutron energy
    captured in surrounding medium. M ≈ 1.0 (no exothermic breeding reactions).
    Source: ASSUMED — standard D-D assumption.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # PLANT CONFIGURATION
    # =========================================================================

    n_mod: int = 1
    """Number of fusion modules per plant.
    Single-module design at paper's native scale.
    Source: ASSUMED — paper describes one laser-colloid system."""

    plant_availability: float = 0.75
    """Plant capacity factor / availability [fraction].
    Lower than standard (85%) due to:
    - Extreme technology immaturity (TRL 1-2 for physics)
    - Unknown degradation of laser optics at MHz operation
    - Unknown gold nanoshell throughput reliability
    - No operational experience of any kind
    Source: ASSUMED.
    HIGH UNCERTAINTY."""

    plant_lifetime_years: float = 40.0
    """Plant economic lifetime [years].
    Source: 1costingfe default. Standard fusion plant assumption."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds 10% contingency on direct costs.
    Source: 1costingfe CAS29 convention."""

    # =========================================================================
    # CAPITAL — LASER SYSTEM (C220107 OVERRIDE)
    # =========================================================================

    laser_capital_M: float = 1.0
    """Capital cost of femtosecond laser system [$M].
    Maps to C220107 (Power Supplies) — CONCEPT OVERRIDE.
    A 3 kW average power femtosecond Yb-based laser system is within
    the range of current industrial systems. Analysis estimates $0.1M-$1M.
    Baseline uses upper end ($1M) given MHz rep-rate requirement.
    This is NEGLIGIBLE compared to other fusion concept driver costs
    ($2B+ for NIF-class, $1B+ for ITER-class magnets).
    Source: analysis.md §S4 (Femtosecond Laser Components).
    MODERATE UNCERTAINTY — commercial technology at lower rep rates."""

    # =========================================================================
    # CAPITAL — NANOSHELL TARGET SYSTEM (C220108 OVERRIDE)
    # =========================================================================

    nanoshell_factory_capital_M: float = 20.0
    """Capital cost of gold nanoshell manufacturing + delivery system [$M].
    Maps to C220108 (Target Factory) — CONCEPT OVERRIDE.
    No production system exists at the required 10^12 shells/second throughput.
    Current synthesis is laboratory batch process (μg-mg quantities).
    Cost is pure speculation. $20M assumes a scaled-up chemical synthesis
    plant with colloid delivery system.
    Source: ASSUMED — no manufacturing design or cost data exists.
    EXTREME UNCERTAINTY — could be $5M-$500M+ depending on process."""

    # =========================================================================
    # CHAMBER & GEOMETRY
    # =========================================================================

    chamber_inner_radius_m: float = 0.30
    """Inner radius of reaction chamber [m].
    Very small compared to other fusion concepts — the reaction occurs
    in a colloidal suspension, not a large plasma chamber.
    No chamber design exists. Size set by liquid jet/sheet target geometry.
    Source: ASSUMED — rough scale for liquid-jet target interaction region.
    HIGH UNCERTAINTY."""

    blanket_thickness_m: float = 0.40
    """Neutron-capturing blanket thickness [m].
    D-D 2.45 MeV neutrons require less shielding than D-T 14.1 MeV.
    The liquid D2O colloid itself provides some moderation.
    No blanket design exists for this concept.
    Source: ASSUMED.
    HIGH UNCERTAINTY."""

    shield_thickness_m: float = 0.30
    """Neutron shielding thickness [m].
    D-D neutrons (2.45 MeV) — less penetrating than D-T, but still
    require biological shielding.
    Source: ASSUMED — reduced from D-T requirements.
    MODERATE UNCERTAINTY."""

    structure_thickness_m: float = 0.15
    """Primary structure thickness [m].
    Source: ASSUMED — compact chamber.
    MODERATE UNCERTAINTY."""

    vessel_thickness_m: float = 0.05
    """Chamber vessel thickness [m].
    Non-vacuum system — liquid colloid environment. Modest pressure vessel.
    Source: ASSUMED.
    MODERATE UNCERTAINTY."""

    blanket_unit_cost: float = 0.15
    """Active region / blanket unit cost [M$/m³].
    D-D: no breeding blanket. Simple neutron-absorbing region with thermal
    management. Cheaper than solid D-T blanket (1costingfe: 0.60 M$/m³)
    but more complex than pure water (needs gold recovery, colloid handling).
    Source: ASSUMED — between water (cheap) and D-D blanket (0.30).
    HIGH UNCERTAINTY."""

    # =========================================================================
    # AUXILIARY POWER
    # =========================================================================

    p_colloid_handling_MW: float = 0.002
    """Colloid circulation and gold recovery power [MW].
    Pumping colloidal suspension through target region, gold recovery,
    D2O recycling. Very low power at this tiny scale.
    Source: ASSUMED.
    HIGH UNCERTAINTY."""

    p_house_MW: float = 0.005
    """Housekeeping / facility power [MW].
    Very small plant — minimal housekeeping load.
    Source: ASSUMED.
    HIGH UNCERTAINTY."""

    p_controls_MW: float = 0.001
    """Laser control, diagnostics, and monitoring power [MW].
    Source: ASSUMED.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # CONSUMABLES — GOLD NANOSHELLS
    # =========================================================================

    nanoshell_outer_radius_nm: float = 100.0
    """Nanoshell outer radius [nm].
    Source: arxiv-2503-nanoshell-paper.md §Equation of motion, "R ~ O(100) nm".
    Ref: analysis.md §S5.
    MODERATE UNCERTAINTY — order-of-magnitude estimate from paper."""

    nanoshell_inner_radius_nm: float = 80.0
    """Nanoshell inner radius [nm] (D2O-filled core).
    Shell thickness must be less than electromagnetic skin depth.
    ~20 nm shell thickness assumed.
    Source: ASSUMED — analysis.md §S4 estimates ~20 nm shell thickness.
    HIGH UNCERTAINTY — paper does not specify shell thickness precisely."""

    gold_price_per_kg: float = 60000.0
    """Gold price [$/kg]. Approximate 2024 market price.
    Source: analysis.md §S4, market data.
    MODERATE UNCERTAINTY — gold price fluctuates but well-bounded."""

    nanoshell_survival_fraction: float = 0.0
    """Fraction of nanoshells surviving laser irradiation [0-1].
    Whether nanoshells survive intense plasmonic excitation or are destroyed
    each pulse is UNKNOWN. Baseline assumes complete destruction (worst case).
    Source: ASSUMED — analysis.md §S4, §S2 (Challenge 4).
    EXTREME UNCERTAINTY — could be 0% or near-100%, completely unknown."""

    # =========================================================================
    # FUEL COSTS (D2O)
    # =========================================================================

    d2o_cost_per_kg: float = 600.0
    """Heavy water (D2O) cost [$/kg].
    Industrial commodity: $500-700/kg depending on purity.
    Source: analysis.md §S4 (Heavy Water).
    MODERATE UNCERTAINTY — well-characterized market."""

    # =========================================================================
    # FINANCIAL
    # =========================================================================

    interest_rate: float = 0.08
    """Real discount rate / WACC [fraction].
    Source: 1costingfe interest_rate default."""

    inflation_rate: float = 0.02
    """Inflation rate for O&M levelization [fraction].
    Source: 1costingfe default."""

    construction_time_years: float = 3.0
    """Construction period [years].
    Very short — the concept is extremely small (0.3 MWe), uses no large
    structural components (no magnets, no large vacuum vessels).
    Source: ASSUMED — tiny facility, no complex assembly.
    MODERATE UNCERTAINTY."""

    om_rate_fraction: float = 0.025
    """Annual O&M as fraction of overnight capital.
    Source: ASSUMED — midpoint of typical range.
    MODERATE UNCERTAINTY."""

    core_lifetime_FPY: float = 10.0
    """Active region / first-wall lifetime [full-power-years before replacement].
    D-D 2.45 MeV neutrons: less damage than D-T. But at ~1 MW fusion,
    the neutron flux is very low, extending component lifetimes.
    Source: 1costingfe costing_constants.yaml core_lifetime_dd.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # REGULATORY
    # =========================================================================

    regulatory_multiplier: float = 1.2
    """Building cost multiplier for D-D nuclear facility regulatory overhead.
    D-D avoids tritium: simpler regulatory environment than D-T.
    Very low neutron flux (~1 MW fusion) → minimal activation.
    Source: ASSUMED — analysis.md §S4 (No Tritium, No Exotic Materials).
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # COMPUTE METHODS
    # =========================================================================

    def _compute_power(self) -> dict:
        """Layer 1: Physics-based power balance from paper parameters.

        Energy flow:
          Laser power [P_laser = 3 kW] → nanoshell plasmonic enhancement
          → D-D fusion power [P_fus = 1 MW] → thermal [P_th]
          → gross electric [P_et] → net electric [P_net] = P_et - P_recirc
        """
        r: dict = {}

        # --- Laser electrical power ---
        # Wall-plug power required to run the laser
        p_laser_MW = self.laser_avg_power_kW / 1000.0  # 0.003 MW
        p_laser_elec_MW = p_laser_MW / self.laser_wallplug_efficiency
        r["p_laser_MW"] = p_laser_MW
        r["p_laser_elec_MW"] = p_laser_elec_MW

        # --- Fusion power (THEORETICAL — UNVALIDATED) ---
        p_fus = self.fusion_power_MW
        r["p_fus"] = p_fus

        # Scientific Q: fusion power / laser optical power
        Q_sci = p_fus / p_laser_MW if p_laser_MW > 0 else 0.0
        r["Q_sci"] = Q_sci

        # Engineering Q: fusion power / total recirculating
        # (computed after aux power below)

        # Neutron flux
        # Paper: F ~ 10^19 n/s
        neutron_rate = p_fus * 1e6 / E_FUSION_J  # fusions/s
        r["neutron_rate_per_s"] = neutron_rate

        # D-D energy partition: ~50% neutrons (2.45 MeV), ~50% charged (p, T, He-3)
        r["p_neutron"] = p_fus * 0.50
        r["p_charged"] = p_fus * 0.50

        # --- Thermal power ---
        p_th = p_fus * self.M_blanket
        r["p_th"] = p_th

        # --- Gross electric ---
        p_et = p_th * self.kappa
        r["p_et"] = p_et

        # --- Recirculating power ---
        p_aux = (self.p_colloid_handling_MW + self.p_house_MW
                 + self.p_controls_MW)
        r["p_aux"] = p_aux
        p_recirc = p_laser_elec_MW + p_aux
        r["p_recirc"] = p_recirc

        # --- Net electric ---
        p_net = p_et - p_recirc
        r["p_net"] = p_net

        # Multi-module plant totals
        r["p_net_plant"] = p_net * self.n_mod
        r["p_et_plant"] = p_et * self.n_mod
        r["p_th_plant"] = p_th * self.n_mod

        # --- Figures of merit ---
        r["Q_eng"] = p_fus / p_recirc if p_recirc > 0 else float('inf')
        r["recirc_fraction"] = p_recirc / p_et if p_et > 0 else float('inf')

        # Paper's Q factor definition (Q = P_fusion × κ / P_laser ≈ 100)
        r["Q_paper"] = (p_fus * self.kappa) / p_laser_MW if p_laser_MW > 0 else 0.0

        # Demonstrated vs. claimed yield gap
        r["demonstrated_neutron_rate"] = 1.0e5    # Cambridge: ~10^5 n/s
        r["claimed_neutron_rate"] = 1.0e19         # Paper: ~10^19 n/s
        r["yield_gap_orders"] = 14                 # 14 orders of magnitude

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Chamber geometry volumes using spherical shells.
        Spherical geometry for compact liquid-jet target chamber."""
        r: dict = {}

        ri = self.chamber_inner_radius_m

        def sphere_shell_vol(r_in: float, thickness: float) -> float:
            r_out = r_in + thickness
            return (4.0 / 3.0) * math.pi * (r_out**3 - r_in**3)

        r_b = ri + self.blanket_thickness_m
        r["blanket_vol_m3"] = sphere_shell_vol(ri, self.blanket_thickness_m)

        r_s = r_b + self.shield_thickness_m
        r["shield_vol_m3"] = sphere_shell_vol(r_b, self.shield_thickness_m)

        r_st = r_s + self.structure_thickness_m
        r["structure_vol_m3"] = sphere_shell_vol(r_s, self.structure_thickness_m)

        r["vessel_vol_m3"] = sphere_shell_vol(r_st, self.vessel_thickness_m)

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts.

        Cortex Fusion-specific overrides (marked [OVERRIDE]):
        • C220103: ZERO — no magnetic confinement
        • C220104: ZERO — laser IS the driver
        • C220107: Direct laser capital (not power-scaled formula)
        • C220108: Nanoshell colloid preparation system (OVERRIDE)
        • C220109: ZERO — no direct energy converter

        All other sub-accounts use 1costingfe power-scaling laws.
        """
        r: dict = {}

        p_th = max(power["p_th"], 0.001)
        p_et = max(power["p_et"], 0.001)
        p_net_safe = max(abs(power["p_net"]) * self.n_mod, 0.001)

        # C220101: Active Region / First Wall (liquid-colloid blanket)
        # Source: ASSUMED blanket_unit_cost = 0.15 M$/m³
        r["C220101"] = (self.blanket_unit_cost
                        * geom["blanket_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220102: Shield (D-D neutrons, 2.45 MeV)
        # Source: 1costingfe shield_unit_cost = 0.74 M$/m³, reduced for D-D
        r["C220102"] = (0.50  # Reduced from 0.74: D-D 2.45 MeV vs D-T 14.1 MeV
                        * geom["shield_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: Coils — ZERO [OVERRIDE: no magnetic confinement]
        r["C220103"] = 0.0

        # C220104: Supplementary Heating — ZERO [OVERRIDE]
        # Laser provides all energy input; no separate heating.
        r["C220104"] = 0.0

        # C220105: Primary Structure
        # Source: 1costingfe structure_unit_cost = 0.15 M$/m³
        r["C220105"] = (0.15
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: Chamber Containment Vessel (non-vacuum, liquid environment)
        # Source: 1costingfe vessel_unit_cost = 0.72 M$/m³, reduced for non-vacuum
        r["C220106"] = (0.30
                        * geom["vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # C220107: Power Supplies — OVERRIDE with laser capital cost
        # Femtosecond Yb laser system: $0.1M-$1M for 3 kW average power.
        # NEGLIGIBLE compared to other fusion concepts.
        # Source: analysis.md §S4 (Femtosecond Laser Components).
        r["C220107"] = self.laser_capital_M

        # C220108: Target Factory — OVERRIDE: Nanoshell preparation system
        # Gold nanoshell synthesis + colloid delivery + recovery system.
        # No manufacturing design exists at 10^12 shells/s.
        # Source: ASSUMED. EXTREME UNCERTAINTY.
        r["C220108"] = self.nanoshell_factory_capital_M

        # C220109: Direct Energy Converter — not applicable
        r["C220109"] = 0.0

        # C220110: Remote Handling (D-D, much simpler than D-T)
        # Source: 1costingfe remote_handling_dd_base = 100 M$ at 1 GWe
        # At 0.3 MWe, this scales to a very small number.
        r["C220110"] = 100.0 * (p_net_safe / P_NET_REF) ** 0.6

        # C220111: Installation labor
        # Source: 1costingfe installation_frac = 0.14
        reactor_sub = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"])
        r["C220111"] = 0.14 * reactor_sub

        # C220112: Isotope Separation — minimal (D-D fuel from D2O)
        # Heavy water procurement includes isotope separation cost.
        r["C220112"] = 0.5  # $0.5M — small-scale D2O procurement setup

        r["CAS22_per_module"] = reactor_sub + r["C220111"] + r["C220112"]

        # --- Plant-wide accounts ---
        p_th_total = power["p_th"] * self.n_mod
        p_net_total = abs(power["p_net"]) * self.n_mod

        # C220200: Coolant Systems
        # Source: 1costingfe CAS22 plant-wide formulas, scaled to tiny plant
        C220201 = 166.0 * (max(p_net_total, 0.001) / 1000.0)
        C220202 = 40.6 * (max(p_th_total, 0.001) / 3500.0) ** 0.55
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling (no cryoplant needed)
        # Source: 1costingfe CAS22 formula
        C220301 = 1.1e-3 * max(p_th_total, 0.001)
        r["C220300"] = C220301

        # C220400: Radioactive Waste Management (D-D, minimal)
        # Source: 1costingfe formula, reduced for D-D
        r["C220400"] = 0.5 * (max(p_th_total, 0.001) / 1000.0)

        # C220500: Fuel Handling & Storage (D-D, D2O + gold colloid)
        # Source: 1costingfe fuel_handling_dd_base = 60 M$ at 1 GWe
        r["C220500"] = 60.0 * (max(p_net_total, 0.001) / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        # Source: 1costingfe formula
        r["C220600"] = 11.5 * (max(p_net_total, 0.001) / 1000.0) ** 0.8

        # C220700: Instrumentation & Control
        # Source: 1costingfe formula
        r["C220700"] = 85.0 * (max(p_th_total, 0.001) / 3500.0) ** 0.65

        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        r["CAS22"] = r["CAS22_per_module"] * self.n_mod + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: CAS10-60 capital cost build-up."""
        r: dict = {}

        p_et = max(power["p_et"], 0.001)
        p_net = power["p_net"]
        p_net_safe = max(abs(p_net) * self.n_mod, 0.001)

        # === CAS10: Pre-construction ===
        land_cost = 0.25 * p_net_safe * 10_000 / 1e6   # acres × $/acre
        licensing = 3.0 if not self.noak else 1.5       # D-D licensing (simpler than D-T)
        # Source: 1costingfe CAS10 constants
        r["CAS10"] = (3.0      # site_permits
                      + (4.0 if self.noak else 20.0)   # plant_studies
                      + 2.0    # plant_permits
                      + 1.0    # plant_reports
                      + 1.0    # other_precon
                      + land_cost
                      + licensing)

        # === CAS21: Buildings ===
        # Tiny facility — most buildings are minimal.
        # Source: 1costingfe building_costs, heavily scaled down for 0.3 MWe plant.
        building_items_M = {
            "site_improvements":    5.0,   # Minimal site work
            "laser_target_hall":   10.0,   # ASSUMED: small laser room + target chamber
            "turbine_building":     5.0,   # Very small thermal conversion
            "hot_cell":             3.0,   # D-D: low activation, small chamber
            "reactor_auxiliaries":  3.0,
            "fuel_storage":         1.0,   # D2O + gold storage
            "control_room":         5.0,   # Minimum viable control room
            "security":             1.0,
            "ventilation_hvac":     2.0,
            "administration":       2.0,
            "maintenance":          3.0,
            "misc":                 1.0,
        }
        # For this tiny plant, buildings are essentially fixed costs —
        # they don't scale much below a minimum viable facility.
        # We do NOT apply the standard (p_et / P_ET_REF) scaling because
        # at 0.3 MWe that produces absurdly small numbers. Instead, these
        # represent minimum-viable-facility costs.
        cas21_raw = sum(building_items_M.values())
        r["CAS21"] = cas21_raw * self.regulatory_multiplier
        r["CAS21_detail"] = {k: v * self.regulatory_multiplier
                             for k, v in building_items_M.items()}

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment ===
        # At 0.3 MWe, this is a very small thermal conversion system.
        # Minimum cost for any credible thermal-electric conversion.
        # Source: DEFAULT 1costingfe turbine_per_mw = 0.20, but minimum viable system
        r["CAS23"] = max(self.n_mod * p_et * 0.20, 2.0)  # Minimum $2M

        # === CAS24: Electric Plant Equipment ===
        # Source: 1costingfe costing_constants.yaml electric_per_mw
        r["CAS24"] = max(self.n_mod * p_et * 0.08418, 0.5)  # Minimum $0.5M

        # === CAS25: Misc Plant Equipment ===
        # Source: 1costingfe costing_constants.yaml misc_per_mw
        r["CAS25"] = max(self.n_mod * p_et * 0.05124, 0.3)  # Minimum $0.3M

        # === CAS26: Heat Rejection ===
        # Source: 1costingfe heat_rej_per_mw
        r["CAS26"] = max(self.n_mod * p_et * 0.03416, 0.2)  # Minimum $0.2M

        # === CAS27: Special Materials (D2O initial fill) ===
        # D2O at $600/kg; small chamber needs modest initial fill.
        # ASSUMED: ~100 kg D2O initial fill ≈ $0.06M
        r["CAS27"] = 0.1  # M$ — small D2O + gold nanoshell initial inventory

        # === CAS28: Digital Twin ===
        # Source: 1costingfe digital_twin = 5 M$ — use minimum for tiny plant
        r["CAS28"] = 2.0

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
        # Source: 1costingfe owner_cost_dd = 31 M$ at 1 GWe, ^0.5 scaling
        # At 0.3 MWe, this is tiny but has a practical minimum
        r["CAS40"] = max(31.0 * (p_net_safe / P_NET_REF) ** 0.5, 1.0)

        # === CAS50: Supplementary Costs ===
        # Source: 1costingfe spare_parts_frac_dd = 0.025
        spare_parts = 0.025 * sum(r[k] for k in ["CAS22", "CAS23", "CAS24",
                                                   "CAS25", "CAS26", "CAS27", "CAS28"])
        # Source: 1costingfe shipping_frac=0.015, tax_frac=0.01, insurance=0.015
        shipping = 0.015 * r["CAS20"]
        taxes = 0.010 * r["CAS20"]
        insurance = 0.015 * (r["CAS20"] + r["CAS30"])
        # Source: 1costingfe startup_fuel_dd = 0.1 M$ at 1 GWe
        startup_fuel = 0.1 * (p_net_safe / P_NET_REF) ** 0.5
        # Source: 1costingfe decom_provision_dd = 93 M$ at 1 GWe, ^0.5
        decom = max(93.0 * (p_net_safe / P_NET_REF) ** 0.5, 1.0)
        r["CAS50"] = spare_parts + shipping + taxes + insurance + startup_fuel + decom

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
        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1 + i)**n / ((1 + i)**n - 1)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]

        # === CAS71: Levelized Annual O&M ===
        annual_om_base = self.om_rate_fraction * costs["overnight_capital"]
        g = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g)**Tc
        if abs(i - g) > 1e-10:
            pv_om = A1 * (1 - ((1 + g) / (1 + i))**n) / (i - g)
        else:
            pv_om = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_om

        # === CAS72: Scheduled Replacement (active region) ===
        eff_yr_per_rep = self.core_lifetime_FPY / self.plant_availability
        n_rep = max(0, int(math.ceil(n / eff_yr_per_rep)) - 1)
        rep_cost = cas22["C220101"] * self.n_mod
        pv_rep = sum(
            rep_cost / (1 + i)**(k * eff_yr_per_rep)
            for k in range(1, n_rep + 1)
            if k * eff_yr_per_rep < n
        )
        r["CAS72"] = crf * pv_rep
        r["n_replacements"] = n_rep

        r["CAS70"] = r["CAS71"] + r["CAS72"]

        # === CAS80: Fuel & Consumables ===
        seconds_per_year = 8760 * 3600 * self.plant_availability

        # --- Gold nanoshell consumption ---
        # Shell volume: 4/3 π (R_out³ - R_in³)
        r_out_m = self.nanoshell_outer_radius_nm * 1e-9
        r_in_m = self.nanoshell_inner_radius_nm * 1e-9
        shell_vol_m3 = (4.0 / 3.0) * math.pi * (r_out_m**3 - r_in_m**3)
        gold_per_shell_kg = shell_vol_m3 * GOLD_DENSITY_KG_M3

        # Shells consumed per second: shells/pulse × pulses/s × (1 - survival)
        shells_per_second = (self.nanoshells_per_pulse
                             * self.laser_rep_rate_MHz * 1e6
                             * (1.0 - self.nanoshell_survival_fraction))
        annual_gold_kg = shells_per_second * gold_per_shell_kg * seconds_per_year
        cas80_gold = annual_gold_kg * self.gold_price_per_kg / 1e6  # M$/yr
        r["CAS80_gold"] = cas80_gold
        r["annual_gold_kg"] = annual_gold_kg

        # --- D2O consumption (net loss from fusion reactions) ---
        # D-D fusion consumes 2 D atoms per event. At ~1 MW fusion:
        fusion_rate = power["p_fus"] * 1e6 / E_FUSION_J  # fusions/s
        M_D2_kg = 4 * AMU_KG  # 2 D atoms consumed per fusion = 4 amu
        annual_D2_kg = fusion_rate * M_D2_kg * seconds_per_year
        # D2O: each molecule has 1 D atom (D2O has 2 D atoms, mass 20 amu)
        # Consumed D atoms → D2O equivalent: 2 D per fusion, D2O mass = 20 amu
        annual_D2O_equiv_kg = annual_D2_kg * (20.0 / 4.0)  # mass ratio D2O/2D
        cas80_d2o = annual_D2O_equiv_kg * self.d2o_cost_per_kg / 1e6
        r["CAS80_d2o"] = cas80_d2o
        r["annual_D2O_kg"] = annual_D2O_equiv_kg

        r["CAS80"] = cas80_gold + cas80_d2o

        # === LCOE ===
        ann_rev = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = ann_rev

        if p_net_total > 0:
            ann_energy_MWh = 8760 * p_net_total * self.plant_availability
            r["annual_energy_MWh"] = ann_energy_MWh
            lcoe = ann_rev * 1e6 / ann_energy_MWh
            r["lcoe_USD_per_MWh"] = lcoe
            r["lcoe_cents_per_kWh"] = lcoe / 10.0
        else:
            r["annual_energy_MWh"] = 0.0
            r["lcoe_USD_per_MWh"] = float('inf')
            r["lcoe_cents_per_kWh"] = float('inf')

        if ann_rev > 0:
            r["capital_fraction"] = r["CAS90"] / ann_rev
            r["om_fraction"] = r["CAS70"] / ann_rev
            r["fuel_fraction"] = r["CAS80"] / ann_rev

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
        geom = self._compute_geometry(power)
        cas22 = self._compute_cas22(power, geom)
        costs = self._compute_costs(power, cas22)
        econ = self._compute_economics(power, costs, cas22)
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

# Net electric power at the concept's native design point [GWe].
# Inferred: 1 MW fusion × 30% conversion − recirculating ≈ 0.29 MWe ≈ 0.3 MWe.
# Matches frontmatter P_native value.  This concept has no archetype
# (Archetype-Fit: None), so the three-forward helper form
# (generic_reference / run_native_and_1gw) does not apply.
P_native = 0.3  # GWe  (actually 0.0003 GWe — kept in MWe-equivalent units per convention)

params = CortexFusionPlantParams()
results = params.compute()

# Pipeline aliases — no archetype means no generic reference or 1 GWe projection.
native = results
result_1gw = None  # Not applicable: no archetype for 1 GWe extrapolation


# ============================================================================
# Output functions
# ============================================================================

def print_results(p: CortexFusionPlantParams, r: dict) -> None:
    """Pretty-print the full LCOE model results with CAS-structured accounting."""
    pw = r["power"]
    cas22 = r["cas22"]
    costs = r["costs"]
    econ = r["economics"]

    print("=" * 76)
    print("Laser ICF Liquid-Jet Target (Cortex Fusion) LCOE Model")
    print("Nano-Sun 1 MHz Reactor Scenario — arXiv:2503.15531")
    print("1cFE CAS-Structured Free-Form Model — FOR CORRIDOR PURPOSES ONLY")
    print("=" * 76)

    # Critical disclaimer
    print()
    print("  +====================================================================+")
    print("  | CRITICAL: THIS IS NOT A CREDIBLE COST ESTIMATE                      |")
    print("  |                                                                      |")
    print("  | The core physics mechanism (plasmonic D-D fusion in nanoshells)      |")
    print("  | is UNVALIDATED. Zero fusion events demonstrated by any group.       |")
    print("  | No energy conversion system, reactor chamber, or blanket design.    |")
    print("  | All cost parameters are ASSUMED — zero cost data from any source.   |")
    print("  |                                                                      |")
    print("  | DEMONSTRATED vs. CLAIMED neutron yield gap: 14 ORDERS OF MAGNITUDE  |")
    print("  | Cambridge kHz experiment: ~10^5 n/s  vs  Paper claim: ~10^19 n/s    |")
    print("  +====================================================================+")
    print()

    # Viability warning
    if pw["p_net"] <= 0:
        print("  *** ENERGY SINK: Net electric is NEGATIVE at these parameters. ***")
        print("  *** LCOE is undefined. Laser consumes more than plant generates. ***")
        print()

    # --- Key Physics Inputs ---
    print(f"\n--- Key Physics Parameters ---")
    print(f"  Laser average power:          {p.laser_avg_power_kW:.1f} kW ({pw['p_laser_MW']*1000:.1f} kW optical)")
    print(f"  Laser wall-plug power:        {pw['p_laser_elec_MW']*1000:.1f} kW ({pw['p_laser_elec_MW']:.4f} MW)")
    print(f"  Laser wall-plug efficiency:   {p.laser_wallplug_efficiency:.0%}")
    print(f"  Repetition rate:              {p.laser_rep_rate_MHz:.0f} MHz")
    print(f"  Nanoshells per pulse:         {p.nanoshells_per_pulse:.0e}")
    print(f"  Fusion power (P_fus):         {pw['p_fus']:.2f} MW  [PHYSICS UNVALIDATED]")
    print(f"  Scientific Q (P_fus/P_laser): {pw['Q_sci']:.0f}")
    print(f"  Paper Q (P_fus*kappa/P_laser):{pw['Q_paper']:.0f}")
    print(f"  Conversion efficiency (kappa):{p.kappa:.0%}  [NO MECHANISM SPECIFIED]")
    print(f"  Plant availability:           {p.plant_availability:.0%}")
    print(f"  Modules:                      {p.n_mod}")

    # --- Power Balance ---
    print(f"\n--- Power Balance ---")
    print(f"  Fusion power (P_fus):         {pw['p_fus']:>8.3f} MW  [THEORETICAL]")
    print(f"    Neutron power (~50%):       {pw['p_neutron']:>8.3f} MW (2.45 MeV D-D)")
    print(f"    Charged power (~50%):       {pw['p_charged']:>8.3f} MW (p, T, He-3)")
    print(f"  Thermal power (P_th):         {pw['p_th']:>8.3f} MW  (x M={p.M_blanket})")
    print(f"  Gross electric (P_et):        {pw['p_et']:>8.3f} MWe (x kappa={p.kappa:.0%})")
    print(f"  Recirculating power:")
    print(f"    Laser (wall-plug):          {pw['p_laser_elec_MW']:>8.4f} MW")
    print(f"    Auxiliaries:                {pw['p_aux']:>8.4f} MW")
    print(f"    Total recirculating:        {pw['p_recirc']:>8.4f} MW")
    print(f"  Net electric (P_net):         {pw['p_net']:>8.3f} MWe")
    print(f"  Engineering Q (Q_eng):        {pw['Q_eng']:>8.1f}")
    print(f"  Recirculating fraction:       {pw['recirc_fraction']:>8.1%}")

    # --- CAS22 ---
    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    cas22_labels = {
        "C220101": ("Active Region / Blanket",       ""),
        "C220102": ("Shield (D-D neutrons)",          ""),
        "C220103": ("Coils",                          "[ZERO — no magnetic confinement]"),
        "C220104": ("Supplementary Heating",          "[ZERO — laser is driver]"),
        "C220105": ("Primary Structure",              ""),
        "C220106": ("Chamber Vessel",                 ""),
        "C220107": ("Laser System",                   "[OVERRIDE — negligible cost]"),
        "C220108": ("Nanoshell Factory",              "[OVERRIDE — no design exists]"),
        "C220109": ("DEC",                            "[ZERO — not applicable]"),
        "C220110": ("Remote Handling",                ""),
        "C220111": ("Installation Labor",             ""),
        "C220112": ("Isotope Separation",             ""),
    }
    for code, (label, note) in cas22_labels.items():
        val = cas22.get(code, 0.0)
        if val > 0.001 or note:
            print(f"    {code} {label:<30s} ${val:>8.3f}M  {note}")
    print(f"    {'_' * 66}")
    print(f"    Per-module subtotal:                   ${cas22['CAS22_per_module']:>8.3f}M")

    pw_labels = {
        "C220200": "Coolant Systems",
        "C220300": "Aux Cooling",
        "C220400": "Rad Waste Management (D-D)",
        "C220500": "Fuel Handling (D2O + colloid)",
        "C220600": "Other Equipment",
        "C220700": "I&C",
    }
    print(f"  Plant-wide accounts:")
    for code, label in pw_labels.items():
        val = cas22[code]
        if val > 0.001:
            print(f"    {code} {label:<36s} ${val:>8.3f}M")
    print(f"    {'_' * 66}")
    print(f"    Plant-wide subtotal:                   ${cas22['CAS22_plant_wide']:>8.3f}M")
    print(f"  CAS22 Total:                             ${cas22['CAS22']:>8.3f}M")

    # --- Capital Costs ---
    print(f"\n--- Capital Costs (CAS10-60) ---")
    print(f"  CAS10 Pre-construction:                  ${costs['CAS10']:>8.2f}M")
    print(f"  CAS21 Buildings (x{p.regulatory_multiplier:.1f}x reg.):          ${costs['CAS21']:>8.2f}M")
    print(f"  CAS22 Reactor Plant Equipment:           ${costs['CAS22']:>8.3f}M")
    print(f"  CAS23 Turbine Plant:                     ${costs['CAS23']:>8.2f}M")
    print(f"  CAS24 Electric Plant:                    ${costs['CAS24']:>8.2f}M")
    print(f"  CAS25 Misc Plant:                        ${costs['CAS25']:>8.2f}M")
    print(f"  CAS26 Heat Rejection:                    ${costs['CAS26']:>8.2f}M")
    print(f"  CAS27 Special Materials (D2O + Au):      ${costs['CAS27']:>8.2f}M")
    print(f"  CAS28 Digital Twin:                      ${costs['CAS28']:>8.2f}M")
    print(f"  CAS29 Contingency:                       ${costs['CAS29']:>8.2f}M")
    print(f"  {'_' * 64}")
    print(f"  CAS20 Direct Costs:                      ${costs['CAS20']:>8.2f}M")
    print(f"  CAS30 Indirect Costs:                    ${costs['CAS30']:>8.2f}M")
    print(f"  CAS40 Owner's Costs:                     ${costs['CAS40']:>8.2f}M")
    print(f"  CAS50 Supplementary:                     ${costs['CAS50']:>8.2f}M")
    print(f"  {'_' * 64}")
    print(f"  Overnight Capital:                       ${costs['overnight_capital']:>8.2f}M")
    print(f"  CAS60 IDC (f={costs['f_IDC']:.3f}):               ${costs['CAS60']:>8.2f}M")
    print(f"  {'=' * 64}")
    print(f"  Total Capital:                           ${costs['total_capital']:>8.2f}M")
    if pw["p_net"] > 0:
        print(f"  Specific Capital:                  ${costs['specific_capital_USD_per_kWe']:>10,.0f} $/kWe")

    # --- Annual Costs ---
    print(f"\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90 Capital charge (CRF={econ['CRF']:.4f}):   ${econ['CAS90']:>8.3f}M/yr")
    print(f"  CAS71 O&M (levelized, {p.om_rate_fraction:.1%}/yr):      ${econ['CAS71']:>8.3f}M/yr")
    print(f"  CAS72 Active region replacements ({econ['n_replacements']}):    ${econ['CAS72']:>8.4f}M/yr")
    print(f"  CAS70 Total O&M:                         ${econ['CAS70']:>8.3f}M/yr")
    print(f"  CAS80 Fuel & consumables:")
    print(f"    Gold nanoshells:                       ${econ['CAS80_gold']:>8.4f}M/yr ({econ['annual_gold_kg']:.2f} kg/yr)")
    print(f"    D2O (net fusion consumption):           ${econ['CAS80_d2o']:>8.6f}M/yr ({econ['annual_D2O_kg']:.4f} kg/yr)")
    print(f"  CAS80 Total:                             ${econ['CAS80']:>8.4f}M/yr")

    # --- LCOE ---
    # Stomped to NOT ENOUGH DATA per concepts 6 and 19 convention: the underlying
    # physics mechanism (plasmonic D-D fusion in nanoshells) is unvalidated and no
    # fusion events have been demonstrated by any group, so no LCOE value is
    # grounded enough to publish. CAS account values above are retained for
    # corridor purposes only.
    print(f"\n--- LCOE ---")
    print("LCOE: (NOT ENOUGH DATA FOR THIS CONCEPT)")
    print("Native LCOE = (NOT ENOUGH DATA FOR THIS CONCEPT)")
    print("Generic LCOE = (NOT ENOUGH DATA FOR THIS CONCEPT)")
    if pw["p_net"] > 0:
        print(f"  Annual energy production:     {econ['annual_energy_MWh']:>12,.1f} MWh/yr")
        print(f"  Annual revenue requirement:   ${econ['annual_revenue_req']:>8.3f}M/yr")
        print(f"  Capital (CAS90):             {econ.get('capital_fraction', 0):.1%}")
        print(f"  O&M    (CAS70):              {econ.get('om_fraction', 0):.1%}")
        print(f"  Fuel   (CAS80):              {econ.get('fuel_fraction', 0):.2%}")

    print()
    print("=" * 76)


def sensitivity_sweep(base_params: CortexFusionPlantParams,
                      param_name: str,
                      values: list,
                      label: str = "") -> list[dict]:
    """Sweep a single parameter and return LCOE and net power for each value."""
    out = []
    for val in values:
        p = CortexFusionPlantParams(**{**base_params.__dict__, param_name: val})
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
    print(f"  {'Value':>12}  {'P_net':>10}  {'recirc':>7}  {'LCOE':>16}")
    print(f"  {'_'*12}  {'_'*10}  {'_'*7}  {'_'*16}")
    for row in sweep_results:
        v = row["param_value"]
        pn = row["net_electric_MW"]
        eps = row["recirc_fraction"]
        lcoe = row["lcoe_USD_MWh"]

        # LCOE stomped to NOT ENOUGH DATA across the sweep — see headline LCOE
        # block above for rationale (physics mechanism unvalidated).
        lcoe_str = "  (NOT ENOUGH DATA)"
        if pn <= 0:
            eps_str = "  >100%"
        else:
            eps_str = f"{eps:>6.1%}"

        # Format value smartly
        if v >= 1e6:
            v_str = f"{v:>12.0e}"
        elif v >= 1:
            v_str = f"{v:>12.2f}"
        else:
            v_str = f"{v:>12.4f}"

        p_str = f"{pn*1000:>8.1f} kW" if abs(pn) < 1.0 else f"{pn:>8.2f} MW"

        print(f"  {v_str}  {p_str}  {eps_str}  {lcoe_str}")


def main():
    """Generate baseline results and sensitivity analysis."""

    print("\n" + "=" * 76)
    print("BASELINE SCENARIO")
    print("=" * 76)
    print_results(params, results)

    print("\n\n" + "=" * 76)
    print("SENSITIVITY ANALYSIS")
    print("=" * 76)
    print("  NOTE: At ~0.3 MWe native power, LCOE is dominated by fixed costs.")
    print("  Sensitivity sweeps explore which parameters most affect LCOE.")
    print()

    # 1. Fusion power (the fundamental claim, most impactful parameter)
    sw1 = sensitivity_sweep(
        params, "fusion_power_MW",
        [0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0],
        "Fusion power [MW] — core physics claim"
    )
    _print_sweep(sw1, "Fusion Power (paper claims 1 MW; Cambridge demonstrated ~0 MW)", "MW")

    # 2. Conversion efficiency kappa (no mechanism specified)
    sw2 = sensitivity_sweep(
        params, "kappa",
        [0.10, 0.20, 0.30, 0.40, 0.50],
        "Thermal-electric conversion efficiency"
    )
    _print_sweep(sw2, "Conversion Efficiency kappa (paper assumes 30%, no mechanism)", "")

    # 3. Nanoshell factory capital (total unknown)
    sw3 = sensitivity_sweep(
        params, "nanoshell_factory_capital_M",
        [5.0, 10.0, 20.0, 50.0, 100.0, 500.0],
        "Nanoshell factory capital"
    )
    _print_sweep(sw3, "Nanoshell Factory Capital [M$] (no manufacturing design exists)", "M$")

    # 4. Nanoshell survival fraction (huge impact on CAS80)
    sw4 = sensitivity_sweep(
        params, "nanoshell_survival_fraction",
        [0.0, 0.50, 0.90, 0.95, 0.99, 1.0],
        "Nanoshell survival fraction"
    )
    _print_sweep(sw4, "Nanoshell Survival Fraction (unknown: destroyed or reusable?)", "")

    # 5. Gold price sensitivity
    sw5 = sensitivity_sweep(
        params, "gold_price_per_kg",
        [20000, 40000, 60000, 80000, 100000],
        "Gold price per kg"
    )
    _print_sweep(sw5, "Gold Price [$/kg] (affects CAS80 if nanoshells consumed)", "$/kg")

    # 6. Plant availability (technology maturity proxy)
    sw6 = sensitivity_sweep(
        params, "plant_availability",
        [0.50, 0.65, 0.75, 0.85, 0.90],
        "Plant availability"
    )
    _print_sweep(sw6, "Plant Availability [fraction]", "")

    # =========================================================================
    # SCENARIO COMPARISON
    # =========================================================================
    print("\n\n" + "=" * 76)
    print("SCENARIO COMPARISON")
    print("=" * 76)

    # Conservative: Higher costs, lower performance
    conservative = CortexFusionPlantParams(
        fusion_power_MW=0.5,             # Lower than claimed
        kappa=0.20,                       # Low conversion efficiency
        nanoshell_factory_capital_M=100.0, # Expensive factory
        nanoshell_survival_fraction=0.0,   # All destroyed
        laser_capital_M=2.0,              # Higher laser cost
        plant_availability=0.60,
    )

    # Moderate: Baseline parameters (already set)
    moderate = params

    # Optimistic: Better physics, nanoshell recycling
    optimistic = CortexFusionPlantParams(
        fusion_power_MW=5.0,              # 5x paper claim (still speculative)
        kappa=0.40,                       # Better conversion system
        nanoshell_factory_capital_M=10.0,  # Cheaper factory
        nanoshell_survival_fraction=0.90,  # 90% recycled
        laser_capital_M=0.5,              # Cheaper laser
        plant_availability=0.85,
    )

    scenarios = [
        ("Conservative", conservative),
        ("Moderate (Baseline)", moderate),
        ("Optimistic", optimistic),
    ]

    print(f"\n  {'Scenario':<24} {'P_net':>10} {'LCOE':>16} {'$/kWe':>14}")
    print(f"  {'_'*24} {'_'*10} {'_'*16} {'_'*14}")

    for name, p_scenario in scenarios:
        r = p_scenario.compute()
        pw = r["power"]
        econ = r["economics"]
        c = r["costs"]

        p_net = pw["p_net_plant"]
        lcoe = econ["lcoe_USD_per_MWh"]
        cap = c["specific_capital_USD_per_kWe"]

        # LCOE stomped to NOT ENOUGH DATA per concepts 6 and 19 convention.
        lcoe_str = "  (NOT ENOUGH DATA)"
        if p_net <= 0:
            p_str = "    (sink)"
            cap_str = "      (sink)"
        else:
            p_str = f"{p_net*1000:>8.1f}kW" if p_net < 1.0 else f"{p_net:>8.1f}MW"
            cap_str = f"  ${cap:>10,.0f}"

        print(f"  {name:<24} {p_str}  {lcoe_str}  {cap_str}")

    # =========================================================================
    # KEY BINDING CONSTRAINTS
    # =========================================================================
    print("\n\n" + "=" * 76)
    print("KEY BINDING CONSTRAINTS (in order of impact)")
    print("=" * 76)

    print("""
  1. PHYSICS VALIDATION GAP (ABSOLUTE BLOCKER)

     The plasmonic nanoshell fusion mechanism has ZERO experimental validation.
     No fusion neutrons have been reported from this mechanism by any group.

     Demonstrated (Cambridge kHz experiment): ~10^5 neutrons/second
     Claimed (Nano-Sun paper):                ~10^19 neutrons/second
     Gap: 14 ORDERS OF MAGNITUDE

     The paper acknowledges that ionization-driven damping of the plasmon
     oscillation could eliminate the enhancement mechanism entirely. The
     deuteron mean free path for fusion (~cm) vastly exceeds the nanoshell
     radius (~100 nm), meaning most accelerated deuterons escape.

     Until the physics is validated, ALL parameters in this model are
     conditional on the mechanism working at all.

  2. FIXED-COST DOMINANCE AT SUB-MW SCALE

     At 0.3 MWe native power, the cost structure is dominated by fixed costs
     (buildings, I&C, control room, minimum-viable-facility infrastructure).
     The concept produces ~2,000 MWh/year — less than a single large wind
     turbine. No amount of engineering optimization can produce competitive
     LCOE at this power level because the denominator (energy production)
     is microscopic while the numerator (facility costs) has a practical floor.

     Scaling to commercial power would require 10,000x more nanoshells per
     pulse, multiple parallel units, or higher yield per nanoshell — none
     of which are discussed in the paper.

  3. ENERGY CONVERSION SYSTEM (UNDESIGNED)

     No mechanism exists to convert ~1 MW of mostly 2.45 MeV neutrons
     emitted isotropically from a liquid colloid into electricity. The
     paper's 30% conversion assumption has no engineering basis. Designing
     the blanket, thermal management, and power conversion for a colloidal
     fusion source is an unsolved engineering problem with no prior art.
""")

    print("=" * 76)
    print()


if __name__ == "__main__":
    main()
