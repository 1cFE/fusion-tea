"""
p-B11 FRC (TAE Technologies) Free-Form LCOE Model
===================================================
1cFE First Pass Concept Analysis
Concept: p-B11 Field-Reversed Configuration, Neutral Beam Injection driven
Company: TAE Technologies (Mission Viejo, CA)
Commercial Design: Da Vinci (50 MWe initial; 350–500 MWe at scale)

This model explores three scenario branches driven by physics uncertainty:
  Branch A — Physics fails: Q_plasma < viability threshold → no LCOE output.
  Branch B — Steam conversion: Da Vinci baseline at ~32% thermal efficiency.
  Branch C — ICC upgrade: Inverse Cyclotron Converter at ~90% direct efficiency.

The model's primary analytical function is to map the Q_plasma × η_NBI parameter
space and identify the viability boundary. The p-B11 physics question (can
Q_plasma > 1 be achieved at all?) is the binding unknown — this is qualitatively
different from engineering uncertainties in D-T concepts where the physics is
validated. There is no standard 1costingfe concept template for this case.

Power balance:
  NBI wall-plug → plasma coupling (η_NBI) → p-B11 fusion (Q_plasma amplification)
  → charged alpha particles (all fusion energy in alphas, aneutronic)
  → radiation loss fraction (bremsstrahlung at 150–300 keV ion temp)
  → thermal or ICC conversion → gross electric
  → minus NBI wall-plug recirculating load → minus auxiliaries → net electric

Viability threshold (Q_plasma breakeven, ignoring auxiliaries):
  Q_break = 1 / [(1 - f_rad) × η_conv × η_NBI]
  At f_rad=0.15, η_th=0.32, η_NBI=0.55:  Q_break ≈ 6.7 (mathematical breakeven)
  Commercial minimum: Q_plasma ≥ 10–15 for 50 MWe net with margin.

Compounding penalty (Mulder et al. arXiv:2103.12451): at sub-unity capacity
factor, NBI recirculating power stays near full-load level (plasma stability
requires continuous NBI), so the effective recirculating fraction rises above
the rated-power calculation. Capacity factor and Q_plasma interact multiplicatively.

CAS cost structure follows 1costingfe costing_constants.yaml with overrides:
  C220101: Minimal X-ray absorber/HX (p-B11 unit cost 0.05 M$/m³, no breeding)
  C220102: Thin water/boron shield (10% of DT shield cost, <1% neutron fraction)
  C220103: Copper resistive coils (override, near-unity FRC beta, ~0.1 T field)
  C220104: NBI system (override, dominant capital driver, ~$10M/MW_NBI)
  C220109: ICC direct converter (Branch C only)
  No hot cell (CAS21), no tritium handling (CAS220500 → boron handling only),
  no remote handling robotics, no D-T startup fuel, no REBCO supply chain.
  O&M: 1costingfe pb11 scaling, 24.0 M$/yr × (P_net/1GWe)^0.5.
  Buildings: 1costingfe pb11 factor, $308/kW × P_net_plant [at 1 GWe ref].

Economy-of-scale scaling to 1000 MWe cross-concept reference (α = 0.6):
  scaled_headline provides LCOE and overnight cost at normalized 1000 MWe.
  Native physics-derived power balance is NOT changed.

Key references:
  - TAE C-2W/Norman machine details (plasma parameters):
    tae-c2w-machine-details.md [iter-01/sources/]
  - TAE DJT Merger / Da Vinci specs (50 MWe, 2026 construction):
    tae-djt-merger-davinci-specs.md [iter-02/sources/]
  - TAE FAQ (steam Rankine baseline confirmed):
    tae-energy-conversion-clarification.md [iter-02/sources/]
  - TAE ICC patents: US7459654, US6628740, US6888907 (>90% efficiency claim)
    tae-energy-conversion-notes.md [iter-01/sources/]
  - Mulder et al. arXiv:2103.12451 (capacity factor × recirculating power)
    arxiv-2103-12451.md [iter-02/sources/]
  - Grokipedia TAE Technologies (concept narrative + FRC stability at scale):
    grokipedia-tae-technologies.md [iter-01/sources/]
  - 1costingfe costing_constants.yaml (scaling laws and unit costs)
  - analysis.md §Section 2, 5 (quantitative inputs and viability derivation)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass

# === Reference power levels for CAS scaling laws (from 1costingfe) ===
P_TH_REF = 2500.0    # Reference thermal power [MW]
P_ET_REF = 1100.0    # Reference gross electric power [MW]
P_NET_REF = 1000.0   # Reference net electric power [MW]


@dataclass
class PB11FRCPlantParams:
    """
    Parameterized p-B11 FRC (TAE Da Vinci) LCOE model.

    Five-layer CAS-structured computation:
      Layer 1: _compute_power()     — NBI → plasma → fusion → electric
      Layer 2: _compute_geometry()  — cylindrical FRC annular volumes
      Layer 3: _compute_cas22()     — CAS22 Reactor Plant Equipment sub-accounts
      Layer 4: _compute_costs()     — CAS10-60 capital costs
      Layer 5: _compute_economics() — CAS70-90 annualized costs → LCOE
    """

    # ========== PHYSICS / POWER BALANCE ==========

    q_plasma: float = 15.0
    """Plasma energy gain Q = P_fusion / P_NBI_absorbed (physics Q).
    Source: Viability threshold derived in analysis.md §Section 2, Challenge 3.
    Mathematical breakeven ≈ 6.7 (at η_th=0.32, η_NBI=0.55, f_rad=0.15);
    commercial minimum Q ≥ 10–15 for 50 MWe net with adequate margin.
    Current record: C-2W/Norman at ~3 keV total temperature, Q << 1.
    Da Vinci target: ~250 keV ion temperature — ~80× extrapolation unvalidated.
    Ref: analysis.md §Section 2 Challenge 3. HIGH UNCERTAINTY.
    TESTABLE PROPOSITION: IF Q_plasma ≥ 10–15 AND η_NBI ≥ 0.55, THEN net
    electricity is achievable with steam conversion at Da Vinci 50 MWe scale;
    ELSE concept does not produce net electricity (Branch A — no LCOE)."""

    p_nbi_plasma_MW: float = 26.0
    """NBI power absorbed by the plasma [MW].
    Source: Derived to yield ~50 MWe net at Q_plasma=15, η_NBI=0.55, η_th=0.32,
    f_rad=0.15: P_NBI = (P_net_target + P_aux) / [Q×(1−f_rad)×η_th − 1/η_NBI]
    = (50 + 7.5) / [15×0.85×0.32 − 1/0.55] = 57.5 / 2.262 ≈ 25.4 MW → 26 MW.
    C-2W/Norman operated at up to 21 MW NBI [tae-c2w-machine-details.md §NBI System].
    Da Vinci is a modest scale-up, but beam energy (>120 keV) introduces new
    engineering challenges (negative-ion NBI required for efficient neutralization).
    Ref: analysis.md §Section 3 NBI System at 250+ keV. MODERATE UNCERTAINTY."""

    eta_nbi: float = 0.55
    """NBI wall-plug efficiency (wall-plug power → plasma-absorbed power).
    Source: Analogue from negative-ion NBI systems used in fusion research.
    Positive-ion NBI at high energy: ~40–50%; negative-ion NBI: ~50–65%.
    Da Vinci beam energy unpublished; 55% is a mid-range negative-ion estimate.
    At η_NBI = 0.40 (positive-ion), Q_break rises to ~8.6, commercial minimum
    to Q ≥ 20, tightening the viability constraint substantially.
    Ref: analysis.md §Section 2 Challenge 3. MODERATE UNCERTAINTY."""

    eta_th: float = 0.32
    """Thermal-to-electric conversion efficiency (steam Rankine, Branch B only).
    Source: Official TAE FAQ confirms Da Vinci uses steam turbine baseline
    [tae-energy-conversion-clarification.md §How do you produce electricity].
    Standard steam Rankine at fusion-relevant temperatures: 30–35%; using 32%.
    Ref: analysis.md §Section 5. MODERATE UNCERTAINTY."""

    eta_icc: float = 0.90
    """Inverse Cyclotron Converter direct conversion efficiency (Branch C only).
    Source: TAE patent claim for ICC direct conversion of MeV-range alpha particles.
    Ref: tae-energy-conversion-notes.md §ICC Efficiency; US7459654.
    Da Vinci baseline does NOT use ICC — ICC is a future upgrade technology.
    HIGH UNCERTAINTY — zero experimental demonstration at MeV-range energies."""

    f_rad: float = 0.15
    """Fraction of fusion energy lost to radiation (bremsstrahlung + synchrotron).
    Source: 1costingfe costing_constants.yaml, f_rad_pb11 = 0.15.
    Reflects high-Z bremsstrahlung penalty at 150–300 keV in the T_i >> T_e
    non-equilibrium regime TAE requires. In a fully thermalized plasma, radiation
    losses would dominate and Q_plasma > 1 would be impossible.
    Ref: analysis.md §Section 2 Challenge 1. HIGH UNCERTAINTY."""

    use_icc: bool = False
    """Energy conversion mode: False = Branch B (steam), True = Branch C (ICC).
    Branch A (physics fails) is flagged when Q_plasma < viability threshold."""

    # ========== PLANT CONFIGURATION ==========

    plant_availability: float = 0.85
    """Plant capacity factor / availability.
    Source: Steady-state FRC avoids disruption penalties of pulsed MFE.
    However, CW FRC operation is undemonstrated (C-2W pulse record ~30–40 ms).
    Early Da Vinci plants likely below 90%; using 85% as moderate first-gen estimate.
    COMPOUNDING INTERACTION: NBI must remain at near-full power to maintain FRC
    stability even at reduced output, so effective recirculating fraction rises as
    CF falls below unity — tightening the Q_plasma floor beyond the rated-power
    calculation [arxiv-2103-12451.md: recirculated power remains high at reduced
    output]. CF and Q_plasma interact multiplicatively, not independently.
    Ref: analysis.md §Section 5 Gap #13. HIGH UNCERTAINTY."""

    plant_lifetime_years: float = 40.0
    """Plant economic lifetime [years]. Standard nuclear/fusion plant assumption."""

    n_mod: int = 1
    """Number of FRC modules per plant. Da Vinci is a single-module design.
    Ref: tae-djt-merger-davinci-specs.md §Deal details (50 MWe total plant)."""

    noak: bool = False
    """FOAK (False) vs NOAK (True). Da Vinci is first-of-a-kind → FOAK=True here.
    FOAK applies 10% contingency on direct costs (CAS29)."""

    interest_rate: float = 0.08
    """Real discount rate (WACC) [fraction]. Standard 1costingfe default."""

    construction_time_years: float = 6.0
    """Construction time [years].
    Da Vinci timeline: construction 2026, first plasma 2029, operations 2031
    [tae-djt-merger-davinci-specs.md] → ~5 years; using 6 as conservative."""

    inflation_rate: float = 0.02
    """Inflation rate for levelizing O&M costs over plant lifetime."""

    # ========== GEOMETRY (cylindrical FRC) ==========

    frc_separatrix_radius_m: float = 1.5
    """FRC separatrix (plasma column) radius [m].
    Source: Da Vinci requires 'major radii of approximately 1–2 meters'
    [grokipedia-tae-technologies.md §FRC Stability at Scale]. Using 1.5 m midpoint.
    C-2W/Norman Rs = 0.4 m [dossier.md §Confinement Concept] — Da Vinci is ~3.75×
    scale-up in radius; stability at this scale is unvalidated.
    Ref: analysis.md §Section 5 missing parameters table. MODERATE UNCERTAINTY."""

    frc_axial_length_m: float = 10.0
    """FRC axial plasma length [m].
    Source: C-2W aspect ratio Rs:L ≈ 0.4:2 = 1:5. Extrapolating to Rs=1.5 m
    gives L ≈ 7.5 m; using 10 m for rounding and margin. Da Vinci geometry
    not publicly disclosed.
    Ref: analysis.md §Section 5 missing parameters table. HIGH UNCERTAINTY."""

    blanket_thickness_m: float = 0.30
    """X-ray absorber / first-wall annular thickness [m].
    Source: p-B11 FRC has no D-T breeding blanket. Minimal X-ray absorber and
    heat exchanger only (alpha particle energy deposition from charged fusion
    products). Thickness set by X-ray absorption depth and heat exchanger coupling.
    Ref: analysis.md §Section 7 Structural TEA differences. HIGH UNCERTAINTY."""

    shield_thickness_m: float = 0.20
    """Neutron + X-ray biological shield annular thickness [m].
    Source: p-B11 fusion produces <1% secondary neutrons — thin water/boron
    shield only, vs. multi-meter composite D-T shielding.
    Ref: analysis.md §Section 7. MODERATE UNCERTAINTY."""

    structure_thickness_m: float = 0.15
    """Primary structure annular thickness [m]. ASSUMED: analogy to FRC vessel."""

    vessel_thickness_m: float = 0.05
    """Vacuum vessel annular thickness [m]. ASSUMED: thin-wall linear device."""

    # ========== CAS22 OVERRIDES ==========

    nbi_cost_per_MW_M_USD: float = 10.0
    """NBI system capital cost per MW of plasma-coupled NBI power [M$/MW].
    Maps to CAS22 account C220104 (Supplementary Heating) — dominant cost driver.
    Source: ITER NBI (2 × 33 MW at 1 MeV D, negative-ion) capital ~$500M total
    → ~$7.6M/MW. TAE claims 50% cost reduction from NBI-only Norm breakthrough
    [tae-nbi-breakthrough-2025.md §The Norm Breakthrough] vs. prior design.
    Using $10M/MW as conservative FOAK estimate for custom fusion-scale NBI.
    No commercial supply chain exists for high-energy NBI at Da Vinci power levels.
    Ref: analysis.md §Section 3 NBI System at 250+ keV. HIGH UNCERTAINTY."""

    magnet_cost_M_USD: float = 20.0
    """Copper resistive coil system capital cost [M$]. Maps to C220103.
    Source: C-2W uses copper coils for equilibrium + mirror fields at ~0.1 T.
    Near-unity FRC beta (~90–100%) means very modest external field — no REBCO
    required [grokipedia-tae-technologies.md §FRC Fundamentals].
    Continuous resistive power consumption (p_magnet_MW) is an operating cost.
    Ref: analysis.md §Section 3 Copper Resistive Magnets. MODERATE UNCERTAINTY."""

    icc_cost_M_USD: float = 100.0
    """ICC direct conversion system base capital cost [M$] (Branch C only).
    Maps to C220109. Scaled by (P_ICC_output / 400 MWe)^0.6.
    Source: 1costingfe dec_base = 100.0 M$ at 400 MWe DEC electric output.
    ICC is patent-stage only; no experimental ICC at MeV-range energies.
    Ref: tae-energy-conversion-notes.md; 1costingfe costing_constants.yaml.
    HIGH UNCERTAINTY."""

    # ========== AUXILIARY LOADS ==========

    p_magnet_MW: float = 3.0
    """Continuous electrical power for copper resistive coils [MW].
    Source: Resistive coil power at ~0.1 T external field over Da Vinci
    coil geometry. ASSUMED: order-of-magnitude estimate. HIGH UNCERTAINTY."""

    p_house_MW: float = 4.0
    """Housekeeping / facility power [MW]. Standard plant auxiliary load."""

    p_fuel_inject_MW: float = 0.5
    """Boron-11 fuel injection system power [MW].
    Source: p-B11 plasma fueling via boron powder or gas puffing.
    Negligible compared to NBI recirculating load. ASSUMED."""

    # ========== COMPONENT LIFETIMES ==========

    core_lifetime_FPY: float = 50.0
    """First-wall / X-ray absorber lifetime [full-power years before replacement].
    Source: 1costingfe costing_constants.yaml core_lifetime_pb11 = 50.0 FPY.
    Near-absence of 14 MeV neutrons means minimal radiation damage (~0.1 dpa/yr).
    Dominant wear mechanism: alpha particle sputtering (manageable).
    Ref: 1costingfe costing_constants.yaml."""

    # ========== FUEL COSTS ==========

    u_b11_per_kg: float = 10000.0
    """Enriched B-11 fuel unit cost [$/kg], FOAK estimate.
    Source: 1costingfe costing_constants.yaml u_b11 = 10000 (FOAK industrial supply).
    NOAK: u_b11_noak = 75 $/kg (industrial chemical exchange distillation at scale).
    Natural boron: ~80% B-11 by abundance [grokipedia-tae-technologies.md].
    Fuel cost contribution to LCOE is negligible (<$1/MWh even at FOAK prices).
    Ref: analysis.md §Section 5 (B-11 fuel cost estimated <$1/MWh)."""

    def _compute_power(self) -> dict:
        """Layer 1: NBI → plasma → fusion → electric power balance.

        Energy flow per module:
          P_NBI_wall = P_NBI_plasma / η_NBI          (wall-plug NBI draw)
          P_fus = Q_plasma × P_NBI_plasma             (fusion power amplification)
          P_alpha = P_fus                              (all energy in charged alphas)
          P_available = P_fus × (1 − f_rad)           (after bremsstrahlung losses)
          P_et = P_available × η_conv                  (gross electric)
          P_net = P_et − P_NBI_wall − P_aux           (net electric)

        Viability threshold (rated-power, no auxiliaries):
          Q_break = 1 / [(1−f_rad) × η_conv × η_NBI]
          Below Q_break: no net electricity possible → Branch A.
          Above Q_break: Branch B (steam) or C (ICC).

        Sub-unity capacity factor tightens Q_plasma floor beyond this rated-power
        estimate because NBI stays near full power even at reduced output
        [arxiv-2103-12451.md], raising the effective recirculating fraction.
        """
        r = {}

        # NBI wall-plug power draw (recirculating load)
        p_nbi_wall = self.p_nbi_plasma_MW / self.eta_nbi
        r["p_nbi_wall_MW"] = p_nbi_wall

        # Fusion power: Q_plasma amplification of NBI plasma coupling
        p_fus = self.q_plasma * self.p_nbi_plasma_MW
        r["p_fus"] = p_fus

        # p-B11 → 3α: essentially all fusion energy in charged alpha particles
        r["p_alpha"] = p_fus       # charged particle power [MW]
        r["p_neutron"] = 0.0       # <1% secondary neutrons, treated as zero

        # Available power after radiation loss fraction (bremsstrahlung, synchrotron)
        p_available = p_fus * (1.0 - self.f_rad)
        r["p_available"] = p_available

        # Thermal / direct conversion to gross electric
        eta_conv = self.eta_icc if self.use_icc else self.eta_th
        r["eta_conv_used"] = eta_conv
        p_et = p_available * eta_conv
        r["p_et"] = p_et
        r["p_th"] = p_available    # available thermal / convertible power [MW]

        # Auxiliary loads (non-NBI recirculating)
        p_aux = self.p_magnet_MW + self.p_house_MW + self.p_fuel_inject_MW
        r["p_aux"] = p_aux

        # Net electric (per module)
        p_net = p_et - p_nbi_wall - p_aux
        r["p_net"] = p_net

        # Multi-module plant totals
        r["p_net_plant"] = p_net * self.n_mod
        r["p_et_plant"] = p_et * self.n_mod
        r["p_th_plant"] = p_available * self.n_mod

        # Q values
        r["Q_sci"] = self.q_plasma                                        # physics Q (input)
        r["Q_eng"] = p_net / p_nbi_wall if p_nbi_wall > 0 else 0.0       # engineering Q

        # Recirculating power fraction
        r["recirc_fraction"] = ((p_nbi_wall + p_aux) / p_et
                                if p_et > 0 else float("inf"))

        # Viability threshold at rated power (ignoring auxiliaries)
        q_break = 1.0 / ((1.0 - self.f_rad) * eta_conv * self.eta_nbi)
        r["q_plasma_breakeven"] = q_break
        r["q_plasma_commercial_min"] = q_break * 1.5   # rough 1.5× margin over breakeven

        # Branch classification
        if p_net <= 0:
            r["branch"] = "A"      # physics fails — no net electricity
        elif self.use_icc:
            r["branch"] = "C"      # ICC direct conversion
        else:
            r["branch"] = "B"      # steam Rankine baseline
        r["viable"] = p_net > 0

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Cylindrical FRC geometry — annular shells around plasma column.

        Linear FRC device: NOT spherical (unlike IFE/MIF). Geometry is a
        cylindrical plasma column surrounded by concentric annular layers.
        End-cap factor (+10%) accounts for the FRC end regions.
        """
        r = {}
        r_s = self.frc_separatrix_radius_m
        L = self.frc_axial_length_m
        end_cap_factor = 1.10     # approximate correction for end regions

        def cyl_shell_vol(r_inner: float, thickness: float) -> float:
            """Annular cylindrical shell volume [m³] with end-cap correction."""
            r_outer = r_inner + thickness
            return math.pi * L * (r_outer ** 2 - r_inner ** 2) * end_cap_factor

        # Plasma volume (reference, not a cost item)
        r["plasma_vol_m3"] = math.pi * r_s ** 2 * L

        # X-ray absorber / first wall (immediately outside plasma)
        r["blanket_vol_m3"] = cyl_shell_vol(r_s, self.blanket_thickness_m)
        r_b_out = r_s + self.blanket_thickness_m

        # Thin neutron/X-ray shield
        r["shield_vol_m3"] = cyl_shell_vol(r_b_out, self.shield_thickness_m)
        r_sh_out = r_b_out + self.shield_thickness_m

        # Primary structure
        r["structure_vol_m3"] = cyl_shell_vol(r_sh_out, self.structure_thickness_m)
        r_st_out = r_sh_out + self.structure_thickness_m

        # Vacuum vessel
        r["vessel_vol_m3"] = cyl_shell_vol(r_st_out, self.vessel_thickness_m)

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts.

        Key overrides vs. standard 1costingfe structure:
          C220101: p-B11 blanket unit cost (0.05 M$/m³, no breeding)
          C220102: 10% fuel-scale factor (aneutronic, <1% neutrons)
          C220103: Direct copper magnet cost override
          C220104: Direct NBI cost override (dominant account)
          C220107: Standard power supplies scaling (coils + control)
          C220108: Zero (no targets in steady-state MFE)
          C220109: ICC cost (Branch C only), scaled by DEC electric output
          C220110: Remote handling minimal (aneutronic, hands-on maintenance)
        """
        r = {}
        p_th = max(power["p_th"], 1.0)
        p_et = max(power["p_et"], 1.0)
        p_net = max(power["p_net"], 1.0)

        # ---- Per-module accounts ----

        # C220101: X-ray absorber / first wall — no breeding blanket
        # Unit cost: 1costingfe blanket_unit_cost_pb11 = 0.05 M$/m³
        r["C220101"] = (0.05 * geom["blanket_vol_m3"]
                        * (p_th / P_TH_REF) ** 0.6)

        # C220102: Thin neutron/X-ray shield — 10% of DT shield unit cost
        # Fuel scale factor 0.10 for aneutronic (<1% neutron fraction)
        r["C220102"] = (0.74 * geom["shield_vol_m3"] * 0.10
                        * (p_th / P_TH_REF) ** 0.6)

        # C220103: Copper resistive coils — OVERRIDE (near-unity FRC beta, ~0.1 T)
        r["C220103"] = self.magnet_cost_M_USD

        # C220104: NBI system — OVERRIDE (dominant cost account)
        # NBI duties: plasma formation, heating, current drive, MHD stabilization
        # [analysis.md §Section 2; dossier.md §Primary Heating]
        r["C220104"] = self.nbi_cost_per_MW_M_USD * self.p_nbi_plasma_MW

        # C220105: Primary structure (cylindrical FRC vessel/frame)
        r["C220105"] = (0.15 * geom["structure_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.5)

        # C220106: Vacuum system
        r["C220106"] = (0.72 * geom["vessel_vol_m3"]
                        * (p_et / P_ET_REF) ** 0.6)

        # C220107: Power supplies (coil power supplies + control)
        # Formula: 80.0 M$ at 1 GWe × (P_et/1000)^0.7
        # Ref: 1costingfe power_supplies_base = 80.0 M$
        r["C220107"] = 80.0 * (p_et / 1000.0) ** 0.7

        # C220108: Target factory — N/A (steady-state MFE, no fuel targets)
        r["C220108"] = 0.0

        # C220109: ICC direct converter (Branch C only)
        # Base: 1costingfe dec_base = 100 M$ at 400 MWe DEC output, scale ^0.6
        if self.use_icc:
            dec_ref_mwe = 400.0
            r["C220109"] = self.icc_cost_M_USD * (p_et / dec_ref_mwe) ** 0.6
        else:
            r["C220109"] = 0.0

        # C220110: Remote handling — conventional (hands-on maintenance, aneutronic)
        # 1costingfe remote_handling_pb11_base=20 M$/GWe × (P_net/1GWe)^0.6
        # Linear FRC concept scale factor 0.5 vs. toroidal reference
        r["C220110"] = 20.0 * 0.5 * (p_net / P_NET_REF) ** 0.6

        # C220111: Installation labor — 14% of reactor subtotal
        # Ref: 1costingfe installation_frac = 0.14
        reactor_sub = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"])
        r["C220111"] = 0.14 * reactor_sub

        # C220112: Isotope separation — zero (no Li-6 enrichment, no tritium)
        r["C220112"] = 0.0

        # Per-module subtotal
        r["CAS22_per_module"] = reactor_sub + r["C220111"] + r["C220112"]

        # ---- Plant-wide accounts ----
        p_net_plant = max(power["p_net_plant"], 1.0)
        p_th_plant = max(power["p_th_plant"], 1.0)

        # C220200: Main coolant / steam circuit (Branch B) or minimal heat dump (Branch C)
        if self.use_icc:
            # ICC: small waste heat circuit only (magnet cooling + residual)
            r["C220200"] = 20.0 * (p_net_plant / 1000.0)
        else:
            # Steam Rankine primary + secondary circuit
            C220201 = 166.0 * (p_net_plant / 1000.0)
            C220202 = 40.6 * (p_th_plant / 3500.0) ** 0.55
            r["C220200"] = C220201 + C220202

        # C220300: Auxiliary cooling — no cryoplant (copper magnets, no HTS)
        r["C220300"] = 1.1e-3 * p_th_plant    # aux coolant only

        # C220400: Radioactive waste management — minimal (aneutronic, ~10% DT)
        r["C220400"] = 1.96 * (p_th_plant / 1000.0) * 0.10

        # C220500: Fuel handling — boron injection system (not tritium handling)
        # 1costingfe fuel_handling_pb11_base = 15 M$/GWe ref, ^0.7 scaling
        r["C220500"] = 15.0 * (p_net_plant / 1000.0) ** 0.7

        # C220600: Other reactor plant equipment
        r["C220600"] = 11.5 * (p_net_plant / 1000.0) ** 0.8

        # C220700: Instrumentation and control
        r["C220700"] = 85.0 * (p_th_plant / 3500.0) ** 0.65

        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        r["CAS22"] = r["CAS22_per_module"] * self.n_mod + r["CAS22_plant_wide"]
        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: CAS10-60 capital cost accounting."""
        r = {}
        p_et = max(power["p_et"], 1.0)
        p_th = max(power["p_th"], 1.0)
        p_net_plant = max(power["p_net_plant"], 1.0)

        # === CAS10: Pre-construction ===
        # p-B11: licensing_cost_pb11 = 0.1 M$ (no NRC jurisdiction for aneutronic)
        # Ref: 1costingfe costing_constants.yaml licensing_cost_pb11
        land_cost = 0.25 * p_net_plant * 10_000.0 / 1e6   # 0.25 acres/MWe × $10k/acre
        r["CAS10"] = 3.0 + 20.0 + 2.0 + 1.0 + 1.0 + land_cost + 0.1  # FOAK studies

        # === CAS21: Buildings ===
        # 1costingfe pb11 total: $308/kW at 1 GWe net reference
        # Scaled to plant net electric. No hot cell (aneutronic, no activation).
        # Turbine building proportional adjustment: Steam +$58/kW, ICC replaced by
        # ICC power conditioning hall (similar cost, use same base).
        building_per_kw_pb11 = 308.0  # $/kW at 1 GWe reference
        r["CAS21"] = building_per_kw_pb11 * p_net_plant / 1000.0  # M$

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment (steam) or ICC power conditioning ===
        if self.use_icc:
            # ICC grid-tie inverter + power conditioning
            # Ref: 1costingfe c_inv_per_kw_net = 150 $/kW → 0.15 M$/MW net
            r["CAS23"] = 0.15 * p_net_plant
        else:
            # Standard steam turbine-generator: 0.19764 M$/MW gross
            r["CAS23"] = self.n_mod * p_et * 0.19764

        # === CAS24: Electric Plant Equipment ===
        r["CAS24"] = self.n_mod * p_et * 0.08418

        # === CAS25: Miscellaneous Plant Equipment ===
        r["CAS25"] = self.n_mod * p_et * 0.05124

        # === CAS26: Heat Rejection ===
        if self.use_icc:
            # ICC: heat rejection only for recirculating power waste heat
            r["CAS26"] = self.n_mod * p_net_plant * 0.01
        else:
            r["CAS26"] = self.n_mod * p_et * 0.03416

        # === CAS27: Special Materials — zero for p-B11 ===
        # 1costingfe special_materials_pb11 = 0.0 (no PbLi, no FLiBe, no Be)
        r["CAS27"] = 0.0

        # === CAS28: Digital Twin ===
        # Ref: 1costingfe digital_twin = 5.0 M$ (fixed)
        r["CAS28"] = 5.0

        # === CAS29: Contingency ===
        # FOAK: 10% of direct costs. NOAK: 0%.
        # Ref: 1costingfe contingency_rate_foak = 0.10
        cas20_sub = sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                        "CAS25", "CAS26", "CAS27", "CAS28"])
        contingency_rate = 0.0 if self.noak else 0.10
        r["CAS29"] = contingency_rate * cas20_sub

        # === CAS20: Total Direct Costs ===
        r["CAS20"] = cas20_sub + r["CAS29"]

        # === CAS30: Indirect Costs ===
        # 20% × CAS20 × (construction_time / 6yr reference)
        # Ref: 1costingfe indirect_fraction = 0.20, reference_construction_time = 6.0
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / 6.0)

        # === CAS40: Owner's Costs ===
        # 1costingfe owner_cost_pb11 = 20.0 M$ at 1 GWe, ^0.5 scaling
        r["CAS40"] = 20.0 * (p_net_plant / P_NET_REF) ** 0.5

        # === CAS50: Supplementary Costs ===
        shipping = 0.015 * r["CAS20"]                   # 1costingfe shipping_frac
        spare_parts = 0.01 * sum(r[k] for k in          # 1costingfe spare_parts_frac_pb11
                                  ["CAS22", "CAS23", "CAS24", "CAS25", "CAS26",
                                   "CAS27", "CAS28"])
        startup_fuel = 0.1 * (p_net_plant / P_NET_REF)  # 1costingfe startup_fuel_pb11
        taxes = 0.01 * r["CAS20"]                        # 1costingfe tax_frac
        insurance = 0.015 * (r["CAS20"] + r["CAS30"])   # 1costingfe construction_insurance_frac
        # Decommissioning: 1costingfe decom_provision_pb11 = 53 M$/GWe, ^0.5 scaling
        decom = 53.0 * (p_net_plant / P_NET_REF) ** 0.5
        r["CAS50"] = shipping + spare_parts + startup_fuel + taxes + insurance + decom

        # === Overnight Capital ===
        r["overnight_capital"] = (r["CAS10"] + r["CAS20"] + r["CAS30"]
                                   + r["CAS40"] + r["CAS50"])

        # === CAS60: Interest During Construction (IDC) ===
        i = self.interest_rate
        T = self.construction_time_years
        f_idc = ((1 + i) ** T - 1) / (i * T) - 1 if (i > 0 and T > 0) else 0.0
        r["CAS60"] = f_idc * r["overnight_capital"]
        r["f_IDC"] = f_idc

        # === Total Capital ===
        r["total_capital"] = r["overnight_capital"] + r["CAS60"]

        if power["p_net_plant"] > 0:
            r["specific_capital_USD_per_kWe"] = (
                r["total_capital"] * 1e6 / (power["p_net_plant"] * 1e3))
        else:
            r["specific_capital_USD_per_kWe"] = float("inf")

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70-90 annualized costs and LCOE."""
        r = {}
        p_net_plant = max(power["p_net_plant"], 1.0)

        # Capital Recovery Factor
        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1 + i) ** n / ((1 + i) ** n - 1)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]   # M$/yr

        # === CAS71: Annual O&M (levelized with inflation) ===
        # 1costingfe: om_cost_pb11 = 24.0 M$/yr at 1 GWe, (P_net/1GWe)^0.5 scaling.
        # NBI maintenance dominates: neutral sources, gas cells, power supply service.
        annual_om_base = 24.0 * (p_net_plant / P_NET_REF) ** 0.5   # M$/yr
        g = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g) ** Tc
        if abs(i - g) > 1e-10:
            pv_om = A1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
        else:
            pv_om = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_om   # M$/yr

        # === CAS72: Scheduled Replacement (first wall / X-ray absorber) ===
        eff_yrs = self.core_lifetime_FPY / self.plant_availability
        n_repl = max(0, int(math.ceil(self.plant_lifetime_years / eff_yrs)) - 1)
        repl_cost = cas22["C220101"]   # first-wall replacement cost
        pv_repl = sum(repl_cost / (1 + i) ** (k * eff_yrs)
                      for k in range(1, n_repl + 1)
                      if k * eff_yrs < self.plant_lifetime_years)
        r["CAS72"] = crf * pv_repl
        r["n_fw_replacements"] = n_repl

        r["CAS70"] = r["CAS71"] + r["CAS72"]   # M$/yr

        # === CAS80: Fuel costs (B-11 + protium) ===
        # B-11 mass burn rate from fusion power:
        #   E_per_reaction = 8.7e6 eV × 1.602e-19 J/eV = 1.394e-12 J
        #   Mass per reaction = 11 amu × 1.66e-27 kg/amu = 1.826e-26 kg (B-11)
        #   burn_rate [kg/s] = P_fus [W] / E_per_reaction × mass_per_reaction
        p_fus_plant = max(power["p_fus"] * self.n_mod, 1.0)
        b11_burn_rate_kg_s = (p_fus_plant * 1e6 / 1.394e-12) * 1.826e-26
        # Gross B-11 fed (accounting for 5% burn fraction, 95% recovery):
        # Annual gross B-11 = burn_rate / burn_fraction × availability × 3600×8760
        annual_b11_kg = (b11_burn_rate_kg_s / 0.05
                         * self.plant_availability * 3600 * 8760)
        annual_b11_cost_M = annual_b11_kg * self.u_b11_per_kg / 1e6
        r["CAS80"] = annual_b11_cost_M + 0.01   # add negligible H fuel cost
        r["CAS80_b11_kg_yr"] = annual_b11_kg
        r["CAS80_b11_cost_M"] = annual_b11_cost_M

        # === LCOE ===
        annual_rev_req = r["CAS90"] + r["CAS70"] + r["CAS80"]   # M$/yr
        r["annual_revenue_req"] = annual_rev_req
        annual_energy_MWh = 8760.0 * p_net_plant * self.plant_availability
        r["annual_energy_MWh"] = annual_energy_MWh

        if annual_energy_MWh > 0 and power["p_net_plant"] > 0:
            lcoe = annual_rev_req * 1e6 / annual_energy_MWh
            r["lcoe_USD_per_MWh"] = lcoe
            r["lcoe_cents_per_kWh"] = lcoe / 10.0
        else:
            r["lcoe_USD_per_MWh"] = float("inf")
            r["lcoe_cents_per_kWh"] = float("inf")

        if annual_rev_req > 0:
            r["capital_fraction"] = r["CAS90"] / annual_rev_req
            r["om_fraction"] = r["CAS70"] / annual_rev_req
            r["fuel_fraction"] = r["CAS80"] / annual_rev_req

        return r

    def compute(self) -> dict:
        """Run all five layers and return a unified results dict.

        Required keys for cross-concept extractor:
          power:     p_fus, p_th, p_et, p_net, Q_eng, Q_sci, recirc_fraction
                     p_net_plant, p_et_plant, p_th_plant  (multi-module)
          cas22:     C220101–C220112, C220200–C220700
          costs:     CAS10–CAS60, CAS20, total_capital, overnight_capital
          economics: CAS70, CAS71, CAS72, CAS80, CAS90, lcoe_USD_per_MWh
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


# ============================================================
#  Module-level interface (required by concept explorer)
# ============================================================

params = PB11FRCPlantParams()
results = params.compute()

# Economy-of-scale scaling to 1000 MWe cross-concept reference
# α = 0.6: standard engineering economy-of-scale exponent
_ALPHA = 0.6
_p_native = results["power"].get("p_net_plant", results["power"]["p_net"])
_factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)
_overnight_per_kw = results["costs"]["overnight_capital"] * 1e3 / max(_p_native, 1.0)

scaled_headline = {
    "p_net_mw": 1000.0,
    "lcoe_per_mwh": results["economics"]["lcoe_USD_per_MWh"] * _factor,
    "overnight_per_kw": _overnight_per_kw * _factor,
}


# ============================================================
#  Output functions
# ============================================================

def print_results(p: PB11FRCPlantParams, r: dict, label: str = ""):
    """Pretty-print LCOE model results with full CAS breakdown."""
    pw = r["power"]
    c22 = r["cas22"]
    co = r["costs"]
    ec = r["economics"]

    branch = pw["branch"]
    branch_labels = {
        "A": "BRANCH A — Physics Fails (no net electricity)",
        "B": "BRANCH B — Da Vinci Baseline (steam Rankine, ~32% η)",
        "C": "BRANCH C — ICC Upgrade (direct conversion, ~90% η)",
    }

    title = f"p-B11 FRC (TAE Da Vinci) LCOE Model"
    if label:
        title = f"{title} — {label}"

    print("=" * 70)
    print(title)
    print(branch_labels.get(branch, f"Branch {branch}"))
    print("=" * 70)

    # --- Key Inputs ---
    print(f"\n--- Key Input Parameters ---")
    print(f"  Q_plasma:                   {p.q_plasma:.1f}  "
          f"(breakeven: {pw['q_plasma_breakeven']:.1f},"
          f" commercial min: {pw['q_plasma_commercial_min']:.1f})")
    print(f"  P_NBI plasma:               {p.p_nbi_plasma_MW:.1f} MW")
    print(f"  NBI wall-plug efficiency:   {p.eta_nbi:.0%}")
    print(f"  Energy conversion:          {'ICC %.0f%%' % (p.eta_icc * 100) if p.use_icc else 'Steam %.0f%%' % (p.eta_th * 100)}")
    print(f"  Radiation loss fraction:    {p.f_rad:.0%}")
    print(f"  Capacity factor:            {p.plant_availability:.0%}")
    print(f"  Plant lifetime:             {p.plant_lifetime_years:.0f} yr")
    print(f"  Interest rate:              {p.interest_rate:.0%}")
    print(f"  FOAK/NOAK:                  {'NOAK' if p.noak else 'FOAK'}")

    # --- Physics Viability ---
    if not pw["viable"]:
        print(f"\n  ╔══════════════════════════════════════════════════════╗")
        print(f"  ║  BRANCH A: Q_plasma = {p.q_plasma:.1f} < breakeven {pw['q_plasma_breakeven']:.1f}           ║")
        print(f"  ║  Net electricity: {pw['p_net']:.1f} MWe (NEGATIVE)              ║")
        print(f"  ║  No LCOE — concept does not produce net energy.      ║")
        print(f"  ╚══════════════════════════════════════════════════════╝")
        return

    # --- Power Balance ---
    print(f"\n--- Power Balance (per module) ---")
    print(f"  P_NBI wall-plug draw:       {pw['p_nbi_wall_MW']:.1f} MW  "
          f"(recirculating load)")
    print(f"  P_fusion:                   {pw['p_fus']:.1f} MW")
    print(f"    All in charged alphas:    {pw['p_alpha']:.1f} MW  (aneutronic)")
    print(f"    Radiation losses ({p.f_rad:.0%}):  {pw['p_fus'] * p.f_rad:.1f} MW")
    print(f"  P_available (post-rad):     {pw['p_th']:.1f} MW")
    print(f"  Gross electric:             {pw['p_et']:.1f} MWe  "
          f"(η_conv = {pw['eta_conv_used']:.0%})")
    print(f"  Recirculating loads:")
    print(f"    NBI wall-plug:            {pw['p_nbi_wall_MW']:.1f} MW")
    print(f"    Auxiliaries:              {pw['p_aux']:.1f} MW  "
          f"(magnets + housekeeping + fuel inject)")
    print(f"  Net electric (per module):  {pw['p_net']:.1f} MWe")
    print(f"  Net electric (plant):       {pw['p_net_plant']:.1f} MWe  ({p.n_mod} module(s))")
    print(f"  Q_sci (plasma):             {pw['Q_sci']:.1f}")
    print(f"  Q_eng (net/NBI_wall):       {pw['Q_eng']:.2f}")
    print(f"  Recirculating fraction:     {pw['recirc_fraction']:.1%}")

    # --- CAS22: Reactor Plant Equipment ---
    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    cas22_labels = {
        "C220101": ("X-ray absorber / first wall",    ""),
        "C220102": ("Shield (thin, aneutronic)",       ""),
        "C220103": ("Copper coils (override)",         " [override]"),
        "C220104": ("NBI system (override)",           " [override — dominant]"),
        "C220105": ("Primary structure",               ""),
        "C220106": ("Vacuum system",                   ""),
        "C220107": ("Power supplies",                  ""),
        "C220108": ("Target factory",                  ""),
        "C220109": ("ICC direct converter",            " [Branch C only]"),
        "C220110": ("Remote handling (minimal)",       ""),
        "C220111": ("Installation labor",              ""),
        "C220112": ("Isotope separation",              ""),
    }
    print(f"  Per-module accounts:")
    for code, (lbl, note) in cas22_labels.items():
        val = c22.get(code, 0.0)
        if val > 0.01:
            print(f"    {code} {lbl:<32s} ${val:>8.1f}M{note}")
    print(f"    {'─' * 52}")
    print(f"    Per-module subtotal:                  ${c22['CAS22_per_module']:>8.1f}M × {p.n_mod}")

    print(f"  Plant-wide accounts:")
    pw_labels = {
        "C220200": "Coolant systems",
        "C220300": "Aux cooling (no cryoplant)",
        "C220400": "Rad waste management (minimal)",
        "C220500": "Fuel handling (boron, not T)",
        "C220600": "Other equipment",
        "C220700": "Instrumentation & control",
    }
    for code, lbl in pw_labels.items():
        val = c22.get(code, 0.0)
        if val > 0.01:
            print(f"    {code} {lbl:<32s} ${val:>8.1f}M")
    print(f"    {'─' * 52}")
    print(f"    Plant-wide subtotal:                  ${c22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                            ${c22['CAS22']:>8.1f}M")

    # --- Capital Costs ---
    print(f"\n--- Capital Costs (CAS10-60) ---")
    for code, lbl in [
        ("CAS10", "Pre-construction"),
        ("CAS21", "Buildings"),
        ("CAS22", "Reactor Plant Equipment"),
        ("CAS23", "Turbine/ICC Plant"),
        ("CAS24", "Electric Plant"),
        ("CAS25", "Misc Plant"),
        ("CAS26", "Heat Rejection"),
        ("CAS28", "Digital Twin"),
        ("CAS29", "Contingency (FOAK 10%)"),
    ]:
        val = co.get(code, 0.0)
        print(f"  {code} {lbl:<36s} ${val:>8.1f}M")
    print(f"  {'─' * 58}")
    print(f"  CAS20 Direct Costs:                     ${co['CAS20']:>8.1f}M")
    print(f"  CAS30 Indirect Costs:                   ${co['CAS30']:>8.1f}M")
    print(f"  CAS40 Owner's Costs:                    ${co['CAS40']:>8.1f}M")
    print(f"  CAS50 Supplementary:                    ${co['CAS50']:>8.1f}M")
    print(f"  {'─' * 58}")
    print(f"  Overnight Capital:                      ${co['overnight_capital']:>8.1f}M")
    print(f"  CAS60 IDC (f={co['f_IDC']:.3f}):               ${co['CAS60']:>8.1f}M")
    print(f"  ══════════════════════════════════════════════════════════")
    print(f"  Total Capital:                          ${co['total_capital']:>8.1f}M")
    print(f"  Specific Capital:                       ${co['specific_capital_USD_per_kWe']:>8.0f} $/kWe")

    # --- Annual Costs ---
    print(f"\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90 Capital charge (CRF={ec['CRF']:.4f}):   ${ec['CAS90']:>8.1f}M/yr")
    print(f"  CAS71 O&M (levelized):                  ${ec['CAS71']:>8.1f}M/yr")
    print(f"  CAS72 First-wall replacement:           ${ec['CAS72']:>8.2f}M/yr  "
          f"({ec['n_fw_replacements']} replacements)")
    print(f"  CAS70 Total O&M:                        ${ec['CAS70']:>8.1f}M/yr")
    print(f"  CAS80 Fuel (B-11):                      ${ec['CAS80']:>8.2f}M/yr  "
          f"({ec['CAS80_b11_kg_yr']:.0f} kg B-11/yr)")

    # --- LCOE ---
    print(f"\n--- LCOE ---")
    print(f"  Annual energy:              {ec['annual_energy_MWh']:,.0f} MWh")
    print(f"  Annual revenue requirement: ${ec['annual_revenue_req']:.1f}M")
    print(f"  ╔══════════════════════════════════════╗")
    lcoe_mwh = ec["lcoe_USD_per_MWh"]
    lcoe_ckwh = ec["lcoe_cents_per_kWh"]
    print(f"  ║  LCOE = {lcoe_ckwh:6.1f} ¢/kWh              ║")
    print(f"  ║       = {lcoe_mwh:6.1f} $/MWh               ║")
    print(f"  ╚══════════════════════════════════════╝")
    print(f"  Capital (CAS90):            {ec.get('capital_fraction', 0):.1%}")
    print(f"  O&M (CAS70):               {ec.get('om_fraction', 0):.1%}")
    print(f"  Fuel (CAS80):               {ec.get('fuel_fraction', 0):.2%}")

    # --- Economy-of-scale headline at 1000 MWe ---
    _p_nat = r["power"].get("p_net_plant", r["power"]["p_net"])
    if _p_nat > 0 and _p_nat < 900.0:
        _fac = (_p_nat / 1000.0) ** (1.0 - _ALPHA)
        _lcoe_1gwe = lcoe_mwh * _fac
        _oc_kw = co["overnight_capital"] * 1e3 / _p_nat * _fac
        print(f"\n  Economy-of-scale projection to 1000 MWe (α=0.6):")
        print(f"    Scaled LCOE:              {_lcoe_1gwe:.1f} $/MWh")
        print(f"    Scaled overnight $/kWe:   ${_oc_kw:.0f} /kWe")


def sensitivity_sweep(base_p: PB11FRCPlantParams, param_name: str,
                       values: list, label: str = "") -> list:
    """Sweep a single parameter and return LCOE/P_net for each value."""
    out = []
    for val in values:
        kwargs = {**base_p.__dict__, param_name: val}
        p_new = PB11FRCPlantParams(**kwargs)
        r_new = p_new.compute()
        pw = r_new["power"]
        ec = r_new["economics"]
        out.append({
            "param_value": float(val) if not isinstance(val, bool) else val,
            "p_net_MW": pw["p_net_plant"],
            "lcoe_USD_MWh": ec["lcoe_USD_per_MWh"],
            "lcoe_cents_kWh": ec["lcoe_cents_per_kWh"],
            "branch": pw["branch"],
            "recirc_fraction": pw["recirc_fraction"],
        })
    return out


def _lcoe_str(row: dict) -> str:
    if row["branch"] == "A":
        return f"  N/A (Branch A, P_net={row['p_net_MW']:.1f} MWe)"
    elif row["lcoe_USD_MWh"] == float("inf"):
        return "  ∞"
    else:
        return f"  {row['lcoe_cents_kWh']:5.1f} ¢/kWh  ({row['lcoe_USD_MWh']:.0f} $/MWh)  P_net={row['p_net_MW']:.1f} MWe"


def main():
    print("\n" + "#" * 70)
    print("# p-B11 FRC (TAE Da Vinci) — Free-Form LCOE Model")
    print("# Physics-first: viability boundary × scenario branches")
    print("#" * 70)

    # ----------------------------------------------------------------
    # Physics viability preamble
    # ----------------------------------------------------------------
    print("\n" + "=" * 70)
    print("PHYSICS VIABILITY ANALYSIS")
    print("=" * 70)
    print("""
