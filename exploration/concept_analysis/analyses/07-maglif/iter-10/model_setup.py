"""MagLIF (D-T) — 1costingfe cost model setup (iter-10).

Concept: Magnetized Liner Inertial Fusion (MagLIF), D-T fuel.
Companies: Pacific Fusion (Santa Cruz, CA), Fuse Energy Technologies (San Leandro, CA).

Modeling Approach
-----------------
MagLIF is a pulsed MIF concept whose dominant cost categories — pulsed power driver
capital, per-shot consumables (liner + RTL), and rep-rated chamber clearing — have no
equivalents in the MFE database that underpins 1costingfe's reference scaling laws.
The framework is therefore used in a constrained mode:

  - ConfinementConcept.MAG_TARGET provides the structural skeleton (MIF/MagLIF layout).
  - cost_overrides inject Z-IFE reference values for the driver and consumable accounts
    that have no framework analogue.
  - All other CAS accounts (BOP, financial) are computed by the framework at the Z-IFE
    reference design point (1000 MWe, 0.5 Hz frozen-FLiBe RTL).

Key Deviations from Framework Defaults
---------------------------------------
1. Driver capital (C220104): overridden to $372M (Z-IFE LTD median); the default
   "heating & CD" account has no physical meaning for a pulsed power driver.
2. RTL + target factory (C220600): overridden to $120M; framework's laser-IFE-scale
   target factory default ($244M) does not apply to frozen-FLiBe RTL.
3. Blanket (C220101): overridden to $50M (Z-IFE FLiBe thick-liquid-wall chamber);
   the framework's PbLi volume-based unit cost does not apply.
4. Coils (C220103): zeroed — MagLIF has no superconducting magnets; pulsed copper
   axial field coils are embedded in driver account.
5. DEC (C220109): zeroed — no direct energy conversion in baseline D-T MagLIF.
6. Divertor (C220108): zeroed — no divertor in a pulsed spherical chamber design.
7. CAS21 Buildings: overridden to $200M (physical footprint estimate anchored to
   Pacific Fusion DS 73m × 80m, scaled to commercial plant); the default MFE/fission
   scaling formula produced $919M, which exceeds the driver cost and likely double-
   counts the capacitor hall already implicit in the Z-IFE $372M driver figure.

Iter-9 additions (addressing assessment F-1, F-2, F-3):
  F-1: Rep rate scenario sweep (0.1–1.8 Hz) at fixed capital — algebraic LCOE
       derived from baseline, calibrated against Z-IFE reference values.
  F-2: Per-shot consumable cost sweep ($0–$10/shot) — annualized consumable O&M
       added to LCOE numerator; break-even $/shot at 100 and 150 $/MWh reported.
  F-3: CAS21 buildings overridden to $200M (physical footprint basis, documented
       below); $919M MFE/fission default identified as a probable scaling artifact.

Iter-10 additions (addressing assessment F-1: eta_th category correction):
  F-1: ETA_TH re-classified as "Thermal (combined cycle, Brayton-Rankine)"; retained
       at 0.42 (steel-chamber near-term regime) as a justified deviation from the
       canonical 0.50 (C-C composite chambers). Added ETA_TH × ETA_PIN combined
       scenario matrix (4 combinations: {0.42, 0.50} × {0.60 LTD, 0.90 IMG}) to
       surface the joint sensitivity that single-point LCOE masks.

Reference Design Point
-----------------------
  - Z-IFE "best LTD case": 1000 MWe net, single chamber, 0.5 Hz, frozen-FLiBe RTL.
  - Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1 and §3.1.2.
  - COE from source: 7.0 ¢/kWeh = 70 $/MWh. Target from this script: comparable range.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import sys

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model creation ──────────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.MAG_TARGET, fuel=Fuel.DT)

# ── Plant configuration ──────────────────────────────────────────────────────
# Z-IFE reference design (z-ife-sand2006-7148-thermal-cycles.md §3.1.1)

# Customer requirements
NET_ELECTRIC_MW = 1000.0    # MWe; Z-IFE reference plant size
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1
                             # NOTE: Pacific Fusion's commercial target is 250 MWe
                             # (ans-news-2025-04-24-article-6980 §Combined power);
                             # 1000 MWe is used to match the Z-IFE COE reference.
                             # LCOE at 250 MWe will be materially higher.

# UNCERTAIN: availability. Z-IFE assumes 85% without explicit attribution.
# Thick-liquid-wall success: 85–90%; chamber/RTL clearing failure: 60–75%.
AVAILABILITY = 0.85         # UNCERTAIN: analysis.md §Section 5 (capacity factor row);
                             # used because it is the only published assumption

LIFETIME_YR = 30            # DEFAULT: consistent with fusion plant finance conventions;
                             # no MagLIF-specific data
CONSTRUCTION_TIME_YR = 4.0  # DEFAULT: from mif_mag_target.yaml; plausible for modular
                             # pulsed-power plant with simpler magnetics than tokamak

INTEREST_RATE = 0.0966      # Fixed charge rate 9.66%;
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1
INFLATION_RATE = 0.0245     # DEFAULT: consistent with tokamak reference example
NOAK = False                # FOAK — first commercial plant in the 2030s per Pacific
                             # Fusion timeline (pacificfusion-updates-experimental-
                             # breakthrough-by-pacific.md); no learning curve applicable

# Repetition rate — reference scenario (frozen-FLiBe RTL, single chamber)
REP_RATE_HZ = 0.5           # Hz; Z-IFE "best LTD case" (single chamber, frozen-FLiBe)
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5
                             # ("0.5 Hz is achievable with frozen-FLiBe RTL concept")
                             # NOTE: 0.5 Hz is NOT the 1 Hz commercial target of Pacific
                             # Fusion (arxiv-2408-15206 §7.1); it is the optimized Z-IFE
                             # published data point, chosen for calibration purposes.

SECONDS_PER_YEAR = 365.25 * 24 * 3600  # 31,557,600 s/yr
SHOTS_PER_YEAR = REP_RATE_HZ * SECONDS_PER_YEAR  # 15,778,800 shots/yr at 0.5 Hz

# ── Power balance ────────────────────────────────────────────────────────────
# Driver and thermal parameters from Z-IFE study

# Pulsed power driver parasitic draw: rep_rate × E_stored / eta_pin
# At 0.5 Hz, 42 MJ stored, 60% LTD efficiency: 42 × 0.5 / 0.6 ≈ 35 MW
P_DRIVER_MW = 35.0          # UNCERTAIN: derived from z-ife §3.1.1.5
                             # (42 MJ stored × 0.5 Hz / 0.60 LTD efficiency ≈ 35 MW)

ETA_TH = 0.42               # DEVIATION (justified): Energy capture = Thermal (combined
                             # cycle, Brayton-Rankine); canonical 0.50 per scoring_framework.md.
                             # Using 0.42 per z-ife-sand2006-7148-thermal-cycles.md §3.2
                             # (steel-chamber near-term regime; 0.50 requires C-C composite
                             # chambers not yet commercially available).
                             # See ETA_TH × ETA_PIN SCENARIO MATRIX below for 0.50 case.

ETA_PIN = 0.60              # LTD driver wall-plug efficiency;
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5
                             # (2005 workshop estimate: 60%)
                             # NOTE: IMG architecture claims ~90% wall-plug efficiency
                             # (analysis.md §Section 5; arxiv-2408-15206 §3.2),
                             # but unverified at plant scale.

MN = 1.1                    # DEFAULT: standard D-T neutron energy multiplier;
                             # no MagLIF-specific blanket multiplier published

# RTL steel remanufacturing parasitic load was 170 MWe for steel RTL baseline;
# frozen-FLiBe RTL eliminates this burden entirely.
F_SUB = 0.03                # DEFAULT: residual recirculating power fraction;
                             # 170 MWe steel RTL factory penalty NOT present here
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.3

P_TARGET_MW = 2.0           # UNCERTAIN: from mif_mag_target.yaml default; actual Z-IFE
                             # frozen-FLiBe RTL factory parasitic power not published
P_TRIT = 10.0               # DEFAULT: standard D-T tritium processing power [MW]
P_HOUSE = 4.0               # DEFAULT from mif_mag_target.yaml
P_PUMP = 1.0                # DEFAULT from mif_mag_target.yaml; FLiBe pump power [MW]
P_CRYO = 0.2                # DEFAULT from mif_mag_target.yaml; minimal cryo [MW]
P_COILS = 0.0               # Zero — no superconducting magnets; pulsed copper coils
                             # are part of driver energy budget, not a separate AC load;
                             # analysis.md §Key Differentiators: "No superconducting magnets"

# ── Chamber geometry ─────────────────────────────────────────────────────────
# Z-IFE reference: 4 m radius spherical chamber, 80 cm FLiBe blanket, 20 cm Al wall
# Source: z-ife-power-plant-concept.md §Abstract (Derzon et al. 2000, via analysis.md §S5)
PLASMA_T = 4.0              # Chamber radius [m]; Z-IFE 4 m radius
                             # Source: analysis.md §Section 5, blanket geometry row
BLANKET_T = 0.80            # FLiBe thick-liquid-wall blanket thickness [m];
                             # Source: z-ife-sand2006-7148-thermal-cycles.md (analysis §S5)
HT_SHIELD_T = 0.20          # 20 cm 6061-T6 Al first-wall structural wall;
                             # Source: z-ife-power-plant-concept.md §Abstract
STRUCTURE_T = 0.15          # DEFAULT from mif_mag_target.yaml
VESSEL_T = 0.10             # DEFAULT from mif_mag_target.yaml
R0 = 0.0                    # Not used for spherical chamber (mag_target concept)

# ── CAS account cost overrides ───────────────────────────────────────────────
# All overrides in M$ (2024$).
# Basis: Z-IFE direct capital decomposition (z-ife-sand2006-7148-thermal-cycles.md §3.1.2)
# and analysis.md §Section 2 "CAS-level cost structure" table.

cost_overrides = {
    # CAS21 — Buildings / Site Infrastructure (F-3 fix)
    # The default MFE/fission scaling formula produces $919M (from ARIES/WAGANER scaling
    # calibrated on tokamak reactor halls + tritium buildings). For MagLIF this is a
    # probable double-count: the Z-IFE $372M driver figure already includes the capacitor
    # hall space, and the tokamak formula is not calibrated for a capacitor bank facility.
    #
    # Physical footprint estimate:
    #   Pacific Fusion DS machine: 73m × 80m = 5,840 m² (published in Fusion Report
    #   interview, pacific-fusion-interview-fusion-report.md §DS Architecture)
    #   Commercial plant (1000 MWe, 10× DS power) → ~20,000–25,000 m² total facility
    #   Nuclear-grade industrial construction: ~$6,000–8,000/m² (US, 2024)
    #   20,000 m² × $7,000/m² = $140M + turbine hall, cooling towers, site work → ~$200M
    #
    # Double-count note: if the Z-IFE $372M driver already includes capacitor hall
    # infrastructure (as implied by Z-IFE §3.1.2 scope), then CAS21 should be ~$60–80M
    # for site work, roads, turbine hall, and non-driver buildings only. $200M is the
    # high-end bound; the low end is closer to $80M. This model uses $200M as the best
    # available physical estimate; $919M is treated as an artifact of MFE scaling.
    # UNCERTAIN: ±100% (physical footprint methodology, not a calibrated fusion cost)
    # Source: analysis.md §Section 2, §Section 5 (CAS21 row); pacific-fusion-interview-
    #         fusion-report.md §DS Architecture
    "CAS21": 200.0,          # M$; physical footprint estimate; replaces $919M default

    # C220103 — Coils / Magnet System
    # MagLIF has NO superconducting magnets. Framework default computes HTS coil cost
    # from geometry. Zeroed.
    # Source: analysis.md §Key Differentiators ("No superconducting magnets")
    "C220103": 0.0,

    # C220104 — Driver / Heating & Current Drive
    # In MagLIF, this account is the pulsed power driver (capacitor banks, switches,
    # transmission lines). Z-IFE LTD median: $372M for a 1 PW LTD driver.
    # Scaling law: C = 372 × (TW/1000)^0.6 M$ (z-ife §3.1.2).
    # LTD cavities: 12,600 units at ~$28k each = $353M (96% of driver capital).
    # Modern IMG architecture (Pacific Fusion DS) may be 5–10× cheaper (analysis §S2
    # Challenge 3; arxiv-2408-15206 §3.2.4 "cost of energy storage and switching must
    # decrease by a factor of 5 to 10"), but no published plant-scale estimate exists.
    # UNCERTAIN: ±50%
    # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.2 (analysis.md §Section 5)
    "C220104": 372.0,        # M$; LTD architecture median

    # C220101 — First Wall + Blanket (FLiBe thick-liquid-wall)
    # Z-IFE reference: FLiBe thick-liquid-wall, 80 cm, 4 m radius spherical chamber.
    # Framework default uses PbLi volume-based unit cost — inapplicable.
    # Estimated from Z-IFE §3.1.2 direct capital split:
    #   Total direct ≈ $575M; driver $372M; chamber+BOP remaining ≈ $203M;
    #   chamber component (FLiBe blanket + Al first wall) ≈ $46M (rough split).
    #   Used $50M as representative of FLiBe blanket + structural first wall.
    # UNCERTAIN: ±40%
    # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.2
    "C220101": 50.0,         # M$; Z-IFE FLiBe blanket + Al first wall analogue

    # C220108 — Divertor
    # MagLIF has no divertor; pulsed spherical chamber with thick liquid wall handles
    # debris removal between shots. Framework computes a divertor cost irrelevant here.
    # Source: analysis.md §Key Differentiators ("pulsed operation, not continuous")
    "C220108": 0.0,

    # C220109 — Direct Energy Conversion
    # No DEC in baseline D-T MagLIF (unlike Helion D-He3 which electromagnetically
    # recovers compression energy). Source: analysis.md §Key Differentiators vs. Helion
    "C220109": 0.0,

    # C220600 — Other Reactor Plant Equipment (RTL + Target Factory)
    # This account captures RTL/target factory capital. Z-IFE frozen-FLiBe RTL factory
    # cost not separately itemized; the study notes it eliminates the 170 MWe steel RTL
    # remanufacturing plant. Proxy: ~50% of laser IFE target factory ($244M) because
    # MagLIF RTL factory has mm-scale tolerances, metallic liner, simpler optics than
    # laser ICF. If cryo ice-layer targets are required, factory cost could be larger.
    # UNCERTAIN: ±100% (no published estimate for frozen-FLiBe RTL factory)
    # Source: analysis.md §Section 2, Challenge 2; costing_constants.yaml target_factory_base
    "C220600": 120.0,        # M$; RTL + target factory capital
}

# ── Forward pass (baseline: 0.5 Hz, 1000 MWe) ────────────────────────────────
result = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=NOAK,
    # Chamber geometry (Z-IFE reference spherical chamber)
    R0=R0,
    plasma_t=PLASMA_T,
    blanket_t=BLANKET_T,
    ht_shield_t=HT_SHIELD_T,
    structure_t=STRUCTURE_T,
    vessel_t=VESSEL_T,
    # Power balance
    p_input=P_DRIVER_MW,
    mn=MN,
    eta_th=ETA_TH,
    eta_pin=ETA_PIN,
    f_sub=F_SUB,
    f_dec=0.0,          # No DEC; analysis.md §Key Differentiators vs. Helion
    p_coils=P_COILS,
    p_pump=P_PUMP,
    p_trit=P_TRIT,
    p_house=P_HOUSE,
    p_cryo=P_CRYO,
    p_target=P_TARGET_MW,
    cost_overrides=cost_overrides,
)

# ── Results ──────────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("MagLIF D-T (Z-IFE LTD reference architecture) — 1000 MWe, 85% availability, 30 yr")
print(f"LCOE: {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.2f}")
print(f"Overridden accounts: {result.overridden}")
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

# ── CAS22 detail ─────────────────────────────────────────────────────────────
print()
print("CAS22 sub-accounts (Reactor Plant Equipment):")
cas22_labels = {
    "C220000": "CAS22 total",
    "C220101": "First Wall + Blanket (FLiBe)",
    "C220102": "Shield",
    "C220103": "Coils (zeroed — no SC magnets)",
    "C220104": "Driver (pulsed power, LTD ref)",
    "C220105": "Structure",
    "C220106": "Vacuum System",
    "C220107": "Power Supplies",
    "C220108": "Divertor (zeroed — absent in MagLIF)",
    "C220109": "DEC (zeroed)",
    "C220111": "Installation",
    "C220112": "Isotope Separation",
    "C220200": "Coolant Handling",
    "C220300": "Aux Cooling",
    "C220400": "Rad Waste",
    "C220500": "Fuel Handling",
    "C220600": "RTL + Target Factory",
    "C220700": "I&C",
}
for key, label in cas22_labels.items():
    val = result.cas22_detail.get(key)
    if val is not None:
        print(f"  {key:<10} {label:<38} {float(val):>8.1f} M$")

# ── Key Assumptions Summary ───────────────────────────────────────────────────
print()
print("=" * 65)
print("KEY ASSUMPTIONS SUMMARY")
print("=" * 65)
print(f"""
Architecture:  Z-IFE LTD reference, single chamber, 0.5 Hz,
               frozen-FLiBe RTL (best published MagLIF scenario).
               NOT the modern IMG architecture (Pacific Fusion DS).

