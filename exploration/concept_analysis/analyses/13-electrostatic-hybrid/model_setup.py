"""
Electrostatic Hybrid (D-T) LCOE Model — Avalanche Energy Orbitron
==================================================================
1cFE First Pass Concept Analysis
Concept: Orbitron — crossed-field magneto-electrostatic D-T fusion device
Company: Avalanche Energy (Seattle, WA)

This is a back-solve viability model, not a conventional LCOE model. The Orbitron
has not demonstrated Q>1 in any configuration, and no commercial plant architecture
exists. The appropriate TEA treatment sweeps Q_engineering and capital cost per kWe
to identify which combinations yield commercially viable LCOE ≤ $100/MWh.

Key physics: 300 kV cathode potential accelerates D-T ions to fusion energies. A
weak magnetic field (~0.5 T HTS, up from ~0.05 T permanent magnets) provides E×B
electron confinement. Ion density enhancement above the space-charge limit — the
concept's central claim — is supported by PIC simulation only; experimental
validation is ongoing.

Cost structure diverges completely from tokamak TEA:
  - Magnets (CAS22 C220103): near-zero (0.5 T HTS pair, no REBCO bottleneck)
  - Breeding blanket (C220101): ABSENT — tritium purchased indefinitely
  - Plasma heating (C220104): replaced by HV power supply + ion gun array
  - HV power supply (C220107): novel dominant account
  - Per-module neutron shielding: novel high-uncertainty account
  - Tritium fuel cost: permanent OPEX (no breeding), dominant at low Q

Net-power break-even: Q_engineering = 1/η.
  - Thermoelectric (η=12%): break-even at Q ≈ 8.3
  - Turbine-array  (η=30%): break-even at Q ≈ 3.3
The baseline default uses Q=10 at η=12% (above thermoelectric break-even).

Economy-of-scale exponent α=0.6 used for 1 GWe normalization in scaled_headline.
Post-hoc scaling applied to native power without modifying physics parameters.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Key references:
  - Lawson et al., AIP Advances 14(8), 085025 (2024) — Orbitron full paper (OSTI 2582151)
  - Avalanche Energy CWFest 2023 blog — operating point targets
  - Avalanche Energy 300 kV milestone press release (2025) — HV feedthrough achievement
  - Avalanche Energy $29M Series A press release (2026) — SC magnet, FusionWERX
  - APS DPP 2023 abstracts — >10^13 n/s capability, >100 keV D ion confinement
  - analysis.md §Section 5 — parameter table and confidence ratings
  - 1costingfe costing_constants.yaml — scaling law reference values
"""

import math
from dataclasses import dataclass

# === Reference power levels for CAS scaling laws (from 1costingfe) ===
P_TH_REF = 2500.0   # Reference thermal power [MW]
P_ET_REF = 1100.0   # Reference gross electric power [MW]


