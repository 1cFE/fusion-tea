"""
Dense Plasma Focus p-B11 (LPPFusion) — Free-Form LCOE Model
============================================================
1cFE First Pass Concept Analysis
Concept: Dense Plasma Focus (DPF) with p-B11 aneutronic fuel
Company: LPPFusion (Eric Lerner et al.)

CRITICAL CAVEAT: This model is conditional on a 120,000× fusion yield improvement
from LPPFusion's current 0.25 J/shot (deuterium) to the 30 kJ net energy target
(p-B11). Every physics and engineering parameter in this model is aspirational.
No credible LCOE can be assigned until net energy is demonstrated experimentally.

Physics notes:
  - p-B11 reaction: p + ¹¹B → 3⁴He + 8.68 MeV (aneutronic; all energy in charged particles)
  - Energy conversion: ion beam decelerator + X-ray photoelectric converter (no thermal cycle)
  - Quantum Magnetic Field (QMF) effect required to suppress bremsstrahlung losses
  - DPF geometry: self-pinching Z-pinch plasmoid (~4 m × 4 m footprint, ~3 ton device)
  - Device cost claimed: $500K/module NOAK (mass production, $0.10/W)
  - Claimed LCOE: 0.3 ¢/kWh (combines capital + maintenance, all assumptions undemonstrated)

Cost accounting follows the CAS (Code of Accounts System) structure used in 1costingfe,
with DPF-specific overrides for the unique direct energy conversion path and modular
device architecture. Plant-level model: n_mod modules × 5 MWe/module ≈ 1 GWe plant.

Power standardization (cross-concept comparison at 1000 MWe reference):
  The native power of this model is p_net_plant = n_mod × p_net_per_module.
  Post-hoc scaling to 1000 MWe uses economy-of-scale exponent α = 0.6:
    LCOE_1000 = LCOE_native × (p_native / 1000)^(1 − α)
  Since native power ≈ 1000 MWe (200 modules × 5 MW), scaling factor ≈ 1.

Key references:
  - Lerner et al. (2023) J. Fusion Energy 42:7  — device specs, energy conversion, cost claims
  - Lerner et al. (2024) Frontiers in Physics   — FF-2B specs, p-B11 preparations
  - LPPFusion (2024) "Our Plan to Net Energy"  — yield targets, rep rate, net output targets
  - LPPFusion (2024) "Executive Summary"        — $500K/device, 0.3 ¢/kWh claim
  - 1costingfe costing_constants.yaml           — CAS scaling laws (p-B11 fuel type used)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math
from dataclasses import dataclass


# === Reference power levels for 1costingfe scaling laws ===
P_TH_REF = 2500.0    # Reference thermal power [MW]
P_ET_REF = 1100.0    # Reference gross electric power [MW]


@dataclass
class DPFPlantParams:
    """
    Parameterized Dense Plasma Focus (p-B11) power plant model.

    Uncertainty tags on parameters:
      (none)               = well-established value with published source
      MODERATE UNCERTAINTY = reasonable estimate from analogues
      HIGH UNCERTAINTY     = speculative or poorly constrained
      ASSUMED              = no data available; analogue or first-principles estimate
    """

    # === DRIVER: CAPACITOR BANK ===

    e_stored_kJ: float = 115.0
    """Stored electrical energy per shot in capacitor bank [kJ].
    Source: FF-2B full 12-capacitor bank, 113 μF total, 45 kV maximum charge.
    Ref: lerner-2023-jfe-paper.md §Experimental Device;
         lerner-2024-frontiers-pB11-prep.md §Introduction.
    NOTE: Commercial design may need higher stored energy for QMF regime;
    current device operated at this specification."""

    driver_coupling_eff: float = 0.85
    """Fraction of stored energy coupled into the Z-pinch plasma [dimensionless].
    Source: Typical low-inductance DPF coupling efficiency; residual losses in
    spark-gap switches (~2%), transmission inductance, return-current path.
    Ref: DPF engineering literature analogy. MODERATE UNCERTAINTY."""

    Q_sci: float = 1.72
    """Scientific gain = fusion energy yield / energy coupled to plasma [dimensionless].
    Back-derived: for 25 kJ net electrical output per shot at 115 kJ stored energy,
    combined direct conversion efficiency = (0.70×0.85 + 0.30×0.80) = 0.835 requires
    E_fus = (25 + 115) / 0.835 = 167.7 kJ → Q_sci = 167.7 / (115×0.85) = 1.72.
    Current Q_sci ≈ 2.6×10⁻⁶ (0.25 J yield / 97.75 kJ plasma input).
    Breakeven Q_sci = 1/(η_coup × η_conv_combined) = 1/(0.85×0.835) = 1.41.
    Target requires 660,000× improvement in Q_sci from current state.
    Ref: analysis.md §Section 2, §Section 5. HIGH UNCERTAINTY (fundamental physics gap)."""

    # === p-B11 ENERGY PARTITIONING ===
    # p + ¹¹B → 3⁴He + 8.68 MeV: all energy in charged particles (no neutrons).
    # DPF output partitions into: (a) energetic ion beam, (b) X-ray bremsstrahlung.
    # QMF effect suppresses bremsstrahlung → more energy in charged particles.
    # Without QMF, bremsstrahlung > fusion power → concept cannot reach net energy.

    f_ion_beam: float = 0.70
    """Fraction of total DPF output energy in the ion beam (charged particles) [dimensionless].
    Remaining fraction (1 − f_ion_beam) = 0.30 goes as X-ray bremsstrahlung.
    Source: Not explicitly quantified in LPPFusion sources; ASSUMED from context.
    With QMF suppression of bremsstrahlung, f_ion_beam > 0.5 required.
    Ref: lppfusion-technology-focus-fusion-energy-dpf-device.md (energy partitioning).
    HIGH UNCERTAINTY (QMF bremsstrahlung suppression unverified experimentally)."""

    eta_dec: float = 0.70  # standardized from 0.85 per scoring_framework.md (Energy Capture: Direct (charged particle))
    """Ion beam decelerator efficiency: fraction of ion beam energy converted to electricity.
    Source: LPPFusion cites energy recovery linac analogy (~85% in accelerator context).
    DPF beam is divergent, multi-species (α, p, B ions), ~10 ns duration — unlike
    mono-energetic collimated accelerator beams where this efficiency is demonstrated.
    Ref: lerner-2023-jfe-paper.md §Energy Capture.
    HIGH UNCERTAINTY (no DPF-specific decelerator prototype exists)."""

    eta_xray: float = 0.70  # standardized from 0.80 per scoring_framework.md (Energy Capture: Direct (charged particle))
    """X-ray photoelectric converter efficiency: fraction of X-ray energy to electricity.
    Source: LPPFusion design estimate ('80%+') for multilayered photoelectric vacuum tube.
    Device is described as 'never-before-built'; efficiency from theoretical modeling only.
    Converter geometry: ~40–50 cm inner radius, ~50 cm length.
    Ref: lerner-2023-jfe-paper.md §Energy Capture.
    HIGH UNCERTAINTY (device never built; no experimental data at any scale)."""

    # === REPETITION RATE & PLANT OPERATION ===

    rep_rate_Hz: float = 200.0
    """Shot repetition rate [Hz].
    Source: LPPFusion commercial target; thermally limited by 10 kW/cm² anode tip.
    Best demonstrated DPF rep rate: 16 Hz (NX2 Singapore, non-fusion X-ray source).
    200 Hz at 2.7 MA × fusion-relevant conditions: never demonstrated.
    Ref: lerner-2023-jfe-paper.md §Steps from Net Energy to Commercialization;
         analysis.md §Section 2 (Challenge 4). HIGH UNCERTAINTY."""

    n_mod: int = 200
    """Number of DPF modules per plant.
    Rationale: each module produces ~5 MWe net; 200 modules → ~1 GWe plant.
    LPPFusion envisions mass-deployed modular devices; this represents a utility-scale
    deployment with staggered maintenance (not all modules down simultaneously).
    ASSUMED: no plant-level design published; 200 is a nominal scaling choice."""

    plant_availability: float = 0.75
    """Plant capacity factor [dimensionless].
    Source: No published estimate for DPF plant. Monthly electrode replacement implies
    ~5–10% scheduled downtime per module; staggered across 200 modules allows high
    plant-level availability. Additional downtime for capacitor switch replacement.
    Ref: lerner-2023-jfe-paper.md §Steps from Net Energy (monthly electrode target).
    MODERATE UNCERTAINTY (no maintenance model; electrode lifetime at 2.7 MA×200 Hz unknown)."""

    plant_lifetime_years: float = 30.0
    """Plant economic lifetime [years].
    Source: Modular devices may be refreshed rather than decommissioned; shorter
    lifetime than conventional nuclear (40–60 yr) assumed for novel technology.
    ASSUMED: no design lifetime published. MODERATE UNCERTAINTY."""

    noak: bool = False
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    FOAK is appropriate given zero commercial deployments of DPF power plants.
    LPPFusion's $500K/device target is an NOAK mass-production estimate.
    FOAK adds contingency (10%) and higher pre-construction costs.
    Ref: 1costingfe CAS29 convention."""

    # === PER-MODULE AUXILIARY LOADS ===

    p_control_kW: float = 10.0
    """I&C, sensors, timing electronics per module [kW].
    ASSUMED: analogy to pulsed power R&D devices. Small but non-negligible at 200 Hz."""

    p_cooling_kW: float = 50.0
    """Electrode and DEC cooling power per module [kW].
    Source: Helium coolant system required for anode tip at 10 kW/cm² thermal limit.
    Ref: lerner-2023-jfe-paper.md §Steps from Net Energy (electrode cooling constraint).
    ASSUMED: rough estimate; no system design published. MODERATE UNCERTAINTY."""

    # === PER-MODULE DEVICE COSTS (NOAK TARGETS) ===
    # LPPFusion states $500K/module NOAK target covering all hardware.
    # We decompose into CAS sub-accounts. FOAK multiplier applied in _compute_cas22.

    cap_bank_cost_M_NOAK: float = 0.18
    """Capacitor bank + charging electronics + spark-gap switches, NOAK [M$/module].
    Basis: 1costingfe c_cap_allin_per_joule = $0.5/J_stored (NOAK all-in pulsed power).
    E_stored = 115,000 J × $0.5/J = $57,500 → rounded to $180K including
    commercial charging circuit, bus work, and mounting hardware.
    Ref: 1costingfe costing_constants.yaml (c_cap_allin_per_joule = 0.5 $/J).
    MODERATE UNCERTAINTY (commercial DPF switch lifetime at 200 Hz uncharacterized)."""

    dec_cost_M_NOAK: float = 0.20
    """Ion beam decelerator + X-ray photoelectric converter, NOAK [M$/module].
    Source: LPPFusion $500K/device target implicitly includes both DEC systems.
    Decomposition (DEC ≈ 40% of module cost) is ASSUMED.
    Cross-check: 1costingfe dec_base = $100M at 400 MWe; per-module DEC output ≈ 5 MW
    → scaling gives $100M × (5/400)^0.6 = $5.5M — far above LPPFusion's target.
    Using LPPFusion's aspirational NOAK figure as the optimistic bound.
    Ref: lerner-2023-jfe-paper.md §Cost; analysis.md §Section 5.
    HIGH UNCERTAINTY (device never built; 1costingfe scaling gives 25× higher cost)."""

    device_structure_cost_M_NOAK: float = 0.12
    """DPF vacuum vessel + electrode assembly + primary structure, NOAK [M$/module].
    Source: Remainder of LPPFusion $500K after cap bank + DEC allocation.
    Device: ~4 m × 4 m footprint, ~3 ton device, ~30 m³.
    Ref: lerner-2023-jfe-paper.md §Steps from Net Energy (device dimensions).
    MODERATE UNCERTAINTY."""

    foak_multiplier: float = 5.0
    """FOAK cost multiplier applied to per-module hardware [dimensionless].
    Source: FOAK premium for novel pulsed power / DEC devices.
    LPPFusion's $500K NOAK target assumes full manufacturing learning curve.
    FOAK for unprecedented device type: 3–10× is typical range; 5× is mid-estimate.
    ASSUMED: no FOAK/NOAK cost trajectory data for DPF devices. HIGH UNCERTAINTY."""

    # === GEOMETRY ===

    converter_inner_radius_m: float = 0.45
    """Inner radius of X-ray photoelectric converter surrounding DPF plasmoid [m].
    Source: LPPFusion describes converter as ~40–50 cm inner radius.
    Ref: lerner-2023-jfe-paper.md §Energy Capture. MODERATE UNCERTAINTY."""

    converter_length_m: float = 0.50
    """Axial length of the ion beam / X-ray converter region [m].
    Source: Inferred from DPF device geometry. Anode radius = 2.8 cm;
    beam expands as it exits the plasmoid.
    Ref: lerner-2024-frontiers-pB11-prep.md §Introduction (anode radius).
    ASSUMED: no engineering drawings published."""

    shield_thickness_m: float = 0.05
    """Minimal biological shield thickness [m].
    p-B11 is aneutronic: no 14 MeV neutrons, no lithium blanket needed.
    Only X-ray shielding for bremsstrahlung leakage + C-11 (20 min half-life) control.
    Ref: analysis.md §Section 7 (aneutronic supply chain advantages). MODERATE UNCERTAINTY."""

    # === ELECTRODE O&M (per module per replacement) ===

    electrode_cost_per_set_USD: float = 10_000.0
    """Cost of one beryllium electrode set (anode + cathode assembly) [USD/set].
    Source: No published cost for commercial DPF electrodes. Industrial beryllium
    machined components: $1,000–$50,000/kg depending on grade and machining complexity.
    Beryllium is specialty-toxic; machining requires dedicated facilities.
    Ref: analysis.md §Section 4 (beryllium electrode; 4,000 t/yr fleet requirement).
    HIGH UNCERTAINTY (no commercial DPF electrode cost data)."""

    electrode_replacement_months: float = 1.0
    """Target electrode replacement interval [months/replacement].
    Source: LPPFusion commercial design intent (monthly cadence).
    Ref: lerner-2023-jfe-paper.md §Steps from Net Energy to Commercialization.
    HIGH UNCERTAINTY (erosion rate at 2.7 MA × 200 Hz never measured)."""

    cap_annual_replacement_frac: float = 0.10
    """Annual replacement fraction of capacitor bank value [dimensionless].
    Source: Standard industrial pulsed power O&M; 10% per year replacement budget.
    At 200 Hz: ~4.7 × 10⁹ shots/module-year; modern film capacitors rated 10¹⁰ shots
    at reduced stress → partial annual replacement is appropriate.
    ASSUMED: no DPF-specific switch lifetime data at commercial duty. MODERATE UNCERTAINTY."""

    # === FUEL COSTS ===

    b11_cost_per_kg_USD: float = 10_000.0
    """Enriched B-11 decaborane cost [USD/kg B-11].
    Source: 1costingfe u_b11 = $10,000/kg (FOAK, no industrial isotopic B-11 supply).
    Isotopic enrichment to < 0.07% B-10 (natural: ~20%) is specialty processing.
    NOAK target: $75/kg (1costingfe u_b11_noak) once industrial supply established.
    Lab-scale anchor (2019): LPPFusion purchased 93 g isotopically pure decaborane
    (99.9999% chemical, 99.9% B-11) at $600/gram = $600,000/kg. Commercial mass
    production projected to reduce per-gram price "many hundred-fold" (~$0.60–$6/gram
    = $600–$6,000/kg at scale). Note: lab procurement required Russian isotopic
    purification + Czech decaborane synthesis (single-source each step).
    Ref: 1costingfe costing_constants.yaml; lppfusion-proton-boron-p11b-fuel-arrives.md.
    HIGH UNCERTAINTY (no commercial B-11 enrichment supply chain exists)."""

    b11_kg_per_module_year: float = 0.10
    """B-11 fuel consumption per module per year [kg/module/yr].
    Back-derived: 200 Hz × 3.15e7 s/yr × 0.75 CF × ~10 μg B-11/shot fusion mass
    with 5% burn fraction and 95% recycle → net consumption << 1 g/yr.
    Using 100 g/yr to account for decaborane losses, leaks, isotopic waste.
    Fuel cost is negligible in LCOE regardless of this estimate.
    ASSUMED: no commercial fuel flow data. LOW UNCERTAINTY for LCOE sensitivity."""

    # === FINANCIAL ===

    interest_rate: float = 0.10
    """Real discount rate / WACC [dimensionless].
    Source: 10% reflects elevated technology risk vs. conventional nuclear (8%).
    Appropriate for pre-demonstration technology with unresolved physics questions.
    Ref: Standard TEA convention for unproven fusion concepts. MODERATE UNCERTAINTY."""

    inflation_rate: float = 0.02
    """Inflation rate [dimensionless]. Ref: 1costingfe default."""

    construction_time_years: float = 3.0
    """Construction period [years].
    Source: Modular assembly of pre-manufactured 5 MW units is faster than site-built
    nuclear. 200 modules shipped and installed; no on-site nuclear construction.
    ASSUMED: no project plan published. MODERATE UNCERTAINTY."""

    om_fixed_base_M: float = 24.0
    """Fixed O&M baseline at 1 GWe [M$/yr], before electrode and cap replacement.
    Source: 1costingfe om_cost_pb11 = 24 M$/yr at 1 GWe (scales as P_net^0.5).
    Covers: staffing (~59 FTE at 1 GWe), routine maintenance, supplies, insurance.
    Ref: 1costingfe costing_constants.yaml (om_cost_pb11). MODERATE UNCERTAINTY."""

    def _compute_power(self) -> dict:
        """Layer 1: Power balance for single DPF module and plant totals.

        Energy flow (per shot):
          Stored energy → plasma pinch (coupling efficiency) → fusion yield (Q_sci)
          → ion beam (f_ion_beam) + X-rays (1-f_ion_beam)
          → electricity via DEC (η_dec, η_xray)
          → net = gross − driver recharge − auxiliaries
        """
        r = {}

        # Energy into plasma per shot
        e_plasma_kJ = self.e_stored_kJ * self.driver_coupling_eff
        r["e_plasma_kJ"] = e_plasma_kJ

        # Fusion energy per shot (Q_sci applied to plasma energy)
        e_fus_kJ = e_plasma_kJ * self.Q_sci
        r["e_fus_kJ"] = e_fus_kJ

        # p-B11 energy split: ion beam vs X-ray bremsstrahlung
        f_xray = 1.0 - self.f_ion_beam
        e_ion_kJ = e_fus_kJ * self.f_ion_beam
        e_xray_kJ = e_fus_kJ * f_xray
        r["e_ion_kJ"] = e_ion_kJ
        r["e_xray_kJ"] = e_xray_kJ
        r["f_xray"] = f_xray

        # Gross electrical per shot (both DEC paths)
        e_gross_kJ = e_ion_kJ * self.eta_dec + e_xray_kJ * self.eta_xray
        r["e_gross_kJ"] = e_gross_kJ

        # Net electrical per shot = gross − driver recharge
        e_net_kJ = e_gross_kJ - self.e_stored_kJ
        r["e_net_kJ"] = e_net_kJ
        r["combined_dec_efficiency"] = e_gross_kJ / e_fus_kJ if e_fus_kJ > 0 else 0.0
        r["Q_sci_breakeven"] = (
            1.0 / (self.driver_coupling_eff * (self.f_ion_beam * self.eta_dec
                                               + f_xray * self.eta_xray))
        )

        # Time-averaged power per module [MW]
        # kJ × Hz = kW; divide by 1000 for MW
        p_fus = e_fus_kJ * self.rep_rate_Hz / 1e3
        p_th = 0.0   # no thermal cycle in direct conversion plant
        p_et = e_gross_kJ * self.rep_rate_Hz / 1e3

        # Auxiliary/parasitic loads per module [MW]
        p_aux = (self.p_control_kW + self.p_cooling_kW) / 1e3

        # Driver recharge recirculating power per module [MW]
        p_driver_recirc = self.e_stored_kJ * self.rep_rate_Hz / 1e3

        # Net electric per module [MW]
        p_net = e_net_kJ * self.rep_rate_Hz / 1e3 - p_aux

        r["p_fus"] = p_fus
        r["p_th"] = p_th
        r["p_et"] = p_et
        r["p_net"] = p_net
        r["p_driver_recirc"] = p_driver_recirc
        r["p_aux"] = p_aux
        r["Q_sci"] = self.Q_sci
        r["Q_eng"] = e_fus_kJ / self.e_stored_kJ if self.e_stored_kJ > 0 else 0.0
        r["recirc_fraction"] = (
            (p_driver_recirc + p_aux) / p_et if p_et > 0 else float("inf")
        )

        # Plant totals
        r["p_net_plant"] = p_net * self.n_mod
        r["p_et_plant"] = p_et * self.n_mod
        r["p_th_plant"] = p_th * self.n_mod

        # Shots per year per module
        r["shots_per_year"] = (
            self.rep_rate_Hz * 3600.0 * 8760.0 * self.plant_availability
        )

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Cylindrical geometry for per-module converter/shield volumes.

        Geometry: concentric cylindrical shells centered on the DPF plasmoid.
          Inner: converter (ion beam decelerator + X-ray photoelectric layers)
          Middle: minimal biological shield
          Outer: primary structure + vacuum vessel
        """
        r = {}
        ri = self.converter_inner_radius_m
        L = self.converter_length_m

        def cyl_shell_vol(r_in: float, thickness: float, length: float) -> float:
            r_out = r_in + thickness
            return math.pi * (r_out**2 - r_in**2) * length

        converter_thickness_m = 0.15   # coil conductors + photoelectric foil layers
        r["converter_vol_m3"] = cyl_shell_vol(ri, converter_thickness_m, L)
        r_conv_out = ri + converter_thickness_m

        r["shield_vol_m3"] = cyl_shell_vol(r_conv_out, self.shield_thickness_m, L)
        r_shield_out = r_conv_out + self.shield_thickness_m

        structure_thickness_m = 0.10
        r["structure_vol_m3"] = cyl_shell_vol(r_shield_out, structure_thickness_m, L)
        r_struct_out = r_shield_out + structure_thickness_m

        vessel_thickness_m = 0.05
        r["vessel_vol_m3"] = cyl_shell_vol(r_struct_out, vessel_thickness_m, L)
        r_vessel_out = r_struct_out + vessel_thickness_m

        r["module_outer_diameter_m"] = 2.0 * r_vessel_out

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment sub-accounts (plant totals).

        DPF-specific account overrides:
          C220101 (blanket)     → ZERO  (aneutronic; no breeding blanket)
          C220102 (shield)      → minimal biological shield; pb11 unit cost
          C220103 (coils)       → ZERO  (no external magnets; DPF self-pinches)
          C220104 (heating)     → ZERO  (no NBI/ECRH; driver provides all energy)
          C220107 (power supply)→ capacitor bank + charging electronics
          C220108 (target fab)  → electrode manufacturing facility (monthly replacement)
          C220109 (DEC)         → ion beam decelerator + X-ray photoelectric converter
          C220110 (remote hdlg) → conventional equipment (no rad-hardened robotics)
          C220200 (coolant)     → minimal (electrode He cooling only; no primary loop)
          C220300 (cryo)        → minimal (no SC magnets, no tritium cryo)
          C220400 (rad waste)   → minimal (short-lived C-11, no long-lived waste)
          C220500 (fuel hdlg)   → enriched decaborane handling (pb11 base from 1costingfe)
        """
        r = {}
        p_et = max(power["p_et_plant"], 1.0)
        p_net_total = max(power["p_net_plant"], 1.0)

        # FOAK/NOAK hardware multiplier
        hw = self.foak_multiplier if not self.noak else 1.0

        # ── Per-module hardware accounts (× n_mod) ──────────────────────────────

        # C220101: First Wall / Blanket — ZERO (aneutronic, no breeding blanket)
        # p-B11 produces no 14 MeV neutrons → no lithium breeding blanket needed.
        # X-ray converter is costed under C220109.
        # Ref: analysis.md §7 (eliminates 30–40% of D-T capital cost structure).
        r["C220101"] = 0.0  # [override] aneutronic — no blanket

        # C220102: Shield — minimal biological shield only (pb11 unit cost)
        # 1costingfe blanket_unit_cost_pb11 = 0.05 M$/m³ (X-ray only, no neutrons).
        # Ref: 1costingfe costing_constants.yaml (blanket_unit_cost_pb11 = 0.05).
        shield_cost_per_mod = 0.05 * geom["shield_vol_m3"]
        r["C220102"] = shield_cost_per_mod * self.n_mod  # [override] minimal

        # C220103: Coils — ZERO (DPF is self-pinching via Z-pinch current)
        # No toroidal/poloidal coils. The pinch current generates its own field.
        r["C220103"] = 0.0  # [override] no external confinement magnets

        # C220104: Supplementary Heating — ZERO
        # Capacitor bank discharge provides all compression; no NBI/ECRH/laser preheat.
        r["C220104"] = 0.0  # [override] no supplementary heating

        # C220105: Primary Structure — volume-based (1costingfe formula, cylindrical)
        # Ref: 1costingfe structure_unit_cost = 0.15 M$/m³.
        structure_per_mod = (
            0.15 * geom["structure_vol_m3"] * (p_et / P_ET_REF) ** 0.5
        )
        r["C220105"] = structure_per_mod * hw * self.n_mod

        # C220106: Vacuum System — volume-based (1costingfe formula)
        # Ref: 1costingfe vessel_unit_cost = 0.72 M$/m³.
        vessel_per_mod = (
            0.72 * geom["vessel_vol_m3"] * (p_et / P_ET_REF) ** 0.6
        )
        r["C220106"] = vessel_per_mod * hw * self.n_mod

        # C220107: Power Supplies — OVERRIDE: capacitor bank per module
        # The capacitor bank IS the DPF power supply. Cost from 1costingfe pulsed power
        # basis: c_cap_allin_per_joule = $0.5/J_stored → 115,000 J × $0.5 = $57.5K NOAK,
        # rounded to $180K including commercial charging circuit and bus work.
        # Ref: 1costingfe costing_constants.yaml (c_cap_allin_per_joule).
        r["C220107"] = self.cap_bank_cost_M_NOAK * hw * self.n_mod  # [override]

        # C220108: Target / Electrode Factory
        # DPF uses consumable beryllium electrodes (monthly replacement).
        # This covers electrode manufacturing/refurbishment facility capital.
        # No analogous IFE target factory; using scaled industrial analogue.
        # ASSUMED: $20M facility at 1 GWe plant scale.
        r["C220108"] = 20.0 * (p_net_total / 1000.0) ** 0.7  # [override] electrode facility

        # C220109: Direct Energy Converter — OVERRIDE: ion beam decelerator + X-ray converter
        # KEY DPF-SPECIFIC ACCOUNT. These are the sole energy conversion path.
        # No thermal cycle fallback exists if DEC underperforms.
        # Cost: LPPFusion's $500K/module NOAK covers DEC (ASSUMED ~40% = $200K).
        # Cross-check vs 1costingfe scaling: 25× higher → LPPFusion very optimistic.
        # Ref: lerner-2023-jfe-paper.md §Energy Capture; analysis.md §Section 2 (Challenge 3).
        r["C220109"] = self.dec_cost_M_NOAK * hw * self.n_mod  # [override]

        # C220110: Remote Handling — conventional equipment (no rad-hardened robotics)
        # p-B11: no activated in-vessel components requiring remote handling.
        # Conventional cranes + platforms + vessel access tooling.
        # Ref: 1costingfe remote_handling_pb11_base = 20 M$ at 1 GWe.
        r["C220110"] = 20.0 * (p_net_total / 1000.0) ** 0.6

        # C220111: Installation labor (14% of reactor equipment subtotal)
        # Ref: 1costingfe installation_frac = 0.14.
        reactor_sub = sum(
            r[k] for k in [
                "C220101", "C220102", "C220103", "C220104", "C220105",
                "C220106", "C220107", "C220108", "C220109", "C220110",
            ]
        )
        r["C220111"] = 0.14 * reactor_sub

        # C220112: Isotope Separation — ZERO (enriched B-11 purchased externally)
        # B-11 isotopic enrichment is performed off-site; no on-site separation plant.
        # Cost of enriched B-11 feed appears in CAS80 (fuel costs).
        r["C220112"] = 0.0

        # ── Per-module subtotal (for reporting) ──────────────────────────────────
        per_mod_total = reactor_sub + r["C220111"] + r["C220112"]
        r["CAS22_per_module"] = per_mod_total / self.n_mod

        # ── Plant-wide accounts ──────────────────────────────────────────────────

        # C220200: Coolant Systems — minimal (electrode He cooling only; no primary loop)
        # No FLiBe/PbLi primary coolant. Only helium anode cooling circuit.
        # Ref: lerner-2023-jfe-paper.md §Steps (He coolant for 10 kW/cm² anode limit).
        r["C220200"] = 5.0 * (p_net_total / 1000.0) ** 0.5  # [override] minimal

        # C220300: Auxiliary Cooling + Cryoplant — minimal
        # No SC magnets, no tritium cryo. Small HVAC cooling only.
        r["C220300"] = 1.0 * (p_net_total / 1000.0) ** 0.5  # [override] minimal

        # C220400: Radioactive Waste Management — minimal
        # C-11 (t½ = 20 min), Be-7 (t½ = 53 d) — low activation, short-lived.
        # Ref: analysis.md §Section 4 (C-11 exhaust management).
        r["C220400"] = 1.0 * (p_net_total / 1000.0) ** 0.5  # [override] minimal

        # C220500: Fuel Handling & Storage — enriched decaborane handling
        # 1costingfe fuel_handling_pb11_base = 15 M$ at 1 GWe.
        # Ref: 1costingfe costing_constants.yaml (fuel_handling_pb11_base).
        r["C220500"] = 15.0 * (p_net_total / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment — standard formula
        r["C220600"] = 11.5 * (p_net_total / 1000.0) ** 0.8

        # C220700: Instrumentation & Control
        # Ref: 1costingfe formula adapted for DPF (uses gross electric as proxy).
        r["C220700"] = 85.0 * (p_et / 3500.0) ** 0.65

        r["CAS22_plant_wide"] = sum(
            r[k] for k in ["C220200", "C220300", "C220400", "C220500", "C220600", "C220700"]
        )

        r["CAS22"] = per_mod_total + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: CAS10-60 capital costs."""
        r = {}
        p_net_total = max(power["p_net_plant"], 1.0)
        p_et = max(power["p_et_plant"], 1.0)

        # === CAS10: Pre-construction ===
        # p-B11 requires minimal NRC licensing (no radioactive materials under Part 30/50).
        # 1costingfe licensing_cost_pb11 = $0.1M; licensing_time_pb11 = 0 years.
        site_permits = 3.0
        plant_studies = 4.0 if self.noak else 20.0
        plant_permits = 2.0
        plant_reports = 1.0
        other_precon = 1.0
        land_cost = 0.25 * p_net_total * math.sqrt(self.n_mod) * 10_000 / 1e6
        licensing_cost = 0.1 if self.noak else 0.5   # pb11: minimal
        r["CAS10"] = (
            site_permits + plant_studies + plant_permits + plant_reports
            + other_precon + land_cost + licensing_cost
        )

        # === CAS21: Buildings ===
        # p-B11 specific values from 1costingfe costing_constants.yaml (pb11 column).
        # Key differences from D-T: no hot cell, no tritium systems, no turbine building.
        # Turbine building replaced by DEC power conditioning building.
        # Ref: 1costingfe building_costs table (pb11 fuel type).
        bld = {}
        bld["site_improvements"] = 69.0                                              # fixed, pb11
        bld["reactor_building"] = 81.0 * (p_et / P_ET_REF) ** 0.6                  # scales p_fus proxy
        bld["hot_cell"] = 0.0                                                        # pb11: none needed
        bld["reactor_auxiliaries"] = 17.0 * (p_et / P_ET_REF) ** 0.6               # scales p_fus proxy
        bld["fuel_storage"] = 1.0                                                    # fixed, pb11
        bld["control_room"] = 12.0                                                   # fixed
        bld["security"] = 2.3                                                        # fixed, pb11
        bld["ventilation_hvac"] = 3.5 * (p_et / P_ET_REF) ** 0.5                   # pb11
        bld["administration"] = 5.0 * (p_net_total / 1000.0) ** 0.3                # staff-scaled
        bld["maintenance"] = 14.0                                                    # fixed
        bld["site_services"] = 3.5                                                   # fixed, pb11
        bld["dec_power_conditioning"] = 17.0 * (p_et / P_ET_REF) ** 0.7            # replaces turbine_building
        bld["power_supply"] = 17.0 * (p_et / P_ET_REF) ** 0.7                      # scales p_et
        bld["onsite_ac"] = 12.0 * (p_et / P_ET_REF) ** 0.7                         # scales p_et
        bld["cryogenics"] = 0.0                                                      # no cryo for DPF
        bld["service_water"] = 9.0 * (p_et / P_ET_REF) ** 0.5
        bld["assembly_hall"] = 21.0                                                  # fixed
        r["CAS21"] = sum(bld.values())
        r["CAS21_detail"] = bld

        # === CAS22 ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment — ZERO (no thermal cycle) ===
        # DPF uses direct energy conversion; no steam turbines, no Rankine cycle.
        # Power conditioning for DEC output is included in CAS21 and CAS24.
        r["CAS23"] = 0.0  # [override] direct conversion plant — no turbine

        # === CAS24: Electric Plant Equipment ===
        # Increased fraction (0.12 vs 1costingfe standard 0.084) for DEC power
        # electronics: bidirectional switching, grid-tie inverters, fast controls.
        # Ref: 1costingfe electric_per_mw = 0.08418 M$/MW; markup for DEC electronics.
        r["CAS24"] = p_et * 0.12

        # === CAS25: Miscellaneous Plant Equipment ===
        # Ref: 1costingfe misc_per_mw = 0.05124 M$/MW.
        r["CAS25"] = p_net_total * 0.05124

        # === CAS26: Heat Rejection — minimal ===
        # No waste heat from thermal cycle. Electrode He cooling loop only.
        # Ref: 1costingfe heat_rej_per_mw ≈ 0.034 M$/MW for thermal plants.
        r["CAS26"] = p_net_total * 0.005  # [override] 1/7th of thermal plant

        # === CAS27: Special Materials — ZERO ===
        # 1costingfe special_materials_pb11 = 0 (no PbLi, no enriched Li, no Be inventory).
        # Ref: 1costingfe costing_constants.yaml.
        r["CAS27"] = 0.0

        # === CAS28: Digital Twin ===
        # Ref: 1costingfe digital_twin = $5M.
        r["CAS28"] = 5.0

        # === CAS29: Contingency ===
        # Ref: 1costingfe contingency_rate_foak = 0.10; noak = 0.0.
        cas20_sub = sum(
            r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24", "CAS25", "CAS26", "CAS27", "CAS28"]
        )
        contingency_rate = 0.0 if self.noak else 0.10
        r["CAS29"] = contingency_rate * cas20_sub
        r["CAS20"] = cas20_sub + r["CAS29"]

        # === CAS30: Indirect Costs ===
        # Ref: 1costingfe indirect_fraction = 0.20; reference_construction_time = 6 yr.
        ref_constr = 6.0
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / ref_constr)

        # === CAS40: Owner's Costs ===
        # 1costingfe owner_cost_pb11 = 20 M$ at 1 GWe × (P_net/1GWe)^0.5.
        # Ref: 1costingfe costing_constants.yaml (owner_cost_pb11 = 20).
        r["CAS40"] = 20.0 * (p_net_total / 1000.0) ** 0.5

        # === CAS50: Supplementary Costs ===
        # Ref: 1costingfe sub-account model (CAS50_supplementary_costs.md).
        spare_parts = 0.01 * sum(r[k] for k in ["CAS24", "CAS25", "CAS26", "CAS28"])
        startup_fuel = 0.1 * (p_net_total / 1000.0)
        shipping = 0.015 * r["CAS20"]
        taxes = 0.01 * r["CAS20"]
        insurance = 0.015 * (r["CAS20"] + r["CAS30"])
        decommission = 53.0 * (p_net_total / 1000.0) ** 0.7  # 1costingfe decom_provision_pb11
        r["CAS50"] = spare_parts + startup_fuel + shipping + taxes + insurance + decommission

        r["overnight_capital"] = (
            r["CAS10"] + r["CAS20"] + r["CAS30"] + r["CAS40"] + r["CAS50"]
        )

        # === CAS60: Interest During Construction ===
        i = self.interest_rate
        T = self.construction_time_years
        f_idc = ((1 + i) ** T - 1) / (i * T) - 1 if (i > 0 and T > 0) else 0.0
        r["CAS60"] = f_idc * r["overnight_capital"]
        r["f_IDC"] = f_idc

        r["total_capital"] = r["overnight_capital"] + r["CAS60"]

        if power["p_net_plant"] > 0:
            r["specific_capital_USD_per_kWe"] = (
                r["total_capital"] * 1e6 / (power["p_net_plant"] * 1e3)
            )
        else:
            r["specific_capital_USD_per_kWe"] = float("inf")

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70-90 annualized costs and LCOE."""
        r = {}
        p_net_total = max(power["p_net_plant"], 1.0)

        # Capital Recovery Factor
        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1 + i) ** n / ((1 + i) ** n - 1)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]

        # === CAS71: Fixed O&M (staffing, routine maintenance, levelized) ===
        # 1costingfe: om_cost_pb11 = 24 M$/yr at 1 GWe × (P_net/1GWe)^0.5.
        annual_om_base = self.om_fixed_base_M * (p_net_total / 1000.0) ** 0.5
        g = self.inflation_rate
        Tc = self.construction_time_years
        A1 = annual_om_base * (1 + g) ** Tc
        if abs(i - g) > 1e-10:
            pv_ann = A1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
        else:
            pv_ann = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_ann

        # === CAS72: Scheduled Replacement (electrodes + capacitor bank) ===
        # (a) Electrode replacement: monthly cadence across all modules
        replacements_per_mod_yr = 12.0 / self.electrode_replacement_months
        annual_electrode_M = (
            replacements_per_mod_yr * self.n_mod
            * self.electrode_cost_per_set_USD / 1e6
        )

        # (b) Capacitor bank / switch replacement: annual fraction of bank value
        hw = self.foak_multiplier if not self.noak else 1.0
        annual_cap_M = (
            self.cap_annual_replacement_frac
            * self.cap_bank_cost_M_NOAK * hw
            * self.n_mod
        )

        r["CAS72"] = annual_electrode_M + annual_cap_M
        r["annual_electrode_cost_M"] = annual_electrode_M
        r["annual_cap_replacement_M"] = annual_cap_M

        r["CAS70"] = r["CAS71"] + r["CAS72"]

        # === CAS80: Fuel & Consumables ===
        annual_b11_M = (
            self.b11_kg_per_module_year * self.n_mod
            * self.b11_cost_per_kg_USD / 1e6
        )
        annual_H_M = 0.001   # protium: negligible
        r["CAS80"] = annual_b11_M + annual_H_M
        r["CAS80_b11"] = annual_b11_M
        r["CAS80_H"] = annual_H_M

        # === LCOE ===
        annual_revenue_req = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_revenue_req
        annual_energy_MWh = 8760.0 * p_net_total * self.plant_availability
        r["annual_energy_MWh"] = annual_energy_MWh

        # Guard: LCOE is undefined when net electric power is zero or negative.
        # p_net_total uses max(..., 1.0) to avoid division errors in cost scaling,
        # but that floor must not propagate into the LCOE output — a plant that
        # produces no net electricity has no defined LCOE regardless of costs.
        if annual_energy_MWh > 0 and power["p_net_plant"] > 0:
            lcoe_USD_MWh = annual_revenue_req * 1e6 / annual_energy_MWh
            r["lcoe_USD_per_MWh"] = lcoe_USD_MWh
            r["lcoe_cents_per_kWh"] = lcoe_USD_MWh / 10.0
        else:
            r["lcoe_USD_per_MWh"] = float("inf")
            r["lcoe_cents_per_kWh"] = float("inf")

        if annual_revenue_req > 0:
            r["capital_fraction"] = r["CAS90"] / annual_revenue_req
            r["om_fraction"] = r["CAS70"] / annual_revenue_req
            r["fuel_fraction"] = r["CAS80"] / annual_revenue_req

        return r

    def compute(self) -> dict:
        """Compute LCOE and all derived quantities via CAS-structured accounting.

        Returns nested dict with keys: power, geometry, cas22, costs, economics.
        Module-level extractor reads params and results directly from module scope.
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


def print_results(params: DPFPlantParams, results: dict) -> None:
    """Pretty-print LCOE model results with CAS-structured accounting."""
    power = results["power"]
    cas22 = results["cas22"]
    costs = results["costs"]
    econ = results["economics"]

    print("=" * 72)
    print("Dense Plasma Focus p-B11 (LPPFusion) — 1cFE CAS-Structured LCOE")
    print(f"{'FOAK' if not params.noak else 'NOAK'} | "
          f"{params.n_mod} modules × {power['p_net']:.1f} MWe each = "
          f"{power['p_net_plant']:.0f} MWe plant")
    print("=" * 72)

    print("\n--- Key Input Parameters ---")
    print(f"  Stored energy / shot:       {params.e_stored_kJ:.0f} kJ")
    print(f"  Driver coupling eff:        {params.driver_coupling_eff:.0%}")
    print(f"  Q_sci (target):             {params.Q_sci:.2f}  "
          f"(breakeven = {power['Q_sci_breakeven']:.2f})")
    print(f"  Q_eng (fusion/stored):      {power['Q_eng']:.2f}")
    print(f"  Ion beam fraction:          {params.f_ion_beam:.0%}")
    print(f"  Ion beam DEC efficiency:    {params.eta_dec:.0%}")
    print(f"  X-ray converter efficiency: {params.eta_xray:.0%}")
    print(f"  Combined DEC efficiency:    {power['combined_dec_efficiency']:.1%}")
    print(f"  Rep rate:                   {params.rep_rate_Hz:.0f} Hz")
    print(f"  Modules:                    {params.n_mod}")
    print(f"  Plant availability:         {params.plant_availability:.0%}")
    print(f"  Plant lifetime:             {params.plant_lifetime_years:.0f} yr")
    print(f"  Interest rate (WACC):       {params.interest_rate:.0%}")
    print(f"  FOAK hw multiplier:         {params.foak_multiplier:.0f}×  "
          f"({'FOAK' if not params.noak else 'NOAK — no multiplier'})")

    print("\n--- Power Balance (per module) ---")
    print(f"  Fusion power:               {power['p_fus']:.2f} MW")
    print(f"    Ion beam ({params.f_ion_beam:.0%}):          "
          f"{power['e_ion_kJ'] * params.rep_rate_Hz / 1e3:.2f} MW  → "
          f"DEC: {power['e_ion_kJ'] * params.rep_rate_Hz / 1e3 * params.eta_dec:.2f} MW_e")
    print(f"    X-ray ({power['f_xray']:.0%}):              "
          f"{power['e_xray_kJ'] * params.rep_rate_Hz / 1e3:.2f} MW  → "
          f"DEC: {power['e_xray_kJ'] * params.rep_rate_Hz / 1e3 * params.eta_xray:.2f} MW_e")
    print(f"  Gross electric (DEC out):   {power['p_et']:.2f} MWe")
    print(f"  Recirculating (driver):     {power['p_driver_recirc']:.2f} MW")
    print(f"  Parasitic aux:              {power['p_aux'] * 1000:.0f} kW  "
          f"(control + cooling)")
    print(f"  Net electric / module:      {power['p_net']:.2f} MWe")
    print(f"  Recirculating fraction:     {power['recirc_fraction']:.1%}")
    print(f"\n--- Plant Totals ({params.n_mod} modules) ---")
    print(f"  Gross electric:             {power['p_et_plant']:.0f} MWe")
    print(f"  Net electric:               {power['p_net_plant']:.0f} MWe")

    print("\n--- CAS22: Reactor Plant Equipment ---")
    cas22_labels = {
        "C220101": ("First Wall / Blanket",        "[override] aneutronic — ZERO"),
        "C220102": ("Shield",                       "[override] minimal bio-shield"),
        "C220103": ("Coils",                        "[override] no external magnets — ZERO"),
        "C220104": ("Supplementary Heating",        "[override] no NBI/ECRH — ZERO"),
        "C220105": ("Primary Structure",            "cylindrical per-module"),
        "C220106": ("Vacuum System",                "cylindrical per-module"),
        "C220107": ("Power Supplies (cap bank)",    "[override] capacitor bank"),
        "C220108": ("Electrode Factory",            "[override] Be electrode facility"),
        "C220109": ("Direct Energy Converter",      "[override] DEC (ion beam + x-ray)"),
        "C220110": ("Remote Handling",              "conventional (no rad robotics)"),
        "C220111": ("Installation",                 "14% of subtotal"),
        "C220112": ("Isotope Separation",           "ZERO (external B-11 supply)"),
    }
    print(f"  Per-module hardware (plant total):")
    for code, (label, note) in cas22_labels.items():
        val = cas22[code]
        if val > 0.01 or code in ("C220101", "C220103", "C220104", "C220112"):
            print(f"    {code} {label:<32s} ${val:>8.1f}M  {note}")
    print(f"  {'─' * 55}")
    print(f"    Per-module avg:                          ${cas22['CAS22_per_module']:>8.2f}M")
    pw_labels = {
        "C220200": "Coolant (He electrode cooling only)",
        "C220300": "Aux Cooling + Cryoplant",
        "C220400": "Radioactive Waste Mgmt (minimal)",
        "C220500": "Fuel Handling (enriched decaborane)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    print(f"  Plant-wide accounts:")
    for code, label in pw_labels.items():
        val = cas22[code]
        print(f"    {code} {label:<40s} ${val:>8.1f}M")
    print(f"  {'─' * 55}")
    print(f"    Plant-wide subtotal:                     ${cas22['CAS22_plant_wide']:>8.1f}M")
    print(f"  CAS22 Total:                               ${cas22['CAS22']:>8.1f}M")

    print("\n--- Capital Costs (CAS10-60) ---")
    print(f"  CAS10 Pre-construction:                    ${costs['CAS10']:>8.1f}M")
    print(f"  CAS21 Buildings:                           ${costs['CAS21']:>8.1f}M  "
          f"(no hot cell, no turbine bldg)")
    print(f"  CAS22 Reactor Plant Equipment:             ${costs['CAS22']:>8.1f}M")
    print(f"  CAS23 Turbine Plant:                       ${costs['CAS23']:>8.1f}M  "
          f"[override] direct conversion — ZERO")
    print(f"  CAS24 Electric Plant:                      ${costs['CAS24']:>8.1f}M  "
          f"(incl. DEC power electronics)")
    print(f"  CAS25 Misc Plant:                          ${costs['CAS25']:>8.1f}M")
    print(f"  CAS26 Heat Rejection:                      ${costs['CAS26']:>8.1f}M  "
          f"(minimal — no waste heat)")
    print(f"  CAS27 Special Materials:                   ${costs['CAS27']:>8.1f}M  "
          f"(pb11: ZERO)")
    print(f"  CAS28 Digital Twin:                        ${costs['CAS28']:>8.1f}M")
    print(f"  CAS29 Contingency:                         ${costs['CAS29']:>8.1f}M  "
          f"({'10% FOAK' if not params.noak else 'NOAK = 0%'})")
    print(f"  {'─' * 55}")
    print(f"  CAS20 Direct Costs:                        ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30 Indirect Costs:                      ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40 Owner's Costs:                       ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50 Supplementary:                       ${costs['CAS50']:>8.1f}M")
    print(f"  {'─' * 55}")
    print(f"  Overnight Capital:                         ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60 IDC (f={costs['f_IDC']:.3f}):                   ${costs['CAS60']:>8.1f}M")
    print(f"  {'═' * 55}")
    print(f"  Total Capital:                             ${costs['total_capital']:>8.1f}M")
    print(f"  Specific Capital:                          ${costs['specific_capital_USD_per_kWe']:>8.0f} $/kWe")

    print("\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90 Capital charge (CRF={econ['CRF']:.4f}):        ${econ['CAS90']:>8.1f}M/yr")
    print(f"  CAS71 Fixed O&M (staffing, levelized):     ${econ['CAS71']:>8.1f}M/yr")
    print(f"  CAS72 Scheduled Replacement:               ${econ['CAS72']:>8.1f}M/yr")
    print(f"    Electrode sets ({params.n_mod} mod × 12/yr × "
          f"${params.electrode_cost_per_set_USD:,.0f}): ${econ['annual_electrode_cost_M']:>8.2f}M/yr")
    print(f"    Cap bank replacement ({params.cap_annual_replacement_frac:.0%}/yr):   "
          f"  ${econ['annual_cap_replacement_M']:>8.2f}M/yr")
    print(f"  CAS70 Total O&M:                           ${econ['CAS70']:>8.1f}M/yr")
    print(f"  CAS80 Fuel & Consumables:                  ${econ['CAS80']:>8.3f}M/yr")
    print(f"    Enriched B-11:                           ${econ['CAS80_b11']:>8.3f}M/yr")

    print(f"\n--- LCOE ---")
    print(f"  Annual energy production:    {econ['annual_energy_MWh']:>12,.0f} MWh")
    print(f"  Annual revenue requirement:  ${econ['annual_revenue_req']:>8.1f}M")
    if econ["lcoe_USD_per_MWh"] < float("inf"):
        print(f"  ╔══════════════════════════════════════════╗")
        print(f"  ║  LCOE = {econ['lcoe_cents_per_kWh']:>7.2f} ¢/kWh                   ║")
        print(f"  ║       = {econ['lcoe_USD_per_MWh']:>7.1f} $/MWh                   ║")
        print(f"  ╚══════════════════════════════════════════╝")
        print(f"  Capital (CAS90):             {econ.get('capital_fraction', 0):.1%}")
        print(f"  O&M (CAS70):                 {econ.get('om_fraction', 0):.1%}")
        print(f"  Fuel (CAS80):                {econ.get('fuel_fraction', 0):.1%}")
    else:
        print(f"  ╔══════════════════════════════════════════╗")
        print(f"  ║  LCOE = UNDEFINED (net power ≤ 0)        ║")
        print(f"  ║  Q_sci below breakeven ({power['Q_sci_breakeven']:.2f})            ║")
        print(f"  ╚══════════════════════════════════════════╝")


def sensitivity_sweep(
    base_params: DPFPlantParams,
    param_name: str,
    values: list,
    label: str = "",
) -> list:
    """Sweep a single parameter and return LCOE for each value."""
    results_list = []
    for val in values:
        p = DPFPlantParams(**{**base_params.__dict__, param_name: val})
        r = p.compute()
        results_list.append(
            {
                "param_value": float(val),
                "lcoe_cents_kWh": r["economics"]["lcoe_cents_per_kWh"],
                "net_electric_MW": r["power"]["p_net_plant"],
                "specific_capital_per_kW": r["costs"]["specific_capital_USD_per_kWe"],
            }
        )
    return results_list


def main() -> None:
    # ── BASELINE: FOAK, LPPFusion target physics ─────────────────────────────
    print("\n" + "#" * 72)
    print("# BASELINE: Dense Plasma Focus p-B11 — FOAK, LPPFusion Target Physics")
    print("#" * 72)
    baseline = DPFPlantParams()
    baseline_results = baseline.compute()
    print_results(baseline, baseline_results)

    # ── SENSITIVITY SWEEPS ───────────────────────────────────────────────────
    print("\n" + "=" * 72)
    print("SENSITIVITY SWEEPS (from baseline)")
    print("=" * 72)
    base_lcoe = baseline_results["economics"]["lcoe_cents_per_kWh"]
    print(f"\nBaseline LCOE: {base_lcoe:.2f} ¢/kWh\n")

    sweeps = {
        "Q_sci": (
            [0.5, 1.0, 1.41, 1.72, 2.5, 4.0, 8.0],
            "Q_sci (scientific gain)",
        ),
        "rep_rate_Hz": (
            [10.0, 50.0, 100.0, 200.0, 400.0],
            "Rep rate [Hz]",
        ),
        "eta_dec": (
            [0.50, 0.65, 0.75, 0.85, 0.92],
            "Ion beam decelerator efficiency",
        ),
        "plant_availability": (
            [0.50, 0.60, 0.70, 0.75, 0.85, 0.90],
            "Plant availability (capacity factor)",
        ),
        "electrode_cost_per_set_USD": (
            [500.0, 2_000.0, 5_000.0, 10_000.0, 50_000.0, 200_000.0],
            "Electrode set cost [USD/set]",
        ),
        "foak_multiplier": (
            [1.0, 2.0, 3.0, 5.0, 8.0, 15.0],
            "FOAK hardware multiplier",
        ),
        "n_mod": (
            [10, 50, 100, 200, 500],
            "Number of modules",
        ),
    }

    for param_name, (values, label) in sweeps.items():
        print(f"  {label}:")
        sweep_results = sensitivity_sweep(baseline, param_name, values)
        for sr in sweep_results:
            val = sr["param_value"]
            lcoe = sr["lcoe_cents_kWh"]
            net = sr["net_electric_MW"]
            if lcoe == float("inf"):
                lcoe_str = f"   N/A (net={net:+.0f} MWe)"
            else:
                lcoe_str = f"{lcoe:7.2f} ¢/kWh  ({net:.0f} MWe)"
            print(f"    {val:>12.3g} → {lcoe_str}")
        print()

    # ── SCENARIO COMPARISON ──────────────────────────────────────────────────
    print("=" * 72)
    print("SCENARIO COMPARISON")
    print("=" * 72)

    # Conservative: FOAK, assume QMF works marginally, modest performance
    conservative = DPFPlantParams(
        Q_sci=1.72,
        rep_rate_Hz=200.0,
        eta_dec=0.80,
        eta_xray=0.70,
        f_ion_beam=0.65,
        plant_availability=0.65,
        electrode_cost_per_set_USD=20_000.0,
        cap_annual_replacement_frac=0.15,
        foak_multiplier=8.0,
        interest_rate=0.12,
        n_mod=200,
        noak=False,
    )

    # Moderate: FOAK, baseline performance, improved reliability
    moderate = DPFPlantParams()  # baseline

    # Optimistic: NOAK (mass production), best-case parameters
    optimistic = DPFPlantParams(
        Q_sci=2.5,
        rep_rate_Hz=200.0,
        eta_dec=0.85,
        eta_xray=0.80,
        f_ion_beam=0.70,
        plant_availability=0.85,
        electrode_cost_per_set_USD=2_000.0,
        cap_annual_replacement_frac=0.05,
        foak_multiplier=1.0,
        interest_rate=0.08,
        n_mod=200,
        noak=True,
        construction_time_years=2.0,
        b11_cost_per_kg_USD=75.0,   # NOAK B-11 supply (1costingfe u_b11_noak)
    )

    # LPPFusion's own claim back-check
    lpp_claim = DPFPlantParams(
        Q_sci=3.0,
        rep_rate_Hz=200.0,
        eta_dec=0.85,
        eta_xray=0.80,
        f_ion_beam=0.70,
        plant_availability=0.85,
        electrode_cost_per_set_USD=500.0,   # assumed negligible by LPPFusion
        cap_annual_replacement_frac=0.02,
        dec_cost_M_NOAK=0.08,               # LPPFusion's $500K total ÷ 200 kW/$ claim
        cap_bank_cost_M_NOAK=0.05,          # LPPFusion assumption
        device_structure_cost_M_NOAK=0.05,
        foak_multiplier=1.0,
        interest_rate=0.05,
        n_mod=200,
        noak=True,
        construction_time_years=2.0,
        b11_cost_per_kg_USD=75.0,
        om_fixed_base_M=5.0,                # LPPFusion implies very low O&M
    )

    scenarios = {
        "Conservative (FOAK, pessimistic)": conservative,
        "Moderate (FOAK, baseline)": moderate,
        "Optimistic (NOAK, best-case)": optimistic,
        "LPPFusion claim back-check": lpp_claim,
    }

    print(f"\n{'Scenario':<32} {'Modules':>7} {'Net MWe':>8} {'$/kWe':>8} {'LCOE':>12}")
    print("-" * 72)
    # Physics-failure row: viability gate that precedes all cost scenarios.
    # This is not a cost scenario — if Q_sci < 1.41, net energy is impossible
    # and LCOE is undefined regardless of engineering assumptions. Decision-makers
    # must pass this gate before any row below is relevant.
    print(f"{'Physics Failure (Q < 1.41)':<32} {'—':>7} {'—':>8} {'—':>8} {'UNDEFINED':>12}")
    print(f"  ↑ Viability gate: current Q_sci = 2.6×10⁻⁶; breakeven requires 660,000× improvement.")
    print(f"  ↑ If not achieved, all scenarios below are moot.")
    print("-" * 72)
    for name, p in scenarios.items():
        r = p.compute()
        net = r["power"]["p_net_plant"]
        spec = r["costs"]["specific_capital_USD_per_kWe"]
        lcoe = r["economics"]["lcoe_cents_per_kWh"]
        if lcoe == float("inf"):
            lcoe_str = "undefined"
        else:
            lcoe_str = f"{lcoe:.2f} ¢/kWh"
        print(f"{name:<32} {p.n_mod:>7d} {net:>8.0f} {spec:>8.0f} {lcoe_str:>12}")

    print()

    # Print full results for optimistic scenario
    print("\n" + "#" * 72)
    print("# OPTIMISTIC SCENARIO (NOAK, best-case): Full Results")
    print("#" * 72)
    print_results(optimistic, optimistic.compute())

    # ── KEY BINDING CONSTRAINTS ──────────────────────────────────────────────
    print("\n" + "=" * 72)
    print("KEY BINDING CONSTRAINTS (top 3 LCOE drivers)")
    print("=" * 72)
    print("""
  1. Q_SCI (FUNDAMENTAL PHYSICS — dominant constraint)
     Current: Q_sci ≈ 2.6 × 10⁻⁶ | Target: 1.72 | Required improvement: 660,000×
     Two sequential unknowns block this:
       (a) QMF bremsstrahlung suppression must work as theorized (TRL 1 — no data)
       (b) Simultaneous high density + high ion energy in p-B11 DPF (never measured)
     If Q_sci < 1.41, no net energy is possible regardless of engineering.
     If Q_sci is achieved, sensitivity shows LCOE can range 3–30 ¢/kWh depending
     on other factors. But without Q_sci > 1.41, LCOE is literally undefined.
     STATUS: blocking. 22-year yield plateau at 0.25 J (D). p-B11 not yet measured.

  2. DIRECT ENERGY CONVERSION (unique single-path constraint)
     Both ion beam decelerator (η=85%) and X-ray converter (η=80%) are unbuilt.
     No prototype, no design drawings, no component tests. DPF ion beam characteristics
     (divergent, multi-species, 10 ns) differ from contexts where 85% is demonstrated.
     LCOE sensitivity shows: η_dec = 0.50 → net power negative (plant impossible).
     LCOE sensitivity shows: η_dec = 0.75 → ~2× higher LCOE vs 0.85 baseline.
     There is NO thermal cycle fallback; underperformance of DEC eliminates the concept.
     STATUS: blocking. Neither device at TRL > 2.

  3. REP-RATE AND ELECTRODE LIFETIME (operational feasibility)
     200 Hz at 2.7 MA × fusion-relevant conditions: never demonstrated.
     Best analogous: 16 Hz (NX2, Singapore, non-fusion, low current).
     Electrode erosion at commercial conditions: zero data.
     Electrode cost sensitivity: $500 → $200,000/set changes LCOE by ~4×.
     Rep rate sensitivity: 10 Hz → ~20× LCOE vs 200 Hz (plant undersized, BOP amortized poorly).
     STATUS: blocking for commercial application. Single-shot R&D operation only.
""")

    print("NOTE: All LCOE values are CONDITIONAL on 120,000× fusion yield improvement")
    print("      and successful demonstration of two novel energy conversion devices.")
    print("      This model maps the parameter space for planning purposes only.")
    print("      LPPFusion's 0.3 ¢/kWh claim requires NOAK manufacturing + very low O&M")
    print("      assumptions not supported by independent analysis.")


# ── Module-level interface (required by concept explorer extractor) ──────────
params = DPFPlantParams()
results = params.compute()

# Post-hoc scaling to 1000 MWe reference (α = 0.6 economy-of-scale exponent)
# Since native power ≈ 1000 MWe (200 modules × 5 MW), scaling factor ≈ 1.
_ALPHA = 0.6
_p_native = results["power"]["p_net_plant"]
_factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)
_overnight_per_kw = results["costs"]["overnight_capital"] * 1e3 / max(_p_native, 1.0)

scaled_headline = {
    "p_net_mw": 1000.0,
    "lcoe_per_mwh": results["economics"]["lcoe_USD_per_MWh"] * _factor,
    "overnight_per_kw": _overnight_per_kw * _factor,
}


if __name__ == "__main__":
    main()
