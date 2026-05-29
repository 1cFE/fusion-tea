"""1costingfe model: State-Backed Tokamak - BEST (Neo Fusion) — Commercial PFPP Analogue.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling approach:
    BEST (Burning Plasma Experimental Superconducting Tokamak) is an experimental
    device — it generates no electricity and is not itself the TEA target. This model
    represents the commercial PFPP (Prototype Fusion Power Plant) descendant that
    China's fusion roadmap (EAST → BEST → CFEDR → PFPP) aims to produce.

Concept rationale:
    The commercial PFPP is characterized by analogy to ARIES-ACT1 (R₀ = 6.25 m,
    B₀ = 6.0 T, A ≈ 4), the closest published plant study to the updated CFETR
    configuration (R₀ = 6.6 m, B₀ = 6.0 T, arxiv-1907-11919) for a conventional-
    aspect-ratio D-T tokamak at commercial scale with LTS-primary magnets.
    ARIES-AT (R₀ = 5.2 m) was the prior analogue but its smaller geometry
    introduces systematic error in capital cost scaling for a 6.6 m machine.
    BEST parameters (R₀ = 3.6 m, B₀ = 6.15 T, Ip = 7 MA) constrain the
    experimental device, not the commercial end-state.

Key deviations from framework defaults:
    - eta_th = 0.347: sCO2 Brayton efficiency from published CFETR/BEST lineage
      studies (cfetr-power-conversion-studies.md); overrides framework preset of 0.47
    - R0 = 6.25 m, plasma_t = 1.5625 m: ARIES-ACT1 analogue for commercial PFPP scale
    - p_input = 200 MW: Q~10 estimate for commercial PFPP (P_fusion/Q ≈ 2200/10)
    - p_cryo = 8.0 MW: LTS Nb3Sn TF/PF coils at 4.5 K; substantially larger than
      HTS designs (which operate at 20 K or 77 K); scaled from ITER cryoplant
    - eta_pin = 0.60: weighted average of BEST 4-method H&CD portfolio (NBI 65%,
      ECRH 52%, ICRH 75%, LHCD 52%)
    - availability = 0.85: canonical per scoring_framework.md §Plant availability (MCF quasi-steady, D-T)

CRITICAL UNCERTAINTY: The PFPP design point is completely unpublished. All machine
    parameters, cost overrides, and efficiency assumptions are by analogy. The LCOE
    output should be treated as a parameterized estimate with very low confidence.
    The Chinese construction cost advantage (2–4× lower than Western baseline) is NOT
    applied as a hard override — its magnitude in fusion context is uncharacterized.
"""

from costingfe import ConfinementConcept, CostModel, Fuel, PowerCycle

# ── Model creation ────────────────────────────────────────────────────────────
# sCO2 Brayton power cycle: sets appropriate CAS23/CAS26 BOP cost coefficients
# for compact, high-efficiency turbomachinery. eta_th overridden below to the
# published CFETR study value (34.7%) rather than the framework preset (47%).
# Source: cfetr-power-conversion-studies.md §Conclusions
model = CostModel(
    concept=ConfinementConcept.TOKAMAK,
    fuel=Fuel.DT,
    power_cycle=PowerCycle.BRAYTON_SCO2,
)

# ── Plant configuration ───────────────────────────────────────────────────────

# Commercial PFPP target: 1 GW net electric
# Source: analysis.md §S5 "Chinese program targets 1 GW class"; analogue to DEMO-class
# Confidence: low — no published PFPP design point
# UKAEA scaling (extrapolation paper): economic optimum 500 MW – 1.2 GW net; LCOE reductions
# diminish sharply beyond 1.2 GW. 1 GW is within the optimal range; supports this assumption.
# Gross-to-net ratio (UKAEA): 42% at 1.2 GW net, degrades to 17% at 100 MW net due to
# recirculating power. At 1 GW, recirculating fraction is modest but non-trivial for LTS
# (large cryoplant + H&CD). Confidence: low — no PFPP-specific ratio published.
NET_ELECTRIC_MW = 1000.0

# Availability: canonical value per scoring_framework.md §Plant availability (MCF quasi-steady, D-T).
# Previously 0.80 (Araiinejad & Shirvan 2025 analogue midpoint); replaced by project-wide policy.
# Tier-A override (externally-published target with stated basis) not available for this concept.
# UNCERTAIN: CFETR Phase I (OSTI 1465662) reports duty cycle 0.3–0.5 for pulsed operation.
# If PFPP inherits pulsed characteristics, CF = 30–50% (not 75–90%). Two scenarios below.
# Central case assumes quasi-steady-state PFPP (justified by BEST's long-pulse design target);
# pulsed scenario uses CFETR Phase I data as lower bound.
AVAILABILITY = 0.85

