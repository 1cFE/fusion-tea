"""
Compact Liquid-Wall HTS Stellarator (Renaissance Fusion) — 1costingfe model.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling approach:
    Renaissance Fusion's stellarator is architecturally unlike any other concept
    in this survey — three elements depart from all other stellarators modeled:
    (1) laser-patterned HTS REBCO film on cylinders (vs. wound tape in 3D coils);
    (2) flowing liquid Li-LiH wall that consolidates FW/blanket/shield/coolant into
        a single pumped circuit; and (3) ignited plasma (Q=∞, zero steady-state heating).
    Published design point: 1 GWe net at R≤4 m, A≈4, 10 T nominal field.

    Because the concept has zero published cost data, two accounts are handled
    from first-principles analogies:
      - C220101 (blanket/FW): overridden to $400M — liquid metal pumped circuit
        analogous to Na-cooled fast reactor primary loop; UNCERTAIN by factor 2–3×.
      - C220103 (coils): NOT overridden — framework tape-winding model is inapplicable
        to laser-patterned film, so the computed coil cost is a placeholder only
        (factor 3–10× uncertainty). No quantitative estimate is available.

    The large recirculating power (p_pump=380 MW) is inferred from the published
    net efficiency (34%) vs. cycle efficiency (50%), implying ~471 MW of parasitic
    load dominated by liquid metal circulation pumps (analysis.md §Challenge 5).

Concept choice rationale:
    STELLARATOR: steady-state, no CS coil, no current-drive heating account,
    no disruption cost. Parameters set for compact A=4 geometry (not the default
    A≈3.1 with R0=5.5 m). Ignited plasma means p_input=0 at steady state.

Key deviations from framework stellarator defaults:
    - eta_th: 0.50 (sCO₂ combined cycle; PowerCycle.BRAYTON_SCO2 default = 0.47)
    - p_pump: 380 MW (LM circulation dominant load; default = 1 MW)
    - p_input: 0 MW (ignited; default = 30 MW ECRH)
    - p_cryo: 35 MW (large HTS magnet system at 20K; default = 0.8 MW)
    - mn: 1.07 (blanket energy multiplication factor; JNM 599 2024; corrected from 1.24
               which was the Pb (n,2n) neutron number multiplication — a distinct metric)
    - R0: 4.0 m (compact; default = 5.5 m)
    - blanket_t: 0.33 m (15 cm Pb + 18 cm Li-LiH; default = 0.80 m)
    - ht_shield_t: 0.50 m (50 cm VH₂ outer shield; default = 0.20 m)
    - C220101: $400M override (LM wall system vs. volume-based $0.60M/m³ default)
"""

import math

from costingfe import ConfinementConcept, CostModel, Fuel, PowerCycle

# ── Model Construction ───────────────────────────────────────────────────────
model = CostModel(
    concept=ConfinementConcept.STELLARATOR,
    fuel=Fuel.DT,
    power_cycle=PowerCycle.BRAYTON_SCO2,  # sCO₂ Brayton-Rankine; eta_th overridden to 0.50 below
)

# ── Plant Configuration Constants ────────────────────────────────────────────

# 1 GWe net — the economically optimized design point
# Source: Nuclear Fusion 64 (2024) 026007 (Samulski et al.)
NET_ELECTRIC_MW = 1000.0

# Source: Renaissance Fusion company disclosure ("near-100% duty cycle"); central
#   estimate 90–95% documented in analysis.md §5 (Nuclear Fusion 64 (2024) 026007
#   technical description).
# Basis: steady-state operation with no disruptions and no pulse cycling, justified
#   by the liquid-metal wall and stellarator topology.
# UNCERTAIN: actual maintenance intervals for LM wall + pump systems uncharacterized.
AVAILABILITY = 0.92  # DEVIATION: from canonical 0.85 (MCF steady-state, D-T) per
                     #   scoring_framework.md §"Plant availability". See preceding
                     #   comment block for source and basis.

LIFETIME_YR = 30
# Longer construction than default 8yr: first-of-kind laser-patterning manufacturing
# and liquid metal wall integration add substantial first-plant schedule risk
CONSTRUCTION_TIME_YR = 10
INTEREST_RATE = 0.07
INFLATION_RATE = 0.0245

