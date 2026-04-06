# STALE: analysis-updated-iter-7
"""MagLIF (D-T) — 1costingfe costing model setup (iter-7).

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Concept: Magnetized Liner Inertial Fusion — pulsed power implosion of magnetized D-T fuel.
Companies: Pacific Fusion (Santa Cruz, CA); Fuse Energy Technologies (San Leandro, CA).
Confinement family: MIF (Magneto-Inertial Fusion).
ConfinementConcept: MAG_TARGET  |  Fuel: DT

=== MODELING APPROACH AND KEY DEVIATIONS ===

This model uses 1costingfe's MAG_TARGET concept as the framework skeleton, but
MagLIF's cost structure is fundamentally different from any MFE concept in the
framework's training data. The analysis.md (§Section 2) explicitly concludes:

  "Reference-class scaling approaches (1costingfe, ARIES-analogous tools, PROCESS)
   are not applicable to MagLIF because the dominant cost categories — pulsed power
   driver capital, per-shot consumables, rep-rated chamber clearing — have no
   analogues in the databases those tools are built on."

Nevertheless, this script provides a structured cost estimate for cross-concept
comparison purposes, using the Z-IFE SAND2006-7148 study as the primary quantitative
source for all overridable cost accounts. All outputs carry very high uncertainty
(±50–100%+ on capital cost; factor-of-several uncertainty on LCOE).

ITER-7 UPDATES vs. ITER-6:
  - Review verdict (iter-4 review, 2026-04-06): PROCEED. Review identified one
    unresolved documentation issue: per-shot consumable O&M (~$15.75M/yr additional
    at $1/shot × 0.5 Hz) was acknowledged in footer notes but not surfaced as a
    concrete line item alongside the reported CAS70 figure. This creates a misleading
    impression that the $132M/yr modeled O&M is complete when it is a material
    undercount. Iter-7 surfaces this gap explicitly with bounding estimates in the
    printed output table, making the omission concrete rather than buried.
  - Added explicit consumable O&M line items: base case ($1/shot), cryo-target pessimistic
    ($10/shot), and the commercial viability threshold ($2/shot maximum) — all printed
    alongside the modeled CAS70 figure for direct comparison.
  - Scenario A and B consumable O&M derived from rep rate (0.5 Hz) and plant scale.

PRIMARY DESIGN POINT: Z-IFE single-chamber, 0.5 Hz scenario (7.0 ¢/kWeh Z-IFE reference).
This is the "optimistic near-term" case: rep rate beyond baseline (0.1 Hz) but short of
the minimum-COE target (1.0–1.8 Hz) described as "beyond reach of RTL."

KEY DEVIATIONS FROM 1costingfe MAG_TARGET DEFAULTS:

  Power balance:
    - eta_th = 0.42 (Combined Brayton-Rankine, steel chamber; vs 0.40 default)
    - eta_pin = 0.60 (LTD driver wall-plug efficiency; vs 0.30 default)
    - p_cryo = 0.0 (no HTS superconducting magnets; pulsed Cu coils only)
    - p_coils = 0.5 (pre-magnetization guide field; minimal per self-magnetizing target path)
    - p_target = 5.0 (frozen-FLiBe RTL factory; eliminates 170 MWe steel RTL load)

  CAS22 overrides (reactor plant equipment):
    - C220103 = $5M   — Cu pre-magnetization coils (vs HTS ~$100M+ default)
    - C220104 = $372M — pulsed power LTD driver (Z-IFE median; novel cost category)
    - C220109 = $0    — no direct energy conversion (D-T uses thermal cycle, not DEC)

  Geometry:
    - plasma_t = 4.0 m (Z-IFE 4 m radius spherical chamber)
    - blanket_t = 0.80 m (FLiBe thick liquid wall, Z-IFE baseline)
    - R0 = 0.0 (spherical chamber, no toroidal major radius)

  Unchanged from defaults:
    - C220101 (Blanket/FW): FLiBe thick liquid wall; volume-based default used as
      placeholder — FLiBe handling systems may offset absence of solid breeding assembly.
    - C220108 (Target/RTL Factory): $244M at 1 GWe default — Z-IFE costed separately
      but gave no sub-account breakdown comparable to 1costingfe's target_factory_base.
      UNCERTAIN: cryo target production at scale could cost dramatically more.
    - CAS21 (Buildings): DT default; pulsed power halls offset cryogenics building removal.
    - CAS70 (O&M): DT default (~$52M/yr at 1 GWe) — does NOT capture per-shot consumable
      O&M. See "CONSUMABLE O&M (NOT IN MODEL)" section below for explicit bounding estimates.

SOURCES:
  [Z-IFE] Olson et al. SAND2006-7148, "Z-Inertial Fusion Energy Power Plant Final
          Report," 2006. The only published plant-level systems code for MagLIF class.
          iter-02/sources/z-ife-sand2006-7148-thermal-cycles.md
  [PMF]   Ellison et al. arXiv:2408.15206, "Opportunities in Pulsed Magnetic Fusion
          Energy," 2025. Multi-institutional roadmap including Pacific Fusion/Sandia.
          iter-01/sources/arxiv-2408-15206-pulsed-magnetic-fusion.md
  [PF]    Pacific Fusion / The Fusion Report interview (DS architecture specs).
          iter-02/sources/pacific-fusion-interview-fusion-report.md
  [ANS]   ANS News, April 24, 2025 — Pacific Fusion CTO Keith LeChien quotes.
          iter-04/sources/ans-news-2025-04-24-article-6980-pacific-fusion-fusing.md
  [GA]    GlobeNewswire, April 24, 2025 — Pacific Fusion + General Atomics partnership.
          iter-04/sources/globenewswire-news-release-2025-04-24-3067836-0-en-pacific.md
  [2504]  Schmit et al. arXiv:2504.10680, April 2025 — multi-dimensional simulations
          benchmarked against Z facility data confirming 50–60 MA → net facility gain.
          iter-03/sources/arxiv-2504-10680.md
"""

