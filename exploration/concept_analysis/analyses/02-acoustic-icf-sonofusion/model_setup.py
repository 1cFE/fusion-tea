"""
Acoustic ICF (Sonofusion) Speculative LCOE Corridor Model
==========================================================
1cFE First Pass Concept Analysis
Concept: Acoustic Inertial Confinement Fusion (Sonofusion)
Company: Sonofusion Energy (UCLA spin-off, founded by Seth Putterman & Carlos Camara)

╔═══════════════════════════════════════════════════════════════════════════════╗
║ CRITICAL: THIS IS NOT A CREDIBLE COST ESTIMATE                               ║
║                                                                               ║
║ This model exists ONLY to establish a speculative LCOE corridor for          ║
║ cross-concept comparison purposes IF the fundamental physics demonstration    ║
║ gap were somehow overcome. It is NOT a validated techno-economic analysis.    ║
║                                                                               ║
║ BLOCKING ISSUES:                                                              ║
║ • No design point specified by Sonofusion Energy (no P_native, no specs)     ║
║ • No archetype assigned (upstream tables: Archetype = [empty])                ║
║ • No comparables list (analysis frontmatter: Comparables = [])                ║
║ • Fundamental physics undemonstrated (4 orders of magnitude temp gap)         ║
║                                                                               ║
║ Under the D1+ analysis contract, quantitative models require validated        ║
║ design-point data and archetype assignment BEFORE modeling. This concept      ║
║ has neither. The model's "native power" (102 MWe) and all other parameters    ║
║ are INVENTED for corridor purposes, not extracted from company disclosures.   ║
║                                                                               ║
║ The analysis.md correctly documents this concept as a data-availability       ║
║ assessment only, not a cost model. The existence of this model file is        ║
║ for cross-concept comparison infrastructure testing only.                     ║
╚═══════════════════════════════════════════════════════════════════════════════╝

PHYSICS DEMONSTRATION GAP (ABSOLUTE BLOCKER):
    Best demonstrated sonoluminescence temperatures: ~16,000 K (Flannigan & Suslick 2010)
    D-D fusion requirement: ~100,000,000 K (100 million K)
    Temperature gap: ~6,000× (4 orders of magnitude)

No credible evidence exists that acoustic cavitation can achieve fusion-relevant
plasma conditions. The Taleyarkhan bubble fusion claims were discredited, found
to involve research misconduct, and have never been independently replicated.
The UCLA Putterman group (30+ years sonoluminescence research) has found no
evidence of fusion neutrons from acoustic cavitation.

This model assumes hypothetical breakthrough physics that closes the 4-order-of-
magnitude temperature gap. ALL PARAMETERS ARE HIGHLY SPECULATIVE. The native
power level (102 MWe), driver capital ($150M), Q_sci (5.0), and all other
parameters are SPECULATIVE ASSUMPTIONS chosen to produce plant-scale output for
modeling corridor purposes, NOT extracted from company-disclosed specifications.

Economy-of-scale cross-concept scaling (α = 0.6):
    scaled_lcoe = native_lcoe × (P_native / 1000 MWe)^(1 - α)
Applied post-hoc to speculative physics-derived power.

Key references:
    UCLA Putterman Research Group (sonoluminescence physics)
    [iter-01/sources/ucla-putterman-group-sonoluminescence.md]

    Wikipedia, Bubble Fusion (historical controversy)
    [iter-01/sources/bubble-fusion-scientific-history.md]

    Flannigan & Suslick, Nature Physics 6, 598-601 (2010)
    (Best measured sonoluminescence plasma conditions: 7,000-16,000 K)

    analysis.md — Phase 1a analysis documenting data gaps
    [analyses/02-acoustic-icf-sonofusion/analysis.md]

    1costingfe costing_constants.yaml — CAS scaling laws and unit costs
    [~/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml]

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass

# Sonofusion Energy discloses no design point — see CRITICAL block above.
# Freeform LCOE: not comparable to 1costingfe-derived numbers. Read by the
# explorer extractor to suppress the headline LCOE in cross-concept views
# (cost landscape, comparison summary). `grep "DATA_GROUNDED = False"
# exploration/concept_analysis/analyses/*/model_setup.py` returns the
# authoritative audit list of suppressed concepts.
DATA_GROUNDED = False

# ============================================================================
# Physical constants
# ============================================================================
E_FUSION_DD_T_MEV  = 4.03                     # D-D → T + p fusion energy [MeV]
E_FUSION_DD_He3_MEV = 3.27                    # D-D → He-3 + n fusion energy [MeV]
E_FUSION_DD_AVG_MEV = (E_FUSION_DD_T_MEV + E_FUSION_DD_He3_MEV) / 2.0  # Average D-D
E_FUSION_J = E_FUSION_DD_AVG_MEV * 1e6 * 1.602e-19  # Average D-D energy [J]
AMU_KG = 1.66053906660e-27                    # 1 atomic mass unit [kg]

# ============================================================================
# Reference power levels for 1costingfe scaling laws
# ============================================================================
P_TH_REF  = 2500.0   # Reference thermal power [MW]
P_ET_REF  = 1100.0   # Reference gross electric power [MW]
P_NET_REF = 1000.0   # Reference net electric power [MW]


@dataclass
class AcousticICFPlantParams:
    """
    Parameterized Acoustic ICF (Sonofusion) power plant model.

    Architecture overview (SPECULATIVE — no disclosed design):
    ┌──────────────────────────────────────────────────────┐
    │  Ultrasonic transducers → deuterated liquid chamber   │
    │       ↓                                              │
    │  Acoustic cavitation → bubble implosion → ???        │
    │       ↓ [TEMPERATURE GAP: 16,000 K → 100,000,000 K]  │
    │  [HYPOTHETICAL] D-D fusion → neutrons + charged      │
    │       ↓                                              │
    │  Neutrons → liquid absorption → thermal energy       │
    │  Charged → local liquid heating → thermal energy     │
    │       ↓                                              │
    │  Thermal cycle (ASSUMED: Rankine) → gross electric   │
    │       ↓                                              │
    │  Net electric = Gross - Recirculating (driver + aux) │
    └──────────────────────────────────────────────────────┘

    Key structural differences from 1costingfe standard models:
    • C220103 (Coils):          ZERO — no magnetic confinement
    • C220104 (Heating):        ZERO — acoustic driver IS the heating mechanism
    • C220107 (Power Supplies): OVERRIDE — ultrasonic driver capital
    • C220108 (Target Factory): ZERO — continuous liquid-phase operation

    Uncertainty tiers used in docstrings:
    • (no tag)             — well-established physics or engineering constant
    • MODERATE UNCERTAINTY — reasonable estimate from documented analogues
    • HIGH UNCERTAINTY     — speculative or poorly constrained
    • EXTREME UNCERTAINTY  — pure speculation, no credible basis
    • PHYSICS UNDEMONSTRATED — fundamental gap, no experimental evidence
    """

    # =========================================================================
    # ACOUSTIC DRIVER (replaces laser/coils/etc.)
    # =========================================================================

    driver_power_MW: float = 50.0
    """Wall-plug electrical power consumed by ultrasonic driver system [MW].
    This is the dominant recirculating load. Analogues: industrial ultrasonic
    cleaning/welding systems operate at kW–MW scale but at far lower duty cycle
    and without fusion requirements. Fusion-relevant power levels unknown.
    Source: ASSUMED — no plant-scale driver design exists.
    EXTREME UNCERTAINTY — range could be 10 MW to 500 MW."""

    driver_frequency_kHz: float = 30.0
    """Acoustic driver frequency [kHz].
    UCLA sonoluminescence experiments: 20-40 kHz standing wave systems.
    Source: analysis.md §S5, ucla-putterman-group-sonoluminescence.md.
    HIGH UNCERTAINTY — fusion-optimized frequency unknown."""

    driver_efficiency: float = 0.85
    """Driver electrical-to-acoustic efficiency [fraction].
    Industrial piezoelectric transducers: 85-95% efficiency at low power.
    Whether this scales to fusion-relevant power and duty cycle is unknown.
    Source: ASSUMED from industrial ultrasonic equipment.
    HIGH UNCERTAINTY."""

    cavitation_sites: int = 1_000_000
    """Number of simultaneous acoustic cavitation fusion sites.
    UCLA single-bubble sonoluminescence: one bubble at a time.
    Power-plant-relevant scaling requires massive parallelization.
    Source: ASSUMED — no multi-site fusion chamber design exists.
    EXTREME UNCERTAINTY — could be 10^3 to 10^9."""

    rep_rate_per_site_kHz: float = 10.0
    """Cavitation/fusion events per site per second [kHz].
    UCLA reports "10 million times per second" for sonoluminescence flashes
    at 40 kHz driver frequency, but this is single-bubble, not fusion.
    Fusion rep rate per site is unknown.
    Source: analysis.md §S5, §S2.
    EXTREME UNCERTAINTY."""

    # =========================================================================
    # FUSION PHYSICS (HYPOTHETICAL — UNDEMONSTRATED)
    # =========================================================================

    yield_per_event_J: float = 1.0e-9
    """Fusion energy yield per cavitation event [J].
    This assumes ~6200 D-D fusions per bubble collapse event
    (= 1e-9 J / 3.65e-13 J/fusion). NO EXPERIMENTAL BASIS.
    Demonstrated sonoluminescence: ZERO fusion neutrons detected.
    Temperature gap: 16,000 K demonstrated vs. 100,000,000 K required (6,000×).
    Source: SPECULATIVE — parameter chosen to produce ~100 MWe plant-scale.
    PHYSICS UNDEMONSTRATED — no evidence acoustic cavitation can reach
    fusion-relevant conditions."""

    Q_sci: float = 5.0
    """Scientific gain: fusion energy out / acoustic energy in (per event).
    Pure speculation. Analogues: Laser ICF achieved Q~1.5 at NIF (2022);
    magnetic confinement Q~1.0 at JET (1997). Acoustic ICF has NO DEMONSTRATED
    fusion reactions, so Q_sci is undefined experimentally.
    Source: ASSUMED — chosen to produce net-positive power output.
    PHYSICS UNDEMONSTRATED."""

    # =========================================================================
    # ENERGY CAPTURE
    # =========================================================================

    M_blanket: float = 1.0
    """Energy multiplication factor (local absorption in liquid).
    D-D produces lower-energy neutrons (2.45 MeV) than D-T (14.1 MeV).
    No breeding blanket required for D-D fuel, so M ≈ 1.0 (no Li-6 reaction).
    Some energy multiplication from neutron thermalization in liquid.
    Source: ASSUMED — deuterated liquid (heavy water) provides moderation
    but no exothermic breeding reactions.
    MODERATE UNCERTAINTY."""

    eta_th: float = 0.35
    """Thermal-to-electric conversion efficiency [fraction].
    Energy conversion pathway not disclosed by Sonofusion Energy.
    Assumed thermal cycle (Rankine steam) at moderate temperature.
    Sonoluminescence plasma flash duration: <50 picoseconds (too short for
    direct conversion). Assumed approach: neutrons + charged products →
    liquid heating → steam → turbine.
    Source: ASSUMED — no conversion system specified.
    HIGH UNCERTAINTY — actual approach unknown."""

    # =========================================================================
    # PLANT CONFIGURATION
    # =========================================================================

    n_mod: int = 4
    """Number of fusion chamber modules per plant.
    Multi-module approach assumed for redundancy and scalability.
    SPECULATIVE CORRIDOR VALUE: Model derives ~102 MWe native plant power
    (4 modules × 25.5 MWe per module) from speculative physics parameters.
    Sonofusion Energy has disclosed NO native power target.
    Source: ASSUMED — company mentions "table-top to utility-scale" but
    provides no specifications.
    HIGH UNCERTAINTY."""

    plant_availability: float = 0.80
    """Plant capacity factor / availability [fraction].
    Lower than baseload thermal plants (85-90%) due to technology immaturity.
    Continuous ultrasonic operation at high power and cavitation-induced
    erosion/fatigue are unknown reliability factors.
    Source: ASSUMED.
    MODERATE UNCERTAINTY."""

    plant_lifetime_years: float = 40.0
    """Plant economic lifetime [years].
    Source: 1costingfe default. Standard fusion plant assumption."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds 10% contingency on direct costs.
    Source: 1costingfe CAS29 convention."""

    # =========================================================================
    # CAPITAL — DRIVER SYSTEM (C220107 OVERRIDE)
    # =========================================================================

    driver_capital_M: float = 150.0
    """Capital cost of ultrasonic driver system (transducers + control + power) [$M].
    Maps to C220107 (Power Supplies) — CONCEPT OVERRIDE.
    Industrial ultrasonic equipment (cleaning, welding): $10k-1M per unit at kW-scale.
    Fusion-relevant system: unknown. Assumed MAJOR COST ADVANTAGE vs. laser
    systems ($2B+ for NIF-scale) or superconducting magnets ($1B+ for ITER-scale).
    BASELINE = $150M assumes ultrasonic transducers are orders of magnitude
    cheaper than lasers or magnets — BUT REQUIRES UNDEMONSTRATED PHYSICS.
    Source: ASSUMED — no fusion-scale driver design exists.
    EXTREME UNCERTAINTY — range could be $50M-$5,000M depending on power
    requirements and design maturity."""

    # =========================================================================
    # CHAMBER & GEOMETRY
    # =========================================================================

    chamber_inner_radius_m: float = 1.5
    """Inner radius of liquid-filled fusion chamber [m].
    Spherical chamber assumed for acoustic wave focusing.
    No chamber design has been published.
    Source: ASSUMED — rough scale for liquid-containment system.
    HIGH UNCERTAINTY."""

    blanket_thickness_m: float = 0.50
    """Liquid-filled active region thickness [m].
    Heavy water (D₂O) serves as both fuel and neutron moderator.
    D-D neutrons (2.45 MeV) require less shielding than D-T (14.1 MeV).
    Source: ASSUMED.
    HIGH UNCERTAINTY."""

    shield_thickness_m: float = 0.40
    """Neutron shielding thickness [m] (if D-D fusion occurred).
    D-D produces 2.45 MeV neutrons in ~50% of reactions.
    Less penetrating than D-T's 14.1 MeV, but still requires shielding.
    The liquid working fluid (heavy water) provides some moderation.
    Source: ASSUMED.
    MODERATE UNCERTAINTY."""

    structure_thickness_m: float = 0.20
    """Primary structure thickness [m].
    Source: ASSUMED — compact chamber structure.
    MODERATE UNCERTAINTY."""

    vessel_thickness_m: float = 0.08
    """Chamber containment vessel thickness [m].
    Non-vacuum system (liquid-filled). Pressure vessel design.
    Source: ASSUMED.
    MODERATE UNCERTAINTY."""

    blanket_unit_cost: float = 0.10
    """Liquid-filled region unit cost [M$/m³].
    Much cheaper than solid breeding blanket (1costingfe: 0.60 M$/m³ for D-T).
    Heavy water fill + simple containment.
    Source: ASSUMED — no breeding blanket, just liquid deuterium carrier.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # AUXILIARY POWER
    # =========================================================================

    p_cooling_MW: float = 5.0
    """Cooling system power [MW] for driver electronics and chamber.
    Source: ASSUMED.
    MODERATE UNCERTAINTY."""

    p_fuel_MW: float = 2.0
    """Heavy water circulation and deuterium replenishment power [MW].
    No tritium handling required for D-D fuel.
    Source: ASSUMED.
    MODERATE UNCERTAINTY."""

    p_house_MW: float = 3.0
    """Housekeeping / facility power [MW].
    Source: 1costingfe ife_zpinch.yaml default."""

    p_controls_MW: float = 2.0
    """Driver control, diagnostics, and monitoring power [MW].
    Source: ASSUMED.
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

    construction_time_years: float = 5.0
    """Construction period [years].
    Shorter than magnetic confinement (6-8 years) due to simpler chamber.
    Source: ASSUMED — no construction experience exists.
    HIGH UNCERTAINTY."""

    om_rate_fraction: float = 0.020
    """Annual O&M as fraction of overnight capital.
    Lower than accelerator-based systems (2.5%) due to simpler driver technology.
    Source: ASSUMED — no operational experience.
    MODERATE UNCERTAINTY."""

    core_lifetime_FPY: float = 8.0
    """Active region / first-wall lifetime [full-power-years before replacement].
    D-D 2.45 MeV neutrons less damaging than D-T 14.1 MeV.
    Acoustic cavitation erosion is additional unknown wear mechanism.
    Source: ASSUMED — longer than D-T blanket (5 FPY) but erosion uncertain.
    HIGH UNCERTAINTY."""

    # =========================================================================
    # FUEL COSTS
    # =========================================================================

    u_deuterium_per_kg: float = 2175.0
    """Deuterium unit cost [$/kg].
    Heavy water: ~$300-1000/kg depending on purity (>99.8% D₂O).
    Source: 1costingfe costing_constants.yaml, u_deuterium."""

    # =========================================================================
    # REGULATORY
    # =========================================================================

    regulatory_multiplier: float = 1.3
    """Building cost multiplier for D-D nuclear facility regulatory overhead.
    Lower than D-T tokamak value (1.5-2.2×): D-D avoids tritium handling
    and breeding blanket complexity. Lower neutron flux than D-T.
    Source: ASSUMED — analysis.md §S4.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # COMPUTE METHODS
    # =========================================================================

    def _compute_power(self) -> dict:
        """Layer 1: Physics-based power balance from acoustic driver parameters.

        Energy flow (per module):
          Driver power [P_driver] → acoustic energy → cavitation events
          → fusion power [P_fus] → thermal [P_th] → gross electric [P_et]
          → net electric [P_net] = P_et - P_driver - P_aux
        """
        r: dict = {}

        # --- Cavitation event rate ---
        total_rep_rate = self.cavitation_sites * self.rep_rate_per_site_kHz * 1000.0  # events/s
        r["cavitation_rate_per_s"] = total_rep_rate

        # --- Acoustic power delivered to cavitation ---
        p_acoustic = self.driver_power_MW * self.driver_efficiency
        r["p_acoustic"] = p_acoustic

        # --- Fusion power (HYPOTHETICAL) ---
        # Use target Q_sci to derive fusion power from driver power
        # P_fus = Q_sci × P_driver (by definition of scientific Q)
        p_fus = self.Q_sci * self.driver_power_MW
        r["p_fus"] = p_fus

        # Derive actual yield per event from power balance
        actual_yield_per_event = (p_fus * 1e6) / total_rep_rate if total_rep_rate > 0 else 0.0  # J/event
        r["actual_yield_per_event_J"] = actual_yield_per_event
        r["specified_yield_per_event_J"] = self.yield_per_event_J

        # Scientific Q (from target)
        r["Q_sci"] = self.Q_sci

        # D-D energy partition: ~50% neutrons (2.45 MeV), ~50% charged products (p, T, He-3)
        r["p_neutron"] = p_fus * 0.50
        r["p_charged"] = p_fus * 0.50

        # --- Thermal power ---
        # All fusion energy eventually thermalizes in the liquid
        p_th = p_fus * self.M_blanket
        r["p_th"] = p_th

        # --- Gross electric ---
        p_et = p_th * self.eta_th
        r["p_et"] = p_et

        # --- Recirculating power ---
        p_aux = (self.p_cooling_MW + self.p_fuel_MW
                 + self.p_house_MW + self.p_controls_MW)
        r["p_aux"] = p_aux
        p_recirc = self.driver_power_MW + p_aux
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

        # Temperature gap reminder
        r["demonstrated_temp_K"] = 16_000
        r["required_temp_K"] = 100_000_000
        r["temperature_gap_factor"] = 100_000_000 / 16_000

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Chamber geometry volumes using spherical shells.
        Spherical geometry for acoustic wave focusing in liquid-filled chamber."""
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

        Acoustic ICF-specific overrides (marked [OVERRIDE]):
        • C220103: ZERO — no magnetic confinement
        • C220104: ZERO — acoustic driver is heating mechanism
        • C220107: Direct driver capital (not power-scaled formula)
        • C220108: ZERO — continuous liquid-phase operation

        All other sub-accounts use 1costingfe power-scaling laws.
        """
        r: dict = {}

        p_th  = max(power["p_th"], 1.0)
        p_et  = max(power["p_et"], 1.0)
        p_net_safe = max(abs(power["p_net"]) * self.n_mod, 1.0)

        # C220101: Active Region / First Wall (liquid-filled volume)
        # Source: ASSUMED blanket_unit_cost = 0.10 M$/m³ (much cheaper than solid blanket)
        r["C220101"] = (self.blanket_unit_cost
                        * geom["blanket_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220102: Shield (D-D neutrons, 2.45 MeV)
        # Source: 1costingfe shield_unit_cost = 0.74 M$/m³, reduced for lower neutron energy
        r["C220102"] = (0.50  # Reduced from 0.74 for D-D vs D-T
                        * geom["shield_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: Coils — ZERO [OVERRIDE: no magnetic confinement]
        # Acoustic ICF key structural advantage: eliminates largest MFE capital item.
        r["C220103"] = 0.0

        # C220104: Supplementary Heating — ZERO [OVERRIDE]
        # Acoustic driver provides all energy input; no separate heating.
        r["C220104"] = 0.0

        # C220105: Primary Structure
        # Source: 1costingfe structure_unit_cost = 0.15 M$/m³
        r["C220105"] = (0.15
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: Chamber Containment Vessel (pressure vessel, non-vacuum)
        # Source: 1costingfe vessel_unit_cost = 0.72 M$/m³, reduced for non-vacuum
        r["C220106"] = (0.40
                        * geom["vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # C220107: Power Supplies — OVERRIDE with acoustic driver capital cost
        # Ultrasonic transducer array + power electronics + acoustic focusing.
        # ASSUMED MAJOR COST ADVANTAGE vs. lasers/magnets — BUT PHYSICS UNDEMONSTRATED.
        # Source: analysis.md §S5b; EXTREME UNCERTAINTY.
        r["C220107"] = self.driver_capital_M

        # C220108: Target Factory — ZERO [OVERRIDE]
        # Acoustic ICF is a continuous liquid-phase process; no per-shot target fabrication.
        r["C220108"] = 0.0

        # C220109: Direct Energy Converter — not applicable
        r["C220109"] = 0.0

        # C220110: Remote Handling (D-D neutron damage requires RH but simpler than D-T)
        # Source: 1costingfe remote_handling_dt_base = 150 M$ at 1 GWe, reduced for D-D
        r["C220110"] = 80.0 * (p_net_safe / P_NET_REF) ** 0.6

        # C220111: Installation labor
        # Source: 1costingfe installation_frac = 0.14
        reactor_sub = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"])
        r["C220111"] = 0.14 * reactor_sub

        # C220112: Isotope Separation — minimal (D-D fuel, no tritium breeding)
        # Heavy water procurement includes isotope separation cost
        r["C220112"] = 5.0

        r["CAS22_per_module"] = reactor_sub + r["C220111"] + r["C220112"]

        # --- Plant-wide accounts ---
        p_th_total  = power["p_th"] * self.n_mod
        p_net_total = abs(power["p_net"]) * self.n_mod

        # C220200: Coolant Systems (thermal cycle primary + intermediate loops)
        # Source: 1costingfe CAS22 plant-wide formulas
        C220201 = 166.0 * (p_net_total / 1000.0)
        C220202 = 40.6  * (p_th_total  / 3500.0) ** 0.55
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling (no cryoplant for acoustic driver)
        # Source: 1costingfe CAS22 formula (C220301 only, no C220302 cryogenics)
        C220301 = 1.1e-3 * p_th_total
        r["C220300"] = C220301

        # C220400: Radioactive Waste Management (D-D produces less activation than D-T)
        # Source: 1costingfe formula, reduced for D-D
        r["C220400"] = 1.0 * (p_th_total / 1000.0)

        # C220500: Fuel Handling & Storage (D-D, no tritium)
        # Source: 1costingfe fuel_handling_dt_base = 120 M$, heavily reduced for D-D
        r["C220500"] = 30.0 * (p_net_total / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        # Source: 1costingfe formula
        r["C220600"] = 11.5 * (p_net_total / 1000.0) ** 0.8

        # C220700: Instrumentation & Control
        # Source: 1costingfe formula
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
        p_net_safe = max(abs(p_net) * self.n_mod, 1.0)

        # === CAS10: Pre-construction ===
        land_cost     = 0.25 * p_net_safe * 10_000 / 1e6   # $0.25 acres/MWe × $10k/acre
        licensing     = 3.0 if not self.noak else 1.5       # D-D licensing (simpler than D-T)
        r["CAS10"] = (3.0      # site_permits
                      + (4.0 if self.noak else 20.0)        # plant_studies
                      + 2.0    # plant_permits
                      + 1.0    # plant_reports
                      + 1.0    # other_precon
                      + land_cost
                      + licensing)

        # === CAS21: Buildings ===
        # D-D facility building costs (M$ at P_ET_REF = 1100 MW gross electric)
        # Source: 1costingfe building_costs dt column; acoustic chamber hall replaces
        # tokamak reactor building; hot cell reduced (no high-flux PFCs).
        building_items_M = {
            "site_improvements":   85.0,
            "chamber_building":    90.0,   # ASSUMED: acoustic chamber hall (simpler than tokamak)
            "turbine_building":    58.0,
            "hot_cell":            40.0,   # Reduced: D-D lower activation vs. D-T
            "reactor_auxiliaries": 29.0,
            "fuel_storage":         5.0,   # Heavy water storage (no tritium)
            "control_room":        14.0,
            "security":             3.5,
            "ventilation_hvac":    17.0,
            "administration":       9.0,
            "maintenance":         17.0,
            "heat_exchanger":      17.0,
            "power_supply_bldg":   10.0,   # Driver power electronics
            "misc":                 5.0,
        }
        total_bldg_ref = sum(building_items_M.values())
        cas21_raw = total_bldg_ref * p_et / P_ET_REF
        # Apply D-D nuclear regulatory multiplier
        r["CAS21"] = cas21_raw * self.regulatory_multiplier
        r["CAS21_detail"] = {k: v * p_et / P_ET_REF * self.regulatory_multiplier
                             for k, v in building_items_M.items()}

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment (Rankine steam cycle ASSUMED) ===
        # Source: 1costingfe turbine_per_mw = 0.20 M$/MW (Rankine)
        r["CAS23"] = self.n_mod * p_et * 0.20

        # === CAS24: Electric Plant Equipment ===
        # Source: 1costingfe costing_constants.yaml electric_per_mw
        r["CAS24"] = self.n_mod * p_et * 0.08418

        # === CAS25: Misc Plant Equipment ===
        # Source: 1costingfe costing_constants.yaml misc_per_mw
        r["CAS25"] = self.n_mod * p_et * 0.05124

        # === CAS26: Heat Rejection ===
        # Source: 1costingfe heat_rej_per_mw
        r["CAS26"] = self.n_mod * p_et * 0.03416

        # === CAS27: Special Materials (heavy water initial fill) ===
        # Source: ASSUMED — heavy water inventory for liquid-filled chamber
        # Heavy water: ~$500/kg; assume 100 m³ fill = 100,000 kg ≈ $50M
        r["CAS27"] = 50.0 * (p_net_safe / P_NET_REF) ** 0.5

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
        # Source: 1costingfe owner_cost_dt = 39 M$ at 1 GWe, reduced for D-D
        r["CAS40"] = 30.0 * (p_net_safe / P_NET_REF) ** 0.5

        # === CAS50: Supplementary Costs ===
        # Source: 1costingfe spare_parts_frac_dt = 0.03
        spare_parts   = 0.03 * sum(r[k] for k in ["CAS22", "CAS23", "CAS24",
                                                    "CAS25", "CAS26", "CAS27", "CAS28"])
        # Source: 1costingfe shipping_frac=0.015, tax_frac=0.01, insurance=0.015
        shipping      = 0.015 * r["CAS20"]
        taxes         = 0.010 * r["CAS20"]
        insurance     = 0.015 * (r["CAS20"] + r["CAS30"])
        # Source: 1costingfe decom_provision_dt = 127 M$ at 1 GWe, reduced for D-D
        decom         = 80.0 * (p_net_safe / P_NET_REF) ** 0.5
        r["CAS50"] = spare_parts + shipping + taxes + insurance + decom

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

        # === CAS72: Scheduled Replacement (active region / first wall) ===
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

        # === CAS80: Fuel & Consumables (D-D; deuterium only) ===
        # Deuterium consumption: 2 D atoms per D-D fusion, M_D = 2 amu
        # D-D reactions produce: (1) D + D → T + p  OR  (2) D + D → He-3 + n
        # Both consume 2 D atoms per fusion
        M_D2_kg = 4 * AMU_KG  # 2 D atoms = 4 amu
        seconds_per_year = 8760 * 3600 * self.plant_availability
        fusion_rate_total = power["cavitation_rate_per_s"]  # events/s (assuming 1 fusion per event)
        annual_D2_kg = fusion_rate_total * M_D2_kg * seconds_per_year
        r["CAS80"] = annual_D2_kg * self.u_deuterium_per_kg / 1e6   # M$/yr
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
        """Compute CAS-structured LCOE from speculative physics first principles.

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
# CRITICAL: This module computes speculative corridor values for cross-concept
# comparison only. The "native power" (~102 MWe) and all cost parameters are
# INVENTED assumptions, not extracted from company-disclosed design-point data.
# Under the D1+ analysis contract, this model should not exist until Sonofusion
# Energy discloses a native power target and upstream tables assign an archetype.
# These values are retained for comparison infrastructure testing only.
# ============================================================================
params  = AcousticICFPlantParams()
results = params.compute()

_ALPHA    = 0.6   # economy-of-scale exponent (standard cross-concept scaling)
_p_native = results["power"].get("p_net_plant", results["power"]["p_net"])  # ~102 MWe SPECULATIVE

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

def print_results(p: AcousticICFPlantParams, r: dict) -> None:
    """Pretty-print the full LCOE model results with CAS-structured accounting."""
    pw    = r["power"]
    cas22 = r["cas22"]
    costs = r["costs"]
    econ  = r["economics"]

    print("=" * 80)
    print("Acoustic ICF (Sonofusion) Speculative LCOE Corridor — Sonofusion Energy")
    print("1cFE CAS-Structured Model — FOR COMPARISON PURPOSES ONLY")
    print("=" * 80)

    # Critical disclaimer
    print()
    print("  ╔════════════════════════════════════════════════════════════════════╗")
    print("  ║  CRITICAL: THIS IS NOT A CREDIBLE COST ESTIMATE                   ║")
    print("  ║                                                                    ║")
    print("  ║  This model exists ONLY for cross-concept comparison corridor     ║")
    print("  ║  purposes IF the fundamental physics were demonstrated. It is NOT ║")
    print("  ║  a validated techno-economic analysis.                            ║")
    print("  ║                                                                    ║")
    print("  ║  BLOCKING ISSUES:                                                 ║")
    print("  ║  • No design point specified by Sonofusion Energy                 ║")
    print("  ║  • No native power target disclosed (102 MWe is INVENTED)         ║")
    print("  ║  • No archetype assigned (upstream: Archetype = [empty])          ║")
    print("  ║  • Fundamental physics undemonstrated (see below)                 ║")
    print("  ║                                                                    ║")
    print("  ║  Under D1+ analysis contract, models require validated design     ║")
    print("  ║  point data BEFORE modeling. This concept has none.               ║")
    print("  ╚════════════════════════════════════════════════════════════════════╝")
    print()
    print("  ╔════════════════════════════════════════════════════════════════════╗")
    print("  ║  PHYSICS DEMONSTRATION GAP (ABSOLUTE BLOCKER)                     ║")
    print("  ║  Best demonstrated temp:  16,000 K (sonoluminescence)             ║")
    print(f"  ║  D-D fusion requirement:  {pw['required_temp_K']:,} K                     ║")
    print(f"  ║  Temperature gap:         {pw['temperature_gap_factor']:.0f}× (4 orders of magnitude)          ║")
    print("  ║                                                                    ║")
    print("  ║  No credible evidence that acoustic cavitation can achieve        ║")
    print("  ║  fusion-relevant plasma conditions. Taleyarkhan bubble fusion     ║")
    print("  ║  claims were discredited. UCLA Putterman group (30+ years         ║")
    print("  ║  sonoluminescence research) has found NO fusion neutrons.         ║")
    print("  ║                                                                    ║")
    print("  ║  ALL PARAMETERS IN THIS MODEL ARE SPECULATIVE ASSUMPTIONS.        ║")
    print("  ╚════════════════════════════════════════════════════════════════════╝")
    print()

    # Viability warning
    if pw["p_net"] <= 0:
        print("  *** ENERGY SINK: Net electric is NEGATIVE at these parameters. ***")
        print("  *** Q_sci × M × η_th < 1 — no net power output. ***")
        print("  *** LCOE is undefined. Driver consumes more than plant generates. ***")
        print()

    # --- Key Physics Inputs ---
    print(f"\n--- Key Physics Parameters (INVENTED FOR CORRIDOR PURPOSES) ---")
    print(f"  (NOT extracted from Sonofusion Energy disclosures)")
    print(f"  Driver power:                 {p.driver_power_MW:.1f} MW [ASSUMED]")
    print(f"  Driver efficiency:            {p.driver_efficiency:.1%} [ASSUMED]")
    print(f"  Driver frequency:             {p.driver_frequency_kHz:.1f} kHz [from literature, not reactor]")
    print(f"  Cavitation sites:             {p.cavitation_sites:,} [ASSUMED]")
    print(f"  Rep rate per site:            {p.rep_rate_per_site_kHz:.1f} kHz [ASSUMED]")
    print(f"  Yield per event:              {p.yield_per_event_J:.2e} J/event [ASSUMED]")
    print(f"  Scientific Q (Q_sci):         {pw['Q_sci']:.3f}  (target: {p.Q_sci:.1f}) [ASSUMED]")
    print(f"  Blanket multiplication M:     {p.M_blanket:.2f} [ASSUMED]")
    print(f"  Thermal efficiency η_th:      {p.eta_th:.1%} [ASSUMED]")
    print(f"  Plant availability:           {p.plant_availability:.0%} [ASSUMED]")
    print(f"  Modules:                      {p.n_mod} [ASSUMED]")
    print(f"  → Native power (derived):     ~{pw['p_net_plant']:.0f} MWe [NO COMPANY TARGET]")

    # --- Power Balance ---
    print(f"\n--- Power Balance (per module) — FROM SPECULATIVE ASSUMPTIONS ---")
    print(f"  Cavitation rate:              {pw['cavitation_rate_per_s']:.2e} events/s [ASSUMED]")
    print(f"  Acoustic power delivered:     {pw['p_acoustic']:>8.1f} MW")
    print(f"  Fusion power (P_fus):         {pw['p_fus']:>8.1f} MW  [HYPOTHETICAL — physics undemonstrated]")
    print(f"    Neutron power (~50%):       {pw['p_neutron']:>8.1f} MW (2.45 MeV D-D → liquid)")
    print(f"    Charged power (~50%):       {pw['p_charged']:>8.1f} MW (p, T, He-3 → liquid)")
    print(f"  Thermal power (P_th):         {pw['p_th']:>8.1f} MW  (× M={p.M_blanket})")
    print(f"  Gross electric (P_et):        {pw['p_et']:>8.1f} MWe (× η={p.eta_th:.1%})")
    print(f"  Recirculating power:")
    print(f"    Driver:                     {p.driver_power_MW:>8.1f} MW")
    print(f"    Auxiliaries:                {pw['p_aux']:>8.1f} MW")
    print(f"    Total recirculating:        {pw['p_recirc']:>8.1f} MW")
    print(f"  Net electric (P_net):         {pw['p_net']:>8.1f} MWe")
    print(f"  Plant net electric:           {pw['p_net_plant']:>8.1f} MWe [NO COMPANY TARGET — INVENTED]")
    print(f"  Engineering Q (Q_eng):        {pw['Q_eng']:>8.3f}")
    print(f"  Recirculating fraction (ε):   {pw['recirc_fraction']:>8.1%}")

    # --- CAS22 ---
    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    cas22_labels = {
        "C220101": ("Active Region / First Wall",    ""),
        "C220102": ("Shield (D-D neutrons)",         ""),
        "C220103": ("Coils",                         "[ZERO — no magnetic confinement]"),
        "C220104": ("Supplementary Heating",         "[ZERO — acoustic driver]"),
        "C220105": ("Primary Structure",             ""),
        "C220106": ("Chamber Containment",           ""),
        "C220107": ("Acoustic Driver System",        "[OVERRIDE — key cost advantage]"),
        "C220108": ("Target Factory",                "[ZERO — continuous liquid phase]"),
        "C220110": ("Remote Handling",               ""),
        "C220111": ("Installation Labor",            ""),
        "C220112": ("Isotope Separation",            ""),
    }
    for code, (label, note) in cas22_labels.items():
        val = cas22.get(code, 0.0)
        if val != 0.0 or note:
            print(f"    {code} {label:<36s} ${val:>8.1f}M  {note}")
    print(f"    {'─' * 66}")
    print(f"    Per-module subtotal:                         ${cas22['CAS22_per_module']:>8.1f}M × {p.n_mod}")

    pw_labels = {
        "C220200": "Coolant Systems (thermal cycle)",
        "C220300": "Aux Cooling",
        "C220400": "Rad Waste Management (D-D)",
        "C220500": "Fuel Handling (heavy water)",
        "C220600": "Other Equipment",
        "C220700": "I&C",
    }
    print(f"  Plant-wide accounts:")
    for code, label in pw_labels.items():
        val = cas22[code]
        if val > 0.01:
            print(f"    {code} {label:<40s} ${val:>8.1f}M")
    print(f"    {'─' * 66}")
    print(f"    Plant-wide subtotal:                         ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                                   ${cas22['CAS22']:>8.1f}M")

    # --- Capital Costs ---
    print(f"\n--- Capital Costs (CAS10–60) ---")
    print(f"  CAS10 Pre-construction:                        ${costs['CAS10']:>8.1f}M")
    print(f"  CAS21 Buildings (×{p.regulatory_multiplier:.1f}× reg. mult.):           ${costs['CAS21']:>8.1f}M")
    print(f"  CAS22 Reactor Plant Equipment:                 ${costs['CAS22']:>8.1f}M")
    print(f"  CAS23 Turbine Plant (Rankine):                 ${costs['CAS23']:>8.1f}M")
    print(f"  CAS24 Electric Plant:                          ${costs['CAS24']:>8.1f}M")
    print(f"  CAS25 Misc Plant:                              ${costs['CAS25']:>8.1f}M")
    print(f"  CAS26 Heat Rejection:                          ${costs['CAS26']:>8.1f}M")
    print(f"  CAS27 Special Materials (heavy water):         ${costs['CAS27']:>8.1f}M")
    print(f"  CAS28 Digital Twin:                            ${costs['CAS28']:>8.1f}M")
    print(f"  CAS29 Contingency:                             ${costs['CAS29']:>8.1f}M")
    print(f"  {'─' * 68}")
    print(f"  CAS20 Direct Costs:                            ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30 Indirect Costs:                          ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40 Owner's Costs:                           ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50 Supplementary:                           ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 68}")
    print(f"  Overnight Capital:                             ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60 IDC (f={costs['f_IDC']:.3f}):                     ${costs['CAS60']:>8.1f}M")
    print(f"  {'═' * 68}")
    print(f"  Total Capital:                                 ${costs['total_capital']:>8.1f}M")
    if pw["p_net"] > 0:
        print(f"  Specific Capital:                        ${costs['specific_capital_USD_per_kWe']:>10,.0f} $/kWe")

    # --- Annual Costs ---
    print(f"\n--- Annual Costs (CAS70–90) ---")
    print(f"  CAS90 Capital charge (CRF={econ['CRF']:.4f}):         ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71 O&M (levelized, {p.om_rate_fraction:.1%}/yr):          ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72 Active region replacements ({econ['n_replacements']} over life): ${econ['CAS72']:>8.1f}M/yr")
    print(f"  CAS70 Total O&M:                               ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80 Fuel (deuterium, D-D):                   ${econ['CAS80']:>8.4f}M/yr")

    # --- LCOE (SPECULATIVE CORRIDOR) ---
    print(f"\n--- LCOE (SPECULATIVE CORRIDOR — NOT A CREDIBLE ESTIMATE) ---")
    if pw["p_net"] > 0:
        print(f"  Annual energy production:     {econ['annual_energy_MWh']:>12,.0f} MWh/yr")
        print(f"  Annual revenue requirement:   ${econ['annual_revenue_req']:>8.1f}M/yr")
        print(f"  ╔═══════════════════════════════════════════════════╗")
        print(f"  ║  CORRIDOR LCOE = {econ['lcoe_cents_per_kWh']:>7.1f} ¢/kWh (at ~102 MWe)  ║")
        print(f"  ║               = {econ['lcoe_USD_per_MWh']:>7.1f} $/MWh                    ║")
        print(f"  ║                                                   ║")
        print(f"  ║  NOT EXTRACTED FROM COMPANY DATA                  ║")
        print(f"  ║  Assumes Q_sci=5.0, driver=$150M, other invented ║")
        print(f"  ║  parameters. For comparison purposes only.        ║")
        print(f"  ╚═══════════════════════════════════════════════════╝")
        print(f"  Capital (CAS90):              {econ.get('capital_fraction', 0):.1%}")
        print(f"  O&M    (CAS70):               {econ.get('om_fraction', 0):.1%}")
        print(f"  Fuel   (CAS80):               {econ.get('fuel_fraction', 0):.2%}")

        if _p_native > 0:
            _f = (_p_native / 1000.0) ** (1.0 - _ALPHA)
            print(f"\n--- Scaled to 1000 MWe Reference (α=0.6) ---")
            print(f"  (Corridor scaling from speculative 102 MWe native)")
            print(f"  Scale factor:    ({_p_native:.0f}/1000)^{1-_ALPHA:.1f} = {_f:.3f}")
            print(f"  Scaled LCOE:     {econ['lcoe_USD_per_MWh'] * _f:.1f} $/MWh"
                  f"  ({econ['lcoe_cents_per_kWh'] * _f:.2f} ¢/kWh)")
    else:
        print(f"  LCOE: UNDEFINED — net electric is negative.")
        print(f"  Plant is an energy sink. LCOE is infinite.")

    print()
    print("=" * 80)


def sensitivity_sweep(base_params: AcousticICFPlantParams,
                      param_name: str,
                      values: list,
                      label: str = "") -> list[dict]:
    """Sweep a single parameter and return LCOE and net power for each value."""
    out = []
    for val in values:
        p = AcousticICFPlantParams(**{**base_params.__dict__, param_name: val})
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
        v = row["param_value"]
        q = row["Q_sci"]
        p = row["net_electric_MW"]
        e = row["recirc_fraction"]
        lcoe_c = row["lcoe_cents_kWh"]

        v_str = f"{v:>12.2f}" if isinstance(v, float) else f"{v:>12}"
        q_str = f"{q:>7.2f}"
        p_str = f"{p:>8.1f} MW" if p > 0 else "   (sink)"
        e_str = f"{e:>6.1%}" if p > 0 else "   —"

        if lcoe_c == float('inf'):
            lcoe_str = "     (infinite)"
        elif lcoe_c > 9999:
            lcoe_str = f"     >{9999:.0f} ¢/kWh"
        else:
            lcoe_str = f"     {lcoe_c:>6.1f} ¢/kWh"

        print(f"  {v_str}  {q_str}  {p_str}  {e_str}  {lcoe_str}")


def main():
    """Generate baseline results and sensitivity analysis."""

    print("\n" + "=" * 80)
    print("BASELINE SCENARIO")
    print("=" * 80)
    print_results(params, results)

    print("\n\n" + "=" * 80)
    print("SENSITIVITY ANALYSIS")
    print("=" * 80)

    # 1. Driver capital cost (EXTREME UNCERTAINTY)
    sweep_driver_cap = sensitivity_sweep(
        params, "driver_capital_M",
        [50.0, 100.0, 150.0, 250.0, 500.0, 1000.0],
        "Driver capital cost"
    )
    _print_sweep(sweep_driver_cap, "Driver Capital Cost", "M$")

    # 2. Scientific Q (PHYSICS UNDEMONSTRATED)
    sweep_qsci = sensitivity_sweep(
        params, "Q_sci",
        [1.0, 2.0, 3.0, 5.0, 10.0, 20.0],
        "Scientific Q"
    )
    _print_sweep(sweep_qsci, "Scientific Q (fusion out / acoustic in)", "")

    # 3. Yield per event (PHYSICS UNDEMONSTRATED)
    sweep_yield = sensitivity_sweep(
        params, "yield_per_event_J",
        [1e-10, 5e-10, 1e-9, 5e-9, 1e-8],
        "Yield per cavitation event"
    )
    _print_sweep(sweep_yield, "Yield per Cavitation Event", "J/event")

    # 4. Cavitation sites (EXTREME UNCERTAINTY)
    sweep_sites = sensitivity_sweep(
        params, "cavitation_sites",
        [100_000, 500_000, 1_000_000, 5_000_000, 10_000_000],
        "Number of cavitation sites"
    )
    _print_sweep(sweep_sites, "Number of Simultaneous Cavitation Sites", "")

    # 5. Driver power (HIGH UNCERTAINTY)
    sweep_driver_pwr = sensitivity_sweep(
        params, "driver_power_MW",
        [20.0, 30.0, 50.0, 75.0, 100.0, 150.0],
        "Driver power"
    )
    _print_sweep(sweep_driver_pwr, "Driver Electrical Power", "MW")

    # 6. Thermal efficiency (MODERATE UNCERTAINTY)
    sweep_eta = sensitivity_sweep(
        params, "eta_th",
        [0.25, 0.30, 0.35, 0.40, 0.45],
        "Thermal efficiency"
    )
    _print_sweep(sweep_eta, "Thermal-to-Electric Efficiency", "")

    print("\n\n" + "=" * 80)
    print("SCENARIO COMPARISON")
    print("=" * 80)

    # Conservative: High costs, low performance, physics barely works
    conservative = AcousticICFPlantParams(
        driver_capital_M=500.0,
        Q_sci=2.0,
        yield_per_event_J=5e-10,
        cavitation_sites=500_000,
        driver_power_MW=75.0,
        eta_th=0.30,
        plant_availability=0.70,
    )

    # Moderate: Baseline parameters (already set)
    moderate = params

    # Optimistic: Low costs, high performance, physics breakthrough
    optimistic = AcousticICFPlantParams(
        driver_capital_M=75.0,
        Q_sci=10.0,
        yield_per_event_J=5e-9,
        cavitation_sites=5_000_000,
        driver_power_MW=30.0,
        eta_th=0.40,
        plant_availability=0.85,
    )

    scenarios = [
        ("Conservative", conservative),
        ("Moderate (Baseline)", moderate),
        ("Optimistic", optimistic),
    ]

    print("\n  Scenario Comparison Table:")
    print(f"  {'Scenario':<24} {'P_net':<10} {'Q_sci':<8} {'LCOE':<16} {'$/kWe':<12}")
    print(f"  {'─'*24} {'─'*10} {'─'*8} {'─'*16} {'─'*12}")

    for name, p_scenario in scenarios:
        r = p_scenario.compute()
        pw = r["power"]
        econ = r["economics"]
        costs = r["costs"]

        p_net = pw["p_net_plant"]
        q_sci = pw["Q_sci"]
        lcoe_c = econ["lcoe_cents_per_kWh"]
        cap_per_kwe = costs["specific_capital_USD_per_kWe"]

        p_str = f"{p_net:>8.0f} MW" if p_net > 0 else "   (sink)"
        q_str = f"{q_sci:>6.2f}"

        if lcoe_c == float('inf'):
            lcoe_str = "(infinite)"
        elif lcoe_c > 999:
            lcoe_str = f">{999:.0f} ¢/kWh"
        else:
            lcoe_str = f"{lcoe_c:>6.1f} ¢/kWh"

        if cap_per_kwe == float('inf'):
            cap_str = "(infinite)"
        elif cap_per_kwe > 99999:
            cap_str = f">${99999:,.0f}"
        else:
            cap_str = f"${cap_per_kwe:>10,.0f}"

        print(f"  {name:<24} {p_str:<10} {q_str:<8} {lcoe_str:<16} {cap_str:<12}")

    print("\n\n" + "=" * 80)
    print("KEY BINDING CONSTRAINTS (in order of impact)")
    print("=" * 80)

    print("""
1. PHYSICS DEMONSTRATION GAP (ABSOLUTE BLOCKER)
   Best demonstrated sonoluminescence temp: 16,000 K
   D-D fusion requirement: 100,000,000 K
   Gap: 6,000× (4 orders of magnitude)

   Impact: ALL parameters in this model are speculative until acoustic
           cavitation is demonstrated to achieve fusion-relevant plasma
           conditions. The Taleyarkhan bubble fusion claims (2002-2008)
           were discredited and never independently replicated. The UCLA
           Putterman group (30+ years sonoluminescence expertise) has
           found NO evidence of fusion neutrons from acoustic cavitation.

   Resolution pathway: Peer-reviewed experimental demonstration of
                      >10 keV (>100 million K) ion temperatures via
                      acoustic bubble collapse, independently replicated.

2. SCIENTIFIC GAIN (Q_sci)
   Baseline: 5.0 (pure speculation, no experimental basis)
   Sensitivity: LCOE ∝ 1/Q_sci approximately

   Impact: At Q_sci = 2.0 (conservative), LCOE >> $100/MWh.
           At Q_sci = 10.0 (optimistic), LCOE ~ $40-60/MWh.

   Q_sci is the fusion energy produced per unit acoustic energy delivered.
   It depends on: (1) whether fusion occurs at all, (2) the number of
   fusions per cavitation event, and (3) the acoustic coupling efficiency.
   All three are unknown and undemonstrated.

3. DRIVER CAPITAL COST
   Baseline: $150M (ASSUMED cost advantage vs. lasers/magnets)
   Range: $50M-$5,000M (20× uncertainty)
   Sensitivity: LCOE varies by ~factor of 3 across this range

   Impact: Ultrasonic transducers are commodity industrial equipment at
           kW-scale, but fusion-relevant power levels and duty cycles are
           unknown. If driver cost approaches laser system costs ($2B+),
           the concept loses its primary economic advantage.

   The cost advantage (orders of magnitude cheaper driver than laser ICF
   or magnetic confinement) is the ONLY reason to pursue acoustic ICF IF
   the fundamental physics were demonstrated. Without this cost advantage,
   there is no economic rationale vs. established approaches.
""")

    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
