"""HTS Tokamak - Full HTS (Energy Singularity) — 1costingfe model setup.

Modeling approach:
    Energy Singularity's HH380 commercial demo has no published design parameters.
    This script constructs a proxy model using CFS ARC/SPARC as the closest published
    analogue for a compact, high-field, D-shaped HTS tokamak (Sorbom et al. 2015 ARC;
    Araiinejad & Shirvan 2025 TEA). All engineering parameters are UNCERTAIN and must
    be replaced when HH380 engineering data becomes available (post-2030).

    The model's primary value is bracketing LCOE sensitivity to the two critical
    technical bets: (1) full HTS CS coil reliability at 25 T under cyclic EM loading,
    and (2) AI plasma control effectiveness at burning-plasma conditions. These are
    modeled as explicit scenario branches per assessment finding F-3.

Concept choice rationale:
    ConfinementConcept.TOKAMAK / Fuel.DT — Energy Singularity targets D-T fusion in
    a D-shaped (conventional aspect ratio) compact high-field tokamak. The defining
    differentiator is a full HTS coil set (TF + PF + CS all in REBCO), extending HTS
    to CS coils — a step beyond CFS (TF-only HTS) and Tokamak Energy (TF + PF HTS).
    No framework parameter captures the full-HTS vs. partial-HTS cost difference
    directly; the additional REBCO tape demand for PF/CS coils is noted in comments
    but cannot be quantified without a disclosed coil design.

Key deviations from mfe_tokamak.yaml defaults:
    - R0 = 2.0 m: analogue from CFS ARC (R = 3.3 m) scaled to compact range; HH170
      is ~70% SPARC volume (SPARC R = 1.85 m), so HH380 commercial estimated 2–2.5 m
    - eta_th = 0.40: steam Rankine assumption; power conversion cycle undisclosed
    - eta_pin = 0.65: ICRH wall-plug efficiency (analysis.md §Challenge 5, 60–70%);
      higher than 0.50 NBI default, lower than ECRH optimum
    - p_cryo = 8.0 MW: full HTS system at 20 K for all coils (TF+PF+CS); higher than
      partial-HTS default (0.5 MW) to reflect uniform 20 K cryoplant for all coils
    - Three availability scenarios bracket the two key technical bets (F-3)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import sys

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ───────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# ── Plant configuration constants ─────────────────────────────────────
# UNCERTAIN: No commercial design (HH380) parameters are published.
# All geometry is analogued from CFS ARC/SPARC (Sorbom et al. 2015, ARC TEA).
# analysis.md §Section 1 — data rating: Limited; §Section 5 — all commercial
# parameters listed as "blocking" gaps.

NET_ELECTRIC_MW = 500.0
# UNCERTAIN: No net electrical output disclosed for HH380.
# analysis.md §Section 5, Missing Parameters row 1 (gap type: proprietary, blocking).
# 500 MW chosen as midrange for compact HTS tokamak concept class;
# ARC reference is ~200 MWe (Sorbom 2015), CFETR target is 1 GWe.

LIFETIME_YR = 30
# DEFAULT: Standard 30-year plant lifetime; no Energy Singularity disclosure.
# mfe_tokamak.yaml default; consistent with tokamak fleet assumptions.

CONSTRUCTION_TIME_YR = 5.0
# UNCERTAIN: Energy Singularity built HH70 in <2 years from design to plasma
# [energy-singularity-overview.md §Construction]. Commercial HH380 construction
# is post-2030 and likely longer. 5 years is optimistic vs. 6-year default,
# reflecting the compact machine and China-domestic supply chain advantage.
# analysis.md §Section 7, Differentiators table.

INTEREST_RATE = 0.07
# DEFAULT: 7% weighted average cost of capital; no financing data for Energy
# Singularity. analysis.md §Section 2 identifies interest rate as "second lever"
# for LCOE sensitivity in capital-intensive concepts.

INFLATION_RATE = 0.0245
# DEFAULT: ~2.45% long-run US inflation; analysis uses Western LCOE conventions
# for comparability. China-domestic costs may differ materially.

NOAK = True
# Nth-of-a-kind assumption; HH380 is described as a demo station not a fleet
# product, but NOAK is used for concept TEA comparability.

# ── Geometry (all UNCERTAIN, CFS ARC/SPARC analogue) ─────────────────
R0 = 2.0
# UNCERTAIN: Major radius [m]. HH170 is ~70% SPARC volume (SPARC R = 1.85 m),
# implying HH170 R ≈ 1.64 m. HH380 commercial demo is larger than HH170.
# Bracket: 1.5 m (compact, near HH170 scale) / 2.0 m (base) / 2.5 m (ARC-like).
# analysis.md §Section 2, Challenge 1 and §Section 5, Missing Parameters.

PLASMA_T = 0.5
# UNCERTAIN: Minor radius / plasma thickness [m], giving aspect ratio A = R0/a = 4.0.
# Conventional D-shaped tokamak (A ≈ 3–4). No HH380 geometry disclosed.
# analysis.md §Section 7: "D-shaped (conventional aspect ratio, ~A ≈ 3–4 estimated)."

ELON = 1.7
# UNCERTAIN: Elongation κ. Standard D-shaped tokamak value; no ES disclosure.
# HH70 is D-shaped [dossier.md §Confinement Concept]; HH380 geometry inferred.

BLANKET_T = 0.60
# UNCERTAIN: Blanket thickness [m]. No blanket design disclosed for any ES machine.
# analysis.md §Section 2, Challenge 2 (Critical impact): blanket "entirely
# undisclosed." 0.60 m is consistent with compact high-field design requiring
# thinner blanket than ITER-like machines.

HT_SHIELD_T = 0.20
# DEFAULT: High-temperature shield thickness [m]. mfe_tokamak.yaml default.

STRUCTURE_T = 0.15
# DEFAULT: Primary structure thickness [m]. Slightly below default (0.20) reflecting
# compact machine geometry.

VESSEL_T = 0.15
# DEFAULT: Vacuum vessel thickness [m]. HH70 vacuum vessel built in <2 years
# [energy-singularity-overview.md §Construction]; commercial scale undisclosed.

# ── Power balance (all UNCERTAIN unless noted) ────────────────────────
P_INPUT = 50.0
# UNCERTAIN: Auxiliary heating power [MW]. ICRH confirmed on HH70 at low power;
# no heating configuration disclosed for HH170 or HH380.
# analysis.md §Section 2, Challenge 5 (Moderate impact); §Section 5, Missing
# Parameters: "Heating power (HH170/HH380)" — gap type: proprietary, important.
# 50 MW is the mfe_tokamak.yaml default; plausible for Q > 10 ignition margin.

MN = 1.1
# DEFAULT: Neutron energy multiplier. Standard DT breeding blanket value.
# mfe_tokamak.yaml default. Blanket design undisclosed; value may vary with
# blanket material choice (FLiBe vs. LiPb vs. ceramic pebble).
# analysis.md §Section 2, Challenge 2; §Section 4: blanket material unknown.

ETA_TH = 0.40
# UNCERTAIN: Thermal conversion efficiency. Power conversion cycle undisclosed.
# analysis.md §Section 2, Challenge 1 and §Section 5 (gap #5: blocking).
# 0.40 is conservative steam Rankine assumption. If sCO₂ Brayton, could reach
# 0.45–0.50. Default (mfe_tokamak.yaml) is 0.46.

ETA_P = 0.5
# DEFAULT: Pumping efficiency. mfe_tokamak.yaml default.

ETA_PIN = 0.65
# UNCERTAIN: Heating system wall-plug efficiency. ICRH confirmed on HH70
# [dossier.md §Primary Heating]. ICRH wall-plug efficiency is ~60–70%.
# analysis.md §Section 2, Challenge 5: "Wall-plug efficiency of ICRH is
# ~60–70%." Using 0.65 (midpoint); vs. 0.50 framework default for generic heating.

ETA_DE = 0.85
# DEFAULT: Direct energy conversion efficiency (DEC). mfe_tokamak.yaml default.
# No DEC system disclosed for ES concept.

F_SUB = 0.03
# DEFAULT: Subsystem recirculating power fraction. mfe_tokamak.yaml default.

F_DEC = 0.0
# DEFAULT: DEC fraction. No DEC disclosed for ES concept.
# analysis.md §Section 2, Challenge 4 mentions no energy recovery pathway.

P_COILS = 5.0
# UNCERTAIN: Coil steady-state power [MW]. Full HTS coil set (TF+PF+CS) at 20 K;
# resistive losses ≈ 0 in HTS regime but control/trim coil power non-zero.
# No ES disclosure. mfe_tokamak.yaml default is 2.0 MW; using 5.0 MW reflecting
# additional CS coil pulsed power for plasma initiation current ramp.
# analysis.md §Section 2, Challenge 3: "Full HTS CS coils must generate and
# sustain plasma initiation current, a demanding duty cycle."

P_COOL = 15.0
# UNCERTAIN: Cooling system power [MW]. Scaled from mfe_tokamak.yaml default
# (13.7 MW) to reflect compact machine with different blanket geometry.
# No ES disclosure.

P_PUMP = 2.0
# DEFAULT: Pumping power [MW]. mfe_tokamak.yaml default.

P_TRIT = 10.0
# DEFAULT: Tritium processing power [MW]. mfe_tokamak.yaml default.
# Tritium fuel cycle and blanket entirely undisclosed for ES.
# analysis.md §Section 2, Challenge 2; §Section 5, Missing Parameters (gap #4).

P_HOUSE = 5.0
# UNCERTAIN: Housekeeping power [MW]. Above mfe_tokamak.yaml default (4.0 MW)
# reflecting AI plasma control system power demand and additional control
# infrastructure. No ES disclosure.
# analysis.md §Section 2, Challenge 4: "AI-based plasma control system."

P_CRYO = 8.0
# UNCERTAIN: Cryogenic system power [MW]. Full HTS coil set (TF+PF+CS) all at
# 20 K requires a unified but larger cryoplant than a partial-HTS design with
# mixed-temperature coils. mfe_tokamak.yaml default (0.5 MW) is calibrated to
# partial-HTS; this value reflects full-HTS cryoplant.
# analysis.md §Section 7, Differentiators: "operating all coils at HTS
# temperatures potentially reduces cryogenic complexity by eliminating the need
# to maintain separate LTS coils at lower temperatures" — benefit vs. LTS
# baseline, but still larger than partial-HTS default.
# Source: UNCERTAIN — no ES disclosure; extrapolated from HTS cryoplant sizing.


def run_scenario(label, availability, extra_note="", cost_overrides=None):
    """Run a single costing scenario and return the result."""
    kwargs = dict(
        net_electric_mw=NET_ELECTRIC_MW,
        availability=availability,
        lifetime_yr=LIFETIME_YR,
        n_mod=1,
        construction_time_yr=CONSTRUCTION_TIME_YR,
        interest_rate=INTEREST_RATE,
        inflation_rate=INFLATION_RATE,
        noak=NOAK,
        # Geometry — all UNCERTAIN, CFS ARC/SPARC analogue
        R0=R0,
        elon=ELON,
        plasma_t=PLASMA_T,
        blanket_t=BLANKET_T,
        ht_shield_t=HT_SHIELD_T,
        structure_t=STRUCTURE_T,
        vessel_t=VESSEL_T,
        # Power balance
        p_input=P_INPUT,          # UNCERTAIN: ICRH scale undisclosed
        mn=MN,                    # DEFAULT: standard DT neutron multiplier
        eta_th=ETA_TH,            # UNCERTAIN: cycle type undisclosed
        eta_p=ETA_P,              # DEFAULT
        eta_pin=ETA_PIN,          # UNCERTAIN: ICRH wall-plug efficiency midpoint
        eta_de=ETA_DE,            # DEFAULT
        f_sub=F_SUB,              # DEFAULT
        f_dec=F_DEC,              # DEFAULT: no DEC
        p_coils=P_COILS,          # UNCERTAIN: full HTS CS cycling power
        p_cool=P_COOL,            # UNCERTAIN
        p_pump=P_PUMP,            # DEFAULT
        p_trit=P_TRIT,            # DEFAULT
        p_house=P_HOUSE,          # UNCERTAIN: AI control system overhead
        p_cryo=P_CRYO,            # UNCERTAIN: full HTS cryoplant
    )
    if cost_overrides:
        kwargs["cost_overrides"] = cost_overrides
    result = model.forward(**kwargs)
    return result, label, availability, extra_note


# ── Three scenario branches (F-3: key technical bets as testable propositions) ───
#
# Base case: AI plasma control works, CS coils achieve target reliability
#   → availability = 80%
#
# Scenario A (CS coil reliability failure): Full HTS CS coils at 25 T under
#   cyclic EM loading fail to achieve target availability.
#   → availability = 65% (from analysis.md §Section 2, Technical bet scenario structure)
#   → CAS72 increased by 30% to represent coil reconditioning / rewinding cost;
#     quantitative value is UNCERTAIN — no published HTS CS replacement cost exists.
#     Elasticity ≈ −0.94 → 80%→65% availability gives ~+14% LCOE before coil costs.
#   → Source: analysis.md §Section 2, Challenge 3; §Key LCOE sensitivity parameters.
#
# Scenario B (AI plasma control underperforms): AI system does not suppress
#   disruptions at burning-plasma conditions; operation is disruption-limited.
#   → availability = 70% (from analysis.md §Section 2, Technical bet scenario structure)
#   → No additional cost override; disruption cost modeled through availability alone.
#   → Elasticity ≈ −0.94 → 80%→70% gives ~+9% LCOE.
#   → Source: analysis.md §Section 2, Challenge 4; §Key LCOE sensitivity parameters.

# Scenario A coil replacement cost override:
# CAS72 (annualized scheduled replacement) increased by ~30% to represent
# periodic CS coil rewinding/reconditioning at 25 T cycling failure mode.
# UNCERTAIN: No published cost for HTS CS coil replacement in tokamak operation.
# The 30% increase on CAS72 is a placeholder — actual cost could be 2–5× higher
# if full coil replacement is required.
# analysis.md §Section 2, Challenge 3: "No published fatigue or reliability data
# exists for full-HTS CS coils in tokamak operation."
CAS72_BASE_FRACTION = 1.30  # 30% penalty on scheduled replacement for CS coil events

results = []

# Base case
r_base, lbl_base, avail_base, note_base = run_scenario(
    label="Base Case (CS coils reliable, AI control nominal)",
    availability=0.80,
    extra_note="80% availability — AI plasma control working, CS coils at design life",
)
results.append((r_base, lbl_base, avail_base, note_base))

# Scenario A: CS coil reliability failure
# Override CAS72 to add coil replacement cost; base CAS72 is computed from the
# model, so we capture it from base case and apply the penalty.
cas72_base_val = float(r_base.costs.cas72) if hasattr(r_base.costs, "cas72") else None
cs_cost_overrides = {}
if cas72_base_val is not None:
    cs_cost_overrides["CAS72"] = cas72_base_val * CAS72_BASE_FRACTION

r_cs, lbl_cs, avail_cs, note_cs = run_scenario(
    label="Scenario A — CS Coil Reliability Failure",
    availability=0.65,
    extra_note=(
        "65% availability + CAS72 ×1.30 for CS coil reconditioning events. "
        "Represents full HTS CS coil fatigue failure at 25 T cyclic EM loading. "
        "UNCERTAIN: coil replacement cost factor is a placeholder (no source)."
    ),
    cost_overrides=cs_cost_overrides if cs_cost_overrides else None,
)
results.append((r_cs, lbl_cs, avail_cs, note_cs))

# Scenario B: AI plasma control underperforms
r_ai, lbl_ai, avail_ai, note_ai = run_scenario(
    label="Scenario B — AI Plasma Control Underperforms",
    availability=0.70,
    extra_note=(
        "70% availability — disruption-limited operation at burning-plasma conditions. "
        "Represents AI control system failing to suppress disruptions at D-T scale. "
        "No additional cost override (disruption cost absorbed into availability)."
    ),
)
results.append((r_ai, lbl_ai, avail_ai, note_ai))


# ── Print results ─────────────────────────────────────────────────────
print("=" * 72)
print("HTS Tokamak - Full HTS (Energy Singularity)")
print("Proxy model: CFS ARC/SPARC analogue | All parameters UNCERTAIN")
print(f"Net electric: {NET_ELECTRIC_MW:.0f} MWe | Lifetime: {LIFETIME_YR} yr | NOAK")
print("=" * 72)
print()

for result, label, avail, note in results:
    c = result.costs
    pt = result.power_table
    print(f"── {label} ──")
    print(f"   Availability: {avail:.0%}")
    if note:
        print(f"   Note: {note}")
    print(f"   LCOE:          {float(c.lcoe):>8.1f} $/MWh")
    print(f"   Overnight:     {float(c.overnight_cost):>8.0f} $/kW")
    print(f"   Fusion power:  {float(pt.p_fus):>8.0f} MW")
    print(f"   Net electric:  {float(pt.p_net):>8.0f} MW")
    print(f"   Q_eng:         {float(pt.q_eng):>8.2f}")
    print()

# ── LCOE comparison table (scenario brackets) ─────────────────────────
print("── LCOE Scenario Comparison ──")
print(f"  {'Scenario':<45} {'Avail':>6}  {'LCOE ($/MWh)':>12}  {'vs. Base':>10}")
print("  " + "-" * 77)
base_lcoe = float(results[0][0].costs.lcoe)
for result, label, avail, _ in results:
    lcoe_val = float(result.costs.lcoe)
    delta = (lcoe_val - base_lcoe) / base_lcoe * 100.0
    delta_str = f"+{delta:.1f}%" if delta > 0 else f"{delta:.1f}%"
    print(f"  {label:<45} {avail:>6.0%}  {lcoe_val:>12.1f}  {delta_str:>10}")
print()

# ── CAS breakdown (base case) ─────────────────────────────────────────
print("── CAS Cost Breakdown — Base Case ──")
c = results[0][0].costs
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

# ── CAS22 detail (base case) ──────────────────────────────────────────
print("── CAS22 Sub-Account Detail — Base Case ──")
cas22_detail = results[0][0].cas22_detail
cas22_labels = {
    "C220101": "First Wall + Blanket",
    "C220102": "Shield",
    "C220103": "Coils (HTS magnet system)",
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
print(f"  {'Sub-account':<12} {'Description':<30} {'M$':>10}")
print("  " + "-" * 55)
for key, label in cas22_labels.items():
    if key in cas22_detail:
        val = cas22_detail[key]
        marker = " *" if key == "C220103" else ""  # flag HTS coil account
        print(f"  {key:<12} {label:<30} {float(val):>10.1f}{marker}")
print("  (* C220103 — full HTS coil system, TF+PF+CS; no cost override applied;")
print("     framework default does not distinguish full-HTS vs. partial-HTS cost penalty)")
print()

# ── Key Assumptions ───────────────────────────────────────────────────
print("── Key Assumptions ──")
print(f"  Net electric output:   {NET_ELECTRIC_MW:.0f} MW  [UNCERTAIN — no HH380 design]")
print(f"  Major radius R0:       {R0} m    [UNCERTAIN — CFS ARC/SPARC analogue]")
print(f"  Minor radius a:        {PLASMA_T} m   [UNCERTAIN — A = R0/a = {R0/PLASMA_T:.1f}]")
print(f"  Elongation κ:          {ELON}       [UNCERTAIN — standard D-shaped]")
print(f"  Blanket thickness:     {BLANKET_T} m  [UNCERTAIN — no blanket design disclosed]")
print(f"  Thermal efficiency:    {ETA_TH:.0%}    [UNCERTAIN — cycle type unknown; steam Rankine]")
print(f"  ICRH wall-plug η:      {ETA_PIN:.0%}   [UNCERTAIN — 60–70% range; analysis.md §Ch.5]")
print(f"  Cryo power:            {P_CRYO} MW   [UNCERTAIN — full HTS 20 K cryoplant]")
print(f"  Construction time:     {CONSTRUCTION_TIME_YR} yr  [UNCERTAIN — optimistic; <2 yr for HH70]")
print(f"  Interest rate:         {INTEREST_RATE:.0%}     [DEFAULT — no ES financing data]")
print()
print("  Data rating: LIMITED — Energy Singularity discloses NO commercial design")
print("  parameters for HH380. All engineering values are analogued from CFS ARC/")
print("  SPARC (Sorbom 2015) or mfe_tokamak.yaml defaults. LCOE carries ±50% or")
print("  greater uncertainty from parameter uncertainty alone.")
print()
print("  Blocking gaps (analysis.md §Section 5):")
print("    - Net electrical output / fusion power / Q for commercial machine")
print("    - Blanket design, TBR, and tritium fuel cycle")
print("    - Power conversion cycle type and thermal efficiency")
print("    - Capital cost estimate or plant cost study")
print()

# ── Sensitivity analysis (base case) ─────────────────────────────────
print("── Sensitivity Analysis — Base Case (elasticity = %ΔLCOE / %Δparam) ──")
sens = model.sensitivity(results[0][0].params)

print("\n  Engineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"    {k:<28} {v:+.4f}")

print("\n  Financial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"    {k:<28} {v:+.4f}")

print()
print("── End of model output ──")
