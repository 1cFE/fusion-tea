"""Negative Triangularity (NT) Tokamak — LCOE model setup (Firefly Fusion / MANTA proxy).

Modeling approach:
  The only published NT tokamak engineering reference is MANTA (Rutherford et al. 2024),
  a community-authored 90 MWe pilot plant study. Firefly Fusion (the target company)
  has disclosed only aspirational parameters (R=2–2.5 m, B=10–12 T, P_fus=50–100 MW)
  and no plant-level cost data. This script uses MANTA as the physics and cost anchor.

  The native result is at MANTA's 90 MWe design point. A second forward() call scales
  to 1 GWe using per-account cost scaling laws via override_reference_mw=90.0.

Key deviations from framework defaults:
  - R0=4.55 m, plasma_t=1.2 m, elon=1.1 (MANTA geometry; NT has near-circular cross-section)
  - p_input=40 MW all-ICRF (MANTA §2.1); NBI zeroed out
  - eta_th=0.38 (back-calculated from MANTA power balance: 539 MW thermal → 90 MWe net
    via steam Rankine with intermediate FLiBe-to-molten-salt HX step)
  - C220103 (TF coils) = 1500 M$ at 90 MWe — MANTA §7.1 dominant cost driver
  - C220108 (divertor) reduced 60% vs PT default: NT's P_SOL=23.5 MW (5.2% of P_fus)
    enables conventional tungsten monoblock without exotic divertor concepts

Concept choice rationale:
  ConfinementConcept.TOKAMAK + Fuel.DT — NT geometry is a positive-triangularity tokamak
  variant; same confinement family, same D-T fuel cycle requirements, same costing structure.
  NT-specific features (simplified divertor, potential ohmic-only operation) are captured
  through cost_overrides rather than a separate concept class.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# ── Plant Configuration ─────────────────────────────────────────────────────
# All parameters sourced from MANTA reference design unless otherwise noted.
# MANTA: Rutherford et al. 2024, arXiv:2405.20243 — iter-02/sources/manta-reference-design.md

_SHARED_KWARGS = dict(
    # ── Operations ──────────────────────────────────────────────────────────
    availability=0.80,          # UNCERTAIN: MANTA pilot ~37% (maintenance-heavy);
                                # commercial target 75–90% per Araiinejad & Shirvan 2025
                                # [01-hts-compact-tokamak analysis §4]. Using 80% for
                                # commercial plant comparison.
    lifetime_yr=30,             # Standard fusion plant economic lifetime assumption
    n_mod=1,                    # Single-module plant
    construction_time_yr=7.0,   # UNCERTAIN: no Firefly/MANTA estimate; 7 yr typical
                                # for first-of-kind fusion pilot plant
    interest_rate=0.07,         # Standard project finance assumption
    inflation_rate=0.0245,      # US long-run CPI target
    noak=True,                  # Nth-of-a-kind; MANTA cost estimate is NOAK-adjacent

    # ── Geometry (MANTA §Table 1) ────────────────────────────────────────────
    R0=4.55,          # Major radius [m]; manta-reference-design.md §Table 1
    plasma_t=1.2,     # Minor radius a [m]; aspect ratio A=3.79 per MANTA §Table 1
    elon=1.1,         # UNCERTAIN: NT geometry is near-circular; MANTA does not publish
                      # kappa directly. NT L-mode favors kappa~1.0–1.2 vs ~1.7 for PT H-mode.
    blanket_t=0.80,   # FLiBe liquid immersion blanket effective thickness [m];
                      # MANTA uses toroidally continuous FLiBe tank serving as
                      # breeder + coolant + shield; manta-reference-design.md §5.1
    ht_shield_t=0.20, # High-temperature shield — framework default
    structure_t=0.20, # Primary structure — framework default
    vessel_t=0.20,    # V-4Cr-4Ti vacuum vessel (~1 cm thick but 20 cm assembly depth);
                      # manta-reference-design.md §5.3

    # ── Power Balance (MANTA) ────────────────────────────────────────────────
    # Derived: P_fus=450 MW, Q=11.5, P_aux=40 MW ICRF, mn=1.11, P_net=90 MWe
    # eta_th back-calculated: P_thermal = 450×1.11 + 40 = 539.5 MW;
    #   recirculating ≈ 40/0.5 + 3+1.5+15+1+10+4 = 114.5 MW;
    #   gross = 90 + 114.5 = 204.5 MW; eta_th = 204.5/539.5 ≈ 0.38
    # Cycle: steam Rankine via NaNO3/KNO3 secondary; limited by FLiBe-to-salt HX
    # "low technological readiness level" — manta-reference-design.md §6.3
    p_input=40.0,     # Total auxiliary heating [MW]; manta-reference-design.md §2.1
    p_nbi=0.0,        # No NBI — MANTA uses ICRF exclusively
    p_icrf=40.0,      # 40 MW He-3 minority ICRF at 110 MHz; manta-reference-design.md §2.1
    mn=1.11,          # Blanket power multiplication (FLiBe TBR=1.15 design);
                      # manta-reference-design.md §5.1
    eta_th=0.38,      # Thermal-to-electric efficiency; back-calculated from MANTA
                      # power balance (see derivation in docstring)
    eta_pin=0.50,     # ICRF wall-plug efficiency; framework default for RF heating
    eta_p=0.50,       # Pumping efficiency — framework default
    eta_de=0.85,      # Direct energy conversion efficiency — unused (f_dec=0.0)
    f_sub=0.03,       # Subsystem power fraction — framework default
    f_dec=0.0,        # No DEC — standard tokamak thermal cycle
    p_coils=3.0,      # UNCERTAIN: HTS coil power at 20 K (liquid H2 cooling);
                      # MANTA targets REBCO at 11 T, 47.2 kA; cryogenic load ~1-3 MW
                      # for HTS vs ~50 MW for LTS; manta-reference-design.md §4
    p_cool=15.0,      # Coolant pump power [MW] — framework default, consistent with
                      # FLiBe primary + molten-salt secondary loop
    p_pump=1.0,       # Vacuum/gas pumping [MW] — framework default
    p_trit=10.0,      # Tritium processing power [MW] — framework default for D-T
    p_house=4.0,      # Housekeeping [MW] — framework default
    p_cryo=1.5,       # Cryogenic power [MW]; elevated vs default (0.5) for LH2
                      # cooling of REBCO at 20 K; manta-reference-design.md §4

    # ── Cost Overrides ───────────────────────────────────────────────────────
    cost_overrides={
        # TF coil cost — the dominant MANTA cost driver ($1.5B of $3.4B total).
        # 18 REBCO TF coils at 11 T, 47.2 kA, demountable joints, 20 K LH2 cooling.
        # Source: manta-reference-design.md §7.1, §Abstract ("most critical upfront cost")
        "C220103": 1500.0,

        # Divertor — NT advantage: P_SOL = 23.5 MW for 450 MW fusion (5.2%) vs
        # 15–25% for comparable positive-triangularity design. Conventional tungsten
        # monoblock at 2.8 MW/m² peak heat flux — within demonstrated limits,
        # no exotic Super-X/snowflake/liquid-metal divertor required.
        # UNCERTAIN: not separately quantified in MANTA; estimated as ~40% of
        # framework default to reflect simpler engineering and reduced replacement rate.
        # Source: manta-reference-design.md §3, §Table 1
        "C220108": 24.0,

        # Heating system — 40 MW ICRF (He-3 minority at 110 MHz).
        # Estimate: ~$150M for fusion-environment ICRF antenna + RF power system
        # at 40 MW, based on JET ICRF analogue (~€100M at 35 MW, scaled for
        # neutron-hardened design). UNCERTAIN: MANTA does not separately publish
        # heating system cost; "detailed antenna design outside scope" — §2.1.
        # If Ball et al. ohmic-only scenario validated, this account → $0.
        "C220104": 150.0,
    },
)

# Native design point: MANTA 90 MWe pilot plant
result = model.forward(net_electric_mw=90.0, **_SHARED_KWARGS)

# 1 GWe scaled result — per-account scaling from 90 MWe reference
# cost_overrides values (C220103, C220108, C220104) are defined at 90 MWe;
# override_reference_mw tells the framework to scale them to 1000 MWe.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=90.0,
    **_SHARED_KWARGS,
)

# ── Results ─────────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("=" * 65)
print("Negative Triangularity Tokamak (Firefly/MANTA proxy)")
print("Native design point: 90 MWe pilot plant (MANTA reference)")
print("=" * 65)
print(f"LCOE:          {c.lcoe:.1f} $/MWh")
print(f"Overnight:     {c.overnight_cost:.0f} $/kW")
print(f"Fusion power:  {pt.p_fus:.0f} MW  (MANTA ref: 450 MW)")
print(f"Net electric:  {pt.p_net:.0f} MWe (MANTA ref: 90 MWe)")
print(f"Q_eng:         {pt.q_eng:.2f}    (MANTA ref: Q=11.5, Q_e=2.4)")
print()

# CAS breakdown
cas = [
    ("CAS10", "Preconstruction",          c.cas10),
    ("CAS21", "Buildings",                c.cas21),
    ("CAS22", "Reactor Plant Equipment",  c.cas22),
    ("CAS23", "Turbine Plant",            c.cas23),
    ("CAS24", "Electrical Plant",         c.cas24),
    ("CAS25", "Miscellaneous",            c.cas25),
    ("CAS26", "Heat Rejection",           c.cas26),
    ("CAS27", "Special Materials",        c.cas27),
    ("CAS28", "Digital Twin",             c.cas28),
    ("CAS29", "Contingency",              c.cas29),
    ("CAS30", "Indirect Costs",           c.cas30),
    ("CAS40", "Owner's Costs",            c.cas40),
    ("CAS50", "Supplementary",            c.cas50),
    ("CAS60", "IDC",                      c.cas60),
    ("CAS70", "O&M (annualized)",         c.cas70),
    ("CAS80", "Fuel (annualized)",        c.cas80),
    ("CAS90", "Financial",                c.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")
print(f"  [MANTA reference overnight cost: $3,400M at 90 MWe]")

# CAS22 detail
print()
print("CAS22 Sub-Accounts:")
print("-" * 48)
cas22_labels = {
    "C220101": "First Wall + Blanket (FLiBe)",
    "C220102": "Shield",
    "C220103": "TF/PF/CS Coils [MANTA $1,500M]",
    "C220104": "Heating (40 MW ICRF) [est]",
    "C220105": "Structure",
    "C220106": "Vacuum System",
    "C220107": "Power Supplies",
    "C220108": "Divertor [NT-simplified]",
    "C220109": "DEC",
    "C220111": "Installation",
    "C220112": "Isotope Separation",
    "C220200": "Coolant (FLiBe+NaNO3/KNO3)",
    "C220300": "Auxiliary Cooling",
    "C220400": "Rad Waste",
    "C220500": "Fuel Handling (tritium)",
    "C220600": "Other Equipment",
    "C220700": "I&C",
    "C220000": "CAS22 Total",
}
for k, label in cas22_labels.items():
    if k in result.cas22_detail:
        print(f"  {k}  {label:<36} {float(result.cas22_detail[k]):>9.1f} M$")

# 1 GWe result
c1 = result_1gw.costs
pt1 = result_1gw.power_table
print()
print("=" * 65)
print("1 GWe Scaled Result (per-account scaling from 90 MWe reference)")
print("=" * 65)
print(f"LCOE:          {c1.lcoe:.1f} $/MWh")
print(f"Overnight:     {c1.overnight_cost:.0f} $/kW")
print(f"Fusion power:  {pt1.p_fus:.0f} MW")
print(f"Net electric:  {pt1.p_net:.0f} MWe")
print(f"Q_eng:         {pt1.q_eng:.2f}")

# Key Assumptions
print()
print("=" * 65)
print("Key Assumptions")
print("=" * 65)
print("""
Physics anchor:
  MANTA (Rutherford et al. 2024) — 90 MWe NT tokamak pilot plant.
  All Firefly Fusion parameters are aspirational; MANTA is the only
  published engineering reference for NT tokamak economics.