LIFETIME_YR = 30         # Standard commercial plant assumption; DEFAULT

# Construction time: 8 years — large LTS tokamak with ITER-lessons but
# Chinese construction efficiency assumed; ITER itself took 20+ years
# UNCERTAIN: No PFPP schedule published
CONSTRUCTION_TIME_YR = 8.0


# ── Shared kwargs ─────────────────────────────────────────────────────────────
# Factored here for clarity; passed directly to model.forward()

_SHARED_KWARGS = dict(
    # ── Economics ─────────────────────────────────────────────────────────────
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=CONSTRUCTION_TIME_YR,

    # ── Geometry: ARIES-ACT1 analogue for conventional-aspect-ratio LTS tokamak ─
    # Source: ARIES-ACT1 (osti-servlets-purl-1178069): R₀ = 6.25 m, B₀ = 6.0 T
    # Replaces prior ARIES-AT analogue (R₀ = 5.2 m) — ARIES-ACT1 geometry matches
    # updated CFETR Phase I (R₀ = 6.6 m, B₀ = 6.0 T, arxiv-1907-11919) far more
    # closely. Capital cost drivers (magnet conductor, vacuum vessel, structural steel)
    # scale non-linearly with R; applying 5.2 m scaling to a 6.6 m machine introduces
    # systematic upward error (volume scales ~R³, implying ~55% more material at 6.6 m).
    # UNCERTAIN: Commercial PFPP geometry completely unspecified; B₀ ≈ 6–8 T likely
    R0=6.25,             # Major radius [m]; ARIES-ACT1 analogue; analysis.md §S7
    plasma_t=1.5625,     # Minor radius a [m]; A ≈ 4.0; ARIES-ACT1 analogue
    elon=1.7,            # Elongation κ; conventional aspect ratio; ARIES-AT analogue
    blanket_t=0.80,      # Blanket thickness [m]; DEFAULT — PFPP blanket tech undecided
                         # UNCERTAIN: COOL/WCCB/WCLL TBM result will set this; analysis.md §S2
                         # UKAEA fluence budget: 10–20 MW-yr/m² blanket allowance is a primary
                         # cost lever (drives replacement schedule and CAS72); see scenario below
    ht_shield_t=0.30,    # High-T shield [m]; slightly thicker for LTS protection
    structure_t=0.20,    # Primary structure [m]; DEFAULT
    vessel_t=0.20,       # Vacuum vessel [m]; DEFAULT

    # ── Magnet parameters: LTS Nb3Sn TF + NbTi PF (ITER-heritage) ────────────
    # Source: best-research-plan-v1.1-summary.md §Section 1.3
    # B₀ = 6.15 T (BEST); ARIES-ACT1 B₀ = 6.0 T; PFPP likely 6–8 T at plasma center
    # Peak TF conductor field: Nb3Sn operational limit ≈ 13–16 T
    b_max=13.0,          # Peak conductor field [T]; Nb3Sn hard limit; analysis.md §S3
    r_coil=3.2,          # Winding bore radius [m]; R₀-a-blanket-shield-struct-vessel
                         # = 6.25-1.5625-0.80-0.30-0.20-0.20 ≈ 3.19 → 3.2; ARIES-ACT1

    # ── Power balance ─────────────────────────────────────────────────────────
    # Heating power: Q~10 commercial PFPP estimate
    # P_fusion ≈ 2200 MWth (for 1 GWe at 34.7% eff, mn=1.1)
    # P_aux = P_fusion / Q ≈ 2200 / 10 ≈ 220 MW → rounded to 200 MW
    # Source: analysis.md §S2 "Q value (commercial PFPP): estimated 5–15"
    # UNCERTAIN: Q value and P_aux completely unanchored for PFPP
    p_input=200.0,       # Auxiliary heating power [MW]; Q~10 analogue; analysis.md §S5

    mn=1.1,              # Neutron energy multiplier; DEFAULT for D-T blanket

    # Thermal efficiency: sCO2 Brayton at 34.7% from CFETR/BEST lineage studies
    # Source: cfetr-power-conversion-studies.md §Conclusions
    # Preferred cycle in published studies; not formally committed for PFPP
    # Literature range: 34.7% (preliminary) to 42.8–53.7% (advanced recompression)
    # UNCERTAIN: sCO2 not formally adopted; blanket coolant choice affects this

    # Heating system wall-plug efficiency: weighted average of BEST 4-method portfolio
    # NBI (60–70%) + ECRH (50–55%) + ICRH (70–80%) + LHCD (50–55%)
    # Mix at BEST: 12MW NBI + 15MW ECRH + 10MW ICRH + 10MW LHCD
    # Weighted avg = (12×0.65 + 15×0.52 + 10×0.75 + 10×0.52) / 47 ≈ 0.60
    # UNCERTAIN: Commercial PFPP H&CD portfolio unspecified; LHCD may not penetrate
    # burning plasma (high-T cutoff); analysis.md §S2 Challenge 4
    eta_pin=0.60,        # H&CD wall-plug efficiency; analysis.md §S2 Challenge 4

    eta_p=0.5,           # Pumping efficiency; DEFAULT
    f_sub=0.04,          # Subsystem power fraction; slightly elevated for LTS
                         # support infrastructure; analysis.md §S3 Magnet System

    # Parasitic power consumers
    p_coils=5.0,         # Coil power [MW]; superconducting but quench protection,
                         # switching, bus joints; scaled from ITER experience; DEFAULT+
    p_cool=25.0,         # Cooling systems [MW]; large machine with active W first-wall
                         # cooling (4 MPa water, 240 modules); analysis.md §S3 FW
    p_pump=2.0,          # Pumping power [MW]; scaled for larger machine; DEFAULT+
    p_trit=10.0,         # Tritium processing [MW]; DEFAULT — T fuel cycle at plant scale
    p_house=5.0,         # Housekeeping [MW]; scaled for commercial plant; DEFAULT+

    # Cryogenic system: LTS Nb3Sn/NbTi coils at 4.5 K — significant parasitic load
    # ITER cryoplant: ~36 MW electrical for ~40 kW@4.5K cooling / ~10,000t cold mass
    # PFPP cold mass estimate ~3000t (15% of ITER) → ~6–8 MW electrical equivalent
    # Source: analysis.md §S4 "Helium (Magnet Cooling)"; analysis.md §S2 Challenge 3
    p_cryo=8.0,          # Cryogenic power [MW]; LTS 4.5K; analysis.md §S4

    # ── Plasma parameters ────────────────────────────────────────────────────
    # Burning plasma regime for commercial PFPP (Q~10, T_e~20 keV)
    n_e=1.0e20,          # Electron density [m⁻³]; DEFAULT
    T_e=20.0,            # Electron temperature [keV]; elevated for burning plasma
                         # regime; cf. BEST target Q~5: T_e ~ 15–25 keV; DEFAULT+
    Z_eff=1.5,           # Effective charge; full-W first wall; analysis.md §S3 FW
    plasma_volume=513.0, # Plasma volume [m³]; derived: 2π²R₀a²κ = 2π²×6.25×2.441×1.7
                         # (R₀=6.25 m, a=1.5625 m, κ=1.7); ARIES-ACT1 analogue
    B=6.0,               # Magnetic field at plasma center [T]; ARIES-ACT1/CFETR 2019
                         # both use B₀=6.0 T; analysis.md §S5
    wall_material="W",   # Full-tungsten FW; analysis.md §S3 FW
    T_edge=0.05,         # Edge temperature [keV]; detached divertor; DEFAULT
    tau_ratio=3.0,       # Impurity confinement / energy confinement; DEFAULT

    # ── Cost overrides: none applied ─────────────────────────────────────────
    # No published capital cost data exists for BEST, CFEDR, or PFPP.
    # The PFPP overnight cost estimate ($5–15B for 500–1000 MWe) in analysis.md §S5
    # is too uncertain to anchor any CAS account.
    #
    # KEY UNMODELED FACTOR — Chinese construction cost discount (analysis.md §S2):
    #   CAS21 (buildings): likely 2–4× lower than Western baseline (labor + supply chain)
    #   This discount is NOT applied here; its fusion-specific magnitude is unknown.
    #   Run a sensitivity: cost_overrides={"CAS21": <base_cas21>/2} for 2× discount.
    #
    # KEY UNMODELED FACTOR — Blanket technology (analysis.md §S2, §S5):
    #   COOL (CO2-cooled LiPb): CAS27 ≈ default $15M (PbLi fill)
    #   WCCB (water-cooled ceramic breeder, Be12Ti multiplier): CAS27 ≈ $200M
    #   Decision awaits BEST TBM experimental results (~2030s)
    #
    # KEY UNMODELED FACTOR — Stewart & Shirvan 2.2× regulatory building cost factor:
    #   The 21-spherical-tokamak-hts analysis applied this as an upper-bound scenario.
    #   May not apply in Chinese regulatory context (analysis.md §S2 Challenge 2).
    #   Upper-bound scenario: cost_overrides={"CAS21": <base_cas21> * 2.2}
)

