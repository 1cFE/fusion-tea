"""Laser ICF - Indirect Drive (D-T) — Inertia Enterprises / Xcimer Energy.

Modeling approach:
  Models the Inertia Enterprises indirect-drive DPSSL architecture (Thunderwall)
  as the primary design point.  Xcimer (KrF, HDD) is noted in comments but not
  separately modeled here; their Hybrid Direct Drive physics may warrant a
  separate concept entry (analysis.md §7 cross-concept note).

  Native design: ~1.5 GWe at Q_eng ~4, 10 Hz rep rate, 10 MJ DPSSL driver.
  Since this diverges from 1 GWe, the dual-result pattern is used to also
  produce a self-consistent 1 GWe comparison point.

Key deviations from defaults:
  - C220107 (laser driver): overridden to NOAK DPSSL estimate — dominant cost,
    no published bottom-up breakdown; framework default ($80M) is tokamak-scale.
  - CAS27 (special materials): liquid Li blanket is cheap; FLiBe/PbLi default
    grossly overstates material cost for an Li-pipe design.
  - eta_th = 0.35: steam Rankine (Inertia references steam in public materials;
    Xcimer's 45% helium Brayton is unconfirmed for any design).
  - availability = 0.75: conservative placeholder; no published IFE capacity
    factor model exists; 3-5 yr chamber replacement (Inertia claim) drives
    scheduled downtime.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# ── Native design point ──────────────────────────────────────────────
# Inertia's published target: ~1.5 GWe net.
# Source: inertia-enterprises-website-and-faq.md §Plant Output (medium confidence)
NATIVE_MW = 1500.0

# ── Shared parameters ────────────────────────────────────────────────
_SHARED_KWARGS = dict(
    # ── Economics ───────────────────────────────────────────────────
    # UNCERTAIN: no published IFE capacity factor model in any source.
    # 3-5 yr chamber replacement (Inertia claim) → scheduled downtime.
    # Cross-concept: Xcimer claims "no structural wall replacement" for
    # liquid-wall design, but unverified.
    # Source: analysis.md §5 (Missing Parameters: capacity factor)
    availability=0.75,
    lifetime_yr=30,
    # IFE construction simpler than tokamak (no magnet winding schedule).
    # pulsed_laser_ife.yaml default
    construction_time_yr=5.0,
    interest_rate=0.07,
    inflation_rate=0.0245,
    n_mod=1,
    noak=True,

    # ── IFE power balance — Inertia Enterprises design point ─────────
    # Q_engineering ~4: gross ~2 GWe, recirculating ~500 MW.
    # Source: handwritten/26-laser-icf-indirect-drive.md §Table 1 (low confidence)
    q_eng=4.0,

    # Thunderwall: 10% wall-plug efficiency (design target, not demonstrated).
    # Source: inertia-enterprises-2026-update.md §Thunderwall Specs (medium confidence)
    eta_pin=0.10,

    # 1,000 beamlines × 10 kJ × 10 Hz = 100 MW average laser output.
    # Source: inertia-enterprises-2026-update.md §Thunderwall Specs (high confidence)
    f_rep=10.0,

    # Thermal efficiency: steam Rankine implied by Inertia public materials.
    # Xcimer's 45% helium Brayton (IFE Workshop 2022) conflicts with their
    # website claim of "steam" — unresolved; not applied here.
    # Source: analysis.md §3 Balance of Plant / §5 Table (low confidence)
    eta_th=0.35,

    # Standard DT neutron energy multiplier; pulsed_laser_ife.yaml default
    mn=1.1,

    # DT radiation fraction; costing_constants.yaml f_rad_dt default
    f_rad=0.10,

    # Subsystem power fraction; pulsed_laser_ife.yaml default
    f_sub=0.03,

    # Pumping power (liquid Li circulation); pulsed_laser_ife.yaml default
    p_pump=1.0,

    # Tritium processing power; pulsed_laser_ife.yaml default
    p_trit=10.0,

    # Housekeeping; pulsed_laser_ife.yaml default
    p_house=4.0,

    # Cryogenic power: cryogenic DT target layering (~mK per shot).
    # pulsed_laser_ife.yaml default; no IFE-specific cryo estimate published
    p_cryo=0.5,

    # Target factory electrical load; pulsed_laser_ife.yaml default
    p_target=1.0,

    # ── Chamber geometry (spherical) ─────────────────────────────────
    # Spherical chamber with liquid Li pipe lining.
    # Inertia's design has no published chamber study; defaults used.
    # Source: analysis.md §3 (Reaction Chamber: no engineering study published)
    plasma_t=4.0,        # Chamber radius [m]; pulsed_laser_ife.yaml default
    blanket_t=0.80,      # Liquid Li blanket thickness [m]; pulsed_laser_ife.yaml default
    ht_shield_t=0.25,    # Shield thickness [m]; pulsed_laser_ife.yaml default
    structure_t=0.15,    # Primary structure [m]; pulsed_laser_ife.yaml default
    vessel_t=0.10,       # Vacuum vessel [m]; pulsed_laser_ife.yaml default

    # ── Cost overrides ───────────────────────────────────────────────
    cost_overrides={
        # UNCERTAIN: Laser driver system (Thunderwall DPSSL), NOAK estimate.
        #
        # FOAK basis: $700-1,000/J × 10 MJ = $7-10B (midpoint $8.5B).
        # Source: handwritten/26-laser-icf-indirect-drive.md §Table 1 (low confidence)
        #
        # NOAK pathway: laser diodes must fall from current ~$0.02/W floor
        # to ~$0.007/W TRUMPF/LLNL viability target (3× reduction).
        # At viability target: $0.007/W × 100 MW optical = $700M diodes;
        # full system (beam delivery, conditioning, optics) × 2 = ~$1.4B.
        # Conservative NOAK midpoint used here: $3,000M (~$300/J).
        # Range: $1,400M (diodes at viability target) to $8,500M (FOAK mid).
        # Source: analysis.md §2 (Uncertainty 1), §4 (Laser Diodes)
        #         handwritten/26-laser-icf-indirect-drive.md §Target Factory
        "C220107": 3000.0,

        # Special materials: liquid Li blanket (Inertia).
        # Li is cheap and abundant; Inertia cites ~15 EVs equivalent inventory.
        # Framework default (15 M$ at 1 GWe) assumes PbLi breeding blanket.
        # Liquid Li inventory at commercial scale is inexpensive by comparison.
        # Source: analysis.md §4 (Liquid Lithium); dossier.md
        "CAS27": 8.0,
    },
)

# ── Primary forward pass: native 1.5 GWe ────────────────────────────
result = model.forward(net_electric_mw=NATIVE_MW, **_SHARED_KWARGS)

# ── Scaled forward pass: 1 GWe comparison point ─────────────────────
# override_reference_mw tells the framework that cost_overrides are
# calibrated at NATIVE_MW; it scales each overridden account to 1 GWe
# using per-account scaling laws, preserving physics self-consistency.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=NATIVE_MW,
    **_SHARED_KWARGS,
)

# ── Print results ────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Laser ICF - Indirect Drive (D-T) — Inertia Enterprises (NOAK)")
print(
    f"Native: {NATIVE_MW:.0f} MWe | Availability: {_SHARED_KWARGS['availability']:.0%}"
    f" | Lifetime: {_SHARED_KWARGS['lifetime_yr']} yr"
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
    "C220107": "Driver / power supplies  [OVERRIDE]",
    "C220108": "Divertor / ash removal",
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
print(f"{'Code':<10} {'Account':<38} {'M$':>10}")
print("-" * 60)
for k, v in result.cas22_detail.items():
    label = cas22_labels.get(k, k)
    print(f"{k:<10} {label:<38} {float(v):>10.1f}")

# ── 1 GWe scaled result ───────────────────────────────────────────────
c1 = result_1gw.costs
pt1 = result_1gw.power_table
print(f"\n1 GWe reference (scaled from {NATIVE_MW:.0f} MWe native design):")
print(f"LCOE: {c1.lcoe:.1f} $/MWh | Overnight: {c1.overnight_cost:.0f} $/kW")
print(
    f"Fusion: {pt1.p_fus:.0f} MW | Net: {pt1.p_net:.0f} MW"
    f" | Q_eng: {pt1.q_eng:.1f}"
)

# ── Key assumptions ───────────────────────────────────────────────────
print("""
Key Assumptions (confidence / uncertainty level):
  1. PRIMARY CONCEPT: Inertia Enterprises indirect drive (NIF Hybrid-E heritage),
     not Xcimer HDD/KrF — Xcimer may warrant reclassification to concept 17a.
     Source: analysis.md §7 cross-concept note.

  2. Q_eng = 4.0 (low confidence): Inertia target; requires total scientific gain
     ~45× at 10 MJ — not demonstrated experimentally (NIF best: 4.13×).
     Source: handwritten/26-laser-icf-indirect-drive.md §Table 1.

  3. eta_pin = 10% (medium confidence): Thunderwall design target; DPSSL in-class
     demonstration does not yet exist at plant scale.
     Source: inertia-enterprises-2026-update.md §Thunderwall Specs.

  4. NOAK laser driver = $3,000M (UNCERTAIN, low confidence): dominant cost item
     with no published NOAK breakdown. Requires diodes reaching $0.007/W viability
     target (current floor ~$0.02/W). Range: $1,400M optimistic to $8,500M FOAK.
     Source: analysis.md §2 (Uncertainty 1), §4 (Laser Diodes).

  5. availability = 75% (UNCERTAIN): no published IFE capacity factor model;
     Inertia projects 3-5 yr chamber replacement intervals.
     Source: analysis.md §5 (Missing Parameters); handwritten §Table 1.

  6. eta_th = 35% steam Rankine: Inertia references steam in public materials;
     Xcimer's claimed 45% helium Brayton (IFE Workshop 2022) unresolved.
     Source: analysis.md §3 Balance of Plant.

  7. CAS27 = $8M: liquid Li blanket (Inertia) — cheap relative to FLiBe default.
     No published Inertia TBR or tritium breeding analysis.
     Source: analysis.md §4 (Liquid Lithium); dossier.md.

  8. Capacity factor model gap is analysis-blocking: a rep-rate-coupled
     availability model (UKAEA PROCESS IFE module or GEM tool) is needed to
     properly capture chamber clearing, target injection synchronization, and
     scheduled maintenance interactions.
     Source: analysis.md §6, Gap #3.
""")

# ── Sensitivity analysis ──────────────────────────────────────────────
sens = model.sensitivity(
    result.params,
    cost_overrides=_SHARED_KWARGS["cost_overrides"],
)

print("Sensitivity (elasticity = %LCOE / %param, evaluated at native 1.5 GWe)")
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
