"""HTS Compact Tokamak (Commonwealth Fusion Systems ARC) — LCOE estimate.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling approach:
    Uses 1costingfe CostModel (TOKAMAK / DT) with selective CAS overrides anchored
    to the Sorbom 2015 ARC paper (arc-reactor-specifications.md §6). ARC's published
    cost data covers only three fabricated components (vacuum vessel, blanket,
    magnets/structure); BOP and indirect accounts are computed by the framework
    using its ARIES-calibrated defaults.

    The nuclear island overrides (C220103, C220101, C220106) inflate ARC's 2014-USD
    fabricated costs to 2024 USD via CPI ×1.34 (BLS CPI-U: ~236 in 2014 → ~315 in
    2024). CAS27 (FLiBe special materials) uses Araiinejad 2025 NOAK estimate which
    is already in ~2025 USD.

Concept choice rationale:
    ConfinementConcept.TOKAMAK / Fuel.DT — directly maps to ARC's configuration.
    The CATF spherical-tokamak geometry defaults are replaced with ARC's published
    radial build (R0=3.3 m, a=1.13 m, B=9.2 T on-axis) from Sorbom 2015.

Key deviations from dt_tokamak.py reference:
    - Much smaller plant (261 MWe vs 1 GWe reference); ARC aggressive-pilot output.
    - eta_th = 0.46: supercritical Rankine at 250 bar / 540°C, ARC recommended cycle.
    - p_input = 38.6 MW: 25 MW LHCD + 13.6 MW ICRF (no NBI in ARC design).
    - C220103 dominates: REBCO-heavy magnet/structure = $6.9B 2024 USD — the single
      largest uncertainty in the cost model (5.5× REBCO price spread in 2014).
    - Availability is UNCERTAIN (not published in any CFS source); 0.75 is the
      central estimate; sensitivity to 0.50–0.90 is the primary output sweep.
    - CAS27 (FLiBe) overridden to 950 t × $154/kg NOAK ≈ $146M; framework default
      (PbLi-based) underestimates by ~20× at this plant size.
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model creation ────────────────────────────────────────────────────────

model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# ── CPI inflation constant (2014 → 2024) ─────────────────────────────────
# BLS CPI-U: ~236 (2014) → ~315 (2024) ≈ 1.336; rounded to 1.34
# Applied to all ARC 2014-USD fabricated component costs from arc-reactor-specifications.md §6
_CPI_2014_TO_2024 = 1.34

# ── Nuclear island cost overrides (ARC-specific, 2024 USD) ───────────────
# Source: arc-reactor-specifications.md §6, "Identification of Cost Feasibility"
# These cover ONLY the three costed subsystems; all BOP accounts use framework defaults.

# C220103: Magnets + structural support — midpoint of $5.1–5.2B 2014 USD
# "The cost of ARC is approximately one-third the cost of the 8 T ARIES-RS (~$14B)"
# Dominated by REBCO tape fabrication; materials only $160–260M; rest is labor/tooling.
# UNCERTAIN: REBCO price ranged $36–198/m in 2014 (5.5× spread); ~$20/m in 2025.
# Commercial viability target ~$10/kA-m — still ~10× below 2025 market prices.
_C220103_2014_M = 5150.0        # M$, midpoint of $5.1–5.2B; arc-reactor-specifications.md §6
C220103_OVERRIDE = _C220103_2014_M * _CPI_2014_TO_2024   # ≈ 6901 M$ 2024 USD

# C220101: First wall + FLiBe blanket — $260M 2014 USD
# Liquid FLiBe immersion blanket (breeder + coolant + shield combined).
# $160M materials + ~$100M fabrication; arc-reactor-specifications.md §6.
_C220101_2014_M = 260.0         # M$; arc-reactor-specifications.md §6
C220101_OVERRIDE = _C220101_2014_M * _CPI_2014_TO_2024   # ≈ 348 M$ 2024 USD

# C220106: Vacuum vessel — $92M 2014 USD
# Inconel-718 double-walled structure; $5.5M materials + fabrication.
# arc-reactor-specifications.md §6.
_C220106_2014_M = 92.0          # M$; arc-reactor-specifications.md §6
C220106_OVERRIDE = _C220106_2014_M * _CPI_2014_TO_2024   # ≈ 123 M$ 2024 USD

# CAS27: FLiBe special materials inventory
# 950 t FLiBe × $154/kg NOAK (20% learning rate assumed by Araiinejad 2025).
# Framework default (PbLi @ $3/kg) would yield ~$8M at this plant size — ~20× low.
# Source: arc-reactor-specifications.md §6 (quantity); Araiinejad & Shirvan 2025 (unit cost)
CAS27_OVERRIDE = 146.0          # M$ ~2025 USD; no inflation adjustment needed

# ── Forward run ──────────────────────────────────────────────────────────

result = model.forward(
    # ── Customer requirements ─────────────────────────────────────────────
    # ARC aggressive pilot: supercritical Rankine at 1200 K FLiBe outlet → 261 MWe
    # Source: arc-power-conversion-studies.md §Results, Table 15 (recommended cycle)
    # NOTE: 2025 CFS public target is 400 MWe — updated design not documented; not modeled.
    net_electric_mw=261.0,

    # UNCERTAIN: Capacity factor not stated in any CFS/ARC publication (blocking gap).
    # Range 0.50–0.90 produces a near-2× LCOE swing; central estimate = 0.75.
    # Depends on: divertor/FW replacement frequency, FLiBe maintenance, remote handling.
    # Source gap: analysis.md §2 Challenge 2; §5 Missing Parameters (capacity factor row)
    availability=0.75,

    lifetime_yr=30,              # Standard 30-yr plant lifetime; >9 FPY → TF coil replacement
                                 # TF coil fluence limit: arc-reactor-specifications.md §5

    n_mod=1,                     # Single-module plant (no multi-unit site assumed)
    construction_time_yr=5.0,    # DEFAULT — compact design; shorter than large LTS tokamak
    interest_rate=0.07,
    inflation_rate=0.0245,
    noak=True,                   # NOAK case (N-th of a kind); consistent with $154/kg FLiBe

    # ── ARC geometry ─────────────────────────────────────────────────────
    # Primary geometry from Sorbom 2015 (arc-reactor-specifications.md §2)
    R0=3.3,                      # Major radius [m]; "R = 3.3 m"; arc-reactor-specifications.md §2
    plasma_t=1.13,               # Minor radius a [m]; "a = 1.13 m"; arc-reactor-specifications.md §2
    elon=1.84,                   # Elongation κ; ARC equilibrium value from Sorbom 2015 §2
    blanket_t=0.80,              # DEFAULT — FLiBe liquid blanket thickness not stated in sources
    ht_shield_t=0.20,            # DEFAULT
    structure_t=0.20,            # DEFAULT
    vessel_t=0.20,               # DEFAULT

    # ── Power balance ────────────────────────────────────────────────────
    # Auxiliary heating: 25 MW LHCD (8 GHz, non-inductive) + 13.6 MW ICRF (120 MHz)
    # Source: arc-reactor-specifications.md §5.1
    # NOTE: 8 GHz LHCD system is TRL 5–6 — not yet demonstrated at required power.
    p_input=38.6,                # [MW]; 25 MW LHCD + 13.6 MW ICRF; arc-reactor-specifications.md §5.1

    mn=1.1,                      # DEFAULT neutron energy multiplier

    # Supercritical Rankine cycle at 250 bar, 540°C steam inlet
    # "Supercritical Rankine is recommended" — arc-power-conversion-studies.md §3.2
    # Net efficiency 46% confirmed by Colliva et al. 2024 independently.
    eta_th=0.46,                 # Net thermal efficiency; arc-power-conversion-studies.md §3.2, Table 15

    eta_p=0.5,                   # DEFAULT pumping efficiency
    eta_pin=0.5,                 # DEFAULT heating system wall-plug efficiency
    eta_de=0.85,                 # DEFAULT
    f_sub=0.03,                  # DEFAULT subsystem power fraction
    f_dec=0.0,                   # No direct energy conversion — thermal-only BOP
                                 # Source: dossier §Energy Capture; arc-power-conversion-studies.md

    p_coils=2.0,                 # DEFAULT coil resistive power [MW]
    p_cool=13.7,                 # DEFAULT cooling system power [MW] (FLiBe pumping)
    p_pump=1.0,                  # DEFAULT
    p_trit=10.0,                 # DEFAULT tritium processing power [MW]
    p_house=4.0,                 # DEFAULT housekeeping power [MW]
    p_cryo=0.5,                  # DEFAULT cryogenic power [MW]; REBCO at 20 K (less than LHe at 4 K)

    # ── CAS cost overrides ───────────────────────────────────────────────
    cost_overrides={
        # Nuclear island — from arc-reactor-specifications.md §6, inflated to 2024 USD
        "C220103": round(C220103_OVERRIDE, 1),  # Magnets+structure: $5.15B×1.34 ≈ $6,901 M$
        "C220101": round(C220101_OVERRIDE, 1),  # FLiBe blanket:     $260M×1.34  ≈ $348 M$
        "C220106": round(C220106_OVERRIDE, 1),  # Vacuum vessel:     $92M×1.34   ≈ $123 M$
        # Special materials — FLiBe inventory (already ~2025 USD from Araiinejad 2025)
        "CAS27":   CAS27_OVERRIDE,              # FLiBe: 950t × $154/kg NOAK = $146 M$
        # All other CAS accounts (CAS21 buildings, CAS23 turbine, CAS24 electrical,
        # CAS25 misc, CAS26 heat rejection, CAS30 indirect, CAS40 owner's, CAS50
        # supplementary) use framework defaults (ARIES-AT analogue calibration).
        # Justified: ARC paper explicitly excludes BOP from cost scope (§6).
    },
)

# ── Results ───────────────────────────────────────────────────────────────

c  = result.costs
pt = result.power_table

print("HTS Compact Tokamak — CFS ARC (261 MWe, 75% avail, 30 yr, NOAK)")
print(f"LCOE: {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.1f}")
print()

cas_rows = [
    ("CAS10", "Preconstruction",         c.cas10),
    ("CAS21", "Buildings",               c.cas21),
    ("CAS22", "Reactor Plant Equipment", c.cas22),
    ("CAS23", "Turbine Plant",           c.cas23),
    ("CAS24", "Electrical Plant",        c.cas24),
    ("CAS25", "Miscellaneous",           c.cas25),
    ("CAS26", "Heat Rejection",          c.cas26),
    ("CAS27", "Special Materials",       c.cas27),
    ("CAS28", "Digital Twin",            c.cas28),
    ("CAS29", "Contingency",             c.cas29),
    ("CAS30", "Indirect Costs",          c.cas30),
    ("CAS40", "Owner's Costs",           c.cas40),
    ("CAS50", "Supplementary",           c.cas50),
    ("CAS60", "IDC",                     c.cas60),
    ("CAS70", "O&M (annualized)",        c.cas70),
    ("CAS80", "Fuel (annualized)",       c.cas80),
    ("CAS90", "Financial",               c.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas_rows:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")

# ── CAS22 sub-account detail ──────────────────────────────────────────────

print("\nCAS22 Sub-accounts (Reactor Plant Equipment):")
print(f"{'Code':<12} {'Account':<32} {'M$':>8}  {'Note'}")
print("-" * 70)

cas22_labels = {
    "C220101": "First Wall + FLiBe Blanket",
    "C220102": "Shield",
    "C220103": "Coils (REBCO magnets+struct)",
    "C220104": "Heating System (ICRF+LHCD)",
    "C220105": "Primary Structure",
    "C220106": "Vacuum Vessel (Inconel-718)",
    "C220107": "Power Supplies",
    "C220108": "Divertor",
    "C220109": "DEC",
    "C220111": "Installation",
    "C220112": "Isotope Separation",
    "C220200": "Coolant (FLiBe circuits)",
    "C220300": "Aux Cooling",
    "C220400": "Rad Waste",
    "C220500": "Fuel Handling (tritium)",
    "C220600": "Other Equipment",
    "C220700": "I&C",
}
overridden = set(result.overridden) if hasattr(result, "overridden") else set()
for code, label in cas22_labels.items():
    val = result.cas22_detail.get(code, 0.0)
    note = "[ARC §6 override]" if code in overridden else "[DEFAULT]"
    print(f"{code:<12} {label:<32} {float(val):>8.1f}  {note}")
print("-" * 70)
total22 = result.cas22_detail.get("C220000", float(c.cas22))
print(f"{'C220000':<12} {'TOTAL':<32} {float(total22):>8.1f}")

# ── Key Assumptions ───────────────────────────────────────────────────────

print("""
Key Assumptions
===============
1. Net electric output: 261 MWe — ARC aggressive pilot, supercritical Rankine cycle.
   Source: arc-power-conversion-studies.md §Results, Table 15.
   NOTE: 2025 CFS public target = 400 MWe; updated design not documented. Not modeled.