@dataclass
class OrbitronPlantParams:
    """
    Parameterized Orbitron back-solve LCOE model.

    Because Q>1 has not been demonstrated, Q_engineering and capital_cost_per_kWe
    are the primary sweep axes. All other parameters either come from published
    sources or documented analogues.
    """

    # ===================================================================
    # POWER BALANCE PARAMETERS
    # ===================================================================

    Q_engineering: float = 10.0
    """Engineering Q: ratio of fusion power to total electrical input.
    Source: Not demonstrated. Near-term target is Q≈1 (1 kW fusion / 1 kW input)
    per CWFest blog [avalanche-cwfest2023-blog.md §Fusion rate scaling].
    Net-power break-even is Q_engineering = 1/η: ≈8.3 for η=12% thermoelectric,
    ≈3.3 for η=30% turbine-array. Default Q=10 is the minimum physically feasible
    thermoelectric baseline (yields ~16% net fraction above break-even).
    Ref: analysis.md §Section 2 (High-leverage parameters).
    HIGH UNCERTAINTY — this is the primary sweep axis for the back-solve."""

    thermal_efficiency: float = 0.35
 # standardized from 0.12 per scoring_framework.md (Energy Capture: Thermal (unspecified))
    """Thermal-to-electric conversion efficiency.
    Source: No conversion system designed. Company states "thermal cycle with turbines"
    [avalanche-orbitron-page.md] but conventional turbines are impractical below ~1 MWe.
    Thermoelectric conversion at kWe scale: ~5–15%.
    Multi-module turbine array (>1 MWe aggregate): ~25–35% possible.
    Ref: analysis.md §Section 2 (Challenge 3), §Section 3 (Energy Conversion TRL 1–2).
    HIGH UNCERTAINTY — baseline uses 12% (thermoelectric scenario)."""

    p_input_module_kW: float = 1.0
    """Total electrical input power per module [kWe].
    Source: CWFest blog target operating point: 600 W cathode + 400 W ion guns = 1 kW
    [avalanche-cwfest2023-blog.md §Fusion rate scaling].
    Ref: analysis.md §Section 5 (Input power row).
    MODERATE UNCERTAINTY — aspirational target, not a measured operating point."""

    n_modules: int = 1000
    """Number of Orbitron modules in the commercial plant.
    Source: No plant architecture exists. The company states "stacked for near-endless
    power applications" [avalanche-orbitron-page.md] without specifying module count.
    At Q=10, η=12%, 1 kWe input: each module yields ~0.2 kWe net; 1000 modules → ~0.2 MWe.
    This is sub-commercial scale — net power scales with (Q×η − 1) × n_modules.
    HIGH UNCERTAINTY — ASSUMED for order-of-magnitude sizing only."""

    plant_availability: float = 0.85
    """Plant capacity factor / availability.
    Source: Steady-state operation mode is explicitly emphasized (300 kV sustained for
    hours) [avalanche-300kv-press-release.md]. Favorable for capacity factor vs. pulsed.
    Cathode and HV feedthrough lifetime under neutron bombardment is the main limit.
    Using 85% — analogy to industrial steady-state continuous process plants.
    Ref: analysis.md §Section 5 (Plant capacity factor row).
    MODERATE UNCERTAINTY."""

    plant_lifetime_years: float = 30.0
    """Plant economic lifetime [years].
    Source: No Orbitron-specific estimate. Shorter than 40-yr tokamak assumption given
    early-stage concept and unknown cathode/HV lifetime. Using 30 yr.
    MODERATE UNCERTAINTY — ASSUMED by analogy to small modular concepts."""

    noak: bool = False
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    Source: The Orbitron has never been built at commercial scale. FOAK is appropriate.
    Mass manufacturing of modules is the company's claimed cost mechanism for NOAK."""

    # ===================================================================
    # GEOMETRY (per module — compact cylindrical device)
    # ===================================================================

    device_radius_m: float = 0.10
    """Inner radius of Orbitron vacuum chamber [m].
    Source: CWFest blog describes "desktop" device; AIP Advances paper Figure 1 shows
    ~10–20 cm diameter device [osti-pages-servlets-purl-2582151.md §III.A].
    Using 0.10 m (10 cm radius) as per-module inner cavity radius.
    MODERATE UNCERTAINTY — no precise dimension in public sources."""

    device_length_m: float = 0.20
    """Active length of Orbitron device [m].
    Source: Not published. Estimated from device photos and AIP Advances Fig 1.
    Ref: osti-pages-servlets-purl-2582151.md §III.A (device description).
    HIGH UNCERTAINTY — ASSUMED from visual inspection of published images."""

    shield_thickness_m: float = 0.30
    """Neutron shielding thickness per module [m].
    Source: CWFest blog describes a "concrete castle" for the Marty prototype
    [avalanche-cwfest2023-blog.md §Marty prototype]. Compact shielding for a
    stacked-module plant is a key unsolved design problem. 0.30 m concrete is
    the minimum for meaningful 14 MeV neutron attenuation at low flux.
    Ref: analysis.md §Section 3 (Neutron Shielding TRL 5–6 / 2–3).
    HIGH UNCERTAINTY — per-module shielding geometry is entirely undefined."""

    # ===================================================================
    # CAS22 COMPONENT COSTS
    # ===================================================================

    hv_power_supply_cost_per_kW_USD: float = 300.0
    """HV power supply + ion gun system cost per kW of input power [$/kW_input].
    Source: No Orbitron cost data. Industrial 300 kV sustained power supplies used
    in particle accelerators and electron beam systems: ~$200–500/kW.
    Ion gun system is additional; 300 kW class: ~$100–300/kW.
    Ref: analysis.md §Section 7 (CAS table: HV power supply ~$100–500/kW).
    NOTE: At 1 kWe input, $/kW_input × 1 kW = $100–$2,000 — always below the
    $50k/module FOAK floor in C220107. Sweeping this parameter at 1 kWe module
    scale has zero LCOE effect. Use hv_per_module_cost_M_USD for sensitivity sweeps.
    HIGH UNCERTAINTY — ASSUMED from accelerator/HVDC industrial analogy."""

    hv_per_module_cost_M_USD: float = 0.0
    """HV power supply + ion gun direct per-module cost override [$M/module].
    If > 0, overrides the $/kW_input × input_power calculation and bypasses
    the $50k FOAK floor in C220107. Use this parameter for sensitivity sweeps at
    1 kWe module scale, where $/kW_input is meaningless (floor always dominates).
    Range: $5k–$200k/module spans the accelerator/HVDC analogy for 1–100 kWe
    sustained 300 kV supplies per analysis.md §Section 7 CAS table.
    Default 0.0 = use existing per-kW calculation with FOAK floor (baseline).
    Ref: F-1 fix — sweep axis for HV cost at module scale."""

    sc_magnet_cost_M_USD: float = 0.05
    """Superconducting HTS magnet system cost per module [$M].
    Source: Two HTS coil pairs targeting 0.5 T at midplane per AIP Advances paper
    [osti-pages-servlets-purl-2582151.md §III.C]. The 0.5 T field is orders of
    magnitude below MFE requirements. HTS coils at this scale (~20 cm bore, 0.5 T)
    require only ~50–200 m of REBCO tape per pair. At $100/m tape + winding/cryostat:
    ~$20–50k material cost; FOAK total estimate ~$50k/module.
    Ref: analysis.md §Section 3 (Aux Magnetic System), §Section 4 (SC Magnets).
    MODERATE UNCERTAINTY."""

    cathode_cost_M_USD: float = 0.1
    """Vacuum chamber and cathode assembly cost per module [$M].
    Source: No Orbitron cost data. Desktop-scale vacuum system with HV feedthrough.
    The proprietary HV feedthrough is Avalanche's key innovation — FOAK cost assumed
    comparable to precision HV industrial components at this scale.
    Ref: avalanche-300kv-press-release.md §"novel HV feedthrough design".
    HIGH UNCERTAINTY — ASSUMED."""

    shielding_cost_per_m3_M_USD: float = 0.015
    """Per-module neutron shielding cost [M$/m³ of shielding volume].
    Source: Analysis §Section 3 warns the "concrete castle" could make modular
    architecture "economically self-defeating." Raw concrete at $200–500/m³ gives
    ~$75–185/module — far too low for a commercial integrated shielding enclosure.
    At $15,000/m³ (concrete + structural supports + radiation doors + module
    integration hardware), shield vol ≈ 0.37 m³ → ~$5,500/module FOAK lower bound.
    This baseline reflects the minimum plausible enclosure; actual cost is unknown
    and should be treated as a sensitivity axis (see shielding sweep in main()).
    Ref: analysis.md §Section 3 (Neutron Shielding TRL 5–6 / 2–3), F-2 fix.
    HIGH UNCERTAINTY — per-module shielding geometry is entirely undefined."""

    cathode_lifetime_FPY: float = 2.0
    """Cathode and first-surface lifetime under neutron bombardment [full-power-years].
    Source: No data. 14 MeV neutron damage to tungsten cathode is a critical unknown.
    Assuming 2 FPY as conservative estimate — shorter than first-wall in tokamaks due
    to direct particle bombardment geometry and high electric field stress.
    Ref: analysis.md §Section 5 (Cathode lifetime — truly-unknown gap).
    HIGH UNCERTAINTY — no fission or fusion analog; requires dedicated test data."""

    # ===================================================================
    # TRITIUM FUEL (PURCHASED — NO BREEDING BLANKET)
    # ===================================================================

    tritium_price_per_g_USD: float = 35000.0
    """Tritium market price [$/g].
    Source: >$35,000/g cited across multiple analyses.
    Ref: 21-spherical-tokamak-hts.md §Section 4 (cross-reference), analysis.md §S4.
    The Orbitron has no breeding blanket; tritium is purchased indefinitely.
    An MoU with Fusion Fuel Cycles (FFC) covering breeding blankets was announced
    (April 2025) [prnewswire-news-releases-avalanche-energy-announces-new.md] but
    no blanket design, timeline, or specification has been published.
    MODERATE UNCERTAINTY — price from current CANDU byproduct market."""

    tritium_consumed_g_per_MJ_fusion: float = 3.47e-6
    """Tritium consumed per MJ of fusion energy [g/MJ_fusion].
    Source: D-T reaction: each fusion consumes 1 T atom (3.016 amu) and yields 17.58 MeV.
    Fusions per MJ = 10^6 J / 2.817×10^-12 J/fusion = 3.55×10^17 /MJ.
    T mass per fusion = 3.016 / (6.022×10^23) g = 5.01×10^-24 g.
    At 100% burn: 3.55×10^17 × 5.01×10^-24 = 1.78×10^-6 g/MJ.
    With 5% burn fraction and 95% fuel recovery: makeup_factor = (1 − 0.95×0.95)/0.05 = 1.95.
    Net consumed = 1.78×10^-6 × 1.95 = 3.47×10^-6 g/MJ.
    Ref: 1costingfe costing_constants.yaml (burn_fraction=0.05, fuel_recovery=0.95)."""

    # ===================================================================
    # FINANCIAL
    # ===================================================================

    interest_rate: float = 0.10
    """Real discount rate (WACC) for FOAK novel energy technology.
    Source: Higher than 1costingfe default (0.08) given FOAK status and unproven physics.
    10% reflects private-equity-style risk premium appropriate for pre-commercial fusion.
    Ref: Standard fusion FOAK financial modeling assumption.
    MODERATE UNCERTAINTY."""

    inflation_rate: float = 0.02
    """Inflation rate for levelized cost calculations.
    Ref: 1costingfe default."""

    construction_time_years: float = 4.0
    """Construction period [years].
    Source: Modular concept with factory-built units may allow faster deployment than
    conventional large plant. 4 years assumed for stacked-module plant assembly.
    Ref: ASSUMED — analogy to modular energy installations."""

    om_frac_of_capex: float = 0.04
    """Annual O&M cost as fraction of overnight capital.
    Source: No O&M data for Orbitron. Standard placeholder for novel fusion concepts:
    2–5% of CAPEX/yr. Using 4% (midpoint) for FOAK with unknown component lifetimes.
    Ref: analysis.md §Section 2 (Challenge 6: O&M uncharacterized), §Section 5."""

    def _compute_power(self) -> dict:
        """Layer 1: Power balance — derive fusion power from Q_engineering and input."""
        r = {}

        # Per-module power balance
        p_input_MW = self.p_input_module_kW / 1000.0  # kW → MW
        r["p_input_module_MW"] = p_input_MW

        # Fusion power per module: Q_engineering = p_fus / p_input
        p_fus_module = self.Q_engineering * p_input_MW
        r["p_fus"] = p_fus_module  # per module, MW

        # D-T: 80% neutron energy, 20% alpha
        r["p_neutron"] = p_fus_module * 0.80
        r["p_alpha"] = p_fus_module * 0.20

        # Thermal power per module: no blanket multiplication (no breeding blanket).
        # Alpha energy thermalizes in plasma and chamber walls.
        # Neutron energy deposited in shielding/chamber (captured as heat).
        p_th_module = p_fus_module  # M=1.0, no blanket
        r["p_th"] = p_th_module

        # Gross electric per module
        p_et_module = p_th_module * self.thermal_efficiency
        r["p_et"] = p_et_module

        # Recirculating power: input power + module-level auxiliaries
        # Aux: vacuum pump (~50 W) + cryo cryocooler (~50 W) + controls (~20 W) ≈ 120 W
        p_recirc_module = p_input_MW + 0.00012  # 1 kW input + ~120 W aux, in MW
        r["p_recirc"] = p_recirc_module

        # Net electric per module
        p_net_module = p_et_module - p_recirc_module
        r["p_net"] = p_net_module

        # Q derived quantities
        r["Q_sci"] = self.Q_engineering  # for steady-state, Q_sci ≈ Q_eng
        r["Q_eng"] = self.Q_engineering
        r["recirc_fraction"] = p_recirc_module / p_et_module if p_et_module > 0 else float("inf")

        # Break-even Q (net power = 0 condition)
        # p_net = p_input × (Q×η − 1) − p_aux ≈ p_input × (Q×η − 1)
        # Break-even: Q_be = (1 + p_aux/p_input) / η ≈ 1/η
        r["Q_breakeven"] = (p_input_MW + 0.00012) / (p_input_MW * self.thermal_efficiency)

        # Plant-level (all modules)
        r["p_fus_plant"] = p_fus_module * self.n_modules
        r["p_th_plant"] = p_th_module * self.n_modules
        r["p_et_plant"] = p_et_module * self.n_modules
        r["p_net_plant"] = p_net_module * self.n_modules

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Per-module geometry for cost scaling."""
        r = {}

        ri = self.device_radius_m
        L = self.device_length_m
        t_sh = self.shield_thickness_m

        # Inner chamber volume (cylindrical)
        r["chamber_vol_m3"] = math.pi * ri**2 * L

        # Shield shell volume (cylindrical annulus around device)
        r_sh_out = ri + t_sh
        L_sh = L + 2 * t_sh  # shield extends axially too
        r["shield_vol_m3"] = math.pi * (r_sh_out**2 - ri**2) * L_sh

        # Total module footprint (shield outer envelope)
        r["module_footprint_m2"] = math.pi * r_sh_out**2

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment — per-module then plant-wide."""
        r = {}

        p_et_plant = max(power["p_et_plant"], 0.001)  # MW, avoid div/0
        p_th_plant = max(power["p_th_plant"], 0.001)
        p_net_plant = max(power["p_net_plant"], 0.001)

        # --- Per-module accounts ---

        # C220101: First Wall / Blanket — OVERRIDE: NO BLANKET
        # The Orbitron has no breeding blanket. Chamber walls are tungsten/SS vacuum
        # components. Replacement cost modeled under CAS72 (cathode replacement).
        # Using a nominal structural wall cost: 0.01 M$ per module.
        r["C220101"] = self.cathode_cost_M_USD * 0.2  # OVERRIDE: chamber wall only, ~$20k/module

        # C220102: Neutron Shield — per-module concrete shielding
        # OVERRIDE: per-module shielding replaces standard toroidal shield formula.
        r["C220102"] = self.shielding_cost_per_m3_M_USD * geom["shield_vol_m3"]

        # C220103: Coils (SC magnet system per module)
        # OVERRIDE: 0.5 T HTS coil pair, compact and cheap vs tokamak-scale SC.
        # Source: AIP Advances paper §III.C — two HTS coil pairs at midplane.
        r["C220103"] = self.sc_magnet_cost_M_USD  # OVERRIDE: HTS pair per module

        # C220104: Supplementary Heating — OVERRIDE: replaced by ion gun array
        # Avalanche uses electrostatic acceleration (cathode voltage) and an ion gun
        # array as the "heating" system. Cost folded into C220107 (power supply).
        r["C220104"] = 0.0  # OVERRIDE: ion gun cost is part of HV power supply system

        # C220105: Primary Structure (cathode + vacuum vessel assembly)
        # OVERRIDE: per-module cathode and vacuum assembly.
        r["C220105"] = self.cathode_cost_M_USD  # OVERRIDE: cathode/vacuum vessel per module

        # C220106: Vacuum System (pumps + feedthroughs per module)
        # Small vacuum system for desktop device. Ion pumps + turbo + HV feedthrough.
        # Estimate: ~$50k–$100k per module at FOAK pricing.
        r["C220106"] = 0.08  # ASSUMED: $80k per module (FOAK), M$

        # C220107: Power Supplies — OVERRIDE: HV power supply + ion gun system
        # The dominant novel account for the Orbitron. 300 kV sustained supply.
        # A sustained 300 kV supply has a minimum cost floor regardless of power level
        # (specialized HV insulation, enclosure, control). Floor: $50k/module at FOAK.
        # Source: analysis.md §Section 7, CAS table — ~$100–500/kW_input for HV supply.
        # NOTE: At 1 kWe input, $/kW_input × 1 kW << $50k floor, so the floor always
        # dominates. hv_per_module_cost_M_USD provides a direct per-module override for
        # meaningful sensitivity sweeps at 1 kWe module scale (F-1 fix).
        if self.hv_per_module_cost_M_USD > 0:
            hv_cost_per_module = self.hv_per_module_cost_M_USD
        else:
            hv_cost_per_module = max(
                self.hv_power_supply_cost_per_kW_USD * self.p_input_module_kW / 1e6,
                0.05   # $50k minimum per module (300 kV supply FOAK floor), M$
            )
        r["C220107"] = hv_cost_per_module  # OVERRIDE: HV PS + ion gun per module

        # C220108: Target Factory — NOT APPLICABLE for steady-state electrostatic device
        r["C220108"] = 0.0

        # C220109: Direct Energy Converter — NOT APPLICABLE (thermal conversion)
        r["C220109"] = 0.0

        # C220110: Remote Handling — compact modules, no complex RH needed
        # Simple robotic module swap; no in-vessel transporter.
        r["C220110"] = 0.005  # ASSUMED: $5k/module robotic handling equipment, M$

        # C220111: Installation labor (14% of reactor subtotal per 1costingfe)
        subtotal_before_install = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110"
        ])
        r["C220111"] = 0.14 * subtotal_before_install

        # C220112: Isotope Separation — 0 (no breeding; tritium purchased)
        r["C220112"] = 0.0

        # Per-module subtotal
        per_module_subtotal = subtotal_before_install + r["C220111"] + r["C220112"]
        r["CAS22_per_module"] = per_module_subtotal

        # --- Plant-wide accounts (scaled to full plant) ---

        # C220200: Main Coolant System — LOW-COST (no large primary loop needed)
        # Each module has its own small thermal circuit. Aggregate is not a single
        # large coolant loop. Scaled analogy to distributed thermal systems.
        C220201 = 166.0 * (p_net_plant / 1000.0)         # Primary (1costingfe formula)
        C220202 = 40.6 * (p_th_plant / 3500.0) ** 0.55   # Intermediate
        r["C220200"] = C220201 + C220202

        # C220300: Aux Cooling + Cryoplant
        # Small cryoplant for HTS coils (0.5 T, compact — very small cryo load).
        C220301 = 1.1e-3 * p_th_plant
        p_cryo_MW = 0.005 * self.n_modules  # ~5 W per module cryo load
        C220302 = 200.0 * (max(p_cryo_MW, 0.01) / 30.0) ** 0.7
        r["C220300"] = C220301 + C220302

        # C220400: Radioactive Waste Management (D-T, 14 MeV neutrons)
        # 1costingfe formula: 1.96 × (p_th / 1000)
        r["C220400"] = 1.96 * (p_th_plant / 1000.0)

        # C220500: Fuel Handling & Storage (D-T: tritium processing)
        # Purchased tritium supply chain + storage + handling for multi-module plant.
        # D-T base: 120 M$ at 1 GWe. Scaled down for modest net power.
        fuel_handling_base = 120.0
        r["C220500"] = fuel_handling_base * (p_net_plant / 1000.0) ** 0.7

        # C220600: Other Reactor Plant Equipment
        r["C220600"] = 11.5 * (p_net_plant / 1000.0) ** 0.8

        # C220700: Instrumentation & Control
        # Many modules require distributed I&C for HV monitoring, module health, etc.
        # Scaled up 1.5× from 1costingfe formula due to module count complexity.
        r["C220700"] = 85.0 * (p_th_plant / 3500.0) ** 0.65 * 1.5

        # Plant-wide subtotal
        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"
        ])

        # Total CAS22
        r["CAS22"] = r["CAS22_per_module"] * self.n_modules + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, cas22: dict) -> dict:
        """Layer 4: CAS10-60 capital costs."""
        r = {}

        p_et_plant = max(power["p_et_plant"], 0.001)
        p_net_plant = max(power["p_net_plant"], 0.001)

        # === CAS10: Pre-construction ===
        # D-T facility licensing even for small device
        r["CAS10"] = (3.0 + (20.0 if not self.noak else 4.0) + 2.0 + 1.0 + 1.0
                      + 0.25 * p_net_plant * 10000 / 1e6  # land
                      + (5.0 if not self.noak else 2.5))   # D-T licensing

        # === CAS21: Buildings ===
        # D-T facility, but modular plant in industrial warehouse-style building.
        # No large tokamak building needed. Scale down reactor_building and hot_cell.
        bld_per_kW = {
            "site_improvements": 85.0,
            "reactor_building": 60.0,   # smaller than tokamak — no large vacuum vessel
            "hot_cell": 50.0,           # needed for D-T activation management
            "turbine_building": 30.0,   # small (thermoelectric or compact turbine array)
            "fuel_storage": 9.0,        # tritium storage
            "control_room": 14.0,
            "security": 3.5,
            "ventilation_hvac": 10.0,
            "misc_buildings": 20.0,
        }
        total_bld_per_kW = sum(bld_per_kW.values())
        r["CAS21"] = total_bld_per_kW * p_et_plant / 1000.0   # M$
        r["CAS21_detail"] = {k: v * p_et_plant / 1000.0 for k, v in bld_per_kW.items()}

        # === CAS22: Reactor Plant Equipment ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Turbine Plant Equipment ===
        # Thermoelectric or small turbine array. Lower cost per MWe than large steam.
        turbine_per_mw = 0.10   # ASSUMED: thermoelectric array or small ORC units
        r["CAS23"] = p_et_plant * turbine_per_mw

        # === CAS24: Electric Plant Equipment ===
        r["CAS24"] = p_et_plant * 0.08418   # 1costingfe default

        # === CAS25: Miscellaneous Plant Equipment ===
        r["CAS25"] = p_et_plant * 0.05124   # 1costingfe default

        # === CAS26: Heat Rejection ===
        r["CAS26"] = p_et_plant * 0.03416   # 1costingfe default

        # === CAS27: Special Materials ===
        # D-T: no FLiBe, no large REBCO. Minimal special materials.
        r["CAS27"] = 2.0 * (p_net_plant / 1000.0)

        # === CAS28: Digital Twin ===
        r["CAS28"] = 5.0

        # === CAS29: Contingency (15% FOAK) ===
        cas20_sub = sum(r[k] for k in ["CAS21", "CAS22", "CAS23", "CAS24",
                                        "CAS25", "CAS26", "CAS27", "CAS28"])
        r["CAS29"] = (0.15 if not self.noak else 0.0) * cas20_sub

        r["CAS20"] = cas20_sub + r["CAS29"]

        # === CAS30: Indirect Costs ===
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / 6.0)

        # === CAS40: Owner's Costs ===
        # 1costingfe: owner_cost_dt=39 M$ at 1 GWe, scaled by (P_net/1GWe)^0.5
        r["CAS40"] = 39.0 * (p_net_plant / 1000.0) ** 0.5

        # === CAS50: Supplementary Costs ===
        shipping = 0.015 * r["CAS20"]
        spare_parts = 0.03 * (r["CAS22"] + r["CAS23"] + r["CAS24"])
        startup_tritium = 40.0 * (p_net_plant / 1000.0)   # M$ — tritium startup inventory
        decom = 127.0 * (p_net_plant / 1000.0)             # M$ — D-T decommissioning
        insurance = 0.015 * (r["CAS20"] + r["CAS30"])
        r["CAS50"] = shipping + spare_parts + startup_tritium + decom + insurance

        # === Overnight Capital ===
        r["overnight_capital"] = r["CAS10"] + r["CAS20"] + r["CAS30"] + r["CAS40"] + r["CAS50"]

        # === CAS60: Interest During Construction ===
        i = self.interest_rate
        T = self.construction_time_years
        if i > 0 and T > 0:
            f_idc = ((1 + i)**T - 1) / (i * T) - 1
        else:
            f_idc = 0.0
        r["CAS60"] = f_idc * r["overnight_capital"]
        r["f_IDC"] = f_idc

        r["total_capital"] = r["overnight_capital"] + r["CAS60"]

        if power["p_net_plant"] > 0:
            r["specific_capital_USD_per_kWe"] = r["total_capital"] * 1e6 / (power["p_net_plant"] * 1e3)
        else:
            r["specific_capital_USD_per_kWe"] = float("inf")

        return r

    def _compute_economics(self, power: dict, costs: dict, cas22: dict) -> dict:
        """Layer 5: CAS70-90 annualized costs and LCOE."""
        r = {}

        p_net_plant = power["p_net_plant"]

        # Capital Recovery Factor
        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1 + i)**n / ((1 + i)**n - 1)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]

        # === CAS71: Annual O&M (fraction of overnight capital, levelized with inflation) ===
        g = self.inflation_rate
        Tc = self.construction_time_years
        annual_om_base = self.om_frac_of_capex * costs["overnight_capital"]
        A1 = annual_om_base * (1 + g)**Tc
        if abs(i - g) > 1e-10:
            pv_growing = A1 * (1 - ((1 + g) / (1 + i))**n) / (i - g)
        else:
            pv_growing = A1 * n / (1 + i)
        r["CAS71"] = crf * pv_growing

        # === CAS72: Cathode/First-Surface Scheduled Replacement ===
        # Replace per-module cathode assembly every cathode_lifetime_FPY.
        eff_yrs_per_replacement = self.cathode_lifetime_FPY / self.plant_availability
        n_replacements = max(0, int(math.ceil(n / eff_yrs_per_replacement)) - 1)
        replacement_cost = cas22["C220105"] * self.n_modules  # full cathode fleet
        pv_replacements = sum(
            replacement_cost / (1 + i) ** (k * eff_yrs_per_replacement)
            for k in range(1, n_replacements + 1)
            if k * eff_yrs_per_replacement < n
        )
        r["CAS72"] = crf * pv_replacements
        r["n_cathode_replacements"] = n_replacements

        r["CAS70"] = r["CAS71"] + r["CAS72"]

        # === CAS80: Tritium Fuel Cost (PURCHASED — no breeding blanket) ===
        # Fusion energy per year: p_fus_plant [MW] × 8760 hr × 3600 s/hr × availability
        p_fus_plant_MW = power["p_fus_plant"]
        annual_fusion_MWh = p_fus_plant_MW * 8760 * self.plant_availability
        annual_fusion_MJ = annual_fusion_MWh * 3600

        annual_tritium_g = self.tritium_consumed_g_per_MJ_fusion * annual_fusion_MJ
        annual_tritium_cost_M = annual_tritium_g * self.tritium_price_per_g_USD / 1e6

        # Deuterium cost (negligible by comparison)
        annual_deuterium_cost_M = annual_tritium_g * 2175.0 / (3.016 / 2.014) / 1e6

        r["CAS80"] = annual_tritium_cost_M + annual_deuterium_cost_M
        r["CAS80_tritium"] = annual_tritium_cost_M
        r["CAS80_deuterium"] = annual_deuterium_cost_M
        r["annual_tritium_g"] = annual_tritium_g

        # === LCOE ===
        annual_revenue_req = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_revenue_req

        annual_energy_MWh = 8760 * p_net_plant * self.plant_availability
        r["annual_energy_MWh"] = annual_energy_MWh

        if annual_energy_MWh > 0 and p_net_plant > 0:
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

    def compute(self) -> dict:
        """Compute LCOE and all intermediate values. Returns nested dict."""
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


