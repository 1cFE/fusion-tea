"""Laser ICF - French National Direct Drive (D-T) — GenF Systems / TARANIS.

Modeling approach:
  Implements the Ribeyre 2025 reactor model (AIP Advances 15(9):095013) as the
  primary technical basis.  GenF targets exactly 1 GWe net at 10 Hz — the
  model runs at the native 1 GWe design point (no dual-result scaling needed).

  Design is shock ignition (SI) direct drive: a lower-energy variant where a
  high-intensity laser spike at the end of the compression pulse ignites the
  hot spot.  This yields higher gain per unit laser energy than central ignition
  but introduces severe LPI risk (SRS, SBS, TPD) at the igniting-spike
  intensity — the dominant unresolved physics uncertainty.

Concept choice rationale:
  Direct drive offers 4–5× better laser-to-target coupling efficiency vs.
  indirect drive (genf-icf-article.md), requiring only 3 MJ per shot (vs.
  ~10 MJ for indirect drive at comparable gain).  This substantially reduces
  laser CAPEX but demands tighter beam uniformity and is more vulnerable to LPI.

Key deviations from defaults:
  - plasma_t = 8.0 m: Ribeyre §III requires 8 m chamber radius to keep X-ray
    flux below ~1 J/cm² (fused silica damage threshold for final optics).
    Default 4.0 m is not physically viable at 360 MJ/shot yield.
  - C220107 (laser driver): NOAK DPSSL estimate at 3 MJ; dominant cost item.
    Calibrated via Inertia indirect-drive analogue ($300/J NOAK × 3 MJ = $900M,
    +10% direct-drive beam-uniformity premium = ~$1,000M).
  - q_eng = 4.8: derived from Ribeyre physics (G × η_pin × G_b × η_th =
    120 × 0.10 × 1.0 × 0.40).  Implies P_gross ≈ 1440 MWe, laser electrical
    draw ≈ 300 MWe, P_net ≈ 1000 MWe (after aux loads).
  - eta_th = 0.40: Ribeyre §III specifies Rankine/gas-turbine at 40%; framework
    RANKINE preset defaults to this value, so no override needed.
  - availability = 0.75: no published IFE capacity factor model; first wall
    material selection is unresolved (IFSA25 Ialovega, no result published).
  - CAS27 = $8M: liquid Li blanket is cheap relative to PbLi/FLiBe default.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# ── Native design point ──────────────────────────────────────────────
# GenF's commercial target is exactly 1 GWe; no dual-result scaling needed.
# Source: genf-website-technology.md §GenF building the world first nuclear
#         fusion reactor (medium confidence — no engineering basis published)
NATIVE_MW = 1000.0

# ── Forward pass: 1 GWe (native design point) ────────────────────────
result = model.forward(
    net_electric_mw=NATIVE_MW,

    # ── Economics ───────────────────────────────────────────────────
    # UNCERTAIN: no IFE capacity factor model exists; first wall material
    # selection is unresolved (IFSA25 Ialovega, no published result).
    # 10 Hz pulsed X-ray/neutron loading at 360 MJ/shot makes scheduled
    # replacement interval highly uncertain — harsher than steady-state MFE.
    # Source: analysis.md §5 (Missing Parameters: capacity factor), §3 (First Wall)
    availability=0.75,
    lifetime_yr=30,
    # IFE construction simpler than tokamak (no magnet winding schedule).
    # Source: pulsed_laser_ife.yaml default
    construction_time_yr=5.0,
    interest_rate=0.07,
    inflation_rate=0.0245,
    n_mod=1,
    noak=True,

    # ── IFE power balance — Ribeyre 2025 design point ────────────────
    # q_eng = G × η_pin × G_b × η_th = 120 × 0.10 × 1.0 × 0.40 = 4.8
    # This gives: P_gross ≈ 1440 MWe, P_laser_elec = 3 MJ/0.10 × 10 Hz = 300 MWe,
    # recirculating fraction ~20.8% of gross, P_net ≈ 1000 MWe (with aux loads).
    # Source: aip-advances-ribeyre-2025.md §III. REACTOR MODEL (medium confidence)
    q_eng=4.8,

    # DPSSL wall-plug efficiency. LUCIA/Mercury/HALNA demonstrated 11.7–13%;
    # "10% seems realistic" at industrial scale per Ribeyre §III.
    # Source: aip-advances-ribeyre-2025.md §III. REACTOR MODEL (medium confidence)
    eta_pin=0.10,

    # 10 Hz repetition rate; consistent across all GenF sources.
    # Source: genf-website-technology.md §GenF building the world first... (high confidence)
    f_rep=10.0,

    # Rankine cycle (steam) or gas turbine at 40% thermal efficiency.
    # Ribeyre §III specifies this; consistent with framework RANKINE preset default.
    # Source: aip-advances-ribeyre-2025.md §III. REACTOR MODEL (medium confidence)
    eta_th=0.40,

    # Standard DT neutron energy multiplier; pulsed_laser_ife.yaml default
    mn=1.1,

    # DT radiation fraction; costing_constants.yaml f_rad_dt default
    f_rad=0.10,

    # Subsystem power fraction; pulsed_laser_ife.yaml default
    f_sub=0.03,

    # Liquid Li circulation pump power; pulsed_laser_ife.yaml default
    p_pump=1.0,

    # Tritium processing power; pulsed_laser_ife.yaml default.
    # Note: actual scale (>1 kg/day) is blocked by TBR feasibility constraint.
    p_trit=10.0,

    # Housekeeping power; pulsed_laser_ife.yaml default
    p_house=4.0,

    # Cryogenic power for DT target layering at 10 Hz; pulsed_laser_ife.yaml default
    p_cryo=0.5,

    # Target factory electrical load; pulsed_laser_ife.yaml default
    p_target=1.0,

    # ── Chamber geometry (spherical) ─────────────────────────────────
    # KEY OVERRIDE: 8 m chamber radius required by Ribeyre §III to keep X-ray
    # flux below ~1 J/cm² vaporization threshold at 360 MJ/shot yield.
    # Default 4.0 m is insufficient for this yield level; 8 m doubles the
    # blanket/shield volume costs relative to the default configuration.
    # Source: aip-advances-ribeyre-2025.md §III. REACTOR MODEL (medium confidence)
    plasma_t=8.0,

    # Liquid Li blanket thickness; pulsed_laser_ife.yaml default
    blanket_t=0.80,

    # High-temperature shield thickness; pulsed_laser_ife.yaml default
    ht_shield_t=0.25,

    # Primary structure thickness; pulsed_laser_ife.yaml default
    structure_t=0.15,

    # Vacuum vessel thickness; pulsed_laser_ife.yaml default
    vessel_t=0.10,

    # ── Cost overrides ───────────────────────────────────────────────
    cost_overrides={
        # UNCERTAIN: Laser driver system (DPSSL, shock ignition direct drive).
        #
        # FOAK basis: $700–1,000/J × 3 MJ = $2.1–3.0B (midpoint $2.6B).
        # Source: analysis.md §2 (Uncertainty 1), §5 Table (low confidence)
        #         [analogue: Inertia Enterprises Thunderwall DPSSL]
        #
        # NOAK pathway: same $/J learning trajectory as indirect-drive analogue.
        # Inertia NOAK: $300/J × 10 MJ = $3,000M.
        # GenF at 3 MJ: $300/J × 3 MJ = $900M (linear energy scaling).
        # +10% premium for direct-drive beam-uniformity complexity (more beam
        # paths, tighter phase-plate tolerances for symmetric illumination, LPI
        # mitigation optics geometry) → NOAK estimate ~$1,000M.
        # Range: $900M (Inertia analogue floor) to $3,000M (FOAK midpoint).
        # Requires laser diodes to reach ~$0.007/W viability target (current ~$0.02/W).
        # Source: analysis.md §2 (Uncertainty 1), §4 (Laser Diodes), §5 Table
        "C220107": 1000.0,

        # Special materials: liquid Li blanket.
        # Liquid Li inventory at IFE scale is inexpensive relative to FLiBe/PbLi.
        # Framework default ($15M at 1 GWe) assumes enriched Li-6 in PbLi blanket.
        # Li-6 enrichment supply chain is constrained globally but Li itself is cheap.
        # Source: analysis.md §4 (Chamber Wall Materials, Li-6 Enrichment); dossier.md
        "CAS27": 8.0,
    },
)

# ── Print results ────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Laser ICF - French National Direct Drive (D-T) — GenF Systems / TARANIS (NOAK)")
print(
    f"Native: {NATIVE_MW:.0f} MWe | Availability: 75%"
    f" | Lifetime: 30 yr | 10 Hz shock ignition direct drive"
)
print(f"LCOE: {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(
    f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW"
    f" | Q_eng: {pt.q_eng:.1f} | Q_sci: {pt.q_sci:.1f}"
)
print()

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

# ── CAS22 detail ─────────────────────────────────────────────────────
print("\nCAS22 Detail (Reactor Plant Equipment):")
cas22_labels = {
    "C220000": "Total CAS22",
    "C220101": "First wall + blanket",
    "C220102": "Shield",
    "C220103": "Coils / magnets",
    "C220104": "Heating / current drive",
    "C220105": "Primary structure",
    "C220106": "Vacuum system",
    "C220107": "Laser driver (DPSSL)            [OVERRIDE]",
    "C220108": "Target injection / removal",
    "C220109": "DEC",
    "C220111": "Installation",
    "C220112": "Isotope separation",
    "C220200": "Coolant handling",
    "C220300": "Auxiliary cooling",
    "C220400": "Rad waste",
    "C220500": "Fuel handling",
    "C220600": "Other equipment (target factory)",
    "C220700": "I&C",
}
print(f"{'Code':<10} {'Account':<44} {'M$':>10}")
print("-" * 66)
for k, v in result.cas22_detail.items():
    label = cas22_labels.get(k, k)
    print(f"{k:<10} {label:<44} {float(v):>10.1f}")

# ── Key assumptions ───────────────────────────────────────────────────
print("""
Key Assumptions (confidence / uncertainty level):
  1. DESIGN POINT: Ribeyre 2025 (AIP Advances 15(9):095013) is the only
     published physics model for this concept.  All physics parameters
     (G = 120, E_d = 3 MJ, 10 Hz, η_d = 10%, η_th = 40%, R_ch = 8 m) derive
     from this source.  GenF has not published independent specifications.
     Source: aip-advances-ribeyre-2025.md §III. REACTOR MODEL.

  2. TARGET GAIN G = 120 (medium confidence, UNCERTAIN): design point for
     shock ignition at 3 MJ.  LPI effects (SRS, SBS, TPD) are explicitly
     excluded from Ribeyre simulations; real gain may be substantially lower.
     NIF best Q_sci ≈ 2.5 using indirect drive at 2.2 MJ — direct drive at
     MJ scale with G ≈ 100+ has never been demonstrated.
     Source: aip-advances-ribeyre-2025.md §IV Conclusion; genf-icf-article.md.

  3. q_eng = 4.8 (medium confidence): derived from Ribeyre physics as
     G × η_pin × G_b × η_th = 120 × 0.10 × 1.0 × 0.40.  Implies P_gross ≈
     1440 MWe, laser electrical draw ≈ 300 MWe, net ≈ 1000 MWe with aux loads.
     Source: aip-advances-ribeyre-2025.md §III. REACTOR MODEL.

  4. NOAK laser driver = $1,000M (UNCERTAIN, low confidence): no GenF or Thales
     cost estimates published.  Derived via Inertia Enterprises indirect-drive
     analogue ($300/J NOAK × 3 MJ + 10% direct-drive uniformity premium).
     Requires diodes to reach ~$0.007/W viability target (current ~$0.02/W).
     FOAK range: $2.1–3.0B.  NOAK range: $900M (floor) to $3.0B (FOAK mid).
     Source: analysis.md §2 (Uncertainty 1), §4 (Laser Diodes), §5 Table.

  5. plasma_t = 8.0 m (medium confidence): directly from Ribeyre §III.
     Required to keep X-ray flux below ~1 J/cm² at 360 MJ/shot.  This doubles
     the chamber radius vs. framework default (4.0 m), significantly increasing
     blanket/shield volume costs.
     Source: aip-advances-ribeyre-2025.md §III. REACTOR MODEL.

  6. availability = 0.75 (UNCERTAIN, low confidence): no published IFE
     capacity factor model; first wall material selection unresolved (active
     research at IFSA25 per Ialovega, no result published).  Combined X-ray,
     neutron, and ion loading at 10 Hz is harsher than any demonstrated fusion
     environment.
     Source: analysis.md §5 (Missing Parameters: capacity factor), §6 Gap #5.

  7. TRITIUM BLOCKING CONSTRAINT (not captured in LCOE model): demonstrated
     TBR = 3.57×10⁻⁴; required TBR > 1.0 for fuel self-sufficiency — a gap
     of ~3,000×.  At 10 Hz, tritium consumption exceeds 1 kg/day vs. global
     CANDU supply <2 kg/yr (~180× shortfall before breeding is achieved).
     This is a feasibility constraint that cannot be reflected in LCOE.
     Source: aip-advances-ribeyre-2025.md §Another important reactor issue.

  8. CAS27 = $8M: liquid Li blanket inventory is inexpensive relative to
     FLiBe/PbLi framework default ($15M).  Li-6 enrichment is supply-
     constrained globally but unit cost is moderate.
     Source: analysis.md §4 (Li-6 Enrichment); dossier.md.

  9. eta_th = 40%: Ribeyre §III specifies Rankine cycle or gas turbine at
     this efficiency; consistent with framework RANKINE preset.
     Source: aip-advances-ribeyre-2025.md §III. REACTOR MODEL.

  10. Target factory (C220600): framework default used as placeholder ($244M
      at 1 GWe).  Goodin criterion requires <$2.78/target at 86,400 targets/day;
      GenF has published no target manufacturing cost data.
      Source: analysis.md §6 Gap #4.
""")

# ── Sensitivity analysis ──────────────────────────────────────────────
sens = model.sensitivity(
    result.params,
    cost_overrides={
        "C220107": 1000.0,
        "CAS27": 8.0,
    },
)

print("Sensitivity (elasticity = %LCOE / %param, evaluated at 1 GWe native)")
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
