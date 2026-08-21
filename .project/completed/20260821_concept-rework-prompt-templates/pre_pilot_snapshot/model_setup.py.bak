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
    2024). CAS27 (FLiBe special materials) uses Araiinejad 2025 NOAK estimate, which
    is already in ~2025 USD.

    Indirect cost framing:
    The FECONS/pyFECONS framework (arxiv-2601-21724 §8.2) provides a structural
    split: direct costs ~71% of total capital cost, indirect/owner/supplementary/
    financial ~29% of TCC. This implies total plant cost is roughly 1.41× the direct
    cost (nuclear island + BOP) — not 2–3× the nuclear island alone. The framework
    defaults encode this split via CAS30/40/50/60 fractions.

    FOAK scenario:
    The NOAK central estimate (noak=True, C220103 at paper value) is paired with a
    discrete FOAK scenario that applies a 2× multiplier to the nuclear island magnets
    cost and sets noak=False. CATF IWG methodology (arxiv-2602-19389 §2.1.5) cites
    FOAK fusion plants at 150–200 $/MWh vs. 60–100 $/MWh NOAK — this is a
    step-function risk, not a continuous sensitivity parameter.

    iter-7 updates (vs. iter-6):
    1. Capacity factor framing corrected to Schwartz et al. (2024, arXiv:2405.01514):
       naive inverse-availability LCOE scaling overstates the economic penalty by up to
       15% when maintenance is scheduled in low-price windows. 80% availability retains
       91% of maintenance-free value (not 80%). Simple inverse used as conservative
       upper bound; Schwartz et al. grid-value curve is the central estimate.
    2. FLiBe chemistry + tritium processing cost now has an order-of-magnitude floor:
       Woodruff Scientific (2020) ARPA-E ALPHA re-costing (OSTI:1820946) gives
       CAS22.5 Fuel Processing averaging $124M at ~500 MWe for compact MIF/Z-pinch
       concepts — structural analogue, not direct match. Treat $100–200M as floor for
       ARC's FLiBe chemistry plant (additive BOP line, not yet in C220500 override).
    3. ARPA-E ALPHA cross-concept NOAK LCOE ($43/MWh, ~$2.4/W, non-HTS compact
       fusion, 90% availability, zero contingency) added to Key Assumptions as a
       non-HTS lower-bound reference.

Concept choice rationale:
    ConfinementConcept.TOKAMAK / Fuel.DT — directly maps to ARC's configuration.
    The CATF spherical-tokamak geometry defaults are replaced with ARC's published
    radial build (R0=3.3 m, a=1.13 m) from Sorbom 2015.

Key deviations from dt_tokamak.py reference:
    - Much smaller plant (261 MWe vs 1 GWe reference); ARC aggressive-pilot output.
    - eta_th = 0.46: supercritical Rankine at 250 bar / 540°C, ARC recommended cycle.
    - p_input = 38.6 MW: 25 MW LHCD + 13.6 MW ICRF (no NBI in ARC design).
    - C220103 dominates: REBCO-heavy magnet/structure = ~$6,901 M$ 2024 USD — the
      single largest uncertainty in the cost model (5.5× REBCO price spread in 2014).
    - Availability: 0.85 canonical per scoring_framework.md §Plant availability
      (MCF steady-state/quasi-steady, D-T). Previously 0.75 (discretionary low end
      of Araiinejad & Shirvan 75–90% band). No Tier-A override exists for ARC.
    - CAS27 (FLiBe) overridden to 950 t × $154/kg NOAK ≈ $146 M$; framework default
      (PbLi-based) underestimates by ~20× at this plant size.
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model creation ────────────────────────────────────────────────────────

model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# ── CPI inflation constant (2014 → 2024) ─────────────────────────────────
# BLS CPI-U: ~236 (2014) → ~315 (2024) ≈ 1.336; rounded to 1.34.
# Applied to all ARC 2014-USD fabricated component costs from arc-reactor-specifications.md §6.
_CPI_2014_TO_2024 = 1.34

