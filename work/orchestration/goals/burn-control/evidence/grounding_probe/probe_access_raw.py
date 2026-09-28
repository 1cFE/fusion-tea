"""Access ramps re-done through the oracle's raw compute (oracle_entry._compute), which returns a
real p_aux_required even where p_net <= 0 makes the cost channels complex. Oracle-side diagnostic."""
import json, os, sys, multiprocessing as mp
SCR = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, SCR)
import probe as pb
def raw(coords, ne, T):
    import oracle_entry as oe
    pt = pb.point(coords["R"], coords["a"], coords["I"], ne, T, coords["wallplug"], coords["eta"], coords["tau"])
    try:
        r = oe._compute(oe._oracle_overrides(pt))
        pn = r["p_net"]; pn = pn.real if isinstance(pn, complex) else pn
        return {"T": T, "p_aux_required": float(r["p_aux_required"]), "p_net": float(pn), "p_fus": float(r["p_fus"]), "tau_E": float(r["tau_E"]), "err": None}
    except Exception as e:
        return {"T": T, "p_aux_required": None, "err": f"{type(e).__name__}: {e}"}
def job(args):
    tag, label, coords, ne, T_op = args
    scan = []; T = 3.0
    while T < T_op - 1e-9:
        scan.append(raw(coords, ne, T)); T += 0.5
    scan.append(raw(coords, ne, T_op))
    ok = [s for s in scan if s["p_aux_required"] is not None]
    m = max(ok, key=lambda s: s["p_aux_required"]) if ok else None
    first_pos_pnet = next((s["T"] for s in ok if s["p_net"] > 0), None)
    return tag, label, {"n_e0": ne, "T_op": T_op, "scan": scan, "max_p_aux_required_MW": m and m["p_aux_required"], "T_at_max_keV": m and m["T"],
                        "n_raised": len(scan) - len(ok), "lowest_T_with_p_net_positive": first_pos_pnet,
                        "monotone_decreasing_in_T": all(ok[i]["p_aux_required"] >= ok[i+1]["p_aux_required"] for i in range(len(ok)-1))}
if __name__ == "__main__":
    res = json.load(open(os.path.join(SCR, "results.json")))
    jobs = []
    for tag, r in res.items():
        c = r["coords"]; n0 = c["n_e0"]; T0 = c["T"]
        jobs.append((tag, "at_point_density", c, n0, T0))
        ns = r["density_control"].get("n_star")
        if ns: jobs.append((tag, "at_n_star", c, ns, T0))
    c0 = res["P0"]["coords"]
    for f in (0.3, 0.4, 0.5, 0.6, 0.7, 0.85):
        jobs.append(("P0", f"baseline_ramp_at_{f}x_n", c0, f * c0["n_e0"], c0["T"]))
    out = {}
    with mp.Pool(min(12, len(jobs))) as pool:
        for tag, label, rec in pool.imap_unordered(job, jobs):
            out.setdefault(tag, {})[label] = rec
            json.dump(out, open(os.path.join(SCR, "access_raw.json"), "w"), indent=1)
    for tag in sorted(out):
        for label, rec in out[tag].items():
            inst = res[tag]["at_point"]["channels"]["heat_coupled"]
            print(f"{tag} {label}: max {rec['max_p_aux_required_MW']:.1f} MW at {rec['T_at_max_keV']} keV ; installed coupled {inst} ; p_net>0 from T {rec['lowest_T_with_p_net_positive']} ; raised {rec['n_raised']} ; monotone {rec['monotone_decreasing_in_T']}")
            print("   ", [(s["T"], None if s["p_aux_required"] is None else round(s["p_aux_required"], 1)) for s in rec["scan"]])