# ── Cost Overrides ───────────────────────────────────────────────────────────
_COST_OVERRIDES = {
    # C220101: Flowing Li-LiH liquid metal wall replaces conventional solid FW/blanket.
    # The integrated circuit (LM pumps, heat exchangers, Pb pebble retention, tritium
    # extraction, MHD-conditioning piping) has no published cost basis.
    # Analogue: Na-cooled fast reactor primary circuit at ~1 GWth scale,
    # plus first-of-kind fusion application premium.
    # UNCERTAIN by factor 2–3×; central estimate $400M
    # Source: analysis.md §Data Gap 5; §Challenge 4; §Cross-Concept Notes
    "C220101": 400.0,  # M$ — UNCERTAIN: LM wall system; Na-cooled fast reactor analogue

    # NOTE: C220103 (coils) is intentionally NOT overridden.
    # The laser-patterned REBCO film cost structure has no published analogue at any
    # scale. The framework's tape-winding cost model ($/kA-m) does not apply.
    # The computed C220103 value is a placeholder — treat as factor 3–10× uncertain.
    # Source: analysis.md §Challenge 2; §Data Gap 2; §S4 (REBCO Film Deposition)
}

# ── Shared Parameters (used in forward() call) ───────────────────────────────
_SHARED_KWARGS = dict(
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=True,

    # ── Machine geometry — compact QI stellarator ────────────────────────────
    # Source: Nuclear Fusion 64 (2024) 026007
    R0=4.0,           # Major radius ≤4 m at cost-optimal design point; NF 64 (2024) 026007
    plasma_t=1.0,     # Minor radius a = R0/A = 4.0/4.0 = 1.0 m; NF 64 (2024) 026007
    elon=1.0,         # Near-circular cross-section (stellarator default)
    # Estimated plasma volume: 2π²·R0·a² ≈ 79 m³ (circular torus); using 200 m³
    # to account for QI shaping and uncertainty; not published
    # UNCERTAIN: compact QI geometry volume not stated in any source
    plasma_volume=200.0,

    # ── Radial build — integrated liquid metal wall system ───────────────────
    # Source: J. Nuclear Materials 599 (2024) 155239
    blanket_t=0.33,       # 15 cm Pb pebble + 18 cm Li-LiH = 33 cm; JNM 599 (2024) 155239
    ht_shield_t=0.50,     # 50 cm VH₂ outer neutron shield; JNM 599 (2024) 155239
    structure_t=0.15,     # DEFAULT: primary structure
    vessel_t=0.10,        # DEFAULT: vacuum vessel

    # ── Magnetic field ───────────────────────────────────────────────────────
    # Source: Nuclear Fusion 64 (2024) 026007
    B=10.0,           # Nominal on-axis magnetic field 10 T; NF 64 (2024) 026007
    b_max=15.0,       # Peak field at coil (primary design target); NF 64 (2024) 026007
                      # (20–40 T upper envelope in paper not used — REBCO Jc concerns)
    # Effective winding bore: a + blanket + shield + structure ≈ 1.0+0.33+0.50+0.15 = 1.98 m
    r_coil=2.0,       # Calibration parameter for coil cost model

    # ── Plasma parameters ────────────────────────────────────────────────────
    T_e=10.0,         # D-T electron temperature 10 keV; NF 64 (2024) 026007
    n_e=1.0e20,       # DEFAULT: electron density [m⁻³]; not published for this design

    # ── Power balance — sCO₂ Brayton-Rankine ─────────────────────────────────
    # Source: Energy Conversion and Management 276 (2023) 116572 (Fama et al.)
    eta_th=0.48,       # standardized from 0.5 per scoring_framework.md (Energy Capture: Thermal (sCO2))
                      # ECM 276 (2023) 116572; overrides PowerCycle.BRAYTON_SCO2 default (0.47)

    # Blanket energy multiplication factor (total thermal energy deposited per unit neutron power).
    # JNM 599 reports M_E = 1.07 for optimized Pb(10cm)+Li-LiH(22cm) config (design req: ≥1.0).
    # The 1.24 figure in the original dossier is the Pb-layer neutron number multiplication
    # (secondary neutrons per primary via Pb (n,2n)) — a distinct metric, not the energy mult.
    # TBR = 1.60 confirmed in same paper (design req TBR ≥ 1.15; 35% margin).
    # Source: JNM 599 (2024) 155239
    mn=1.07,  # DEVIATION: from canonical 1.1 (D-T) — Renaissance Pb-Li blanket per JNM 599 (2024) 155239

    # ── Ignited plasma — NNBI startup only ───────────────────────────────────
    # Q=∞ target: zero steady-state heating power at operating point
    # Source: Nuclear Fusion 64 (2024) 026007
    p_input=0.0,      # Ignited; NNBI runs only during ramp-up, not at steady state
    p_nbi=0.0,        # No NBI at operating point (startup-only; capital cost absorbed elsewhere)
    p_ecrh=0.0,       # No ECRH required (ignited — no current drive, no steady-state heating)
    eta_pin=0.60,     # NNBI neutralization efficiency (startup sizing reference);
                      # NF 64 (2024) 026007; irrelevant at p_input=0
    eta_p=0.50,       # DEFAULT: pumping efficiency
    eta_de=0.00,       # standardized from 0.85 per scoring_framework.md (Energy Capture: Thermal (sCO2))
    f_sub=0.03,       # DEFAULT: subsystem power fraction
    f_dec=0.0,        # No direct energy converter

    # ── Recirculating parasitic loads ─────────────────────────────────────────
    # Published constraint: net efficiency = 34%, cycle efficiency = 50%
    # → recirculating fraction ≈ 32% of gross electric ≈ 471 MW at 1 GWe
    # Source: ECM 276 (2023) 116572; analysis.md §Challenge 5
    # UNCERTAIN: individual load breakdown not published in any source
    #
    # Power budget (UNCERTAIN):
    #   p_pump   380 MW  (LM circulation — dominant, unidentified contributor)
    #   p_cryo    35 MW  (HTS at 20K; large magnet system)
    #   p_cool    20 MW  (auxiliary cooling; LM heat exchanger secondary loops)
    #   p_coils    3 MW  (resistive losses; HTS carries DC supercurrent)
    #   p_trit    10 MW  (tritium processing)
    #   p_house    5 MW  (housekeeping)
    #   Total:   453 MW  → net eff ≈ 34.4% (consistent with published 34%)
    #
    p_pump=380.0,     # UNCERTAIN ±50%: LM circulation; dominant contributor to ~32%
                      # recirculating fraction; not disclosed in any source;
                      # analysis.md §Data Gap 3; challenge: 25 MW/m² continuous wall loading
    p_cryo=35.0,      # UNCERTAIN: HTS cryogenics at 20K for large magnet system;
                      # 20K is ~2× more efficient than 4K LTS (lower Carnot penalty);
                      # full magnet cryogenic load uncharacterized in any source
    p_cool=20.0,      # UNCERTAIN: auxiliary cooling for LM-to-sCO₂ heat exchanger systems
    p_coils=3.0,      # Minimal; HTS carries DC supercurrent (near-zero resistive loss)
    p_trit=10.0,      # DEFAULT: tritium processing plant
    p_house=5.0,      # DEFAULT: housekeeping loads

    # ── Wall material ────────────────────────────────────────────────────────
    # Li-LiH flowing liquid metal wall serves as plasma-facing surface
    # Source: JNM 599 (2024) 155239
    wall_material='Li',

    cost_overrides=_COST_OVERRIDES,
)