# ── Forward model ─────────────────────────────────────────────────────────────
# Native design point is 1000 MWe — no result_1gw needed.
result = model.forward(net_electric_mw=NET_ELECTRIC_MW, **_SHARED_KWARGS)

# ── Results printing ──────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("State-Backed Tokamak - BEST → Commercial PFPP Analogue (Neo Fusion / ASIPP)")
print("ARIES-ACT1 geometry | sCO2 Brayton 34.7% | Q~10 | LTS Nb3Sn | NOAK")
print(f"LCOE: {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.2f}")
print()

cas_accounts = [
    ("CAS10", "Preconstruction",            c.cas10),
    ("CAS21", "Buildings",                  c.cas21),
    ("CAS22", "Reactor Plant Equipment",    c.cas22),
    ("CAS23", "Turbine Plant",              c.cas23),
    ("CAS24", "Electrical Plant",           c.cas24),
    ("CAS25", "Miscellaneous",              c.cas25),
    ("CAS26", "Heat Rejection",             c.cas26),
    ("CAS27", "Special Materials",          c.cas27),
    ("CAS28", "Digital Twin",               c.cas28),
    ("CAS29", "Contingency",               c.cas29),
    ("CAS30", "Indirect Costs",             c.cas30),
    ("CAS40", "Owner's Costs",              c.cas40),
    ("CAS50", "Supplementary",              c.cas50),
    ("CAS60", "IDC",                        c.cas60),
    ("CAS70", "O&M (annualized)",           c.cas70),
    ("CAS80", "Fuel (annualized)",          c.cas80),
    ("CAS90", "Financial",                  c.cas90),
]

