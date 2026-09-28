import json, os, sys, multiprocessing as mp
SCR = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, SCR)
import probe as pb
sel = json.load(open(os.path.join(SCR, "selected_points.json")))
row = sel["P0"]
coords = {"R": float(row["R"]), "a": float(row["a"]), "I": float(row["I_coil_A"]), "n_e0": float(row["n_e0"]),
          "T": float(row["T_i0_keV"]), "wallplug": float(row["p_wallplug_heat_MW"]), "eta": float(row["eta_source_heat"]), "tau": float(row["tau_ratio_ash"])}
def ramp(frac):
    nn = frac * coords["n_e0"]; scan = []; T = 5.0
    while T < coords["T"] - 1e-9:
        v, e = pb.paux(coords, ne=nn, T=T); scan.append((T, v, (e or "")[:40])); T += 0.5
    v, e = pb.paux(coords, ne=nn, T=coords["T"]); scan.append((coords["T"], v, (e or "")[:40]))
    ok = [(T, v) for T, v, e in scan if v is not None]
    ch, vv, e = pb.ev(coords, ne=nn)
    return frac, {"scan": scan, "max": max(ok, key=lambda x: x[1]) if ok else None, "lowest_evaluable_T": min(ok)[0] if ok else None,
                  "at_T_op": {"p_aux_required": ch["p_aux_required"], "lcoe": ch["lcoe"], "p_fus": ch["p_fus"], "wall_load_peak": ch["wall_load_peak"], "p_net": ch["p_net"], "rec_frac": ch["rec_frac"], "violated": vv["violated"]} if ch else e}
def stable_root(_):
    target = 49.07960078792678
    f = lambda T: (lambda v: (None if v[0] is None else v[0] - target, v[1]))(pb.paux(coords, T=T))
    fa, _ = f(21.0); fb, _ = f(22.0)
    x, fx, it, e = pb.bisect(f, 21.0, 22.0, fa, fb)
    ch, vv, e2 = pb.ev(coords, T=x)
    fp, _ = pb.paux(coords, T=x + 0.2); fm, _ = pb.paux(coords, T=x - 0.2)
    return "stable_root", {"T": x, "p_aux_required": ch["p_aux_required"], "dpaux_dT": (fp - fm) / 0.4, "channels": ch, "verdicts": vv}
if __name__ == "__main__":
    out = {}
    with mp.Pool(7) as pool:
        jobs = [pool.apply_async(stable_root, (0,))] + [pool.apply_async(ramp, (f,)) for f in (0.3, 0.4, 0.5, 0.6, 0.7, 0.85)]
        for j in jobs:
            k, v = j.get(); out[str(k)] = v
            json.dump(out, open(os.path.join(SCR, "p0_extra.json"), "w"), indent=1, default=str)
    sr = out["stable_root"]; c = sr["channels"]
    print(f"P0 fixed-heating stable root: T {sr['T']:.3f} paux {sr['p_aux_required']:.2f} d/dT {sr['dpaux_dT']:.2f} lcoe {c['lcoe']:.1f} pfus {c['p_fus']:.0f} wall {c['wall_load_peak']:.3f} beta {c['beta']:.4f} pnet {c['p_net']:.0f} rec {c['rec_frac']:.3f} W {c['W_th']:.1f} viol {sr['verdicts']['violated']}")
    for f in ("0.3", "0.4", "0.5", "0.6", "0.7", "0.85"):
        r = out[f]; print(f"n={f}x: ramp max {r['max']} lowest evaluable T {r['lowest_evaluable_T']} ; at T_op {r['at_T_op']}")
        print("   ", [(T, None if v is None else round(v, 1)) for T, v, e in r["scan"]])