from costingfe import ConfinementConcept, CostModel, Fuel

model = CostModel(concept=ConfinementConcept.MAG_TARGET, fuel=Fuel.DT)

# ── Consumable O&M parameters (NOT in 1costingfe model; computed separately) ──
# Source: analysis.md §2 Challenge 2 and §5 (RTL unit cost row)
REP_RATE_HZ = 0.5            # Z-IFE baseline 0.5 Hz frozen-FLiBe RTL [Z-IFE §3.1.1.5]
SECS_PER_YEAR = 3.156e7      # seconds per year
SHOTS_PER_YEAR = REP_RATE_HZ * SECS_PER_YEAR  # ~15.75M shots/yr at 0.5 Hz

# RTL/target cost scenarios [M$/yr]:
# Historical steel RTL estimate: ~$0.70/shot [Z-IFE era, analysis.md §5]
#   → $0.70 × 15.75M shots = ~$11.0M/yr  [optimistic; predates cryo target requirement]
# Base case $1/shot: commercial viability analysis threshold cited in analysis.md §2
#   → $1.00 × 15.75M shots = ~$15.75M/yr
# Pessimistic: $10/shot cryo target (analysis.md §2 Challenge 2 "TEA consequence of failure")
#   → $10.00 × 15.75M shots = ~$157.5M/yr
# Commercial viability threshold: <$2/shot (analysis.md §2)
#   → $2.00 × 15.75M shots = ~$31.5M/yr (maximum viable)
CONSUMABLE_OM_HISTORICAL_M_PER_YR = 0.70 * SHOTS_PER_YEAR / 1e6   # ~11.0 M$/yr
CONSUMABLE_OM_BASE_M_PER_YR = 1.00 * SHOTS_PER_YEAR / 1e6         # ~15.75 M$/yr
CONSUMABLE_OM_MAX_VIABLE_M_PER_YR = 2.00 * SHOTS_PER_YEAR / 1e6   # ~31.5 M$/yr
CONSUMABLE_OM_PESSIMISTIC_M_PER_YR = 10.00 * SHOTS_PER_YEAR / 1e6 # ~157.5 M$/yr

# ── Shared engineering parameters ────────────────────────────────────────────
# All parameters shared across both scenarios. Design point: Z-IFE single-chamber,
# ~0.5 Hz, frozen-FLiBe RTL, thick liquid FLiBe wall.
# Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1 (reference plant).

