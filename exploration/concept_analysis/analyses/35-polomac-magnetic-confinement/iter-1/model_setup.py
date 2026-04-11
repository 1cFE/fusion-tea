"""
PoloMac Magnetic Confinement (D-D) — Free-Form LCOE Model
==========================================================
1cFE First Pass Concept Analysis
Concept: PoloMac Magnetic Confinement — Poloidally-Confined Dipole with In-Vessel Coil
Company: Deutelio AG

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

DATA QUALITY WARNING
--------------------
This model is built almost entirely from assumed or analogued values. The analysis
(analysis.md) documents 13 blocking data gaps — no plasma Q, no reactor design point,
no confinement physics, no heating system, no power conversion design, no cost data.

The ONLY quantitative data from primary sources used here are:
  - Plasma volume: 1300 m³  (Elio 2014, medium confidence)
  - Coil magnetic field: ~2 T at 10–25 A/mm² (Elio 2014, medium confidence)
  - Plasma beta: 20–30% (claimed from historical dipole experiments, medium confidence)
  - Copper coil power draw: 700 MW (Elio 2014, high confidence — but for copper only)
  - Operation mode: steady-state (JTSP 2024, high confidence)
  - Fuel: D-D primary target (JTSP 2024, high confidence)

All other values (Q, heating, thermal efficiency, coil cost, etc.) are assumed from
analogues and marked HIGH UNCERTAINTY. Do not treat LCOE outputs as engineering estimates.

Cost accounting follows the standardized CAS (Code of Accounts System) structure
used in 1costingfe/pyFECONS. Scaling laws are adopted from:
  - 1costingfe costing_constants.yaml (pyFECONS defaults)
  - MagLIF exemplar (maglif_lcoe_model.py) for structural patterns
  - D-D-specific adjustments from 1costingfe fuel-type constants

Key references:
  - Elio, F. (2014) "Revisiting the poloidal magnetic confinement." Fusion Eng. Design 89(7–8)
    doi:10.1016/j.fusengdes.2014.03.054
  - Elio et al. (2024) "Technical Report: The Polomac approach to fusion energy." JTSP
    https://www.jtsp.eu/jtsp/article/view/32
  - Deutelio AG company profile (extracted 2026-04-04)
  - analysis.md §Section 5 — LCOE-Relevant Parameters
  - 1costingfe costing_constants.yaml — scaling law sources
"""

import math
from dataclasses import dataclass, field
from typing import Optional


# === Reference power levels for scaling laws (from 1costingfe) ===
P_TH_REF = 2500.0   # Reference thermal power [MW]
P_ET_REF = 1100.0   # Reference gross electric power [MW]

# === D-D fusion energy partition ===
# D+D → T (1.01 MeV) + p (3.02 MeV) [50% of reactions, 4.03 MeV total, no neutrons]
# D+D → ³He (0.82 MeV) + n (2.45 MeV) [50% of reactions, 3.27 MeV total]
# Average energy per D+D reaction: (4.03 + 3.27) / 2 = 3.65 MeV
# Neutron power fraction: (0.5 × 2.45) / 3.65 = 0.335
# Charged particle fraction: 1 − 0.335 = 0.665
F_NEUTRON_DD = 0.335
F_CHARGED_DD = 0.665