# ===================================================================
# Module-level instances (required by concept explorer)
# ===================================================================
params = OrbitronPlantParams()
results = params.compute()

# Post-hoc scaling to 1000 MWe reference (economy-of-scale exponent α=0.6)
_ALPHA = 0.6
_p_native = results["power"].get("p_net_plant", results["power"]["p_net"])
if _p_native > 0:
    _factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)
    _overnight = results["costs"]["overnight_capital"] * 1e3 / _p_native
    scaled_headline = {
        "p_net_mw": 1000.0,
        "lcoe_per_mwh": results["economics"]["lcoe_USD_per_MWh"] * _factor,
        "overnight_per_kw": _overnight * _factor,
    }
else:
    scaled_headline = {
        "p_net_mw": 1000.0,
        "lcoe_per_mwh": float("inf"),
        "overnight_per_kw": float("inf"),
    }


# ===================================================================
# PRINT RESULTS
# ===================================================================

def print_results(p: OrbitronPlantParams, res: dict, label: str = ""):
    """Pretty-print CAS-structured results."""
    power = res["power"]
    cas22 = res["cas22"]
    costs = res["costs"]
    econ = res["economics"]

    title = f"Electrostatic Hybrid D-T (Orbitron) — {label}" if label else "Electrostatic Hybrid D-T (Orbitron)"
    print("=" * 70)
    print(title)
    print("=" * 70)

    print(f"\n--- Key Input Parameters ---")
    print(f"  Q_engineering:              {p.Q_engineering:.1f}  (break-even = {power['Q_breakeven']:.1f})")
    print(f"  Thermal efficiency:         {p.thermal_efficiency:.1%}")
    print(f"  Input power per module:     {p.p_input_module_kW:.1f} kWe")
    print(f"  Number of modules:          {p.n_modules:,}")
    print(f"  Plant availability:         {p.plant_availability:.1%}")
    print(f"  FOAK/NOAK:                  {'NOAK' if p.noak else 'FOAK'}")
    print(f"  Plant lifetime:             {p.plant_lifetime_years:.0f} years")
    print(f"  Interest rate:              {p.interest_rate:.1%}")

    print(f"\n--- Power Balance (per module + plant) ---")
    print(f"  Input power / module:       {power['p_input_module_MW']*1000:.1f} kWe")
    print(f"  Fusion power / module:      {power['p_fus']*1000:.3f} kWe  (Q={p.Q_engineering:.1f})")
    print(f"  Gross electric / module:    {power['p_et']*1000:.3f} kWe  (η={p.thermal_efficiency:.0%})")
    print(f"  Recirc. power / module:     {power['p_recirc']*1000:.3f} kWe")
    print(f"  Net electric / module:      {power['p_net']*1000:.3f} kWe")
    print(f"  Recirculating fraction:     {power['recirc_fraction']:.1%}")
    print(f"  ─────── Plant ({p.n_modules:,} modules) ───────")
    print(f"  Fusion power (plant):       {power['p_fus_plant']*1000:.1f} kWe  ({power['p_fus_plant']:.4f} MW)")
    print(f"  Gross electric (plant):     {power['p_et_plant']*1000:.1f} kWe")
    print(f"  Net electric (plant):       {power['p_net_plant']*1000:.2f} kWe  ({power['p_net_plant']:.4f} MW)")

    print(f"\n--- CAS22: Reactor Plant Equipment ---")
    print(f"  Per-module accounts (× {p.n_modules:,} modules):")
    cas22_labels = {
        "C220101": "Chamber Wall (no blanket)",
        "C220102": "Neutron Shield",
        "C220103": "HTS Magnet (0.5 T pair)",
        "C220104": "Supplementary Heating",
        "C220105": "Cathode/Vacuum Assembly",
        "C220106": "Vacuum System",
        "C220107": "HV Power Supply + Ion Gun",
        "C220108": "Target Factory",
        "C220109": "Direct Energy Converter",
        "C220110": "Remote Handling",
        "C220111": "Installation",
        "C220112": "Isotope Separation",
    }
    overrides = {"C220101", "C220103", "C220104", "C220105", "C220107", "C220108", "C220110"}
    for code, lbl in cas22_labels.items():
        val = cas22.get(code, 0.0)
        tag = " [override]" if code in overrides else ""
        val_fleet = val * p.n_modules
        if val > 0 or code in overrides:
            print(f"    {code} {lbl:<30s} ${val*1000:.1f}k/mod  ${val_fleet:.2f}M fleet{tag}")
    print(f"  ─────────────────────────────────────────────")
    print(f"    Per-module subtotal:       ${cas22['CAS22_per_module']*1000:.1f}k   "
          f"${cas22['CAS22_per_module']*p.n_modules:.2f}M fleet")

    print(f"  Plant-wide accounts:")
    pw_labels = {
        "C220200": "Coolant Systems",
        "C220300": "Aux Cooling + Cryoplant",
        "C220400": "Rad Waste Management",
        "C220500": "Tritium Handling (purchased)",
        "C220600": "Other Equipment",
        "C220700": "Instrumentation & Control",
    }
    for code, lbl in pw_labels.items():
        val = cas22.get(code, 0.0)
        if val > 0.01:
            print(f"    {code} {lbl:<30s} ${val:.2f}M")
    print(f"  ─────────────────────────────────────────────")
    print(f"    Plant-wide subtotal:       ${cas22['CAS22_plant_wide']:.2f}M")
    print(f"  CAS22 Total:                ${cas22['CAS22']:.2f}M")

    print(f"\n--- Capital Costs (CAS10-60) ---")
    for acc, lbl in [("CAS10", "Pre-construction"), ("CAS21", "Buildings"),
                     ("CAS22", "Reactor Plant Equipment"), ("CAS23", "Turbine Plant"),
                     ("CAS24", "Electric Plant"), ("CAS25", "Misc Plant"),
                     ("CAS26", "Heat Rejection"), ("CAS27", "Special Materials"),
                     ("CAS28", "Digital Twin"), ("CAS29", "Contingency")]:
        print(f"  {acc} {lbl:<28s} ${costs[acc]:>8.1f}M")
    print(f"  {'─'*50}")
    print(f"  CAS20 Direct Costs:                 ${costs['CAS20']:>8.1f}M")
    print(f"  CAS30 Indirect Costs:               ${costs['CAS30']:>8.1f}M")
    print(f"  CAS40 Owner's Costs:                ${costs['CAS40']:>8.1f}M")
    print(f"  CAS50 Supplementary:                ${costs['CAS50']:>8.1f}M")
    print(f"  {'─'*50}")
    print(f"  Overnight Capital:                  ${costs['overnight_capital']:>8.1f}M")
    print(f"  CAS60 IDC (f={costs['f_IDC']:.3f}):             ${costs['CAS60']:>8.1f}M")
    print(f"  {'═'*50}")
    print(f"  Total Capital:                      ${costs['total_capital']:>8.1f}M")
    if costs["specific_capital_USD_per_kWe"] < 1e9:
        print(f"  Specific Capital:                   ${costs['specific_capital_USD_per_kWe']:>8.0f} $/kWe")
    else:
        print(f"  Specific Capital:                   N/A (negative or zero net power)")

    print(f"\n--- Annual Costs (CAS70-90) ---")
    print(f"  CAS90 Capital charge (CRF={econ['CRF']:.4f}): ${econ['CAS90']:>8.2f}M/yr")
    print(f"  CAS71 O&M (levelized):              ${econ['CAS71']:>8.2f}M/yr")
    print(f"  CAS72 Cathode replacement:          ${econ['CAS72']:>8.2f}M/yr  ({econ['n_cathode_replacements']} replacements)")
    print(f"  CAS70 Total O&M:                    ${econ['CAS70']:>8.2f}M/yr")
    print(f"  CAS80 Tritium fuel (purchased):     ${econ['CAS80']:>8.2f}M/yr")
    print(f"    Tritium: {econ['annual_tritium_g']:,.1f} g/yr  ×  ${p.tritium_price_per_g_USD:,.0f}/g  = ${econ['CAS80_tritium']:.2f}M/yr")

    print(f"\n--- LCOE ---")
    print(f"  Annual net energy:          {econ['annual_energy_MWh']:,.0f} MWh")
    print(f"  Annual revenue requirement: ${econ['annual_revenue_req']:.2f}M")
    print(f"  ╔══════════════════════════════════════╗")
    if econ['lcoe_USD_per_MWh'] < 1e9:
        print(f"  ║  LCOE = {econ['lcoe_cents_per_kWh']:>8.1f} ¢/kWh             ║")
        print(f"  ║       = {econ['lcoe_USD_per_MWh']:>8.1f} $/MWh             ║")
    else:
        print(f"  ║  LCOE = UNDEFINED (net power ≤ 0)    ║")
    print(f"  ╚══════════════════════════════════════╝")
    if econ.get("capital_fraction"):
        print(f"  Capital (CAS90):            {econ['capital_fraction']:.1%}")
        print(f"  O&M (CAS70):               {econ['om_fraction']:.1%}")
        print(f"  Fuel/Tritium (CAS80):       {econ['fuel_fraction']:.1%}")