print(f"{'Code':<8} {'Account':<30} {'M$':>10}")
print("-" * 50)
for code, name, val in cas_accounts:
    print(f"{code:<8} {name:<30} {float(val):>10.1f}")
print("-" * 50)
print(f"{'':8} {'Total Capital':<30} {float(c.total_capital):>10.1f}")

# ── CAS22 breakdown ───────────────────────────────────────────────────────────
print()
print("CAS22 Sub-account Detail:")
for k, v in result.cas22_detail.items():
    print(f"  {k}: {float(v):.1f} M$")

# ── Key assumptions summary ───────────────────────────────────────────────────
print()
print("Key Assumptions (PFPP Commercial Analogue — Very Low Confidence):")
print(f"  Commercial PFPP native power:    {NET_ELECTRIC_MW:.0f} MWe (no published design point)")
print(f"  Geometry analogue:               ARIES-ACT1 (R₀=6.25m, a=1.5625m, κ=1.7; osti-servlets-purl-1178069)")
print(f"  Magnet technology:               LTS Nb3Sn/NbTi TF/PF + YBCO CS sub-coils")
print(f"  Thermal efficiency:              {result.params['eta_th']:.3f} (from costingfe power_cycle preset)")
print(f"  Availability:                    {AVAILABILITY:.0%} (canonical per scoring_framework.md §Plant availability; previously 0.80)")
print(f"  Q value implied (commercial):    ~10 (drives p_input = {_SHARED_KWARGS['p_input']:.0f} MW)")
print(f"  H&CD wall-plug efficiency:       {_SHARED_KWARGS['eta_pin']:.2f} (4-method portfolio avg)")
print(f"  Cryogenic load (LTS 4.5K):      {_SHARED_KWARGS['p_cryo']:.1f} MW (ITER-scaled)")
print(f"  Blanket technology:              DEFAULT (PbLi; COOL/WCCB/WCLL undecided)")
print(f"  Chinese construction discount:   NOT APPLIED (unknown magnitude in fusion context)")
print(f"  Regulatory 2.2× factor:          NOT APPLIED (Chinese context uncertain)")
print(f"  NOAK:                            {result.params['noak']}")
print(f"  Construction time:               {CONSTRUCTION_TIME_YR:.0f} yr (UNCERTAIN)")

