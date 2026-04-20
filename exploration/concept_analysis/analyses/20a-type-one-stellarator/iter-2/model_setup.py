"""QI Modular HTS Stellarator - Infinity Two (Type One Energy) — LCOE estimate.

Modeling approach
-----------------
Infinity Two is the most thoroughly physics-documented private fusion concept
with six peer-reviewed JPP 2025 papers establishing R=12.5 m, A=10, Q>40,
800 MW D-T fusion, 350 MWe net, TBR=1.30 (HCPB+Be, OpenMC).  No capital cost,
LCOE estimate, or plant study has been published.

This script:
  1. Uses all published machine parameters directly (R0, A, B_ax, P_fus, P_net).
  2. Derives thermal efficiency from the published power balance (800 MW fusion
     × 1.15 blanket multiplier → ~920 MW thermal; net 350 MWe + ~65 MWe
     estimated recirculating → ~415 MWe gross; η_th ≈ 45%).  A conservative
     central estimate of 0.40 is used (steam Rankine with reheat) because the
     published bound is only "> 30%" and cycle type is unconfirmed.
  3. Derives ECRH power from the Q>40 constraint: P_ECRH ≤ 800/40 = 20 MW
     (microwave); actual Q likely >40 so 20 MW is a conservative upper bound.
  4. Overrides CAS27 (special materials) from the PbLi default to reflect the
     HCPB beryllium-pebble + Li-ceramic inventory (costing_constants.yaml note).
  5. Falls back to framework stellarator defaults for all uncharacterised cost
     accounts (magnets, vessel, blanket, divertor, maintenance, O&M).

The dominant cost risk — 3D HTS coil manufacturing (no cost precedent; W7-X LTS
magnets cost ~€1B) — cannot be captured in the framework without a published
figure.  C220103 (coils) uses the framework default, which likely understates
the true cost for non-planar REBCO winding.  This is a material downward bias on
total capital.

Concept choice rationale
------------------------
ConfinementConcept.STELLARATOR / Fuel.DT — confirmed by published design.
Steady-state operation eliminates current drive and disruption costs relative
to tokamak framework parameters; island divertor cost structure is approximated
by the framework's divertor account (C220108).

Key deviations from stellarator defaults
-----------------------------------------
- R0 = 12.5 m (vs default 5.5 m) — published
- plasma_t = 1.25 m (minor radius a = R0/A = 12.5/10) — derived from published values
- elon = 1.0 — near-circular cross-section; standard for large-A stellarator
- p_input = 20 MW (vs default 30 MW) — ECRH upper bound from Q>40
- mn = 1.15 (vs default 1.1) — HCPB blanket with Be multiplier (1.10–1.20 range)
- eta_th = 0.40 — UNCERTAIN; implied 38–42% from power balance; conservative estimate
- p_cryo = 1.5 MW (vs default 0.8 MW) — UNCERTAIN; HTS at 20–30 K but large coil set
- construction_time_yr = 10.0 — UNCERTAIN; 3D HTS coils + R=12.5 m scale
- CAS27 override = 70 M$ — HCPB + Be pebble inventory at 350 MWe (not PbLi default)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ──────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# ── Plant configuration ──────────────────────────────────────────────

# Customer-level requirements
NET_ELECTRIC_MW = 350.0     # Published: "delivers a nominal 350 MWe to the power grid"
                            # Source: analysis.md §Section 5;
                            #   typeoneenergy-type-one-energy-issues-first-realistic.md §Physics Solution

AVAILABILITY = 0.87         # UNCERTAIN: 2-year operating + 30-day maintenance cycle gives
                            # ~96% theoretical maximum (730/760 days).  No published availability
                            # target.  Conservative central estimate 87% (between 85–90% MCF
                            # literature range for steady-state designs per Araiinejad & Shirvan
                            # 2025; shifted toward upper half for stellarator steady-state advantage).
                            # Source: analysis.md §Section 5 (implied capacity factor);
                            #   Araiinejad & Shirvan (2025) ApplEnergy 401, 126567

LIFETIME_YR = 30            # DEFAULT: standard fusion plant lifetime assumption
CONSTRUCTION_TIME_YR = 10.0 # UNCERTAIN: R=12.5 m machine with 3D HTS non-planar coils —
                            # stellarator default 8 yr extended to 10 yr for scale;
                            # W7-X (LTS, smaller) took ~7 years of construction;
                            # Source: analysis.md §Section 3 (3D HTS TRL 2–3)

# ── Geometry (Infinity Two — published design) ───────────────────────

R0 = 12.5                   # Major radius [m]; 4-field-period QI/maximum-J configuration
                            # Source: analysis.md §Section 5; J. Plasma Phys. 2025 E65

ASPECT_RATIO = 10           # Published; large-aspect-ratio stellarator
                            # Source: analysis.md §Section 5; J. Plasma Phys. 2025 E65

PLASMA_T = R0 / ASPECT_RATIO  # Minor radius a = R0/A = 1.25 m; derived from published values

ELON = 1.0                  # Near-circular cross-section; standard for large-A stellarator;
                            # stellarator framework default

BLANKET_T = 0.80            # DEFAULT: HCPB blanket radial build not published;
                            # framework stellarator default applied.  HCPB pebble bed +
                            # Be multiplier + helium coolant structure consistent with 0.8 m.
                            # Source: analysis.md §Section 5 Missing Parameters

HT_SHIELD_T = 0.20          # DEFAULT: framework stellarator default
STRUCTURE_T = 0.15          # DEFAULT: framework stellarator default
VESSEL_T = 0.10             # DEFAULT: framework stellarator default

# ── Power balance ─────────────────────────────────────────────────────

ETA_TH = 0.40               # UNCERTAIN: thermal conversion efficiency.  Published bound only
                            # "> 30%" (dossier.md — "Rankine with reheat").  Power balance
                            # derivation: 800 MW × 1.15 blanket mult. = 920 MW thermal;
                            # 350 MWe net + ~65 MWe recirculating → ~415 MWe gross;
                            # η_th = 415/920 ≈ 0.45.  Conservative central estimate 0.40
                            # (steam Rankine, below the derived upper bound) because exact
                            # recirculating power and cycle type are unconfirmed.
                            # Source: analysis.md §Section 2, Challenge 3;
                            #   analysis.md §Section 5 (Missing Parameters: thermal efficiency)

ETA_PIN = 0.52              # ECRH gyrotron wall-plug efficiency.  Current-generation gyrotrons
                            # achieve ~50–55%.  Central estimate 52%.
                            # Source: analysis.md §Section 3 (ECRH TRL 5–7);
                            #   W7-X gyrotron specifications (140 GHz, 1 MW CW)

P_INPUT_MW = 20.0           # ECRH microwave power: upper bound from Q>40.
                            # P_ECRH = P_fus / Q = 800 / 40 = 20 MW (at Q=40).
                            # Actual Q likely >40 so 20 MW is conservative upper bound.
                            # Source: analysis.md §Section 5 (HCPB ECRH power ≤ 20 MW)

MN = 1.15                   # UNCERTAIN: neutron energy multiplier for HCPB blanket with Be
                            # multiplier.  Range 1.10–1.20 for HCPB+Be; central estimate 1.15.
                            # Source: analysis.md §Section 5; J. Plasma Phys. 2025 E86
                            #   (TBR=1.30 confirmed for HCPB+Be configuration)

ETA_P = 0.5                 # DEFAULT: pumping efficiency
ETA_DE = 0.85               # DEFAULT: DEC efficiency (DEC not used — f_dec=0)

F_SUB = 0.03                # DEFAULT: subsystem power fraction of gross electric
F_DEC = 0.0                 # No direct energy conversion; stellarator steady-state, ECRH only

P_COILS = 3.0               # DEFAULT: framework stellarator default; 3D HTS coils at 20–30 K
                            # have very low resistive losses; cryo overhead captured in p_cryo.
                            # Source: analysis.md §Section 3 (HTS coil TRL 6–8)

P_COOL = 15.0               # DEFAULT: framework stellarator default; HCPB helium primary
                            # coolant circuit pumping; no Infinity Two-specific data.

P_PUMP = 1.0                # DEFAULT: framework stellarator default

P_TRIT = 10.0               # DEFAULT: tritium processing power for 2-year continuous cycle.
                            # HCPB tritium extraction at kg/day throughput is not characterised.
                            # Source: analysis.md §Section 2, Challenge 6 (tritium constraint)

P_HOUSE = 4.0               # DEFAULT: housekeeping
P_CRYO = 1.5                # UNCERTAIN: HTS at 20–30 K has lower cryo load than LTS at 4 K,
                            # but Infinity Two has a large coil set (R=12.5 m, ~40 coils).
                            # Slightly above default 0.8 MW; no published figure.
                            # Source: analysis.md §Section 3 (HTS TRL 6–8, REBCO at 20–30 K)

# ── Financial parameters ──────────────────────────────────────────────

INTEREST_RATE = 0.07        # DEFAULT: standard project finance assumption
INFLATION_RATE = 0.0245     # DEFAULT: US long-run CPI target
NOAK = True                 # NOAK reference case (no contingency, mature supply chain).
                            # NOTE: 3D HTS coil manufacturing is TRL 2–3 — a true NOAK
                            # scenario requires demonstrated winding capability, which does
                            # not yet exist.  NOAK is aspirational for this concept.

# ── Cost overrides ────────────────────────────────────────────────────

# CAS27: Special Materials — HCPB beryllium pebbles + Li-ceramic pebble inventory.
# The framework default (15 M$ at 1 GWe) assumes PbLi blanket.  HCPB with Be
# multiplier requires: Be pebbles (~$850/kg nuclear grade, multi-tonne inventory),
# Li₄SiO₄/Li₂TiO₃ ceramic pebbles (enriched Li-6), and initial coolant inventory.
# costing_constants.yaml note: "For HCPB concepts with beryllium neutron multiplier,
# override CAS27 to ~$200M" (at 1 GWe reference).  Scaled to 350 MWe proportionally
# (linear with fusion power): 200 × (350/1000) ≈ 70 M$.
# Source: costing_constants.yaml §CAS27; analysis.md §Section 4 (Be supply chain)
COST_OVERRIDES = {
    "CAS27": 70.0,          # UNCERTAIN: HCPB+Be special materials at 350 MWe native power
}

# ── Shared kwargs (used for both native and 1 GW forward passes) ──────

_SHARED_KWARGS = dict(
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=NOAK,

    # Infinity Two geometry (published)
    R0=R0,                          # 12.5 m — published J. Plasma Phys. E65
    plasma_t=PLASMA_T,              # 1.25 m — derived from R0/A = 12.5/10
    elon=ELON,                      # 1.0 — near-circular stellarator cross-section (DEFAULT)
    blanket_t=BLANKET_T,            # 0.80 m — DEFAULT (HCPB radial build not published)
    ht_shield_t=HT_SHIELD_T,        # 0.20 m — DEFAULT
    structure_t=STRUCTURE_T,        # 0.15 m — DEFAULT
    vessel_t=VESSEL_T,              # 0.10 m — DEFAULT

    # Power balance
    p_input=P_INPUT_MW,             # 20 MW — ECRH upper bound from Q>40
    mn=MN,                          # 1.15 — UNCERTAIN (HCPB+Be multiplier)
    eta_th=ETA_TH,                  # 0.40 — UNCERTAIN (steam Rankine; implied 38–42%)
    eta_p=ETA_P,                    # 0.5 — DEFAULT
    eta_pin=ETA_PIN,                # 0.52 — gyrotron wall-plug efficiency
    eta_de=ETA_DE,                  # 0.85 — DEFAULT (DEC not used)
    f_sub=F_SUB,                    # 0.03 — DEFAULT
    f_dec=F_DEC,                    # 0.0 — no DEC
    p_coils=P_COILS,                # 3.0 MW — DEFAULT (HTS, low resistive loss)
    p_cool=P_COOL,                  # 15.0 MW — DEFAULT (HCPB He coolant circuit)
    p_pump=P_PUMP,                  # 1.0 MW — DEFAULT
    p_trit=P_TRIT,                  # 10.0 MW — DEFAULT (2-yr continuous tritium extraction)
    p_house=P_HOUSE,                # 4.0 MW — DEFAULT
    p_cryo=P_CRYO,                  # 1.5 MW — UNCERTAIN (HTS large coil set)

    # Cost overrides
    cost_overrides=COST_OVERRIDES,  # CAS27: HCPB+Be special materials override
)

# ── Model forward passes ──────────────────────────────────────────────

# Native design point: 350 MWe (published net output)
result = model.forward(net_electric_mw=NET_ELECTRIC_MW, **_SHARED_KWARGS)

# Self-consistent 1 GW result for cross-concept comparison.
# override_reference_mw tells the framework that cost_overrides values (CAS27=70 M$)
# are valid at 350 MWe and should scale to 1000 MWe using per-account scaling laws.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=NET_ELECTRIC_MW,
    **_SHARED_KWARGS,
)

# ── Results ───────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("QI Modular HTS Stellarator — Infinity Two (Type One Energy)")
print(f"  Config: {NET_ELECTRIC_MW:.0f} MWe net | {AVAILABILITY:.0%} availability | {LIFETIME_YR} yr | NOAK")
print(f"  Geometry: R0={R0} m, A={ASPECT_RATIO}, a={PLASMA_T:.2f} m, κ={ELON}")
print(f"  Field: B_ax=9 T on-axis | Heating: ECRH-only (η_pin={ETA_PIN})")
print(f"  Thermal eff.: η_th={ETA_TH} (UNCERTAIN — steam Rankine; implied 38–42%)")
print(f"  Blanket: HCPB + Be multiplier | TBR=1.30 (OpenMC, JPP E86)")
print()
print(f"LCOE:       {c.lcoe:.1f} $/MWh  [LOWER BOUND — coil cost (elasticity +0.99) uses framework default, likely understated]")
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
print(f"  Net electric (published):                  {NET_ELECTRIC_MW:.0f} MWe  [HIGH confidence]")
print(f"  Major radius R0:                           {R0} m  [HIGH confidence]")
print(f"  Aspect ratio A → minor radius:             {ASPECT_RATIO} → {PLASMA_T:.2f} m [HIGH confidence]")
print(f"  On-axis field B:                           9 T      [HIGH confidence]")
print(f"  Fusion power:                              800 MW   [HIGH confidence]")
print(f"  Q (fusion gain):                           > 40     [HIGH confidence]")
print(f"  TBR (HCPB+Be, OpenMC):                    1.30     [HIGH confidence]")
print(f"  Elongation κ (near-circular stellarator):  {ELON}    [DEFAULT — large-A stellarator]")
print(f"  Thermal efficiency η_th:                   {ETA_TH}   [UNCERTAIN — implied 38–42%; > 30% only bound]")
print(f"  ECRH power p_input:                        {P_INPUT_MW:.0f} MW  [MEDIUM — derived upper bound from Q>40]")
print(f"  Heating η_pin (gyrotron):                  {ETA_PIN}   [MEDIUM — W7-X gyrotron analogue]")
print(f"  Availability:                              {AVAILABILITY:.0%}   [UNCERTAIN — no published target; 2-yr cycle → 96% max]")
print(f"  Construction time:                         {CONSTRUCTION_TIME_YR:.0f} yr   [UNCERTAIN — 3D HTS coil complexity]")
print(f"  CAS27 special materials (HCPB+Be):         {COST_OVERRIDES['CAS27']:.0f} M$  [UNCERTAIN — scaled from $200M/GWe reference]")
print(f"  C220103 coils (3D HTS):                    FRAMEWORK DEFAULT — likely underestimates significantly")
print(f"    (W7-X LTS magnets ~€1B; Infinity Two 3D HTS has no cost precedent)")
print(f"  All other capital accounts:                FRAMEWORK DEFAULTS — no published cost data")
print(f"  NOAK assumption:                           Aspirational; 3D HTS winding not yet demonstrated (TRL 2–3)")

# ── Coil cost scenario sweep ──────────────────────────────────────────
# C220103 (3D HTS coils) has elasticity ≈ +0.99 — the highest in the model —
# and uses the framework default, which is acknowledged as a likely underestimate
# relative to W7-X LTS magnets (~€1B for a smaller machine with simpler LTS coils).
# A 2× error in coil cost produces nearly a 2× error in LCOE.  Present LCOE as a
# range across plausible coil cost realizations rather than a single point estimate.
_base_coil = float(result.cas22_detail["C220103"])
_shared_no_overrides = {k: v for k, v in _SHARED_KWARGS.items() if k != "cost_overrides"}

print()
print("=" * 60)
print("Coil Cost Scenario Sweep (C220103 — 3D HTS, elasticity ~+0.99)")
print("=" * 60)
print(f"  Framework default C220103 = {_base_coil:.1f} M$  (1× baseline, lower bound)")
print(f"  W7-X LTS reference: ~\u20ac1B for magnets on a smaller, simpler machine")
print(f"  3\u00d7 / 5\u00d7 bracket plausible non-planar REBCO winding premium")
print()
print(f"  {'Multiplier':<16} {'C220103 (M$)':>14} {'LCOE 350MWe':>14} {'LCOE 1GW':>12}")
print("  " + "-" * 58)
_coil_lcoe_native = []
for mult in [1, 3, 5]:
    _ov = {**COST_OVERRIDES, "C220103": _base_coil * mult}
    _rc = model.forward(net_electric_mw=NET_ELECTRIC_MW, cost_overrides=_ov, **_shared_no_overrides)
    _rc1gw = model.forward(
        net_electric_mw=1000.0, override_reference_mw=NET_ELECTRIC_MW,
        cost_overrides=_ov, **_shared_no_overrides,
    )
    _coil_lcoe_native.append(_rc.costs.lcoe)
    _tag = "  ← lower bound" if mult == 1 else ""
    print(f"  {mult}\u00d7{_tag:<14} {_base_coil * mult:>14.1f} {_rc.costs.lcoe:>12.1f} $/MWh {_rc1gw.costs.lcoe:>8.1f} $/MWh")
print()
print(f"  LCOE range (350 MWe): {_coil_lcoe_native[0]:.0f}\u2013{_coil_lcoe_native[-1]:.0f} $/MWh depending on 3D HTS coil cost realization")
print(f"  The 1\u00d7 base case ({_coil_lcoe_native[0]:.0f} $/MWh) IS A LOWER BOUND and should not be cited as a central estimate.")

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
