"""Laser ICF — Hybrid Direct Drive, D-T (Xcimer Energy / Athena pilot)
=====================================================================

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling approach
-----------------
Uses the 1costingfe LASER_IFE / DT framework for BOP, target factory, tritium,
and structural accounts. The laser driver capital — which dominates (~50–70%)
of direct cost — is injected via C220104 cost override derived from the
Xcimer-TRUMPF Feb 2026 whitepaper (XEC-20260224) subsystem-level $/J estimates.

Framework accounts used without override (trusting framework defaults):
  * Target factory capital (C220108 IFE/MIF path: target_factory_base scaling)
  * Tritium breeding / supply chain (CAS27, CAS80, CAS50 startup fuel)
  * BOP turbine plant (CAS23–26) under both thermal cycle scenarios
  * Buildings, indirect costs, IDC (CAS21, CAS30, CAS60)

Framework limitations / manual overrides for this concept
----------------------------------------------------------
  1. Laser driver capital (C220104) — overridden with $/J × 10 MJ.
     No standard CAS account covers a KrF excimer MJ-class driver.
  2. Magnets (C220103) — overridden to 0.0; IFE has no superconducting coils.
     (Framework geometry layer assigns non-zero coil cost by default.)
  3. Divertor (C220108) — kept at framework IFE default (target factory);
     liquid FLiBe wet wall eliminates traditional plasma-facing components.
  4. FLiBe thick-wall pumping (p_pump) — elevated from 1 MW default to 15 MW
     to approximate the thick-liquid-wall jet hydraulics load.
  5. Thermal cycle — two scenarios: He Brayton 45% (HYLIFE heritage) and
     Steam Rankine 33% (Xcimer science page language). Unresolved in sources.
  6. Target factory O&M cost per shot — the H-4 threshold analysis below
     quantifies the LCOE contribution at three cost-per-target points.
     Framework target_factory_base covers capital only.

Key hypotheses tested
---------------------
  H-1: Laser cost range (FOAK $110/J vs NOAK $60–80/J) → LCOE spread
  H-3: Thermal cycle gap (He Brayton 45% vs Steam Rankine 33%)
  H-4: Target fabrication cost threshold ($1 / $5 / $10 per target)

Sources:
    [XEC]     xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md
    [sci]     xcimer-science-page.md
    [app]     xcimer-energy-approach.md
    [an]      analyses/17a-laser-icf-hybrid-drive/analysis.md
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Create model ─────────────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# ════════════════════════════════════════════════════════════════════════════
# Plant configuration constants
# ════════════════════════════════════════════════════════════════════════════

# Net electric output — Xcimer "Athena" pilot plant target
# Source: [XEC] §Executive Summary: "~400 MWe net electrical output"
#         [an] §Section 5 Table, "Net electrical output — Athena pilot"
# Confidence: medium — company-stated, no independent engineering validation
NET_ELECTRIC_MW = 400.0

# Availability (capacity factor)
# Upper scenario: 0.85 — 30-yr liquid-wall chamber life, no first-wall replacement
# Lower scenario: 0.70 — conservative, pulsed-power maintenance analogue
# UNCERTAIN: blocking gap — no maintenance schedule, laser diode lifetime, or
#   FLiBe pump/nozzle service interval published.
# Source: [an] §Section 5 Missing Parameters (gap #3 "truly-unknown")
AVAILABILITY = 0.85  # upper scenario; run with 0.70 for conservative bound

# Plant lifetime — 30-year structural chamber lifetime claimed by Xcimer
# Source: [app] §Xcimer's approach; [an] §Section 5 Table
# Enabled by FLiBe liquid wall protecting structural steel from neutron fluence.
# HYLIFE-III 2024 paper (FED, behind paywall) underpins this claim.
LIFETIME_YR = 30

# ── Laser driver configuration ────────────────────────────────────────────────

# Laser energy per pulse: 8–12 MJ (KrF excimer ASPEN architecture)
# Source: [XEC] §Executive Summary: "8–12 MJ on target"; [an] §Section 5 Table
# Confidence: medium (commercial design point; NIF comparison: 2.1 MJ)
LASER_ENERGY_MJ = 10.0  # MJ per pulse — midpoint of 8–12 MJ range

# Rep rate: sub-Hz, "every couple seconds" → 0.25–1 Hz
# Source: [app] §Rep Rate; [XEC] §Executive Summary; [an] §Section 5 Table
# Confidence: high ("every couple seconds" confirmed multiple sources)
# UNCERTAIN: exact rep rate not disclosed; 0.5 Hz used as nominal
REP_RATE_HZ = 0.5  # Hz nominal

# Average laser optical output power fed to framework [MW] = E_pulse × f_rep
# Note: derived for Qsci=250 self-consistency, this gives p_implosion ≈ 4.7 MW.
# Using 10 MJ × 0.5 Hz = 5.0 MW (slightly higher; consistent at Qsci ≈ 240–250).
# Source: [an] §Section 5: Qsci ~250 at NOAK; rep rate 0.25–1 Hz
P_IMPLOSION_MW = LASER_ENERGY_MJ * REP_RATE_HZ  # 5 MW average optical output

# No separate ignition pulse in Xcimer HDD.
# The hohlraum pre-pulse that creates the ablation plasma is part of the same
# two-beam KrF shot — not a distinct ignition laser chain.
# Source: [an] §Section 2.3: "only two beams...brief hohlraum pre-pulse"
P_IGNITION_MW = 0.0

# Laser wall-plug efficiency (eta_pin1)
# NOAK target (Nth-of-a-kind): 7%, achieved with full Argos/SBS/NLO architecture
# Demonstrated (NRL Electra, 750 J): 7% at sub-kJ scale
# Source: [XEC] §Challenge 3: "7% laser efficiency" for NOAK system
# UNCERTAIN: not yet demonstrated at MJ scale; Xcimer aspirational target is 10%
ETA_PIN1 = 0.07  # NOAK target — [XEC] §Challenge 3
                 # Conservative vs Xcimer 10% aspirational; see sensitivity sweep

# ── Thermal cycle ─────────────────────────────────────────────────────────────
# BLOCKING AMBIGUITY: cycle type unresolved in available sources.
# Source: [an] §Section 2.5 (blocking gap #2); §Section 5 Missing Parameters

# He Brayton (45%): HYLIFE-II heritage, well-matched to FLiBe primary loop
# Source: HYLIFE-II 1994 — ~45% thermal efficiency for He Brayton at FLiBe temp
ETA_TH_BRAYTON = 0.45  # He Brayton — HYLIFE heritage; high confidence for that design

# Steam Rankine (33%): implied by Xcimer science page language ("steam turbines")
# Source: [sci] §Energy Conversion: "generate steam, which in turn drives turbines"
# UNCERTAIN: may be simplified marketing language; steam ~33% is the typical
#   saturated/superheated steam cycle. If true, increases gross thermal requirement.
ETA_TH_STEAM = 0.33  # UNCERTAIN: Steam Rankine; [sci] §Energy Conversion

# ── FLiBe thick-liquid-wall pumping ──────────────────────────────────────────
# The HYLIFE jet system recirculates dense FLiBe (ρ ≈ 1940 kg/m³) at high
# volumetric flow to form protective jets and clear the chamber in ~1 s between
# shots. Framework default (1 MW) is calibrated for a thin-coolant IFE system.
# No published pumping power estimate for a thick-liquid-wall HYLIFE-scale plant.
# 15 MW is an order-of-magnitude estimate for jet-forming pumps at ~400 MWe scale.
# Source: [an] §Section 2.4 (FLiBe hydraulics gap); [XEC] §Xcimer's Chamber Design
# UNCERTAIN: FLiBe jet pump power — may be 5–30 MW depending on jet geometry
P_PUMP_MW = 15.0  # UNCERTAIN: FLiBe thick-liquid-wall hydraulics; [an] §2.4

# ── Laser capital cost (C220104 override) ─────────────────────────────────────
# Bottom-up from ($/J) × (driver energy in joules)
#
# NOAK: $60–80/J on-target (midpoint $70/J)
#   Source: [XEC] §Xcimer Laser Cost and Schedule
#   Subsystem breakdown (NOAK): capacitors ~$0.40/J (target), Marx $8/J,
#     e-beam $6/J, chamber/gas $9/J, optics $12/J, seed/NLO $17/J, control $4/J
#   UNCERTAIN: depends on in-house capacitor manufacturing hitting <$0.40/J
#     (current market ~$10/J). Target not yet achieved.
#     [an] §Section 5 Table: confidence "low"
#
# FOAK: ~$100/J on-target
#   Source: [XEC] §Xcimer Laser Cost and Schedule: FOAK ~$100/J
#   Subsystem breakdown published in whitepaper; confidence "medium"
#   $110/J used as midpoint (consistent with analysis.md context)
#
# At 10 MJ on-target:
#   NOAK low  $60/J:  $600 M$
#   NOAK mid  $70/J:  $700 M$  ← primary design-point
#   NOAK high $80/J:  $800 M$
#   FOAK      $110/J: $1,100 M$  (midpoint $100–120/J)
LASER_NOAK_LOW_PER_J = 60.0   # $/J; [XEC] §Xcimer Laser Cost (NOAK lower bound)
LASER_NOAK_MID_PER_J = 70.0   # $/J; midpoint of NOAK range
LASER_NOAK_HIGH_PER_J = 80.0  # $/J; [XEC] §Xcimer Laser Cost (NOAK upper bound)
LASER_FOAK_PER_J = 110.0      # $/J; midpoint FOAK range; [XEC] §Xcimer Laser Cost

# M$ = $/J × MJ (unit identity: $/J × 10^6 J / 10^6 $/M$ = $/J × MJ = M$)
LASER_NOAK_LOW_MS = LASER_NOAK_LOW_PER_J * LASER_ENERGY_MJ    #  600 M$
LASER_NOAK_MID_MS = LASER_NOAK_MID_PER_J * LASER_ENERGY_MJ    #  700 M$
LASER_NOAK_HIGH_MS = LASER_NOAK_HIGH_PER_J * LASER_ENERGY_MJ  #  800 M$
LASER_FOAK_MS = LASER_FOAK_PER_J * LASER_ENERGY_MJ            # 1100 M$

# ── Cost overrides (shared structure) ────────────────────────────────────────
def _overrides(laser_ms: float, noak: bool) -> dict:
    return {
        # Laser driver capital — C220104 (supplementary heating / driver account)
        # No standard CAS account covers a KrF excimer MJ-class laser; C220104 is
        # the closest available sub-account. Default C220104 = 0 for IFE (no NBI/ICRF).
        # Source: [XEC] §Xcimer Laser Cost and Schedule; [an] §Section 5 Table
        "C220104": laser_ms,
        # No superconducting magnets — IFE concept, no coil system.
        # Framework geometry layer computes non-zero coil cost by default; zero here.
        # Source: [app]; [an] §Section 7 cross-concept table (Magnet systems → absent)
        "C220103": 0.0,
    }

# ════════════════════════════════════════════════════════════════════════════
# Forward runs
# ════════════════════════════════════════════════════════════════════════════

# Shared engineering kwargs (same for all scenario branches)
_ENG = dict(
    n_mod=1,
    construction_time_yr=5.0,    # DEFAULT: ife_laser_ife.yaml — no magnet assembly
    interest_rate=0.07,           # DEFAULT: standard discount rate
    inflation_rate=0.0245,        # DEFAULT: US long-run CPI
    # ── Laser driver ─────────────────────────────────────────────────────────
    p_implosion=P_IMPLOSION_MW,   # 5 MW avg; 10 MJ/pulse × 0.5 Hz
                                  # Source: [XEC] §Executive Summary
    p_ignition=P_IGNITION_MW,     # 0 MW; HDD unified laser, no separate igniter
                                  # Source: [an] §Section 2.3
    eta_pin1=ETA_PIN1,            # 0.07 KrF wall-plug (NOAK); [XEC] §Challenge 3
    eta_pin2=ETA_PIN1,            # same laser train; no separate ignition driver
    eta_p=0.5,                    # DEFAULT: ife_laser_ife.yaml (pumping efficiency)
    # ── Power balance ────────────────────────────────────────────────────────
    mn=1.1,                       # DEFAULT: FLiBe blanket neutron multiplier
                                  # FLiBe (⁹Be) → (n,2n) → mn ≈ 1.1; consistent with
                                  # TBR ~1.2 (natural Li); [XEC] §Xcimer's Chamber Design
    f_sub=0.03,                   # DEFAULT: subsystem auxiliary power fraction
    p_pump=P_PUMP_MW,             # 15 MW: FLiBe thick-liquid-wall hydraulics estimate
                                  # UNCERTAIN; [an] §Section 2.4
    p_trit=10.0,                  # DEFAULT: tritium extraction power from FLiBe loop
                                  # Low startup inventory (<150 g; [XEC] §Chamber Design)
                                  # implies active in-situ extraction; default is adequate
    p_house=4.0,                  # DEFAULT: housekeeping power [MW]
    p_cryo=0.5,                   # DEFAULT: cryogenics power [MW]
    p_target=1.0,                 # DEFAULT: target factory electrical load [MW]
    # ── Chamber geometry (HYLIFE-class, spherical) ───────────────────────────
    plasma_t=4.0,                 # DEFAULT: chamber radius [m] (ife_laser_ife.yaml)
                                  # UNCERTAIN: Xcimer HYLIFE-III scale unconfirmed
    blanket_t=0.80,               # DEFAULT: FLiBe blanket thickness [m]
                                  # FLiBe liquid wall is ~1–2 m deep; default 0.8 m
                                  # underestimates blanket volume slightly
    ht_shield_t=0.25,             # DEFAULT
    structure_t=0.15,             # DEFAULT; conventional commercial steel adequate
                                  # (FLiBe wall reduces neutron fluence to structure)
                                  # Source: [app] §Xcimer's approach: "commercially
                                  # available materials"; [an] §Section 4
    vessel_t=0.10,                # DEFAULT
)

# NOAK — He Brayton 45% (base / optimistic scenario)
result_noak = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    noak=True,
    eta_th=ETA_TH_BRAYTON,        # 0.45 He Brayton; HYLIFE heritage; [an] §2.5 scenario A
    cost_overrides=_overrides(LASER_NOAK_MID_MS, noak=True),
    **_ENG,
)

# NOAK — Steam Rankine 33% (H-3 alternative thermal scenario)
result_steam = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    noak=True,
    eta_th=ETA_TH_STEAM,          # 0.33 Steam Rankine; UNCERTAIN; [sci] §Energy Conversion
    cost_overrides=_overrides(LASER_NOAK_MID_MS, noak=True),
    **_ENG,
)

# FOAK — He Brayton (FOAK reference for learning-curve context)
result_foak = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    noak=False,                   # FOAK: 10% contingency premium
    eta_th=ETA_TH_BRAYTON,
    cost_overrides=_overrides(LASER_FOAK_MS, noak=False),
    **_ENG,
)

# NOAK laser cost range: $60–80/J (for H-1 sensitivity sweep)
result_noak_low = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    noak=True,
    eta_th=ETA_TH_BRAYTON,
    cost_overrides=_overrides(LASER_NOAK_LOW_MS, noak=True),
    **_ENG,
)
result_noak_high = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    noak=True,
    eta_th=ETA_TH_BRAYTON,
    cost_overrides=_overrides(LASER_NOAK_HIGH_MS, noak=True),
    **_ENG,
)

# ════════════════════════════════════════════════════════════════════════════
# Results — base scenario (NOAK / He Brayton / $70/J laser)
# ════════════════════════════════════════════════════════════════════════════
c  = result_noak.costs
pt = result_noak.power_table
qwp = pt.q_sci * ETA_PIN1   # wall-plug gain = Qsci × η_wpe

print("=" * 70)
print("Laser ICF — Hybrid Direct Drive, D-T  (Xcimer Energy / Athena)")
print(f"Base scenario: NOAK | He Brayton {ETA_TH_BRAYTON*100:.0f}% | "
      f"η_laser {ETA_PIN1*100:.0f}% | laser $70/J")
print(f"Net electric: {NET_ELECTRIC_MW:.0f} MWe | Availability: {AVAILABILITY:.0%} | "
      f"Lifetime: {LIFETIME_YR} yr")
print("=" * 70)
print(f"LCOE:         {c.lcoe:.1f} $/MWh")
print(f"Overnight:    {c.overnight_cost:.0f} $/kW")
print(f"Fusion power: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.2f}")
print(f"Qsci: {pt.q_sci:.0f} | Qwp: {qwp:.1f} | Recirc: {pt.rec_frac:.1%} "
      f"(laser: {100 * (P_IMPLOSION_MW / ETA_PIN1) / float(pt.p_et):.1f}% of gross)")
print()

# ── Scenario comparison: H-1 (laser cost range) ──────────────────────────────
cs = result_steam.costs
cf = result_foak.costs

print("─" * 70)
print("H-1  Laser cost range (NOAK $60–80/J) + H-3 thermal cycle gap:")
print(f"  {'Scenario':<48} {'LCOE':>7}  {'OCC':>7}")
print(f"  {'':48} {'$/MWh':>7}  {'$/kW':>7}")
print(f"  {'':-<48}")
rows_scenario = [
    ("NOAK / He Brayton 45% / laser $60/J",  result_noak_low.costs),
    ("NOAK / He Brayton 45% / laser $70/J",  result_noak.costs),    # base
    ("NOAK / He Brayton 45% / laser $80/J",  result_noak_high.costs),
    ("NOAK / Steam Rankine 33% / laser $70/J", result_steam.costs),  # H-3 alt
    ("FOAK / He Brayton 45% / laser $110/J", result_foak.costs),     # FOAK ref
]
for label, rc in rows_scenario:
    marker = " ← base" if "70/J" in label and "Brayton" in label and "NOAK" in label else ""
    if "Steam" in label: marker = " ← H-3 alt"
    if "FOAK" in label:  marker = " ← FOAK ref"
    print(f"  {label:<48} {rc.lcoe:>7.1f}  {rc.overnight_cost:>7.0f}{marker}")
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
print("CAS22 detail (base scenario — NOAK He Brayton $70/J):")
print(f"  {'Account':<14} {'M$':>10}  Notes")
print(f"  {'':-<54}")
sub = result_noak.cas22_detail
for k in sorted(k for k in sub if k != "C220000"):
    note = ""
    if k == "C220104":
        note = f"← laser driver override (${LASER_NOAK_MID_PER_J}/J × {LASER_ENERGY_MJ:.0f} MJ)"
    elif k == "C220103":
        note = "← 0 override (no magnets, IFE)"
    elif k == "C220108":
        note = "← target factory (IFE default; FLiBe wall = no divertor)"
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
      f"{REP_RATE_HZ} Hz → {P_IMPLOSION_MW:.0f} MW avg optical output")
print(f"                    Source: [XEC] §Executive Summary; [an] §S5 Table")
print()
print(f"  Laser capital:    NOAK ${LASER_NOAK_MID_PER_J}/J × {LASER_ENERGY_MJ:.0f} MJ = "
      f"${LASER_NOAK_MID_MS:.0f}M  (range: "
      f"${LASER_NOAK_LOW_MS:.0f}M – ${LASER_NOAK_HIGH_MS:.0f}M)")
print(f"                    FOAK ${LASER_FOAK_PER_J}/J × {LASER_ENERGY_MJ:.0f} MJ = "
      f"${LASER_FOAK_MS:.0f}M")
print(f"  UNCERTAIN:        Self-reported; no independent verification.")
print(f"                    Depends on capacitor cost <$0.40/J (current market ~$10/J).")
print(f"                    Source: [XEC] §Xcimer Laser Cost and Schedule; [an] §S5 Table")
print()
print(f"  Thermal eff:      {ETA_TH_BRAYTON*100:.0f}% He Brayton (base) vs "
      f"{ETA_TH_STEAM*100:.0f}% Steam Rankine (H-3 alt)")
print(f"  UNCERTAIN:        Blocking gap; HYLIFE heritage = Brayton; [sci] implies steam.")
print(f"                    Source: [an] §S2 Challenge 5; §S5 Missing Parameters gap #2")
print()
print(f"  Laser wall-plug:  {ETA_PIN1*100:.0f}% (NOAK KrF demonstrated at Electra 750 J)")
print(f"  UNCERTAIN:        Xcimer aspirational target 10%; not demonstrated at MJ scale.")
print(f"                    Source: [XEC] §Challenge 3; [an] §S5 Table")
print()
print(f"  Availability:     {AVAILABILITY:.0%} upper scenario")
print(f"  UNCERTAIN:        No maintenance model published. FLiBe liquid wall eliminates")
print(f"                    first-wall replacement outages (advantage), but pump/nozzle")
print(f"                    maintenance interval unknown. Source: [an] §S5 gap #3")
print()
print(f"  FLiBe pumping:    {P_PUMP_MW:.0f} MW (estimated; UNCERTAIN)")
print(f"                    Framework default (1 MW) calibrated for thin-coolant IFE.")
print(f"                    Thick-liquid-wall jet pump: no published estimate.")
print(f"                    Source: [an] §S2 Challenge 4; [XEC] §Xcimer's Chamber Design")
print()
print(f"  Qsci (implied):   {pt.q_sci:.0f} (from inverse power balance at 400 MWe)")
print(f"                    XEC target ~250. At Qsci ~{pt.q_sci:.0f} and η_wpe={ETA_PIN1:.0%}:")
print(f"                    Qwp = {pt.q_sci:.0f} × {ETA_PIN1:.0%} = {qwp:.1f} "
      f"(XEC claims ~17.5 at Qsci=250, η_wpe=7%). [XEC] §Challenge 3")
print()
print(f"  Target factory:   Framework default (target_factory_base IFE scaling)")
print(f"  CAS27 / FLiBe:    Framework default (FLiBe inventory at Xcimer scale unknown)")
print(f"                    Default PbLi-calibrated; likely understates FLiBe/Be cost.")
print(f"                    Source: [an] §S6 gap #7")
print(f"  Magnets C220103:  0.0 M$ override — no superconducting coils in IFE")
print(f"                    Source: [app]; [an] §S7 cross-concept table")
print()

# ════════════════════════════════════════════════════════════════════════════
# H-4: Target fabrication cost threshold analysis
# ════════════════════════════════════════════════════════════════════════════
SHOTS_PER_YEAR = REP_RATE_HZ * 86400 * 365 * AVAILABILITY   # shots/yr at availability
ANNUAL_ENERGY_GWH = NET_ELECTRIC_MW * AVAILABILITY * 8760 / 1000  # GWh/yr

print("─" * 70)
print(f"H-4  Target fabrication cost threshold (Goodin et al. criterion)")
print(f"     {SHOTS_PER_YEAR/1e6:.1f}M shots/yr at {REP_RATE_HZ} Hz × "
      f"{AVAILABILITY:.0%} CF   |   {ANNUAL_ENERGY_GWH:.0f} GWh/yr")
print(f"     Goodin criterion: targets <10% of electricity produced/shot → ~$2–3/target")
print(f"     Source: [an] §Section 2.6; §Section 7 (cross-concept analysis)")
print()
print(f"  {'Cost/target':>12}  {'Annual M$/yr':>14}  {'LCOE contrib $/MWh':>20}")
print(f"  {'':-<50}")
for tgt_cost in [1.0, 2.5, 5.0, 10.0]:
    annual_ms = tgt_cost * SHOTS_PER_YEAR / 1e6     # M$/yr
    lcoe_add  = annual_ms * 1000 / ANNUAL_ENERGY_GWH  # $/MWh
    flag = ""
    if tgt_cost == 2.5:
        flag = " ← Goodin threshold (~$2–3/target at 400 MWe)"
    elif tgt_cost == 10.0:
        flag = " ← 10× over threshold: economically disqualifying"
    print(f"  ${tgt_cost:>10.2f}/target  {annual_ms:>14.1f}  {lcoe_add:>18.1f}{flag}")
print()
print("  Note: this recurring cost has NO analogue in MFE and is NOT in CAS70/80")
print("  defaults. Target cost at commercial throughput (8–31M shots/yr) is a")
print("  blocking gap — no Xcimer estimate published. Source: [an] §S5 gap #4")
print()

# ════════════════════════════════════════════════════════════════════════════
# Sensitivity analysis
# ════════════════════════════════════════════════════════════════════════════
print("─" * 70)
print("Sensitivity  (elasticity = %ΔLCOE / %Δparam)")
print("Base case: NOAK | He Brayton 45% | laser $70/J | η_laser 7%")
print("Overridden accounts (C220103, C220104) have zero gradient by construction.")
print("-" * 55)

sens = model.sensitivity(
    result_noak.params,
    cost_overrides=_overrides(LASER_NOAK_MID_MS, noak=True),
)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")
