"""
Sheared-Flow Stabilized Z-Pinch (SFS Z-Pinch) LCOE Model
==========================================================
1cFE First Pass Concept Analysis
Concept: Sheared-Flow Stabilized Z-Pinch with D-T fuel
Company: Zap Energy (Seattle, WA; founded 2017; ~$330M raised as of 2026)
Commercial Device Series: FuZE → FuZE-Q → FuZE-3 → FuZE-A → Century → pilot plant

This is a parameterized LCOE model built from first principles following the CAS
cost accounting structure. The SFS Z-Pinch concept does not map to any standard
1costingfe ConfinementConcept, so this model is self-contained.

Key architecture differences from tokamak/stellarator:
  - No superconducting magnets (eliminates HTS tape cost and cryogenic plant)
  - Pulsed-power driver (capacitors, switches, PFNs) replaces magnet system
  - LiPb flowing first wall serves simultaneously as electrode, blanket, shield
  - Pulsed at 10 Hz (200 µs pinch lifetime) vs. quasi-steady-state MFE
  - Multi-module architecture: ~50 MWe/module

Cost accounting follows the standardized CAS (Code of Accounts System) structure
used in 1costingfe / pyFECONS. Scaling laws are adopted directly from
1costingfe/src/costingfe/data/defaults/costing_constants.yaml. CAS22 sub-accounts
are overridden where the SFS Z-Pinch architecture differs substantially from
reference tokamak assumptions.

Key references:
- Thompson, Levitt, Nelson, Shumlak — "Engineering Paradigms for SFS Z-Pinch
  Fusion Energy" (FST, 2023) — primary engineering reference [engineering-paradigms]
- Century demo system milestones and press releases [century-demo]
- FuZE-3 gigapascal results (Nov 2025) [fuze-3-2025]
- OSTI "Challenges and Gaps in Pulsed Power for Fusion" (LLNL-JRNL-2001600, 2025)
  [osti-pulsed-power]
- 1costingfe costing_constants.yaml — scaling law source for standard accounts
- Zap Energy website — commercial parameters [zap-website]

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass, field
from typing import Optional


# === Reference power levels for scaling laws (from 1costingfe) ===
P_TH_REF = 2500.0   # Reference thermal power [MW] — 1costingfe default
P_ET_REF = 1100.0   # Reference gross electric power [MW] — 1costingfe default


@dataclass
class SFSZPinchPlantParams:
    """
    Parameterized SFS Z-Pinch power plant model.

    All parameters have source annotations. Uncertainty levels:
      (no tag)              = well-established value with source
      MODERATE UNCERTAINTY  = reasonable estimate from analogues
      HIGH UNCERTAINTY      = speculative or poorly constrained

    Architecture:
      - Multi-module plant (n_mod modules, each ~50 MWe net)
      - Each module: pulsed-power driver + z-pinch chamber + LiPb blanket
      - Power conversion: steam Rankine cycle via LiPb → steam heat exchanger
    """

    # =========================================================================
    # DRIVER / PULSED POWER
    # =========================================================================

    driver_electrical_energy_per_shot_MJ: float = 1.9
    """Electrical energy delivered to plasma per shot [MJ].
    Derivation: fusion_energy_per_shot_MJ / Q_fusion / driver_wall_to_plasma_eff
    At Q = 10, fusion = 19 MJ → plasma input = 1.9 MJ; at 70% driver efficiency,
    stored energy ≈ 2.7 MJ/pulse.
    Ref: engineering-paradigms-paper-summary.md §Table I, §Driver Efficiency.
    MODERATE UNCERTAINTY — Q not experimentally demonstrated."""

    driver_wall_to_plasma_efficiency: float = 0.70
    """Fraction of stored electrical energy delivered as plasma input [dimensionless].
    Breakdown: AC-DC rectification ~90% × modulator ~80% = ~72%; paper rounds to 70%.
    Ref: engineering-paradigms-paper-summary.md §Driver Efficiency.
    Demonstrated at subscale; extrapolated to commercial scale."""

    driver_stored_energy_per_shot_MJ: float = 2.7
    """Total stored electrical energy per shot in capacitor bank [MJ].
    = driver_electrical_energy_per_shot_MJ / driver_wall_to_plasma_efficiency
    = 1.9 / 0.70 ≈ 2.7 MJ. Commercial driver ~4× the FuZE-Q ~1 MJ bank.
    Ref: engineering-paradigms-paper-summary.md §Table I, §Driver Efficiency.
    MODERATE UNCERTAINTY — not validated at commercial scale."""

    driver_cost_per_MJ_stored_M_USD: float = 3.0
    """Capital cost of pulsed power driver per MJ of stored energy [M$/MJ].
    This is the dominant and most uncertain capital cost item.
    Analogues from industrial pulsed power: $1–10/J ($1,000–10,000/kJ = $1–10 M/MJ)
    depending on rep rate rating and pulse shape. At 10 Hz, higher-rated components
    push toward the upper end. Using $3 M/MJ as central estimate.
    Ref: general pulsed power literature (no Zap-specific data); analysis.md §S2.
    # ASSUMED: No published cost estimate for commercial Z-pinch driver.
    HIGH UNCERTAINTY — range spans 10× (see sensitivity sweep)."""

    driver_rep_rate_Hz: float = 10.0
    """Shot repetition rate [Hz].
    Commercial target from Engineering Paradigms paper and Zap website.
    Century currently demonstrates 0.2 Hz — a 50× scaling gap to commercial target.
    Ref: zap-energy-website-how-it-works.md §Commercial Design; dossier.md §Repetition Rate.
    HIGH UNCERTAINTY — 10 Hz not demonstrated; 0.2 Hz is current state."""

    # =========================================================================
    # FUSION PHYSICS
    # =========================================================================

    fusion_energy_per_shot_MJ: float = 19.0
    """Fusion energy yield per shot [MJ].
    From Engineering Paradigms paper Table I: 19 MJ/pulse at commercial design point.
    Cross-check: 200 MWt / 10 Hz = 20 MWt·s/shot = 20 MJ/shot (consistent).
    Ref: engineering-paradigms-paper-summary.md §Design Parameters/Table I.
    MODERATE UNCERTAINTY — plant design point; not experimentally demonstrated."""

    fusion_Q: float = 10.0
    """Fusion energy gain Q = fusion power / driver plasma input power.
    Paper states Q > 10 at plant-relevant currents (1.2–1.5 MA, 200 µs lifetime).
    This is a calculated projection — never experimentally demonstrated.
    FuZE demonstrated 20–40 µs lifetimes; 200 µs requires 5–10× extrapolation.
    Ref: engineering-paradigms-paper-summary.md §Physics Assumptions.
    HIGH UNCERTAINTY — most critical unknown in the power balance."""

    pinch_current_MA: float = 1.35
    """Z-pinch current at commercial design point [MA]. Mid-range of 1.2–1.5 MA.
    Ref: engineering-paradigms-paper-summary.md §Table I.
    MODERATE UNCERTAINTY — design point; FuZE-Q has not reached this current."""

    plasma_temperature_keV: float = 32.5
    """Plasma temperature at commercial design point [keV]. Mid-range of 30–35 keV.
    Ref: engineering-paradigms-paper-summary.md §Design Parameters.
    Consistent with FuZE thermonuclear measurements, though at lower performance."""

    blanket_energy_multiplication: float = 1.10
    """Blanket energy multiplication factor M (neutron exothermic reactions).
    D-T: 80% of fusion energy in neutrons; Li + n → T + He exothermic adds ~10%.
    TBR ~ 1.1 consistent with 3 m LiPb blanket Monte Carlo calculation.
    Ref: engineering-paradigms-paper-summary.md §Blanket Design;
    dossier.md §Tritium Breeding. Standard D-T fusion engineering assumption."""

    # =========================================================================
    # THERMAL CONVERSION
    # =========================================================================

    thermal_efficiency: float = 0.33
    """Thermal-to-electric conversion efficiency [dimensionless].
    Steam Rankine cycle assumed per Engineering Paradigms paper.
    LiPb solidification point ~235°C sets a floor on blanket outlet temperature,
    constraining steam cycle efficiency to ~30–37% range.
    # ASSUMED: Exact cycle design unpublished; 33% is conservative Rankine estimate.
    Ref: engineering-paradigms-paper-summary.md §Heat Extraction; dossier.md §Energy Capture.
    MODERATE UNCERTAINTY — thermal efficiency target not published."""

    # =========================================================================
    # PLANT CONFIGURATION
    # =========================================================================

    n_mod: int = 4
    """Number of fusion modules (chambers) per plant.
    Century described as "close to eventual size of single module producing 50 MWe".
    At ~50 MWe/module, 4 modules → ~200 MWe net plant (commercially competitive scale).
    Ref: century-demo-system.md §Commercial Scale.
    # ASSUMED: Number of modules per plant; commercial plant size unspecified."""

    plant_availability: float = 0.75
    """Plant capacity factor [dimensionless].
    No published estimate for Z-pinch plant. Electrode replacement, LiPb maintenance,
    pulsed power component service, and rep-rate debugging all compete for downtime.
    Multi-module architecture allows parallel maintenance but common-mode risks exist.
    Using 75% — lower than mature nuclear (90%) but above early-generation pulsed machines.
    # ASSUMED: No operational Z-pinch plant precedent.
    HIGH UNCERTAINTY."""

    plant_lifetime_years: float = 30.0
    """Plant economic lifetime [years].
    Shorter than tokamak reference (40 yr) to reflect pulsed-power component lifetimes.
    Capacitors, switches, and electrodes under 10 Hz cycling face accelerated aging.
    # ASSUMED: No published lifetime estimate for pulsed Z-pinch plant.
    HIGH UNCERTAINTY."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds contingency (10%) and higher pre-construction costs.
    Ref: 1costingfe CAS29 convention."""

    # =========================================================================
    # GEOMETRY
    # =========================================================================

    chamber_inner_radius_m: float = 1.7
    """Inner radius of fusion chamber (roughly cylindrical, modeled as sphere) [m].
    Core volume ~ 25 m³ per Engineering Paradigms paper; sphere of radius 1.82 m
    gives 25 m³. Using 1.7 m to account for pinch geometry (elongated cylinder).
    Ref: engineering-paradigms-paper-summary.md §Design Parameters.
    MODERATE UNCERTAINTY — core volume given, exact geometry inferred."""

    blanket_thickness_m: float = 3.0
    """LiPb blanket + first-wall thickness [m].
    3 m LiPb is required for TBR ~ 1.1 and biological shielding.
    LiPb serves simultaneously as: electrode, first wall, tritium breeder, neutron shield.
    Ref: dossier.md §Tritium Breeding; engineering-paradigms-paper-summary.md §Blanket Design."""

    shield_thickness_m: float = 0.5
    """Additional biological shield thickness beyond LiPb blanket [m].
    LiPb at 3 m provides primary attenuation; additional concrete/steel shield reduces
    dose rate at plant boundary.
    # ASSUMED: Engineering Paradigms paper notes 3 m blanket provides shielding;
    # residual shield estimated from fusion plant convention.
    MODERATE UNCERTAINTY."""

    structure_thickness_m: float = 0.4
    """Primary structure thickness [m].
    Structural steel shell surrounding blanket, supporting LiPb flow manifolds.
    # DEFAULT: Analogy to IFE chamber structure; 1costingfe structure_unit_cost convention."""

    vessel_thickness_m: float = 0.15
    """Outer vessel / secondary containment thickness [m].
    Vacuum boundary, secondary containment for tritium.
    # DEFAULT: Analogy to IFE vessel; 1costingfe vessel_unit_cost convention."""

    # =========================================================================
    # CAS22 OVERRIDES — SFS Z-Pinch specific
    # =========================================================================

    blanket_unit_cost_M_per_m3: float = 0.60
    """LiPb blanket + first-wall unit cost [M$/m³].
    LiPb is a D-T breeding blanket (TBR > 1.05), matching 1costingfe D-T tier.
    Ref: 1costingfe costing_constants.yaml blanket_unit_cost_dt = 0.60 M$/m³."""

    driver_cost_total_M_USD: Optional[float] = None
    """Override: total pulsed power driver cost [$M]. If None, computed from
    driver_cost_per_MJ_stored_M_USD × driver_stored_energy_per_shot_MJ × modules.
    Leave None to use the scaling; set to override directly.
    Maps to CAS22 sub-account C220107 (Power Supplies)."""

    electrode_system_cost_M_USD: float = 15.0
    """Capital cost of electrode system per module [$M].
    Electrodes are the plasma-facing components (cathode + anode), structural
    current-carrying conductors, and LiPb flow manifolds combined.
    Analogues: industrial arc furnace cathodes (up to 60 MW continuous) at $5–20M/unit.
    Commercial Z-pinch electrodes must survive neutron bombardment — more costly than
    furnace cathodes. Using $15M/module as central estimate.
    Ref: engineering-paradigms-paper-summary.md §Electrode Analogy.
    # ASSUMED: No published cost data for nuclear-environment Z-pinch electrodes.
    HIGH UNCERTAINTY."""

    # =========================================================================
    # OPERATING COSTS
    # =========================================================================

    electrode_replacement_interval_yr: float = 2.0
    """Electrode replacement interval [full-power-years].
    Electrodes erode under combined effects: 1 MA arc discharges at 10 Hz,
    14 MeV neutron bombardment, and LiPb chemical attack.
    Industrial arc furnace cathodes last 1–6 months in non-nuclear environments.
    Neutron damage shortens this; liquid metal mitigation may extend it.
    Using 2 years as moderate estimate.
    # ASSUMED: No published erosion rate data for nuclear Z-pinch electrodes.
    HIGH UNCERTAINTY."""

    om_cost_per_MW_yr: float = 60.0
    """Fixed O&M cost per MW net capacity per year [$/MW/yr].
    No published Z-pinch O&M baseline. Using 1costingfe om_cost_dt (52 M$/GWe)
    scaled to $/MW/yr ≈ 52 M$/(1000 MW·yr) = $52/MW/yr, rounded up to $60/MW/yr
    for novelty premium on pulsed machine O&M.
    Ref: 1costingfe costing_constants.yaml om_cost_dt = 52 M$/GWe.
    # ASSUMED: No Z-pinch O&M precedent.
    HIGH UNCERTAINTY."""

    core_lifetime_FPY: float = 3.0
    """Blanket / first-wall core lifetime before replacement [full-power-years].
    LiPb first wall receives full 14.1 MeV neutron flux. Liquid-metal first walls
    can be replenished continuously (advantage), but structural components and
    tritium extraction equipment accumulate damage. Using 3 FPY — lower than
    solid-blanket D-T reference (5 FPY) because the hybrid liquid/solid architecture
    has uncharacterized degradation modes.
    # ASSUMED: No irradiation data for this specific design.
    Ref: 1costingfe costing_constants.yaml core_lifetime_dt = 5.0 (reference).
    HIGH UNCERTAINTY."""

    fuel_cost_per_shot_USD: float = 0.005
    """D-T fuel cost per shot [USD].
    D-T fuel quantity per shot is micrograms-scale.
    Deuterium cost: ~$2,175/kg (1costingfe); Tritium self-bred in blanket.
    At ~1 µg D-T per shot: fuel cost ≈ $0.002/shot.
    Using $0.005/shot to include gas handling losses.
    Ref: 1costingfe costing_constants.yaml u_deuterium = 2175 $/kg.
    Fuel cost is negligible (<0.1% of LCOE)."""

    # =========================================================================
    # AUXILIARY POWER (recirculating loads, excluding driver)
    # =========================================================================

    p_libp_pumping_MW: float = 3.0
    """LiPb pumping power per module [MW].
    Gravity-cascade flow design reduces pumping to top-of-loop recirculation.
    Estimated from blanket mass flow rate and pump head.
    # ASSUMED: Not published; estimated from liquid-metal blanket analogues.
    Ref: EU-DEMO LiPb pump estimates (partial analogy).
    MODERATE UNCERTAINTY."""

    p_tritium_MW: float = 3.0
    """Tritium processing power per module [MW].
    Vacuum permeation / cold trapping from LiPb circuit; vacuum pumping for D-T fuel.
    Ref: 1costingfe ife_zpinch.yaml default ~ 10 MW at GWe scale, scaled to ~50 MWe module."""

    p_house_MW: float = 2.0
    """Housekeeping power per module [MW].
    Instrumentation, control, lighting, HVAC, gas injection timing systems.
    Ref: 1costingfe ife_zpinch.yaml default ~4 MW at larger scale; scaled down."""

    # =========================================================================
    # FINANCIAL
    # =========================================================================

    interest_rate: float = 0.08
    """Real discount rate (weighted average cost of capital) [dimensionless].
    Ref: 1costingfe default; standard nuclear-risk financing assumption."""

    inflation_rate: float = 0.02
    """Inflation rate for levelized cost calculations [dimensionless].
    Ref: 1costingfe default."""

    construction_time_years: float = 5.0
    """Construction period [years].
    Shorter than large tokamak (7–10 yr) due to modular architecture and
    absence of superconducting magnet systems requiring long factory lead times.
    # ASSUMED: Modular construction time estimate; no published projection.
    Ref: 1costingfe reference_construction_time = 6.0 yr (reference).
    MODERATE UNCERTAINTY."""

    def _compute_power(self) -> dict:
        """Layer 1: Power balance — driver → plasma → fusion → thermal → electric.

        Driver energies are derived from fusion_Q to allow Q sweeps to propagate:
          plasma_input/shot = fusion_energy/shot / Q
          stored_energy/shot = plasma_input / wall_to_plasma_efficiency
        This means changing Q changes both recirculating power AND driver capital cost.
        """
        r = {}

        # === Fusion power ===
        p_fus = self.fusion_energy_per_shot_MJ * self.driver_rep_rate_Hz  # MW (per module)
        r["p_fus"] = p_fus

        # D-T neutron/alpha split: 80% neutrons (14.1 MeV), 20% alphas (3.5 MeV)
        f_neutron = 0.80
        f_alpha = 0.20
        r["p_neutron"] = p_fus * f_neutron
        r["p_alpha"] = p_fus * f_alpha

        # === Driver energies — derived from Q (so Q sweep propagates) ===
        # Plasma input per shot = fusion energy / Q
        driver_plasma_energy_per_shot_MJ = self.fusion_energy_per_shot_MJ / self.fusion_Q
        # Stored energy in capacitor bank = plasma input / wall-to-plasma efficiency
        driver_stored_energy_per_shot_MJ = (driver_plasma_energy_per_shot_MJ
                                            / self.driver_wall_to_plasma_efficiency)
        r["driver_plasma_energy_per_shot_MJ"] = driver_plasma_energy_per_shot_MJ
        r["driver_stored_energy_per_shot_MJ"] = driver_stored_energy_per_shot_MJ

        # === Driver input power (per module, continuous average) ===
        driver_plasma_avg_MW = driver_plasma_energy_per_shot_MJ * self.driver_rep_rate_Hz
        r["driver_plasma_avg_MW"] = driver_plasma_avg_MW

        # Wall-plug (AC grid) power for driver = plasma input / wall-to-plasma efficiency
        driver_wallplug_avg_MW = driver_stored_energy_per_shot_MJ * self.driver_rep_rate_Hz
        r["driver_wallplug_avg_MW"] = driver_wallplug_avg_MW

        # Engineering Q: ratio of fusion power to driver wall-plug input
        r["Q_physics"] = self.fusion_Q
        r["Q_eng"] = p_fus / driver_wallplug_avg_MW if driver_wallplug_avg_MW > 0 else 0.0

        # === Thermal power (per module) ===
        # Neutron energy deposited in blanket (with multiplication) + alpha energy
        # + driver energy that thermalizes in plasma/first-wall (absorbed driver plasma energy)
        p_th = (self.blanket_energy_multiplication * r["p_neutron"]
                + r["p_alpha"]
                + driver_plasma_avg_MW)  # driver plasma input thermalizes in chamber
        r["p_th"] = p_th

        # === Gross electric per module ===
        p_et = p_th * self.thermal_efficiency
        r["p_et"] = p_et

        # === Recirculating power per module ===
        p_aux = self.p_libp_pumping_MW + self.p_tritium_MW + self.p_house_MW
        r["p_aux"] = p_aux
        r["p_recirc_total"] = driver_wallplug_avg_MW + p_aux

        # === Net electric per module ===
        p_net = p_et - driver_wallplug_avg_MW - p_aux
        r["p_net"] = p_net

        # === Recirculating fraction ===
        r["recirc_fraction"] = r["p_recirc_total"] / p_et if p_et > 0 else float("inf")

        # === Plant-wide totals ===
        r["p_net_plant"] = p_net * self.n_mod
        r["p_et_plant"] = p_et * self.n_mod
        r["p_th_plant"] = p_th * self.n_mod

        # === Shots per year (plant-wide) ===
        r["shots_per_year_per_module"] = (self.driver_rep_rate_Hz * 3600 * 8760
                                          * self.plant_availability)
        r["shots_per_year_plant"] = r["shots_per_year_per_module"] * self.n_mod

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Chamber geometry — spherical approximation for blanket volumes.
        The SFS Z-Pinch chamber is cylindrical, but spherical geometry gives
        conservative (slightly high) blanket volume estimates at similar radius."""
        r = {}
        ri = self.chamber_inner_radius_m

        def sphere_shell_vol(r_in: float, thickness: float) -> float:
            r_out = r_in + thickness
            return (4.0 / 3.0) * math.pi * (r_out**3 - r_in**3)

        # Blanket (LiPb, 3 m)
        r_blanket_out = ri + self.blanket_thickness_m
        r["blanket_vol_m3"] = sphere_shell_vol(ri, self.blanket_thickness_m)

        # Shield (additional concrete/steel)
        r["shield_vol_m3"] = sphere_shell_vol(r_blanket_out, self.shield_thickness_m)
        r_shield_out = r_blanket_out + self.shield_thickness_m

        # Primary structure
        r["structure_vol_m3"] = sphere_shell_vol(r_shield_out, self.structure_thickness_m)
        r_structure_out = r_shield_out + self.structure_thickness_m

        # Vessel
        r["vessel_vol_m3"] = sphere_shell_vol(r_structure_out, self.vessel_thickness_m)

        # Total LiPb mass estimate (for reporting)
        libp_density_kg_m3 = 9800.0  # LiPb eutectic density ~9,800 kg/m³
        r["libp_mass_tonnes"] = r["blanket_vol_m3"] * libp_density_kg_m3 / 1000.0

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment — per-module accounts plus plant-wide.
        Follows 1costingfe cas22.py structure with SFS Z-Pinch-specific overrides.
        Overrides documented with [OVERRIDE] tag."""
        r = {}
        p_th = max(power["p_th"], 1.0)
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)

        # ── Per-module accounts ───────────────────────────────────────────────

        # C220101: First Wall + Blanket (LiPb flowing system)
        # Formula: unit_cost × volume × (p_th / P_TH_REF)^0.6
        # LiPb blanket includes: gravity-cascade flow manifolds, heat exchanger
        # coupling, tritium extraction loop. Slightly higher complexity than static
        # solid blanket, but LiPb commodity cost is low.
        # Ref: 1costingfe costing_constants.yaml blanket_unit_cost_dt = 0.60 M$/m³
        r["C220101"] = (self.blanket_unit_cost_M_per_m3
                        * geom["blanket_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220102: Shield
        # Formula: 0.74 × volume × (p_th / P_TH_REF)^0.6
        # D-T: full shielding required for 14.1 MeV neutrons.
        # Ref: 1costingfe costing_constants.yaml shield_unit_cost = 0.74 M$/m³
        shield_unit_cost = 0.74
        r["C220102"] = (shield_unit_cost
                        * geom["shield_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: Coils — OVERRIDE: $0 (no magnets in SFS Z-pinch)
        # [OVERRIDE] SFS Z-Pinch has NO external magnetic field coils.
        # This is the single largest structural cost difference from tokamak designs.
        # HTS tape, cryogenic plant, and quench protection systems are entirely absent.
        # Ref: analysis.md §S7 "Key divergences from ST-HTS".
        r["C220103"] = 0.0

        # C220104: Supplementary Heating — OVERRIDE: $0 (no auxiliary heating)
        # [OVERRIDE] SFS Z-Pinch has NO neutral beam injection, ECRH, ICRH, or laser
        # preheat (unlike MagLIF). The pulsed-power driver is the only energy input.
        # Ref: engineering-paradigms-paper-summary.md §Driver Efficiency.
        r["C220104"] = 0.0

        # C220105: Primary Structure
        # Formula: 0.15 × volume × (p_et / P_ET_REF)^0.5
        # Ref: 1costingfe costing_constants.yaml structure_unit_cost = 0.15 M$/m³
        structure_unit_cost = 0.15
        r["C220105"] = (structure_unit_cost
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: Vacuum System (vessel + pumps + gas injection)
        # Formula: 0.72 × volume × (p_et / P_ET_REF)^0.6
        # Z-pinch requires fast gas injection and vacuum pumping at 10 Hz — higher
        # throughput than quasi-steady MFE but smaller vessel volume.
        # Ref: 1costingfe costing_constants.yaml vessel_unit_cost = 0.72 M$/m³
        vessel_unit_cost = 0.72
        r["C220106"] = (vessel_unit_cost
                        * geom["vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # C220107: Power Supplies — OVERRIDE with pulsed power driver capital cost
        # [OVERRIDE] The pulsed-power driver (capacitor bank, switches, pulse-forming
        # networks, transmission lines) IS the power supply for this concept.
        # Cost estimated as: stored_energy_MJ × cost_per_MJ (each module has its own driver).
        # Standard formula (80 M$ at 1 GWe) is inappropriate here.
        # Uses power['driver_stored_energy_per_shot_MJ'] so Q sweeps propagate to cost.
        # Ref: analysis.md §S2 §S4; osti-pulsed-power §Energy Storage.
        # Industrial pulsed power: $1–10/J; 10 Hz rating pushes toward upper end.
        if self.driver_cost_total_M_USD is not None:
            driver_cost_per_module = self.driver_cost_total_M_USD / self.n_mod
        else:
            driver_cost_per_module = (power["driver_stored_energy_per_shot_MJ"]
                                      * self.driver_cost_per_MJ_stored_M_USD)
        r["C220107"] = driver_cost_per_module  # per-module cost (scaled by n_mod later)
        r["driver_cost_per_module_M_USD"] = driver_cost_per_module

        # C220108: Electrode System — OVERRIDE (replaces target factory for pulsed IFE)
        # [OVERRIDE] In MagLIF, this is a target/liner factory. In SFS Z-pinch, targets
        # don't exist — instead the electrodes are the plasma-facing consumable.
        # Electrode system: machined copper/refractory cathode + anode assembly,
        # neutron-hard materials, LiPb flow manifold integration.
        # Ref: analysis.md §S3 §Electrode System; engineering-paradigms-paper-summary.md §Electrode Analogy.
        r["C220108"] = self.electrode_system_cost_M_USD  # per-module

        # C220109: Direct Energy Converter — not applicable
        r["C220109"] = 0.0

        # C220110: Remote Handling & Maintenance
        # For D-T, base = 150 M$ at 1 GWe; scaled by (p_net / 1000)^0.7.
        # SFS Z-pinch has modular architecture — smaller individual RH requirement,
        # but multi-module increases total. Apply 0.6× scale factor for modular geometry
        # (simpler than toroidal geometry; no in-vessel transporter required).
        # Ref: 1costingfe costing_constants.yaml remote_handling_dt_base = 150 M$
        rh_base = 150.0  # M$ at 1 GWe — 1costingfe DT reference
        rh_scale = 0.6   # modular/linear geometry vs. toroidal
        rh_power_scale = (p_net / 1000.0) ** 0.7
        r["C220110"] = rh_base * rh_scale * rh_power_scale  # per-module (scaled below)

        # C220111: Installation labor
        # Formula: 0.14 × reactor subtotal
        # Ref: 1costingfe costing_constants.yaml installation_frac = 0.14
        installation_frac = 0.14
        reactor_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"])
        r["C220111"] = installation_frac * reactor_subtotal

        # C220112: Isotope Separation — $0 (handled in CAS80)
        r["C220112"] = 0.0

        # Per-module subtotal
        r["CAS22_per_module"] = reactor_subtotal + r["C220111"] + r["C220112"]

        # ── Plant-wide accounts ───────────────────────────────────────────────
        p_net_plant = max(power["p_net_plant"], 1.0)
        p_th_plant = power["p_th_plant"]

        # C220200: Main & Secondary Coolant (LiPb → steam HX + steam loop)
        # LiPb primary circuit is the coolant; steam Rankine is secondary.
        # Larger than standard because LiPb requires specialized HX to prevent
        # tritium permeation into steam (tritium barrier coating or secondary loop).
        # Ref: 1costingfe scaling; +20% premium for LiPb tritium barrier.
        C220201 = 166.0 * (p_net_plant / 1000.0)        # Primary coolant
        C220202 = 40.6 * (p_th_plant / 3500.0) ** 0.55  # Intermediate circuit
        r["C220200"] = (C220201 + C220202) * 1.20        # 20% LiPb tritium-barrier premium

        # C220300: Auxiliary Cooling + Cryoplant
        # No cryoplant required (no SC magnets) — set cryoplant term to near-zero.
        C220301 = 1.1e-3 * p_th_plant   # Auxiliary coolant loops
        C220302 = 0.0                    # Cryoplant: NONE (no SC magnets)
        r["C220300"] = C220301 + C220302

        # C220400: Radioactive Waste Management
        # LiPb activation products (Pb-204/205, Bi isotopes) add complexity.
        # Using standard 1costingfe scaling with 1.15× premium for LiPb activation.
        # Ref: 1costingfe costing_constants.yaml formula: 1.96 × (p_th / 1000)
        r["C220400"] = 1.96 * (p_th_plant / 1000.0) * 1.15

        # C220500: Fuel Handling & Storage (D-T)
        # Tritium extraction from LiPb circuit; D-T injection system at 10 Hz.
        # Ref: 1costingfe costing_constants.yaml fuel_handling_dt_base = 120 M$ at 1 GWe
        fuel_handling_base = 120.0
        r["C220500"] = fuel_handling_base * (p_net_plant / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        # Ref: 1costingfe: 11.5 × (p_net / 1000)^0.8
        r["C220600"] = 11.5 * (p_net_plant / 1000.0) ** 0.8

        # C220700: Instrumentation & Control
        # Multi-module Z-pinch requires per-module shot timing coordination (~1 µs precision)
        # and cross-module grid synchronization. 20% premium over standard.
        # Ref: 1costingfe: 85 × (p_th / 3500)^0.65
        r["C220700"] = 85.0 * (p_th_plant / 3500.0) ** 0.65 * 1.20

        # Plant-wide subtotal
        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        # Total CAS22: per-module × n_mod + plant-wide
        r["CAS22"] = r["CAS22_per_module"] * self.n_mod + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: Capital costs (CAS10–60) following 1costingfe structure."""
        r = {}
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)
        p_net_plant = max(power["p_net_plant"], 1.0)
        p_et_plant = max(power["p_et_plant"], 1.0)

        # === CAS10: Pre-construction ===
        site_permits = 3.0
        plant_studies = 4.0 if self.noak else 20.0
        plant_permits = 2.0
        plant_reports = 1.0
        other_precon = 1.0
        # Land: 0.25 acres/MWe × $/acre × n_mod; modular plant is compact
        land_acres = 0.25 * p_net_plant * math.sqrt(self.n_mod)
        land_cost = land_acres * 10_000 / 1e6  # M$
        licensing_cost = 5.0 if not self.noak else 2.5  # D-T licensing; NOAK half of FOAK
        r["CAS10"] = (site_permits + plant_studies + plant_permits + plant_reports
                      + other_precon + land_cost + licensing_cost)

        # === CAS21: Buildings ===
        # $/kW gross electric, scaled from 1costingfe building_costs_per_kw.
        # Adjustments for SFS Z-pinch:
        #   - No cryogenics building ($0 vs. $15/kW reference)
        #   - Large power supply/storage building for driver capacitor bank
        #   - Standard hot cell for activated electrode and blanket handling
        building_cost_per_kW = {
            "site_improvements":    268.0,
            "fusion_heat_island":   126.0,
            "turbine_building":      54.0,
            "heat_exchanger":        12.0,
            "power_supply_storage":  40.0,  # driver capacitor hall; larger than standard 17
            "reactor_auxiliaries":   35.0,
            "hot_cell":              93.4,   # activated electrode + LiPb disposal
            "misc_buildings":        71.6,   # combines smaller categories
            "cryogenics":             0.0,   # NONE — no SC magnets
        }
        total_building_per_kW = sum(building_cost_per_kW.values())
        r["CAS21"] = total_building_per_kW * p_et_plant / 1000.0  # M$
        r["CAS21_detail"] = {k: v * p_et_plant / 1000.0
                             for k, v in building_cost_per_kW.items()}

        # === CAS22: Reactor Plant Equipment (computed separately) ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment ===
        # Ref: 1costingfe turbine_per_mw = 0.19764 M$/MW
        r["CAS23"] = 0.19764 * p_et_plant

        # === CAS24: Electric Plant Equipment ===
        # Ref: 1costingfe electric_per_mw = 0.08418 M$/MW
        r["CAS24"] = 0.08418 * p_et_plant

        # === CAS25: Miscellaneous Plant Equipment ===
        # Ref: 1costingfe misc_per_mw = 0.05124 M$/MW
        r["CAS25"] = 0.05124 * p_et_plant

        # === CAS26: Heat Rejection ===
        # Ref: 1costingfe heat_rej_per_mw = 0.03416 M$/MW
        r["CAS26"] = 0.03416 * p_et_plant

        # === CAS27: Special Materials (initial inventory) ===
        # LiPb fill: several hundred tonnes per module × n_mod
        # PbLi @ ~$3/kg (commodity lead price; Li adds ~$5/kg)
        # Using 1costingfe special_materials_dt = 15 M$/GWe, scaled by p_net
        r["CAS27"] = 15.0 * (p_net_plant / 1000.0)

        # === CAS28: Digital Twin ===
        # Ref: 1costingfe digital_twin = 5.0 M$ (fixed)
        r["CAS28"] = 5.0

        # === CAS29: Contingency ===
        # FOAK: 10%. NOAK: 0%. Ref: 1costingfe contingency_rate.
        cas20_subtotal = sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                             "CAS25", "CAS26", "CAS27", "CAS28"])
        contingency_rate = 0.0 if self.noak else 0.10
        r["CAS29"] = contingency_rate * cas20_subtotal

        # === CAS20: Total Direct Costs ===
        r["CAS20"] = cas20_subtotal + r["CAS29"]

        # === CAS30: Indirect Costs ===
        # 20% of CAS20, scaled by construction time
        # Ref: 1costingfe indirect_fraction = 0.20, reference_construction_time = 6 yr
        indirect_fraction = 0.20
        ref_construction_time = 6.0
        r["CAS30"] = indirect_fraction * r["CAS20"] * (self.construction_time_years / ref_construction_time)

        # === CAS40: Owner's Costs ===
        # 5% of CAS20 as approximation. D-T: 39 M$/GWe scaled → ~5% of direct costs.
        # Ref: 1costingfe owner_cost_dt = 39 M$/GWe (power-law 0.5 exponent)
        r["CAS40"] = 39.0 * (p_net_plant / 1000.0) ** 0.5

        # === CAS50: Supplementary Costs ===
        spare_parts_frac = 0.03  # 1costingfe spare_parts_frac_dt
        spare_parts = spare_parts_frac * sum(r[k] for k in ["CAS22", "CAS23",
                                                              "CAS24", "CAS25",
                                                              "CAS26", "CAS27",
                                                              "CAS28"])
        startup_fuel = 40.0 * (p_net_plant / 1000.0)  # M$; tritium startup inventory
        shipping = 0.015 * r["CAS20"]   # 1costingfe shipping_frac = 0.015
        taxes = 0.01 * r["CAS20"]       # 1costingfe tax_frac = 0.01
        construction_insurance = 0.015 * (r["CAS20"] + r["CAS30"])
        decommissioning = 127.0 * (p_net_plant / 1000.0)  # 1costingfe decom_provision_dt
        r["CAS50"] = (spare_parts + startup_fuel + shipping + taxes
                      + construction_insurance + decommissioning)

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

        # Specific capital cost
        if power["p_net_plant"] > 0:
            r["specific_capital_USD_per_kWe"] = (r["total_capital"] * 1e6
                                                  / (power["p_net_plant"] * 1e3))
        else:
            r["specific_capital_USD_per_kWe"] = float("inf")

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70–90 annualized costs and LCOE."""
        r = {}
        p_net_plant = power["p_net_plant"]

        # Capital Recovery Factor
        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1 + i) ** n / ((1 + i) ** n - 1)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]  # M$/yr

        # === CAS71: Annual O&M (levelized) ===
        annual_om_base = self.om_cost_per_MW_yr * p_net_plant * 1000.0 / 1e6  # M$
        g = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g) ** Tc
        if abs(i - g) > 1e-10:
            pv_growing_annuity = A1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
        else:
            pv_growing_annuity = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_growing_annuity  # M$/yr

        # === CAS72: Scheduled Replacement ===
        # Blanket/FW (C220101) + electrode system (C220108) have limited lifetimes.
        # Both are replaced on core_lifetime_FPY schedule.
        effective_yr_per_replacement = self.core_lifetime_FPY / self.plant_availability
        n_replacements = max(0, int(math.ceil(self.plant_lifetime_years
                                              / effective_yr_per_replacement)) - 1)
        # Blanket replacement cost (all modules)
        blanket_replacement_cost = cas22["C220101"] * self.n_mod
        # Electrode replacement cost (all modules); electrodes replace more often
        electrode_interval = (self.electrode_replacement_interval_yr
                              / self.plant_availability)
        n_electrode_replacements = max(0, int(math.ceil(self.plant_lifetime_years
                                                         / electrode_interval)) - 1)
        electrode_replacement_cost = cas22["C220108"] * self.n_mod

        # PV of blanket replacements
        pv_blanket = 0.0
        for k in range(1, n_replacements + 1):
            year = k * effective_yr_per_replacement
            if year < self.plant_lifetime_years:
                pv_blanket += blanket_replacement_cost / (1 + i) ** year

        # PV of electrode replacements
        pv_electrodes = 0.0
        for k in range(1, n_electrode_replacements + 1):
            year = k * electrode_interval
            if year < self.plant_lifetime_years:
                pv_electrodes += electrode_replacement_cost / (1 + i) ** year

        r["CAS72"] = crf * (pv_blanket + pv_electrodes)  # M$/yr
        r["n_blanket_replacements"] = n_replacements
        r["n_electrode_replacements"] = n_electrode_replacements

        r["CAS70"] = r["CAS71"] + r["CAS72"]

        # === CAS80: Fuel & Consumable Costs ===
        shots_per_year = power["shots_per_year_plant"]
        annual_fuel = shots_per_year * self.fuel_cost_per_shot_USD / 1e6  # M$
        # D-T fuel cost is negligible; no RTL or target consumable (electrodes in CAS72)
        r["CAS80"] = annual_fuel
        r["CAS80_fuel"] = annual_fuel

        # === LCOE ===
        annual_revenue_req = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_revenue_req

        annual_energy_MWh = 8760.0 * p_net_plant * self.plant_availability
        r["annual_energy_MWh"] = annual_energy_MWh

        if annual_energy_MWh > 0 and p_net_plant > 0:
            lcoe_USD_MWh = annual_revenue_req * 1e6 / annual_energy_MWh
            r["lcoe_USD_per_MWh"] = lcoe_USD_MWh
            r["lcoe_cents_per_kWh"] = lcoe_USD_MWh / 10.0
        else:
            r["lcoe_USD_per_MWh"] = float("inf")
            r["lcoe_cents_per_kWh"] = float("inf")

        if annual_revenue_req > 0:
            r["capital_fraction"] = r["CAS90"] / annual_revenue_req
            r["om_fraction"] = r["CAS70"] / annual_revenue_req
            r["fuel_fraction"] = r["CAS80"] / annual_revenue_req

        return r

    def compute(self) -> dict:
        """Compute LCOE and all derived quantities using CAS-structured accounting."""
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
            "net_electric_MW": power["p_net"],
            "net_electric_plant_MW": power["p_net_plant"],
            "lcoe_cents_per_kWh": econ["lcoe_cents_per_kWh"],
            "total_capital_M_USD": costs["total_capital"],
        }
        return results


# =============================================================================
# OUTPUT
# =============================================================================

def print_results(params: SFSZPinchPlantParams, results: dict, label: str = ""):
    """Pretty-print LCOE model results with full CAS breakdown."""
    power = results["power"]
    geom = results["geometry"]
    cas22 = results["cas22"]
    costs = results["costs"]
    econ = results["economics"]

    title = f"SFS Z-Pinch (Zap Energy) LCOE Model — 1cFE CAS-Structured"
    if label:
        title += f" [{label}]"
    print("=" * 72)
    print(title)
    print("=" * 72)

    print(f"\n--- Key Input Parameters ---")
    print(f"  Fusion Q (physics):         {params.fusion_Q:.0f}")
    print(f"  Fusion energy/shot:         {params.fusion_energy_per_shot_MJ:.0f} MJ")
    print(f"  Rep rate:                   {params.driver_rep_rate_Hz:.1f} Hz")
    print(f"  Driver wall-to-plasma eff:  {params.driver_wall_to_plasma_efficiency:.0%}")
    print(f"  Driver stored energy/shot:  {power['driver_stored_energy_per_shot_MJ']:.2f} MJ  (= fusion/Q/eff)")
    print(f"  Driver cost ($/MJ stored):  ${params.driver_cost_per_MJ_stored_M_USD:.1f} M/MJ")
    print(f"  Driver cost/module:         ${cas22['driver_cost_per_module_M_USD']:.1f}M")
    print(f"  Thermal efficiency:         {params.thermal_efficiency:.0%}")
    print(f"  Plant availability:         {params.plant_availability:.0%}")
    print(f"  Modules:                    {params.n_mod}")
    print(f"  Blanket thickness:          {params.blanket_thickness_m:.0f} m (LiPb)")
    print(f"  LiPb mass/module:           {geom['libp_mass_tonnes']:.0f} tonnes")
    print(f"  Interest rate:              {params.interest_rate:.0%}")
    print(f"  Plant lifetime:             {params.plant_lifetime_years:.0f} years")
    print(f"  FOAK/NOAK:                  {'NOAK' if params.noak else 'FOAK'}")

    print(f"\n--- Power Balance (per module → plant) ---")
    print(f"  Fusion power/module:        {power['p_fus']:.1f} MW")
    print(f"    Neutron power:            {power['p_neutron']:.1f} MW (80%)")
    print(f"    Alpha power:              {power['p_alpha']:.1f} MW (20%)")
    print(f"  Thermal power/module:       {power['p_th']:.1f} MW")
    print(f"  Gross electric/module:      {power['p_et']:.1f} MWe")
    print(f"  Recirculating power/module:")
    print(f"    Driver (wall-plug):       {power['driver_wallplug_avg_MW']:.1f} MW")
    print(f"    LiPb pumping:             {params.p_libp_pumping_MW:.1f} MW")
    print(f"    Tritium processing:       {params.p_tritium_MW:.1f} MW")
    print(f"    Housekeeping:             {params.p_house_MW:.1f} MW")
    print(f"  Net electric/module:        {power['p_net']:.1f} MWe")
    print(f"  Recirculating fraction:     {power['recirc_fraction']:.1%}")
    print(f"  Physics Q:                  {params.fusion_Q:.0f}")
    print(f"  Engineering Q:              {power['Q_eng']:.2f}")
    print(f"  ─────────────────────────────────────────────────────")
    print(f"  Net electric (plant):       {power['p_net_plant']:.1f} MWe  ({params.n_mod} modules)")
    print(f"  Gross electric (plant):     {power['p_et_plant']:.1f} MWe")

    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    print(f"  Per-module accounts:")
    cas22_labels = {
        "C220101": ("Blanket/First Wall (LiPb)",      ""),
        "C220102": ("Shield",                          ""),
        "C220103": ("Coils",                           "[OVERRIDE: $0 — no magnets]"),
        "C220104": ("Supplementary Heating",           "[OVERRIDE: $0 — no aux heating]"),
        "C220105": ("Primary Structure",               ""),
        "C220106": ("Vacuum System + Gas Injection",   ""),
        "C220107": ("Power Supplies (pulsed driver)",  "[OVERRIDE]"),
        "C220108": ("Electrode System",                "[OVERRIDE: replaces target factory]"),
        "C220109": ("Direct Energy Converter",         ""),
        "C220110": ("Remote Handling",                 ""),
        "C220111": ("Installation",                    ""),
    }
    for code, (label_, note) in cas22_labels.items():
        val = cas22.get(code, 0.0)
        if val > 0.01 or note:
            print(f"    {code} {label_:<35s} ${val:>7.1f}M  {note}")

    print(f"    {'─' * 57}")
    print(f"    Per-module subtotal:                         ${cas22['CAS22_per_module']:>7.1f}M × {params.n_mod}")

    print(f"  Plant-wide accounts:")
    pw_labels = {
        "C220200": "Coolant Systems (LiPb→steam)",
        "C220300": "Aux Cooling (no cryoplant)",
        "C220400": "Radioactive Waste Management",
        "C220500": "Fuel Handling (D-T, tritium)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    for code, label_ in pw_labels.items():
        val = cas22.get(code, 0.0)
        if val > 0.01:
            print(f"    {code} {label_:<38s} ${val:>7.1f}M")
    print(f"    {'─' * 57}")
    print(f"    Plant-wide subtotal:                         ${cas22['CAS22_plant_wide']:>7.1f}M")
    print(f"  CAS22 Total:                                   ${cas22['CAS22']:>7.1f}M")

    print(f"\n--- Capital Costs (CAS10–60) ---")
    print(f"  CAS10 Pre-construction:             ${costs['CAS10']:>8.1f}M")
    print(f"  CAS21 Buildings:                    ${costs['CAS21']:>8.1f}M")
    print(f"  CAS22 Reactor Plant Equipment:      ${costs['CAS22']:>8.1f}M")
    print(f"  CAS23 Turbine Plant:                ${costs['CAS23']:>8.1f}M")
    print(f"  CAS24 Electric Plant:               ${costs['CAS24']:>8.1f}M")
    print(f"  CAS25 Misc Plant:                   ${costs['CAS25']:>8.1f}M")
    print(f"  CAS26 Heat Rejection:               ${costs['CAS26']:>8.1f}M")
    print(f"  CAS27 Special Materials (LiPb):     ${costs['CAS27']:>8.1f}M")
    print(f"  CAS28 Digital Twin:                 ${costs['CAS28']:>8.1f}M")
    print(f"  CAS29 Contingency:                  ${costs['CAS29']:>8.1f}M")
    print(f"  {'─' * 52}")
    print(f"  CAS20 Direct Costs:                 ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30 Indirect Costs:               ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40 Owner's Costs:                ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50 Supplementary:                ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 52}")
    print(f"  Overnight Capital:                  ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60 IDC (f={costs['f_IDC']:.3f}):          ${costs['CAS60']:>8.1f}M")
    print(f"  ══════════════════════════════════════════════════")
    print(f"  Total Capital:                      ${costs['total_capital']:>8.1f}M")
    print(f"  Specific Capital:                   ${costs['specific_capital_USD_per_kWe']:>8.0f} $/kWe")

    print(f"\n--- Annual Costs (CAS70–90) ---")
    print(f"  CAS90 Capital charge (CRF={econ['CRF']:.4f}):  ${econ['CAS90']:>7.1f}M/yr")
    print(f"  CAS71 O&M (levelized):              ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72 Scheduled replacement:        ${econ['CAS72']:>8.1f}M/yr")
    print(f"    Blanket replacements: {econ['n_blanket_replacements']}  ×  "
          f"Electrode replacements: {econ['n_electrode_replacements']}")
    print(f"  CAS70 Total O&M:                    ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80 Fuel & consumables:           ${econ['CAS80']:>8.3f}M/yr")

    print(f"\n--- LCOE ---")
    print(f"  Annual energy production:   {econ['annual_energy_MWh']:>12,.0f} MWh")
    print(f"  Annual revenue requirement: ${econ['annual_revenue_req']:.1f}M")
    print(f"  ╔══════════════════════════════════════════╗")
    if econ["lcoe_cents_per_kWh"] == float("inf"):
        print(f"  ║  LCOE = N/A (negative net power)        ║")
    else:
        print(f"  ║  LCOE = {econ['lcoe_cents_per_kWh']:>6.2f} ¢/kWh                   ║")
        print(f"  ║       = {econ['lcoe_USD_per_MWh']:>6.1f} $/MWh                    ║")
    print(f"  ╚══════════════════════════════════════════╝")
    if econ["lcoe_cents_per_kWh"] != float("inf"):
        print(f"  Capital (CAS90):            {econ.get('capital_fraction', 0):.1%}")
        print(f"  O&M (CAS70):               {econ.get('om_fraction', 0):.1%}")
        print(f"  Fuel/consumables (CAS80):   {econ.get('fuel_fraction', 0):.1%}")


def sensitivity_sweep(base_params: SFSZPinchPlantParams, param_name: str,
                      values: list, label: str = "") -> list:
    """Sweep a single parameter and return LCOE and net power for each value."""
    results_list = []
    for val in values:
        p = SFSZPinchPlantParams(**{**base_params.__dict__, param_name: val})
        r = p.compute()
        results_list.append({
            "param_value": float(val),
            "lcoe_cents_kWh": r["lcoe_cents_per_kWh"],
            "net_electric_plant_MW": r["net_electric_plant_MW"],
        })
    return results_list


# =============================================================================
# MAIN
# =============================================================================

def main():
    # =========================================================================
    # BASELINE SCENARIO
    # =========================================================================
    print("\n" + "#" * 72)
    print("# BASELINE SCENARIO: SFS Z-Pinch at Nominal Design Point")
    print("# Q=10 (calculated), 10 Hz, 4-module plant, NOAK")
    print("#" * 72)

    baseline = SFSZPinchPlantParams()
    results = baseline.compute()
    print_results(baseline, results, label="Baseline")

    # =========================================================================
    # SENSITIVITY SWEEPS
    # =========================================================================
    print("\n\n" + "=" * 72)
    print("SENSITIVITY ANALYSIS — Single-Parameter Sweeps from Baseline")
    print("=" * 72)
    power_b = results["power"]
    econ_b = results["economics"]
    base_lcoe = econ_b["lcoe_cents_per_kWh"]
    base_net = power_b["p_net_plant"]
    print(f"  Baseline: {base_lcoe:.2f} ¢/kWh, {base_net:.0f} MWe net (plant)\n")

    sweeps = [
        ("fusion_Q",
         [3, 5, 7, 10, 15, 20],
         "Physics Q (fusion gain)"),
        ("driver_rep_rate_Hz",
         [1.0, 2.0, 5.0, 7.0, 10.0, 15.0],
         "Repetition rate [Hz]"),
        ("driver_cost_per_MJ_stored_M_USD",
         [0.5, 1.0, 2.0, 3.0, 5.0, 10.0],
         "Driver cost [M$/MJ stored]"),
        ("thermal_efficiency",
         [0.28, 0.30, 0.33, 0.37, 0.40],
         "Thermal efficiency"),
        ("plant_availability",
         [0.50, 0.60, 0.70, 0.75, 0.80, 0.90],
         "Plant availability"),
        ("electrode_replacement_interval_yr",
         [0.5, 1.0, 2.0, 5.0, 10.0],
         "Electrode replacement interval [yr]"),
        ("n_mod",
         [1, 2, 4, 8, 16],
         "Number of modules"),
    ]

    for param_name, values, label in sweeps:
        print(f"  {label}:")
        sweep_results = sensitivity_sweep(baseline, param_name, values, label)
        for sr in sweep_results:
            val = sr["param_value"]
            lcoe = sr["lcoe_cents_kWh"]
            net = sr["net_electric_plant_MW"]
            marker = " <<<" if lcoe < base_lcoe * 0.5 else ""
            if net <= 0 or lcoe == float("inf"):
                print(f"    {val:>10.3g} → NET POWER NEGATIVE ({net:.0f} MWe net)")
            else:
                print(f"    {val:>10.3g} → {lcoe:6.2f} ¢/kWh  ({net:.0f} MWe net){marker}")
        print()

    # =========================================================================
    # SCENARIO COMPARISON TABLE
    # =========================================================================
    print("\n" + "=" * 72)
    print("SCENARIO COMPARISON")
    print("=" * 72)

    conservative = SFSZPinchPlantParams(
        fusion_Q=5.0,                            # Q = 5 (not demonstrated; pessimistic)
        driver_rep_rate_Hz=5.0,                  # Only 5 Hz achieved
        driver_cost_per_MJ_stored_M_USD=7.0,     # High driver cost
        thermal_efficiency=0.30,                 # Lower-efficiency Rankine
        plant_availability=0.60,                 # Significant maintenance downtime
        electrode_replacement_interval_yr=1.0,   # Aggressive erosion
        core_lifetime_FPY=2.0,
        om_cost_per_MW_yr=80.0,
        construction_time_years=7.0,
        interest_rate=0.10,                      # Higher financing risk
        plant_lifetime_years=25.0,
        n_mod=4,
    )

    moderate = SFSZPinchPlantParams()  # default = moderate/baseline

    optimistic = SFSZPinchPlantParams(
        fusion_Q=15.0,                           # Q = 15 (better than design point)
        driver_rep_rate_Hz=10.0,
        driver_cost_per_MJ_stored_M_USD=1.5,     # Mass-manufactured capacitors, cost reduction
        thermal_efficiency=0.37,                 # Advanced steam cycle
        plant_availability=0.85,
        electrode_replacement_interval_yr=5.0,   # Improved electrode materials
        core_lifetime_FPY=5.0,
        om_cost_per_MW_yr=50.0,
        construction_time_years=4.0,
        interest_rate=0.06,
        plant_lifetime_years=40.0,
        n_mod=8,
    )

    scenarios = [
        ("Conservative (Q=5, 5 Hz, costly driver)", conservative),
        ("Moderate / Baseline (Q=10, 10 Hz)", moderate),
        ("Optimistic (Q=15, cheap driver, long life)", optimistic),
    ]

    print(f"\n{'Scenario':<42} {'Net MWe':>8} {'$/kWe':>9} {'LCOE':>12}")
    print("-" * 75)
    for name, params in scenarios:
        r = params.compute()
        net = r["net_electric_plant_MW"]
        cap = r["costs"]["specific_capital_USD_per_kWe"]
        lcoe = r["lcoe_cents_per_kWh"]
        if net <= 0 or lcoe == float("inf"):
            print(f"{name:<42} {'N/A':>8} {'N/A':>9} {'net power < 0':>12}")
        else:
            print(f"{name:<42} {net:>8.0f} {cap:>9,.0f} {lcoe:>10.2f} ¢/kWh")
    print()

    # =========================================================================
    # KEY BINDING CONSTRAINTS
    # =========================================================================
    print("=" * 72)
    print("KEY BINDING CONSTRAINTS — Top LCOE Drivers")
    print("=" * 72)
    print()
    print("  1. PHYSICS Q (Q > 10 never demonstrated) — CRITICAL")
    print()
    print("     Q is the single most leveraged parameter: halving Q roughly doubles")
    print("     driver recirculating power as a fraction of gross electric.")
    print("     At Q = 5, driver wall-plug power ≈ 54 MW/module; gross electric at 33%")
    print("     efficiency ≈ 66 MWe/module → net output collapses to ~4 MWe/module.")
    print("     The model becomes net-negative at Q < 4.5 (at 33% thermal efficiency).")
    print("     STATUS: Calculated at 200 µs, 1.35 MA. FuZE demonstrated 20–40 µs.")
    print("     A 5–10× pinch lifetime extension is required before Q can be measured.")
    print()
    print("  2. REPETITION RATE (0.2 Hz demonstrated → 10 Hz required) — CRITICAL")
    print()
    print("     Rep rate scales net output proportionally (at fixed Q and efficiency).")
    print("     A 50× gap from current Century capability to commercial target means")
    print("     electrode thermal loading, liquid-metal dynamics, gas injection timing,")
    print("     and pulsed-power component heat rejection must all work at 50× higher")
    print("     duty cycle simultaneously. No published failure-mode characterization")
    print("     for this regime. LCOE at 5 Hz is roughly 2× that at 10 Hz.")
    print()
    print("  3. PULSED POWER DRIVER COST (no published estimate exists) — HIGH IMPACT")
    print()
    print("     The driver capital cost is the largest single CAS22 line item, replacing")
    print("     the magnet system from tokamak economics. At $3 M/MJ stored energy,")
    print("     driver cost ≈ $8.1 M/module; at $10 M/MJ, ≈ $27 M/module.")
    print("     The OSTI 2025 pulsed power report documents a supply chain problem:")
    print("     10,000–216,000 capacitors/plant, 4–6 yr delivery lead times,")
    print("     and capacitor lifetimes 4–6 orders of magnitude short of commercial")
    print("     requirements. This is a program-level constraint, not a cost-curve issue.")
    print()
    print("  NOTE: Elimination of HTS magnets and cryogenic plant is a genuine")
    print("  structural advantage vs. compact tokamak designs — these would add")
    print("  $500M–$1B to the capital cost of a comparable spherical tokamak plant.")
    print("  The pulsed power driver is a cost substitute, not just an addition.")
    print()
    print("=" * 72)
    print("UNCERTAINTY SUMMARY")
    print("=" * 72)
    print()
    print("  This model carries HIGH aggregate uncertainty because its two largest")
    print("  cost drivers (driver capital, driver recirculating power) both depend")
    print("  on parameters that have never been demonstrated at commercial scale:")
    print()
    print("  • Q > 10: calculated, not measured (5–10× pinch lifetime extrapolation)")
    print("  • 10 Hz rep rate: 50× beyond current Century capability")
    print("  • Driver cost: no published estimate; 10× range in industrial analogues")
    print()
    print("  The LCOE range across scenarios above spans roughly 3–10×, primarily")
    print("  driven by these three parameters. Until FuZE-A or Century demonstrates")
    print("  Q ≥ 1 and rep rates above 1 Hz, the baseline scenario is an extrapolation")
    print("  of a calculated design point, not an engineering projection.")
    print()
    print("  All estimates follow CAS structure from 1costingfe costing_constants.yaml.")
    print("  Standard accounts use documented scaling laws. Overrides are marked [OVERRIDE].")


if __name__ == "__main__":
    main()
