import csv, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
rows = {r['case_id'].split(':')[-1]: r for r in csv.DictReader(open(os.path.join(ROOT, 'exploration/stellarator_e2e/studies/20260907-burn-control/results/points.csv')))}
base_rows = [r for r in rows.values() if r['is_baseline_point'] == 'True']
print("baseline rows:", [(r['case_id'], r['R'], r['a'], r['I_coil_A'], r['n_e0'], r['T_i0_keV'], r['p_wallplug_heat_MW'], r['eta_source_heat'], r['tau_ratio_ash']) for r in base_rows])
out = {}
for tag in ('c2823', 'c3694'):
    row = rows[tag]
    coords = {"R": float(row["R"]), "a": float(row["a"]), "I": float(row["I_coil_A"]), "n_e0": float(row["n_e0"]),
              "T": float(row["T_i0_keV"]), "wallplug": float(row["p_wallplug_heat_MW"]),
              "eta": float(row["eta_source_heat"]), "tau": float(row["tau_ratio_ash"])}
    t0 = time.time(); ch, v, err = ev(coords); dt = time.time() - t0
    if tag == 'c2823':
        pt = point(coords["R"], coords["a"], coords["I"], coords["n_e0"], coords["T"], coords["wallplug"], coords["eta"], coords["tau"])
        allch = oe().evaluate(pt)
        with open(os.path.join(SCR, 'keys.txt'), 'w') as h:
            h.write("\n".join(sorted(allch)) + "\n")
        r, _ = raw(coords)
        with open(os.path.join(SCR, 'raw_keys.txt'), 'w') as h:
            h.write("\n".join(f"{k}\t{type(r[k]).__name__}" for k in sorted(r)) + "\n")
        print("n evaluate keys", len(allch), "n raw keys", len(r))
        print("extra map", extra_map(allch))
    cmp = {}
    for mine, csvcol in (("lcoe", "lcoe"), ("p_aux_required", "p_aux_required_MW_oracle"), ("wall_load_peak", "wall_load_peak"),
                         ("beta", "beta"), ("B_peak", "B_peak"), ("plasma_volume", "plasma_volume"), ("vol_cold", "vol_cold"),
                         ("p_cryo", "p_cryo"), ("magnet_capital", "magnet_capital"), ("magnet_capital_1cfe_form", "magnet_capital_1cfe_form"),
                         ("heating_capital", "heating_capital"), ("cas72", "cas72"), ("total_capital", "total_capital")):
        if mine in ch:
            rec = float(row[csvcol]); got = ch[mine]
            cmp[mine] = {"oracle": got, "csv": rec, "rel_dev": abs(got - rec) / max(1e-300, abs(rec))}
    out[tag] = {"coords": coords, "elapsed_s": dt, "compare": cmp, "verdicts": v, "err": err,
                "max_rel_dev": max(c["rel_dev"] for c in cmp.values())}
    print(tag, f"{dt:.2f}s", "max_rel_dev", out[tag]["max_rel_dev"])
    for k, c in cmp.items(): print("  ", k, c)
    print("  verdicts violated:", v["violated"] if v else err)
json.dump(out, open(os.path.join(SCR, 'step0.json'), 'w'), indent=1, default=str)
