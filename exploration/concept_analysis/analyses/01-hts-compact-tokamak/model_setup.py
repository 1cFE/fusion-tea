# STALE: analysis-updated-iter-4
"""HTS Compact Tokamak (CFS ARC) — 1costingfe parametric LCOE model.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling approach:
    The ARC cost database (Sorbom et al. 2015) covers only three fabricated
    subsystems — vacuum vessel, FLiBe blanket, and magnet/structure — explicitly
    excluding balance of plant. The analysis (analysis.md §5) recommends a
    free-form parametric scaling approach, not a full structured CAS build.
    This script uses the 1costingfe CAS framework with three targeted
    cost_overrides where ARC-specific data exists:
      - C220103: coil cost from ARC's published REBCO tape requirement (5,730 km)
      - C220104: heating cost from ARC's LHCD+ICRF mix (no NBI)
      - CAS27:   FLiBe blanket fill from Araiinejad & Shirvan (2025) NOAK estimate
    All other CAS accounts use framework defaults calibrated to reference D-T
    tokamaks — appropriate order-of-magnitude estimates, but not validated against
    ARC-specific design data.

Concept choice rationale:
    CFS ARC is the most extensively published private HTS compact tokamak.
    Sorbom et al. (2015) provides component-level costs; the 2020 power
    conversion study establishes 46% net Rankine efficiency. The September 2021
    CFS magnet demonstration (20 T large-bore HTS) directly validates the core
    technology at the design operating point.

Key deviations from the reference dt_tokamak.py (CATF spherical tokamak):
    1. Net electric: 270 MWe (ARC 2015 aggressive pilot ~261 MWe, rounded)
       vs. 1,000 MWe CATF reference. CFS 2025 target is 400 MWe (not documented).
    2. Geometry: R0=3.3 m, a=1.13 m (aspect ratio 3) vs. CATF R0=3.0 m, a=1.1 m.
    3. eta_th=0.46 from ARC-specific supercritical Rankine analysis.
    4. C220103 overridden from ARC's 5,730 km REBCO tape requirement at NOAK prices.
    5. C220104 overridden for LHCD+ICRF heating (no NBI — ARC uses klystrons/tetrodes).
    6. CAS27 overridden for FLiBe (950 t × $154/kg NOAK) vs. default PbLi assumption.
    7. CRITICAL UNCERTAINTY — availability (capacity factor) is unpublished for ARC.
       80% is a medium assumption. Analysis shows 50%→90% produces near-2× LCOE swing.
"""

from costingfe import ConfinementConcept, CostModel, Fuel

model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# ── Cost Override Pre-computation ────────────────────────────────────────────
#
# C220103: Coil cost from ARC's REBCO tape requirement
# ARC TF + PF coils require 5,730 km REBCO tape [arc-reactor-specifications.md §4.1, §6].
# Critical current: ~250 A per meter of tape at 20 K, 20 T
#   [analysis.md §S4: "250 A/m at 20K, 20T"].
# NOAK conductor target: $50/kAm [costingfe costing_constants.yaml CoilMaterial.REBCO_HTS].
# Manufacturing markup: 8× for tokamak [costingfe layers/cas22.py _COIL_DEFAULTS].
# This overrides the framework's geometry-based formula (default b_max=12 T, r_coil=1.85 m)
# with the published tape figure — ARC's 23 T peak field is not propagated through
# model.forward() to the coil scaling formula.
_REBCO_KM = 5730.0         # km; arc-reactor-specifications.md §4.1
_IC_A_PER_M = 250.0        # A/m at 20 K, 20 T; analysis.md §S4
_REBCO_NOAK_PER_KAM = 50.0 # $/kAm NOAK target; costing_constants.yaml
_TOKAMAK_MARKUP = 8.0      # manufacturing complexity; cas22.py _COIL_DEFAULTS TOKAMAK
_total_kAm = (_REBCO_KM * 1e3) * (_IC_A_PER_M / 1000.0)   # 1,432,500 kA-m
_conductor_cost_M = _total_kAm * _REBCO_NOAK_PER_KAM / 1e6
C220103_COILS = _conductor_cost_M * _TOKAMAK_MARKUP  # M$

