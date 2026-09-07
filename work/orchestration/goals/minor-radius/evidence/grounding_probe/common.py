"""Probe-A helpers, copied from the burn-control grounding probe (probe.py) rather than imported."""
import os, sys, time
ROOT = '/home/reid/1cfe/fusion-tea'
SCR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, 'exploration/stellarator_e2e/studies'))
P = 'stellarator_09__stellaris__'
HELD = {"availability": 0.85, "discount_rate": 0.07, "j_wp": 118.8271604938272,
        "eta_couple_heat": 1.0, "p_delivered_direct_heat": 0.0, "p_coupled_direct_heat": 0.0}
LIM = {"beta_limit": 0.05, "B_max": 24.9, "recirc_threshold": 0.5, "wall_load_limit": 4.05,
       "sigma_allow": 800e6, "eps_cond_allow": 0.004, "tbr": 1.074, "tbr_floor": 1.05}
NAMED = {"p_aux_required": "sustain__p_aux_required", "heat_coupled": "heat__p_coupled",
         "lcoe": "lcoe_calc__lcoe", "p_fus": "fusion__p_fus", "wall_load_peak": "wall_peak_calc__wall_load_peak",
         "wall_load_avg": "wall_load_calc__wall_load", "beta": "beta_calc__beta", "B_peak": "peak_field_calc__B_peak",
         "p_net": "pb__p_net", "rec_frac": "pb__rec_frac", "q_eng": "pb__q_eng", "sigma_wp": "wp_stress__sigma_wp",
         "eps_cond": "cond_strain__eps_cond", "W_th": "sustain__W_th", "tau_E": "sustain__tau_E",
         "p_rad": "sustain__p_rad", "p_alpha_heat": "sustain__p_alpha_heat", "n_He0": "sustain__n_He0",
         "p_th": "pb__p_th", "total_capital": "total_capital__total_capital"}
# extra store channels asked for by the probe, resolved from the study's own channel map
# (exploration/stellarator_e2e/studies/20260907-burn-control/study.py CHANNELS) and oracle_entry.ORACLE_OUTPUT_TO_CHANNEL.
EXTRA = {"plasma_volume": "geom__V", "p_cryo": "cryo_elec__p_elec",
         "magnet_capital": "magnet_capital_rollup__capital_cost",      # the rollup that enters total_capital
         "magnet_capital_1cfe_form": "magnet_cost__capital_cost",      # the 1cfe-form comparison channel
         "heating_capital": "heating_cost__cost", "cas72": "cas72_calc__cost",
         "overnight_capital": "overnight_capital__overnight_capital", "B_axis": "field_calc__B_axis",
         "cryo_cost": "aux_cooling__cryo_cost"}
# vol_cold (store: wp_volume__vol_cold_total) is NOT an oracle output; recomputed below from the oracle's own
# expression (verify_stellaris.py:412-420): f_wp_vol * n_coils * wp_side^2 * k_coil * R0 + vol_cold_cryo.

_oe = None
def oe():
    global _oe
    if _oe is None:
        import oracle_entry
        _oe = oracle_entry
    return _oe

def point(R, a, I, ne, T, wallplug, eta, tau):
    return {f"{P}R": R, f"{P}magnet__R0": R, f"{P}a": a, f"{P}availability": HELD["availability"],
            f"{P}discount_rate": HELD["discount_rate"], f"{P}magnet__j_wp": HELD["j_wp"], f"{P}T_i0": T,
            f"{P}magnet__I_coil": I, f"{P}n_e0": ne, f"{P}p_wallplug_heat": wallplug,
            f"{P}eta_source_heat": eta, f"{P}eta_couple_heat": HELD["eta_couple_heat"],
            f"{P}p_delivered_direct_heat": HELD["p_delivered_direct_heat"],
            f"{P}p_coupled_direct_heat": HELD["p_coupled_direct_heat"], f"{P}tau_ratio_ash": tau}

def verdicts(c):
    v = {"beta_ok": c["beta"] <= LIM["beta_limit"], "peak_field_ok": c["B_peak"] <= LIM["B_max"],
         "net_positive": c["p_net"] > 0.0, "recirc_ok": c["rec_frac"] <= LIM["recirc_threshold"],
         "wall_load_ok": c["wall_load_peak"] <= LIM["wall_load_limit"],
         "wp_stress_ok": c["sigma_wp"] <= LIM["sigma_allow"], "cond_strain_ok": c["eps_cond"] <= LIM["eps_cond_allow"],
         "sustainment_ok": c["p_aux_required"] <= c["heat_coupled"],
         "tbr_ok": LIM["tbr"] >= LIM["tbr_floor"],
         "burn_hold_ok": c["p_aux_required"] >= 0.0}   # tenth verdict (SV-059 form)
    v["all_satisfied"] = all(v.values())
    v["violated"] = [k for k, ok in v.items() if k not in ("all_satisfied",) and not ok]
    return v

def vol_cold(R, I):
    import verify_stellaris as vs
    p = vs.IN
    wp_side = (I / HELD["j_wp"]) ** 0.5 / 1000.0
    return p["magnet_f_wp_vol"] * p["magnet_n_coils"] * wp_side * wp_side * p["magnet_k_coil"] * R + p["vol_cold_cryo"]

def ev(coords, ne=None, T=None, a=None):
    c = dict(coords)
    if ne is not None: c["n_e0"] = ne
    if T is not None: c["T"] = T
    if a is not None: c["a"] = a
    pt = point(c["R"], c["a"], c["I"], c["n_e0"], c["T"], c["wallplug"], c["eta"], c["tau"])
    try:
        ch = oe().evaluate(pt)
    except Exception as exc:
        return None, None, f"{type(exc).__name__}: {exc}"
    out = {k: ch[P + v] for k, v in NAMED.items()}
    for w, key in EXTRA.items():
        out[w] = ch[P + key]
    out["vol_cold"] = vol_cold(c["R"], c["I"])
    out["n_e0"] = c["n_e0"]; out["T"] = c["T"]; out["a"] = c["a"]
    return out, verdicts(out), None

def raw(coords, ne=None, T=None, a=None):
    """Raw oracle compute (no channel mapping); real sustainment values even where p_net <= 0."""
    c = dict(coords)
    if ne is not None: c["n_e0"] = ne
    if T is not None: c["T"] = T
    if a is not None: c["a"] = a
    pt = point(c["R"], c["a"], c["I"], c["n_e0"], c["T"], c["wallplug"], c["eta"], c["tau"])
    o = oe()
    try:
        r = o._compute(o._oracle_overrides(pt))
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"
    return r, None

def paux(coords, **kw):
    ch, _, err = ev(coords, **kw)
    return (None if ch is None else ch["p_aux_required"]), err

def paux_raw(coords, **kw):
    r, err = raw(coords, **kw)
    if r is None: return None, err
    return float(r["p_aux_required"]), None