Net output:    1000 MWe (Z-IFE reference, 4× larger than Pacific
               Fusion's 250 MWe commercial target; LCOE at 250 MWe
               will be materially higher — 500 MWe case in Z-IFE
               is already >10 ¢/kWeh per z-ife §3.1.1.6).

CAS21 Bldgs:   $200M (physical footprint estimate; default $919M
               is probable MFE/fission scaling artifact — exceeds
               driver cost and likely double-counts capacitor hall
               already implicit in the Z-IFE $372M driver figure).
               See analysis.md §Section 2 CAS-level cost table.

Driver cost:   $372M (LTD median, C220104); IMG 5–10× reduction
               (~$37–75M) would meaningfully lower LCOE (see sweep).
               Scaling: C = 372 × (TW/1000)^0.6 M$ from z-ife §3.1.2.

Blanket:       C220101 = $50M   [Z-IFE FLiBe chamber; ±40%]
RTL factory:   C220600 = $120M  [analogy estimate; ±100%]
Coils:         C220103 = $0M    [no superconducting magnets]
Divertor:      C220108 = $0M    [no divertor in MagLIF]
DEC:           C220109 = $0M    [D-T, no direct energy conversion]

Thermal eff.:  42% (combined Brayton-Rankine, steel chamber;
               C-C composite could reach 50% but not yet commercial)

