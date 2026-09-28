"""Probe A: minor-radius transect, all channels, three columns."""
import csv, json, os, sys, time, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
A_VALUES = [round(1.3 + 0.1 * k, 1) for k in range(12)] + [2.5, 2.6, 2.8, 3.0]
COLS = {"c2823_100MW": {"R": 15.7, "a": 2.2, "I": 13.0e6, "n_e0": 5.06e20, "T": 13.0, "wallplug": 100.0, "eta": 0.5, "tau": 8.0},
        "baseline_100MW": {"R": 12.7, "a": 1.3, "I": 15.4e6, "n_e0": 5.06e20, "T": 14.63, "wallplug": 100.0, "eta": 0.5, "tau": 8.0},
        "c2823_220MW": {"R": 15.7, "a": 2.2, "I": 13.0e6, "n_e0": 5.06e20, "T": 13.0, "wallplug": 220.0, "eta": 0.5, "tau": 8.0}}
def job(args):
    col, a = args
    coords = COLS[col]; t0 = time.time()
    ch, v, err = ev(coords, a=a)
    rec = {"column": col, "a": a, "err": err, "channels": ch, "verdicts": v}
    # raw sustainment channel too (real even where evaluate raises on p_net <= 0)
    r, rerr = raw(coords, a=a)
    rec["raw_err"] = rerr
    if r is not None:
        rec["raw"] = {k: (float(r[k].real) if isinstance(r[k], complex) else float(r[k])) for k in
                      ("p_aux_required", "p_fus", "W_th", "tau_E", "p_rad", "p_alpha_heat", "p_net", "n_He0", "V", "beta", "wall_load_peak")}
    fp, ep = paux_raw(coords, a=a, T=coords["T"] + 0.2); fm, em = paux_raw(coords, a=a, T=coords["T"] - 0.2)
    if fp is not None and fm is not None:
        d = (fp - fm) / 0.4
        rec["dpaux_dT"] = d; rec["branch"] = "rising" if d > 0 else "falling"
    else:
        rec["dpaux_dT"] = None; rec["branch"] = f"n/a (+0.2: {ep}; -0.2: {em})"
    rec["elapsed_s"] = time.time() - t0
    return rec
if __name__ == "__main__":
    jobs = [(c, a) for c in COLS for a in A_VALUES]
    out = []
    t0 = time.time()
    with mp.Pool(11) as pool:
        for rec in pool.imap_unordered(job, jobs):
            out.append(rec)
            print(f"[{len(out)}/{len(jobs)}] {rec['column']} a={rec['a']} err={rec['err']} raw_err={rec['raw_err']} branch={rec['branch']}", file=sys.stderr, flush=True)
            json.dump(out, open(os.path.join(SCR, "probe_a_results.json"), "w"), indent=1, default=str)
    print(f"done in {time.time()-t0:.0f}s", file=sys.stderr)
    # flat csv
    keys = ["column", "a", "err", "raw_err", "dpaux_dT", "branch"]
    chk = list(NAMED) + list(EXTRA) + ["vol_cold"]
    with open(os.path.join(SCR, "probe_a_results.csv"), "w", newline="") as h:
        w = csv.writer(h); w.writerow(keys + chk + ["raw_p_aux_required", "raw_p_fus", "raw_p_net", "violated"])
        for rec in sorted(out, key=lambda r: (r["column"], r["a"])):
            ch = rec["channels"] or {}
            w.writerow([rec[k] for k in keys] + [ch.get(k) for k in chk] +
                       [rec.get("raw", {}).get("p_aux_required"), rec.get("raw", {}).get("p_fus"), rec.get("raw", {}).get("p_net"),
                        ";".join(rec["verdicts"]["violated"]) if rec["verdicts"] else ""])
