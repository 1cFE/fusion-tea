"""Oracle-side diagnostic probe: density control, thermal stability sign, fixed-density
attractor, access heating, for nine selected points. Nothing here is package evidence."""
import csv, json, math, os, sys, time, traceback
import multiprocessing as mp

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
         "tbr_ok": LIM["tbr"] >= LIM["tbr_floor"]}   # both operands are held inputs; constant
    v["all_satisfied"] = all(v.values())
    v["violated"] = [k for k, ok in v.items() if k not in ("all_satisfied",) and not ok]
    return v

def ev(coords, ne=None, T=None):
    """Evaluate at coords with optional n_e0/T override. Returns (channels, verdicts, err)."""
    c = dict(coords)
    if ne is not None: c["n_e0"] = ne
    if T is not None: c["T"] = T
    pt = point(c["R"], c["a"], c["I"], c["n_e0"], c["T"], c["wallplug"], c["eta"], c["tau"])
    try:
        ch = oe().evaluate(pt)
    except Exception as exc:
        return None, None, f"{type(exc).__name__}: {exc}"
    out = {k: ch[P + v] for k, v in NAMED.items()}
    out["n_e0"] = c["n_e0"]; out["T"] = c["T"]
    return out, verdicts(out), None

def paux(coords, ne=None, T=None):
    ch, _, err = ev(coords, ne, T)
    return (None if ch is None else ch["p_aux_required"]), err

def bisect(fn, lo, hi, flo, fhi, tol_rel=1e-4, maxit=40):
    """Root of fn between lo and hi given signs flo, fhi (opposite). Returns x, f(x), iterations."""
    it = 0
    while it < maxit and (hi - lo) > tol_rel * abs(hi):
        mid = 0.5 * (lo + hi); fm, err = fn(mid); it += 1
        if fm is None:
            return None, None, it, f"raise at {mid}: {err}"
        if (fm > 0) == (fhi > 0):
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    x = 0.5 * (lo + hi); fx, err = fn(x)
    return x, fx, it, None

def save(tag, res):
    with open(os.path.join(SCR, f"point_{tag}.json"), "w") as h:
        json.dump(res, h, indent=1, default=str)

def ratio(a, b):
    return {k: (a[k] / b[k] if isinstance(a.get(k), float) and isinstance(b.get(k), float) and b[k] != 0 else None)
            for k in ("lcoe", "p_fus", "W_th", "wall_load_peak", "beta", "p_net", "tau_E", "n_e0")}