SHARED_KWARGS = dict(
    n_mod=1,                  # Single chamber — Z-IFE single-chamber baseline [Z-IFE §3.1.1.6]
    construction_time_yr=5.0, # UNCERTAIN: 4–6 yr; no factory-build modular path yet
    interest_rate=0.07,       # DEFAULT: standard fusion finance rate
    inflation_rate=0.02,      # DEFAULT
    noak=True,                # Assuming volume-production driver hardware at commercial scale

    # ── Power balance ──────────────────────────────────────────────────────
    # Z-IFE 0.5 Hz scenario: ~5 GJ/shot fusion yield, ~50 MJ driver energy/shot.
    # Time-averaged driver output: 50 MJ × 0.5 Hz = 25 MW average delivered to target.
    p_driver=25.0,    # Time-averaged pulsed power delivered to target [MW]
                      # UNCERTAIN: derived from yield/gain estimates; Z-IFE scenario-specific.
                      # Source: analysis.md §5, inferred from COE=7.0 ¢/kWeh at 0.5 Hz

    mn=1.1,           # Neutron energy multiplier — FLiBe blanket (Be-9 → 2n reactions)
                      # DEFAULT: same as standard DT blanket
                      # Source: analysis.md §5 / standard DT blanket assumption

    eta_th=0.42,      # Thermal conversion efficiency — Combined Brayton-Rankine, steel chamber
                      # Source: z-ife-sand2006-7148-thermal-cycles.md §3.2
                      # "Combined Brayton-Rankine achieves ~42% efficiency with current steel"
                      # NOTE: 50% possible with C-C composite chamber [Z-IFE §3.2] but
                      # requires high-temperature materials not commercially available;
                      # analysis.md §3 (Energy Conversion TRL 6-7, gap #10).

    eta_p=0.50,       # DEFAULT: pumping efficiency

    eta_pin=0.60,     # Pulsed power wall-plug efficiency — LTD driver architecture
                      # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5
                      # "2005 workshop LTD efficiency estimate: 60%"
                      # NOTE: IMG claims ~90% wall-plug [PMF §3.2] — not verified at plant scale.
                      # Using LTD figure as conservative anchor.
                      # analysis.md §5 (Driver efficiency row, confidence: medium)

    f_sub=0.03,       # DEFAULT: subsystem power fraction
    f_dec=0.0,        # No direct energy conversion — D-T uses thermal cycle, not DEC
                      # Source: analysis.md §Section 2 (CAS account cost structure table)

    # Parasitic loads
    p_coils=0.5,      # Pre-magnetization coil average power [MW]
                      # Small: Pacific Fusion Oct 2025 self-magnetizing target demonstration
                      # showed external Helmholtz coils can be eliminated entirely.
                      # Source: analysis.md §3 (Target Physics TRL 3-4, self-magnetizing milestone)
                      # UNCERTAIN: near-zero if self-magnetizing path scales; up to a few MW
                      # if conventional external coils retained at commercial scale.

    p_pump=2.0,       # FLiBe primary loop pumping [MW]
                      # Slightly elevated vs. default (1.0 MW) — FLiBe is a viscous,
                      # high-density molten salt at 733–850 K requiring larger pumps.
                      # Source: analysis.md §3 (Energy Conversion / BOP TRL 6-7)

    p_trit=10.0,      # DEFAULT: tritium processing power [MW]
                      # Standard D-T tritium processing plant.
                      # Source: analysis.md §4 (D-T fuel cycle — shared with all D-T concepts)

    p_house=4.0,      # DEFAULT: housekeeping power [MW]

    p_cryo=0.0,       # No cryogenic power — no HTS superconducting magnets.
                      # MagLIF uses pulsed copper coils (or none, self-magnetizing).
                      # Key supply-chain advantage vs. all tokamak/stellarator concepts.
                      # Source: analysis.md §Key Differentiators (No superconducting magnets)

    p_target=5.0,     # RTL/liner factory parasitic electrical load [MW]
                      # Z-IFE steel RTL remanufacturing consumed 170 MWe (17% of gross) —
                      # forcing adoption of frozen-FLiBe RTL as base case to eliminate load.
                      # Frozen-FLiBe RTL residual: cryo-cooling + automated fabrication.
                      # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.3
                      # UNCERTAIN: no published estimate for frozen-FLiBe RTL factory load.

    # ── Geometry — Z-IFE spherical chamber ────────────────────────────────
    # Source: z-ife-power-plant-concept.md §Abstract (SAND2000-3132J) and
    #         z-ife-sand2006-7148-thermal-cycles.md §3.1.1 (chamber dimensions)
    R0=0.0,            # No toroidal major radius — spherical chamber geometry
    plasma_t=4.0,      # Chamber inner radius [m] — "4 m radius chamber" [Z-IFE §Abstract]
    blanket_t=0.80,    # FLiBe thick liquid wall thickness [m] — "80 cm FLiBe" [Z-IFE §Abstract]
    ht_shield_t=0.20,  # High-temperature shield [m] — DEFAULT order of magnitude
    structure_t=0.15,  # Primary structure [m] — DEFAULT
    vessel_t=0.10,     # Vacuum/pressure vessel [m] — DEFAULT

    # ── Cost overrides — CAS22 reactor plant equipment ─────────────────────
    cost_overrides={
        # C220103: Pre-magnetization coils — conventional copper pulsed coils, not superconducting.
        # MagLIF requires only a modest axial pre-magnetization B-field (~10 T),
        # delivered by conventional copper coils. With Pacific Fusion's self-magnetizing
        # composite targets (Oct 2025 demonstration at 22 MA on Z), even these may be
        # eliminated entirely by embedding field penetration into target geometry.
        # Compare: HTS superconducting coil default in framework >> $100M.
        # Source: analysis.md §Key Differentiators (No superconducting magnets) and
        #         analysis.md §3 (Target Physics TRL 3-4, self-magnetizing milestone)
        "C220103": 5.0,   # Cu pre-magnetization coils [M$] — UNCERTAIN: $2–20M range

        # C220104: Pulsed power driver — the dominant novel capital cost item.
        # In MagLIF, the pulsed power driver performs the function of heating/current-drive
        # systems in a tokamak: it compresses, heats, and implodes the fuel target.
        # Z-IFE bottom-up cost model: $372M median ($862M 95th pctile) for 1 PW LTD driver.
        #   12,600 LTD cavities at ~$28k each = ~$353M (96% of driver cost).
        # Modern IMG (Imploding Metal Geometry) architecture claimed to be 5–10× cheaper
        # per joule [PMF §3.2.4] — but no plant-scale cost estimate published for IMG.
        # Using LTD Z-IFE reference as CONSERVATIVE upper bound; IMG goal: <$0.50/J.
        # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.2
        #   "Driver cost $372M median; LTD cavities 96% of total driver cost"
        # UNCERTAIN: ±100%; IMG may be 2–5× lower if component cost targets met per [PMF §3.2.4]
        "C220104": 372.0,  # Pulsed power driver [M$] — LTD Z-IFE median estimate

        # C220109: Direct Energy Conversion — not applicable for D-T MagLIF.
        # D-T fusion energy is captured as heat in the FLiBe blanket and converted
        # via Brayton-Rankine thermal cycle. DEC is relevant for D-He3 and aneutronic
        # fuel cycles only.
        "C220109": 0.0,   # No DEC [M$]
    },
    # NOTE — accounts left at framework defaults with rationale:
    #
    # C220101 (Blanket/FW): FLiBe thick liquid wall. Framework uses volume-based solid
    #   blanket unit costs, which likely OVERestimates FLiBe capital (no structured solid
    #   breeding assembly required). However, FLiBe handling systems and freeze/thaw
    #   infrastructure for the frozen RTL concept may partially offset savings.
    #   Kept at default as order-of-magnitude placeholder.
    #
    # C220108 (Target/RTL Factory): RTL + liner fabrication facility.
    #   Z-IFE treated as a separate direct capital account; no sub-account cost breakdown
    #   was published comparable to 1costingfe's target_factory_base ($244M at 1 GWe).
    #   Used as placeholder. UNCERTAIN: cryo ice-layer target production at 0.5 Hz could
    #   cost dramatically more; self-magnetizing non-cryo targets (if gain is sufficient)
    #   could cost less. GA partnership (April 2025) provides organizational path to
    #   address cryogenics/target fabrication but no published cost data yet.
    #   Source for GA context: analysis.md §3 (Target Fabrication at Scale) [GA ref]
    #
    # CAS21 (Buildings): Pulsed power capacitor bank halls are large (Pacific Fusion DS:
    #   73m × 80m for the experimental machine), partially offset by elimination of
    #   cryogenics buildings (no HTS magnets). Net change vs. DT tokamak baseline unclear;
    #   left at DT default (~$800M at 1 GWe).
    #
    # CAS70 (O&M): Framework DT baseline (~$52M/yr at 1 GWe). MagLIF's per-shot
    #   consumable O&M is NOT captured — a material omission. The "CONSUMABLE O&M"
    #   section below surfaces this gap with explicit bounding estimates.
    #   Source: analysis.md §5 (RTL unit cost ~$0.70/shot historical steel estimate)
    #   UNCERTAIN: cryo ice-layer targets could be $10–10,000+/shot currently; no
    #   demonstrated path to sub-$2/shot — the commercial viability threshold.
)

