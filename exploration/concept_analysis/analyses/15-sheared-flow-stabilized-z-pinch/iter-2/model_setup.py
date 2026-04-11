"""
Sheared-Flow Stabilized Z-Pinch (SFS Z-Pinch) First-Pass LCOE Model
=====================================================================
1cFE Concept Analysis — Zap Energy / SFS Z-Pinch D-T Concept

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

This model computes LCOE for the Sheared-Flow Stabilized Z-Pinch (SFS Z-Pinch)
as developed by Zap Energy (Seattle, WA). The concept uses pulsed axial current
(~1.2–1.5 MA, 200 µs) to create a Z-pinch plasma stabilized by radially sheared
axial flow rather than external magnetic coils. The primary capital cost driver
is the pulsed-power driver (capacitors, switches, pulse-forming networks), which
substitutes for the magnet system cost that dominates tokamak economics.

Key concept features:
- No external magnets (eliminates dominant tokamak capital cost)
- LiPb cascade serves simultaneously as first wall, blanket, and electrode
- Pulsed operation at 10 Hz with 200 µs plasma lifetime (design target)
- Modular 50 MWe/module architecture
- Steam Rankine power conversion

Cost accounting follows the standardized CAS (Code of Accounts System) structure
used in 1costingfe / pyFECONS, with concept-specific overrides for the pulsed-power
driver (C220107), electrode system (C220108), and LiPb blanket/wall (C220101).

Key references:
- Thompson, Levitt, Nelson, Shumlak — "Engineering Paradigms for SFS Z-Pinch
  Fusion Energy" (Fusion Science & Technology, 2023) — the "Engineering Paradigms"
  paper. Primary source for all plasma parameters, blanket design, driver efficiency.
  [engineering-paradigms-paper-summary.md]
- Zap Energy Century Demo System (FST 2025 / press release) — commercial architecture,
  50 MWe module concept, Century milestones. [century-demo-system.md]
- Zap Energy FuZE-3 gigapascal results (Nov 2025) — latest plasma performance.
  [fuze-3-gigapascal-results-2025.md]
- Zap Energy "How It Works" website — 10 Hz target, LiPb wall, no-magnet claim.
  [zap-energy-website-how-it-works.md]
- Phase 1a Dossier SFS Z-Pinch — taxonomy classification, TBR, rep rate.
  [dossier.md]
- 1costingfe costing_constants.yaml — CAS scaling laws and unit costs used throughout.
  [https://github.com/1cFE/1costingfe]

WARNING: This analysis carries HIGH UNCERTAINTY across almost all parameters.
Q > 10 is a calculated projection (not demonstrated). Rep rate of 10 Hz is
not demonstrated (Century at 0.2 Hz). Capital costs have no public estimate.
Results represent a plausible design corridor, not a prediction.
"""

import math
from dataclasses import dataclass, field
from typing import Optional


# === Reference power levels for scaling laws (from 1costingfe) ===
P_TH_REF = 2500.0   # Reference thermal power [MWt] — 1costingfe calibration point
P_ET_REF = 1100.0   # Reference gross electric power [MWe] — 1costingfe calibration point


