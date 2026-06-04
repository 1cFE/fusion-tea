"""HTS Tokamak - Full HTS (Energy Singularity) — 1costingfe model setup (iter-5).

Modeling approach:
    Energy Singularity's HH380 commercial demo has no published design parameters.
    This script constructs a proxy model using CFS ARC/SPARC as the closest published
    analogue for a compact, high-field, D-shaped HTS tokamak (Sorbom et al. 2015 ARC;
    Araiinejad & Shirvan 2025 TEA). All engineering parameters are UNCERTAIN and must
    be replaced when HH380 engineering data becomes available (post-2030).

    This iteration (iter-5) addresses one important assessment finding:

    F-1 (important): Base-case availability standardized to canonical 0.85.
        iter-4 used availability=0.80 for the base case and scale scenarios (C/D).
        A new project-wide policy in scoring_framework.md §"Plant availability" sets
        the canonical value to 0.85 for MCF steady-state, D-T concepts. No Tier-A
        override exists for this concept (no externally-published availability target
        with a stated basis). Base case and Scenarios C/D are updated to 0.85.
        Scenarios A (0.65) and B (0.70) are deliberate downside excursions and are
        PRESERVED unchanged — they bracket technical-bet failure modes around the
        new canonical central case. Cross-concept LCOE comparisons within the MCF
        family are now apples-to-apples on the availability dimension.
        # DEVIATION: Scenarios A (0.65) and B (0.70) intentionally deviate from
        the 0.85 canonical value — they represent CS coil reliability failure and
        AI plasma control underperformance failure modes, not central-case estimates.
        analysis.md §Section 5 (availability row); §Section 2 (Challenge 4, bet structure)

    Prior-iteration findings (carried forward, no change needed):

    iter-4 F-1 (important): structure_t and vessel_t corrected to tokamak-peer-group default.
        iter-3 used STRUCTURE_T = 0.15 m and VESSEL_T = 0.15 m with the comment
        "slightly below default reflecting compact geometry." Neither value matched
        steady_state_tokamak.yaml (0.20/0.20) and the compactness rationale was
        inverted — compact HTS tokamaks face *higher* TF out-of-plane loads and
        disruption EM loads, not lower. All peer tokamaks (concepts 01, 21, 29, 33,
        34) use the 0.20/0.20 default. No SPARC, ARC, or CFETR disclosure justifies
        a deviation for the compact-HTS class; SPARC (R=1.85 m) still uses >0.15 m
        primary structure in structural analyses. Both values are updated to 0.20 m
        and labeled DEFAULT, matching the peer group.
        A sensitivity sweep over [0.10, 0.15, 0.20, 0.25] m quantifies the CAS22
        impact of the thickness uncertainty.
        analysis.md §Section 2 Challenge 2; §Section 4 (engineering parameters)

    Prior-iteration findings (carried forward, no change needed):

    iter-3 F-1 (blocking): Full HTS coil cost premium applied to C220103.
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

    iter-3 F-2 (important): Major radius scenario sweep — design-point uncertainty bracketed.
        HH380 design point is unknown. The analysis identifies major radius as the
        third-highest structural LCOE lever and explicitly calls for discrete scenario
        runs — not marginal sensitivity perturbations — because the uncertainty is
        about the unknown design point (is HH380 a ~250 MWe machine at R≈1.5m or an
        ~800 MWe machine at R≈2.5m?). Two new scenarios are added:
          Scenario C (small machine): R=1.5 m, net electric ~250 MWe
          Scenario D (large machine): R=2.5 m, net electric ~800 MWe
        Reported in a unified 5-scenario LCOE table alongside Scenarios A and B.
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

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ───────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# ── Full HTS coil cost premium (F-1) ─────────────────────────────────
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

# ── Plant configuration constants ─────────────────────────────────────
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

# ── Geometry at base scale (R=2.0 m) ─────────────────────────────────
# Aspect ratio A = R0 / plasma_t = 4.0 maintained across all scale scenarios.
# analysis.md §Section 7: "D-shaped (conventional aspect ratio, ~A ≈ 3–4 estimated)."

R0_BASE = 2.0
# UNCERTAIN: Major radius [m]. HH170 ~70% SPARC volume (SPARC R=1.85 m) →
# HH170 R ≈ 1.6 m. HH380 commercial demo is larger; 2.0 m is midrange estimate.
# Bracketed by Scenarios C (1.5 m) and D (2.5 m) per F-2.
# analysis.md §Section 2, Challenge 1; §Section 5 (major radius: truly-unknown, important).

PLASMA_T_BASE = 0.50       # R0_BASE / 4.0 = 0.50 m — minor radius [m]
PLASMA_T_C = 0.375         # 1.5 / 4.0 = 0.375 m — Scenario C (small)
PLASMA_T_D = 0.625         # 2.5 / 4.0 = 0.625 m — Scenario D (large)

ELON = 1.7
# UNCERTAIN: Elongation κ. Standard D-shaped tokamak value; no ES disclosure.

BLANKET_T = 0.60
# UNCERTAIN: Blanket thickness [m]. No blanket design disclosed for any ES machine.
# analysis.md §Section 2, Challenge 2 (Critical): blanket "entirely undisclosed."
# 0.60 m consistent with compact high-field design.

HT_SHIELD_T = 0.20   # DEFAULT: steady_state_tokamak.yaml default.
STRUCTURE_T = 0.20
# DEFAULT: matches steady_state_tokamak.yaml; no compact-tokamak-specific disclosure
# justifies deviation. Peer group (concepts 01, 21, 29, 33, 34) all use 0.20 m.
# Compact HTS geometry increases TF out-of-plane loads and disruption EM demand —
# the prior iter-3 rationale ("compact geometry → thinner") was inverted.
# No published SPARC, ARC, or CFETR primary-structure disclosure provides a
# concept-specific value; 0.20 m is the conservative default.
# F-1 (iter-4): corrected from 0.15 m. See structure/vessel sensitivity sweep below.
VESSEL_T = 0.20
# DEFAULT: matches steady_state_tokamak.yaml; no HTS-tokamak-specific vacuum vessel
# disclosure found for HH70, HH170, SPARC, or ARC that justifies deviation from
# peer-group default. Vacuum vessel sizing is driven by atmospheric pressure + halo
# current + neutron shielding margin; compactness does not systematically reduce these.
# F-1 (iter-4): corrected from 0.15 m. See structure/vessel sensitivity sweep below.

# ── Power balance ─────────────────────────────────────────────────────
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

# CAS72 scheduled replacement penalty for Scenario A (CS coil reliability failure)
CAS72_COIL_PENALTY = 1.30
# UNCERTAIN: 30% increase on annualized scheduled replacement (CAS72) to represent
# periodic CS coil reconditioning / rewinding events under 25 T cyclic EM loading.
# No published cost for HTS CS coil replacement in tokamak operation; 30% is a
# conservative placeholder (actual cost could be 2–5× if full replacement required).
# analysis.md §Section 2, Challenge 3: "No published fatigue or reliability data
# exists for full-HTS CS coils in tokamak operation."


# ── Helper: base forward kwargs at a given geometry scale ─────────────
def _base_kwargs(r0, net_electric_mw, plasma_t, availability):
    return dict(
        net_electric_mw=net_electric_mw,
        availability=availability,
        lifetime_yr=LIFETIME_YR,
        n_mod=1,
        construction_time_yr=CONSTRUCTION_TIME_YR,
        interest_rate=INTEREST_RATE,
        inflation_rate=INFLATION_RATE,
        noak=NOAK,
        R0=r0,
        elon=ELON,
        plasma_t=plasma_t,
        blanket_t=BLANKET_T,
        ht_shield_t=HT_SHIELD_T,
        structure_t=STRUCTURE_T,
        vessel_t=VESSEL_T,
        p_input=P_INPUT,
        mn=MN,
        # eta_th, eta_p, eta_pin, eta_de removed — power-conversion efficiencies
        # are never spec keys (1costingfe-glossary policy). Library defaults apply.
        f_sub=F_SUB,
        f_dec=F_DEC,
        p_coils=P_COILS,
        p_cool=P_COOL,
        p_pump=P_PUMP,
        p_trit=P_TRIT,
        p_house=P_HOUSE,
        p_cryo=P_CRYO,
    )


# ── Reference pass: compute framework C220103 without premium ─────────
# Used to anchor the hts_full_coil_premium multiplier at each scale.
# F-1: C220103 framework default assumes a "standard" HTS tokamak coil set
# (calibrated to TF-only HTS architecture as in ARC/SPARC). Full HTS requires
# additional tape for PF and CS coils.
ref_base = model.forward(**_base_kwargs(R0_BASE, 500.0, PLASMA_T_BASE, 0.85))
ref_250  = model.forward(**_base_kwargs(1.5, 250.0, PLASMA_T_C, 0.85))
ref_800  = model.forward(**_base_kwargs(2.5, 800.0, PLASMA_T_D, 0.85))

c220103_framework_base = float(ref_base.cas22_detail["C220103"])
c220103_framework_250  = float(ref_250.cas22_detail["C220103"])
c220103_framework_800  = float(ref_800.cas22_detail["C220103"])

# Apply hts_full_coil_premium at each scale
c220103_500 = c220103_framework_base * HTS_FULL_COIL_PREMIUM
c220103_250 = c220103_framework_250  * HTS_FULL_COIL_PREMIUM
c220103_800 = c220103_framework_800  * HTS_FULL_COIL_PREMIUM


def run_scenario(label, r0, net_electric_mw, plasma_t, availability,
                 cost_overrides, extra_note=""):
    """Run one costing scenario with the given overrides."""
    kwargs = _base_kwargs(r0, net_electric_mw, plasma_t, availability)
    kwargs["cost_overrides"] = cost_overrides
    result = model.forward(**kwargs)
    return result, label, r0, net_electric_mw, availability, extra_note


# ── Five scenario branches ────────────────────────────────────────────
#
# Base case  — R=2.0m, 500 MWe, 85% avail (canonical per scoring_framework.md)
#   CS coils reliable, AI plasma control nominal, full HTS premium applied.
#
# Scenario A — CS Coil Reliability Failure (analysis.md §Section 2, bet #1)
#   Full HTS CS coils at 25 T under cyclic EM loading fail to achieve target
#   availability. CAS72 increased ×1.30 for CS coil reconditioning events.
#   → availability = 65%; # DEVIATION: deliberate downside excursion from canonical 0.85.
#      LCOE impact vs. canonical base: +28.5% from availability drop alone (model output).
#
# Scenario B — AI Plasma Control Underperforms (analysis.md §Section 2, bet #2)
#   AI control does not suppress disruptions at burning-plasma conditions;
#   operation is disruption-limited rather than steady-state.
#   → availability = 70%; # DEVIATION: deliberate downside excursion from canonical 0.85.
#      LCOE impact vs. canonical base: +20.1% (model output).
#
# Scenario C — Small Machine (F-2: R≈1.5m, ~250 MWe)  [NEW in iter-3]
#   Lower bound on HH380 design point: compact machine near HH170 scale.
#   R=1.5m, net electric ~250 MWe, A=4.0, 85% avail (canonical), full HTS premium applied.
#   → Shows how LCOE evolves if HH380 is a smaller, cheaper plant.
#
# Scenario D — Large Machine (F-2: R≈2.5m, ~800 MWe)  [NEW in iter-3]
#   Upper bound on HH380 design point: ARC-class machine, larger than SPARC.
#   R=2.5m, net electric ~800 MWe, A=4.0, 85% avail (canonical), full HTS premium applied.
#   → Shows benefit of scale economies if HH380 is a larger plant.

# Base case
r_base, *_ = run_scenario(
    label="Base Case",
    r0=R0_BASE, net_electric_mw=500.0, plasma_t=PLASMA_T_BASE,
    availability=0.85,  # canonical per scoring_framework.md §Plant availability (MCF steady-state, D-T)
    cost_overrides={"C220103": c220103_500},
    extra_note="R=2.0m, 500 MWe, 85% avail (canonical) — CS coils reliable, AI control nominal",
)

# Scenario A: CS coil reliability failure — apply CAS72 penalty on base CAS72
# CAS72 from base case (with C220103 premium already in place)
cas72_base_val = float(r_base.costs.cas72) if hasattr(r_base.costs, "cas72") else 0.0
r_a, *_ = run_scenario(
    label="Scenario A — CS Coil Reliability Failure",
    r0=R0_BASE, net_electric_mw=500.0, plasma_t=PLASMA_T_BASE,
    availability=0.65,  # DEVIATION: deliberate downside excursion from canonical 0.85
    cost_overrides={
        "C220103": c220103_500,
        **({"CAS72": cas72_base_val * CAS72_COIL_PENALTY} if cas72_base_val else {}),
    },
    extra_note=(
        "R=2.0m, 500 MWe, 65% avail + CAS72 ×1.30 for CS coil reconditioning. "
        "UNCERTAIN: coil replacement cost is a placeholder — no published source."
    ),
)

# Scenario B: AI plasma control underperforms
r_b, *_ = run_scenario(
    label="Scenario B — AI Plasma Control Underperforms",
    r0=R0_BASE, net_electric_mw=500.0, plasma_t=PLASMA_T_BASE,
    availability=0.70,  # DEVIATION: deliberate downside excursion from canonical 0.85
    cost_overrides={"C220103": c220103_500},
    extra_note="R=2.0m, 500 MWe, 70% avail — disruption-limited at burning-plasma conditions",
)

# Scenario C: Small machine (F-2)
r_c, *_ = run_scenario(
    label="Scenario C — Small Machine",
    r0=1.5, net_electric_mw=250.0, plasma_t=PLASMA_T_C,
    availability=0.85,  # canonical per scoring_framework.md §Plant availability (MCF steady-state, D-T)
    cost_overrides={"C220103": c220103_250},
    extra_note=(
        "R=1.5m, ~250 MWe, 85% avail (canonical) — lower bound on HH380 design point. "
        "A=4.0 maintained. Capital scaled from R=2.0m base via geometry inputs. "
        "UNCERTAIN: all parameters scaled from base; HH380 design unknown."
    ),
)

# Scenario D: Large machine (F-2)
r_d, *_ = run_scenario(
    label="Scenario D — Large Machine",
    r0=2.5, net_electric_mw=800.0, plasma_t=PLASMA_T_D,
    availability=0.85,  # canonical per scoring_framework.md §Plant availability (MCF steady-state, D-T)
    cost_overrides={"C220103": c220103_800},
    extra_note=(
        "R=2.5m, ~800 MWe, 85% avail (canonical) — upper bound on HH380 design point. "
        "A=4.0 maintained. Capital scaled from R=2.0m base via geometry inputs. "
        "UNCERTAIN: all parameters scaled from base; HH380 design unknown."
    ),
)

scenarios = [
    (r_base, "Base Case",                              R0_BASE, 500.0, 0.85),
    (r_a,    "Scenario A — CS Coil Reliability Fail", R0_BASE, 500.0, 0.65),
    (r_b,    "Scenario B — AI Control Underperforms", R0_BASE, 500.0, 0.70),
    (r_c,    "Scenario C — Small Machine",            1.5,     250.0, 0.85),
    (r_d,    "Scenario D — Large Machine",            2.5,     800.0, 0.85),
]


# ── Print results ─────────────────────────────────────────────────────
print("=" * 78)
print("HTS Tokamak - Full HTS (Energy Singularity)")
print("Proxy model: CFS ARC/SPARC analogue | All parameters UNCERTAIN")
print(f"Base: R={R0_BASE}m, 500 MWe, 85% avail (canonical) | Lifetime: {LIFETIME_YR} yr | NOAK")
print(f"C220103 hts_full_coil_premium: ×{HTS_FULL_COIL_PREMIUM:.2f} "
      f"(framework base: ${c220103_framework_base:.0f}M → "
      f"with premium: ${c220103_500:.0f}M)")
print("=" * 78)
print()

# Per-scenario detail
for result, label, r0, p_net, avail in scenarios:
    c = result.costs
    pt = result.power_table
    print(f"── {label} ──")
    print(f"   R0={r0}m  |  Net electric: {p_net:.0f} MWe  |  Availability: {avail:.0%}")
    print(f"   LCOE:          {float(c.lcoe):>8.1f} $/MWh")
    print(f"   Overnight:     {float(c.overnight_cost):>8.0f} $/kW")
    print(f"   Fusion power:  {float(pt.p_fus):>8.0f} MW")
    print(f"   Net electric:  {float(pt.p_net):>8.0f} MW")
    print(f"   Q_eng:         {float(pt.q_eng):>8.2f}")
    print()

# Unified 5-scenario LCOE comparison table
print("── Unified LCOE Scenario Table (all five scenarios) ──")
print(f"  {'Scenario':<45} {'R0':>4} {'MWe':>5} {'Avail':>6}  {'LCOE':>10}  {'vs. Base':>9}")
print("  " + "-" * 82)
base_lcoe = float(r_base.costs.lcoe)
for result, label, r0, p_net, avail in scenarios:
    lcoe_val = float(result.costs.lcoe)
    delta_pct = (lcoe_val - base_lcoe) / base_lcoe * 100.0
    delta_str = f"+{delta_pct:.1f}%" if delta_pct > 0 else f"{delta_pct:.1f}%"
    print(f"  {label:<45} {r0:>4.1f} {p_net:>5.0f} {avail:>6.0%}  {lcoe_val:>10.1f}  {delta_str:>9}")
print()
print("  Note — Scenarios A/B bracket technical-bet failure modes at fixed design point.")
print("  Scenarios C/D bracket design-point uncertainty (HH380 scale unknown).")
print()

# CAS breakdown — base case
print("── CAS Cost Breakdown — Base Case ──")
c = r_base.costs
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

# CAS22 sub-account detail — base case
print("── CAS22 Sub-Account Detail — Base Case ──")
cas22_detail = r_base.cas22_detail
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
    if key in cas22_detail:
        val = cas22_detail[key]
        print(f"  {key:<12} {label:<34} {float(val):>10.1f}")
print()
print(f"  * C220103 overridden: framework ${c220103_framework_base:.0f}M "
      f"× ×{HTS_FULL_COIL_PREMIUM:.2f} premium = ${c220103_500:.0f}M")
print(f"    Premium represents incremental REBCO tape for PF+CS coils beyond TF-only HTS.")
print(f"    UNCERTAIN: ×1.1–×1.3 placeholder range; no published CS+PF tape volume estimate.")
print()

# hts_full_coil_premium sensitivity sweep (F-1)
print("── hts_full_coil_premium Sensitivity (F-1) ──")
print("  Effect of full HTS coil scope premium on base-case LCOE")
print(f"  Base: R={R0_BASE}m, 500 MWe, 85% avail (canonical)")
print(f"  Framework C220103 (TF-only baseline): ${c220103_framework_base:.0f}M")
print()
print(f"  {'Premium':<10} {'C220103 (M$)':>14} {'LCOE ($/MWh)':>14} {'Delta vs ×1.0':>14}")
print("  " + "-" * 55)

lcoe_no_premium = None
for prem in [1.0, 1.1, 1.2, 1.3]:
    override_val = c220103_framework_base * prem
    r_prem = model.forward(
        **_base_kwargs(R0_BASE, 500.0, PLASMA_T_BASE, 0.85),
        cost_overrides={"C220103": override_val},
    )
    lcoe_prem = float(r_prem.costs.lcoe)
    if prem == 1.0:
        lcoe_no_premium = lcoe_prem
    delta = (lcoe_prem - lcoe_no_premium) / lcoe_no_premium * 100.0 if lcoe_no_premium else 0.0
    marker = " ← base case" if prem == HTS_FULL_COIL_PREMIUM else ""
    delta_str = f"+{delta:.2f}%" if delta > 0 else f"{delta:.2f}%"
    print(f"  ×{prem:<8.1f} {override_val:>14.0f} {lcoe_prem:>14.1f} {delta_str:>14}{marker}")
print()
print("  Interpretation: each 10% increase in full-HTS coil scope cost translates")
print("  directly to a ~proportional increase in C220103, which propagates into CAS22,")
print("  total capital, and LCOE. Magnitude depends on C220103's fraction of total capital.")
print()

# Structure / vessel thickness sensitivity sweep (F-1, iter-4)
print("── Structure / Vessel Thickness Sensitivity (F-1, iter-4) ──")
print("  Effect of primary structure thickness and vacuum vessel thickness on base-case LCOE.")
print(f"  Base: R={R0_BASE}m, 500 MWe, 85% avail (canonical) | C220103 override held fixed at ${c220103_500:.0f}M")
print(f"  Peer-group default (all tokamak concepts 01/21/29/33/34): 0.20 m / 0.20 m")
print()
print(f"  {'struct_t':>8} {'vessel_t':>8} {'LCOE ($/MWh)':>14} {'Δ vs 0.20/0.20':>16}")
print("  " + "-" * 52)
lcoe_ref_struct = None
for t in [0.10, 0.15, 0.20, 0.25]:
    kw = _base_kwargs(R0_BASE, 500.0, PLASMA_T_BASE, 0.85)
    kw["structure_t"] = t
    kw["vessel_t"] = t
    r_sv = model.forward(**kw, cost_overrides={"C220103": c220103_500})
    lcoe_sv = float(r_sv.costs.lcoe)
    if t == 0.20:
        lcoe_ref_struct = lcoe_sv
    delta_sv = (lcoe_sv - lcoe_ref_struct) / lcoe_ref_struct * 100.0 if lcoe_ref_struct else 0.0
    marker = " ← default / this model" if t == STRUCTURE_T else ""
    delta_str = f"+{delta_sv:.2f}%" if delta_sv > 0 else f"{delta_sv:.2f}%"
    print(f"  {t:>8.2f} {t:>8.2f} {lcoe_sv:>14.1f} {delta_str:>16}{marker}")
print()
print("  Note: both structure_t and vessel_t are swept together at equal values.")
print("  Cost drivers: structure volume at ~$0.15M/m³ (C220105),")
print("  vessel volume at ~$0.72M/m³ (C220106) per costing_constants.yaml.")
print()

# Key Assumptions
print("── Key Assumptions ──")
print(f"  Net electric (base):   500 MWe  [UNCERTAIN — no HH380 design]")
print(f"  Major radius (base):   {R0_BASE} m    [UNCERTAIN — CFS ARC/SPARC analogue]")
print(f"  Minor radius a (base): {PLASMA_T_BASE} m   [UNCERTAIN — A = {R0_BASE/PLASMA_T_BASE:.1f}]")
print(f"  Elongation κ:          {ELON}       [UNCERTAIN — standard D-shaped]")
print(f"  Blanket thickness:     {BLANKET_T} m  [UNCERTAIN — no blanket design disclosed]")
print(f"  Structure thickness:   {STRUCTURE_T} m  [DEFAULT — steady_state_tokamak.yaml; matches peer group 01/21/29/33/34]")
print(f"  Vessel thickness:      {VESSEL_T} m  [DEFAULT — steady_state_tokamak.yaml; matches peer group 01/21/29/33/34]")
print(f"  Thermal efficiency:    {ETA_TH:.0%}    [UNCERTAIN — cycle type unknown; steam Rankine]")
print(f"  ICRH wall-plug η:      {ETA_PIN:.0%}   [UNCERTAIN — 60–70% range; analysis.md §Ch.5]")
print(f"  Cryo power:            {P_CRYO} MW   [UNCERTAIN — full HTS 20 K cryoplant estimate]")
print(f"  Construction time:     {CONSTRUCTION_TIME_YR} yr  [UNCERTAIN — optimistic; <2 yr for HH70]")
print(f"  Interest rate:         {INTEREST_RATE:.0%}     [DEFAULT — no ES financing data]")
print(f"  hts_full_coil_premium: ×{HTS_FULL_COIL_PREMIUM:.2f}    [UNCERTAIN — placeholder ×1.1–×1.3]")
print()
print("  Data rating: LIMITED — Energy Singularity discloses NO commercial design")
print("  parameters for HH380. All engineering values are analogued from CFS ARC/")
print("  SPARC (Sorbom 2015) or steady_state_tokamak.yaml defaults. LCOE carries")
print("  ±50% or greater uncertainty from parameter uncertainty alone.")
print()
print("  Blocking gaps (analysis.md §Section 5):")
print("    - Net electrical output / fusion power / Q for commercial machine (HH380)")
print("    - Blanket design, TBR, and tritium fuel cycle (entirely undisclosed)")
print("    - Power conversion cycle type and thermal efficiency")
print("    - Capital cost estimate or plant cost study")
print("    - Major radius / design point of HH380 (→ Scenarios C/D bracket this)")
print()

# Sensitivity analysis — base case (with C220103 override as constant)
print("── Sensitivity Analysis — Base Case (elasticity = %ΔLCOE / %Δparam) ──")
print("  C220103 overridden → zero gradient; sensitivity is over remaining params.")
print()
sens = model.sensitivity(r_base.params, cost_overrides={"C220103": c220103_500})

print("  Engineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"    {k:<28} {v:+.4f}")

print("\n  Financial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"    {k:<28} {v:+.4f}")

print()
print("── End of model output ──")