# ── Forward Run ──────────────────────────────────────────────────────────────
# Native design point IS 1000 MWe — no result_1gw needed
result = model.forward(net_electric_mw=NET_ELECTRIC_MW, **_SHARED_KWARGS)

# ── Results Output ───────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Compact Liquid-Wall HTS Stellarator (Renaissance Fusion)")
print("1 GWe net — NOAK — sCO₂ Brayton-Rankine — ignited (Q=∞)")
print(f"LCOE: {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.1f}")
print()

cas = [
    ("CAS10", "Preconstruction",           c.cas10),
    ("CAS21", "Buildings",                 c.cas21),
    ("CAS22", "Reactor Plant Equipment",   c.cas22),
    ("CAS23", "Turbine Plant",             c.cas23),
    ("CAS24", "Electrical Plant",          c.cas24),
    ("CAS25", "Miscellaneous",             c.cas25),
    ("CAS26", "Heat Rejection",            c.cas26),
    ("CAS27", "Special Materials",         c.cas27),
    ("CAS28", "Digital Twin",              c.cas28),
    ("CAS29", "Contingency",               c.cas29),
    ("CAS30", "Indirect Costs",            c.cas30),
    ("CAS40", "Owner's Costs",             c.cas40),
    ("CAS50", "Supplementary",             c.cas50),
    ("CAS60", "IDC",                       c.cas60),
    ("CAS70", "O&M (annualized)",          c.cas70),
    ("CAS80", "Fuel (annualized)",         c.cas80),
    ("CAS90", "Financial",                 c.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")

# CAS22 sub-account detail
print()
print("CAS22 Detail:")
for k, v in result.cas22_detail.items():
    print(f"  {k:<12} {float(v):>10.1f}  M$")

# ── Key Assumptions Summary ──────────────────────────────────────────────────
print()
print("Key Assumptions:")
print("  [UNCERTAIN x3-10] C220103 coil cost: framework tape-winding model does NOT")
print("                    apply to laser-patterned REBCO film. No cost analogue exists.")
print("                    Treat computed value as rough placeholder only.")
print("  [UNCERTAIN x2-3]  C220101 = $400M (Na-cooled fast reactor primary circuit")
print("                    analogue for flowing Li-LiH wall system)")
print("  [UNCERTAIN ±50%]  p_pump = 380 MW (LM circulation dominant load;")
print("                    inferred from published net eff. 34% vs. cycle eff. 50%)")
print("  [UNCERTAIN]       Availability = 92% (maintenance intervals uncharacterized)")
print("  [INFERRED]        P_thermal ≈ 2941 MWth (1 GWe / 0.34 net efficiency)")
print("  [INFERRED]        Recirculating ≈ 471 MW (32% of ~1471 MWe gross)")
print("  [CONFIRMED]       TBR = 1.60 (JNM 599 2024; design req >=1.15; 35% margin)")
print("  [NOTE]            mn=1.07 = blanket energy mult. factor (JNM 599); distinct from")
print("                    Pb (n,2n) neutron number mult. = 1.24 (also in JNM 599)")

# ── Sensitivity Analysis ─────────────────────────────────────────────────────
print()
sens = model.sensitivity(result.params, cost_overrides=_COST_OVERRIDES)

print("Sensitivity (elasticity = %LCOE / %param)")
print("-" * 48)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<36} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<36} {v:+.4f}")