# C220104: Heating system — LHCD + ICRF (no NBI)
# ARC aux heating: 25 MW LHCD (8 GHz) + 13.6 MW ICRF (120 MHz)
#   [arc-reactor-specifications.md §5.1; sparc-icrf-heating-paper.md §Introduction].
# ICRF selected specifically for cost-effectiveness using existing technology
#   [sparc-icrf-heating-paper.md §Introduction: "can be built cost-effectively"].
# Unit costs: LHCD $4.0 M/MW, ICRF $4.1494 M/MW [costingfe defaults.py].
# Framework default uses p_nbi=50 MW ($353 M); ARC uses no NBI (klystrons/tetrodes).
_P_LHCD_MW = 25.0   # MW LHCD; arc-reactor-specifications.md §5.1
_P_ICRF_MW = 13.6   # MW ICRF; arc-reactor-specifications.md §5.1
_LHCD_PER_MW = 4.0      # M$/MW; costingfe defaults.py heating_lhcd_per_mw
_ICRF_PER_MW = 4.1494   # M$/MW; costingfe defaults.py heating_icrf_per_mw
C220104_HEATING = _P_LHCD_MW * _LHCD_PER_MW + _P_ICRF_MW * _ICRF_PER_MW  # M$

# CAS27: FLiBe blanket material fill (not PbLi)
# ARC blanket tank contains ~950 t FLiBe (LiF-BeF₂) [arc-reactor-specifications.md §5.4].
# NOAK unit cost: ~$154/kg (Araiinejad & Shirvan 2025, 20% learning rate assumed)
#   [analysis.md §S4: "FLiBe unit cost (NOAK): ~$154/kg"].
# Default CAS27 assumes PbLi at $3/kg (~$15 M at 1 GWe) — underestimates FLiBe by ~50×.
_FLIBE_TONNES = 950.0       # t; arc-reactor-specifications.md §5.4
_FLIBE_NOAK_PER_KG = 154.0  # $/kg NOAK; Araiinejad & Shirvan 2025; analysis.md §S5
CAS27_FLIBE = _FLIBE_TONNES * 1e3 * _FLIBE_NOAK_PER_KG / 1e6  # M$; ~$146 M