# ── Scenario A: 1000 MWe (Z-IFE single-chamber reference) ────────────────────
# Used for cross-concept benchmarking. Matches Z-IFE reference plant scale.
# Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1 (reference plant, 1000 MWe)
result_a = model.forward(
    net_electric_mw=1000.0,    # 1 GWe — Z-IFE single-chamber reference plant [Z-IFE §3.1.1]
    availability=0.85,         # UNCERTAIN: Z-IFE assumption for thick-liquid-wall success
                                # scenario; 85–90% success vs. 60–75% failure.
                                # Source: analysis.md §5 (capacity factor rows)
    lifetime_yr=30,             # DEFAULT: standard fusion plant lifetime
    **SHARED_KWARGS,
)

# ── Scenario B: 250 MWe (Pacific Fusion commercial design point) ──────────────
# Pacific Fusion CTO LeChien (April 2025) stated 250 MWe target with ≤25 acres.
# This is 4× smaller than the Z-IFE reference. Z-IFE economy-of-scale data:
# 1000 MWe 0.5 Hz → 7.0 ¢/kWeh; 2000 MWe → 5.7 ¢/kWeh; 500 MWe → >10 ¢/kWeh.
# Source: ans-news-2025-04-24-article-6980-pacific-fusion-fusing.md §Combined power
#   "One attractive combination would let us produce about 250 net MWe with a very
#    compact footprint of 25 acres or less" — Keith LeChien, Pacific Fusion CTO
# analysis.md §2 Scale note: "All COE figures should be treated as lower bounds
#   for Pacific Fusion's commercial design point."
result_b = model.forward(
    net_electric_mw=250.0,     # 250 MWe — Pacific Fusion commercial target [ANS April 2025]
    availability=0.85,         # Same availability assumption as Scenario A (UNCERTAIN)
    lifetime_yr=30,
    **SHARED_KWARGS,
)

