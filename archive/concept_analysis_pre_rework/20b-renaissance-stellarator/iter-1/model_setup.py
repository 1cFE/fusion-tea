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
    - mn: 1.24 (Pb pebble neutron multiplier; default = 1.1)
    - R0: 4.0 m (compact; default = 5.5 m)
    - blanket_t: 0.33 m (15 cm Pb + 18 cm Li-LiH; default = 0.80 m)
    - ht_shield_t: 0.50 m (50 cm VH₂ outer shield; default = 0.20 m)
    - C220101: $400M override (LM wall system vs. volume-based $0.60M/m³ default)
"""

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

# Availability: estimated 90–95% (steady-state, no disruptions, no pulse cycling)
# Source: analysis.md §5; company website confirms "near-100% duty cycle"
# UNCERTAIN: actual maintenance intervals for LM wall + pump systems uncharacterized
AVAILABILITY = 0.92

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
    eta_th=0.50,      # sCO₂ Brayton-Rankine combined cycle; mid-range of 49–51%;
                      # ECM 276 (2023) 116572; overrides PowerCycle.BRAYTON_SCO2 default (0.47)

    # Pb pebble layer neutron energy multiplication factor
    # Source: JNM 599 (2024) 155239 — NOTE: fm ≠ TBR; TBR is unconfirmed in available sources
    mn=1.24,

    # ── Ignited plasma — NNBI startup only ───────────────────────────────────
    # Q=∞ target: zero steady-state heating power at operating point
    # Source: Nuclear Fusion 64 (2024) 026007
    p_input=0.0,      # Ignited; NNBI runs only during ramp-up, not at steady state
    p_nbi=0.0,        # No NBI at operating point (startup-only; capital cost absorbed elsewhere)
    p_ecrh=0.0,       # No ECRH required (ignited — no current drive, no steady-state heating)
    eta_pin=0.60,     # NNBI neutralization efficiency (startup sizing reference);
                      # NF 64 (2024) 026007; irrelevant at p_input=0
    eta_p=0.50,       # DEFAULT: pumping efficiency
    eta_de=0.85,      # DEFAULT: DEC efficiency (no DEC deployed)
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
print("  [UNCONFIRMED]     TBR: fm=1.24 confirmed (Pb pebble neutron mult.);")
print("                    TBR (tritium breeding ratio) not confirmed in available sources")

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
