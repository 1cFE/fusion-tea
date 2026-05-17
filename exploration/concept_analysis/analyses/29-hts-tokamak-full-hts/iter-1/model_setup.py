"""1costingfe model setup: HTS Tokamak - Full HTS (Energy Singularity / HH380)

Modeling approach
-----------------
Energy Singularity's HH380 commercial demo has NO published design parameters.
Every quantitative value below is an analogue estimate derived from:
  - CFS ARC concept (Sorbom et al. 2015) — best published proxy for a compact
    high-field HTS tokamak commercial design (D-shaped, demountable magnets, ~500 MWe)
  - HH170 physics targets (on-axis field, size relative to SPARC) — medium confidence
  - Framework defaults — where no analogue or physics argument constrains the choice

The LCOE output should be interpreted as a PROXY estimate for a compact high-field
HTS D-T tokamak, NOT a true Energy Singularity forecast. Uncertainty is ±50% on
capital cost alone (analysis.md §S2 Challenge 1).

Key concept features modeled:
  - Full HTS coil set (TF + PF + CS) — novel, introduces CS reliability risk
  - Compact D-shaped geometry at high field (~14 T on-axis target)
  - Steady-state operation (AI plasma control, confirmed on HH70)
  - ICRH primary heating (wall-plug efficiency ~65% vs. default 50%)
  - China-domestic supply chain context (not captured in framework cost basis)

Key deviations from framework defaults:
  - eta_pin raised to 0.65 (ICRH vs. default NBI/EC mix at 0.50)
  - availability lowered to 0.80 (unproven full-HTS CS coil reliability)
  - construction_time_yr reduced to 5.0 yr (company demonstrated fast build cadence)
  - All geometry parameters are UNCERTAIN analogue estimates

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ──────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# ── Plant-level configuration ────────────────────────────────────────────────
# Net electric output
# UNCERTAIN: No HH380 design exists. CFS ARC targets ~500 MWe for a compact
# HTS tokamak at similar field. analysis.md §S1 Gap 1 — blocking parameter.
# Source: Sorbom et al. (2015) ARC design, cited in analysis.md §S8 ref 4.
NET_ELECTRIC_MW = 500.0

# Capacity factor / availability
# UNCERTAIN: Full HTS CS coils under cyclic EM loading + neutron flux are
# undemonstrated (analysis.md §S3 "Full HTS Coil Set"). Lowered from 0.85
# default to reflect this novel reliability risk. AI plasma control may improve
# disruption frequency (analysis.md §S2 Challenge 4) — partially offsetting.
AVAILABILITY = 0.80

# Economic parameters — standard
LIFETIME_YR = 30        # DEFAULT: standard fusion plant lifetime assumption
N_MOD = 1               # DEFAULT: single-module commercial demo
INTEREST_RATE = 0.07    # DEFAULT: standard WACC assumption
INFLATION_RATE = 0.0245 # DEFAULT: US CPI baseline
NOAK = True             # NOAK scenario for cross-concept comparison

# Construction time
# UNCERTAIN: Energy Singularity built HH70 in under 2 years with >95% domestic
# sourcing (analysis.md §S1 "Build time"; energy-singularity-overview.md §Construction).
# Commercial-scale HH380 will take longer, but the track record suggests fast
# build cadence. Using 5 yr vs. default 6 yr.
CONSTRUCTION_TIME_YR = 5.0

# ── Geometry (all UNCERTAIN — no HH380 design parameters published) ───────────
# Analogue: CFS ARC (R0=3.3 m, a=1.1 m) from Sorbom et al. (2015) — analysis.md §S8.
# HH170 targets ~70% of SPARC volume (dossier.md §Confinement Concept).
# HH380 as a commercial power plant is expected to be larger than HH170.
# Using R0=3.0 m, A≈3.0 (D-shaped conventional aspect ratio) as central estimate.
R0 = 3.0        # UNCERTAIN: major radius [m]; CFS ARC analogue (3.3 m); analysis.md §S2 Challenge 1
PLASMA_T = 1.0  # UNCERTAIN: minor radius a [m]; A=3.0, consistent with compact D-shaped HTS
ELON = 1.7      # UNCERTAIN: elongation κ; standard D-shaped tokamak (ITER=1.85; SPARC~1.8)
BLANKET_T = 0.80  # DEFAULT: blanket thickness [m]; no blanket design disclosed (analysis.md §S1 Gap 3)
HT_SHIELD_T = 0.20  # DEFAULT: high-temperature shield [m]
STRUCTURE_T = 0.20  # DEFAULT: primary structure [m]
VESSEL_T = 0.20     # DEFAULT: vacuum vessel [m]

# ── Power balance ─────────────────────────────────────────────────────────────
# Heating power
# DEFAULT: No heating configuration disclosed for HH170 or HH380.
# ICRH confirmed on HH70 at low power (dossier.md §Primary Heating).
# 50 MW is a representative heating power for a Q>10 tokamak at this size class.
P_INPUT = 50.0  # DEFAULT: auxiliary heating power [MW]

# Neutron energy multiplier
MN = 1.1  # DEFAULT: standard D-T breeding blanket multiplier

# Thermal conversion efficiency
# DEFAULT: Power conversion cycle type not disclosed (analysis.md §S2 Challenge 5,
# analysis.md §S5 "Missing Parameters" row 5). Standard steam Rankine assumed.
ETA_TH = 0.46  # DEFAULT: thermal-to-electric efficiency; cycle undisclosed

# Pumping efficiency
ETA_P = 0.50  # DEFAULT

# Heating system wall-plug efficiency
# UNCERTAIN: ICRH confirmed as primary heating on HH70 (dossier.md §Primary Heating).
# ICRH wall-plug efficiency ~60-70% (analysis.md §S2 Challenge 5).
# Raised from default 0.50 to 0.65 to reflect ICRH vs. typical NBI/EC assumption.
ETA_PIN = 0.65  # UNCERTAIN: ICRH wall-plug ~60-70%; analysis.md §S2 Challenge 5

# Direct energy conversion
ETA_DE = 0.85  # DEFAULT: no DEC scheme disclosed for tokamak configuration
F_DEC = 0.0    # DEFAULT: no DEC

# Subsystem power fraction
F_SUB = 0.03  # DEFAULT

# Parasitic loads
P_COILS = 2.0   # DEFAULT: HTS coils have low resistive losses; cryogenic overhead in p_cryo
P_COOL = 13.7   # DEFAULT: cooling loads undisclosed
P_PUMP = 1.0    # DEFAULT
P_TRIT = 10.0   # DEFAULT: tritium processing power; full D-T plant
P_HOUSE = 4.0   # DEFAULT: housekeeping power
P_CRYO = 0.5    # DEFAULT: cryogenic system power [MW]; full HTS (TF+PF+CS) at 20 K
                #   Note: analysis.md §S7 notes full HTS may reduce cryogenic complexity
                #   vs. mixed LTS/HTS, but no specific data available for HH380.

# ── Model execution ──────────────────────────────────────────────────────────
result = model.forward(
    # Customer requirements
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=N_MOD,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=NOAK,

    # Geometry
    R0=R0,
    plasma_t=PLASMA_T,
    elon=ELON,
    blanket_t=BLANKET_T,
    ht_shield_t=HT_SHIELD_T,
    structure_t=STRUCTURE_T,
    vessel_t=VESSEL_T,

    # Power balance
    p_input=P_INPUT,
    mn=MN,
    eta_th=ETA_TH,
    eta_p=ETA_P,
    eta_pin=ETA_PIN,
    eta_de=ETA_DE,
    f_sub=F_SUB,
    f_dec=F_DEC,
    p_coils=P_COILS,
    p_cool=P_COOL,
    p_pump=P_PUMP,
    p_trit=P_TRIT,
    p_house=P_HOUSE,
    p_cryo=P_CRYO,

    # No cost_overrides: no published cost figures for any Energy Singularity
    # commercial component. All CAS accounts computed from framework defaults.
    # See analysis.md §S5 "Missing Parameters" — capital cost is blocking-gap.
    # anti-hallucination: do NOT invent cost figures for magnet system, blanket,
    # or any other account without an anchoring source.
)

# ── Results ──────────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("=" * 65)
print("HTS Tokamak - Full HTS (Energy Singularity / HH380 proxy)")
print("ALL parameters are analogue estimates — no HH380 design exists")
print("=" * 65)
print(f"LCOE:           {c.lcoe:.1f} $/MWh")
print(f"Overnight cost: {c.overnight_cost:.0f} $/kW")
print()
print(f"Fusion power:   {pt.p_fus:.0f} MW")
print(f"Thermal power:  {pt.p_th:.0f} MW")
print(f"Net electric:   {pt.p_net:.0f} MW")
print(f"Recirc. frac:   {pt.rec_frac:.2%}")
print(f"Q_engineering:  {pt.q_eng:.2f}")
print()

# CAS breakdown
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

print(f"{'Code':<8} {'Account':<30} {'M$':>10}")
print("-" * 50)
for code, name, val in cas:
    print(f"{code:<8} {name:<30} {float(val):>10.1f}")
print("-" * 50)
print(f"{'':8} {'Total Capital':<30} {float(c.total_capital):>10.1f}")

# CAS22 detail
print()
print("CAS22 Sub-Account Detail (Reactor Plant Equipment):")
print("-" * 50)
cas22_labels = {
    "C220101": "First Wall + Blanket",
    "C220102": "Shield",
    "C220103": "Coils (HTS TF+PF+CS)",
    "C220104": "Heating System (ICRH)",
    "C220105": "Primary Structure",
    "C220106": "Vacuum System",
    "C220107": "Power Supplies",
    "C220108": "Divertor",
    "C220109": "Direct Energy Conv.",
    "C220111": "Installation",
    "C220112": "Isotope Separation",
    "C220200": "Coolant System",
    "C220300": "Aux Cooling",
    "C220400": "Rad Waste",
    "C220500": "Fuel Handling",
    "C220600": "Other Equipment",
    "C220700": "I&C",
    "C220000": "CAS22 Total",
}
detail = result.cas22_detail
for key, label in cas22_labels.items():
    if key in detail:
        print(f"  {key}  {label:<26} {float(detail[key]):>10.1f}")

# Key assumptions
print()
print("=" * 65)
print("KEY ASSUMPTIONS (all UNCERTAIN — no HH380 design published)")
print("=" * 65)
print(f"  Net electric:   {NET_ELECTRIC_MW:.0f} MWe  [CFS ARC analogue; Sorbom et al. 2015]")
print(f"  Major radius:   {R0:.1f} m     [CFS ARC analogue; analysis.md §S2 Challenge 1]")
print(f"  Minor radius:   {PLASMA_T:.1f} m     [A={R0/PLASMA_T:.0f}, D-shaped; analogue]")
print(f"  Availability:   {AVAILABILITY:.0%}      [below 0.85 default; full HTS CS risk]")
print(f"  eta_th:         {ETA_TH:.2f}      [DEFAULT; power cycle undisclosed]")
print(f"  eta_pin:        {ETA_PIN:.2f}      [ICRH ~60-70%; analysis.md §S2 Ch.5]")
print(f"  Build time:     {CONSTRUCTION_TIME_YR:.0f} yr       [fast cadence; <2yr for HH70]")
print()
print("  BLOCKING GAPS (analysis.md §S5):")
print("    - No HH380 fusion power, net electric, or Q disclosed")
print("    - No blanket design — TBR, material, breeder type all unknown")
print("    - No thermal conversion cycle specified")
print("    - No capital cost study or plant engineering exists")
print("    - Full HTS CS coil fatigue/reliability data absent globally")

# ── Sensitivity analysis ─────────────────────────────────────────────────────
print()
print("=" * 65)
print("SENSITIVITY ANALYSIS (elasticity = %ΔLCOE / %Δparam)")
print("=" * 65)
sens = model.sensitivity(result.params)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<30} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<30} {v:+.4f}")
