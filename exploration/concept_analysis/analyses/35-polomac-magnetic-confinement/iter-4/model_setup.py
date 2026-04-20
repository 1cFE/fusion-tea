"""
PoloMac Magnetic Confinement (Deutelio) — Free-Form LCOE Model
==============================================================
1cFE Concept Analysis — Scenario Bounds Model
Concept: PoloMac Poloidal Dipole Magnetic Confinement with D-D Fuel
Company: Deutelio AG

This is a scenario-bounds LCOE model, NOT an engineering estimate. All plasma
physics parameters (Q_sci, P_fus_MW) are scenario assumptions because no
confinement physics analysis exists for PoloMac. The model tests three
propositions identified in analysis.md §Modeling Approach Rationale:

  1. SC coil viability: If the in-vessel SC dipole coil can be bounded at
     $300–500M capital cost, and Q_sci ≥ 10–15 is achievable for D-D, then
     gross LCOE could in principle reach competitive ranges at plant scale.
  2. Blanket elimination value: D-D eliminates the tritium breeding blanket
     ($200–500M savings vs comparable D-T MFE), contingent on D-D ignition.
  3. Confinement physics and scale (Q_sci, P_fus) are the dominant LCOE levers
     in the model. SC coil viability is the economic barrier, not the top driver.

Key data constraint: The 2014 Elio FED paper (the primary technical source)
reports 700 MW resistive power for copper coils at 2 T in a 1300 m³ plasma
volume. This model assumes the superconducting coil path replaces this with
a ~10–30 MW cryogenic load — but no SC coil design has been published.

Cost accounting follows the 1costingfe CAS (Code of Accounts System) structure.
D-D fuel energy split:
  - Branch A (50%): D+D → ³He + n,  Q = 3.27 MeV (2.45 MeV neutron)
  - Branch B (50%): D+D → T + p,    Q = 4.03 MeV (charged particles only)
  → Neutron fraction: ~33.6% | Charged-particle fraction: ~66.4%

Key references:
- Elio, F. (2014) "Revisiting the poloidal magnetic confinement." Fusion Eng.
  Design, 89(7–8), pp. 1454–1458. [primary technical source]
- Elio et al. (2024) "Technical Report: The Polomac approach to fusion energy."
  JTSP. [full paper; prototype engineering specs + D-D performance predictions]
- Deutelio AG company profile (extracted 2026-04-04). [stage/roadmap]
- 1costingfe costing_constants.yaml [scaling laws and unit costs]
- analysis.md (this concept's D1+ analysis) [all assumptions documented here]

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

# === D-D fuel energy split (physics constants) ===
# Branch A (50%): D+D → ³He + n,  Q_A = 3.27 MeV
# Branch B (50%): D+D → T + p,    Q_B = 4.03 MeV
# Average energy per D-D reaction: (3.27 + 4.03) / 2 = 3.65 MeV
# Neutron fraction = 0.5 * 2.45 / 3.65 = 0.336
# Charged-particle fraction = 1 - 0.336 = 0.664
DD_NEUTRON_FRACTION = 0.336
DD_CHARGED_FRACTION = 0.664
# Also: Branch B produces tritium — if recovered and burned, adds secondary fusion
# potential. Model ignores secondary T burn (conservative, consistent with no
# tritium handling infrastructure assumed).

# === D-T fuel energy split (physics constants) ===
# D+T → ⁴He + n,  Q = 17.6 MeV (14.1 MeV neutron, 3.5 MeV alpha)
# Neutron fraction = 14.1 / 17.6 = 0.801
# Charged-particle fraction = 3.5 / 17.6 = 0.199
DT_NEUTRON_FRACTION = 0.801
DT_CHARGED_FRACTION = 0.199


@dataclass
class PoloMacPlantParams:
    """
    Parameterized PoloMac power plant LCOE model.

    WARNING: This is a scenario model. The absence of published plasma physics
    data, confinement scaling, or reactor design point means all plasma
    parameters are scenario assumptions. See analysis.md §Section 2 for the
    full blocking gaps. Results are conditions under which PoloMac COULD be
    competitive, not engineering estimates.

    All parameters have source annotations. Uncertainty tags:
      (no tag)              = value drawn from identified source
      MODERATE UNCERTAINTY  = reasonable analogue from published MFE concepts
      HIGH UNCERTAINTY      = speculative, no specific basis in available sources
      ASSUMED               = not in any source; required to close the model
    """

    # === PLASMA PHYSICS (scenario assumptions — nothing in sources) ===

    Q_sci: float = 10.0
    """Scientific energy gain: Q_sci = P_fus / P_heat (dimensionless).
    Source: Not specified in any available source. No confinement analysis exists.
    Ref: analysis.md §Section 2 (blocking gap #3).
    ASSUMED: 10.0 is chosen as a plausible target for a commercial MFE device.
    Sensitivity to Q_sci is critical — see sensitivity_sweep() in main().
    HIGH UNCERTAINTY."""

    p_fus_MW: float = 500.0
    """Fusion power [MW] per plant module.
    Source: No reactor design point exists. 1300 m³ plasma volume from the 2014
    Elio FED paper is a sub-reactor design study, not a power plant point.
    Ref: elio-2014-fed-poloidal-confinement.md §Coil support and supply.
    ASSUMED: 500 MW is consistent with a large MFE plant (commercial scale).
    The required plasma pressure at this power level in a ~3000 m³ vessel
    implies energy confinement times far beyond any demonstrated dipole
    experiment. See analysis.md §Section 3 (TRL 1).
    HIGH UNCERTAINTY."""

    # === D-D ENERGY BALANCE ===

    dd_neutron_fraction: float = DD_NEUTRON_FRACTION
    """Fraction of D-D fusion energy carried by neutrons (dimensionless).
    Source: Nuclear physics — D-D reaction kinematics.
    Branch A (50%): D+D → ³He + n, Q=3.27 MeV, 2.45 MeV in neutron.
    Branch B (50%): D+D → T + p,   Q=4.03 MeV, no fast neutron.
    f_n = 0.5 * 2.45 / ((3.27 + 4.03)/2) = 0.336.
    Note: 14x lower fast-neutron energy (2.45 MeV vs 14.1 MeV D-T). Lower
    wall loading per MW of fusion power than D-T, but still requires shielding.
    Ref: Standard nuclear physics tables."""

    blanket_energy_capture: float = 1.03
    """Effective energy multiplication from D-D blanket (dimensionless).
    For D-D, no tritium breeding reaction (no Li-6 + n exotherm).
    Blanket captures neutrons (~2.45 MeV) and thermalizes them.
    Value ~1.0 (no multiplication) + small inelastic scattering contribution.
    Ref: 1costingfe blanket_unit_cost_dd notes (DD: 'energy capture, no breeding').
    MODERATE UNCERTAINTY — no blanket design published for PoloMac."""

    thermal_efficiency: float = 0.38
    """Gross thermal-to-electric conversion efficiency (dimensionless).
    Source: No power conversion design exists for PoloMac.
    Ref: analysis.md §Section 3 (BOP TRL 2).
    ASSUMED: 0.38 is consistent with a steam Rankine cycle at fusion-relevant
    temperatures (T_exit ~500°C). Standard MFE assumption.
    Ref: 1costingfe CAS23 basis; ARIES-AT: ~0.41; STARFIRE: ~0.35.
    MODERATE UNCERTAINTY."""

    # === IN-VESSEL SC DIPOLE COIL (the central design uncertainty) ===

    sc_coil_capital_M: float = 500.0
    """Capital cost of the in-vessel superconducting dipole coil system [M$].
    Source: No SC coil design has been published. The JTSP 2024 prototype design
    uses copper (resistive) coils: 960 m copper conductor, 2500 A max current,
    750 kW ohmic losses at 0.2–0.3 T prototype field. The commercial SC path
    (replacing 700 MW copper at 2 T, Elio 2014) has no published design.
    Ref: elio-2014-fed-poloidal-confinement.md §Coil support and supply;
    analysis.md §Section 2 (blocking gap #2).
    This is the highest-leverage parameter in the model. Sensitivity range:
    $200M (optimistic, low-field REBCO coil with novel radiation hardening)
    to $1000M (conservative, large-bore HTS coil at fusion neutron fluence).
    Analogue: LDX levitated dipole coil program; ITER TF coil ~$1B total.
    For context, a large tokamak SC magnet system is $500M–$2B total.
    The PoloMac in-vessel coil must be smaller than a TF coil system but
    faces the additional challenge of radiation-hard HTS in a neutron environment.
    Maps to CAS22 C220103 override.
    HIGH UNCERTAINTY."""

    sc_coil_cryo_MW: float = 15.0
    """Cryogenic cooling load for the SC dipole coil [MW].
    Source: Not specified. Copper baseline is 700 MW (Elio 2014); SC replaces
    resistive loss with cryogenic refrigeration.
    Ref: analysis.md §Section 7 ('transition from 700 MW resistive loss to
    ~tens of MW cryogenic load is the critical engineering milestone').
    ASSUMED: 15 MW is plausible for a large-bore HTS coil. LHC cryoplant
    ~30 MW for 27 km of SC magnets. A compact HTS coil: ~5-30 MW.
    MODERATE UNCERTAINTY."""

    sc_coil_lifetime_FPY: float = 8.0
    """In-vessel SC coil lifetime [full-power years] before replacement.
    Source: No shielding design or neutron fluence estimate exists.
    Ref: analysis.md §Section 2 (blocking gap #6: 'In-vessel coil neutron
    fluence limit — truly-unknown — blocking').
    ASSUMED: 8 FPY analogued to D-D first-wall lifetime (1costingfe:
    core_lifetime_dd = 10 FPY). The in-vessel coil is more exposed than the
    first wall in a conventional tokamak; 8 FPY is conservative.
    For D-D, 2.45 MeV neutrons (vs 14.1 MeV D-T) cause less dpa per MW,
    supporting a longer interval than D-T but shorter than the ideal SC coil.
    HIGH UNCERTAINTY — sets the maintenance cost and capacity factor floor."""

    # === REACTOR GEOMETRY ===

    R_major_m: float = 7.5
    """Major radius of the plasma torus [m].
    Source: No commercial design point. 1300 m³ volume from 2014 sub-reactor study
    at R~5m scale; commercial plant would require larger volume for higher power.
    Ref: elio-2014-fed-poloidal-confinement.md §Coil support; analysis.md §S5.
    ASSUMED: R=7.5m for a 500 MW D-D plant. Yields plasma volume ~3200 m³.
    The PoloMac plasma geometry approximated as a torus around the in-vessel
    dipole coil. True shape is more complex (dipole field traps plasma in
    min-B regions), but toroidal shell is adequate for blanket/vessel costing.
    MODERATE UNCERTAINTY."""

    R_minor_m: float = 3.5
    """Minor plasma radius [m] (half-width of plasma cross-section).
    Source: Assumed. See R_major_m note.
    ASSUMED: R_minor = 3.5m with elongation 2.2 → V_p ≈ 3200 m³.
    MODERATE UNCERTAINTY."""

    elongation: float = 2.2
    """Plasma elongation (κ = height/width of plasma cross-section).
    Source: Dipole confinement naturally produces high-beta elongated plasmas.
    Historical dipole experiments: β = 20–30% (Elio 2014 §Introduction).
    High elongation consistent with high-beta dipole confinement.
    MODERATE UNCERTAINTY."""

    blanket_thickness_m: float = 0.8
    """Blanket thickness around the plasma [m].
    Source: No design. D-D does not require tritium breeding blanket.
    Ref: 1costingfe blanket_unit_cost_dd (energy capture only).
    ASSUMED: 0.8m thinner than D-T (which needs ~1m for breeding).
    Analogue: Inertial confinement thick-liquid blankets ~0.5–1m.
    MODERATE UNCERTAINTY."""

    shield_thickness_m: float = 1.2
    """Neutron shield thickness [m] (includes bioshield).
    Source: No design. Must protect in-vessel coil from neutron damage.
    This is a critical design challenge — the in-vessel coil requires
    neutron shielding that is INSIDE the plasma vessel, which creates a
    geometry problem not present in any other MFE concept.
    ASSUMED: 1.2m for the outer vessel shield. Inner-coil shielding is
    addressed by the in-vessel coil capital cost (sc_coil_capital_M).
    Slightly thicker than MagLIF (0.5m) because 2.45 MeV neutrons require
    substantial shield for the sensitive SC coil system.
    MODERATE UNCERTAINTY."""

    structure_thickness_m: float = 0.4
    """Primary structure thickness [m].
    Ref: Standard MFE plant structure.
    MODERATE UNCERTAINTY."""

    vessel_thickness_m: float = 0.15
    """Vacuum vessel wall thickness [m].
    Ref: Large MFE vacuum vessel (ITER vessel: ~0.6m double-wall with shielding).
    A simpler PoloMac vessel without ports for neutral beams from all sides may
    be simpler. Using 0.15m as structural steel shell estimate.
    MODERATE UNCERTAINTY."""

    # === HEATING SYSTEM ===

    p_heat_overhead_MW: float = 20.0
    """Additional heating power overhead beyond P_fus/Q_sci [MW].
    Source: JTSP 2024 specifies 5–10 kW ECH (electron cyclotron heating) at 4 GHz
    for the prototype. Commercial-scale heating power remains unspecified.
    Ref: analysis.md §Section 2 (blocking gap #1, partially resolved: ECH for
    prototype; commercial scale and power unspecified).
    ASSUMED: Fixed overhead for control and heating system losses. ECH (microwave)
    efficiency is typically 50–60% wall-to-plasma; this overhead captures those
    losses above the P_fus/Q_sci plasma heating term. Commercial ECH systems at
    fusion-relevant power (tens of MW) are feasible with existing gyrotron technology.
    MODERATE UNCERTAINTY."""

    heating_system_cost_M: float = 150.0
    """Capital cost of auxiliary heating system [M$]. Maps to C220104.
    Source: JTSP 2024 specifies ECH (4 GHz microwave) for the prototype at 5–10 kW.
    Commercial-scale heating design (likely ECH/gyrotron) is unspecified.
    Gyrotron-based ECH systems at fusion scale: ~$3–5M/MW of output power.
    ASSUMED: ECH/RF system at ~$3M/MW × 50 MW installed → ~$150M commercial.
    Analogue: ITER ECH ~$250M for 20 MW; DEMO ECH concepts ~$200-300M for 50 MW.
    Ref: 1costingfe power_supplies_base (80 M$ at 1 GWe), scaled here directly.
    MODERATE UNCERTAINTY."""

    # === PLANT CONFIGURATION ===

    n_mod: int = 1
    """Number of fusion modules per plant.
    Source: No multi-module design published.
    ASSUMED: Single-module plant (simplest). Dipole geometry does not lend
    itself to modular replication the way linear (mirror, FRC) concepts do.
    MODERATE UNCERTAINTY."""

    plant_availability: float = 0.70
    """Plant capacity factor [dimensionless].
    Source: No O&M data available (analysis.md §Section 3).
    ASSUMED: 0.70 is conservative relative to mature nuclear (0.90) but
    reflects the TRL-1 status of the plasma physics and the unresolved
    in-vessel coil replacement challenge. The coil replacement interval
    (sc_coil_lifetime_FPY) is the primary driver of forced outage.
    Lower bound: CF=0.50 is a plausible scenario if in-vessel coil replacement
    requires extended vessel access (weeks to months per cycle, analogous to
    major overhaul in levitated dipole designs). The sensitivity sweep shows
    CF=0.40 → ~157 ¢/kWh and CF=0.55 → ~124 ¢/kWh. CF=0.70 baseline should
    be treated as optimistic until a maintenance design exists.
    HIGH UNCERTAINTY."""

    plant_lifetime_years: float = 40.0
    """Economic plant lifetime [years].
    Ref: Standard assumption for nuclear power plants."""

    noak: bool = True
    """Nth-of-a-kind cost basis (True) vs First-of-a-kind (False).
    NOAK reduces contingency and pre-construction costs.
    Ref: 1costingfe CAS29 convention."""

    # === CAS22 COMPONENT COSTS ===

    blanket_unit_cost_dd: float = 0.30
    """D-D blanket unit cost [M$/m³] (energy capture, no breeding).
    Source: 1costingfe costing_constants.yaml: blanket_unit_cost_dd = 0.30 M$/m³.
    Applies because PoloMac targets D-D fuel, eliminating the tritium breeding
    blanket (one of the key claimed cost advantages).
    Ref: analysis.md §Section 4 ('Tritium breeding blanket — not required for D-D').
    Note: This is 0.5× the D-T rate (0.60 M$/m³), reflecting no Li/Be, no
    tritium processing infrastructure in blanket, simpler coolant chemistry."""

    shield_unit_cost: float = 0.74
    """Shield unit cost [M$/m³].
    Source: 1costingfe costing_constants.yaml: shield_unit_cost = 0.74 M$/m³."""

    structure_unit_cost: float = 0.15
    """Structure unit cost [M$/m³].
    Source: 1costingfe costing_constants.yaml: structure_unit_cost = 0.15 M$/m³."""

    vessel_unit_cost: float = 0.72
    """Vessel unit cost [M$/m³].
    Source: 1costingfe costing_constants.yaml: vessel_unit_cost = 0.72 M$/m³."""

    remote_handling_scale: float = 1.5
    """Remote handling cost scaling factor relative to D-D tokamak base [dimensionless].
    Source: 1costingfe costing_constants.yaml: remote_handling_dd_base = 100 M$
    at 1 GWe. PoloMac's in-vessel coil adds unique remote handling complexity:
    the activated SC coil must be removed/replaced in a neutron environment
    through a geometry without clear equivalent in any operating MFE concept.
    Ref: analysis.md §Section 3 ('in-vessel coil maintenance and lifetime').
    ASSUMED: 1.5× base D-D remote handling to reflect this additional complexity.
    Compare: standard D-D = 1.0×, D-T = 1.5× (more activation). PoloMac D-D
    with in-vessel coil challenge ≈ intermediate between D-D and D-T bases.
    MODERATE UNCERTAINTY."""

    # === AUXILIARY POWER ===

    p_house_MW: float = 5.0
    """Housekeeping/facility power [MW].
    Ref: 1costingfe ife_zpinch.yaml default (4 MW), scaled up for larger plant.
    MODERATE UNCERTAINTY."""

    p_vacuum_MW: float = 2.0
    """Vacuum system pumping power [MW].
    Ref: Analogue from large MFE devices. ITER vacuum pumping ~2–5 MW total.
    MODERATE UNCERTAINTY."""

    p_fuel_handling_MW: float = 1.0
    """Fuel handling and D-D gas injection power [MW].
    Source: D-D fuel is cheap and simple — no tritium processing infrastructure.
    Ref: 1costingfe: p_target_factory_MW default ~1.5 MW. D-D gas injection
    is simpler than D-T handling.
    MODERATE UNCERTAINTY."""

    # === FINANCIAL PARAMETERS ===

    interest_rate: float = 0.08
    """Real weighted average cost of capital (WACC) [dimensionless].
    Ref: 1costingfe default."""

    inflation_rate: float = 0.02
    """Inflation rate for levelized cost calculations [dimensionless].
    Ref: 1costingfe default."""

    construction_time_years: float = 7.0
    """Construction period [years].
    Source: No estimate available. PoloMac at TRL 1–2 would require extended
    R&D before construction; first commercial plant construction period likely
    longer than a mature MFE concept.
    ASSUMED: 7 years (ITER: ~20 years; DEMO targets ~12 years; optimistic
    commercial first plant ~7 years). Longer than 1costingfe default (6 years)
    given unresolved engineering challenges.
    MODERATE UNCERTAINTY."""

    # === O&M ===

    om_base_cost_M_per_yr: float = 50.0
    """Annual fixed O&M cost at reference scale [M$/yr] at 500 MW net electric.
    Source: 1costingfe costing_constants.yaml: om_cost_dd = 39 M$/yr at 1 GWe.
    Scaled: 39 × (500/1000)^0.5 ≈ 27.6 M$/yr base + uplift for in-vessel coil
    maintenance complexity → ~50 M$/yr.
    MODERATE UNCERTAINTY."""

    core_lifetime_FPY: float = 10.0
    """D-D first wall / blanket core lifetime [full-power years].
    Source: 1costingfe costing_constants.yaml: core_lifetime_dd = 10 FPY.
    D-D: 2.45 MeV neutrons, ~7 dpa/yr at typical neutron wall loading.
    The in-vessel coil replacement (sc_coil_lifetime_FPY) is modeled separately
    as it is more expensive and potentially shorter-lived than the first wall."""

    # === FUEL COSTS ===

    deuterium_cost_per_kg: float = 2175.0
    """Deuterium unit cost [$/kg].
    Source: 1costingfe costing_constants.yaml: u_deuterium = 2175 $/kg.
    Deuterium is present in natural water at ~155 ppm D/H.
    Industrial electrolysis/distillation; abundant and cheap.
    Ref: analysis.md §Section 4 ('Deuterium fuel — no supply constraint')."""

    # === D-T TRITIUM BLANKET (zero for D-D mode) ===

    dt_tritium_blanket_capital_M: float = 0.0
    """Capital cost of tritium breeding blanket system [M$]. Zero for D-D operation.
    For D-T mode: $200–400M range covers Li-6 enriched breeding blanket, tritium
    extraction, and T-handling infrastructure. Maps to CAS22 C220101 additive override.
    Ref: F-2 assessment finding; analysis.md §Section 4.
    HIGH UNCERTAINTY — no D-T design published for PoloMac."""

    # === D-D FUEL CONSUMPTION ===
    burn_fraction: float = 0.05
    """Fraction of injected deuterium burned per plasma circulation [dimensionless].
    Source: 1costingfe costing_constants.yaml: burn_fraction = 0.05.
    Standard fusion plasma recycling assumption."""

    fuel_recovery: float = 0.95
    """Fraction of unburned fuel recovered and recycled [dimensionless].
    Source: 1costingfe costing_constants.yaml: fuel_recovery = 0.95."""

    # =========================================================================
    # COMPUTE METHODS
    # =========================================================================

    def _compute_power(self) -> dict:
        """Layer 1: Power balance for D-D steady-state operation.

        D-D has two branches:
          A (50%): D+D → ³He + n,   Q_A = 3.27 MeV (33.6% of avg energy is neutrons)
          B (50%): D+D → T + p,     Q_B = 4.03 MeV (all charged particles)

        Heating power is determined by plasma Q: P_heat = P_fus / Q_sci.
        All steady-state (no rep-rate, no per-shot quantities).
        """
        r = {}

        p_fus = self.p_fus_MW
        r["p_fus"] = p_fus
        r["Q_sci"] = self.Q_sci

        # Heating power required to maintain plasma
        p_heat = p_fus / self.Q_sci
        r["p_heat"] = p_heat

        # D-D energy split
        p_neutron = p_fus * self.dd_neutron_fraction     # 2.45 MeV neutrons
        p_charged = p_fus * self.dd_charged_fraction_    # alpha/ash/proton heating
        r["p_neutron"] = p_neutron
        r["p_charged"] = p_charged

        # Thermal power: blanket captures neutrons (with modest multiplication)
        # + charged particles thermalize in vessel + heating power thermalizes
        p_th = (p_neutron * self.blanket_energy_capture
                + p_charged
                + p_heat)   # heating power becomes heat (drives plasma, which heats vessel)
        r["p_th"] = p_th

        # Gross electric
        p_et = p_th * self.thermal_efficiency
        r["p_et"] = p_et

        # Recirculating power:
        #  - Heating system wall-plug draw (assume 60% efficiency wall-to-plasma for NBI/RF)
        p_recirc_heat = p_heat / 0.60
        r["p_recirc_heat"] = p_recirc_heat
        #  - SC coil cryogenic load
        r["p_cryo"] = self.sc_coil_cryo_MW
        #  - Overhead (housekeeping, vacuum, fuel handling)
        p_aux = self.p_house_MW + self.p_vacuum_MW + self.p_fuel_handling_MW
        r["p_aux"] = p_aux
        #  - Overhead from heating system
        r["p_heat_overhead"] = self.p_heat_overhead_MW

        p_recirc_total = p_recirc_heat + self.sc_coil_cryo_MW + p_aux + self.p_heat_overhead_MW
        r["p_recirc_total"] = p_recirc_total

        # Net electric
        p_net = p_et - p_recirc_total
        r["p_net"] = p_net

        # Multi-module totals (n_mod = 1 for baseline)
        r["p_net_plant"] = p_net * self.n_mod
        r["p_et_plant"] = p_et * self.n_mod
        r["p_th_plant"] = p_th * self.n_mod

        # Figures of merit
        r["Q_eng"] = p_fus / p_recirc_total if p_recirc_total > 0 else float('inf')
        r["recirc_fraction"] = p_recirc_total / p_et if p_et > 0 else float('inf')

        # Note: 700 MW copper reference (Elio 2014) vs SC path
        r["copper_coil_MW_reference"] = 700.0   # prohibitive; SC replaces with cryo load
        r["sc_cryo_vs_copper_ratio"] = self.sc_coil_cryo_MW / 700.0

        return r

    @property
    def dd_charged_fraction_(self) -> float:
        """D-D charged particle fraction (complement of neutron fraction)."""
        return 1.0 - self.dd_neutron_fraction

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Toroidal shell geometry for the PoloMac plasma vessel.

        Approximates PoloMac geometry as an axisymmetric torus with elliptical
        cross-section. The plasma is contained by the poloidal dipole field around
        the in-vessel coil. Shell volumes are computed for blanket, shield,
        structure, and vessel.

        Key datum from sources: 1300 m³ plasma volume at R~5m scale (2014 FED
        paper, sub-reactor design). Commercial plant at 500 MW requires larger
        volume — R_major_m scaled up to ~7.5m.
        """
        r = {}

        R = self.R_major_m
        a = self.R_minor_m
        kappa = self.elongation  # elongation (height/width ratio)

        # Plasma volume: V_p = 2π² R a² κ  (torus with elliptical cross-section)
        V_plasma = 2.0 * math.pi**2 * R * a**2 * kappa
        r["V_plasma_m3"] = V_plasma

        # Shell volume helper: toroidal shell at major radius R, minor radius a to a+δ
        # V_shell ≈ 2π² R [(a + δ)² - a²] κ  (thin-shell approximation)
        # For thick shells, update a_out for next shell.

        def toroidal_shell_vol(R_maj, a_in, thickness, kap):
            a_out = a_in + thickness
            return 2.0 * math.pi**2 * R_maj * (a_out**2 - a_in**2) * kap

        a_plasma = a

        # Blanket shell
        r["blanket_vol_m3"] = toroidal_shell_vol(R, a_plasma, self.blanket_thickness_m, kappa)
        a_blanket_out = a_plasma + self.blanket_thickness_m

        # Shield shell
        r["shield_vol_m3"] = toroidal_shell_vol(R, a_blanket_out, self.shield_thickness_m, kappa)
        a_shield_out = a_blanket_out + self.shield_thickness_m

        # Structure shell
        r["structure_vol_m3"] = toroidal_shell_vol(R, a_shield_out, self.structure_thickness_m, kappa)
        a_structure_out = a_shield_out + self.structure_thickness_m

        # Vessel shell
        r["vessel_vol_m3"] = toroidal_shell_vol(R, a_structure_out, self.vessel_thickness_m, kappa)

        # Total outer minor radius (for reference)
        r["a_outer_m"] = a_structure_out + self.vessel_thickness_m

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts.

        Key overrides relative to standard 1costingfe MFE:
        - C220101: D-D blanket (no breeding, 0.30 M$/m³ vs 0.60 for D-T)
        - C220103: In-vessel SC dipole coil (direct capital cost override)
        - C220104: Heating system (direct cost override, NBI/RF analogue)
        - C220108: 0 (no target factory — steady-state MFE)
        - C220110: Enhanced remote handling (in-vessel coil complexity)
        """
        r = {}
        p_th = max(power["p_th"], 1.0)
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)

        # === Per-module reactor accounts ===

        # C220101: First Wall + Blanket (D-D energy capture, no breeding)
        # Formula: unit_cost × volume × (p_th / P_TH_REF)^0.6
        # Using blanket_unit_cost_dd = 0.30 M$/m³ (1costingfe) vs 0.60 for D-T.
        # This captures the blanket elimination advantage of the D-D fuel cycle.
        # For D-T mode: dt_tritium_blanket_capital_M adds the breeding system capital.
        r["C220101"] = (self.blanket_unit_cost_dd
                        * geom["blanket_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6
                        + self.dt_tritium_blanket_capital_M)

        # C220102: Shield (HT + LT + Bioshield)
        # Formula: 0.74 × volume × fuel_scale × (p_th / P_TH_REF)^0.6
        # Fuel scale for D-D: 0.7 (2.45 MeV neutrons less penetrating than D-T 14.1 MeV)
        # BUT in-vessel coil requires enhanced internal shielding (not captured here;
        # see sc_coil_capital_M for the coil-specific shielding cost).
        shield_fuel_scale = 0.70   # D-D: less energetic neutrons → lighter shield
        r["C220102"] = (self.shield_unit_cost
                        * geom["shield_vol_m3"]
                        * shield_fuel_scale
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: In-vessel SC dipole coil — OVERRIDE
        # This is the central novel cost item in PoloMac. The poloidal dipole field
        # is generated by a superconducting coil INSIDE the vacuum vessel, supported
        # through the plasma via "magnetic tunnels" (field-free channels in the plasma).
        # No standard scaling law applies. Direct capital cost override.
        # See sc_coil_capital_M parameter for basis and uncertainty.
        r["C220103"] = self.sc_coil_capital_M   # [override] in-vessel SC dipole coil

        # C220104: Supplementary Heating — OVERRIDE
        # ECH (4 GHz microwave) specified for prototype (JTSP 2024); commercial scale
        # unspecified. Heating power needed: P_fus / Q_sci. At Q=10, P_fus=500 MW →
        # P_heat = 50 MW. Cost: $150M baseline for ~50 MW installed ECH/gyrotron system.
        r["C220104"] = self.heating_system_cost_M   # [override] ECH/gyrotron heating system

        # C220105: Primary Structure
        # Formula: 0.15 × volume × (p_et / P_ET_REF)^0.5
        r["C220105"] = (self.structure_unit_cost
                        * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: Vacuum System (vessel + pumps)
        # Formula: 0.72 × volume × (p_et / P_ET_REF)^0.6
        # Large plasma volume → large vacuum vessel → significant cost.
        r["C220106"] = (self.vessel_unit_cost
                        * geom["vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # C220107: Power Supplies (standard scaling)
        # Formula: 80.0 × (p_et/1000)^0.7 (from 1costingfe power_supplies_base)
        r["C220107"] = 80.0 * (p_et / 1000.0) ** 0.7

        # C220108: Target Factory — NOT APPLICABLE (steady-state MFE, no targets)
        r["C220108"] = 0.0

        # C220109: Direct Energy Converter — NOT APPLICABLE (thermal cycle)
        r["C220109"] = 0.0

        # C220110: Remote Handling & Maintenance Equipment — ENHANCED for in-vessel coil
        # Base: 1costingfe remote_handling_dd_base = 100 M$ at 1 GWe.
        # Scale: (p_et / 1000)^0.7 (power-law, 1costingfe convention).
        # Enhancement factor: self.remote_handling_scale (default 1.5×) for the unique
        # challenge of replacing an activated in-vessel SC coil in a neutron environment.
        # The magnetic tunnel concept requires specialized tooling not present in any
        # operating MFE concept.
        rh_base = 100.0   # M$ D-D base (1costingfe: remote_handling_dd_base)
        r["C220110"] = (rh_base
                        * self.remote_handling_scale
                        * (p_et / 1000.0) ** 0.7)   # [enhanced] in-vessel coil RH

        # C220111: Installation labor
        # Formula: 0.14 × reactor subtotal (1costingfe: installation_frac = 0.14)
        reactor_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"])
        r["C220111"] = 0.14 * reactor_subtotal

        # C220112: Isotope Separation — 0 for D-D (no tritium enrichment needed)
        # This is a genuine cost advantage of D-D vs D-T (no Li-6 enrichment,
        # no tritium processing for breeding).
        r["C220112"] = 0.0

        # Per-module subtotal
        r["CAS22_per_module"] = reactor_subtotal + r["C220111"] + r["C220112"]

        # === Plant-wide accounts ===
        p_net_total = p_net * self.n_mod
        p_th_total = p_th * self.n_mod

        # C220200: Main & Secondary Coolant
        C220201 = 166.0 * (p_net_total / 1000.0)
        C220202 = 40.6 * (p_th_total / 3500.0) ** 0.55
        r["C220200"] = C220201 + C220202

        # C220300: Auxiliary Cooling + Cryoplant
        # Cryoplant for SC coil: scaled from 1costingfe C220302 formula.
        # Reference: 200 M$ for 30 MW cryogenic load (1costingfe cryoplant formula).
        C220301 = 1.1e-3 * p_th_total
        C220302 = 200.0 * (max(self.sc_coil_cryo_MW, 0.1) / 30.0) ** 0.7
        r["C220300"] = C220301 + C220302

        # C220400: Radioactive Waste Management
        # D-D: lower activation than D-T (2.45 MeV neutrons vs 14.1 MeV).
        # Scale by 0.5× D-T rate.
        r["C220400"] = 0.5 * 1.96 * (p_th_total / 1000.0)

        # C220500: Fuel Handling & Storage (D-D)
        # 1costingfe: fuel_handling_dd_base = 60 M$ at 1 GWe.
        # No tritium breeding or Li processing → cheaper than D-T.
        # Includes D2 gas injection, exhaust processing, isotope monitoring.
        fuel_handling_base_dd = 60.0   # M$ at 1 GWe (1costingfe fuel_handling_dd_base)
        r["C220500"] = fuel_handling_base_dd * (p_net_total / 1000.0) ** 0.7

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
        """Layer 4: CAS10-60 total capital cost structure."""
        r = {}
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)

        # === CAS10: Pre-construction (licensing, permits, studies) ===
        # D-D licensing less burdensome than D-T (no tritium): licensing_cost_dd = 3 M$
        site_permits = 3.0
        plant_studies = 4.0 if self.noak else 20.0
        plant_permits = 2.0
        plant_reports = 1.0
        other_precon = 1.0
        land_acres = 0.25 * p_net * math.sqrt(self.n_mod)
        land_cost = land_acres * 10_000 / 1e6   # M$
        licensing_cost = 3.0 if self.noak else 6.0  # D-D (1costingfe: licensing_cost_dd = 3)
        r["CAS10"] = (site_permits + plant_studies + plant_permits + plant_reports
                      + other_precon + land_cost + licensing_cost)

        # === CAS21: Buildings ===
        # $/kW gross electric (from 1costingfe building_costs_per_kw).
        # No hot cell for D-D fusion? Still needed for activated in-vessel coil.
        building_cost_per_kW = {
            "site_improvements": 268.0,
            "reactor_building": 126.0,      # fusion_heat_island
            "turbine_building": 54.0,
            "heat_exchanger": 12.0,
            "power_supply_building": 35.0,  # reactor_auxiliaries
            "hot_cell": 50.0,               # Reduced vs D-T (93.4 $/kW): less activation
            "misc_buildings": 80.0,         # Other site buildings combined
        }
        total_bldg_per_kW = sum(building_cost_per_kW.values())  # ~625 $/kW
        r["CAS21"] = total_bldg_per_kW * p_et / 1000.0  # M$

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment ===
        r["CAS23"] = 0.19764 * p_et * self.n_mod  # M$ (1costingfe: turbine_per_mw)

        # === CAS24: Electric Plant Equipment ===
        r["CAS24"] = 0.08418 * p_et * self.n_mod  # M$ (1costingfe: electric_per_mw)

        # === CAS25: Miscellaneous Plant Equipment ===
        r["CAS25"] = 0.05124 * p_et * self.n_mod  # M$ (1costingfe: misc_per_mw)

        # === CAS26: Heat Rejection ===
        r["CAS26"] = 0.03416 * p_et * self.n_mod  # M$ (1costingfe: heat_rej_per_mw)

        # === CAS27: Special Materials ===
        # D-D: no PbLi, no enriched Li-6, no beryllium → minimal special materials.
        # 1costingfe: special_materials_dd = 2 M$ at 1 GWe.
        r["CAS27"] = 2.0 * (p_net / 1000.0)  # M$ (scaled)

        # === CAS28: Digital Twin ===
        r["CAS28"] = 5.0  # M$ (1costingfe: digital_twin = 5.0)

        # === CAS29: Contingency ===
        cas20_subtotal = sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                             "CAS25", "CAS26", "CAS27", "CAS28"])
        contingency_rate = 0.0 if self.noak else 0.10
        r["CAS29"] = contingency_rate * cas20_subtotal

        # === CAS20: Total Direct Costs ===
        r["CAS20"] = cas20_subtotal + r["CAS29"]

        # === CAS30: Indirect Costs ===
        # 20% of CAS20, scaled by construction time ratio.
        ref_construction_time = 6.0   # 1costingfe: reference_construction_time
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / ref_construction_time)

        # === CAS40: Owner's Costs ===
        # 1costingfe: owner_cost_dd = 31 M$ at 1 GWe, scaled (P_net/1000)^0.5.
        owner_cost_base = 31.0  # M$ at 1 GWe
        r["CAS40"] = owner_cost_base * (p_net / 1000.0) ** 0.5

        # === CAS50: Supplementary Costs ===
        # Spare parts (D-D: spare_parts_frac_dd = 0.025 of CAS22-28)
        spare_parts_frac = 0.025
        spare_parts = spare_parts_frac * (cas20_subtotal - r["CAS21"])
        # Startup D-D fuel inventory: very cheap
        startup_fuel = 0.1 * (p_net / 1000.0)  # M$ (1costingfe: startup_fuel_dd = 0.1 at 1GWe)
        # Decommissioning provision (D-D: lower activation than D-T)
        decom = 93.0 * (p_net / 1000.0)  # M$ at scale (1costingfe: decom_provision_dd = 93)
        # PV of decom cost at commissioning: decom / (1+i)^lifetime
        decom_pv = decom / (1 + self.interest_rate) ** self.plant_lifetime_years
        shipping = 0.015 * r["CAS20"]
        taxes = 0.01 * r["CAS20"]
        insurance = 0.015 * (r["CAS20"] + r["CAS30"])
        r["CAS50"] = spare_parts + startup_fuel + decom_pv + shipping + taxes + insurance

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

        # === Total Capital (Overnight + IDC) ===
        r["total_capital"] = overnight + r["CAS60"]

        # Specific capital cost
        p_net_plant = p_net * self.n_mod
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

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]  # M$/yr

        # === CAS71: Annual O&M (levelized with inflation) ===
        g = self.inflation_rate
        Tc = self.construction_time_years
        A1 = self.om_base_cost_M_per_yr * (1 + g) ** Tc  # First-year cost
        if abs(i - g) > 1e-10:
            pv_growing_annuity = A1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
        else:
            pv_growing_annuity = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_growing_annuity  # M$/yr

        # === CAS72a: Annualized Blanket/FW Scheduled Replacement ===
        effective_years_per_fw = self.core_lifetime_FPY / self.plant_availability
        n_fw_replacements = max(0, int(math.ceil(
            self.plant_lifetime_years / effective_years_per_fw)) - 1)
        fw_replacement_cost = cas22["C220101"]
        pv_fw = 0.0
        for k in range(1, n_fw_replacements + 1):
            year = k * effective_years_per_fw
            if year < self.plant_lifetime_years:
                pv_fw += fw_replacement_cost / (1 + i) ** year
        r["CAS72a_blanket"] = crf * pv_fw  # M$/yr
        r["n_fw_replacements"] = n_fw_replacements

        # === CAS72b: Annualized SC Coil Replacement ===
        # The in-vessel SC dipole coil must be replaced periodically due to
        # neutron damage. This is the unique high-cost scheduled maintenance item.
        effective_years_per_coil = self.sc_coil_lifetime_FPY / self.plant_availability
        n_coil_replacements = max(0, int(math.ceil(
            self.plant_lifetime_years / effective_years_per_coil)) - 1)
        coil_replacement_cost = self.sc_coil_capital_M  # Replace at full capital cost
        pv_coil = 0.0
        for k in range(1, n_coil_replacements + 1):
            year = k * effective_years_per_coil
            if year < self.plant_lifetime_years:
                pv_coil += coil_replacement_cost / (1 + i) ** year
        r["CAS72b_coil"] = crf * pv_coil  # M$/yr
        r["n_coil_replacements"] = n_coil_replacements

        r["CAS72"] = r["CAS72a_blanket"] + r["CAS72b_coil"]  # M$/yr
        r["CAS70"] = r["CAS71"] + r["CAS72"]  # M$/yr

        # === CAS80: Annualized Fuel Costs (D-D) ===
        # D-D fuel: deuterium consumption rate from fusion power.
        # D-D average energy per reaction: (3.27 + 4.03)/2 MeV = 3.65 MeV
        MeV_per_reaction = 3.65  # MeV
        J_per_reaction = MeV_per_reaction * 1.602e-13  # J
        # Reactions per second at P_fus
        p_fus_W = power["p_fus"] * 1e6  # W
        reactions_per_s = p_fus_W / J_per_reaction
        # Two D atoms consumed per reaction; mass in kg using kg/mol (2.014e-3 kg/mol)
        D_atoms_consumed_per_s = 2.0 * reactions_per_s
        D_mass_consumed_per_s = D_atoms_consumed_per_s * 2.014e-3 / 6.022e23  # kg/s
        D_consumed_per_yr = D_mass_consumed_per_s * 3600 * 8760 * self.plant_availability
        # Net deuterium purchased: burned fuel + unrecovered exhaust losses.
        # Gross injection = D_consumed / burn_fraction.
        # Unrecovered losses = injection × (1-burn_fraction) × (1-fuel_recovery).
        # Total purchased = burned + losses = D_consumed × [1 + (1-f_b)(1-f_r)/f_b]
        # = D_consumed × (1 - fuel_recovery*(1-burn_fraction)) / burn_fraction
        f_b = self.burn_fraction
        f_r = self.fuel_recovery
        D_purchased_per_yr = D_consumed_per_yr * (1.0 - f_r * (1.0 - f_b)) / f_b
        annual_D_cost = D_purchased_per_yr * self.deuterium_cost_per_kg / 1e6  # M$
        r["CAS80"] = annual_D_cost  # M$/yr
        r["CAS80_deuterium_kg_yr"] = D_consumed_per_yr

        # === LCOE ===
        annual_revenue_req = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_revenue_req

        annual_energy_MWh = 8760 * p_net_total * self.plant_availability
        r["annual_energy_MWh"] = annual_energy_MWh

        if annual_energy_MWh > 0 and p_net > 0:
            lcoe_USD_MWh = annual_revenue_req * 1e6 / annual_energy_MWh
            r["lcoe_USD_per_MWh"] = lcoe_USD_MWh
            r["lcoe_cents_per_kWh"] = lcoe_USD_MWh / 10.0
        else:
            r["lcoe_USD_per_MWh"] = float('inf')
            r["lcoe_cents_per_kWh"] = float('inf')

        if annual_revenue_req > 0:
            r["capital_fraction"] = r["CAS90"] / annual_revenue_req
            r["om_fraction"] = r["CAS70"] / annual_revenue_req
            r["fuel_fraction"] = r["CAS80"] / annual_revenue_req

        return r

    def compute(self) -> dict:
        """
        Compute LCOE and all intermediate values using CAS-structured accounting.
        Returns dict with sub-dicts required by the concept explorer.

        Required output keys (from model_setup_prompt.md):
          'power': p_fus, p_th, p_et, p_net, Q_eng, Q_sci, recirc_fraction,
                   p_net_plant, p_et_plant, p_th_plant
          'costs': CAS10-CAS60, CAS20, total_capital, overnight_capital
          'economics': CAS70, CAS71, CAS72, CAS80, CAS90, lcoe_USD_per_MWh
          'cas22': C220101-C220112, C220200-C220700
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

        # Convenience top-level aliases
        results["net_electric_MW"] = power["p_net"]
        results["lcoe_cents_per_kWh"] = econ["lcoe_cents_per_kWh"]
        results["total_capital_M_USD"] = costs["total_capital"]

        return results


# ===========================================================================
# Module-level interface for concept explorer
# ===========================================================================

params = PoloMacPlantParams()
results = params.compute()


# ===========================================================================
# OUTPUT FUNCTIONS
# ===========================================================================

def print_results(p: PoloMacPlantParams, r: dict):
    """Pretty-print the PoloMac LCOE model results with full CAS breakdown."""
    power = r["power"]
    geom = r["geometry"]
    cas22 = r["cas22"]
    costs = r["costs"]
    econ = r["economics"]

    print("=" * 72)
    print("PoloMac Magnetic Confinement (Deutelio) — Free-Form LCOE Model")
    print("1cFE Concept Analysis  |  D-D Fuel  |  SCENARIO BOUNDS, NOT ESTIMATE")
    print("=" * 72)

    print("\n⚠  ALL PLASMA PARAMETERS ARE SCENARIO ASSUMPTIONS (see analysis.md §S2)")
    print("   Blocking gaps: no Q_sci, no P_fus, no confinement physics.")
    print("   Heating approach partially resolved: ECH (4 GHz) for prototype;")
    print("   commercial-scale heating power and integration still unspecified.")
    print("   Results test whether competitive LCOE is POSSIBLE, not that it IS.\n")

    # --- Key Inputs ---
    print("--- Key Input Parameters ---")
    print(f"  Fusion power (assumed):     {p.p_fus_MW:.0f} MW")
    print(f"  Scientific Q (assumed):     {p.Q_sci:.1f}  → heating = {p.p_fus_MW/p.Q_sci:.0f} MW")
    print(f"  SC coil capital:            ${p.sc_coil_capital_M:.0f}M  [override, HIGH UNCERTAINTY]")
    print(f"  SC coil lifetime:           {p.sc_coil_lifetime_FPY:.0f} FPY  [HIGH UNCERTAINTY]")
    print(f"  SC cryo load:               {p.sc_coil_cryo_MW:.0f} MW  (vs 700 MW copper reference)")
    print(f"  Thermal efficiency:         {p.thermal_efficiency:.1%}  [MODERATE UNCERTAINTY]")
    print(f"  Plant capacity factor:      {p.plant_availability:.1%}  [HIGH UNCERTAINTY]")
    print(f"  Modules:                    {p.n_mod}")
    print(f"  NOAK:                       {'Yes' if p.noak else 'No (FOAK)'}")
    print(f"  Interest rate:              {p.interest_rate:.1%}")
    print(f"  Construction time:          {p.construction_time_years:.0f} years")
    print(f"  Plant lifetime:             {p.plant_lifetime_years:.0f} years")

    # --- Geometry ---
    print(f"\n--- Plasma Geometry ---")
    print(f"  Major radius:               {p.R_major_m:.1f} m")
    print(f"  Minor radius:               {p.R_minor_m:.1f} m  (elongation κ={p.elongation:.1f})")
    print(f"  Plasma volume:              {geom['V_plasma_m3']:.0f} m³"
          f"  (2014 study: 1300 m³ at sub-reactor scale)")
    print(f"  Outer minor radius:         {geom['a_outer_m']:.1f} m")
    print(f"  Blanket volume:             {geom['blanket_vol_m3']:.0f} m³")
    print(f"  Shield volume:              {geom['shield_vol_m3']:.0f} m³")

    # --- Power Balance ---
    print(f"\n--- Power Balance (D-D fuel, steady-state) ---")
    print(f"  Fusion power:               {power['p_fus']:.0f} MW")
    print(f"    Neutron power:            {power['p_neutron']:.0f} MW ({DD_NEUTRON_FRACTION:.1%})")
    print(f"    Charged particle power:   {power['p_charged']:.0f} MW ({DD_CHARGED_FRACTION:.1%})")
    print(f"  Thermal power:              {power['p_th']:.0f} MW")
    print(f"  Gross electric:             {power['p_et']:.0f} MWe")
    print(f"  Recirculating power:")
    print(f"    Heating wall-plug:        {power['p_recirc_heat']:.0f} MW"
          f"  (={p.p_fus_MW/p.Q_sci:.0f} MW plasma / 60% heater eff)")
    print(f"    SC coil cryo:             {power['p_cryo']:.0f} MW  [vs 700 MW copper]")
    print(f"    Housekeeping:             {power['p_aux']:.0f} MW")
    print(f"    Heat overhead:            {power['p_heat_overhead']:.0f} MW")
    print(f"    TOTAL recirculating:      {power['p_recirc_total']:.0f} MW")
    print(f"  Net electric:               {power['p_net']:.0f} MWe")
    print(f"  Engineering Q:              {power['Q_eng']:.2f}")
    print(f"  Recirculating fraction:     {power['recirc_fraction']:.1%}")

    # --- CAS22 ---
    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    print(f"  Per-module accounts:")
    cas22_labels = {
        "C220101": ("First Wall + Blanket (D-D, no breed)", False),
        "C220102": ("Shield (D-D, 0.7× D-T scale)", False),
        "C220103": ("In-vessel SC Dipole Coil", True),
        "C220104": ("Heating System (NBI/RF analogue)", True),
        "C220105": ("Primary Structure", False),
        "C220106": ("Vacuum System (vessel)", False),
        "C220107": ("Power Supplies", False),
        "C220108": ("Target Factory (N/A)", False),
        "C220110": ("Remote Handling (1.5× enhanced)", True),
        "C220111": ("Installation Labor", False),
        "C220112": ("Isotope Separation (N/A, D-D)", False),
    }
    for code, (label, override) in cas22_labels.items():
        val = cas22.get(code, 0.0)
        tag = " [override]" if override else ""
        if val > 0.1:
            print(f"    {code}  {label:<38s} ${val:>8.1f}M{tag}")
    print(f"    {'─' * 58}")
    print(f"    Per-module subtotal:                              ${cas22['CAS22_per_module']:>8.1f}M × {p.n_mod}")

    print(f"  Plant-wide accounts:")
    pw_labels = {
        "C220200": "Coolant Systems",
        "C220300": "Aux Cooling + Cryoplant (SC coil)",
        "C220400": "Radioactive Waste Management",
        "C220500": "Fuel Handling (D-D, no T breeding)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    for code, label in pw_labels.items():
        val = cas22[code]
        if val > 0.1:
            print(f"    {code}  {label:<38s} ${val:>8.1f}M")
    print(f"    {'─' * 58}")
    print(f"    Plant-wide subtotal:                              ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                                        ${cas22['CAS22']:>8.1f}M")

    # --- Capital Costs ---
    print(f"\n--- Capital Costs (CAS10-60) ---")
    cas_lines = [
        ("CAS10", "Pre-construction"),
        ("CAS21", "Buildings"),
        ("CAS22", "Reactor Plant Equipment"),
        ("CAS23", "Turbine Plant"),
        ("CAS24", "Electric Plant"),
        ("CAS25", "Misc Plant"),
        ("CAS26", "Heat Rejection"),
        ("CAS27", "Special Materials"),
        ("CAS28", "Digital Twin"),
        ("CAS29", "Contingency"),
    ]
    for k, label in cas_lines:
        val = costs.get(k, 0.0)
        print(f"  {k}  {label:<38s} ${val:>8.1f}M")
    print(f"  {'─' * 58}")
    print(f"  CAS20  {'Direct Costs':<38s} ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30  {'Indirect Costs':<38s} ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40  {'Owner Costs':<38s} ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50  {'Supplementary Costs':<38s} ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 58}")
    print(f"  {'Overnight Capital':<42s} ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60  {'IDC (f={:.3f})'.format(costs['f_IDC']):<38s} ${costs['CAS60']:>8.1f}M")
    print(f"  {'═' * 58}")
    print(f"  {'Total Capital':<42s} ${costs['total_capital']:>8.1f}M")
    print(f"  {'Specific Capital':<42s} ${costs['specific_capital_USD_per_kWe']:>8.0f} $/kWe")

    # --- Annual Costs ---
    print(f"\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90  Capital charge (CRF={econ['CRF']:.4f}):        ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71  O&M (levelized):                     ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72a FW/blanket replacement ({econ['n_fw_replacements']} times):    ${econ['CAS72a_blanket']:>8.1f}M/yr")
    print(f"  CAS72b SC coil replacement    ({econ['n_coil_replacements']} times):    ${econ['CAS72b_coil']:>8.1f}M/yr  [HIGH UNCERTAINTY]")
    print(f"  CAS72  Scheduled replacement (total):       ${econ['CAS72']:>8.1f}M/yr")
    print(f"  CAS70  Total O&M:                           ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80  Fuel (D-D deuterium):                ${econ['CAS80']:>8.4f}M/yr"
          f"  ({econ['CAS80_deuterium_kg_yr']:.2f} kg D burned/yr, D-D cost ≈ negligible)")

    # --- LCOE ---
    print(f"\n--- LCOE ---")
    print(f"  Annual net energy:          {econ['annual_energy_MWh']:,.0f} MWh")
    print(f"  Annual revenue requirement: ${econ['annual_revenue_req']:.1f}M")
    print(f"  ╔══════════════════════════════════════════╗")
    print(f"  ║  LCOE = {econ['lcoe_cents_per_kWh']:>7.2f} ¢/kWh                   ║")
    print(f"  ║       = {econ['lcoe_USD_per_MWh']:>7.1f} $/MWh                   ║")
    print(f"  ╚══════════════════════════════════════════╝")
    print(f"  Capital fraction (CAS90):   {econ.get('capital_fraction', 0):.1%}")
    print(f"  O&M fraction (CAS70):       {econ.get('om_fraction', 0):.1%}")
    print(f"  Fuel fraction (CAS80):      {econ.get('fuel_fraction', 0):.1%}")


def sensitivity_sweep(base_p: PoloMacPlantParams, param_name: str,
                      values: list, label: str = "") -> list:
    """Sweep a single parameter and return LCOE results for each value."""
    results_list = []
    for val in values:
        p = PoloMacPlantParams(**{**base_p.__dict__, param_name: val})
        r = p.compute()
        results_list.append({
            "param_value": float(val),
            "lcoe_cents_kWh": r["lcoe_cents_per_kWh"],
            "net_electric_MW": r["net_electric_MW"],
        })
    return results_list


def main():
    """
    Run baseline, sensitivity sweeps, scenario comparison, and binding constraints.
    """

    # -------------------------------------------------------------------------
    # 1. BASELINE RESULTS
    # -------------------------------------------------------------------------
    baseline = PoloMacPlantParams()
    base_r = baseline.compute()

    print_results(baseline, base_r)

    # -------------------------------------------------------------------------
    # 2. SENSITIVITY SWEEPS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("SENSITIVITY ANALYSIS — Single-Parameter Sweeps from Baseline")
    print("Baseline LCOE: {:.2f} ¢/kWh".format(base_r["lcoe_cents_per_kWh"]))
    print("=" * 72)

    sweeps = [
        ("sc_coil_capital_M",   [200, 300, 400, 500, 700, 1000], "SC coil capital cost [M$]"),
        ("Q_sci",               [3, 5, 7, 10, 15, 20],           "Scientific Q (plasma gain)"),
        ("p_fus_MW",            [200, 300, 500, 750, 1000],      "Fusion power [MW]"),
        ("plant_availability",  [0.40, 0.55, 0.70, 0.80, 0.90], "Plant capacity factor"),
        ("sc_coil_lifetime_FPY",[3, 5, 8, 12, 20],              "SC coil lifetime [FPY]"),
        ("thermal_efficiency",  [0.30, 0.35, 0.38, 0.42, 0.46], "Thermal efficiency"),
        ("sc_coil_cryo_MW",     [5, 10, 15, 25, 50, 100],       "SC cryogenic load [MW]"),
    ]

    for param_name, values, label in sweeps:
        print(f"\n  {label}:")
        sweep_results = sensitivity_sweep(baseline, param_name, values)
        for sr in sweep_results:
            val = sr["param_value"]
            lcoe = sr["lcoe_cents_kWh"]
            net = sr["net_electric_MW"]
            flag = " ⟵ competitive" if lcoe <= 10.0 else ""
            if net <= 0:
                print(f"    {val:>8.3g}  →  NET POWER NEGATIVE ({net:.0f} MWe)")
            else:
                print(f"    {val:>8.3g}  →  {lcoe:>7.2f} ¢/kWh  ({net:.0f} MWe){flag}")

    # -------------------------------------------------------------------------
    # 3. SCENARIO COMPARISON TABLE
    # -------------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("SCENARIO COMPARISON: Conservative | Moderate | Optimistic")
    print("=" * 72)

    scenarios = {
        "Conservative": PoloMacPlantParams(
            # Poor Q, low fusion power, expensive/fragile coil, low CF
            Q_sci=5.0,
            p_fus_MW=300.0,
            sc_coil_capital_M=800.0,
            sc_coil_lifetime_FPY=4.0,
            sc_coil_cryo_MW=25.0,
            plant_availability=0.50,
            thermal_efficiency=0.35,
            heating_system_cost_M=200.0,
            interest_rate=0.10,
            construction_time_years=9.0,
            noak=False,          # FOAK: higher contingency + pre-construction
        ),
        "Moderate": PoloMacPlantParams(
            # Baseline (defaults)
        ),
        "Optimistic": PoloMacPlantParams(
            # Good Q, high fusion power, cheap/durable SC coil, high CF
            Q_sci=15.0,
            p_fus_MW=800.0,
            sc_coil_capital_M=280.0,
            sc_coil_lifetime_FPY=15.0,
            sc_coil_cryo_MW=8.0,
            plant_availability=0.85,
            thermal_efficiency=0.42,
            heating_system_cost_M=100.0,
            interest_rate=0.06,
            construction_time_years=6.0,
        ),
    }

    header = f"  {'Scenario':<16} {'P_fus':>7} {'Q_sci':>6} {'P_net':>7} {'CapEx':>9} {'LCOE':>10}"
    print(header)
    print("  " + "─" * 60)
    for name, sc_params in scenarios.items():
        r = sc_params.compute()
        lcoe = r["economics"]["lcoe_USD_per_MWh"]
        p_net = r["power"]["p_net"]
        capex = r["costs"]["specific_capital_USD_per_kWe"]
        pf = sc_params.p_fus_MW
        Q = sc_params.Q_sci
        lcoe_str = f"{lcoe:.1f} $/MWh" if p_net > 0 else "NEGATIVE"
        capex_str = f"${capex:.0f}/kWe" if p_net > 0 else "N/A"
        print(f"  {name:<16} {pf:>6.0f}MW {Q:>5.0f}  {p_net:>6.0f}MW {capex_str:>9} {lcoe_str:>10}")

    # -------------------------------------------------------------------------
    # 4. D-T SCENARIO COMPARISON (F-2: D-T is a stated design claim)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("D-T SCENARIO COMPARISON — Conservative | Moderate | Optimistic")
    print("D-T: 80% neutron / 20% charged particle | requires tritium breeding blanket")
    print("D-T achievable Q ≥ 10 is far more plausible than D-D Q ≥ 10")
    print("Tests whether blanket cost penalty exceeds the Q threshold benefit")
    print("=" * 72)

    dt_scenarios = {
        "Conservative": PoloMacPlantParams(
            Q_sci=7.0,
            p_fus_MW=300.0,
            dd_neutron_fraction=DT_NEUTRON_FRACTION,
            blanket_unit_cost_dd=0.60,         # D-T breeding blanket unit cost (1costingfe)
            dt_tritium_blanket_capital_M=400.0, # high-end tritium system capital
            sc_coil_capital_M=800.0,
            sc_coil_lifetime_FPY=4.0,
            sc_coil_cryo_MW=25.0,
            plant_availability=0.50,
            thermal_efficiency=0.35,
            heating_system_cost_M=200.0,
            interest_rate=0.10,
            construction_time_years=9.0,
            noak=False,
        ),
        "Moderate": PoloMacPlantParams(
            Q_sci=10.0,
            p_fus_MW=500.0,
            dd_neutron_fraction=DT_NEUTRON_FRACTION,
            blanket_unit_cost_dd=0.60,
            dt_tritium_blanket_capital_M=300.0,
        ),
        "Optimistic": PoloMacPlantParams(
            Q_sci=15.0,
            p_fus_MW=800.0,
            dd_neutron_fraction=DT_NEUTRON_FRACTION,
            blanket_unit_cost_dd=0.60,
            dt_tritium_blanket_capital_M=200.0,  # low-end tritium system capital
            sc_coil_capital_M=280.0,
            sc_coil_lifetime_FPY=15.0,
            sc_coil_cryo_MW=8.0,
            plant_availability=0.85,
            thermal_efficiency=0.42,
            heating_system_cost_M=100.0,
            interest_rate=0.06,
            construction_time_years=6.0,
        ),
    }

    print(f"\n  D-D vs D-T at equivalent scenario assumptions (blanket = tritium breeding capital):")
    hdr = (f"  {'Scenario':<22} {'Fuel':<5} {'P_fus':>7} {'Q':>4} "
           f"{'P_net':>7} {'Blanket$':>9} {'CapEx':>10} {'LCOE':>10}")
    print(hdr)
    print("  " + "─" * 79)
    for name, sc_params in scenarios.items():
        r = sc_params.compute()
        lcoe = r["economics"]["lcoe_USD_per_MWh"]
        p_net = r["power"]["p_net"]
        capex = r["costs"]["specific_capital_USD_per_kWe"]
        lcoe_str = f"{lcoe:.1f} $/MWh" if p_net > 0 else "NEGATIVE"
        capex_str = f"${capex:.0f}/kWe" if p_net > 0 else "N/A"
        print(f"  {name:<22} {'D-D':<5} {sc_params.p_fus_MW:>6.0f}MW {sc_params.Q_sci:>3.0f}"
              f"  {p_net:>6.0f}MW {'none':>9} {capex_str:>10} {lcoe_str:>10}")
    print("  " + "─" * 79)
    for name, sc_params in dt_scenarios.items():
        r = sc_params.compute()
        lcoe = r["economics"]["lcoe_USD_per_MWh"]
        p_net = r["power"]["p_net"]
        capex = r["costs"]["specific_capital_USD_per_kWe"]
        lcoe_str = f"{lcoe:.1f} $/MWh" if p_net > 0 else "NEGATIVE"
        capex_str = f"${capex:.0f}/kWe" if p_net > 0 else "N/A"
        blanket_str = f"${sc_params.dt_tritium_blanket_capital_M:.0f}M"
        print(f"  {name:<22} {'D-T':<5} {sc_params.p_fus_MW:>6.0f}MW {sc_params.Q_sci:>3.0f}"
              f"  {p_net:>6.0f}MW {blanket_str:>9} {capex_str:>10} {lcoe_str:>10}")

    # -------------------------------------------------------------------------
    # 5. KEY BINDING CONSTRAINTS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("KEY BINDING CONSTRAINTS — Ranked by Model Sensitivity")
    print("=" * 72)
    print("""
  1. PLASMA Q AND FUSION POWER (dominant LCOE levers)
     Q_sci and fusion power produce the widest LCOE swings in the model.
     At Q=3 (near D-D threshold), net power goes negative — no viable output.
     At Q=20, LCOE reaches ~68 ¢/kWh. Fusion power swings LCOE from ~751 ¢/kWh
     at 200 MW to ~50 ¢/kWh at 1000 MW (a 15× range). These are TRL-1 unknowns:
     no confinement physics data exists for PoloMac, and D-D ignition requires
     ~6× higher plasma pressure than D-T at equivalent density. D-D Q ≥ 10 is
     an extraordinary extrapolation from current dipole experiments. This is the
     parameter that most governs whether PoloMac's economics are investigable.

  2. THERMAL EFFICIENCY AND CAPACITY FACTOR (secondary physics/engineering levers)
     Thermal efficiency swings LCOE from 193 ¢/kWh (30%) to 64 ¢/kWh (46%) —
     a 3× range across plausible engineering designs. Capacity factor similarly
     moves LCOE ~40% across CF=0.40–0.90. Both are driven by downstream
     engineering (power conversion cycle design, maintenance regime) that has
     not been specified for PoloMac. The SC coil replacement interval is the
     primary driver of forced outage and therefore the primary lever on CF.

  3. SC COIL VIABILITY (framing constraint, secondary cost lever)
     The 700 MW copper coil draw (Elio 2014) is an absolute economic barrier —
     no viable LCOE is possible without the superconducting coil path. However,
     once the SC path is assumed, LCOE sensitivity to sc_coil_capital_M is
     narrower than for Q or fusion power: a 5× capital span ($200M–$1000M)
     produces only ~82–115 ¢/kWh. Coil lifetime produces the narrowest
     sensitivity of any swept parameter (109–90 ¢/kWh from 3 to 20 FPY).
     The SC coil constraint matters primarily as a viability gate — the model
     requires cryo load ≲ 100 MW; at ~100 MW cryo, net power falls to near zero
     as recirculating draw exhausts gross electric output entirely.
""")


if __name__ == "__main__":
    main()
