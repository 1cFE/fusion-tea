"""Laser ICF — NIF Commercialization (D-T): 1costingfe model setup.

Concept: Inertia Enterprises indirect-drive D-T laser ICF, commercializing the
NIF Hybrid-E target design (co-founder Kritcher led the Dec. 2022 ignition shot).
Thunderwall DPSSL driver: ~1,000 beamlines × 10 kJ each, 10 Hz rep rate, 10%
wallplug efficiency. Liquid lithium blanket for tritium breeding and energy
capture. Steam Rankine power conversion.

Modeling approach:
  - Native design point: 1,500 MWe (Inertia stated commercial target).
  - q_eng is anchored to e_driver_mj = 10 MJ (Inertia stated design: 1,000
    beamlines × 10 kJ/beamline). At 1,500 MWe net, this requires Q_sci ≈ 52.5×
    (model-derived; §S2 simplified estimate of ~56 omits the neutron multiplier
    benefit from mn=1.1). The stated >30× commercial threshold yields only
    ~440 MWe net from a single 10 MJ / 10 Hz system (model physics; §S2 simplified
    formula gives ~350 MWe, omitting mn). Reaching 1,500 MWe requires either
    modular architecture or Q_sci ≈ 52.5+. This model represents the single-system
    1,500 MWe closure scenario.
  - Laser driver q_eng derivation: fixing e_driver_mj=10 at p_net=1500 MWe:
    p_driver=100 MW, recirculating base=1,017 MW (1,000 driver/eta_pin + 17 aux),
    q_eng = 2,517 / 1,062 ≈ 2.370 (solves pulsed_thermal_inverse analytically).
  - Laser driver capital cost is overridden to reflect a NOAK $100/J projected
    semiconductor-diode-pumped laser (10× learning from $700-1,000/J FOAK).
  - Annual O&M is inflated via a custom om_cost_dt to capture target material
    consumables ($315M/yr at <$1/target × 10 Hz × 3.15×10⁷ s/yr) — the dominant
    IFE O&M cost driver, not in the framework's staffing-based default.
  - Thermal efficiency: LLNL LIFE analogue (45%); Inertia has not published a
    confirmed plant-level value.
  - No cryogenics: IFE plant has no superconducting magnets.

Key deviations from framework defaults:
  - q_eng = 2.370    UNCERTAIN: anchored to e_driver_mj = 10 MJ; Q_sci ≈ 52.5 at closure
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
    # Anchored to e_driver_mj = 10 MJ (Inertia stated design: 1,000 × 10 kJ beamlines).
    # Derivation (exact, solving pulsed_thermal_inverse for e_driver_mj = 10):
    #   p_driver = 10 MJ × 10 Hz = 100 MW → p_recirc_driver = 100/0.10 = 1,000 MW
    #   fixed_aux = p_pump(1) + p_trit(10) + p_house(4) + p_target(2) = 17 MW
    #   At p_net = 1,500 MWe: 0.97×p_et = 1,500 + 1,017 → p_et = 2,595 MW
    #   q_eng = p_et / recirc = 2,595 / (1,017 + 0.03×2,595) = 2,595/1,095 ≈ 2.370
    #   Analytic: q = 2,517 / 1,062 ≈ 2.3701 (solving for 100 MW driver exactly)
    # Model derives Q_sci ≈ 52.5 (vs. §S2 simplified ~56 which omits mn=1.1 benefit).
    # Stated >30× threshold at e_driver_mj=10: model gives ~440 MWe net per system.
    # Source: analysis §S2 Challenge 1; enr-mike-dunne-interview.md §Performance Targets
    q_eng=2.370,                 # UNCERTAIN: anchored to e_driver_mj=10 MJ; Q_sci≈52.5

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
        #
        # Laser diode cost fractionation (Haefner ILT IFE Workshop 2023):
        #   Diodes ≈ 1/3 of total drive laser capital:
        #     Diode capital  (NOAK): ~$333M  (FOAK: ~$2.3B)
        #     Other laser    (NOAK): ~$667M  (FOAK: ~$4.7B)
        #   Diode lifetime target: 14–20 GShots; current devices ~7–10× short
        #   (~1.4–2.9 GShots). At 10 Hz continuous: replacement every 4.4–9.2 yrs.
        #   Over 30-yr plant life: ~3–7 diode replacements × ~$333M NOAK each
        #   = ~$1.0–2.3B periodic diode capex NOT included in current O&M model.
        #   Gap: framework has no account for this periodic large-capex replacement.
        "C220104": 1000.0,       # UNCERTAIN: $1B NOAK (10 MJ × $100/J; diodes ~$333M)

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
print(f"  q_eng = 2.370    UNCERTAIN: anchored to e_driver_mj = 10 MJ (stated design)")
print(f"                   Model-derived Q_sci ≈ 52.5 for 1,500 MWe closure (§S2")
print(f"                   simplified ~56 omits mn=1.1 neutron multiplier benefit)")
print(f"                   Stated >30 threshold → ~440 MWe/system (model); ~350 MWe")
print(f"                   (§S2 simplified; omits mn). Modular architecture required.")
print(f"  eta_th = 0.45    UNCERTAIN: LLNL LIFE analogue; Inertia has not published value")
print(f"  avail = 0.80     UNCERTAIN: no 10 Hz IFE plant; high-turnover components expected")
print(f"  C220104 = $1.0B  UNCERTAIN: $100/J NOAK laser; FOAK estimate $7–10B at $700–1,000/J")
print(f"    Diode frac ~1/3  (Haefner 2023): diodes ~$333M NOAK, other laser ~$667M NOAK")
print(f"    Diode lifetime:  target 14–20 GShots; current ~7–10× short (1.4–2.9 GShots)")
print(f"    Replacement int: ~4.4–9.2 yrs (current-gen); ~44–63 yrs (if target met)")
print(f"    Periodic capex:  ~$1.0–2.3B over 30-yr life — NOT included in O&M model")
print(f"  om_cost_dt=309   UNCERTAIN: inflated from 52 to capture ~$315M/yr target materials")
print(f"                   ($1/target × 315M targets/yr at 10 Hz); goal unverified")
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

# ── Q_sci Sweep (e_driver_mj = 10 MJ fixed) ──────────────────────────────────
# Sweeps Q_sci 30–60 with e_driver_mj pinned to 10 MJ (Inertia stated design).
# For each Q_sci: derive q_eng analytically (from pulsed_thermal_inverse with
# p_driver=100 MW fixed), then run cost model at the resulting net power to get
# LCOE. Shows the tension between the >30× commercial threshold (~440 MWe) and
# the 1,500 MWe design target (~52.5×).
# Source: analysis §S2 Challenge 1; carried-forward finding CF-F1

# DT physics constants (from costingfe: E_alpha=3.52 MeV, Q_DT=17.58 MeV, mn=1.1)
_DT_ASH_FRAC = 3.52 / 17.58
_C_TH = 1.1 * (1.0 - _DT_ASH_FRAC) + _DT_ASH_FRAC  # ≈ 1.08 effective thermal coeff

_SWEEP_KWARGS = {k: v for k, v in _SHARED_KWARGS.items() if k != "q_eng"}

print("\nQ_sci Sweep (e_driver_mj = 10 MJ fixed, single-system, 1,500 MWe design):")
print(f"  {'Q_sci':>7}  {'Net MWe':>9}  {'q_eng':>6}  {'LCOE $/MWh':>11}  Notes")
print("  " + "-" * 65)

for _qsci in [30.0, 35.0, 40.0, 45.0, 50.0, 52.5, 56.0, 60.0]:
    # Physics with e_driver_mj = 10 MJ (p_driver = 100 MW)
    _p_fus = _qsci * 100.0
    _p_th = _C_TH * _p_fus + 101.0      # neutron+ash thermal + 100 MW driver + 1 MW pump
    _p_et = 0.45 * _p_th                 # gross electric (eta_th = 0.45)
    _p_sub = 0.03 * _p_et                # subsystem load (f_sub = 0.03)
    _recirc = 1017.0 + _p_sub            # 1,000 driver + 17 fixed aux + subsys
    _q_eng_pt = _p_et / _recirc
    _p_net = _p_et - _recirc

    # Run cost model (cost model requires p_net > 0; skip if non-viable)
    if _p_net < 50.0:
        _note = "non-viable (negative or near-zero net)"
        print(f"  {_qsci:>7.1f}  {_p_net:>9.0f}  {_q_eng_pt:>6.3f}  {'—':>11}  {_note}")
        continue

    _rsweep = model.forward(
        net_electric_mw=_p_net,
        q_eng=_q_eng_pt,
        **_SWEEP_KWARGS,
    )
    _lcoe_str = f"{_rsweep.costs.lcoe:.0f}"

    if abs(_qsci - 30.0) < 0.5:
        _note = "← stated threshold (shortfall)"
    elif abs(_p_net - NATIVE_MW) < 150:
        _note = "← closure (~1,500 MWe)"
    elif _p_net > NATIVE_MW:
        _note = "above design target"
    else:
        _note = ""

    print(f"  {_qsci:>7.1f}  {_p_net:>9.0f}  {_q_eng_pt:>6.3f}  {_lcoe_str:>11}  {_note}")

print()
print(f"  Physics note: model gives ~440 MWe at Q_sci=30 (neutron multiplier mn=1.1")
print(f"  adds ~10% thermal power vs. the §S2 simplified formula giving ~350 MWe).")
print(f"  Closure at 1,500 MWe: Q_sci ≈ 52.5 (model) vs. §S2 simplified ~56.")
print(f"  LCOE at threshold (Q_sci=30): driven by low capacity factor at ~440 MWe")

# ── LIFE Heritage Calibration (OSTI-1022881, Anklam 2011) ────────────────────
# Pre-conceptual bottom-up COE for ~900 MWe LIFE plant (indirect-drive D-T,
# liquid-Li first wall) -- same architecture as Inertia. Source: OSTI-1022881
# (LLNL-TR-480444). Provides order-of-magnitude sanity check on modeled outputs.
_LIFE_COE_2011    = 69.0    # $/MWh (2011$)
_LIFE_LASER_FRAC  = 0.30    # ~30% of LIFE COE (~$18/MWh) -- laser dominant cost
_LIFE_TARGET_M    = 110.0   # M$/yr target fuel cost at ~900 MWe (annualized)
_LIFE_ETA_TH      = 0.44    # thermal efficiency (model uses 0.45)
_LIFE_AVAIL_FOAK  = 0.70    # first-unit availability (NOAK target: 92%)

# Cross-check: LIFE target fuel cost scaled to 1,500 MWe vs. model's $1/target
_life_target_scaled_m = _LIFE_TARGET_M * (NATIVE_MW / 900.0)
_model_target_m = 1.0 * 315.0     # $1/target x 315M targets/yr [M$]
_goodin_target_m = 0.41 * (315.0 * NATIVE_MW / 900.0)  # $0.41 x 525M tgt/yr

print("LIFE Heritage Calibration (OSTI-1022881, Anklam 2011, 2011$, ~900 MWe):")
print(f"  LIFE COE:               ${_LIFE_COE_2011:.0f}/MWh")
print(f"  Laser fraction:         {_LIFE_LASER_FRAC:.0%} (~${_LIFE_LASER_FRAC*_LIFE_COE_2011:.0f}/MWh; ~40% of capital)")
print(f"  Target fuel:            ${_LIFE_TARGET_M:.0f}M/yr at ~900 MWe")
print(f"  Non-fuel O&M:           ~19% (~${0.19*_LIFE_COE_2011:.0f}/MWh)")
print(f"  Capital fraction:       ~60% of COE")
print(f"  LIFE thermal eff:       {_LIFE_ETA_TH:.0%}  [model uses {_SHARED_KWARGS['eta_th']:.0%}]")
print(f"  LIFE first-unit avail:  {_LIFE_AVAIL_FOAK:.0%}  [model uses NOAK {_SHARED_KWARGS['availability']:.0%}]")
print(f"  Target cost cross-check (scaled to {NATIVE_MW:.0f} MWe):")
print(f"    LIFE basis x(1500/900):  ${_life_target_scaled_m:.0f}M/yr")
print(f"    Model ($1/tgt x315M/yr): ${_model_target_m:.0f}M/yr  [{_model_target_m/_life_target_scaled_m:.1f}x LIFE basis]")
print(f"    Goodin ($0.41 NOAK):     ${_goodin_target_m:.0f}M/yr  [{_goodin_target_m/_life_target_scaled_m:.1f}x LIFE basis]")
print()

# ── Laser Cost Scenario Sweep (FOAK -> NOAK) ─────────────────────────────────
# DPSSL driver at $700-1,000/J FOAK is the dominant capital cost (analysis S5).
# Sweep shows LCOE across the FOAK-to-NOAK cost trajectory for 10 MJ total.
# All other parameters held at base-case values (1,500 MWe, q_eng=2.370).
# C220104 = cost_per_J [$/J] x 10 MJ = cost_per_J x 10 [M$]
#   (10e6 J x $/J x 1e-6 M$/$ = $/J x 10 M$)
# Source: analysis S5 cost overrides; carried-forward finding CF-F1 (blocking)

_laser_scenarios = [
    (700.0, "FOAK  ($700/J x 10 MJ = $7.0B)",  "first-of-a-kind"),
    (500.0, "Early ($500/J x 10 MJ = $5.0B)",  ""),
    (300.0, "Mid   ($300/J x 10 MJ = $3.0B)",  ""),
    (100.0, "NOAK  ($100/J x 10 MJ = $1.0B)",  "base case"),
]

print("Laser Cost Scenario Sweep (FOAK -> NOAK, 10 MJ system, 1,500 MWe):")
print(f"  {'Scenario':<42}  {'C220104 M$':>11}  {'LCOE $/MWh':>11}  {'OC $/kW':>9}  Notes")
print("  " + "-" * 90)

for _jpj, _label, _note in _laser_scenarios:
    _c220104_m = _jpj * 10.0   # $/J x 10 MJ -> M$
    _co = {"C220104": _c220104_m}
    _kw_laser = {**_SHARED_KWARGS, "cost_overrides": _co}
    _rl = model.forward(net_electric_mw=NATIVE_MW, **_kw_laser)
    _suffix = f"  <- {_note}" if _note else ""
    print(f"  {_label:<42}  {_c220104_m:>11.0f}  {_rl.costs.lcoe:>11.1f}  {_rl.costs.overnight_cost:>9.0f}{_suffix}")

print()

# ── Diode Replacement Periodic Capital (LCOE adder) ──────────────────────────
# Diodes ~1/3 of total laser capital (Haefner ILT IFE Workshop 2023).
# NOAK diode capital: ~$333M (1/3 of $1B C220104).
# Current devices fall 7-10x short of the 14-20 GShot lifetime target
# -> ~1.4-2.9 GShots today -> replacement every 4.4-9.2 yr at 10 Hz.
# LCOE adder = (diode_capital_M / interval_yr) * 1e6 / (annual_energy_GWh * 1e3)
# This periodic capital is NOT in the base O&M model (see Key Assumptions).
# Source: carried-forward finding CF-F2; Haefner ILT IFE Workshop 2023

_diode_cap_m = 1000.0 / 3.0                              # ~$333M NOAK (1/3 of C220104)
_annual_energy_gwh = NATIVE_MW * 8760.0 * 0.80 / 1000.0  # GWh/yr at 80% avail

_diode_scenarios = [
    (4.4,  "Current-gen short (4.4 yr, 1.4 GShot lifetime)"),
    (9.2,  "Current-gen long  (9.2 yr, 2.9 GShot lifetime)"),
    (44.0, "Target-met short (44 yr, 14 GShot lifetime)"),
    (63.0, "Target-met long  (63 yr, 20 GShot lifetime)"),
]

print("Diode Replacement Periodic Capital (annualized LCOE adder, not in base O&M):")
print(f"  Diode capital (NOAK, 1/3 of $1B C220104): ${_diode_cap_m:.0f}M")
print(f"  Annual energy at {NATIVE_MW:.0f} MWe / 80% avail: {_annual_energy_gwh:.0f} GWh/yr")
print(f"  {'Scenario':<50}  {'Interval':>9}  {'M$/yr':>7}  {'Adder $/MWh':>12}  {'Total LCOE':>11}")
print("  " + "-" * 97)

_base_lcoe = result.costs.lcoe
for _interval_yr, _dlabel in _diode_scenarios:
    _annual_m = _diode_cap_m / _interval_yr
    _adder = _annual_m * 1e6 / (_annual_energy_gwh * 1e3)   # $/MWh
    _total = _base_lcoe + _adder
    print(f"  {_dlabel:<50}  {_interval_yr:>8.1f}yr  {_annual_m:>7.1f}  {_adder:>12.1f}  {_total:>11.1f}")

_adder_lo = _diode_cap_m / 9.2 * 1e6 / (_annual_energy_gwh * 1e3)
_adder_hi = _diode_cap_m / 4.4 * 1e6 / (_annual_energy_gwh * 1e3)
_adder_target = _diode_cap_m / 44.0 * 1e6 / (_annual_energy_gwh * 1e3)
print()
print(f"  Base LCOE (no diode replacement): {_base_lcoe:.1f} $/MWh")
print(f"  Current-gen diode replacement adds ${_adder_lo:.1f}-${_adder_hi:.1f}/MWh")
print(f"  ({_adder_lo/_base_lcoe:.1%}-{_adder_hi/_base_lcoe:.1%} of base LCOE).")
print(f"  Closing the 7-10x lifetime gap would reduce adder to <${_adder_target:.2f}/MWh.")
