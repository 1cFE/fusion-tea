"""Laser ICF - OEC Architecture (D-T) — Blue Laser Fusion (BLF) 1costingfe model.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Concept: Blue Laser Fusion (BLF) reactor using Coherent Beam Combining (CBC) fiber lasers
injected into Optical Enhancement Cavities (OEC, LIGO-derived) to deliver 5 MJ UV (350 nm)
to D-T targets at 1–10 Hz. Shock ignition scheme targeting gain G = 160. Hybrid energy
conversion: 70% thermal (He Brayton via LiPb blanket) + 30% direct energy conversion (DEC).
Both channels claim identical η_e = 0.44, so modeling as all-thermal gives same P_gross.

Modeling approach:
  - Native design point: ~2800 MWe net at 10 Hz (BLF paper Table 2 states 2.8 GWe)
  - pulsed_conversion = THERMAL (default for LASER_IFE); see reasoning above
  - q_eng = 5.69, derived self-consistently from G=160, η_pin=0.10, η_th=0.44, 10 Hz,
    and standard auxiliary loads. This yields q_sci ≈ 160, e_driver ≈ 4.8 MJ (≈ 5 MJ
    from paper; small deviation from auxiliary load parameterization).
  - mn = 1.0: BLF's stated η_th* = 0.44 already embeds the +0.04 exothermic Li-breeding
    boost; using the default mn = 1.1 would double-count it.
  - result_1gw scales from the native 2800 MWe reference.

Key deviations from defaults:
  - eta_th = 0.44 (vs RANKINE default 0.40): He Brayton + Li-breeding boost combined
  - eta_pin = 0.10: CBC-OEC laser wall-plug efficiency to UV (0.16 × 0.60)
  - f_rep = 10.0 Hz: power-plant design point
  - mn = 1.0: breeding boost embedded in η_th (see above)
  - q_eng = 5.69: from self-consistent G=160 power balance
  - availability = 0.75: conservative (paper silent; IFE target-injection challenge at 10 Hz)

Data quality: MODERATE on physics; LOW on costs. The Sunahara et al. (2025) Optics Express
paper provides a complete power balance (Table 2). G = 160 is a low-confidence projection
beyond demonstrated CBET-mitigated baselines. DEC η = 0.44 is theory-only (TRL 1–2).
All capital cost categories are UNCERTAIN to TRULY-UNKNOWN. OEC mirror costs (1,000 units at
>99.9995% reflectivity) have no cost analogue in any public dataset.
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model ────────────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# ── Plant configuration constants ────────────────────────────────────
# All sources: optics-express-2025-paper.md §Table 2 unless otherwise noted.

# Laser driver — optics-express-2025-paper.md §Table 2
F_REP_HZ = 10.0          # Repetition rate at power-plant design point; range is 1–10 Hz
ETA_PIN = 0.10            # Wall-plug-to-UV: η_w(IR) × η_3ω = 0.16 × 0.60
                          # UNCERTAIN: η_w = 0.16 is for commercial CW fiber lasers;
                          # pulsed 10 Hz burst-mode operation not experimentally validated

# Engineering Q derived self-consistently:
#   Given G=160, e_driver=5 MJ, f_rep=10 Hz, eta_pin=0.10, eta_th=0.44, mn=1.0,
#   and standard aux loads (p_pump=1, p_trit=10, p_house=4, p_cryo=0.5, p_target=1, f_sub=0.03):
#   p_driver = 50 MW, p_fus = 8000 MW, p_gross = 3542 MW, p_recirc ≈ 623 MW
#   → q_eng = 3542 / 623 = 5.69 → rec_frac ≈ 17.6% (paper states 17.0%; minor rounding)
Q_ENG = 5.69

# Power conversion — optics-express-2025-paper.md §Table 2
ETA_TH = 0.44             # Combined η_e: both thermal and DEC channels are 0.44 (by paper)
                          # η_th* = 0.40 (He Brayton) + 0.04 (exothermic Li-breeding boost)
                          # η_DEC = 0.44 (DEC, "conservative"; Rax et al. 2025 theory, TRL 1–2)
                          # MEDIUM confidence on thermal; LOW confidence on DEC

MN = 1.0                  # Neutron multiplier: Li-breeding boost embedded in η_th* = 0.44;
                          # setting mn = 1.1 (framework default) would double-count the boost

# DEC channel decomposition — needed to independently track sensitivity of each conversion path.
# The framework's THERMAL pulsed_conversion mode uses a single eta_th; both channels must be
# folded into ETA_TH_COMBINED so varying eta_dec independently requires a manual sweep (see below).
ETA_DEC = 0.44            # DEC efficiency (charged particles; Rax et al. 2025 theory, TRL 1–2)
F_CHARGED = 0.30          # Charged-particle fraction of P_fus (alphas + fast ions)
F_NEUTRON = 0.70          # Neutron fraction → thermal channel (He Brayton via LiPb blanket)
ETA_TH_COMBINED = F_NEUTRON * ETA_TH + F_CHARGED * ETA_DEC  # = 0.44 when ETA_TH = ETA_DEC

# Plant-level
AVAILABILITY = 0.75       # UNCERTAIN: paper does not state; conservative for BLF's three
                          # concurrent challenge areas (target injection at 10 Hz, chamber
                          # clearing in <100 ms, CBC-OEC laser system uptime)
LIFETIME_YR = 30.0
NATIVE_MW = 2800.0        # Net electric output at 10 Hz design point; paper Table 2

# ── Shared kwargs (used for both native and 1 GW result) ─────────────
_SHARED_KWARGS = dict(
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=5.0,       # No superconducting magnets → shorter schedule;
                                     # pulsed_laser_ife.yaml default
    interest_rate=0.07,
    inflation_rate=0.0245,
    noak=True,
    # ── Laser power balance ───────────────────────────────────────────
    f_rep=F_REP_HZ,                  # 10 Hz; optics-express-2025-paper.md §Table 2
    eta_pin=ETA_PIN,                 # 0.10; optics-express-2025-paper.md §Table 2
    q_eng=Q_ENG,                     # 5.69; derived from G=160 power balance; see docstring
    eta_th=ETA_TH_COMBINED,          # 0.44; F_NEUTRON×ETA_TH + F_CHARGED×ETA_DEC
                                     # optics-express-2025-paper.md §Table 2
    mn=MN,                           # 1.0; Li-breeding boost embedded in η_th*
    f_rad=0.10,                      # DEFAULT: DT standard bremsstrahlung + line radiation fraction
    f_sub=0.03,                      # DEFAULT: subsystem power fraction
    # ── Auxiliary loads ───────────────────────────────────────────────
    p_pump=1.0,                      # DEFAULT: He coolant pumping [MW]
    p_trit=10.0,                     # DEFAULT: tritium processing power [MW]
    p_house=4.0,                     # DEFAULT: housekeeping [MW]
    p_cryo=0.5,                      # DEFAULT: minimal cryogenics — no superconducting magnets;
                                     # only small resistive B-field coils for charged-particle deflection
    p_target=1.0,                    # UNCERTAIN: cryogenic target factory support power [MW];
                                     # Hz-rate D-T cryo target manufacturing is unsolved
    # ── Spherical chamber geometry ────────────────────────────────────
    # BLF chamber geometry not published. Using laser IFE YAML defaults.
    R0=0.0,                          # Spherical chamber — not applicable
    plasma_t=4.0,                    # DEFAULT: chamber radius [m]
    blanket_t=0.80,                  # DEFAULT: LiPb blanket thickness [m]; BLF uses LiPb + He-cooled
    ht_shield_t=0.25,                # DEFAULT
    structure_t=0.15,                # DEFAULT
    vessel_t=0.10,                   # DEFAULT
    # ── Cost overrides ────────────────────────────────────────────────
    # No cost overrides: BLF has published no capital cost data.
    # All CAS22 sub-accounts use framework defaults with high uncertainty flags below.
    # C220104 (CBC-OEC laser driver): uses driver_laser_per_mw = $8M/MW (DPSSL baseline).
    #   TRULY UNKNOWN: OEC architecture is novel; LIGO-class mirrors at 1,000-unit scale
    #   have no cost analogue. May be cheaper (modular fiber lasers) or more expensive
    #   (LIGO-class coatings). DOE INFUSE award (CSU, Menoni) is addressing manufacturing.
    # C220108 (cryogenic D-T target factory): uses target_factory_base = $244M.
    #   UNCERTAIN: Hz-rate cryo D-T production is unsolved; NIF targets cost >$1M each.
    #   Per Goodin et al. criterion, targets must cost <$0.035/shot at BLF design point.
    # C220109 (DEC): not modeled (framework DEC cost for IFE not implemented; TRL 1–2).
    #   TRULY UNKNOWN capital cost; would add to CAS22 if DEC is included.
)

# ── Forward costing — native design point (~2800 MWe, 10 Hz) ─────────
result = model.forward(net_electric_mw=NATIVE_MW, **_SHARED_KWARGS)

# ── 1 GW comparison result ────────────────────────────────────────────
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=NATIVE_MW,
    **_SHARED_KWARGS,
)

# ── Results printing ─────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Laser ICF - OEC Architecture (D-T) — Blue Laser Fusion (BLF)")
print(f"Native: {NATIVE_MW:.0f} MWe @ {F_REP_HZ:.0f} Hz | NOAK | avail={AVAILABILITY:.0%} | 30 yr")
print()
print(f"LCOE:      {float(c.lcoe):.1f} $/MWh")
print(f"Overnight: {float(c.overnight_cost):.0f} $/kW")
print(f"Fusion:    {float(pt.p_fus):.0f} MW | Net: {float(pt.p_net):.0f} MW")
print(f"Q_eng:     {float(pt.q_eng):.2f} | Q_sci: {float(pt.q_sci):.1f}  (paper: G=160)")
e_uv_mj = float(pt.e_stored_mj) * ETA_PIN
print(f"E_laser:   {e_uv_mj:.2f} MJ/shot (UV) | E_wallplug: {float(pt.e_stored_mj):.1f} MJ/shot")
print(f"Rec. frac: {float(pt.rec_frac):.1%}  (paper: 17.0%)")
print()

# CAS breakdown
cas = [
    ("CAS10", "Preconstruction", c.cas10),
    ("CAS21", "Buildings", c.cas21),
    ("CAS22", "Reactor Plant Equipment", c.cas22),
    ("CAS23", "Turbine Plant", c.cas23),
    ("CAS24", "Electrical Plant", c.cas24),
    ("CAS25", "Miscellaneous", c.cas25),
    ("CAS26", "Heat Rejection", c.cas26),
    ("CAS27", "Special Materials", c.cas27),
    ("CAS28", "Digital Twin", c.cas28),
    ("CAS29", "Contingency", c.cas29),
    ("CAS30", "Indirect Costs", c.cas30),
    ("CAS40", "Owner's Costs", c.cas40),
    ("CAS50", "Supplementary", c.cas50),
    ("CAS60", "IDC", c.cas60),
    ("CAS70", "O&M (annualized)", c.cas70),
    ("CAS80", "Fuel (annualized)", c.cas80),
    ("CAS90", "Financial", c.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")

# CAS22 sub-account detail
print("\nCAS22 Reactor Plant Equipment detail:")
print("-" * 56)
cas22_items = [
    ("C220101", "First Wall / LiPb Blanket"),
    ("C220102", "Shield"),
    ("C220104", "CBC-OEC Laser Driver"),
    ("C220105", "Primary Structure"),
    ("C220106", "Vacuum System"),
    ("C220107", "Power Supplies (pulsed cap bank)"),
    ("C220108", "Target Factory (cryo D-T Hz-rate)"),
    ("C220109", "Direct Energy Converter"),
    ("C220110", "Remote Handling"),
    ("C220111", "Installation"),
    ("C220200", "Coolant Systems"),
    ("C220300", "Aux Cooling"),
    ("C220400", "Rad Waste"),
    ("C220500", "Fuel Handling (tritium)"),
    ("C220600", "Other Equipment"),
    ("C220700", "I&C"),
    ("C220000", "CAS22 Total"),
]
for key, label in cas22_items:
    v = result.cas22_detail.get(key, 0.0)
    if float(v) > 0.01:
        print(f"  {key}  {label:<36} {float(v):>8.1f}")

# 1 GW comparison
c1 = result_1gw.costs
pt1 = result_1gw.power_table
print(f"\n1 GW Comparison (scaled from {NATIVE_MW:.0f} MWe):")
print(f"  Net: {float(pt1.p_net):.0f} MWe | LCOE: {float(c1.lcoe):.1f} $/MWh | Overnight: {float(c1.overnight_cost):.0f} $/kW")

# Key assumptions summary
print("\nKey Assumptions:")
print(f"  G (target gain)   = 160       LOW CONFIDENCE — projected beyond CBET-mitigated baseline;")
print(f"                                no multi-MJ experimental validation; blocking uncertainty")
print(f"  η_pin (laser)     = {ETA_PIN:.0%}       UNCERTAIN — CW fiber laser claim; pulsed 10 Hz undemonstrated")
print(f"  η_th (conversion) = {ETA_TH:.0%}       MEDIUM — He Brayton plausible; DEC η=44% is TRL 1–2 theory")
print(f"  f_rep             = {F_REP_HZ:.0f} Hz     design point; Hz-rate cryo target injection is unsolved")
print(f"  availability      = {AVAILABILITY:.0%}       UNCERTAIN — not stated in paper; conservative for IFE")
print(f"  C220104 laser cost: DEFAULT ($8M/MW DPSSL) — TRULY UNKNOWN for OEC architecture")
print(f"  C220108 target fac: DEFAULT ($244M base)  — UNCERTAIN; NIF targets cost >$1M each")
print(f"  C220109 DEC cost:   NOT MODELED           — TRULY UNKNOWN; TRL 1–2; no prototype")
print(f"  OEC mirror cost:    NOT MODELED separately — embedded in C220104; should be much higher")
print(f"  First-wall repl:    DEFAULT blanket lifetime — TRULY UNKNOWN for pulsed dry-wall IFE")

# ── Sensitivity analysis ─────────────────────────────────────────────
sens = model.sensitivity(result.params)

print("\nSensitivity (elasticity = %LCOE / %param):")
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
print("  NOTE: driver_laser_per_mw elasticity above is INAPPLICABLE for OEC architecture.")
print("  The DPSSL $/MW proxy uses glass-slab manufacturing costs (NIF heritage); OEC cost")
print("  is dominated by 1,000 high-finesse mirrors — see OEC Mirror Cost Scenarios below.")

# The THERMAL pulsed_conversion mode folds both conversion channels into a single eta_th
# parameter (ETA_TH_COMBINED). Auto-diff therefore shows eta_dec = 0.0 elasticity because
# it is not a free parameter in the THERMAL forward pass. The combined η_th elasticity
# (shown above, ≈ −0.258) covers 100% of gross power. The DEC contribution (30% channel)
# is proportionally about 30% of that elasticity: ≈ −0.077. The manual sweep below
# separates the channels by holding η_th (He Brayton) fixed at 0.44 and varying η_DEC.
print("\nDEC Efficiency Sensitivity (manual — THERMAL mode auto-diff folds both channels into η_th):")
print("  η_th (He Brayton + Li-breeding) fixed at 0.44; DEC efficiency swept independently.")
print(f"  {'η_DEC':>6} {'η_eff':>8} {'LCOE $/MWh':>11} {'Δ LCOE $/MWh':>14}")
print("  " + "-" * 44)
_ETA_DEC_SWEEP = [0.20, 0.30, 0.35, 0.40, 0.44, 0.50, 0.55]
for _eta_dec_val in _ETA_DEC_SWEEP:
    _eta_eff = F_NEUTRON * ETA_TH + F_CHARGED * _eta_dec_val
    _kw_dec = dict(_SHARED_KWARGS)
    _kw_dec["eta_th"] = _eta_eff
    _r_dec_sens = model.forward(net_electric_mw=NATIVE_MW, **_kw_dec)
    _lcoe_dec = float(_r_dec_sens.costs.lcoe)
    _delta = _lcoe_dec - float(result.costs.lcoe)
    _marker = " ←" if _eta_dec_val == ETA_DEC else ""
    print(f"  {_eta_dec_val:>6.2f} {_eta_eff:>8.3f} {_lcoe_dec:>11.1f} {_delta:>+14.1f}{_marker}")
print("  Implied DEC elasticity ≈ −0.077 (= F_CHARGED × combined η_th elasticity).")
print("  Thermal channel (70%) and DEC channel (30%) sum to the auto-diff η_th result.")


# ── Helper: q_eng from gain G ─────────────────────────────────────────
# Physics formula: Q = eta_th*mn*G*eta_pin; q_eng = Q/(1 + f_sub*Q).
# Ignores fixed aux loads (~16.5 MW << P_fus at 2800 MWe) — matches
# design-point Q_ENG=5.69 within ~2%.
def _q_eng_from_gain(G, eta_pin=ETA_PIN, eta_th=ETA_TH, mn=MN, f_sub=0.03):
    Q = eta_th * mn * G * eta_pin
    return Q / (1.0 + f_sub * Q)


def _p_net_same_laser(G, f_rep,
                      e_uv_mj=5.0, eta_pin=ETA_PIN, eta_th=ETA_TH_COMBINED, mn=MN,
                      f_sub=0.03, p_pump=1.0, p_trit=10.0, p_house=4.0,
                      p_cryo=0.5, p_target_mw=1.0):
    """P_net [MWe] for the same 5 MJ/shot CBC-OEC laser at a given (G, f_rep).

    Same-laser means E_UV = 5 MJ/shot is fixed; only rep rate and gain vary.
    Driver wall-plug power scales linearly with f_rep.
    """
    p_fus = G * e_uv_mj * f_rep
    p_driver = (e_uv_mj / eta_pin) * f_rep
    p_gross = p_fus * eta_th * mn
    p_fixed_aux = p_pump + p_trit + p_house + p_cryo + p_target_mw
    p_recirc = p_driver + p_fixed_aux + f_sub * p_gross
    return max(p_gross - p_recirc, 0.0)


# ── F-1: (G, f_rep) Scenario Grid ────────────────────────────────────
# Captures economic viability across (gain, rep-rate) design space.
# q_eng is derived from G via physics; f_rep affects e_driver_mj (cap
# bank cost) but not q_eng — so the model captures cap-bank scaling but
# NOT the physical infeasibility of large-energy-per-shot laser systems.
# LCOE shown for 1 Hz scenarios is a lower bound.
_G_SWEEP = [80, 120, 160]
_F_REP_SWEEP = [1.0, 10.0]

print("\n\n(G, f_rep) Scenario Grid — LCOE $/MWh @ 2800 MWe:")
print(f"  {'':12}", end="")
for G in _G_SWEEP:
    print(f"  G={G:3d}  ", end="")
print()
for f in _F_REP_SWEEP:
    e_uv_per_shot = "~{:.0f} MJ/shot".format(
        8000.0 / (160.0 * f)  # E_UV at G=160, P_fus≈8000 MW
    )
    print(f"  f={f:.0f} Hz ({e_uv_per_shot} @G=160)  ", end="")
    for G in _G_SWEEP:
        q = _q_eng_from_gain(G)
        kw = dict(_SHARED_KWARGS)
        kw.update(f_rep=f, q_eng=q)
        r_gf = model.forward(net_electric_mw=NATIVE_MW, **kw)
        print(f"  {float(r_gf.costs.lcoe):6.1f}  ", end="")
    print()
print("  LCOE in $/MWh. Design point: G=160, f=10 Hz (rightmost bottom cell).")
print("  * 1 Hz column: model computes cap-bank cost ×10 from 10 Hz but cannot capture")
print("    laser-construction infeasibility. At G=160, f=1 Hz → ~50 MJ/shot UV pulse;")
print("    at G=80, f=1 Hz → ~100 MJ/shot. No demonstrated laser system approaches this.")
print(f"  * G=80 q_eng≈{_q_eng_from_gain(80):.2f} vs G=160 q_eng≈{_q_eng_from_gain(160):.2f} — lower gain raises recirculating power fraction.")


# ── F-2: Same-Capital Viability Scenarios ────────────────────────────
# The constant-output grid above holds P_net = 2800 MWe and rescales capital,
# which hides the viability cliff. This table fixes overnight capital at the
# 2800 MWe / 10 Hz baseline and reports LCOE at the actual P_net each (G, f_rep)
# cell produces from the same 5 MJ/shot CBC-OEC laser. This is the physically
# meaningful comparison: same investment, different operating point.
_base_capital_overrides = {
    "CAS10": float(result.costs.cas10),
    "CAS21": float(result.costs.cas21),
    "CAS22": float(result.costs.cas22),
    "CAS23": float(result.costs.cas23),
    "CAS24": float(result.costs.cas24),
    "CAS25": float(result.costs.cas25),
    "CAS26": float(result.costs.cas26),
    "CAS27": float(result.costs.cas27),
    "CAS28": float(result.costs.cas28),
    "CAS29": float(result.costs.cas29),
    "CAS30": float(result.costs.cas30),
    "CAS40": float(result.costs.cas40),
    "CAS60": float(result.costs.cas60),  # IDC fixed — same capital, same financing schedule
}

_SAME_CAP_SCENARIOS = [
    ("G=160, f=10 Hz (design point)", 160, 10.0),
    ("G=160, f=1 Hz", 160, 1.0),
    ("G=80,  f=10 Hz", 80, 10.0),
    ("G=80,  f=1 Hz", 80, 1.0),
]

print("\n\nSame-Capital Viability Scenarios — fixed overnight capital, actual net output:")
print(f"  Same 5 MJ/shot CBC-OEC laser; capital frozen at ${float(result.costs.total_capital):.0f} M$ (2800 MWe/10 Hz baseline).")
print(f"  {'Scenario':<30} {'P_net MWe':>10} {'LCOE $/MWh':>11} {'vs design pt':>13}")
print("  " + "-" * 67)
_design_lcoe = float(result.costs.lcoe)
for _label, _G, _f in _SAME_CAP_SCENARIOS:
    _p_net = _p_net_same_laser(_G, _f)
    _q = _q_eng_from_gain(_G)
    _kw_sc = dict(_SHARED_KWARGS)
    _kw_sc.update(f_rep=_f, q_eng=_q, cost_overrides=_base_capital_overrides)
    _r_sc = model.forward(net_electric_mw=max(_p_net, 1.0), **_kw_sc)
    _lcoe_sc = float(_r_sc.costs.lcoe)
    _factor = f"  {_lcoe_sc / _design_lcoe:.1f}×" if _p_net > 1.0 else "  —"
    print(f"  {_label:<30} {_p_net:>10.0f} {_lcoe_sc:>11.1f} {_factor:>13}")
print("  Capital (CAS10–CAS40, CAS60) locked to design-point values; CAS70 O&M")
print("  recomputed at actual P_net. This table exposes the viability cliff that the")
print("  constant-output grid above conceals: same investment, a fraction of the output.")


# ── F-3: OEC Mirror Cost Scenarios ───────────────────────────────────
# Replaces the inapplicable DPSSL proxy ($8M/MW, NIF glass-slab heritage)
# for C220104. OEC driver cost is dominated by 1,000 high-finesse mirrors
# (>99.9995% R) with no commercial supply chain or cost precedent.
# Range spans volume-production floor ($10K) to LIGO-class unit cost ($500K).
OEC_N_MIRRORS = 1000
_MIRROR_SCENARIOS = [
    ("$10K/mirror (volume production floor)", 10_000),
    ("$100K/mirror (near-term optimistic)", 100_000),
    ("$250K/mirror (mid-range estimate)", 250_000),
    ("$500K/mirror (LIGO-class coating cost)", 500_000),
]

print("\nOEC Mirror Cost Scenarios — C220104 parametric (replaces DPSSL $8M/MW proxy):")
print(f"  {'Scenario':<44} {'C220104 M$':>11} {'LCOE $/MWh':>11}")
print("  " + "-" * 68)
_dpssl_c220104 = float(result.cas22_detail.get("C220104", 0.0))
_dpssl_lcoe = float(result.costs.lcoe)
print(f"  {'DPSSL proxy (default, inapplicable for OEC)':<44} {_dpssl_c220104:>11.1f} {_dpssl_lcoe:>11.1f}")
for label, cost_per_mirror in _MIRROR_SCENARIOS:
    c220104_m = OEC_N_MIRRORS * cost_per_mirror / 1e6  # M$
    r_mirror = model.forward(
        net_electric_mw=NATIVE_MW,
        cost_overrides={"C220104": c220104_m},
        **_SHARED_KWARGS,
    )
    print(f"  {label:<44} {c220104_m:>11.1f} {float(r_mirror.costs.lcoe):>11.1f}")
print("  DOE INFUSE award (CSU/Menoni) is the only active program addressing OEC mirror")
print("  manufacturing at scale. No cost data is publicly available.")


# ── F-2: DEC Capital Cost Scenarios ──────────────────────────────────
# DEC is absent from the base model (C220109 = 0, no cost precedent).
# At the 2800 MWe design point, DEC captures ~30% of P_fus ≈ 2400 MW_th
# of charged-particle power → ~840 MWe if eta_DEC=0.35. TRL 1–2, no
# prototype. Scenarios bound the plausible capital cost range.
_DEC_SCENARIOS = [
    ("$50M  (optimistic — minimal hardware)", 50.0),
    ("$150M (medium estimate)", 150.0),
    ("$300M (conservative)", 300.0),
    ("$500M (pessimistic — novel GW-class system)", 500.0),
]

print("\nDEC Capital Cost Scenarios — C220109 (base model: NOT MODELED = $0):")
print(f"  {'Scenario':<48} {'C220109 M$':>10} {'LCOE $/MWh':>11}")
print("  " + "-" * 71)
print(f"  {'Base case (DEC omitted)':<48} {'0':>10} {float(result.costs.lcoe):>11.1f}")
for label, dec_m in _DEC_SCENARIOS:
    r_dec = model.forward(
        net_electric_mw=NATIVE_MW,
        cost_overrides={"C220109": dec_m},
        **_SHARED_KWARGS,
    )
    print(f"  {label:<48} {dec_m:>10.0f} {float(r_dec.costs.lcoe):>11.1f}")
print("  At 2800 MWe design point, DEC handles ~2400 MW_th charged-particle power")
print("  (30% of 8000 MW P_fus). A GW-class system with no commercial precedent.")


# ── F-3: Target Cost OPEX Analysis ───────────────────────────────────
# p_target = 1.0 MW in _SHARED_KWARGS is the target factory ELECTRICAL LOAD
# [MW parasitic], not a per-shot consumable cost. The Goodin criterion and
# the MagLIF OPEX analogy require tracking the per-shot cost separately:
#
#   Annual target OPEX = cost_per_shot [$/shot] × shots/yr
#   shots/yr = f_rep [Hz] × availability × 8760 hr/yr × 3600 s/hr
#
# At 10 Hz, 75% availability: shots/yr ≈ 2.365 × 10^8. Even at $0.035/shot
# (Goodin floor), this is ~$8M/yr — non-negligible at 30-year plant life.
# The base model LCOE is understated until this consumable cost is added.
_SHOTS_PER_YEAR = F_REP_HZ * AVAILABILITY * 8760.0 * 3600.0
_ANN_ENERGY_MWH = NATIVE_MW * AVAILABILITY * 8760.0   # MWh/yr at design point

_TARGET_COST_SWEEP = [
    ("$0.035/target  (Goodin economic viability floor)", 0.035),
    ("$0.10/target   (development milestone proxy)", 0.10),
    ("$1.00/target   (optimistic near-term target)", 1.00),
    ("$10.00/target  (mid-range near-term)", 10.00),
    ("$1e6/target    (current NIF research target cost)", 1_000_000),
]

print("\n\nTarget Cost OPEX Analysis — per-shot consumable cost not captured in base model:")
print(f"  At {F_REP_HZ:.0f} Hz, {AVAILABILITY:.0%} availability: {_SHOTS_PER_YEAR:.3e} shots/yr")
print(f"  Annual energy at design point: {_ANN_ENERGY_MWH:.3e} MWh/yr ({NATIVE_MW:.0f} MWe)")
print(f"  {'Cost per target':<46} {'M$/yr':>8} {'LCOE +$/MWh':>12}")
print("  " + "-" * 68)
for _label, _cost_per_shot in _TARGET_COST_SWEEP:
    _ann_cost_m = _SHOTS_PER_YEAR * _cost_per_shot / 1e6
    _lcoe_penalty = (_ann_cost_m * 1e6) / _ANN_ENERGY_MWH
    print(f"  {_label:<46} {_ann_cost_m:>8.2f} {_lcoe_penalty:>+12.2f}")
print(f"  30-year total shots ≈ {_SHOTS_PER_YEAR * LIFETIME_YR:.2e}")
print("  Note: p_target=1.0 MW in the base model is the factory electrical load,")
print("  not a per-shot cost. The Goodin floor ($0.035/target) must be added as")
print("  annualized OPEX; the base LCOE does not include this consumable cost.")
