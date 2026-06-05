"""Laser ICF — Nanostructured Target (p-B11): 1costingfe model setup.

Modeling approach:
    Marvel Fusion design point (100 MW pilot, 2033 EU CORDIS target). Physics
    is entirely undemonstrated at gain-relevant scales; q_eng is the primary
    free parameter — treat all LCOE outputs as contingent on ignition. Primary
    result uses conservative 40% thermal efficiency (steam Rankine path) rather
    than Marvel's unvalidated 70% hybrid claim. HB11 Energy (1 Hz, steam,
    ~1 GW) included as a comparison scenario.

Concept choice rationale:
    LASER_IFE / PB11: aneutronic (>99% energy in charged alphas), room-
    temperature silicon nanowire targets, no tritium breeding, no heavy
    shielding, no superconducting magnets. Framework PB11 fuel defaults
    correctly reflect reduced blanket/shield/remote handling vs D-T baseline.

Key deviations from framework defaults:
    - eta_pin=0.10 (HB11 stated WPE target; Marvel unpublished; UNCERTAIN)
    - eta_th=0.40 (conservative steam; Marvel hybrid 70% is unvalidated)
    - q_eng=5.0 (UNCERTAIN: physics not demonstrated; 4 OOM gap for HB11)
    - availability=0.75 (no pulsed laser IFE plant operational analogue)
    - mn=1.0 (aneutronic: no neutron energy multiplication)
    - p_trit=0.0, p_cryo=0.0 (no tritium, no superconducting magnets)
    - blanket_t=0.20, ht_shield_t=0.10 (minimal: no breeding or heavy shielding)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import math

from costingfe import ConfinementConcept, CostModel, Fuel, PulsedConversion
from costingfe.layers.physics import pulsed_dec_forward as _pulsed_dec_fwd

# ── Model ─────────────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.PB11)

# DEC variant: activates INDUCTIVE_DEC conversion path so eta_dec
# appears in the physics computation and yields non-zero sensitivity.
# Used for the Marvel hybrid conversion sweep only; base cases use model.
model_dec = CostModel(
    concept=ConfinementConcept.LASER_IFE,
    fuel=Fuel.PB11,
    pulsed_conversion=PulsedConversion.INDUCTIVE_DEC,
)

# ── Plant Configuration Constants ─────────────────────────────────────

# Native design point: Marvel Fusion pilot plant
# Source: marvel-fusion-2025-updates.md §Objective; EU CORDIS Project ID 101189082
NATIVE_MW = 100.0

# UNCERTAIN: Engineering gain — physics undemonstrated at any scale.
# HB11 experimental: ~0.005% laser-to-alpha efficiency (~4 OOM from Q_eng>1).
# Marvel has published no yield data from any facility.
# Source: newatlas-energy-hb11-laser-fusion-demonstration.md; analysis.md §S1, §S2
# Value below assumes physics eventually works; do not treat as validated.
Q_ENG = 5.0

# Repetition rate: Marvel commercial target, confirmed by ATLAS facility design
# Source: analysis.md §5; optics-news-16-4-4.md; optics-news-15-10-4.md
F_REP_MARVEL = 10.0  # Hz

# UNCERTAIN: Laser wall-plug efficiency
# HB11 stated target: ~10% vs <1% for conventional high-power lasers.
# Marvel has not characterized WPE in any public source.
# 10% at 10 Hz with petawatt-class pulses is undemonstrated.
# Source: energynewsbulletin-energy-transition-features-articles.md; analysis.md §S2 Challenge 2
ETA_PIN = 0.10

# UNCERTAIN: Thermal-to-electric efficiency — conservative (steam Rankine path)
# Marvel claims hybrid magnetic + electrostatic + steam "up to ~70%" — marketing
# claim, no engineering detail, no demonstrated analogue (TRL 2).
# HB11 explicitly pivoted to steam cycle (~35-40%) as direct conversion not yet
# tractable at scale. Using 0.40 as conservative primary estimate.
# Source: dossier.md §Energy Capture; analysis.md §S2 Challenge 3; hb11-energy-technology.md
ETA_TH_CONSERVATIVE = 0.40

# UNCERTAIN: Plant availability — no pulsed laser IFE plant operational analogue.
# Lower than D-T baseline (0.85) given higher TRL uncertainty on all subsystems.
# Source: analysis.md §5 Missing Parameters
AVAILABILITY_MARVEL = 0.75

# ── Marvel hybrid DEC sweep parameters ────────────────────────────────
# f_pdv: fraction of charged-particle energy directed into PdV recovery loop.
# Framework default 0.80; no Marvel publication characterizes this value.
# eta_dec sweep: 0% = all DEC output wasted (steam-only fallback);
#                60% = near Marvel's claimed ~70% net efficiency upper bound.
# At q_eng=5 with f_pdv=0.80: DEC crossover to net-positive at eta_dec≈20%.
# Source: analysis.md §S2 Challenge 3; dossier.md §Energy Capture
F_PDV_MARVEL = 0.80  # UNCERTAIN: framework default; no Marvel publication
ETA_DEC_SWEEP = [0.0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60]

# ── Shared kwargs (Marvel design point) ───────────────────────────────
_SHARED_KWARGS = dict(
    availability=AVAILABILITY_MARVEL,  # UNCERTAIN; analysis.md §5 Missing Parameters
    lifetime_yr=30,                    # DEFAULT: standard 30-yr project life
    construction_time_yr=5.0,          # No large magnets; pulsed_laser_ife.yaml default
    interest_rate=0.07,                # DEFAULT: standard WACC
    inflation_rate=0.0245,             # DEFAULT: US CPI baseline
    noak=True,
    # ── Power balance ──────────────────────────────────────────────────
    q_eng=Q_ENG,                       # UNCERTAIN; see constant above
    f_rep=F_REP_MARVEL,                # 10 Hz; analysis.md §5; optics-news-16-4-4.md
    eta_pin=ETA_PIN,                   # UNCERTAIN; analysis.md §5
    eta_th=ETA_TH_CONSERVATIVE,        # UNCERTAIN; conservative steam estimate
    mn=1.0,                            # Aneutronic: no neutron multiplication
                                       # Source: dossier.md §Neutron Management; analysis.md §4
    f_sub=0.03,                        # DEFAULT: subsystem power fraction
    p_pump=1.0,                        # DEFAULT
    p_trit=0.0,                        # No tritium processing; p-B11 aneutronic
                                       # Source: analysis.md §4 (no tritium in fuel cycle)
    p_house=4.0,                       # DEFAULT
    p_cryo=0.0,                        # No superconducting magnets
                                       # Source: analysis.md §4 (no external confinement)
    p_target=2.0,                      # Elevated vs default: 10 Hz target factory power load
                                       # UNCERTAIN: no published data; conservative estimate
    # ── Chamber geometry (spherical) ───────────────────────────────────
    plasma_t=3.5,                      # DEFAULT: spherical chamber radius ~3.5 m
    blanket_t=0.20,                    # Minimal: no breeding blanket (aneutronic)
                                       # Source: analysis.md §4; dossier.md §Neutron Management
    ht_shield_t=0.10,                  # Minimal: no heavy neutron shielding
                                       # Source: hb11-2025-08-04-assoc-prof-patrick-burr.md
    structure_t=0.15,                  # DEFAULT: conventional steel (aneutronic environment)
    vessel_t=0.10,                     # DEFAULT
    # No cost_overrides: no published cost data exists for either company.
    # analysis.md §5: "Capital cost by subsystem — proprietary, blocking"
    # Framework pb11 fuel defaults handle reduced blanket/shield/remote handling.
)

# ── Primary result: Marvel pilot at native 100 MWe ────────────────────
result = model.forward(net_electric_mw=NATIVE_MW, **_SHARED_KWARGS)

# ── 1 GW result: scale from 100 MWe reference ─────────────────────────
# No cost_overrides supplied at 100 MWe, so override_reference_mw enables
# per-account power-law scaling from native to 1 GWe.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=NATIVE_MW,
    **_SHARED_KWARGS,
)

# ── Comparison: HB11 Energy design point (steam, 1 Hz, ~1 GW) ─────────
# More defensible design: validated fusion (single-shot), steam cycle,
# conventional steel. Still assumes physics gap is closed.
# Source: hb11-energy-technology.md; analysis.md §S7
result_hb11 = model.forward(
    net_electric_mw=1000.0,           # HB11 targets ~1 GW baseload; analysis.md §5
    availability=0.80,                 # UNCERTAIN; 1 Hz simpler maintenance than 10 Hz
    lifetime_yr=30,
    construction_time_yr=5.0,
    interest_rate=0.07,
    inflation_rate=0.0245,
    noak=True,
    q_eng=4.0,                        # UNCERTAIN; slightly lower Q for lower-rep design
    f_rep=1.0,                        # HB11 rep rate; hb11-energy-technology.md; analysis.md §5
    eta_pin=0.10,                     # UNCERTAIN; HB11 stated target
    eta_th=0.55,                       # standardized from 0.38 per scoring_framework.md (Energy Capture: Hybrid (thermal + direct))
    mn=1.0,
    f_sub=0.03,
    p_pump=1.0,
    p_trit=0.0,
    p_house=4.0,
    p_cryo=0.0,
    p_target=1.0,                     # 1 Hz: ~86k targets/day vs Marvel's 864k/day
    plasma_t=3.5,
    blanket_t=0.20,
    ht_shield_t=0.10,
    structure_t=0.15,
    vessel_t=0.10,
)

# ── Marvel hybrid DEC sweep ───────────────────────────────────────────
# Sweeps eta_dec (alpha capture efficiency) to quantify the LCOE lever
# claimed by Marvel's hybrid electrostatic/magnetic/steam conversion.
#
# Method: fix p_fus at the thermal baseline (100 MWe, eta_th=40%) and
# let p_net increase as eta_dec rises.  This is the correct physical
# story: the same fusion driver produces more electricity as DEC
# efficiency improves.  The alternative (fix p_net, vary q_eng) would
# require less fusion power per unit output — showing LCOE reduction
# from a smaller driver — but is harder to compute without re-solving
# the inverse at variable q_eng.
#
# Approach:
#   1. Get p_fus and e_driver_mj from the thermal base result.
#   2. For each eta_dec, call pulsed_dec_forward (fixed p_fus) to get
#      the resulting p_net and natural q_eng.
#   3. Pass those to model_dec.forward() to price the scenario.
#
# At eta_dec=0 the DEC model still installs inverters and cap-bank
# switchgear (delta_switch + delta_inv + delta_ctrl ≈ 15 M$), explaining
# the ~5 $/MWh overhead relative to the pure-thermal Marvel result.
# Source: analysis.md §S2 Challenge 3; dossier.md §Energy Capture

_F_RAD_PB11 = 0.15  # costing_constants.yaml: PB11 bremsstrahlung fraction
_DEC_BASE_P_FUS = float(result.power_table.p_fus)
_DEC_BASE_E_DRIVER_MJ = float(result.power_table.e_driver_mj)
# Exclude q_eng: the natural q_eng from the forward pass is used instead
_DEC_SWEEP_KWARGS = {k: v for k, v in _SHARED_KWARGS.items() if k != "q_eng"}

results_dec_sweep = []
for _eta in ETA_DEC_SWEEP:
    # Forward pass: fixed p_fus, compute p_net and natural q_eng at this eta_dec
    _pt_fwd = _pulsed_dec_fwd(
        p_fus=_DEC_BASE_P_FUS,
        fuel=Fuel.PB11,
        e_driver_mj=_DEC_BASE_E_DRIVER_MJ,
        f_rep=F_REP_MARVEL,
        mn=1.0,
        eta_th=ETA_TH_CONSERVATIVE,
        eta_pin=ETA_PIN,
        eta_dec=_eta,
        f_pdv=F_PDV_MARVEL,
        f_rad=_F_RAD_PB11,
        f_sub=0.03,
        p_pump=1.0,
        p_trit=0.0,
        p_house=4.0,
        p_cryo=0.0,
        p_target=2.0,
    )
    _p_net_at_eta = float(_pt_fwd.p_net)
    _q_eng_at_eta = float(_pt_fwd.q_eng)
    _r = model_dec.forward(
        net_electric_mw=_p_net_at_eta,
        q_eng=_q_eng_at_eta,
        eta_dec=_eta,
        f_pdv=F_PDV_MARVEL,
        **_DEC_SWEEP_KWARGS,
    )
    results_dec_sweep.append((_eta, _r))

# ── Results ────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table
c1 = result_1gw.costs
pt1 = result_1gw.power_table
c_hb11 = result_hb11.costs
pt_hb11 = result_hb11.power_table

print("=" * 72)
print("Laser ICF — Nanostructured Target (p-B11)")
print("** ALL LCOE VALUES CONTINGENT ON UNDEMONSTRATED IGNITION PHYSICS **")
print("=" * 72)

print(f"\n── Marvel Pilot (100 MWe, 10 Hz, eta_th=40%, eta_pin=10%) ──")
print(f"LCOE:      {c.lcoe:.1f} $/MWh   |  Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion:    {pt.p_fus:.0f} MW     |  Net: {pt.p_net:.0f} MW   |  Q_eng: {pt.q_eng:.1f}")
print(f"Q_sci:     {pt.q_sci:.1f}         |  Recirc frac: {pt.rec_frac:.2%}")

print(f"\n── Marvel Scaled to 1 GWe (from 100 MWe reference, per-account scaling) ──")
print(f"LCOE:      {c1.lcoe:.1f} $/MWh  |  Overnight: {c1.overnight_cost:.0f} $/kW")
print(f"Fusion:    {pt1.p_fus:.0f} MW   |  Net: {pt1.p_net:.0f} MW   |  Q_eng: {pt1.q_eng:.1f}")

print(f"\n── HB11 Energy (1 GWe, 1 Hz, steam cycle, eta_th=38%) ──")
print(f"LCOE:      {c_hb11.lcoe:.1f} $/MWh  |  Overnight: {c_hb11.overnight_cost:.0f} $/kW")
print(f"Fusion:    {pt_hb11.p_fus:.0f} MW   |  Net: {pt_hb11.p_net:.0f} MW   |  Q_eng: {pt_hb11.q_eng:.1f}")

print("\n── Marvel Hybrid DEC Sweep (INDUCTIVE_DEC, fixed p_fus=base, f_pdv=0.80) ──")
print("  p_fus fixed at thermal baseline; p_net increases with eta_dec.")
print("  eta_dec=0%: DEC hardware overhead only (~15 M$ inverters+switches);")
print("  eta_dec=60%: ~70–75% more net output from same fusion investment.")
print("  ~5 $/MWh offset vs thermal result at eta_dec=0 = cost of installed DEC infra.")
print(f"\n  {'eta_dec':>8}  {'LCOE ($/MWh)':>14}  {'p_net (MW)':>11}  {'q_eng':>7}  {'recirc':>8}")
print("  " + "-" * 56)
for _eta, _r in results_dec_sweep:
    _c = _r.costs
    _pt = _r.power_table
    _rec = getattr(_pt, "rec_frac", float("nan"))
    _qe = getattr(_pt, "q_eng", float("nan"))
    print(f"  {_eta:>7.0%}  {_c.lcoe:>14.1f}  {_pt.p_net:>11.1f}  {_qe:>7.2f}  {_rec:>8.2%}")

# ── CAS Breakdown ──────────────────────────────────────────────────────
print("\n── CAS Breakdown: Marvel 100 MWe pilot ──")
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

print(f"\n{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")

# ── CAS22 Detail ──────────────────────────────────────────────────────
print("\n── CAS22 Sub-accounts (Marvel 100 MWe) ──")
for key, val in result.cas22_detail.items():
    if float(val) > 0:
        print(f"  {key}: {float(val):.1f} M$")

# ── Key Assumptions ───────────────────────────────────────────────────
print("""
── Key Assumptions / Data Quality ──────────────────────────────────────
CRITICAL UNCERTAIN — physics not demonstrated:
  q_eng = 5.0     ASSUMED. HB11 data: ~0.005% laser-to-alpha efficiency
                  (~4 OOM from net energy gain). Marvel: no yield data.
                  All LCOE results are contingent on ignition being achieved.

  eta_pin = 10%   UNCERTAIN. HB11 stated target; Marvel unpublished.
                  10 Hz continuous at PW-class energies is undemonstrated.

  eta_th = 40%    CONSERVATIVE. Marvel claims hybrid "up to ~70%" with
                  no engineering detail (TRL 2). HB11 uses ~38% steam.
                  Primary result uses steam-only assumption.

