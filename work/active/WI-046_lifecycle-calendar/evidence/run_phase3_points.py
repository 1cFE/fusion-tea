"""WI-046 phase 3: the held-mode identity (first), the live baseline, arms A-D, the stepping
points E-F; oracle parity through the seam. Modelled on WI-045's run_phase3_points.py."""
import csv, json, shutil, sys
from pathlib import Path

REPO = Path("/home/reid/1cfe/fusion-tea")
sys.path.insert(0, str(REPO / "exploration/stellarator_e2e/studies"))
sys.path.insert(0, str(REPO / "exploration/stellarator_e2e"))
import study_route as route  # noqa: E402
import oracle_entry as oe  # noqa: E402
import verify_stellaris as vs  # noqa: E402

P = route.P
WI = REPO / "work/active/WI-046_lifecycle-calendar"
BEFORE = json.load(open(WI / "evidence/baseline_before/baseline_result.json"))
PRED = json.load(open(WI / "prototype/proto_results_at_wi045.json"))
CAL = ["availability", "coil_life_margin_fpy", "replacement_pv", "planned_downtime_yr",
       "terminal_downtime_yr", "unplanned_downtime_yr", "productive_fpy", "dated_energy_ratio",
       "cas72_annual", "n_replacements", "physical_life_fpy"]
CAL_CH = [f"{P}calendar__{o}" for o in CAL]
WI045_CH = [f"{P}source_heat__q_source",
            *[f"{P}primary_loop__{o}" for o in ("mdot", "T_out", "mdot_loop", "dp_loop", "p_loop_margin", "r_comp",
                                                  "T_comp_in", "w_fluid", "p_elec", "q_ihx", "capacity_margin",
                                                  "p_pump_total", "q_recovered_total")],
            *[f"{P}cycle__{o}" for o in ("T2_C", "eta_fit", "eta_th", "margin_low", "margin_high", "domain_product")]]
REQ = dict(route.CHANNELS)
for k in WI045_CH + CAL_CH:
    REQ[k.split("__", 2)[2]] = k
# the baseline point: the manifest's, with the retired availability key replaced by the live switch
m = json.load(open(route.MANIFEST_PATH))
base = {k: v for k, v in m["baseline"]["point"].items() if not k.endswith("__availability")}
base[f"{P}availability_direct"] = 0.0
print("baseline point:", base)


def run(study_id, proposals, out_dir):
    work = Path("/tmp/claude-1000/-home-reid-1cfe-fusion-tea/62c1de19-8042-4dea-b909-a71da826820c/scratchpad/work") / study_id
    if work.exists():
        shutil.rmtree(work)
    cases, db = route.run_points(study_id, proposals, work, required_channels=REQ)
    out = []
    for c in cases:
        outputs = {k: (float(v) if isinstance(v, (int, float)) else v) for k, v in dict(c.outputs).items()}
        out.append({"case_id": getattr(c, "case_id", None), "state": c.state, "inputs": dict(c.inputs),
                    "outputs": outputs, "verdicts": getattr(c, "verdicts", None)})
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "result.json").write_text(json.dumps(out, indent=1, default=str))
    return out


def verd(r):
    v = r["verdicts"]
    if isinstance(v, dict):
        return {k: (x.get("status") if isinstance(x, dict) else x) for k, x in v.items()}
    return v


def rel(a, b):
    return abs(a - b) / (abs(b) or 1.0)


# ---------------------------------------------------------------- held-mode identity
compat = run("wi046-compat", [dict(base, **{f"{P}availability_direct": 0.85})], WI / "evidence/compat_mode")
c0 = compat[0]
diff, gone = {}, []
for k, v in BEFORE["channels"].items():
    got = c0["outputs"].get(k)
    if got is None:
        gone.append(k)
    elif got != v:
        diff[k] = {"before": v, "compat": got}
new_vals = {k: c0["outputs"].get(k) for k in CAL_CH}
verd_before = {v["source_local_identity"]: v["status"] for v in BEFORE["verdicts"]}
(WI / "evidence/compat_mode/diff_vs_before.json").write_text(json.dumps(
    {"channels_compared": len(BEFORE["channels"]), "channels_moved": len(diff), "diff": diff,
     "channels_gone": gone, "new_channels": new_vals, "lcoe_compat": c0["outputs"].get(f"{P}lcoe_calc__lcoe"),
     "verdicts_before": verd_before, "case_verdicts": verd(c0)}, indent=1, default=str))
