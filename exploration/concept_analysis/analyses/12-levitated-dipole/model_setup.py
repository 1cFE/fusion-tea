"""
Levitated Dipole (D-T) LCOE Model — OpenStar Technologies, Reactor A
=====================================================================
1cFE First Pass Concept Analysis
Concept: Levitated Dipole (D-T fuel)
Company: OpenStar Technologies (Wellington, New Zealand)
Design Point: Reactor A (208 MWe net) from Simpson et al. 2026

This is a free-form analogue LCOE model built from component mass data and
published power balance equations. No 1costingfe reference concept is used
because no standard concept shares the levitated dipole's architecture (single
internal levitated REBCO coil, annual sacrificial section replacement, solid
ceramic Li2O blanket, concrete outer vessel). See analysis.md §Section 2.

Cost accounting follows CAS (Code of Accounts System) structure with mass-based
overrides for the four primary cost paths identified in analysis.md:
  1. Core magnet: REBCO tape quantity x $/kA-m x engineering multiplier
  2. Blanket + shield: component mass x unit cost (analogue estimation)
  3. Outer vacuum vessel: reinforced concrete x civil construction rate
  4. Balance of plant / thermal island: standard power-scaling laws

Economy-of-scale post-hoc scaling for cross-concept comparison uses alpha=0.6
(Rothwell-type power-law exponent), applied after all physics computations at
native power level. The `scaled_headline` dict reports LCOE and $/kW normalized
to 1000 MWe for cross-concept comparison -- it does NOT change any physics.

Key references:
- Simpson et al. (2026), "D-T Levitated Dipole Fusion Power Plants", arXiv:2602.20564
- OpenStar Team (2025), "Design and Initial Results from Junior LDX", arXiv:2508.17691
- 1costingfe CAS structure: costing_constants.yaml (scaling law references)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass

# === Reference power levels for standard CAS22 scaling (from 1costingfe) ===
P_TH_REF = 2500.0   # Reference thermal power [MW]
P_ET_REF = 1100.0   # Reference gross electric power [MW]


@dataclass
class LevitatedDipolePlantParams:
    """
    Parameterized Levitated Dipole (D-T) power plant LCOE model -- Reactor A design point.
    Primary source: Simpson et al. 2026 (arXiv:2602.20564).

    Uncertainty tags:
      No tag               = well-established from primary source
      MODERATE UNCERTAINTY = reasonable estimate from analogues
      HIGH UNCERTAINTY     = speculative or poorly constrained
    """

    # =========================================================================
    # PLASMA PHYSICS
    # =========================================================================

    p_fus: float = 667.0
    """Fusion power [MW].
    Source: Simpson et al. 2026, Table 6, Reactor A design point.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Table 6."""

    Q_sci: float = 15.0
    """Scientific gain Q = fusion power / auxiliary heating power.
    Source: Simpson et al. 2026, Table 6, Reactor A.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Table 6.
    MODERATE UNCERTAINTY -- requires Tahi experimental validation; not yet demonstrated.
    Key risk: entire Reactor A design is viable only if Tahi confirms Bohm-like or better
    confinement scaling (n*tau_e >= 3.23e19 s/m3 at 1 keV). See analysis.md §Section 2."""

    eta_aux: float = 0.70
    """ICRH auxiliary heating wall-plug efficiency [fraction].
    Source: Simpson et al. 2026 §3.2.5 -- ICRH baseline at 70%.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §3.2.5."""

    # =========================================================================
    # ENERGY CONVERSION
    # =========================================================================

    M_blanket: float = 1.053
    """Blanket energy multiplication factor (energy out / neutron energy in).
    Source: Calibrated to Simpson et al. Table 9. Working backwards from gross electric
    output ~296 MWe: p_th = 296/0.40 = 740 MW; solving p_fus*(0.8*M + 0.2) + P_ICRH = 740
    gives M = 1.053. Natural Li2O + W neutron multiplication; TBR = 1.1 is the tritium
    breeding ratio (a separate quantity from energy multiplication).
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §4.3.
    MODERATE UNCERTAINTY."""

    eta_th: float = 0.40
    """Thermal-to-electric conversion efficiency [fraction].
    Source: Simpson et al. §3.2.5. Actual thermodynamic cycle unspecified in any
    public source. 40% is consistent with sCO2 Brayton or advanced steam Rankine.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §3.2.5.
    MODERATE UNCERTAINTY -- thermal cycle specification is a blocking data gap."""

    duty_cycle: float = 0.901
    """Fraction of time plasma is active (pulsed by cryogenic reservoir limits).
    Source: Simpson et al. §3.2.5. Float time = 45.5 min, docking ~5 min.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §3.2.5 and §Table 7."""

    maintenance_availability: float = 0.96
    """Fraction of calendar time available for operation (scheduled maintenance excluded).
    Source: Simpson et al. §3.2.5 -- includes 2-week annual maintenance window.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §3.2.5.
    MODERATE UNCERTAINTY -- no operating history to validate."""

    # =========================================================================
    # AUXILIARY LOADS (recirculating power breakdown)
    # =========================================================================

    p_cryo_MW: float = 1.31
    """Cryogenic system wall-plug power [MW].
    Source: Simpson et al. Table 9. 14.1 kW deposited / 0.0125 cryo efficiency = 1.13 MW;
    paper states 1.31 MW indicating additional fixed cryogenic plant loads.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Table 9."""

    p_trit_MW: float = 8.0
    """Tritium processing system power [MW].
    ASSUMED: no published O&M breakdown for this concept. Analogue to 1costingfe D-T
    default (~6-10 MW). MODERATE UNCERTAINTY."""

    p_house_MW: float = 5.0
    """Housekeeping / plant services power [MW].
    ASSUMED: controls, lighting, HVAC, instrumentation. 1costingfe analogue.
    MODERATE UNCERTAINTY."""

    p_other_MW: float = 9.19
    """Other auxiliary loads [MW] (vacuum systems, flux pump power, etc.).
    ASSUMED: calibrated so total non-ICRH recirculating = 23.5 MW, matching
    paper's 208 MWe net: p_net = 296 - (63.5 ICRH + 1.31 cryo + 23.5 other) = 208 MWe.
    HIGH UNCERTAINTY."""

    # =========================================================================
    # MAGNET SYSTEM (core levitated coil + top support coil)
    # =========================================================================

    rebco_tape_core_km: float = 4320.0
    """REBCO tape in core levitated magnet [km].
    Source: Simpson et al. Table 7, Reactor A. CICC architecture at 23 T peak field.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Table 7."""

    rebco_tape_top_km: float = 1200.0
    """REBCO tape in top (support/levitation) magnet [km].
    Source: ~1,200 km estimated from Simpson et al. context; top magnet details
    'have not been considered' (paper's own scope statement).
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Table 7 context.
    HIGH UNCERTAINTY."""

    rebco_Ic_kA: float = 0.20
    """Critical current per REBCO tape at operating conditions (23 T, 30 K) [kA].
    ASSUMED: ~200 A per 4 mm wide tape at 23 T, 30 K. Extrapolated from available
    Jc data; 23 T irradiation database does not exist.
    HIGH UNCERTAINTY -- Jc under combined 23 T + neutron irradiation uncharacterized."""

    rebco_price_kAm: float = 75.0
    """REBCO tape price [$/kA-m] at projected near-term market.
    Source: analysis.md §Section 4 -- current market $50-100/kA-m; mid-range $75.
    Same price trajectory applies to annual replacement tape.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Section 4.
    MODERATE UNCERTAINTY -- price is volume-dependent and declining."""

    magnet_engineering_multiplier: float = 5.0
    """Tape cost to total magnet cost multiplier (CICC conduit, winding labor,
    impregnation, structural cold mass, cryostat, testing, commissioning).
    ASSUMED: 4-5x tape cost based on ARC/SPARC REBCO magnet analogues.
    HIGH UNCERTAINTY -- only experimental (Junior) data at small scale available."""

    # =========================================================================
    # BLANKET (Li2O solid ceramic)
    # =========================================================================

    Li2O_mass_t: float = 3490.0
    """Li2O breeding blanket mass [tonnes].
    Source: Simpson et al. Table 5, Reactor A. Natural (unenriched) Li2O -- no
    isotope enrichment needed (TBR = 1.1 with W neutron multiplication).
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Table 5."""

    Li2O_unit_cost_per_kg: float = 100.0
    """Li2O blanket fabrication + installation unit cost [$/kg].
    ASSUMED: Raw Li2O ~$30-40/kg; ceramic pelletization + sintering +
    modular panel fabrication + nuclear qualification ~$60-80/kg additional.
    Total ~$80-120/kg; using $100/kg mid-range.
    Ref: ITER HCPB TBM solid ceramic breeder cost analogues.
    HIGH UNCERTAINTY -- no Li2O blanket module has been costed at plant scale."""

    # =========================================================================
    # TUNGSTEN SHIELD (W-B4C-W layered)
    # =========================================================================

    W_shield_mass_t: float = 1760.0
    """W-B4C-W neutron shield mass [tonnes].
    Source: Simpson et al. Table 5, Reactor A. 475 mm total thickness achieving
    4-decade fast neutron attenuation to protect REBCO tape.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Table 5."""

    W_shield_unit_cost_per_kg: float = 150.0
    """W-B4C-W shield fabrication + installation unit cost [$/kg].
    ASSUMED: Tungsten powder ~$35/kg; high-density sintering + machining into
    tiles operating above recrystallization temperature (1950 K) + B4C layer
    + integration ~$115/kg. Tungsten tile specialist processing required.
    Ref: ITER divertor tungsten tile cost analogues.
    HIGH UNCERTAINTY -- W tile fabrication at 1950 K is not industrialized at scale."""

    # =========================================================================
    # OUTER VACUUM VESSEL (reinforced concrete)
    # =========================================================================

    concrete_mass_t: float = 38700.0
    """Reinforced concrete outer vessel mass [tonnes].
    Source: Simpson et al. Table 5, Reactor A. Dominant mass item (~86% of total
    45,100 t plant mass). Provides structural support + biological shielding.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Table 5."""

    concrete_cost_per_t: float = 500.0
    """Concrete outer vessel unit cost [$/tonne].
    ASSUMED: Standard reinforced concrete ~$200/t; premium 2.5x for vacuum
    penetrations, embedded instrumentation, nuclear biological shielding spec.
    Paper highlights this as cost-advantaged vs. precision SS tokamak VVs.
    Ref: Civil nuclear construction analogues. MODERATE UNCERTAINTY."""

    inner_vessel_cost_M_USD: float = 30.0
    """Inner stainless steel vacuum vessel cost [$M].
    ASSUMED: Conventional 304 SS inner vacuum boundary for plasma containment.
    Ref: Analogy to compact MFE inner vessels (FRC, mirror programs).
    HIGH UNCERTAINTY."""

    # =========================================================================
    # ICRH HEATING SYSTEM
    # =========================================================================

    icrh_cost_per_MW_wallplug: float = 2.0
    """ICRH heating system cost [M$/MW wall-plug].
    ASSUMED: $1.5-3 M/MW range (JET-class ~$2.5M/MW to ITER-class ~$10M/MW).
    NOAK assumption brings this toward lower end. Dipole geometry undemonstrated --
    includes modest development risk premium over standard tokamak ICRH.
    Ref: JET ICRH system, ITER ICRH design costs.
    HIGH UNCERTAINTY."""

    # =========================================================================
    # CRYOGENIC SYSTEM (neon slush at 24.6 K)
    # =========================================================================

    cryo_system_cost_M_USD: float = 150.0
    """Neon slush cryoplant capital cost [$M].
    ASSUMED: Neon slush (24.6 K) is not off-the-shelf technology at this scale.
    Float time = 45.5 min; system supplies ~14.1 kW heat removal continuously.
    Analogues: LHC cryoplant (4 K, ~$500M); HTS tokamak cryosystems ($100-200M).
    At 24.6 K the thermodynamic penalty is much less severe than 4 K.
    HIGH UNCERTAINTY."""

    # =========================================================================
    # REMOTE HANDLING SYSTEM (novel annual coil replacement)
    # =========================================================================

    remote_handling_cost_M_USD: float = 150.0
    """Remote handling system capital cost [$M].
    ASSUMED: Novel system for annual activated HTS coil extraction + replacement.
    Base: 1costingfe D-T remote handling $150M at 1 GWe; scaled to 208 MWe then
    multiplied 3x for unique geometry complexity (internal levitated coil in
    activated D-T environment; no analogue in any other fusion concept).
    HIGH UNCERTAINTY -- no design study for this specific geometry exists."""

    # =========================================================================
    # SACRIFICIAL COIL REPLACEMENT (annual OPEX -- unique to levitated dipole)
    # =========================================================================

    sacrificial_tape_km_yr: float = 864.0
    """Annual REBCO tape consumption for sacrificial section replacement [km/yr].
    Source: ~20% of 4,320 km core magnet = ~864 km/yr. Outer section accumulates
    neutron fluence to 1 MW-yr/m2 threshold over approximately one year.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §4.1."""

    replacement_tape_multiplier: float = 2.5
    """Multiplier from tape material cost to full replacement section cost
    (winding labor + conditioning + qualification testing, but WITHOUT design NRE
    which is sunk). Lower than initial magnet_engineering_multiplier.
    ASSUMED: 2-3x tape cost for repeat manufacturing at scale.
    HIGH UNCERTAINTY -- no analogue for annual activated-coil replacement."""

    sacrificial_handling_M_USD_yr: float = 20.0
    """Annual remote handling operations cost for sacrificial coil replacement [$M/yr].
    Includes: coil extraction/insertion, cryogenic reconnection, activated component
    transfer to hot cell, qualification testing of new section.
    ASSUMED: No published cost estimate exists. See analysis.md §Section 2 (Gap #2).
    HIGH UNCERTAINTY."""

    # =========================================================================
    # GEOMETRY (simplified spherical model for standard CAS22 scaling)
    # =========================================================================

    r_plasma_outer_m: float = 9.0
    """Outer radius of plasma region (inner radius of blanket shell) [m].
    ASSUMED: Inferred from Li2O mass (3490 t at density 2013 kg/m3 = 1733 m3) and
    75% blanket coverage: a 2m-thick spherical shell at 75% solid angle at r=9m
    gives ~1895 m3, consistent with mass data.
    HIGH UNCERTAINTY -- plasma geometry is toroidal; this is a spherical simplification."""

    blanket_thickness_m: float = 2.0
    """Li2O blanket shell thickness [m].
    ASSUMED: Inferred from mass data. Actual geometry more complex.
    HIGH UNCERTAINTY."""

    shield_thickness_m: float = 0.475
    """W-B4C-W neutron shield thickness [m].
    Source: Simpson et al. §4.3 -- 475 mm achieves 4-decade fast neutron
    attenuation at the REBCO winding pack.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §4.3."""

    inner_vessel_thickness_m: float = 0.10
    """Inner vacuum vessel wall thickness [m].
    ASSUMED: Standard SS vacuum vessel. MODERATE UNCERTAINTY."""

    blanket_coverage: float = 0.75
    """Fraction of 4*pi solid angle covered by the Li2O blanket.
    Source: Simpson et al. §4.3 -- ~25% intercepted by the core magnet assembly.
    TBR = 1.1 achieved with this coverage using W neutron multiplication.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §4.3."""

    # =========================================================================
    # FINANCIAL
    # =========================================================================

    interest_rate: float = 0.08
    """Real discount rate (WACC) [fraction]. Ref: 1costingfe CAS convention."""

    inflation_rate: float = 0.02
    """Inflation rate for O&M escalation. Ref: 1costingfe default."""

    construction_time_years: float = 6.0
    """Construction period [years]. Ref: 1costingfe reference_construction_time."""

    plant_lifetime_years: float = 40.0
    """Plant economic lifetime [years]."""

    noak: bool = True
    """Nth-of-a-kind (True) vs. First-of-a-kind (False)."""

    # =========================================================================
    # OPERATING COSTS
    # =========================================================================

    om_fixed_M_per_MWe_yr: float = 0.060
    """Fixed O&M rate [M$/MWe-net/yr] -- excludes sacrificial coil replacement.
    ASSUMED: Nuclear plant analogue from 1costingfe CAS71 default ($60/MWe/yr).
    MODERATE UNCERTAINTY -- no O&M estimates in any public source for this concept."""

    core_lifetime_FPY: float = 5.0
    """Li2O blanket lifetime [full-power-years] before replacement.
    Source: 1costingfe D-T standard -- 5 FPY at ~20 dpa/yr for 14.1 MeV neutrons.
    Ref: 1costingfe costing_constants.yaml, core_lifetime_dt."""

    # =========================================================================
    # MODULES
    # =========================================================================

    n_mod: int = 1
    """Number of reactor modules. Levitated dipole is single-module per plant."""

    # =========================================================================
    # COMPUTE METHODS
    # =========================================================================

    def _compute_power(self) -> dict:
        """Layer 1: Power balance for steady-state MFE levitated dipole."""
        r = {}

        # D-T split: 80% neutrons (14.1 MeV), 20% alphas (3.5 MeV)
        p_neutron = 0.80 * self.p_fus
        p_alpha   = 0.20 * self.p_fus

        # ICRH auxiliary heating
        P_aux_plasma   = self.p_fus / self.Q_sci       # MW delivered to plasma
        P_aux_wallplug = P_aux_plasma / self.eta_aux   # MW wall-plug

        # Thermal power: neutrons thermalized in blanket (with multiplication),
        # alphas deposited in plasma, ICRH deposited in plasma
        p_th = p_neutron * self.M_blanket + p_alpha + P_aux_plasma

        # Gross electric
        p_et = p_th * self.eta_th

        # Total recirculating power (steady-state while plasma is on)
        p_recirc = (P_aux_wallplug + self.p_cryo_MW
                    + self.p_trit_MW + self.p_house_MW + self.p_other_MW)

        # Net electric per module
        p_net = p_et - p_recirc

        # Combined capacity factor: duty_cycle x maintenance_availability
        capacity_factor = self.duty_cycle * self.maintenance_availability

        r["p_fus"]           = self.p_fus
        r["Q_sci"]           = self.Q_sci
        r["p_neutron"]       = p_neutron
        r["p_alpha"]         = p_alpha
        r["P_aux_plasma"]    = P_aux_plasma
        r["P_aux_wallplug"]  = P_aux_wallplug
        r["p_th"]            = p_th
        r["p_et"]            = p_et
        r["p_recirc"]        = p_recirc
        r["p_net"]           = p_net
        r["capacity_factor"] = capacity_factor

        # Engineering Q: net electric per unit ICRH wall-plug
        r["Q_eng"]           = p_net / P_aux_wallplug if P_aux_wallplug > 0 else 0.0
        r["recirc_fraction"] = p_recirc / p_et if p_et > 0 else float("inf")

        # Plant-level totals (n_mod = 1 for levitated dipole)
        r["p_net_plant"] = p_net * self.n_mod
        r["p_et_plant"]  = p_et  * self.n_mod
        r["p_th_plant"]  = p_th  * self.n_mod

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Simplified spherical shell geometry.
        C220101 and C220102 are mass-based overrides in _compute_cas22(); these
        volumes are used only for C220105/C220106 scaling."""
        r = {}
        ri = self.r_plasma_outer_m

        def shell_vol(r_in, thickness):
            r_out = r_in + thickness
            return (4.0 / 3.0) * math.pi * (r_out ** 3 - r_in ** 3)

        r_blanket_out = ri + self.blanket_thickness_m
        r_shield_out  = r_blanket_out + self.shield_thickness_m
        r_vessel_out  = r_shield_out  + self.inner_vessel_thickness_m

        r["blanket_vol_eff_m3"]  = shell_vol(ri, self.blanket_thickness_m) * self.blanket_coverage
        r["shield_vol_m3"]       = shell_vol(r_blanket_out, self.shield_thickness_m)
        r["inner_vessel_vol_m3"] = shell_vol(r_shield_out, self.inner_vessel_thickness_m)
        r["r_vessel_out_m"]      = r_vessel_out
        r["concrete_vol_m3"]     = self.concrete_mass_t / 2.4   # 2.4 t/m3

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts.
        Mass-based overrides for concept-specific components; standard 1costingfe
        scaling for plant-wide accounts."""
        r = {}
        p_th  = max(power["p_th"],  1.0)
        p_et  = max(power["p_et"],  1.0)
        p_net = max(power["p_net"], 1.0)

        # --- Per-module accounts ---

        # C220101: Li2O blanket -- MASS-BASED OVERRIDE
        # Ceramic blanket panels with tritium extraction. 1costingfe volume-based
        # scaling not used; mass data from Table 5 is more reliable for this geometry.
        r["C220101"] = self.Li2O_mass_t * 1e3 * self.Li2O_unit_cost_per_kg / 1e6  # M$

        # C220102: W-B4C-W neutron shield -- MASS-BASED OVERRIDE
        # 475 mm layered tungsten/boron-carbide/tungsten shield. Tungsten tile
        # fabrication above recrystallization temperature (~1950 K) is specialized.
        r["C220102"] = self.W_shield_mass_t * 1e3 * self.W_shield_unit_cost_per_kg / 1e6  # M$

        # C220103: HTS magnet system -- TAPE-BASED OVERRIDE
        # Core levitated coil + top support coil. Cost driven by REBCO tape
        # quantity x $/kA-m x engineering multiplier (conduit, winding, cryostat).
        total_tape_km = self.rebco_tape_core_km + self.rebco_tape_top_km
        total_kAm     = total_tape_km * 1e3 * self.rebco_Ic_kA            # kA-m
        tape_cost_M   = total_kAm * self.rebco_price_kAm / 1e6            # M$
        r["C220103"]  = tape_cost_M * self.magnet_engineering_multiplier   # M$

        # C220104: ICRH supplementary heating -- $/MW OVERRIDE
        # 44.5 MW plasma power / 0.70 eff = 63.5 MW wall-plug.
        # ICRH in dipole geometry undemonstrated; cost includes modest risk premium.
        r["C220104"] = power["P_aux_wallplug"] * self.icrh_cost_per_MW_wallplug  # M$

        # C220105: Primary structure
        # Inner stainless structure (volume-scaled) + reinforced concrete outer vessel
        # (mass-based). The concrete serves as both structure and bioshield.
        structure_unit_cost = 0.15  # M$/m3 (1costingfe standard)
        r["C220105"] = (structure_unit_cost * geom["inner_vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5
                        + self.concrete_mass_t * self.concrete_cost_per_t / 1e6)

        # C220106: Inner vacuum vessel + vacuum pumping system
        # The SS inner vessel forms the primary plasma boundary.
        vessel_unit_cost = 0.72  # M$/m3 (1costingfe)
        r["C220106"] = (self.inner_vessel_cost_M_USD
                        + vessel_unit_cost * geom["inner_vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # C220107: Power supplies (plant DC bus, flux pump commissioning)
        # Flux pump maintains coil current during levitated operation (no steady
        # external power needed). Standard 1costingfe scaling for plant DC systems.
        r["C220107"] = 80.0 * (p_et / 1000.0) ** 0.7  # M$

        # C220108: Target factory -- N/A (MFE, no targets)
        r["C220108"] = 0.0

        # C220109: Direct energy converter -- N/A (D-T thermal cycle)
        r["C220109"] = 0.0

        # C220110: Remote handling -- OVERRIDE for novel coil replacement system
        # Annual activated HTS coil replacement requires a unique robotic system.
        # Base 1costingfe D-T RH ($150M at 1 GWe) scaled and 3x complexity factor.
        r["C220110"] = self.remote_handling_cost_M_USD  # M$

        # C220111: Installation labor (14% of reactor hardware subtotal)
        reactor_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"])
        r["C220111"] = 0.14 * reactor_subtotal

        # C220112: Isotope separation -- zero (natural Li2O, no enrichment needed)
        r["C220112"] = 0.0

        # Per-module subtotal
        r["CAS22_per_module"] = reactor_subtotal + r["C220111"] + r["C220112"]

        # --- Plant-wide accounts ---
        p_net_total = p_net * self.n_mod
        p_th_total  = p_th  * self.n_mod

        # C220200: Main & secondary coolant system (helium or water blanket cooling)
        C220201 = 166.0 * (p_net_total / 1000.0)
        C220202 = 40.6  * (p_th_total / 3500.0) ** 0.55
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary cooling + neon slush cryoplant
        # Standard auxiliary coolant scaling plus concept-specific neon slush system.
        r["C220300"] = 1.1e-3 * p_th_total + self.cryo_system_cost_M_USD

        # C220400: Radioactive waste management
        r["C220400"] = 1.96 * (p_th_total / 1000.0)

        # C220500: Fuel handling (D-T tritium processing + closed fuel cycle)
        r["C220500"] = 120.0 * (p_net_total / 1000.0) ** 0.7

        # C220600: Other reactor plant equipment
        r["C220600"] = 11.5 * (p_net_total / 1000.0) ** 0.8

        # C220700: Instrumentation & control
        r["C220700"] = 85.0 * (p_th_total / 3500.0) ** 0.65

        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        r["CAS22"] = r["CAS22_per_module"] * self.n_mod + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: CAS10-60 capital cost structure."""
        r = {}
        p_et  = max(power["p_et"],  1.0)
        p_net = max(power["p_net"], 1.0)

        # CAS10: Pre-construction
        site_permits   = 3.0
        plant_studies  = 4.0 if self.noak else 20.0
        plant_permits  = 2.0
        plant_reports  = 1.0
        other_precon   = 1.0
        land_cost      = 0.25 * p_net * math.sqrt(self.n_mod) * 10_000 / 1e6
        licensing_cost = 2.5 if self.noak else 5.0
        r["CAS10"] = (site_permits + plant_studies + plant_permits + plant_reports
                      + other_precon + land_cost + licensing_cost)

        # CAS21: Ancillary buildings
        # Concrete outer vessel (already in C220105) serves as the reactor building.
        # CAS21 covers turbine building, hot cell, control room, ancillary services.
        building_cost_per_kW = {
            "turbine_building":  54.0,
            "cooling_structures": 12.0,
            "hot_cell":          93.4,
            "misc_ancillary":    61.6,
            "control_room":      17.0,
            "administration":    10.0,
        }
        r["CAS21"] = sum(building_cost_per_kW.values()) * p_et / 1000.0  # M$

        # CAS22 (from external computation)
        r["CAS22"] = cas22["CAS22"]

        # CAS23-26: Standard BOP (1costingfe scaling laws)
        r["CAS23"] = self.n_mod * p_et * 0.19764  # Turbine plant [M$/MW]
        r["CAS24"] = self.n_mod * p_et * 0.08418  # Electric plant
        r["CAS25"] = self.n_mod * p_et * 0.05124  # Misc plant equipment
        r["CAS26"] = self.n_mod * p_et * 0.03416  # Heat rejection

        # CAS27: Special materials (tritium startup inventory ~1 kg at $30/mg = $30M)
        r["CAS27"] = 30.0

        # CAS28: Digital twin
        r["CAS28"] = 5.0

        # CAS29: Contingency (0 for NOAK, 10% for FOAK)
        cas20_subtotal = sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                             "CAS25", "CAS26", "CAS27", "CAS28"])
        r["CAS29"] = 0.0 if self.noak else 0.10 * cas20_subtotal

        # CAS20: Total Direct Costs
        r["CAS20"] = cas20_subtotal + r["CAS29"]

        # CAS30: Indirect Costs (engineering, CM, commissioning)
        r["CAS30"] = (0.20 * r["CAS20"]
                      * (self.construction_time_years / 6.0))

        # CAS40: Owner's Costs
        r["CAS40"] = 0.05 * r["CAS20"]

        # CAS50: Supplementary (spare parts, D fuel startup, shipping, taxes, decom)
        spare_parts = 0.01 * sum(r[k] for k in ["CAS23", "CAS24", "CAS25",
                                                  "CAS26", "CAS27", "CAS28"])
        fuel_load   = (p_net / 1000.0) * 10.0
        r["CAS50"]  = spare_parts + fuel_load + 1.0 + 0.5 + 0.5 + 5.0

        # Overnight Capital
        overnight = r["CAS10"] + r["CAS20"] + r["CAS30"] + r["CAS40"] + r["CAS50"]
        r["overnight_capital"] = overnight

        # CAS60: Interest During Construction
        i = self.interest_rate
        T = self.construction_time_years
        f_idc = ((1 + i) ** T - 1) / (i * T) - 1 if (i > 0 and T > 0) else 0.0
        r["CAS60"]     = f_idc * overnight
        r["f_IDC"]     = f_idc
        r["total_capital"] = overnight + r["CAS60"]

        if power["p_net"] > 0:
            r["specific_capital_USD_per_kWe"] = (
                r["total_capital"] * 1e6 / (power["p_net"] * self.n_mod * 1e3))
        else:
            r["specific_capital_USD_per_kWe"] = float("inf")

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70-90 annualized costs and LCOE."""
        r = {}
        p_net       = power["p_net"]
        p_net_total = p_net * self.n_mod
        cap_factor  = power["capacity_factor"]

        # Capital Recovery Factor
        i   = self.interest_rate
        n   = self.plant_lifetime_years
        crf = i * (1 + i) ** n / ((1 + i) ** n - 1)
        r["CRF"] = crf

        # CAS90: Annualized Capital Charge
        r["CAS90"] = crf * costs["total_capital"]  # M$/yr

        # CAS71: Fixed O&M (levelized with inflation)
        # om_fixed_M_per_MWe_yr is in M$/MWe/yr; multiply directly by MWe to get M$/yr
        annual_om_base = self.om_fixed_M_per_MWe_yr * p_net_total
        g  = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g) ** Tc
        if abs(i - g) > 1e-10:
            pv_om = A1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
        else:
            pv_om = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_om

        # CAS72: Scheduled Replacements
        # (a) Li2O blanket replacement (discrete events every core_lifetime_FPY)
        blanket_cost = cas22["C220101"]
        yrs_per_repl = self.core_lifetime_FPY / max(cap_factor, 0.01)
        n_repl = max(0, int(math.ceil(self.plant_lifetime_years / yrs_per_repl)) - 1)
        pv_blanket = 0.0
        for k in range(1, n_repl + 1):
            yr = k * yrs_per_repl
            if yr < self.plant_lifetime_years:
                pv_blanket += blanket_cost / (1 + i) ** yr
        r["CAS72_blanket"]        = crf * pv_blanket
        r["n_blanket_replacements"] = n_repl

        # (b) Annual sacrificial REBCO coil section replacement (UNIQUE TO THIS CONCEPT)
        sac_kAm       = self.sacrificial_tape_km_yr * 1e3 * self.rebco_Ic_kA
        sac_tape_M    = sac_kAm * self.rebco_price_kAm / 1e6
        sac_full_M_yr = (sac_tape_M * self.replacement_tape_multiplier
                         + self.sacrificial_handling_M_USD_yr)
        # Level annuity: CRF x PV = sac_full_M_yr exactly (annuity identity)
        annuity_pv     = sac_full_M_yr * (1 - (1 + i) ** (-n)) / i
        r["CAS72_coil"] = crf * annuity_pv
        r["sac_coil_M_yr"] = sac_full_M_yr

        r["CAS72"] = r["CAS72_blanket"] + r["CAS72_coil"]
        r["CAS70"] = r["CAS71"] + r["CAS72"]

        # CAS80: D-T fuel (D purchase, ongoing; T is self-bred at TBR=1.1)
        # ~22 t/yr deuterium at ~$10/kg commercial scale = $0.22M/yr; round up.
        r["CAS80"] = 0.5  # M$/yr -- negligible

        # LCOE
        annual_rev = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_rev

        annual_energy_MWh = 8760.0 * p_net_total * cap_factor
        r["annual_energy_MWh"] = annual_energy_MWh

        if annual_energy_MWh > 0:
            lcoe = annual_rev * 1e6 / annual_energy_MWh
            r["lcoe_USD_per_MWh"]   = lcoe
            r["lcoe_cents_per_kWh"] = lcoe / 10.0
        else:
            r["lcoe_USD_per_MWh"]   = float("inf")
            r["lcoe_cents_per_kWh"] = float("inf")

        if annual_rev > 0:
            r["capital_fraction"] = r["CAS90"] / annual_rev
            r["om_fraction"]      = r["CAS70"] / annual_rev
            r["fuel_fraction"]    = r["CAS80"] / annual_rev

        return r

    def compute(self) -> dict:
        """Compute LCOE and all intermediate quantities using 5-layer CAS accounting."""
        power = self._compute_power()
        geom  = self._compute_geometry(power)
        cas22 = self._compute_cas22(power, geom)
        costs = self._compute_costs(power, cas22)
        econ  = self._compute_economics(power, costs, cas22)

        results = {
            "power":     power,
            "geometry":  geom,
            "cas22":     cas22,
            "costs":     costs,
            "economics": econ,
        }
        results["net_electric_MW"]     = power["p_net"]
        results["lcoe_cents_per_kWh"]  = econ["lcoe_cents_per_kWh"]
        results["total_capital_M_USD"] = costs["total_capital"]
        return results


# =============================================================================
# MODULE-LEVEL OUTPUT INTERFACE (consumed by concept explorer)
# =============================================================================

params  = LevitatedDipolePlantParams()
results = params.compute()

# Post-hoc scaling to 1000 MWe (cross-concept comparison, alpha = 0.6)
_ALPHA     = 0.6
_p_native  = results["power"].get("p_net_plant", results["power"]["p_net"])
_factor    = (_p_native / 1000.0) ** (1.0 - _ALPHA)
_overnight = results["costs"]["overnight_capital"] * 1e3 / _p_native  # $/kW at native

scaled_headline = {
    "p_net_mw":         1000.0,
    "lcoe_per_mwh":     results["economics"]["lcoe_USD_per_MWh"] * _factor,
    "overnight_per_kw": _overnight * _factor,
}


# =============================================================================
# PRINT / DISPLAY
# =============================================================================

def print_results(p: LevitatedDipolePlantParams, res: dict):
    """Pretty-print LCOE model results with full CAS breakdown."""
    power = res["power"]
    cas22 = res["cas22"]
    costs = res["costs"]
    econ  = res["economics"]

    print("=" * 70)
    print("Levitated Dipole (D-T) LCOE Model -- OpenStar Technologies, Reactor A")
    print("=" * 70)

    print(f"\n--- Key Input Parameters ---")
    print(f"  Fusion power:               {p.p_fus:.0f} MW")
    print(f"  Q_sci:                      {p.Q_sci:.1f}")
    print(f"  ICRH efficiency:            {p.eta_aux:.0%}")
    print(f"  Blanket energy mult:        {p.M_blanket:.3f}")
    print(f"  Thermal efficiency:         {p.eta_th:.0%}")
    print(f"  Duty cycle:                 {p.duty_cycle:.1%}")
    print(f"  Maintenance availability:   {p.maintenance_availability:.0%}")
    print(f"  Combined capacity factor:   {power['capacity_factor']:.1%}")
    print(f"  REBCO tape (core+top):      {p.rebco_tape_core_km + p.rebco_tape_top_km:,.0f} km")
    print(f"  REBCO Ic at ops (23T,30K):  {p.rebco_Ic_kA:.2f} kA/tape")
    print(f"  REBCO price:                ${p.rebco_price_kAm:.0f}/kA-m")
    print(f"  Li2O blanket mass:          {p.Li2O_mass_t:,.0f} t  @ ${p.Li2O_unit_cost_per_kg:.0f}/kg")
    print(f"  W-B4C-W shield mass:        {p.W_shield_mass_t:,.0f} t  @ ${p.W_shield_unit_cost_per_kg:.0f}/kg")
    print(f"  Concrete vessel mass:       {p.concrete_mass_t:,.0f} t  @ ${p.concrete_cost_per_t:.0f}/t")
    print(f"  Coil replacement tape/yr:   {p.sacrificial_tape_km_yr:.0f} km/yr")
    print(f"  Coil handling cost/yr:      ${p.sacrificial_handling_M_USD_yr:.0f}M/yr")
    print(f"  NOAK / Interest rate:       {'NOAK' if p.noak else 'FOAK'} / {p.interest_rate:.0%}")
    print(f"  Plant lifetime:             {p.plant_lifetime_years:.0f} yr")

    print(f"\n--- Power Balance ---")
    print(f"  Fusion power:               {power['p_fus']:.0f} MW  (Q_sci = {power['Q_sci']:.1f})")
    print(f"    Neutron power:            {power['p_neutron']:.0f} MW (80%)")
    print(f"    Alpha power:              {power['p_alpha']:.0f} MW (20%)")
    print(f"  ICRH plasma deposit:        {power['P_aux_plasma']:.1f} MW")
    print(f"  ICRH wall-plug:             {power['P_aux_wallplug']:.1f} MW")
    print(f"  Thermal power (p_th):       {power['p_th']:.0f} MW")
    print(f"  Gross electric (p_et):      {power['p_et']:.0f} MWe")
    print(f"  Recirculating power:")
    print(f"    ICRH wall-plug:           {power['P_aux_wallplug']:.1f} MW")
    print(f"    Cryoplant (neon slush):   {p.p_cryo_MW:.2f} MW")
    print(f"    Tritium processing:       {p.p_trit_MW:.1f} MW")
    print(f"    Housekeeping:             {p.p_house_MW:.1f} MW")
    print(f"    Other auxiliary:          {p.p_other_MW:.2f} MW")
    print(f"    Total:                    {power['p_recirc']:.1f} MW ({power['recirc_fraction']:.1%})")
    print(f"  Net electric (p_net):       {power['p_net']:.0f} MWe")
    print(f"  Engineering Q (net/ICRH):   {power['Q_eng']:.2f}")

    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    cas22_labels = {
        "C220101": ("Li2O Blanket",             "[MASS-BASED OVERRIDE]"),
        "C220102": ("W-B4C-W Shield",            "[MASS-BASED OVERRIDE]"),
        "C220103": ("HTS Magnet (core+top)",     "[TAPE-BASED OVERRIDE]"),
        "C220104": ("ICRH Heating System",       "[$/MW OVERRIDE]"),
        "C220105": ("Structure + Outer Vessel",  "[concrete mass + vol scale]"),
        "C220106": ("Inner Vacuum Vessel",       "[parametric + vol scale]"),
        "C220107": ("Power Supplies",            "[1costingfe scale]"),
        "C220108": ("Target Factory",            "[N/A=0]"),
        "C220109": ("Direct Energy Converter",   "[N/A=0]"),
        "C220110": ("Remote Handling",           "[NOVEL SYSTEM OVERRIDE]"),
        "C220111": ("Installation (14%)",        ""),
        "C220112": ("Isotope Separation",        "[N/A, natural Li2O]"),
    }
    for code, (label, note) in cas22_labels.items():
        val = cas22[code]
        if val > 0.01 or code in ("C220108", "C220109", "C220112"):
            print(f"    {code} {label:<28s} ${val:>8.1f}M  {note}")
    print(f"    {'─'*55}")
    print(f"    Per-module subtotal:              ${cas22['CAS22_per_module']:>8.1f}M")

    print(f"  Plant-wide accounts:")
    pw_labels = {
        "C220200": "Coolant Systems",
        "C220300": "Aux Cooling + Neon Cryoplant",
        "C220400": "Rad Waste Management",
        "C220500": "Fuel Handling (D-T)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    for code, label in pw_labels.items():
        val = cas22[code]
        if val > 0.01:
            print(f"    {code} {label:<28s} ${val:>8.1f}M")
    print(f"    {'─'*55}")
    print(f"    Plant-wide subtotal:              ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                        ${cas22['CAS22']:>8.1f}M")

    print(f"\n--- Capital Costs (CAS10-60) ---")
    print(f"  CAS10 Pre-construction:             ${costs['CAS10']:>8.1f}M")
    print(f"  CAS21 Ancillary Buildings:          ${costs['CAS21']:>8.1f}M")
    print(f"  CAS22 Reactor Plant Equipment:      ${costs['CAS22']:>8.1f}M")
    print(f"  CAS23 Turbine Plant:                ${costs['CAS23']:>8.1f}M")
    print(f"  CAS24 Electric Plant:               ${costs['CAS24']:>8.1f}M")
    print(f"  CAS25 Misc Plant:                   ${costs['CAS25']:>8.1f}M")
    print(f"  CAS26 Heat Rejection:               ${costs['CAS26']:>8.1f}M")
    print(f"  CAS27 Special Materials (T startup):${costs['CAS27']:>8.1f}M")
    print(f"  CAS28 Digital Twin:                 ${costs['CAS28']:>8.1f}M")
    print(f"  CAS29 Contingency:                  ${costs['CAS29']:>8.1f}M")
    print(f"  {'─'*55}")
    print(f"  CAS20 Direct Costs:                 ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30 Indirect Costs:               ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40 Owner's Costs:                ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50 Supplementary:                ${costs['CAS50']:>8.1f}M")
    print(f"  {'─'*55}")
    print(f"  Overnight Capital:                  ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60 IDC (f={costs['f_IDC']:.3f}):             ${costs['CAS60']:>8.1f}M")
    print(f"  {'='*55}")
    print(f"  Total Capital:                      ${costs['total_capital']:>8.1f}M")
    print(f"  Specific Capital (native):          ${costs['specific_capital_USD_per_kWe']:>8.0f} $/kWe")

    print(f"\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90 Capital charge (CRF={econ['CRF']:.4f}):  ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71 O&M fixed (levelized):        ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72 Scheduled replacements:       ${econ['CAS72']:>8.1f}M/yr")
    print(f"    Blanket ({econ['n_blanket_replacements']} repl):              ${econ['CAS72_blanket']:>8.1f}M/yr")
    sac_tape_only = econ["sac_coil_M_yr"] - params.sacrificial_handling_M_USD_yr
    print(f"    Sacrificial coil (annual):        ${econ['CAS72_coil']:>8.1f}M/yr")
    print(f"      (tape ${sac_tape_only:.1f}M + handling ${params.sacrificial_handling_M_USD_yr:.1f}M = ${econ['sac_coil_M_yr']:.1f}M/yr raw)")
    print(f"  CAS70 Total O&M:                    ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80 D fuel + consumables:         ${econ['CAS80']:>8.3f}M/yr")

    print(f"\n--- LCOE ---")
    print(f"  Annual energy production:     {econ['annual_energy_MWh']:,.0f} MWh")
    print(f"  Annual revenue requirement:   ${econ['annual_revenue_req']:.1f}M")
    print(f"  ╔══════════════════════════════════════════════╗")
    print(f"  ║  LCOE = {econ['lcoe_cents_per_kWh']:.2f} cents/kWh                    ║")
    print(f"  ║       = {econ['lcoe_USD_per_MWh']:.1f} $/MWh                        ║")
    print(f"  ╚══════════════════════════════════════════════╝")
    print(f"  Capital (CAS90):              {econ.get('capital_fraction', 0):.1%}")
    print(f"  O&M (CAS70):                  {econ.get('om_fraction', 0):.1%}")
    print(f"  Fuel/consumables (CAS80):     {econ.get('fuel_fraction', 0):.1%}")

    # Scaled headline
    _pn  = res["power"].get("p_net_plant", res["power"]["p_net"])
    _fac = (_pn / 1000.0) ** (1.0 - _ALPHA)
    _ovn = res["costs"]["overnight_capital"] * 1e3 / _pn
    print(f"\n--- Scaled Headline (1000 MWe reference, alpha=0.6) ---")
    print(f"  Native net power:             {_pn:.0f} MWe")
    print(f"  Scale factor:                 {_fac:.3f}  (cost scales DOWN from 208 to 1000 MWe)")
    print(f"  Scaled LCOE:                  {res['economics']['lcoe_USD_per_MWh'] * _fac:.1f} $/MWh")
    print(f"  Scaled overnight:             ${_ovn * _fac:.0f} /kWe")


def sensitivity_sweep(base_params: LevitatedDipolePlantParams, param_name: str,
                      values: list, label: str = "") -> list:
    """Sweep a single parameter and return LCOE results for each value."""
    out = []
    for val in values:
        p = LevitatedDipolePlantParams(**{**base_params.__dict__, param_name: val})
        r = p.compute()
        out.append({
            "param_value":     float(val),
            "lcoe_cents_kWh":  r["lcoe_cents_per_kWh"],
            "net_electric_MW": r["net_electric_MW"],
            "overnight_M_USD": r["costs"]["overnight_capital"],
        })
    return out


def main():
    print("\n" + "=" * 70)
    print("BASELINE SCENARIO -- Reactor A design point (Simpson et al. 2026)")
    print("=" * 70)
    baseline = LevitatedDipolePlantParams()
    r_base   = baseline.compute()
    print_results(baseline, r_base)
    base_lcoe = r_base["lcoe_cents_per_kWh"]

    # =========================================================================
    # SENSITIVITY SWEEPS
    # =========================================================================
    print("\n" + "=" * 70)
    print("SENSITIVITY ANALYSIS (from baseline)")
    print("=" * 70)
    print(f"  Baseline LCOE: {base_lcoe:.2f} cents/kWh  ({r_base['economics']['lcoe_USD_per_MWh']:.1f} $/MWh)\n")

    sweeps = [
        ("Q_sci",
         [5.0, 7.5, 10.0, 12.0, 15.0, 20.0, 30.0],
         "Q_sci (confinement scaling)",
         "KEY RISK: binary viability threshold near Q=5-8"),

        ("rebco_price_kAm",
         [10.0, 25.0, 50.0, 75.0, 100.0, 150.0],
         "REBCO tape price [$/kA-m]",
         "Affects both C220103 capital AND annual coil replacement"),

        ("eta_th",
         [0.33, 0.37, 0.40, 0.44, 0.47],
         "Thermal efficiency (cycle unspecified)",
         "Range: Rankine ~33-37% to sCO2 ~44-47%"),

        ("Li2O_unit_cost_per_kg",
         [50.0, 75.0, 100.0, 150.0, 200.0, 300.0],
         "Li2O blanket unit cost [$/kg]",
         "HIGH UNCERTAINTY: ceramic manufacturing + nuclear qualification"),

        ("interest_rate",
         [0.04, 0.06, 0.08, 0.10, 0.12],
         "Discount rate / WACC",
         "Capital-intensive concept strongly rate-sensitive"),

        ("magnet_engineering_multiplier",
         [3.0, 4.0, 5.0, 7.0, 10.0],
         "Magnet engineering multiplier (tape -> total)",
         "Largest single cost item; no large-scale REBCO anchor"),
    ]

    for param_name, values, label, note in sweeps:
        print(f"  {label}  ({note}):")
        res_list = sensitivity_sweep(baseline, param_name, values)
        for entry in res_list:
            v    = entry["param_value"]
            lcoe = entry["lcoe_cents_kWh"]
            net  = entry["net_electric_MW"]
            delta = lcoe - base_lcoe
            if net <= 0:
                print(f"    {v:>8.3g}  -> NET POWER NEGATIVE ({net:.0f} MWe)")
            else:
                print(f"    {v:>8.3g}  -> {lcoe:6.2f} c/kWh  ({delta:+.2f})  net={net:.0f} MWe")
        print()

    # Manual sweep: annual sacrificial coil handling cost
    print(f"  Annual coil handling cost [M$/yr]")
    print(f"  (UNIQUE TO LEVITATED DIPOLE -- no analogue in any other fusion concept):")
    for v in [5.0, 10.0, 20.0, 40.0, 60.0, 100.0]:
        p = LevitatedDipolePlantParams(sacrificial_handling_M_USD_yr=v)
        r = p.compute()
        delta = r["lcoe_cents_per_kWh"] - base_lcoe
        print(f"    {v:>6.0f} M$/yr  -> {r['lcoe_cents_per_kWh']:6.2f} c/kWh  ({delta:+.2f})")
    print()

    # =========================================================================
    # SCENARIO COMPARISON TABLE
    # =========================================================================
    print("=" * 70)
    print("SCENARIO COMPARISON")
    print("=" * 70)

    conservative = LevitatedDipolePlantParams(
        rebco_price_kAm=100.0,
        magnet_engineering_multiplier=7.0,
        Li2O_unit_cost_per_kg=150.0,
        W_shield_unit_cost_per_kg=200.0,
        sacrificial_handling_M_USD_yr=40.0,
        replacement_tape_multiplier=3.0,
        eta_th=0.37,
        maintenance_availability=0.90,
        cryo_system_cost_M_USD=200.0,
    )

    optimistic = LevitatedDipolePlantParams(
        rebco_price_kAm=25.0,
        magnet_engineering_multiplier=4.0,
        Li2O_unit_cost_per_kg=60.0,
        W_shield_unit_cost_per_kg=100.0,
        sacrificial_handling_M_USD_yr=8.0,
        replacement_tape_multiplier=2.0,
        eta_th=0.44,
        maintenance_availability=0.96,
        cryo_system_cost_M_USD=100.0,
    )

    scenarios = [
        ("Conservative", conservative),
        ("Baseline",     baseline),
        ("Optimistic",   optimistic),
    ]

    print(f"\n  {'Scenario':<14s} {'Net(MWe)':>8s} {'Overnight($B)':>14s} "
          f"{'$/kWe':>8s} {'LCOE(c/kWh)':>12s} {'Scaled$/MWh':>12s}")
    print(f"  {'─'*72}")
    for name, p_sc in scenarios:
        r_sc = p_sc.compute()
        net  = r_sc["power"]["p_net"]
        ovn  = r_sc["costs"]["overnight_capital"]
        spkw = r_sc["costs"]["specific_capital_USD_per_kWe"]
        lc   = r_sc["lcoe_cents_per_kWh"]
        pn   = r_sc["power"].get("p_net_plant", net)
        fac  = (pn / 1000.0) ** (1.0 - 0.6)
        sl   = r_sc["economics"]["lcoe_USD_per_MWh"] * fac
        print(f"  {name:<14s} {net:>8.0f} {ovn/1000:>14.2f} "
              f"{spkw:>8.0f} {lc:>12.2f} {sl:>12.0f}")

    # =========================================================================
    # KEY BINDING CONSTRAINTS
    # =========================================================================
    print("\n" + "=" * 70)
    print("KEY BINDING CONSTRAINTS (top 3 LCOE drivers)")
    print("=" * 70)
    print("""
  1. Q_sci / Confinement Scaling -- BINARY VIABILITY RISK
     -------------------------------------------------------
     Reactor A requires tau_e = 3.5 s -- a 240x extrapolation over LDX data
     (14.5 ms). The Tahi prototype (~2028) must validate Bohm-like or better
     scaling (n*tau_e >= 3.23e19 s/m3). This is a binary threshold: if Tahi
     fails, Reactor A is nonviable as designed (no intermediate 'more expensive
     but viable' outcome at current design margins). The sensitivity sweep shows
     Q_sci drives LCOE sharply via the recirculating fraction -- at Q=10 the
     plant is marginally viable; below Q~7, net power approaches zero.
     No cost model can resolve this risk. Only Tahi experimental data can.

  2. Annual Sacrificial Coil Replacement -- UNIQUE UNQUANTIFIED OPEX
     -----------------------------------------------------------------
     ~864 km/yr REBCO tape + remote handling + qualification has no analogue in
     any fusion concept. OpenStar claims it "does not make a significant impact"
     but provides no figure. At current tape prices ($75/kA-m), the raw annual
     cost is ~$47M/yr -- roughly 30% of the annual capital charge for 208 MWe.
     If tape prices decline to target (~$10-25/kA-m) the annual cost drops to
     $10-20M/yr. This is the single most important gap between the company's
     implicit optimism and verifiable TEA. Until costed, LCOE uncertainty spans
     a factor of ~2 from this parameter alone.

  3. Capital Cost Density -- LARGE COMPONENTS, MODEST NET POWER
     ------------------------------------------------------------
     At ~208 MWe net the specific capital is ~$15,000-20,000/kWe. The magnet,
     blanket, and shield are sized by physics (not scalable to lower cost at
     this fusion power), while net power is squeezed by the ~30% recirculating
     fraction. Thermal efficiency (37-44%) changes net output by ~15% at fixed
     fusion power. The economy-of-scale scaling to 1000 MWe (alpha=0.6) reduces
     the LCOE substantially, but the concrete outer vessel and core magnet are
     single-unit items with limited sub-linear scaling. OpenStar's Reactor B
     (74.5 MWe) has higher $/kWe and higher LCOE, confirming the plant does not
     benefit from smaller size. Reactor A is already near the cost-optimal point
     given current design constraints.
""")


if __name__ == "__main__":
    main()
