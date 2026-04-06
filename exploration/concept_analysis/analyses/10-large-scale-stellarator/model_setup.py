# STALE: analysis-updated-iter-2
"""Large-Scale Stellarator (Gauss Fusion GIGA) — 1costingfe LCOE model.

Modeling approach
-----------------
GIGA is a quasi-isodynamic (QI) D-T stellarator derived from the HELIAS HSR4/18
reactor study (4 field periods, 18 m major radius, 1 GWe net output). The concept
has rich scientific heritage but no public CDR cost data; this model therefore:

  1. Anchors the overnight cost to the disclosed FOAK range (€15–18B ≈ $16–20B at
     ~1.1 $/€), expressed as a cost_override on CAS22.
  2. Treats NOAK learning as the primary sensitivity parameter (`noak_fraction`,
     0.40–0.70), which is described in the analysis as "the single most important
     modeling gap" (Section 2, Challenge #1).
  3. Uses the Helios/Thea Energy capacity factor (88%) as an engineering-grounded
     analog anchor (Section 2, Challenge #6; Section 5 table).
  4. Sets thermal efficiency from the HELIAS reference (35% gross, ~33% net after
     recirculating power), consistent with the HCPB/steam Rankine path (Section 5).

Key deviations from framework defaults
---------------------------------------
- R0: 18 m (vs. default 5.5 m) — GIGA geometry; gauss-fusion-technical-summary.md
- plasma_t: 1.7 m minor radius — gauss-fusion-technical-summary.md
- plasma_volume: 1500 m³ — gauss-fusion-technical-summary.md
- eta_th: 0.35 (gross) → 0.333 net-implied; using 0.35 as gross conversion
- availability: 0.88 (Helios analog anchor); sensitivity sweep covers 0.75–0.90
- CAS22 override: NOAK-adjusted overnight cost derived from FOAK disclosure
- p_input: 75 MW ECRH (startup/profile control only; no current drive needed)
- noak=True with explicit NOAK fraction applied to CAS22

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import sys

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ──────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# ── Plant configuration constants ────────────────────────────────────────────

# FOAK specific capital cost: €15,000–18,000/kWe × 1.10 $/€ → ~$16,500–19,800/kWe
# Midpoint: ~$18,150/kWe for 1 GWe = $18,150M overnight (FOAK)
# Source: gauss-fusion-technical-summary.md §Funding; analysis.md §Section 5 table
FOAK_OVERNIGHT_M_USD = 18_150.0   # M$ (FOAK midpoint: $18.15B)

# NOAK fraction: NOAK as a fraction of FOAK.
# Analysis Section 2, Challenge #1: "NOAK may be 40–60% of FOAK"
# Central estimate: 55% (midpoint of disclosed uncertainty range)
# Sensitivity sweep below covers 0.40–0.70.
NOAK_FRACTION_CENTRAL = 0.55

# Derived NOAK overnight cost at central estimate
NOAK_OVERNIGHT_M_USD = FOAK_OVERNIGHT_M_USD * NOAK_FRACTION_CENTRAL   # ~$9,982M

# CAS22 override: framework CAS22 covers reactor plant equipment.
# We allocate ~65% of overnight to CAS22 (analogous to tokamak cost structure),
# with the remainder distributed across other CAS accounts via framework defaults.
# UNCERTAIN: CAS22 fraction — no GIGA-specific cost breakdown published (CDR not public)
CAS22_FRACTION = 0.65   # fraction of overnight cost allocated to CAS22
CAS22_NOAK_M_USD = NOAK_OVERNIGHT_M_USD * CAS22_FRACTION   # ~$6,489M

# Remote handling premium: GIGA blanket has 80 segment shapes (vs ~2 for tokamak).
# Analysis Section 2, Challenge #3: 3D segment diversity raises fabrication and RH cost.
# DEFAULT: framework remote_handling_dt_base = 150 M$ at 1 GWe; apply 1.5× multiplier
# UNCERTAIN: No published GIGA RH cost estimate; factor-of-1.5 is engineering judgment.
RH_OVERRIDE_M_USD = 225.0   # M$ (150 × 1.5× for 3D blanket geometry complexity)

# Special materials: HCPB option uses beryllium pebble beds (~tens of tonnes).
# costing_constants.yaml note: "For HCPB concepts with beryllium neutron multiplier,
# override CAS27 to ~$200M."
# Analysis Section 4: HCPB uses Be neutron multiplier; DCLL does not.
# Using HCPB as reference path (He coolant at 445–485°C matches steam Rankine cycle).
CAS27_OVERRIDE_M_USD = 200.0   # M$ (HCPB path with Be multiplier)

# ── Forward model ────────────────────────────────────────────────────────────
result = model.forward(
    # ── Customer requirements ──────────────────────────────────────────────
    net_electric_mw=1000.0,
    # Source: gauss-fusion-technical-summary.md §GIGA Power Plant (stated design target)

    availability=0.88,
    # Helios/Thea Energy QA stellarator: 88% from ~84-day biennial outage
    # Source: arxiv-2512-08027v1.md §2 Summary of the design
    # Note: Helios is QA/planar at 8 m; GIGA is QI/non-planar at 18 m.
    # GIGA's 3D blanket may push outage duration higher (Section 2, Challenge #6).
    # 88% used as upper anchor; sensitivity sweep covers 0.75–0.90.

    lifetime_yr=40,
    # Source: gauss-fusion-technical-summary.md §GIGA Power Plant
    # "Magnet and vacuum vessel life: 40 years"

    n_mod=1,
    # Single-module FOAK/NOAK plant; no fleet aggregation at this stage

    construction_time_yr=10.0,
    # UNCERTAIN: No published schedule for GIGA.
    # Basis: ITER ~15 years (complex first-of-kind); W7-X ~9 years (complex SC stellarator).
    # GIGA is more complex than W7-X but has benefit of established HELIAS design heritage.
    # 10 years is a conservative NOAK estimate; FOAK likely 12–15 years.

    interest_rate=0.07,
    # DEFAULT: 7% real weighted cost of capital (framework default for FOAK fusion projects)

    inflation_rate=0.0245,
    # DEFAULT: 2.45% (framework default)

    noak=True,
    # Modeling NOAK state: fleet learning applied; FOAK contingency (10%) not included.
    # NOAK fraction vs. FOAK cost is the primary sensitivity parameter — see sweep below.

    # ── GIGA plasma geometry ───────────────────────────────────────────────
    R0=18.0,
    # Source: gauss-fusion-technical-summary.md §GIGA Power Plant
    # "HSR4/18 heritage (4 field periods, R=18m)"

    plasma_t=1.7,
    # Minor radius; Source: gauss-fusion-technical-summary.md §GIGA Power Plant

    elon=1.0,
    # Near-circular (stellarator); DEFAULT from mfe_stellarator.yaml

    blanket_t=0.60,
    # DEFAULT: mfe_stellarator.yaml
    # UNCERTAIN: No GIGA-specific blanket thickness published.
    # HELIAS HCPB design has ~0.55 m radial depth (helias-blanket-studies.md §3);
    # 0.60 m rounds up to account for 3D geometry integration depth.

    ht_shield_t=0.20,
    # DEFAULT: mfe_stellarator.yaml

    structure_t=0.15,
    # DEFAULT: mfe_stellarator.yaml

    vessel_t=0.10,
    # DEFAULT: mfe_stellarator.yaml

    # ── Plasma volume (explicit override) ──────────────────────────────────
    plasma_volume=1500.0,
    # Source: gauss-fusion-technical-summary.md §GIGA Power Plant

    # ── Power balance ──────────────────────────────────────────────────────
    p_input=75.0,
    # ECRH heating power (startup + profile control only; no current drive required).
    # UNCERTAIN: Gauss has not published ECRH specification.
    # Basis: analysis.md §Section 2, Challenge #6: "ECRH likely ~50–100 MW" at burning
    # plasma conditions. 75 MW is midpoint. Stellarator needs no NBI/ECRH for current
    # sustainment — this is purely auxiliary (profile control, impurity management).

    mn=1.1,
    # DEFAULT: mfe_stellarator.yaml (neutron energy multiplier)

    eta_th=0.35,
    # Gross thermal conversion efficiency — HCPB/steam Rankine path.
    # Source: helias-reactor-context.md §7: "~35% standard; >40% TAURO advanced"
    # Note: Net implied by 1 GWe / 3 GWth = 33.3%, consistent with 35% gross minus
    # ~5–7% recirculating power. If DCLL/sCO2 path chosen, eta_th → 0.40–0.42.
    # Analysis Section 2, Challenge #2 (blanket type uncertainty): HCPB is reference.

    eta_p=0.5,
    # DEFAULT: mfe_stellarator.yaml (pumping system efficiency)

    eta_pin=0.5,
    # DEFAULT: mfe_stellarator.yaml (ECRH wall-plug efficiency ~50–55%)
    # Source: analysis.md §Section 3, ECRH: "current wall-plug efficiency ~50–55%"

    eta_de=0.85,
    # DEFAULT: mfe_stellarator.yaml (direct energy conversion efficiency — not applicable
    # to D-T; value is placeholder consistent with framework)

    f_sub=0.03,
    # DEFAULT: mfe_stellarator.yaml (subsystem power fraction)

    f_dec=0.0,
    # No direct energy conversion for D-T stellarator

    p_coils=5.0,
    # Demountable joint ohmic dissipation + cryogenic load (coil power).
    # Basis: ~10,000 joints at ~1 nΩ × (100 kA)² = ~10 kW per joint → ~100 MW total
    # joint loss... but this is NOT the p_coils parameter (which is LV power to coil
    # infrastructure). Cryogenic load for LTS (~4K) dominates.
    # UNCERTAIN: Gauss has not published coil power budget.
    # Using 5 MW as estimate (slightly above mfe_stellarator.yaml default of 3 MW) to
    # account for higher cryogenic load from 40 large LTS coils vs. typical stellarator.
    # Source: analysis.md §Section 2, Challenge #5 (LTS vs. HTS cryogenic load)

    p_cool=20.0,
    # He coolant pumping power for HCPB at 8 MPa operating pressure.
    # UNCERTAIN: No published figure. Above default (15 MW) because GIGA's larger
    # blanket volume (1,500 m³ plasma volume, ~2,000 m² first wall area) implies
    # proportionally higher He coolant flow. Scaling from HELIAS reactor context.
    # Source: helias-blanket-studies.md §Table 5 (He coolant at 8 MPa / 445–485°C)

    p_pump=1.0,
    # DEFAULT: mfe_stellarator.yaml

    p_trit=10.0,
    # DEFAULT: mfe_stellarator.yaml (tritium processing power)
    # Note: GIGA requires ~55 kg/year throughput (analysis.md §Section 3, Tritium Fuel Cycle)
    # — consistent with ITER-class tritium system power draw.

    p_house=4.0,
    # DEFAULT: mfe_stellarator.yaml

    p_cryo=2.5,
    # Cryogenic system power for 40 LTS coils at 4 K (LTS track assumed for this model).
    # UNCERTAIN: No published cryogenic budget. Scaled above default (0.8 MW) to reflect
    # GIGA's 40-coil superconducting system at 18 m scale vs. smaller reference designs.
    # Source: analysis.md §Section 2, Challenge #5 (LTS cryogenic requirements)

    # ── Magnetic field ────────────────────────────────────────────────────
    B=6.0,
    # On-axis magnetic field.
    # Source: dossier.md §Driver Technology (explicitly stated)

    # ── Cost overrides ────────────────────────────────────────────────────
    cost_overrides={
        "CAS22": CAS22_NOAK_M_USD,
        # CAS22 (Reactor Plant Equipment): NOAK-adjusted overnight cost component.
        # Derivation: FOAK midpoint $18,150M × NOAK fraction 0.55 × CAS22 fraction 0.65
        # = ~$6,489M. This is the dominant cost account and the primary source of
        # LCOE uncertainty (analysis.md §Section 2, Challenge #1).
        # Source: gauss-fusion-technical-summary.md §Funding (FOAK base)

        "C220110": RH_OVERRIDE_M_USD,
        # CAS22 sub-account C220110 (Remote Handling & Maintenance Equipment):
        # 1.5× premium on framework DT base ($150M) for 3D blanket geometry with
        # 80 unique segment shapes per sector, complex 3D RH tooling requirement.
        # Source: analysis.md §Section 2, Challenge #3 (blanket geometry complexity)
        # UNCERTAIN: No published GIGA remote handling cost estimate.
        # Note: When C220110 is set alongside CAS22, the CAS22 override takes precedence
        # for the total; C220110 is recorded for sub-account breakdown transparency.

        "CAS27": CAS27_OVERRIDE_M_USD,
        # Special materials (HCPB path): Be neutron multiplier.
        # Source: costing_constants.yaml note: "For HCPB concepts with beryllium
        # neutron multiplier, override CAS27 to ~$200M."
        # Source: helias-blanket-studies.md §3.2 (Be pebble bed multiplier)
    },
)

# ── Results output ───────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Large-Scale Stellarator (Gauss Fusion GIGA) — 1 GWe, 88% availability, 40 yr")
print(f"NOAK fraction applied: {NOAK_FRACTION_CENTRAL:.0%} of FOAK (central estimate)")
print(f"FOAK overnight: ${FOAK_OVERNIGHT_M_USD/1000:.1f}B | NOAK overnight: ${NOAK_OVERNIGHT_M_USD/1000:.1f}B")
print()
print(f"LCOE: {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.1f}")
print()

# ── CAS breakdown ────────────────────────────────────────────────────────────
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
print("CAS22 sub-account detail (Reactor Plant Equipment):")
print("-" * 48)
try:
    cas22_detail = [
        ("CAS2201", "First Wall + Blanket",    c.cas2201),
        ("CAS2202", "Shield",                  c.cas2202),
        ("CAS2203", "Magnets",                 c.cas2203),
        ("CAS2204", "Vacuum Vessel",           c.cas2204),
        ("CAS2205", "Power Supplies",          c.cas2205),
        ("CAS2206", "Divertor",               c.cas2206),
        ("CAS2207", "Direct Energy Conv.",     c.cas2207),
        ("CAS2208", "Heating & CD",            c.cas2208),
        ("CAS2209", "Fuel Handling",           c.cas2209),
        ("CAS2210", "Remote Handling",         c.cas2210),
        ("CAS2211", "Installation",            c.cas2211),
    ]
    for code, name, val in cas22_detail:
        print(f"  {code:<10} {name:<26} {float(val):>10.1f}")
except AttributeError:
    print("  (CAS22 sub-accounts not available in this framework version)")

# ── Key assumptions summary ──────────────────────────────────────────────────
print()
print("=" * 60)
print("KEY ASSUMPTIONS")
print("=" * 60)
print(f"  FOAK overnight cost:     ${FOAK_OVERNIGHT_M_USD/1000:.2f}B")
print(f"    Source: gauss-fusion-technical-summary.md §Funding")
print(f"    (€15–18B at ~1.10 $/€ → midpoint ~$18.15B)")
print(f"  NOAK fraction (central): {NOAK_FRACTION_CENTRAL:.0%} of FOAK")
print(f"    Source: analysis.md §Section 2, Challenge #1")
print(f"    Range: 40–70% (sensitivity sweep below)")
print(f"  Capacity factor:         88% (Helios/Thea Energy analog)")
print(f"    Source: arxiv-2512-08027v1.md §2 (84-day biennial outage)")
print(f"    Note: GIGA-specific target undisclosed; 85–90% model range")
print(f"  Thermal efficiency:      35% (HCPB/steam Rankine)")
print(f"    Source: helias-reactor-context.md §7")
print(f"    Alt: 40%+ if DCLL/sCO2 path chosen")
print(f"  Construction time:       10 yr (NOAK estimate)")
print(f"    UNCERTAIN: No Gauss-published schedule")
print(f"  CAS22 allocation:        {CAS22_FRACTION:.0%} of NOAK overnight")
print(f"    UNCERTAIN: No CAS breakdown in public CDR")
print(f"  Blanket type:            HCPB assumed (He coolant, steam Rankine)")
print(f"    UNCERTAIN: Gauss internal decision, not disclosed")

# ── Sensitivity analysis ─────────────────────────────────────────────────────
sens = model.sensitivity(result.params)

print()
print("=" * 60)
print("SENSITIVITY ANALYSIS (elasticity = %LCOE / %param)")
print("=" * 60)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

# ── NOAK fraction sweep (primary uncertainty) ────────────────────────────────
print()
print("=" * 60)
print("NOAK FRACTION SWEEP (primary uncertainty — analysis.md §Section 2 H1)")
print("  FOAK overnight: ${:.1f}B | Capacity factor: {:.0%}".format(
    FOAK_OVERNIGHT_M_USD / 1000, 0.88))
print(f"  {'NOAK Fraction':<16} {'NOAK $/kWe':>12} {'LCOE $/MWh':>12}  Notes")
print("-" * 60)

noak_fractions = [0.40, 0.50, 0.55, 0.60, 0.70]
for frac in noak_fractions:
    noak_overnight = FOAK_OVERNIGHT_M_USD * frac
    cas22_override = noak_overnight * CAS22_FRACTION
    r = model.forward(
        net_electric_mw=1000.0,
        availability=0.88,
        lifetime_yr=40,
        n_mod=1,
        construction_time_yr=10.0,
        interest_rate=0.07,
        inflation_rate=0.0245,
        noak=True,
        R0=18.0,
        plasma_t=1.7,
        elon=1.0,
        blanket_t=0.60,
        ht_shield_t=0.20,
        structure_t=0.15,
        vessel_t=0.10,
        plasma_volume=1500.0,
        p_input=75.0,
        mn=1.1,
        eta_th=0.35,
        eta_p=0.5,
        eta_pin=0.5,
        eta_de=0.85,
        f_sub=0.03,
        f_dec=0.0,
        p_coils=5.0,
        p_cool=20.0,
        p_pump=1.0,
        p_trit=10.0,
        p_house=4.0,
        p_cryo=2.5,
        B=6.0,
        cost_overrides={
            "CAS22": cas22_override,
            "C220110": RH_OVERRIDE_M_USD,
            "CAS27": CAS27_OVERRIDE_M_USD,
        },
    )
    noak_kwe = noak_overnight * 1000 / 1000   # $/kWe (M$ * 1000 kW/MW / 1000 MW)
    notes = " ← central" if frac == NOAK_FRACTION_CENTRAL else ""
    notes += " ← competitive threshold (~$100/MWh)" if r.costs.lcoe < 105 else ""
    print(f"  {frac:<16.0%} {noak_overnight*1000/1000:>12,.0f} {r.costs.lcoe:>12.1f}  {notes}")

# ── Capacity factor sweep (H3) ────────────────────────────────────────────────
print()
print("=" * 60)
print("CAPACITY FACTOR SWEEP (H3: stellarator steady-state advantage)")
print(f"  NOAK fraction: {NOAK_FRACTION_CENTRAL:.0%} (central) | Overnight: ${NOAK_OVERNIGHT_M_USD/1000:.1f}B")
print(f"  {'Availability':<16} {'LCOE $/MWh':>12}  Notes")
print("-" * 60)

for avail in [0.75, 0.80, 0.85, 0.88, 0.90]:
    r = model.forward(
        net_electric_mw=1000.0,
        availability=avail,
        lifetime_yr=40,
        n_mod=1,
        construction_time_yr=10.0,
        interest_rate=0.07,
        inflation_rate=0.0245,
        noak=True,
        R0=18.0,
        plasma_t=1.7,
        elon=1.0,
        blanket_t=0.60,
        ht_shield_t=0.20,
        structure_t=0.15,
        vessel_t=0.10,
        plasma_volume=1500.0,
        p_input=75.0,
        mn=1.1,
        eta_th=0.35,
        eta_p=0.5,
        eta_pin=0.5,
        eta_de=0.85,
        f_sub=0.03,
        f_dec=0.0,
        p_coils=5.0,
        p_cool=20.0,
        p_pump=1.0,
        p_trit=10.0,
        p_house=4.0,
        p_cryo=2.5,
        B=6.0,
        cost_overrides={
            "CAS22": CAS22_NOAK_M_USD,
            "C220110": RH_OVERRIDE_M_USD,
            "CAS27": CAS27_OVERRIDE_M_USD,
        },
    )
    notes = " ← Helios analog anchor (arxiv-2512-08027v1)" if avail == 0.88 else ""
    notes = " ← pulsed tokamak (DEMO basis)" if avail == 0.80 else notes
    notes = " ← model central" if avail == 0.88 and not notes else notes
    print(f"  {avail:<16.0%} {r.costs.lcoe:>12.1f}  {notes}")