# ── Results — Scenario A (1000 MWe, Z-IFE reference) ─────────────────────────
c_a = result_a.costs
pt_a = result_a.power_table
lcoe_ckwh_a = float(c_a.lcoe) / 10

print("=" * 65)
print("MagLIF (D-T) — Pacific Fusion / Fuse Energy Technologies")
print("=" * 65)
print()
print("SCENARIO A: 1000 MWe — Z-IFE single-chamber reference plant")
print("  Driver: LTD pulsed power ($372M) | eta_pin=60% | eta_th=42%")
print()
print(f"  LCOE:        {c_a.lcoe:.1f} $/MWh  ({lcoe_ckwh_a:.2f} c/kWh)")
print(f"  Overnight:   {c_a.overnight_cost:.0f} $/kW")
print(f"  Fusion pwr:  {pt_a.p_fus:.0f} MW  |  Net: {pt_a.p_net:.0f} MW")
print(f"  Q_eng:       {pt_a.q_eng:.2f}  |  Q_sci: {pt_a.q_sci:.1f}")
print(f"  Recirc frac: {pt_a.rec_frac:.1%}")

# ── Results — Scenario B (250 MWe, PF commercial design point) ───────────────
c_b = result_b.costs
pt_b = result_b.power_table
lcoe_ckwh_b = float(c_b.lcoe) / 10

