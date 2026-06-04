"""
Particle Accelerator-Driven Fusion (D-T) — SHINE Technologies
FLARE Facility Economics Model
=====================================
1cFE Concept Analysis — Free-Form (Non-Standard) Model
Concept: Beam-Target D-T Fusion / Neutron Production / Medical Isotopes
Company: SHINE Technologies (Janesville, WI)

CRITICAL NOTE — WHY LCOE IS UNDEFINED:
Beam-target D-T fusion has Q_sci in the range 10^{-3}–10^{-2} by physics. Each accelerated deuteron
deposits ~300 keV of kinetic energy; the D-T reaction releases 17.59 MeV, but
only a tiny fraction of beam deuterons fuse before losing energy to Coulomb
scattering and ionization in the target gas. The effective Q is set by the ratio
of the fusion cross-section to the stopping cross-section — a property of atomic
physics, not a technology maturity limit. SHINE's FLARE system produces ~141 W of fusion power. At the model baseline
of 50 mA beam current, beam power is ~15 kW and Q_sci ≈ 0.0094. At ~235 mA
(representative of higher-current operation), beam power is ~70 kW and
Q_sci ≈ 0.002. Both values fall within the published literature range of
10^{-3}–10^{-2} for beam-target D-T at 200–300 keV lab energy (F-1).

Net electricity output = 0. p_net = 0. LCOE = ∞. This is not fixable by
engineering improvements — break-even requires Q_sci > ~2.1, approximately
1,000× above the physics ceiling for beam-target D-T (Q_sci < 0.01).

This model has two parts:
  PART A: Physics demonstration of Q_sci and break-even gap (Layer 1)
  PART B: Actual SHINE FLARE facility economics (industrial facility model)

Concept-appropriate cost metrics (Part B):
  • Annual revenue requirement (M$/yr)
  • Cost per neutron [$/neutron]
  • Cost per unit steady-state flux [M$/(neutron/s)]
  • Revenue coverage ratio (Mo-99 revenue / annual facility cost)

Capital cost analogue basis: analysis.md §S6 Gap #3 cites $30-150M for
comparable Mo-99 production facilities. This model builds up from components
within that range. All capital estimates carry HIGH UNCERTAINTY.

CAS structure: Follows 1costingfe costing_constants.yaml unit costs and
installation_frac where applicable. All CAS22 sub-accounts are concept-specific
overrides (no standard fusion power-plant sub-system applies).

Key references:
- analysis.md §S2 — physics ceiling derivation, Q_sci calculation
- analysis.md §S5 — LCOE-relevant parameters table
- analysis.md §S6 — data gap inventory and analogue capital ranges
- shine-technology-overview.md §Key Facts — 5e13 reactions/s, 300 kV beam
- dossier.md — taxonomy: beam voltage, steady-state operation, neutron products
- NRC ML13172A262, ML15258A372 — licensing records
- 1costingfe costing_constants.yaml — CAS unit costs and scaling factors

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass

# === Physical constants ===
E_DT_MEV = 17.59        # D-T reaction energy [MeV] (14.07 MeV n + 3.52 MeV alpha)
J_PER_MEV = 1.602e-13   # J/MeV
F_NEUTRON = 14.07 / 17.59   # neutron energy fraction (0.7997)
F_ALPHA = 3.52 / 17.59      # alpha energy fraction (0.2003)
AVOGADRO = 6.022e23

# === Reference power levels for 1costingfe scaling (not primary for this concept) ===
P_TH_REF = 2500.0   # Reference thermal power [MW]
P_ET_REF = 1100.0   # Reference gross electric [MW]


@dataclass
class SHINEFLAREParams:
    """
    SHINE Technologies FLARE facility economics model.

    Represents the actual SHINE FLARE neutron production facility:
    a single compact linear D-beam accelerator driving a T-gas target,
    surrounded by an NRC-licensed subcritical LEU assembly for Mo-99
    production. The FLARE system is the world's highest-flux commercial
    D-T fusion neutron source (TRL 9).

    This concept produces ZERO net electricity. Layer 1 (power balance)
    demonstrates the Q_sci gap from first principles. Layers 2-5 model
    the actual industrial facility economics.

    Uncertainty tags:
      (no tag)             = well-established value with cited source
      MODERATE UNCERTAINTY = analogue-based estimate with clear reasoning
      HIGH UNCERTAINTY     = speculative or proprietary; no public data
    """

    # ── ACCELERATOR / BEAM ─────────────────────────────────────────────────────

    beam_voltage_kV: float = 300.0
    """Peak deuterium beam voltage [kV].
    Source: shine-technology-overview.md §Key Facts; dossier.md §Primary Heating.
    "Deuterium ions accelerated to up to 300 kV." Upper design limit for FLARE."""

    beam_current_mA: float = 50.0
    """Estimated beam current per accelerator [mA].
    Source: Not published by SHINE (proprietary). 50 mA is mid-range based on
    beam-target neutron generator literature for 100-400 kV class systems.
    Ref: analysis.md §S2 ("50 mA midpoint estimate from accelerator literature").
    HIGH UNCERTAINTY — largest numerical unknown in this model."""

    accelerator_wall_efficiency: float = 0.70
    """Wall-plug to delivered beam efficiency [fraction].
    Source: Typical for compact electrostatic ion accelerators at 100-400 kV.
    Modern capacitive HV supplies and RF ion sources achieve 65-80%.
    Ref: NEC Pelletron, HVEE Tandetron operational parameters.
    MODERATE UNCERTAINTY."""

    n_mod: int = 1
    """Number of identical facility modules (= 1 for SHINE FLARE).
    SHINE FLARE is modeled as a single integrated facility unit."""

    facility_overhead_kW: float = 30.0
    """Non-beam facility electrical load [kW]: HVAC, controls, hot cell, lighting.
    ASSUMED: Industrial nuclear facility overhead excluding accelerator beam power.
    MODERATE UNCERTAINTY."""

    # ── FUSION PHYSICS ─────────────────────────────────────────────────────────

    fusion_rate_per_s: float = 5.0e13
    """D-T fusion reaction rate [reactions/s].
    Source: SHINE FLARE system specification.
    Ref: shine-technology-overview.md §Key Facts; shinefusion.com FLARE press
    release (2024) — "world's most powerful continuous fusion neutron system."
    High confidence."""

    blanket_energy_multiplication: float = 1.10
    """Blanket energy multiplication [dimensionless].
    Standard D-T Li blanket: Li-6 + n produces He-4 + T + 4.8 MeV (~10% bonus).
    Ref: 1costingfe costing_constants.yaml standard assumption for D-T."""

    blanket_capture_fraction: float = 0.85
    """Fraction of D-T neutrons thermalized in the surrounding assembly.
    Source: ASSUMED. The NRC-licensed subcritical LEU assembly surrounds the
    target and captures most neutrons for fission-product (Mo-99) generation.
    Ref: NRC ML13172A262 (subcritical assembly geometry). MODERATE UNCERTAINTY."""

    thermal_efficiency: float = 0.33
    """Thermal-to-electric conversion efficiency (hypothetical only).
    Source: ASSUMED for physics demonstration. SHINE has NO thermal cycle.
    Used only to calculate the break-even Q_sci threshold.
    Ref: Small Rankine / ORC cycle efficiency range. MODERATE UNCERTAINTY."""

    # ── PLANT CONFIGURATION ────────────────────────────────────────────────────

    capacity_factor: float = 0.90
    """Beam-on availability fraction [fraction].
    Source: Medical isotope production requires >90% uptime — Mo-99 t_1/2 = 66 hr.
    Analogues: NRU, BR2 reactor-based Mo-99 producers target >=90% availability.
    Ref: analysis.md §S6 Gap #5. MODERATE UNCERTAINTY."""

    plant_lifetime_years: float = 20.0
    """Facility economic lifetime [years].
    ASSUMED: Industrial radiopharmaceutical facility norm (15-25 yr).
    MODERATE UNCERTAINTY."""

    noak: bool = True
    """Nth-of-a-kind flag. SHINE FLARE represents a mature design iteration."""

    # ── TARGET SYSTEM GEOMETRY ─────────────────────────────────────────────────

    target_radius_m: float = 0.05
    """Tritium gas target cell inner radius [m].
    ASSUMED: ~5 cm is typical for neutron-generator class D-T targets.
    Ref: Adelphi Technology, Sodern neutron generator geometries.
    MODERATE UNCERTAINTY."""

    target_length_m: float = 0.30
    """Tritium gas target active length [m].
    ASSUMED: 30 cm thick-target cell. Sufficient for ~300 keV deuteron stopping.
    MODERATE UNCERTAINTY."""

    # ── LEU SUBCRITICAL ASSEMBLY GEOMETRY ──────────────────────────────────────

    leu_radius_m: float = 0.40
    """Subcritical aqueous LEU assembly radius [m].
    ASSUMED: Criticality-safe cylindrical geometry for aqueous U (6.19% enrichment).
    Ref: NRC ML13172A262. MODERATE UNCERTAINTY."""

    leu_height_m: float = 0.60
    """Subcritical aqueous LEU assembly height [m]. Aspect ratio ~1.5. ASSUMED."""

    shielding_thickness_m: float = 1.20
    """Biological shielding thickness around the combined target + assembly [m].
    ASSUMED: Heavy concrete for 14.1 MeV neutrons + secondary gamma.
    Ref: NCRP Report No. 151 (structural shielding). MODERATE UNCERTAINTY."""

    # ── CAPITAL COSTS — ALL HIGH UNCERTAINTY ───────────────────────────────────

    accelerator_unit_cost_M: float = 15.0
    """Capital cost of accelerator system [$M].
    ASSUMED: Compact 300 kV linear accelerator with HV power supply, beam optics,
    ion source, vacuum system, diagnostics. Commercial analogues (NEC Pelletron,
    HVEE Tandetron) at $2-10M; SHINE's high-current CW version scaled to ~$15M.
    Ref: analysis.md §S6 Gap #3. HIGH UNCERTAINTY."""

    target_system_cost_M: float = 4.0
    """Capital cost of tritium gas target system [$M].
    ASSUMED: Target cell, T-gas recycling, NRC-licensed T-handling, secondary
    containment.
    Ref: analysis.md §S6 Gap #3. HIGH UNCERTAINTY."""

    leu_assembly_cost_M: float = 22.0
    """Capital cost of subcritical LEU assembly [$M].
    ASSUMED: NRC-licensed aqueous assembly with criticality monitoring, remote
    handling, solution management. Aqueous homogeneous reactor analogues: $15-35M.
    Ref: analysis.md §S6 Gap #3; NRC ML13172A262. HIGH UNCERTAINTY."""

    isotope_processing_cost_M: float = 28.0
    """Capital cost of Mo-99/Lu-177 hot cell and processing infrastructure [$M].
    ASSUMED: Pharmaceutical-grade hot cell for radiochemical separation, QC,
    dispensing. Comparable facilities: $15-40M.
    Ref: NorthStar Medical Radioisotopes analogues. HIGH UNCERTAINTY."""

    # ── FINANCIAL ──────────────────────────────────────────────────────────────

    interest_rate: float = 0.08
    """Real discount rate (WACC) [fraction]. Ref: 1costingfe default."""

    inflation_rate: float = 0.02
    """Inflation rate [fraction]. Ref: 1costingfe default."""

    construction_time_years: float = 4.0
    """Facility construction period [years].
    ASSUMED: Industrial nuclear facility; shorter than power plant.
    MODERATE UNCERTAINTY."""

    # ── OPERATING COSTS ────────────────────────────────────────────────────────

    staff_count: int = 35
    """Facility staff headcount [FTE].
    ASSUMED: NRC-licensed facility requires licensed nuclear operators, health
    physics staff, radiochemists, maintenance, engineering, administration.
    Analogues: Mo-99 production facilities operate with 20-60 FTE.
    Ref: analysis.md §S2 O&M placeholder. HIGH UNCERTAINTY."""

    avg_staff_cost_k_USD: float = 140.0
    """Average fully-loaded staff cost [k$/FTE-yr].
    ASSUMED: Wisconsin-area technical staff. BLS nuclear operators ~$100k;
    fully-loaded ~1.4x. Ref: BLS OES 51-8011. MODERATE UNCERTAINTY."""

    grid_electricity_price_per_kWh: float = 0.075
    """Grid electricity price [$/kWh].
    ASSUMED: Wisconsin industrial rate ~$0.07/kWh.
    Ref: EIA Electric Power Monthly. MODERATE UNCERTAINTY."""

    leu_cost_M_per_yr: float = 0.50
    """Annual LEU fuel procurement and waste disposal [$M/yr].
    ASSUMED: Includes NNSA-qualified supplier contracts and radwaste processing.
    Ref: analysis.md §S4. HIGH UNCERTAINTY."""

    tritium_cost_per_g: float = 35000.0
    """Tritium unit cost [$/g].
    Source: Established from HTS Compact Tokamak and market data.
    Ref: analysis.md §S2 ("~$35,000/g approximate civilian price")."""

    maintenance_frac: float = 0.03
    """Annual maintenance as fraction of overnight capital [fraction/yr].
    ASSUMED: Industrial nuclear facility norm.
    Ref: 1costingfe industrial O&M convention. MODERATE UNCERTAINTY."""

    # ── ISOTOPE PRODUCTION (revenue context only, not in CAS70-90) ─────────────

    mo99_ci_per_week: float = 1200.0
    """Mo-99 production [6-day Ci/week].
    ASSUMED: ~10% of ~12,000 Ci/week global demand.
    Ref: analysis.md §S4. HIGH UNCERTAINTY — not published by SHINE."""

    mo99_price_per_ci: float = 5000.0
    """Mo-99 producer price [$/6-day Ci].
    Source: Historical range $2,000-$30,000; $5,000 is conservative mid-range.
    Ref: analysis.md §S4. MODERATE UNCERTAINTY."""

    # ─────────────────────────────────────────────────────────────────────────
    # COMPUTE METHODS
    # ─────────────────────────────────────────────────────────────────────────

    def _compute_power(self) -> dict:
        """Layer 1: Power balance and Q_sci physics demonstration.

        Energy flow: grid -> accelerator -> D beam -> T gas target -> D-T fusion
        -> neutrons -> subcritical LEU assembly (isotope production, NOT heat capture)
        -> no thermal cycle -> p_net = 0

        The Q_sci analysis shows the 1000x gap to break-even from first principles.
        """
        r = {}

        # D-T fusion physics from the stated reaction rate
        # Source: analysis.md §S2 derivation
        p_fus_W = self.fusion_rate_per_s * E_DT_MEV * J_PER_MEV
        r["p_fus"] = p_fus_W / 1e6           # MW: ~1.41e-4 MW (141 mW)
        r["p_neutron"] = r["p_fus"] * F_NEUTRON
        r["p_alpha"] = r["p_fus"] * F_ALPHA

        # Beam power (per accelerator)
        p_beam_W = (self.beam_voltage_kV * 1e3) * (self.beam_current_mA * 1e-3)
        r["p_beam_kW"] = p_beam_W / 1e3
        r["p_beam_MW"] = p_beam_W / 1e6

        # Q_sci: fusion power / beam power delivered to target
        # At baseline 50 mA: Q_sci ≈ 0.0094 (within literature range 10^-3–10^-2).
        # At ~235 mA: Q_sci ≈ 0.002. Physics ceiling ~0.01 near 240 keV lab energy.
        # (Analysis text's 10^-5 at 50 mA is incorrect; F-1 correction.)
        r["Q_sci"] = r["p_fus"] / r["p_beam_MW"] if r["p_beam_MW"] > 0 else 0.0
        r["beam_current_mA"] = self.beam_current_mA

        # Break-even Q_sci needed for net electric power = 0
        # Derivation: net power = eta_th*(p_beam + M*f_n*f_cap*p_fus + f_a*p_fus) - p_beam = 0
        # Solving for Q_sci = p_fus/p_beam:
        #   Q_sci_be = (1 - eta_th) / (eta_th * (M*f_n*f_cap + f_a))
        eff_gain = (self.blanket_energy_multiplication * F_NEUTRON * self.blanket_capture_fraction
                    + F_ALPHA)
        denom = self.thermal_efficiency * eff_gain
        r["Q_sci_breakeven"] = (1.0 - self.thermal_efficiency) / denom if denom > 0 else float("inf")
        r["Q_sci_gap_factor"] = (r["Q_sci_breakeven"] / r["Q_sci"]
                                  if r["Q_sci"] > 0 else float("inf"))

        # Wall-plug power for accelerator
        r["p_wall_accel_kW"] = r["p_beam_kW"] / self.accelerator_wall_efficiency
        r["p_facility_kW"] = r["p_wall_accel_kW"] * self.n_mod + self.facility_overhead_kW
        r["p_facility_MW"] = r["p_facility_kW"] / 1e3

        # SHINE produces zero net electricity — all power consumed from grid
        # Neutrons enter the LEU assembly for isotope production, not a heat exchanger.
        r["p_th"] = 0.0    # MW — no thermal capture for power generation
        r["p_et"] = 0.0    # MWe — no gross electricity output
        r["p_net"] = 0.0   # MWe — not a power plant

        # Q_eng is formally zero (no net electrical output)
        r["Q_eng"] = 0.0
        # recirc_fraction is infinite — all power input is "consumed" with zero output
        r["recirc_fraction"] = float("inf")

        # Tritium consumption — analysis.md §S2 derivation
        # 5e13 T-atoms/s x 3 g/mol / (6.022e23 atoms/mol) x 3.15e7 s/yr ≈ 8 mg/yr
        r["tritium_g_per_yr"] = (self.fusion_rate_per_s * 3.0 / AVOGADRO
                                  * 3.15e7 * self.capacity_factor)
        r["tritium_cost_per_yr_USD"] = r["tritium_g_per_yr"] * self.tritium_cost_per_g

        # Annual neutron production metrics
        r["annual_operating_hours"] = 8760.0 * self.capacity_factor
        r["annual_neutrons"] = self.fusion_rate_per_s * r["annual_operating_hours"] * 3600.0

        # Multi-module plant-level aliases (required by concept explorer interface)
        r["p_fus_plant"] = r["p_fus"] * self.n_mod
        r["p_th_plant"] = r["p_th"]      # zero
        r["p_et_plant"] = r["p_et"]      # zero
        r["p_net_plant"] = r["p_net"]    # zero

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Cylindrical geometry for beam-target + subcritical assembly.

        Linear accelerator geometry: beam enters along cylinder axis into T-gas
        target, surrounded by LEU assembly, then biological shielding.
        Volumes are compact — many orders of magnitude smaller than a fusion
        power plant chamber.
        """
        r = {}

        # Target chamber (vacuum tube, cylindrical)
        r["target_vol_m3"] = math.pi * self.target_radius_m**2 * self.target_length_m

        # Subcritical LEU assembly (cylindrical)
        r["leu_assembly_vol_m3"] = math.pi * self.leu_radius_m**2 * self.leu_height_m

        # Biological shielding (annular cylinder around combined system)
        r_inner = max(self.target_radius_m, self.leu_radius_m)
        h_inner = self.target_length_m + self.leu_height_m
        r_outer = r_inner + self.shielding_thickness_m
        h_outer = h_inner + 2.0 * self.shielding_thickness_m
        r["shield_vol_m3"] = (math.pi * r_outer**2 * h_outer
                               - math.pi * r_inner**2 * h_inner)

        # Vacuum vessel (thin steel wall around target chamber)
        wall_m = 0.01   # 1 cm steel
        r["vessel_vol_m3"] = (math.pi
                               * ((self.target_radius_m + wall_m)**2
                                  - self.target_radius_m**2)
                               * self.target_length_m)

        # Primary structure (support framing)
        struct_m = 0.05
        r["structure_vol_m3"] = (math.pi
                                  * ((r_inner + struct_m)**2 - r_inner**2)
                                  * h_inner)

        # Blanket volume proxy: LEU assembly serves blanket function (no energy blanket)
        r["blanket_vol_m3"] = r["leu_assembly_vol_m3"]

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment.

        ALL sub-accounts are concept-specific overrides — no standard fusion
        power plant sub-system applies to beam-target D-T.

        1costingfe unit costs from costing_constants.yaml applied where the
        underlying physics is similar (shielding, structure, vessel volumes).
        """
        r = {}

        # Use facility electrical consumption as proxy for CAS22 power-scaling
        # (the standard p_th and p_et are both zero for this concept)
        p_fac = max(power["p_facility_MW"] * 100, 1.0)  # scale proxy [MW-equivalent]

        # C220101: First Wall / Blanket -> LEU Subcritical Assembly [override]
        # Functional analogue: the LEU assembly captures neutrons for useful work,
        # as a blanket captures neutrons in a power plant.
        r["C220101"] = self.leu_assembly_cost_M

        # C220102: Shield -> Biological Shielding
        # Volume-based with heavy concrete unit cost.
        # 1costingfe shield_unit_cost = 0.74 M$/m3 for fusion-grade steel/concrete.
        # Using 0.020 M$/m3 for plain heavy concrete (no activation-hardened steel).
        r["C220102"] = 0.020 * geom["shield_vol_m3"]

        # C220103: Coils -> 0 [override]
        # No magnetic coils. Beam-target D-T uses no plasma confinement.
        # Ref: analysis.md §S4 "No HTS Tape ... SHINE is supply-chain-simple."
        r["C220103"] = 0.0

        # C220104: Supplementary Heating -> Linear Accelerator System [override]
        # The accelerator IS the driver and energy source.
        # Standard formula (80 M$ at 1 GWe) not applicable.
        r["C220104"] = self.accelerator_unit_cost_M * self.n_mod

        # C220105: Primary Structure
        # 1costingfe structure_unit_cost = 0.15 M$/m3
        r["C220105"] = 0.15 * geom["structure_vol_m3"]

        # C220106: Vacuum System (target chamber beam tube + turbo pumps)
        # 1costingfe vessel_unit_cost = 0.72 M$/m3
        r["C220106"] = 0.72 * geom["vessel_vol_m3"]

        # C220107: Power Supplies -> Accelerator HV Power Supply [override]
        # HV supply is ~20% of accelerator capital (separated for accounting).
        # Standard formula: 80 M$ x (p_et/1000)^0.7 — not applicable here.
        r["C220107"] = self.accelerator_unit_cost_M * self.n_mod * 0.20

        # C220108: Target Factory -> Tritium Gas Target + Isotope Processing [override]
        # Replaces IFE pellet/liner factory. Includes:
        #   - T-gas target cell, recycling, NRC-compliant handling
        #   - Mo-99/Lu-177 hot cell, separation chemistry, quality control
        # IFE formula: 244 M$ x (p_et/1000)^0.7 — not applicable here.
        r["C220108"] = self.target_system_cost_M + self.isotope_processing_cost_M

        # C220109: Direct Energy Converter -> 0 [override]
        r["C220109"] = 0.0

        # C220111: Installation labor (14% of equipment subtotal)
        # Ref: 1costingfe costing_constants.yaml installation_frac = 0.14
        equip_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109"])
        r["C220111"] = 0.14 * equip_subtotal

        # C220112: Isotope Separation -> 0 (included in C220108)
        r["C220112"] = 0.0

        r["CAS22_per_module"] = equip_subtotal + r["C220111"] + r["C220112"]

        # ── Plant-wide accounts (ASSUMED — no published SHINE data) ──
        # These are minimal for an industrial-scale, low-power facility.

        r["C220200"] = 0.50   # Coolant (electronics + shielding cooling only)
        r["C220300"] = 0.30   # Auxiliary cooling
        r["C220400"] = 3.00   # Radwaste: LEU activation products + isotope waste
        r["C220500"] = 2.00   # Fuel handling: T-gas + LEU solution systems
        r["C220600"] = 1.50   # Other equipment
        r["C220700"] = 4.00   # I&C: NRC criticality monitoring + beam diagnostics

        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        r["CAS22"] = r["CAS22_per_module"] * self.n_mod + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: CAS10-60 capital costs.

        Power-scaling laws from 1costingfe are not applicable (zero electric output).
        Building and BOP costs use ASSUMED values for an industrial nuclear facility
        consistent with the $30-150M analogue range from analysis.md §S6 Gap #3.
        """
        r = {}

        # CAS10: Pre-construction
        # NRC licensing for accelerator-driven subcritical assembly: less than
        # D-T power plant ($5M), analogous to DD neutron source licensing ($3M).
        site_permits = 3.0
        plant_studies = 4.0 if self.noak else 12.0
        plant_permits = 2.0
        plant_reports = 1.0
        other_precon = 1.0
        licensing = 3.0    # NRC Part 50/70 pathway for subcritical assembly
        r["CAS10"] = site_permits + plant_studies + plant_permits + plant_reports + other_precon + licensing

        # CAS21: Buildings
        # ASSUMED: ~3,000 m2 specialized nuclear facility (accelerator hall + hot cell
        # + offices + utilities). $18M is consistent with analogue industrial nuclear
        # facility construction cost.
        r["CAS21"] = 18.0

        # CAS22: from above
        r["CAS22"] = cas22["CAS22"]

        # CAS23: Turbine Plant -> 0 (no turbine)
        r["CAS23"] = 0.0

        # CAS24: Electric Plant Equipment (facility HV distribution, UPS)
        r["CAS24"] = 1.50   # ASSUMED: M$

        # CAS25: Misc Plant Equipment
        r["CAS25"] = 1.00   # ASSUMED: M$

        # CAS26: Heat Rejection (cooling for electronics and hot cell HVAC only)
        r["CAS26"] = 0.50   # ASSUMED: M$

        # CAS27: Special Materials (initial LEU solution inventory)
        r["CAS27"] = 2.00   # ASSUMED: M$

        # CAS28: Digital Twin / Control System
        r["CAS28"] = 2.00   # ASSUMED: M$

        # CAS29: Contingency (0% for NOAK; 15% for FOAK — novel NRC licensing)
        cas20_raw = sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                        "CAS25", "CAS26", "CAS27", "CAS28"])
        contingency_rate = 0.0 if self.noak else 0.15
        r["CAS29"] = contingency_rate * cas20_raw

        r["CAS20"] = cas20_raw + r["CAS29"]

        # CAS30: Indirect Costs (20% of CAS20, scaled by construction time)
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / 6.0)

        # CAS40: Owner's Costs (5% of CAS20 — standard convention)
        r["CAS40"] = 0.05 * r["CAS20"]

        # CAS50: Supplementary Costs
        # Initial tritium inventory (holding stock + consumed), spare accelerator
        # components, startup operations costs.
        r["CAS50"] = 3.00   # ASSUMED: M$

        r["overnight_capital"] = (r["CAS10"] + r["CAS20"] + r["CAS30"]
                                   + r["CAS40"] + r["CAS50"])

        # CAS60: Interest During Construction
        i = self.interest_rate
        T = self.construction_time_years
        f_idc = ((1 + i)**T - 1) / (i * T) - 1 if (i > 0 and T > 0) else 0.0
        r["CAS60"] = f_idc * r["overnight_capital"]
        r["f_IDC"] = f_idc

        r["total_capital"] = r["overnight_capital"] + r["CAS60"]
        r["specific_capital_USD_per_kWe"] = float("inf")   # Not a power plant

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70-90 annualized costs and concept-appropriate metrics.

        Standard LCOE ($/MWh) is undefined since p_net = 0. This layer computes:
        - Annual revenue requirement (total M$/yr)
        - Cost per neutron [$/neutron]
        - Revenue coverage ratio (Mo-99 revenue / annual cost)
        """
        r = {}

        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1 + i)**n / ((1 + i)**n - 1)
        r["CRF"] = crf

        # CAS90: Annualized Capital Charge
        r["CAS90"] = crf * costs["total_capital"]   # M$/yr

        # CAS71: Annual O&M (staffing + electricity + maintenance)
        annual_staff_M = self.staff_count * self.avg_staff_cost_k_USD / 1e3
        annual_electricity_M = (power["p_facility_kW"] * power["annual_operating_hours"]
                                 * self.grid_electricity_price_per_kWh / 1e6)
        annual_maintenance_M = self.maintenance_frac * costs["overnight_capital"]

        r["CAS71"] = annual_staff_M + annual_electricity_M + annual_maintenance_M
        r["CAS71_staff"] = annual_staff_M
        r["CAS71_electricity"] = annual_electricity_M
        r["CAS71_maintenance"] = annual_maintenance_M

        # CAS72: Scheduled Replacement (accelerator ion source + hot cell tooling)
        # 2% of CAS22 per year levelized (conservative for industrial equipment).
        r["CAS72"] = 0.02 * costs["CAS22"]   # M$/yr
        r["n_blanket_replacements"] = 0       # No blanket; sentinel for interface

        r["CAS70"] = r["CAS71"] + r["CAS72"]   # M$/yr

        # CAS80: Fuel and Consumables
        annual_leu_M = self.leu_cost_M_per_yr
        # Tritium: 8 mg/yr × $35,000/g ≈ $280/yr — analysis.md §S2 confirms negligible
        annual_tritium_M = power["tritium_cost_per_yr_USD"] / 1e6
        annual_deuterium_M = 0.001   # D-gas: trivial quantity at negligible cost
        r["CAS80"] = annual_leu_M + annual_tritium_M + annual_deuterium_M
        r["CAS80_leu"] = annual_leu_M
        r["CAS80_tritium"] = annual_tritium_M
        r["CAS80_deuterium"] = annual_deuterium_M

        # Annual Revenue Requirement
        r["annual_revenue_req"] = r["CAS90"] + r["CAS70"] + r["CAS80"]

        # LCOE — undefined for a zero-power device
        r["annual_energy_MWh"] = 0.0
        r["lcoe_USD_per_MWh"] = float("inf")
        r["lcoe_cents_per_kWh"] = float("inf")

        # Concept-appropriate cost metrics
        annual_neutrons = power["annual_neutrons"]
        r["annual_neutrons"] = annual_neutrons
        if annual_neutrons > 0:
            r["cost_per_neutron_USD"] = r["annual_revenue_req"] * 1e6 / annual_neutrons
            r["cost_per_flux_unit_M_USD"] = r["annual_revenue_req"] / self.fusion_rate_per_s
        else:
            r["cost_per_neutron_USD"] = float("inf")
            r["cost_per_flux_unit_M_USD"] = float("inf")

        # Mo-99 revenue context (shows economic viability as isotope producer)
        annual_mo99_M = self.mo99_ci_per_week * 52.0 * self.mo99_price_per_ci / 1e6
        r["mo99_annual_revenue_M"] = annual_mo99_M
        r["annual_cost_coverage_ratio"] = (annual_mo99_M / r["annual_revenue_req"]
                                            if r["annual_revenue_req"] > 0 else 0.0)

        # Cost breakdown fractions
        rev = r["annual_revenue_req"]
        r["capital_fraction"] = r["CAS90"] / rev if rev > 0 else float("nan")
        r["om_fraction"] = r["CAS70"] / rev if rev > 0 else float("nan")
        r["fuel_fraction"] = r["CAS80"] / rev if rev > 0 else float("nan")

        return r

    def compute(self) -> dict:
        """Compute facility economics using CAS-structured accounting.

        Returns a dict with sub-dicts matching the concept-explorer interface:
        power, geometry, cas22, costs, economics.
        """
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