# ── Nuclear island cost overrides (ARC-specific, 2024 USD) ───────────────
# Source: arc-reactor-specifications.md §6, "Identification of Cost Feasibility"
# These cover ONLY the three costed subsystems; all BOP accounts use framework defaults.
# ARC paper explicitly excludes BOP: "a full costing of the ARC reactor is beyond
# the scope of this paper." — arc-reactor-specifications.md §6

# C220103: Magnets + structural support — midpoint of $5.1–5.2B 2014 USD
# "The cost of ARC is approximately one-third the cost of the 8 T ARIES-RS (~$14B)"
# Dominated by REBCO tape fabrication; materials only $160–260M; rest is labor/tooling.
# UNCERTAIN: REBCO price ranged $36–198/m in 2014 (5.5× spread); ~$20/m in 2025 (~$100/kA-m).
# Commercial viability target ~$10/kA-m — still ~10× above 2025 market prices.
# Source: arc-reactor-specifications.md §4.1, §6;
#         sciencedirect-science-article-pii-s2772830725000390.md §Introduction
_C220103_2014_M = 5150.0        # M$, midpoint of $5.1–5.2B; arc-reactor-specifications.md §6
C220103_OVERRIDE = _C220103_2014_M * _CPI_2014_TO_2024  # ≈ 6,901 M$ 2024 USD

# C220101: First wall + FLiBe blanket — $260M 2014 USD
# Liquid FLiBe immersion blanket (breeder + coolant + shield combined).
# $160M materials + ~$100M fabrication; arc-reactor-specifications.md §6.
_C220101_2014_M = 260.0         # M$; arc-reactor-specifications.md §6
C220101_OVERRIDE = _C220101_2014_M * _CPI_2014_TO_2024  # ≈ 348 M$ 2024 USD

# C220106: Vacuum vessel — $92M 2014 USD
# Inconel-718 double-walled structure; $5.5M materials + fabrication.
# Source: arc-reactor-specifications.md §6
_C220106_2014_M = 92.0          # M$; arc-reactor-specifications.md §6
C220106_OVERRIDE = _C220106_2014_M * _CPI_2014_TO_2024  # ≈ 123 M$ 2024 USD

# CAS27: FLiBe special materials inventory
# 950 t FLiBe × $154/kg NOAK (20% learning rate assumed by Araiinejad 2025).
# Framework default (PbLi @ $3/kg) would yield ~$8M at this plant size — ~20× low.
# NOTE: FLiBe chemistry plant + tritium extraction system capital cost is NOT included
# here. iter-7 update: Woodruff Scientific (2020) ARPA-E ALPHA re-costing (OSTI:1820946)
# gives CAS22.5 Fuel Processing averaging $124M at ~500 MWe for compact MIF/Z-pinch
# concepts. Structural analogue only (different blanket chemistry, no FLiBe); treat
# $100–200M as an order-of-magnitude floor for ARC's additive FLiBe chemistry +
# tritium extraction BOP line. Not yet included in model — still a truly-unknown additive.
# Source: arc-reactor-specifications.md §6 (quantity); Araiinejad & Shirvan 2025 (price);
#         analysis.md §6, gap #15; osti-servlets-purl-1820946.md (ALPHA re-costing floor)
CAS27_OVERRIDE = 146.0          # M$ ~2025 USD; no CPI adjustment needed

# Shared cost_overrides dict (used by both NOAK run and sensitivity)
_NOAK_OVERRIDES = {
    "C220103": round(C220103_OVERRIDE, 1),  # Magnets+structure: $5,150M×1.34 ≈ $6,901 M$
    "C220101": round(C220101_OVERRIDE, 1),  # FLiBe blanket:     $260M×1.34   ≈ $348 M$
    "C220106": round(C220106_OVERRIDE, 1),  # Vacuum vessel:     $92M×1.34    ≈ $123 M$
    "CAS27":   CAS27_OVERRIDE,              # FLiBe: 950 t × $154/kg NOAK = $146 M$
}