# ── Plant Configuration ──────────────────────────────────────────────────────
result = model.forward(
    # ── Customer requirements ───────────────────────────────────────────────
    # ARC 2015 paper: 190 MWe (FNSF phase) to 261 MWe (aggressive pilot phase)
    # [arc-power-conversion-studies.md §Results]. Using 270 MWe as the aggressive
    # pilot rounded up slightly. CFS 2025 communications describe 400 MWe (updated
    # design, parameters not published) [cfs-2025-2026-updates.md].
    net_electric_mw=270.0,
    # UNCERTAIN: Capacity factor not published anywhere for ARC [analysis.md §S5].
    # Analysis §S2 Hypothesis 2: sub-$100/MWh LCOE requires >70-80% CF sustained.
    # 80% is a medium assumption; see sensitivity section below for 50-90% sweep.
    availability=0.80,
    # ARC TF coil fluence limit: 9 FPY [arc-reactor-specifications.md §5].
    # Demountable coil design enables in-situ replacement; 30-year plant life
    # assumes ~3 magnet generations. Standard nuclear plant lifetime analogue.
    lifetime_yr=30.0,
    n_mod=1,
    # UNCERTAIN: Construction time not published; analogue to large nuclear (6-10 yr).
    # ARC's novel HTS technology and regulatory path suggest upper end of range.
    construction_time_yr=7.0,
    interest_rate=0.07,      # DEFAULT: standard utility financing assumption
    inflation_rate=0.0245,   # DEFAULT: ~2.5% long-run US inflation
    noak=True,

    # ── ARC Reactor Geometry ────────────────────────────────────────────────
    # ARC major radius R0 = 3.3 m [arc-reactor-specifications.md §2]
    R0=3.3,
    # ARC minor radius a = 1.13 m, aspect ratio A = 3 [arc-reactor-specifications.md §2]
    plasma_t=1.13,
    # UNCERTAIN: Elongation κ not stated in analysis; 1.84 is typical for compact
    # D-T tokamak (I-mode regime). SPARC uses κ≈1.97; ARC power plant may differ.
    elon=1.84,
    # FLiBe liquid blanket: compact radial build. ~20 cm outboard + inboard layers.
    # UNCERTAIN: exact radial build not fully published for ARC.
    blanket_t=0.35,
    # TiH₂ neutron shielding, ~380 t [arc-reactor-specifications.md §6].
    # UNCERTAIN: exact shield thickness not stated.
    ht_shield_t=0.10,
    structure_t=0.10,  # DEFAULT: compact primary structure estimate
    # Inconel-718 double-wall vacuum vessel [arc-reactor-specifications.md §4.3].
    # UNCERTAIN: exact VV thickness not stated; ARC VV cost = $92 M (2014 USD).
    vessel_t=0.10,

    # ── Power Balance ───────────────────────────────────────────────────────
    # Total auxiliary heating: 25 MW LHCD + 13.6 MW ICRF = 38.6 MW
    # [arc-reactor-specifications.md §5.1]
    p_input=38.6,
    mn=1.1,          # DEFAULT: standard DT neutron energy multiplier
    # Supercritical Rankine steam cycle at 250 bar, 540°C inlet: 46% net efficiency.
    # [arc-power-conversion-studies.md §3.2, Table 15; Colliva et al. 2024 independently].
    # 645 MWth to PCS → 297 MWe gross → ~261-270 MWe net at this output level.
    eta_th=0.46,
    eta_p=0.5,       # DEFAULT: pumping efficiency
    # Wall-plug efficiency: weighted average LHCD klystrons (~45%) + ICRF tetrodes (~65%).
    # (25×0.45 + 13.6×0.65) / 38.6 ≈ 0.52.
    # UNCERTAIN: LHCD at 8 GHz not yet demonstrated at required power; analysis.md §S2 Ch.5.
    eta_pin=0.52,
    # No direct energy conversion — ARC is purely thermal cycle (supercritical Rankine).
    # [analysis.md §S7: "Borrowed: supercritical steam Rankine BOP"]
    f_dec=0.0,
    # Subsystem power fraction elevated for ARC: cryo at 20 K + FLiBe pumping.
    # Default 0.03 calibrated to LTS tokamaks. ARC's 20 K cryoplant + FLiBe
    # chemistry plant add parasitic load. UNCERTAIN: no published ARC estimate.
    f_sub=0.05,
    # HTS magnet power supplies (persistent current mode, ramp control).
    # UNCERTAIN: analogue; 20 K operation smaller steady-state supply load than 4 K LTS.
    p_coils=3.0,
    # Primary circuit heat rejection (FLiBe loop).
    # UNCERTAIN: analogue; FLiBe MHD effects may increase pumping/cooling load.
    p_cool=13.0,
    # FLiBe blanket primary pumping against MHD pressure drop (≤0.2 m/s design limit).
    # MHD drag in 9.2 T field may substantially increase pumping requirement.
    # [arc-reactor-specifications.md §7: "detailed investigation is needed"]
    p_pump=2.5,
    # Tritium processing from FLiBe molten-salt extraction system.
    # Elevated vs. solid-blanket baseline; chemistry plant scale uncertain.
    # UNCERTAIN: FLiBe tritium extraction at kg/day rates not demonstrated; analysis.md §S2 Ch.3.
    p_trit=15.0,
    p_house=4.0,  # DEFAULT: housekeeping (control, instrumentation, HVAC)
    # Cryogenic plant at 20 K (REBCO operating temperature).
    # 20 K is ~3× more efficient than 4 K (LHe) but ARC's compact high-field coils
    # have substantial heat load. UNCERTAIN: no published ARC cryoplant estimate.
    p_cryo=2.0,

    # ── Cost Overrides (justified from ARC sources) ─────────────────────────
    cost_overrides={
        # Coil cost from ARC's published REBCO tape figure (5,730 km at 250 A/m),
        # NOAK $50/kAm × 8× tokamak manufacturing markup.
        # Overrides geometry-based formula; b_max=23 T not propagated through forward().
        # Source: arc-reactor-specifications.md §4.1, §6; analysis.md §S5
        "C220103": C220103_COILS,
        # Heating from LHCD (25 MW) + ICRF (13.6 MW); eliminates default NBI (p_nbi=50 MW).
        # Source: arc-reactor-specifications.md §5.1; sparc-icrf-heating-paper.md §Intro
        "C220104": C220104_HEATING,
        # FLiBe blanket fill (950 t × $154/kg NOAK); replaces default PbLi assumption.
        # Source: arc-reactor-specifications.md §5.4; Araiinejad & Shirvan 2025
        "CAS27": CAS27_FLIBE,
    },
)

# ── Results ──────────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("HTS Compact Tokamak (CFS ARC) — NOAK, 270 MWe, 80% availability, 30 yr")
print(f"LCOE:         {c.lcoe:.1f} $/MWh")
print(f"Overnight:    {c.overnight_cost:.0f} $/kW")
print(f"Fusion power: {pt.p_fus:.0f} MW  |  Net: {pt.p_net:.0f} MW  |  Q_eng: {pt.q_eng:.2f}")
print(f"Recirculating fraction: {pt.rec_frac:.3f}")
print()

