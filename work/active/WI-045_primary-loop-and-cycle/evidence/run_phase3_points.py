"""WI-045 phase 3: the held-mode identity (first), then P1/P3/P4 and the synthetic cases."""
import json, math, shutil, sys
from pathlib import Path

REPO = Path("/home/reid/1cfe/fusion-tea")
sys.path.insert(0, str(REPO / "exploration/stellarator_e2e/studies"))
sys.path.insert(0, str(REPO / "exploration/stellarator_e2e"))
import study_route as route  # noqa: E402
import oracle_entry as oe  # noqa: E402

P = route.P
WI = REPO / "work/active/WI-045_primary-loop-and-cycle"
ENTER = json.load(open(REPO / "exploration/stellarator_e2e/studies/20260907-minor-radius/results/baseline_result.json"))
NEW_CH = [
    f"{P}source_heat__q_source",
    *[f"{P}primary_loop__{o}" for o in ("mdot", "T_out", "mdot_loop", "dp_loop", "p_loop_margin", "r_comp",
                                          "T_comp_in", "w_fluid", "p_elec", "q_ihx", "capacity_margin",
                                          "p_pump_total", "q_recovered_total")],
    *[f"{P}cycle__{o}" for o in ("T2_C", "eta_fit", "eta_th", "margin_low", "margin_high", "domain_product")],
]
REQ = dict(route.CHANNELS)
for k in NEW_CH:
    REQ[k.split("__", 2)[2]] = k
base = route._baseline_point(route.MANIFEST_PATH)
print("baseline point keys:", sorted(base.keys()))
HELD = {f"{P}loop_live": 0.0, f"{P}cycle_live": 0.0, f"{P}p_pump_direct": 195.0,
        f"{P}eta_p_direct": 0.5, f"{P}eta_th_direct": 0.333}


def run(study_id, proposals, out_dir):
    work = Path("/tmp/claude-1000/-home-reid-1cfe-fusion-tea/62c1de19-8042-4dea-b909-a71da826820c/scratchpad/work") / study_id
    if work.exists():
        shutil.rmtree(work)
    cases, db = route.run_points(study_id, proposals, work, required_channels=REQ)
    out = []
    for c in cases:
        outputs = {k: (float(v) if isinstance(v, (int, float)) else v) for k, v in dict(c.outputs).items()}
        verdicts = getattr(c, "verdicts", None)
        out.append({"case_id": getattr(c, "case_id", None), "state": c.state, "inputs": dict(c.inputs),
                    "outputs": outputs, "verdicts": verdicts})
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "result.json").write_text(json.dumps(out, indent=1, default=str))
    return out


# ---------------------------------------------------------------- held-mode identity
compat = run("wi045-compat", [dict(base, **HELD)], WI / "evidence/compat_mode")
c0 = compat[0]
print("compat state", c0["state"], "n outputs", len(c0["outputs"]))
diff = {}
for k, v in ENTER["channels"].items():
    got = c0["outputs"].get(k)
    if got is None or got != v:
        diff[k] = {"pin": v, "compat": got}
print("channels of the entering pin:", len(ENTER["channels"]), "moved:", len(diff))
verd_pin = {v["source_local_identity"]: v["status"] for v in ENTER["verdicts"]}
print("old verdicts", verd_pin)
(WI / "evidence/compat_mode/diff_vs_pin.json").write_text(json.dumps(
    {"channels_compared": len(ENTER["channels"]), "channels_moved": len(diff), "diff": diff,
     "lcoe_compat": c0["outputs"].get(f"{P}lcoe_calc__lcoe"),
     "new_channels": {k: c0["outputs"].get(k) for k in NEW_CH},
     "case_verdicts": c0["verdicts"]}, indent=1, default=str))
assert not diff, f"HELD MODE MOVED {len(diff)} CHANNELS -- STOP (owner gate)"
print("HELD-MODE IDENTITY: every channel bit-identical; lcoe", c0["outputs"][f"{P}lcoe_calc__lcoe"])

# ---------------------------------------------------------------- off-design points
def pt(**over):
    d = dict(base)
    d.update(over)
    return d

P1 = pt(**{f"{P}a": 1.4})
P3 = pt(**{f"{P}R": 15.7, f"{P}magnet__R0": 15.7, f"{P}a": 2.2, f"{P}magnet__I_coil": 13.0e6,
           f"{P}T_i0": 13.0, f"{P}n_e0": 5.06e20})