NT-specific cost adjustments vs. positive-triangularity baseline:
  C220103 (coils):   $1,500M @ 90 MWe — MANTA §7.1 (dominant driver)
  C220104 (heating): $150M — 40 MW ICRF; eliminates if ohmic-only validated
  C220108 (divertor): $24M — 60% reduction vs PT; conventional W monoblock
                       enabled by P_SOL = 23.5 MW (5.2% of P_fus)

Ohmic-only scenario (not modeled here):
  Ball et al. (2024) show ohmic-only NT could reach Q~500, eliminating
  $150M ICRF system (~4% of overnight cost). If validated, C220104 → $0.

Critical uncertainties (in order of LCOE impact):
  1. NT confinement scaling to burning plasma — H_NA=2 unvalidated (TRL 2-3)
  2. Commercial-scale NT cost study nonexistent — MANTA is sub-commercial
  3. FLiBe-to-molten-salt HX — "low TRL" (MANTA §6.3); affects eta_th
  4. Availability 80% assumed for commercial plant vs. MANTA pilot 37%
  5. TF coil replacement lifetime: ~3100 ± 400 MW·yr (MANTA §5.2)
     PF2 limiting: ~890 MW·yr (~2 FPY maintenance cycle driver)

Capacity factor note:
  MANTA pilot capacity factor ~37% (planned maintenance + pilot operations).
  Commercial plant target 75-90% per Araiinejad & Shirvan 2025.
  This model uses 80% — results are sensitive to this assumption.
""")

# ── Sensitivity Analysis ─────────────────────────────────────────────────────
print("=" * 65)
print("Sensitivity Analysis (elasticity = %ΔLCOE / %Δparam)")
print("=" * 65)

sens = model.sensitivity(result.params, cost_overrides=_SHARED_KWARGS["cost_overrides"])

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
