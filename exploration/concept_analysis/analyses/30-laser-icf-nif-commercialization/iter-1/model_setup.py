"""Laser ICF — NIF Commercialization (D-T): 1costingfe model setup.

Concept: Inertia Enterprises indirect-drive D-T laser ICF, commercializing the
NIF Hybrid-E target design (co-founder Kritcher led the Dec. 2022 ignition shot).
Thunderwall DPSSL driver: ~1,000 beamlines × 10 kJ each, 10 Hz rep rate, 10%
wallplug efficiency. Liquid lithium blanket for tritium breeding and energy
capture. Steam Rankine power conversion.

Modeling approach:
  - Native design point: 1,500 MWe (Inertia stated commercial target).
  - q_eng is set to correspond to Q_target ~56, required to close the energy
    balance for a single 1,000-beamline system at 1,500 MWe net (analysis §S2,
    Challenge 1). Inertia states Q_target > 30 as the commercial threshold, but
    at 10 Hz with 10% wallplug and 45% thermal efficiency, Q_target = 30 yields
    only ~350 MWe net per system — either 4× modular architecture or higher
    gain is required. This model represents the single-system closure scenario.
  - Laser driver capital cost is overridden to reflect a NOAK $100/J projected
    semiconductor-diode-pumped laser (10× learning from $700-1,000/J FOAK).
  - Annual O&M is inflated via a custom om_cost_dt to capture target material
    consumables ($315M/yr at <$1/target × 10 Hz × 3.15×10⁷ s/yr) — the dominant
    IFE O&M cost driver, not in the framework's staffing-based default.
  - Thermal efficiency: LLNL LIFE analogue (45%); Inertia has not published a
    confirmed plant-level value.
  - No cryogenics: IFE plant has no superconducting magnets.

Key deviations from framework defaults:
  - q_eng = 2.77     UNCERTAIN: Q_target ~56 for 1,500 MWe closure (see §S2)
  - C220104 = 1,000 M$  UNCERTAIN: $100/J NOAK laser; FOAK $7–10B at $700–1,000/J
  - om_cost_dt = 309    UNCERTAIN: inflated from 52 to capture $315M/yr target materials
  - p_cryo = 0.0     No superconducting magnets; no cryogenics
  - availability = 0.80  No 10 Hz IFE plant; high-turnover components

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel
from costingfe.defaults import load_costing_constants

# Inflate om_cost_dt to approximate IFE target material consumable costs.
# At 10 Hz, the 1,500 MWe plant fires 315 million targets/year. At $1/target
# (Inertia stated goal): $315M/yr in target material costs — dominant O&M driver
# not in the framework's staffing-based default (om_cost_dt = 52 M$/GWe^0.5).
# The framework scales CAS71 as om_cost_dt × (p_net/1 GWe)^0.5.
# To add ~$315M at 1,500 MWe: delta = 315 / sqrt(1.5) ≈ 257 → new ≈ 309.
# UNCERTAIN: $1/target goal unverified; true target O&M may be 5–50× higher.
# Note: target costs are fixed with rep rate, not power; power-law scaling to
#   1 GWe in result_1gw will proportionally reduce, understating target cost burden.
# Source: inertia-website-technical.md §Economics FAQ; analysis §S2 Challenge 3
_CC = load_costing_constants().replace(om_cost_dt=309.0)

model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT, costing_constants=_CC)

# ── Native design point ───────────────────────────────────────────────────────
# Inertia states "long-term goal is to build a 1.5-GW capacity power plant"
# Source: inertia-website-technical.md §Specs; enr-mike-dunne-interview.md
NATIVE_MW = 1500.0

# ── Shared parameters ─────────────────────────────────────────────────────────
_SHARED_KWARGS = dict(
    # ── Plant availability and lifetime ──────────────────────────────────────
    # No 10 Hz IFE plant has operated; analysis §S5 notes "90% would be optimistic"
    # given high-replacement-rate components: final optics, laser diodes, target
    # injection mechanisms, first wall structural elements (analysis §S2, Challenge 6)
    availability=0.80,           # UNCERTAIN; analysis §S5 (derivable)
    lifetime_yr=30,              # Standard fusion plant design lifetime
    n_mod=1,                     # Single unit at native 1,500 MWe

    # ── Power balance ─────────────────────────────────────────────────────────
    # UNCERTAIN: Q_target ~56 required for 1,500 MWe net from a single
    # 1,000-beamline system. Derivation: q_eng ≈ eta_th × (1.08×Q_target + 1)
    # × eta_pin = 0.045 × (1.08 × 56 + 1) ≈ 2.77.
    # Stated >30× commercial threshold → q_eng ≈ 1.50 → only ~350 MWe net.
    # Source: analysis §S2 Challenge 1 [inferred]; enr-mike-dunne-interview.md §Performance Targets
    q_eng=2.77,                  # UNCERTAIN: corresponds to Q_target ~56

    # Repetition rate: 10 Hz confirmed in all Inertia public sources
    # Source: inertia-website-technical.md §Specs; globenewswire-series-a-press-release.md
    f_rep=10.0,                  # [Hz]

    # Thunderwall DPSSL beamline wallplug efficiency: 10% explicitly stated
    # Source: globenewswire-series-a-press-release.md §Thunderwall Specs;
    #         inertia-website-technical.md §Laser FAQ
    eta_pin=0.10,

    # Thermal efficiency: LLNL LIFE program analogue (liquid Li → steam Rankine)
    # Modern sCO2 cycle could reach ~50%; Inertia has not disclosed a confirmed value
    # Source: analysis §S5 [analogue, unsourced]; analysis §S2 Challenge 4
    eta_th=0.45,                 # UNCERTAIN: LLNL LIFE analogue

    mn=1.1,                      # DT neutron energy multiplier (standard D-T)
    f_rad=0.10,                  # Radiation fraction of ash power (DT default)
    f_sub=0.03,                  # Subsystem power fraction (DEFAULT)
    p_pump=1.0,                  # Pumping power [MW] (DEFAULT)
    p_trit=10.0,                 # Tritium processing power [MW] (DEFAULT)
    p_house=4.0,                 # Housekeeping power [MW] (DEFAULT)

    # No cryogenics: IFE uses laser driver, not superconducting magnets
    # Source: inertia-website-technical.md §Laser FAQ (semiconductor diode pumped)
    p_cryo=0.0,

    # Target factory operational power — increased above 1 MW default to reflect
    # 315 million target/year throughput and cryogenic D-T layering operations
    p_target=2.0,                # [MW]; DEFAULT is 1.0

    # ── Chamber geometry (spherical IFE chamber, liquid Li first wall) ────────
    # Liquid Li provides neutron energy capture, tritium breeding, and serves
    # as the thermal working fluid for the steam cycle
    # Source: inertia-website-technical.md §Energy Conversion FAQ
    plasma_t=4.0,                # Chamber radius [m] (DEFAULT: IFE default)
    blanket_t=0.80,              # Liquid Li blanket thickness [m] (DEFAULT: IFE default)
    ht_shield_t=0.25,            # High-temperature shield [m] (DEFAULT)
    structure_t=0.15,            # Primary structure [m] (DEFAULT)
    vessel_t=0.10,               # Vacuum vessel [m] (DEFAULT)

    # ── Construction / financial ──────────────────────────────────────────────
    # Extended construction time: novel first-of-kind large-scale IFE plant;
    # 10 Hz driver integration and liquid-Li first wall add complexity
    construction_time_yr=6.0,
    interest_rate=0.07,
    inflation_rate=0.0245,
    noak=True,                   # NOAK: long-run commercial economics

    # ── Cost overrides ────────────────────────────────────────────────────────
    cost_overrides={
        # C220104 — Laser Driver Capital
        # 10 MJ total system at NOAK projected semiconductor diode cost.
        # FOAK: $700–1,000/J × 10 MJ = $7–10B
        #   Source: analysis §S5; handwritten exemplar 26-laser-icf-indirect-drive.md
        #           §Comparison Table (citing Xcimer whitepaper context)
        # NOAK: If semiconductor diode costs follow solar-panel learning curve,
        #   10× reduction → ~$100/J → $1B for 10 MJ total.
        #   Thesis: diode target cost $0.007/W (analysis §S4, citing TRUMPF/LLNL);
        #   current diode pricing ~$0.1–1/W implies 10–100× reduction needed.
        # UNCERTAIN: $100/J NOAK assumes aggressive learning; no published roadmap.
        #   Scale-up factor 100× explicitly required (analysis §S4; inertia-website-technical.md)
        "C220104": 1000.0,       # UNCERTAIN: $1B NOAK (10 MJ × $100/J)

    },
    # O&M note: target material costs (~$315M/yr at $1/target × 10 Hz) are captured
    # via the custom om_cost_dt in the CostingConstants above, not as a cost_override.
)

# ── Primary result — native 1,500 MWe design point ───────────────────────────
result = model.forward(net_electric_mw=NATIVE_MW, **_SHARED_KWARGS)

# ── Scaled 1 GW result — per-account scaling from 1,500 MWe ─────────────────
# Used for cross-concept comparison at standard 1 GWe reference.
# override_reference_mw tells the framework that cost_overrides values are
# valid at 1,500 MWe and scales them to 1,000 MWe using per-account scaling laws.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=NATIVE_MW,
    **_SHARED_KWARGS,
)

# ── Cost Results ─────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Laser ICF — NIF Commercialization (D-T) | Inertia Enterprises")
print(f"Native design: {NATIVE_MW:.0f} MWe | 10 Hz | Indirect drive (Hybrid-E target)")
print(f"LCOE:          {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion:        {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.2f}")
print(f"Q_sci (target gain): {pt.q_sci:.1f}  [model-derived; stated threshold >30]")
print(f"Driver E/shot: {pt.e_driver_mj:.2f} MJ  [stated Inertia design: 10 MJ]")
print()

# ── CAS Breakdown ─────────────────────────────────────────────────────────────
cas_table = [
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
for code, name, val in cas_table:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")
print()

# ── CAS22 Detail ──────────────────────────────────────────────────────────────
det = result.cas22_detail
print("CAS22 sub-accounts:")
for k in sorted(det.keys()):
    if k != "C220000":
        print(f"  {k}  {float(det[k]):>10.1f} M$")
print(f"  {'C220000 (Total)':<14} {float(det.get('C220000', c.cas22)):>10.1f} M$")
print()

# ── 1 GWe comparison ──────────────────────────────────────────────────────────
c1 = result_1gw.costs
print(f"1 GWe scaled:  LCOE = {c1.lcoe:.1f} $/MWh | Overnight = {c1.overnight_cost:.0f} $/kW")
print()

# ── Key Assumptions ───────────────────────────────────────────────────────────
print("Key Assumptions and Uncertainties:")
print(f"  q_eng = 2.77     UNCERTAIN: Q_target ~56 needed for 1,500 MWe net single-system")
print(f"                   closure; stated >30 threshold gives only ~350 MWe/system")
print(f"  eta_th = 0.45    UNCERTAIN: LLNL LIFE analogue; Inertia has not published value")
print(f"  avail = 0.80     UNCERTAIN: no 10 Hz IFE plant; high-turnover components expected")
print(f"  C220104 = $1.0B  UNCERTAIN: $100/J NOAK laser; FOAK estimate $7–10B at $700–1,000/J")
print(f"  om_cost_dt=309   UNCERTAIN: inflated from 52 to capture ~$315M/yr target materials")
print(f"                   ($1/target × 315M targets/yr at 10 Hz); goal unverified")
print(f"                   laser diode replacement O&M NOT included (no data basis)")
print(f"  Note: model-derived e_driver_mj may differ from stated 10 MJ/shot due to")
print(f"        energy balance inconsistency in Inertia's published parameters")
print()

# ── Sensitivity Analysis ──────────────────────────────────────────────────────
sens = model.sensitivity(result.params)

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
