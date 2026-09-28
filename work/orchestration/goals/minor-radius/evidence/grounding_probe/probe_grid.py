"""Probe B / C: two-dimensional access map (T_i0 x n_e0) through the raw sustainment channel."""
import csv, json, os, sys, time, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
GEOMS = {"B_baseline": {"R": 12.7, "a": 1.3, "I": 15.4e6, "n_e0": 5.06e20, "T": 14.63, "wallplug": 100.0, "eta": 0.5, "tau": 8.0},
         "C_c2823": {"R": 15.7, "a": 2.2, "I": 13.0e6, "n_e0": 5.06e20, "T": 13.0, "wallplug": 100.0, "eta": 0.5, "tau": 8.0}}
T_VALUES = [round(2.0 + 0.5 * k, 2) for k in range(29)]
F_VALUES = [round(0.10 + 0.05 * k, 2) for k in range(21)]
RAW_KEYS = ("p_aux_required", "p_fus", "W_th", "p_alpha_heat", "p_rad", "tau_E", "p_net", "n_He0", "p_brems", "p_sync", "p_line", "n_e_volav")
def job(args):
    tag, f, T = args
    coords = GEOMS[tag]
    r, err = raw(coords, ne=f * coords["n_e0"], T=T)
    rec = {"geom": tag, "n_factor": f, "n_e0": f * coords["n_e0"], "T": T, "err": err}
    if r is not None:
        for k in RAW_KEYS:
            v = r.get(k)
            rec[k] = None if v is None else (float(v.real) if isinstance(v, complex) else float(v))
    return rec
if __name__ == "__main__":
    tag = sys.argv[1]
    coords = GEOMS[tag]
    Ts = T_VALUES + ([coords["T"]] if coords["T"] not in T_VALUES else [])
    jobs = [(tag, f, T) for f in F_VALUES for T in Ts]
    path = os.path.join(SCR, f"access_grid_{tag}.csv")
    t0 = time.time(); n = 0
    with open(path, "w", newline="") as h, mp.Pool(11) as pool:
        w = csv.DictWriter(h, fieldnames=["geom", "n_factor", "n_e0", "T", "err"] + list(RAW_KEYS)); w.writeheader()
        for rec in pool.imap_unordered(job, jobs, chunksize=4):
            w.writerow(rec); h.flush(); n += 1
            if n % 50 == 0 or rec["err"]:
                print(f"[{n}/{len(jobs)}] {time.time()-t0:.0f}s last: f={rec['n_factor']} T={rec['T']} paux={rec.get('p_aux_required')} err={rec['err']}", file=sys.stderr, flush=True)
    print(f"done {n} points in {time.time()-t0:.0f}s -> {path}", file=sys.stderr, flush=True)
