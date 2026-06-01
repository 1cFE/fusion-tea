"""Heavy Ion Beam ICF (D-T) — Intensity Energy: 1costingfe model setup.

Concept: Heavy ion beam inertial confinement fusion (IFE), D-T fuel. Based on the
HYLIFE-II power plant design study (OSTI 7021072, LLNL, early 1990s) as the
primary economic analog. No private company ("Intensity Energy") was verified as
existing in 2026; this analysis treats HIF as a technology archetype anchored to
published national-laboratory design data. HIBALL (KfK-3202, 1985) provides the
only published recirculating-power fraction (15%).

Modeling approach:
  - Native design point: 940 MWe (HYLIFE-II baseline, OSTI 7021072).
  - All cost data is from 1985–1994; inflated to 2026 by CPI ×2.5.
  - Driver cost (C220104): $570M HYLIFE-II (early-1990s) → $1,400M 2026.
  - eta_pin = 0.35: mid-range of published 30-40% HIF driver wall-plug efficiency;
    HYLIFE-II-specific value not published, but efficiency is a principal advantage
    over laser ICF (1–15%).
  - q_eng = 6.5: derived from HIBALL published 15% recirculating power fraction
    (Q_eng ≈ 1/0.15 ≈ 6.7); applied slightly conservatively to HYLIFE-II scale.
  - eta_th = 0.38: conservative steam Rankine for 1990s-era design; no HIF study
    has evaluated sCO2. HYLIFE-II energy balance suggests ~40-45% is possible if
    driver waste heat is fully recuperated; 0.38 is the defensible lower bound.
  - p_cryo = 0.5: accelerator quadrupole cryogenics (no plasma-confining magnets);
    framework default retained — quadrupole cryogenic load is comparable to a small
    HTS coil system in absolute terms.
  - FLiBe special materials (Be + enriched Li-6) not separately costed in CAS27;
    framework DT default ($15M for PbLi) is almost certainly an underestimate but
    no modern FLiBe inventory cost exists.

Key deviations from framework defaults:
  - C220104 = $1,400M  UNCERTAIN: $570M 1990s driver × 2.5 CPI; ancient estimate
  - q_eng = 6.5        UNCERTAIN: derived from HIBALL 15% recirc; HYLIFE-II unpublished
  - eta_pin = 0.35     UNCERTAIN: mid-range 30-40%; HYLIFE-II-specific value unpublished
  - eta_th = 0.38      UNCERTAIN: steam Rankine analogue; no modern HIF thermal study
  - availability = 0.80  UNCERTAIN: no published availability target; no HIF commercial plant
  - f_rep = 6.0        HYLIFE-II nominal (analysis §S5); default YAML is 5.0 Hz (HIBALL)
  - construction_time_yr = 7.0  Extended for accelerator complex; YAML default is 6.0

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

model = CostModel(concept=ConfinementConcept.HEAVY_ION, fuel=Fuel.DT)

# ── Native design point ────────────────────────────────────────────────────────
# HYLIFE-II baseline: 940 MWe net electric output
# Source: hif-technology-overview.md §HYLIFE-II; analysis §S5 parameter table
NATIVE_MW = 940.0

# ── Shared parameters ─────────────────────────────────────────────────────────
_SHARED_KWARGS = dict(
    # ── Plant availability and lifetime ────────────────────────────────────────
    # No published HYLIFE-II or HIBALL availability target. High rep rate (6 Hz) is
    # more forgiving of maintenance downtime than low-rep-rate IFE (0.1–1 Hz) because
    # each shot contributes less power and single-shot downtime is smaller relative to
    # total energy. Analogue to laser IFE concepts with high-replacement-rate components.
    # Source: analysis §S5 [analogue]; analysis §S2 Challenge 3 (rep-rated chamber)
    availability=0.80,              # UNCERTAIN: analysis §S5 [analogue, low confidence]

    lifetime_yr=30,                 # HYLIFE-II designed for 30-yr chamber lifetime
                                    # Source: hif-technology-overview.md §HYLIFE-II

    n_mod=1,                        # Single chamber at native 940 MWe

    # ── Power balance ───────────────────────────────────────────────────────────
    # q_eng (engineering gain) derived from HIBALL 15% recirculating power fraction.
    # HIBALL: P_recirc / P_gross = 15% → Q_eng = P_gross / P_recirc = 1/0.15 ≈ 6.7.
    # Applied slightly conservatively (6.5) to HYLIFE-II scale.
    # Source: hif-technology-overview.md §HIBALL (15% recirc, 3.8 GWe plant)
    # UNCERTAIN: HYLIFE-II recirc fraction not directly published; HIBALL is a larger
    #   single-pass linac (HYLIFE-II uses recirculating architecture — may differ).
    q_eng=6.5,                      # UNCERTAIN: analysis §S5; hif-technology-overview.md §HIBALL

    # Repetition rate: HYLIFE-II nominal single-chamber design rate
    # Source: dossier.md §Repetition Rate; analysis §S5 parameter table
    f_rep=6.0,                      # [Hz]; HYLIFE-II nominal (HIBALL: 5 Hz; future: 10-15 Hz)

    # Driver wall-plug efficiency: confirmed 30-40% range across sources
    # This is HIF's primary economic advantage over laser ICF (1-15%)
    # HYLIFE-II-specific value not published; using mid-range
    # Source: hif-technology-overview.md §Driver Technology;
    #         hif-recent-research-compilation.md §Key Technical Parameters - Driver Efficiency
    eta_pin=0.35,                   # UNCERTAIN: mid-range 30-40%; analysis §S5

    # Thermal efficiency: steam Rankine, analogous to 1990s nuclear steam plants
    # HYLIFE-II uses FLiBe primary coolant → secondary steam cycle
    # Modern sCO2 Brayton not evaluated for HIF (no published study)
    # Source: analysis §S5 [analogue, low confidence]; analysis §S3 BOP section
    eta_th=0.38,                    # UNCERTAIN: steam Rankine analogue

    mn=1.1,                         # DT neutron energy multiplier (standard D-T)
    f_rad=0.10,                     # Radiation fraction of ash power (DT default)
    f_sub=0.03,                     # Subsystem power fraction (DEFAULT)
    p_pump=1.0,                     # Pumping power [MW] (DEFAULT)
    p_trit=10.0,                    # Tritium processing power [MW] (DEFAULT)
    p_house=4.0,                    # Housekeeping power [MW] (DEFAULT)

    # Accelerator quadrupole cryogenics: HYLIFE-II uses superconducting beam
    # transport magnets. No plasma-confining HTS/LTS magnets → cryogenic load is
    # modest compared to tokamak/stellarator. Framework default (0.5 MW) retained
    # as representative of accelerator quadrupole cryogenics.
    # Source: analysis §S3 Superconducting Final Focus Magnets; §S7 cross-concept notes
    p_cryo=0.5,                     # DEFAULT: accelerator quad cryogenics only

    # Target factory power: HYLIFE-II direct-drive D-T ice targets at 6 Hz
    # (~189M targets/yr). Simpler geometry than laser ICF hohlraums but still
    # requires cryogenic D-T layering. Framework default retained.
    # Source: analysis §S2 Challenge 2; analysis §S3 Target Fabrication
    p_target=0.8,                   # [MW]; DEFAULT (framework HEAVY_ION default)

    # ── Chamber geometry (spherical IFE chamber, FLiBe thick liquid wall) ─────
    # HYLIFE-II FLiBe jet system: thick-liquid-wall chamber with spherical geometry.
    # Chamber radius (plasma_t) not explicitly stated in available sources; using
    # IFE default (4.0 m chamber radius) — consistent with HYLIFE-II ~5 m geometry.
    # Source: analysis §S3 Rep-Rated Chamber section; hif-technology-overview.md §HYLIFE-II
    plasma_t=4.0,                   # Chamber radius [m] (DEFAULT: IFE default)
    blanket_t=0.80,                 # FLiBe liquid jet thickness [m] (DEFAULT)
    ht_shield_t=0.25,               # High-temperature shield [m] (DEFAULT)
    structure_t=0.15,               # Primary structure [m] (DEFAULT)
    vessel_t=0.10,                  # Vacuum vessel [m] (DEFAULT)

    # ── Construction / financial ───────────────────────────────────────────────
    # Extended construction time: large accelerator complex (~3 km linac equivalent
    # for HIBALL; recirculating storage ring architecture for HYLIFE-II) plus
    # first-of-kind fusion chamber and liquid-wall systems.
    # Source: analysis §S3 LIA Driver section (HIBALL: ~3 km linac, HYLIFE-II: recirculating)
    construction_time_yr=7.0,       # Extended for accelerator complex complexity
    interest_rate=0.07,
    inflation_rate=0.0245,
    noak=True,                      # NOAK: long-run commercial economics reference case

    # ── Cost overrides ─────────────────────────────────────────────────────────
    cost_overrides={
        # C220104 — Driver Capital (Induction Linac Accelerator)
        # HYLIFE-II estimated $570M direct cost for recirculating induction
        # accelerator (early-1990s dollars). Inflated by CPI ×2.5 to 2026 dollars.
        # $570M × 2.5 ≈ $1,425M → rounded to $1,400M.
        # This is the ONLY published bottom-up HIF driver cost estimate.
        # UNCERTAIN: (a) 1990s dollars inflated by CPI only — does not capture
        #   component cost changes (induction cells, pulsed power) relative to CPI;
        #   (b) HYLIFE-II recirculating architecture vs. HIBALL single-pass ~3 km linac
        #   have different cost structures; (c) modular architecture (mass-produced
        #   identical cells) could reduce costs via learning, not reflected here.
        # Source: hif-technology-overview.md §HYLIFE-II; analysis §S2 Challenge 1;
        #         analysis §S5 parameter table
        "C220104": 1400.0,          # UNCERTAIN: $570M 1990s × 2.5 CPI = $1,425M → $1,400M
    },
)

# ── Primary result — native 940 MWe design point (HYLIFE-II) ──────────────────
result = model.forward(net_electric_mw=NATIVE_MW, **_SHARED_KWARGS)

# ── Scaled 1 GW result — per-account scaling from 940 MWe ────────────────────
# Used for cross-concept comparison at standard 1 GWe reference.
# override_reference_mw tells the framework that cost_overrides values are
# valid at 940 MWe and scales them to 1,000 MWe using per-account scaling laws.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=NATIVE_MW,
    **_SHARED_KWARGS,
)

# ── Cost Results ──────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Heavy Ion Beam ICF (D-T) | HYLIFE-II archetype — Intensity Energy")
print(f"Native design: {NATIVE_MW:.0f} MWe | 6 Hz | Recirculating induction linac + FLiBe wall")
print(f"LCOE:          {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion:        {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.2f}")
print(f"Q_sci (target gain): {pt.q_sci:.1f}  [HYLIFE-II nominal: 70 at 5 MJ]")
print(f"Driver E/shot: {pt.e_driver_mj:.2f} MJ  [HYLIFE-II stated: 5 MJ]")
print()

# Historical LCOE cross-check: HYLIFE-II 6.5 ¢/kWh (early-1990s) → ~16 ¢/kWh 2026
_hylife2_lcoe_1990s = 65.0   # $/MWh (early-1990s dollars)
_hylife2_lcoe_2026  = 65.0 * 2.5  # CPI × 2.5
print(f"Historical reference: HYLIFE-II LCOE = ${_hylife2_lcoe_1990s:.0f}/MWh (early-1990s) "
      f"→ ~${_hylife2_lcoe_2026:.0f}/MWh 2026 (CPI ×2.5)")
print(f"  Source: hif-technology-overview.md §HYLIFE-II; analysis §S5")
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
print(f"  C220104 = $1,400M  UNCERTAIN: $570M 1990s HYLIFE-II driver × 2.5 CPI")
print(f"                     Only published HIF driver bottom-up cost. Does not")
print(f"                     capture modular cell manufacturing learning potential.")
print(f"                     Source: hif-technology-overview.md §HYLIFE-II; analysis §S2.1")
print(f"  q_eng = 6.5        UNCERTAIN: from HIBALL 15% recirc fraction (Q_eng ≈ 6.7)")
print(f"                     HYLIFE-II recirculating arch may have different fraction.")
print(f"                     Source: hif-technology-overview.md §HIBALL; analysis §S5")
print(f"  eta_pin = 0.35     UNCERTAIN: mid-range 30-40%; structural HIF advantage")
print(f"                     over laser ICF (1-15%) confirmed; exact value unpublished")
print(f"                     Source: hif-technology-overview.md §Driver Technology")
print(f"  eta_th = 0.38      UNCERTAIN: conservative steam Rankine (1990s design era)")
print(f"                     sCO2 not evaluated for HIF; actual HYLIFE-II value unclear")
print(f"                     Source: analysis §S5 [analogue, low confidence]")
print(f"  availability = 0.80  UNCERTAIN: no published HYLIFE-II availability target")
print(f"                     High 6 Hz rep rate reduces per-shot energy but adds wear")
print(f"                     Source: analysis §S5 [analogue, low confidence]")
print(f"  CAS27 = DEFAULT    UNCERTAIN: FLiBe inventory (Be + Li-6) not separately costed")
print(f"                     Framework DT default ($15M) assumes PbLi blanket, not FLiBe")
print(f"                     FLiBe cost is sparse in all sources; HYLIFE-II has only 1994$")
print(f"                     Source: analysis §S4 FLiBe supply chain; memory note")
print(f"  Target factory O&M = DEFAULT  UNCERTAIN: no HIF target production cost exists")
print(f"                     Framework staffing-based default does not capture ~189M")
print(f"                     targets/yr consumable costs; true OPEX may be significantly")
print(f"                     higher. Source: analysis §S2 Challenge 2; analysis §S5")
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

# ── Driver Efficiency Scenario Sweep ─────────────────────────────────────────
# HIF's principal economic claim is 30-40% driver efficiency vs. 1-15% for laser ICF.
# This sweep shows LCOE sensitivity across the full published efficiency range.
# eta_pin range: 0.25 (below published range) to 0.45 (above published range).
# Source: hif-technology-overview.md §Driver Technology; analysis §S5
_eta_scenarios = [
    (0.25, "Below range (0.25 — pessimistic)"),
    (0.30, "Low end    (0.30)"),
    (0.35, "Mid-range  (0.35 — base case)"),
    (0.40, "High end   (0.40)"),
    (0.45, "Above range (0.45 — optimistic)"),
]

print("\nDriver Efficiency Scenario Sweep (eta_pin, HYLIFE-II 30-40% published range):")
print(f"  {'Scenario':<42}  {'eta_pin':>8}  {'LCOE $/MWh':>11}  {'OC $/kW':>9}  Notes")
print("  " + "-" * 85)

_sweep_kwargs = {k: v for k, v in _SHARED_KWARGS.items() if k != "eta_pin"}
for _eta, _label in _eta_scenarios:
    _rsweep = model.forward(net_electric_mw=NATIVE_MW, eta_pin=_eta, **_sweep_kwargs)
    _note = "  <- base case" if abs(_eta - 0.35) < 0.01 else ""
    print(f"  {_label:<42}  {_eta:>8.2f}  {_rsweep.costs.lcoe:>11.1f}  "
          f"{_rsweep.costs.overnight_cost:>9.0f}{_note}")

print()
_laser_reference_eta = 0.10
_rsweep_laser = model.forward(
    net_electric_mw=NATIVE_MW, eta_pin=_laser_reference_eta, **_sweep_kwargs
)
print(f"  Reference: laser ICF eta_pin ~0.10 (10%) applied to HIF parameters:")
print(f"    LCOE = {_rsweep_laser.costs.lcoe:.1f} $/MWh | OC = {_rsweep_laser.costs.overnight_cost:.0f} $/kW")
print(f"    (Shows how HIF 30-40% driver efficiency advantages the LCOE vs. laser ICF)")
print()

# ── Driver Cost Scenario Sweep ────────────────────────────────────────────────
# Driver capital is the dominant LCOE uncertainty (analysis §S2 Challenge 1).
# Range spans: HYLIFE-II 1990s inflated ($1.4B base) to optimistic modular
# manufacturing scenario ($0.7B, reflecting mass-production cost reduction potential)
# and pessimistic scenario ($2.5B, reflecting no learning over scientific-instrument
# procurement). Source: analysis §S2 Challenge 1; analysis §S5 parameter table
_driver_scenarios = [
    (700.0,  "Optimistic modular NOAK  ($0.7B)"),
    (1000.0, "Mid-range scenario       ($1.0B)"),
    (1400.0, "HYLIFE-II inflated base  ($1.4B)"),
    (2000.0, "No-learning pessimistic  ($2.0B)"),
    (2500.0, "Worst-case conservative  ($2.5B)"),
]

print("Driver Capital Cost Scenario Sweep (C220104, HYLIFE-II base: $1.4B 2026$):")
print(f"  {'Scenario':<42}  {'C220104 M$':>11}  {'LCOE $/MWh':>11}  {'OC $/kW':>9}  Notes")
print("  " + "-" * 88)

_base_kwargs_no_co = {k: v for k, v in _SHARED_KWARGS.items() if k != "cost_overrides"}
for _driver_m, _label in _driver_scenarios:
    _co = {"C220104": _driver_m}
    _rdri = model.forward(
        net_electric_mw=NATIVE_MW,
        cost_overrides=_co,
        **_base_kwargs_no_co,
    )
    _note = "  <- base case" if abs(_driver_m - 1400.0) < 1.0 else ""
    print(f"  {_label:<42}  {_driver_m:>11.0f}  {_rdri.costs.lcoe:>11.1f}  "
          f"{_rdri.costs.overnight_cost:>9.0f}{_note}")

print()
print("  Note: modular induction linac architecture (identical cells, factory")
print("  manufacturing) is frequently cited as a path to cost reduction from")
print("  scientific-instrument procurement levels. No learning-curve analysis")
print("  exists. Source: analysis §S2 Challenge 1; hif-technology-overview.md §Driver Technology")
print()

# ── Regulatory Cost Scenario (fission-analog upper bound) ────────────────────
# Stewart & Shirvan (2022) 2.2× construction cost multiplier under fission-analog
# regulatory framework. Applies to HIF as a D-T IFE facility.
# Source: 21-spherical-tokamak-hts analysis §S2; analysis §S7 cross-concept notes
_reg_multiplier = 2.2
_c_direct = float(result.costs.total_capital)  # approximate

print("Regulatory Cost Scenario (Stewart & Shirvan 2022 fission-analog framework):")
print(f"  Base LCOE (no regulatory multiplier): {c.lcoe:.1f} $/MWh")
print(f"  Note: Stewart & Shirvan 2.2× construction cost multiplier applies as")
print(f"  conservative upper bound for D-T IFE regulatory pathway.")
print(f"  No HIF plant has entered regulatory process; no licensing pathway scoped.")
print(f"  Source: analysis §S2 Challenge 6; analysis §S7; 21-spherical-tokamak-hts §S2")
print()