print("HELD MODE: channels compared", len(BEFORE["channels"]), "moved", len(diff), "gone", gone)
assert not diff, f"HELD MODE MOVED {len(diff)} CHANNELS -- STOP (owner gate)"
assert gone == [f"{P}cas72_calc__cost"], gone
print("  held readings:", {k.split('__')[-1]: v for k, v in new_vals.items()})

# ---------------------------------------------------------------- live baseline + A-D
arms = {
    "live_7mo_u0": (dict(base), "7mo_u0"),
    "A_5mo_u0": (dict(base, **{f"{P}outage_years": 5.0 / 12.0}), "5mo_u0"),
    "B_7mo_u005": (dict(base, **{f"{P}unplanned_fraction": 0.05}), "7mo_u005"),
    "C_7mo_u010": (dict(base, **{f"{P}unplanned_fraction": 0.10}), "7mo_u010"),
    "D_10mo_u0": (dict(base, **{f"{P}outage_years": 10.0 / 12.0}), "10mo_u0"),
}
res = run("wi046-live-arms", [a[0] for a in arms.values()], WI / "evidence/offdesign_points")
summary, worst_all = {}, 0.0
for (name, (prop, key)), r in zip(arms.items(), res):
    o = r["outputs"]
    pr = PRED["live"][key]
    lcoe_pred = PRED["lcoe_exact"][key]["lcoe"]
    checks = {c: rel(o[f"{P}calendar__{c}"], pr[c]) for c in CAL}
    checks["lcoe"] = rel(o[f"{P}lcoe_calc__lcoe"], lcoe_pred)
    ev = oe.evaluate(r["inputs"])
    parity = {c: rel(ev[f"{P}calendar__{c}"], o[f"{P}calendar__{c}"]) for c in CAL}
    parity["lcoe"] = rel(ev[f"{P}lcoe_calc__lcoe"], o[f"{P}lcoe_calc__lcoe"])
    worst = max(checks.values()); worst_all = max(worst_all, worst, max(parity.values()))
    summary[name] = {"state": r["state"], "availability": o[f"{P}calendar__availability"],
                     "n_replacements": o[f"{P}calendar__n_replacements"], "cas72": o[f"{P}calendar__cas72_annual"],
                     "lcoe": o[f"{P}lcoe_calc__lcoe"], "lcoe_predicted": lcoe_pred,
                     "vs_prediction_reldev": checks, "vs_prediction_worst": worst,
                     "oracle_parity_worst": max(parity.values()), "verdicts": verd(r)}
    print(name, r["state"], "A", o[f"{P}calendar__availability"], "n", o[f"{P}calendar__n_replacements"],
          "cas72", round(o[f"{P}calendar__cas72_annual"], 2), "lcoe", o[f"{P}lcoe_calc__lcoe"],
          "worst vs pred", f"{worst:.2e}", "parity", f"{max(parity.values()):.2e}")
live = res[0]
(WI / "evidence/baseline_live/result.json").write_text(json.dumps(live, indent=1, default=str))
live_verd = verd(live)
print("live verdicts:", live_verd)

# ---------------------------------------------------------------- E, F from the committed record
rows = {}
with open(REPO / "exploration/stellarator_e2e/studies/20260907-minor-radius/results/points.csv") as f:
    for row in csv.DictReader(f):
        if row["case_id"] in ("20260907-minor-radius:c3343", "20260907-minor-radius:c7752"):
            rows[row["case_id"].split(":")[1]] = row
def pt_from(row):
    d = dict(base)
    d.update({f"{P}R": float(row["R"]), f"{P}magnet__R0": float(row["R"]), f"{P}a": float(row["a"]),
              f"{P}magnet__I_coil": float(row["I_coil_A"]), f"{P}n_e0": float(row["n_e0"]),
              f"{P}T_i0": float(row["T_i0_keV"]), f"{P}p_wallplug_heat": float(row["p_wallplug_heat_MW"])})
    return d
