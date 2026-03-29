# STALE: analysis-updated-by-source-integration-20260329T153422
"""
Laser ICF — Hybrid Direct Drive, D-T (Xcimer Energy / Athena pilot)
=====================================================================

Modeling approach
-----------------
Uses the 1costingfe LASER_IFE / DT framework for BOP, target factory, tritium,
and structural accounts.  The laser driver capital — which dominates (~60–80 %)
of direct cost — is injected via a C220104 cost override derived bottom-up from
the Xcimer-TRUMPF Feb 2026 $/J estimates (accessed via reference artifact
26-laser-icf-indirect-drive.md; not yet directly extracted — gap #7).

Framework accounts used without override (trusting framework defaults):
  * Target factory capital / O&M (target_factory_base, built-in IFE scaling)
  * Tritium breeding / supply chain (CAS27, CAS80, CAS50 startup fuel)
  * BOP turbine plant (CAS23–26) under both thermal cycle scenarios
  * Buildings, indirect costs, IDC (CAS21, CAS30, CAS60)

Framework limitations / manual overrides for this concept
----------------------------------------------------------
  1. Laser driver capital (C220104) — overridden with $/J × driver energy.
     Framework default heating-system scaling calibrated to generic IFE, not
     specifically to a KrF excimer ASPEN architecture.
  2. Magnets (C220103) — overridden to 0.0; IFE has no superconducting coils.
  3. Divertor (C220108) — overridden to 0.0; liquid FLiBe wet wall eliminates
     the plasma-facing component account entirely.
  4. FLiBe primary loop (C220200 / CAS27) — DEFAULT: HYLIFE-II FLiBe inventory
     at Xcimer pilot scale is unknown (gap #9 in analysis.md §S6).
  5. Thermal cycle — run as two scenarios: He Brayton (45 %, HYLIFE-II heritage)
     and Steam Rankine (33 %, Xcimer Science page).  Ambiguity documented in
     analysis.md §H-3; pending direct extraction of Xcimer-TRUMPF whitepaper.
  6. Target factory O&M cost per shot — not modeled as a CAS override; the
     H-4 threshold analysis below quantifies the LCOE contribution at three
     cost-per-target points.  Framework target_factory_base covers capital.

Key hypotheses tested
---------------------
  H-1: Laser efficiency × cost breakeven (driven by sensitivity on eta_pin1)
  H-3: Thermal cycle gap (He Brayton 45 % vs Steam Rankine 33 %)
  H-4: Target fabrication cost threshold ($1 / $5 / $10 per target)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Create model ─────────────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# ════════════════════════════════════════════════════════════════════════════
# Plant configuration constants
# ════════════════════════════════════════════════════════════════════════════

# Net electric output — Xcimer "Athena" pilot plant target
# UNCERTAIN: 400 MWe figure from Xcimer-TRUMPF whitepaper Feb 2026 (gap #7)
# Source: 26-laser-icf-indirect-drive.md §Comparison Table (citing whitepaper)
#         analysis.md §Section 5 Table, "Net electrical output (pilot)"
NET_ELECTRIC_MW = 400.0

# Availability (capacity factor) — no public maintenance schedule data
# Upper scenario: 0.85 (Xcimer claims 30-yr chamber life, no PFC replacement)
# Lower scenario: 0.70 (conservative, pulsed-power maintenance analogue)
# Source: analysis.md §Section 2, Challenge 6 — "CF = 0.70 vs. 0.85 bounding scenarios"
# UNCERTAIN: blocking gap — no e-beam diode lifetime or Marx capacitor data published
AVAILABILITY = 0.85  # upper scenario; rerun with 0.70 for conservative bound

# Plant lifetime — 30-year structural chamber lifetime
# Source: analysis.md §Section 5 Table, "Chamber lifetime claim: 30 years"
#         dossier.md §Neutron Management; xcimer-energy-approach.md
# Medium confidence: based on HYLIFE-III 2024 nuclear analysis (paper not extracted)
LIFETIME_YR = 30

# ── Laser driver configuration ────────────────────────────────────────────────

# Laser energy per pulse: ~10+ MJ (KrF excimer ASPEN)
# Source: xcimer-energy-approach.md §Driver
#         xcimer-science-page.md §Laser Energy; analysis.md §S5 Table — high confidence
LASER_ENERGY_MJ = 10.0  # MJ per pulse

# Rep rate: sub-Hz, "every couple seconds" → 0.25–0.5 Hz central estimate
# Source: xcimer-energy-approach.md §Rep Rate; xcimer-science-page.md §Rep Rate
#         analysis.md §S5 Table: "0.25–1 Hz (<1 Hz)" — high confidence
# UNCERTAIN: exact rep rate not disclosed; 0.5 Hz used as nominal
REP_RATE_HZ = 0.5  # Hz

# Average laser output power fed to framework (MW)
# = laser energy per pulse × rep rate
P_IMPLOSION_MW = LASER_ENERGY_MJ * REP_RATE_HZ  # 5 MW average at 0.5 Hz

# Laser wall-plug efficiency (eta_pin1)
# Target: ~10% (Xcimer ASPEN design goal)
# Source: xcimer-science-page.md §Laser Efficiency — "10% target"
# Demonstrated (Phoenix, kJ-scale, June 2025): ~5–7%
# Source: analysis.md §S5 Table; 26-laser-icf-indirect-drive.md §Comparison Table
# UNCERTAIN: Phoenix milestone reached but efficiency not publicly disclosed;
#            10% target undemonstrated at 10 MJ ASPEN scale
ETA_PIN1 = 0.07  # UNCERTAIN: conservative (demonstrated KrF wall-plug efficiency)
                 # Xcimer target is 0.10; see sensitivity analysis for η_laser sweep

# ── Thermal cycle ─────────────────────────────────────────────────────────────

# SCENARIO BRANCH — analysis.md §H-3 (blocking ambiguity until gap #1 is closed)
# He Brayton: HYLIFE-II heritage, 940 MWe / 2.1 GW thermal = 44.8 %
#   Source: hylife-energy-conversion-notes.orig.md §HYLIFE-II
#           HYLIFE-II Final Report 1994, Fusion Technology 15:25–70 (gap #4)
ETA_TH_BRAYTON = 0.45  # He Brayton — HYLIFE-II reference; high confidence for heritage

# Steam Rankine: implied by Xcimer Science page ("steam which drives turbines")
#   Source: xcimer-science-page.md §Energy Conversion
#   UNCERTAIN: may be simplified marketing language; steam ~33 % is nominal
ETA_TH_STEAM = 0.33  # UNCERTAIN: Steam Rankine; Xcimer Science page

# ── Laser capital cost (C220104 override) ────────────────────────────────────

# Laser system capital: bottom-up from ($/J) × (driver energy in joules)
# NOAK: $60–80/J (midpoint $70/J)  →  $70/J × 10 MJ = $700 M$
# FOAK: $100–120/J (midpoint $110/J) → $110/J × 10 MJ = $1,100 M$
# Source: 26-laser-icf-indirect-drive.md §Comparison Table
#   (data attributed to Xcimer-TRUMPF whitepaper Feb 2026 — gap #7, NOT directly extracted;
#    verify against xcimer.energy/wp-content/uploads/2026/02/XEC-20260224-... before
#    treating these figures as confirmed)
# Note: "system" cost ($60–120/J) vs. "on-target" cost ($20–30/J from ASPEN 2022 PDF,
#    gap #6) — this model uses system cost per analysis.md §S2 Challenge 1
# UNCERTAIN: full range spans factor of 2 (FOAK) or 1.33 (NOAK); propagates directly to LCOE
LASER_NOAK_PER_J = 70.0   # $/J; UNCERTAIN: midpoint of $60–80/J NOAK range
LASER_FOAK_PER_J = 110.0  # $/J; UNCERTAIN: midpoint of $100–120/J FOAK range

# M$ = $/J × MJ (unit identity: $/J × 10^6 J / 10^6 $/M$ = $/J × MJ = M$)
LASER_NOAK_MS = LASER_NOAK_PER_J * LASER_ENERGY_MJ   # 700 M$
LASER_FOAK_MS = LASER_FOAK_PER_J * LASER_ENERGY_MJ   # 1100 M$

# ── Cost overrides ────────────────────────────────────────────────────────────

OVERRIDES_NOAK_BRAYTON = {
    # Laser driver capital — C220104 (heating / driver system account)
    # NOAK $70/J × 10 MJ = $700 M$
    # Source: analysis.md §S2 Challenge 1; §S5 Table (laser cost row)
    # UNCERTAIN: via reference artifact 26-laser-icf-indirect-drive.md; not primary extract
    "C220104": LASER_NOAK_MS,
    # No superconducting magnets — IFE concept, no coil system
    # Source: xcimer-energy-approach.md; analysis.md §S7 cross-concept table (Magnet systems)
    "C220103": 0.0,
    # No divertor — liquid FLiBe wet wall protects structural steel from direct exposure
    # Source: xcimer-energy-approach.md §Liquid Wall; xcimer-science-page.md §Materials
    #         analysis.md §S7 cross-concept table (Plasma-facing / first-wall)
    "C220108": 0.0,
}

# ════════════════════════════════════════════════════════════════════════════
# Forward model — NOAK, He Brayton (base / optimistic scenario)
# ════════════════════════════════════════════════════════════════════════════
result_noak = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,           # 400 MWe Athena pilot
    availability=AVAILABILITY,                 # 0.85 upper scenario
    lifetime_yr=LIFETIME_YR,                   # 30 yr
    n_mod=1,
    construction_time_yr=5.0,      # DEFAULT: ife_laser_ife.yaml — no magnet assembly
    interest_rate=0.07,            # DEFAULT: standard discount rate
    inflation_rate=0.0245,         # DEFAULT: US long-run CPI
    noak=True,
    # ── Laser driver ─────────────────────────────────────────────────────────
    p_implosion=P_IMPLOSION_MW,    # 5 MW avg; 10 MJ/pulse × 0.5 Hz
                                   # Source: xcimer-energy-approach.md §Driver
    p_ignition=0.0,                # No separate ignition pulse in HDD; the brief
                                   # hohlraum pre-pulse is part of ASPEN main beam
                                   # Source: analysis.md §S3 HDD Target Physics
    eta_pin1=ETA_PIN1,             # 0.07 KrF wall-plug efficiency (conservative)
                                   # Source: analysis.md §S3 KrF Excimer Laser
                                   # UNCERTAIN — Xcimer target is 0.10
    eta_pin2=ETA_PIN1,             # Same laser train; no separate ignition driver
    eta_p=0.5,                     # DEFAULT: ife_laser_ife.yaml (pumping efficiency)
    # ── Power balance ────────────────────────────────────────────────────────
    mn=1.1,                        # DEFAULT: standard neutron energy multiplier
    eta_th=ETA_TH_BRAYTON,         # 0.45 He Brayton; analysis.md §H-3 base scenario
                                   # Source: hylife-energy-conversion-notes.orig.md §HYLIFE-II
    f_sub=0.03,                    # DEFAULT: subsystem auxiliary power fraction
    p_pump=1.0,                    # DEFAULT: FLiBe primary loop pumping power [MW]
    p_trit=10.0,                   # DEFAULT: tritium processing power [MW]
    p_house=4.0,                   # DEFAULT: housekeeping power [MW]
    p_cryo=0.5,                    # DEFAULT: cryogenics power [MW]
    p_target=1.0,                  # DEFAULT: target factory electrical load [MW]
    # ── Chamber geometry (HYLIFE-class, spherical) ───────────────────────────
    plasma_t=4.0,                  # DEFAULT: chamber radius [m] (ife_laser_ife.yaml)
                                   # UNCERTAIN: Xcimer HYLIFE-III scale unconfirmed
    blanket_t=0.80,                # DEFAULT: FLiBe blanket thickness [m]
    ht_shield_t=0.25,              # DEFAULT
    structure_t=0.15,              # DEFAULT
    vessel_t=0.10,                 # DEFAULT
    cost_overrides=OVERRIDES_NOAK_BRAYTON,
)

# ════════════════════════════════════════════════════════════════════════════
# Forward model — NOAK, Steam Rankine (H-3 alternative thermal scenario)
# ════════════════════════════════════════════════════════════════════════════
result_steam = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=5.0,
    interest_rate=0.07,
    inflation_rate=0.0245,
    noak=True,
    p_implosion=P_IMPLOSION_MW,
    p_ignition=0.0,
    eta_pin1=ETA_PIN1,
    eta_pin2=ETA_PIN1,
    eta_p=0.5,
    mn=1.1,
    eta_th=ETA_TH_STEAM,           # 0.33 Steam Rankine; UNCERTAIN — analysis.md §H-3 alt
                                   # Source: xcimer-science-page.md §Energy Conversion
    f_sub=0.03,
    p_pump=1.0,
    p_trit=10.0,
    p_house=4.0,
    p_cryo=0.5,
    p_target=1.0,
    plasma_t=4.0,
    blanket_t=0.80,
    ht_shield_t=0.25,
    structure_t=0.15,
    vessel_t=0.10,
    cost_overrides=OVERRIDES_NOAK_BRAYTON,
)

# ════════════════════════════════════════════════════════════════════════════
# Forward model — FOAK, He Brayton (FOAK reference for learning-curve context)
# ════════════════════════════════════════════════════════════════════════════
OVERRIDES_FOAK_BRAYTON = {
    "C220104": LASER_FOAK_MS,      # $1,100 M$ FOAK laser capital
    "C220103": 0.0,
    "C220108": 0.0,
}

result_foak = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=5.0,
    interest_rate=0.07,
    inflation_rate=0.0245,
    noak=False,                    # FOAK: includes contingency, first-of-kind premium
    p_implosion=P_IMPLOSION_MW,
    p_ignition=0.0,
    eta_pin1=ETA_PIN1,
    eta_pin2=ETA_PIN1,
    eta_p=0.5,
    mn=1.1,
    eta_th=ETA_TH_BRAYTON,
    f_sub=0.03,
    p_pump=1.0,
    p_trit=10.0,
    p_house=4.0,
    p_cryo=0.5,
    p_target=1.0,
    plasma_t=4.0,
    blanket_t=0.80,
    ht_shield_t=0.25,
    structure_t=0.15,
    vessel_t=0.10,
    cost_overrides=OVERRIDES_FOAK_BRAYTON,
)

# ════════════════════════════════════════════════════════════════════════════
# Results — base scenario (NOAK / He Brayton)
# ════════════════════════════════════════════════════════════════════════════
c  = result_noak.costs
pt = result_noak.power_table

print("=" * 70)
print("Laser ICF — Hybrid Direct Drive, D-T  (Xcimer Energy / Athena)")
print(f"Base scenario: NOAK | He Brayton {ETA_TH_BRAYTON*100:.0f}% | "
      f"η_laser {ETA_PIN1*100:.0f}% (conservative)")
print(f"Net electric: {NET_ELECTRIC_MW:.0f} MWe | Availability: {AVAILABILITY:.0%} | "
      f"Lifetime: {LIFETIME_YR} yr")
print("=" * 70)
print(f"LCOE:         {c.lcoe:.1f} $/MWh")
print(f"Overnight:    {c.overnight_cost:.0f} $/kW")
print(f"Fusion power: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.2f}")
print()

# ── Scenario comparison ───────────────────────────────────────────────────────
cs = result_steam.costs
cf = result_foak.costs

print("─" * 70)
print("Scenario comparison:")
print(f"  {'Scenario':<42} {'LCOE':>8}  {'OCC':>8}")
print(f"  {'':42} {'$/MWh':>8}  {'$/kW':>8}")
print(f"  {'':-<42}")
print(f"  {'NOAK / He Brayton 45% / η_laser 7%':<42} "
      f"{c.lcoe:>8.1f}  {c.overnight_cost:>8.0f}")
print(f"  {'NOAK / Steam Rankine 33% / η_laser 7%':<42} "
      f"{cs.lcoe:>8.1f}  {cs.overnight_cost:>8.0f}  ← H-3 alt")
print(f"  {'FOAK / He Brayton 45% / η_laser 7%':<42} "
      f"{cf.lcoe:>8.1f}  {cf.overnight_cost:>8.0f}  ← FOAK ref")
print()

# ── CAS breakdown (base scenario) ────────────────────────────────────────────
cas = [
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
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")
print()

# ── CAS22 sub-account detail ──────────────────────────────────────────────────
print("CAS22 detail (base scenario):")
print(f"  {'Account':<14} {'M$':>10}  Notes")
print(f"  {'':-<50}")
sub = result_noak.cas22_detail
for k in sorted(k for k in sub if k != "C220000"):
    note = ""
    if k == "C220104":
        note = f"← laser driver override (${LASER_NOAK_PER_J}/J × {LASER_ENERGY_MJ:.0f} MJ)"
    elif k == "C220103":
        note = "← 0 (no magnets, IFE)"
    elif k == "C220108":
        note = "← 0 (no divertor, liquid wall)"
    print(f"  {k:<14} {float(sub[k]):>10.1f}  {note}")
print(f"  {'C220000 TOTAL':<14} {float(sub['C220000']):>10.1f}")
print()

# ════════════════════════════════════════════════════════════════════════════
# Key Assumptions Summary
# ════════════════════════════════════════════════════════════════════════════
print("=" * 70)
print("Key Assumptions")
print("=" * 70)
print(f"  Laser system:     KrF excimer ASPEN, {LASER_ENERGY_MJ:.0f} MJ/pulse, "
      f"{REP_RATE_HZ} Hz → {P_IMPLOSION_MW:.0f} MW avg")
print(f"                    Source: xcimer-energy-approach.md; xcimer-science-page.md")
print()
print(f"  Laser capital:    NOAK ${LASER_NOAK_PER_J}/J × {LASER_ENERGY_MJ:.0f} MJ "
      f"= ${LASER_NOAK_MS:.0f}M  |  FOAK ${LASER_FOAK_PER_J}/J = ${LASER_FOAK_MS:.0f}M")
print(f"  UNCERTAIN:        Xcimer-TRUMPF whitepaper Feb 2026 (gap #7 — not directly extracted)")
print(f"                    Source: 26-laser-icf-indirect-drive.md §Comparison Table")
print()
print(f"  Thermal eff:      {ETA_TH_BRAYTON*100:.0f}% He Brayton (base) vs "
      f"{ETA_TH_STEAM*100:.0f}% Steam Rankine (alt)")
print(f"  UNCERTAIN:        Blocking gap #1; HYLIFE-III 2024 paper needed for resolution")
print(f"                    Source: analysis.md §H-3; hylife-energy-conversion-notes.orig.md")
print()
print(f"  Laser wall-plug:  {ETA_PIN1*100:.0f}% (conservative demonstrated-scale KrF)")
print(f"  UNCERTAIN:        Xcimer target 10%; Phoenix (kJ-scale) ~5–7% demonstrated")
print(f"                    Source: analysis.md §S2 Challenge 2; xcimer-science-page.md")
print()
print(f"  Availability:     {AVAILABILITY:.0%} upper scenario (30-yr liquid wall life claimed)")
print(f"  UNCERTAIN:        Blocking gap #2; no laser maintenance schedule published")
print(f"                    Source: analysis.md §S2 Challenge 6")
print()
print(f"  Target factory:   Framework default (target_factory_base scaling; no C220104 impact)")
print(f"  FLiBe / CAS27:    Framework default (HYLIFE-II inventory at Xcimer scale unknown; gap #9)")
print(f"  Magnets:          C220103 = 0.0 (no superconducting coils in IFE architecture)")
print(f"  Divertor:         C220108 = 0.0 (FLiBe liquid wall, no plasma-facing component)")
print()

# ════════════════════════════════════════════════════════════════════════════
# H-4: Target fabrication cost threshold analysis
# ════════════════════════════════════════════════════════════════════════════
SHOTS_PER_YEAR = REP_RATE_HZ * 86400 * 365 * AVAILABILITY   # shots/yr at availability
ANNUAL_ENERGY_GWH = NET_ELECTRIC_MW * AVAILABILITY * 8760 / 1000  # GWh/yr

print("─" * 70)
print(f"H-4  Target fabrication cost threshold")
print(f"     {SHOTS_PER_YEAR/1e6:.1f}M shots/yr at {REP_RATE_HZ} Hz × "
      f"{AVAILABILITY:.0%} CF   |   {ANNUAL_ENERGY_GWH:.0f} GWh/yr")
print(f"     Source: analysis.md §H-4; Goodin et al. criterion ~$1–5/target for viability")
print()
print(f"  {'Cost/target':>12}  {'Annual M$':>10}  {'LCOE contrib $/MWh':>20}")
print(f"  {'':-<46}")
for tgt_cost in [1.0, 5.0, 10.0, 100.0]:
    annual_ms = tgt_cost * SHOTS_PER_YEAR / 1e6   # M$/yr
    lcoe_add  = annual_ms * 1000 / ANNUAL_ENERGY_GWH  # $/MWh (M$/GWh × 1000)
    flag = " ← viability threshold" if tgt_cost == 5.0 else ""
    flag = " ← DISQUALIFYING" if tgt_cost == 100.0 else flag
    print(f"  ${tgt_cost:>10.0f}/target  {annual_ms:>10.1f}  {lcoe_add:>18.1f}{flag}")
print()

# ════════════════════════════════════════════════════════════════════════════
# Sensitivity analysis
# ════════════════════════════════════════════════════════════════════════════
print("─" * 70)
print("Sensitivity  (elasticity = %ΔLCOE / %Δparam)")
print("Base case: NOAK | He Brayton | η_laser 7%")
print("Note: overridden accounts (C220103, C220104, C220108) have zero gradient")
print("-" * 55)

sens = model.sensitivity(result_noak.params, cost_overrides=OVERRIDES_NOAK_BRAYTON)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")
