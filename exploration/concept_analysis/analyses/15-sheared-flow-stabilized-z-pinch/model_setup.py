"""
Sheared-Flow Stabilized Z-Pinch (SFS Z-Pinch) — First-Pass LCOE Model
=======================================================================
1cFE First Pass Concept Analysis
Concept: Sheared-Flow Stabilized Z-Pinch with D-T fuel
Company: Zap Energy (Seattle, WA; founded 2017; ~$330M raised as of 2026)
Commercial Device Series: FuZE → FuZE-Q → FuZE-3 → Century → pilot plant

This is a parameterized LCOE model built from publicly available information
in the Engineering Paradigms paper (Thompson et al., FST 2023), Century demo
system updates, FuZE-3 gigapascal results, and the OSTI 2025 pulsed power
challenges report (LLNL-JRNL-2001600).

Cost accounting follows the CAS (Code of Accounts System) structure used in
1costingfe / pyFECONS. Power-scaling laws are adapted from 1costingfe's
costing_constants.yaml, with concept-specific overrides for:
  - C220103 (Coils): 0 — no superconducting or conventional magnets
  - C220104 (Heating): 0 — no auxiliary heating (no NBI, ECRH, or laser)
  - C220107 (Power Supplies): pulsed power driver OVERRIDE (capacitors + switches + PFNs)
  - C220108 (Target/Electrode Factory): electrode manufacturing system OVERRIDE

Architecture: multi-module plant (n_mod × ~46 MWe/module per baseline)

Economy-of-scale post-hoc scaling: For cross-concept comparison at 1000 MWe
reference, the `scaled_headline` dict applies a power-law correction:
    LCOE_scaled = LCOE_native * (P_native / 1000) ^ (1 - alpha)
    alpha = 0.6 (standard fusion plant economy-of-scale exponent)
The native physics and cost model are NOT altered — only the headline numbers
are adjusted for comparison. All parameter sweeps and scenario tables use
native power levels.

Key references:
- Thompson, Levitt, Nelson, Shumlak — "Engineering Paradigms for SFS Z-Pinch
  Fusion Energy", Fusion Science & Technology (2023)
  (summarized in knowledge/concept_research/15-.../engineering-paradigms-paper-summary.md)
- Zap Energy — Century Demo System (FST 2025 / press release)
  (century-demo-system.md)
- FuZE-3 Gigapascal Results, Zap Energy press release, Nov 2025
  (fuze-3-gigapascal-results-2025.md)
- OSTI "Challenges and Gaps in Pulsed Power for Fusion" (LLNL-JRNL-2001600, 2025)
  (osti-servlets-purl-2588719.md)
- 1costingfe costing_constants.yaml — scaling laws and unit costs
  (https://github.com/1cFE/1costingfe)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass


# === Reference power levels for scaling laws (from 1costingfe costing_constants.yaml) ===
P_TH_REF = 2500.0   # Reference thermal power [MW]
P_ET_REF = 1100.0   # Reference gross electric power [MW]


@dataclass
class SFSZPinchParams:
    """
    Parameterized SFS Z-Pinch power plant model (Zap Energy concept).
    All parameters have source annotations. Uncertainty levels:
      (no tag)             = well-established value with published source
      MODERATE UNCERTAINTY = reasonable estimate from analogues
      HIGH UNCERTAINTY     = speculative or poorly constrained
    """

    # === PLASMA / FUSION PHYSICS ===

    fusion_energy_per_pulse_MJ: float = 19.0
    """Fusion energy per Z-pinch pulse [MJ].
    Source: Thompson et al. FST 2023 Table I: "19 MJ fusion energy per pulse"
    at commercial design point (Q > 10, 1.2–1.5 MA pinch current).
    Ref: engineering-paradigms-paper-summary.md §Design Parameters.
    MODERATE UNCERTAINTY: calculated projection, never experimentally demonstrated."""

    Q_sci: float = 10.0
    """Scientific fusion gain Q_sci = P_fus / P_plasma_input (dimensionless).
    Source: Engineering Paradigms paper: "Q > 10 at plant-relevant currents."
    Ref: engineering-paradigms-paper-summary.md §Physics Assumptions.
    HIGH UNCERTAINTY: Q not experimentally demonstrated at any scale. FuZE demonstrated
    thermonuclear neutrons but not Q > 1. Commercial requires 200 µs pinch lifetime;
    FuZE demonstrated 20–40 µs (5–10× extrapolation). This is the single most
    constraining gap in the entire model."""

    rep_rate_Hz: float = 10.0
    """Shot repetition rate [Hz] (shots per second per module).
    Source: Zap Energy commercial target is 10 Hz.
    Ref: zap-energy-website-how-it-works.md §Commercial Design; dossier.md §Repetition Rate.
    HIGH UNCERTAINTY: Century demonstrated 0.2 Hz (50× gap to commercial); no path to 10 Hz
    published. Rep rate scaling is a program-level risk comparable to Q demonstration."""

    driver_eta: float = 0.70
    """Wall-to-plasma efficiency (fraction of stored electrical energy delivered to plasma).
    Source: Engineering Paradigms paper: AC-DC rectification ~90% × modulator ~80% = ~70%.
    Ref: engineering-paradigms-paper-summary.md §Driver Efficiency.
    MODERATE UNCERTAINTY: demonstrated at subscale; commercial-scale unverified."""

    blanket_energy_multiplication: float = 1.10
    """Blanket energy multiplication M (neutron energy amplification in LiPb blanket).
    Source: Standard D-T LiPb value; consistent with Engineering Paradigms TBR ~1.1.
    Ref: engineering-paradigms-paper-summary.md §Blanket Design; dossier.md §Tritium Breeding.
    Pb provides (n,2n) multiplication; Li-6(n,T)He-4 reaction is exothermic (+4.8 MeV)."""

    thermal_efficiency: float = 0.38
    """Thermal-to-electric conversion efficiency (LiPb → steam Rankine cycle).
    Source: Engineering Paradigms paper implies steam Rankine; LiPb solidification point
    ~235°C sets a floor on blanket outlet temperature, limiting Rankine efficiency.
    Ref: engineering-paradigms-paper-summary.md §Heat Extraction; dossier.md §Energy Capture.
    MODERATE UNCERTAINTY: cycle design unpublished; 38% is plausible for LiPb-cooled Rankine."""

    # === PLANT CONFIGURATION ===

    n_mod: int = 10
    """Number of fusion modules (Z-pinch cores + driver + blanket) per plant.
    Source: Century described as "close to eventual size of single module producing ~50 MWe."
    Multi-module architecture required for utility scale; 10 modules → ~460 MWe.
    Ref: century-demo-system.md §Commercial Scale.
    MODERATE UNCERTAINTY: commercial plant module count unspecified by Zap Energy."""

    plant_availability: float = 0.75
    """Plant capacity factor / availability.
    Source: No published estimate for pulsed Z-pinch power plant.
    Lower than 0.80 (NOAK tokamak) due to uncharacterized electrode maintenance
    intervals, LiPb system downtime, and pulsed power servicing requirements.
    ASSUMED: 0.75. HIGH UNCERTAINTY."""

    plant_lifetime_years: float = 40.0
    """Plant economic lifetime [years].
    Ref: Standard assumption consistent with 1costingfe and nuclear industry convention."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds 10% contingency (CAS29) per 1costingfe convention."""

    # === AUXILIARY POWER (per module) ===

    p_lipb_pump_MW: float = 2.0
    """LiPb pumping power per module [MW] (gravity cascade return pumping).
    Source: LiPb must be circulated under gravity and pumped back to injection nozzles.
    ASSUMED: 2 MW/module estimate from hydraulic analogy. MODERATE UNCERTAINTY."""

    p_house_MW: float = 1.5
    """Housekeeping and balance-of-plant auxiliary power per module [MW].
    Ref: Analogy to 1costingfe ife_zpinch.yaml defaults; vacuum pumping, gas injection,
    monitoring, controls at 10 Hz.
    ASSUMED: 1.5 MW/module."""

    p_trit_MW: float = 1.5
    """Tritium processing power per module [MW] (extraction from LiPb circuit).
    Source: Tritium must be extracted from circulating LiPb by vacuum permeation
    or cold trapping; significant pumping and separation power required.
    Ref: Analogy to 1costingfe fuel_handling defaults.
    MODERATE UNCERTAINTY: LiPb tritium extraction system design unpublished."""

    # === CHAMBER GEOMETRY ===

    chamber_inner_radius_m: float = 1.82
    """Inner radius of fusion chamber (spherical equivalent) [m].
    Source: Engineering Paradigms paper gives core volume ~25 m³.
    Derived: V = (4/3) pi r^3 → r = (3 * 25 / (4 * pi))^(1/3) = 1.82 m.
    Ref: engineering-paradigms-paper-summary.md §Design Parameters.
    The actual geometry is cylindrical (~3 m diameter); spherical equivalent used
    for volume-based cost scaling consistency with 1costingfe."""

    lipb_blanket_thickness_m: float = 3.0
    """LiPb flowing blanket thickness [m].
    Source: Engineering Paradigms paper + dossier: 3 m LiPb blanket achieves TBR ~1.1.
    Ref: engineering-paradigms-paper-summary.md §Blanket Design; dossier.md §Tritium Breeding.
    LiPb serves simultaneously as first wall, blanket, neutron shield, and tritium breeder."""

    shield_thickness_m: float = 0.25
    """Additional structural/biological shield thickness beyond LiPb [m].
    Source: LiPb provides primary neutron attenuation; additional borated steel/concrete
    for biological shielding of outer structure.
    ASSUMED: 0.25 m. MODERATE UNCERTAINTY."""

    structure_thickness_m: float = 0.30
    """Primary structural shell thickness [m].
    Ref: Analogy to IFE/MIF chamber structural design.
    ASSUMED: 0.30 m."""

    vessel_thickness_m: float = 0.15
    """Vacuum vessel / pressure boundary wall thickness [m].
    Ref: Analogy to IFE chamber vacuum vessel.
    ASSUMED: 0.15 m."""

    # === CAS22 OVERRIDES (concept-specific) ===

    driver_cost_per_module_M: float = 75.0
    """Capital cost of pulsed power driver per module [$M]. Maps to C220107 OVERRIDE.
    Source: No commercial-scale estimate exists. Analogy basis:
    - Commercial Z-pinch requires ~2.7 MJ stored electrical/shot at 10 Hz
    - Industrial pulsed power: $1–10/J for current non-repetitive systems
    - HIGH-CYCLE PREMIUM: current capacitors achieve 10^4–10^5 shots;
      commercial requires 10^8–10^9 shots (4–6 orders of magnitude gap)
    - OSTI 2025 (LLNL-JRNL-2001600): 10,000–216,000 capacitors/plant,
      4–6 year lead times, 125–250 years to build 150 plants at current Western
      manufacturing capacity; 10–20 year maturation timeline required
    - Switches: current SiC tops at 6.5–15 kV; Z-pinch requires 50–200 kV
      (different technology class, not just higher voltage rating)
    - $75M/module assumes substantial manufacturing learning and component cost
      reduction — optimistic end of plausible range.
    ASSUMED: HIGH UNCERTAINTY — no comparable commercial repetitive-pulse system exists."""

    electrode_system_cost_per_module_M: float = 20.0
    """Capital cost of electrode manufacturing/conditioning infrastructure per module [$M].
    Maps to C220108 OVERRIDE (replaces target factory account from IFE concepts).
    Source: Industrial arc furnace cathodes provide partial engineering analogy.
    Z-pinch electrodes are plasma-facing, current-carrying, neutron-activated components
    requiring dedicated fabrication, remote handling, and conditioning bays.
    ASSUMED: $20M/module. HIGH UNCERTAINTY: no nuclear-environment analogue."""

    lipb_blanket_unit_cost: float = 0.50
    """LiPb blanket/first-wall unit cost [M$/m^3].
    Source: 1costingfe costing_constants.yaml blanket_unit_cost_dt = 0.60 M$/m^3.
    Slightly reduced vs. solid D-T breeding blanket (no separate FW material needed),
    but includes LiPb recirculation pumps, nozzles, and heat exchangers.
    Ref: 1costingfe costing_constants.yaml."""

    # === OPERATING COSTS ===

    om_cost_per_MW_yr: float = 65.0
    """Fixed O&M cost scaling factor [$/kW/yr equivalent].
    (In compute: annual_om = om_cost_per_MW_yr * p_net_total_MW * 1000 / 1e6 M$/yr)
    Source: 1costingfe CAS70 D-T reference = 52 $/kW/yr at 1 GWe.
    Raised to 65 $/kW/yr for SFS Z-pinch: novel pulsed system, no O&M precedent,
    uncharacterized electrode replacement schedule, LiPb circuit maintenance,
    higher staff-to-MW ratio for a 10-module modular plant.
    Ref: 1costingfe costing_constants.yaml om_cost_dt = 52.0.
    HIGH UNCERTAINTY: no O&M baseline for pulsed Z-pinch at commercial scale."""

    electrode_replacement_cost_per_module_M: float = 3.0
    """Annual electrode replacement consumable cost per module [M$/yr].
    Electrodes erode under 14 MeV neutron bombardment and repeated 1 MA arcing.
    Activated electrodes require remote handling and disposal as radioactive waste.
    Replacement schedule and material cost unknown; $3M/module/yr is an estimate
    from industrial furnace cathode analogy + nuclear environment premium.
    ASSUMED: HIGH UNCERTAINTY. Enters CAS80 (consumables) not O&M."""

    core_lifetime_FPY: float = 3.0
    """LiPb circuit / chamber core lifetime in full-power-years before refurbishment.
    Source: 1costingfe core_lifetime_dt = 5.0 FPY for D-T blanket.
    Reduced to 3 FPY for SFS Z-pinch: LiPb activation buildup, structural material
    neutron damage at first wall surfaces, electrode/chamber erosion.
    Ref: 1costingfe costing_constants.yaml core_lifetime_dt = 5.0.
    HIGH UNCERTAINTY: no neutron fluence data for Z-pinch geometry."""

    # === FINANCIAL ===

    interest_rate: float = 0.08
    """Real discount rate / weighted average cost of capital.
    Ref: 1costingfe default interest_rate = 0.08."""

    inflation_rate: float = 0.02
    """Inflation rate for levelized O&M calculation.
    Ref: 1costingfe default."""

    construction_time_years: float = 6.0
    """Plant construction period [years].
    Ref: 1costingfe reference_construction_time = 6.0."""

    # === FUEL COSTS ===

    deuterium_cost_per_kg: float = 2175.0
    """Deuterium unit cost [$/kg].
    Ref: 1costingfe costing_constants.yaml u_deuterium = 2175."""

    dt_fuel_mass_per_pulse_kg: float = 1.5e-7
    """D-T fuel mass consumed per pulse [kg].
    Derivation: 19 MJ fusion at 17.6 MeV/reaction → ~6.7e18 reactions → ~3.3e-8 mol DT
    → ~1.0e-7 kg. ~50% is deuterium (purchased); tritium is self-bred from LiPb blanket.
    MODERATE UNCERTAINTY: fuel mass well-defined by fusion physics; tritium self-breeding
    requires TBR >= 1.0 (calculated at 1.1, marginal)."""

    def _compute_power(self) -> dict:
        """Layer 1: Per-module power balance.

        Energy flow:
          stored electrical -> (driver_eta) -> plasma -> (x Q_sci) -> fusion
          D-T: 80% neutron energy -> blanket (x blanket_mult), 20% alpha -> thermal
          Gross electric = P_thermal * thermal_efficiency
          Net electric = Gross - Driver avg power (recirculating) - Auxiliaries
        """
        r = {}

        # Plasma input per pulse (energy delivered to plasma)
        plasma_input_MJ = self.fusion_energy_per_pulse_MJ / self.Q_sci
        r["plasma_input_per_pulse_MJ"] = plasma_input_MJ

        # Stored electrical energy per pulse (wall plug, in capacitors)
        driver_stored_MJ = plasma_input_MJ / self.driver_eta
        r["driver_stored_per_pulse_MJ"] = driver_stored_MJ

        # Time-averaged fusion power at rep rate
        p_fus = self.fusion_energy_per_pulse_MJ * self.rep_rate_Hz   # MW
        r["p_fus"] = p_fus

        # D-T neutron/alpha power split: 80%/20%
        p_neutron = 0.80 * p_fus
        p_alpha   = 0.20 * p_fus
        r["p_neutron"] = p_neutron
        r["p_alpha"]   = p_alpha

        # Thermal power: blanket multiplies neutron energy; alpha deposits in plasma/wall
        # Driver inefficiency losses occur in driver hardware (not captured as useful heat)
        p_th = self.blanket_energy_multiplication * p_neutron + p_alpha
        r["p_th"] = p_th

        # Gross electric per module
        p_et = p_th * self.thermal_efficiency
        r["p_et"] = p_et

        # Driver average recirculating power (continuous recharge at rep rate)
        driver_avg_MW = driver_stored_MJ * self.rep_rate_Hz
        r["driver_avg_power_MW"] = driver_avg_MW

        # Other auxiliaries per module
        p_aux = self.p_lipb_pump_MW + self.p_house_MW + self.p_trit_MW
        r["p_aux"] = p_aux

        # Net electric per module
        p_net = p_et - driver_avg_MW - p_aux
        r["p_net"] = p_net

        # Plant totals (n_mod modules)
        r["p_net_plant"] = p_net * self.n_mod
        r["p_et_plant"]  = p_et  * self.n_mod
        r["p_th_plant"]  = p_th  * self.n_mod

        # Derived figures of merit
        r["Q_sci"] = self.Q_sci
        r["Q_eng"] = p_fus / driver_avg_MW if driver_avg_MW > 0 else 0.0
        r["recirc_fraction"] = (driver_avg_MW + p_aux) / p_et if p_et > 0 else float('inf')

        # Shots per year per module (used for consumable cost)
        r["shots_per_year_per_module"] = self.rep_rate_Hz * 3600.0 * 8760.0 * self.plant_availability

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Chamber shell volumes using spherical equivalent geometry.

        The Z-pinch chamber is cylindrical (~3 m diameter, ~3.5 m tall per
        25 m^3 core volume), but spherical equivalent geometry is used for
        volume-based cost scaling consistency with 1costingfe.

        Shell sequence (inside out):
          [plasma] -> LiPb blanket (first wall + breeding + primary shield)
                   -> additional bioshield
                   -> primary structure
                   -> vacuum vessel
        """
        r = {}
        ri = self.chamber_inner_radius_m

        def sphere_shell_vol(r_in: float, thickness: float) -> float:
            r_out = r_in + thickness
            return (4.0 / 3.0) * math.pi * (r_out ** 3 - r_in ** 3)

        r["blanket_vol_m3"]   = sphere_shell_vol(ri, self.lipb_blanket_thickness_m)
        r_bl_out = ri + self.lipb_blanket_thickness_m

        r["shield_vol_m3"]    = sphere_shell_vol(r_bl_out, self.shield_thickness_m)
        r_sh_out = r_bl_out + self.shield_thickness_m

        r["structure_vol_m3"] = sphere_shell_vol(r_sh_out, self.structure_thickness_m)
        r_st_out = r_sh_out + self.structure_thickness_m

        r["vessel_vol_m3"]    = sphere_shell_vol(r_st_out, self.vessel_thickness_m)
        r["outer_radius_m"]   = r_st_out + self.vessel_thickness_m

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts.

        Standard 1costingfe volume/power scaling with Z-pinch-specific overrides:
          C220103 = 0   (no magnets of any kind — no SC, no conventional, no Helmholtz)
          C220104 = 0   (no auxiliary heating — no NBI, ECRH, or laser preheat)
          C220107 = driver_cost_per_module_M  (pulsed power driver)
          C220108 = electrode_system_cost_per_module_M  (electrode manufacturing system)

        Scaling exponents from 1costingfe costing_constants.yaml:
          Blanket/shield:   (p_th / P_TH_REF)^0.6
          Structure/vessel: (p_et / P_ET_REF)^0.5 or ^0.6
        """
        r = {}
        p_th  = max(power["p_th"],  1.0)
        p_et  = max(power["p_et"],  1.0)
        p_net = max(power["p_net"], 1.0)

        # C220101: LiPb First Wall + Blanket (combined; LiPb IS the first wall)
        # Unit cost 0.50 M$/m^3 (slightly below 0.60 for solid DT blanket; includes
        # LiPb recirculation hardware but no separate FW armor material required).
        # Scaling: 1costingfe (p_th / P_TH_REF)^0.6
        r["C220101"] = (self.lipb_blanket_unit_cost
                        * geom["blanket_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220102: Additional biological/structural shield (borated steel, concrete)
        # Ref: 1costingfe shield_unit_cost = 0.74 M$/m^3, D-T fuel scale = 1.0
        r["C220102"] = 0.74 * geom["shield_vol_m3"] * 1.0 * (p_th / P_TH_REF) ** 0.6

        # C220103: Coils — OVERRIDE $0 (no magnets)
        # No superconducting magnets, no conventional coils, no HTS tape, no cryogenics.
        # This is the largest structural simplification vs. tokamak/stellarator designs.
        r["C220103"] = 0.0  # OVERRIDE: no magnets

        # C220104: Supplementary Heating — OVERRIDE $0 (no auxiliary heating)
        # No NBI, no ECRH, no laser preheat. Plasma heated by Z-pinch compression alone.
        r["C220104"] = 0.0  # OVERRIDE: no auxiliary heating

        # C220105: Primary Structure
        # Ref: 1costingfe structure_unit_cost = 0.15 M$/m^3, (p_et/P_ET_REF)^0.5
        r["C220105"] = 0.15 * geom["structure_vol_m3"] * (p_et / P_ET_REF) ** 0.5

        # C220106: Vacuum System (vessel + turbo/cryo pumps)
        # Ref: 1costingfe vessel_unit_cost = 0.72 M$/m^3, (p_et/P_ET_REF)^0.6
        r["C220106"] = 0.72 * geom["vessel_vol_m3"] * (p_et / P_ET_REF) ** 0.6

        # C220107: Power Supplies — OVERRIDE with pulsed power driver
        # Capacitor bank + pulse-forming networks + high-voltage switches + buswork.
        # Standard formula (80 * (p_et/1000)^0.7) replaced by per-module direct estimate.
        # Ref: osti-servlets-purl-2588719.md §Energy Storage and §High Voltage Switching
        r["C220107"] = self.driver_cost_per_module_M  # OVERRIDE: pulsed power driver

        # C220108: Electrode Manufacturing System — OVERRIDE (replaces target factory)
        # Fabrication bays, conditioning equipment, remote handling for activated electrodes.
        # No targets or liners (unlike IFE/MagLIF); electrodes are the per-shot consumable.
        r["C220108"] = self.electrode_system_cost_per_module_M  # OVERRIDE: electrode system

        # C220109: Direct Energy Converter — not applicable
        r["C220109"] = 0.0

        # C220110: Remote Handling & Maintenance Equipment
        # Required for activated electrodes, LiPb circuit components, and chamber access.
        # Ref: 1costingfe remote_handling_dt_base = 150 M$ at 1 GWe, scaled (p_net/1000)^0.7
        # concept_rh_scale = 0.6 (linear/open geometry; no in-vessel transporter needed,
        # but activated electrode and LiPb handling still required)
        r["C220110"] = 150.0 * 0.6 * (p_net / 1000.0) ** 0.7

        # C220111: Installation Labor
        # Ref: 1costingfe installation_frac = 0.14 of reactor hardware subtotal
        reactor_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"])
        r["C220111"] = 0.14 * reactor_subtotal

        # C220112: Isotope Separation — handled in CAS80 fuel costs
        r["C220112"] = 0.0

        # Per-module subtotal
        r["CAS22_per_module"] = reactor_subtotal + r["C220111"] + r["C220112"]

        # --- Plant-wide accounts ---
        p_net_total = p_net * self.n_mod
        p_th_total  = p_th  * self.n_mod

        # C220200: Main & Secondary Coolant (LiPb primary + steam secondary)
        # Ref: 1costingfe CAS22 formulas (cas22.py)
        C220201 = 166.0 * (p_net_total / 1000.0)
        C220202 = 40.6  * (p_th_total / 3500.0) ** 0.55
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling (NO cryoplant — no magnets, no cryogenic systems)
        # Ref: 1costingfe C220301 = 1.1e-3 * p_th_total; C220302 (cryoplant) = 0
        r["C220300"] = 1.1e-3 * p_th_total

        # C220400: Radioactive Waste Management
        # Ref: 1costingfe 1.96 * (p_th / 1000)
        r["C220400"] = 1.96 * (p_th_total / 1000.0)

        # C220500: Fuel Handling & Storage (D-T: tritium extraction from LiPb + D2)
        # Ref: 1costingfe fuel_handling_dt_base = 120 M$ at 1 GWe, (p_net/1000)^0.7
        r["C220500"] = 120.0 * (p_net_total / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        # Ref: 1costingfe 11.5 * (p_net/1000)^0.8
        r["C220600"] = 11.5 * (p_net_total / 1000.0) ** 0.8

        # C220700: Instrumentation & Control
        # Ref: 1costingfe 85.0 * (p_th/3500)^0.65
        r["C220700"] = 85.0 * (p_th_total / 3500.0) ** 0.65

        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        r["CAS22"] = r["CAS22_per_module"] * self.n_mod + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: CAS10-60 capital cost structure.

        Building costs from 1costingfe costing_constants.yaml ($/kW gross electric).
        No cryogenics building; pulsed power storage building added.
        """
        r = {}
        p_et_plant  = max(power["p_et"],  1.0) * self.n_mod
        p_net_plant = max(power["p_net"], 1.0) * self.n_mod

        # === CAS10: Pre-construction ===
        # Ref: 1costingfe costing_constants.yaml CAS10 entries
        site_permits   = 3.0
        plant_studies  = 4.0 if self.noak else 20.0
        plant_permits  = 2.0
        plant_reports  = 1.0
        other_precon   = 1.0
        land_cost      = 0.25 * p_net_plant * math.sqrt(self.n_mod) * 10_000 / 1e6
        licensing_cost = 2.5 if self.noak else 5.0   # D-T licensing: $5M FOAK, $2.5M NOAK
        r["CAS10"] = (site_permits + plant_studies + plant_permits + plant_reports
                      + other_precon + land_cost + licensing_cost)

        # === CAS21: Buildings ===
        # Ref: 1costingfe building_costs_per_kw ($/kW gross electric, 2024$)
        # No cryogenics building; pulsed power storage building replaces cryogenics.
        building_per_kW = {
            "site_improvements":     268.0,
            "reactor_building":      126.0,
            "turbine_building":       54.0,
            "cooling_structures":     12.0,
            "pulsed_power_building":  25.0,   # houses capacitor banks (no cryogenics)
            "hot_cell":               93.4,
            "misc_buildings":         71.6,
        }
        total_bldg_per_kW = sum(building_per_kW.values())   # ~650 $/kW
        r["CAS21"] = total_bldg_per_kW * p_et_plant / 1000.0   # M$

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment ===
        # Ref: 1costingfe turbine_per_mw = 0.19764 M$/MW
        r["CAS23"] = p_et_plant * 0.19764

        # === CAS24: Electric Plant Equipment ===
        # Ref: 1costingfe electric_per_mw = 0.08418 M$/MW
        r["CAS24"] = p_et_plant * 0.08418

        # === CAS25: Miscellaneous Plant Equipment ===
        # Ref: 1costingfe misc_per_mw = 0.05124 M$/MW
        r["CAS25"] = p_et_plant * 0.05124

        # === CAS26: Heat Rejection ===
        # Ref: 1costingfe heat_rej_per_mw = 0.03416 M$/MW
        r["CAS26"] = p_et_plant * 0.03416

        # === CAS27: Special Materials (LiPb initial inventory) ===
        # LiPb eutectic fill for multi-module plant; commodity Pb + Li.
        # Ref: 1costingfe special_materials_dt = 15 M$ at 1 GWe, scaled by p_net
        r["CAS27"] = 15.0 * (p_net_plant / 1000.0)

        # === CAS28: Digital Twin ===
        # Ref: 1costingfe digital_twin = 5.0 M$
        r["CAS28"] = 5.0

        # === CAS29: Contingency ===
        # Ref: 1costingfe contingency_rate_noak = 0.0, contingency_rate_foak = 0.10
        cas20_sub = sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                        "CAS25", "CAS26", "CAS27", "CAS28"])
        r["CAS29"] = 0.0 if self.noak else 0.10 * cas20_sub

        # === CAS20: Total Direct Costs ===
        r["CAS20"] = cas20_sub + r["CAS29"]

        # === CAS30: Indirect Costs ===
        # Ref: 1costingfe indirect_fraction = 0.20 of CAS20, scaled by construction time
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / 6.0)

        # === CAS40: Owner's Costs ===
        # Ref: 1costingfe owner_cost_dt = 39 M$ at 1 GWe, scaled (p_net/1000)^0.5
        r["CAS40"] = 39.0 * (p_net_plant / 1000.0) ** 0.5

        # === CAS50: Supplementary Costs ===
        # Ref: 1costingfe shipping 1.5%, spare parts 3%, taxes 1%, insurance 1.5%,
        # tritium startup 40 M$ at 1 GWe, decommissioning 127 M$ at 1 GWe
        spare_parts     = 0.03 * sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                                      "CAS25", "CAS26", "CAS27", "CAS28"])
        startup_tritium = 40.0  * (p_net_plant / 1000.0)
        shipping        = 0.015 * r["CAS20"]
        taxes           = 0.01  * r["CAS20"]
        insurance       = 0.015 * (r["CAS20"] + r["CAS30"])
        decom           = 127.0 * (p_net_plant / 1000.0)
        r["CAS50"] = spare_parts + startup_tritium + shipping + taxes + insurance + decom

        # === Overnight Capital ===
        overnight = r["CAS10"] + r["CAS20"] + r["CAS30"] + r["CAS40"] + r["CAS50"]
        r["overnight_capital"] = overnight

        # === CAS60: Interest During Construction ===
        # Ref: 1costingfe IDC formula: f_IDC = ((1+i)^T - 1) / (i*T) - 1
        i = self.interest_rate
        T = self.construction_time_years
        f_idc = ((1 + i) ** T - 1) / (i * T) - 1 if (i > 0 and T > 0) else 0.0
        r["CAS60"]  = f_idc * overnight
        r["f_IDC"]  = f_idc

        r["total_capital"] = overnight + r["CAS60"]

        p_net_for_spec = power["p_net"] * self.n_mod
        if p_net_for_spec > 0:
            r["specific_capital_USD_per_kWe"] = r["total_capital"] * 1e6 / (p_net_for_spec * 1e3)
        else:
            r["specific_capital_USD_per_kWe"] = float('inf')

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70-90 annualized costs and LCOE.

        LCOE = (CAS90 + CAS70 + CAS80) / annual_energy_MWh
        """
        r = {}
        p_net_total = max(power["p_net"], 0.0) * self.n_mod

        # Capital Recovery Factor
        i   = self.interest_rate
        n   = self.plant_lifetime_years
        crf = i * (1 + i) ** n / ((1 + i) ** n - 1)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]  # M$/yr

        # === CAS71: Annual Fixed O&M (levelized) ===
        annual_om_base = self.om_cost_per_MW_yr * p_net_total * 1000.0 / 1e6  # M$/yr
        g  = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g) ** Tc
        if abs(i - g) > 1e-10:
            pv_om = A1 * (1.0 - ((1 + g) / (1 + i)) ** n) / (i - g)
        else:
            pv_om = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_om  # M$/yr

        # === CAS72: Scheduled Core Replacement ===
        # LiPb circuit + chamber hardware replaced every core_lifetime_FPY full-power-years
        eff_yr = self.core_lifetime_FPY / self.plant_availability
        n_reps = max(0, int(math.ceil(n / eff_yr)) - 1)
        # Replacement cost = all modules' C220101 (LiPb circuit + chamber hardware)
        replacement_cost = cas22["C220101"] * self.n_mod
        pv_reps = sum(replacement_cost / (1 + i) ** (k * eff_yr)
                      for k in range(1, n_reps + 1)
                      if k * eff_yr < n)
        r["CAS72"] = crf * pv_reps  # M$/yr
        r["n_core_replacements"] = n_reps

        r["CAS70"] = r["CAS71"] + r["CAS72"]  # M$/yr

        # === CAS80: Fuel and Consumable Costs ===
        shots_plant_yr = power["shots_per_year_per_module"] * self.n_mod

        # Electrode replacement consumables (electrodes consumed under pulsed arc erosion)
        r["CAS80_electrodes"] = self.electrode_replacement_cost_per_module_M * self.n_mod

        # Deuterium fuel (tritium self-bred; only D purchased)
        annual_d_kg = shots_plant_yr * self.dt_fuel_mass_per_pulse_kg * 0.50
        r["CAS80_fuel"] = annual_d_kg * self.deuterium_cost_per_kg / 1e6  # M$/yr

        r["CAS80"] = r["CAS80_electrodes"] + r["CAS80_fuel"]  # M$/yr

        # === LCOE ===
        annual_rev_req = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_rev_req

        annual_energy_MWh = 8760.0 * p_net_total * self.plant_availability
        r["annual_energy_MWh"] = annual_energy_MWh

        if annual_energy_MWh > 0 and p_net_total > 0:
            lcoe = annual_rev_req * 1e6 / annual_energy_MWh
            r["lcoe_USD_per_MWh"]   = lcoe
            r["lcoe_cents_per_kWh"] = lcoe / 10.0
        else:
            r["lcoe_USD_per_MWh"]   = float('inf')
            r["lcoe_cents_per_kWh"] = float('inf')

        if annual_rev_req > 0:
            r["capital_fraction"]    = r["CAS90"] / annual_rev_req
            r["om_fraction"]         = r["CAS70"] / annual_rev_req
            r["consumable_fraction"] = r["CAS80"] / annual_rev_req

        return r

    def compute(self) -> dict:
        """Compute LCOE via CAS-structured accounting. Returns full output dict."""
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


# ============================================================
# Module-level interface for concept explorer
# ============================================================
params  = SFSZPinchParams()
results = params.compute()

# Post-hoc scaling to 1000 MWe (cross-concept comparison)
# Physics and native cost model are UNCHANGED.
# alpha = 0.6: standard fusion plant economy-of-scale exponent (1costingfe convention).
_ALPHA    = 0.6
_p_native = results["power"].get("p_net_plant", results["power"]["p_net"])
_factor   = (_p_native / 1000.0) ** (1.0 - _ALPHA)
_overnight = results["costs"]["overnight_capital"] * 1e3 / _p_native  # $/kW native

scaled_headline = {
    "p_net_mw":       1000.0,
    "lcoe_per_mwh":   results["economics"]["lcoe_USD_per_MWh"] * _factor,
    "overnight_per_kw": _overnight * _factor,
}


# ============================================================
# Output functions
# ============================================================

def print_results(p: SFSZPinchParams, res: dict):
    """Pretty-print full CAS-structured results."""
    power = res["power"]
    cas22 = res["cas22"]
    costs = res["costs"]
    econ  = res["economics"]

    print("=" * 72)
    print("SFS Z-Pinch (D-T) LCOE Model — 1cFE CAS-Structured (Zap Energy)")
    print("=" * 72)

    print("\n--- Key Input Parameters ---")
    print(f"  Fusion Q_sci:               {p.Q_sci:.1f}  [HIGH UNCERTAINTY: not demonstrated]")
    print(f"  Fusion energy/pulse:        {p.fusion_energy_per_pulse_MJ:.0f} MJ")
    print(f"  Rep rate:                   {p.rep_rate_Hz:.0f} Hz  [HIGH UNCERTAINTY: Century at 0.2 Hz]")
    print(f"  Driver wall-to-plasma eta:  {p.driver_eta:.0%}")
    print(f"  Blanket multiplication:     {p.blanket_energy_multiplication:.2f}")
    print(f"  Thermal efficiency:         {p.thermal_efficiency:.0%}")
    print(f"  Plant availability:         {p.plant_availability:.0%}")
    print(f"  Modules:                    {p.n_mod}")
    print(f"  FOAK/NOAK:                  {'NOAK' if p.noak else 'FOAK'}")
    print(f"  Interest rate:              {p.interest_rate:.0%}")
    print(f"  Plant lifetime:             {p.plant_lifetime_years:.0f} yr")

    print("\n--- Power Balance (per module) ---")
    print(f"  Driver stored energy/pulse: {power['driver_stored_per_pulse_MJ']:.2f} MJ")
    print(f"  Fusion power (avg):         {power['p_fus']:.0f} MW")
    print(f"    Neutron power:            {power['p_neutron']:.0f} MW (80%)")
    print(f"    Alpha power:              {power['p_alpha']:.0f} MW (20%)")
    print(f"  Thermal power:              {power['p_th']:.0f} MW")
    print(f"  Gross electric:             {power['p_et']:.1f} MWe")
    print(f"  Recirculating:")
    print(f"    Driver recharge:          {power['driver_avg_power_MW']:.1f} MW")
    print(f"    Auxiliaries:              {power['p_aux']:.1f} MW  (LiPb pump+house+trit)")
    print(f"  Net electric (per module):  {power['p_net']:.1f} MWe")
    print(f"  Net electric (plant):       {power['p_net_plant']:.0f} MWe  ({p.n_mod} modules)")
    print(f"  Q_sci:                      {power['Q_sci']:.1f}")
    print(f"  Q_eng (p_fus/p_driver):     {power['Q_eng']:.2f}")
    print(f"  Recirculating fraction:     {power['recirc_fraction']:.1%}")

    print("\n--- CAS22: Reactor Plant Equipment ---")
    cas22_labels = {
        "C220101": "LiPb First Wall + Blanket",
        "C220102": "Additional Shield",
        "C220103": "Coils [OVERRIDE: $0, none]",
        "C220104": "Aux Heating [OVERRIDE: $0, none]",
        "C220105": "Primary Structure",
        "C220106": "Vacuum System",
        "C220107": "Pulsed Power Driver [OVERRIDE]",
        "C220108": "Electrode System [OVERRIDE]",
        "C220110": "Remote Handling",
        "C220111": "Installation",
    }
    overrides = {"C220103", "C220104", "C220107", "C220108"}
    print("  Per-module accounts:")
    for code, label in cas22_labels.items():
        val = cas22.get(code, 0.0)
        tag = " [override]" if code in overrides else ""
        if val > 0.01 or code in overrides:
            print(f"    {code} {label:<36s} ${val:>8.1f}M{tag}")
    print(f"  {'─' * 56}")
    print(f"    Per-module subtotal:                      ${cas22['CAS22_per_module']:>8.1f}M x{p.n_mod}")

    pw_labels = {
        "C220200": "LiPb + Steam Coolant Systems",
        "C220300": "Aux Cooling (no cryoplant)",
        "C220400": "Rad Waste Management",
        "C220500": "Fuel Handling (D-T/LiPb/tritium)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    print("  Plant-wide accounts:")
    for code, label in pw_labels.items():
        val = cas22.get(code, 0.0)
        if val > 0.01:
            print(f"    {code} {label:<36s} ${val:>8.1f}M")
    print(f"  {'─' * 56}")
    print(f"    Plant-wide subtotal:                      ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                               ${cas22['CAS22']:>9.1f}M")

    print("\n--- Capital Costs (CAS10-60) ---")
    for key, label in [
        ("CAS10", "Pre-construction"),
        ("CAS21", "Buildings"),
        ("CAS22", "Reactor Plant Equipment"),
        ("CAS23", "Turbine Plant"),
        ("CAS24", "Electric Plant"),
        ("CAS25", "Misc Plant"),
        ("CAS26", "Heat Rejection"),
        ("CAS27", "Special Materials (LiPb)"),
        ("CAS28", "Digital Twin"),
        ("CAS29", "Contingency"),
    ]:
        print(f"  {key} {label:<36s} ${costs[key]:>8.1f}M")
    print(f"  {'─' * 56}")
    print(f"  CAS20 Direct Costs:                        ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30 Indirect Costs:                      ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40 Owner's Costs:                       ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50 Supplementary:                       ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 56}")
    print(f"  Overnight Capital:                         ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60 IDC (f={costs['f_IDC']:.3f}):                   ${costs['CAS60']:>8.1f}M")
    print(f"  {'=' * 56}")
    print(f"  Total Capital:                             ${costs['total_capital']:>8.1f}M")
    print(f"  Specific Capital:                          ${costs['specific_capital_USD_per_kWe']:>8.0f} $/kWe")

    print("\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90 Capital charge (CRF={econ['CRF']:.4f}):     ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71 O&M (levelized):                     ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72 Core replacements ({econ['n_core_replacements']}x):            ${econ['CAS72']:>8.1f}M/yr")
    print(f"  CAS70 Total O&M:                           ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80 Electrode consumables:               ${econ['CAS80_electrodes']:>8.1f}M/yr")
    print(f"  CAS80 D-T fuel (D only):                   ${econ['CAS80_fuel']:>10.3f}M/yr")
    print(f"  CAS80 Total:                               ${econ['CAS80']:>8.1f}M/yr")

    print("\n--- LCOE ---")
    print(f"  Annual energy production: {econ['annual_energy_MWh']:>12,.0f} MWh")
    print(f"  Annual revenue req:       ${econ['annual_revenue_req']:>9.1f}M")
    print(f"  +---------------------------------------------------+")
    print(f"  | LCOE (native {power['p_net_plant']:.0f} MWe) = {econ['lcoe_cents_per_kWh']:.2f} c/kWh      |")
    print(f"  |                       = {econ['lcoe_USD_per_MWh']:.1f} $/MWh             |")
    print(f"  +---------------------------------------------------+")
    print(f"  Capital fraction (CAS90): {econ.get('capital_fraction', 0):.1%}")
    print(f"  O&M fraction (CAS70):     {econ.get('om_fraction', 0):.1%}")
    print(f"  Consumables (CAS80):      {econ.get('consumable_fraction', 0):.1%}")

    # Scaled headline
    _p_nat  = power.get("p_net_plant", power["p_net"])
    _fac    = (_p_nat / 1000.0) ** (1.0 - _ALPHA)
    _oc_kw  = costs["overnight_capital"] * 1e3 / _p_nat
    print(f"\n  Post-hoc 1000 MWe scaling (alpha=0.6):")
    print(f"    LCOE @ 1000 MWe:      {econ['lcoe_USD_per_MWh'] * _fac:.1f} $/MWh")
    print(f"    Overnight @ 1000 MWe: ${_oc_kw * _fac:,.0f} /kW")


def sensitivity_sweep(base_p: SFSZPinchParams, param_name: str,
                      values: list, label: str = "") -> list:
    """Sweep one parameter and return [{param_value, lcoe_cents_kWh, p_net_plant_MW}]."""
    out = []
    for val in values:
        p = SFSZPinchParams(**{**base_p.__dict__, param_name: val})
        r = p.compute()
        out.append({
            "param_value":    float(val),
            "lcoe_cents_kWh": r["economics"]["lcoe_cents_per_kWh"],
            "p_net_plant_MW": r["power"]["p_net_plant"],
        })
    return out


def main():
    # ==================================================================
    # 1. BASELINE SCENARIO
    # ==================================================================
    print("\n" + "#" * 72)
    print("# BASELINE: SFS Z-Pinch — Moderate Design Point")
    print("#   Q=10, 10 Hz, 10 modules, eta_th=38%, avail=75%, $75M driver/mod")
    print("#" * 72)

    baseline     = SFSZPinchParams()
    base_results = baseline.compute()
    print_results(baseline, base_results)

    # ==================================================================
    # 2. SENSITIVITY SWEEPS
    # ==================================================================
    print("\n\n" + "=" * 72)
    print("SENSITIVITY SWEEPS (from baseline)")
    print("=" * 72)

    sweeps = [
        ("Q_sci",
         [5.0, 7.0, 10.0, 12.0, 15.0, 20.0],
         "Fusion Q_sci (gain)"),
        ("driver_cost_per_module_M",
         [25.0, 50.0, 75.0, 125.0, 200.0, 350.0],
         "Driver cost per module [M$]"),
        ("plant_availability",
         [0.50, 0.60, 0.70, 0.75, 0.80, 0.90],
         "Plant availability"),
        ("thermal_efficiency",
         [0.30, 0.33, 0.35, 0.38, 0.40, 0.42],
         "Thermal efficiency"),
        ("n_mod",
         [4, 6, 8, 10, 15, 20],
         "Number of modules"),
        ("driver_eta",
         [0.55, 0.60, 0.65, 0.70, 0.75, 0.80],
         "Wall-to-plasma efficiency"),
        ("electrode_replacement_cost_per_module_M",
         [0.5, 1.0, 3.0, 5.0, 10.0, 20.0],
         "Electrode replacement cost [M$/mod/yr]"),
    ]

    for param_name, values, label in sweeps:
        print(f"\n  {label}:")
        rows = sensitivity_sweep(baseline, param_name, values)
        for row in rows:
            pval = row["param_value"]
            lcoe = row["lcoe_cents_kWh"]
            net  = row["p_net_plant_MW"]
            if net <= 0:
                print(f"    {pval:>8.3g}  ->  NET POWER NEGATIVE ({net:.0f} MWe)")
            else:
                print(f"    {pval:>8.3g}  ->  {lcoe:6.2f} c/kWh  ({net:.0f} MWe net)")

    # ==================================================================
    # 3. SCENARIO COMPARISON TABLE
    # ==================================================================
    print("\n\n" + "=" * 72)
    print("SCENARIO COMPARISON")
    print("=" * 72)

    scenarios = {
        "Conservative (Q=7)": SFSZPinchParams(
            Q_sci=7.0,
            driver_cost_per_module_M=150.0,
            plant_availability=0.65,
            thermal_efficiency=0.33,
            n_mod=10,
            electrode_replacement_cost_per_module_M=8.0,
            core_lifetime_FPY=2.0,
        ),
        "Moderate (baseline)": SFSZPinchParams(),
        "Optimistic (Q=15)": SFSZPinchParams(
            Q_sci=15.0,
            driver_cost_per_module_M=40.0,
            plant_availability=0.85,
            thermal_efficiency=0.42,
            n_mod=10,
            electrode_replacement_cost_per_module_M=1.0,
            core_lifetime_FPY=5.0,
            interest_rate=0.06,
            construction_time_years=5.0,
        ),
        "Q=5 pessimistic": SFSZPinchParams(
            Q_sci=5.0,
            driver_cost_per_module_M=150.0,
            plant_availability=0.60,
            thermal_efficiency=0.33,
            n_mod=10,
        ),
        "Small plant (4 mod)": SFSZPinchParams(n_mod=4),
        "Large plant (20 mod)": SFSZPinchParams(n_mod=20),
    }

    print(f"\n  {'Scenario':<28} {'Q':>5} {'Net MWe':>8} {'OvernC $B':>9} {'$/kWe':>8} {'LCOE':>12}")
    print("  " + "-" * 74)
    for name, p in scenarios.items():
        r   = p.compute()
        net = r["power"]["p_net_plant"]
        ovn = r["costs"]["overnight_capital"]
        spc = r["costs"]["specific_capital_USD_per_kWe"]
        lc  = r["economics"]["lcoe_cents_per_kWh"]
        if net <= 0:
            lcoe_str = "N/A (neg)"
            spc_str  = "N/A"
        else:
            lcoe_str = f"{lc:.1f} c/kWh"
            spc_str  = f"${spc:,.0f}"
        print(f"  {name:<28} {p.Q_sci:>5.1f} {net:>7.0f}  ${ovn/1e3:>6.1f}B"
              f" {spc_str:>8}  {lcoe_str:>12}")

    # ==================================================================
    # 4. KEY BINDING CONSTRAINTS
    # ==================================================================
    print("\n\n" + "=" * 72)
    print("KEY BINDING CONSTRAINTS (top 3 LCOE drivers)")
    print("=" * 72)

    print("""
  1. Q_SCI NOT DEMONSTRATED — single most critical constraint
     Every LCOE number in this model is conditional on achieving Q >= 10.
     Commercial power balance anchors entirely on a calculated projection
     (Engineering Paradigms paper). FuZE demonstrated thermonuclear neutrons,
     but Q has never been measured at any scale. Commercial requires 200 us
     pinch lifetime; FuZE achieves 20-40 us (5-10x extrapolation required).
     Q_sci sensitivity: at Q=5 vs Q=10, net electric drops ~60% and LCOE roughly
     triples. At Q=5, recirculating fraction exceeds 70% and net output is marginal.

  2. PULSED POWER DRIVER COST AND SUPPLY CHAIN — program-level risk
     The driver is the single dominant capital cost item (~50-60% of overnight
     capital in baseline), replacing HTS magnets in tokamak economics. No commercial
     cost estimate exists anywhere in public literature.
     - Capacitors: 10^4-10^5 shot life vs. 10^8-10^9 required (4-6 OOM gap)
     - Switches: SiC at 6.5-15 kV vs. 50-200 kV needed (different technology class)
     - OSTI 2025: 10-20 year maturation roadmap before commercial deployment credible
     Driver cost sensitivity: $25M vs $350M/module spans 2x LCOE range.

  3. PLANT AVAILABILITY AND ELECTRODE DURABILITY — key unknown
     No erosion rate data for electrodes under nuclear duty cycle (14 MeV neutrons,
     10 Hz, 1 MA arcing). Replacement interval governs both O&M cost and capacity
     factor (LCOE denominator). Availability 0.60->0.85 changes LCOE by ~25%.
     Combined with electrode consumable cost uncertainty ($0.5M-$20M/mod/yr),
     this is the dominant O&M uncertainty source.
""")

    print("  NOTE: All estimates carry HIGH UNCERTAINTY. This model is for")
    print("  first-pass corridor mapping only. See parameter docstrings for sources.")
    print("  Cost accounts follow CAS structure (1costingfe) with power-scaling laws.")
    print()

    _p = results["power"]["p_net_plant"]
    print(f"  Native plant:   {_p:.0f} MWe -> LCOE {results['economics']['lcoe_USD_per_MWh']:.1f} $/MWh")
    print(f"  Scaled 1000 MWe (alpha=0.6):  "
          f"LCOE {scaled_headline['lcoe_per_mwh']:.1f} $/MWh,  "
          f"${scaled_headline['overnight_per_kw']:,.0f}/kW overnight")


if __name__ == "__main__":
    main()