print()
print("SCENARIO B: 250 MWe — Pacific Fusion commercial design point")
print("  Same engineering parameters; 4× smaller plant vs. Z-IFE reference.")
print("  Z-IFE shows economy-of-scale penalty below 1000 MWe (scale law on capital).")
print()
print(f"  LCOE:        {c_b.lcoe:.1f} $/MWh  ({lcoe_ckwh_b:.2f} c/kWh)")
print(f"  Overnight:   {c_b.overnight_cost:.0f} $/kW")
print(f"  Fusion pwr:  {pt_b.p_fus:.0f} MW  |  Net: {pt_b.p_net:.0f} MW")
print(f"  Q_eng:       {pt_b.q_eng:.2f}  |  Q_sci: {pt_b.q_sci:.1f}")
print(f"  Recirc frac: {pt_b.rec_frac:.1%}")
print()
lcoe_penalty_pct = (float(c_b.lcoe) - float(c_a.lcoe)) / float(c_a.lcoe) * 100
print(f"  Scale penalty vs. 1000 MWe: {lcoe_penalty_pct:+.1f}% LCOE")
print()

# ── Z-IFE reference COE comparisons ──────────────────────────────────────────
print("Z-IFE published COE reference points (LTD architecture):")
print("  10-chamber, 0.1 Hz: ~20.0 c/kWh  [Z-IFE §3.1.1.6]  ← baseline (RTL-limited)")
print("  1-chamber,  0.5 Hz:  ~7.0 c/kWh  [Z-IFE §3.1.1.6]  ← Scenario A design point")
print("  2-chamber, 2000 MWe:  ~5.7 c/kWh [Z-IFE §3.1.1.6]  ← scale economy case")
print("  Advanced fission:    4–6 c/kWh   [Z-IFE §3.1.1.6]  ← competitive threshold")
print()

# ── CAS breakdown — Scenario A ───────────────────────────────────────────────
cas_accounts = [
    ("CAS10", "Preconstruction"),
    ("CAS21", "Buildings"),
    ("CAS22", "Reactor Plant Equipment"),
    ("CAS23", "Turbine Plant"),
    ("CAS24", "Electrical Plant"),
    ("CAS25", "Miscellaneous"),
    ("CAS26", "Heat Rejection"),
    ("CAS27", "Special Materials"),
    ("CAS28", "Digital Twin"),
    ("CAS29", "Contingency"),
    ("CAS30", "Indirect Costs"),
    ("CAS40", "Owner's Costs"),
    ("CAS50", "Supplementary"),
    ("CAS60", "IDC"),
    ("CAS70", "O&M (annualized)"),
    ("CAS80", "Fuel (annualized)"),
    ("CAS90", "Financial"),
]

print("CAS BREAKDOWN — Scenario A (1000 MWe):")
print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name in cas_accounts:
    val = getattr(c_a, code.lower(), None)
    if val is not None:
        print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c_a.total_capital):>10.1f}")

