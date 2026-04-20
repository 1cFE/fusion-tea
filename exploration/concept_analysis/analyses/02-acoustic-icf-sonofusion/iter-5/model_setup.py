"""
Acoustic ICF / Sonofusion (D-D) — Second-Pass LCOE Model
=========================================================
1cFE First Pass Concept Analysis
Concept: Acoustic ICF / Sonofusion (D-D)
Company: Sonofusion Energy (UCLA spin-off, Putterman/Camara)

CRITICAL CAVEAT: This model is purely speculative corridor mapping. Sonofusion
has not demonstrated fusion from acoustic cavitation in any credible, replicated
experiment. The ~4 orders-of-magnitude temperature gap between demonstrated
sonoluminescence (~16,000 K) and D-D fusion threshold (~10⁸ K) remains unbridged.
All parameters involving fusion gain Q are entirely hypothetical. This model
answers "what would LCOE be IF Q could be achieved" — it is NOT a projection.

Architecture: Spherical D₂O vessel(s) driven by piezoelectric ultrasonic transducers
at ~30 kHz. The heavy-water medium serves as both the fusion medium and the
thermal blanket. Energy conversion via Rankine steam cycle on the D₂O coolant.
D-D fuel: no external tritium supply needed; tritium produced as a byproduct.

Key references:
- analysis.md — concept analysis with parameter availability and gap assessment
- ucla-putterman-group-sonoluminescence.md — demonstrated sonoluminescence physics
- bubble-fusion-scientific-history.md — Taleyarkhan controversy, temperature gap
- sonofusion-energy-website.md — company claims (no technical specs disclosed)
- Flannigan & Suslick 2010, Nature Physics 6, 598–601 — temperature upper bound
- 1costingfe costing_constants.yaml — CAS scaling laws (D-D fuel parameters used)
- SAND2006-7148 — Z-IFE study (geometry and IFE chamber analogy)

Changes from iter-1:
- compute_sensitivity() now correctly skips integer-typed fields (n_mod, n_turbines)
  to avoid passing floats to int-annotated parameters
- Q_sci in to_explorer_dict() mapped to fusion_gain_Q (acoustic gain, not Q_eng)
  with clearer inline comment
- Scenario comparison table reworked to show breakeven context
- KEY BINDING CONSTRAINTS section expanded with quantitative LCOE levers
- sensitivity_sweep() uses dataclasses.replace() approach for cleaner reconstruction

Changes from iter-2/iter-3 (source-integration pass, iter-4):
- d2o_unit_cost_per_m3 updated from $773,500/m³ ($700/kg) to $497,250/m³ ($450/kg),
  anchored to 2023 UN Comtrade empirical range $300–$475/kg (volume-weighted ~$450/kg).
  Source: wits-trade-comtrade-en-country-all-year-2023-tradeflow.md. Prior $700/kg
  (CANDU industry analogy) overstated by ~50%. Gap #14 partially resolved.
- KEY BINDING CONSTRAINTS section updated to cite empirical D₂O price range and
  India+Canada supply concentration (~80% of global D₂O exports by value, 2023).

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import json
import math
import dataclasses as dc
from dataclasses import dataclass

# === Reference power levels for CAS scaling laws (from 1costingfe) ===
P_TH_REF = 2500.0   # Reference thermal power [MW]
P_ET_REF = 1100.0   # Reference gross electric power [MW]


@dataclass
class SonofusionPlantParams:
    """
    Parameterized Acoustic ICF / Sonofusion power plant model.

    All parameters carry source annotations. Uncertainty tags:
      (no tag)               = well-established value with published source
      MODERATE UNCERTAINTY   = reasonable estimate from documented analogues
      HIGH UNCERTAINTY       = speculative or poorly constrained
      ASSUMED                = no source; engineering judgment only
      BLOCKING UNCERTAINTY   = foundational unknown — concept not viable without
                               resolving this (see analysis.md §Section 2)
    """

    # =========================================================================
    # ACOUSTIC DRIVER
    # =========================================================================

    acoustic_power_MW: float = 100.0
    """Electrical power drawn by acoustic transducer array per module [MW].
    This is the steady-state driver input power. For a continuous-wave acoustic
    system at 30 kHz, this drives the bubble field in the D₂O vessel.
    No reactor-scale estimate exists. Industrial ultrasonic cleaning systems run
    at kW to ~100 kW. Scaling to 100 MW is a multi-order-of-magnitude extrapolation.
    Ref: Industry analogy (Crest/Branson/Hielscher ultrasonic systems).
    HIGH UNCERTAINTY — no published reactor-scale acoustic driver power estimate."""

    acoustic_driver_efficiency: float = 0.85
    """Fraction of electrical input converted to acoustic power by PZT transducers.
    The APC International Model 90-4040 datasheet documents planar coupling Kp ≥ 0.55.
    Kp is the electromechanical coupling coefficient at resonance for a thin disk — it
    measures how much stored elastic energy couples to the electric field, NOT wall-plug
    efficiency. Wall-plug efficiency (electrical → acoustic power delivered to load) is
    higher than Kp at resonance in matched-load industrial service, but no published
    reactor-scale measurement exists. 85% is an optimistic upper-bound assumption, not
    a measured value. At Kp~0.55–0.65 (the only measured datapoint), the derivation
    of 85% wall-plug efficiency has no open-literature support.
    Source: APC International 90-4040 datasheet (Kp ≥ 0.55); americanpiezo-products-
    services-ultrasonic-power-transducers.md. No wall-plug efficiency cited in sources.
    Ref: analysis.md §Section 3 (Acoustic Driver).
    HIGH UNCERTAINTY — 85% is speculative; see sensitivity sweep for 0.55–0.85 range.
    IMPACT: η_driver affects Q breakeven threshold (see KEY BINDING CONSTRAINTS)."""

    fusion_gain_Q: float = 10.0
    """Fusion gain Q = P_fusion / P_acoustic (fusion power / acoustic power delivered).
    This is the 'scientific Q' vs acoustic input — analogous to NIF's target gain.
    The engineering Q (vs electrical input) = fusion_gain_Q × acoustic_driver_efficiency.
    Q > 1 is energy breakeven; Q >> 5 required for commercial LCOE.
    BLOCKING UNCERTAINTY — no fusion from acoustic cavitation has been demonstrated.
    Temperature gap: ~16,000 K demonstrated vs ~10⁸ K required (4 orders of magnitude).
    Ref: analysis.md §Section 2 (Challenge 1); bubble-fusion-scientific-history.md §Current.
    Baseline Q=10 is for illustration only. All LCOE values conditional on this Q."""

    transducer_cost_per_kW: float = 500.0
    """Capital cost of piezoelectric transducer array per kW of acoustic power [$/ kW].
    Industrial ultrasonic cleaning systems: $100–500/kW at kW scale.
    Medical ultrasound: $1,000–10,000/kW (much smaller scale, higher precision).
    Reactor scale requires: materials compatibility with neutron-activated D₂O,
    long-lifetime qualification, geometry around a 3m sphere.
    Source: Industry analogy; no reactor-scale cost estimate exists in literature.
    Ref: analysis.md §Section 5. MODERATE UNCERTAINTY — reactor qualification adds 2–5×."""

    acoustic_freq_kHz: float = 30.0
    """Acoustic driving frequency [kHz] — informational, not directly in cost model.
    UCLA Putterman group: 40 kHz (single-bubble); cited directly.
    20 kHz lower bound from general industrial ultrasonic range (not directly cited).
    30 kHz midpoint used here as interpolation.
    Source: ucla-putterman-group-sonoluminescence.md §Key Technical Facts.
    Ref: analysis.md §Section 5 (acoustic driving frequency row).
    MODERATE UNCERTAINTY — multi-bubble range inferred."""

    # =========================================================================
    # FUSION PHYSICS & ENERGY CONVERSION
    # =========================================================================

    blanket_energy_multiplication: float = 1.05
    """D-D blanket energy multiplication factor [dimensionless].
    D-D produces 2.45 MeV neutrons (50% of reactions) and charged particles (50%).
    No Li-6 breeding blanket needed (unlike D-T). Slight multiplication (1.05)
    from neutron moderation energy deposited in D₂O bulk.
    Source: 1costingfe costing_constants.yaml (D-D: no breeding, energy capture only).
    Ref: Standard nuclear data for D-D reactions in heavy water."""

    f_neutron_dd: float = 0.336
    """Fraction of D-D fusion energy carried by neutrons [dimensionless].
    D-D reaction channels (equal probability):
      Branch 1 (50%): D+D → T(1.01 MeV) + p(3.02 MeV), total 4.03 MeV/reaction
      Branch 2 (50%): D+D → He-3(0.82 MeV) + n(2.45 MeV), total 3.27 MeV/reaction
    Average energy: 0.5×4.03 + 0.5×3.27 = 3.65 MeV per event
    Neutron energy fraction: (0.5×2.45) / 3.65 = 1.225/3.65 ≈ 0.336
    Source: Standard nuclear physics / ENDF nuclear data.
    Ref: NuDat 2; analysis.md §Section 2 (Challenge 5 — D-D neutron economics)."""

    thermal_efficiency: float = 0.35
    """Thermal-to-electric conversion efficiency [fraction].
    D₂O heated to ~300°C → conventional Rankine steam cycle (BWR-like).
    35% is conservative; 40–45% possible with superheated steam if temperature permits.
    Source: Standard power engineering; no concept-specific design exists.
    Ref: SAND2006-7148 Rankine cycle reference; general steam cycle engineering.
    MODERATE UNCERTAINTY — depends on D₂O operating temperature and pressure."""

    # =========================================================================
    # GEOMETRY (spherical vessel — analogous to IFE chamber)
    # =========================================================================

    vessel_inner_radius_m: float = 3.0
    """Inner radius of D₂O-filled fusion vessel [m].
    The sphere filled with heavy water serves as acoustic medium, fusion medium,
    and primary coolant simultaneously. Impulse Devices experimental reactor:
    ~0.15m radius (1-foot sphere, $250K — source: bubble-fusion-scientific-history.md).
    Commercial plant analogy: IFE chamber radius ~3m (SAND2006-7148).
    Source: analysis.md §Section 3 (Reactor Vessel) + SAND2006-7148 chamber geometry.
    HIGH UNCERTAINTY — no power plant design; this is a dimensional analogy."""

    shield_thickness_m: float = 1.5
    """Biological shield thickness around vessel [m].
    D-D neutrons (2.45 MeV) are lower energy than D-T (14.1 MeV), reducing depth.
    D₂O is an excellent neutron moderator (CANDU experience), reducing external shield.
    1.5m conservative for a commercial D-D neutron field.
    Source: Analogy to D-T IFE shielding (SAND2006-7148) scaled for D-D neutron energy.
    Ref: 1costingfe shield_unit_cost with D-D fuel factor; SAND2006-7148.
    MODERATE UNCERTAINTY — no D-D power plant shielding calculation exists."""

    structure_thickness_m: float = 0.3
    """Primary structural shell thickness around shield [m].
    Source: Analogy to IFE chamber structural support (SAND2006-7148).
    ASSUMED — no acoustic ICF plant structural design."""

    vessel_wall_thickness_m: float = 0.15
    """Pressure vessel wall thickness (stainless steel sphere) [m].
    D₂O at ~10 MPa operating pressure, 3m radius sphere:
    Hoop stress formula: t = P×r/(2×σ_allow) = 10e6×3/(2×200e6) = 0.075m → ~0.15m with
    factor of 2 safety margin for nuclear-qualified construction.
    Source: ASME Boiler & Pressure Vessel Code Section III analogy.
    Ref: Structural engineering first principles. MODERATE UNCERTAINTY."""

    # =========================================================================
    # PLANT CONFIGURATION
    # =========================================================================

    n_mod: int = 4
    """Number of sonofusion modules (D₂O vessels) per plant [integer].
    Multiple modules reduce single-point failure risk and allow staged commissioning.
    Source: ASSUMED — no sonofusion plant design exists.
    Ref: Analogy to modular IFE concepts (SAND2006-7148 multi-chamber studies).
    NOTE: This integer field is excluded from sensitivity sweeps (non-differentiable)."""

    plant_availability: float = 0.75
    """Plant capacity factor / availability [fraction].
    Acoustic transducers in industrial service achieve >99% uptime (TRL 8–9).
    Key uncertainty: neutron-induced PZT degradation in a fusion environment.
    Also: D₂O management, tritium byproduct extraction, maintenance access.
    75% chosen as conservative for a novel nuclear system.
    Source: analysis.md §Section 6 (gap #10); CANDU availability ~90% (mature D₂O).
    Ref: No concept-specific estimate available. MODERATE UNCERTAINTY."""

    plant_lifetime_years: float = 40.0
    """Plant economic lifetime [years]. Standard nuclear plant assumption.
    Ref: 1costingfe convention; US nuclear plant regulatory life 40–60 years."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds 10% contingency and higher pre-construction costs.
    Ref: 1costingfe CAS29 convention (contingency_rate_foak = 0.10)."""

    # =========================================================================
    # CAS22 OVERRIDES — Sonofusion-specific subsystem costs
    # =========================================================================

    d2o_unit_cost_per_m3: float = 497_250.0
    """D₂O (heavy water) cost to fill vessel [$/m³].
    D₂O density ≈ 1,105 kg/m³. 2023 UN Comtrade data: actual global export prices
    $300–$475/kg (India ~$458/kg at 100,331 kg, Canada ~$474/kg at 80,701 kg,
    Romania ~$301/kg at 20,297 kg). Volume-weighted average ≈ $450/kg.
    $450/kg × 1,105 kg/m³ = $497,250/m³.
    Prior estimate of ~$700/kg (CANDU industry analogy) overstated by ~50%.
    Source: wits-trade-comtrade-en-country-all-year-2023-tradeflow.md (2023 UN Comtrade).
    Ref: analysis.md §Section 5 (D₂O fuel cost, gap #14 partially resolved).
    MODERATE UNCERTAINTY — price varies with global D₂O supply/demand; India+Canada
    account for ~80% of global D₂O exports by value (moderate supply concentration risk)."""

    vessel_structural_cost_M_USD: float = 15.0
    """Capital cost of stainless steel pressure vessel structure per module [$M].
    Impulse Devices experimental 1-foot sphere: ~$250K (source: analysis.md §Section 3).
    Commercial 3m radius pressure vessel: surface area ≈ 113 m². At $50K–150K/m²
    for nuclear-qualified stainless steel construction → $5.6M–$17M range.
    Using $15M as mid-range for nuclear-qualified construction.
    Source: analysis.md §Section 3 (Reactor Vessel) + ASME nuclear vessel cost analogy.
    MODERATE UNCERTAINTY — scale-up from experimental reactor is large extrapolation."""

    # =========================================================================
    # AUXILIARY POWER (recirculating loads)
    # =========================================================================

    p_tritium_handling_MW: float = 2.0
    """Tritium handling system power per plant [MW].
    D-D Branch 1 (~50%) produces tritium as a byproduct. Unlike D-T, no breeding
    blanket is needed, but produced tritium must be separated from D₂O and contained.
    Lower than D-T plant estimate (~10 MW in 1costingfe).
    Source: 1costingfe fuel_handling_dd baseline; reduced from D-T. ASSUMED."""

    p_house_MW: float = 4.0
    """Housekeeping electrical load per plant [MW].
    Source: 1costingfe ife_zpinch.yaml default. ASSUMED."""

    p_cryo_MW: float = 0.1
    """Cryoplant power per plant [MW]. Minimal — no superconducting magnets.
    Source: 1costingfe IFE/MIF default reduced for absence of SC magnet system. ASSUMED."""

    p_d2o_circulation_MW: float = 3.0
    """D₂O primary coolant circulation and heat exchange pumping power per plant [MW].
    CANDU reactor primary coolant pumping: ~10 MW per GWth thermal.
    Scaled proportionally to sonofusion plant thermal power.
    Source: CANDU design data analogy. ASSUMED."""

    # =========================================================================
    # FINANCIAL
    # =========================================================================

    interest_rate: float = 0.10
    """Real discount rate / WACC [fraction].
    Set higher than mature nuclear (8%) to reflect technological risk of a concept
    with undemonstrated fusion physics. Pre-commercial fusion projects face 10–15%
    WACC in venture/government-backed scenarios.
    Source: Fusion industry financing analogies; risk-adjusted WACC convention.
    MODERATE UNCERTAINTY — actual financing terms unknown until concept proven."""

    inflation_rate: float = 0.02
    """General inflation rate [fraction].
    Ref: 1costingfe default; US Fed long-run target 2%."""

    construction_time_years: float = 6.0
    """Construction period [years].
    Ref: 1costingfe reference_construction_time = 6.0 years."""

    # =========================================================================
    # OPERATING COSTS
    # =========================================================================

    om_cost_per_MW_yr: float = 80.0
    """O&M cost per MW net electric capacity per year [$/MW/yr].
    Higher than MagLIF baseline ($60/MW/yr) due to:
    - Novel technology with uncertain maintenance requirements
    - Neutron activation of D₂O vessel and transducer components
    - Potential transducer replacement cycles under irradiation
    - Tritium byproduct extraction and containment operations
    Source: 1costingfe CAS71 D-D baseline ($39M/GWe × 1000/$MW = $39/MW/yr), scaled up
    for technology novelty. Using $80/MW/yr (2× the mature D-D estimate).
    Ref: 1costingfe costing_constants.yaml (om_cost_dd). MODERATE UNCERTAINTY."""

    core_lifetime_FPY: float = 10.0
    """Transducer array lifetime [full-power-years] before scheduled replacement.
    D-D neutrons (2.45 MeV) cause less damage per neutron than D-T (14.1 MeV).
    Industrial PZT transducers are extremely reliable in non-irradiated service.
    Neutron irradiation effects on PZT in fusion-relevant fluences: unstudied.
    Using D-D core lifetime analogy from 1costingfe (core_lifetime_dd = 10.0 FPY).
    Source: 1costingfe costing_constants.yaml.
    Ref: analysis.md §Section 6 (gap #13 — PZT irradiation unknown).
    MODERATE UNCERTAINTY — could be much shorter if PZT is radiation-sensitive."""

    d2o_annual_replenishment_frac: float = 0.02
    """Fraction of D₂O inventory replaced annually [fraction/year].
    Accounts for: deuterium consumed in fusion, tritium extraction losses,
    D₂O radiolysis under neutron irradiation, and handling losses.
    CANDU reactors replenish ~1–3% of D₂O inventory annually.
    Source: CANDU operational data analogy.
    Ref: analysis.md §Section 4 (Working Fluid). ASSUMED."""

    # =========================================================================
    # COMPUTE METHODS
    # =========================================================================

    def _compute_power(self) -> dict:
        """Layer 1: Power balance — electrical driver → acoustic → fusion → electricity."""
        r = {}

        # Acoustic power delivered to D₂O medium after transducer conversion losses
        p_acoustic = self.acoustic_power_MW * self.acoustic_driver_efficiency
        r["p_acoustic"] = p_acoustic

        # Fusion thermal power: Q × acoustic power delivered
        # Q = P_fusion / P_acoustic (gain vs acoustic input, not vs electrical input)
        p_fus = p_acoustic * self.fusion_gain_Q
        r["p_fus"] = p_fus

        # D-D energy partitioning between reaction channels
        f_charged = 1.0 - self.f_neutron_dd
        r["p_neutron"] = p_fus * self.f_neutron_dd    # 2.45 MeV neutrons (Branch 2, 50%)
        r["p_charged"] = p_fus * f_charged             # p + T charged particles (Branch 1, 50%)

        # Thermal power in D₂O:
        #   (1) Acoustic energy that does NOT go to fusion thermalizes in D₂O
        #   (2) Charged particle energy stops in D₂O (range ~ mm in liquid)
        #   (3) Neutron energy thermalizes in D₂O × blanket multiplication
        # NOTE: acoustic energy that DOES create fusion (p_acoustic × efficiency × Q)
        # is already accounted via fusion products; acoustic energy that doesn't
        # drive fusion still thermalizes. Total acoustic power thermalizes + fusion products.
        p_th = (p_acoustic                                              # all acoustic input thermalizes
                + r["p_charged"]                                        # charged particles stop in D₂O
                + r["p_neutron"] * self.blanket_energy_multiplication)  # neutrons moderate in D₂O
        r["p_th"] = p_th

        # Gross electric via Rankine cycle on D₂O
        p_et = p_th * self.thermal_efficiency
        r["p_et"] = p_et

        # Recirculating loads (per module basis; plant-wide total in _compute_costs)
        # p_aux is per-plant, not per-module — divide by n_mod for per-module accounting
        p_aux_per_plant = (self.p_tritium_handling_MW
                           + self.p_house_MW
                           + self.p_cryo_MW
                           + self.p_d2o_circulation_MW)
        r["p_aux_per_plant"] = p_aux_per_plant

        # Net electric per module: gross − electrical driver draw − per-module aux share
        p_net = p_et - self.acoustic_power_MW - (p_aux_per_plant / self.n_mod)
        r["p_net"] = p_net

        # Engineering Q = P_fusion / P_electrical_driver (the relevant economic Q)
        # Q_eng < fusion_gain_Q because fusion_gain_Q is vs acoustic (post-transducer)
        r["Q_eng"] = p_fus / self.acoustic_power_MW    # P_fus / P_elec_driver

        # Q_sci = fusion_gain_Q (acoustic Q), reported separately for context
        r["Q_sci"] = self.fusion_gain_Q

        # Recirculating fraction = (driver + aux) / gross electric (per plant)
        p_et_plant = p_et * self.n_mod
        if p_et_plant > 0:
            r["recirc_fraction"] = (self.acoustic_power_MW * self.n_mod
                                    + p_aux_per_plant) / p_et_plant
        else:
            r["recirc_fraction"] = float('inf')

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Spherical geometry for D₂O vessel and surrounding structures."""
        r = {}
        ri = self.vessel_inner_radius_m

        def sphere_shell_vol(r_in: float, thickness: float) -> float:
            r_out = r_in + thickness
            return (4.0 / 3.0) * math.pi * (r_out**3 - r_in**3)

        # Inner D₂O volume (filled sphere) — fusion medium + primary coolant
        r["d2o_vol_m3"] = (4.0 / 3.0) * math.pi * ri**3

        # Stainless steel pressure vessel wall
        r["vessel_wall_vol_m3"] = sphere_shell_vol(ri, self.vessel_wall_thickness_m)
        r_vessel_out = ri + self.vessel_wall_thickness_m

        # Biological shield shell
        r["shield_vol_m3"] = sphere_shell_vol(r_vessel_out, self.shield_thickness_m)
        r_shield_out = r_vessel_out + self.shield_thickness_m

        # Primary structural shell
        r["structure_vol_m3"] = sphere_shell_vol(r_shield_out, self.structure_thickness_m)
        r["total_outer_radius_m"] = r_shield_out + self.structure_thickness_m

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts.
        Per-module accounts use sonofusion-specific overrides where standard
        1costingfe scaling laws do not apply. Plant-wide accounts follow 1costingfe."""
        r = {}
        p_th = max(power["p_th"], 1.0)
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)

        # ── Per-module accounts ──────────────────────────────────────────────

        # C220101: D₂O Vessel + Liquid  [OVERRIDE]
        # In standard 1costingfe: blanket_unit_cost × volume × (p_th/P_TH_REF)^0.6
        # Override because D₂O cost dominates and scales with volume (not power density).
        # D-D blanket_unit_cost_dd = 0.30 M$/m³ from 1costingfe; but D₂O at $773,500/m³
        # is far more expensive than the 1costingfe energy-capture blanket reference.
        # OVERRIDE: direct material + structural cost.
        d2o_fill_cost_M = (self.d2o_unit_cost_per_m3 * geom["d2o_vol_m3"]) / 1e6
        r["C220101"] = d2o_fill_cost_M + self.vessel_structural_cost_M_USD

        # C220102: Shield (biological — 2.45 MeV D-D neutron + gamma)
        # 1costingfe scaling: shield_unit_cost_dt = 0.74 M$/m³ × fuel scale factor.
        # D-D scale factor: 0.65 (lower neutron energy, 2.45 MeV vs 14.1 MeV D-T).
        # DEFAULT: 1costingfe shield_unit_cost (0.74 M$/m³) × 0.65 D-D factor.
        shield_unit_cost_dd = 0.74 * 0.65   # M$/m³  [DEFAULT 1costingfe × D-D scale]
        r["C220102"] = (shield_unit_cost_dd
                        * geom["shield_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: Coils  [NOT APPLICABLE — no magnetic confinement]
        r["C220103"] = 0.0

        # C220104: Supplementary Heating  [NOT APPLICABLE — acoustic driver in C220107]
        r["C220104"] = 0.0

        # C220105: Primary Structure (vessel frame, seismic isolation, supports)
        # DEFAULT 1costingfe: structure_unit_cost = 0.15 M$/m³
        structure_unit_cost = 0.15   # M$/m³  [DEFAULT 1costingfe structure_unit_cost]
        r["C220105"] = (structure_unit_cost
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: D₂O Circulation System  [OVERRIDE — replaces vacuum system]
        # The vessel is pressurized D₂O (not vacuum). Primary heat exchange loop
        # pumps D₂O through steam generators.
        # ASSUMED: CANDU primary coolant circuit analogy: ~$50M per GWth thermal.
        d2o_circ_base_per_gwth = 50.0   # M$/GWth  [ASSUMED: CANDU circuit analogy]
        r["C220106"] = d2o_circ_base_per_gwth * (p_th / 1000.0)

        # C220107: Acoustic Transducer Array  [OVERRIDE — replaces power supplies]
        # Standard 1costingfe: power_supplies_base = 80.0 M$ × (p_et/1000)^0.7
        # Override: transducer array cost = cost/kW × acoustic power output in kW.
        # p_acoustic is the output from the transducer (post-conversion), not input.
        p_acoustic = power["p_acoustic"]
        r["C220107"] = (self.transducer_cost_per_kW * p_acoustic * 1e3) / 1e6   # M$

        # C220108: D₂O Fuel Management System  [OVERRIDE — analogous to IFE target factory]
        # Handles: tritium extraction from D₂O, deuterium replenishment, D₂O chemistry
        # control, isotopic purity monitoring. Bulk liquid management; simpler than IFE.
        # Scale factor 0.20 applied to 1costingfe target_factory_base (244 M$ at 1 GWe).
        # ASSUMED: 0.20 scale factor — bulk liquid much simpler than discrete targets.
        target_factory_base = 244.0   # M$ at 1 GWe  [DEFAULT 1costingfe target_factory_base]
        d2o_mgmt_scale = 0.20         # [ASSUMED: bulk liquid vs. discrete IFE targets]
        r["C220108"] = d2o_mgmt_scale * target_factory_base * (p_et / 1000.0) ** 0.7

        # C220109: Direct Energy Converter  [NOT APPLICABLE — thermal cycle only]
        r["C220109"] = 0.0

        # C220111: Installation labor (14% of reactor equipment subtotal)
        # DEFAULT from 1costingfe: installation_frac = 0.14
        installation_frac = 0.14   # [DEFAULT 1costingfe installation_frac]
        reactor_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109"
        ])
        r["C220111"] = installation_frac * reactor_subtotal

        # C220112: Tritium Separation (D-D byproduct removal from D₂O)
        # D-D Branch 1 produces tritium; must be separated for safety.
        # Less extensive than D-T breeding infrastructure; scales with plant size.
        # ASSUMED: $5M at 1 GWe reference, (p_net/1000)^0.7 power-law scaling.
        r["C220112"] = 5.0 * (p_net / 1000.0) ** 0.7   # [ASSUMED]

        # Per-module subtotal
        r["CAS22_per_module"] = reactor_subtotal + r["C220111"] + r["C220112"]

        # ── Plant-wide accounts ──────────────────────────────────────────────
        p_net_total = p_net * self.n_mod
        p_th_total = p_th * self.n_mod

        # C220200: Main & Secondary Coolant (D₂O → steam generators → Rankine)
        C220201 = 166.0 * (p_net_total / 1000.0)               # [DEFAULT 1costingfe]
        C220202 = 40.6 * (p_th_total / 3500.0) ** 0.55         # [DEFAULT 1costingfe]
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling + Cryoplant (minimal — no SC magnets)
        C220301 = 1.1e-3 * p_th_total                                  # [DEFAULT 1costingfe]
        C220302 = 200.0 * (max(self.p_cryo_MW, 0.01) / 30.0) ** 0.7   # [DEFAULT 1costingfe]
        r["C220300"] = C220301 + C220302

        # C220400: Radioactive Waste Management
        # D-D: ~0.5× D-T activation rate (lower neutron energy, less activation,
        # no Li-bearing blanket waste). DEFAULT 1costingfe × 0.5 D-D scale factor.
        r["C220400"] = 1.96 * 0.5 * (p_th_total / 1000.0)   # [DEFAULT × 0.5 D-D scale]

        # C220500: Fuel Handling (D-D baseline)
        # Includes: D₂O storage/inventory management, small-scale tritium containment.
        # fuel_handling_dd_base = 60.0 M$ at 1 GWe from 1costingfe.
        fuel_handling_base = 60.0   # M$ at 1 GWe  [DEFAULT 1costingfe fuel_handling_dd_base]
        r["C220500"] = fuel_handling_base * (p_net_total / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        r["C220600"] = 11.5 * (p_net_total / 1000.0) ** 0.8   # [DEFAULT 1costingfe]

        # C220700: Instrumentation & Control
        r["C220700"] = 85.0 * (p_th_total / 3500.0) ** 0.65   # [DEFAULT 1costingfe]

        # Plant-wide subtotal
        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"
        ])

        # Total CAS22 = (per-module subtotal × n_mod) + plant-wide
        r["CAS22"] = r["CAS22_per_module"] * self.n_mod + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: CAS10-60 capital costs following 1costingfe structure."""
        r = {}
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)
        p_net_total = p_net * self.n_mod
        p_et_total = p_et * self.n_mod

        # CAS10: Pre-construction costs
        # D-D licensing lower than D-T (lower neutron energy, no tritium breeding).
        # licensing_cost_dd = 3.0 M$ (FOAK/NOAK from 1costingfe costing_constants.yaml).
        site_permits = 3.0         # M$  [DEFAULT 1costingfe site_permits]
        plant_studies = 4.0 if self.noak else 20.0    # M$  [DEFAULT 1costingfe]
        plant_permits = 2.0        # M$  [DEFAULT 1costingfe plant_permits]
        plant_reports = 1.0        # M$  [DEFAULT 1costingfe plant_reports]
        other_precon = 1.0         # M$  [DEFAULT 1costingfe other_precon]
        land_cost = 0.25 * p_net_total * math.sqrt(self.n_mod) * 10_000 / 1e6  # [DEFAULT]
        licensing_cost = 1.5 if self.noak else 3.0    # M$  [DEFAULT 1costingfe licensing_cost_dd]
        r["CAS10"] = (site_permits + plant_studies + plant_permits + plant_reports
                      + other_precon + land_cost + licensing_cost)

        # CAS21: Buildings
        # D-D modifications vs D-T 1costingfe baseline:
        # - hot_cell: 0.5× (no D-T tritium processing wing; small D-D tritium separation only)
        # - cryogenics: 0 (no SC magnet cryoplant building needed)
        # All others: DEFAULT from 1costingfe building_costs_per_kw
        building_cost_per_kw = {
            "site_improvements":    268.0,   # [DEFAULT 1costingfe]
            "fusion_heat_island":   126.0,   # [DEFAULT 1costingfe]
            "turbine_building":      54.0,   # [DEFAULT 1costingfe]
            "heat_exchanger":        12.0,   # [DEFAULT 1costingfe]
            "power_supply_storage":  17.0,   # [DEFAULT 1costingfe] — houses transducer power amps
            "reactor_auxiliaries":   35.0,   # [DEFAULT 1costingfe]
            "hot_cell":              46.7,   # 0.5× D-T standard (small D-D tritium separation)
            "reactor_services":      25.0,   # [DEFAULT 1costingfe]
            "service_water":         11.0,   # [DEFAULT 1costingfe]
            "fuel_storage":           9.1,   # [DEFAULT 1costingfe]
            "control_room":          17.0,   # [DEFAULT 1costingfe]
            "onsite_ac":             21.0,   # [DEFAULT 1costingfe]
            "administration":        10.0,   # [DEFAULT 1costingfe]
            "site_services":          4.0,   # [DEFAULT 1costingfe]
            "cryogenics":             0.0,   # N/A — no SC magnets
            "security":               8.0,   # [DEFAULT 1costingfe]
            "ventilation_stack":      9.2,   # [DEFAULT 1costingfe]
            "assembly_hall":         20.0,   # [DEFAULT 1costingfe]
        }
        total_building_per_kw = sum(building_cost_per_kw.values())
        r["CAS21"] = total_building_per_kw * p_et_total / 1000.0   # M$
        r["CAS21_total_per_kw"] = total_building_per_kw

        # CAS22: Reactor Plant Equipment (from _compute_cas22)
        r["CAS22"] = cas22["CAS22"]

        # CAS23–26: Balance of Plant (steam Rankine on D₂O system)
        turbine_per_mw  = 0.19764   # M$/MW  [DEFAULT 1costingfe turbine_per_mw]
        electric_per_mw = 0.08418   # M$/MW  [DEFAULT 1costingfe electric_per_mw]
        misc_per_mw     = 0.05124   # M$/MW  [DEFAULT 1costingfe misc_per_mw]
        heat_rej_per_mw = 0.03416   # M$/MW  [DEFAULT 1costingfe heat_rej_per_mw]
        r["CAS23"] = p_et_total * turbine_per_mw
        r["CAS24"] = p_et_total * electric_per_mw
        r["CAS25"] = p_et_total * misc_per_mw
        r["CAS26"] = p_et_total * heat_rej_per_mw

        # CAS27: Special Materials — D-D baseline ($2M at 1 GWe from 1costingfe)
        # Initial D₂O fill is already in C220101. This covers other special materials.
        r["CAS27"] = 2.0   # M$  [DEFAULT 1costingfe special_materials_dd]

        # CAS28: Digital Twin
        r["CAS28"] = 5.0   # M$  [DEFAULT 1costingfe digital_twin]

        # CAS29: Contingency on direct costs
        cas20_subtotal = sum(r[k] for k in [
            "CAS21", "CAS22", "CAS23", "CAS24", "CAS25", "CAS26", "CAS27", "CAS28"
        ])
        contingency_rate = 0.0 if self.noak else 0.10   # [DEFAULT 1costingfe]
        r["CAS29"] = contingency_rate * cas20_subtotal

        # CAS20: Total Direct Costs
        r["CAS20"] = cas20_subtotal + r["CAS29"]

        # CAS30: Indirect Costs (20% of CAS20, scaled by construction time)
        ref_construction_time = 6.0   # years  [DEFAULT 1costingfe reference_construction_time]
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / ref_construction_time)

        # CAS40: Owner's Costs — D-D: $31M at 1 GWe from 1costingfe
        owner_cost_dd = 31.0   # M$ at 1 GWe  [DEFAULT 1costingfe owner_cost_dd]
        r["CAS40"] = owner_cost_dd * (p_net_total / 1000.0) ** 0.5

        # CAS50: Supplementary Costs (spare parts, shipping, taxes, insurance, decom)
        cas22_to_28 = sum(r[k] for k in ["CAS22", "CAS23", "CAS24", "CAS25",
                                          "CAS26", "CAS27", "CAS28"])
        spare_parts = 0.025 * cas22_to_28                         # [DEFAULT D-D: spare_parts_frac_dd]
        shipping = 0.015 * r["CAS20"]                             # [DEFAULT 1costingfe shipping_frac]
        taxes = 0.01 * r["CAS20"]                                 # [DEFAULT 1costingfe tax_frac]
        construction_insurance = 0.015 * (r["CAS20"] + r["CAS30"])  # [DEFAULT 1costingfe]
        startup_fuel = 0.1 * (p_net_total / 1000.0)               # [DEFAULT 1costingfe startup_fuel_dd]
        decom = 5.0                                                # M$  [ASSUMED: simplified]
        r["CAS50"] = (spare_parts + shipping + taxes
                      + construction_insurance + startup_fuel + decom)

        # Overnight Capital
        overnight = r["CAS10"] + r["CAS20"] + r["CAS30"] + r["CAS40"] + r["CAS50"]
        r["overnight_capital"] = overnight

        # CAS60: Interest During Construction (IDC)
        # f_IDC = ((1+i)^T - 1) / (i×T) - 1  [convention from MagLIF model / 1costingfe]
        i = self.interest_rate
        T = self.construction_time_years
        if i > 0 and T > 0:
            f_idc = ((1 + i) ** T - 1) / (i * T) - 1
        else:
            f_idc = 0.0
        r["CAS60"] = f_idc * overnight
        r["f_IDC"] = f_idc

        # Total Capital (overnight + IDC)
        r["total_capital"] = overnight + r["CAS60"]

        # Specific capital cost [$/kWe]
        p_net_plant = power["p_net"] * self.n_mod
        if p_net_plant > 0:
            r["specific_capital_USD_per_kWe"] = r["total_capital"] * 1e6 / (p_net_plant * 1e3)
        else:
            r["specific_capital_USD_per_kWe"] = float('inf')

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70-90 annualized costs and LCOE."""
        r = {}
        p_net = power["p_net"]
        p_net_total = p_net * self.n_mod

        # Capital Recovery Factor
        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1 + i) ** n / ((1 + i) ** n - 1)
        r["CRF"] = crf

        # CAS90: Annualized Capital Charge
        r["CAS90"] = crf * costs["total_capital"]   # M$/year

        # CAS71: Levelized O&M (growing annuity at inflation rate)
        annual_om_base = self.om_cost_per_MW_yr * p_net_total * 1e3 / 1e6   # M$
        g = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g) ** Tc    # First year of operation cost
        if abs(i - g) > 1e-10:
            pv_growing = A1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
        else:
            pv_growing = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_growing   # M$/year

        # CAS72: Scheduled Replacement (transducer array replacement)
        # The transducer array (C220107 × n_mod) is the primary replaceable sub-account.
        # D₂O replenishment handled in CAS80.
        eff_years_per_replacement = self.core_lifetime_FPY / self.plant_availability
        n_replacements = max(0, int(math.ceil(
            self.plant_lifetime_years / eff_years_per_replacement)) - 1)
        transducer_replacement_cost = cas22["C220107"] * self.n_mod   # Total array cost M$
        pv_replacements = 0.0
        for k in range(1, n_replacements + 1):
            year = k * eff_years_per_replacement
            if year < self.plant_lifetime_years:
                pv_replacements += transducer_replacement_cost / (1 + i) ** year
        r["CAS72"] = crf * pv_replacements   # M$/year
        r["n_transducer_replacements"] = n_replacements

        # CAS70: Total O&M
        r["CAS70"] = r["CAS71"] + r["CAS72"]

        # CAS80: Annualized Fuel & Consumables
        # Primary fuel cost: annual D₂O replenishment.
        total_d2o_vol_m3 = (4.0 / 3.0) * math.pi * self.vessel_inner_radius_m**3 * self.n_mod
        annual_d2o_replenish_m3 = self.d2o_annual_replenishment_frac * total_d2o_vol_m3
        annual_d2o_cost_M = annual_d2o_replenish_m3 * self.d2o_unit_cost_per_m3 / 1e6
        r["CAS80"] = annual_d2o_cost_M   # M$/year
        r["CAS80_d2o_m3_per_yr"] = annual_d2o_replenish_m3

        # LCOE
        annual_revenue_req = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_revenue_req

        annual_energy_MWh = 8760.0 * p_net_total * self.plant_availability
        r["annual_energy_MWh"] = annual_energy_MWh

        if annual_energy_MWh > 0 and p_net_total > 0:
            r["lcoe_USD_per_MWh"] = annual_revenue_req * 1e6 / annual_energy_MWh
            r["lcoe_cents_per_kWh"] = r["lcoe_USD_per_MWh"] / 10.0
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
        """
        Compute LCOE and all intermediate results using CAS-structured accounting.
        Returns nested dict: {power, geometry, cas22, costs, economics} plus aliases.
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
            # Convenience aliases
            "net_electric_MW": power["p_net"] * self.n_mod,
            "lcoe_cents_per_kWh": econ["lcoe_cents_per_kWh"],
            "total_capital_M_USD": costs["total_capital"],
        }