def sensitivity_sweep(base_p: OrbitronPlantParams, param_name: str,
                      values: list, label: str = "") -> list[dict]:
    """Single-parameter sensitivity sweep. Returns list of result dicts."""
    out = []
    for val in values:
        p2 = OrbitronPlantParams(**{**base_p.__dict__, param_name: val})
        r2 = p2.compute()
        pnet = r2["power"]["p_net_plant"]
        spec_cap = r2["costs"]["specific_capital_USD_per_kWe"]
        out.append({
            "param_value": float(val),
            "lcoe_USD_per_MWh": r2["economics"]["lcoe_USD_per_MWh"],
            "lcoe_cents_per_kWh": r2["economics"]["lcoe_cents_per_kWh"],
            "p_net_plant_MW": pnet,
            "specific_capital_USD_per_kWe": spec_cap,
        })
    return out


def back_solve_lcoe_surface():
    """
    Back-solve: sweep Q_engineering across three module-cost scenarios and print
    LCOE surface with verified specific capital ($/kWe) per cell.

    Capital scenario lever: cathode_cost_M_USD (the dominant per-module account).
    This represents the range from NOAK mass-manufactured modules to FOAK
    precision hardware. The actual specific capital ($/kWe) is computed per row —
    it varies strongly with Q because net power ∝ (Q×η − 1).

    Note on HV supply: at 1 kWe input, the $50k/module minimum floor always
    binds for any reasonable $/kW_input rate ($300/kW × 1 kW = $0.3k << $50k),
    so hv_power_supply_cost_per_kW_USD has no effect at this module scale (F-1).
    The cathode_cost_M_USD ($20–250k/module range) is the effective capital lever
    in this surface; see the sensitivity sweeps for the hv_per_module_cost_M_USD axis.
    """
    print("\n" + "=" * 70)
    print("BACK-SOLVE: LCOE Surface — Q_engineering × Module Capital Scenarios")
    print("(Actual computed $/kWe shown per cell — not assumed from inputs)")
    print("  Capital lever: cathode/vacuum assembly cost per module")
    print("  [Optimistic = $30k/mod NOAK | Baseline = $100k/mod FOAK | Pessimistic = $250k/mod FOAK]")
    print("=" * 70)

    # Three capital scenarios: vary cathode_cost_M_USD (dominant per-module account).
    # Optimistic: mass-manufactured module at NOAK learning rates (~$30k/module)
    # Baseline: FOAK precision hardware (~$100k/module, default)
    # Pessimistic: conservative FOAK estimate for novel HV device (~$250k/module)
    cap_scenarios = [
        ("Optimistic $30k/mod",  0.030),
        ("Baseline  $100k/mod",  0.100),
        ("Pessimistic $250k/mod", 0.250),
    ]

    # Two thermal efficiency scenarios
    eta_scenarios = [
        ("Thermoelectric (η=12%)", 0.12),
        ("Multi-module turbine (η=30%)", 0.30),
    ]

    Q_values = [3.0, 5.0, 7.0, 9.0, 10.0, 12.0, 15.0, 20.0, 30.0]

    for eta_name, eta in eta_scenarios:
        q_be = 1.0 / eta  # approximate break-even Q
        print(f"\n  [{eta_name}]  — break-even Q ≈ {q_be:.1f}")
        print(f"  {'Q_eng':>5}  {'Net kWe':>9}  "
              f"{'Opt $/kWe':>12}  {'LCOE$/MWh':>10}  "
              f"{'Base $/kWe':>12}  {'LCOE$/MWh':>10}  "
              f"{'Pess $/kWe':>12}  {'LCOE$/MWh':>10}")
        print(f"  {'─'*95}")

        for Q in Q_values:
            net_mw_ref = None
            row_parts = []

            for scen_name, cath_cost in cap_scenarios:
                p_s = OrbitronPlantParams(Q_engineering=Q, thermal_efficiency=eta,
                                         cathode_cost_M_USD=cath_cost)
                r_s = p_s.compute()
                net_mw_s = r_s["power"]["p_net_plant"]
                lcoe_s = r_s["economics"]["lcoe_USD_per_MWh"]
                spec_cap = r_s["costs"]["specific_capital_USD_per_kWe"]
                if net_mw_ref is None:
                    net_mw_ref = net_mw_s

                if net_mw_s <= 0:
                    row_parts.append(f"  {'NEG POWER':>12}  {'—':>10}")
                elif spec_cap > 1e8:
                    row_parts.append(f"  {'>>$1M/kWe':>12}  {'>$999k':>10}")
                elif lcoe_s > 999999:
                    row_parts.append(f"  {f'${spec_cap:,.0f}':>12}  {'>$999k':>10}")
                else:
                    viable = " ◄" if lcoe_s <= 100 else ""
                    row_parts.append(f"  {f'${spec_cap:,.0f}':>12}  {f'${lcoe_s:,.0f}':>10}{viable}")

            if net_mw_ref is not None and net_mw_ref > 0:
                net_str = f"{net_mw_ref*1000:>7.2f} kWe"
                be_marker = " ← ~break-even" if abs(Q - q_be) < 0.7 else ""
            else:
                net_str = "   NEG kWe"
                be_marker = ""

            print(f"  Q={Q:>4.1f}  {net_str}{''.join(row_parts)}{be_marker}")

    print(f"\n  Notes:")
    print(f"  - '$/kWe' = total capital / net electric power (computed from model, not assumed)")
    print(f"  - Capital scenarios vary cathode/vacuum assembly cost (dominant per-module account)")
    print(f"  - $/kWe varies strongly with Q because net power ∝ (Q×η − 1) × n_modules")
    print(f"  - '◄ VIABLE' = LCOE ≤ $100/MWh in that (Q, capital scenario) cell")
    print(f"  - Tritium purchased at ${OrbitronPlantParams().tritium_price_per_g_USD:,.0f}/g — permanent OPEX, no breeding blanket")
    print(f"  - Net power shown for 1000 modules at 1 kWe input per module")


