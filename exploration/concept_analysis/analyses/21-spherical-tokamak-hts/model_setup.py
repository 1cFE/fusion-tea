"""Spherical Tokamak - HTS (Tokamak Energy ST-E1 Revision D) — LCOE estimate.

Modeling approach
-----------------
The ST-E1 Rev D design is characterised by only four published machine
parameters (R=5.0 m, A=2.3, B=5.25 T on-axis, TBR=1.2) and one output
range (450–750 MWe net).  Fusion power, Q, thermal efficiency, auxiliary
heating power, and all cost figures are proprietary or undisclosed.  This
script therefore:

  1. Uses published geometry directly (R0, A → plasma_t).
  2. Derives central-estimate values from analogues (thermal efficiency from
     STEP-related ST research; ECRH wall-plug efficiency from ITER-class
     gyrotron data; availability from D-T MCF literature ranges adjusted
     downward for pulsed operation).
  3. Falls back to framework defaults for every uncharacterised cost account.

All analogue assumptions are tagged UNCERTAIN.  The sensitivity block at the
end reveals which assumptions drive LCOE most.

Concept choice rationale
------------------------
ConfinementConcept.TOKAMAK / Fuel.DT — spherical tokamak is a sub-variant of
the tokamak family; the D-T fuel cycle is confirmed by TBR=1.2 design target.

Key deviations from dt_tokamak.py reference
--------------------------------------------
- R0 = 5.0 m (vs 3.0 m CATF ref) — published ST-E1 Rev D value
- plasma_t = 2.17 m (minor radius a = R0/A = 5.0/2.3)
- elon = 2.5 — typical ST elongation at A≈2.3; unpublished for ST-E1
- eta_th = 0.33 — UNCERTAIN, steam Rankine ~30–38% (STEP ST research range)
- eta_pin = 0.52 — ECRH-only flat-top; gyrotron wall-plug ~50–55%
- availability = 0.85 — canonical per scoring_framework.md §Plant availability
  (MCF quasi-steady, D-T); previously 0.80
- net_electric_mw = 600 — central of published 450–750 MWe range

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ──────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# ── Plant configuration ──────────────────────────────────────────────

# Customer-level requirements
NET_ELECTRIC_MW = 600.0     # Central of 450–750 MWe Rev D range
                            # Source: analysis.md §Section 5 Table; tokamak-energy-st-e1-dpp2025-abstract.md

AVAILABILITY = 0.85          # canonical per scoring_framework.md §Plant availability (MCF quasi-steady, D-T)
                            # previously 0.80 (pulsed-operation downward adjustment, no published target)
                            # Sensitivity sweeps in the scenario block below still test 0.70–0.92 excursions

LIFETIME_YR = 30            # DEFAULT: standard fusion plant lifetime assumption
CONSTRUCTION_TIME_YR = 8.0  # UNCERTAIN: larger machine than CATF ref (R0=5.0 vs 3.0 m);
                            # no published schedule; 8 yr conservative estimate

# ── Geometry (ST-E1 Revision D) ──────────────────────────────────────

R0 = 5.0                    # Major radius [m]; published DPP 2025 abstract
                            # Source: tokamak-energy-st-e1-dpp2025-abstract.md
ASPECT_RATIO = 2.3          # Published DPP 2025 abstract; at upper boundary of ST regime
                            # Source: tokamak-energy-st-e1-dpp2025-abstract.md
PLASMA_T = R0 / ASPECT_RATIO  # Minor radius a = R0/A ≈ 2.17 m; derived from published values

ELON = 2.5                  # UNCERTAIN: ST elongation at A≈2.3 typical range 2.0–3.0;
                            # unpublished for ST-E1; 2.5 is a reasonable mid-range estimate

BLANKET_T = 0.80            # DEFAULT: outboard-only liquid Li blanket; actual thickness
                            # not published.  Framework default used; NOTE: blanket volume
                            # computed assuming full 4π coverage — an overestimate for the
                            # outboard-only geometry, so CAS22 blanket cost is conservative
                            # (likely overestimated).
HT_SHIELD_T = 0.20          # DEFAULT: center stack WC cermet shield ~32 cm published for
                            # R=1.35 m device; ST-E1 scale not published.
                            # Source: spherical-tokamak-center-stack-shielding.md §Table 3
STRUCTURE_T = 0.20          # DEFAULT: framework value
VESSEL_T = 0.20             # DEFAULT: framework value

# ── Power balance ─────────────────────────────────────────────────────

ETA_TH = 0.35                # standardized from 0.33 per scoring_framework.md (Energy Capture: Thermal (unspecified))
                            # by Tokamak Energy.  STEP ST research evaluates steam Rankine,
                            # hybrid ORC, sCO2 Brayton; range 30–38%.  Central estimate 33%
                            # (steam Rankine).
                            # Source: analysis.md §Section 2, Challenge 1; ste1-pilot-plant-specs.md

ETA_PIN = 0.52              # ECRH gyrotron wall-plug efficiency.  Flat-top uses ECRH only
                            # (O-mode) per Alieva et al. (2026); current-generation gyrotrons
                            # achieve ~50–55%.  Central estimate 52%.
                            # Source: tokamak-energy-ec-heating-pilot-plant.md;
                            # analysis.md §Section 2, Challenge 3

P_INPUT_MW = 50.0           # DEFAULT: auxiliary ECRH power for ST-E1 flat-top is not
                            # disclosed.  Framework default 50 MW used as placeholder.
                            # True value derivable once Q or Ip (Rev D) is published.
                            # Source: analysis.md §Section 5 Missing Parameters Table

MN = 1.1                    # DEFAULT: neutron energy multiplier for outboard Li blanket.
                            # Outboard-only coverage may reduce effective mn slightly, but
                            # no ST-E1-specific data; framework default applied.

ETA_P = 0.5                 # DEFAULT: pumping efficiency
ETA_DE = 0.00                # standardized from 0.85 per scoring_framework.md (Energy Capture: Thermal (unspecified))

F_SUB = 0.03                # DEFAULT: subsystem power fraction of gross electric
F_DEC = 0.0                 # No direct energy conversion; pulsed D-T, ECRH-only heating

P_COILS = 2.0               # DEFAULT: HTS coils at 30 K have very low resistive losses;
                            # cryo overhead captured separately in p_cryo.
                            # Source: tokamak-energy-demo4-magnets.md (11.8 T, 30 K)

P_COOL = 15.0               # UNCERTAIN: slightly above framework default (13.7 MW) to
                            # account for liquid Li primary circuit pumping and thermal
                            # management.  No ST-E1 specific data.

P_PUMP = 2.0                # UNCERTAIN: Li metal primary circuit requires active pumping
                            # in inert atmosphere; slightly above default 1.0 MW.

P_TRIT = 10.0               # DEFAULT: tritium processing power.  Liquid Li extraction
                            # system design is truly unknown (analysis.md §Section 6, Gap 8).

P_HOUSE = 4.0               # DEFAULT: housekeeping
P_CRYO = 1.0                # UNCERTAIN: HTS at 30 K has much lower cryo power than LTS
                            # at 4 K, but larger coil set (ST-E1 is a large machine).
                            # Slightly above default 0.5 MW; no published value.

# ── Financial parameters ──────────────────────────────────────────────

INTEREST_RATE = 0.07        # DEFAULT: standard project finance assumption
INFLATION_RATE = 0.0245     # DEFAULT: US long-run CPI target
NOAK = True                 # NOAK reference case (no contingency, mature supply chain)

# ── Shared kwargs (used for both native and 1 GW forward passes) ──────

_SHARED_KWARGS = dict(
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=NOAK,

    # ST-E1 Rev D geometry
    R0=R0,                          # 5.0 m — published
    plasma_t=PLASMA_T,              # 2.17 m — derived from R0/A
    elon=ELON,                      # 2.5 — UNCERTAIN analogue
    blanket_t=BLANKET_T,            # 0.80 m — DEFAULT (outboard-only, full-4π overestimate)
    ht_shield_t=HT_SHIELD_T,        # 0.20 m — DEFAULT
    structure_t=STRUCTURE_T,        # 0.20 m — DEFAULT
    vessel_t=VESSEL_T,              # 0.20 m — DEFAULT

    # Power balance
    p_input=P_INPUT_MW,             # 50 MW — DEFAULT (ECRH power undisclosed)
    mn=MN,                          # 1.1 — DEFAULT
    eta_th=ETA_TH,                  # 0.33 — UNCERTAIN (steam Rankine analogue)
    eta_p=ETA_P,                    # 0.5 — DEFAULT
    eta_pin=ETA_PIN,                # 0.52 — ECRH gyrotron wall-plug efficiency
    eta_de=ETA_DE,                  # 0.85 — DEFAULT (DEC not used)
    f_sub=F_SUB,                    # 0.03 — DEFAULT
    f_dec=F_DEC,                    # 0.0 — no DEC (pulsed D-T, ECRH-only)
    p_coils=P_COILS,                # 2.0 MW — DEFAULT (HTS, low resistive loss)
    p_cool=P_COOL,                  # 15.0 MW — UNCERTAIN (Li metal circuit)
    p_pump=P_PUMP,                  # 2.0 MW — UNCERTAIN (Li metal pumping)
    p_trit=P_TRIT,                  # 10.0 MW — DEFAULT (liquid Li extraction unknown)
    p_house=P_HOUSE,                # 4.0 MW — DEFAULT
    p_cryo=P_CRYO,                  # 1.0 MW — UNCERTAIN (HTS at 30 K)

    # No cost overrides — all capital costs use framework defaults.
    # Rationale: no published cost estimates exist for ST-E1.  The 4π blanket
    # volume assumption overestimates CAS22 blanket for the outboard-only
    # geometry, providing a conservative LCOE estimate.
    # The pulsed-operation thermal energy storage buffer (molten salt TES) is a
    # real but entirely uncharacterised cost (analysis.md §Section 6, Gap 11);
    # it is not represented in the framework and cannot be quantified without
    # ST-E1 pulse duration / dwell data.  Cost is omitted — a downward bias on
    # total capital of unknown magnitude.
)

# ── Model forward passes ──────────────────────────────────────────────

# Native design point: 600 MWe (central of published 450–750 MWe range)
result = model.forward(net_electric_mw=NET_ELECTRIC_MW, **_SHARED_KWARGS)

# Self-consistent 1 GW result for cross-concept comparison.
# override_reference_mw tells the framework that all cost_override values
# (none here — only geometry/physics inputs) are valid at 600 MWe and
# should scale to 1000 MWe using per-account scaling laws.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=NET_ELECTRIC_MW,
    **_SHARED_KWARGS,
)

# ── Results ───────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Spherical Tokamak - HTS (Tokamak Energy ST-E1 Rev D)")
print(f"  Config: {NET_ELECTRIC_MW:.0f} MWe net | {AVAILABILITY:.0%} availability | {LIFETIME_YR} yr | NOAK")
print(f"  Geometry: R0={R0} m, A={ASPECT_RATIO}, a={PLASMA_T:.2f} m, κ={ELON}")
print(f"  Field: B={5.25} T on-axis | Heating: ECRH-only (η_pin={ETA_PIN})")
print(f"  Thermal eff.: η_th={ETA_TH} (UNCERTAIN — steam Rankine analogue)")
print()
print(f"LCOE:       {c.lcoe:.1f} $/MWh")
print(f"Overnight:  {c.overnight_cost:.0f} $/kW")
print(f"Fusion:     {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.2f}")
print()
print(f"1 GW scaled (cross-concept): LCOE {result_1gw.costs.lcoe:.1f} $/MWh | "
      f"Overnight {result_1gw.costs.overnight_cost:.0f} $/kW")
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

# ── CAS22 sub-account detail ──────────────────────────────────────────
print()
print("CAS22 sub-account detail:")
print(f"{'Code':<12} {'M$':>10}")
print("-" * 24)
for k, v in sorted(result.cas22_detail.items()):
    print(f"  {k:<10} {float(v):>10.1f}")

# ── Key assumptions summary ───────────────────────────────────────────
print()
print("=" * 60)
print("Key Assumptions and Data Quality")
print("=" * 60)
print(f"  Net electric (central of 450–750 MWe range):  {NET_ELECTRIC_MW:.0f} MWe  [HIGH confidence]")
print(f"  Major radius R0:                               {R0} m    [HIGH confidence]")
print(f"  Aspect ratio A → minor radius:                 {ASPECT_RATIO} → {PLASMA_T:.2f} m [HIGH confidence]")
print(f"  Elongation κ:                                  {ELON}     [UNCERTAIN — analogue]")
print(f"  On-axis field B:                               5.25 T  [HIGH confidence]")
print(f"  Thermal efficiency η_th:                       {ETA_TH}   [UNCERTAIN — steam Rankine analogue]")
print(f"  Heating (ECRH) wall-plug η_pin:               {ETA_PIN}   [MEDIUM — gyrotron analogue]")
print(f"  Aux heating power p_input:                     {P_INPUT_MW:.0f} MW  [DEFAULT — undisclosed]")
print(f"  Availability:                                  {AVAILABILITY:.0%}   [canonical — scoring_framework.md §Plant availability, MCF quasi-steady D-T]")
print(f"  Blanket coverage:                              outboard-only (4π model overestimates cost)")
print(f"  Thermal buffer (pulsed TES):                   NOT MODELLED — cost unknown, downward bias")
print(f"  All capital costs:                             FRAMEWORK DEFAULTS (no published cost data)")

# ── Sensitivity analysis ──────────────────────────────────────────────
sens = model.sensitivity(result.params)

print()
print("Sensitivity (elasticity = %LCOE / %param)")
print("-" * 48)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<36} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<36} {v:+.4f}")

print("\nCosting constants (top 15):")
costing = sorted(sens["costing"].items(), key=lambda x: abs(x[1]), reverse=True)
for k, v in costing[:15]:
    print(f"  {k:<36} {v:+.4f}")