# ── CONSUMABLE O&M (NOT IN MODEL) ────────────────────────────────────────────
# ITER-7 ADDITION: Surface per-shot consumable O&M as concrete line items.
# The modeled CAS70 (~$132M/yr) is a material undercount because per-shot
# target/RTL destruction costs are not captured by the framework.
# Source: analysis.md §2 Challenge 2; §5 (RTL unit cost); review.md §1 (iter-4 review)
print()
print("CONSUMABLE O&M (PER-SHOT, NOT CAPTURED IN CAS70):")
print(f"  Rep rate:                          {REP_RATE_HZ:.1f} Hz [Z-IFE §3.1.1.5]")
print(f"  Shots per year at {REP_RATE_HZ:.1f} Hz:         {SHOTS_PER_YEAR / 1e6:.2f}M shots/yr")
print()
print(f"  {'Scenario':<36} {'M$/yr':>8}  {'% of CAS70':>10}")
print("  " + "-" * 58)
cas70_a = float(c_a.cas70)
print(f"  {'CAS70 (modeled O&M, Scenario A)':<36} {cas70_a:>8.1f}  {'100% baseline':>10}")
print(f"  {'Add: hist. steel RTL (~$0.70/shot)':<36} {CONSUMABLE_OM_HISTORICAL_M_PER_YR:>8.1f}  {CONSUMABLE_OM_HISTORICAL_M_PER_YR / cas70_a * 100:>9.1f}%")
print(f"  {'Add: base case ($1.00/shot)':<36} {CONSUMABLE_OM_BASE_M_PER_YR:>8.1f}  {CONSUMABLE_OM_BASE_M_PER_YR / cas70_a * 100:>9.1f}%")
print(f"  {'Commercial viability max ($2.00/shot)':<36} {CONSUMABLE_OM_MAX_VIABLE_M_PER_YR:>8.1f}  {CONSUMABLE_OM_MAX_VIABLE_M_PER_YR / cas70_a * 100:>9.1f}%")
print(f"  {'Pessimistic cryo ($10.00/shot)':<36} {CONSUMABLE_OM_PESSIMISTIC_M_PER_YR:>8.1f}  {CONSUMABLE_OM_PESSIMISTIC_M_PER_YR / cas70_a * 100:>9.1f}%")
print()
print(f"  CAS70 + base consumable (true O&M lower bound): {cas70_a + CONSUMABLE_OM_BASE_M_PER_YR:.1f} M$/yr")
print(f"  CAS70 + cryo pessimistic (O&M upper bound):     {cas70_a + CONSUMABLE_OM_PESSIMISTIC_M_PER_YR:.1f} M$/yr")
print()
print("  *** IMPORTANT: If cryo target cost cannot reach <$2/shot, annual O&M at 1 Hz")
print("  *** exceeds $300M/yr at 1 Hz — comparable to annual capital amortization on")
print("  *** the driver, making O&M the binding LCOE constraint. Commercial viability")
print("  *** threshold: <$2/shot [analysis.md §2 Challenge 2].")

# ── CAS22 sub-account detail ──────────────────────────────────────────────────
print("\nCAS22 Reactor Plant Equipment breakdown (Scenario A, 1000 MWe):")
print("-" * 60)
cas22_items = [
    ("C220101", "First Wall / FLiBe Blanket"),
    ("C220102", "Shield"),
    ("C220103", "Pre-magnetization Coils (Cu)"),
    ("C220104", "Pulsed Power Driver (LTD)"),
    ("C220105", "Primary Structure"),
    ("C220106", "Vacuum System"),
    ("C220107", "Power Supplies (aux)"),
    ("C220108", "RTL + Target Factory"),
    ("C220109", "Direct Energy Converter"),
    ("C220110", "Remote Handling"),
    ("C220111", "Installation"),
    ("C220112", "Isotope Separation"),
    ("C220200", "Coolant Systems (FLiBe)"),
    ("C220300", "Aux Cooling / Cryo"),
    ("C220400", "Rad Waste"),
    ("C220500", "Fuel Handling (DT)"),
    ("C220600", "Other Equipment"),
    ("C220700", "I&C"),
]
for key, label in cas22_items:
    v = float(result_a.cas22_detail.get(key, 0.0))
    if v > 0.01:
        override_flag = " [OVERRIDE]" if key in result_a.overridden else ""
        print(f"  {key}  {label:<32} {v:>8.1f} M${override_flag}")
print(f"\n  {'':7} {'CAS22 Total':<32} {float(c_a.cas22):>8.1f} M$")
print(f"\nOverridden accounts: {', '.join(result_a.overridden)}")