MEDIUM CONFIDENCE:
  f_rep = 10 Hz   Marvel ATLAS facility design; not yet at commercial scale.
  availability=75% No pulsed laser IFE plant analogue; placeholder.
  p-B11 aneutronic No blanket/tritium/heavy shielding confirmed.

FRAMEWORK DEFAULTS (no override data available):
  Laser driver    8.0 M$/MW_driver (NOAK DPSSL; no Marvel/HB11 cost data)
  Target factory  244 M$ at 1 GWe ref (Goodin et al. analogue)
  O&M             24 M$/yr base (pb11, aneutronic, no tritium)
  B-11 fuel cost  75 $/kg NOAK (industrial estimate; enrichment need unconfirmed)

SUPPLY CHAIN ADVANTAGES vs D-T:
  No tritium → no breeding blanket, no TBR constraint, no tritium startup cost
  No HTS tape → no superconducting magnet supply chain risk
  No beryllium/Li-6 → no exotic breeder materials
  Standard steel construction viable (UNSW collaboration confirms)
""")

# ── Sensitivity Analysis ──────────────────────────────────────────────
# NaN values in JAX autodiff arise from jnp.ceil in core_lifetime/availability
# calculations (ceil is not smoothly differentiable). Patch with central finite
# differences for any parameter that JAX cannot differentiate cleanly.
def _patch_nan_sensitivities(mdl, params, sens_dict):
    """Replace NaN elasticities with central finite-difference estimates."""
    import jax.numpy as jnp
    lcoe_fn, keys, base_vals = mdl._build_lcoe_fn(params)
    base_lcoe = float(lcoe_fn(base_vals))
    for category_dict in sens_dict.values():
        for k in list(category_dict.keys()):
            if math.isnan(category_dict[k]) and k in keys:
                idx = keys.index(k)
                p0 = float(base_vals[idx])
                h = p0 * 0.01
                if h == 0.0:
                    continue
                x_hi = base_vals.at[idx].set(p0 + h)
                x_lo = base_vals.at[idx].set(p0 - h)
                grad = (float(lcoe_fn(x_hi)) - float(lcoe_fn(x_lo))) / (2 * h)
                category_dict[k] = grad * p0 / base_lcoe
    return sens_dict

sens = model.sensitivity(result.params)
sens = _patch_nan_sensitivities(model, result.params, sens)

# Compute eta_dec elasticity using the DEC model (thermal model has eta_dec=0,
# giving a trivially undefined elasticity; DEC model activates the physics path).
_dec_params = dict(result.params)
_dec_params["eta_dec"] = 0.30  # mid-range base point for elasticity
_dec_params["f_pdv"] = F_PDV_MARVEL
_result_dec_base = model_dec.forward(
    net_electric_mw=NATIVE_MW,
    eta_dec=0.30,
    f_pdv=F_PDV_MARVEL,
    **_SHARED_KWARGS,
)
_sens_dec = model_dec.sensitivity(_result_dec_base.params)
_eta_dec_elasticity = _sens_dec.get("engineering", {}).get("eta_dec", float("nan"))

print("── Sensitivity (elasticity = %LCOE / %param) — Marvel 100 MWe ──")
print("-" * 56)
print("  (NaN values replaced with central finite-difference estimates)")
print(f"  eta_dec elasticity (DEC model, base eta_dec=30%): {_eta_dec_elasticity:+.4f}")

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
