"""
Polomac Magnetic Confinement (Deutelio) Freeform LCOE Model
============================================================
Concept: Poloidal magnetic confinement with magnetic tunnel supports
Company: Deutelio

╔═══════════════════════════════════════════════════════════════════════════════╗
║ CRITICAL: THIS IS NOT A CREDIBLE COST ESTIMATE                               ║
║                                                                               ║
║ This model exists ONLY to establish a speculative LCOE corridor for          ║
║ cross-concept comparison purposes IF the fundamental physics demonstration    ║
║ gap were somehow overcome. It is NOT a validated techno-economic analysis.    ║
║                                                                               ║
║ BLOCKING ISSUES:                                                              ║
║ • No design point specified by Deutelio (no P_native, no specs)              ║
║ • No archetype assigned (upstream tables: Archetype = [empty])                ║
║ • No comparables list (analysis frontmatter: Comparables = [])                ║
║ • Fundamental physics undemonstrated (magnetic tunnel concept)                ║
║ • Power balance unknown (Q_eng, recirculating power fraction undefined)      ║
║                                                                               ║
║ Under the analysis contract, quantitative models require validated design-    ║
║ point data and archetype assignment BEFORE modeling. This concept has        ║
║ neither. All parameters are SPECULATIVE ASSUMPTIONS for corridor purposes.   ║
╚═══════════════════════════════════════════════════════════════════════════════╝

PHYSICS DEMONSTRATION GAP (ABSOLUTE BLOCKER):
    Magnetic tunnel concept has NEVER been experimentally demonstrated.
    Particle loss rates through tunnels are unquantified.
    Confinement advantage over tokamaks (2-3× lower field) is unvalidated.
    Temperature gap: 100 eV prototype → 8.1 keV D-T reactor (~80× increase)

    2014 design had 700 MW coil power consumption (excessive for steady state).
    2024 report mentions superconducting magnets but provides no Q_eng analysis.

This model assumes hypothetical breakthrough physics and transition to
superconducting coils. ALL PARAMETERS ARE HIGHLY SPECULATIVE. The native
power level, fusion power, Q_eng, and all cost parameters are INVENTED for
modeling corridor purposes, NOT extracted from company-disclosed specifications.

Key references:
    analysis.md — Phase 1a analysis documenting data gaps
    [analyses/35-polomac-magnetic-confinement/analysis.md]

    jtsp-2024-polomac-technical-report.md — Primary technical source
    [knowledge/concept_research/35-polomac-magnetic-confinement/sources/...]

    elio-2014-fed-poloidal-confinement.md — Foundational paper
    [knowledge/concept_research/35-polomac-magnetic-confinement/sources/...]

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass

# ============================================================================
# Physical constants
# ============================================================================
E_FUSION_DT_MEV = 17.6                        # D-T fusion energy [MeV]
E_FUSION_J = E_FUSION_DT_MEV * 1e6 * 1.602e-19  # D-T energy [J]
AMU_KG = 1.66053906660e-27                    # 1 atomic mass unit [kg]

# ============================================================================
# Reference power levels for 1costingfe scaling laws
# ============================================================================
P_TH_REF  = 2500.0   # Reference thermal power [MW]
P_ET_REF  = 1100.0   # Reference gross electric power [MW]
P_NET_REF = 1000.0   # Reference net electric power [MW]


@dataclass
class PolomacPlantParams:
    """
    Parameterized Polomac Magnetic Confinement power plant model.

    Architecture overview (SPECULATIVE — no disclosed design):
    ┌──────────────────────────────────────────────────────┐
    │  Poloidal dipole field (internal coil + external)     │
    │  Magnetic tunnel supports (field-free channels)       │
    │       ↓                                              │
    │  [UNVALIDATED] Plasma confinement at 2-3 T field     │
    │       ↓ [PHYSICS GAP: 100 eV → 8.1 keV demonstrated] │
    │  [HYPOTHETICAL] D-T fusion → neutrons + alpha        │
    │       ↓                                              │
    │  Neutrons → blanket → thermal energy                 │
    │  Alpha → plasma heating                              │
    │       ↓                                              │
    │  Thermal cycle (ASSUMED: Rankine or sCO2) → electric │
    │       ↓                                              │
    │  Net electric = Gross - Recirculating (coils + aux)  │
    └──────────────────────────────────────────────────────┘

    Key structural differences from standard MFE:
    • Lower magnetic field (2-3 T vs 5+ T tokamak) — IF physics works
    • Magnetic tunnel penetrations — unique structural challenges
    • Large plasma volume (1300 m³ from 2014 design)
    • Steady-state operation (no disruptions)
    • High beta (20-30%) claimed

    Uncertainty tiers used in docstrings:
    • (no tag)             — well-established physics or engineering constant
    • MODERATE UNCERTAINTY — reasonable estimate from documented analogues
    • HIGH UNCERTAINTY     — speculative or poorly constrained
    • EXTREME UNCERTAINTY  — pure speculation, no credible basis
    • PHYSICS UNDEMONSTRATED — fundamental gap, no experimental evidence
    """

    # =========================================================================
    # PLASMA PARAMETERS (D-T PATHWAY)
    # =========================================================================

    B_field_T: float = 2.5
    """On-axis magnetic field [T].
    D-T pathway: 2-3 T claimed (analysis §S5).
    Lower than ITER (5.3 T) or HTS tokamaks (12-20 T).
    Source: jtsp-2024-polomac-technical-report.md §V.
    HIGH UNCERTAINTY — unvalidated claim of 2-3× lower field for equivalent performance."""

    plasma_volume_m3: float = 1300.0
    """Plasma volume [m³].
    From 2014 conceptual design (elio-2014-fed-poloidal-confinement.md §Coil support).
    Much larger than compact tokamaks (ARC ~60 m³).
    Source: elio-2014-fed-poloidal-confinement.md.
    MODERATE UNCERTAINTY — 2014 value, no updated reactor-scale volume in 2024 report."""

    beta: float = 0.25
    """Plasma beta (pressure / magnetic pressure) [fraction].
    Analysis §S5: 20-30% from past poloidal experiments.
    High beta is key claimed advantage.
    Source: elio-2014-fed-poloidal-confinement.md §Introduction.
    HIGH UNCERTAINTY — past experiments were at much lower field and temperature."""

    ion_temp_keV: float = 8.1
    """Ion temperature [keV].
    D-T standard fusion temperature.
    Source: jtsp-2024-polomac-technical-report.md §V.
    MODERATE UNCERTAINTY — standard value, but achieving it is undemonstrated."""

    density_m3: float = 1e20
    """Plasma density [m⁻³].
    D-T pathway: 10²⁰ m⁻³ (analysis §S5).
    Comparable to tokamak density.
    Source: jtsp-2024-polomac-technical-report.md §V.
    MODERATE UNCERTAINTY."""

    tau_E_s: float = 4.5
    """Energy confinement time [s].
    D-T pathway: 4-5 s claimed (analysis §S5).
    Comparable to ITER target.
    Source: jtsp-2024-polomac-technical-report.md §V.
    HIGH UNCERTAINTY — no experimental basis for magnetic tunnel confinement."""

    # =========================================================================
    # FUSION POWER (HYPOTHETICAL — POWER BALANCE UNKNOWN)
    # =========================================================================

    p_fus_MW: float = 400.0
    """Fusion power [MW].
    SPECULATIVE VALUE chosen to produce ~100 MWe plant at Q_eng ~ 5.
    No fusion power estimate exists in sources.
    Source: ASSUMED — corridor parameter.
    EXTREME UNCERTAINTY — no power balance analysis exists."""

    Q_sci: float = 10.0
    """Scientific gain: fusion power / heating power.
    ASSUMED value typical of D-T magnetic confinement targets.
    Source: ASSUMED — no heating system or Q_sci disclosed.
    PHYSICS UNDEMONSTRATED — heating method for reactor scale unknown."""

    # =========================================================================
    # ENERGY CAPTURE & CONVERSION
    # =========================================================================

    M_blanket: float = 1.15
    """Energy multiplication factor (tritium breeding blanket).
    D-T blanket with Li-6 breeding: M ~ 1.1-1.2.
    Source: Standard D-T blanket value.
    MODERATE UNCERTAINTY — no blanket design for Polomac geometry."""

    eta_th: float = 0.35
    """Thermal-to-electric conversion efficiency [fraction].
    Analysis §S5: "350°C" target for electricity generation.
    ASSUMED Rankine steam cycle at moderate temperature.
    Source: jtsp-2024-polomac-technical-report.md §VII; ASSUMED cycle.
    MODERATE UNCERTAINTY — no power cycle specified."""

    # =========================================================================
    # MAGNETIC SYSTEM
    # =========================================================================

    magnet_stored_energy_MJ: float = 5000.0
    """Stored magnetic energy [MJ].
    For 1300 m³ plasma at 2.5 T, E_mag ~ B²V/(2μ₀) ~ 3000-6000 MJ.
    Much lower than ITER (~50 GJ at 5.3 T) due to lower field.
    Source: CALCULATED from B²V scaling.
    MODERATE UNCERTAINTY."""

    p_coil_MW: float = 15.0
    """Steady-state coil power consumption [MW].
    ASSUMES superconducting magnets (cryo power + control).
    2014 design had 700 MW for copper coils (excessive).
    2024 report mentions superconducting transition but no power analysis.
    Source: ASSUMED — superconducting cryo load.
    HIGH UNCERTAINTY — no disclosed superconducting coil design."""

    # =========================================================================
    # HEATING & CURRENT DRIVE (REACTOR SCALE)
    # =========================================================================

    p_heating_MW: float = 40.0
    """Auxiliary heating power [MW].
    Derived from P_fus / Q_sci = 400 MW / 10 = 40 MW.
    Heating method for 8.1 keV D-T in poloidal geometry is unknown.
    Small prototype uses 5-10 kW ECRH at 4 GHz (not scalable to reactor).
    Source: DERIVED from assumed Q_sci.
    EXTREME UNCERTAINTY — no reactor-scale heating system specified."""

    # =========================================================================
    # AUXILIARY POWER
    # =========================================================================

    p_cooling_MW: float = 8.0
    """Cooling system power [MW] for magnets, blanket, shields.
    Source: ASSUMED from tokamak analogues.
    MODERATE UNCERTAINTY."""

    p_fuel_MW: float = 3.0
    """Tritium fuel cycle power [MW] (if D-T operation).
    Includes tritium extraction, processing, recycling.
    Source: ASSUMED from D-T tokamak analogues.
    MODERATE UNCERTAINTY."""

    p_house_MW: float = 5.0
    """Housekeeping / facility power [MW].
    Source: Standard MFE plant estimate.
    MODERATE UNCERTAINTY."""

    p_controls_MW: float = 2.0
    """Control, diagnostics, and monitoring power [MW].
    Source: ASSUMED.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # PLANT CONFIGURATION
    # =========================================================================

    n_mod: int = 1
    """Number of fusion modules per plant.
    Large plasma volume (1300 m³) suggests single-module design.
    Source: ASSUMED — poloidal dipole is integrated device.
    MODERATE UNCERTAINTY."""

    plant_availability: float = 0.80
    """Plant capacity factor / availability [fraction].
    Lower than baseload thermal plants (85-90%) due to technology immaturity.
    Steady-state operation avoids pulsed tokamak downtime.
    Source: ASSUMED.
    MODERATE UNCERTAINTY."""

    plant_lifetime_years: float = 40.0
    """Plant economic lifetime [years].
    Source: Standard fusion plant assumption."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds 10% contingency on direct costs."""

    # =========================================================================
    # CAPITAL — MAGNET SYSTEM (C220103 OVERRIDE)
    # =========================================================================

    magnet_capital_M: float = 180.0
    """Capital cost of superconducting magnet system (internal dipole + external coils) [$M].
    Maps to C220103 (Coils) — CONCEPT-SPECIFIC.
    Lower field (2.5 T) vs tokamak (5+ T) or HTS compact (12-20 T) enables lower cost.
    ASSUMED: LTS (NbTi/Nb3Sn) at 2.5 T rather than HTS.
    Analogues: ITER magnets ~€1B at 5.3 T; Polomac 2.5 T should be cheaper.
    BUT: Magnetic tunnel geometry creates unique structural challenges.
    Source: ASSUMED — lower field advantage, but no disclosed magnet design.
    HIGH UNCERTAINTY — range $100M-$500M depending on tunnel integration."""

    # =========================================================================
    # CHAMBER & GEOMETRY
    # =========================================================================

    major_radius_m: float = 7.0
    """Approximate major radius [m] for dipole field geometry.
    Derived from 1300 m³ plasma volume assuming toroidal-like geometry.
    V ~ 2π²Rₘₐⱼ × r² → R ~ (V/(2π²r²))^(1/3) ~ 6-8 m for r ~ 2-3 m.
    Source: DERIVED from plasma volume.
    HIGH UNCERTAINTY — no geometric parameters in sources."""

    blanket_thickness_m: float = 0.60
    """Tritium breeding blanket thickness [m].
    D-T blanket for neutron absorption and tritium production.
    Standard thickness for 14.1 MeV D-T neutrons.
    Source: Standard D-T blanket value.
    MODERATE UNCERTAINTY — no blanket design for magnetic tunnel geometry."""

    shield_thickness_m: float = 0.80
    """Neutron shielding thickness [m].
    D-T 14.1 MeV neutrons require substantial shielding.
    Magnetic tunnels may create neutron streaming paths.
    Source: ASSUMED from tokamak analogues.
    HIGH UNCERTAINTY — tunnel streaming effects unknown."""

    structure_thickness_m: float = 0.50
    """Primary structure thickness [m].
    Magnetic tunnel supports require non-standard structural design.
    Source: ASSUMED.
    HIGH UNCERTAINTY — tunnel penetrations create unique loading."""

    vessel_thickness_m: float = 0.08
    """Vacuum vessel thickness [m].
    Source: Standard tokamak vessel.
    MODERATE UNCERTAINTY."""

    blanket_unit_cost: float = 0.60
    """Blanket unit cost [M$/m³].
    D-T breeding blanket with lithium, beryllium multiplier.
    Source: 1costingfe blanket_unit_cost default.
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
    Similar to tokamak (6-8 years) due to large chamber size.
    Source: ASSUMED.
    MODERATE UNCERTAINTY."""

    om_rate_fraction: float = 0.025
    """Annual O&M as fraction of overnight capital.
    Slightly higher than tokamak (2%) due to first-of-a-kind technology.
    Source: ASSUMED.
    MODERATE UNCERTAINTY."""

    core_lifetime_FPY: float = 5.0
    """First wall / blanket lifetime [full-power-years before replacement].
    D-T 14.1 MeV neutron damage.
    Source: Standard D-T tokamak value.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # FUEL COSTS
    # =========================================================================

    u_deuterium_per_kg: float = 2175.0
    """Deuterium unit cost [$/kg].
    Source: 1costingfe costing_constants.yaml."""

    u_tritium_per_g: float = 30000.0
    """Tritium unit cost [$/g].
    Source: 1costingfe costing_constants.yaml."""

    # =========================================================================
    # REGULATORY
    # =========================================================================

    regulatory_multiplier: float = 1.8
    """Building cost multiplier for D-T nuclear facility regulatory overhead.
    D-T tokamak value: 1.5-2.2×.
    Source: ASSUMED from tokamak analogues.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # COMPUTE METHODS
    # =========================================================================

    def _compute_power(self) -> dict:
        """Layer 1: Power balance from assumed fusion power and Q_sci.

        Energy flow:
          Heating power [P_heat] → plasma → fusion power [P_fus]
          → thermal [P_th] → gross electric [P_et]
          → net electric [P_net] = P_et - P_heat - P_coil - P_aux
        """
        r: dict = {}

        # --- Fusion power (SPECULATIVE) ---
        p_fus = self.p_fus_MW
        r["p_fus"] = p_fus

        # Scientific Q (ASSUMED)
        r["Q_sci"] = self.Q_sci

        # Heating power (derived from Q_sci)
        p_heat = p_fus / self.Q_sci if self.Q_sci > 0 else 0.0
        r["p_heating"] = p_heat

        # Alpha power (D-T: 20% of fusion energy to alphas)
        p_alpha = p_fus * 0.20
        r["p_alpha"] = p_alpha

        # Neutron power (D-T: 80% of fusion energy to neutrons)
        p_neutron = p_fus * 0.80
        r["p_neutron"] = p_neutron

        # --- Thermal power ---
        # Neutrons deposit in blanket with multiplication
        # Alphas thermalize in plasma then to first wall
        p_th = (p_neutron * self.M_blanket) + p_alpha
        r["p_th"] = p_th

        # --- Gross electric ---
        p_et = p_th * self.eta_th
        r["p_et"] = p_et

        # --- Recirculating power ---
        p_aux = (self.p_cooling_MW + self.p_fuel_MW
                 + self.p_house_MW + self.p_controls_MW)
        r["p_aux"] = p_aux
        p_recirc = p_heat + self.p_coil_MW + p_aux
        r["p_recirc"] = p_recirc
        r["p_coil"] = self.p_coil_MW

        # --- Net electric ---
        p_net = p_et - p_recirc
        r["p_net"] = p_net

        # Multi-module plant totals (n_mod = 1 for Polomac)
        r["p_net_plant"] = p_net * self.n_mod
        r["p_et_plant"]  = p_et * self.n_mod
        r["p_th_plant"]  = p_th * self.n_mod

        # --- Figures of merit ---
        r["Q_eng"] = p_fus / p_recirc if p_recirc > 0 else float('inf')
        r["recirc_fraction"] = p_recirc / p_et if p_et > 0 else float('inf')

        # Physics gap reminder
        r["demonstrated_temp_eV"] = 100
        r["required_temp_keV"] = self.ion_temp_keV
        r["temperature_gap_factor"] = (self.ion_temp_keV * 1000) / 100

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Chamber geometry volumes using toroidal shells.

        Approximate toroidal geometry for dipole field chamber.
        V_plasma = 1300 m³ given. Derive major radius and minor radius.
        """
        r: dict = {}

        # Given plasma volume, estimate major and minor radii
        # V_plasma ~ 2π²Rₘₐⱼ × rₘᵢₙ²
        # Assume aspect ratio A ~ 3 → R/r ~ 3
        V_plasma = self.plasma_volume_m3
        aspect_ratio = 3.0
        # r_min = (V_plasma / (2π² * A))^(1/3)
        r_min = (V_plasma / (2.0 * math.pi**2 * aspect_ratio)) ** (1.0/3.0)
        R_maj = aspect_ratio * r_min

        r["major_radius_m"] = R_maj
        r["minor_radius_m"] = r_min
        r["plasma_vol_m3"] = V_plasma

        def toroidal_shell_vol(R: float, r_in: float, thickness: float) -> float:
            """Volume of toroidal shell."""
            r_out = r_in + thickness
            return 2.0 * math.pi**2 * R * (r_out**2 - r_in**2)

        r_b = r_min + self.blanket_thickness_m
        r["blanket_vol_m3"] = toroidal_shell_vol(R_maj, r_min, self.blanket_thickness_m)

        r_s = r_b + self.shield_thickness_m
        r["shield_vol_m3"] = toroidal_shell_vol(R_maj, r_b, self.shield_thickness_m)

        r_st = r_s + self.structure_thickness_m
        r["structure_vol_m3"] = toroidal_shell_vol(R_maj, r_s, self.structure_thickness_m)

        r["vessel_vol_m3"] = toroidal_shell_vol(R_maj, r_st, self.vessel_thickness_m)

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts.

        Polomac-specific features:
        • C220103: Lower-field magnets (2.5 T) with magnetic tunnel geometry
        • C220104: Heating method unknown — use power-scaled estimate
        • Large plasma volume → large blanket, shield, vessel costs

        All sub-accounts use 1costingfe power-scaling laws unless overridden.
        """
        r: dict = {}

        p_th  = max(power["p_th"], 1.0)
        p_et  = max(power["p_et"], 1.0)
        p_net_safe = max(abs(power["p_net"]) * self.n_mod, 1.0)

        # C220101: Active Region / First Wall / Blanket
        # D-T breeding blanket in large toroidal volume
        r["C220101"] = (self.blanket_unit_cost
                        * geom["blanket_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220102: Shield (D-T 14.1 MeV neutrons)
        # Source: 1costingfe shield_unit_cost = 0.74 M$/m³
        r["C220102"] = (0.74
                        * geom["shield_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: Coils — OVERRIDE with Polomac superconducting magnets
        # Lower field (2.5 T) vs tokamak but magnetic tunnel geometry
        r["C220103"] = self.magnet_capital_M

        # C220104: Supplementary Heating
        # No disclosed heating method; use power-scaled estimate
        # Source: 1costingfe heating_base ~ $150M at 1 GWe for NBI/ECRH
        r["C220104"] = 100.0 * (p_net_safe / P_NET_REF) ** 0.7

        # C220105: Primary Structure
        # Magnetic tunnel supports create non-standard loading
        # Source: 1costingfe structure_unit_cost = 0.15 M$/m³, increased for tunnels
        r["C220105"] = (0.20  # Increased from 0.15 for tunnel complexity
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: Vacuum Vessel
        # Source: 1costingfe vessel_unit_cost = 0.72 M$/m³
        r["C220106"] = (0.72
                        * geom["vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # C220107: Power Supplies (coil power supplies + control)
        # Superconducting coils require lower steady-state power than 2014 copper design
        # Source: 1costingfe power_supply_base ~ $50M at 1 GWe
        r["C220107"] = 40.0 * (p_net_safe / P_NET_REF) ** 0.6

        # C220108: Target Factory — not applicable to MFE
        r["C220108"] = 0.0

        # C220109: Direct Energy Converter — not applicable
        r["C220109"] = 0.0

        # C220110: Remote Handling (D-T neutron damage)
        # Source: 1costingfe remote_handling_dt_base = 150 M$ at 1 GWe
        r["C220110"] = 120.0 * (p_net_safe / P_NET_REF) ** 0.6

        # C220111: Installation labor
        # Source: 1costingfe installation_frac = 0.14
        reactor_sub = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"])
        r["C220111"] = 0.14 * reactor_sub

        # C220112: Isotope Separation (D-T fuel cycle)
        # Source: 1costingfe tritium system base cost
        r["C220112"] = 15.0 * (p_net_safe / P_NET_REF) ** 0.5

        r["CAS22_per_module"] = reactor_sub + r["C220111"] + r["C220112"]

        # --- Plant-wide accounts ---
        p_th_total  = power["p_th"] * self.n_mod
        p_net_total = abs(power["p_net"]) * self.n_mod

        # C220200: Coolant Systems
        # Source: 1costingfe CAS22 plant-wide formulas
        C220201 = 166.0 * (p_net_total / 1000.0)
        C220202 = 40.6  * (p_th_total  / 3500.0) ** 0.55
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling (cryoplant for superconducting coils)
        # Source: 1costingfe CAS22 formula
        C220301 = 1.1e-3 * p_th_total
        C220302 = 40.0  # Cryoplant for superconducting magnets
        r["C220300"] = C220301 + C220302

        # C220400: Radioactive Waste Management (D-T)
        # Source: 1costingfe formula
        r["C220400"] = 1.5 * (p_th_total / 1000.0)

        # C220500: Fuel Handling & Storage (D-T tritium cycle)
        # Source: 1costingfe fuel_handling_dt_base = 120 M$
        r["C220500"] = 100.0 * (p_net_total / 1000.0) ** 0.7

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
        licensing     = 3.0 if not self.noak else 1.5
        r["CAS10"] = (3.0      # site_permits
                      + (4.0 if self.noak else 20.0)        # plant_studies
                      + 2.0    # plant_permits
                      + 1.0    # plant_reports
                      + 1.0    # other_precon
                      + land_cost
                      + licensing)

        # === CAS21: Buildings ===
        # D-T MFE facility building costs (M$ at P_ET_REF = 1100 MW gross electric)
        # Large plasma volume (1300 m³) suggests large reactor building
        building_items_M = {
            "site_improvements":   85.0,
            "reactor_building":    180.0,  # Large building for 1300 m³ plasma + tunnels
            "turbine_building":    58.0,
            "hot_cell":            55.0,   # D-T activation
            "reactor_auxiliaries": 35.0,
            "fuel_storage":        12.0,   # D-T tritium storage
            "control_room":        14.0,
            "security":             3.5,
            "ventilation_hvac":    20.0,
            "administration":       9.0,
            "maintenance":         20.0,
            "heat_exchanger":      17.0,
            "power_supply_bldg":   15.0,
            "cryogenics_bldg":     12.0,   # For superconducting magnets
            "misc":                 5.0,
        }
        total_bldg_ref = sum(building_items_M.values())
        cas21_raw = total_bldg_ref * p_et / P_ET_REF
        # Apply D-T nuclear regulatory multiplier
        r["CAS21"] = cas21_raw * self.regulatory_multiplier
        r["CAS21_detail"] = {k: v * p_et / P_ET_REF * self.regulatory_multiplier
                             for k, v in building_items_M.items()}

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment ===
        # Source: 1costingfe turbine_per_mw = 0.20 M$/MW (Rankine) or 0.25 (sCO2)
        r["CAS23"] = self.n_mod * p_et * 0.20

        # === CAS24: Electric Plant Equipment ===
        # Source: 1costingfe electric_per_mw
        r["CAS24"] = self.n_mod * p_et * 0.08418

        # === CAS25: Misc Plant Equipment ===
        # Source: 1costingfe misc_per_mw
        r["CAS25"] = self.n_mod * p_et * 0.05124

        # === CAS26: Heat Rejection ===
        # Source: 1costingfe heat_rej_per_mw
        r["CAS26"] = self.n_mod * p_et * 0.03416

        # === CAS27: Special Materials (initial tritium inventory)
        # Source: 1costingfe special_materials_dt
        r["CAS27"] = 80.0 * (p_net_safe / P_NET_REF) ** 0.5

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
        # Source: 1costingfe owner_cost_dt = 39 M$ at 1 GWe
        r["CAS40"] = 35.0 * (p_net_safe / P_NET_REF) ** 0.5

        # === CAS50: Supplementary Costs ===
        # Source: 1costingfe spare_parts_frac_dt = 0.03
        spare_parts   = 0.03 * sum(r[k] for k in ["CAS22", "CAS23", "CAS24",
                                                    "CAS25", "CAS26", "CAS27", "CAS28"])
        shipping      = 0.015 * r["CAS20"]
        taxes         = 0.010 * r["CAS20"]
        insurance     = 0.015 * (r["CAS20"] + r["CAS30"])
        decom         = 120.0 * (p_net_safe / P_NET_REF) ** 0.5
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
        r["n_replacements"] = n_rep

        r["CAS70"] = r["CAS71"] + r["CAS72"]

        # === CAS80: Fuel & Consumables (D-T) ===
        # D-T fusion: D + T → n + α (17.6 MeV)
        # Fuel consumption: P_fus / (17.6 MeV) = reactions/s
        # Each reaction consumes 1 D atom (2 amu) + 1 T atom (3 amu)
        p_fus_W = power["p_fus"] * 1e6  # W
        reaction_rate = p_fus_W / E_FUSION_J  # reactions/s

        M_D_kg_per_reaction = 2 * AMU_KG
        M_T_kg_per_reaction = 3 * AMU_KG

        seconds_per_year = 8760 * 3600 * self.plant_availability
        annual_D_kg = reaction_rate * M_D_kg_per_reaction * seconds_per_year
        annual_T_kg = reaction_rate * M_T_kg_per_reaction * seconds_per_year

        r["CAS80_deuterium"] = annual_D_kg * self.u_deuterium_per_kg / 1e6  # M$/yr
        r["CAS80_tritium"] = annual_T_kg * self.u_tritium_per_g * 1000 / 1e6  # M$/yr
        r["CAS80"] = r["CAS80_deuterium"] + r["CAS80_tritium"]

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
# CRITICAL: Native-scale only. Do NOT extrapolate to 1 GWe via economy-of-scale.
# Freeform concepts report at their native power scale only.
# ============================================================================
params  = PolomacPlantParams()
results = params.compute()


# ============================================================================
# Output functions
# ============================================================================

def print_results(p: PolomacPlantParams, r: dict) -> None:
    """Pretty-print the full LCOE model results with CAS-structured accounting."""
    pw    = r["power"]
    geom  = r["geometry"]
    cas22 = r["cas22"]
    costs = r["costs"]
    econ  = r["economics"]

    print("=" * 80)
    print("Polomac Magnetic Confinement (Deutelio) — Speculative LCOE Corridor")
    print("Freeform CAS-Structured Model — FOR COMPARISON PURPOSES ONLY")
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
    print("  ║  • No design point specified by Deutelio                          ║")
    print("  ║  • No native power target disclosed (value here is INVENTED)      ║")
    print("  ║  • No archetype assigned (upstream: Archetype = [empty])          ║")
    print("  ║  • Magnetic tunnel concept never experimentally demonstrated      ║")
    print("  ║  • Power balance unknown (Q_eng, P_fus undefined in sources)      ║")
    print("  ║                                                                    ║")
    print("  ║  Under analysis contract, models require validated design         ║")
    print("  ║  point data BEFORE modeling. This concept has none.               ║")
    print("  ╚════════════════════════════════════════════════════════════════════╝")
    print()
    print("  ╔════════════════════════════════════════════════════════════════════╗")
    print("  ║  PHYSICS DEMONSTRATION GAP (ABSOLUTE BLOCKER)                     ║")
    print("  ║  Demonstrated conditions:  100 eV (small prototype)               ║")
    print(f"  ║  D-T fusion requirement:   {pw['required_temp_keV']:.1f} keV                           ║")
    print(f"  ║  Temperature gap:          {pw['temperature_gap_factor']:.0f}× ({pw['temperature_gap_factor']/10:.0f} orders of magnitude)     ║")
    print("  ║                                                                    ║")
    print("  ║  Magnetic tunnel concept has never been experimentally validated. ║")
    print("  ║  Particle loss rates through tunnels are unquantified.            ║")
    print("  ║  2014 design had 700 MW coil power (excessive for steady state).  ║")
    print("  ║  No Q_eng or recirculating power analysis exists.                 ║")
    print("  ║                                                                    ║")
    print("  ║  ALL PARAMETERS IN THIS MODEL ARE SPECULATIVE ASSUMPTIONS.        ║")
    print("  ╚════════════════════════════════════════════════════════════════════╝")
    print()

    # Viability warning
    if pw["p_net"] <= 0:
        print("  *** ENERGY SINK: Net electric is NEGATIVE at these parameters. ***")
        print("  *** Q_eng < 1 — no net power output. ***")
        print("  *** LCOE is undefined. Recirculating power exceeds gross electric. ***")
        print()

    # --- Key Physics Inputs ---
    print(f"\n--- Key Physics Parameters (INVENTED FOR CORRIDOR PURPOSES) ---")
    print(f"  (NOT extracted from Deutelio disclosures)")
    print(f"  Magnetic field:               {p.B_field_T:.1f} T [from literature range 2-3 T]")
    print(f"  Plasma volume:                {p.plasma_volume_m3:.0f} m³ [from 2014 paper]")
    print(f"  Beta:                         {p.beta:.1%} [from literature 20-30%]")
    print(f"  Ion temperature:              {p.ion_temp_keV:.1f} keV [D-T standard]")
    print(f"  Density:                      {p.density_m3:.1e} m⁻³ [from literature]")
    print(f"  Confinement time:             {p.tau_E_s:.1f} s [from literature 4-5 s]")
    print(f"  Fusion power (P_fus):         {pw['p_fus']:.1f} MW [ASSUMED — no source value]")
    print(f"  Scientific Q (Q_sci):         {pw['Q_sci']:.1f} [ASSUMED — no heating method disclosed]")
    print(f"  Blanket multiplication M:     {p.M_blanket:.2f} [standard D-T]")
    print(f"  Thermal efficiency η_th:      {p.eta_th:.1%} [ASSUMED Rankine at 350°C]")
    print(f"  Plant availability:           {p.plant_availability:.0%} [ASSUMED]")
    print(f"  Modules:                      {p.n_mod} [single large dipole]")
    print(f"  → Native power (derived):     ~{pw['p_net_plant']:.0f} MWe [NO COMPANY TARGET]")

    # --- Geometry ---
    print(f"\n--- Geometry (derived from 1300 m³ plasma) ---")
    print(f"  Major radius (approx):        {geom['major_radius_m']:.1f} m")
    print(f"  Minor radius (approx):        {geom['minor_radius_m']:.1f} m")
    print(f"  Plasma volume:                {geom['plasma_vol_m3']:.0f} m³")
    print(f"  Blanket volume:               {geom['blanket_vol_m3']:.0f} m³")
    print(f"  Shield volume:                {geom['shield_vol_m3']:.0f} m³")

    # --- Power Balance ---
    print(f"\n--- Power Balance — FROM SPECULATIVE ASSUMPTIONS ---")
    print(f"  Fusion power (P_fus):         {pw['p_fus']:>8.1f} MW  [HYPOTHETICAL — physics undemonstrated]")
    print(f"    Neutron power (80%):        {pw['p_neutron']:>8.1f} MW (14.1 MeV → blanket)")
    print(f"    Alpha power (20%):          {pw['p_alpha']:>8.1f} MW (→ plasma heating)")
    print(f"  Thermal power (P_th):         {pw['p_th']:>8.1f} MW  (× M={p.M_blanket})")
    print(f"  Gross electric (P_et):        {pw['p_et']:>8.1f} MWe (× η={p.eta_th:.1%})")
    print(f"  Recirculating power:")
    print(f"    Heating:                    {pw['p_heating']:>8.1f} MW")
    print(f"    Coils (superconducting):    {pw['p_coil']:>8.1f} MW")
    print(f"    Auxiliaries:                {pw['p_aux']:>8.1f} MW")
    print(f"    Total recirculating:        {pw['p_recirc']:>8.1f} MW")
    print(f"  Net electric (P_net):         {pw['p_net']:>8.1f} MWe")
    print(f"  Plant net electric:           {pw['p_net_plant']:>8.1f} MWe [NO COMPANY TARGET — INVENTED]")
    print(f"  Engineering Q (Q_eng):        {pw['Q_eng']:>8.3f}")
    print(f"  Recirculating fraction (ε):   {pw['recirc_fraction']:>8.1%}")

    # --- CAS22 ---
    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    cas22_labels = {
        "C220101": ("Blanket / First Wall (D-T)",    ""),
        "C220102": ("Shield (14.1 MeV neutrons)",    ""),
        "C220103": ("Magnets (2.5 T supercond.)",    "[OVERRIDE — lower field, tunnel geometry]"),
        "C220104": ("Supplementary Heating",         "[method unknown]"),
        "C220105": ("Primary Structure",             "[tunnel supports]"),
        "C220106": ("Vacuum Vessel",                 ""),
        "C220107": ("Power Supplies",                ""),
        "C220110": ("Remote Handling",               ""),
        "C220111": ("Installation Labor",            ""),
        "C220112": ("Isotope Separation (D-T)",      ""),
    }
    for code, (label, note) in cas22_labels.items():
        val = cas22.get(code, 0.0)
        if val != 0.0 or note:
            print(f"    {code} {label:<36s} ${val:>8.1f}M  {note}")
    print(f"    {'─' * 66}")
    print(f"    Per-module subtotal:                         ${cas22['CAS22_per_module']:>8.1f}M × {p.n_mod}")

    pw_labels = {
        "C220200": "Coolant Systems (thermal cycle)",
        "C220300": "Aux Cooling + Cryoplant",
        "C220400": "Rad Waste Management (D-T)",
        "C220500": "Fuel Handling (D-T tritium)",
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
    print(f"  CAS27 Special Materials (tritium):             ${costs['CAS27']:>8.1f}M")
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
    print(f"  CAS72 Blanket replacements ({econ['n_replacements']} over life):    ${econ['CAS72']:>8.1f}M/yr")
    print(f"  CAS70 Total O&M:                               ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80 Fuel (D-T):                              ${econ['CAS80']:>8.4f}M/yr")

    # --- LCOE (NATIVE SCALE ONLY) ---
    print(f"\n--- LCOE (FREEFORM, NATIVE-SCALE ONLY) ---")
    if pw["p_net"] > 0:
        print(f"  Annual energy production:     {econ['annual_energy_MWh']:>12,.0f} MWh/yr")
        print(f"  Annual revenue requirement:   ${econ['annual_revenue_req']:>8.1f}M/yr")
        print(f"  ╔═══════════════════════════════════════════════════╗")
        print(f"  ║  LCOE = {econ['lcoe_cents_per_kWh']:>7.1f} ¢/kWh                            ║")
        print(f"  ║       = {econ['lcoe_USD_per_MWh']:>7.1f} $/MWh   (freeform, native-scale only)  ║")
        print(f"  ║                                                   ║")
        print(f"  ║  NOT EXTRACTED FROM COMPANY DATA                  ║")
        print(f"  ║  Assumes P_fus={p.p_fus_MW:.0f} MW, Q_sci={p.Q_sci:.0f}, B={p.B_field_T:.1f} T, other  ║")
        print(f"  ║  invented parameters. For comparison only.        ║")
        print(f"  ╚═══════════════════════════════════════════════════╝")
        print(f"  Capital (CAS90):              {econ.get('capital_fraction', 0):.1%}")
        print(f"  O&M    (CAS70):               {econ.get('om_fraction', 0):.1%}")
        print(f"  Fuel   (CAS80):               {econ.get('fuel_fraction', 0):.2%}")
    else:
        print(f"  LCOE: UNDEFINED — net electric is negative.")
        print(f"  Plant is an energy sink. LCOE is infinite.")

    print()
    print("=" * 80)


def sensitivity_sweep(base_params: PolomacPlantParams,
                      param_name: str,
                      values: list,
                      label: str = "") -> list[dict]:
    """Sweep a single parameter and return LCOE and net power for each value."""
    out = []
    for val in values:
        p = PolomacPlantParams(**{**base_params.__dict__, param_name: val})
        r = p.compute()
        pw = r["power"]
        out.append({
            "param_value":    float(val),
            "lcoe_cents_kWh": r["economics"]["lcoe_cents_per_kWh"],
            "lcoe_USD_MWh":   r["economics"]["lcoe_USD_per_MWh"],
            "net_electric_MW": pw["p_net"],
            "Q_eng":          pw["Q_eng"],
            "recirc_fraction": pw["recirc_fraction"],
        })
    return out


def _print_sweep(sweep_results: list[dict], label: str,
                 param_unit: str = "") -> None:
    """Print a sensitivity sweep table."""
    print(f"\n  {label}:")
    print(f"  {'Value':>12}  {'Q_eng':>7}  {'P_net':>8}  {'ε':>6}  {'LCOE':>14}")
    print(f"  {'─'*12}  {'─'*7}  {'─'*8}  {'─'*6}  {'─'*14}")
    for row in sweep_results:
        v = row["param_value"]
        q = row["Q_eng"]
        p = row["net_electric_MW"]
        e = row["recirc_fraction"]
        lcoe_c = row["lcoe_cents_kWh"]

        v_str = f"{v:>12.1f}" if isinstance(v, float) else f"{v:>12}"
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

    # 1. Fusion power (EXTREME UNCERTAINTY)
    sweep_pfus = sensitivity_sweep(
        params, "p_fus_MW",
        [200.0, 300.0, 400.0, 600.0, 800.0],
        "Fusion power"
    )
    _print_sweep(sweep_pfus, "Fusion Power (P_fus)", "MW")

    # 2. Scientific Q (PHYSICS UNDEMONSTRATED)
    sweep_qsci = sensitivity_sweep(
        params, "Q_sci",
        [5.0, 7.5, 10.0, 15.0, 20.0],
        "Scientific Q"
    )
    _print_sweep(sweep_qsci, "Scientific Q (fusion out / heating in)", "")

    # 3. Magnet capital cost (HIGH UNCERTAINTY)
    sweep_magnet = sensitivity_sweep(
        params, "magnet_capital_M",
        [100.0, 150.0, 180.0, 250.0, 400.0],
        "Magnet capital cost"
    )
    _print_sweep(sweep_magnet, "Magnet Capital Cost", "M$")

    # 4. Coil power consumption (HIGH UNCERTAINTY)
    sweep_coil_pwr = sensitivity_sweep(
        params, "p_coil_MW",
        [10.0, 15.0, 25.0, 50.0, 100.0],
        "Coil power"
    )
    _print_sweep(sweep_coil_pwr, "Coil Steady-State Power", "MW")

    # 5. Thermal efficiency (MODERATE UNCERTAINTY)
    sweep_eta = sensitivity_sweep(
        params, "eta_th",
        [0.30, 0.35, 0.40, 0.45],
        "Thermal efficiency"
    )
    _print_sweep(sweep_eta, "Thermal-to-Electric Efficiency", "")

    print("\n\n" + "=" * 80)
    print("SCENARIO COMPARISON")
    print("=" * 80)

    # Conservative: Physics barely works, high losses through tunnels
    conservative = PolomacPlantParams(
        p_fus_MW=250.0,
        Q_sci=5.0,
        p_coil_MW=50.0,
        magnet_capital_M=300.0,
        eta_th=0.30,
        plant_availability=0.70,
    )

    # Moderate: Baseline parameters (already set)
    moderate = params

    # Optimistic: Physics breakthrough, magnetic tunnels work perfectly
    optimistic = PolomacPlantParams(
        p_fus_MW=600.0,
        Q_sci=15.0,
        p_coil_MW=10.0,
        magnet_capital_M=120.0,
        eta_th=0.40,
        plant_availability=0.85,
    )

    scenarios = [
        ("Conservative", conservative),
        ("Moderate (Baseline)", moderate),
        ("Optimistic", optimistic),
    ]

    print("\n  Scenario Comparison Table:")
    print(f"  {'Scenario':<24} {'P_net':<10} {'Q_eng':<8} {'LCOE':<16} {'$/kWe':<12}")
    print(f"  {'─'*24} {'─'*10} {'─'*8} {'─'*16} {'─'*12}")

    for name, p_scenario in scenarios:
        r = p_scenario.compute()
        pw = r["power"]
        econ = r["economics"]
        costs = r["costs"]

        p_net = pw["p_net_plant"]
        q_eng = pw["Q_eng"]
        lcoe_c = econ["lcoe_cents_per_kWh"]
        cap_per_kwe = costs["specific_capital_USD_per_kWe"]

        p_str = f"{p_net:>8.0f} MW" if p_net > 0 else "   (sink)"
        q_str = f"{q_eng:>6.2f}"

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
   Magnetic tunnel concept: NEVER experimentally demonstrated
   Particle loss rates through tunnels: UNQUANTIFIED
   Small prototype: 100 eV, 0.2-0.3 T, hydrogen plasma
   Reactor requirement: 8.1 keV D-T, 2-3 T field
   Temperature gap: 81× increase

   Impact: ALL parameters in this model are speculative until magnetic
           tunnel confinement is experimentally demonstrated. The concept
           claims 2-3× lower magnetic field than tokamaks for equivalent
           performance, but this has zero experimental validation.

   The 2014 design had 700 MW coil power consumption (excessive for
   steady-state). The 2024 report mentions superconducting magnets but
   provides NO Q_eng or recirculating power analysis.

   Resolution pathway: Build and operate small prototype demonstrating:
                      (1) Magnetic tunnel concept at keV temperatures
                      (2) Quantified particle loss rates
                      (3) Measured Q_eng and power balance

2. FUSION POWER & Q_ENG (UNKNOWN)
   Baseline: P_fus = 400 MW, Q_eng ~ 5 (pure speculation)
   Sensitivity: LCOE ∝ 1/P_fus and ∝ 1/Q_eng approximately

   Impact: No fusion power estimate exists in sources. No heating system
           for reactor scale is specified. Small prototype uses 5-10 kW
           ECRH, not scalable to 8.1 keV D-T operation.

   Without Q_eng analysis, recirculating power fraction is unknown.
   The concept's economic viability depends entirely on achieving
   net-positive power output, which is undemonstrated.

3. MAGNET CAPITAL COST
   Baseline: $180M (ASSUMED lower field advantage at 2.5 T)
   Range: $100M-$400M depending on tunnel geometry complexity
   Sensitivity: LCOE varies by ~30% across this range

   Impact: Lower magnetic field (2.5 T vs 5+ T tokamak) should reduce
           magnet cost, but magnetic tunnel penetrations create unique
           structural challenges. The discontinuous azimuthal geometry
           may offset field advantage. No magnet design exists.

   If tunnel integration requires expensive custom coil structures,
           the claimed cost advantage over tokamaks disappears.

4. LARGE PLASMA VOLUME (1300 m³)
   Much larger than compact tokamaks (ARC ~60 m³)
   Impact: Large volume → large blanket, shield, vessel, building costs
           Even with lower field, capital cost may be high due to size.

   The 2014 conceptual design had 1300 m³ plasma volume. No updated
   reactor-scale volume in 2024 report. Large size partially negates
   lower-field magnet cost advantage.
""")

    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