# =============================================================================
# MODULE-LEVEL INTERFACE (consumed by concept explorer at import time)
# =============================================================================

params = SonofusionPlantParams()
results = params.compute()


def to_explorer_dict() -> dict:
    """Return structured data for the concept explorer.
    All monetary values in M$ (millions USD). All power values in MW.
    Maps from compute() output structure to the explorer's expected schema.
    """
    c = results["costs"]
    pw = results["power"]
    econ = results["economics"]
    cas22 = results["cas22"]
    p_net_total = pw["p_net"] * params.n_mod

    overnight_cost_per_kw = (
        c["overnight_capital"] * 1e3 / p_net_total if p_net_total > 0 else float("inf")
    )

    return {
        "costs": {
            # CAS direct accounts [M$]
            "cas10": c["CAS10"],
            "cas21": c["CAS21"],
            "cas22": c["CAS22"],
            "cas23": c["CAS23"],
            "cas24": c["CAS24"],
            "cas25": c["CAS25"],
            "cas26": c["CAS26"],
            "cas27": c["CAS27"],
            "cas28": c["CAS28"],
            "cas29": c["CAS29"],
            "cas20": c["CAS20"],
            "cas30": c["CAS30"],
            "cas40": c["CAS40"],
            "cas50": c["CAS50"],
            "cas60": c["CAS60"],
            "cas70": econ["CAS70"],
            "cas71": econ["CAS71"],
            "cas72": econ["CAS72"],
            "cas80": econ["CAS80"],
            "cas90": econ["CAS90"],
            "total_capital": c["total_capital"],        # [M$] includes IDC
            "lcoe": econ["lcoe_USD_per_MWh"],            # [$/MWh]
            "overnight_cost": overnight_cost_per_kw,     # [$/kW]
        },
        "power_table": {
            "p_fus": pw["p_fus"] * params.n_mod,        # Total fusion power [MW]
            "p_th": pw["p_th"] * params.n_mod,           # Total thermal [MW]
            "p_et": pw["p_et"] * params.n_mod,           # Gross electric [MW]
            "p_net": p_net_total,                         # Net electric [MW]
            "q_sci": pw["Q_sci"],                         # Scientific Q (vs acoustic power)
            "q_eng": pw["Q_eng"],                         # Engineering Q (vs electrical input)
            "availability": params.plant_availability,    # Capacity factor [0-1]
            "rec_frac": pw["recirc_fraction"],             # Recirculating fraction [0-1]
        },
        "cas22_detail": {
            # Per-module sub-accounts [M$] (single module values)
            "C220101": cas22["C220101"],    # D₂O vessel + liquid [OVERRIDE]
            "C220102": cas22["C220102"],    # Shield (biological, D-D neutrons)
            "C220103": cas22["C220103"],    # Coils [N/A → 0]
            "C220104": cas22["C220104"],    # Supplementary heating [N/A → 0]
            "C220105": cas22["C220105"],    # Primary structure
            "C220106": cas22["C220106"],    # D₂O circulation system [OVERRIDE]
            "C220107": cas22["C220107"],    # Acoustic transducer array [OVERRIDE]
            "C220108": cas22["C220108"],    # D₂O management system [OVERRIDE]
            "C220109": cas22["C220109"],    # Direct energy converter [N/A → 0]
            "C220111": cas22["C220111"],    # Installation (14% of subtotal)
            "C220112": cas22["C220112"],    # Tritium separation (D-D byproduct)
            # Plant-wide sub-accounts [M$]
            "C220200": cas22["C220200"],    # Coolant systems
            "C220300": cas22["C220300"],    # Auxiliary cooling + cryoplant
            "C220400": cas22["C220400"],    # Radioactive waste management
            "C220500": cas22["C220500"],    # Fuel handling (D-D)
            "C220600": cas22["C220600"],    # Other equipment
            "C220700": cas22["C220700"],    # Instrumentation & control
        },
        "params": {
            f.name: getattr(params, f.name)
            for f in dc.fields(params)
            if isinstance(getattr(params, f.name), (int, float))
        },
        "overridden": [],   # Freeform script; overrides documented inline
    }