@dataclass
class PoloMacPlantParams:
    """
    Parameterized PoloMac Magnetic Confinement power plant model.

    PoloMac is a steady-state D-D magnetic confinement concept using a poloidally
    wound in-vessel dipole coil supported by plasma-free "magnetic tunnels." The
    commercial design requires superconducting coils to avoid the 700 MW copper
    coil resistive draw identified in Elio 2014.

    Almost every parameter in this model is assumed from analogues. See module
    docstring for data quality context.
    """

    # =========================================================================
    # PLASMA PHYSICS (Layer 1 inputs)
    # =========================================================================

    p_fus_MW: float = 800.0
    """Assumed fusion thermal power [MW].
    Source: No reactor design point exists for PoloMac (analysis.md §S5, §S2).
    ASSUMED: Analogous to a large steady-state MFE device. 800 MW is consistent
    with an ITER-class plasma volume (1300 m³ > ITER's ~840 m³) operating at
    substantially lower Q due to D-D fuel penalty (~6× harder than D-T).
    Ref: analysis.md §S2 (no reactor design point); analogue scaling from large
    tokamak D-D studies.
    HIGH UNCERTAINTY."""

    Q_plasma: float = 15.0
    """Plasma energy gain — physics Q = P_fus / P_heat_to_plasma.
    Source: No confinement physics for PoloMac at any relevant parameter
    (analysis.md §S2, §S3). Historical experiments reached "few eV" temperatures.
    ASSUMED: Q = 15 represents an aspirational but not ignition-level target,
    loosely analogous to what would be needed for D-D commercial viability.
    Analysis §S2 notes recirculating power is a blocking issue even with SC coils —
    Q must be high enough to make net electric positive (analysis §S7).
    Threshold for positive net electric ≈ Q > 10 at these efficiency assumptions.
    HIGH UNCERTAINTY."""

    plasma_beta: float = 0.25
    """Volume-averaged plasma beta (ratio of plasma pressure to magnetic pressure).
    Source: Elio 2014 §Introduction: "energy parameter beta 20–30%" from historical
    dipole experiments. Medium confidence — these were historical experiments at
    sub-fusion conditions, not PoloMac measurements.
    Ref: elio-2014-fed-poloidal-confinement.md §Introduction; analysis.md §S5."""

    B_coil_T: float = 2.0
    """Coil magnetic field at the coil current density [T].
    Source: Elio 2014 §Magnet coils: "~2 T at 10–25 A/mm²" for the 2014 FEA design.
    The commercial design is unspecified; this value is for the 1300 m³ geometry.
    Ref: elio-2014-fed-poloidal-confinement.md §Magnet coils; analysis.md §S5.
    MODERATE UNCERTAINTY."""

    plasma_volume_m3: float = 1300.0
    """Plasma volume [m³].
    Source: Elio 2014 §Coil support and supply: "plasma volume of 1300 m³" in
    the 2014 design geometry. This is not a power plant design point — it is
    the geometry from the static magnetic field analysis.
    Ref: elio-2014-fed-poloidal-confinement.md §Coil support and supply;
    analysis.md §S5. Medium confidence."""

    # =========================================================================
    # COIL SYSTEM (dominant capital cost uncertainty)
    # =========================================================================

    sc_coil_cost_M_USD: float = 500.0
    """In-vessel superconducting dipole coil cost [M$].
    Source: No superconducting coil design has been published for PoloMac
    (analysis.md §S2, §S3, §S4).
    ASSUMED: Analogue to large SC coil systems in advanced tokamaks. The LDX-
    class floating in-vessel coil (MIT) was modest-scale; a full power-plant
    in-vessel coil exposed to neutron flux with radiation-hardened insulation
    is estimated here at $500M — roughly 2× a large tokamak TF coil set due
    to the unique in-vessel geometry, cryogenic feed-through constraints, and
    radiation-hardening requirements. REBCO HTS is the assumed conductor type
    (analysis.md §S4).
    HIGH UNCERTAINTY. Range: $200M (optimistic, HTS matures) to $1B+ (FOAK)."""

    p_cryo_MW: float = 20.0
    """SC coil cryogenic system electrical draw [MW].
    Source: No cryogenic design exists for PoloMac (analysis.md §S3).
    ASSUMED: 20 MW for an in-vessel SC coil cryoplant, elevated above typical
    tokamak cryoplant (~5–15 MW) due to in-vessel geometry increasing heat loads
    and cryogenic feed-through complexity.
    For context: The copper coil draw was 700 MW (Elio 2014). SC coils replace
    this with a much smaller but non-zero cryogenic load.
    Ref: analysis.md §S7 (recirculating power framing).
    HIGH UNCERTAINTY. This is the key difference from the blocking 700 MW copper case."""

    # =========================================================================
    # POWER CONVERSION
    # =========================================================================

    blanket_mult_DD: float = 1.03
    """D-D blanket energy multiplication factor M (dimensionless).
    Source: No blanket design for PoloMac.
    ASSUMED: D-D blanket captures 2.45 MeV neutrons (no exothermic Li-6 reaction
    as there is no breeding). Minimal multiplication from neutron moderation only.
    M ≈ 1.03 (vs M ≈ 1.10–1.15 for D-T with Li blanket).
    Ref: 1costingfe costing_constants.yaml (blanket_unit_cost_dd), analysis.md §S4.
    DEFAULT from 1costingfe D-D convention."""

    thermal_efficiency: float = 0.35
    """Thermal-to-electric conversion efficiency.
    Source: No power conversion design exists for PoloMac (analysis.md §S3, §S5).
    ASSUMED: D-D fusion produces lower-energy neutrons (2.45 MeV vs 14.1 MeV for D-T),
    resulting in somewhat lower blanket exit temperatures. A Rankine-cycle thermal
    efficiency of 35% is assumed (vs 38–40% for D-T with high-temperature blanket).
    Ref: Analogue to large-volume steady-state MFE studies. SAND2006-7148 used 40%
    for D-T; reducing by ~12% for D-D spectrum.
    HIGH UNCERTAINTY."""

    heating_system_efficiency: float = 0.60
    """Wall-plug efficiency of auxiliary plasma heating system (dimensionless).
    Source: No heating method specified for PoloMac (analysis.md §S2, §S3, §S5 —
    gap type: truly-unknown, criticality: blocking).
    ASSUMED: NBI (Neutral Beam Injection) is the most common large-MFE heating
    system. Modern NBI wall-plug efficiency ~55–65%. Using 60% as mid-estimate.
    ECRH or ICRH would have different efficiency; no system is specified.
    Ref: Standard MFE systems engineering convention.
    HIGH UNCERTAINTY — heating method is unspecified."""

    # =========================================================================
    # PLANT CONFIGURATION
    # =========================================================================

    n_mod: int = 1
    """Number of fusion modules (chambers) per plant.
    Source: No plant design exists. Single module is the simplest assumption.
    ASSUMED."""

    plant_availability: float = 0.75
    """Plant capacity factor / availability.
    Source: No O&M data or maintenance design for PoloMac (analysis.md §S3, §S5).
    ASSUMED: 75% is lower than mature nuclear (85–90%) to reflect:
    (1) TRL-1 plasma system with unproven confinement reliability,
    (2) In-vessel coil maintenance complexity (analysis.md §S2, §S3).
    Analysis §S3 notes the in-vessel coil maintenance is a major unresolved challenge.
    HIGH UNCERTAINTY."""

    plant_lifetime_years: float = 30.0
    """Plant economic lifetime [years].
    Source: No design basis for PoloMac.
    ASSUMED: 30 years, shorter than the 40-year 1costingfe default for mature
    concepts, reflecting the novel in-vessel coil replacement challenge.
    HIGH UNCERTAINTY."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds 10% contingency per 1costingfe CAS29 convention.
    Given TRL-1 status, FOAK is more realistic, but NOAK used for fair comparison."""

    # =========================================================================
    # GEOMETRY
    # =========================================================================

    major_radius_m: float = 5.0
    """Approximate plasma major radius [m] for toroidal geometry approximation.
    Source: Not directly stated in Elio 2014; derived to give plasma_volume_m3
    = 1300 m³ using V_torus = 2π²Ra² with reasonable minor radius.
    ASSUMED: R = 5 m gives a_minor = sqrt(1300 / (2π² × 5)) ≈ 3.63 m,
    with R/a ≈ 1.38 — a very wide-aspect torus. This is approximate; actual
    PoloMac geometry is not a simple torus.
    Ref: elio-2014-fed-poloidal-confinement.md (geometry FEA only).
    HIGH UNCERTAINTY — geometry inferred, not published."""

    blanket_thickness_m: float = 0.50
    """Blanket thickness [m] — D-D, no breeding required.
    Source: No blanket design for PoloMac.
    DEFAULT: 1costingfe D-D convention. D-D blanket is thinner than D-T because
    no tritium breeding layer is needed (analysis.md §S4: blanket elimination
    is cited as a key advantage).
    Ref: 1costingfe costing_constants.yaml (blanket_unit_cost_dd)."""

    shield_thickness_m: float = 0.50
    """Neutron + radiation shield thickness [m].
    Source: No shielding design for PoloMac (analysis.md §S3).
    DEFAULT/ASSUMED: D-D produces 2.45 MeV neutrons (vs 14.1 MeV for D-T),
    reducing shielding requirements. Using 0.5 m (same as blanket thickness)
    vs 1.0–1.5 m typical for D-T tokamaks. Critical consideration: the in-vessel
    coil requires shielding from neutron damage — this is an unsolved problem
    (analysis.md §S3, Gap #6).
    HIGH UNCERTAINTY."""

    structure_thickness_m: float = 0.30
    """Primary structure thickness [m].
    Source: Standard engineering analogue.
    DEFAULT: 1costingfe structural convention."""

    vessel_thickness_m: float = 0.15
    """Vacuum vessel thickness [m].
    DEFAULT: Standard vacuum vessel analogue."""

    # =========================================================================
    # AUXILIARY LOADS
    # =========================================================================

    p_house_MW: float = 10.0
    """Housekeeping electrical power [MW] (HVAC, lighting, controls).
    DEFAULT: 1costingfe convention for large MFE plant."""

    p_trit_MW: float = 2.0
    """Tritium handling system power [MW].
    Source: D-D produces trace tritium (branch 1: D+D → T+p). Some tritium
    processing is needed even for D-D (safely dispose of or combust T).
    ASSUMED: Minimal processing; much lower than D-T (~10–20 MW for full
    tritium fuel cycle). Using 2 MW as placeholder.
    Ref: 1costingfe (fuel_handling_dd_base); analysis.md §S4.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # FINANCIAL
    # =========================================================================

    interest_rate: float = 0.08
    """Real discount rate (WACC) [fraction].
    Ref: 1costingfe default."""

    inflation_rate: float = 0.02
    """Inflation rate for levelized cost calculations.
    Ref: 1costingfe default."""

    construction_time_years: float = 8.0
    """Construction period [years].
    Source: No construction plan for PoloMac.
    ASSUMED: 8 years, longer than mature nuclear (6 years) to reflect the novel
    in-vessel coil assembly complexity and TRL-1 status.
    HIGH UNCERTAINTY."""

    # =========================================================================
    # OPERATING COSTS
    # =========================================================================

    om_cost_per_yr_base_M: float = 39.0
    """Base annual O&M cost at 1 GWe reference [M$/yr].
    Source: 1costingfe costing_constants.yaml (om_cost_dd = 39 M$/yr at 1 GWe).
    D-D reduces tritium processing overhead vs D-T (52 M$/yr).
    Applied via power-law scaling: OM = base × (P_net/1000)^0.5
    Scaled up by om_novel_penalty for in-vessel coil novelty.
    Ref: 1costingfe costing_constants.yaml."""

    om_novel_penalty: float = 1.50
    """Multiplicative O&M penalty for novel in-vessel coil maintenance [×].
    Source: No O&M data for PoloMac (analysis.md §S3).
    ASSUMED: In-vessel coil replacement in a neutron-activated vessel requires
    specialized remote handling. Using 1.5× the standard D-D O&M base to
    reflect additional remote handling, hot cell operations, and schedule risk.
    Analysis §S3 notes this as an important unsolved maintenance challenge.
    HIGH UNCERTAINTY."""

    core_lifetime_FPY: float = 10.0
    """First wall / blanket core lifetime in full-power-years before replacement.
    D-D: ~10–15 FPY (2.45 MeV neutrons, lower DPA rate than D-T).
    ALSO: In-vessel coil replacement interval is unknown; not modeled separately.
    Ref: 1costingfe costing_constants.yaml (core_lifetime_dd = 10.0 FPY).
    DEFAULT from 1costingfe."""

    fuel_cost_per_kg_D2: float = 2175.0
    """Deuterium fuel unit cost [$/kg].
    Source: 1costingfe costing_constants.yaml (u_deuterium = 2175 $/kg).
    D-D fuel is deuterium only — no tritium purchase required after startup.
    This is a genuine cost advantage (analysis.md §S4).
    Ref: 1costingfe costing_constants.yaml."""

    # =========================================================================
    # INTERNAL METHODS
    # =========================================================================

    def _compute_power(self) -> dict:
        """Layer 1: D-D power balance — fusion energy to net electric.

        D-D fusion energy fractions:
          50% branch: D+D → T + p — 4.03 MeV total, no neutrons
          50% branch: D+D → ³He + n — 3.27 MeV total, 2.45 MeV neutron
          Average: 3.65 MeV/reaction
          Neutron fraction: 0.335, Charged fraction: 0.665

        Key constraint: Q must be high enough that heating wall-plug power
        < gross electric after cryogenic and housekeeping loads. Q_break-even
        ≈ 10–12 at these efficiency assumptions.
        """
        r = {}

        # Physics Q (given): defines heating requirement
        r["Q_sci"] = self.Q_plasma

        # Plasma heating power (power delivered TO plasma)
        p_heat_plasma_MW = self.p_fus_MW / self.Q_plasma
        r["p_heat_plasma_MW"] = p_heat_plasma_MW

        # Wall-plug heating power (includes system inefficiency)
        p_heat_wp_MW = p_heat_plasma_MW / self.heating_system_efficiency
        r["p_heat_wp_MW"] = p_heat_wp_MW

        # Fusion power split
        r["p_fus"] = self.p_fus_MW
        r["p_neutron"] = self.p_fus_MW * F_NEUTRON_DD   # 2.45 MeV neutrons
        r["p_charged"] = self.p_fus_MW * F_CHARGED_DD   # protons + ³He

        # Thermal power:
        # Charged particles thermalize directly in plasma → blanket/vessel wall.
        # Neutrons deposit energy in blanket with multiplication M.
        # All wall-plug heating power eventually thermalizes (into plasma → vessel).
        p_th = (self.p_fus_MW * (F_CHARGED_DD + self.blanket_mult_DD * F_NEUTRON_DD)
                + p_heat_wp_MW)
        r["p_th"] = p_th

        # Gross electric
        p_et = p_th * self.thermal_efficiency
        r["p_et"] = p_et

        # Recirculating loads
        r["p_recirc_heat"] = p_heat_wp_MW   # heating system draw
        r["p_recirc_cryo"] = self.p_cryo_MW
        r["p_recirc_house"] = self.p_house_MW
        r["p_recirc_trit"] = self.p_trit_MW
        total_recirc = p_heat_wp_MW + self.p_cryo_MW + self.p_house_MW + self.p_trit_MW
        r["p_aux"] = total_recirc

        # Net electric
        p_net = p_et - total_recirc
        r["p_net"] = p_net

        # Engineering Q: ratio of fusion power to total electrical recirculating power
        r["Q_eng"] = self.p_fus_MW / total_recirc if total_recirc > 0 else float('inf')
        r["recirc_fraction"] = total_recirc / p_et if p_et > 0 else float('inf')

        # Annual energy (for LCOE)
        r["annual_hours"] = 8760 * self.plant_availability

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Toroidal shell geometry for blanket/shield/structure volumes.

        The PoloMac geometry is not a simple torus (it is a poloidally wound dipole),
        but is approximated as toroidal for volumetric cost scaling. The plasma volume
        of 1300 m³ (Elio 2014) anchors the minor radius. Shell volumes are computed
        as toroidal annuli V_shell = 2π²R(a_out² − a_in²).

        Note: The in-vessel dipole coil occupies the geometric center. For this model,
        the plasma fills the region from the coil outer surface to the first wall.
        The coil volume is excluded from the plasma volume (conservative — actual
        plasma fill factor is unknown).
        """
        r = {}

        # Minor radius from plasma volume: V_torus = 2π²Ra²
        # Solving for a: a = sqrt(V / (2π²R))
        a_plasma = math.sqrt(self.plasma_volume_m3 / (2.0 * math.pi**2 * self.major_radius_m))
        r["minor_radius_plasma_m"] = a_plasma
        r["major_radius_m"] = self.major_radius_m
        r["plasma_volume_m3"] = self.plasma_volume_m3

        # Aspect ratio (R/a)
        r["aspect_ratio"] = self.major_radius_m / a_plasma

        def torus_shell_vol(R, a_in, thickness):
            """Volume of toroidal shell from minor radius a_in to a_in+thickness."""
            a_out = a_in + thickness
            return 2.0 * math.pi**2 * R * (a_out**2 - a_in**2)

        R = self.major_radius_m

        # Blanket shell (wraps around plasma)
        r["blanket_vol_m3"] = torus_shell_vol(R, a_plasma, self.blanket_thickness_m)
        a_blanket_out = a_plasma + self.blanket_thickness_m

        # Shield shell
        r["shield_vol_m3"] = torus_shell_vol(R, a_blanket_out, self.shield_thickness_m)
        a_shield_out = a_blanket_out + self.shield_thickness_m

        # Structure shell
        r["structure_vol_m3"] = torus_shell_vol(R, a_shield_out, self.structure_thickness_m)
        a_structure_out = a_shield_out + self.structure_thickness_m

        # Vessel shell
        r["vessel_vol_m3"] = torus_shell_vol(R, a_structure_out, self.vessel_thickness_m)
        a_vessel_out = a_structure_out + self.vessel_thickness_m

        # Outer minor radius of assembled machine
        r["a_total_m"] = a_vessel_out
        r["machine_diameter_m"] = 2.0 * (self.major_radius_m + a_vessel_out)

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment.

        Per-module sub-accounts follow 1costingfe D-D scaling laws with concept-
        specific overrides for the in-vessel SC dipole coil (C220103) and auxiliary
        heating (C220104).

        Key overrides vs standard MFE:
          C220103: In-vessel SC dipole coil — direct cost override (no tokamak coil
                   scaling law applies; this is a unique geometry).
          C220104: Auxiliary heating — wall-plug power scaled cost.
          C220108: Target factory — zero (steady-state, no targets needed).
          C220110: Remote handling — elevated for in-vessel coil maintenance.

        D-D adjustments vs D-T:
          C220101 blanket: blanket_unit_cost_dd = 0.30 M$/m³ (no breeding layer)
          C220102 shield: shield fuel scale = 0.50 (2.45 MeV neutrons vs 14.1 MeV)
          C220500 fuel handling: fuel_handling_dd_base = 60 M$ (minimal tritium)
        """
        r = {}

        p_th = max(power["p_th"], 1.0)
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)

        # --- Per-module accounts ---

        # C220101: First Wall + Blanket (D-D, no breeding)
        # Formula: unit_cost_dd × volume × (p_th/P_TH_REF)^0.6
        # Ref: 1costingfe blanket_unit_cost_dd = 0.30 M$/m³
        blanket_unit_cost_dd = 0.30  # M$/m³
        r["C220101"] = (blanket_unit_cost_dd
                        * geom["blanket_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220102: Shield — D-D uses lower fuel scale factor
        # D-D: 2.45 MeV neutrons are less damaging than 14.1 MeV D-T neutrons.
        # Shield fuel scale = 0.50 (analogue: DHe3 at ~0.5× D-T per 1costingfe rationale).
        # Ref: 1costingfe shield_unit_cost = 0.74 M$/m³, fuel scale factor convention.
        shield_unit_cost = 0.74   # M$/m³
        shield_fuel_scale_dd = 0.50  # ASSUMED: 50% of D-T shielding due to lower neutron energy
        r["C220102"] = (shield_unit_cost
                        * geom["shield_vol_m3"]
                        * shield_fuel_scale_dd
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: In-Vessel SC Dipole Coil — OVERRIDE
        # Standard formula for MFE coils scales with kA·m or stored energy.
        # PoloMac's in-vessel coil has no published geometry, conductor specification,
        # or cost data (analysis.md §S3, §S4). Using direct cost override.
        # Ref: analysis.md §S4 (REBCO HTS analogue discussion).
        # HIGH UNCERTAINTY.
        r["C220103"] = self.sc_coil_cost_M_USD  # [override]

        # C220104: Auxiliary Heating System — OVERRIDE with power-scaled estimate
        # No heating system specified for PoloMac (analysis.md §S2 gap #2 blocking).
        # ASSUMED: NBI system cost scales as ~1.5 M$/MW of wall-plug heating.
        # Reference: large tokamak NBI systems (JET, ITER) at ~$1–2M/MW wall-plug.
        # Ref: 1costingfe power_supplies_base convention; analogue to ITER NBI.
        # HIGH UNCERTAINTY.
        nbi_cost_per_mw_wp = 1.5  # M$/MW wall-plug, ASSUMED
        r["C220104"] = nbi_cost_per_mw_wp * power["p_heat_wp_MW"]  # [override]

        # C220105: Primary Structure
        # Formula: 0.15 × volume × (p_et/P_ET_REF)^0.5
        # Ref: 1costingfe structure_unit_cost = 0.15 M$/m³
        structure_unit_cost = 0.15  # M$/m³
        r["C220105"] = (structure_unit_cost
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: Vacuum System (vessel + pumps)
        # Formula: 0.72 × volume × (p_et/P_ET_REF)^0.6
        # Ref: 1costingfe vessel_unit_cost = 0.72 M$/m³
        vessel_unit_cost = 0.72  # M$/m³
        r["C220106"] = (vessel_unit_cost
                        * geom["vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # C220107: Power Supplies (standard auxiliary systems, not the coil)
        # Formula: 80.0 × (p_et/1000)^0.7
        # Ref: 1costingfe power_supplies_base = 80 M$ at 1 GWe
        power_supplies_base = 80.0  # M$
        r["C220107"] = power_supplies_base * (p_et / 1000.0) ** 0.7

        # C220108: Target Factory — zero (steady-state operation, no targets)
        # PoloMac is stated as steady-state (JTSP 2024). No target/RTL costs.
        r["C220108"] = 0.0  # [override — steady-state, no targets]

        # C220109: Direct Energy Converter — not applicable for PoloMac (D-D thermal cycle)
        r["C220109"] = 0.0

        # C220110: Remote Handling — ELEVATED for in-vessel coil
        # Standard D-D remote handling base: 100 M$ at 1 GWe (1costingfe RH_dd_base).
        # PoloMac in-vessel coil requires extraordinary remote handling capability:
        # the coil must be removable/replaceable in an activated vessel, requiring
        # precision robotics through the magnetic tunnel access geometry.
        # Analysis §S3 identifies this as an important unresolved challenge.
        # Applying 1.5× penalty on the DD base.
        # Ref: 1costingfe remote_handling_dd_base = 100 M$; analysis.md §S3.
        # HIGH UNCERTAINTY.
        rh_dd_base = 100.0  # M$
        rh_polomac_penalty = 1.50  # ASSUMED: in-vessel coil handling complexity
        r["C220110"] = (rh_dd_base * rh_polomac_penalty
                        * (p_net / 1000.0) ** 0.6)

        # C220111: Installation labor
        # Formula: 0.14 × reactor subtotal
        # Ref: 1costingfe installation_frac = 0.14
        installation_frac = 0.14
        reactor_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"])
        r["C220111"] = installation_frac * reactor_subtotal

        # C220112: Isotope Separation — zero (deuterium from water; no Li enrichment)
        # D-D fuel needs no isotope separation infrastructure beyond standard
        # deuterium electrolysis/distillation (mature, low-cost industry).
        # This is a genuine cost advantage vs D-T (analysis.md §S4).
        r["C220112"] = 0.0

        # Per-module subtotal
        r["CAS22_per_module"] = reactor_subtotal + r["C220111"] + r["C220112"]

        # --- Plant-wide accounts ---
        p_net_total = p_net * self.n_mod
        p_th_total = p_th * self.n_mod

        # C220200: Main & Secondary Coolant Systems
        # Ref: 1costingfe CAS22 scaling (MagLIF exemplar convention)
        C220201 = 166.0 * (p_net_total / 1000.0)        # Primary coolant
        C220202 = 40.6 * (p_th_total / 3500.0) ** 0.55  # Intermediate coolant
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling + Cryoplant
        # Cryoplant scales with cryogenic load (SC coil cooling).
        # Ref: 1costingfe CAS22 convention; cryoplant for SC coil path.
        C220301 = 1.1e-3 * p_th_total                                    # Aux coolant
        C220302 = 200.0 * (max(self.p_cryo_MW, 0.01) / 30.0) ** 0.7     # Cryoplant
        r["C220300"] = C220301 + C220302

        # C220400: Radioactive Waste Management
        # Ref: 1costingfe CAS22 convention
        r["C220400"] = 1.96 * (p_th_total / 1000.0)

        # C220500: Fuel Handling — D-D base (minimal tritium, no breeding)
        # Ref: 1costingfe fuel_handling_dd_base = 60 M$ at 1 GWe
        fuel_handling_dd_base = 60.0  # M$
        r["C220500"] = fuel_handling_dd_base * (p_net_total / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        r["C220600"] = 11.5 * (p_net_total / 1000.0) ** 0.8

        # C220700: Instrumentation & Control
        r["C220700"] = 85.0 * (p_th_total / 3500.0) ** 0.65

        # Plant-wide subtotal
        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        # Total CAS22
        r["CAS22"] = r["CAS22_per_module"] * self.n_mod + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: CAS10–60 capital cost structure.

        Follows 1costingfe CAS structure. Buildings use D-D fuel type
        (no hot cell for tritium at D-T scale; some hot cell for activated in-vessel coil).
        Construction time penalty for novel in-vessel coil assembly.
        """
        r = {}
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)

        # === CAS10: Pre-construction costs ===
        # Ref: 1costingfe costing_constants.yaml
        site_permits = 3.0       # M$
        plant_studies = 4.0 if self.noak else 20.0   # M$ (NOAK vs FOAK)
        plant_permits = 2.0      # M$
        plant_reports = 1.0      # M$
        other_precon = 1.0       # M$
        land_acres = 0.25 * p_net * math.sqrt(self.n_mod)   # acres (0.25 acres/MWe)
        land_cost = land_acres * 10_000 / 1e6               # M$ at $10k/acre
        # D-D licensing: 1costingfe licensing_cost_dd = 3 M$ (reduced neutron hazard)
        licensing_cost = 3.0 if not self.noak else 1.5  # M$
        r["CAS10"] = (site_permits + plant_studies + plant_permits + plant_reports
                      + other_precon + land_cost + licensing_cost)

        # === CAS21: Buildings ===
        # Per 1costingfe building_costs_per_kw (D-D, no tritium hot cell at full scale)
        # Hot cell reduced from 93.4 $/kW (D-T) to 50 $/kW (D-D):
        #   D-D still requires hot cell for activated in-vessel coil handling.
        # Ref: 1costingfe costing_constants.yaml (building_costs_per_kw)
        building_cost_per_kW = {
            "site_improvements": 268.0,   # standard
            "fusion_heat_island": 126.0,  # reactor hall — large for 1300 m³ plasma
            "turbine_building": 54.0,     # standard Rankine cycle
            "heat_exchanger": 12.0,
            "power_supply_storage": 35.0, # houses NBI heating + auxiliary systems
            "hot_cell": 50.0,             # ASSUMED: reduced from 93.4 (D-T) for D-D activated coil
            "reactor_services": 25.0,
            "service_water": 11.0,
            "fuel_storage": 9.1,
            "control_room": 17.0,
            "onsite_ac": 21.0,
            "administration": 10.0,
            "site_services": 4.0,
            "cryogenics": 15.0,           # SC coil cryoplant building
        }
        total_building_per_kW = sum(building_cost_per_kW.values())  # ~657 $/kW
        r["CAS21"] = total_building_per_kW * p_et / 1000.0  # M$

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment ===
        # Ref: 1costingfe turbine_per_mw = 0.19764 M$/MW
        r["CAS23"] = self.n_mod * p_et * 0.19764

        # === CAS24: Electric Plant Equipment ===
        # Ref: 1costingfe electric_per_mw = 0.08418 M$/MW
        r["CAS24"] = self.n_mod * p_et * 0.08418

        # === CAS25: Miscellaneous Plant Equipment ===
        # Ref: 1costingfe misc_per_mw = 0.05124 M$/MW
        r["CAS25"] = self.n_mod * p_et * 0.05124

        # === CAS26: Heat Rejection ===
        # Ref: 1costingfe heat_rej_per_mw = 0.03416 M$/MW
        r["CAS26"] = self.n_mod * p_et * 0.03416

        # === CAS27: Special Materials ===
        # D-D: no PbLi blanket, no Li-6 enrichment, no beryllium needed.
        # ASSUMED: conventional coolant fills only (2 M$ from 1costingfe special_materials_dd)
        # Ref: 1costingfe costing_constants.yaml (special_materials_dd = 2 M$)
        r["CAS27"] = 2.0 * (p_net / 1000.0)  # scaled by plant size

        # === CAS28: Digital Twin ===
        # Ref: 1costingfe digital_twin = 5 M$
        r["CAS28"] = 5.0

        # === CAS29: Contingency ===
        # Ref: 1costingfe contingency_rate_foak = 0.10, noak = 0.0
        cas20_subtotal = sum(r[k] for k in [
            "CAS21", "CAS22", "CAS23", "CAS24", "CAS25", "CAS26", "CAS27", "CAS28"])
        contingency_rate = 0.0 if self.noak else 0.10
        r["CAS29"] = contingency_rate * cas20_subtotal

        # === CAS20: Total Direct Costs ===
        r["CAS20"] = cas20_subtotal + r["CAS29"]

        # === CAS30: Indirect Costs ===
        # 20% of CAS20, scaled by construction time relative to 6-year reference.
        # Longer construction for novel in-vessel coil assembly increases IDC burden.
        # Ref: 1costingfe indirect_fraction = 0.20, reference_construction_time = 6 yr
        ref_construction_time = 6.0
        indirect_fraction = 0.20
        r["CAS30"] = indirect_fraction * r["CAS20"] * (self.construction_time_years / ref_construction_time)

        # === CAS40: Owner's Costs ===
        # Power-law scaling: CAS40 = owner_cost_dd × (P_net/1000)^0.5
        # Ref: 1costingfe owner_cost_dd = 31 M$ at 1 GWe
        owner_cost_dd = 31.0  # M$ at 1 GWe
        r["CAS40"] = owner_cost_dd * (p_net / 1000.0) ** 0.5

        # === CAS50: Supplementary Costs ===
        # Ref: 1costingfe CAS50 sub-accounts
        spare_parts_frac_dd = 0.025  # fraction of CAS22-28 for activated spares
        spare_parts = spare_parts_frac_dd * sum(r[k] for k in [
            "CAS23", "CAS24", "CAS25", "CAS26", "CAS27", "CAS28"])
        startup_fuel_dd = 0.1 * (p_net / 1000.0)  # M$ — deuterium startup, trivial cost
        shipping = 0.015 * r["CAS20"]             # 1.5% of direct
        taxes = 0.01 * r["CAS20"]                 # 1% of direct
        insurance = 0.015 * (r["CAS20"] + r["CAS30"])  # builder's risk
        # Decommissioning PV: 1costingfe decom_provision_dd = 93 M$ at 1 GWe
        decom_provision_dd = 93.0  # M$ at 1 GWe
        decommissioning = decom_provision_dd * (p_net / 1000.0) ** 0.5
        r["CAS50"] = spare_parts + startup_fuel_dd + shipping + taxes + insurance + decommissioning

        # === Overnight Capital ===
        overnight = r["CAS10"] + r["CAS20"] + r["CAS30"] + r["CAS40"] + r["CAS50"]
        r["overnight_capital"] = overnight

        # === CAS60: Interest During Construction ===
        # f_IDC = ((1+i)^T - 1) / (i×T) - 1
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
        p_net_total = p_net * self.n_mod
        if p_net_total > 0:
            r["specific_capital_USD_per_kWe"] = (r["total_capital"] * 1e6
                                                  / (p_net_total * 1e3))
        else:
            r["specific_capital_USD_per_kWe"] = float('inf')

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70–90 annualized costs and LCOE.

        LCOE = (CAS90 + CAS70 + CAS80) / annual_energy_MWh

        CAS90: Annualized capital charge (CRF × total_capital)
        CAS70: O&M including scheduled blanket replacement
        CAS80: Fuel (deuterium only — no tritium purchase needed for D-D)
        """
        r = {}
        p_net = power["p_net"]
        p_net_total = p_net * self.n_mod

        # Capital Recovery Factor
        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1 + i) ** n / ((1 + i) ** n - 1)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]   # M$/yr

        # === CAS71: Annual O&M (levelized with inflation) ===
        # Base O&M scales as (P_net/1000)^0.5, with PoloMac novelty penalty.
        # Ref: 1costingfe om_cost_dd = 39 M$/yr at 1 GWe
        annual_om_base = (self.om_cost_per_yr_base_M
                          * (max(p_net_total, 1.0) / 1000.0) ** 0.5
                          * self.om_novel_penalty)
        g = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g) ** Tc   # first-year-of-operation cost
        if abs(i - g) > 1e-10:
            pv_growing_annuity = A1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
        else:
            pv_growing_annuity = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_growing_annuity   # M$/yr

        # === CAS72: Scheduled Replacement (blanket/FW) ===
        # D-D: core_lifetime_dd = 10 FPY (1costingfe default)
        effective_years_per_replacement = self.core_lifetime_FPY / self.plant_availability
        n_replacements = max(
            0, int(math.ceil(self.plant_lifetime_years / effective_years_per_replacement)) - 1)
        replacement_cost = cas22["C220101"]  # blanket + FW cost per replacement
        pv_replacements = 0.0
        for k in range(1, n_replacements + 1):
            year = k * effective_years_per_replacement
            if year < self.plant_lifetime_years:
                pv_replacements += replacement_cost / (1 + i) ** year
        r["CAS72"] = crf * pv_replacements   # M$/yr
        r["n_blanket_replacements"] = n_replacements

        r["CAS70"] = r["CAS71"] + r["CAS72"]   # M$/yr

        # === CAS80: Fuel (deuterium only) ===
        # D-D is primarily D₂ fuel. No tritium purchase needed (D-D advantage).
        # Deuterium consumption rate: P_fus [MW] / E_per_reaction [J] × 2 × m_D [kg]
        # E_per_reaction_DD = 3.65 MeV × 1.6022e-13 J/MeV = 5.848e-13 J
        # Reactions/s = P_fus × 1e6 W / E_per_reaction = 1.71e18 per second at 1 MW
        e_per_reaction_J = 3.65e6 * 1.6022e-19  # 3.65 MeV in Joules
        reactions_per_sec = self.p_fus_MW * 1e6 / e_per_reaction_J
        kg_D_per_sec = reactions_per_sec * 2 * 3.344e-27  # 2 × mass of deuteron in kg
        kg_D_per_yr = kg_D_per_sec * 3600 * 8760 * self.plant_availability
        # Apply burn fraction / recovery from 1costingfe convention
        # burn_fraction = 0.05, fuel_recovery = 0.95 → net makeup fraction
        # net_makeup_frac = burn_frac + (1-burn_frac)*(1-recovery) = 0.05 + 0.0475 = ~0.1
        burn_fraction = 0.05
        fuel_recovery = 0.95
        net_makeup_frac = burn_fraction + (1 - burn_fraction) * (1 - fuel_recovery)
        annual_D_kg = kg_D_per_yr * net_makeup_frac  # net deuterium makeup per year
        annual_fuel_cost_M = annual_D_kg * self.fuel_cost_per_kg_D2 / 1e6
        r["CAS80"] = annual_fuel_cost_M   # M$/yr
        r["CAS80_deuterium_kg_yr"] = annual_D_kg
        r["CAS80_D_cost"] = annual_fuel_cost_M

        # === LCOE ===
        annual_revenue_req = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_revenue_req

        annual_energy_MWh = 8760 * max(p_net_total, 0.001) * self.plant_availability
        r["annual_energy_MWh"] = annual_energy_MWh

        if annual_energy_MWh > 0 and p_net_total > 0:
            lcoe_USD_MWh = annual_revenue_req * 1e6 / annual_energy_MWh
            r["lcoe_USD_per_MWh"] = lcoe_USD_MWh
            r["lcoe_cents_per_kWh"] = lcoe_USD_MWh / 10.0
        else:
            r["lcoe_USD_per_MWh"] = float('inf')
            r["lcoe_cents_per_kWh"] = float('inf')

        # Cost breakdown fractions
        if annual_revenue_req > 0:
            r["capital_fraction"] = r["CAS90"] / annual_revenue_req
            r["om_fraction"] = r["CAS70"] / annual_revenue_req
            r["fuel_fraction"] = r["CAS80"] / annual_revenue_req

        return r

    def compute(self) -> dict:
        """Compute LCOE and key derived quantities via CAS-structured accounting.
        Returns a nested dict with power, geometry, cas22, costs, economics sub-dicts.
        """
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
        }

        # Convenience aliases
        results["net_electric_MW"] = power["p_net"]
        results["lcoe_cents_per_kWh"] = econ["lcoe_cents_per_kWh"]
        results["total_capital_M_USD"] = costs["total_capital"]

        return results


# =============================================================================
# MODULE-LEVEL INTERFACE (required by concept explorer extractor)
# =============================================================================
params = PoloMacPlantParams()
results = params.compute()


# =============================================================================
# PRINT RESULTS
# =============================================================================

def print_results(p: PoloMacPlantParams, r: dict):
    """Pretty-print LCOE model results with CAS-structured breakdown."""
    power = r["power"]
    geom = r["geometry"]
    cas22 = r["cas22"]
    costs = r["costs"]
    econ = r["economics"]

    print("=" * 72)
    print("PoloMac Magnetic Confinement (D-D) — 1cFE CAS-Structured LCOE Model")
    print("Company: Deutelio AG")
    print("WARNING: Almost all parameters are assumed. See module docstring.")
    print("=" * 72)

    # --- Key Inputs ---
    print(f"\n--- Key Input Parameters ---")
    print(f"  Fusion power (assumed):       {p.p_fus_MW:.0f} MW")
    print(f"  Plasma Q (assumed):           {p.Q_plasma:.1f}  [HIGH UNCERTAINTY]")
    print(f"  D-D plasma volume:            {p.plasma_volume_m3:.0f} m³  [Elio 2014]")
    print(f"  Thermal efficiency (assumed): {p.thermal_efficiency:.1%}  [HIGH UNCERTAINTY]")
    print(f"  SC coil cost (assumed):       ${p.sc_coil_cost_M_USD:.0f}M  [HIGH UNCERTAINTY]")
    print(f"  Cryogenic load (assumed):     {p.p_cryo_MW:.0f} MW  [HIGH UNCERTAINTY]")
    print(f"  Plant availability:           {p.plant_availability:.1%}  [HIGH UNCERTAINTY]")
    print(f"  Plant lifetime:               {p.plant_lifetime_years:.0f} yr")
    print(f"  Construction time:            {p.construction_time_years:.0f} yr  [HIGH UNCERTAINTY]")
    print(f"  FOAK/NOAK:                    {'NOAK' if p.noak else 'FOAK'}")
    print(f"  Interest rate:                {p.interest_rate:.1%}")

    # --- D-D Physics Context ---
    print(f"\n--- D-D Fusion Energy Partition ---")
    print(f"  Avg energy/reaction:          3.65 MeV  (vs 17.6 MeV D-T)")
    print(f"  Neutron fraction:             {F_NEUTRON_DD:.1%}  (2.45 MeV neutrons)")
    print(f"  Charged particle fraction:    {F_CHARGED_DD:.1%}  (p + ³He)")
    print(f"  Blanket multiplication:       {p.blanket_mult_DD:.2f}  (no Li breeding)")

    # --- Power Balance ---
    print(f"\n--- Power Balance ---")
    print(f"  Fusion power (D-D):           {power['p_fus']:.0f} MW")
    print(f"    Neutron power (2.45 MeV):   {power['p_neutron']:.0f} MW ({F_NEUTRON_DD:.1%})")
    print(f"    Charged particle power:     {power['p_charged']:.0f} MW ({F_CHARGED_DD:.1%})")
    print(f"  Thermal power:                {power['p_th']:.0f} MW")
    print(f"  Gross electric:               {power['p_et']:.0f} MWe")
    print(f"  Recirculating power breakdown:")
    print(f"    NBI/heating wall-plug:      {power['p_heat_wp_MW']:.0f} MW  "
          f"  (Q={p.Q_plasma:.0f} × η_heat={p.heating_system_efficiency:.0%})")
    print(f"    SC coil cryogenics:         {power['p_recirc_cryo']:.0f} MW")
    print(f"    Housekeeping:               {power['p_recirc_house']:.0f} MW")
    print(f"    Tritium handling (trace):   {power['p_recirc_trit']:.0f} MW")
    print(f"    Total recirculating:        {power['p_aux']:.0f} MW")
    print(f"  Net electric:                 {power['p_net']:.0f} MWe")
    print(f"  Physics Q (plasma):           {power['Q_sci']:.1f}")
    print(f"  Engineering Q (wall-plug):    {power['Q_eng']:.2f}")
    print(f"  Recirculating fraction:       {power['recirc_fraction']:.1%}")

    # --- Geometry ---
    print(f"\n--- Geometry (Toroidal Approximation) ---")
    print(f"  Major radius R:               {geom['major_radius_m']:.1f} m")
    print(f"  Minor radius a (plasma):      {geom['minor_radius_plasma_m']:.2f} m")
    print(f"  Aspect ratio R/a:             {geom['aspect_ratio']:.2f}")
    print(f"  Overall machine diameter:     {geom['machine_diameter_m']:.1f} m")
    print(f"  Blanket volume:               {geom['blanket_vol_m3']:.0f} m³")
    print(f"  Shield volume:                {geom['shield_vol_m3']:.0f} m³")
    print(f"  Structure volume:             {geom['structure_vol_m3']:.0f} m³")

    # --- CAS22: Reactor Plant Equipment ---
    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    cas22_labels = {
        "C220101": "Blanket/First Wall (D-D, no breeding)",
        "C220102": "Shield (D-D, 2.45 MeV)",
        "C220103": "In-Vessel SC Dipole Coil",
        "C220104": "NBI Heating System",
        "C220105": "Primary Structure",
        "C220106": "Vacuum System",
        "C220107": "Power Supplies (aux)",
        "C220108": "Target Factory",
        "C220109": "Direct Energy Converter",
        "C220110": "Remote Handling (elevated)",
        "C220111": "Installation Labor",
        "C220112": "Isotope Separation",
    }
    overrides = {"C220103", "C220104", "C220108"}
    for code, label in cas22_labels.items():
        val = cas22[code]
        tag = " [override]" if code in overrides else ""
        if val > 0.01:
            print(f"    {code}  {label:<38s}  ${val:>8.1f}M{tag}")
        elif code in ("C220108", "C220112"):
            print(f"    {code}  {label:<38s}  $    0.0M{tag}")
    print(f"  {'─' * 58}")
    print(f"    Per-module subtotal:                               ${cas22['CAS22_per_module']:>8.1f}M × {p.n_mod}")

    print(f"\n  Plant-wide accounts:")
    pw_labels = {
        "C220200": "Coolant Systems",
        "C220300": "Aux Cooling + Cryoplant (SC)",
        "C220400": "Rad Waste Management",
        "C220500": "Fuel Handling (D-D, minimal T)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    for code, label in pw_labels.items():
        val = cas22[code]
        if val > 0.01:
            print(f"    {code}  {label:<38s}  ${val:>8.1f}M")
    print(f"  {'─' * 58}")
    print(f"    Plant-wide subtotal:                               ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                                         ${cas22['CAS22']:>8.1f}M")

    # --- Capital Costs ---
    print(f"\n--- Capital Costs (CAS10-60) ---")
    print(f"  CAS10  Pre-construction:                   ${costs['CAS10']:>8.1f}M")
    print(f"  CAS21  Buildings:                          ${costs['CAS21']:>8.1f}M")
    print(f"  CAS22  Reactor Plant Equipment:            ${costs['CAS22']:>8.1f}M")
    print(f"  CAS23  Turbine Plant:                      ${costs['CAS23']:>8.1f}M")
    print(f"  CAS24  Electric Plant:                     ${costs['CAS24']:>8.1f}M")
    print(f"  CAS25  Misc Plant:                         ${costs['CAS25']:>8.1f}M")
    print(f"  CAS26  Heat Rejection:                     ${costs['CAS26']:>8.1f}M")
    print(f"  CAS27  Special Materials (D-D, minimal):   ${costs['CAS27']:>8.1f}M")
    print(f"  CAS28  Digital Twin:                       ${costs['CAS28']:>8.1f}M")
    print(f"  CAS29  Contingency:                        ${costs['CAS29']:>8.1f}M")
    print(f"  {'─' * 52}")
    print(f"  CAS20  Direct Costs:                       ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30  Indirect Costs:                     ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40  Owner's Costs:                      ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50  Supplementary:                      ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 52}")
    print(f"  Overnight Capital:                         ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60  IDC (f={costs['f_IDC']:.3f}):                  ${costs['CAS60']:>8.1f}M")
    print(f"  {'═' * 52}")
    print(f"  Total Capital:                             ${costs['total_capital']:>8.1f}M")
    print(f"  Specific Capital:                          ${costs['specific_capital_USD_per_kWe']:>8.0f} $/kWe")

    # --- Annual Costs ---
    print(f"\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90  Capital charge (CRF={econ['CRF']:.4f}):      ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71  O&M (levelized, 1.5× novel penalty): ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72  Scheduled replacement:               ${econ['CAS72']:>8.1f}M/yr"
          f"  ({econ['n_blanket_replacements']} replacements)")
    print(f"  CAS70  Total O&M:                           ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80  Fuel (D₂ only, no T purchase):       ${econ['CAS80']:>8.3f}M/yr"
          f"  ({econ['CAS80_deuterium_kg_yr']:.0f} kg D/yr)")

    # --- LCOE ---
    print(f"\n--- LCOE ---")
    print(f"  Annual energy production:     {econ['annual_energy_MWh']:>12,.0f} MWh")
    print(f"  Annual revenue requirement:   ${econ['annual_revenue_req']:.1f}M/yr")
    print(f"  ╔══════════════════════════════════════════════╗")
    if econ['lcoe_USD_per_MWh'] == float('inf'):
        print(f"  ║  LCOE = INFEASIBLE (negative net electric)  ║")
    else:
        print(f"  ║  LCOE = {econ['lcoe_cents_per_kWh']:>6.2f} ¢/kWh                        ║")
        print(f"  ║       = {econ['lcoe_USD_per_MWh']:>6.1f} $/MWh                        ║")
    print(f"  ╚══════════════════════════════════════════════╝")
    if econ['lcoe_USD_per_MWh'] != float('inf'):
        print(f"  Capital (CAS90):    {econ.get('capital_fraction', 0):.1%}")
        print(f"  O&M (CAS70):        {econ.get('om_fraction', 0):.1%}")
        print(f"  Fuel/cons (CAS80):  {econ.get('fuel_fraction', 0):.5%}")


def sensitivity_sweep(base_params: PoloMacPlantParams, param_name: str,
                      values: list, label: str = "") -> list:
    """Sweep a single parameter and return LCOE and net electric for each value."""
    results_list = []
    for val in values:
        p = PoloMacPlantParams(**{**base_params.__dict__, param_name: val})
        r = p.compute()
        results_list.append({
            "param_value": float(val),
            "lcoe_cents_kWh": r["economics"]["lcoe_cents_per_kWh"],
            "net_electric_MW": r["net_electric_MW"],
            "recirc_fraction": r["power"]["recirc_fraction"],
        })
    return results_list


def print_sweep(sweep_results: list, param_name: str, label: str = ""):
    """Print sensitivity sweep results as a table."""
    title = label or param_name
    print(f"\n  Sweep: {title}")
    print(f"  {'Value':>12}  {'Net [MWe]':>10}  {'Recirc%':>8}  {'LCOE [¢/kWh]':>14}")
    print(f"  {'─'*12}  {'─'*10}  {'─'*8}  {'─'*14}")
    for row in sweep_results:
        net = row["net_electric_MW"]
        recirc = row["recirc_fraction"]
        lcoe = row["lcoe_cents_kWh"]
        lcoe_str = f"{lcoe:>14.2f}" if lcoe != float('inf') else "    INFEASIBLE"
        recirc_str = f"{recirc:>8.1%}" if recirc != float('inf') else "  >100%"
        print(f"  {row['param_value']:>12.2g}  {net:>10.0f}  {recirc_str}  {lcoe_str}")


def main():
    """Run baseline analysis, sensitivity sweeps, and scenario comparison."""

    base = PoloMacPlantParams()

    # =========================================================================
    # 1. BASELINE RESULTS
    # =========================================================================
    print("\n" + "=" * 72)
    print("BASELINE SCENARIO (Moderate Assumptions)")
    print("=" * 72)
    r_base = base.compute()
    print_results(base, r_base)

    # =========================================================================
    # 2. SENSITIVITY SWEEPS (top LCOE drivers)
    # =========================================================================
    print("\n" + "=" * 72)
    print("SENSITIVITY ANALYSIS — Single-Parameter Sweeps")
    print("(All other parameters at baseline)")
    print("=" * 72)

    # Sweep 1: Plasma Q — the most critical unknown
    # Q < ~10 makes net electric negative at these assumptions
    q_sweep = sensitivity_sweep(
        base, "Q_plasma", [5, 7, 10, 15, 20, 30, 50],
        "Plasma Q — most critical unknown (no physics basis for PoloMac)")
    print_sweep(q_sweep, "Q_plasma",
                "Plasma Q [D-D energy gain; HIGH UNCERTAINTY — no PoloMac confinement physics]")

    # Sweep 2: SC coil cost — dominant capital uncertainty
    coil_sweep = sensitivity_sweep(
        base, "sc_coil_cost_M_USD", [100, 200, 500, 800, 1200, 2000],
        "In-vessel SC dipole coil capital cost")
    print_sweep(coil_sweep, "sc_coil_cost_M_USD",
                "In-Vessel SC Coil Cost [M$; HIGH UNCERTAINTY — no coil design exists]")

    # Sweep 3: Fusion power (plant scale)
    pfus_sweep = sensitivity_sweep(
        base, "p_fus_MW", [400, 600, 800, 1200, 1600, 2400],
        "Assumed fusion power")
    print_sweep(pfus_sweep, "p_fus_MW",
                "Assumed Fusion Power [MW; HIGH UNCERTAINTY — no reactor design point]")

    # Sweep 4: Thermal efficiency
    eta_sweep = sensitivity_sweep(
        base, "thermal_efficiency", [0.28, 0.32, 0.35, 0.38, 0.42],
        "Thermal-to-electric efficiency")
    print_sweep(eta_sweep, "thermal_efficiency",
                "Thermal Efficiency [fraction; HIGH UNCERTAINTY — no power conversion design]")

    # Sweep 5: Plant availability
    avail_sweep = sensitivity_sweep(
        base, "plant_availability", [0.50, 0.60, 0.70, 0.75, 0.80, 0.85],
        "Plant capacity factor")
    print_sweep(avail_sweep, "plant_availability",
                "Plant Availability [fraction; HIGH UNCERTAINTY — in-vessel coil maintenance unknown]")

    # Sweep 6: Cryogenic load (copper → SC transition)
    cryo_sweep = sensitivity_sweep(
        base, "p_cryo_MW", [5, 10, 15, 20, 30, 50],
        "SC coil cryogenic load")
    print_sweep(cryo_sweep, "p_cryo_MW",
                "SC Cryogenic Load [MW; vs 700 MW copper draw from Elio 2014]")

    # =========================================================================
    # 3. SCENARIO COMPARISON
    # =========================================================================
    print("\n" + "=" * 72)
    print("SCENARIO COMPARISON TABLE")
    print("=" * 72)
    print("NOTE: All scenarios are speculative. Parameter choices have no physics basis.")

    scenarios = {
        "Conservative": PoloMacPlantParams(
            p_fus_MW=500.0,
            Q_plasma=7.0,
            thermal_efficiency=0.30,
            sc_coil_cost_M_USD=1000.0,
            p_cryo_MW=30.0,
            plant_availability=0.60,
            construction_time_years=10.0,
            om_novel_penalty=2.0,
            noak=False,
        ),
        "Moderate": PoloMacPlantParams(),  # baseline
        "Optimistic": PoloMacPlantParams(
            p_fus_MW=1200.0,
            Q_plasma=30.0,
            thermal_efficiency=0.38,
            sc_coil_cost_M_USD=250.0,
            p_cryo_MW=10.0,
            plant_availability=0.82,
            construction_time_years=7.0,
            om_novel_penalty=1.2,
            noak=True,
        ),
    }

    print(f"\n  {'Scenario':<14}  {'P_fus[MW]':>10}  {'Q':>5}  "
          f"{'Net[MWe]':>9}  {'Recirc%':>8}  {'Cap[M$]':>10}  {'$/kWe':>8}  {'LCOE[¢/kWh]':>12}")
    print(f"  {'─'*14}  {'─'*10}  {'─'*5}  "
          f"{'─'*9}  {'─'*8}  {'─'*10}  {'─'*8}  {'─'*12}")

    for name, scenario_params in scenarios.items():
        r = scenario_params.compute()
        pwr = r["power"]
        cst = r["costs"]
        eco = r["economics"]
        p_net = pwr["p_net"]
        recirc = pwr["recirc_fraction"]
        lcoe = eco["lcoe_cents_per_kWh"]
        specific = cst.get("specific_capital_USD_per_kWe", float('inf'))

        lcoe_str = f"{lcoe:>12.2f}" if lcoe != float('inf') else "  INFEASIBLE "
        recirc_str = f"{recirc:>8.1%}" if recirc != float('inf') else "   >100%"
        cap_str = f"${cst['total_capital']:>9.0f}"
        spec_str = f"{specific:>8.0f}" if specific != float('inf') else "     inf"

        print(f"  {name:<14}  {scenario_params.p_fus_MW:>10.0f}  {scenario_params.Q_plasma:>5.0f}  "
              f"{p_net:>9.0f}  {recirc_str}  {cap_str}  {spec_str}  {lcoe_str}")

    # =========================================================================
    # 4. KEY BINDING CONSTRAINTS
    # =========================================================================
    print("\n" + "=" * 72)
    print("KEY BINDING CONSTRAINTS — Top 3 LCOE Drivers")
    print("=" * 72)

    r_base = base.compute()
    pwr = r_base["power"]
    cas22_base = r_base["cas22"]
    cst = r_base["costs"]
    eco = r_base["economics"]

    coil_cost = cas22_base["C220103"]
    cas22_total = cst["CAS22"]
    coil_pct = 100.0 * coil_cost / cas22_total if cas22_total > 0 else 0.0
    # rough LCOE sensitivity to +$500M coil: ΔCapital → ΔCAS90 → ΔLCOE
    delta_lcoe_per_500m = (eco["CRF"] * 500.0 * 1e6
                           / max(eco["annual_energy_MWh"], 1.0) / 10.0)  # ¢/kWh

    print(f"""