# ── Scenario analysis ────────────────────────────────────────────────────────
# Carried F-1: Chinese construction cost discount — the single most important PFPP
# differentiator. H1 hypothesis requires ~60 $/MWh LCOE reduction at 2× discount.
# Applying discount only to CAS21 (buildings, ~8% of capital) cannot produce this —
# the discount must cover all direct capital accounts CAS21–CAS26 to test H1.
# CAS21 buildings + CAS22 reactor plant + CAS23 turbine + CAS24 electrical +
# CAS25 miscellaneous + CAS26 heat rejection ≈ 57% of overnight capital.
# Source: analysis.md §S2 Challenge 1, H1 hypothesis.
_direct_accounts = {
    "CAS21": float(c.cas21),
    "CAS22": float(c.cas22),
    "CAS23": float(c.cas23),
    "CAS24": float(c.cas24),
    "CAS25": float(c.cas25),
    "CAS26": float(c.cas26),
}
_base_direct_total = sum(_direct_accounts.values())
print()
print("Scenario: Chinese construction cost discount (CAS21–CAS26 direct capital accounts)")
print("  Source: analysis.md §S2 Challenge 1; H1 hypothesis requires broad discount to test")
print(f"  Base direct capital CAS21–CAS26 (Western/NOAK):")
for _k, _v in _direct_accounts.items():
    print(f"    {_k}: {_v:.0f} M$")
print(f"  Total direct: {_base_direct_total:.0f} M$")
for _factor, _label in [(1.0, "No discount (Western baseline)"),
                         (2.0, "2× Chinese discount — central estimate (H1 test)"),
                         (4.0, "4× Chinese discount — optimistic estimate")]:
    _r = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        cost_overrides={k: v / _factor for k, v in _direct_accounts.items()},
        **_SHARED_KWARGS,
    )
    print(f"  {_label}: direct={_base_direct_total/_factor:.0f} M$ → LCOE={_r.costs.lcoe:.1f} $/MWh")

# Regulatory cost factor: Stewart & Shirvan 2.2× applied to CAS21 only
# May not apply in Chinese regulatory context; included as Western-upper-bound scenario
_r_reg = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    cost_overrides={"CAS21": _direct_accounts["CAS21"] * 2.2},
    **_SHARED_KWARGS,
)
print(f"  Western 2.2× regulatory factor (CAS21 only): CAS21={_direct_accounts['CAS21']*2.2:.0f} M$"
      f" → LCOE={_r_reg.costs.lcoe:.1f} $/MWh")

# F-1: Capacity factor — quasi-steady-state vs pulsed CFETR-lineage operation
# CFETR Phase I (OSTI 1465662): duty cycle 0.3–0.5 for pulsed intermediate step.
# Central case (AVAILABILITY=0.85, canonical) assumes quasi-steady-state PFPP; pulsed cases show
# LCOE impact if PFPP inherits CFETR pulsed characteristics.
_kwargs_no_avail = {k: v for k, v in _SHARED_KWARGS.items() if k != 'availability'}
print()
print("Scenario: Capacity factor — quasi-steady-state vs. pulsed operation")
print("  Source F-1: CFETR Phase I duty cycle 0.3–0.5 (OSTI 1465662) vs. quasi-steady-state")
for _cf, _label in [
    (0.35, "Pulsed low  — CFETR Phase I duty cycle ~0.3"),
    (0.50, "Pulsed high — CFETR Phase I duty cycle ~0.5"),
    (0.85, "Central     — canonical MCF quasi-steady D-T (scoring_framework.md)"),
    (0.90, "QSS upper   — Araiinejad & Shirvan analogue upper bound"),
]:
    _r_cf = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        availability=_cf,
        **_kwargs_no_avail,
    )
    print(f"  CF={_cf:.0%}: {_label}: LCOE={_r_cf.costs.lcoe:.1f} $/MWh")