def compute_sensitivity(dp_fraction: float = 0.01) -> dict:
    """Compute LCOE elasticities for all numeric parameters via central difference.

    Returns {"engineering": {param: elasticity}, "financial": {param: elasticity}}.
    Elasticity = (d LCOE / d param) × (param / LCOE) — dimensionless.

    Integer-typed fields (n_mod) are excluded because central difference
    requires continuous variation and int params would produce float instances
    that break type expectations in the dataclass.
    """
    base_lcoe = results["economics"]["lcoe_USD_per_MWh"]
    if base_lcoe <= 0 or not math.isfinite(base_lcoe):
        return {"engineering": {}, "financial": {}}

    # Fields to exclude from sensitivity (integer or boolean parameters)
    integer_fields = {f.name for f in dc.fields(params) if f.type in ("int", int)}
    bool_fields = {f.name for f in dc.fields(params) if f.type in ("bool", bool)}
    skip_fields = integer_fields | bool_fields

    financial_keys = {"interest_rate", "inflation_rate"}
    engineering: dict = {}
    financial: dict = {}

    base_dict = dc.asdict(params)

    for f in dc.fields(params):
        if f.name in skip_fields:
            continue
        val = getattr(params, f.name)
        if not isinstance(val, (int, float)) or val == 0.0:
            continue
        dp = abs(val) * dp_fraction

        kw_up = {**base_dict, f.name: val + dp}
        lcoe_up = type(params)(**kw_up).compute()["economics"]["lcoe_USD_per_MWh"]

        kw_dn = {**base_dict, f.name: val - dp}
        lcoe_dn = type(params)(**kw_dn).compute()["economics"]["lcoe_USD_per_MWh"]

        if not (math.isfinite(lcoe_up) and math.isfinite(lcoe_dn)):
            continue
        elast = (lcoe_up - lcoe_dn) / (2 * dp) * val / base_lcoe
        target = financial if f.name in financial_keys else engineering
        target[f.name] = elast

    return {"engineering": engineering, "financial": financial}


# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

def print_results(p: SonofusionPlantParams, r: dict):
    """Pretty-print LCOE model results with full CAS breakdown."""
    power = r["power"]
    geom = r["geometry"]
    cas22 = r["cas22"]
    costs = r["costs"]
    econ = r["economics"]

    print("=" * 70)
    print("Acoustic ICF / Sonofusion (D-D) — 1cFE CAS-Structured LCOE Model")
    print("=" * 70)
    print("  *** SPECULATIVE — fusion from acoustic cavitation undemonstrated ***")
    print("  *** Q is hypothetical; breakeven requires Q ≥ ~3.5 (baseline params)")
    print("  *** η_driver=85% is UNSUPPORTED — only Kp≥55% measured (APC 90-4040)")
    print("  *** At η_driver=0.60, breakeven Q threshold shifts to ~5.6 ***")

    # --- Key Inputs ---
    print(f"\n--- Key Input Parameters ---")
    print(f"  Acoustic driver power:      {p.acoustic_power_MW:.0f} MW (elec) per module")
    p_ac = p.acoustic_power_MW * p.acoustic_driver_efficiency
    print(f"  Driver efficiency (PZT):    {p.acoustic_driver_efficiency:.1%} → {p_ac:.0f} MW acoustic")
    print(f"  Fusion gain Q (acoustic):   {p.fusion_gain_Q:.1f}  [*** SPECULATIVE ***]")
    print(f"  Acoustic frequency:         {p.acoustic_freq_kHz:.0f} kHz")
    d2o_vol = (4.0/3.0) * math.pi * p.vessel_inner_radius_m**3
    print(f"  Vessel inner radius:        {p.vessel_inner_radius_m:.1f} m  "
          f"(D₂O vol = {d2o_vol:.0f} m³/module)")
    print(f"  Blanket mult (D-D):         {p.blanket_energy_multiplication:.2f}")
    print(f"  Thermal efficiency:         {p.thermal_efficiency:.1%} (Rankine/D₂O)")
    print(f"  Plant availability:         {p.plant_availability:.1%}")
    print(f"  Modules:                    {p.n_mod}")
    print(f"  FOAK/NOAK:                  {'NOAK' if p.noak else 'FOAK'}")
    print(f"  Interest rate:              {p.interest_rate:.1%}")
    print(f"  Plant lifetime:             {p.plant_lifetime_years:.0f} years")

    # --- Power Balance (per module) ---
    print(f"\n--- Power Balance (per module) ---")
    print(f"  Acoustic power in D₂O:      {power['p_acoustic']:.0f} MW")
    print(f"  Fusion power (Q×acoustic):  {power['p_fus']:.0f} MW")
    print(f"    D-D neutron:              {power['p_neutron']:.0f} MW ({p.f_neutron_dd:.1%}, 2.45 MeV)")
    print(f"    D-D charged (p+T):        {power['p_charged']:.0f} MW ({1-p.f_neutron_dd:.1%})")
    print(f"  Thermal power in D₂O:       {power['p_th']:.0f} MW")
    print(f"  Gross electric (Rankine):   {power['p_et']:.0f} MWe")
    print(f"  Recirculating loads:")
    print(f"    Acoustic driver:          {p.acoustic_power_MW:.0f} MW (elec)")
    print(f"    Aux (plant share/mod):    {power['p_aux_per_plant']/p.n_mod:.1f} MW")
    print(f"  Net electric per module:    {power['p_net']:.0f} MWe")
    print(f"  Net electric (all modules): {power['p_net'] * p.n_mod:.0f} MWe")
    print(f"  Q_sci (acoustic):           {power['Q_sci']:.1f}  (P_fus / P_acoustic)")
    print(f"  Q_eng (electrical):         {power['Q_eng']:.1f}  (P_fus / P_elec_driver)")
    print(f"  Recirculating fraction:     {power['recirc_fraction']:.1%}  (plant total)")

    # --- CAS22: Reactor Plant Equipment ---
    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    print(f"  Per-module accounts (single module):")
    cas22_labels = {
        "C220101": "D₂O Vessel + Liquid     [OVERRIDE]",
        "C220102": "Shield (biolog, D-D n)  [D-D scale]",
        "C220103": "Coils                   [N/A → $0]",
        "C220104": "Supp. Heating           [N/A → $0]",
        "C220105": "Primary Structure",
        "C220106": "D₂O Circulation System  [OVERRIDE]",
        "C220107": "Acoustic Transducer Arr [OVERRIDE]",
        "C220108": "D₂O Management System   [OVERRIDE]",
        "C220109": "Direct Energy Conv      [N/A → $0]",
        "C220111": "Installation (14%)",
        "C220112": "Tritium Sep (D-D byprod)",
    }
    for code, label in cas22_labels.items():
        val = cas22[code]
        if val > 0.01:
            print(f"    {code} {label:<38s} ${val:>8.1f}M")
        elif val == 0.0:
            print(f"    {code} {label:<38s}     $0.0M")
    print(f"  {'─' * 58}")
    print(f"    Per-module subtotal:                              ${cas22['CAS22_per_module']:>8.1f}M × {p.n_mod}")

    print(f"  Plant-wide accounts:")
    pw_labels = {
        "C220200": "Coolant (D₂O → steam gen)",
        "C220300": "Aux Cooling + Cryoplant",
        "C220400": "Rad Waste (D-D, 0.5× D-T)",
        "C220500": "Fuel Handling (D-D)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    for code, label in pw_labels.items():
        val = cas22[code]
        if val > 0.01:
            print(f"    {code} {label:<38s} ${val:>8.1f}M")
    print(f"  {'─' * 58}")
    print(f"    Plant-wide subtotal:                              ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                                        ${cas22['CAS22']:>8.1f}M")

    # --- Capital Costs (CAS10-60) ---
    print(f"\n--- Capital Costs (CAS10-60) ---")
    print(f"  CAS10  Pre-construction:              ${costs['CAS10']:>8.1f}M")
    print(f"  CAS21  Buildings ({costs['CAS21_total_per_kw']:.0f} $/kWe):       ${costs['CAS21']:>8.1f}M")
    print(f"  CAS22  Reactor Plant Equipment:       ${costs['CAS22']:>8.1f}M")
    print(f"  CAS23  Turbine Plant:                 ${costs['CAS23']:>8.1f}M")
    print(f"  CAS24  Electric Plant:                ${costs['CAS24']:>8.1f}M")
    print(f"  CAS25  Misc Plant:                    ${costs['CAS25']:>8.1f}M")
    print(f"  CAS26  Heat Rejection:                ${costs['CAS26']:>8.1f}M")
    print(f"  CAS27  Special Materials:             ${costs['CAS27']:>8.1f}M")
    print(f"  CAS28  Digital Twin:                  ${costs['CAS28']:>8.1f}M")
    print(f"  CAS29  Contingency:                   ${costs['CAS29']:>8.1f}M")
    print(f"  {'─' * 52}")
    print(f"  CAS20  Direct Costs:                  ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30  Indirect Costs:                ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40  Owner's Costs:                 ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50  Supplementary:                 ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 52}")
    print(f"  Overnight Capital:                    ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60  IDC (f={costs['f_IDC']:.3f}):               ${costs['CAS60']:>8.1f}M")
    print(f"  {'═' * 52}")
    print(f"  Total Capital:                        ${costs['total_capital']:>8.1f}M")
    if math.isfinite(costs['specific_capital_USD_per_kWe']):
        print(f"  Specific Capital:                     ${costs['specific_capital_USD_per_kWe']:>8.0f} $/kWe")
    else:
        print(f"  Specific Capital:                         UNDEFINED (net power ≤ 0)")

    # --- Annual Costs (CAS70-90) ---
    print(f"\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90  Capital charge (CRF={econ['CRF']:.4f}):   ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71  O&M (levelized):               ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72  Transducer replacement:        ${econ['CAS72']:>8.1f}M/yr  "
          f"({econ['n_transducer_replacements']} repl. over {p.plant_lifetime_years:.0f}yr)")
    print(f"  CAS70  Total O&M:                     ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80  D₂O replenishment:             ${econ['CAS80']:>8.1f}M/yr  "
          f"({econ['CAS80_d2o_m3_per_yr']:.1f} m³/yr)")

    # --- LCOE ---
    lcoe = econ["lcoe_cents_per_kWh"]
    print(f"\n--- LCOE ---")
    print(f"  Annual energy production:     {econ['annual_energy_MWh']:,.0f} MWh/yr")
    print(f"  Annual revenue requirement:   ${econ['annual_revenue_req']:.1f}M/yr")
    if not math.isfinite(lcoe) or power["p_net"] <= 0:
        print(f"  ╔══════════════════════════════════════════╗")
        print(f"  ║  LCOE = UNDEFINED (net power ≤ 0)        ║")
        print(f"  ║  Q = {p.fusion_gain_Q:.1f} insufficient — need Q ≥ ~3.5   ║")
        print(f"  ╚══════════════════════════════════════════╝")
    else:
        print(f"  ╔══════════════════════════════════════════╗")
        print(f"  ║  LCOE = {lcoe:6.2f} ¢/kWh                  ║")
        print(f"  ║       = {econ['lcoe_USD_per_MWh']:7.1f} $/MWh                  ║")
        print(f"  ╚══════════════════════════════════════════╝")
        print(f"  Capital (CAS90):    {econ.get('capital_fraction', 0):.1%}")
        print(f"  O&M (CAS70):        {econ.get('om_fraction', 0):.1%}")
        print(f"  Fuel/D₂O (CAS80):   {econ.get('fuel_fraction', 0):.1%}")


def sensitivity_sweep(base_p: SonofusionPlantParams,
                      param_name: str,
                      values: list,
                      label: str = "") -> list:
    """Sweep a single parameter and return LCOE + net power for each value."""
    results_list = []
    base_dict = dc.asdict(base_p)
    for val in values:
        kw = {**base_dict, param_name: val}
        p_new = SonofusionPlantParams(**kw)
        r = p_new.compute()
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
    # =========================================================================
    # SECTION 0: Q BREAKEVEN SCAN
    # =========================================================================
    print("\n" + "#" * 70)
    print("# Q BREAKEVEN SCAN — minimum Q for net positive electricity")
    print("#" * 70)
    print("\n  Scanning Q from 1 to 30 (baseline parameters, n_mod=4)...")
    print(f"\n  {'Q':>6}  {'Net MWe (plant)':>18}  {'Status / LCOE'}")
    print(f"  {'─'*6}  {'─'*18}  {'─'*28}")
    for q_val in [1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]:
        p = SonofusionPlantParams(fusion_gain_Q=q_val)
        r = p.compute()
        net = r["net_electric_MW"]
        if net <= 0:
            status = f"NET NEGATIVE  ({net:.0f} MWe)"
        else:
            status = f"{r['lcoe_cents_per_kWh']:.1f} ¢/kWh"
        print(f"  {q_val:>6.1f}  {net:>18.0f}  {status}")

    # =========================================================================
    # SECTION 1: BASELINE SCENARIO
    # =========================================================================
    print("\n" + "#" * 70)
    print("# BASELINE SCENARIO: Moderate Q=10, standard parameters")
    print("#" * 70)
    baseline = SonofusionPlantParams()
    baseline_results = baseline.compute()
    print_results(baseline, baseline_results)

    # =========================================================================
    # SECTION 2: SINGLE-PARAMETER SENSITIVITY SWEEPS
    # =========================================================================
    print("\n" + "=" * 70)
    print("SENSITIVITY SWEEPS — most impactful parameters (baseline Q=10)")
    print("=" * 70)

    base_lcoe = baseline_results["lcoe_cents_per_kWh"]
    print(f"  Baseline LCOE: {base_lcoe:.2f} ¢/kWh\n")

    sweeps = [
        ("fusion_gain_Q",
         [3.5, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0, 50.0],
         "Fusion gain Q  [*** BLOCKING UNCERTAINTY ***]"),

        ("acoustic_power_MW",
         [1.0, 10.0, 25.0, 50.0, 100.0, 200.0, 500.0, 1000.0],
         "Acoustic driver power per module [MW]  [*** SPECULATIVE — 3 OOM above demonstrated ***]"),

        ("transducer_cost_per_kW",
         [100.0, 200.0, 500.0, 1000.0, 2000.0],
         "Transducer capital cost [$/kW acoustic]"),

        ("thermal_efficiency",
         [0.28, 0.32, 0.35, 0.38, 0.42, 0.45],
         "Thermal efficiency [fraction]"),

        ("plant_availability",
         [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90],
         "Plant availability [fraction]"),

        ("vessel_inner_radius_m",
         [1.5, 2.0, 3.0, 4.0, 5.0],
         "Vessel inner radius [m] (affects D₂O capital cost)"),

        ("interest_rate",
         [0.05, 0.07, 0.08, 0.10, 0.12, 0.15],
         "Interest rate / WACC [fraction]"),

        ("acoustic_driver_efficiency",
         [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85],
         "Acoustic driver efficiency [fraction]  [baseline=0.85 unsupported; Kp≥0.55 only measured]"),
    ]

    for param_name, values, label in sweeps:
        print(f"  {label}:")
        for item in sensitivity_sweep(baseline, param_name, values):
            val = item["param_value"]
            net = item["net_electric_MW"]
            lcoe = item["lcoe_cents_kWh"]
            is_baseline = abs(val - getattr(baseline, param_name)) < 1e-9
            marker = " <<< baseline" if is_baseline else ""
            if net <= 0:
                print(f"    {val:>10.3g}  →  NET NEGATIVE ({net:.0f} MWe){marker}")
            else:
                print(f"    {val:>10.3g}  →  {lcoe:7.2f} ¢/kWh   ({net:.0f} MWe net){marker}")
        print()

    # =========================================================================
    # SECTION 3: SCENARIO COMPARISON TABLE
    # =========================================================================
    print("=" * 70)
    print("SCENARIO COMPARISON (conditional on physics viability)")
    print("=" * 70)

    scenarios = {
        "Conservative (Q=5, FOAK)": SonofusionPlantParams(
            fusion_gain_Q=5.0,
            transducer_cost_per_kW=1000.0,
            thermal_efficiency=0.32,
            plant_availability=0.65,
            interest_rate=0.12,
            n_mod=4,
            noak=False,
            om_cost_per_MW_yr=100.0,
        ),
        "Moderate/Baseline (Q=10)": SonofusionPlantParams(),
        "Optimistic (Q=25, NOAK)": SonofusionPlantParams(
            fusion_gain_Q=25.0,
            transducer_cost_per_kW=200.0,
            thermal_efficiency=0.40,
            plant_availability=0.85,
            interest_rate=0.07,
            n_mod=4,
            acoustic_power_MW=100.0,
            om_cost_per_MW_yr=55.0,
            construction_time_years=5.0,
        ),
    }

    # Baseline for parameter-diff display
    _base = SonofusionPlantParams()
    _base_dict = dc.asdict(_base)

    print(f"\n  All scenarios: n_mod=4, acoustic_power_MW=100 (same as Q breakeven scan).")
    print(f"  Parameters differing from baseline are listed under each scenario.\n")
    print(f"{'Scenario':<28} {'Q':>5} {'η_drv':>6} {'Net MWe':>9} {'Cap $M':>9} "
          f"{'$/kWe':>8} {'LCOE':>12}")
    print("-" * 82)
    for name, scen_params in scenarios.items():
        r = scen_params.compute()
        net = r["net_electric_MW"]
        cap = r["total_capital_M_USD"]
        if net <= 0:
            lcoe_str = "N/A (neg)"
            spcc_str = "N/A"
        else:
            lcoe_str = f"{r['lcoe_cents_per_kWh']:.2f} ¢/kWh"
            spcc_str = f"{r['costs']['specific_capital_USD_per_kWe']:,.0f}"
        eta = scen_params.acoustic_driver_efficiency
        print(f"{name:<28} {scen_params.fusion_gain_Q:>5.0f} {eta:>6.2f} {net:>9.0f} "
              f"{cap:>9.0f} {spcc_str:>8} {lcoe_str:>12}")
        # Show all parameters that differ from baseline
        scen_dict = dc.asdict(scen_params)
        diffs = [(k, _base_dict[k], v) for k, v in scen_dict.items()
                 if v != _base_dict[k]]
        if diffs:
            diff_strs = [f"{k}={v} (base:{bv})" for k, bv, v in diffs]
            print(f"  {'  '.join(diff_strs)}")

    print()
    print("  NOTE: All scenarios are conditional on D-D fusion from acoustic")
    print("  cavitation being achievable — currently undemonstrated by 4 orders")
    print("  of magnitude in temperature.")

    # =========================================================================
    # SECTION 4: ELASTICITY SUMMARY
    # =========================================================================
    print(f"\n{'=' * 70}")
    print("LCOE ELASTICITIES (central difference, dp=1%)")
    print(f"{'=' * 70}")
    sens = compute_sensitivity()
    eng = sens["engineering"]
    fin = sens["financial"]

    # Sort by absolute elasticity, descending
    all_elast = {**eng, **fin}
    sorted_params = sorted(all_elast.items(), key=lambda x: abs(x[1]), reverse=True)
    print(f"\n  {'Parameter':<35} {'Elasticity':>10}  (type)")
    print(f"  {'─'*35}  {'─'*10}  {'─'*12}")
    for pname, elast in sorted_params[:12]:
        ptype = "financial" if pname in fin else "engineering"
        print(f"  {pname:<35} {elast:>+10.3f}  ({ptype})")

    # =========================================================================
    # SECTION 5: KEY BINDING CONSTRAINTS
    # =========================================================================
    print(f"\n{'═' * 70}")
    print("KEY BINDING CONSTRAINTS — top 3 LCOE drivers")
    print(f"{'═' * 70}")
    print()
    print("  1. FUSION GAIN Q: THE SINGLE BLOCKING SCIENTIFIC CONSTRAINT")
    print("     Q is the product of an undemonstrated physics mechanism.")
    print("     Demonstrated sonoluminescence: ~16,000 K (Flannigan & Suslick 2010).")
    print("     Required for D-D thermonuclear fusion: ~10⁸ K.")
    print("     Temperature gap: ~4 orders of magnitude — no published mechanism bridges it.")
    print("     Net-positive operation (baseline params) requires Q ≥ ~3.5.")
    print("     LCOE leverage: Q=5 → ~35–50 ¢/kWh; Q=10 → ~12–15 ¢/kWh;")
    print("     Q=25 → ~3–5 ¢/kWh (all conditional on physics being achievable).")
    print("     STATUS: Not demonstrated. Taleyarkhan (2002) claims discredited (2008).")
    print()
    d2o_fill = params.d2o_unit_cost_per_m3 * (4/3)*math.pi*params.vessel_inner_radius_m**3 / 1e6
    print(f"  2. D₂O VESSEL CAPITAL COST — ${d2o_fill:.0f}M fill + ~$15M structure per module")
    print("     2023 UN Comtrade: D₂O global export prices $300–$475/kg (volume-weighted")
    print("     ~$450/kg); India+Canada supply ~80% of global exports by value.")
    print("     A 3m-radius vessel holds ~113 m³ of D₂O at 1,105 kg/m³.")
    print(f"     D₂O fill alone: ~${d2o_fill:.0f}M per module (4 modules = ~${d2o_fill*4:.0f}M).")
    print("     This is unavoidable — D₂O IS the fusion medium.")
    print("     Higher Q → more fusion power per vessel → lower $/kWe → lower LCOE.")
    print("     Potential mitigation: deuterated acetone (cheaper per kg) but no")
    print("     industrial supply and radiation compatibility unknown.")
    print()
    print("  3. RECIRCULATING POWER / Q THRESHOLD — SENSITIVE TO η_DRIVER")
    print("     The acoustic driver draws full electrical power continuously.")
    print("     Breakeven requires: Q_sci × η_driver × η_thermal > 1 + aux_fraction.")
    print("     At η_driver=0.85, η_th=0.35: Q_sci × 0.298 > 1 → Q_sci > 3.36 (baseline).")
    print("     At η_driver=0.65, η_th=0.35: Q_sci × 0.228 > 1 → Q_sci > 4.39.")
    print("     At η_driver=0.55, η_th=0.35: Q_sci × 0.193 > 1 → Q_sci > 5.19.")
    print("     The η_driver=0.85 assumption (unsupported — only Kp≥0.55 measured) raises")
    print("     the Q breakeven threshold by ~50% if the true efficiency is closer to 0.55.")
    print("     LCOE elasticity: |ε(η_driver)| ≈ 0.52 — nearly equal to |ε(Q)| ≈ 0.53.")
    print("     Both Q and η_driver are speculative; see driver efficiency sweep above.")
    print("     Ref: APC International 90-4040 (Kp≥0.55); analysis.md §Section 3.")
    print()
    print("  NOTE: This model makes dozens of speculative assumptions about a concept")
    print("  that has not demonstrated fusion. All LCOE values should be treated as")
    print("  'LCOE IF physics works at stated Q' — existence proofs, not forecasts.")
    print("  See analysis.md §Section 2 for 5 blocking uncertainties and §Section 6")
    print("  for the full data gap inventory (15 items, 9 blocking).")
    print()
    print("NOTE: Parameters marked HIGH UNCERTAINTY or ASSUMED carry significant risk.")
    print("CAS accounts follow 1costingfe CAS10-LCOE structure with D-D fuel parameters.")
    print("Overrides documented inline. See parameter docstrings for full citations.")


if __name__ == "__main__":
    main()