The p-B11 fusion reaction requires ion temperatures ~150–300 keV —
~80× above the C-2W/Norman record of ~3 keV total temperature.
Q_plasma > 1 has never been demonstrated for p-B11 in ANY confinement device.

Mathematical Q_plasma breakeven (rated power, ignoring auxiliaries):
  Q_break = 1 / [(1 − f_rad) × η_conv × η_NBI]

  Branch B (steam, f_rad=0.15, η_th=0.32, η_NBI=0.55):  Q_break ≈ 6.7
  Branch B (steam, f_rad=0.15, η_th=0.32, η_NBI=0.40):  Q_break ≈ 9.2
  Branch C (ICC,   f_rad=0.15, η_icc=0.90, η_NBI=0.55): Q_break ≈ 2.4

Commercial minimum (with 50 MWe margin and auxiliaries):
  Branch B, η_NBI=0.55:  Q_plasma ≥ 10–15
  Branch B, η_NBI=0.40:  Q_plasma ≥ 20–25

COMPOUNDING PENALTY (Mulder et al. arXiv:2103.12451):
  At sub-unity capacity factor, NBI must remain at ~full power for FRC
  stability. Effective recirculating fraction rises above rated-power
  calculation. Capacity factor and Q_plasma interact multiplicatively.
  Early Da Vinci (undemonstrated CW FRC) may operate at CF 60–75%,
  raising the effective Q_plasma requirement above the values above.