# ── NOAK forward run (central estimate) ──────────────────────────────────

result = model.forward(
    # ── Customer requirements ─────────────────────────────────────────────
    # ARC aggressive pilot: supercritical Rankine at 1200 K FLiBe outlet → 261 MWe.
    # Source: arc-power-conversion-studies.md §Results, Table 15 (recommended cycle).
    # NOTE: 2025 CFS public target is 400 MWe — updated design not publicly documented.
    net_electric_mw=261.0,

    # Canonical 0.85 per scoring_framework.md §Plant availability (MCF steady-state/
    # quasi-steady, D-T). Previously 0.75 (discretionary low end of Araiinejad &
    # Shirvan 75–90% band — no published 75% target). No Tier-A override (externally-
    # published availability target with stated maintenance basis) exists for ARC;
    # the canonical value therefore applies. Cross-concept LCOE comparisons within the
    # MCF/pulsed-IFE family are now apples-to-apples on this dimension.
    # iter-7 note: naive 2× LCOE swing from 50% → 90% availability is an upper bound.
    # Schwartz et al. (2024, arXiv:2405.01514) show grid-value-weighted penalty is up
    # to 15% smaller when maintenance is scheduled in low-price windows (spring/summer).
    # At 80% availability, a fusion plant retains 91% of maintenance-free plant value.
    # Simple inverse scaling (used below) is the conservative upper bound, not central.
    # Source: scoring_framework.md §Plant availability; arxiv-2405-01514.md §2.2 Results
    availability=0.85,

    lifetime_yr=30,               # Standard 30-yr plant lifetime; DEFAULT
                                  # NOTE: TF coil fluence limit = 9 FPY (REBCO neutron limit).
                                  # Coil replacement required at ~9 FPY — cost not yet modeled.
                                  # Source: arc-reactor-specifications.md §5

    n_mod=1,                      # Single-module plant
    construction_time_yr=5.0,     # DEFAULT — compact; shorter than large LTS tokamak (6 yr)
    interest_rate=0.07,           # DEFAULT — standard capital cost rate
    inflation_rate=0.0245,        # DEFAULT
    noak=True,                    # NOAK case; consistent with $154/kg FLiBe and $1.06M/tonne scaling

    # ── ARC geometry ─────────────────────────────────────────────────────
    # Primary geometry from Sorbom 2015 (arc-reactor-specifications.md §2).
    R0=3.3,                       # Major radius [m]; arc-reactor-specifications.md §2
    plasma_t=1.13,                # Minor radius a [m]; arc-reactor-specifications.md §2
    elon=1.84,                    # Elongation κ; ARC equilibrium; arc-reactor-specifications.md §2
    blanket_t=0.80,               # DEFAULT — FLiBe blanket thickness not stated in sources
    ht_shield_t=0.20,             # DEFAULT
    structure_t=0.20,             # DEFAULT
    vessel_t=0.20,                # DEFAULT

    # ── Power balance ────────────────────────────────────────────────────
    # Auxiliary heating: 25 MW LHCD (8 GHz, non-inductive) + 13.6 MW ICRF (120 MHz).
    # Source: arc-reactor-specifications.md §5.1.
    # NOTE: 8 GHz LHCD system is TRL 5–6 — not yet demonstrated at required power level.
    #        analysis.md §2, Challenge 5; analysis.md §3 (LHCD)
    p_input=38.6,                 # [MW]; 25 MW LHCD + 13.6 MW ICRF; arc-reactor-specifications.md §5.1

    mn=1.1,                       # DEFAULT neutron energy multiplier

    # Supercritical Rankine cycle at 250 bar, 540°C steam inlet.
    # "Supercritical Rankine is recommended" — arc-power-conversion-studies.md §3.2.
    # Net efficiency 46% confirmed independently by Colliva et al. 2024.
    # Source: arc-power-conversion-studies.md §3.2, Table 15
    eta_th=0.46,

    eta_p=0.5,                    # DEFAULT pumping efficiency
    eta_pin=0.5,                  # DEFAULT heating system wall-plug efficiency
    eta_de=0.85,                  # DEFAULT
    f_sub=0.03,                   # DEFAULT subsystem power fraction
                                  # Cross-check: Schwartz et al. (arXiv:2405.01514) report
                                  # 5% active + 10% passive = 15% total parasitic load.
                                  # f_sub=0.03 captures part of active load only; passive
                                  # (cryogenics, vacuum pumps, tritium handling) encoded
                                  # in p_cryo, p_trit, p_house below. Net derating ≈ 0.85×
                                  # gross. Source: arxiv-2405-01514.md §2.1
    f_dec=0.0,                    # No direct energy conversion — thermal-only BOP.
                                  # Source: dossier §Energy Capture; arc-power-conversion-studies.md

    p_coils=2.0,                  # DEFAULT coil resistive power [MW]; REBCO has low resistive loss
    p_cool=13.7,                  # DEFAULT cooling system power [MW] (FLiBe pumping included)
    p_pump=1.0,                   # DEFAULT
    p_trit=10.0,                  # DEFAULT tritium processing power [MW]
    p_house=4.0,                  # DEFAULT housekeeping power [MW]
    p_cryo=0.5,                   # DEFAULT cryogenic power [MW]; REBCO at 20 K (less than LHe)

    # ── CAS cost overrides ───────────────────────────────────────────────
    cost_overrides=_NOAK_OVERRIDES,
    # All other CAS accounts (CAS21, CAS23, CAS24, CAS25, CAS26, CAS30, CAS40, CAS50)
    # use framework defaults (ARIES-AT analogue calibration). Indirect cost structure:
    # direct costs ~71% of TCC, indirect/owner/supplementary/financial ~29% of TCC.
    # Source: arxiv-2601-21724 §8.2 (FECONS reference design). Implies total plant cost
    # ≈ 1.41× direct cost (nuclear island + BOP), not 2–3× nuclear island alone.
)

