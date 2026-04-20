"""
Polywell (D-T) First-Pass LCOE Model
======================================
1cFE First Pass Concept Analysis
Concept: Polywell (D-T) — Electrostatic/Magnetic Cusp Confinement
Company: EMC2 (Energy Matter Conversion Corporation)

The Polywell is a magnetic cusp device that traps electrons electrostatically
to form a virtual cathode (Wiffleball), then uses the resulting electrostatic
well to confine and accelerate D-T ions to fusion temperatures. The reactor
design is based on the Park et al. 2025 preprint (arXiv:2508.06761), which
is the only publicly available reactor-scale physics scaling study.

CRITICAL UNCERTAINTIES (see analysis.md §Section 2):
1. Loss reduction factor γ=0.1 is a free parameter with no experimental validation.
   The entire Q=10.5 projection depends on this single unvalidated assumption.
   γ=0.2 halves Q to ~6.3; γ=0.4 likely makes net energy marginal.
2. No energy conversion architecture exists — thermal cycle, blanket coolant,
   and BOP are all unspecified. Thermal efficiency is modeled by analogy to MFE D-T.
3. Tritium breeding blanket faces geometry-specific challenge from coil neutron
   shadowing. No TBR calculation or blanket design exists.
4. All capital cost estimates are analogues from MFE/IFE concepts — no Polywell
   plant engineering study or cost breakdown has been published.

Cost accounting follows the CAS (Code of Accounts System) structure from 1costingfe.
Scaling laws adopt 1costingfe costing_constants.yaml reference values and exponents.
Concept-specific overrides (coil system, electron beam injection) are documented.

Power scaling for cross-concept comparison: economy-of-scale exponent α=0.6
applied to scaled_headline for 1000 MWe reference.
LCOE_1000 = LCOE_native × (P_native/1000)^(1-α)
OCC_1000  = OCC_native  × (P_native/1000)^(1-α)

Key references:
- Park et al., "Polywell Revisited," arXiv:2508.06761 (2025) — reactor scaling
- Park et al., Phys. Rev. X 5, 021024 (2015) — WB-X experimental results
- analysis.md §Section 5 — LCOE-relevant parameters and confidence ratings
- 1costingfe costing_constants.yaml — CAS scaling laws and unit costs

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass


# === Reference power levels for 1costingfe scaling laws ===
P_TH_REF = 2500.0   # Reference thermal power [MW]
P_ET_REF = 1100.0   # Reference gross electric power [MW]

# === Park 2025 γ reference values for coupled scaling relation ===
# p_beam ∝ γ (higher losses require more beam), p_fus ∝ 1/γ (lower confinement reduces fusion yield).
# Used by gamma_coupled_sweep() to ensure both quantities update together.
GAMMA_REF = 0.1      # Reference loss reduction factor (Park 2025 design point)
P_BEAM_REF = 78.0    # Reference beam power at γ=GAMMA_REF [MW]
P_FUS_REF = 980.0    # Reference fusion power at γ=GAMMA_REF [MW]


@dataclass
class PolywellPlantParams:
    """
    Parameterized Polywell (D-T) power plant model.

    Parameter values derive from Park et al. arXiv:2508.06761 and analysis.md §5.
    Where concept-specific data is absent, analogues from MFE D-T are used
    (marked ASSUMED or ANALOGUE). Uncertainty levels:
      (no tag)              = sourced value with reasonable confidence
      MODERATE UNCERTAINTY  = reasonable analogue, plausible range ±50%
      HIGH UNCERTAINTY      = speculative, range could be ×2–5
    """

    # =========================================================================
    # PHYSICS / PLASMA PARAMETERS
    # =========================================================================

    p_fus_MW: float = 980.0
    """Fusion power [MW] at loss reduction factor γ=0.1.
    Source: Park et al. arXiv:2508.06761 §Scaling for Net Energy.
    Note: Park 2025 reports Q_plasma~10.5 with 78 MW beam → implies ~819 MW;
    the 980 MW figure is the stated result for the reference design point.
    The discrepancy may reflect different Q accounting conventions.
    HIGH UNCERTAINTY — entire projection depends on unvalidated γ=0.1.
    Sensitivity: γ=0.2 → Q~6.3, p_fus~490 MW; γ=0.05 → Q~21, p_fus~1960 MW."""

    p_beam_MW: float = 78.0
    """Total electron beam injection power [MW].
    Source: Park et al. arXiv:2508.06761 §Scaling for Net Energy: 60 keV × 1.3 kA.
    Sensitivity: γ=0.2 → 156 MW required for same fusion power.
    HIGH UNCERTAINTY — scales inversely with γ."""

    beam_supply_efficiency: float = 0.85
    """Wall-plug efficiency of electron beam power supplies [fraction].
    Source: Industrial electron beam systems (Leybold, Sciaky) achieve 80–90%
    efficiency at MW scale for materials processing.
    Ref: analysis.md §Section 5 Note on beam power supply efficiency.
    MODERATE UNCERTAINTY — integration at 78 MW total not demonstrated."""

    blanket_energy_multiplication: float = 1.10
    """Blanket energy multiplication factor M (D-T Li neutron multiplication).
    Source: Standard for D-T with Li-containing blanket. Li-6 + n → T + α
    releases 4.78 MeV exothermic, adding ~10% to 14.1 MeV neutron energy.
    Ref: 1costingfe standard D-T assumption.
    MODERATE UNCERTAINTY — depends on undesigned blanket geometry."""

    thermal_efficiency: float = 0.40
    """Thermal-to-electric conversion efficiency [fraction].
    Source: ANALOGUE from MFE D-T concepts using steam Rankine cycle.
    Ref: analysis.md §Section 7 placeholder analogues: 40% Rankine baseline.
    No thermal cycle has been specified for the Polywell.
    HIGH UNCERTAINTY — energy conversion architecture completely unspecified."""

    # =========================================================================
    # GEOMETRY PARAMETERS
    # =========================================================================

    blanket_inner_radius_m: float = 1.0
    """Inner radius of blanket shell (from device center) [m].
    Source: Park et al. 1.6 m cube side → 0.8 m half-side + ~0.2 m coil thickness.
    Ref: arXiv:2508.06761 §Scaling for Net Energy: "1.6 m cube."
    MODERATE UNCERTAINTY — depends on coil and structural design."""

    blanket_thickness_m: float = 0.8
    """Blanket + first wall thickness [m].
    Source: ASSUMED thicker than standard MFE (~0.6 m) to compensate for
    coil neutron shadowing in polyhedral geometry.
    Ref: analysis.md §Section 2 Point 4: "innovative breeding solutions to
    address neutron shadowing caused by internal coil structures."
    HIGH UNCERTAINTY — no neutronics study exists for this geometry."""

    shield_thickness_m: float = 0.5
    """Biological shield thickness [m]. HT + LT + bioshield.
    Source: ANALOGUE from MFE concepts.
    MODERATE UNCERTAINTY."""

    structure_thickness_m: float = 0.3
    """Primary structure thickness [m].
    Source: ANALOGUE from IFE/MIF chamber structure.
    MODERATE UNCERTAINTY."""

    vessel_thickness_m: float = 0.1
    """Vacuum vessel wall thickness [m].
    Source: Standard engineering estimate for ~2 m diameter vessel.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # CAS22 CONCEPT-SPECIFIC COST OVERRIDES
    # =========================================================================

    coil_system_cost_M_USD: float = 150.0
    """Capital cost of 6-coil SC magnet system [M$]. Maps to CAS22 C220103.
    Source: ASSUMED. 6 independent SC coil assemblies at 4.5 T boundary field.
    Analogue: compact HTS coils for small devices; scaled from SPARC-class
    tokamak coil costs (~$100–300M for full TF coil set) adjusted downward
    for smaller coil scale (80 cm) and 6-sided geometry.
    Note: WB-series used resistive copper; SC design unspecified by EMC2.
    Ref: analysis.md §Section 3 SC Coil subsystem, §Section 4 Coil Conductors.
    HIGH UNCERTAINTY — no SC Polywell coil design has been published."""

    ebeam_system_cost_M_USD: float = 100.0
    """Capital cost of electron beam injection system [M$]. Maps to CAS22 C220104.
    Source: ASSUMED. 78 MW total injection (multiple MW-class commercial beams
    at 60 keV, 1.3 kA each). Commercial e-beam systems ~$5–15M per unit at
    hundreds of kW; 10–20 beams at ~4–8 MW each plus integration engineering.
    Ref: analysis.md §Section 3 Electron Beam: "commercial-grade MW-class
    electron beam injectors are available."
    HIGH UNCERTAINTY — 78 MW total into magnetic cusp not demonstrated."""

    blanket_cost_override_M_USD: float = 75.0
    """Capital cost of first wall + blanket system [M$]. Maps to CAS22 C220101.
    Source: CONCEPT-SPECIFIC OVERRIDE. The standard analogue formula
    (0.60 M$/m³ × volume) yields ~$7.3M but is derived from toroidal MFE geometry
    and is inapplicable to the 6-faced polyhedral cusp. The polyhedral geometry
    creates neutron-shadowing with no proposed engineering solution (TRL 1).
    ARIES-class D-T studies estimate blanket costs at $50–150M for comparable
    neutron power levels; $75M is a conservative ARIES lower-bound analogue.
    Ref: analysis.md §Section 3 TRL 1; §Section 6 gap #5 (blocking).
    Range: $50–200M. Actual cost requires an unperformed neutronics study.
    HIGH UNCERTAINTY — no blanket design exists for polyhedral cusp geometry."""

    # =========================================================================
    # PLANT CONFIGURATION
    # =========================================================================

    n_mod: int = 1
    """Number of fusion reactor modules per plant.
    Source: ASSUMED. Park 2025 design is a single module (~300 MWe net).
    Multiple modules would share BOP (turbine, cooling towers, grid connection).
    Ref: analysis.md §Section 7 discusses modular assembly advantage.
    MODERATE UNCERTAINTY."""

    plant_availability: float = 0.80
    """Plant capacity factor / availability [fraction].
    Source: ANALOGUE from MFE D-T aspirational targets.
    Ref: analysis.md §Section 7 placeholder: 80% capacity factor.
    No maintenance strategy or unplanned outage model exists for Polywell.
    HIGH UNCERTAINTY."""

    plant_lifetime_years: float = 40.0
    """Plant economic lifetime [years].
    Source: ANALOGUE — standard nuclear plant economic lifetime assumption."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds 10% contingency (CAS29) and higher pre-construction costs.
    Ref: 1costingfe CAS29 convention."""

    # =========================================================================
    # AUXILIARY / RECIRCULATING POWER
    # =========================================================================

    p_cryo_MW: float = 15.0
    """Cryogenic system power for SC coils [MW].
    Source: ASSUMED. 4.5 T SC coil system with 6 independent coil assemblies.
    Analogue: SPARC-class SC systems ~10–20 MW cryogenic load.
    MODERATE UNCERTAINTY — depends on SC coil design and operating temperature."""

    p_house_MW: float = 4.0
    """Housekeeping power [MW].
    Source: ANALOGUE. Standard fusion plant auxiliary loads.
    Ref: 1costingfe ife_zpinch.yaml default."""

    p_trit_MW: float = 10.0
    """Tritium processing power [MW].
    Source: ANALOGUE from MFE D-T tritium handling systems.
    Ref: 1costingfe default for D-T fuel cycle.
    MODERATE UNCERTAINTY."""

    p_vac_MW: float = 2.0
    """Vacuum pumping power [MW].
    Source: ANALOGUE. D-T-compatible turbomolecular + cryogenic pumping.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # FINANCIAL PARAMETERS
    # =========================================================================

    interest_rate: float = 0.08
    """Real discount rate / weighted average cost of capital [fraction].
    Source: 1costingfe default. Standard utility-scale nuclear project WACC."""

    inflation_rate: float = 0.02
    """Inflation rate for levelized cost calculations [fraction].
    Ref: 1costingfe default."""

    construction_time_years: float = 6.0
    """Construction period [years].
    Source: ANALOGUE. 1costingfe reference_construction_time.
    MODERATE UNCERTAINTY — compact device may reduce construction time."""

    # =========================================================================
    # OPERATING COSTS
    # =========================================================================

    core_lifetime_FPY: float = 5.0
    """Blanket / first-wall lifetime before replacement [full-power-years].
    Source: 1costingfe core_lifetime_dt = 5.0 FPY.
    Standard D-T assumption at 14.1 MeV neutron flux.
    Ref: analysis.md §Section 3 — no PFC lifetime published for Polywell.
    MODERATE UNCERTAINTY."""

    om_cost_scaling: float = 52.0
    """O&M cost coefficient [M$/yr at 1 GWe net, D-T].
    Source: 1costingfe CAS70 staffing-based build-up, om_cost_dt = 52.0.
    Scales as (P_net_plant / 1000)^0.5.
    MODERATE UNCERTAINTY — no Polywell staffing or operational model exists."""

    # =========================================================================
    # FUEL PARAMETERS
    # =========================================================================

    deuterium_cost_per_kg: float = 2175.0
    """Deuterium unit cost [$/kg].
    Source: 1costingfe costing_constants.yaml u_deuterium.
    Ref: STARFIRE (1980) inflation-adjusted."""

    fuel_burnup_fraction: float = 0.05
    """Fraction of injected fuel that undergoes fusion per pass [fraction].
    Source: 1costingfe costing_constants.yaml burn_fraction.
    Unburned fuel recycled at 95% efficiency (standard D-T assumption)."""

    # =========================================================================
    # COMPUTATION METHODS
    # =========================================================================

    def _compute_power(self) -> dict:
        """Layer 1: Steady-state power balance for Polywell (D-T).

        Energy flow: electron beam → plasma potential well → D-T fusion
        → neutrons (80%) + alphas (20%) → blanket → thermal cycle → net electric.
        Key recirculating load: wall-plug power for 78 MW e-beam injection.
        """
        r = {}

        # Scientific gain (plasma Q)
        # Note: Park 2025 reports Q~10.5; our computed value (p_fus/p_beam) differs
        # slightly due to ambiguity in the published Q definition.
        r["Q_sci"] = self.p_fus_MW / self.p_beam_MW if self.p_beam_MW > 0 else 0.0

        r["p_fus"] = self.p_fus_MW

        # D-T energy partition: 80% to 14.1 MeV neutrons, 20% to 3.52 MeV alphas
        f_neutron = 0.80
        f_alpha = 0.20
        r["p_neutron"] = f_neutron * self.p_fus_MW
        r["p_alpha"] = f_alpha * self.p_fus_MW

        # Thermal power: blanket captures neutrons (with exothermic multiplication)
        # plus alpha energy thermalized in plasma → blanket
        r["p_th"] = (self.blanket_energy_multiplication * r["p_neutron"]
                     + r["p_alpha"])

        # Gross electric
        r["p_et"] = self.thermal_efficiency * r["p_th"]

        # Recirculating power (wall-plug)
        # E-beam wall-plug: beam injection power divided by supply efficiency
        r["p_beam_wallplug"] = self.p_beam_MW / self.beam_supply_efficiency
        r["p_aux"] = self.p_cryo_MW + self.p_house_MW + self.p_trit_MW + self.p_vac_MW
        r["p_recirc"] = r["p_beam_wallplug"] + r["p_aux"]

        # Net electric per module
        r["p_net"] = r["p_et"] - r["p_recirc"]

        # Engineering Q: fusion power / all recirculating (wall-plug) power
        r["Q_eng"] = (self.p_fus_MW / r["p_recirc"]
                      if r["p_recirc"] > 0 else float("inf"))

        r["recirc_fraction"] = r["p_recirc"] / r["p_et"] if r["p_et"] > 0 else float("inf")

        # Plant-wide totals for multi-module configuration
        r["p_net_plant"] = r["p_net"] * self.n_mod
        r["p_et_plant"] = r["p_et"] * self.n_mod
        r["p_th_plant"] = r["p_th"] * self.n_mod

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Spherical shell geometry approximation for Polywell blanket system.

        The actual device is a 1.6 m cube with coils on each face.
        We approximate the surrounding blanket/shield system as concentric spherical
        shells — conservative (overestimates volume slightly vs. cubic geometry).
        The blanket is thicker than standard MFE to compensate for coil neutron
        shadowing (analysis.md §Section 2 Point 4).
        """
        r = {}

        def sphere_shell_vol(r_in: float, thickness: float) -> float:
            r_out = r_in + thickness
            return (4.0 / 3.0) * math.pi * (r_out**3 - r_in**3)

        ri = self.blanket_inner_radius_m
        r["blanket_vol_m3"] = sphere_shell_vol(ri, self.blanket_thickness_m)

        r_blanket_out = ri + self.blanket_thickness_m
        r["shield_vol_m3"] = sphere_shell_vol(r_blanket_out, self.shield_thickness_m)

        r_shield_out = r_blanket_out + self.shield_thickness_m
        r["structure_vol_m3"] = sphere_shell_vol(r_shield_out, self.structure_thickness_m)

        r_structure_out = r_shield_out + self.structure_thickness_m
        r["vessel_vol_m3"] = sphere_shell_vol(r_structure_out, self.vessel_thickness_m)

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts.

        Follows 1costingfe cas22.py structure adapted for Polywell steady-state MIF/EC.
        C220103 (coils) and C220104 (e-beam injection) are concept-specific overrides.
        Scaling law exponents from 1costingfe costing_constants.yaml.
        """
        r = {}
        p_th = max(power["p_th"], 1.0)
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)
        p_th_plant = max(power["p_th_plant"], 1.0)
        p_net_plant = max(power["p_net_plant"], 1.0)

        # --- Per-module accounts ---

        # C220101: First Wall + Blanket — OVERRIDE (HIGH UNCERT)
        # Standard analogue formula (0.60 M$/m³ × volume) yields ~$7.3M but is
        # derived from toroidal MFE geometry and is inapplicable to the 6-faced
        # polyhedral cusp. The geometry creates a neutron-shadowing problem with
        # no proposed engineering solution (analysis.md §Section 3 TRL 1; §Section 6
        # gap #5: blocking). ARIES-class D-T studies estimate $50–150M at comparable
        # neutron power. This override uses $75M as a conservative analogue lower bound.
        # NOTE: actual cost requires a neutronics study that has not been performed.
        # Ref: blanket_cost_override_M_USD docstring.
        r["C220101"] = self.blanket_cost_override_M_USD  # [override, HIGH UNCERT]

        # C220102: Shield (HT + LT + Bioshield)
        # Formula: shield_unit_cost × volume × (p_th / P_TH_REF)^0.6
        # Ref: 1costingfe costing_constants.yaml shield_unit_cost = 0.74 M$/m³
        r["C220102"] = (0.74
                        * geom["shield_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: Coil System — OVERRIDE
        # Polywell has 6 independent SC coil assemblies (non-interlocking cube geometry).
        # Standard formula scales by kAm; we override with a direct cost estimate
        # because the polyhedral geometry has no precedent in published literature.
        # Ref: analysis.md §Section 3 SC Coil subsystem; coil_system_cost_M_USD docstring.
        r["C220103"] = self.coil_system_cost_M_USD  # [override]

        # C220104: Supplementary Heating → Electron Beam Injection System — OVERRIDE
        # In MFE, this is NBI/ECRH. In Polywell, energy injection is via e-beam.
        # Standard formula: 80 × (p_et/1000)^0.7 for heating systems.
        # Override: direct e-beam system cost from commercial e-beam analogue.
        # Ref: analysis.md §Section 3 Electron Beam; ebeam_system_cost_M_USD docstring.
        r["C220104"] = self.ebeam_system_cost_M_USD  # [override]

        # C220105: Primary Structure
        # Formula: structure_unit_cost × volume × (p_et / P_ET_REF)^0.5
        # Ref: 1costingfe costing_constants.yaml structure_unit_cost = 0.15 M$/m³
        r["C220105"] = (0.15
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: Vacuum System (vessel + turbo + cryo pumps)
        # Formula: vessel_unit_cost × volume × (p_et / P_ET_REF)^0.6
        # Ref: 1costingfe costing_constants.yaml vessel_unit_cost = 0.72 M$/m³
        r["C220106"] = (0.72
                        * geom["vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # C220107: Power Supplies (general plant electrical, not e-beam)
        # Formula: 80.0 × (p_et / 1000)^0.7
        # Ref: 1costingfe costing_constants.yaml power_supplies_base = 80.0 M$/GWe
        # Note: e-beam power supplies included in C220104; this covers grid interface,
        #       auxiliary power conditioning, cryogenic power supplies, etc.
        r["C220107"] = 80.0 * (p_et / 1000.0) ** 0.7

        # C220108: Target Factory / Pellet Injector — not applicable
        # Polywell is steady-state; no fuel pellets or IFE targets required.
        # D-T gas fueling handled in C220500 (Fuel Handling).
        r["C220108"] = 0.0

        # C220109: Direct Energy Converter — not applicable
        # Standard Rankine thermal cycle assumed; no direct conversion.
        r["C220109"] = 0.0

        # C220110: Remote Handling & Maintenance Equipment
        # Standard D-T formula: 150 × (p_net/1000)^0.7 (1costingfe remote_handling_dt_base)
        # Polywell scale factor 0.4: Park 2025 claims "easily assembled and disassembled
        # in a modular manner" due to non-interlocking coils. Lighter RH suite assumed.
        # Ref: analysis.md §Section 7: "modular coil advantage claimed."
        # MODERATE UNCERTAINTY — modular advantage is a design claim, not demonstrated.
        r["C220110"] = 150.0 * 0.4 * (p_net / 1000.0) ** 0.7  # [partial override]

        # C220111: Installation Labor
        # Formula: 0.14 × reactor subtotal
        # Ref: 1costingfe costing_constants.yaml installation_frac = 0.14
        reactor_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"])
        r["C220111"] = 0.14 * reactor_subtotal

        # C220112: Isotope Separation — 0 (handled in CAS80 fuel costs)
        r["C220112"] = 0.0

        # Per-module subtotal
        r["CAS22_per_module"] = reactor_subtotal + r["C220111"] + r["C220112"]

        # --- Plant-wide accounts ---

        # C220200: Main & Secondary Coolant Systems
        # Ref: 1costingfe cas22.py C220200 formula
        C220201 = 166.0 * (p_net_plant / 1000.0)            # Primary coolant loop
        C220202 = 40.6 * (p_th_plant / 3500.0) ** 0.55      # Intermediate loop
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling + Cryoplant
        C220301 = 1.1e-3 * p_th_plant                                          # Aux coolant
        C220302 = 200.0 * (max(self.p_cryo_MW * self.n_mod, 0.01) / 30.0) ** 0.7  # Cryoplant
        r["C220300"] = C220301 + C220302

        # C220400: Radioactive Waste Management
        # Ref: 1costingfe formula
        r["C220400"] = 1.96 * (p_th_plant / 1000.0)

        # C220500: Fuel Handling & Storage (D-T tritium cycle)
        # Ref: 1costingfe costing_constants.yaml fuel_handling_dt_base = 120 M$ at 1 GWe
        r["C220500"] = 120.0 * (p_net_plant / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        r["C220600"] = 11.5 * (p_net_plant / 1000.0) ** 0.8

        # C220700: Instrumentation & Control
        # Ref: 1costingfe formula
        r["C220700"] = 85.0 * (p_th_plant / 3500.0) ** 0.65

        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        # Total CAS22 (per-module × n_mod + plant-wide)
        r["CAS22"] = r["CAS22_per_module"] * self.n_mod + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: CAS10–60 capital costs following 1costingfe structure."""
        r = {}
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)
        p_net_plant = max(power["p_net_plant"], 1.0)

        # === CAS10: Pre-construction ===
        site_permits = 3.0
        plant_studies = 4.0 if self.noak else 20.0
        plant_permits = 2.0
        plant_reports = 1.0
        other_precon = 1.0
        land_cost = 0.25 * p_net_plant * math.sqrt(self.n_mod) * 10_000 / 1e6
        # D-T licensing includes NRC Part 30 + fusion-specific review, ~2 years
        # Ref: 1costingfe costing_constants.yaml licensing_cost_dt = 5.0 M$
        licensing_cost = 5.0 if not self.noak else 2.5
        r["CAS10"] = (site_permits + plant_studies + plant_permits + plant_reports
                      + other_precon + land_cost + licensing_cost)

        # === CAS21: Buildings ===
        # D-T building cost: 502 $/kWe at 1 GWe gross reference (1costingfe CAS21 total D-T)
        # Scaled by gross electric power (P_et): turbine hall, reactor building, hot cell
        # all scale with plant thermal/electric output, not device size.
        # Ref: 1costingfe costing_constants.yaml building_costs, comment "DT=$502/kW"
        building_cost_per_kW_dt = 502.0  # $/kWe (D-T total, includes hot cell, tritium)
        r["CAS21"] = building_cost_per_kW_dt * p_et * self.n_mod / 1000.0  # M$

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment ===
        # Ref: 1costingfe CAS23-26, turbine_per_mw = 0.19764 M$/MW
        r["CAS23"] = self.n_mod * p_et * 0.19764

        # === CAS24: Electric Plant Equipment ===
        # Ref: 1costingfe costing_constants.yaml electric_per_mw = 0.08418 M$/MW
        r["CAS24"] = self.n_mod * p_et * 0.08418

        # === CAS25: Miscellaneous Plant Equipment ===
        # Ref: 1costingfe costing_constants.yaml misc_per_mw = 0.05124 M$/MW
        r["CAS25"] = self.n_mod * p_et * 0.05124

        # === CAS26: Heat Rejection ===
        # Ref: 1costingfe CAS26 heat_rej_per_mw = 0.03416 M$/MW
        r["CAS26"] = self.n_mod * p_et * 0.03416

        # === CAS27: Special Materials (enriched Li-6 for D-T breeding blanket) ===
        # Ref: 1costingfe costing_constants.yaml special_materials_dt = 15 M$ at 1 GWe
        # Polywell may need more Li-6 enrichment due to coil neutron shadowing
        r["CAS27"] = 15.0 * (p_net_plant / 1000.0)

        # === CAS28: Digital Twin ===
        # Ref: 1costingfe costing_constants.yaml digital_twin = 5.0 M$
        r["CAS28"] = 5.0

        # === CAS29: Contingency ===
        cas20_subtotal = sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                             "CAS25", "CAS26", "CAS27", "CAS28"])
        contingency_rate = 0.10 if not self.noak else 0.0
        r["CAS29"] = contingency_rate * cas20_subtotal

        # === CAS20: Total Direct Costs ===
        r["CAS20"] = cas20_subtotal + r["CAS29"]

        # === CAS30: Indirect Costs ===
        # Ref: 1costingfe indirect_fraction = 0.20, reference_construction_time = 6 years
        ref_construction_time = 6.0
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / ref_construction_time)

        # === CAS40: Capitalized Owner's Costs ===
        # Ref: 1costingfe owner_cost_dt = 39.0 M$ at 1 GWe, scaled by (P_net/1000)^0.5
        r["CAS40"] = 39.0 * (p_net_plant / 1000.0) ** 0.5

        # === CAS50: Capitalized Supplementary Costs ===
        # Ref: 1costingfe CAS50 sub-account model
        shipping = 0.015 * r["CAS20"]
        spare_parts = 0.03 * (r["CAS22"] + r["CAS23"] + r["CAS24"] +
                               r["CAS25"] + r["CAS26"] + r["CAS27"] + r["CAS28"])
        taxes = 0.01 * r["CAS20"]
        construction_insurance = 0.015 * (r["CAS20"] + r["CAS30"])
        # Tritium startup inventory: ~40 M$ at 1 GWe (scaled to plant size)
        # Ref: 1costingfe startup_fuel_dt = 40.0 M$ at 1 GWe
        startup_tritium = 40.0 * (p_net_plant / 1000.0)
        # Decommissioning provision: PV of future decommissioning costs
        # Ref: 1costingfe decom_provision_dt = 127 M$ at 1 GWe
        decommissioning = 127.0 * (p_net_plant / 1000.0)
        r["CAS50"] = (shipping + spare_parts + taxes + construction_insurance
                      + startup_tritium + decommissioning)

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

        # Specific capital cost ($/kWe)
        if power["p_net_plant"] > 0:
            r["specific_capital_USD_per_kWe"] = (r["total_capital"] * 1e6
                                                  / (power["p_net_plant"] * 1e3))
        else:
            r["specific_capital_USD_per_kWe"] = float("inf")

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70–90 annualized costs and LCOE."""
        r = {}
        p_net_plant = max(power["p_net_plant"], 1.0)

        # Capital Recovery Factor
        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1 + i) ** n / ((1 + i) ** n - 1)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]  # M$/year

        # === CAS71: Annual O&M (levelized) ===
        # Base rate: 52 M$/yr at 1 GWe, scaled by (P_net/1000)^0.5
        # Ref: 1costingfe om_cost_dt = 52.0
        annual_om_base = self.om_cost_scaling * (p_net_plant / 1000.0) ** 0.5
        g = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g) ** Tc
        if abs(i - g) > 1e-10:
            pv_growing_annuity = A1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
        else:
            pv_growing_annuity = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_growing_annuity  # M$/year

        # === CAS72: Annualized Scheduled Replacement (blanket/FW) ===
        effective_years_per_replacement = self.core_lifetime_FPY / self.plant_availability
        n_replacements = max(0, int(
            math.ceil(self.plant_lifetime_years / effective_years_per_replacement)) - 1)
        # Replacement cost = C220101 cost × n_mod
        replacement_cost = cas22["C220101"] * self.n_mod
        pv_replacements = 0.0
        for k in range(1, n_replacements + 1):
            year = k * effective_years_per_replacement
            if year < self.plant_lifetime_years:
                pv_replacements += replacement_cost / (1 + i) ** year
        r["CAS72"] = crf * pv_replacements  # M$/year
        r["n_blanket_replacements"] = n_replacements

        r["CAS70"] = r["CAS71"] + r["CAS72"]  # M$/year

        # === CAS80: Annual Fuel Costs ===
        # Deuterium consumption: D + T → He-4 + n; D and T consumed equimolarly.
        # Fusion power [MW] → fusion rate [reactions/s]
        # Energy per reaction: 17.58 MeV = 2.817e-12 J
        eV_per_rxn = 17.58e6       # eV
        J_per_eV = 1.602e-19       # J/eV
        J_per_rxn = eV_per_rxn * J_per_eV
        rxn_per_s = power["p_fus"] * 1e6 / J_per_rxn  # reactions/s (per module)
        rxn_per_yr = rxn_per_s * 3600 * 8760 * self.plant_availability

        # Deuterium mass consumed per year (per module): 1 D per reaction, mass = 2 amu
        m_D_consumed_kg_yr = rxn_per_yr * 2 * 1.6605e-27 * self.n_mod
        # With recycling, injected mass >> consumed mass; cost on net consumed D
        annual_D_cost = m_D_consumed_kg_yr * self.deuterium_cost_per_kg / 1e6  # M$
        # Tritium is self-bred in blanket — no ongoing purchase (startup in CAS50)
        # NOTE: assumes breeding blanket works; if TBR < 1, external T purchase adds ~$30M/yr
        r["CAS80"] = annual_D_cost  # M$/year (tritium breeding assumed adequate)
        r["CAS80_deuterium"] = annual_D_cost
        r["m_D_consumed_kg_yr"] = m_D_consumed_kg_yr

        # === LCOE ===
        annual_revenue_req = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_revenue_req

        annual_energy_MWh = 8760 * p_net_plant * self.plant_availability
        r["annual_energy_MWh"] = annual_energy_MWh

        if annual_energy_MWh > 0:
            lcoe = annual_revenue_req * 1e6 / annual_energy_MWh
            r["lcoe_USD_per_MWh"] = lcoe
            r["lcoe_cents_per_kWh"] = lcoe / 10.0
        else:
            r["lcoe_USD_per_MWh"] = float("inf")
            r["lcoe_cents_per_kWh"] = float("inf")

        if annual_revenue_req > 0:
            r["capital_fraction"] = r["CAS90"] / annual_revenue_req
            r["om_fraction"] = r["CAS70"] / annual_revenue_req
            r["fuel_fraction"] = r["CAS80"] / annual_revenue_req

        return r

    def compute(self) -> dict:
        """Compute LCOE using CAS-structured accounting. Returns full results dict."""
        power = self._compute_power()
        geom = self._compute_geometry(power)
        cas22 = self._compute_cas22(power, geom)
        costs = self._compute_costs(power, cas22)
        econ = self._compute_economics(power, costs, cas22)

        return {
            "power": power,
            "geometry": geom,
            "cas22": cas22,
            "costs": costs,
            "economics": econ,
        }


# =============================================================================
# MODULE-LEVEL EXPOSURE (required for concept explorer)
# =============================================================================

params = PolywellPlantParams()
results = params.compute()

# Cross-concept comparison at normalized 1000 MWe reference
# Economy-of-scale exponent α=0.6: LCOE scales as (P_native/P_ref)^(1-α)
# Larger plants have lower LCOE per unit energy (scale economy).
# Ref: Standard cost scaling law for capital-intensive power plants.
_ALPHA = 0.6
_p_native = results["power"].get("p_net_plant", results["power"]["p_net"])
_factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)
_overnight = results["costs"]["overnight_capital"] * 1e3 / _p_native

scaled_headline = {
    "p_net_mw": 1000.0,
    "lcoe_per_mwh": results["economics"]["lcoe_USD_per_MWh"] * _factor,
    "overnight_per_kw": _overnight * _factor,
}


# =============================================================================
# PRINT / REPORTING FUNCTIONS
# =============================================================================

def print_results(p: PolywellPlantParams, res: dict):
    """Pretty-print Polywell LCOE results with CAS-structured accounting."""
    power = res["power"]
    cas22 = res["cas22"]
    costs = res["costs"]
    econ = res["economics"]

    print("=" * 70)
    print("Polywell (D-T) LCOE Model — 1cFE CAS-Structured")
    print("Company: EMC2 (Energy Matter Conversion Corporation)")
    print("=" * 70)

    print(f"\n--- Key Input Parameters ---")
    print(f"  Fusion power (p_fus):       {p.p_fus_MW:.0f} MW  [HIGH UNCERT]")
    print(f"  E-beam injection (p_beam):  {p.p_beam_MW:.0f} MW")
    print(f"  Beam supply efficiency:     {p.beam_supply_efficiency:.1%}")
    print(f"  Blanket multiplication:     {p.blanket_energy_multiplication:.2f}")
    print(f"  Thermal efficiency:         {p.thermal_efficiency:.1%}  [HIGH UNCERT]")
    print(f"  Plant availability:         {p.plant_availability:.1%}")
    print(f"  Modules:                    {p.n_mod}")
    print(f"  FOAK/NOAK:                  {'NOAK' if p.noak else 'FOAK'}")
    print(f"  Interest rate:              {p.interest_rate:.1%}")
    print(f"  Plant lifetime:             {p.plant_lifetime_years:.0f} years")
    print(f"  SC coil system:             ${p.coil_system_cost_M_USD:.0f}M  [HIGH UNCERT]")
    print(f"  E-beam system:              ${p.ebeam_system_cost_M_USD:.0f}M  [HIGH UNCERT]")
    print(f"  Blanket/FW (C220101):       ${p.blanket_cost_override_M_USD:.0f}M  [HIGH UNCERT — polyhedral geometry]")

    print(f"\n--- Power Balance ---")
    print(f"  Fusion power (p_fus):       {power['p_fus']:.0f} MW")
    print(f"    Neutron power (80%):      {power['p_neutron']:.0f} MW (14.1 MeV)")
    print(f"    Alpha power  (20%):       {power['p_alpha']:.0f} MW (3.52 MeV)")
    print(f"  Thermal power (p_th):       {power['p_th']:.0f} MW")
    print(f"  Gross electric (p_et):      {power['p_et']:.0f} MWe")
    print(f"  Recirculating power:")
    print(f"    E-beam wall-plug:         {power['p_beam_wallplug']:.1f} MW")
    print(f"    Cryogenic (SC coils):     {p.p_cryo_MW:.1f} MW")
    print(f"    Housekeeping:             {p.p_house_MW:.1f} MW")
    print(f"    Tritium processing:       {p.p_trit_MW:.1f} MW")
    print(f"    Vacuum pumping:           {p.p_vac_MW:.1f} MW")
    print(f"    Total recirculating:      {power['p_recirc']:.1f} MW")
    print(f"  Net electric (p_net):       {power['p_net']:.0f} MWe  (per module)")
    print(f"  Net electric (plant):       {power['p_net_plant']:.0f} MWe  ({p.n_mod} module(s))")
    print(f"  Q_sci = p_fus / p_beam:     {power['Q_sci']:.2f}")
    print(f"  Q_eng = p_fus / p_recirc:   {power['Q_eng']:.2f}")
    print(f"  Recirculating fraction:     {power['recirc_fraction']:.1%}")

    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    cas22_labels = {
        "C220101": "Blanket/First Wall",
        "C220102": "Shield",
        "C220103": "SC Coil System (6-faced)",
        "C220104": "E-Beam Injection System",
        "C220105": "Primary Structure",
        "C220106": "Vacuum System",
        "C220107": "Power Supplies (general)",
        "C220108": "Target Factory",
        "C220109": "Direct Energy Converter",
        "C220110": "Remote Handling",
        "C220111": "Installation Labor",
        "C220112": "Isotope Separation",
    }
    overrides = {"C220101", "C220103", "C220104"}
    print(f"  Per-module accounts:")
    for code, label in cas22_labels.items():
        val = cas22[code]
        tag = " [override]" if code in overrides else ""
        if val > 0.01:
            print(f"    {code} {label:<32s} ${val:>8.1f}M{tag}")
    print(f"  {'':>4s} {'─' * 49}")
    print(f"    Per-module subtotal:                  ${cas22['CAS22_per_module']:>8.1f}M × {p.n_mod}")
    print(f"  Plant-wide accounts:")
    pw_labels = {
        "C220200": "Coolant Systems",
        "C220300": "Aux Cooling + Cryoplant",
        "C220400": "Rad Waste Management",
        "C220500": "Fuel Handling (D-T)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    for code, label in pw_labels.items():
        val = cas22[code]
        if val > 0.01:
            print(f"    {code} {label:<32s} ${val:>8.1f}M")
    print(f"  {'':>4s} {'─' * 49}")
    print(f"    Plant-wide subtotal:                  ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                            ${cas22['CAS22']:>8.1f}M")

    print(f"\n--- Capital Costs (CAS10–60) ---")
    print(f"  CAS10 Pre-construction:                 ${costs['CAS10']:>8.1f}M")
    print(f"  CAS21 Buildings (D-T, 502 $/kWe):       ${costs['CAS21']:>8.1f}M")
    print(f"  CAS22 Reactor Plant Equipment:          ${costs['CAS22']:>8.1f}M")
    print(f"  CAS23 Turbine Plant:                    ${costs['CAS23']:>8.1f}M")
    print(f"  CAS24 Electric Plant:                   ${costs['CAS24']:>8.1f}M")
    print(f"  CAS25 Misc Plant:                       ${costs['CAS25']:>8.1f}M")
    print(f"  CAS26 Heat Rejection:                   ${costs['CAS26']:>8.1f}M")
    print(f"  CAS27 Special Materials (Li-6):         ${costs['CAS27']:>8.1f}M")
    print(f"  CAS28 Digital Twin:                     ${costs['CAS28']:>8.1f}M")
    print(f"  CAS29 Contingency:                      ${costs['CAS29']:>8.1f}M")
    print(f"  {'─' * 58}")
    print(f"  CAS20 Direct Costs:                     ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30 Indirect Costs:                   ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40 Owner's Costs:                    ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50 Supplementary (T-startup+decom):  ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 58}")
    print(f"  Overnight Capital:                      ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60 IDC (f={costs['f_IDC']:.3f}):               ${costs['CAS60']:>8.1f}M")
    print(f"  {'═' * 58}")
    print(f"  Total Capital:                          ${costs['total_capital']:>8.1f}M")
    print(f"  Specific Capital:                       ${costs['specific_capital_USD_per_kWe']:>8.0f} $/kWe")

    print(f"\n--- Annual Costs (CAS70–90) ---")
    print(f"  CAS90 Capital charge (CRF={econ['CRF']:.4f}):    ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71 O&M (levelized):                  ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72 Blanket replacement:              ${econ['CAS72']:>8.1f}M/yr"
          f"  ({econ['n_blanket_replacements']} replacements)")
    print(f"  CAS70 Total O&M:                        ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80 Fuel (D consumption):             ${econ['CAS80']:>8.3f}M/yr"
          f"  ({econ['m_D_consumed_kg_yr']:.1f} kg D/yr)")

    print(f"\n--- LCOE ---")
    print(f"  Annual net energy:          {econ['annual_energy_MWh']:,.0f} MWh/yr")
    print(f"  Annual revenue requirement: ${econ['annual_revenue_req']:.1f}M/yr")
    print(f"  ╔══════════════════════════════════════╗")
    print(f"  ║  LCOE = {econ['lcoe_cents_per_kWh']:.2f} ¢/kWh                 ║")
    print(f"  ║       = {econ['lcoe_USD_per_MWh']:.1f} $/MWh                 ║")
    print(f"  ╚══════════════════════════════════════╝")
    print(f"  Capital (CAS90):            {econ.get('capital_fraction', 0):.1%}")
    print(f"  O&M (CAS70):               {econ.get('om_fraction', 0):.1%}")
    print(f"  Fuel (CAS80):              {econ.get('fuel_fraction', 0):.1%}")


def sensitivity_sweep(base_params: PolywellPlantParams, param_name: str,
                      values: list, label: str = "") -> list:
    """Sweep a single parameter and return LCOE for each value."""
    results_list = []
    for val in values:
        p = PolywellPlantParams(**{**base_params.__dict__, param_name: val})
        r = p.compute()
        results_list.append({
            "param_value": float(val),
            "lcoe_cents_kWh": r["economics"]["lcoe_cents_per_kWh"],
            "net_electric_MW": r["power"]["p_net"],
            "overnight_M": r["costs"]["overnight_capital"],
        })
    return results_list


def gamma_coupled_sweep(base_params: PolywellPlantParams, gamma_values: list) -> list:
    """Coupled γ sweep: both p_fus and p_beam update together per Park 2025 scaling.

    Park 2025 relation:
      p_beam = P_BEAM_REF × (γ / GAMMA_REF)   [more losses → more injection required]
      p_fus  = P_FUS_REF  × (GAMMA_REF / γ)   [lower confinement → less fusion yield]

    This is the physically correct representation of a γ deviation. A plant designed
    for the reference point (γ=0.1, 980 MW fusion, 301 MWe net) that instead operates
    at γ=0.2 suffers BOTH a fusion yield reduction AND a beam cost increase simultaneously.
    Capital cost is fixed at the design-point plant size, so the underutilization penalty
    is reflected in the per-MWh energy cost. Compare to the p_fus_MW sweep (branch b
    only: fixed beam, p_fus varies), which underestimates the γ=0.2 penalty.
    """
    results_list = []
    for gamma in gamma_values:
        p_beam = P_BEAM_REF * (gamma / GAMMA_REF)
        p_fus = P_FUS_REF * (GAMMA_REF / gamma)
        p = PolywellPlantParams(**{
            **base_params.__dict__,
            "p_fus_MW": p_fus,
            "p_beam_MW": p_beam,
        })
        r = p.compute()
        results_list.append({
            "gamma": gamma,
            "p_fus_MW": p_fus,
            "p_beam_MW": p_beam,
            "Q_sci": r["power"]["Q_sci"],
            "lcoe_cents_kWh": r["economics"]["lcoe_cents_per_kWh"],
            "net_electric_MW": r["power"]["p_net"],
            "overnight_M": r["costs"]["overnight_capital"],
        })
    return results_list


def main():
    # =========================================================================
    # SCENARIO DEFINITIONS
    # =========================================================================

    # Conservative: γ=0.2, FOAK — physically coupled per Park 2025 scaling relation.
    # p_beam ∝ γ: at γ=0.2, beam doubles to 156 MW (more losses require more injection).
    # p_fus ∝ 1/γ: at γ=0.2, fusion power halves to 490 MW (lower confinement quality).
    # Q_sci = 490/156 ≈ 3.1 — this is the correct coupled representation of γ=0.2,
    # not branch (b) (fixed beam, p_fus only varies) which was used in prior iterations.
    conservative = PolywellPlantParams(
        p_fus_MW=490.0,             # γ=0.2, p_fus ∝ 1/γ (ref: 980 MW at γ=0.1)
        p_beam_MW=156.0,            # γ=0.2, p_beam ∝ γ (ref: 78 MW at γ=0.1)
        beam_supply_efficiency=0.82,
        thermal_efficiency=0.38,    # no thermal cycle spec → conservative
        coil_system_cost_M_USD=200.0,
        ebeam_system_cost_M_USD=130.0,
        plant_availability=0.70,
        interest_rate=0.10,
        noak=False,                 # FOAK
    )

    # Moderate: Park 2025 baseline (γ=0.1, Q≈12.6 as modeled)
    moderate = PolywellPlantParams()  # all defaults

    # Optimistic: Park 2025 physics holds + better BOP engineering
    optimistic = PolywellPlantParams(
        p_fus_MW=980.0,
        p_beam_MW=78.0,
        beam_supply_efficiency=0.90,
        thermal_efficiency=0.45,    # sCO2 cycle
        coil_system_cost_M_USD=100.0,
        ebeam_system_cost_M_USD=70.0,
        plant_availability=0.85,
        interest_rate=0.06,
        construction_time_years=5.0,
        noak=True,
    )

    # =========================================================================
    # BASELINE (MODERATE) SCENARIO
    # =========================================================================
    print("\n" + "#" * 70)
    print("# BASELINE SCENARIO: Polywell (D-T) — Park 2025 Design Point")
    print("#" * 70)
    baseline_results = moderate.compute()
    print_results(moderate, baseline_results)

    # =========================================================================
    # SENSITIVITY SWEEPS
    # =========================================================================
    print("\n" + "=" * 70)
    print("SENSITIVITY ANALYSIS — Single-Parameter Sweeps from Baseline")
    print("=" * 70)
    base_lcoe = baseline_results["economics"]["lcoe_cents_per_kWh"]
    base_net = baseline_results["power"]["p_net"]
    print(f"  Baseline LCOE:  {base_lcoe:.2f} ¢/kWh  |  Net electric: {base_net:.0f} MWe\n")

    sweeps = [
        ("p_fus_MW",
         [245, 490, 735, 980, 1225, 1470],
         "Fusion power [MW] — branch (b) proxy: fixed beam at 78 MW, confinement degrades"
         " (see coupled γ sweep below for physically correct representation)"),
        ("thermal_efficiency",
         [0.33, 0.37, 0.40, 0.43, 0.47, 0.50],
         "Thermal efficiency — unspecified BOP cycle"),
        ("beam_supply_efficiency",
         [0.75, 0.80, 0.85, 0.90, 0.95],
         "E-beam power supply efficiency"),
        ("coil_system_cost_M_USD",
         [75.0, 100.0, 150.0, 200.0, 300.0],
         "SC coil system cost [M$]"),
        ("ebeam_system_cost_M_USD",
         [50.0, 75.0, 100.0, 150.0, 200.0],
         "E-beam injection system cost [M$]"),
        ("plant_availability",
         [0.60, 0.70, 0.80, 0.85, 0.90],
         "Plant capacity factor / availability"),
        ("interest_rate",
         [0.06, 0.07, 0.08, 0.10, 0.12],
         "Real discount rate / WACC"),
        ("blanket_cost_override_M_USD",
         [50.0, 75.0, 100.0, 150.0, 200.0],
         "Blanket/First Wall cost [M$] — polyhedral cusp geometry, no neutronics study"
         " (standard analogue $7.3M inapplicable; ARIES range $50–150M)  [HIGH UNCERT]"),
    ]

    for param_name, values, label in sweeps:
        print(f"  {label}:")
        sweep_results = sensitivity_sweep(moderate, param_name, values)
        for sr in sweep_results:
            net = sr["net_electric_MW"]
            if net <= 0:
                print(f"    {sr['param_value']:>10.3g} → NET POWER NEGATIVE ({net:.0f} MWe)")
            else:
                delta = sr["lcoe_cents_kWh"] - base_lcoe
                marker = " ←" if abs(delta) > 0.5 else ""
                print(f"    {sr['param_value']:>10.3g} → {sr['lcoe_cents_kWh']:7.2f} ¢/kWh"
                      f"  (Δ{delta:+.2f})  net={net:.0f} MWe{marker}")
        print()

    # Coupled γ sweep — both p_fus and p_beam vary per Park 2025 scaling relation.
    # This is the physically correct γ sensitivity; compare to the p_fus_MW sweep above
    # (branch b only) which underestimates the γ=0.2 penalty.
    print(f"  Loss reduction factor γ — COUPLED sweep (p_beam ∝ γ, p_fus ∝ 1/γ):")
    print(f"    {'γ':>6}  {'p_fus':>8}  {'p_beam':>7}  {'Q_sci':>6}  {'LCOE':>11}  {'net':>8}")
    gamma_sweep_values = [0.05, 0.075, 0.10, 0.15, 0.20, 0.30, 0.40]
    gamma_results = gamma_coupled_sweep(moderate, gamma_sweep_values)
    for gr in gamma_results:
        net = gr["net_electric_MW"]
        marker = " ← ref" if abs(gr["gamma"] - GAMMA_REF) < 0.001 else ""
        if net <= 0:
            print(f"    {gr['gamma']:>6.3f}  {gr['p_fus_MW']:>8.0f}  {gr['p_beam_MW']:>7.0f}"
                  f"  {gr['Q_sci']:>6.2f}  {'NET NEG':>11}  {net:>7.0f} MWe{marker}")
        else:
            delta = gr["lcoe_cents_kWh"] - base_lcoe
            print(f"    {gr['gamma']:>6.3f}  {gr['p_fus_MW']:>8.0f}  {gr['p_beam_MW']:>7.0f}"
                  f"  {gr['Q_sci']:>6.2f}  {gr['lcoe_cents_kWh']:>9.2f} ¢/kWh"
                  f"  {net:>7.0f} MWe{marker}")
    print(f"  Note: γ=0.2 coupled gives Q_sci≈{490/156:.2f} vs Q_sci≈{490/78:.2f}"
          f" (branch b, fixed beam).")
    print(f"        Coupled scenario reflects both yield loss and beam cost increase.\n")

    # =========================================================================
    # SCENARIO COMPARISON TABLE
    # =========================================================================
    print("=" * 70)
    print("SCENARIO COMPARISON")
    print("=" * 70)
    scenarios = [
        ("Conservative (γ=0.2, FOAK)", conservative),
        ("Moderate / Baseline (γ=0.1)", moderate),
        ("Optimistic (γ=0.1, sCO2, NOAK)", optimistic),
    ]

    print(f"\n{'Scenario':<38} {'p_fus':>8} {'p_net':>8} {'OCC':>10} {'LCOE':>12}")
    print(f"{'':38} {'[MW]':>8} {'[MWe]':>8} {'[M$]':>10} {'[¢/kWh]':>12}")
    print("-" * 80)
    for name, p in scenarios:
        r = p.compute()
        p_fus = r["power"]["p_fus"]
        p_net = r["power"]["p_net"]
        occ = r["costs"]["overnight_capital"]
        lcoe = r["economics"]["lcoe_cents_per_kWh"]
        if p_net <= 0:
            print(f"{name:<38} {p_fus:>8.0f} {'NEG':>8} {occ:>10.0f} {'N/A':>12}")
        else:
            print(f"{name:<38} {p_fus:>8.0f} {p_net:>8.0f} {occ:>10.0f} {lcoe:>12.2f}")
    print()

    # Cross-concept comparison at 1000 MWe (economy-of-scale normalized)
    print(f"\n--- Scaled to 1000 MWe Reference (α=0.6 economy-of-scale) ---")
    print(f"{'Scenario':<38} {'LCOE [$/MWh]':>14} {'OCC [$/kWe]':>14}")
    print("-" * 68)
    for name, p in scenarios:
        r = p.compute()
        p_net_native = r["power"].get("p_net_plant", r["power"]["p_net"])
        if p_net_native <= 0:
            print(f"{name:<38} {'N/A':>14} {'N/A':>14}")
            continue
        factor = (p_net_native / 1000.0) ** (1.0 - _ALPHA)
        lcoe_scaled = r["economics"]["lcoe_USD_per_MWh"] * factor
        occ_per_kw = r["costs"]["overnight_capital"] * 1e3 / p_net_native
        occ_scaled = occ_per_kw * factor
        print(f"{name:<38} {lcoe_scaled:>14.1f} {occ_scaled:>14.0f}")

    # =========================================================================
    # KEY BINDING CONSTRAINTS
    # =========================================================================
    print(f"\n{'═' * 70}")
    print("KEY BINDING CONSTRAINTS (in order of LCOE leverage)")
    print(f"{'═' * 70}\n")

    print("  1. LOSS REDUCTION FACTOR γ (proxy: p_fus_MW sweep)")
    print("     The entire cost model rests on the unvalidated assumption γ=0.1.")
    print("     γ controls the electron loss rate from the Wiffleball cusp.")
    print("     At γ=0.2, p_fus halves to ~490 MW (or beam power doubles to 156 MW)")
    print("     and LCOE roughly doubles. No experiment has validated γ=0.1 at")
    print("     any plasma density above WB-X's sub-microsecond pulses.")
    print("     University of Sydney (2019) found 'little or no trace of virtual")
    print("     electrode formation' at higher densities — contested by EMC2 but")
    print("     unrefuted in peer-reviewed literature.")
    print("     STATUS: Blocking. FPNS program is the next validation milestone.\n")

    print("  2. THERMAL EFFICIENCY / ENERGY CONVERSION ARCHITECTURE")
    print("     No thermal cycle, coolant, or BOP has been specified by EMC2.")
    print("     The sweep shows ±5 ¢/kWh variation between 33% and 50% efficiency.")
    print("     80% of fusion energy (14.1 MeV neutrons) flows into a blanket with")
    print("     unspecified cooling. Without a defined thermal circuit, net electric")
    print("     output is unknown within ±50%. The 40% Rankine analogue is a")
    print("     placeholder, not an engineering assessment.")
    print("     STATUS: Blocking for serious LCOE estimation.\n")

    print("  3. CAPITAL COST UNCERTAINTY (coil + e-beam overrides dominate CAS22)")
    print("     The two concept-specific CAS22 overrides (C220103=$150M coils,")
    print("     C220104=$100M e-beam) together represent ~$250M of the per-module")
    print("     CAS22. These are analogues with ×2–3 uncertainty. The sweep shows")
    print("     coil cost is the larger lever (no existing SC Polywell design).")
    print("     Unlike MFE tokamaks, no engineering cost study or supplier quote")
    print("     exists for 6-sided polyhedral SC coils at 4.5 T.")
    print("     STATUS: High uncertainty, reducible with an engineering design study.\n")

    print("  4. BLANKET/FIRST WALL COST (C220101) — POLYHEDRAL GEOMETRY CHALLENGE")
    print("     The standard toroidal MFE analogue ($7.3M) is inapplicable to the")
    print("     6-faced polyhedral cusp. Coils on each face create neutron-shadowing")
    print("     with no proposed engineering solution (TRL 1, analysis.md §Section 3")
    print("     and §Section 6 gap #5: blocking). ARIES-class D-T studies estimate")
    print("     $50–150M for comparable neutron power levels; the model override")
    print("     baseline of $75M may understate by 2× if novel breeding geometry is")
    print("     required. The blanket cost sensitivity sweep quantifies this range.")
    print("     STATUS: High uncertainty; blocking for blanket design feasibility.")

    print(f"\n{'─' * 70}")
    print("NOTE: This model rests on a physics scaling projection with unvalidated")
    print("free parameters, no energy conversion design, and no plant engineering")
    print("study. All values carry HIGH UNCERTAINTY. LCOE estimates serve as")
    print("corridor indicators only — not cost projections.")
    print(f"{'─' * 70}")


if __name__ == "__main__":
    main()