# Override echo
print(f"[Overrides applied]")
print(f"  C220103 coils  = {C220103_COILS:.1f} M$ "
      f"({_REBCO_KM:.0f} km REBCO × {_IC_A_PER_M:.0f} A/m × ${_REBCO_NOAK_PER_KAM:.0f}/kAm × {_TOKAMAK_MARKUP:.0f}× markup)")
print(f"  C220104 heat   = {C220104_HEATING:.1f} M$ "
      f"({_P_LHCD_MW:.0f} MW LHCD + {_P_ICRF_MW:.1f} MW ICRF, no NBI)")
print(f"  CAS27 FLiBe    = {CAS27_FLIBE:.1f} M$ "
      f"({_FLIBE_TONNES:.0f} t × ${_FLIBE_NOAK_PER_KG:.0f}/kg NOAK)")
print()

# ── CAS Breakdown ─────────────────────────────────────────────────────────────
cas = [
    ("CAS10", "Preconstruction",          c.cas10),
    ("CAS21", "Buildings",                c.cas21),
    ("CAS22", "Reactor Plant Equipment",  c.cas22),
    ("CAS23", "Turbine Plant",            c.cas23),
    ("CAS24", "Electrical Plant",         c.cas24),
    ("CAS25", "Miscellaneous",            c.cas25),
    ("CAS26", "Heat Rejection",           c.cas26),
    ("CAS27", "Special Materials (FLiBe)",c.cas27),
    ("CAS28", "Digital Twin",             c.cas28),
    ("CAS29", "Contingency",              c.cas29),
    ("CAS30", "Indirect Costs",           c.cas30),
    ("CAS40", "Owner's Costs",            c.cas40),
    ("CAS50", "Supplementary",            c.cas50),
    ("CAS60", "IDC",                      c.cas60),
    ("CAS70", "O&M (annualized)",         c.cas70),
    ("CAS80", "Fuel (annualized)",        c.cas80),
    ("CAS90", "Financial",                c.cas90),
]

print(f"{'Code':<8} {'Account':<30} {'M$':>10}")
print("-" * 50)
for code, name, val in cas:
    print(f"{code:<8} {name:<30} {float(val):>10.1f}")
print("-" * 50)
print(f"{'':8} {'Total Capital':<30} {float(c.total_capital):>10.1f}")
print()

# ── CAS22 Sub-Account Detail ─────────────────────────────────────────────────
_CAS22_NAMES = {
    "C220101": "First Wall + Blanket",
    "C220102": "Shield",
    "C220103": "Coils (REBCO HTS) [ovr]",
    "C220104": "Heating LHCD+ICRF [ovr]",
    "C220105": "Primary Structure",
    "C220106": "Vacuum System (Inconel-718)",
    "C220107": "Power Supplies",
    "C220108": "Divertor",
    "C220109": "Direct Energy Converter",
    "C220110": "Remote Handling",
    "C220111": "Installation Labor",
    "C220500": "Fuel Handling (tritium)",
    "C220000": "CAS22 TOTAL",
}
print("CAS22 Reactor Plant Equipment — sub-account detail")
print(f"  {'Code':<12} {'Account':<30} {'M$':>10}")
print("  " + "-" * 54)
for key in sorted(k for k in result.cas22_detail if k != "C220000"):
    name = _CAS22_NAMES.get(key, key)
    print(f"  {key:<12} {name:<30} {float(result.cas22_detail[key]):>10.1f}")
print("  " + "-" * 54)
total22 = result.cas22_detail.get("C220000", c.cas22)
print(f"  {'C220000':<12} {'CAS22 TOTAL':<30} {float(total22):>10.1f}")
print()

# ── Key Assumptions ──────────────────────────────────────────────────────────
print("Key Assumptions:")
print(f"  Net electric:   {result.params.get('net_electric_mw', 270):.0f} MWe  "
      f"(ARC 2015 aggressive pilot ~261 MWe; 2025 target 400 MWe not modeled)")
print(f"  Availability:   {result.params.get('availability', 0.80):.0%}  "
      f"[UNCERTAIN — not published by CFS; primary LCOE lever]")
print(f"  Lifetime:       {result.params.get('lifetime_yr', 30):.0f} yr  "
      f"(30 yr with ~3 magnet replacements at 9 FPY fluence limit each)")
print(f"  eta_th:         46%  [supercritical Rankine; arc-power-conversion-studies.md §3.2]")
print(f"  REBCO tape:     {_REBCO_KM:.0f} km at {_IC_A_PER_M:.0f} A/m → "
      f"{_total_kAm:,.0f} kA-m at NOAK ${_REBCO_NOAK_PER_KAM:.0f}/kAm")