print("\nCosting constants (top 15):")
costing = sorted(sens["costing"].items(), key=lambda x: abs(x[1]), reverse=True)
for k, v in costing[:15]:
    print(f"  {k:<36} {v:+.4f}")

# ── Coil Cost Scenario Analysis ──────────────────────────────────────────────
# C220103 is computed by framework tape-winding model, which is inapplicable to
# laser-patterned REBCO film (factor 3–10× uncertainty, no manufacturing analogue).
# Three scenarios bracket the uncertainty: low (0.3×), mid (1×), high (10×).
print()
print("Coil Cost Scenario Analysis (C220103):")
print("  Tape-winding model NOT applicable to laser-patterned film. 3-10x uncertain.")

c220103_base = float(result.cas22_detail.get("C220103", 0.0))
print(f"  Baseline C220103 (tape-winding placeholder): {c220103_base:.1f} M$")
print()
print(f"  {'Scenario':<10} {'Mult':>6} {'C220103 M$':>12} {'LCOE $/MWh':>12}  Note")
print(f"  {'-'*65}")

_coil_scenarios = [
    ("low",  0.3,  "optimistic: novel film process cheaper than tape-winding"),
    ("mid",  1.0,  "nominal: tape-winding analogue (inapplicable, placeholder)"),
    ("high", 10.0, "pessimistic: first-of-kind manufacturing premium"),
]