# ─────────────────────────────────────────────────────────────────────────────
# Module-level interface (consumed by concept explorer)
# ─────────────────────────────────────────────────────────────────────────────

params = SHINEFLAREParams()
results = params.compute()


# ─────────────────────────────────────────────────────────────────────────────
# Output functions
# ─────────────────────────────────────────────────────────────────────────────

def print_results(p: SHINEFLAREParams, res: dict):
    """Pretty-print facility economics with CAS-structured accounting."""
    power = res["power"]
    cas22 = res["cas22"]
    costs = res["costs"]
    econ = res["economics"]
    q_be = power["Q_sci_breakeven"]
    gap = power["Q_sci_gap_factor"]

    print("=" * 72)
    print("Particle Accelerator-Driven Fusion (D-T) — SHINE Technologies FLARE")
    print("Facility Economics Model — 1cFE CAS-Structured (Free-Form)")
    print("=" * 72)
    print()
    print("  *** IMPORTANT: SHINE IS NOT A POWER PLANT (p_net = 0 by physics) ***")
    print(f"  Q_sci = {power['Q_sci']:.2e}  |  Break-even = {q_be:.2f}  |  Gap = {gap:.0f}x")
    print("  LCOE ($/MWh) is undefined. Concept-appropriate metrics follow.")
    print()

    print("--- Fusion Physics (PART A: Q_sci demonstration) ---")
    print(f"  Fusion reaction rate:      {p.fusion_rate_per_s:.2e} reactions/s  [high confidence]")
    print(f"  Fusion power:              {power['p_fus']*1e6:.1f} mW  (~141 mW)")
    print(f"  Beam voltage:              {p.beam_voltage_kV:.0f} kV  [known]")
    print(f"  Beam current (est.):       {p.beam_current_mA:.0f} mA  [HIGH UNCERTAINTY]")
    print(f"  Beam power (to target):    {power['p_beam_kW']:.1f} kW")
    print(f"  Wall-plug (accelerator):   {power['p_wall_accel_kW']:.1f} kW")
    print(f"  Total facility draw:       {power['p_facility_kW']:.1f} kW")
    print(f"  Q_sci (fusion/beam):       {power['Q_sci']:.4f}  [physics ceiling: <0.01]")
    print(f"  Q_sci needed for p_net=0:  {q_be:.3f}  ({gap:.0f}x above current)")
    print(f"  Q_eng:                     0  (no net electricity output)")
    print(f"  recirc_fraction:           inf  (all input power consumed)")
    print()
    print("  Tritium consumed:          {:.2f} mg/yr".format(power["tritium_g_per_yr"]*1e3))
    print("  Tritium cost:              ${:,.0f}/yr  (negligible)".format(power["tritium_cost_per_yr_USD"]))
    print()

    print("--- Neutron Production ---")
    print(f"  Capacity factor:           {p.capacity_factor:.1%}")
    print(f"  Annual neutrons:           {power['annual_neutrons']:.3e} neutrons/yr")
    print()

    print("--- CAS22: Facility Equipment (PART B: FLARE facility economics) ---")
    print("  All accounts are concept-specific overrides. No standard fusion")
    print("  power-plant sub-system applies.")
    cas22_labels = {
        "C220101": "LEU Subcritical Assembly   [override]",
        "C220102": "Biological Shield",
        "C220103": "Coils (N/A)               [override=0]",
        "C220104": "Linear Accelerator        [override]",
        "C220105": "Primary Structure",
        "C220106": "Vacuum System (beam tube)",
        "C220107": "HV Power Supply           [override]",
        "C220108": "Target + Isotope Proc.    [override]",
        "C220109": "Direct Energy Conv. (N/A) [override=0]",
        "C220111": "Installation (14%)",
        "C220112": "Isotope Sep. (in C220108)",
    }
    for code, label in cas22_labels.items():
        val = cas22[code]
        if val > 0.005 or "override" in label:
            print(f"  {code}  {label:<44s}  ${val:>8.2f}M")
    print(f"  {'─'*60}")
    print(f"  Per-module subtotal:                                    ${cas22['CAS22_per_module']:>8.2f}M")
    pw_labels = {
        "C220200": "Coolant Systems (minimal)",
        "C220300": "Auxiliary Cooling",
        "C220400": "Radioactive Waste Management",
        "C220500": "Fuel Handling (T + LEU)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    for code, label in pw_labels.items():
        print(f"  {code}  {label:<44s}  ${cas22[code]:>8.2f}M")
    print(f"  {'─'*60}")
    print(f"  Plant-wide subtotal:                                    ${cas22['CAS22_plant_wide']:>8.2f}M")
    print(f"  CAS22 Total:                                            ${cas22['CAS22']:>8.2f}M")
    print()

    print("--- Capital Costs (CAS10-60) ---")
    print(f"  CAS10 Pre-construction:                         ${costs['CAS10']:>8.2f}M")
    print(f"  CAS21 Buildings:                                ${costs['CAS21']:>8.2f}M")
    print(f"  CAS22 Facility Equipment:                       ${costs['CAS22']:>8.2f}M")
    print(f"  CAS23 Turbine Plant:                            ${costs['CAS23']:>8.2f}M  (N/A)")
    print(f"  CAS24 Electric Plant:                           ${costs['CAS24']:>8.2f}M")
    print(f"  CAS25 Misc Equipment:                           ${costs['CAS25']:>8.2f}M")
    print(f"  CAS26 Heat Rejection:                           ${costs['CAS26']:>8.2f}M")
    print(f"  CAS27 Special Materials (LEU):                  ${costs['CAS27']:>8.2f}M")
    print(f"  CAS28 Control System:                           ${costs['CAS28']:>8.2f}M")
    print(f"  CAS29 Contingency:                              ${costs['CAS29']:>8.2f}M")
    print(f"  {'─'*55}")
    print(f"  CAS20 Direct Costs:                             ${costs['CAS20']:>8.2f}M")
    print(f"  CAS30 Indirect Costs:                           ${costs['CAS30']:>8.2f}M")
    print(f"  CAS40 Owner's Costs:                            ${costs['CAS40']:>8.2f}M")
    print(f"  CAS50 Supplementary:                            ${costs['CAS50']:>8.2f}M")
    print(f"  {'─'*55}")
    print(f"  Overnight Capital:                              ${costs['overnight_capital']:>8.2f}M")
    print(f"  CAS60 IDC (f={costs['f_IDC']:.3f}):                     ${costs['CAS60']:>8.2f}M")
    print(f"  {'='*55}")
    print(f"  Total Capital:                                  ${costs['total_capital']:>8.2f}M")
    print(f"  Specific Capital:                               N/A (not a power plant)")
    print()

    print("--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90 Capital Charge (CRF={econ['CRF']:.4f}):       ${econ['CAS90']:>8.2f}M/yr")
    print(f"  CAS71 O&M:")
    print(f"    Staffing ({p.staff_count} FTE x ${p.avg_staff_cost_k_USD:.0f}k):    ${econ['CAS71_staff']:>8.2f}M/yr")
    print(f"    Grid electricity ({power['p_facility_kW']:.0f} kW):    ${econ['CAS71_electricity']:>8.4f}M/yr")
    print(f"    Maintenance ({p.maintenance_frac:.1%} of overnight): ${econ['CAS71_maintenance']:>8.2f}M/yr")
    print(f"  CAS71 O&M Total:                                ${econ['CAS71']:>8.2f}M/yr")
    print(f"  CAS72 Scheduled Replacement (2% CAS22):         ${econ['CAS72']:>8.2f}M/yr")
    print(f"  CAS70 Total O&M:                                ${econ['CAS70']:>8.2f}M/yr")
    print(f"  CAS80 Fuel + Consumables:")
    print(f"    LEU fuel + waste:                             ${econ['CAS80_leu']:>8.3f}M/yr")
    print(f"    Tritium ({power['tritium_g_per_yr']*1e3:.2f} mg/yr):                ${econ['CAS80_tritium']*1e6:>8.2f}/yr")
    print(f"  CAS80 Total:                                    ${econ['CAS80']:>8.3f}M/yr")
    print(f"  {'─'*55}")
    print(f"  Annual Revenue Requirement:                     ${econ['annual_revenue_req']:>8.2f}M/yr")
    print()

    print("  Cost Breakdown:")
    print(f"    Capital (CAS90):  {econ.get('capital_fraction', 0):.1%}")
    print(f"    O&M (CAS70):      {econ.get('om_fraction', 0):.1%}")
    print(f"    Fuel (CAS80):     {econ.get('fuel_fraction', 0):.1%}")
    print()

    print("--- LCOE and Concept-Appropriate Metrics ---")
    print(f"  LCOE:                    NOT APPLICABLE (freeform, native-scale only) — p_net = 0 by physics")
    print(f"  Annual neutrons:         {econ['annual_neutrons']:.3e} neutrons/yr")
    print(f"  Cost per neutron:        ${econ['cost_per_neutron_USD']:.3e} / neutron")
    print(f"  Cost per flux unit:      ${econ['cost_per_flux_unit_M_USD']:.4e} M$ / (neutron/s)")
    print()

    print("--- Mo-99 Revenue Context ---")
    print(f"  Production (assumed):    {p.mo99_ci_per_week:,.0f} Ci/week")
    print(f"  Producer price:          ${p.mo99_price_per_ci:,.0f}/6-day Ci")
    print(f"  Annual Mo-99 revenue:    ${econ['mo99_annual_revenue_M']:.1f}M/yr  [HIGH UNCERTAINTY]")
    print(f"  Annual facility cost:    ${econ['annual_revenue_req']:.2f}M/yr")
    print(f"  Revenue coverage ratio:  {econ['annual_cost_coverage_ratio']:.0f}x")
    print()
    print("  SHINE's commercial viability is driven by isotope market pricing,")
    print("  NOT electricity markets. Coverage ratio >1 shows economic viability")
    print("  as an isotope producer. The concept has no path to LCOE competitiveness.")
    print()


def sensitivity_sweep(base_p: SHINEFLAREParams, param_name: str,
                      values: list) -> list:
    """Sweep a single parameter; return annual cost and coverage ratio."""
    out = []
    for val in values:
        p = SHINEFLAREParams(**{**base_p.__dict__, param_name: val})
        r = p.compute()
        econ = r["economics"]
        out.append({
            "param_value": float(val),
            "annual_cost_M": econ["annual_revenue_req"],
            "cost_per_neutron": econ.get("cost_per_neutron_USD", float("inf")),
            "coverage_ratio": econ.get("annual_cost_coverage_ratio", 0.0),
            "Q_sci": r["power"]["Q_sci"],
            "Q_sci_gap": r["power"]["Q_sci_gap_factor"],
        })
    return out


def main():
    # ── BASELINE ─────────────────────────────────────────────────────────────
    print("\n" + "#" * 72)
    print("# BASELINE: SHINE FLARE Facility — Moderate Estimates")
    print("#" * 72)

    baseline = SHINEFLAREParams()
    res = baseline.compute()
    print_results(baseline, res)

    # ── SENSITIVITY SWEEPS ────────────────────────────────────────────────────
    print("=" * 72)
    print("SENSITIVITY ANALYSIS — Annual Revenue Requirement (M$/yr)")
    print("LCOE is infinite for all cases; sweeps show cost-driver sensitivity.")
    print("=" * 72)

    base_cost = res["economics"]["annual_revenue_req"]
    print(f"\nBaseline annual cost: ${base_cost:.2f}M/yr\n")

    # NOTE (F-3): beam_voltage_kV is intentionally excluded from sweeps.
    # Q_sci peaks near 120 keV CM energy (~240 keV lab for D on T); above and below
    # this optimum, Q_sci declines, but the physics ceiling of ~0.01 applies across
    # the entire accessible voltage range (100–400 kV). Sweeping beam_voltage_kV at
    # fixed q_eff produces a flat line; at variable q_eff the result is "stay near
    # 300 kV." Neither sweep adds decision-relevant information.
    sweeps = [
        ("beam_current_mA",        [10, 30, 50, 100, 200],       "Beam current [mA]   [HIGH UNCERTAINTY — not published]"),
        ("capacity_factor",        [0.70, 0.80, 0.90, 0.95],     "Capacity factor"),
        ("leu_assembly_cost_M",    [10, 15, 22, 35, 50],         "LEU assembly cost [$M]"),
        ("isotope_processing_cost_M", [15, 22, 28, 40, 55],      "Isotope processing cost [$M]"),
        ("staff_count",            [20, 30, 35, 50, 60],         "Staff count [FTE]   [HIGH UNCERTAINTY]"),
        ("interest_rate",          [0.05, 0.08, 0.10, 0.12],     "Interest rate (WACC)"),
    ]

    for param_name, values, label in sweeps:
        print(f"  {label}:")
        sweep_results = sensitivity_sweep(baseline, param_name, values)
        for sr in sweep_results:
            is_base = abs(sr["param_value"] - getattr(baseline, param_name)) < 1e-9
            mark = "  <- baseline" if is_base else ""
            print(f"    {sr['param_value']:>10.3g}  ->  ${sr['annual_cost_M']:>7.2f}M/yr"
                  f"   coverage {sr['coverage_ratio']:.0f}x{mark}")
        print()

    # ── SCENARIO COMPARISON ───────────────────────────────────────────────────
    print("=" * 72)
    print("SCENARIO COMPARISON")
    print("=" * 72)
    print()
    print(f"  {'Scenario':<28} {'Overnight ($M)':>14} {'Annual ($M/yr)':>14} {'Coverage':>10}")
    print("  " + "-" * 70)

    scenarios = {
        "Conservative (high cost)": SHINEFLAREParams(
            capacity_factor=0.75,
            leu_assembly_cost_M=35.0,
            isotope_processing_cost_M=40.0,
            staff_count=50,
            interest_rate=0.10,
            construction_time_years=5.0,
            mo99_ci_per_week=800.0,
        ),
        "Moderate (baseline)": SHINEFLAREParams(),
        "Optimistic (low cost)": SHINEFLAREParams(
            capacity_factor=0.92,
            leu_assembly_cost_M=15.0,
            isotope_processing_cost_M=20.0,
            staff_count=25,
            interest_rate=0.06,
            construction_time_years=3.5,
            mo99_ci_per_week=1800.0,
            mo99_price_per_ci=7000.0,
        ),
    }

    for name, sp in scenarios.items():
        sr = sp.compute()
        overnight = sr["costs"]["overnight_capital"]
        ann = sr["economics"]["annual_revenue_req"]
        cov = sr["economics"]["annual_cost_coverage_ratio"]
        print(f"  {name:<28} ${overnight:>11.1f}M   ${ann:>11.2f}M/yr   {cov:>7.0f}x")

    print()

    # ── KEY BINDING CONSTRAINTS ───────────────────────────────────────────────
    print("=" * 72)
    print("KEY BINDING CONSTRAINTS — Top 3 Cost / Viability Drivers")
    print("=" * 72)

    q_be = res["power"]["Q_sci_breakeven"]
    gap = res["power"]["Q_sci_gap_factor"]
    cap = res["costs"]["overnight_capital"]
    ann = res["economics"]["annual_revenue_req"]
    p_fac_kW = res["power"]["p_facility_kW"]

    print(f"""
1. FUNDAMENTAL PHYSICS CEILING ON Q_sci (ELIMINATES POWER-GENERATION VIABILITY)
   Current Q_sci = {res['power']['Q_sci']:.2e} (at {baseline.beam_current_mA:.0f} mA)
   Break-even Q_sci needed = {q_be:.2f}   |   Gap = {gap:.0f}x

   In beam-target D-T at 300 keV, the D-T cross-section at the D-T peak
   (~120 keV CM energy = ~240 keV lab) is ~5 barns. But the stopping cross-
   section for Coulomb interactions with electrons in the target gas is
   ~1000x larger. Only ~0.1-1% of beam deuterons fuse before losing their
   energy. This ratio is set by atomic physics, not engineering.

   Breaking even requires Q_sci > {q_be:.2f} — about {gap:.0f}x above the physics
   ceiling for ANY beam-target D-T geometry. No accelerator optimization,
   no blanket improvement, and no capital reduction can overcome this.
   A plasma-confining device (tokamak, FRC, etc.) would be required instead.

2. STAFFING DOMINATES O&M (LARGEST ANNUAL COST DRIVER)
   Staffing at baseline = ${res['economics']['CAS71_staff']:.1f}M/yr ({res['economics']['CAS71_staff']/ann*100:.0f}% of annual cost)
   NRC-mandated licensed operators and health physics staff cannot be
   eliminated. Sensitivity: 20 to 50 FTE shifts annual cost by ~+/-$2.1M/yr.

   CONTRAST: Grid electricity for the entire facility = ${res['economics']['CAS71_electricity']*1e3:.0f}k/yr
   (beam power at {p_fac_kW:.0f} kW is negligible as a cost driver at this scale).
   The facility is not an energy consumer in any economically meaningful sense.

3. REVENUE MODEL IS ISOTOPE PRICING — NOT ENERGY PRICING
   Facility cost: ~${ann:.1f}M/yr  |  Mo-99 revenue (assumed): ~${res['economics']['mo99_annual_revenue_M']:.0f}M/yr
   Coverage ratio: ~{res['economics']['annual_cost_coverage_ratio']:.0f}x

   SHINE's commercial viability comes from the Mo-99 and Lu-177 isotope
   markets, not from electricity. The LCOE comparison framework is
   categorically inapplicable — SHINE competes with reactor-based Mo-99
   producers (NRU, BR2, SAFARI-1), not with power plants.

   From the TEA project perspective, SHINE establishes the lower Q bound of
   commercially-deployed D-T fusion: TRL 9 at Q_sci ~ 10^{{-3}} to 10^{{-2}},
   capital ~ ${cap:.0f}M, economically sustained by the isotope market.
   Every accelerator-driven fusion POWER concept must clear Q_sci >> 1;
   SHINE demonstrates that reaching TRL 9 at Q << 1 is already achievable.
""")

    print("NOTE: All estimates carry HIGH UNCERTAINTY. LCOE = inf for all realistic")
    print("parameter values. See analysis.md §S2 for the physics ceiling derivation.")


if __name__ == "__main__":
    main()