# Carried F-3: Blanket technology scenario — COOL/PbLi+sCO2 vs. WCCB/Rankine
# (a) COOL/PbLi: sCO2 Brayton, eta_th=34.7% — current base case (model already uses this)
# (b) WCCB/ceramic breeder: steam Rankine at 26.4% — lower thermal efficiency, different
#     BOP cost structure. Source: analysis.md §S2 Challenge 5, §S6 Gap 3.
_model_rankine = CostModel(
    concept=ConfinementConcept.TOKAMAK,
    fuel=Fuel.DT,
    power_cycle=PowerCycle.RANKINE,
)
_wccb_kwargs = dict(_SHARED_KWARGS)
_wccb_kwargs['eta_th'] = 0.264  # Steam Rankine at 26.4% for WCCB/water-cooled ceramic breeder
_r_wccb = _model_rankine.forward(net_electric_mw=NET_ELECTRIC_MW, **_wccb_kwargs)
print()
print("Scenario: Blanket technology — COOL/PbLi+sCO2 vs. WCCB/ceramic breeder+Rankine")
print("  Source F-3 carried: analysis.md §S2 Challenge 5, §S6 Gap 3")
print(f"  (a) COOL/PbLi + sCO2 Brayton  (eta_th=34.7%): LCOE={c.lcoe:.1f} $/MWh  [base case]")
print(f"  (b) WCCB/ceramic + Rankine     (eta_th=26.4%): LCOE={_r_wccb.costs.lcoe:.1f} $/MWh")
print(f"  Delta: {_r_wccb.costs.lcoe - c.lcoe:+.1f} $/MWh for WCCB vs. COOL")

# ── Sensitivity analysis ──────────────────────────────────────────────────────
sens = model.sensitivity(result.params)

print()
print("Sensitivity (elasticity = %LCOE / %param)")
print("-" * 50)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<38} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<38} {v:+.4f}")

print("\nCosting constants (top 15):")
costing = sorted(sens["costing"].items(), key=lambda x: abs(x[1]), reverse=True)
for k, v in costing[:15]:
    print(f"  {k:<38} {v:+.4f}")

# F-1: CF sweep — quantifies LCOE impact over full quasi-steady-state to pulsed range
# Source: CFETR Phase I duty cycle 0.3–0.5 (OSTI 1465662) establishes pulsed lower bound;
# canonical central case 0.85 per scoring_framework.md §Plant availability.
print()
print("Capacity factor sweep (CF = 0.35 → 0.90: pulsed CFETR to quasi-steady-state):")
_cf_sweep = [0.35, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90]
_kwargs_no_avail_s = {k: v for k, v in _SHARED_KWARGS.items() if k != 'availability'}
for _cf in _cf_sweep:
    _r_s = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        availability=_cf,
        **_kwargs_no_avail_s,
    )
    _marker = " ← base" if _cf == AVAILABILITY else ""
    print(f"  CF={_cf:.2f}: LCOE={_r_s.costs.lcoe:.1f} $/MWh{_marker}")

# F-2 (carried): Q sweep — reveals cliff-edge behavior near minimum viable Q
# The analysis identifies Q as low-confidence spanning 5–15 but the base model
# fixes Q~10. At low Q, auxiliary heating power consumes a large fraction of gross
# electrical output, non-linearly degrading net output and driving up LCOE.
# At Q≈5: p_input_thermal ≈ p_fus/5; p_input_electrical ≈ p_input_thermal/eta_pin,
# which at eta_pin=0.60 can approach or exceed gross electrical output.
# p_input for each Q computed from base p_fus: p_input = p_fus_ref / Q.
# Source: analysis.md §S2 Challenge 3, §S6 Gap 11.
_p_fus_ref = float(pt.p_fus)
_kwargs_no_pinput = {k: v for k, v in _SHARED_KWARGS.items() if k != 'p_input'}
print()
print("Q sweep (Q = 5 → 15: minimum viable to optimistic commercial PFPP range):")
print("  Source F-2 (carried): analysis.md §S2 Challenge 3, §S6 Gap 11")
print(f"  Reference: p_fus={_p_fus_ref:.0f} MW at Q~10 (p_input={_SHARED_KWARGS['p_input']:.0f} MW)")
print(f"  Note: p_input at each Q = p_fus_ref / Q (first-order approximation)")
print(f"  {'Q':>4}  {'p_input_th':>12}  {'p_input_elec':>13}  {'LCOE':>10}  {'p_net':>8}")
for _q in [5, 6, 7, 8, 9, 10, 12, 15]:
    _p_input_th = _p_fus_ref / _q         # thermal power to plasma [MW]
    _p_input_elec = _p_input_th / _SHARED_KWARGS['eta_pin']  # wall-plug elec draw [MW]
    _r_q = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        p_input=_p_input_th,
        **_kwargs_no_pinput,
    )
    _marker = " ← base" if _q == 10 else ""
    print(f"  Q={_q:2d}: p_in_th={_p_input_th:6.0f} MW, p_in_elec={_p_input_elec:6.0f} MW"
          f" → LCOE={_r_q.costs.lcoe:.1f} $/MWh, p_net={_r_q.power_table.p_net:.0f} MW{_marker}")