def main():
    # ================================================================
    # BASELINE SCENARIO
    # ================================================================
    print("\n" + "#" * 70)
    print("# BASELINE: Thermoelectric scenario above break-even")
    print("# Q_engineering=10, η=12%, 1000 modules × 1 kWe input")
    print("# Break-even at Q≈8.3 for η=12%; Q=10 yields ~16% net fraction")
    print("#" * 70)
    baseline = OrbitronPlantParams()
    r_base = baseline.compute()
    print_results(baseline, r_base, label="Baseline (Q=10, η=12%)")

    # ================================================================
    # SENSITIVITY SWEEPS
    # ================================================================
    print("\n\n" + "=" * 70)
    print("SENSITIVITY SWEEPS (from baseline: Q=10, η=12%, 1000 modules)")
    print("=" * 70)

    base_lcoe = r_base["economics"]["lcoe_USD_per_MWh"]
    base_spec_cap = r_base["costs"]["specific_capital_USD_per_kWe"]
    if base_lcoe < 1e9:
        print(f"\nBaseline LCOE: ${base_lcoe:,.0f}/MWh  |  Specific capital: ${base_spec_cap:,.0f}/kWe\n")
    else:
        print(f"\nBaseline LCOE: UNDEFINED  |  Specific capital: N/A\n")

    # Q and η sweeps span break-even thresholds explicitly
    sweeps = [
        ("Q_engineering",
         [1.0, 2.0, 3.0, 5.0, 7.0, 8.0, 9.0, 10.0, 12.0, 15.0, 20.0, 30.0],
         "Q_engineering  [break-even @η=12%: Q≈8.3; @η=30%: Q≈3.3]"),
        ("thermal_efficiency",
         [0.05, 0.08, 0.12, 0.20, 0.30, 0.40],
         "Thermal efficiency"),
        ("n_modules",
         [100, 500, 1000, 5000, 10000, 50000],
         "Module count"),
        ("hv_per_module_cost_M_USD",
         [0.005, 0.010, 0.020, 0.050, 0.100, 0.200],
         "HV supply $/module (direct; $/kW_input sweep broken at 1 kWe scale — F-1)"),
        ("shielding_cost_per_m3_M_USD",
         [0.002, 0.005, 0.015, 0.050, 0.150, 0.500],
         "Shielding M$/m³ [$740–$185k/module at baseline geometry — F-2]"),
        ("tritium_price_per_g_USD",
         [15000, 25000, 35000, 50000, 100000],
         "Tritium $/g"),
        ("om_frac_of_capex",
         [0.02, 0.03, 0.04, 0.06, 0.08],
         "O&M frac of CAPEX"),
        ("cathode_lifetime_FPY",
         [0.5, 1.0, 2.0, 5.0, 10.0],
         "Cathode lifetime (FPY)"),
    ]

    for param_name, values, label in sweeps:
        print(f"  {label}:")
        sweep_results = sensitivity_sweep(baseline, param_name, values)
        for sr in sweep_results:
            val = sr["param_value"]
            lcoe = sr["lcoe_USD_per_MWh"]
            net = sr["p_net_plant_MW"]
            spec = sr["specific_capital_USD_per_kWe"]
            marker = " ◄ VIABLE" if lcoe <= 100 else ""
            if net <= 0:
                print(f"    {val:>10.3g}  →  NET POWER ≤ 0 ({net*1000:.2f} kWe)")
            elif lcoe > 999999:
                print(f"    {val:>10.3g}  →  >${lcoe/1000:.0f}k/MWh  ({net*1000:.1f} kWe, ${spec:,.0f}/kWe)")
            else:
                print(f"    {val:>10.3g}  →  ${lcoe:>8,.0f}/MWh  ({net*1000:.1f} kWe, ${spec:,.0f}/kWe){marker}")
        print()

    # ================================================================
    # BACK-SOLVE: LCOE SURFACE (Q × capital scenarios with verified $/kWe)
    # ================================================================
    back_solve_lcoe_surface()

    # ================================================================
    # SCENARIO COMPARISON TABLE
    # ================================================================
    print("\n\n" + "=" * 70)
    print("SCENARIO COMPARISON TABLE")
    print("All scenarios represent physically feasible configurations (net power > 0).")
    print("=" * 70)
    # Note: break-even Q for η=12% is ~9.3; for η=30% is ~3.4 (including ~120 W aux).
    # All rows below use Q above break-even and produce positive net power.
    print(f"\n{'Scenario':<40} {'Q_eng':>6} {'η':>6} {'Mods':>6} "
          f"{'Net kWe':>9} {'$/kWe':>9} {'LCOE $/MWh':>12}")
    print("─" * 95)

    scenario_defs = [
        ("Q=10, thermoelectric (baseline)",
         OrbitronPlantParams(Q_engineering=10.0, thermal_efficiency=0.12, n_modules=1000)),
        ("Q=12, thermoelectric",
         OrbitronPlantParams(Q_engineering=12.0, thermal_efficiency=0.12, n_modules=1000)),
        ("Q=20, thermoelectric",
         OrbitronPlantParams(Q_engineering=20.0, thermal_efficiency=0.12, n_modules=1000)),
        ("Q=5, turbine array (η=30%)",
         OrbitronPlantParams(Q_engineering=5.0, thermal_efficiency=0.30, n_modules=1000)),
        ("Q=10, turbine array (η=30%)",
         OrbitronPlantParams(Q_engineering=10.0, thermal_efficiency=0.30, n_modules=1000)),
        ("Q=10, turbine, NOAK, large plant",
         OrbitronPlantParams(Q_engineering=10.0, thermal_efficiency=0.30,
                             n_modules=5000, noak=True,
                             hv_power_supply_cost_per_kW_USD=200.0)),
        ("Q=20, turbine, NOAK, large plant",
         OrbitronPlantParams(Q_engineering=20.0, thermal_efficiency=0.30,
                             n_modules=10000, noak=True,
                             hv_power_supply_cost_per_kW_USD=150.0)),
    ]

    for name, p_scen in scenario_defs:
        r_scen = p_scen.compute()
        net_kwe = r_scen["power"]["p_net_plant"] * 1000  # MWe → kWe
        lcoe = r_scen["economics"]["lcoe_USD_per_MWh"]
        spec = r_scen["costs"]["specific_capital_USD_per_kWe"]
        if net_kwe <= 0:
            lcoe_str = "N/A (neg)"
            spec_str = "    N/A"
        elif lcoe > 999999:
            lcoe_str = f">${lcoe/1000:.0f}k"
            spec_str = f"${spec:>6,.0f}" if spec < 1e8 else ">$1M"
        else:
            viable = " ◄" if lcoe <= 100 else ""
            lcoe_str = f"${lcoe:>8,.0f}{viable}"
            spec_str = f"${spec:>6,.0f}" if spec < 1e8 else ">$1M"
        print(f"  {name:<38} {p_scen.Q_engineering:>6.1f} {p_scen.thermal_efficiency:>5.0%} "
              f"{p_scen.n_modules:>6,} {net_kwe:>7.1f}  {spec_str:>9}  {lcoe_str:>12}")

    # ================================================================
    # KEY BINDING CONSTRAINTS — stated as falsifiable propositions
    # ================================================================
    print("\n\n" + "=" * 70)
    print("KEY BINDING CONSTRAINTS — Conditional Viability Propositions")
    print("=" * 70)

    # Compute H1 threshold: find minimum Q for LCOE ≤ $100/MWh at η=12%
    h1_q_threshold = None
    h1_lcoe_at_q20 = None
    for Q_test in [q * 0.5 for q in range(18, 200)]:  # Q from 9.0 to 100.0, step 0.5
        p_t = OrbitronPlantParams(Q_engineering=Q_test, thermal_efficiency=0.12)
        r_t = p_t.compute()
        if r_t["power"]["p_net_plant"] > 0:
            lcoe_t = r_t["economics"]["lcoe_USD_per_MWh"]
            if Q_test == 20.0:
                h1_lcoe_at_q20 = lcoe_t
            if lcoe_t <= 100.0 and h1_q_threshold is None:
                h1_q_threshold = Q_test

    # Compute H2 threshold: find minimum Q for LCOE ≤ $100/MWh at η=30%
    h2_q_threshold = None
    h2_lcoe_at_q10 = None
    for Q_test in [q * 0.5 for q in range(8, 200)]:  # Q from 4.0 to 100.0, step 0.5
        p_t = OrbitronPlantParams(Q_engineering=Q_test, thermal_efficiency=0.30)
        r_t = p_t.compute()
        if r_t["power"]["p_net_plant"] > 0:
            lcoe_t = r_t["economics"]["lcoe_USD_per_MWh"]
            if abs(Q_test - 10.0) < 0.01:
                h2_lcoe_at_q10 = lcoe_t
            if lcoe_t <= 100.0 and h2_q_threshold is None:
                h2_q_threshold = Q_test

    # Compute tritium cost contribution at Q=10, η=12%
    r_h1 = OrbitronPlantParams(Q_engineering=10.0, thermal_efficiency=0.12).compute()
    trit_frac_q10 = r_h1["economics"].get("fuel_fraction", float("nan"))
    trit_cost_q10 = r_h1["economics"]["CAS80_tritium"]
    lcoe_q10_eta12 = r_h1["economics"]["lcoe_USD_per_MWh"]

    h1_str = f"Q > {h1_q_threshold:.1f}" if h1_q_threshold else "Q > 100 (not found in model range)"
    h2_str = f"Q > {h2_q_threshold:.1f}" if h2_q_threshold else "Q > 100 (not found in model range)"
    h1_lcoe_str = f"${h1_lcoe_at_q20:,.0f}/MWh" if h1_lcoe_at_q20 else "N/A"
    h2_lcoe_str = f"${h2_lcoe_at_q10:,.0f}/MWh" if h2_lcoe_at_q10 else "N/A"

    print(f"""
  H1 — Thermoelectric scenario (η=12%):
    PROPOSITION: LCOE ≤ $100/MWh under thermoelectric conversion requires
    Q_engineering ≥ {h1_str} (1000 modules, FOAK, $300/kW_input HV supply).
    Net-power break-even alone requires Q_engineering ≥ 8.3 (= 1/0.12); commercial
    viability requires substantially higher Q due to capital cost per kWe.
    MODEL RESULT: At Q=20, the model computes LCOE = {h1_lcoe_str}. The $100/MWh
    threshold {("requires " + h1_str) if h1_q_threshold else "is not reached within the model Q range"}.
    PHYSICS BARRIER: Coulomb collision physics is cited as making Q >> 1 structurally
    difficult in this confinement class (Lampe-Mannheimer 1998: collision rate 25–37×
    fusion rate at required densities). If this barrier limits achievable Q below the
    model-computed threshold, the thermoelectric scenario is structurally non-viable
    regardless of capital cost assumptions.

  H2 — Turbine-array scenario (η=30%):
    PROPOSITION: LCOE ≤ $100/MWh under turbine-array conversion requires
    Q_engineering ≥ {h2_str} (1000 modules, FOAK, $300/kW_input HV supply)
    AND a plant scale sufficient to justify turbine-array conversion (>1 MWe aggregate,
    implying >>1000 modules at 1 kWe/module input).
    MODEL RESULT: At Q=10, the model computes LCOE = {h2_lcoe_str}.
    The $100/MWh threshold {("requires " + h2_str) if h2_q_threshold else "is not reached within the model Q range"}.
    ARCHITECTURE BARRIER: η=30% requires megawatt-aggregate scale per thermal unit —
    a plant architecture (module stacking, shared BOP) that does not yet exist or have
    a published design. This scenario requires both the Q threshold AND a demonstrated
    plant architecture to be simultaneously achieved.

  H3 — Tritium cost axis (both scenarios):
    PROPOSITION: Purchased tritium at >${OrbitronPlantParams().tritium_price_per_g_USD:,.0f}/g constitutes
    {trit_frac_q10:.0%} of total annual revenue requirement at Q=10, η=12%
    (${trit_cost_q10:.1f}M/yr for 1000 modules, contributing ~${trit_frac_q10 * lcoe_q10_eta12:,.0f}/MWh
    of the total ${lcoe_q10_eta12:,.0f}/MWh LCOE). Tritium cost per MWh scales inversely
    with Q (∝ p_fus/p_net ∝ Q/(Q×η−1)): as Q approaches break-even, tritium cost
    per unit electricity diverges regardless of capital cost. No breeding blanket
    design has been published; an MoU with Fusion Fuel Cycles (FFC, April 2025)
    covers breeding as a collaboration direction but no specification, timeline, or
    technical design exists. At Q < 5, purchased tritium cost alone may preclude
    commercial viability independent of capital cost — a third constraint axis beyond
    Q and $/kWe that does not appear in mainstream D-T TEA.
""")

    print("=" * 70)
    print("NOTE: All LCOE values carry EXTREME UNCERTAINTY. This model is a conditional")
    print("viability map — not a cost projection. The Orbitron has not demonstrated Q>1")
    print("and the central density-enhancement physics is simulation-only (AIP Advances 2024).")
    print("Cost accounts follow 1costingfe CAS structure with extensive concept-specific")
    print("overrides. See parameter docstrings for sources and uncertainty levels.")
    print("=" * 70)


if __name__ == "__main__":
    main()