def probe(args):
    tag, row = args
    t0 = time.time()
    coords = {"R": float(row["R"]), "a": float(row["a"]), "I": float(row["I_coil_A"]), "n_e0": float(row["n_e0"]),
              "T": float(row["T_i0_keV"]), "wallplug": float(row["p_wallplug_heat_MW"]),
              "eta": float(row["eta_source_heat"]), "tau": float(row["tau_ratio_ash"])}
    res = {"tag": tag, "case_id": row["case_id"], "coords": coords, "recorded": row, "evals": 0}
    base, vb, err = ev(coords)
    res["at_point"] = {"channels": base, "verdicts": vb, "err": err}
    res["reproduces"] = None if base is None else {
        "p_aux_required": (base["p_aux_required"], float(row["p_aux_required_MW_oracle"])),
        "lcoe": (base["lcoe"], float(row["lcoe"])), "wall_load_peak": (base["wall_load_peak"], float(row["wall_load_peak"])),
        "max_rel_dev": max(abs(base["lcoe"] / float(row["lcoe"]) - 1), abs(base["wall_load_peak"] / float(row["wall_load_peak"]) - 1),
                           abs(base["p_aux_required"] - float(row["p_aux_required_MW_oracle"])) / max(1e-9, abs(float(row["p_aux_required_MW_oracle"]))))}
    save(tag, res)
    n0, T0 = coords["n_e0"], coords["T"]

    # (i) density control
    dc = {"skipped": False}
    if base is None or base["p_aux_required"] >= 0:
        dc["skipped"] = True; dc["reason"] = "p_aux_required already >= 0 at the point (driven); no n* <= n_e0 with p_aux_required = 0 sought"
    else:
        lo_f = 0.10; lo = lo_f * n0; flo, e = paux(coords, ne=lo); tried = [(lo_f, flo, e)]
        while flo is None and lo_f < 0.95:
            lo_f += 0.05; lo = lo_f * n0; flo, e = paux(coords, ne=lo); tried.append((lo_f, flo, e))
        dc["lower_bracket_search"] = tried
        if flo is None:
            dc["result"] = "no evaluable lower bracket"
        elif flo < 0:
            dc["result"] = f"p_aux_required still negative at {lo_f:.2f} x n_e0 ({flo:.2f} MW); no root in [{lo_f:.2f}, 1.0] x n_e0 -- ignited all the way down the evaluable range"
        else:
            # ensure monotone-ish: coarse scan to locate the LAST sign change below n0 (largest n* < n0)
            scan = []
            fr = [lo_f + (1 - lo_f) * k / 12 for k in range(13)]
            for f_ in fr:
                v, e = paux(coords, ne=f_ * n0); scan.append((f_, v, e))
            dc["coarse_scan"] = scan
            brk = None
            for k in range(len(scan) - 1, 0, -1):
                a_, b_ = scan[k - 1], scan[k]
                if a_[1] is not None and b_[1] is not None and a_[1] >= 0 and b_[1] < 0:
                    brk = (a_, b_); break
            if brk is None:
                dc["result"] = "no positive-to-negative crossing found in coarse scan"
            else:
                x, fx, it, e = bisect(lambda n: paux(coords, ne=n), brk[0][0] * n0, brk[1][0] * n0, brk[0][1], brk[1][1])
                if x is None:
                    dc["result"] = f"bisection failed: {e}"
                else:
                    ch, vv, e2 = ev(coords, ne=x)
                    dc["n_star"] = x; dc["n_star_over_n_e0"] = x / n0; dc["p_aux_required_at_n_star"] = fx
                    dc["bisect_iterations"] = it; dc["channels"] = ch; dc["verdicts"] = vv
                    dc["ratio_to_point"] = ratio(ch, base) if ch else None
                    dc["result"] = "ok"
    res["density_control"] = dc; save(tag, res)
    n_star = dc.get("n_star")

    # (ii) thermal stability sign
    ts = {}
    for label, nn in (("at_point", n0), ("at_n_star", n_star)):
        if nn is None:
            ts[label] = {"skipped": True}; continue
        fp, ep = paux(coords, ne=nn, T=T0 + 0.2); fm, em = paux(coords, ne=nn, T=T0 - 0.2)
        if fp is None or fm is None:
            ts[label] = {"err": f"+0.2: {ep}; -0.2: {em}"}
        else:
            d = (fp - fm) / 0.4
            ts[label] = {"n_e0": nn, "T": T0, "p_aux_T_plus": fp, "p_aux_T_minus": fm, "dpaux_dT_MW_per_keV": d,
                         "sign": "positive (stable: a temperature rise needs more heating)" if d > 0 else "negative (runaway: a temperature rise needs less heating)"}
    res["thermal_stability"] = ts; save(tag, res)

    # (iii) attractor at fixed density: scan T upward to 45 keV
    att = {}
    for label, nn in (("at_point_density", n0), ("at_n_star", n_star)):
        if nn is None:
            att[label] = {"skipped": True}; continue
        f_here, e = paux(coords, ne=nn, T=T0)
        scan = [(T0, f_here, e)]
        Tg = math.floor(T0) + 1.0
        while Tg <= 45.0:
            v, e = paux(coords, ne=nn, T=Tg); scan.append((Tg, v, e)); Tg += 1.0
        rec = {"scan": scan, "crossings": []}
        for k in range(1, len(scan)):
            a_, b_ = scan[k - 1], scan[k]
            if a_[1] is None or b_[1] is None: continue
            if a_[1] < 0 and b_[1] >= 0: rec["crossings"].append(("neg_to_pos", a_[0], b_[0]))
            if a_[1] >= 0 and b_[1] < 0: rec["crossings"].append(("pos_to_neg", a_[0], b_[0]))
        first = next((c for c in rec["crossings"] if c[0] == "neg_to_pos"), None)
        if first is None:
            rec["result"] = "no negative-to-positive crossing of p_aux_required between the point's T and 45 keV at this density"
        else:
            fa, _ = paux(coords, ne=nn, T=first[1]); fb, _ = paux(coords, ne=nn, T=first[2])
            x, fx, it, e = bisect(lambda T: paux(coords, ne=nn, T=T), first[1], first[2], fa, fb, tol_rel=1e-4)
            if x is None:
                rec["result"] = f"bisection failed: {e}"
            else:
                ch, vv, e2 = ev(coords, ne=nn, T=x)
                rec["T_root"] = x; rec["p_aux_at_root"] = fx; rec["channels"] = ch; rec["verdicts"] = vv
                rec["ratio_to_point"] = ratio(ch, base) if (ch and base) else None
                # stability at the root
                fp, _ = paux(coords, ne=nn, T=x + 0.2); fm, _ = paux(coords, ne=nn, T=x - 0.2)
                rec["dpaux_dT_at_root"] = None if (fp is None or fm is None) else (fp - fm) / 0.4
                rec["result"] = "ok"
        att[label] = rec
        res["attractor"] = att; save(tag, res)

    # (iv) access heating: T from 3 keV to T_op in 0.5 steps
    acc = {}
    for label, nn in (("at_point_density", n0), ("at_n_star", n_star)):
        if nn is None:
            acc[label] = {"skipped": True}; continue
        scan = []; T = 3.0
        while T < T0 - 1e-9:
            v, e = paux(coords, ne=nn, T=T); scan.append((T, v, e)); T += 0.5
        v, e = paux(coords, ne=nn, T=T0); scan.append((T0, v, e))
        ok = [(T, v) for T, v, e in scan if v is not None]
        rec = {"scan": scan, "n_evaluable": len(ok), "n_raised": len(scan) - len(ok),
               "raised_at": [(T, e) for T, v, e in scan if v is None]}
        if ok:
            mT, mv = max(ok, key=lambda x: x[1])
            rec["max_p_aux_required_MW"] = mv; rec["T_at_max_keV"] = mT
            rec["p_coupled_installed_MW"] = base["heat_coupled"] if base else None
            rec["max_minus_installed_MW"] = (mv - base["heat_coupled"]) if base else None
            rec["lowest_evaluable_T"] = min(ok)[0]
        acc[label] = rec
    res["access_heating"] = acc
    res["elapsed_s"] = time.time() - t0
    save(tag, res)
    return tag, res

if __name__ == "__main__":
    sel = json.load(open(os.path.join(SCR, "selected_points.json")))
    order = ["P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
    items = [(t, sel[t]) for t in order if t in sel]
    results = {}
    with mp.Pool(processes=len(items)) as pool:
        for tag, res in pool.imap_unordered(probe, items):
            results[tag] = res
            print(f"[done] {tag} {res['case_id']} {res['elapsed_s']:.0f}s", file=sys.stderr, flush=True)
            with open(os.path.join(SCR, "results.json"), "w") as h:
                json.dump({k: results[k] for k in order if k in results}, h, indent=1, default=str)