# ── Results ───────────────────────────────────────────────────────────────

c  = result.costs
pt = result.power_table

print("HTS Compact Tokamak — CFS ARC (261 MWe, 85% avail, 30 yr, NOAK)")
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
print("-" * 72)

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
print("-" * 72)
total22 = result.cas22_detail.get("C220000", float(c.cas22))
print(f"{'C220000':<12} {'TOTAL':<32} {float(total22):>8.1f}")

# ── FOAK scenario (discrete branch) ──────────────────────────────────────
# FOAK premiums for advanced nuclear / novel manufacturing are NOT a continuous
# sensitivity parameter. They are a step-function cost risk for plants 1–3 in the
# deployment sequence, disappearing after fleet learning.
# CATF IWG methodology (arxiv-2602-19389 §2.1.5): FOAK fusion = 150–200 $/MWh,
# NOAK fusion = 60–100 $/MWh. Approx. 2–3× gap.
# Modeled here as 2× C220103 (REBCO manufacturing learning, quality assurance rework,
# supply chain immaturity) + noak=False (adds 10% contingency per CAS29).
# Source: analysis.md §2 Hypothesis 4; arxiv-2602-19389 §2.1.3, §2.1.5

_FOAK_OVERRIDES = {
    "C220103": round(C220103_OVERRIDE * 2.0, 1),  # 2× NOAK magnet cost — manufacturing immaturity
    "C220101": round(C220101_OVERRIDE, 1),         # Blanket: unchanged (conventional fabrication)
    "C220106": round(C220106_OVERRIDE, 1),         # VV: unchanged (Inconel-718 is mature)
    "CAS27":   CAS27_OVERRIDE,
}

