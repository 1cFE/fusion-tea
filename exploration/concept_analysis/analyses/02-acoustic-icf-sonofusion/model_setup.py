# STALE: analysis-updated-iter-2
"""
Acoustic ICF / Sonofusion (D-D) — First-Pass LCOE Model
========================================================
1cFE First Pass Concept Analysis
Concept: Acoustic ICF / Sonofusion (D-D)
Company: Sonofusion Energy (UCLA spin-off, Putterman/Camara)

CRITICAL CAVEAT: This model is purely speculative corridor mapping. Sonofusion
has not demonstrated fusion from acoustic cavitation in any credible, replicated
experiment. The ~4 orders-of-magnitude temperature gap between demonstrated
sonoluminescence (~16,000 K) and D-D fusion threshold (~10^8 K) remains unbridged.
All parameters involving fusion gain Q are entirely hypothetical. This model
answers "what would LCOE be IF Q could be achieved" — it is NOT a projection.

Architecture: Spherical D₂O vessel(s) driven by piezoelectric ultrasonic transducers
at ~30 kHz. The heavy-water medium serves as both the fusion medium and the
thermal blanket. Energy conversion via Rankine steam cycle on the D₂O coolant.
D-D fuel: no external tritium supply needed; tritium produced as a byproduct.

Cost accounting follows CAS10-LCOE structure from 1costingfe, with overrides for
sonofusion-specific subsystems (transducer array, D₂O vessel, D₂O circulation).
Scaling laws from 1costingfe costing_constants.yaml used where applicable.

Key references:
- ucla-putterman-group-sonoluminescence.md — demonstrated sonoluminescence physics
- bubble-fusion-scientific-history.md — Taleyarkhan controversy, temperature gap
- sonofusion-energy-website.md — company claims (no technical specs disclosed)
- Flannigan & Suslick 2010, Nature Physics 6, 598-601 — temperature upper bound
- 1costingfe costing_constants.yaml — CAS scaling laws (D-D fuel parameters used)
- SAND2006-7148 — Z-IFE study (geometry and IFE chamber analogy)
- analysis.md — concept analysis with parameter availability assessment

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass, field
from typing import Optional

# === Reference power levels for CAS scaling laws (from 1costingfe) ===
P_TH_REF = 2500.0   # Reference thermal power [MW]
P_ET_REF = 1100.0   # Reference gross electric power [MW]


@dataclass
class SonofusionPlantParams:
    """
    Parameterized Acoustic ICF / Sonofusion power plant model.

    All parameters have source annotations. Uncertainty tags:
      (no tag)               = well-established value with published source
      MODERATE UNCERTAINTY   = reasonable estimate from analogues
      HIGH UNCERTAINTY       = speculative or poorly constrained
      ASSUMED                = no source; engineering judgement only
      BLOCKING UNCERTAINTY   = foundational unknown — concept not viable without resolving this
    """

    # =========================================================================
    # ACOUSTIC DRIVER
    # =========================================================================

    acoustic_power_MW: float = 100.0
    """Electrical power drawn by acoustic transducer array per module [MW].
    This is the driver input power equivalent (analogous to pulsed-power stored energy
    divided by rep-rate in MagLIF). For a continuous-wave acoustic system, this is the
    steady-state electrical draw.
    Source: No published estimate for a reactor-scale system. Industrial ultrasonic
    cleaning at MW scale exists (e.g., Crest Ultrasonics large-tank systems, ~kW to
    100 kW range). Scaling to 100 MW is an order-of-magnitude extrapolation.
    Ref: Industry analogy from ultrasonic cleaning systems. HIGH UNCERTAINTY."""

    acoustic_driver_efficiency: float = 0.85
    """Fraction of electrical input converted to acoustic power by PZT transducers.
    PZT transducers at their resonant frequency achieve 85-95% electromechanical
    conversion efficiency in industrial applications (IEEE Std 177).
    High efficiency because resonant operation minimizes losses.
    Source: Industrial ultrasonic transducer specifications; standard PZT physics.
    Ref: IEEE Standard 177; vendor datasheets for industrial ultrasonics.
    NOTE: Neutron irradiation effects on PZT conversion efficiency in a fusion
    environment are unstudied. This value may degrade with activation.
    MODERATE UNCERTAINTY (irradiation effects unknown)."""

    fusion_gain_Q: float = 10.0
    """Engineering fusion gain Q = fusion thermal power / acoustic input power [dimensionless].
    Q > 1 required for positive energy balance; Q >> 5 required for commercial LCOE.
    BLOCKING UNCERTAINTY — no fusion from acoustic cavitation has been demonstrated.
    The demonstrated temperature gap (~4 orders of magnitude, Flannigan & Suslick 2010)
    means Q is undefined experimentally; no theoretical mechanism bridges the gap.
    This parameter is the single most critical unknown in the model.
    Ref: analysis.md §Section 2 Challenge 1; bubble-fusion-scientific-history.md.
    HIGH UNCERTAINTY — entirely speculative. Baseline value 10 chosen for illustration."""

    transducer_cost_per_kW: float = 500.0
    """Capital cost of piezoelectric transducer array per kW of acoustic power output [$/kW].
    Industrial ultrasonic systems: $100-500/kW for large cleaning tanks at kW-scale.
    Medical ultrasound imaging transducers: $1,000-10,000/kW (much smaller scale).
    Reactor-scale requires: materials compatibility with neutron-irradiated D₂O,
    long-lifetime qualification, geometrical arrangement around a 3m sphere.
    Source: Industry analogy; no reactor-scale cost estimate exists.
    Ref: Industrial ultrasonic vendor pricing (Crest, Branson, Hielscher); analogy only.
    MODERATE UNCERTAINTY — reactor qualification likely increases cost 2-5×."""

    acoustic_freq_kHz: float = 30.0
    """Acoustic driving frequency [kHz] — contextual parameter, not directly in LCOE.
    Source: UCLA Putterman group operates at 40 kHz (single-bubble); this is the only
    frequency explicitly supported by reviewed sources. The 20 kHz lower bound reflects
    the general industrial ultrasonic range — not directly from reviewed sources.
    The 30 kHz midpoint used here is an interpolation; only 40 kHz (UCLA single-bubble)
    is directly cited.
    Ref: ucla-putterman-group-sonoluminescence.md §Key Technical Facts.
    MODERATE UNCERTAINTY — multi-bubble range is inferred from industrial practice."""

    # =========================================================================
    # FUSION PHYSICS & ENERGY CONVERSION
    # =========================================================================

    blanket_energy_multiplication: float = 1.05
    """D-D blanket energy multiplication factor [dimensionless].
    D-D produces no 14.1 MeV neutrons (unlike D-T); 2.45 MeV neutrons thermalize
    in D₂O with minimal additional reactions. Li-6 breeding is not needed.
    Slight multiplication (1.05) from neutron moderation energy deposition in D₂O.
    Source: 1costingfe costing_constants.yaml (D-D: blanket_unit_cost_dd, no breeding).
    Ref: Standard nuclear data for D-D reactions in heavy water."""

    f_neutron_dd: float = 0.336
    """Fraction of D-D fusion energy carried by neutrons [dimensionless].
    D-D reaction channels (equal probability):
      Branch 1 (50%): D+D → T(1.01 MeV) + p(3.02 MeV), total 4.03 MeV
      Branch 2 (50%): D+D → He-3(0.82 MeV) + n(2.45 MeV), total 3.27 MeV
    Average total energy: 0.5×4.03 + 0.5×3.27 = 3.65 MeV per event
    Neutron energy fraction: (0.5×2.45) / 3.65 = 1.225/3.65 = 0.336
    Source: Standard nuclear physics; D-D cross-section tables.
    Ref: NuDat 2 / ENDF nuclear data; analysis.md §Section 2 Challenge 5."""

    thermal_efficiency: float = 0.35
    """Thermal-to-electric conversion efficiency [fraction].
    D₂O at moderate temperatures (~300°C) → conventional Rankine steam cycle.
    35% is conservative for a hot-water/steam cycle; analogous to BWR efficiency.
    Higher efficiency (40-45%) possible with superheated steam if D₂O temperature permits.
    Source: Standard power engineering; no concept-specific design exists.
    Ref: General steam cycle engineering; SAND2006-7148 Rankine cycle reference.
    MODERATE UNCERTAINTY — depends on D₂O operating temperature and pressure."""

    # =========================================================================
    # GEOMETRY (spherical vessel — analogous to IFE chamber)
    # =========================================================================

    vessel_inner_radius_m: float = 3.0
    """Inner radius of D₂O-filled fusion vessel [m].
    The vessel is a sphere filled with heavy water; the D₂O serves as the
    acoustic medium, fusion medium, and primary coolant simultaneously.
    Impulse Devices experimental reactor: ~0.15m radius (1-foot sphere, $250K).
    Commercial plant analogy: IFE chamber radius ~3m (SAND2006-7148).
    Power density assumption: ~850 MW fusion / 113 m³ ≈ 7.5 MW/m³ (at Q=10, η=0.85 baseline).
    Ref: bubble-fusion-scientific-history.md §Other Companies; SAND2006-7148.
    HIGH UNCERTAINTY — no power plant design exists; this is a scale analogy."""

    shield_thickness_m: float = 1.5
    """Biological shield thickness around vessel [m].
    D-D neutrons (2.45 MeV) are lower energy than D-T (14.1 MeV), reducing
    shielding requirements. However, D₂O is an excellent neutron moderator
    (CANDU experience), which reduces external shield needs somewhat.
    1.5m chosen to be conservative for a commercial D-D neutron field.
    Source: Analogy to D-T IFE shielding (SAND2006-7148) reduced for D-D neutron energy.
    Ref: 1costingfe shield_unit_cost with D-D scale factor; SAND2006-7148.
    MODERATE UNCERTAINTY — no D-D power plant shielding calculation exists."""

    structure_thickness_m: float = 0.3
    """Primary structural shell thickness around shield [m].
    Source: Analogy to IFE chamber structural support.
    Ref: SAND2006-7148 structural estimates; standard industrial vessel analogy."""

    vessel_wall_thickness_m: float = 0.15
    """Pressure vessel wall thickness (stainless steel sphere) [m].
    D₂O at ~10 MPa operating pressure in a 3m sphere → ~15 cm SS wall
    (hoop stress estimate: P×r/(2×σ_allow) = 10e6×3/(2×200e6) = 0.075m → 15cm with safety).
    Source: Pressure vessel engineering; stainless steel allowable stress ~200 MPa.
    Ref: ASME Boiler & Pressure Vessel Code Section III analogy. MODERATE UNCERTAINTY."""

    # =========================================================================
    # PLANT CONFIGURATION
    # =========================================================================

    n_mod: int = 4
    """Number of sonofusion modules (D₂O vessels) per plant.
    Multiple modules reduce single-point failure risk and allow staged construction.
    Source: ASSUMED — no sonofusion plant design exists.
    Ref: Analogy to modular IFE concepts (SAND2006-7148 multi-chamber studies).
    ASSUMED — no design basis for optimal module count."""

    plant_availability: float = 0.75
    """Plant capacity factor / availability [fraction].
    Acoustic transducers in industrial service achieve >99% uptime (TRL 8-9).
    Key uncertainty: neutron-induced PZT degradation in a fusion environment.
    Also: D₂O management, tritium byproduct extraction, maintenance access.
    75% chosen as conservative for a novel nuclear system.
    Source: No concept-specific estimate; industrial transducer MTBF is excellent;
    nuclear system availability typically 80-90% for mature designs.
    Ref: analysis.md §Section 6 gap #10; CANDU availability ~90% (mature D₂O system).
    MODERATE UNCERTAINTY — transducer lifetime under neutron flux is unknown."""

    plant_lifetime_years: float = 40.0
    """Plant economic lifetime [years]. Standard nuclear plant assumption."""

    noak: bool = True
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK adds 10% contingency and higher pre-construction costs.
    Ref: 1costingfe CAS29 convention (contingency_rate_foak = 0.10)."""

    # =========================================================================
    # CAS22 OVERRIDES — Sonofusion-specific subsystem costs
    # =========================================================================

    d2o_unit_cost_per_m3: float = 773_500.0
    """D₂O (heavy water) cost to fill vessel [$/ m³].
    D₂O density ≈ 1,105 kg/m³; price ~$700/kg from CANDU nuclear industry.
    $700/kg × 1,105 kg/m³ = $773,500/m³.
    Source: Commercial CANDU industry pricing for nuclear-grade D₂O.
    Ref: analysis.md §Section 5 (Available Parameters); CANDU reactor procurement data.
    MODERATE UNCERTAINTY — price varies with global D₂O supply/demand."""

    vessel_structural_cost_M_USD: float = 15.0
    """Cost of stainless steel pressure vessel structure per module [$M].
    Impulse Devices experimental 1-foot sphere: ~$250K (research grade).
    Commercial 3m radius pressure vessel: surface area ≈ 113 m², SS316L pressure vessel
    at ~$50K-150K/m² for nuclear-qualified construction → $5.6M-$17M.
    Using $15M as mid-range estimate for nuclear-qualified construction.
    Source: bubble-fusion-scientific-history.md §Other Companies (experimental reactor cost);
    industrial nuclear vessel pricing analogy.
    Ref: ASME nuclear vessel construction cost data (analogy). MODERATE UNCERTAINTY."""

    # =========================================================================
    # AUXILIARY POWER (recirculating loads, per plant)
    # =========================================================================

    p_tritium_handling_MW: float = 2.0
    """Tritium handling system power per plant [MW].
    D-D Branch 1 (~50%) produces tritium as a byproduct (proton + triton).
    Unlike D-T, no breeding blanket needed — but produced tritium requires
    separation from D₂O and containment. Lower than D-T plant (~10 MW).
    Source: 1costingfe fuel_handling_dd analogy; reduced from D-T baseline.
    Ref: 1costingfe costing_constants.yaml (p_trit_MW D-D analogy). ASSUMED."""

    p_house_MW: float = 4.0
    """Housekeeping electrical load per plant [MW].
    Source: 1costingfe ife_zpinch.yaml default. ASSUMED."""

    p_cryo_MW: float = 0.1
    """Cryoplant power per plant [MW]. Minimal — no superconducting magnets.
    Source: 1costingfe IFE/MIF default, reduced for absence of SC magnet system.
    Ref: 1costingfe costing_constants.yaml. ASSUMED."""

    p_d2o_circulation_MW: float = 3.0
    """D₂O primary coolant circulation and heat exchange pumping power per plant [MW].
    Source: CANDU reactor primary coolant pumping: ~10 MW per GWth.
    Scaled to sonofusion plant thermal power.
    Ref: CANDU design data analogy. ASSUMED: 3 MW at ~1 GWth thermal."""

    # =========================================================================
    # FINANCIAL
    # =========================================================================

    interest_rate: float = 0.10
    """Real discount rate / WACC [fraction].
    Set higher than mature nuclear (8%) to reflect technological risk of a concept
    that has not demonstrated fusion. Pre-commercial fusion projects typically face
    10-15% WACC in venture/government-backed scenarios.
    Source: Standard high-risk early-stage technology finance assumption.
    Ref: Fusion industry financing analogies. MODERATE UNCERTAINTY."""

    inflation_rate: float = 0.02
    """General inflation rate [fraction]. Ref: 1costingfe default."""

    construction_time_years: float = 6.0
    """Construction period [years]. Ref: 1costingfe reference_construction_time."""

    # =========================================================================
    # OPERATING COSTS
    # =========================================================================

    om_cost_per_MW_yr: float = 80.0
    """O&M cost per MW net electric capacity per year [$/MW/yr].
    Higher than MagLIF ($60/MW/yr) due to:
    - Novel technology with uncertain maintenance requirements
    - Neutron activation of D₂O vessel and transducer components
    - Potential transducer replacement cycles under irradiation
    - Tritium byproduct extraction and containment operations
    Source: 1costingfe CAS71 default ($60/MW/yr) increased for technology novelty.
    Ref: 1costingfe costing_constants.yaml. MODERATE UNCERTAINTY."""

    core_lifetime_FPY: float = 10.0
    """Transducer array lifetime [full-power-years] before scheduled replacement.
    D-D neutrons (2.45 MeV) cause less damage per neutron than D-T (14.1 MeV).
    Industrial PZT transducers are extremely reliable in non-irradiated service.
    Neutron irradiation effects on PZT in a fusion-relevant environment: unstudied.
    Using D-D core lifetime analogy from 1costingfe (10 FPY vs 5 FPY for D-T).
    Source: 1costingfe costing_constants.yaml (core_lifetime_dd = 10.0 FPY).
    Ref: analysis.md §Section 6 gap #13 (PZT irradiation unknown).
    MODERATE UNCERTAINTY — could be much shorter if PZT is radiation-sensitive."""

    d2o_annual_replenishment_frac: float = 0.02
    """Fraction of D₂O inventory replaced annually [fraction/year].
    Accounts for: deuterium consumption in fusion reactions, tritium extraction losses,
    D₂O radiolysis (neutron dissociation of water), and handling losses.
    CANDU reactors replenish ~1-3% of D₂O inventory annually.
    Source: CANDU reactor D₂O management analogy.
    Ref: CANDU operational data; 1costingfe startup_fuel_dd. ASSUMED."""


    def _compute_power(self) -> dict:
        """Layer 1: Power balance — acoustic driver → plasma → fusion → electricity."""
        r = {}

        # Acoustic power delivered to D₂O medium (after transducer conversion losses)
        p_acoustic = self.acoustic_power_MW * self.acoustic_driver_efficiency
        r["p_acoustic"] = p_acoustic

        # Fusion thermal power (time-averaged, from Q × acoustic input)
        # Q = P_fusion / P_acoustic (fusion power per unit acoustic power delivered)
        p_fus = p_acoustic * self.fusion_gain_Q
        r["p_fus"] = p_fus

        # D-D energy partitioning between channels
        f_charged = 1.0 - self.f_neutron_dd
        r["p_neutron"] = p_fus * self.f_neutron_dd   # 2.45 MeV neutrons (50% of D-D reactions)
        r["p_charged"] = p_fus * f_charged            # p + T charged particles (50%)

        # Thermal power in D₂O system:
        # = acoustic background heating (non-fusion acoustic energy thermalizes in D₂O)
        # + charged particle energy (stops in D₂O)
        # + neutron energy × blanket multiplication (neutrons moderate in D₂O, slight mult.)
        p_th = (p_acoustic
                + r["p_charged"]
                + r["p_neutron"] * self.blanket_energy_multiplication)
        r["p_th"] = p_th

        # Gross electric power (Rankine cycle on D₂O)
        p_et = p_th * self.thermal_efficiency
        r["p_et"] = p_et

        # Recirculating loads (per plant, continuous)
        p_aux = (self.p_tritium_handling_MW
                 + self.p_house_MW
                 + self.p_cryo_MW
                 + self.p_d2o_circulation_MW)
        r["p_aux"] = p_aux

        # Net electric = gross - full electrical driver draw - auxiliaries
        # Note: subtract acoustic_power_MW (electrical draw), not p_acoustic (acoustic output)
        p_net = p_et - self.acoustic_power_MW - p_aux
        r["p_net"] = p_net

        # Metrics
        # Q_eng < fusion_gain_Q because fusion_gain_Q is defined against acoustic power
        # (post-transducer), while Q_eng is against electrical input (pre-transducer).
        # Q_eng = efficiency × fusion_gain_Q at baseline.
        r["Q_eng"] = p_fus / self.acoustic_power_MW  # fusion / electrical driver input
        r["recirc_fraction"] = ((self.acoustic_power_MW + p_aux) / p_et
                                if p_et > 0 else float('inf'))

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Spherical geometry for D₂O vessel and surrounding structures."""
        r = {}
        ri = self.vessel_inner_radius_m

        def sphere_shell_vol(r_in: float, thickness: float) -> float:
            r_out = r_in + thickness
            return (4.0 / 3.0) * math.pi * (r_out**3 - r_in**3)

        # Inner D₂O volume (sphere) — the fusion medium and primary coolant
        r["d2o_vol_m3"] = (4.0 / 3.0) * math.pi * ri**3

        # Vessel wall (stainless steel pressure sphere)
        r["vessel_wall_vol_m3"] = sphere_shell_vol(ri, self.vessel_wall_thickness_m)
        r_vessel_out = ri + self.vessel_wall_thickness_m

        # Biological shield (concentric sphere shell)
        r["shield_vol_m3"] = sphere_shell_vol(r_vessel_out, self.shield_thickness_m)
        r_shield_out = r_vessel_out + self.shield_thickness_m

        # Primary structure (outer frame / support shell)
        r["structure_vol_m3"] = sphere_shell_vol(r_shield_out, self.structure_thickness_m)
        r["total_outer_radius_m"] = r_shield_out + self.structure_thickness_m

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts.
        Per-module accounts (C220101-C220112) use sonofusion-specific overrides.
        Plant-wide accounts (C220200-C220700) use 1costingfe power-scaling laws."""
        r = {}
        p_th = max(power["p_th"], 1.0)
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)

        # --- Per-module accounts ---

        # C220101: D₂O vessel + liquid — OVERRIDE
        # The heavy water IS the blanket medium (no separate D-T breeding blanket).
        # Cost = D₂O fill + pressure vessel structure.
        # 1costingfe scaling law (volume × unit_cost × power^0.6) replaced by direct cost
        # because the D₂O cost dominates and scales with vessel volume, not power density.
        d2o_fill_cost_M = (self.d2o_unit_cost_per_m3 * geom["d2o_vol_m3"]) / 1e6
        r["C220101"] = d2o_fill_cost_M + self.vessel_structural_cost_M_USD

        # C220102: Shield (biological, gamma + 2.45 MeV neutron)
        # D-D scale factor 0.65 vs D-T (lower neutron energy, less shielding depth needed).
        # Adopts 1costingfe scaling: unit_cost × volume × (p_th/P_TH_REF)^0.6
        # shield_unit_cost_dt = 0.74 M$/m³ from 1costingfe; D-D = 0.74 × 0.65 = 0.481
        shield_unit_cost_dd = 0.74 * 0.65   # M$/m³; DEFAULT from 1costingfe × D-D factor
        r["C220102"] = (shield_unit_cost_dd
                        * geom["shield_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: Coils — NOT APPLICABLE
        # No magnetic confinement; acoustic driver requires no superconducting magnets.
        r["C220103"] = 0.0

        # C220104: Supplementary Heating — NOT APPLICABLE
        # The acoustic driver IS the heating/compression mechanism (accounted in C220107).
        r["C220104"] = 0.0

        # C220105: Primary Structure (vessel frame, supports, seismic isolation)
        # Formula from 1costingfe: 0.15 M$/m³ × structure_volume × (p_et/P_ET_REF)^0.5
        structure_unit_cost = 0.15   # M$/m³; DEFAULT from 1costingfe structure_unit_cost
        r["C220105"] = (structure_unit_cost
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: D₂O Circulation System — OVERRIDE
        # Replaces standard vacuum system (vessel is pressurized D₂O, not vacuum).
        # Primary heat exchange loop: pump D₂O to steam generators.
        # Analogy: CANDU primary coolant circuit cost ~$50M per GWth thermal.
        # ASSUMED: CANDU D₂O circuit analogy (cost/thermal power).
        d2o_circ_base_per_gwth = 50.0   # M$/GWth; ASSUMED from CANDU circuit analogy
        r["C220106"] = d2o_circ_base_per_gwth * (p_th / 1000.0)

        # C220107: Acoustic Transducer Array — OVERRIDE
        # This is the power supply + driver system equivalent for sonofusion.
        # Standard 1costingfe formula: 80.0 M$ × (p_et/1000)^0.7 (power supplies)
        # Override: transducer array cost = cost/kW × acoustic power output in kW
        p_acoustic = power["p_acoustic"]
        r["C220107"] = (self.transducer_cost_per_kW * p_acoustic * 1000.0) / 1e6  # M$

        # C220108: D₂O Fuel Management System (IFE "target factory" analogue)
        # Handles: tritium extraction, deuterium replenishment, D₂O chemistry control,
        # isotopic purity monitoring. Simpler than IFE target factory (bulk liquid vs. pellets).
        # Scale factor 0.20 applied to 1costingfe target_factory_base (244 M$ at 1 GWe).
        # ASSUMED: 0.20 scale factor for bulk liquid vs. discrete target manufacturing.
        target_factory_base = 244.0   # M$ at 1 GWe; DEFAULT from 1costingfe
        d2o_mgmt_scale = 0.20         # ASSUMED: simpler than IFE target factory
        r["C220108"] = d2o_mgmt_scale * target_factory_base * (p_et / 1000.0) ** 0.7

        # C220109: Direct Energy Converter — NOT APPLICABLE
        # D-D thermal cycle; no direct conversion (charged particle fraction too diffuse).
        r["C220109"] = 0.0

        # C220111: Installation labor (14% of reactor subtotal)
        # DEFAULT from 1costingfe installation_frac = 0.14
        installation_frac = 0.14
        reactor_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109"
        ])
        r["C220111"] = installation_frac * reactor_subtotal

        # C220112: Tritium Separation (D-D byproduct)
        # D-D Branch 1 produces tritium; must be separated from D₂O for safety.
        # Less extensive than D-T breeding infrastructure; scaled with plant size.
        # ASSUMED: $5M at 1 GWe reference, (p_net/1000)^0.7 scaling.
        r["C220112"] = 5.0 * (p_net / 1000.0) ** 0.7   # ASSUMED

        # Per-module subtotal
        r["CAS22_per_module"] = reactor_subtotal + r["C220111"] + r["C220112"]

        # --- Plant-wide accounts (all modules combined) ---
        p_net_total = p_net * self.n_mod
        p_th_total = p_th * self.n_mod

        # C220200: Main & Secondary Coolant (D₂O → steam generators → Rankine)
        C220201 = 166.0 * (p_net_total / 1000.0)              # Primary coolant; DEFAULT 1costingfe
        C220202 = 40.6 * (p_th_total / 3500.0) ** 0.55        # Intermediate; DEFAULT 1costingfe
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling + Cryoplant (minimal — no SC magnets)
        C220301 = 1.1e-3 * p_th_total                                    # Aux coolant; DEFAULT
        C220302 = 200.0 * (max(self.p_cryo_MW, 0.01) / 30.0) ** 0.7     # Cryoplant; DEFAULT
        r["C220300"] = C220301 + C220302

        # C220400: Radioactive Waste Management
        # D-D: ~0.5× D-T rate (lower neutron energy, less activation, no Li blanket waste).
        # DEFAULT 1costingfe × 0.5 D-D scale.
        r["C220400"] = 1.96 * 0.5 * (p_th_total / 1000.0)

        # C220500: Fuel Handling (D-D baseline from 1costingfe)
        # Includes: D₂O storage/inventory, small-scale tritium containment.
        # fuel_handling_dd_base = 60.0 M$ at 1 GWe from 1costingfe.
        fuel_handling_base = 60.0   # M$ at 1 GWe; DEFAULT from 1costingfe fuel_handling_dd_base
        r["C220500"] = fuel_handling_base * (p_net_total / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        r["C220600"] = 11.5 * (p_net_total / 1000.0) ** 0.8   # DEFAULT 1costingfe

        # C220700: Instrumentation & Control
        r["C220700"] = 85.0 * (p_th_total / 3500.0) ** 0.65   # DEFAULT 1costingfe

        # Plant-wide subtotal
        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"
        ])

        # Total CAS22
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
        # licensing_cost_dd = 3.0 M$ NOAK from 1costingfe costing_constants.yaml.
        site_permits = 3.0        # DEFAULT 1costingfe
        plant_studies = 4.0 if self.noak else 20.0    # DEFAULT 1costingfe
        plant_permits = 2.0       # DEFAULT 1costingfe
        plant_reports = 1.0       # DEFAULT 1costingfe
        other_precon = 1.0        # DEFAULT 1costingfe
        land_cost = 0.25 * p_net_total * math.sqrt(self.n_mod) * 10_000 / 1e6  # DEFAULT
        licensing_cost = 3.0 if not self.noak else 1.5   # D-D from 1costingfe
        r["CAS10"] = (site_permits + plant_studies + plant_permits + plant_reports
                      + other_precon + land_cost + licensing_cost)

        # CAS21: Buildings
        # D-D modifications vs D-T 1costingfe baseline:
        # - hot_cell: 0.5× (no D-T tritium processing wing; only small T separation)
        # - cryogenics: 0 (no SC magnets)
        # All other building categories: DEFAULT from 1costingfe building_costs_per_kw
        building_cost_per_kw = {
            "site_improvements":    268,
            "fusion_heat_island":   126,
            "turbine_building":      54,
            "heat_exchanger":        12,
            "power_supply_storage":  17,
            "reactor_auxiliaries":   35,
            "hot_cell":              46.7,   # 0.5× standard (D-D: small T separation only)
            "reactor_services":      25,
            "service_water":         11,
            "fuel_storage":           9.1,
            "control_room":          17,
            "onsite_ac":             21,
            "administration":        10,
            "site_services":          4,
            "cryogenics":             0,     # No SC magnet cryoplant building
            "security":               8,
            "ventilation_stack":      9.2,
            "assembly_hall":         20,
        }
        total_building_per_kw = sum(building_cost_per_kw.values())
        r["CAS21"] = total_building_per_kw * p_et_total / 1000.0   # M$
        r["CAS21_total_per_kw"] = total_building_per_kw

        # CAS22: Reactor Plant Equipment (from _compute_cas22)
        r["CAS22"] = cas22["CAS22"]

        # CAS23: Turbine Plant Equipment (steam Rankine on D₂O system)
        turbine_per_mw = 0.19764    # M$/MW; DEFAULT from 1costingfe
        r["CAS23"] = p_et_total * turbine_per_mw

        # CAS24: Electric Plant Equipment
        electric_per_mw = 0.08418   # M$/MW; DEFAULT from 1costingfe
        r["CAS24"] = p_et_total * electric_per_mw

        # CAS25: Miscellaneous Plant Equipment
        misc_per_mw = 0.05124       # M$/MW; DEFAULT from 1costingfe
        r["CAS25"] = p_et_total * misc_per_mw

        # CAS26: Heat Rejection (cooling towers)
        heat_rej_per_mw = 0.03416   # M$/MW; DEFAULT from 1costingfe
        r["CAS26"] = p_et_total * heat_rej_per_mw

        # CAS27: Special Materials — D-D baseline from 1costingfe ($2M at 1 GWe)
        # Initial D₂O fill already in C220101. This covers other special materials.
        r["CAS27"] = 2.0   # DEFAULT from 1costingfe special_materials_dd

        # CAS28: Digital Twin
        r["CAS28"] = 5.0   # DEFAULT from 1costingfe digital_twin

        # CAS29: Contingency on direct costs
        cas20_subtotal = sum(r[k] for k in [
            "CAS21", "CAS22", "CAS23", "CAS24", "CAS25", "CAS26", "CAS27", "CAS28"
        ])
        contingency_rate = 0.0 if self.noak else 0.10   # DEFAULT 1costingfe
        r["CAS29"] = contingency_rate * cas20_subtotal

        # CAS20: Total Direct Costs
        r["CAS20"] = cas20_subtotal + r["CAS29"]

        # CAS30: Indirect Costs (20% of CAS20, scaled by construction time)
        ref_construction_time = 6.0   # years; DEFAULT 1costingfe
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / ref_construction_time)

        # CAS40: Owner's Costs (D-D: $31M at 1 GWe from 1costingfe owner_cost_dd)
        owner_cost_dd = 31.0   # M$ at 1 GWe; DEFAULT from 1costingfe
        r["CAS40"] = owner_cost_dd * (p_net_total / 1000.0) ** 0.5

        # CAS50: Supplementary Costs
        cas22_to_28 = sum(r[k] for k in ["CAS22", "CAS23", "CAS24", "CAS25",
                                          "CAS26", "CAS27", "CAS28"])
        spare_parts = 0.025 * cas22_to_28                        # DEFAULT D-D rate
        shipping = 0.015 * r["CAS20"]                            # DEFAULT 1costingfe
        taxes = 0.01 * r["CAS20"]                                # DEFAULT 1costingfe
        construction_insurance = 0.015 * (r["CAS20"] + r["CAS30"])  # DEFAULT 1costingfe
        startup_fuel = 0.1 * (p_net_total / 1000.0)              # DEFAULT D-D from 1costingfe
        decom = 5.0                                               # M$ simplified
        r["CAS50"] = (spare_parts + shipping + taxes
                      + construction_insurance + startup_fuel + decom)

        # Overnight Capital
        overnight = r["CAS10"] + r["CAS20"] + r["CAS30"] + r["CAS40"] + r["CAS50"]
        r["overnight_capital"] = overnight

        # CAS60: Interest During Construction (IDC)
        # f_IDC = ((1+i)^T - 1)/(i×T) - 1
        i = self.interest_rate
        T = self.construction_time_years
        if i > 0 and T > 0:
            f_idc = ((1 + i) ** T - 1) / (i * T) - 1
        else:
            f_idc = 0.0
        r["CAS60"] = f_idc * overnight
        r["f_IDC"] = f_idc

        # Total Capital
        r["total_capital"] = overnight + r["CAS60"]

        # Specific capital
        if power["p_net"] * self.n_mod > 0:
            r["specific_capital_USD_per_kWe"] = (r["total_capital"] * 1e6
                                                  / (power["p_net"] * self.n_mod * 1e3))
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
        annual_om_base = self.om_cost_per_MW_yr * p_net_total * 1000.0 / 1e6  # M$
        g = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g) ** Tc    # first year of operation
        if abs(i - g) > 1e-10:
            pv_growing = A1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
        else:
            pv_growing = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_growing   # M$/year

        # CAS72: Scheduled Replacement (transducer array)
        # The transducer array (C220107, per module × n_mod) is the primary replaceable item.
        # D₂O replenishment handled in CAS80.
        eff_years_per_replacement = self.core_lifetime_FPY / self.plant_availability
        n_replacements = max(0, int(math.ceil(
            self.plant_lifetime_years / eff_years_per_replacement)) - 1)
        transducer_replacement_cost = cas22["C220107"] * self.n_mod  # total array cost
        pv_replacements = 0.0
        for k in range(1, n_replacements + 1):
            year = k * eff_years_per_replacement
            if year < self.plant_lifetime_years:
                pv_replacements += transducer_replacement_cost / (1 + i) ** year
        r["CAS72"] = crf * pv_replacements   # M$/year
        r["n_transducer_replacements"] = n_replacements

        r["CAS70"] = r["CAS71"] + r["CAS72"]   # Total O&M

        # CAS80: Annualized Fuel & Consumables
        # Primary fuel cost: annual D₂O replenishment (replaces per-shot fuel in MagLIF).
        # Total D₂O volume across all modules.
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
        Returns dict with all intermediate and final values.
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
            # Convenience aliases
            "net_electric_MW": power["p_net"] * self.n_mod,
            "lcoe_cents_per_kWh": econ["lcoe_cents_per_kWh"],
            "total_capital_M_USD": costs["total_capital"],
        }
        return results


# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

def print_results(params: SonofusionPlantParams, results: dict):
    """Pretty-print LCOE model results with full CAS breakdown."""
    power = results["power"]
    geom = results["geometry"]
    cas22 = results["cas22"]
    costs = results["costs"]
    econ = results["economics"]

    print("=" * 70)
    print("Acoustic ICF / Sonofusion (D-D) — 1cFE CAS-Structured LCOE Model")
    print("=" * 70)
    print("  *** SPECULATIVE MODEL — fusion from acoustic cavitation undemonstrated ***")
    print("  *** Q is a hypothetical parameter; breakeven requires Q ≥ ~3           ***")

    # --- Key Inputs ---
    print(f"\n--- Key Input Parameters ---")
    print(f"  Acoustic driver power:      {params.acoustic_power_MW:.0f} MW (elec) per module")
    print(f"  Driver efficiency (PZT):    {params.acoustic_driver_efficiency:.1%} → "
          f"{params.acoustic_power_MW * params.acoustic_driver_efficiency:.0f} MW acoustic")
    print(f"  Fusion gain Q:              {params.fusion_gain_Q:.1f}  [*** SPECULATIVE ***]")
    print(f"  Acoustic frequency:         {params.acoustic_freq_kHz:.0f} kHz")
    print(f"  Vessel inner radius:        {params.vessel_inner_radius_m:.1f} m  "
          f"(D₂O vol = {geom['d2o_vol_m3']:.0f} m³/module)")
    print(f"  Blanket mult (D-D):         {params.blanket_energy_multiplication:.2f}")
    print(f"  Thermal efficiency:         {params.thermal_efficiency:.1%} (Rankine/D₂O)")
    print(f"  Plant availability:         {params.plant_availability:.1%}")
    print(f"  Modules:                    {params.n_mod}")
    print(f"  FOAK/NOAK:                  {'NOAK' if params.noak else 'FOAK'}")
    print(f"  Interest rate:              {params.interest_rate:.1%}")
    print(f"  Plant lifetime:             {params.plant_lifetime_years:.0f} years")

    # --- Power Balance ---
    print(f"\n--- Power Balance (per module) ---")
    print(f"  Acoustic power in D₂O:      {power['p_acoustic']:.0f} MW")
    print(f"  Fusion power (Q×acoustic):  {power['p_fus']:.0f} MW")
    print(f"    D-D neutron power:        {power['p_neutron']:.0f} MW ({params.f_neutron_dd:.1%}, 2.45 MeV)")
    print(f"    D-D charged power:        {power['p_charged']:.0f} MW ({1-params.f_neutron_dd:.1%}, p+T)")
    print(f"  Thermal power in D₂O:       {power['p_th']:.0f} MW")
    print(f"  Gross electric (Rankine):   {power['p_et']:.0f} MWe")
    print(f"  Recirculating loads:")
    print(f"    Acoustic driver:          {params.acoustic_power_MW:.0f} MW (elec)")
    print(f"    Auxiliaries:              {power['p_aux']:.1f} MW "
          f"(T-handling+house+cryo+D₂O-pumps)")
    print(f"  Net electric per module:    {power['p_net']:.0f} MWe")
    print(f"  Net electric (all modules): {power['p_net'] * params.n_mod:.0f} MWe")
    print(f"  Engineering Q:              {power['Q_eng']:.1f}  (P_fus / P_elec_driver)")
    print(f"  Recirculating fraction:     {power['recirc_fraction']:.1%}")

    # --- CAS22: Reactor Plant Equipment ---
    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    print(f"  Per-module accounts:")
    cas22_labels = {
        "C220101": "D₂O Vessel + Liquid        [OVERRIDE]",
        "C220102": "Shield (biolog, D-D n)     [D-D scale]",
        "C220103": "Coils                      [N/A → $0]",
        "C220104": "Supp. Heating              [N/A → $0]",
        "C220105": "Primary Structure",
        "C220106": "D₂O Circulation System     [OVERRIDE]",
        "C220107": "Acoustic Transducer Array  [OVERRIDE]",
        "C220108": "D₂O Management System      [OVERRIDE]",
        "C220109": "Direct Energy Converter    [N/A → $0]",
        "C220111": "Installation (14%)",
        "C220112": "Tritium Separation (D-D)",
    }
    for code, label in cas22_labels.items():
        val = cas22[code]
        if val > 0.01:
            print(f"    {code} {label:<40s} ${val:>8.1f}M")
        elif val == 0.0 and "[N/A" in label:
            print(f"    {code} {label:<40s}     $0.0M")
    print(f"  {'─' * 55}")
    print(f"    Per-module subtotal:                           ${cas22['CAS22_per_module']:>8.1f}M × {params.n_mod}")

    print(f"  Plant-wide accounts:")
    pw_labels = {
        "C220200": "Coolant Systems (D₂O → steam)",
        "C220300": "Aux Cooling + Cryoplant",
        "C220400": "Rad Waste (D-D, 0.5× D-T)",
        "C220500": "Fuel Handling (D-D)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    for code, label in pw_labels.items():
        val = cas22[code]
        if val > 0.01:
            print(f"    {code} {label:<40s} ${val:>8.1f}M")
    print(f"  {'─' * 55}")
    print(f"    Plant-wide subtotal:                           ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                                     ${cas22['CAS22']:>8.1f}M")

    # --- Capital Costs (CAS10-60) ---
    print(f"\n--- Capital Costs (CAS10-60) ---")
    print(f"  CAS10  Pre-construction:             ${costs['CAS10']:>8.1f}M")
    print(f"  CAS21  Buildings ({costs['CAS21_total_per_kw']:.0f} $/kW):       ${costs['CAS21']:>8.1f}M")
    print(f"  CAS22  Reactor Plant Equipment:      ${costs['CAS22']:>8.1f}M")
    print(f"  CAS23  Turbine Plant:                ${costs['CAS23']:>8.1f}M")
    print(f"  CAS24  Electric Plant:               ${costs['CAS24']:>8.1f}M")
    print(f"  CAS25  Misc Plant:                   ${costs['CAS25']:>8.1f}M")
    print(f"  CAS26  Heat Rejection:               ${costs['CAS26']:>8.1f}M")
    print(f"  CAS27  Special Materials:            ${costs['CAS27']:>8.1f}M")
    print(f"  CAS28  Digital Twin:                 ${costs['CAS28']:>8.1f}M")
    print(f"  CAS29  Contingency:                  ${costs['CAS29']:>8.1f}M")
    print(f"  {'─' * 50}")
    print(f"  CAS20  Direct Costs:                 ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30  Indirect Costs:               ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40  Owner's Costs:                ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50  Supplementary:                ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 50}")
    print(f"  Overnight Capital:                   ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60  IDC (f={costs['f_IDC']:.3f}):              ${costs['CAS60']:>8.1f}M")
    print(f"  {'═' * 50}")
    print(f"  Total Capital:                       ${costs['total_capital']:>8.1f}M")
    print(f"  Specific Capital:                    ${costs['specific_capital_USD_per_kWe']:>8.0f} $/kWe")

    # --- Annual Costs (CAS70-90) ---
    print(f"\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90  Capital charge (CRF={econ['CRF']:.4f}):  ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71  O&M (levelized):              ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72  Transducer replacement:       ${econ['CAS72']:>8.1f}M/yr  "
          f"({econ['n_transducer_replacements']} replacements over {params.plant_lifetime_years:.0f} yr)")
    print(f"  CAS70  Total O&M:                    ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80  D₂O replenishment:            ${econ['CAS80']:>8.1f}M/yr  "
          f"({econ['CAS80_d2o_m3_per_yr']:.1f} m³/yr)")

    # --- LCOE ---
    lcoe = econ["lcoe_cents_per_kWh"]
    print(f"\n--- LCOE ---")
    print(f"  Annual energy production:    {econ['annual_energy_MWh']:,.0f} MWh/yr")
    print(f"  Annual revenue requirement:  ${econ['annual_revenue_req']:.1f}M/yr")
    if lcoe == float('inf') or power["p_net"] <= 0:
        print(f"  ╔══════════════════════════════════════════╗")
        print(f"  ║  LCOE = UNDEFINED (net power ≤ 0)         ║")
        print(f"  ║  Q = {params.fusion_gain_Q:.1f} insufficient for net positive  ║")
        print(f"  ╚══════════════════════════════════════════╝")
    else:
        print(f"  ╔══════════════════════════════════════════╗")
        print(f"  ║  LCOE = {lcoe:.2f} ¢/kWh                   ║")
        print(f"  ║       = {econ['lcoe_USD_per_MWh']:.1f} $/MWh                    ║")
        print(f"  ╚══════════════════════════════════════════╝")
        print(f"  Capital (CAS90):   {econ.get('capital_fraction', 0):.1%}")
        print(f"  O&M (CAS70):       {econ.get('om_fraction', 0):.1%}")
        print(f"  Fuel/D₂O (CAS80):  {econ.get('fuel_fraction', 0):.1%}")


def sensitivity_sweep(base_params: SonofusionPlantParams,
                      param_name: str,
                      values: list,
                      label: str = "") -> list:
    """Sweep a single parameter and return LCOE + net power for each value."""
    results_list = []
    for val in values:
        kwargs = {k: v for k, v in base_params.__dict__.items()}
        kwargs[param_name] = val
        p = SonofusionPlantParams(**kwargs)
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
    # =========================================================================
    # SECTION 0: BREAKEVEN ANALYSIS
    # =========================================================================
    print("\n" + "#" * 70)
    print("# Q BREAKEVEN SCAN — minimum Q for net positive electricity")
    print("#" * 70)
    print("\n  Scanning Q from 1 to 30 (all other params at baseline)...")
    print(f"\n  {'Q':>6}  {'Net MWe (all modules)':>22}  {'Status'}")
    print(f"  {'─'*6}  {'─'*22}  {'─'*25}")
    baseline_scan = SonofusionPlantParams()
    for q_val in [1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]:
        p = SonofusionPlantParams(fusion_gain_Q=q_val)
        r = p.compute()
        net = r["net_electric_MW"]
        if net <= 0:
            status = f"NET NEGATIVE ({net:.0f} MWe)"
        else:
            status = f"{r['lcoe_cents_per_kWh']:.1f} ¢/kWh"
        print(f"  {q_val:>6.1f}  {net:>22.0f}  {status}")

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
    print("SENSITIVITY SWEEPS — most impactful parameters")
    print("=" * 70)

    base_lcoe = baseline_results["lcoe_cents_per_kWh"]
    print(f"  Baseline LCOE: {base_lcoe:.2f} ¢/kWh\n")

    sweeps = [
        # (param_name, values, label)
        ("fusion_gain_Q",
         [3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0, 50.0],
         "Fusion gain Q [*** BLOCKING UNCERTAINTY ***]"),

        ("acoustic_power_MW",
         [25.0, 50.0, 100.0, 200.0, 500.0],
         "Acoustic driver power per module [MW]"),

        ("transducer_cost_per_kW",
         [100.0, 200.0, 500.0, 1000.0, 2000.0],
         "Transducer cost [$/kW acoustic]"),

        ("thermal_efficiency",
         [0.28, 0.32, 0.35, 0.38, 0.42, 0.45],
         "Thermal efficiency [fraction]"),

        ("plant_availability",
         [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90],
         "Plant availability [fraction]"),

        ("n_mod",
         [1, 2, 4, 8, 16],
         "Number of modules"),

        ("interest_rate",
         [0.05, 0.07, 0.08, 0.10, 0.12, 0.15],
         "Interest rate / WACC [fraction]"),
    ]

    for param_name, values, label in sweeps:
        print(f"  {label}:")
        for item in sensitivity_sweep(baseline, param_name, values):
            val = item["param_value"]
            net = item["net_electric_MW"]
            lcoe = item["lcoe_cents_kWh"]
            marker = " <<< baseline" if abs(val - getattr(baseline, param_name)) < 1e-9 else ""
            if net <= 0:
                print(f"    {val:>10.3g}  →  NET NEGATIVE ({net:.0f} MWe)")
            else:
                print(f"    {val:>10.3g}  →  {lcoe:7.2f} ¢/kWh   ({net:.0f} MWe net){marker}")
        print()

    # =========================================================================
    # SECTION 3: SCENARIO COMPARISON TABLE
    # =========================================================================
    print("=" * 70)
    print("SCENARIO COMPARISON")
    print("=" * 70)

    scenarios = {
        "Conservative (Q=5)": SonofusionPlantParams(
            fusion_gain_Q=5.0,
            transducer_cost_per_kW=1000.0,
            thermal_efficiency=0.32,
            plant_availability=0.65,
            interest_rate=0.12,
            n_mod=4,
            noak=False,   # FOAK for conservative
        ),
        "Moderate / Baseline (Q=10)": SonofusionPlantParams(),  # all defaults
        "Optimistic (Q=25)": SonofusionPlantParams(
            fusion_gain_Q=25.0,
            transducer_cost_per_kW=200.0,
            thermal_efficiency=0.40,
            plant_availability=0.85,
            interest_rate=0.07,
            n_mod=8,
            acoustic_power_MW=100.0,
            om_cost_per_MW_yr=60.0,
            construction_time_years=5.0,
        ),
    }

    print(f"\n{'Scenario':<28} {'Q':>5} {'Net MWe':>9} {'Capital $M':>11} "
          f"{'$/kWe':>8} {'LCOE':>12}")
    print("-" * 77)
    for name, params in scenarios.items():
        r = params.compute()
        net = r["net_electric_MW"]
        cap = r["total_capital_M_USD"]
        if net <= 0:
            lcoe_str = "N/A (neg)"
            spcc_str = "N/A"
        else:
            lcoe_str = f"{r['lcoe_cents_per_kWh']:.2f} ¢/kWh"
            spcc_str = f"{r['costs']['specific_capital_USD_per_kWe']:,.0f}"
        print(f"{name:<28} {params.fusion_gain_Q:>5.0f} {net:>9.0f} {cap:>11.0f} "
              f"{spcc_str:>8} {lcoe_str:>12}")

    # =========================================================================
    # SECTION 4: KEY BINDING CONSTRAINTS
    # =========================================================================
    print(f"\n{'═' * 70}")
    print("KEY BINDING CONSTRAINTS — top 3 LCOE drivers")
    print(f"{'═' * 70}")
    print()
    print("  1. FUSION GAIN Q: THE SINGLE BLOCKING CONSTRAINT")
    print("     Q is the product of an undemonstrated physics mechanism — there is no")
    print("     validated path from acoustic cavitation (~16,000 K) to D-D fusion")
    print("     (~10^8 K). The demonstrated temperature gap is ~4 orders of magnitude.")
    print("     Until Q > 3 is demonstrated in a credible replicated experiment,")
    print("     all downstream LCOE calculations are purely hypothetical.")
    print("     LCOE leverage: Q=5 → ~30-40 ¢/kWh; Q=10 → ~10-15 ¢/kWh;")
    print("     Q=25 → ~3-5 ¢/kWh. Net-positive operation requires Q ≥ ~3.")
    print("     STATUS: Not demonstrated. Taleyarkhan (2002) claims discredited.")
    print()
    print("  2. CAPITAL COST — D₂O VESSEL DOMINATES")
    print("     At baseline (3m radius vessel, $700K/m³ D₂O), the D₂O fill alone")
    print(f"     costs ~${(700_000 * (4/3)*3.14159*27)/1e6:.0f}M per module (${(700_000 * (4/3)*3.14159*27)/1e6*4:.0f}M for 4 modules).")
    print("     This is unavoidable for the concept: the D₂O IS the fusion medium.")
    print("     Higher Q → more power per vessel → lower $/kWe → lower LCOE.")
    print("     The D₂O cost is a fixed capital item, so plant availability and")
    print("     capacity factor strongly leverage the amortization.")
    print("     Potential mitigation: use deuterated acetone (cheaper per kg?) but")
    print("     no industrial-scale supply chain exists; radioactivity concerns apply.")
    print()
    print("  3. RECIRCULATING POWER FRACTION (DRIVER EFFICIENCY)")
    print("     The acoustic driver draws full electrical power continuously.")
    print("     At Q=5: driver recirculates ~20-35% of gross electric.")
    print("     At Q=10: driver recirculates ~11% of gross electric (baseline).")
    print("     PZT transducer efficiency (85-95%) is already high and not a")
    print("     major lever — the binding factor is Q, not transducer efficiency.")
    print("     Transducer capital cost ($500/kW → $42.5M/module) is secondary to")
    print("     D₂O vessel cost and shield cost in the capital breakdown.")
    print()
    print("  NOTE: This model makes dozens of speculative assumptions about a concept")
    print("  that has not demonstrated fusion. All scenario LCOEs should be treated as")
    print("  existence proofs ('could be economic IF physics works') rather than")
    print("  predictions. The analysis.md §Section 2 identifies 5 blocking uncertainties.")

    print()
    print("NOTE: Parameters marked HIGH UNCERTAINTY or ASSUMED carry significant risk.")
    print("Cost accounts follow CAS10-LCOE structure from 1costingfe with D-D fuel")
    print("parameters. Overrides documented inline. See parameter docstrings for sources.")


if __name__ == "__main__":
    main()