2. Availability: 75% [UNCERTAIN — blocking data gap; analysis.md §5 Missing Parameters]
   Not published in any CFS or ARC document. Physically meaningful range: 50–90%.
   2× swing in availability ≈ 2× LCOE swing for this CAPEX-heavy concept.
   (analysis.md §2, Challenge 2; Hypothesis 2)

3. Magnet/structure cost: $6,901 M$ 2024 USD [UNCERTAIN — primary LCOE uncertainty]
   Basis: $5,150 M$ 2014 USD (midpoint of $5.1–5.2B) × CPI 1.34.
   Source: arc-reactor-specifications.md §6.
   REBCO price in 2014: $36–198/m (5.5× spread → $206–1,134 M$ materials alone).
   REBCO price in 2025: ~$20/m (~$100/kA-m) — still ~10× above $10/kA-m target.
   Sensitivity sweep: vary C220103 by ±50% to bracket REBCO price uncertainty.

4. Thermal efficiency: 46% net — supercritical Rankine at 250 bar / 540°C.
   Source: arc-power-conversion-studies.md §3.2, Table 15 (recommended cycle).
   Confirmed by Colliva et al. 2024 as "most promising solution" for ARC.

5. FLiBe special materials: $146 M$ (~2025 USD).
   Basis: 950 t FLiBe × $154/kg NOAK (20% learning rate).
   Source: arc-reactor-specifications.md §6 (quantity); Araiinejad & Shirvan 2025 (price).
   NOTE: FLiBe chemistry plant + tritium extraction system capital cost is NOT included
   (no published estimate exists; analysis.md §6, gap #15). This is a truly-unknown
   additive BOP cost with no ARIES analogue.

6. BOP and indirect costs: framework defaults (ARIES-AT analogue calibration).
   Justified: ARC paper explicitly excludes BOP from cost scope (§6 — "a full costing
   of the ARC reactor is beyond the scope of this paper").

7. No direct energy conversion: f_dec = 0.0. ARC uses thermal Rankine cycle only.
   Source: dossier §Energy Capture; arc-power-conversion-studies.md.
""")

# ── Sensitivity analysis ──────────────────────────────────────────────────

sens = model.sensitivity(
    result.params,
    cost_overrides={
        "C220103": round(C220103_OVERRIDE, 1),
        "C220101": round(C220101_OVERRIDE, 1),
        "C220106": round(C220106_OVERRIDE, 1),
        "CAS27":   CAS27_OVERRIDE,
    },
)

print("Sensitivity (elasticity = %LCOE / %param)")
print("-" * 48)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")