result_foak = model.forward(
    net_electric_mw=261.0,
    availability=0.85,
    lifetime_yr=30,
    n_mod=1,
    construction_time_yr=5.0,
    interest_rate=0.07,
    inflation_rate=0.0245,
    noak=False,                   # FOAK: adds 10% contingency (CAS29); plant_studies_foak
    R0=3.3,
    plasma_t=1.13,
    elon=1.84,
    blanket_t=0.80,
    ht_shield_t=0.20,
    structure_t=0.20,
    vessel_t=0.20,
    p_input=38.6,
    mn=1.1,
    eta_th=0.46,
    eta_p=0.5,
    eta_pin=0.5,
    eta_de=0.85,
    f_sub=0.03,
    f_dec=0.0,
    p_coils=2.0,
    p_cool=13.7,
    p_pump=1.0,
    p_trit=10.0,
    p_house=4.0,
    p_cryo=0.5,
    cost_overrides=_FOAK_OVERRIDES,
)

cf = result_foak.costs
print(f"\nFOAK scenario (2× C220103 + contingency, same availability):")
print(f"  LCOE: {cf.lcoe:.1f} $/MWh | Overnight: {cf.overnight_cost:.0f} $/kW")
print(f"  (CATF IWG FOAK range: 150–200 $/MWh; NOAK range: 60–100 $/MWh)")
print(f"  Source: arxiv-2602-19389 §2.1.5; analysis.md §2 Hypothesis 4")

# ── Key Assumptions ───────────────────────────────────────────────────────