# ── Key Assumptions Summary ───────────────────────────────────────────────────
print()
print("=" * 65)
print("KEY ASSUMPTIONS")
print("=" * 65)
print(f"  Scenario A / B net electric:  1000 / 250 MWe")
print(f"  Availability:                 85%   (UNCERTAIN: thick-LW success scenario)")
print(f"  Lifetime:                     30 yr")
print(f"  Thermal efficiency:           42%   (Brayton-Rankine, steel chamber)")
print(f"    [Z-IFE §3.2; 50% possible with C-C composite, unavailable commercially]")
print(f"  Driver wall-plug efficiency:  60%   (LTD; IMG claims 90%, unverified)")
print(f"    [Z-IFE §3.1.1.5; analysis.md §5; IMG claim: PMF §3.2]")
print(f"  Driver capital:               $372M (LTD Z-IFE median; IMG may be 5–10× lower)")
print(f"    [Z-IFE §3.1.2; 12,600 LTD cavities at ~$28k each = 96% of driver cost]")
print(f"  Rep rate (implied):           ~0.5 Hz (Z-IFE optimized frozen-FLiBe RTL case)")
print(f"    [Z-IFE §3.1.1.5; 1.0–1.8 Hz minimum-COE rate 'beyond reach of RTL']")
print(f"  No superconducting magnets    (HTS/Nb3Sn fully eliminated; $5M Cu coils only)")
print(f"  Thick liquid FLiBe wall       (scheduled FW replacement eliminated IF demonstrated)")
print(f"  Frozen-FLiBe RTL              (eliminates 170 MWe steel RTL remanufacturing load)")
print(f"  Gain basis:                   Multi-dim. simulations anchored to Z data")
print(f"    [arXiv:2504.10680: 50–60 MA → net facility gain; ignition undemonstrated on Z]")
print()
print("CRITICAL UNCERTAINTIES NOT CAPTURED IN THIS ESTIMATE:")
print("  1. Rep rate achievement: COE scales ~10:1 with rep rate")
print("     (0.1 Hz → ~20 c/kWh; 1.0 Hz → ~5 c/kWh at 1 GWe per Z-IFE)")
print("  2. Per-shot consumable O&M: target cost must reach <$2/shot")
print("     (see CONSUMABLE O&M table above for explicit bounding estimates)")
print("     ($0.70/shot historical steel RTL; cryo ice-layer targets orders-of-magnitude higher)")
print("  3. Gain scaling unvalidated: χ ≈ 0.1 on Z; GJ-class yields undemonstrated")
print("     (simulation-anchored at 50–60 MA per arXiv:2504.10680; not experimentally tested)")
print("  4. IMG driver capital: may be 2–5× lower than $372M LTD reference")
print("     (PMF §3.2.4: must decrease 5–10× from $5/J current commercial pricing)")
print("  5. Chamber lifetime under GJ-scale repetitive shots: untested environment")
print("  6. 250 MWe commercial target (Scenario B) faces economy-of-scale penalty")
print("     vs. 1000 MWe Z-IFE reference — all published COE figures are lower")
print("     bounds for Pacific Fusion's actual commercial design point.")
print("     Source: ans-news-2025-04-24-article-6980-pacific-fusion-fusing.md")
print()
print("  See analysis.md §Section 2 and §Section 6 for full gap inventory.")

# ── Sensitivity Analysis ──────────────────────────────────────────────────────
sens = model.sensitivity(result_a.params)

print()
print("=" * 65)
print("SENSITIVITY — Scenario A (elasticity = %LCOE / %param)")
print("=" * 65)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<32} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<32} {v:+.4f}")

print()
print("NOTE: The sensitivity table above reflects standard 1costingfe gradients")
print("and does NOT capture the dominant MagLIF LCOE drivers:")
print("  - Rep rate (no framework parameter; must be swept as p_driver × scale factor)")
print("  - Per-shot target/RTL cost (not parameterized in CAS70 or C220108)")
print("    → See CONSUMABLE O&M table above for the explicit gap quantification")
print("  - Driver capital uncertainty (C220104 overridden; gradient = 0 by construction)")
print("  - Plant scale (Scenario A vs. B shows this directly in the output above)")
print()
print("For MagLIF, the four dominant LCOE levers identified in analysis.md §2 are:")
print("  1. Rep rate (Hz)       — C220104 capital amortized per MWh")
print("  2. Target $/shot       — variable O&M floor (quantified above; not in framework)")
print("  3. Driver $/J capital  — C220104 sensitivity to IMG vs. LTD architecture")
print("  4. Plant scale (MWe)   — economy-of-scale; 250 MWe raises LCOE vs. 1 GWe")