_lcoe_vals = {}
for _label, _mult, _note in _coil_scenarios:
    if _mult == 1.0:
        _r = result
    else:
        _c220103_override = {**_COST_OVERRIDES, "C220103": c220103_base * _mult}
        _kwargs = {k: v for k, v in _SHARED_KWARGS.items() if k != "cost_overrides"}
        _r = model.forward(net_electric_mw=NET_ELECTRIC_MW, cost_overrides=_c220103_override, **_kwargs)
    _lcoe_vals[_label] = float(_r.costs.lcoe)
    print(f"  {_label:<10} {_mult:>5.1f}x {c220103_base * _mult:>10.1f}   {float(_r.costs.lcoe):>10.1f}  ({_note})")

print()
print(f"  LCOE range from coil cost uncertainty alone: "
      f"{_lcoe_vals['low']:.1f} – {_lcoe_vals['high']:.1f} $/MWh "
      f"(swing: {_lcoe_vals['high'] - _lcoe_vals['low']:.1f} $/MWh)")

# ── b_max Scenario Sweep ──────────────────────────────────────────────────────
# b_max = peak coil field; 4th-largest LCOE sensitivity lever (elasticity +0.38).
# Published design envelope: 15–40 T (NF 64 2024). REBCO Jc degrades sharply
# above ~20 T at 20 K — the upper end requires larger coil cross-section to
# maintain required current at reduced Jc. This lever is distinct from r_coil:
#   r_coil  → manufacturing cost ($/film-deposition unit), a process uncertainty
#   b_max   → physics-driven field requirement (coil cross-section scales with Jc),
#             a design-point uncertainty linked to REBCO performance limits.
# Source: NF 64 (2024) 026007 (15–40 T published range); see Section 3 REBCO risk.
print()
print("b_max Scenario Sweep (Peak Coil Field, 15–40 T published envelope):")
print("  Sensitivity elasticity: +0.38 (4th-largest engineering lever)")
print("  Mechanism: peak field drives coil cross-section at fixed Jc → scales C220103")
print("  Independent from r_coil sweep: field requirement vs. manufacturing cost")
print()
print(f"  {'b_max (T)':>10} {'LCOE ($/MWh)':>14}  Note")
print(f"  {'-'*60}")

_bmax_scenarios = [
    (15.0, "baseline (primary design target)"),
    (20.0, "REBCO Jc knee threshold at 20 K"),
    (25.0, "high-field operating regime"),
    (30.0, "upper-mid design envelope"),
    (40.0, "maximum published design target"),
]

_bmax_lcoe_vals = {}
for _bmax, _note in _bmax_scenarios:
    _kwargs_bmax = {k: v for k, v in _SHARED_KWARGS.items()
                   if k not in ("cost_overrides", "b_max")}
    _kwargs_bmax["b_max"] = _bmax
    _r_bmax = model.forward(
        net_electric_mw=NET_ELECTRIC_MW, cost_overrides=_COST_OVERRIDES, **_kwargs_bmax
    )
    _bmax_lcoe_vals[_bmax] = float(_r_bmax.costs.lcoe)
    _marker = " ← baseline" if _bmax == 15.0 else ""
    print(f"  {_bmax:>10.0f} {float(_r_bmax.costs.lcoe):>14.1f}  ({_note}){_marker}")

print()
print(f"  LCOE range from peak field uncertainty alone: "
      f"{min(_bmax_lcoe_vals.values()):.1f} – {max(_bmax_lcoe_vals.values()):.1f} $/MWh "
      f"(swing: {max(_bmax_lcoe_vals.values()) - min(_bmax_lcoe_vals.values()):.1f} $/MWh)")
print("  Note: 15→40 T represents the published design uncertainty band, not")
print("  a single well-characterised operating point. The 3–10× coil cost and")
print("  the peak field uncertainty are compounding risks in C220103.")