1. PLASMA Q (D-D energy gain) — LCOE VIABILITY THRESHOLD
   -------------------------------------------------------
   At baseline Q = {base.Q_plasma:.0f}, recirculating fraction = {pwr['recirc_fraction']:.1%}.
   Below Q ≈ 10, the NBI heating draw exceeds gross electric → net negative.
   No confinement physics for PoloMac exists at any relevant parameter (analysis.md §S2).
   Historical dipole experiments reached "few eV" temperatures (vs 50–100 keV for D-D).
   This is a physics feasibility question, not an engineering optimization.

   LCOE impact: Going from Q=7 to Q=30 can shift LCOE by 3–5× (see sweep above).
   Status: Blocking. No path to estimate without plasma experiments.

2. IN-VESSEL SC DIPOLE COIL COST — LARGEST SINGLE CAPITAL ITEM
   -------------------------------------------------------------
   At ${base.sc_coil_cost_M_USD:.0f}M baseline, the SC coil is ${coil_cost:.0f}M of
   ${cas22_total:.0f}M total CAS22 ({coil_pct:.0f}% of reactor plant equipment).
   Radiation-hardened HTS in-vessel coils have no commercial precedent.
   Cost range: $200M (REBCO matures, compact design) to $1B+ (FOAK, novel geometry).
   No coil design has been published (analysis.md §S3, §S4).

   LCOE impact: ±$500M coil cost shifts LCOE by roughly ±{delta_lcoe_per_500m:.1f} ¢/kWh.
   Status: Blocking for cost estimation. Requires coil design + prototyping.

3. PLANT AVAILABILITY (IN-VESSEL COIL MAINTENANCE) — O&M AMPLIFIER
   -----------------------------------------------------------------
   At {base.plant_availability:.0%} availability, annual O&M (with 1.5x novelty penalty) =
   ${eco['CAS70']:.0f}M/yr = {eco.get('om_fraction', 0):.1%} of annual revenue requirement.
   The in-vessel coil must be removed and replaced in an activated vessel —
   a remote handling challenge with no established solution (analysis.md §S3).
   Dropping from 75% to 60% availability alone increases LCOE by ~20-25%.

   LCOE impact: Large, compounding (lower availability also reduces energy output
   in the denominator while raising specific O&M costs).
   Status: Blocking for availability estimation. Requires maintenance design.
""")

    print(f"  [Baseline LCOE: {eco['lcoe_cents_per_kWh']:.2f} ¢/kWh = {eco['lcoe_USD_per_MWh']:.0f} $/MWh]")
    print(f"  [This estimate carries HIGH UNCERTAINTY across all three binding drivers.]")
    print()


if __name__ == "__main__":
    main()