# E (c3343: R 17.2, a 1.8, peak 9.04) at the instance's 14 loops fails in the package -- the
# loop's per-loop flow drives its pressure loss past the 8 MPa loop pressure (a complex root;
# WI-045's domain, recorded in stepping_points/c3343_at_14_loops_execution_failed.json). The
# calendar's count and availability do not depend on the loop count, so E runs with the loop
# re-sized to 60 loops (every chain in domain); F runs as committed.
E = pt_from(rows["c3343"]); E[f"{P}n_loops"] = 60.0
ef = run("wi046-stepping", [E, pt_from(rows["c7752"])], WI / "evidence/stepping_points")
picks = PRED["stepping_points"]["picks"]
ef_summary = {}
for cid, r in zip(("c3343", "c7752"), ef):
    o = r["outputs"]; pk = picks[f"20260907-minor-radius:{cid}"]
    ev = oe.evaluate(r["inputs"])
    parity = max(rel(ev[k], o[k]) for k in CAL_CH + [f"{P}lcoe_calc__lcoe", f"{P}wall_peak_calc__wall_load_peak"])
    wall_identity = rel(o[f"{P}wall_peak_calc__wall_load_peak"], float(rows[cid]["wall_load_peak"]))
    ef_summary[cid] = {"state": r["state"], "availability": o[f"{P}calendar__availability"],
                       "n_replacements": o[f"{P}calendar__n_replacements"], "cas72": o[f"{P}calendar__cas72_annual"],
                       "lcoe": o[f"{P}lcoe_calc__lcoe"], "committed_lcoe": float(rows[cid]["lcoe"]) if "lcoe" in rows[cid] else None,
                       "predicted_n": pk["live_n"], "predicted_A": pk["live_A"],
                       "n_agrees": o[f"{P}calendar__n_replacements"] == pk["live_n"],
                       "A_reldev": rel(o[f"{P}calendar__availability"], pk["live_A"]),
                       "wall_peak_vs_committed_reldev": wall_identity, "oracle_parity_worst": parity,
                       "verdicts": verd(r)}
    worst_all = max(worst_all, parity, ef_summary[cid]["A_reldev"], wall_identity)
    print(cid, ef_summary[cid]["state"], "n", o[f"{P}calendar__n_replacements"], "(pred", pk["live_n"], ") A",
          o[f"{P}calendar__availability"], "(pred", pk["live_A"], ") lcoe", o[f"{P}lcoe_calc__lcoe"],
          "wall id", f"{wall_identity:.1e}", "parity", f"{parity:.2e}")

# event dates (diagnostic, D6) from the oracle's closed form at the baseline and at E/F
def events_at(inputs, a_direct):
    ov = oe._oracle_overrides(inputs); ov["availability_direct"] = a_direct
    saved = dict(vs.IN); vs.IN.update(ov)
    try:
        o = vs.compute()
        return vs._oracle_lifecycle_calendar(
            cost_per_event=(o["blanket"] + o["divertor"]) * vs.IN["n_mod"], q_n=o["wall_load_peak"],
            fluence_limit=vs.IN["fluence_limit"], interest_rate=vs.IN["discount_rate"],
            operational_years=vs.IN["operational_years"], outage_years=vs.IN["outage_years"],
            unplanned_fraction=vs.IN["unplanned_fraction"], coil_life_fpy=vs.IN["coil_life_fpy"],
            availability_direct=a_direct)["events"]
    finally:
        vs.IN.clear(); vs.IN.update(saved)
(WI / "evidence/baseline_live/events.json").write_text(json.dumps(
    {"live_7mo_u0": events_at(live["inputs"], 0.0), "held_0.85_periodic": events_at(live["inputs"], 0.85)}, indent=1))
(WI / "evidence/offdesign_points/events.json").write_text(json.dumps(
    {name: events_at(r["inputs"], 0.0) for name, r in zip(arms.keys(), res)} |
    {cid: events_at(r["inputs"], 0.0) for cid, r in zip(("c3343", "c7752"), ef)}, indent=1))
(WI / "evidence/offdesign_points/summary.json").write_text(json.dumps(
    {"arms": summary, "stepping_points": ef_summary, "worst_deviation_overall": worst_all}, indent=1, default=str))
print("WORST DEVIATION OVERALL", worst_all)
print("done")