# ── ISS04 Confinement Scaling — Design Point Closure ─────────────────────────
# The ISS04 scaling is the current recommended stellarator confinement scaling
# in UKAEA PROCESS. It allows first-principles estimation of τ_E, plasma density
# design point, and Lawson criterion closure for the published machine geometry.
#
# Formula (UKAEA PROCESS stellarator documentation):
#   τ_E = 0.134 · R₀^0.64 · a_p^2.28 · n₂₀^0.54 · B₀^0.84 · P^-0.61 · ī^0.41
# where: R₀ [m], a_p [m], n₂₀ [10²⁰ m⁻³], B₀ [T], P [MW], ī = rotational transform
#
# Alternative scalings for bounding uncertainty (all from UKAEA PROCESS):
#   ISS95: τ_E = 0.079 · R₀^0.65 · a^2.21 · n₂₀^0.51 · B₀^0.83 · P^-0.59 · ī^0.40
#   LHD:   τ_E = 0.036 · R₀^0.75 · a^2.0  · n₂₀^0.69 · B₀^0.84 · P^-0.58  (no ī dep.)
#
# Sudo stellarator density limit:
#   n_max [10²⁰ m⁻³] = 0.25 · sqrt(P·B₀ / (R₀·a_p²))   [P in MW]
#   Note: extrapolation to high-power reactor scale is "unclear" per PROCESS docs.
#
# Beta limit: β ≤ 5% (3-D MHD stability; PROCESS hard constraint for stellarators)

_ISS04_R0     = 4.0    # m  (NF 64 2024)
_ISS04_a      = 1.0    # m  (= R0/A = 4/4)
_ISS04_B0     = 10.0   # T  (NF 64 2024)
_ISS04_T_keV  = 10.0   # keV (nominal; T_e in model)
_ISS04_V      = 200.0  # m³ (plasma volume — UNCERTAIN; compact QI geometry)

# Physical constants and D-T cross-section at T = 10 keV
_mu0     = 4 * math.pi * 1e-7          # T·m/A
_kT_J    = _ISS04_T_keV * 1e3 * 1.602e-19   # J  (1 keV = 1.602×10⁻¹⁶ J)
_Ealpha  = 3.52e6 * 1.602e-19          # J  (alpha particle energy)
_Efus    = 17.6e6 * 1.602e-19          # J  (total D-T fusion energy)
_sigv_10 = 1.1e-22                     # m³/s  (<σv>_DT at T=10 keV)

# Lawson ignition criterion at T = 10 keV (n·τ_E condition for Q=∞)
#   (n_e/2)²·<σv>·E_α = 3·n_e·kT/τ_E  →  n_e·τ_E = 12·kT/(<σv>·E_α)
_lawson_ntau = 12 * _kT_J / (_sigv_10 * _Ealpha)   # m⁻³·s

# Beta density limit: β = 2n_e·kT·μ₀/B² ≤ 0.05
_n_beta_m3 = 0.025 * _ISS04_B0**2 / (_mu0 * _kT_J)
_n_beta_20 = _n_beta_m3 / 1e20   # 10²⁰ m⁻³

# Design density from 2 GW fusion power target at T = 10 keV:
#   P_fus = (n_e/2)²·<σv>·E_fus·V  →  n_e = 2·sqrt(P_fus/(<σv>·E_fus·V))
_P_fus_W       = 2000e6   # W  (2 GW; implied by 1 GWe net at ~34% net efficiency)
_n_e_design    = 2 * math.sqrt(_P_fus_W / (_sigv_10 * _Efus * _ISS04_V))  # m⁻³
_n_e20_design  = _n_e_design / 1e20
_P_alpha_MW    = _P_fus_W / 5 / 1e6   # MW  (alphas = 20% of fusion energy)
_beta_design   = 2 * _n_e_design * _kT_J * _mu0 / _ISS04_B0**2

def _iss04(R0, a, n20, B0, P_MW, iota):
    """ISS04 energy confinement time scaling (UKAEA PROCESS, recommended)."""
    return 0.134 * R0**0.64 * a**2.28 * n20**0.54 * B0**0.84 * P_MW**-0.61 * iota**0.41

def _iss95(R0, a, n20, B0, P_MW, iota):
    """ISS95 confinement time scaling (UKAEA PROCESS)."""
    return 0.079 * R0**0.65 * a**2.21 * n20**0.51 * B0**0.83 * P_MW**-0.59 * iota**0.40

def _lhd_scaling(R0, a, n20, B0, P_MW):
    """LHD scaling (UKAEA PROCESS; no rotational transform dependence)."""
    return 0.036 * R0**0.75 * a**2.0 * n20**0.69 * B0**0.84 * P_MW**-0.58

def _sudo_n20(P_MW, B0, R0, a):
    """Sudo stellarator density limit in units of 10²⁰ m⁻³."""
    return 0.25 * math.sqrt(P_MW * B0 / (R0 * a**2))