print("""
Key Assumptions
===============
1. Net electric output: 261 MWe — ARC aggressive pilot, supercritical Rankine cycle.
   Source: arc-power-conversion-studies.md §Results, Table 15.
   NOTE: 2025 CFS public target = 400 MWe; updated design not publicly documented. Not modeled.

2. Availability: 85% — canonical per scoring_framework.md §Plant availability
   (MCF steady-state/quasi-steady, D-T); previously 0.75 (discretionary low end of
   Araiinejad & Shirvan 75–90% band — no published 75% target exists for ARC).
   No Tier-A override (externally-published target with stated maintenance basis) applies.
   Naive inverse scaling implies ~1.5× LCOE swing for 50% vs 90% availability — an upper
   bound. Schwartz et al. (2024, arXiv:2405.01514) show grid-value-weighted penalty is up
   to 15% smaller with strategic maintenance scheduling (low-price windows); at 80%
   availability, a plant retains 91% of maintenance-free value (not 80%).
   Source: scoring_framework.md §Plant availability; arxiv-2405-01514.md §2.2 Results

3. Magnet/structure cost (NOAK): ~$6,901 M$ 2024 USD [UNCERTAIN — primary LCOE uncertainty]
   Basis: $5,150 M$ 2014 USD (midpoint of $5.1–5.2B) × CPI 1.34.
   Source: arc-reactor-specifications.md §6.
   REBCO price in 2014: $36–198/m (5.5× spread → $206–1,134 M$ materials alone).
   REBCO price in 2025: ~$20/m (~$100/kA-m) — still ~10× above $10/kA-m commercial target.
   Source: sciencedirect-science-article-pii-s2772830725000390.md §Introduction
   Sensitivity sweep: vary C220103 by ±50% to bracket REBCO price uncertainty.

4. FOAK scenario (discrete scenario branch, NOT a sensitivity parameter):
   C220103 × 2.0 + noak=False → LCOE approximately 2–3× NOAK central estimate.
   Consistent with CATF IWG range: FOAK = 150–200 $/MWh, NOAK = 60–100 $/MWh.
   Source: arxiv-2602-19389 §2.1.5; analysis.md §2 Hypothesis 4.

5. Thermal efficiency: 46% net — supercritical Rankine at 250 bar / 540°C.
   Source: arc-power-conversion-studies.md §3.2, Table 15 (recommended cycle).
   Confirmed by Colliva et al. 2024 as "most promising solution" for ARC.

6. Indirect cost structure: framework defaults encode ~29% of TCC for indirect/owner/
   supplementary/financial costs, with direct costs ~71% of TCC.
   Total plant cost ≈ 1.41× direct cost (nuclear island + BOP) — not 2–3× nuclear island alone.
   Source: arxiv-2601-21724 §8.2 (FECONS/pyFECONS reference design).
   Reference LCOE benchmarks:
     - FECONS illustrative DT tokamak: 55.1 $/MWh at 636.75 MWe, 0.9 availability, 30-yr life
       (arxiv-2601-21724 §8.3 Table 3)
     - ARPA-E ALPHA compact fusion NOAK (non-HTS): 43 $/MWh (~$2.4/W) at ~500 MWe,
       90% availability, 3-yr construction, zero contingency (osti-servlets-purl-1820946.md
       Table 4, COE2); LOWER BOUND for ARC — excludes HTS magnet cost premium entirely.
     - ARIES-AT: ~5 ¢/kWh at ~1,000 MWe (~2000–2003 USD); order-of-magnitude only.

7. FLiBe special materials: $146 M$ (~2025 USD).
   Basis: 950 t FLiBe × $154/kg NOAK (20% learning rate).
   Source: arc-reactor-specifications.md §6 (quantity); Araiinejad & Shirvan 2025 (price).
   NOTE: FLiBe chemistry plant + tritium extraction system capital cost is NOT included.
   iter-7 order-of-magnitude floor: Woodruff Scientific ARPA-E ALPHA re-costing
   (OSTI:1820946) gives CAS22.5 Fuel Processing averaging $124M at ~500 MWe for compact
   MIF/Z-pinch concepts (structural analogue only — different blanket chemistry, no FLiBe).
   Treat $100–200M as a floor for ARC's additive FLiBe chemistry/tritium processing BOP
   line; ARC-specific scope (FLiBe redox control, MHD-driven flow purification) may push
   above this range. Source: analysis.md §6, gap #15; osti-servlets-purl-1820946.md

8. O&M (CAS70): framework default DT O&M scaling.
   Fusion-specific anchor: $60/kWe-yr (FECONS/pyFECONS, arxiv-2601-21724 §6.5)
   → ~$15.7M/yr at 261 MWe. Not ARC-specific; 2–4× below fission-BoP analogue.
   Cross-check: Schwartz et al. (2024) VO&M = $2.07/MWh_net ($1.74/MWh_gross) at ~261 MWe.
   Annual O&M breakdown not published in any ARC/CFS source (analysis.md §6, gap #7).
   Source: arxiv-2601-21724 §6.5; arxiv-2405-01514.md §2.1

9. No direct energy conversion: f_dec = 0.0. ARC uses thermal Rankine cycle only.
   Source: dossier §Energy Capture; arc-power-conversion-studies.md.

10. ARC's $5.56B fabricated component cost reflects NOAK/learning-assumed scaling
    ($1.06M/tonne benchmarked against ARIES/FIRE conceptual designs). FOAK costs for
    the first physical ARC plant would be substantially higher. The inferred
    $/kWe figures ($21,300–29,200/kWe from nuclear island alone) represent the NOAK
    floor, not the first-plant expectation. Source: analysis.md §2 Hypothesis 4;
    arxiv-2602-19389 §2.1.3.

11. Parasitic power split (Schwartz et al. 2024): 5% active (plasma heating, magnets,
    coolant pumps) + 10% passive (cryogenics, vacuum pumps, tritium handling) = 15%
    total. Passive load persists during maintenance outages, raising effective cost of
    downtime. f_sub=0.03 captures part of active load; remaining active/passive load
    encoded in p_cryo, p_trit, p_house, p_cool. Source: arxiv-2405-01514.md §2.1
""")

# ── Sensitivity analysis ──────────────────────────────────────────────────

sens = model.sensitivity(
    result.params,
    cost_overrides=_NOAK_OVERRIDES,
)

print("Sensitivity (elasticity = %LCOE / %param) — NOAK central estimate")
print("-" * 50)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")