Driver eff.:   60% LTD (IMG claims ~90%; unverified at plant scale)

Rep rate:      0.5 Hz (frozen-FLiBe RTL, single chamber, reference).
               Z-IFE reference COE at 0.5 Hz: 7.0 ¢/kWeh = 70 $/MWh.
               See REP RATE SWEEP below for full scenario range.

Per-shot consumables:
               Baseline captures frozen-FLiBe RTL (eliminates 170 MWe
               steel RTL factory parasitic load from z-ife §3.1.1.3).
               Cryo ice-layer target cost at scale is unknown and NOT
               captured as explicit O&M. See CONSUMABLE SWEEP below
               for break-even thresholds. Current cryo target cost
               (thousands $/shot) is orders of magnitude above the
               ~$1–2/shot commercial viability threshold.

References:    z-ife-sand2006-7148-thermal-cycles.md §3.1.1, §3.1.2
               analysis.md §Section 2 and §Section 5
               pacific-fusion-interview-fusion-report.md §DS Architecture
""")

# ── Sensitivity Analysis ─────────────────────────────────────────────────────
sens = model.sensitivity(result.params, cost_overrides=cost_overrides)

print("Sensitivity (elasticity = %LCOE / %param)")
print("NOTE: Overridden accounts (CAS21, C220104, C220101, C220600)")
print("      have zero gradient — use explicit sweeps below to test.")
print("-" * 55)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<30} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<30} {v:+.4f}")

# ── Rep Rate Scenario Sweep — Hypothesis 1 (F-1) ─────────────────────────────
#
# Physics: for a pulsed concept at fixed single-chamber capital, net electric output
# scales linearly with rep rate (P_net ∝ rep_rate × yield_per_shot × eta_th × mn).
# LCOE consequently scales as 1/rep_rate at fixed capital.
#
# Calibration: baseline LCOE at 0.5 Hz anchors the sweep. Model gives ~7.6 ¢/kWeh
# vs. Z-IFE reference 7.0 ¢/kWeh — 8% discrepancy (acceptable, from financial
# parameter differences). Analysis confirmed this calibration in analysis.md §S2.
#
# Algebraic derivation:
#   yield_per_shot_GJ: calibrated so that P_net = 1000 MWe at rep_rate = 0.5 Hz
#   P_net(rr) = yield_per_shot_GJ × rr × eta_th × mn × 1000  [MWe]
#   annual_energy(rr) = P_net(rr) × 8760 × availability          [MWh/yr]
#   LCOE(rr) = LCOE_baseline × (REP_RATE_HZ / rr)              [$/MWh]
#
# Why algebraic and not framework calls at each net_electric_mw?
#   The framework scales power-dependent BOP accounts (CAS23-26, buildings) with
#   net electric, which is appropriate for differently sized plants but not for a
#   single plant whose output changes with rep rate at fixed capital investment.
#   The algebraic form isolates the rep rate lever correctly.
#
# Source for Z-IFE reference calibration points:
#   z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6

print()
print("=" * 65)
print("REP RATE SCENARIO SWEEP — Hypothesis 1 (F-1)")
print("LCOE at fixed single-chamber capital, varying rep rate")
print("Baseline calibrated to 0.5 Hz → Z-IFE ref 7.0 ¢/kWeh = 70 $/MWh")
print("=" * 65)

LCOE_BASELINE = float(c.lcoe)          # $/MWh, from model at 0.5 Hz
# Yield per shot: calibrated from baseline net power
# P_net ≈ yield_per_shot_GJ × rep_rate_hz × eta_th × mn × 1000 MWe/GJ
# => yield_per_shot_GJ = NET_ELECTRIC_MW / (REP_RATE_HZ × ETA_TH × MN × 1000)
YIELD_PER_SHOT_GJ = NET_ELECTRIC_MW / (REP_RATE_HZ * ETA_TH * MN * 1000)

rep_rate_scenarios = [
    (0.1,  "10-chamber steel RTL (Z-IFE baseline)"),
    (0.25, "Single chamber, sub-Hz"),
    (0.5,  "Single chamber, frozen-FLiBe RTL (reference)"),
    (1.0,  "Single chamber, commercial target"),
    (1.8,  "Single chamber, minimum-COE (beyond RTL reach)"),
]

print(f"\n  {'Rep Rate':>8}  {'Net Power':>10}  {'LCOE $/MWh':>12}  {'LCOE ¢/kWeh':>12}  Notes")
print("  " + "-" * 82)

ZIFE_REF = {0.1: 200.0, 0.5: 70.0}  # Z-IFE reference COE in $/MWh for comparison

for rr, label in rep_rate_scenarios:
    p_net_mw = YIELD_PER_SHOT_GJ * rr * ETA_TH * MN * 1000
    lcoe_rr = LCOE_BASELINE * (REP_RATE_HZ / rr)
    lcoe_ckweh = lcoe_rr / 10.0  # $/MWh → ¢/kWeh
    zife_note = ""
    if rr in ZIFE_REF:
        zife_note = f"  [Z-IFE ref: {ZIFE_REF[rr]:.0f} $/MWh]"
    print(f"  {rr:>7.2f} Hz  {p_net_mw:>8.0f} MWe  {lcoe_rr:>10.1f} $/MWh"
          f"  {lcoe_ckweh:>10.2f} ¢/kWeh  {label}{zife_note}")

print()
print("  Calibration check: model LCOE at 0.5 Hz =", f"{LCOE_BASELINE:.1f} $/MWh",
      f"({LCOE_BASELINE/10:.2f} ¢/kWeh)")
print("  Z-IFE reference at 0.5 Hz: 70 $/MWh (7.0 ¢/kWeh); discrepancy:",
      f"{abs(LCOE_BASELINE - 70.0)/70.0*100:.0f}%")
print()
print("  Advanced fission threshold:  40–60 $/MWh (4–6 ¢/kWeh)")
print("  Break-even rep rate (≤60 $/MWh):",
      f"{REP_RATE_HZ * LCOE_BASELINE / 60.0:.2f} Hz")
print("  Break-even rep rate (≤40 $/MWh):",
      f"{REP_RATE_HZ * LCOE_BASELINE / 40.0:.2f} Hz")
print()
print("  NOTE: 0.1 Hz algebraic LCOE (single chamber) is HIGHER than Z-IFE's")
print("        20 ¢/kWeh because Z-IFE uses 10 chambers at 0.1 Hz to produce")
print("        1000 MWe total — the multi-chamber capital dilutes per-MWh cost")
print("        vs. single-chamber at 0.1 Hz. Single-chamber at 0.1 Hz is")
print("        economically unviable regardless of driver or target cost.")

# ── Per-Shot Consumable Cost Sweep — Hypothesis 2 (F-2) ──────────────────────
#
# Target consumable cost (cryo ice-layer liner + RTL) is unknown at commercial scale.
# This sweep adds annualized consumable O&M to the LCOE numerator and finds break-even.
#
# Consumable cost formula:
#   annual_consumable_M = cost_per_shot_$ × shots_per_year / 1e6
#
# LCOE with consumables:
#   LCOE_with_consm = LCOE_baseline + annual_consumable_M × 1e6 / annual_energy_MWh
#
# Break-even $/shot at threshold T $/MWh:
#   cost_per_shot_breakeven = (T - LCOE_baseline) × annual_energy_MWh / shots_per_year
#
# Shots/yr at 0.5 Hz: 0.5 × 31,557,600 = 15,778,800 shots/yr
# Annual energy: 1000 × 8760 × 0.85 = 7,446,000 MWh/yr
#
# Source: analysis.md §Section 2, Challenge 2 (consumable cost floor analysis)

print()
print("=" * 65)
print("PER-SHOT CONSUMABLE COST SWEEP — Hypothesis 2 (F-2)")
print(f"Baseline scenario: {REP_RATE_HZ} Hz, {int(NET_ELECTRIC_MW)} MWe,",
      f"{int(SHOTS_PER_YEAR/1e6*10)/10:.1f}M shots/yr")
print("Adding annualized cryo target + RTL consumable cost to LCOE")
print("=" * 65)

ANNUAL_ENERGY_MWH = NET_ELECTRIC_MW * 8760 * AVAILABILITY  # MWh/yr

consumable_scenarios = [0, 1, 2, 5, 10]  # $/shot

print(f"\n  {'$/shot':>7}  {'Annual cost M$':>14}  {'LCOE $/MWh':>12}  {'LCOE ¢/kWeh':>12}")
print("  " + "-" * 52)
for cps in consumable_scenarios:
    annual_consm_M = cps * SHOTS_PER_YEAR / 1e6
    lcoe_with = LCOE_BASELINE + annual_consm_M * 1e6 / ANNUAL_ENERGY_MWH
    print(f"  {cps:>7.0f}  {annual_consm_M:>12.1f} M$  {lcoe_with:>10.1f} $/MWh"
          f"  {lcoe_with/10:>10.2f} ¢/kWeh")

# Break-even thresholds
for threshold in [100.0, 150.0]:
    if LCOE_BASELINE < threshold:
        headroom_m = (threshold - LCOE_BASELINE) * ANNUAL_ENERGY_MWH / 1e6  # M$/yr
        breakeven_per_shot = headroom_m * 1e6 / SHOTS_PER_YEAR
        print(f"\n  Break-even at {threshold:.0f} $/MWh: {breakeven_per_shot:.1f} $/shot"
              f"  (annual budget: {headroom_m:.0f} M$/yr)")
    else:
        print(f"\n  Baseline LCOE already exceeds {threshold:.0f} $/MWh — no headroom.")

print()
print("  Commercial viability threshold: ~$1–2/shot")
print("  Current cryo target cost: thousands of $/shot (no production path)")
print("  Source: analysis.md §Section 2, Challenge 2; analysis.md §Section 5")
print("          (Consumable cost floor table: RTL unit cost ~$0.70/shot historical;")
print("           cryo ice-layer target cost: truly-unknown, critically-blocking)")

# ── Driver Cost Sweep — Hypothesis 3 ─────────────────────────────────────────
#
# How sensitive is LCOE to driver capital (C220104) as IMG architecture
# (Pacific Fusion DS, Fuse Energy TITAN) potentially achieves 5–10× cost reduction
# vs. the Z-IFE LTD reference?
#
# NOTE: with CAS21 corrected to $200M (vs. prior $919M), driver capital is now a
# larger fraction of total capital than in iter-8, so driver cost sensitivity is
# higher than the previous model implied. The $919M buildings artifact had diluted
# the driver cost signal.
#
# Source: arxiv-2408-15206-pulsed-magnetic-fusion.md §3.2.4 ("factor of 5 to 10"
#         reduction required); analysis.md §Section 2, Challenge 3

print()
print("=" * 65)
print("DRIVER COST SWEEP (C220104) — Hypothesis 3")
print("LCOE as pulsed power cost falls from LTD baseline to IMG target")
print("NOTE: CAS21 corrected to $200M (iter-9), increasing driver sensitivity")
print("vs. iter-8 where $919M buildings dominated and diluted driver signal.")
print("=" * 65)

driver_scenarios = [
    ("LTD ref median",        372.0, "Z-IFE LTD reference ($372M)"),
    ("2× reduction",          186.0, "2× improvement over LTD"),
    ("4× reduction",           93.0, "4× improvement"),
    ("5× reduction (target)",  75.0, "5× — IMG cost target (arXiv:2408.15206 §3.2.4)"),
    ("10× reduction",          37.0, "10× — optimistic IMG (ibid.)"),
]

print(f"\n  {'Scenario':<28} {'Driver M$':>9}  {'Driver %Cap':>11}  {'LCOE $/MWh':>10}")
print("  " + "-" * 64)
for label, driver_m, note in driver_scenarios:
    r = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        availability=AVAILABILITY,
        lifetime_yr=LIFETIME_YR,
        n_mod=1,
        construction_time_yr=CONSTRUCTION_TIME_YR,
        interest_rate=INTEREST_RATE,
        inflation_rate=INFLATION_RATE,
        noak=NOAK,
        R0=R0,
        plasma_t=PLASMA_T,
        blanket_t=BLANKET_T,
        ht_shield_t=HT_SHIELD_T,
        structure_t=STRUCTURE_T,
        vessel_t=VESSEL_T,
        p_input=P_DRIVER_MW,
        mn=MN,
        eta_th=ETA_TH,
        eta_pin=ETA_PIN,
        f_sub=F_SUB,
        f_dec=0.0,
        p_coils=P_COILS,
        p_pump=P_PUMP,
        p_trit=P_TRIT,
        p_house=P_HOUSE,
        p_cryo=P_CRYO,
        p_target=P_TARGET_MW,
        cost_overrides={**cost_overrides, "C220104": driver_m},
    )
    pct_cap = driver_m / float(r.costs.total_capital) * 100
    print(f"  {label:<28} {driver_m:>9.0f}  {pct_cap:>9.1f}%  {float(r.costs.lcoe):>10.1f}"
          f"  ({note})")

print()
print("  Z-IFE reference COE at 0.5 Hz: 70 $/MWh (7.0 ¢/kWeh)")
print("  Advanced fission threshold:     40–60 $/MWh (4–6 ¢/kWeh)")
print("  Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6")

# ── ETA_TH × ETA_PIN Combined Scenario Matrix — F-1 (iter-10) ────────────────
#
# F-1 correction: ETA_TH re-classified as combined Brayton-Rankine (canonical 0.50).
# Baseline retained at 0.42 (steel-chamber regime, peer-reviewed Z-IFE value).
# This matrix surfaces the joint sensitivity between thermal cycle maturity (eta_th)
# and driver architecture (eta_pin), which single-point LCOE at {0.42, 0.60} masks.
#
# eta_th = 0.42: steel chamber, near-term achievable (Z-IFE §3.2 baseline)
# eta_th = 0.50: C-C composite chamber, advanced material assumption (Z-IFE §3.2 path)
# eta_pin = 0.60: LTD driver wall-plug efficiency (Z-IFE §3.1.1.5 2005 estimate)
# eta_pin = 0.90: IMG architecture claim (arXiv:2408.15206 §3.2; unverified at plant scale)
#
# Because eta_pin affects P_DRIVER_MW (the recirculating driver draw), and P_DRIVER_MW
# is held fixed in the baseline forward pass (derived from stored energy and rep rate),
# the cleaner lever here is to vary ETA_PIN's effect on net power balance: a higher
# eta_pin means the same 42 MJ stored energy requires less wall-plug draw. We capture
# this by adjusting p_input proportionally: p_input = 42e-3 GJ × 0.5 Hz / eta_pin × 1000.
# At eta_pin=0.60: 42 × 0.5 / 0.60 = 35 MW (current baseline).
# At eta_pin=0.90: 42 × 0.5 / 0.90 ≈ 23 MW (IMG scenario).
#
# Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5, §3.2; arxiv-2408-15206 §3.2

STORED_ENERGY_GJ = 42e-3     # 42 MJ stored per shot (Z-IFE LTD reference)

eta_th_scenarios = [
    (0.42, "0.42 — steel chamber, Z-IFE baseline"),
    (0.50, "0.50 — C-C composite, advanced material assumption"),
]
eta_pin_scenarios = [
    (0.60, "0.60 — LTD (Z-IFE reference)"),
    (0.90, "0.90 — IMG claim (unverified at plant scale)"),
]

print()
print("=" * 72)
print("ETA_TH × ETA_PIN COMBINED SCENARIO MATRIX — F-1 (iter-10)")
print("Joint sensitivity: thermal cycle maturity × driver architecture")
print("Canonical eta_th = 0.50 (combined Brayton-Rankine, scoring_framework.md)")
print("Baseline: 0.42 (steel chamber, Z-IFE §3.2 justified deviation)")
print("=" * 72)
print(f"\n  {'eta_th':<6} {'eta_pin':<8} {'P_driver MW':>11} {'LCOE $/MWh':>12} {'LCOE ¢/kWeh':>12}  Notes")
print("  " + "-" * 80)

for eth, eth_label in eta_th_scenarios:
    for epin, epin_label in eta_pin_scenarios:
        p_drv = STORED_ENERGY_GJ * REP_RATE_HZ / epin * 1000  # MW
        r = model.forward(
            net_electric_mw=NET_ELECTRIC_MW,
            availability=AVAILABILITY,
            lifetime_yr=LIFETIME_YR,
            n_mod=1,
            construction_time_yr=CONSTRUCTION_TIME_YR,
            interest_rate=INTEREST_RATE,
            inflation_rate=INFLATION_RATE,
            noak=NOAK,
            R0=R0,
            plasma_t=PLASMA_T,
            blanket_t=BLANKET_T,
            ht_shield_t=HT_SHIELD_T,
            structure_t=STRUCTURE_T,
            vessel_t=VESSEL_T,
            p_input=p_drv,
            mn=MN,
            eta_th=eth,
            eta_pin=epin,
            f_sub=F_SUB,
            f_dec=0.0,
            p_coils=P_COILS,
            p_pump=P_PUMP,
            p_trit=P_TRIT,
            p_house=P_HOUSE,
            p_cryo=P_CRYO,
            p_target=P_TARGET_MW,
            cost_overrides=cost_overrides,
        )
        lcoe = float(r.costs.lcoe)
        tag = " ← baseline" if (eth == 0.42 and epin == 0.60) else ""
        print(f"  {eth:<6.2f} {epin:<8.2f} {p_drv:>9.1f} MW  {lcoe:>10.1f} $/MWh"
              f"  {lcoe/10:>10.2f} ¢/kWeh  {tag}")

print()
print("  Rows: thermal cycle maturity (steel chamber vs. C-C composite)")
print("  Cols: driver architecture (LTD 60% vs. IMG 90% wall-plug efficiency)")
print("  eta_th=0.50 rows represent 'advanced material assumption' scenarios.")
print("  eta_pin=0.90 column is unverified at plant scale (IMG claim only).")
print("  Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5, §3.2")
print("          arxiv-2408-15206-pulsed-magnetic-fusion.md §3.2")
print()
sys.stdout.flush()
