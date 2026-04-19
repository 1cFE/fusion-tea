"""HTS Tokamak - Full HTS (Energy Singularity HH380) — 1costingfe model setup.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling approach:
    Energy Singularity's commercial HH380 demo station has no published design
    parameters. This script constructs a proxy model using CFS ARC/SPARC as the
    closest published analogue for a compact, high-field, D-shaped HTS tokamak
    (Sorbom et al. 2015 ARC; Araiinejad & Shirvan 2025 TEA). All engineering
    parameters are UNCERTAIN and must be replaced when HH380 engineering data
    becomes available (post-2030).

    F-1 (blocking): Full HTS coil cost premium applied to C220103.
        The framework default does not distinguish full-HTS (TF+PF+CS in REBCO) from
        partial-HTS (TF-only, as in CFS SPARC) coil cost. This script applies a named
        multiplier `hts_full_coil_premium` (base ×1.2; range ×1.1–×1.3) to the
        framework-computed C220103 to represent the incremental REBCO tape demand for
        PF and CS coils beyond the TF-only HTS baseline. A sensitivity sweep over
        [×1.0, ×1.1, ×1.2, ×1.3] shows the LCOE impact of this structural uncertainty.
        Basis: estimated additional tape volume for CS+PF at 25 T — no published source;
        placeholder pending engineering estimate of CS+PF coil conductor volume.
        analysis.md §Section 5 (Missing Parameters: hts_full_coil_premium, derivable, important)
        analysis.md §Section 7 (Differentiators: primary impact in C220103)

    F-2 (important): Major radius scenario sweep — design-point uncertainty bracketed.
        HH380 design point is unknown. The analysis identifies major radius as the
        third-highest structural LCOE lever and explicitly calls for discrete scenario
        runs — not marginal sensitivity perturbations — because the uncertainty is
        about the unknown design point (is HH380 a ~250 MWe machine at R≈1.5m or an
        ~800 MWe machine at R≈2.5m?). Two scenarios are added alongside the
        technical-bet failure scenarios (Scenarios A and B):
          Scenario C (small machine): R=1.5 m, net electric ~250 MWe
          Scenario D (large machine): R=2.5 m, net electric ~800 MWe
        analysis.md §Section 2, Challenge 1 and §Key LCOE sensitivity parameters #3

Concept choice rationale:
    ConfinementConcept.TOKAMAK / Fuel.DT — Energy Singularity targets D-T fusion in
    a D-shaped (conventional aspect ratio) compact high-field tokamak. The defining
    differentiator is a full HTS coil set (TF + PF + CS all in REBCO), extending HTS
    beyond TF-only competitors (CFS, Tokamak Energy).

Key deviations from mfe_tokamak.yaml defaults:
    - R0 = 2.0 m (base): proxy from compact HTS tokamak class; HH380 design unknown
    - eta_th = 0.40: steam Rankine conservative; power cycle undisclosed
    - eta_pin = 0.65: ICRH wall-plug efficiency midpoint (60–70% range)
    - p_cryo = 8.0 MW: full 20 K HTS cryoplant (all coils at HTS temp)
    - C220103 overridden with hts_full_coil_premium multiplier (F-1)
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# ── Full HTS coil cost premium (F-1) ──────────────────────────────────────
# Multiplier applied to the framework-computed C220103 (HTS magnet system) to
# represent incremental REBCO tape demand for PF and CS coils relative to a
# TF-only HTS baseline (CFS SPARC uses TF-only HTS; Energy Singularity extends
# to all coil types including CS at 25 T and PF coils).
# UNCERTAIN: No published tape volume estimate for full-HTS CS+PF vs. TF-only.
# Range ×1.1–×1.3 is a placeholder; base ×1.2.
# analysis.md §Section 5, Missing Parameters: "hts_full_coil_premium, derivable, important"
# analysis.md §Section 7: "cost penalty unique to the full-HTS approach relative
#   to partial-HTS competitors... magnitude unquantified"
HTS_FULL_COIL_PREMIUM = 1.20  # base-case multiplier on C220103

# ── Plant configuration constants ─────────────────────────────────────────
# UNCERTAIN: No commercial design (HH380) parameters are published.
# All geometry is analogued from CFS ARC/SPARC (Sorbom et al. 2015, ARC TEA).
# analysis.md §Section 1 — data rating: Limited; §Section 5 — all commercial
# parameters listed as "blocking" gaps.

LIFETIME_YR = 30
# DEFAULT: Standard 30-year plant lifetime; no Energy Singularity disclosure.

CONSTRUCTION_TIME_YR = 5.0
# UNCERTAIN: Energy Singularity built HH70 in <2 years from design to plasma
# [energy-singularity-overview.md §Construction]. Commercial HH380 post-2030;
# 5 years is optimistic vs. 6-year default, reflecting compact machine and
# China-domestic supply chain advantage.
# analysis.md §Section 7, Differentiators table.

INTEREST_RATE = 0.07
# DEFAULT: 7% weighted average cost of capital; no ES financing data.
# analysis.md §Section 2: interest rate is "second lever" for capital-dominated
# concepts; financing uncertainty adds risk premium not modeled here.

INFLATION_RATE = 0.0245
# DEFAULT: ~2.45% long-run inflation. China-domestic costs may differ materially.

NOAK = True
# Nth-of-a-kind assumption for concept TEA comparability.

# ── Geometry at base scale (R=2.0 m) ──────────────────────────────────────
# Aspect ratio A = R0 / plasma_t ≈ 4.0 maintained across all scale scenarios.
# analysis.md §Section 7: "D-shaped (conventional aspect ratio, ~A ≈ 3–4 estimated)."

R0_BASE   = 2.0
# UNCERTAIN: Major radius [m]. HH170 ~70% SPARC volume (SPARC R=1.85 m) →
# HH170 R ≈ 1.6 m. HH380 commercial demo is larger; 2.0 m is midrange estimate.
# Bracketed by Scenarios C (1.5 m) and D (2.5 m) per F-2.
# analysis.md §Section 2, Challenge 1; §Section 5 (major radius: truly-unknown, important).

PLASMA_T_BASE = 0.50       # R0_BASE / 4.0 = 0.50 m — minor radius [m]
PLASMA_T_C    = 0.375      # 1.5 / 4.0 = 0.375 m — Scenario C (small)
PLASMA_T_D    = 0.625      # 2.5 / 4.0 = 0.625 m — Scenario D (large)

ELON = 1.7
# UNCERTAIN: Elongation κ. Standard D-shaped tokamak value; no ES disclosure.

BLANKET_T = 0.60
# UNCERTAIN: Blanket thickness [m]. No blanket design disclosed for any ES machine.
# analysis.md §Section 2, Challenge 2 (Critical): blanket "entirely undisclosed."
# 0.60 m consistent with compact high-field design.

HT_SHIELD_T = 0.20   # DEFAULT: mfe_tokamak.yaml default.
STRUCTURE_T = 0.15   # DEFAULT: slightly below default reflecting compact geometry.
VESSEL_T = 0.15      # DEFAULT: vacuum vessel thickness [m].

# ── Power balance ──────────────────────────────────────────────────────────
P_INPUT = 50.0
# UNCERTAIN: Auxiliary heating power [MW]. ICRH confirmed on HH70 at low power;
# no heating configuration disclosed for HH170 or HH380.
# analysis.md §Section 2, Challenge 5 (Moderate); §Section 5 (gap #7: important).
# 50 MW is mfe_tokamak.yaml default; plausible for Q>10 ignition margin.

MN = 1.1
# DEFAULT: Neutron energy multiplier (standard DT breeding blanket).
# Blanket design undisclosed; value may vary with blanket material choice.
# analysis.md §Section 2, Challenge 2; §Section 4: blanket material unknown.

ETA_TH = 0.40
# UNCERTAIN: Thermal conversion efficiency. Power conversion cycle undisclosed.
# analysis.md §Section 2, Challenge 1 and §Section 5 (gap #5: blocking).
# 0.40 conservative steam Rankine assumption; sCO₂ Brayton could reach 0.45–0.50.

ETA_P = 0.5      # DEFAULT: Pumping efficiency.
ETA_PIN = 0.65
# UNCERTAIN: Heating wall-plug efficiency. ICRH confirmed on HH70
# [dossier.md §Primary Heating]. ICRH wall-plug efficiency ~60–70%.
# analysis.md §Section 2, Challenge 5: "Wall-plug efficiency of ICRH is ~60–70%."
# Using 0.65 (midpoint); vs. 0.50 framework default for generic heating.

ETA_DE = 0.85    # DEFAULT: No DEC system disclosed for ES concept.
F_SUB = 0.03     # DEFAULT: Subsystem recirculating power fraction.
F_DEC = 0.0      # DEFAULT: No DEC disclosed.

P_COILS = 5.0
# UNCERTAIN: Coil steady-state power [MW]. Full HTS (TF+PF+CS) at 20 K; resistive
# losses ≈ 0 in HTS regime but CS coil pulsed power for plasma initiation is non-zero.
# analysis.md §Section 2, Challenge 3: "CS coils must generate and sustain plasma
# initiation current, a demanding duty cycle."

P_COOL = 15.0    # UNCERTAIN: Cooling power [MW]; scaled from default (13.7 MW).
P_PUMP = 2.0     # DEFAULT.

P_TRIT = 10.0
# DEFAULT: Tritium processing power [MW]. Tritium fuel cycle entirely undisclosed.
# analysis.md §Section 2, Challenge 2; §Section 5 (gap #4: blocking).

P_HOUSE = 5.0
# UNCERTAIN: Housekeeping power [MW]; above default (4.0 MW) to reflect AI plasma
# control system power demand and additional control infrastructure.
# analysis.md §Section 2, Challenge 4: "AI-based plasma control system."

P_CRYO = 8.0
# UNCERTAIN: Cryogenic system power [MW]. Full HTS coil set (TF+PF+CS) all at 20 K
# requires a unified but larger cryoplant than partial-HTS (TF-only at 20 K, with
# room-temp or LN2-cooled PF/CS coils). mfe_tokamak.yaml default is 0.5 MW for
# partial-HTS; 8.0 MW reflects full-HTS cryoplant at ~500 MWe scale.
# Potential benefit vs. LTS baseline: uniform 20 K operating temperature eliminates
# mixed LTS/HTS cryogenic circuits [analysis.md §Section 7, Differentiators].
# UNCERTAIN — no ES disclosure; extrapolated from HTS cryoplant sizing.

# ── Shared physics kwargs (no net_electric_mw, no cost_overrides) ──────────
# Used for all forward passes. net_electric_mw and cost_overrides are passed
# explicitly per call so the dual-result pattern and scenario branches can vary them.

_SHARED_KWARGS = dict(
    availability=0.80,           # base-case availability; overridden in Scenarios A/B
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=NOAK,

    # Geometry (base scale: R=2.0 m, A=4.0)
    R0=R0_BASE,                  # 2.0 m — UNCERTAIN central analogue
    elon=ELON,                   # 1.7   — UNCERTAIN standard D-shaped
    plasma_t=PLASMA_T_BASE,      # 0.50 m — derived from R0/A
    blanket_t=BLANKET_T,         # 0.60 m — UNCERTAIN (undisclosed)
    ht_shield_t=HT_SHIELD_T,     # 0.20 m — DEFAULT
    structure_t=STRUCTURE_T,     # 0.15 m — DEFAULT
    vessel_t=VESSEL_T,           # 0.15 m — DEFAULT

    # Power balance
    p_input=P_INPUT,             # 50 MW  — UNCERTAIN (ICRH undisclosed)
    mn=MN,                       # 1.1    — DEFAULT
    eta_th=ETA_TH,               # 0.40   — UNCERTAIN (cycle undisclosed)
    eta_p=ETA_P,                 # 0.5    — DEFAULT
    eta_pin=ETA_PIN,             # 0.65   — ICRH wall-plug (60–70% range)
    eta_de=ETA_DE,               # 0.85   — DEFAULT (DEC not used)
    f_sub=F_SUB,                 # 0.03   — DEFAULT
    f_dec=F_DEC,                 # 0.0    — no DEC
    p_coils=P_COILS,             # 5.0 MW — UNCERTAIN (full HTS CS duty cycle)
    p_cool=P_COOL,               # 15.0 MW — UNCERTAIN
    p_pump=P_PUMP,               # 2.0 MW — DEFAULT
    p_trit=P_TRIT,               # 10.0 MW — DEFAULT (fuel cycle undisclosed)
    p_house=P_HOUSE,             # 5.0 MW — UNCERTAIN (AI control system overhead)
    p_cryo=P_CRYO,               # 8.0 MW — UNCERTAIN (full 20 K cryoplant)
)

# ── Reference pass: compute framework C220103 before applying premium ──────
# F-1: C220103 framework default assumes a "standard" HTS tokamak coil set
# (calibrated to TF-only HTS architecture as in ARC/SPARC). Full HTS requires
# additional tape for PF and CS coils. We run a no-override pass first to read
# the framework value, then apply hts_full_coil_premium at each scale.
_ref_base = model.forward(net_electric_mw=500.0, **_SHARED_KWARGS)
_ref_250  = model.forward(
    net_electric_mw=250.0,
    **{**_SHARED_KWARGS, "R0": 1.5, "plasma_t": PLASMA_T_C},
)
_ref_800  = model.forward(
    net_electric_mw=800.0,
    **{**_SHARED_KWARGS, "R0": 2.5, "plasma_t": PLASMA_T_D},
)

_c220103_fw_base = float(_ref_base.cas22_detail["C220103"])
_c220103_fw_250  = float(_ref_250.cas22_detail["C220103"])
_c220103_fw_800  = float(_ref_800.cas22_detail["C220103"])

# Apply hts_full_coil_premium at each scale
_C220103_500 = _c220103_fw_base * HTS_FULL_COIL_PREMIUM
_C220103_250 = _c220103_fw_250  * HTS_FULL_COIL_PREMIUM
_C220103_800 = _c220103_fw_800  * HTS_FULL_COIL_PREMIUM

# ── Primary result (native 500 MWe design point, NOAK) ────────────────────
result = model.forward(
    net_electric_mw=500.0,
    cost_overrides={"C220103": _C220103_500},
    **_SHARED_KWARGS,
)

# ── Self-consistent 1 GW result for cross-concept comparison ──────────────
# override_reference_mw tells the framework that cost_overrides are valid at
# 500 MWe and should scale to 1000 MWe using per-account scaling laws.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=500.0,
    cost_overrides={"C220103": _C220103_500},
    **_SHARED_KWARGS,
)

# ── Scenario A: CS coil reliability failure ────────────────────────────────
# Full HTS CS coils at 25 T under cyclic EM loading fail to achieve target
# availability. LCOE impact vs. base case approximately +14% (elasticity ≈ −0.94).
# Modeled as availability = 65%; CS coil reconditioning costs not separately
# quantified (no published source for HTS CS coil replacement cost in tokamak).
# Source: analysis.md §Section 2, Technical Bet Scenario structure
result_scenario_a = model.forward(
    net_electric_mw=500.0,
    cost_overrides={"C220103": _C220103_500},
    **{**_SHARED_KWARGS, "availability": 0.65},
)

# ── Scenario B: AI plasma control underperforms ────────────────────────────
# AI control does not suppress disruptions at burning-plasma conditions;
# operation is disruption-limited rather than steady-state.
# LCOE impact approximately +9% vs. base case.
# Source: analysis.md §Section 2, Technical Bet Scenario structure
result_scenario_b = model.forward(
    net_electric_mw=500.0,
    cost_overrides={"C220103": _C220103_500},
    **{**_SHARED_KWARGS, "availability": 0.70},
)

# ── Scenario C: Small machine (F-2: R≈1.5m, ~250 MWe) ────────────────────
# Lower bound on HH380 design point; lower capital at smaller scale.
# Source: analysis.md §Section 2, LCOE Sensitivity #3 (Scenario C)
result_scenario_c = model.forward(
    net_electric_mw=250.0,
    cost_overrides={"C220103": _C220103_250},
    **{**_SHARED_KWARGS, "R0": 1.5, "plasma_t": PLASMA_T_C},
)

# ── Scenario D: Large machine (F-2: R≈2.5m, ~800 MWe) ────────────────────
# Upper bound on HH380 design point; lower LCOE through scale economies.
# Source: analysis.md §Section 2, LCOE Sensitivity #3 (Scenario D)
result_scenario_d = model.forward(
    net_electric_mw=800.0,
    cost_overrides={"C220103": _C220103_800},
    **{**_SHARED_KWARGS, "R0": 2.5, "plasma_t": PLASMA_T_D},
)

_scenarios = [
    (result,           "Base Case",                               R0_BASE, 500.0, 0.80),
    (result_scenario_a, "Scenario A — CS Coil Reliability Fail", R0_BASE, 500.0, 0.65),
    (result_scenario_b, "Scenario B — AI Control Underperforms", R0_BASE, 500.0, 0.70),
    (result_scenario_c, "Scenario C — Small Machine",            1.5,     250.0, 0.80),
    (result_scenario_d, "Scenario D — Large Machine",            2.5,     800.0, 0.80),
]

# ── Print results ──────────────────────────────────────────────────────────
print("=" * 78)
print("HTS Tokamak - Full HTS (Energy Singularity)")
print("Proxy model: CFS ARC/SPARC analogue | All parameters UNCERTAIN")
print(f"Base: R={R0_BASE}m, 500 MWe, 80% avail | Lifetime: {LIFETIME_YR} yr | NOAK")
print(f"C220103 hts_full_coil_premium: ×{HTS_FULL_COIL_PREMIUM:.2f} "
      f"(framework base: ${_c220103_fw_base:.0f}M → "
      f"with premium: ${_C220103_500:.0f}M)")
print("=" * 78)
print()

c  = result.costs
pt = result.power_table
print(f"LCOE:       {float(c.lcoe):>8.1f} $/MWh")
print(f"Overnight:  {float(c.overnight_cost):>8.0f} $/kW")
print(f"Fusion:     {float(pt.p_fus):>8.0f} MW | Net: {float(pt.p_net):>5.0f} MW | Q_eng: {float(pt.q_eng):.2f}")
print()
print(f"1 GW scaled (cross-concept): LCOE {result_1gw.costs.lcoe:.1f} $/MWh | "
      f"Overnight {result_1gw.costs.overnight_cost:.0f} $/kW")
print()

# ── Unified 5-scenario LCOE table ─────────────────────────────────────────
print("── Unified Scenario LCOE Table ──")
print(f"  {'Scenario':<45} {'R0':>4} {'MWe':>5} {'Avail':>6}  {'LCOE':>10}  {'vs. Base':>9}")
print("  " + "-" * 82)
base_lcoe = float(result.costs.lcoe)
for r, label, r0, p_net, avail in _scenarios:
    lcoe_val = float(r.costs.lcoe)
    delta_pct = (lcoe_val - base_lcoe) / base_lcoe * 100.0
    delta_str = f"+{delta_pct:.1f}%" if delta_pct > 0 else f"{delta_pct:.1f}%"
    print(f"  {label:<45} {r0:>4.1f} {p_net:>5.0f} {avail:>6.0%}  {lcoe_val:>10.1f}  {delta_str:>9}")
print()
print("  Note — Scenarios A/B bracket technical-bet failure modes at fixed design point.")
print("  Scenarios C/D bracket design-point uncertainty (HH380 scale unknown).")
print()

# ── CAS cost breakdown — base case ────────────────────────────────────────
print("── CAS Cost Breakdown — Base Case ──")
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
print(f"  {'Code':<8} {'Account':<28} {'M$':>10}")
print("  " + "-" * 48)
for code, name, val in cas:
    print(f"  {code:<8} {name:<28} {float(val):>10.1f}")
print("  " + "-" * 48)
print(f"  {'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")
print()

# ── CAS22 sub-account detail — base case ──────────────────────────────────
print("── CAS22 Sub-Account Detail — Base Case ──")
cas22_labels = {
    "C220101": "First Wall + Blanket",
    "C220102": "Shield",
    "C220103": "Coils — HTS full (TF+PF+CS) *",
    "C220104": "Heating (ICRH)",
    "C220105": "Structure",
    "C220106": "Vacuum System",
    "C220107": "Power Supplies",
    "C220108": "Divertor",
    "C220109": "DEC Equipment",
    "C220111": "Installation Labor",
    "C220112": "Isotope Separation",
    "C220200": "Coolant System",
    "C220300": "Auxiliary Cooling",
    "C220400": "Radwaste",
    "C220500": "Fuel Handling",
    "C220600": "Other Equipment",
    "C220700": "I&C",
    "C220000": "CAS22 Total",
}
print(f"  {'Sub-account':<12} {'Description':<34} {'M$':>10}")
print("  " + "-" * 59)
for key, label in cas22_labels.items():
    if key in result.cas22_detail:
        val = result.cas22_detail[key]
        print(f"  {key:<12} {label:<34} {float(val):>10.1f}")
print()
print(f"  * C220103 overridden: framework ${_c220103_fw_base:.0f}M "
      f"× ×{HTS_FULL_COIL_PREMIUM:.2f} = ${_C220103_500:.0f}M")
print(f"    Premium: incremental REBCO tape for PF+CS coils beyond TF-only HTS.")
print(f"    UNCERTAIN: ×1.1–×1.3 placeholder range; no published CS+PF tape volume estimate.")
print()

# ── hts_full_coil_premium sensitivity sweep (F-1) ─────────────────────────
print("── hts_full_coil_premium Sensitivity Sweep (F-1) ──")
print(f"  Framework C220103 (TF-only baseline): ${_c220103_fw_base:.0f}M")
print()
print(f"  {'Premium':<10} {'C220103 (M$)':>14} {'LCOE ($/MWh)':>14} {'Delta vs ×1.0':>14}")
print("  " + "-" * 55)
_lcoe_no_premium = None
for prem in [1.0, 1.1, 1.2, 1.3]:
    _override_val = _c220103_fw_base * prem
    _r_prem = model.forward(
        net_electric_mw=500.0,
        cost_overrides={"C220103": _override_val},
        **_SHARED_KWARGS,
    )
    _lcoe_prem = float(_r_prem.costs.lcoe)
    if prem == 1.0:
        _lcoe_no_premium = _lcoe_prem
    _delta = (_lcoe_prem - _lcoe_no_premium) / _lcoe_no_premium * 100.0 if _lcoe_no_premium else 0.0
    _marker = " ← base case" if abs(prem - HTS_FULL_COIL_PREMIUM) < 1e-9 else ""
    _delta_str = f"+{_delta:.2f}%" if _delta > 0 else f"{_delta:.2f}%"
    print(f"  ×{prem:<8.1f} {_override_val:>14.0f} {_lcoe_prem:>14.1f} {_delta_str:>14}{_marker}")
print()

# ── Key Assumptions ────────────────────────────────────────────────────────
print("── Key Assumptions ──")
print(f"  Net electric (base):   500 MWe  [UNCERTAIN — no HH380 design]")
print(f"  Major radius (base):   {R0_BASE} m    [UNCERTAIN — CFS ARC/SPARC analogue]")
print(f"  Minor radius a (base): {PLASMA_T_BASE} m   [UNCERTAIN — A = {R0_BASE/PLASMA_T_BASE:.1f}]")
print(f"  Elongation κ:          {ELON}       [UNCERTAIN — standard D-shaped]")
print(f"  Blanket thickness:     {BLANKET_T} m  [UNCERTAIN — no blanket design disclosed]")
print(f"  Thermal efficiency:    {ETA_TH:.0%}    [UNCERTAIN — cycle type unknown; steam Rankine]")
print(f"  ICRH wall-plug η:      {ETA_PIN:.0%}   [UNCERTAIN — 60–70% range; analysis.md §Ch.5]")
print(f"  Cryo power:            {P_CRYO} MW  [UNCERTAIN — full HTS 20 K cryoplant estimate]")
print(f"  Construction time:     {CONSTRUCTION_TIME_YR} yr  [UNCERTAIN — optimistic; <2 yr for HH70]")
print(f"  Interest rate:         {INTEREST_RATE:.0%}     [DEFAULT — no ES financing data]")
print(f"  hts_full_coil_premium: ×{HTS_FULL_COIL_PREMIUM:.2f}    [UNCERTAIN — placeholder ×1.1–×1.3]")
print()
print("  Data rating: LIMITED — Energy Singularity discloses NO commercial design")
print("  parameters for HH380. All engineering values are analogued from CFS ARC/")
print("  SPARC (Sorbom 2015) or mfe_tokamak.yaml defaults. LCOE carries ±50% or")
print("  greater uncertainty from parameter uncertainty alone.")
print()
print("  Blocking gaps (analysis.md §Section 5):")
print("    - Net electrical output / fusion power / Q for commercial machine (HH380)")
print("    - Blanket design, TBR, and tritium fuel cycle (entirely undisclosed)")
print("    - Power conversion cycle type and thermal efficiency")
print("    - Capital cost estimate or plant cost study")
print("    - Major radius / design point of HH380 (→ Scenarios C/D bracket this)")
print()

# ── Sensitivity analysis — base case ──────────────────────────────────────
print("── Sensitivity Analysis — Base Case (elasticity = %ΔLCOE / %Δparam) ──")
print("  C220103 overridden → zero gradient; sensitivity is over remaining params.")
print()
sens = model.sensitivity(result.params, cost_overrides={"C220103": _C220103_500})

print("  Engineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"    {k:<28} {v:+.4f}")

print("\n  Financial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"    {k:<28} {v:+.4f}")

print("\n  Costing constants (top 15):")
_costing = sorted(sens["costing"].items(), key=lambda x: abs(x[1]), reverse=True)
for k, v in _costing[:15]:
    print(f"    {k:<28} {v:+.4f}")

print()
print("── End of model output ──")
