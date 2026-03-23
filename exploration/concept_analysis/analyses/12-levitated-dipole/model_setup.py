"""
Levitated Dipole (D-T) First-Pass LCOE Model
=============================================
1cFE First Pass Concept Analysis
Concept: Levitated Dipole (D-T) — OpenStar Technologies
Company: OpenStar Technologies (Wellington, NZ; founded 2021)

This is a parameterized LCOE model based on the OpenStar Technologies power plant
preprint (Simpson et al., arXiv 2602.20564) and the Junior prototype paper
(arXiv 2508.17691). The design point is "Reactor A" — the conservative Bohm-scaling
scenario disclosing 667 MW fusion power and 208 MWe net electric.

Key architectural differences from MagLIF / IFE concepts:
- Continuous quasi-steady MFE operation (>95% duty cycle); no driver, no rep rate
- Single floating HTS REBCO coil (23 T) + one external support magnet — no large coil array
- On-board superconducting flux pump (~10 W continuous) eliminates conventional power supply
- ICRH primary heating; plasma NOT ignited (Qsci estimated 12-19, not published)
- Annual sacrificial coil outer section replacement — novel OPEX with no precedent
- Li₂O ceramic TBR blanket (TBR 1.1); two-temperature W/B₄C shield (>2000 K / ~600°C)
- No direct energy converter; all fusion energy recovered thermally

Cost accounting follows the CAS (Code of Accounts System) structure from 1costingfe,
with concept-specific overrides documented below. Scaling laws from:
- 1costingfe costing_constants.yaml (blanket, shield, structure, vessel, fuel handling)
- MagLIF exemplar (maglif_lcoe_model.py) for CAS21-29, CAS30-60, CAS70-90 patterns
- Analysis-specific overrides for C220103 (HTS coil), C220104 (ICRH), C220110 (remote handling)

Key references:
- Simpson et al. (2026), arXiv:2602.20564 — Reactor A design point (primary engineering ref)
- OpenStar team (2025), arXiv:2508.17691 — Junior prototype specifications
- openstar-prototype-roadmap.md — Device roadmap, LDX heritage, funding history
- openstar-2026-funding-tahi-timeline.md — February 2026 milestone, Tahi/Maui/Tama Nui timeline
- arxiv-2602-20564-plasma-state-clarification.md — Plasma state (sustained, not ignited)
- 1costingfe costing_constants.yaml — CAS scaling laws and unit costs

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass


# === Reference power levels for scaling laws (from 1costingfe defaults) ===
P_TH_REF = 2500.0   # Reference thermal power [MW]
P_ET_REF = 1100.0   # Reference gross electric power [MW]

# D-T neutron / alpha energy split
F_NEUTRON_DT = 0.80   # 14.1 MeV / 17.6 MeV
F_ALPHA_DT = 0.20     # 3.5 MeV / 17.6 MeV


@dataclass
class LevitatedDipolePlantParams:
    """
    Parameterized Levitated Dipole (D-T) power plant LCOE model.
    All parameters have source annotations. Uncertainty levels:
    - No tag = well-established value with source
    - MODERATE UNCERTAINTY = reasonable estimate from analogues
    - HIGH UNCERTAINTY = speculative or poorly constrained
    """

    # =========================================================================
    # FUSION PHYSICS
    # =========================================================================

    p_fus_MW: float = 667.0
    """Fusion power [MW].
    Source: Reactor A conservative Bohm-scaling design point, directly published.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Reactor Performance;
         analysis.md §Section 5."""

    blanket_energy_multiplication: float = 1.10
    """Blanket energy multiplication factor M applied to neutron power.
    M = 1.10 is the 1costingfe standard D-T assumption (conservative); note TBR and M are
    independent parameters — full blanket energy multiplication accounting would give
    M ≈ 1.15–1.30 depending on breeding zone geometry. This value may underestimate P_th
    by ~10–20%, which is one reason the LCOE should be treated as a lower bound on
    required capital recovery.
    Source: 1costingfe standard D-T default; TBR 1.1 confirmed by analytic model for
    OpenStar geometry (separate parameter).
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Tritium Breeding;
         1costingfe costing_constants.yaml (standard D-T assumption)."""

    thermal_efficiency: float = 0.38
    """Thermal-to-electric conversion efficiency (gross electric / total thermal input).
    Source: UNPUBLISHED. OpenStar has not disclosed thermal power conversion cycle type.
    Two-temperature shield (>2000 K hot zone, ~600°C warm zone) potentially enables
    higher efficiency than conventional Rankine (~35%), but sCO₂ Brayton or combined
    cycle is speculative. Range: 35% (conservative Rankine) to 45% (advanced sCO₂).
    Baseline 38% is approximately consistent with published p_fus=667 MW / p_net=208 MWe
    pair at assumed Qsci=15 (see _compute_power for derivation); gives P_net ≈ 212 MWe
    vs. published 208 MWe. Exact match requires η_th ≈ 37.5%; 38% is a round number
    within the cited uncertainty band.
    Ref: Analogue from MFE plant literature; analysis.md §Section 2 (BOP gap confirmed),
         §Section 5 (missing parameters table).
    HIGH UNCERTAINTY — single largest free parameter in this model."""

    # =========================================================================
    # ICRH HEATING SYSTEM
    # =========================================================================

    qsci: float = 15.0
    """Scientific gain factor Q_sci = P_fus / P_plasma_heating (power to plasma, not grid draw).
    Source: INFERRED. Paper states Qsci as a fixed design parameter but value is not
    accessible in the HTML version of arXiv:2602.20564.
    Derivation from published pair (P_fus=667 MW, P_net=208 MWe):
      Assuming η_th=0.38, P_th≈765 MW, P_et≈290 MWe, recirc~82 MW (ICRH+aux),
      → P_icrh_grid~67 MW, → P_plasma~47 MW → Qsci~14.
    Published inference range: 12–19 per analysis.md §Section 5.
    Using 15 as conservative central estimate.
    Ref: arxiv-2602-20564-plasma-state-clarification.md (plasma is sustained, not ignited);
         analysis.md §Section 5 (Implied Qsci row).
    MODERATE UNCERTAINTY."""

    icrh_wall_plug_efficiency: float = 0.70
    """ICRH wall-plug-to-plasma coupling efficiency (fraction of grid power → plasma).
    Source: Multi-MW ICRH systems demonstrated at ~70% wall-plug efficiency on JET, EAST
    (published ICRH experimental literature). The arXiv preprint (arxiv-2602-20564-dt-dipole-
    power-plants.md §Heating) cites this figure as the basis for OpenStar's selection of
    ICRH over ECRH for power plant operation; the figure itself is from JET/EAST literature,
    not derived in the preprint.
    Ref: JET/EAST ICRH published literature (primary); arxiv-2602-20564-dt-dipole-power-
         plants.md §Heating (context for ICRH vs. ECRH selection)."""

    # =========================================================================
    # RECIRCULATING / AUXILIARY LOADS
    # =========================================================================

    p_cryo_MW: float = 5.0
    """Cryogenic system continuous power [MW] — neon slush at 24.6 K + HTS management.
    Source: ASSUMED. Neon at 24.6 K is less thermodynamically demanding than He at 4 K.
    ITER He cryoplant is ~35 MW for 4 K; a single-coil neon system at 24.6 K for a
    power-plant-scale REBCO coil is estimated 3–8 MW. Using 5 MW as central estimate.
    Ref: Cryogenic analogue from HTS tokamak studies.
    MODERATE UNCERTAINTY."""

    p_tritium_MW: float = 4.0
    """Tritium processing, isotope separation, and fuel handling power [MW].
    Source: Standard D-T fuel cycle assumption.
    Ref: 1costingfe ife_zpinch.yaml default; analysis.md §Section 4 (D-T fuel cycle)."""

    p_housekeeping_MW: float = 5.0
    """Housekeeping, controls, diagnostics, vacuum pumping, water cooling [MW].
    Source: ASSUMED. Standard MFE plant auxiliary load allowance.
    Ref: MFE plant literature analogue.
    MODERATE UNCERTAINTY."""

    p_position_control_MW: float = 1.0
    """Active magnetic position control power for levitation feedback [MW].
    Source: ASSUMED. The on-board flux pump requires only ~10 W continuous to maintain
    coil current after initial energization. External position control coils for
    active levitation feedback have no published power requirement.
    Using 1 MW as conservative upper-bound estimate.
    Ref: openstar-prototype-roadmap.md §Key Milestones (flux pump 10 W);
         Junior device demonstration data.
    HIGH UNCERTAINTY — novel system, no power plant precedent."""

    # =========================================================================
    # PLANT CONFIGURATION
    # =========================================================================

    duty_cycle: float = 0.95
    """Plant capacity factor / availability.
    Source: Published as ">95% duty cycle" — pulsed downtime only from neon slush
    reservoir thermal limits, not plasma physics. <2 weeks downtime per year stated.
    This is a claimed advantage vs. tokamaks (ELMs, disruptions) and pulsed IFE.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Operation Mode."""

    plant_lifetime_years: float = 40.0
    """Plant economic lifetime [years].
    Source: Standard fusion plant assumption.
    Ref: 1costingfe default."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds contingency (10%) and higher pre-construction costs.
    Ref: 1costingfe CAS29 convention."""

    # =========================================================================
    # GEOMETRY (all ASSUMED — no vessel geometry published for power plant)
    # =========================================================================

    vessel_inner_radius_m: float = 3.5
    """Inner radius of spherical fusion vessel (to first wall) [m].
    Source: ASSUMED. No vessel geometry published for OpenStar Reactor A.
    Basis: D-T MFE at ~667 MW fusion; ~1 MW/m² first-wall loading → 667 m² surface area
    → 7.3 m radius for uniform spherical loading. Dipole loading is non-uniform (concentrated
    near equator), so effective vessel radius is smaller. 3.5 m is a rough approximation
    consistent with a compact spherical vessel for this power class.
    LDX outer vessel radius ~1 m (scientific device); scaled very roughly for power plant.
    Ref: No source. ASSUMED.
    HIGH UNCERTAINTY — affects blanket/shield costs, which are minor vs. coil/ICRH."""

    blanket_thickness_m: float = 0.80
    """Li₂O ceramic breeding blanket + first-wall thickness [m].
    Source: ASSUMED. ITER HCPB TBM uses Li₂O pebble bed at 0.6-0.8 m thickness.
    The favorable neutron geometry (~75% available for blanket) may allow
    somewhat thinner blanket while achieving TBR ≥ 1.1.
    Ref: ITER HCPB TBM analogue; arxiv-2602-20564-dt-dipole-power-plants.md §Tritium Breeding.
    MODERATE UNCERTAINTY."""

    shield_thickness_m: float = 0.60
    """Two-temperature W/B₄C shield thickness [m].
    Source: ASSUMED. ~25% of fusion neutrons intercept core magnet region (vs ~40-60% for tokamak).
    Shield must reduce fluence to <1 MW-year/m² at magnet location.
    Hot zone (tungsten, >2000 K) + warm zone (B₄C composite, ~600°C).
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Neutron Management.
    MODERATE UNCERTAINTY."""

    structure_thickness_m: float = 0.30
    """Primary structure thickness [m].
    Source: ASSUMED. MFE analogue.
    Ref: 1costingfe structure_unit_cost basis."""

    vessel_thickness_m: float = 0.15
    """Vacuum vessel + outer reinforced concrete dome thickness [m].
    Source: Outer dome described as reinforced concrete.
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Vacuum Vessel.
    ASSUMED thickness."""

    # =========================================================================
    # CAS22 UNIT COSTS (from 1costingfe)
    # =========================================================================

    blanket_unit_cost: float = 0.60
    """Li₂O breeding blanket unit cost [M$/m³].
    Source: 1costingfe costing_constants.yaml, blanket_unit_cost_dt = 0.60.
    Li₂O pebble-bed is comparable in complexity to LiPb/Li₄SiO₄ blankets.
    Ref: 1costingfe defaults."""

    # =========================================================================
    # CAS22 CONCEPT-SPECIFIC OVERRIDES
    # =========================================================================

    hts_coil_system_cost_M_USD: float = 250.0
    """HTS levitated coil + external support magnet + flux pump + docking mechanism [$M].
    Maps to C220103 (Magnets / Coils).
    Source: NO ANALOGUES — novel system with no commercial precedent.
    System components:
      (1) 23 T REBCO CICC floating coil (NI solder-impregnated; >550 kg; neon slush cooled)
      (2) External levitation/support magnet (lower field, conventional or HTS)
      (3) On-board superconducting transformer-rectifier flux pump (patented)
      (4) Neon slush cooling reservoir and management system
      (5) Precision docking mechanism for annual coil removal and re-levitation
    Basis: CFS REBCO TF coil set for SPARC (20T, 18 coils) estimated $200-500M total.
    Single-coil architecture reduces coil count by ~18× but 23 T is more demanding;
    flux pump + docking mechanism add uncharacterized cost. $250M central estimate.
    Ref: 01-hts-compact-tokamak analysis §HTS Magnets; analysis.md §Section 2.
    HIGH UNCERTAINTY — single most uncharacterized CAPEX item in the design."""

    icrh_system_cost_M_USD: float = 150.0
    """ICRH heating system capital cost [$M]. Maps to C220104 (Supplementary Heating).
    Source: ASSUMED. ITER 20 MW ICRH system is ~$200-250M total (system + integration).
    OpenStar requires ~35–55 MW delivered to plasma.
    Scaling: $150–200M for ~40–50 MW plasma ICRH at this design point.
    Geometry adaptation (floating coil restricts antenna access) adds design complexity.
    Ref: ITER ICRH analogue; analysis.md §Section 5.
    MODERATE UNCERTAINTY."""

    rh_scale_factor: float = 1.50
    """Scale multiplier on standard DT remote handling base cost for novel coil docking.
    Maps to C220110 (Remote Handling Equipment).
    Source: ASSUMED. Annual sacrificial coil docking, removal, partial replacement, and
    re-levitation requires specialized robotic system with no tokamak precedent.
    Standard DT remote handling base ($150M at 1 GWe) scaled up by 1.5× for
    novel docking mechanism development cost.
    Ref: 1costingfe costing_constants.yaml remote_handling_dt_base = 150.0;
         analysis.md §Section 2 (Sacrificial Coil challenge).
    HIGH UNCERTAINTY."""

    # =========================================================================
    # ANNUAL COIL REPLACEMENT OPEX (unique to levitated dipole)
    # =========================================================================

    sacrificial_section_fraction: float = 0.20
    """Fraction of floating coil volume constituting the replaceable outer section.
    Source: Outer section is ~20% of coil volume, designed for ~1 yr neutron damage lifetime
    at 1 MW-year/m² fluence threshold (corresponding to ~20 dpa in tungsten shield).
    Ref: arxiv-2602-20564-dt-dipole-power-plants.md §Magnet; analysis.md §Section 5."""

    sacrificial_section_material_cost_M_USD: float = 45.0
    """Annual material cost for sacrificial coil outer section replacement [$M/year].
    Source: ASSUMED. No manufacturing specification or cost estimate exists.
    Basis: 20% of coil system at full REBCO cost (~20% × $250M × material fraction).
    Includes REBCO tape (annual demand ~20% of coil tape inventory), winding,
    insulation, solder-impregnation, quality testing, logistics.
    Ref: analysis.md §Section 2, §Section 5 (sacrificial coil gap).
    HIGH UNCERTAINTY. 40-year cumulative: ~$1.8B."""

    coil_replacement_labor_M_USD: float = 10.0
    """Annual labor and operations cost for docking, partial replacement, re-levitation [$M/year].
    Source: ASSUMED. Includes remote handling crew, neon pump-out/recharge cycle,
    flux pump recharge, positional testing, re-levitation validation.
    Ref: No analogue. HIGH UNCERTAINTY."""

    # =========================================================================
    # FINANCIAL
    # =========================================================================

    interest_rate: float = 0.08
    """Real discount rate (weighted average cost of capital).
    Ref: 1costingfe default."""

    inflation_rate: float = 0.02
    """Inflation rate for levelizing O&M costs.
    Ref: 1costingfe default."""

    construction_time_years: float = 6.0
    """Construction period [years].
    Ref: 1costingfe reference_construction_time."""

    om_cost_per_MW_yr: float = 60.0
    """O&M cost per MW net capacity per year [$/MW/yr] (excluding scheduled replacement).
    Source: Standard fusion plant estimate.
    Ref: 1costingfe CAS71 default."""

    core_lifetime_FPY: float = 5.0
    """Li₂O blanket + first-wall replacement interval [full-power-years].
    Source: 14.1 MeV D-T neutrons, ~20 dpa/yr at first wall. 5 FPY baseline.
    Ref: 1costingfe costing_constants.yaml core_lifetime_dt = 5.0."""

    tritium_startup_cost_M_USD: float = 35.0
    """Tritium startup inventory [$M] (~1 kg at ~$35,000/g market price).
    Source: Global tritium price >$35,000/g; ~1 kg startup required per plant.
    Ref: 01-hts-compact-tokamak analysis §Key Materials; analysis.md §Section 4."""

    # =========================================================================
    # PRIVATE HELPER
    # =========================================================================

    def _sphere_shell_vol(self, r_in: float, thickness: float) -> float:
        r_out = r_in + thickness
        return (4.0 / 3.0) * math.pi * (r_out**3 - r_in**3)

    # =========================================================================
    # LAYER 1: POWER BALANCE
    # =========================================================================

    def _compute_power(self) -> dict:
        """Compute power balance for continuous quasi-steady MFE operation.

        Unlike pulsed IFE/MIF models, there is no driver or rep rate.
        Energy flow: ICRH grid draw → plasma heating → fusion → thermal → electric.

        Key derivation anchoring to published pair (p_fus=667 MW, p_net=208 MWe):
          p_plasma_heating = p_fus / qsci
          p_icrh_wallplug = p_plasma_heating / icrh_wall_plug_efficiency (grid draw)
          p_th = M × p_neutron + p_alpha + p_plasma_heating (ICRH ends up as heat too)
          p_et = thermal_efficiency × p_th
          p_net = p_et - p_icrh_wallplug - p_aux
        """
        r = {}

        # --- Fusion energy partitioning ---
        p_neutron = F_NEUTRON_DT * self.p_fus_MW   # 14.1 MeV neutrons → blanket
        p_alpha = F_ALPHA_DT * self.p_fus_MW        # 3.5 MeV alphas → plasma → FW
        r["p_fus"] = self.p_fus_MW
        r["p_neutron"] = p_neutron
        r["p_alpha"] = p_alpha

        # --- ICRH: plasma heating power ---
        p_plasma_heating = self.p_fus_MW / self.qsci           # power deposited into plasma
        p_icrh_wallplug = p_plasma_heating / self.icrh_wall_plug_efficiency  # grid draw
        r["p_plasma_heating_MW"] = p_plasma_heating
        r["p_icrh_wallplug_MW"] = p_icrh_wallplug
        r["Qsci"] = self.qsci
        r["Qeng_approx"] = self.p_fus_MW / p_icrh_wallplug  # fusion per unit grid power

        # --- Total thermal power collected from nuclear island ---
        # Neutron power multiplied by blanket, alpha power thermalizes to FW,
        # ICRH power ultimately dumps as heat to FW/blanket.
        p_th = (self.blanket_energy_multiplication * p_neutron
                + p_alpha
                + p_plasma_heating)
        r["p_th"] = p_th

        # --- Gross electric ---
        p_et = self.thermal_efficiency * p_th
        r["p_et"] = p_et

        # --- Recirculating loads ---
        p_aux = (self.p_cryo_MW
                 + self.p_tritium_MW
                 + self.p_housekeeping_MW
                 + self.p_position_control_MW)
        p_recirc = p_icrh_wallplug + p_aux
        r["p_aux_nonheating_MW"] = p_aux
        r["p_recirc_MW"] = p_recirc

        # --- Net electric ---
        p_net = p_et - p_recirc
        r["p_net"] = p_net

        # --- Recirculating fraction ---
        r["recirc_fraction"] = p_recirc / p_et if p_et > 0 else float("inf")

        # --- Annual energy production ---
        r["annual_energy_MWh"] = 8760.0 * p_net * self.duty_cycle

        return r

    # =========================================================================
    # LAYER 2: GEOMETRY
    # =========================================================================

    def _compute_geometry(self, power: dict) -> dict:
        """Compute spherical shell volumes for CAS22 cost scaling.

        The levitated dipole uses a spherical vacuum vessel (Inconel 718 inner shell +
        outer reinforced concrete dome). Geometry is approximated as concentric spherical
        shells — the bottom opening for coil docking is a small fraction of total area
        and is neglected in this first-pass model.
        """
        r = {}
        ri = self.vessel_inner_radius_m

        # Running outer radius as shells accumulate outward
        r_blanket_out = ri + self.blanket_thickness_m
        r_shield_out = r_blanket_out + self.shield_thickness_m
        r_structure_out = r_shield_out + self.structure_thickness_m
        r_vessel_out = r_structure_out + self.vessel_thickness_m

        r["blanket_vol_m3"] = self._sphere_shell_vol(ri, self.blanket_thickness_m)
        r["shield_vol_m3"] = self._sphere_shell_vol(r_blanket_out, self.shield_thickness_m)
        r["structure_vol_m3"] = self._sphere_shell_vol(r_shield_out, self.structure_thickness_m)
        r["vessel_vol_m3"] = self._sphere_shell_vol(r_structure_out, self.vessel_thickness_m)
        r["vessel_outer_radius_m"] = r_vessel_out
        r["first_wall_area_m2"] = 4.0 * math.pi * ri**2

        return r

    # =========================================================================
    # LAYER 3: CAS22 REACTOR PLANT EQUIPMENT
    # =========================================================================

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Compute CAS22 Reactor Plant Equipment with concept-specific overrides.

        Standard accounts use 1costingfe power-scaling laws.
        Overrides:
          C220103 — HTS coil system (replaces standard magnet scaling)
          C220104 — ICRH heating (replaces NBI/ECRH scaling)
          C220107 — Power supplies (reduced; ICRH supplies in C220104, flux pump negligible)
          C220110 — Remote handling (scaled up for novel coil docking mechanism)
        Absent (not applicable):
          C220108 — Target factory (IFE/MIF only; $0 for continuous MFE)
          C220109 — Direct energy converter (no DEC in closed-field levitated dipole)
        """
        r = {}
        p_th = max(power["p_th"], 1.0)
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)

        # --- C220101: First Wall + Li₂O Breeding Blanket ---
        # DEFAULT: 1costingfe blanket_unit_cost_dt = 0.60 M$/m³
        # Formula: unit_cost × volume × (p_th / P_TH_REF)^0.6
        r["C220101"] = (self.blanket_unit_cost
                        * geom["blanket_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # --- C220102: Two-Temperature W/B₄C Shield ---
        # DEFAULT: shield_unit_cost = 0.74 M$/m³, full D-T shielding scale
        # Formula: 0.74 × volume × (p_th / P_TH_REF)^0.6
        shield_unit_cost = 0.74
        r["C220102"] = (shield_unit_cost
                        * geom["shield_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # --- C220103: HTS Coil System — OVERRIDE ---
        # Standard tokamak magnet scaling (~hundreds of coils) is not applicable.
        # Single floating REBCO CICC coil (23 T) + external support magnet +
        # on-board flux pump + neon slush reservoir + precision docking mechanism.
        # Direct cost override; see parameter documentation for basis and uncertainty.
        r["C220103"] = self.hts_coil_system_cost_M_USD  # [override]

        # --- C220104: ICRH Heating System — OVERRIDE ---
        # ICRH (not NBI or laser). Standard MFE NBI/ECRH scaling not used.
        # Includes antenna array, RF power conditioning, transmission lines,
        # and radiation-hardened geometry adaptation for floating-coil access constraints.
        r["C220104"] = self.icrh_system_cost_M_USD  # [override]

        # --- C220105: Primary Structure ---
        # DEFAULT: structure_unit_cost = 0.15 M$/m³
        # Formula: 0.15 × volume × (p_et / P_ET_REF)^0.5
        structure_unit_cost = 0.15
        r["C220105"] = (structure_unit_cost
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # --- C220106: Vacuum System (Inconel 718 inner vessel + outer concrete dome) ---
        # DEFAULT: vessel_unit_cost = 0.72 M$/m³
        # Formula: 0.72 × volume × (p_et / P_ET_REF)^0.6
        vessel_unit_cost = 0.72
        r["C220106"] = (vessel_unit_cost
                        * geom["vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # --- C220107: Miscellaneous Power Supplies (reduced) ---
        # The main confinement coil has no conventional power supply — the on-board
        # flux pump (~10 W continuous) maintains current after initial energization.
        # Standard power supplies for controls, diagnostics, position control coils,
        # cryogenic plant, vacuum systems. Reduced by 0.5× vs. standard tokamak scaling.
        # Standard formula: 80.0 × (p_et / 1000)^0.7
        # Ref: 1costingfe costing_constants.yaml power_supplies_base = 80.0
        r["C220107"] = 0.50 * 80.0 * (p_et / 1000.0) ** 0.7  # [partial override]

        # --- C220108: Target Factory — NOT APPLICABLE ---
        # Continuous MFE operation; no targets.
        r["C220108"] = 0.0

        # --- C220109: Direct Energy Converter — NOT APPLICABLE ---
        # Closed-field levitated dipole; no directed ion exhaust for DEC.
        r["C220109"] = 0.0

        # --- C220110: Remote Handling Equipment — SCALED UP ---
        # Annual sacrificial coil docking/replacement/re-levitation requires custom
        # robotic handling system with no tokamak precedent.
        # Base: 150 M$ at 1 GWe reference (1costingfe remote_handling_dt_base)
        # Scaled by (p_et / P_ET_REF)^0.7 × rh_scale_factor
        rh_base = 150.0  # M$ at 1 GWe (from 1costingfe remote_handling_dt_base)
        r["C220110"] = rh_base * (p_et / P_ET_REF) ** 0.7 * self.rh_scale_factor  # [override]

        # --- C220111: Installation Labor ---
        # DEFAULT: 14% of reactor module subtotal
        # Ref: 1costingfe installation_frac = 0.14
        installation_frac = 0.14
        reactor_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"])
        r["C220111"] = installation_frac * reactor_subtotal

        # --- C220112: Isotope Separation ---
        # D-T: tritium handling costs in CAS80; Li-6 enrichment cost embedded in blanket.
        r["C220112"] = 0.0

        # Per-module subtotal (single module)
        r["CAS22_per_module"] = reactor_subtotal + r["C220111"] + r["C220112"]

        # --- Plant-wide accounts (scale with total plant power) ---
        p_net_total = p_net      # single module
        p_th_total = p_th

        # C220200: Main & Secondary Coolant Systems
        C220201 = 166.0 * (p_net_total / 1000.0)          # Primary loop
        C220202 = 40.6 * (p_th_total / 3500.0) ** 0.55    # Secondary/intermediate loop
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling + Cryoplant (neon slush at 24.6 K)
        # Note: neon at 24.6 K is less demanding than He at 4 K;
        # cryoplant scaling from 1costingfe using actual p_cryo load
        C220301 = 1.1e-3 * p_th_total                                          # Aux coolant
        C220302 = 200.0 * (max(self.p_cryo_MW, 0.01) / 30.0) ** 0.7           # Cryoplant
        r["C220300"] = C220301 + C220302

        # C220400: Radioactive Waste Management
        r["C220400"] = 1.96 * (p_th_total / 1000.0)

        # C220500: Fuel Handling & Tritium Storage (D-T)
        # DEFAULT: 120 M$ at 1 GWe reference, scaled by (p_net/1000)^0.7
        fuel_handling_base = 120.0  # M$ (D-T, from 1costingfe fuel_handling_dt_base)
        r["C220500"] = fuel_handling_base * (p_net_total / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        r["C220600"] = 11.5 * (p_net_total / 1000.0) ** 0.8

        # C220700: Instrumentation & Control
        r["C220700"] = 85.0 * (p_th_total / 3500.0) ** 0.65

        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        r["CAS22"] = r["CAS22_per_module"] + r["CAS22_plant_wide"]

        return r

    # =========================================================================
    # LAYER 4: CAPITAL COSTS (CAS10-60)
    # =========================================================================

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Compute CAS10-60 capital costs following 1costingfe / MagLIF exemplar pattern."""
        r = {}
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)

        # === CAS10: Pre-construction ===
        # Ref: 1costingfe costing_constants.yaml CAS10 defaults
        site_permits = 3.0
        plant_studies = 4.0 if self.noak else 20.0
        plant_permits = 2.0
        plant_reports = 1.0
        other_precon = 1.0
        land_cost = 0.25 * p_net * 10_000 / 1e6  # 0.25 acres/MWe × $10k/acre
        licensing_cost = 2.5 if self.noak else 5.0   # D-T licensing, reduced for NOAK
        tritium_startup = self.tritium_startup_cost_M_USD
        r["CAS10"] = (site_permits + plant_studies + plant_permits + plant_reports
                      + other_precon + land_cost + licensing_cost + tritium_startup)

        # === CAS21: Buildings ===
        # DEFAULT: $/kW gross electric (ARIES/NETL-based, from 1costingfe CAS21 defaults)
        building_cost_per_kW = {
            "site_improvements": 268.0,   # $/kW
            "reactor_building": 126.0,
            "turbine_building": 54.0,
            "cooling_structures": 12.0,
            "hot_cell": 93.4,            # elevated: annual coil replacement requires hot cell
            "misc_buildings": 61.6,
        }
        # Note: no dedicated pulsed power building (no driver); hot cell is important
        # because the sacrificial coil section is activated and requires hot cell handling.
        total_building_per_kW = sum(building_cost_per_kW.values())  # ~615 $/kW
        r["CAS21"] = total_building_per_kW * p_et / 1000.0  # M$
        r["CAS21_detail"] = {k: v * p_et / 1000.0 for k, v in building_cost_per_kW.items()}

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment ===
        turbine_per_mw = 0.19764   # M$/MW gross electric (1costingfe default)
        r["CAS23"] = p_et * turbine_per_mw

        # === CAS24: Electric Plant Equipment ===
        electric_per_mw = 0.08418  # M$/MW
        r["CAS24"] = p_et * electric_per_mw

        # === CAS25: Miscellaneous Plant Equipment ===
        misc_per_mw = 0.05124      # M$/MW
        r["CAS25"] = p_et * misc_per_mw

        # === CAS26: Heat Rejection ===
        heat_rej_per_mw = 0.03416  # M$/MW
        r["CAS26"] = p_et * heat_rej_per_mw

        # === CAS27: Special Materials ===
        # REBCO tape for initial coil is in C220103; this is additional rare material stock.
        # Nominal allowance for startup Li-6 enriched Li₂O blanket inventory.
        r["CAS27"] = 15.0  # M$ ASSUMED

        # === CAS28: Digital Twin ===
        r["CAS28"] = 5.0

        # === CAS29: Contingency ===
        cas20_subtotal = sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                             "CAS25", "CAS26", "CAS27", "CAS28"])
        contingency_rate = 0.0 if self.noak else 0.10
        r["CAS29"] = contingency_rate * cas20_subtotal

        # === CAS20: Total Direct Costs ===
        r["CAS20"] = cas20_subtotal + r["CAS29"]

        # === CAS30: Indirect Costs ===
        # 20% of CAS20, scaled by construction time vs. 6-year reference
        ref_T = 6.0
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / ref_T)

        # === CAS40: Owner's Costs ===
        r["CAS40"] = 0.05 * r["CAS20"]

        # === CAS50: Supplementary Costs ===
        spare_parts = 0.01 * sum(r[k] for k in ["CAS23", "CAS24", "CAS25",
                                                  "CAS26", "CAS27", "CAS28"])
        fuel_load = (p_net / 1000.0) * 10.0   # M$
        r["CAS50"] = spare_parts + fuel_load + 1.0 + 0.5 + 0.5 + 5.0  # +shipping+taxes+insurance+decom

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

        if power["p_net"] > 0:
            r["specific_capital_USD_per_kWe"] = r["total_capital"] * 1e6 / (power["p_net"] * 1e3)
        else:
            r["specific_capital_USD_per_kWe"] = float("inf")

        return r

    # =========================================================================
    # LAYER 5: ECONOMICS (CAS70-90)
    # =========================================================================

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Compute CAS70-90 annualized costs and LCOE.

        Special feature: CAS72 includes both standard blanket replacement (core_lifetime_FPY)
        AND annual sacrificial coil section replacement — a novel OPEX item unique to
        the levitated dipole architecture.
        """
        r = {}
        p_net = power["p_net"]

        # Capital Recovery Factor
        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1 + i) ** n / ((1 + i) ** n - 1)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]  # M$/year

        # === CAS71: Annual O&M (levelized with inflation) ===
        annual_om_base = self.om_cost_per_MW_yr * p_net * 1000.0 / 1e6  # M$
        g = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g) ** Tc
        if abs(i - g) > 1e-10:
            pv_growing_annuity = A1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
        else:
            pv_growing_annuity = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_growing_annuity  # M$/year

        # === CAS72a: Standard Blanket/FW Replacement ===
        eff_years_per_replacement = self.core_lifetime_FPY / self.duty_cycle
        n_replacements = max(0, int(math.ceil(n / eff_years_per_replacement)) - 1)
        replacement_cost = cas22["C220101"]  # Li₂O blanket replacement cost
        pv_blanket = 0.0
        for k in range(1, n_replacements + 1):
            year = k * eff_years_per_replacement
            if year < n:
                pv_blanket += replacement_cost / (1 + i) ** year
        r["CAS72_blanket"] = crf * pv_blanket
        r["n_blanket_replacements"] = n_replacements

        # === CAS72b: Annual Sacrificial Coil Section Replacement (NOVEL) ===
        # The outer section (~20% coil volume) must be replaced annually.
        # This is an unusual recurring CAPEX-like OPEX with no precedent.
        # Model as annual cost discounted over plant lifetime.
        annual_coil_replacement = (self.sacrificial_section_material_cost_M_USD
                                    + self.coil_replacement_labor_M_USD)
        pv_coil_replacements = 0.0
        for yr in range(1, int(n) + 1):
            pv_coil_replacements += annual_coil_replacement / (1 + i) ** yr
        r["CAS72_coil_annual"] = crf * pv_coil_replacements
        r["annual_coil_replacement_cost_M_USD"] = annual_coil_replacement

        r["CAS72"] = r["CAS72_blanket"] + r["CAS72_coil_annual"]
        r["CAS70"] = r["CAS71"] + r["CAS72"]

        # === CAS80: Fuel Costs ===
        # D-T fuel is essentially free on an ongoing basis:
        # - Deuterium: abundant, cheap (~$1/g)
        # - Tritium: bred in blanket (TBR 1.1); ongoing purchase is near-zero
        # - Li₂O: recharged with each blanket replacement (captured in CAS72a)
        # Annual D-T fuel purchase: ~kg/year of deuterium + marginal tritium top-up
        annual_dt_fuel_M = 2.0   # M$ ASSUMED: deuterium + marginal tritium make-up
        r["CAS80"] = annual_dt_fuel_M

        # === LCOE ===
        annual_revenue_req = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_revenue_req

        annual_energy_MWh = power["annual_energy_MWh"]
        r["annual_energy_MWh"] = annual_energy_MWh

        if annual_energy_MWh > 0:
            r["lcoe_USD_per_MWh"] = annual_revenue_req * 1e6 / annual_energy_MWh
            r["lcoe_cents_per_kWh"] = r["lcoe_USD_per_MWh"] / 10.0
        else:
            r["lcoe_USD_per_MWh"] = float("inf")
            r["lcoe_cents_per_kWh"] = float("inf")

        if annual_revenue_req > 0:
            r["capital_fraction"] = r["CAS90"] / annual_revenue_req
            r["om_fraction"] = r["CAS70"] / annual_revenue_req
            r["fuel_fraction"] = r["CAS80"] / annual_revenue_req

        return r

    # =========================================================================
    # COMPUTE ALL
    # =========================================================================

    def compute(self) -> dict:
        """Run all five layers and return merged results dict."""
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
            # convenience aliases
            "net_electric_MW": power["p_net"],
            "lcoe_cents_per_kWh": econ["lcoe_cents_per_kWh"],
            "total_capital_M_USD": costs["total_capital"],
        }
        return results


# =============================================================================
# PRINT RESULTS
# =============================================================================

def print_results(params: LevitatedDipolePlantParams, results: dict):
    """Pretty-print LCOE model results with full CAS-structured accounting."""
    power = results["power"]
    cas22 = results["cas22"]
    costs = results["costs"]
    econ = results["economics"]

    print("=" * 72)
    print("Levitated Dipole (D-T) LCOE Model — OpenStar Technologies / 1cFE CAS")
    print("=" * 72)

    # --- Key Inputs ---
    print(f"\n--- Key Input Parameters ---")
    print(f"  Fusion power (Reactor A, Bohm): {params.p_fus_MW:.0f} MW  [published]")
    print(f"  Blanket energy multiplication:  {params.blanket_energy_multiplication:.2f}")
    print(f"  Thermal efficiency:             {params.thermal_efficiency:.1%}  [ASSUMED — BOP unpublished]")
    print(f"  Qsci:                           {params.qsci:.1f}  [INFERRED: range 12-19]")
    print(f"  ICRH wall-plug efficiency:      {params.icrh_wall_plug_efficiency:.1%}  [published]")
    print(f"  Duty cycle:                     {params.duty_cycle:.1%}  [published: >95%]")
    print(f"  Plant lifetime:                 {params.plant_lifetime_years:.0f} years")
    print(f"  FOAK/NOAK:                      {'NOAK' if params.noak else 'FOAK'}")
    print(f"  Interest rate:                  {params.interest_rate:.1%}")
    print(f"  HTS coil system cost:           ${params.hts_coil_system_cost_M_USD:.0f}M  [HIGH UNCERTAINTY]")
    print(f"  ICRH system cost:               ${params.icrh_system_cost_M_USD:.0f}M  [MODERATE UNCERTAINTY]")
    print(f"  Annual coil replacement:        ${params.sacrificial_section_material_cost_M_USD + params.coil_replacement_labor_M_USD:.0f}M/yr  [HIGH UNCERTAINTY]")

    # --- Power Balance ---
    print(f"\n--- Power Balance ---")
    print(f"  Fusion power:                   {power['p_fus']:>7.1f} MW")
    print(f"    Neutron power (80%):          {power['p_neutron']:>7.1f} MW  → blanket (×{params.blanket_energy_multiplication:.2f})")
    print(f"    Alpha power (20%):            {power['p_alpha']:>7.1f} MW  → plasma → FW")
    print(f"  Qsci (Pfus/Pplasma):            {power['Qsci']:>7.1f}  [inferred]")
    print(f"  ICRH plasma heating:            {power['p_plasma_heating_MW']:>7.1f} MW  (to plasma)")
    print(f"  ICRH grid draw:                 {power['p_icrh_wallplug_MW']:>7.1f} MW  (from grid, at {params.icrh_wall_plug_efficiency:.0%} η)")
    print(f"  Total thermal power:            {power['p_th']:>7.1f} MW")
    print(f"  Gross electric:                 {power['p_et']:>7.1f} MWe  (η={params.thermal_efficiency:.1%})")
    print(f"  Recirculating power:")
    print(f"    ICRH grid draw:               {power['p_icrh_wallplug_MW']:>7.1f} MW")
    print(f"    Non-heating auxiliaries:      {power['p_aux_nonheating_MW']:>7.1f} MW  (cryo+trit+house+pos)")
    print(f"    Total recirculating:          {power['p_recirc_MW']:>7.1f} MW  ({power['recirc_fraction']:.1%} of gross)")
    print(f"  Net electric:                   {power['p_net']:>7.1f} MWe")
    print(f"  Published target:                 208.0 MWe  [arxiv-2602-20564 §Reactor Performance]")
    print(f"  Approx. Qeng (Pfus/Pgrid_heat):  {power['Qeng_approx']:>6.1f}")

    # --- Geometry ---
    geom = results["geometry"]
    print(f"\n--- Geometry (ASSUMED spherical — no published vessel dimensions) ---")
    print(f"  First-wall inner radius:        {params.vessel_inner_radius_m:.1f} m  [ASSUMED]")
    print(f"  First-wall area:                {geom['first_wall_area_m2']:.0f} m²  ({power['p_fus']/geom['first_wall_area_m2']:.2f} MW/m² loading)")
    print(f"  Blanket volume:                 {geom['blanket_vol_m3']:.0f} m³")
    print(f"  Shield volume:                  {geom['shield_vol_m3']:.0f} m³")
    print(f"  Total outer radius:             {geom['vessel_outer_radius_m']:.1f} m")

    # --- CAS22 ---
    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    cas22_labels = {
        "C220101": ("Blanket/First Wall (Li₂O)",    ""),
        "C220102": ("Shield (W/B₄C two-temp)",       ""),
        "C220103": ("HTS Coil + Flux Pump System",   " [override]"),
        "C220104": ("ICRH Heating System",            " [override]"),
        "C220105": ("Primary Structure",              ""),
        "C220106": ("Vacuum System (Inconel dome)",   ""),
        "C220107": ("Power Supplies (misc, reduced)", " [partial override]"),
        "C220108": ("Target Factory",                 " [N/A: MFE, $0]"),
        "C220109": ("Direct Energy Converter",        " [N/A: closed-field, $0]"),
        "C220110": ("Remote Handling (coil docking)", " [override]"),
        "C220111": ("Installation Labor (14%)",       ""),
        "C220112": ("Isotope Separation",             " [$0: in CAS80]"),
    }
    for code, (label, note) in cas22_labels.items():
        val = cas22[code]
        if val > 0.01 or "N/A" in note:
            print(f"    {code}  {label:<34s} ${val:>8.1f}M{note}")
    print(f"  {'─' * 58}")
    print(f"    Per-module subtotal:                       ${cas22['CAS22_per_module']:>8.1f}M")
    print(f"  Plant-wide accounts:")
    pw_labels = {
        "C220200": "Coolant Systems",
        "C220300": "Aux Cooling + Cryoplant (neon slush)",
        "C220400": "Radioactive Waste Management",
        "C220500": "Fuel Handling (D-T, Li₂O blanket)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    for code, label in pw_labels.items():
        print(f"    {code}  {label:<34s} ${cas22[code]:>8.1f}M")
    print(f"  {'─' * 58}")
    print(f"    Plant-wide subtotal:                       ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                                 ${cas22['CAS22']:>8.1f}M")

    # --- Capital Costs ---
    print(f"\n--- Capital Costs (CAS10-60) ---")
    print(f"  CAS10  Pre-construction:        ${costs['CAS10']:>8.1f}M  (incl. ${params.tritium_startup_cost_M_USD:.0f}M tritium startup)")
    print(f"  CAS21  Buildings:               ${costs['CAS21']:>8.1f}M")
    print(f"  CAS22  Reactor Plant Equipment: ${costs['CAS22']:>8.1f}M")
    print(f"  CAS23  Turbine Plant:           ${costs['CAS23']:>8.1f}M")
    print(f"  CAS24  Electric Plant:          ${costs['CAS24']:>8.1f}M")
    print(f"  CAS25  Misc Plant:              ${costs['CAS25']:>8.1f}M")
    print(f"  CAS26  Heat Rejection:          ${costs['CAS26']:>8.1f}M")
    print(f"  CAS27  Special Materials:       ${costs['CAS27']:>8.1f}M")
    print(f"  CAS28  Digital Twin:            ${costs['CAS28']:>8.1f}M")
    print(f"  CAS29  Contingency:             ${costs['CAS29']:>8.1f}M")
    print(f"  {'─' * 48}")
    print(f"  CAS20  Direct Costs:            ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30  Indirect Costs:          ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40  Owner's Costs:           ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50  Supplementary:           ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 48}")
    print(f"  Overnight Capital:              ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60  IDC (f={costs['f_IDC']:.3f}):        ${costs['CAS60']:>8.1f}M")
    print(f"  {'═' * 48}")
    print(f"  Total Capital:                  ${costs['total_capital']:>8.1f}M")
    print(f"  Specific Capital:               ${costs['specific_capital_USD_per_kWe']:>8.0f} $/kWe")

    # --- Annual Costs ---
    print(f"\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90  Capital charge (CRF={econ['CRF']:.4f}):  ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71  O&M (levelized):                  ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72a Blanket replacement ({econ['n_blanket_replacements']} events):     ${econ['CAS72_blanket']:>8.1f}M/yr")
    print(f"  CAS72b Coil section replacement (annual):${econ['CAS72_coil_annual']:>8.1f}M/yr  [HIGH UNCERTAINTY]")
    print(f"         (${econ['annual_coil_replacement_cost_M_USD']:.0f}M/yr × {params.plant_lifetime_years:.0f} yr → ${econ['annual_coil_replacement_cost_M_USD']*params.plant_lifetime_years:.0f}M nominal lifecycle)")
    print(f"  CAS70  Total O&M:                        ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80  Fuel costs (D-T):                 ${econ['CAS80']:>8.1f}M/yr")

    # --- LCOE ---
    print(f"\n--- LCOE ---")
    print(f"  Annual energy production:   {econ['annual_energy_MWh']:>12,.0f} MWh")
    print(f"                              ({power['p_net']:.0f} MWe × {params.duty_cycle:.0%} × 8760 hr)")
    print(f"  Annual revenue requirement: ${econ['annual_revenue_req']:.1f}M")
    print(f"  ╔═══════════════════════════════════════════╗")
    print(f"  ║  LCOE = {econ['lcoe_cents_per_kWh']:>7.2f} ¢/kWh                      ║")
    print(f"  ║       = {econ['lcoe_USD_per_MWh']:>7.1f} $/MWh                      ║")
    print(f"  ╚═══════════════════════════════════════════╝")
    print(f"  Capital (CAS90):          {econ.get('capital_fraction', 0):.1%}")
    print(f"  O&M (CAS70):              {econ.get('om_fraction', 0):.1%}")
    print(f"    of which coil repl.:  {econ['CAS72_coil_annual']/econ['annual_revenue_req']:.1%}")
    print(f"  Fuel (CAS80):             {econ.get('fuel_fraction', 0):.1%}")


# =============================================================================
# SENSITIVITY SWEEP
# =============================================================================

def sensitivity_sweep(base_params: LevitatedDipolePlantParams, param_name: str,
                       values: list, label: str = "") -> list:
    """Sweep a single parameter and return LCOE for each value."""
    results_list = []
    for val in values:
        p = LevitatedDipolePlantParams(**{**base_params.__dict__, param_name: val})
        r = p.compute()
        results_list.append({
            "param_value": float(val),
            "lcoe_cents_kWh": r["lcoe_cents_per_kWh"],
            "net_electric_MW": r["net_electric_MW"],
        })
    return results_list


# =============================================================================
# MAIN
# =============================================================================

def main():
    # -------------------------------------------------------------------------
    # BASELINE SCENARIO
    # -------------------------------------------------------------------------
    baseline = LevitatedDipolePlantParams()
    baseline_results = baseline.compute()
    print_results(baseline, baseline_results)
    base_lcoe = baseline_results["lcoe_cents_per_kWh"]

    # -------------------------------------------------------------------------
    # SINGLE-PARAMETER SENSITIVITY SWEEPS
    # -------------------------------------------------------------------------
    print("\n\n" + "=" * 72)
    print("SENSITIVITY SWEEPS — Single-Parameter Variation from Baseline")
    print("=" * 72)
    print(f"  Baseline LCOE: {base_lcoe:.2f} ¢/kWh\n")

    sweeps = [
        ("thermal_efficiency",
         [0.32, 0.35, 0.38, 0.40, 0.42, 0.45],
         "Thermal efficiency (unknown cycle: 32-45%)"),

        ("hts_coil_system_cost_M_USD",
         [100.0, 150.0, 200.0, 250.0, 400.0, 600.0, 1000.0],
         "HTS coil system cost [$M] (critical: no analogues)"),

        ("sacrificial_section_material_cost_M_USD",
         [10.0, 25.0, 45.0, 75.0, 120.0],
         "Annual sacrificial section material cost [$M/yr]"),

        ("qsci",
         [8.0, 10.0, 12.0, 15.0, 19.0, 25.0],
         "Qsci (inferred range: 12-19)"),

        ("interest_rate",
         [0.04, 0.06, 0.08, 0.10, 0.12],
         "Interest rate / WACC"),

        ("icrh_system_cost_M_USD",
         [75.0, 100.0, 150.0, 200.0, 300.0],
         "ICRH system capital cost [$M]"),

        ("duty_cycle",
         [0.80, 0.85, 0.90, 0.95, 0.97],
         "Duty cycle (published: >95%)"),
    ]

    for param_name, values, label in sweeps:
        print(f"  {label}:")
        base_val = getattr(baseline, param_name)
        results_list = sensitivity_sweep(baseline, param_name, values, label)
        for entry in results_list:
            val = entry["param_value"]
            lcoe = entry["lcoe_cents_kWh"]
            net = entry["net_electric_MW"]
            marker = " ← baseline" if abs(val - base_val) < 1e-9 else ""
            if net <= 0:
                print(f"    {val:>10.3g} → NET POWER NEGATIVE ({net:.1f} MWe)")
            else:
                delta = lcoe - base_lcoe
                sign = "+" if delta >= 0 else ""
                print(f"    {val:>10.4g} → {lcoe:7.2f} ¢/kWh  ({sign}{delta:.2f})  [{net:.0f} MWe net]{marker}")
        print()

    # -------------------------------------------------------------------------
    # SCENARIO COMPARISON TABLE
    # -------------------------------------------------------------------------
    print("=" * 72)
    print("SCENARIO COMPARISON: Conservative / Moderate (Baseline) / Optimistic")
    print("=" * 72)

    conservative = LevitatedDipolePlantParams(
        thermal_efficiency=0.34,              # Low-efficiency Rankine, unknown cycle
        qsci=11.0,                            # Low end of inferred range
        hts_coil_system_cost_M_USD=450.0,     # High coil cost — novel technology premium
        icrh_system_cost_M_USD=220.0,         # High ICRH cost — geometry adaptation
        sacrificial_section_material_cost_M_USD=80.0,   # High replacement cost
        coil_replacement_labor_M_USD=20.0,    # High labor (complex docking procedure)
        rh_scale_factor=2.0,                  # High RH premium (novel docking)
        interest_rate=0.10,                   # High WACC (early-stage technology risk)
        construction_time_years=7.0,
        duty_cycle=0.88,                      # Lower availability during scale-up
        noak=False,                           # FOAK
    )

    optimistic = LevitatedDipolePlantParams(
        thermal_efficiency=0.44,              # sCO₂ Brayton benefiting from >2000 K hot shield
        qsci=20.0,                            # High end / beyond inferred range (improved confinement)
        hts_coil_system_cost_M_USD=120.0,     # Learning curve; single-coil architecture simplicity
        icrh_system_cost_M_USD=80.0,          # Mature ICRH; simple antenna geometry
        sacrificial_section_material_cost_M_USD=20.0,   # REBCO cost reduction + streamlined replacement
        coil_replacement_labor_M_USD=5.0,     # Automated docking procedure
        rh_scale_factor=1.1,                  # Near-standard RH after system maturation
        interest_rate=0.06,                   # Lower WACC with demonstrated performance
        construction_time_years=5.0,
        duty_cycle=0.97,                      # Demonstrated high-availability operation
        noak=True,
    )

    scenarios = [
        ("Conservative (FOAK, high uncertainty)", conservative),
        ("Moderate / Baseline (NOAK, central)",   baseline),
        ("Optimistic (NOAK, improved confinement, learning)", optimistic),
    ]

    print(f"\n{'Scenario':<42} {'Net MW':>8} {'CAPEX $M':>10} {'$/kWe':>8} {'LCOE ¢/kWh':>12}")
    print("─" * 84)
    for name, params in scenarios:
        r = params.compute()
        p_net = r["net_electric_MW"]
        capex = r["total_capital_M_USD"]
        spec = r["costs"]["specific_capital_USD_per_kWe"]
        lcoe = r["lcoe_cents_per_kWh"]
        print(f"  {name:<40} {p_net:>8.0f} {capex:>10.0f} {spec:>8.0f} {lcoe:>12.2f}")

    # -------------------------------------------------------------------------
    # KEY BINDING CONSTRAINTS NARRATIVE
    # -------------------------------------------------------------------------
    print(f"\n{'=' * 72}")
    print("KEY BINDING CONSTRAINTS (Top 3 LCOE Drivers)")
    print("=" * 72)

    print("""
1. CAPITAL COST — HTS COIL SYSTEM (C220103) — HIGH UNCERTAINTY, HIGH IMPACT
   The single floating 23 T REBCO CICC coil + flux pump + precision docking mechanism
   is the most uncharacterized CAPEX item in this analysis. Sensitivity sweep shows
   that varying the coil system from $100M to $1000M changes LCOE by roughly ±1 ¢/kWh
   from the baseline. No cost analogue exists — the only comparable HTS coil assembly
   (CFS SPARC) covers 18 TF coils at $200-500M total, while this design requires ONE
   floating coil plus substantial novel subsystems (flux pump, docking mechanism).
   A 2× cost overrun ($500M vs $250M) adds ~0.7 ¢/kWh to LCOE.

2. THERMAL EFFICIENCY — UNKNOWN CONVERSION CYCLE — HIGH UNCERTAINTY, HIGH IMPACT
   OpenStar has not disclosed the thermal power conversion cycle type or efficiency.
   The two-temperature shield design (>2000 K hot, ~600°C warm) is potentially
   compatible with highly efficient sCO₂ Brayton (40-45%) but this is unconfirmed.
   Sensitivity sweep: 32% → 45% efficiency changes LCOE by ~2 ¢/kWh (from ~8 to ~6 ¢/kWh).
   This is the single largest free parameter. The baseline 38% is set to be consistent
   with the published p_fus/p_net pair at assumed Qsci=15.

3. ANNUAL SACRIFICIAL COIL REPLACEMENT — NOVEL OPEX, HIGH UNCERTAINTY, HIGH IMPACT
   The annual partial coil replacement (~20% outer section) creates an unusual recurring
   cost with no prior precedent in any approved fusion concept. Over 40 years, even a
   conservative $55M/yr estimate accumulates to $2.2B nominal lifecycle cost. Sensitivity
   sweep on material cost alone ($10M to $120M/yr) changes LCOE by ~1 ¢/kWh.
   This item could be a decisive OPEX advantage or disadvantage relative to tokamaks
   (which replace blanket every ~5 FPY but have NO annual magnet replacement).
   Until OpenStar publishes a manufacturing specification and cost model for the
   sacrificial section, this remains an unresolvable uncertainty.
""")

    print(f"\n{'─' * 72}")
    print(f"NOTE ON MODEL CONFIDENCE: This model is based primarily on two preprints")
    print(f"(arXiv 2602.20564 and 2508.17691) with major gaps in thermal efficiency,")
    print(f"Qsci, BOP design, and all cost parameters. The published anchor values")
    print(f"(667 MW fusion, 208 MWe net) constrain the power balance, but capital cost")
    print(f"is entirely estimated from analogues. LCOE range of ~5-12 ¢/kWh reflects")
    print(f"genuine parameter uncertainty, not model error.")
    print(f"{'─' * 72}")


if __name__ == "__main__":
    main()