print()
print("ISS04 Confinement Scaling — Q=∞ Feasibility Check")
print("  τ_E = 0.134 · R₀^0.64 · a^2.28 · n₂₀^0.54 · B₀^0.84 · P^-0.61 · ī^0.41")
print("  Source: UKAEA PROCESS stellarator documentation (ISS04; current recommended scaling)")
print(f"  Machine geometry: R₀={_ISS04_R0} m, a={_ISS04_a} m, B₀={_ISS04_B0} T, V={_ISS04_V} m³")
print(f"  Derived design density (P_fus=2 GW, T=10 keV): n_e = {_n_e20_design:.2f}×10²⁰ m⁻³")
print(f"  Alpha heating at design point: P_α = {_P_alpha_MW:.0f} MW")
print(f"  Plasma beta at design point: β = {_beta_design*100:.1f}%  (5% limit: NOT binding)")
print(f"  Beta density ceiling: {_n_beta_20:.1f}×10²⁰ m⁻³  (design is {_n_beta_20/_n_e20_design:.1f}× headroom)")
print(f"  Lawson ignition criterion (T=10 keV): n·τ_E ≥ {_lawson_ntau:.2e} m⁻³·s")
print()
print(f"  {'ī':>6} {'τ_ISS04 s':>11} {'τ_ISS95 s':>11} {'τ_LHD s':>11} "
      f"{'n·τ_ISS04':>13} {'ign. margin':>12} {'n_Sudo':>8}")
print(f"  {'-'*80}")

_sudo_n20_val = _sudo_n20(_P_alpha_MW, _ISS04_B0, _ISS04_R0, _ISS04_a)
for _iota in [0.25, 0.30, 0.35, 0.40, 0.45, 0.50]:
    _tau04  = _iss04(_ISS04_R0, _ISS04_a, _n_e20_design, _ISS04_B0, _P_alpha_MW, _iota)
    _tau95  = _iss95(_ISS04_R0, _ISS04_a, _n_e20_design, _ISS04_B0, _P_alpha_MW, _iota)
    _taulhd = _lhd_scaling(_ISS04_R0, _ISS04_a, _n_e20_design, _ISS04_B0, _P_alpha_MW)
    _ntau04 = _n_e_design * _tau04
    _margin = _ntau04 / _lawson_ntau
    print(f"  {_iota:>6.2f} {_tau04:>11.3f} {_tau95:>11.3f} {_taulhd:>11.3f} "
          f"{_ntau04:>13.2e} {_margin:>12.3f} {_sudo_n20_val:>8.2f}")

print()
_tau04_mid = _iss04(_ISS04_R0, _ISS04_a, _n_e20_design, _ISS04_B0, _P_alpha_MW, 0.35)
_margin_mid = _n_e_design * _tau04_mid / _lawson_ntau
print(f"  ISS04 ignition margin at ī=0.35: {_margin_mid:.3f}×  "
      f"(~{1/_margin_mid:.0f}× below Lawson threshold)")
print(f"  Sudo density limit: {_sudo_n20_val:.2f}×10²⁰ m⁻³ — design density "
      f"({_n_e20_design:.2f}×10²⁰) is NOT binding")
print()
print("  INTERPRETATION:")
print(f"  ISS04 extrapolated to this geometry predicts τ_E ≈ {_tau04_mid*1e3:.0f} ms at ī=0.35,")
print(f"  yielding n·τ_E ≈ {_n_e_design * _tau04_mid:.1e} m⁻³·s — ~{1/_margin_mid:.0f}× below the Lawson")
print("  ignition threshold. This is Gap #7 quantified: Q=∞ closure is NOT supported")
print("  by ISS04 extrapolation at T=10 keV. The design likely relies on one or more of:")
print("    (a) Higher operating temperature (20–30 keV where <σv>/T² peaks for D-T)")
print("    (b) Confinement improvement beyond ISS04 from high-field QI optimization")
print("    (c) Plasma volume larger than 200 m³ (UNCERTAIN; no published geometry detail)")
print("  The beta limit (5%) and Sudo density limit are NOT binding at the 2 GW design")
print("  density — these constraints leave headroom; the ignition gap is confinement time.")
print("  ISS95 and LHD scalings bracket ISS04; none closes the ignition gap at T=10 keV.")