print(f"  FLiBe fill:     {_FLIBE_TONNES:.0f} t at ${_FLIBE_NOAK_PER_KG:.0f}/kg NOAK = "
      f"${CAS27_FLIBE:.0f} M  [Araiinejad & Shirvan 2025]")
print(f"  Regulatory:     NRC Part 30 framework modeled (no Part 50 multiplier)")
print()
print("Unmodeled risks that could substantially change LCOE:")
print("  - REBCO tape price above NOAK target ($50/kAm): see sensitivity below")
print("  - I-mode non-accessible at ARC parameters → net output drops to ~80-100 MWe")
print("  - FLiBe/Inconel corrosion requiring blanket material substitution")
print("  - ARC 400 MWe updated design (2025) vs. 270 MWe modeled here")
print("  - NRC Part 50 vs. Part 30 regulation: 2.2× building cost multiplier possible")
print()

# ── Sensitivity Analysis ─────────────────────────────────────────────────────
sens = model.sensitivity(result.params, cost_overrides={
    "C220103": C220103_COILS,
    "C220104": C220104_HEATING,
    "CAS27":   CAS27_FLIBE,
})

print("Sensitivity (elasticity = %ΔLCOE / %Δparam):")
print("-" * 50)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<30} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<30} {v:+.4f}")

# ── Capacity Factor Sweep ─────────────────────────────────────────────────────
# ARC is CAPEX-heavy: analysis §S2 Hypothesis 2 shows ~2× LCOE swing from 50%→90% CF.
print("\nCapacity Factor Sweep (primary LCOE lever — unpublished for ARC):")
print(f"  {'Availability':>14} {'LCOE ($/MWh)':>14}")
print("  " + "-" * 30)
cf_values = [0.50, 0.60, 0.70, 0.80, 0.85, 0.90]
lcoes_cf = model.batch_lcoe(
    {"availability": cf_values},
    result.params,
    cost_overrides={
        "C220103": C220103_COILS,
        "C220104": C220104_HEATING,
        "CAS27":   CAS27_FLIBE,
    },
)
for cf, lcoe in zip(cf_values, lcoes_cf):
    marker = " ← baseline" if cf == 0.80 else ""
    print(f"  {cf:>14.0%} {lcoe:>14.1f}{marker}")

# ── REBCO Tape Cost Scenarios ─────────────────────────────────────────────────
# REBCO cost is the largest single cost uncertainty in ARC [analysis.md §S2 Ch.1].
# Span: NOAK target $50/kAm → current market ~$300/kAm (2025); 6× range.
# This drives C220103 proportionally (all other accounts held constant).
print()
print("REBCO Tape Cost Scenarios (C220103 varies; all other accounts held at NOAK):")
print(f"  {'Price ($/kAm)':>14} {'C220103 (M$)':>14} {'LCOE ($/MWh)':>14} {'Scenario'}")
print("  " + "-" * 70)
rebco_prices = [
    (50.0,  "NOAK target — commercial viability threshold"),
    (100.0, "2× NOAK — near-term optimistic"),
    (200.0, "4× NOAK — near-term realistic (improving from 2014 high-end)"),
    (300.0, "6× NOAK — current market (2025 estimate)"),
    (500.0, "10× NOAK — 2014 mid-range ($198/m at 250 A/m ≈ $792/kAm, FOAK)"),
]
base_co = {"C220104": C220104_HEATING, "CAS27": CAS27_FLIBE}
for price, label in rebco_prices:
    c103 = (_total_kAm * price / 1e6) * _TOKAMAK_MARKUP
    co = {**base_co, "C220103": c103}
    r = model.forward(
        net_electric_mw=270.0,
        availability=0.80,
        lifetime_yr=30.0,
        n_mod=1,
        construction_time_yr=7.0,
        interest_rate=0.07,
        inflation_rate=0.0245,
        noak=True,
        R0=3.3, elon=1.84, plasma_t=1.13,
        blanket_t=0.35, ht_shield_t=0.10, structure_t=0.10, vessel_t=0.10,
        p_input=38.6, mn=1.1, eta_th=0.46, eta_p=0.5, eta_pin=0.52,
        f_dec=0.0, f_sub=0.05, p_coils=3.0, p_cool=13.0,
        p_pump=2.5, p_trit=15.0, p_house=4.0, p_cryo=2.0,
        cost_overrides=co,
    )
    marker = " ← baseline" if price == 50.0 else ""
    print(f"  {price:>14.0f} {c103:>14.1f} {r.costs.lcoe:>14.1f}  {label}{marker}")