P4 = dict(P3, **{f"{P}n_loops": 27.0})
S_T350 = pt(**{f"{P}loop_T_in": 623.15 - 200.0})
S_N7 = pt(**{f"{P}n_loops": 7.0})
print("I_coil baseline:", base.get(f"{P}magnet__I_coil"), "n_e0:", base.get(f"{P}n_e0"), "T_i0:", base.get(f"{P}T_i0"))
res = run("wi045-offdesign", [P1, P3, P4, S_T350, S_N7], WI / "evidence/offdesign_points")
names = ["P1_design_a1.4", "P3_c2823_14loops", "P4_c2823_resized", "synthetic_T_hot_350C", "synthetic_n_loops_7"]
pred = json.load(open(WI / "prototype/proto_results.json"))
summary = {}
for name, r in zip(names, res):
    o = r["outputs"]
    row = {"state": r["state"],
           "q_source": o.get(f"{P}source_heat__q_source"), "mdot_loop": o.get(f"{P}primary_loop__mdot_loop"),
           "dp_loop": o.get(f"{P}primary_loop__dp_loop"), "p_elec": o.get(f"{P}primary_loop__p_elec"),
           "capacity_margin": o.get(f"{P}primary_loop__capacity_margin"),
           "eta_fit": o.get(f"{P}cycle__eta_fit"), "eta_th": o.get(f"{P}cycle__eta_th"),
           "domain_product": o.get(f"{P}cycle__domain_product"),
           "p_th": o.get(f"{P}pb__p_th"), "p_net": o.get(f"{P}pb__p_net"), "rec_frac": o.get(f"{P}pb__rec_frac"),
           "lcoe": o.get(f"{P}lcoe_calc__lcoe"), "verdicts": r["verdicts"]}
    # oracle seam at the same point
    inputs = r["inputs"]
    ev = oe.evaluate(inputs)
    row["oracle_reldev"] = {k.split("__", 2)[2]: (abs(ev[k] - o[k]) / (abs(o[k]) or 1.0)) for k in NEW_CH + [f"{P}lcoe_calc__lcoe"] if k in ev and k in o}
    row["oracle_reldev_max"] = max(row["oracle_reldev"].values())
    summary[name] = row
    print(name, {k: row[k] for k in ("state", "p_elec", "eta_th", "p_net", "rec_frac", "lcoe", "oracle_reldev_max")})
    print("   verdicts:", row["verdicts"])
# compare with predictions
cmp = {}
for name, key in (("P1_design_a1.4", "P1_design_a1.4"), ("P3_c2823_14loops", "P3_c2823_14loops"), ("P4_c2823_resized", "P4_c2823_resized")):
    pr = pred[key]
    got = summary[name]
    checks = {
        "p_elec": (got["p_elec"], pr["loop"]["p_elec"]),
        "mdot_loop": (got["mdot_loop"], pr["loop"]["mdot_loop"]),
        "dp_loop": (got["dp_loop"], pr["loop"]["dp_loop"]),
        "eta_th": (got["eta_th"], pr["cycle"]["eta_th"]),
        "p_net": (got["p_net"], pr["live"]["p_net"]),
        "rec_frac": (got["rec_frac"], pr["live"]["rec_frac"]),
        "lcoe": (got["lcoe"], pr["live"]["lcoe"]),
    }
    cmp[name] = {k: {"executed": a, "predicted": b, "reldev": abs(a - b) / (abs(b) or 1.0)} for k, (a, b) in checks.items()}
    print(name, "max reldev vs prediction", max(x["reldev"] for x in cmp[name].values()))
syn = {"synthetic_T_hot_350C": {"eta_fit": (summary["synthetic_T_hot_350C"]["eta_fit"], pred["synthetic"]["T_hot_350C"]["eta_fit"]),
                                "domain_product": (summary["synthetic_T_hot_350C"]["domain_product"], pred["synthetic"]["T_hot_350C"]["domain_product"])},
       "synthetic_n_loops_7": {"p_elec": (summary["synthetic_n_loops_7"]["p_elec"], pred["synthetic"]["n_loops_7"]["p_elec"]),
                               "capacity_margin": (summary["synthetic_n_loops_7"]["capacity_margin"], pred["synthetic"]["n_loops_7"]["capacity_margin"])}}
print("synthetic", syn)
(WI / "evidence/offdesign_points/summary.json").write_text(json.dumps({"summary": summary, "vs_predictions": cmp, "synthetic": syn}, indent=1, default=str))
(WI / "evidence/synthetic_cases").mkdir(exist_ok=True)
(WI / "evidence/synthetic_cases/results.json").write_text(json.dumps({k: summary[k] for k in names[3:]}, indent=1, default=str))
print("done")