@dataclass
class SFSZPinchPlantParams:
    """
    Parameterized SFS Z-Pinch power plant model (single module).
    All parameters annotated with source, reference, and uncertainty level.

    Architecture: pulsed (200 µs pulse, 10 Hz), single Z-pinch core per module,
    LiPb flowing first wall / blanket / electrode, steam Rankine cycle.
    Plant = n_mod modules operating in parallel, staggered to smooth grid output.
    """

    # =========================================================================
    # PLASMA / FUSION PHYSICS
    # =========================================================================

    fusion_energy_per_pulse_MJ: float = 19.0
    """Fusion energy yield per pulse [MJ].
    Source: "Nominal 19 MJ fusion energy per pulse" from Engineering Paradigms
    paper Table I design point.
    Ref: engineering-paradigms-paper-summary.md §Design Parameters / Table I.
    MODERATE UNCERTAINTY — design target; not experimentally achieved."""

    fusion_Q: float = 10.0
    """Fusion gain Q = P_fusion / P_input (dimensionless).
    Source: "At plant-relevant currents, Q > 10" — Engineering Paradigms paper.
    Ref: engineering-paradigms-paper-summary.md §Physics Assumptions.
    HIGH UNCERTAINTY — calculated projection; never demonstrated at any scale.
    FuZE demonstrated thermonuclear neutrons; Q < 1 on current devices.
    Commercial Q requires 200 µs lifetime — 5–10× extrapolation from FuZE (20–40 µs)."""

    rep_rate_Hz: float = 10.0
    """Pulse repetition rate [Hz].
    Source: "10 Hz" commercial target.
    Ref: zap-energy-website-how-it-works.md §Commercial Design; dossier.md §Repetition Rate.
    HIGH UNCERTAINTY — Century operates at 0.2 Hz (50× below commercial target).
    50× scaling gap is uncharacterized in public literature."""

    blanket_energy_multiplication: float = 1.10
    """Blanket energy multiplication factor M (14 MeV neutron capture + Li exothermic rxn).
    Source: Standard D-T assumption; LiPb TBR ~ 1.1 from Monte Carlo neutronics.
    Ref: engineering-paradigms-paper-summary.md §Blanket Design; dossier.md §Tritium Breeding.
    Note: TBR = 1.1 is marginal — a 10% reduction could push TBR below 1.0."""

    thermal_efficiency: float = 0.33
    """Thermal-to-electric conversion efficiency (steam Rankine cycle).
    Source: Steam Rankine is confirmed as the power conversion choice in the
    Engineering Paradigms paper. LiPb solidification point (~235°C) sets a floor
    on blanket outlet temperature, constraining maximum steam cycle efficiency.
    Ref: engineering-paradigms-paper-summary.md §Heat Extraction; dossier.md §Energy Capture.
    # ASSUMED: Exact thermal efficiency not published. Using 33% for steam Rankine
    # at moderate temperature (~400–500°C LiPb outlet). 35–37% is needed to match
    # the "50 MWe module" claim from Century materials (see net electric notes).
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # PULSED POWER DRIVER
    # =========================================================================

    driver_wall_to_plasma_efficiency: float = 0.70
    """Fraction of AC wall power delivered to plasma (wall-plug to plasma).
    Source: "Wall-to-plasma efficiency ~70%: AC-DC rectification ~90% × modulator ~80%"
    Ref: engineering-paradigms-paper-summary.md §Driver Efficiency.
    MODERATE UNCERTAINTY — efficiency breakdown documented; demonstrated at subscale."""

    driver_cost_per_module_M_USD: float = 150.0
    """Capital cost of pulsed power driver per module [$M]. Maps to C220107.
    Source: No published estimate for commercial SFS Z-pinch driver.
    Basis: Engineering Paradigms paper states pulsed power "well within technical
    state of the art" for ~1 MA delivery. Industrial pulsed power systems cost
    approximately $1–10/J of stored energy depending on rep rate and pulse requirements.
    Driver stored energy per pulse ~ fusion_energy/Q/efficiency = 19/(10×0.70) ~ 2.7 MJ.
    At $5–50/J, driver cost = $13.5M–$135M for energy storage alone.
    Including switches, PFN, control, installation: scaling to $150M per module.
    Ref: general pulsed power literature analogy; no Zap-specific data.
    # ASSUMED: $150M/module is a central estimate. Range: $50M (optimistic, mass manufacturing)
    # to $500M (high complexity, specialty procurement).
    HIGH UNCERTAINTY."""

    driver_cost_per_joule_USD: float = 50.0
    """Cross-check: pulsed power system cost per joule stored energy [$/J].
    Source: Industrial pulsed power systems ~$1–$10/J for conventional applications;
    NIF laser pulsed power is in the $100+/J range (fusion-grade specialty).
    Ref: General pulsed power literature (analogue — no Zap-specific data).
    # ASSUMED: Used for cross-check only, not primary calculation.
    HIGH UNCERTAINTY."""

    # =========================================================================
    # ELECTRODE SYSTEM (concept-specific consumable)
    # =========================================================================

    electrode_replacement_interval_years: float = 2.0
    """Electrode replacement interval [years at commercial duty].
    Source: No published erosion rate data for SFS Z-pinch electrodes under nuclear duty.
    Engineering Paradigms paper references industrial arc furnace cathode analogy.
    # ASSUMED: 2 years is a plausible but entirely unvalidated estimate.
    Electrode erosion at 10 Hz × 1 MA is uncharacterized; nuclear environment
    (14 MeV neutrons, activation) makes industrial analogues unreliable.
    HIGH UNCERTAINTY."""

    electrode_cost_per_set_M_USD: float = 5.0
    """Cost per electrode set replacement [$M].
    Source: No published data. Tungsten or refractory metal electrodes.
    Global tungsten production ~90,000 t/yr; specialty machining for nuclear use.
    # ASSUMED: $5M per set is a rough estimate for precision-machined refractory
    # components at plant scale. Could be $1M–$20M depending on material and geometry.
    HIGH UNCERTAINTY."""

    # =========================================================================
    # CHAMBER GEOMETRY (for blanket/shield volume scaling)
    # =========================================================================

    chamber_inner_radius_m: float = 1.5
    """Inner radius of fusion chamber [m] (pinch core to LiPb inner surface).
    Source: "Core diameter ~3 m" from Engineering Paradigms paper implies ~1.5 m radius.
    Ref: engineering-paradigms-paper-summary.md §Design Parameters.
    MODERATE UNCERTAINTY — design point only."""

    blanket_thickness_m: float = 3.0
    """LiPb blanket thickness [m] (first wall + breeder + shield).
    Source: "3 m LiPb blanket" gives TBR ~ 1.1 per Monte Carlo neutronics.
    Ref: engineering-paradigms-paper-summary.md §Blanket Design; dossier.md §Tritium Breeding.
    Note: LiPb serves simultaneously as first wall, neutron moderator/multiplier,
    tritium breeder, biological shield, and outer electrode — a 'quadruple-duty' design.
    MODERATE UNCERTAINTY — thickness well-sourced; flow dynamics unvalidated."""

    shield_thickness_m: float = 0.3
    """Additional structural shield thickness beyond LiPb [m].
    Source: LiPb provides primary shielding; modest additional structural shielding assumed.
    # ASSUMED: 0.3 m structural/activated-material shield. Thinner than tokamak because
    # LiPb bulk provides most biological shielding function.
    MODERATE UNCERTAINTY."""

    structure_thickness_m: float = 0.3
    """Primary structural shell thickness [m].
    # ASSUMED: Analogy to IFE chamber structure.
    MODERATE UNCERTAINTY."""

    vessel_thickness_m: float = 0.1
    """Vacuum vessel wall thickness [m].
    # ASSUMED: Analogy to IFE vessel; no external magnets eliminates need for
    # large port structures (NBI, ECRH), simplifying vessel geometry.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # PLANT CONFIGURATION
    # =========================================================================

    n_mod: int = 4
    """Number of fusion modules per plant.
    Source: Century described as "close to eventual size of single module producing
    50 MWe." Multi-module plant architecture explicit in Zap Energy roadmap.
    Ref: century-demo-system.md §Commercial Scale.
    # ASSUMED: 4 modules × ~50 MWe/module ≈ 200 MWe net plant. This is a plausible
    # commercial plant scale consistent with the modular architecture.
    MODERATE UNCERTAINTY."""

    plant_availability: float = 0.75
    """Plant capacity factor / availability.
    Source: No published target. No operational Z-pinch plant data.
    # ASSUMED: 75% is pessimistic relative to mature nuclear (~85–90%) to account
    # for: electrode replacement downtime, pulsed power component maintenance,
    # LiPb system maintenance, rep rate scaling uncertainty.
    HIGH UNCERTAINTY."""

    plant_lifetime_years: float = 30.0
    """Plant economic lifetime [years].
    # ASSUMED: 30 years (shorter than standard nuclear 40–60 yr due to pulsed
    # power component lifetime uncertainty and early commercial technology).
    HIGH UNCERTAINTY."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds 10% contingency; NOAK is the mature commercial baseline.
    Ref: 1costingfe CAS29 convention."""

    # =========================================================================
    # CAS22 BLANKET/FIRST WALL UNIT COSTS
    # =========================================================================

    blanket_unit_cost: float = 0.60
    """LiPb blanket/first wall unit cost [M$/m³].
    Source: 1costingfe costing_constants.yaml, blanket_unit_cost_dt = 0.60 M$/m³.
    Ref: 1costingfe defaults (D-T full breeding blanket).
    Note: Applied to LiPb flowing first wall + blanket volume. The quadruple-duty
    nature of the LiPb system (first wall + blanket + shield + electrode) may justify
    a cost premium; $0.60/m³ is the D-T tokamak reference.
    DEFAULT: Using 1costingfe D-T default."""

    # =========================================================================
    # AUXILIARY POWER LOADS (recirculating)
    # =========================================================================

    p_trit_MW: float = 8.0
    """Tritium processing plant power [MWe] per module.
    Source: 1costingfe ife_zpinch.yaml default ~10 MW scaled to module size.
    # ASSUMED: Scaled from 1costingfe reference (~10 MW at 1 GWe) to ~50 MWe module.
    p_trit ~ 10 × (50/1000)^0.5 ≈ 2.2 MW per module. Using 8 MW for full plant.
    DEFAULT from 1costingfe analogy."""

    p_house_MW: float = 3.0
    """Housekeeping / station service power [MWe] per module.
    Source: 1costingfe ife_zpinch.yaml default.
    # ASSUMED: Small plant equivalent. DEFAULT from 1costingfe analogy."""

    p_lipb_pump_MW: float = 2.0
    """LiPb circulation pump power [MWe] per module.
    Source: No published estimate. Gravity-cascade design minimizes pumping.
    # ASSUMED: 2 MW per module for LiPb circulation in gravity-assist system.
    Derivable from flow velocity and hydraulic resistance but no design data published.
    HIGH UNCERTAINTY."""

    # =========================================================================
    # CONSUMABLES (per-shot)
    # =========================================================================

    dt_fuel_cost_per_shot_USD: float = 0.01
    """D-T fuel cost per shot [USD].
    Source: D-T fuel mass per shot is ~µg scale. Deuterium is cheap (~$1/g).
    Tritium is self-bred; startup inventory dominates, not ongoing cost.
    Ref: Standard fusion fuel cost estimates.
    Note: This is essentially zero compared to other consumables."""

    electrode_erosion_cost_per_shot_USD: float = 0.005
    """Electrode erosion consumable cost per shot [USD].
    Source: No published erosion rate. Derived from:
    electrode_cost_per_set_M_USD / (electrode_replacement_interval_years ×
    rep_rate_Hz × 3600 × 8760 × availability).
    # ASSUMED: Cross-check value — primary electrode cost tracked in CAS72.
    HIGH UNCERTAINTY."""

    # =========================================================================
    # FINANCIAL PARAMETERS
    # =========================================================================

    interest_rate: float = 0.08
    """Real discount rate (weighted average cost of capital).
    Ref: 1costingfe default; standard nuclear project assumption."""

    inflation_rate: float = 0.02
    """Inflation rate for levelized cost calculations.
    Ref: 1costingfe default."""

    construction_time_years: float = 5.0
    """Construction period [years].
    # ASSUMED: Modular design may enable faster construction than large tokamak
    (6–8 yr). 5 years assumed for modular factory-built modules.
    MODERATE UNCERTAINTY."""

    om_cost_per_MW_yr: float = 80.0
    """Annual O&M cost per MW net capacity [$/kW/yr = $1000/MW/yr].
    Source: No Z-pinch precedent. 1costingfe D-T reference: ~52 M$/yr at 1 GWe
    → ~52,000 $/MW/yr. Scaling to small modular: apply 0.5^0.5 ratio for smaller
    plant, plus premium for novel technology with unproven maintenance procedures.
    # ASSUMED: $80/kW/yr is 50% above mature nuclear estimates to reflect:
    (a) electrode replacement overhead, (b) pulsed power component maintenance,
    (c) learning curve inefficiencies for first commercial plants.
    HIGH UNCERTAINTY."""

    core_lifetime_FPY: float = 5.0
    """LiPb first wall / blanket circuit lifetime in full-power-years before replacement.
    Source: 1costingfe core_lifetime_dt = 5 FPY for D-T at 14.1 MeV neutron fluence.
    Ref: 1costingfe costing_constants.yaml, core_lifetime_dt.
    Note: LiPb is flowing (continuously replenished), so 'blanket lifetime' means
    LiPb circuit structural components (pipes, heat exchangers, pumps), not the
    liquid metal itself. Structural component lifetime under neutron activation
    is the binding constraint.
    DEFAULT: Using 1costingfe D-T default."""

    # =========================================================================
    # SPECIAL MATERIALS (CAS27)
    # =========================================================================

    lipb_inventory_tonnes: float = 800.0
    """LiPb inventory in circulation per module [tonnes].
    Source: "3 m thick blanket around ~25 m³ core implies several hundred tonnes
    of LiPb per module" from analysis.md §Section 4.
    Ref: analysis.md §Section 4.
    # ASSUMED: 800 tonnes per module for 3 m blanket at ~10,500 kg/m³ LiPb density.
    MODERATE UNCERTAINTY."""

    lipb_cost_per_tonne_USD: float = 3000.0
    """Cost of LiPb eutectic per tonne [USD/tonne].
    Source: 1costingfe special_materials_dt notes: "PbLi fill (~4,500 t @ $3/kg)".
    Ref: 1costingfe costing_constants.yaml, CAS27 comment.
    Note: Lead commodity price; Li price modest for natural Li (no enrichment needed
    at 3 m blanket thickness per Engineering Paradigms paper).
    DEFAULT: Using 1costingfe reference price."""

    # =========================================================================

    def _compute_power(self) -> dict:
        """Layer 1: Power balance — driver → plasma → fusion → energy recovery."""
        r = {}

        # --- Fusion power ---
        # Time-averaged fusion power = energy per pulse × rep rate
        p_fus = self.fusion_energy_per_pulse_MJ * self.rep_rate_Hz  # MW
        r["p_fus"] = p_fus

        # D-T neutron/alpha split: 14.06 MeV neutrons (80%), 3.52 MeV alphas (20%)
        f_neutron = 0.80
        f_alpha = 0.20
        r["p_neutron"] = p_fus * f_neutron
        r["p_alpha"] = p_fus * f_alpha

        # --- Driver power (recirculating) ---
        # Plasma input power = fusion power / Q
        # Driver (wall-plug) power = plasma input power / wall-to-plasma efficiency
        p_plasma_input = p_fus / self.fusion_Q  # MW (time-averaged)
        r["p_plasma_input"] = p_plasma_input
        p_driver_wallplug = p_plasma_input / self.driver_wall_to_plasma_efficiency  # MWe
        r["p_driver_wallplug"] = p_driver_wallplug

        # Driver electrical energy per pulse (for sizing / cross-check)
        # p_driver_wallplug = energy_per_pulse × rep_rate
        driver_energy_per_pulse_MJ = p_driver_wallplug / self.rep_rate_Hz
        r["driver_energy_per_pulse_MJ"] = driver_energy_per_pulse_MJ

        # Engineering Q = fusion power / wall-plug driver power
        r["Q_eng"] = p_fus / p_driver_wallplug if p_driver_wallplug > 0 else 0.0

        # --- Thermal power ---
        # Neutrons are captured in LiPb blanket (with multiplication factor M)
        # Alpha power thermalizes in plasma → conducted to LiPb wall
        # Driver input power: fraction = (1 - η_wall_to_plasma) thermalizes in driver
        #   hardware; fraction = η_wall_to_plasma is deposited in plasma → LiPb.
        # Conservative: only account for plasma-deposited driver power in blanket.
        p_th = (self.blanket_energy_multiplication * r["p_neutron"]
                + r["p_alpha"])  # MWt
        r["p_th"] = p_th

        # --- Gross electric ---
        p_et = p_th * self.thermal_efficiency  # MWe
        r["p_et"] = p_et

        # --- Auxiliary loads (non-driver recirculating) ---
        p_aux = self.p_trit_MW + self.p_house_MW + self.p_lipb_pump_MW  # MWe
        r["p_aux"] = p_aux

        # --- Net electric (per module) ---
        p_net = p_et - p_driver_wallplug - p_aux
        r["p_net"] = p_net

        # --- Recirculating fraction ---
        r["recirc_fraction"] = (p_driver_wallplug + p_aux) / p_et if p_et > 0 else float("inf")

        # --- Annual shots ---
        r["shots_per_year"] = self.rep_rate_Hz * 3600.0 * 8760.0 * self.plant_availability

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Chamber geometry — cylindrical approximation for Z-pinch.

        The SFS Z-pinch has a roughly cylindrical chamber geometry (unlike spherical
        IFE chambers). Pinch length ~0.5 m but blanket wraps around the full assembly.
        We approximate the blanket/shield geometry as concentric cylindrical shells
        around an effective spherical equivalent volume for cost-scaling purposes.

        The Engineering Paradigms paper gives core volume ~25 m³ and diameter ~3 m,
        implying a roughly spherical or short-cylinder geometry for the full
        blanket assembly. We use spherical shells as the geometric approximation
        consistent with the MagLIF exemplar and 1costingfe volume-based scaling.
        """
        r = {}
        ri = self.chamber_inner_radius_m

        def sphere_shell_vol(r_in: float, thickness: float) -> float:
            r_out = r_in + thickness
            return (4.0 / 3.0) * math.pi * (r_out**3 - r_in**3)

        # LiPb blanket volume (first wall + breeder + primary shield)
        r["blanket_vol_m3"] = sphere_shell_vol(ri, self.blanket_thickness_m)
        r_blanket_out = ri + self.blanket_thickness_m

        # Additional structural shield volume
        r["shield_vol_m3"] = sphere_shell_vol(r_blanket_out, self.shield_thickness_m)
        r_shield_out = r_blanket_out + self.shield_thickness_m

        # Primary structure volume
        r["structure_vol_m3"] = sphere_shell_vol(r_shield_out, self.structure_thickness_m)
        r_structure_out = r_shield_out + self.structure_thickness_m

        # Vacuum vessel volume
        r["vessel_vol_m3"] = sphere_shell_vol(r_structure_out, self.vessel_thickness_m)

        # Outer radius (for building sizing reference)
        r["outer_radius_m"] = r_structure_out + self.vessel_thickness_m

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts.

        Follows 1costingfe cas22.py structure with concept-specific overrides:
        - C220101: LiPb first wall + blanket (volume-based, D-T unit cost)
        - C220103: NO COILS — set to $0 (key differentiator vs. tokamaks)
        - C220104: NO HEATING SYSTEM — set to $0 (no NBI/ECRH; driver provides heating)
        - C220107: OVERRIDE — pulsed power driver replaces standard power-supply scaling
        - C220108: OVERRIDE — electrode system (novel consumable, no factory needed)
        """
        r = {}
        p_th = max(power["p_th"], 1.0)
        p_et = max(power["p_et"], 1.0)
        p_net_mod = max(power["p_net"], 1.0)

        # --- Per-module accounts ---

        # C220101: First Wall + LiPb Blanket (the 'quadruple-duty' LiPb system)
        # Formula: unit_cost × volume × (p_th / P_TH_REF)^0.6
        # Ref: 1costingfe costing_constants.yaml, blanket_unit_cost_dt = 0.60 M$/m³
        r["C220101"] = (self.blanket_unit_cost
                        * geom["blanket_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220102: Shield (structural + biological, excluding LiPb which is in C220101)
        # Formula: 0.74 × volume × (p_th / P_TH_REF)^0.6
        # Ref: 1costingfe costing_constants.yaml, shield_unit_cost = 0.74 M$/m³
        shield_unit_cost = 0.74
        r["C220102"] = (shield_unit_cost
                        * geom["shield_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: Coils — OVERRIDE to $0
        # The SFS Z-pinch has NO external magnets. This is the key structural
        # difference from all tokamak/stellarator/mirror concepts. Eliminates
        # the dominant capital cost item in compact HTS tokamak designs.
        r["C220103"] = 0.0  # OVERRIDE: no coils, no cryogenics

        # C220104: Supplementary Heating — OVERRIDE to $0
        # No NBI, no ECRH, no laser preheat (unlike MagLIF). The pulsed-power
        # driver provides all plasma heating via ohmic/compression. The cost
        # of the driver is captured in C220107.
        r["C220104"] = 0.0  # OVERRIDE: no auxiliary heating system

        # C220105: Primary Structure
        # Formula: 0.15 × volume × (p_et / P_ET_REF)^0.5
        # Ref: 1costingfe costing_constants.yaml, structure_unit_cost = 0.15 M$/m³
        structure_unit_cost = 0.15
        r["C220105"] = (structure_unit_cost
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: Vacuum System (vessel + roughing/turbo pumps)
        # Formula: 0.72 × volume × (p_et / P_ET_REF)^0.6
        # Ref: 1costingfe costing_constants.yaml, vessel_unit_cost = 0.72 M$/m³
        vessel_unit_cost = 0.72
        r["C220106"] = (vessel_unit_cost
                        * geom["vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # C220107: Power Supplies — OVERRIDE with pulsed power driver cost
        # The driver (capacitor bank + pulse-forming networks + solid-state switches +
        # AC-DC rectification + control) IS the power supply system.
        # Standard 1costingfe formula: 80.0 × (p_et/1000)^0.7 ≈ too low for
        # specialty pulsed power at this scale.
        # Override: direct cost estimate per module from pulsed power analogy.
        # Ref: analysis.md §Section 2 (pulsed power driver cost discussion)
        r["C220107"] = self.driver_cost_per_module_M_USD  # OVERRIDE

        # C220108: Electrode System — OVERRIDE (concept-specific, no IFE target factory)
        # Standard C220108 in 1costingfe is "Target Factory" for IFE/MIF concepts.
        # For SFS Z-pinch, there are no discrete targets — the electrode system
        # (inner electrode, outer electrode / LiPb interface) is the per-module
        # capital investment. Electrode replacement is handled in CAS72.
        # Initial electrode installation cost ~ 2× replacement cost.
        # Ref: engineering-paradigms-paper-summary.md §Electrode Engineering
        r["C220108"] = 2.0 * self.electrode_cost_per_set_M_USD  # OVERRIDE: initial install

        # C220109: Direct Energy Converter — not applicable
        r["C220109"] = 0.0

        # C220111: Installation labor
        # Formula: 0.14 × reactor subtotal
        # Ref: 1costingfe costing_constants.yaml, installation_frac = 0.14
        installation_frac = 0.14
        reactor_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109"])
        r["C220111"] = installation_frac * reactor_subtotal

        # C220112: Isotope Separation — $0 (handled in CAS80 / startup inventory)
        r["C220112"] = 0.0

        # Per-module subtotal
        r["CAS22_per_module"] = reactor_subtotal + r["C220111"] + r["C220112"]

        # --- Plant-wide accounts (scale with total plant power) ---
        p_net_total = p_net_mod * self.n_mod
        p_th_total = p_th * self.n_mod

        # C220200: Main & Secondary Coolant (LiPb primary + steam secondary)
        # Formula: 166.0 × (p_net_total/1000) for primary; 40.6 × (p_th_total/3500)^0.55 for secondary
        # Ref: 1costingfe cas22.py C220200 scaling
        C220201 = 166.0 * (p_net_total / 1000.0)
        C220202 = 40.6 * (p_th_total / 3500.0) ** 0.55
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling + Cryoplant
        # Note: No cryoplant needed (no superconducting magnets) — set cryoplant to ~0
        # Ref: 1costingfe cas22.py C220300 scaling
        C220301 = 1.1e-3 * p_th_total   # auxiliary cooling
        C220302 = 0.0                   # OVERRIDE: no cryoplant (no SC magnets)
        r["C220300"] = C220301 + C220302

        # C220400: Radioactive Waste Management
        # Ref: 1costingfe scaling: 1.96 × (p_th_total/1000)
        r["C220400"] = 1.96 * (p_th_total / 1000.0)

        # C220500: Fuel Handling & Storage (tritium processing for D-T)
        # Ref: 1costingfe, fuel_handling_dt_base = 120 M$ at 1 GWe
        fuel_handling_base = 120.0
        r["C220500"] = fuel_handling_base * (max(p_net_total, 1.0) / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        # Ref: 1costingfe scaling: 11.5 × (p_net/1000)^0.8
        r["C220600"] = 11.5 * (max(p_net_total, 1.0) / 1000.0) ** 0.8

        # C220700: Instrumentation & Control
        # Ref: 1costingfe scaling: 85.0 × (p_th_total/3500)^0.65
        r["C220700"] = 85.0 * (p_th_total / 3500.0) ** 0.65

        # Plant-wide subtotal
        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        # Total CAS22
        r["CAS22"] = r["CAS22_per_module"] * self.n_mod + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, geom: dict, cas22: dict) -> dict:
        """Layer 4: CAS10-60 capital costs."""
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
        land_cost = 0.25 * p_net_total * 10_000.0 / 1e6  # 0.25 acres/MWe × $10k/acre
        # D-T licensing: $5M FOAK, $2.5M NOAK
        # Ref: 1costingfe costing_constants.yaml, licensing_cost_dt = 5.0 M$
        licensing_cost = 5.0 if not self.noak else 2.5
        r["CAS10"] = (site_permits + plant_studies + plant_permits + plant_reports
                      + other_precon + land_cost + licensing_cost)

        # === CAS21: Buildings ===
        # Cost per kW of gross electric, from 1costingfe building_costs_per_kw.
        # Note: No cryogenics building needed (no SC magnets). Pulsed power
        # driver needs substantial power supply/storage building.
        # Ref: 1costingfe costing_constants.yaml, building_costs_per_kw
        building_cost_per_kW = {
            "site_improvements":       268.0,
            "fusion_heat_island":      126.0,  # chamber + blanket building
            "turbine_building":         54.0,
            "heat_exchanger":           12.0,
            "power_supply_storage":     35.0,  # pulsed power driver bays
            "hot_cell":                 93.4,  # LiPb processing, activated components
            "reactor_services":         25.0,
            "service_water":            11.0,
            "fuel_storage":              9.1,  # tritium inventory
            "control_room":             17.0,
            "onsite_ac":                21.0,
            "administration":           10.0,
            "site_services":             4.0,
            "cryogenics":                0.0,  # OVERRIDE: no cryogenics
            "security":                  8.0,
            "ventilation_stack":         9.2,
            "assembly_hall":            20.0,
        }
        total_building_per_kW = sum(building_cost_per_kW.values())
        p_et_total = p_et * self.n_mod
        r["CAS21"] = total_building_per_kW * p_et_total / 1000.0  # M$
        r["CAS21_detail"] = {k: v * p_et_total / 1000.0 for k, v in building_cost_per_kW.items()}

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment ===
        # Ref: 1costingfe, turbine_per_mw = 0.19764 M$/MW
        turbine_per_mw = 0.19764
        r["CAS23"] = p_et_total * turbine_per_mw

        # === CAS24: Electric Plant Equipment ===
        # Ref: 1costingfe, electric_per_mw = 0.08418 M$/MW
        electric_per_mw = 0.08418
        r["CAS24"] = p_et_total * electric_per_mw

        # === CAS25: Miscellaneous Plant Equipment ===
        # Ref: 1costingfe, misc_per_mw = 0.05124 M$/MW
        misc_per_mw = 0.05124
        r["CAS25"] = p_et_total * misc_per_mw

        # === CAS26: Heat Rejection ===
        # Ref: 1costingfe, heat_rej_per_mw = 0.03416 M$/MW
        heat_rej_per_mw = 0.03416
        r["CAS26"] = p_et_total * heat_rej_per_mw

        # === CAS27: Special Materials (LiPb initial inventory) ===
        # LiPb inventory per module × n_mod × unit cost
        # Ref: 1costingfe special_materials_dt = 15 M$ at 1 GWe (PbLi fill @$3/kg)
        # Cross-check: n_mod × lipb_inventory_tonnes × lipb_cost_per_tonne_USD / 1e6
        lipb_cost = (self.n_mod * self.lipb_inventory_tonnes
                     * self.lipb_cost_per_tonne_USD / 1e6)
        # Include enriched Li-6 startup if needed (Engineering Paradigms paper says
        # natural Li sufficient at 3 m blanket — no enrichment assumed)
        tritium_startup = 40.0 * (p_net_total / 1000.0)  # M$ — 1costingfe startup_fuel_dt
        r["CAS27"] = lipb_cost + tritium_startup

        # === CAS28: Digital Twin ===
        # Ref: 1costingfe, digital_twin = 5.0 M$
        r["CAS28"] = 5.0

        # === CAS29: Contingency ===
        # Ref: 1costingfe, contingency_rate_foak = 0.10, contingency_rate_noak = 0.0
        cas20_subtotal = sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                             "CAS25", "CAS26", "CAS27", "CAS28"])
        contingency_rate = 0.0 if self.noak else 0.10
        r["CAS29"] = contingency_rate * cas20_subtotal

        # === CAS20: Total Direct Costs ===
        r["CAS20"] = cas20_subtotal + r["CAS29"]

        # === CAS30: Indirect Costs ===
        # 20% of CAS20, scaled by relative construction time
        # Ref: 1costingfe, indirect_fraction = 0.20, reference_construction_time = 6 yr
        ref_construction_time = 6.0
        indirect_fraction = 0.20
        r["CAS30"] = indirect_fraction * r["CAS20"] * (self.construction_time_years / ref_construction_time)

        # === CAS40: Owner's Costs ===
        # Ref: 1costingfe, owner_cost_dt = 39 M$ at 1 GWe, scaling (P_net/1GWe)^0.5
        owner_cost_dt_ref = 39.0  # M$ at 1 GWe
        r["CAS40"] = owner_cost_dt_ref * (p_net_total / 1000.0) ** 0.5

        # === CAS50: Supplementary Costs ===
        # Ref: 1costingfe CAS50 sub-account conventions
        spare_parts_frac = 0.03  # D-T: 1costingfe spare_parts_frac_dt
        spare_parts = spare_parts_frac * sum(r[k] for k in ["CAS23", "CAS24", "CAS25",
                                                              "CAS26", "CAS27", "CAS28"])
        shipping = 0.015 * r["CAS20"]  # 1costingfe shipping_frac
        taxes = 0.01 * r["CAS20"]      # 1costingfe tax_frac
        insurance = 0.015 * (r["CAS20"] + r["CAS30"])  # 1costingfe construction_insurance_frac
        # Decommissioning provision (D-T): 127 M$ at 1 GWe
        decom = 127.0 * (p_net_total / 1000.0)
        r["CAS50"] = spare_parts + shipping + taxes + insurance + decom

        # === Overnight Capital ===
        overnight = r["CAS10"] + r["CAS20"] + r["CAS30"] + r["CAS40"] + r["CAS50"]
        r["overnight_capital"] = overnight

        # === CAS60: Interest During Construction (IDC) ===
        i = self.interest_rate
        T = self.construction_time_years
        if i > 0 and T > 0:
            f_idc = ((1.0 + i) ** T - 1.0) / (i * T) - 1.0
        else:
            f_idc = 0.0
        r["CAS60"] = f_idc * overnight
        r["f_IDC"] = f_idc

        # === Total Capital ===
        r["total_capital"] = overnight + r["CAS60"]

        # Specific capital cost
        if power["p_net"] > 0:
            r["specific_capital_USD_per_kWe"] = (r["total_capital"] * 1e6
                                                  / (power["p_net"] * self.n_mod * 1e3))
        else:
            r["specific_capital_USD_per_kWe"] = float("inf")

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70-90 annualized costs and LCOE."""
        r = {}
        p_net = power["p_net"]
        p_net_total = p_net * self.n_mod

        # Capital Recovery Factor
        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1.0 + i) ** n / ((1.0 + i) ** n - 1.0)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]  # M$/yr

        # === CAS71: Annual O&M (levelized with inflation) ===
        # Ref: 1costingfe CAS70 convention; om_cost_dt = 52 M$/yr at 1 GWe
        # Using per-kW scaling with concept-specific premium
        annual_om_base = (self.om_cost_per_MW_yr / 1000.0) * p_net_total  # M$/yr
        g = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1.0 + g) ** Tc
        if abs(i - g) > 1e-10:
            pv_growing_annuity = A1 * (1.0 - ((1.0 + g) / (1.0 + i)) ** n) / (i - g)
        else:
            pv_growing_annuity = A1 * n / (1.0 + i)
        r["CAS71"] = crf * pv_growing_annuity  # M$/yr

        # === CAS72: Scheduled Replacement ===
        # Two replaceable components:
        # (a) LiPb circuit structural components (blanket replacement, core_lifetime_FPY)
        # (b) Electrode sets (electrode_replacement_interval_years)

        # (a) Blanket/LiPb circuit replacement
        eff_years_per_blanket_replace = (self.core_lifetime_FPY / self.plant_availability)
        n_blanket_replacements = max(
            0, int(math.ceil(self.plant_lifetime_years / eff_years_per_blanket_replace)) - 1)
        blanket_replacement_cost = cas22["C220101"]  # per module; scale by n_mod
        pv_blanket = 0.0
        for k in range(1, n_blanket_replacements + 1):
            yr = k * eff_years_per_blanket_replace
            if yr < self.plant_lifetime_years:
                pv_blanket += (blanket_replacement_cost * self.n_mod) / (1.0 + i) ** yr

        # (b) Electrode replacement
        n_electrode_replacements = max(
            0, int(math.ceil(self.plant_lifetime_years / self.electrode_replacement_interval_years)) - 1)
        electrode_replacement_cost = self.electrode_cost_per_set_M_USD * self.n_mod
        pv_electrode = 0.0
        for k in range(1, n_electrode_replacements + 1):
            yr = k * self.electrode_replacement_interval_years
            if yr < self.plant_lifetime_years:
                pv_electrode += electrode_replacement_cost / (1.0 + i) ** yr

        r["CAS72_blanket"] = crf * pv_blanket
        r["CAS72_electrode"] = crf * pv_electrode
        r["CAS72"] = r["CAS72_blanket"] + r["CAS72_electrode"]
        r["n_blanket_replacements"] = n_blanket_replacements
        r["n_electrode_replacements"] = n_electrode_replacements

        r["CAS70"] = r["CAS71"] + r["CAS72"]  # M$/yr

        # === CAS80: Fuel & Consumables ===
        shots_per_year = power["shots_per_year"]

        # D-T fuel (negligible — tritium is self-bred; deuterium is cheap)
        annual_fuel_cost = shots_per_year * self.dt_fuel_cost_per_shot_USD / 1e6  # M$/yr

        # Gas injection (D-T prefill gas for each pulse)
        # # ASSUMED: ~1 mg D-T per shot at ~50% T × $30,000/g T → ~$1.50/shot T cost
        # But T is self-bred — ongoing T purchase is negligible. D cost is ~$0/shot.
        # Total per-shot fuel cost is dt_fuel_cost_per_shot_USD above.

        r["CAS80"] = annual_fuel_cost
        r["CAS80_fuel"] = annual_fuel_cost

        # === LCOE ===
        annual_revenue_req = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_revenue_req

        annual_energy_MWh = 8760.0 * p_net_total * self.plant_availability
        r["annual_energy_MWh"] = annual_energy_MWh

        if annual_energy_MWh > 0:
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
        """Compute LCOE and key derived quantities. Returns dict of all intermediate values."""
        power = self._compute_power()
        geom = self._compute_geometry(power)
        cas22 = self._compute_cas22(power, geom)
        costs = self._compute_costs(power, geom, cas22)
        econ = self._compute_economics(power, costs, cas22)

        results = {
            "power": power,
            "geometry": geom,
            "cas22": cas22,
            "costs": costs,
            "economics": econ,
        }
        results["net_electric_MW"] = power["p_net"]
        results["lcoe_cents_per_kWh"] = econ["lcoe_cents_per_kWh"]
        results["total_capital_M_USD"] = costs["total_capital"]
        return results


# =============================================================================
# OUTPUT / DISPLAY
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
        title += f"\nScenario: {label}"
    print("=" * 72)
    print(title)
    print("=" * 72)

    print(f"\n--- Key Input Parameters ---")
    print(f"  Fusion energy/pulse:        {params.fusion_energy_per_pulse_MJ:.0f} MJ")
    print(f"  Fusion Q (plasma):          {params.fusion_Q:.1f}")
    print(f"  Rep rate:                   {params.rep_rate_Hz:.1f} Hz")
    print(f"  Wall-to-plasma efficiency:  {params.driver_wall_to_plasma_efficiency:.0%}")
    print(f"  Blanket multiplication:     {params.blanket_energy_multiplication:.2f}")
    print(f"  Thermal efficiency:         {params.thermal_efficiency:.0%}")
    print(f"  Plant availability:         {params.plant_availability:.0%}")
    print(f"  Modules:                    {params.n_mod}")
    print(f"  Plant lifetime:             {params.plant_lifetime_years:.0f} yr")
    print(f"  FOAK/NOAK:                  {'NOAK' if params.noak else 'FOAK'}")
    print(f"  Interest rate:              {params.interest_rate:.0%}")
    print(f"  Driver cost/module:         ${params.driver_cost_per_module_M_USD:.0f}M")

    print(f"\n--- Power Balance (per module) ---")
    print(f"  Fusion energy/pulse:        {params.fusion_energy_per_pulse_MJ:.1f} MJ")
    print(f"  Rep rate:                   {params.rep_rate_Hz:.1f} Hz")
    print(f"  Fusion power (avg):         {power['p_fus']:.1f} MWt")
    print(f"    Neutron power:            {power['p_neutron']:.1f} MWt (80%)")
    print(f"    Alpha power:              {power['p_alpha']:.1f} MWt (20%)")
    print(f"  Plasma input power:         {power['p_plasma_input']:.1f} MWt  [P_fus / Q]")
    print(f"  Driver wallplug power:      {power['p_driver_wallplug']:.1f} MWe  [plasma_in / η_driver]")
    print(f"  Driver energy/pulse:        {power['driver_energy_per_pulse_MJ']:.2f} MJ")
    print(f"  Thermal power:              {power['p_th']:.1f} MWt")
    print(f"  Gross electric:             {power['p_et']:.1f} MWe")
    print(f"  Auxiliary loads:            {power['p_aux']:.1f} MWe  (tritium+house+LiPb pumps)")
    print(f"  Net electric (per module):  {power['p_net']:.1f} MWe")
    print(f"  Net electric (plant):       {power['p_net'] * params.n_mod:.1f} MWe")
    print(f"  Engineering Q:              {power['Q_eng']:.2f}  [P_fus / P_driver_wallplug]")
    print(f"  Recirculating fraction:     {power['recirc_fraction']:.1%}  [of gross electric]")

    print(f"\n--- Geometry (spherical approximation per module) ---")
    print(f"  Inner radius:               {params.chamber_inner_radius_m:.1f} m")
    print(f"  LiPb blanket thickness:     {params.blanket_thickness_m:.1f} m  (first wall + breeder + shield)")
    print(f"  Blanket volume:             {geom['blanket_vol_m3']:.0f} m³")
    print(f"  Shield volume:              {geom['shield_vol_m3']:.0f} m³")
    print(f"  Outer radius:               {geom['outer_radius_m']:.1f} m")

    print(f"\n--- CAS22: Reactor Plant Equipment (per module) ---")
    cas22_labels = {
        "C220101": "LiPb First Wall + Blanket",
        "C220102": "Structural Shield",
        "C220103": "Coils [OVERRIDE: $0 — no magnets]",
        "C220104": "Heating [OVERRIDE: $0 — no aux heating]",
        "C220105": "Primary Structure",
        "C220106": "Vacuum System",
        "C220107": "Pulsed Power Driver [OVERRIDE]",
        "C220108": "Electrode System [OVERRIDE]",
        "C220109": "Direct Energy Converter",
        "C220111": "Installation (14%)",
        "C220112": "Isotope Separation",
    }
    for code, label in cas22_labels.items():
        val = cas22[code]
        if val > 0.001 or "OVERRIDE" in label:
            print(f"    {code}  {label:<40s}  ${val:>8.1f}M")
    print(f"    {'─' * 55}")
    print(f"    Per-module subtotal:                             ${cas22['CAS22_per_module']:>8.1f}M × {params.n_mod}")

    print(f"  Plant-wide accounts:")
    pw_labels = {
        "C220200": "LiPb + Steam Coolant Systems",
        "C220300": "Auxiliary Cooling (no cryoplant)",
        "C220400": "Radioactive Waste Management",
        "C220500": "Fuel Handling (D-T tritium)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    for code, lbl in pw_labels.items():
        val = cas22[code]
        print(f"    {code}  {lbl:<40s}  ${val:>8.1f}M")
    print(f"    {'─' * 55}")
    print(f"    Plant-wide subtotal:                             ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                                       ${cas22['CAS22']:>8.1f}M")

    print(f"\n--- Capital Costs (CAS10-60) ---")
    print(f"  CAS10  Pre-construction:              ${costs['CAS10']:>8.1f}M")
    print(f"  CAS21  Buildings:                     ${costs['CAS21']:>8.1f}M")
    print(f"  CAS22  Reactor Plant Equipment:       ${costs['CAS22']:>8.1f}M")
    print(f"  CAS23  Turbine Plant:                 ${costs['CAS23']:>8.1f}M")
    print(f"  CAS24  Electric Plant:                ${costs['CAS24']:>8.1f}M")
    print(f"  CAS25  Misc Plant:                    ${costs['CAS25']:>8.1f}M")
    print(f"  CAS26  Heat Rejection:                ${costs['CAS26']:>8.1f}M")
    print(f"  CAS27  Special Materials (LiPb+T):    ${costs['CAS27']:>8.1f}M")
    print(f"  CAS28  Digital Twin:                  ${costs['CAS28']:>8.1f}M")
    print(f"  CAS29  Contingency:                   ${costs['CAS29']:>8.1f}M")
    print(f"  {'─' * 52}")
    print(f"  CAS20  Direct Costs:                  ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30  Indirect Costs:                ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40  Owner's Costs:                 ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50  Supplementary (decom+spare):   ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 52}")
    print(f"  Overnight Capital:                    ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60  IDC (f={costs['f_IDC']:.3f}):               ${costs['CAS60']:>8.1f}M")
    print(f"  {'═' * 52}")
    print(f"  Total Capital:                        ${costs['total_capital']:>8.1f}M")
    spec = costs["specific_capital_USD_per_kWe"]
    if spec < 1e8:
        print(f"  Specific Capital:                     ${spec:>8.0f} $/kWe")
    else:
        print(f"  Specific Capital:                     N/A (negative net power)")

    print(f"\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90  Capital charge (CRF={econ['CRF']:.4f}): ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71  O&M (levelized):               ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72  Scheduled replacement:         ${econ['CAS72']:>8.1f}M/yr")
    print(f"           Blanket ({econ['n_blanket_replacements']} times): ${econ['CAS72_blanket']:>8.1f}M/yr")
    print(f"           Electrode ({econ['n_electrode_replacements']} times): ${econ['CAS72_electrode']:>8.1f}M/yr")
    print(f"  CAS70  Total O&M:                     ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80  Fuel & consumables:             ${econ['CAS80']:>8.1f}M/yr")

    print(f"\n--- LCOE ---")
    print(f"  Annual energy:              {econ['annual_energy_MWh']:>12,.0f} MWh")
    print(f"  Annual revenue req:         ${econ['annual_revenue_req']:.1f}M/yr")
    print(f"  ╔══════════════════════════════════════════╗")
    lcoe_c = econ["lcoe_cents_per_kWh"]
    lcoe_d = econ["lcoe_USD_per_MWh"]
    if lcoe_c < 1e6:
        print(f"  ║  LCOE = {lcoe_c:>7.2f} ¢/kWh                    ║")
        print(f"  ║       = {lcoe_d:>7.1f} $/MWh                    ║")
    else:
        print(f"  ║  LCOE = N/A (negative net power)           ║")
    print(f"  ╚══════════════════════════════════════════╝")
    if econ.get("capital_fraction") is not None:
        print(f"  Capital (CAS90):            {econ['capital_fraction']:.1%}")
        print(f"  O&M (CAS70):                {econ['om_fraction']:.1%}")
        print(f"  Fuel/consumables (CAS80):   {econ['fuel_fraction']:.1%}")


# =============================================================================
# SENSITIVITY ANALYSIS
# =============================================================================

def sensitivity_sweep(base_params: SFSZPinchPlantParams, param_name: str,
                      values: list, label: str = "") -> list:
    """Sweep a single parameter and return LCOE for each value."""
    results_list = []
    for val in values:
        p = SFSZPinchPlantParams(**{**base_params.__dict__, param_name: val})
        r = p.compute()
        net_mw = r["power"]["p_net"] * p.n_mod
        results_list.append({
            "param_value": float(val),
            "lcoe_cents_kWh": r["lcoe_cents_per_kWh"],
            "net_electric_MW": net_mw,
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
    print("# BASELINE SCENARIO: SFS Z-Pinch Moderate Design Point")
    print("# Q=10, 10 Hz, 4 modules, steam Rankine 33%, availability 75%")
    print("#" * 72)

    baseline = SFSZPinchPlantParams()
    base_results = baseline.compute()
    print_results(baseline, base_results, label="Baseline — moderate design point")

    # =========================================================================
    # SINGLE-PARAMETER SENSITIVITY SWEEPS
    # =========================================================================
    print("\n\n" + "=" * 72)
    print("SENSITIVITY SWEEPS: Impact on LCOE from baseline")
    print("=" * 72)

    base_lcoe = base_results["lcoe_cents_per_kWh"]
    print(f"  Baseline LCOE: {base_lcoe:.2f} ¢/kWh\n")

    sweeps = [
        # (param_name, values, display_label)
        ("fusion_Q",
         [3.0, 5.0, 7.0, 10.0, 15.0, 20.0],
         "Fusion Q (plasma gain)"),

        ("rep_rate_Hz",
         [1.0, 2.0, 5.0, 10.0, 15.0, 20.0],
         "Rep rate [Hz]"),

        ("driver_cost_per_module_M_USD",
         [30.0, 75.0, 150.0, 300.0, 500.0],
         "Driver cost per module [$M]"),

        ("thermal_efficiency",
         [0.28, 0.33, 0.37, 0.40, 0.45],
         "Thermal efficiency"),

        ("plant_availability",
         [0.50, 0.60, 0.75, 0.80, 0.90],
         "Plant availability (capacity factor)"),

        ("n_mod",
         [1, 2, 4, 8, 12],
         "Number of modules (plant size)"),

        ("driver_wall_to_plasma_efficiency",
         [0.50, 0.60, 0.70, 0.80, 0.90],
         "Wall-to-plasma driver efficiency"),
    ]

    for param_name, values, disp_label in sweeps:
        print(f"  {disp_label}:")
        sweep_res = sensitivity_sweep(baseline, param_name, values)
        for entry in sweep_res:
            val = entry["param_value"]
            lcoe = entry["lcoe_cents_kWh"]
            net = entry["net_electric_MW"]
            marker = " <<< baseline" if abs(val - getattr(baseline, param_name)) < 1e-9 else ""
            if net <= 0:
                print(f"    {val:>8.2g}  →  NET POWER NEGATIVE  ({net:.0f} MWe total){marker}")
            else:
                print(f"    {val:>8.2g}  →  {lcoe:7.2f} ¢/kWh  ({net:.0f} MWe total){marker}")
        print()

    # =========================================================================
    # SCENARIO COMPARISON TABLE
    # =========================================================================
    print("\n" + "=" * 72)
    print("SCENARIO COMPARISON TABLE")
    print("=" * 72)

    scenarios = {
        "Conservative (Q=7, 5 Hz)": SFSZPinchPlantParams(
            fusion_Q=7.0,
            rep_rate_Hz=5.0,
            driver_cost_per_module_M_USD=250.0,
            thermal_efficiency=0.30,
            plant_availability=0.65,
            om_cost_per_MW_yr=100.0,
            n_mod=4,
        ),
        "Moderate (baseline)": SFSZPinchPlantParams(),
        "Optimistic (Q=15, 10 Hz, cheap driver)": SFSZPinchPlantParams(
            fusion_Q=15.0,
            rep_rate_Hz=10.0,
            driver_cost_per_module_M_USD=75.0,
            thermal_efficiency=0.37,
            plant_availability=0.85,
            om_cost_per_MW_yr=60.0,
            electrode_replacement_interval_years=4.0,
            interest_rate=0.06,
            construction_time_years=4.0,
            plant_lifetime_years=40.0,
            n_mod=6,
        ),
        "Q=5 stress test": SFSZPinchPlantParams(
            fusion_Q=5.0,
            rep_rate_Hz=10.0,
            driver_cost_per_module_M_USD=150.0,
        ),
        "Single module (50 MWe)": SFSZPinchPlantParams(n_mod=1),
    }

    hdr = f"{'Scenario':<38} {'Q':>5} {'Hz':>5} {'Driver$':>9} {'Net MWe':>9} {'LCOE':>14}"
    print(hdr)
    print("-" * 82)
    for name, params in scenarios.items():
        r = params.compute()
        net_mw = r["power"]["p_net"] * params.n_mod
        lcoe_c = r["lcoe_cents_per_kWh"]
        driver_str = f"${params.driver_cost_per_module_M_USD:.0f}M"
        if net_mw <= 0:
            lcoe_str = "N/A (neg)"
        elif lcoe_c > 999:
            lcoe_str = ">999 ¢/kWh"
        else:
            lcoe_str = f"{lcoe_c:.2f} ¢/kWh"
        print(f"{name:<38} {params.fusion_Q:>5.1f} {params.rep_rate_Hz:>5.1f} {driver_str:>9}"
              f" {net_mw:>9.0f} {lcoe_str:>14}")

    # =========================================================================
    # KEY BINDING CONSTRAINTS NARRATIVE
    # =========================================================================
    print(f"\n\n{'=' * 72}")
    print("KEY BINDING CONSTRAINTS — Top LCOE Drivers")
    print("=" * 72)

    print("""
  1. RECIRCULATING POWER / Q VALUE (Critical leverage)

     The SFS Z-pinch has the highest recirculating fraction of any concept in
     this analysis. At Q=10 and 70% driver efficiency, the driver consumes ~43%
     of gross electric output. If Q falls to 5, recirculating fraction climbs to
     ~85%, leaving minimal net output.

     Baseline: Q=10 gives ~{:.0f}% recirculating fraction.
     Q is a CALCULATED PROJECTION — never experimentally demonstrated at any scale.
     Commercial Q requires 200 µs pinch lifetime; FuZE demonstrates 20–40 µs.
     This is the dominant uncertainty in the entire model.

     LCOE sensitivity: Q=7 → Q=15 spans ~3× LCOE swing.

  2. PULSED POWER DRIVER COST (Dominant capital cost)

     The pulsed power driver (C220107) is the largest single CAS22 sub-account,
     substituting for the magnet system cost in tokamak concepts. With NO published
     cost estimate for a commercial Z-pinch driver, the assumed $150M/module carries
     HIGH UNCERTAINTY (plausible range: $30M–$500M/module).

     No magnet system (C220103=$0) eliminates the dominant tokamak cost, but the
     pulsed power driver cost offsets this advantage. The net capital advantage
     vs. compact HTS tokamaks depends entirely on driver manufacturing economics.

     LCOE sensitivity: $30M vs $500M/module spans ~2× LCOE swing.

  3. MODULAR SCALE / REP RATE (Net power denominator)

     Net electric per module is thin (~{:.0f} MWe at baseline). LCOE is highly
     sensitive to anything that reduces net output further (lower Q, lower rep rate,
     higher auxiliary loads). The 50 MWe/module target requires simultaneously:
     Q > 10 (undemonstrated), 10 Hz (undemonstrated at Century), and ~37% thermal
     efficiency (not published). Any one of these falling short collapses net output.

     Century is at 0.2 Hz — 50× below commercial. The rep rate scaling path
     (thermal management, electrode durability, LiPb dynamics at 10 Hz) is the
     most concrete engineering challenge between current state and commercial viability.

  NOTE: All values carry HIGH UNCERTAINTY. This model maps the plausible LCOE
  corridor, not a point estimate. The dominant message is sensitivity to Q and
  driver cost, both of which are currently unconstrained by experiment.
""".format(
        base_results["power"]["recirc_fraction"] * 100,
        base_results["power"]["p_net"],
    ))

    print("=" * 72)
    print("NOTE: All estimates carry HIGH UNCERTAINTY. This model is a first-pass")
    print("corridor map. Key anchors (Q>10, 10 Hz, driver cost) are unvalidated.")
    print("Parameter values sourced from engineering-paradigms-paper-summary.md,")
    print("century-demo-system.md, and 1costingfe costing_constants.yaml.")
    print("=" * 72)


if __name__ == "__main__":
    main()