Three model branches:
  A — Physics fails (Q_plasma < threshold): no LCOE output.
  B — Da Vinci steam baseline (Q threshold met, ~32% η).
  C — ICC upgrade (Q threshold met, ~90% η): long-term economic vision.
""")

    # ----------------------------------------------------------------
    # Branch B baseline
    # ----------------------------------------------------------------
    print("\n" + "#" * 70)
    print("# BRANCH B BASELINE: Q=15, η_NBI=0.55, CF=85%, Steam 32%")
    print("#" * 70)
    p_b_baseline = PB11FRCPlantParams()
    r_b_baseline = p_b_baseline.compute()
    print_results(p_b_baseline, r_b_baseline, "Branch B Baseline")

    # ----------------------------------------------------------------
    # Branch C: ICC upgrade (same physics, higher conversion)
    # ----------------------------------------------------------------
    print("\n" + "#" * 70)
    print("# BRANCH C: Q=15, η_NBI=0.55, CF=85%, ICC 90%")
    print("#" * 70)
    p_c_base = PB11FRCPlantParams(use_icc=True)
    r_c_base = p_c_base.compute()
    print_results(p_c_base, r_c_base, "Branch C — ICC Upgrade")

    # ----------------------------------------------------------------
    # Sensitivity sweeps
    # ----------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SENSITIVITY SWEEPS (from Branch B baseline)")
    print("=" * 70)

    # 1. Q_plasma — primary viability axis
    print(f"\n--- 1. Q_plasma sweep (most critical parameter) ---")
    print(f"  Q_break ≈ 6.7 (steam, η_NBI=0.55); commercial min ≈ 10")
    print(f"  {'Q_plasma':>10}  {'Result'}")
    q_values = [3.0, 5.0, 6.7, 8.0, 10.0, 12.0, 15.0, 20.0, 30.0, 50.0]
    for row in sensitivity_sweep(p_b_baseline, "q_plasma", q_values):
        flag = " *** BREAKEVEN" if abs(row["param_value"] - 6.7) < 0.4 else ""
        flag = " *** COMMERCIAL MIN" if abs(row["param_value"] - 10.0) < 0.1 else flag
        print(f"  {row['param_value']:>10.1f}  {_lcoe_str(row)}{flag}")

    # 2. NBI wall-plug efficiency
    print(f"\n--- 2. NBI wall-plug efficiency sweep ---")
    print(f"  {'η_NBI':>10}  {'Result'}")
    for row in sensitivity_sweep(p_b_baseline, "eta_nbi",
                                  [0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65]):
        print(f"  {row['param_value']:>10.2f}  {_lcoe_str(row)}")

    # 3. Capacity factor (interacts with NBI recirculating power)
    print(f"\n--- 3. Capacity factor sweep (NBI recirculating interaction) ---")
    print(f"  Note: NBI stays at full power even at reduced CF → effective")
    print(f"  recirculating fraction is constant; only energy output falls.")
    print(f"  {'CF':>10}  {'Result'}")
    for row in sensitivity_sweep(p_b_baseline, "plant_availability",
                                  [0.50, 0.60, 0.70, 0.75, 0.85, 0.90, 0.95]):
        print(f"  {row['param_value']:>10.0%}  {_lcoe_str(row)}")

    # 4. NBI capital cost (dominant capital uncertainty)
    print(f"\n--- 4. NBI capital cost [M$/MW_NBI] sweep ---")
    print(f"  {'NBI $/MW':>10}  {'Result'}")
    for row in sensitivity_sweep(p_b_baseline, "nbi_cost_per_MW_M_USD",
                                  [3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 30.0]):
        print(f"  {row['param_value']:>10.1f}  {_lcoe_str(row)}")

    # 5. Thermal efficiency (steam Rankine)
    print(f"\n--- 5. Thermal efficiency sweep (Branch B only) ---")
    print(f"  {'η_th':>10}  {'Result'}")
    for row in sensitivity_sweep(p_b_baseline, "eta_th",
                                  [0.25, 0.28, 0.30, 0.32, 0.35, 0.38, 0.40]):
        print(f"  {row['param_value']:>10.0%}  {_lcoe_str(row)}")

    # 6. NBI plasma power (plant sizing)
    print(f"\n--- 6. NBI plasma power [MW] sweep (plant sizing) ---")
    print(f"  {'P_NBI MW':>10}  {'Result'}")
    for row in sensitivity_sweep(p_b_baseline, "p_nbi_plasma_MW",
                                  [15.0, 20.0, 26.0, 35.0, 50.0, 75.0, 100.0]):
        print(f"  {row['param_value']:>10.1f}  {_lcoe_str(row)}")

    # 7. Q_plasma vs η_NBI viability grid
    print(f"\n--- 7. Q_plasma × η_NBI viability boundary grid ---")
    print(f"  (Branch A = no net electricity; B = viable steam; C = ICC)")
    q_grid = [5, 8, 10, 15, 20, 30]
    nbi_grid = [0.40, 0.45, 0.50, 0.55, 0.60, 0.65]
    header = f"  {'Q\\η_NBI':>10}" + "".join(f"  {n:.2f}" for n in nbi_grid)
    print(header)
    for q in q_grid:
        row_str = f"  {'Q='+str(q):>10}"
        for n in nbi_grid:
            kw = {**p_b_baseline.__dict__, "q_plasma": float(q), "eta_nbi": n}
            pw2 = PB11FRCPlantParams(**kw).compute()["power"]
            if pw2["branch"] == "A":
                row_str += "     A  "
            else:
                lc = PB11FRCPlantParams(**kw).compute()["economics"]["lcoe_cents_per_kWh"]
                row_str += f" {lc:5.0f}¢ "
        print(row_str)
    print(f"  (values in ¢/kWh; A = Branch A, no LCOE)")

    # ----------------------------------------------------------------
    # Scenario comparison table
    # ----------------------------------------------------------------
    print("\n\n" + "=" * 70)
    print("SCENARIO COMPARISON TABLE")
    print("=" * 70)
    print(f"{'Scenario':<38} {'Q':>5} {'η_NBI':>6} {'CF':>5} {'P_net':>7} {'LCOE':>14}")
    print("-" * 75)

    scenarios = [
        ("Branch A — Physics fails (Q=3)",
         PB11FRCPlantParams(q_plasma=3.0)),
        ("B Conservative (Q=10, η=0.50, CF=70%)",
         PB11FRCPlantParams(q_plasma=10.0, eta_nbi=0.50, plant_availability=0.70)),
        ("B Baseline (Q=15, η=0.55, CF=85%)",
         PB11FRCPlantParams()),
        ("B Optimistic (Q=25, η=0.60, CF=90%)",
         PB11FRCPlantParams(q_plasma=25.0, eta_nbi=0.60, plant_availability=0.90)),
        ("C Baseline — ICC (Q=15, η=0.55, CF=85%)",
         PB11FRCPlantParams(use_icc=True)),
        ("C Optimistic — ICC (Q=25, η=0.60, CF=90%)",
         PB11FRCPlantParams(q_plasma=25.0, eta_nbi=0.60,
                             plant_availability=0.90, use_icc=True)),
    ]

    for name, sp in scenarios:
        sr = sp.compute()
        pw2 = sr["power"]
        ec2 = sr["economics"]
        p_net_str = f"{pw2['p_net_plant']:.0f} MWe"
        if pw2["branch"] == "A":
            lcoe_str2 = "N/A (no net power)"
        else:
            lcoe_str2 = f"{ec2['lcoe_cents_per_kWh']:.1f} ¢/kWh"
        print(f"  {name:<36} {sp.q_plasma:>5.0f} {sp.eta_nbi:>6.2f} "
              f"{sp.plant_availability:>5.0%} {p_net_str:>7} {lcoe_str2:>14}")

    # ----------------------------------------------------------------
    # Key Binding Constraints
    # ----------------------------------------------------------------
    print(f"\n\n{'=' * 70}")
    print("KEY BINDING CONSTRAINTS (top 3 LCOE drivers)")
    print("=" * 70)
    print("""
  1. Q_PLASMA — The fundamental physics unknown (binding constraint)
     Q_plasma > 1 has never been demonstrated for p-B11 in any device.
     C-2W/Norman achieved ~3 keV total temperature; Da Vinci requires ~250 keV
     — an ~80× extrapolation with no validated scaling law. Q_plasma is not
     just the top sensitivity parameter: it determines whether the concept
     produces ANY net electricity. Below Q ≈ 6.7 (steam, η_NBI=0.55), there
     is no LCOE — Branch A has no meaningful cost model output.
     Status: Copernicus (unbuilt) is the intended intermediate-scale validation.
     Resolution timeline: unknown; no published Copernicus parameters.

  2. NBI CAPITAL COST & RECIRCULATING POWER FRACTION (jointly binding)
     NBI is the dominant capital account (C220104 ≈ $260M at $10M/MW × 26 MW).
     It is also the dominant recirculating load (~49 MW wall-plug at baseline).
     These two effects reinforce: high NBI cost → high capital LCOE component;
     high NBI recirculating load → low net output → high LCOE denominator.
     At $10M/MW_NBI, NBI accounts for >50% of CAS22. At $20M/MW, it exceeds
     total remaining plant cost. No commercial supply chain exists for fusion-
     scale high-energy NBI; cost is extrapolated from research-scale systems.
     Compounding: at CF < 85%, NBI stays at full power but plant output drops,
     raising the effective recirc fraction [arxiv-2103-12451.md].

  3. ENERGY CONVERSION ARCHITECTURE — ICC vs. Steam (structural LCOE gap)
     Da Vinci's steam baseline (~32%) vs. ICC target (~90%) represents a ~3×
     difference in gross electricity from identical fusion power. This single
     architectural choice changes Branch B LCOE from ~$200/MWh to Branch C
     LCOE ~$40/MWh (at Q=15 baseline). ICC is patent-stage only — zero
     experimental demonstration at MeV-range fusion product energies.
     The near-term Da Vinci plant cannot realize the core economic advantage
     of the aneutronic fuel choice (direct conversion) — it pays the capital
     cost of an aneutronic system but achieves only steam cycle efficiency.
     Insight: p-B11 FRC LCOE is only competitive if BOTH the physics (Q_plasma
     threshold) AND the ICC technology succeed. Steam-only p-B11 FRC is
     economically inferior to any D-T concept with equivalent Q_plasma.
""")

    print("\nNOTE: All estimates carry HIGH UNCERTAINTY. This model is intended")
    print("for physics-viability and scenario boundary mapping only.")
    print("Six blocking data gaps exist (analysis.md §Section 6); this model")
    print("uses assumed / analogized values for all key physics parameters.")


if __name__ == "__main__":
    main()
