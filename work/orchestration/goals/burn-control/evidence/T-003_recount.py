"""Recount of the re-reading study's results (goal burn-control round 1, T-003), from the record's own
`results/points.csv` and `results/excluded_points.csv` only -- the numbers record.md sections 3-6, 12 and
15 state, derived in one place so a reader (the fresh administrator, the checkpoint, the round review) can
reproduce every one. Usage:
    uv run python T-003_recount.py <record_dir>
Bases: "here" = this record (the WI-043 pin; ten verdicts); "committed" = the 20260905-stored-energy-basis
record's own columns joined per point (the WI-042 pin; nine verdicts). Both at the WI-042 profile family and
the held coupling 1.00. Comparisons are over the `executed_in_both` class only.
"""
import csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path

rec = Path(sys.argv[1]); R = rec / "results"
def b(x): return str(x).strip().lower() == "true"
def f(x):
    try: return float(x)
    except (TypeError, ValueError): return None
pts = list(csv.DictReader((R / "points.csv").open()))
exc = list(csv.DictReader((R / "excluded_points.csv").open())) if (R / "excluded_points.csv").exists() else []
out = {"evaluated": len(pts), "excluded": len(exc)}
arms = sorted({p["arm_id"] for p in pts})
VERD = ["beta_ok", "burn_hold_ok", "cond_strain_ok", "net_positive", "peak_field_ok", "recirc_ok", "sustainment_ok", "tbr_ok", "wall_load_ok", "wp_stress_ok"]

out["classes"] = dict(Counter(p["class_vs_committed"] for p in pts))
out["excluded_classes"] = dict(Counter(e["class_vs_committed"] for e in exc))
both = [p for p in pts if p["class_vs_committed"] == "executed_in_both"]
out["executed_in_both"] = len(both)

# --- the identities WI-043 predicted (SV-059 and the channel identity) ---
def worst(rows, col):
    v = [f(r[col]) for r in rows if f(r[col]) is not None]
    return {"n": len(v), "max": max(v) if v else None}
out["identity_channels_vs_committed"] = {c: worst(both, c) for c in ("lcoe_reldev_vs_committed", "p_fus_reldev_vs_committed", "wall_peak_reldev_vs_committed", "p_aux_absdev_MW_vs_committed")}
out["W_ratio_vs_committed"] = worst(both, "W_ratio_vs_committed") | {"min": min(f(r["W_ratio_vs_committed"]) for r in both if f(r["W_ratio_vs_committed"]) is not None)}
out["ignited_equals_committed"] = {"true": sum(b(p["ignited_equals_committed"]) for p in both), "false": sum(p["ignited_equals_committed"] == "False" for p in both)}
out["sv059"] = {
    "feasible_equals_driven_all": {"true": sum(b(p["sv059_feasible_equals_driven"]) for p in pts), "false": sum(p["sv059_feasible_equals_driven"] == "False" for p in pts)},
    "verdict_equals_sign_all": {"true": sum(b(p["sv059_verdict_equals_sign"]) for p in pts), "false": sum(p["sv059_verdict_equals_sign"] == "False" for p in pts)},
    "verdict_equals_committed_sign_both": {"true": sum(b(p["sv059_verdict_equals_committed_sign"]) for p in both), "false": sum(p["sv059_verdict_equals_committed_sign"] == "False" for p in both)},
}
out["sv059_disagreements"] = [{k: p[k] for k in ("case_id", "arm_id", "R", "a", "I_coil_A", "T_i0_keV", "n_e0", "burn_hold_ok", "p_aux_required_MW_oracle", "committed_p_aux_required_MW", "feasible", "feasible_driven")}
                              for p in pts if p["sv059_feasible_equals_driven"] == "False" or p["sv059_verdict_equals_sign"] == "False" or p["sv059_verdict_equals_committed_sign"] == "False"][:20]
out["W_store_vs_oracle_worst_reldev"] = worst(pts, "W_store_vs_oracle_reldev")["max"]

# --- per-arm counts here (all executed points) and beside the committed reading (both-class) ---
def counts(rows):
    return {"evaluated": len(rows), "feasible_ten": sum(b(r["feasible"]) for r in rows),
            "feasible_nine": sum(b(r["feasible_nine"]) for r in rows),
            "ignited": sum(b(r["ignited"]) for r in rows),
            "ignited_state": sum(b(r["feasible_nine"]) and b(r["ignited"]) for r in rows),
            "feasible_driven": sum(b(r["feasible_driven"]) for r in rows),
            "burn_hold_violated": sum(r["burn_hold_ok"] == "violated" for r in rows)}
out["per_arm_here_all"] = {a: counts([p for p in pts if p["arm_id"] == a]) for a in arms}
out["per_arm_here_both"] = {a: counts([p for p in both if p["arm_id"] == a]) for a in arms}
def ccounts(rows):
    return {"evaluated": len(rows), "feasible": sum(b(r["committed_feasible"]) for r in rows),
            "ignited": sum(b(r["committed_ignited"]) for r in rows),
            "feasible_driven": sum(b(r["committed_feasible_driven"]) for r in rows)}
out["per_arm_committed_both"] = {a: ccounts([p for p in both if p["arm_id"] == a]) for a in arms}
out["totals_here"] = counts(pts); out["totals_committed_both"] = ccounts(both)

# --- verdict flips per constraint (both-class); burn_hold_ok has no committed column and is read against the sign ---
flips = {}
for v in VERD:
    c = f"committed_{v}"
    if c not in pts[0]: continue
    tr = Counter((p[c], p[v]) for p in both)
    flips[v] = {f"{a_}->{b_}": n for (a_, b_), n in tr.items() if a_ != b_}
out["verdict_flips_both"] = flips
out["violated_per_constraint_here_all"] = {v: sum(p[v] == "violated" for p in pts) for v in VERD}
out["violated_alone_here_all"] = {v: sum(p[v] == "violated" and all(p[w] == "satisfied" for w in VERD if w != v) for p in pts) for v in VERD}

# --- transitions (both-class): the committed three-state against this record's, and the ten-verdict fate ---
out["transitions_both"] = dict(Counter(p["transition_vs_committed"] for p in both))
out["transitions_both_per_arm"] = {a: dict(Counter(p["transition_vs_committed"] for p in both if p["arm_id"] == a)) for a in arms}
out["committed_feasible_fate_under_ten"] = dict(Counter(("feasible_ten" if b(p["feasible"]) else ("burn_hold_violated" if p["burn_hold_ok"] == "violated" else "other")) for p in both if b(p["committed_feasible"])))

# --- the stability pass: branch by state, arm, T, a ---
stab = [p for p in pts if p.get("branch_oracle") not in (None, "")]
out["stability"] = {"points_with_sign": len(stab), "branch": dict(Counter(p["branch_oracle"] for p in stab)),
                    "branch_by_state": {s: dict(Counter(p["branch_oracle"] for p in stab if p["state_here"] == s)) for s in ("driven", "ignited")},
                    "branch_by_arm": {a: dict(Counter(p["branch_oracle"] for p in stab if p["arm_id"] == a)) for a in arms},
                    "branch_by_T": {T: dict(Counter(p["branch_oracle"] for p in stab if abs(float(p["T_i0_keV"]) - T) < 1e-6)) for T in (13.0, 14.63, 16.0, 17.0, 18.0)},
                    "slope_MW_per_keV": {"driven": worst([p for p in stab if p["state_here"] == "driven"], "dpaux_dT_MW_per_keV_oracle") | {"min": min((f(p["dpaux_dT_MW_per_keV_oracle"]) for p in stab if p["state_here"] == "driven"), default=None)},
                                         "ignited": worst([p for p in stab if p["state_here"] == "ignited"], "dpaux_dT_MW_per_keV_oracle") | {"min": min((f(p["dpaux_dT_MW_per_keV_oracle"]) for p in stab if p["state_here"] == "ignited"), default=None)}},
                    "rising_points": [{k: p[k] for k in ("case_id", "arm_id", "R", "a", "I_coil_A", "T_i0_keV", "n_e0", "state_here", "dpaux_dT_MW_per_keV_oracle", "p_aux_required_MW_oracle", "lcoe")} for p in stab if p["branch_oracle"] == "rising"][:30],
                    "missing_sign_among_feasible_nine": sum(1 for p in pts if b(p["feasible_nine"]) and p.get("branch_oracle") in (None, ""))}
base = [r for r in pts if b(r["is_baseline_point"])]
out["baseline_row"] = ({k: base[0][k] for k in ("case_id", "lcoe", "p_aux_required_MW_oracle", "burn_hold_ok", "sustainment_ok", "wall_load_peak", "W_th_MJ_oracle", "beta", "dpaux_dT_MW_per_keV_oracle", "branch_oracle", "committed_lcoe", "committed_p_aux_required_MW", "lcoe_reldev_vs_committed")} if base else None)

# --- the cheapest points per arm: ten-verdict feasible, driven, and the committed driven ---
def cheapest(rows, key="lcoe", cond="feasible"):
    cand = [r for r in rows if b(r[cond]) and f(r[key]) is not None]
    if not cand: return None
    r = min(cand, key=lambda r: f(r[key]))
    return {k: r[k] for k in ("case_id", "arm_id", "R", "a", "I_coil_A", "T_i0_keV", "n_e0", "eta_source_heat", "tau_ratio_ash", "lcoe", "wall_load_peak", "p_aux_required_MW_oracle", "burn_hold_ok", "branch_oracle", "dpaux_dT_MW_per_keV_oracle", "committed_case_id", "committed_lcoe", "committed_feasible_driven", "class_vs_committed")}
out["cheapest_feasible_ten_per_arm"] = {a: cheapest([p for p in pts if p["arm_id"] == a]) for a in arms}
out["cheapest_driven_per_arm"] = {a: cheapest([p for p in pts if p["arm_id"] == a], cond="feasible_driven") for a in arms}
out["cheapest_feasible_nine_per_arm"] = {a: cheapest([p for p in pts if p["arm_id"] == a], cond="feasible_nine") for a in arms}
out["cheapest_feasible_ten_per_arm_both_only"] = {a: cheapest([p for p in both if p["arm_id"] == a]) for a in arms}
def cheapest_by(rows, keyf, cond="feasible"):
    d = defaultdict(list)
    for r in rows:
        if b(r[cond]) and f(r["lcoe"]) is not None: d[keyf(r)].append(f(r["lcoe"]))
    return {str(k): min(v) for k, v in sorted(d.items())}
p100 = [p for p in pts if p["arm_id"] == "arm-fence-p100"]; p220 = [p for p in pts if p["arm_id"] == "arm-search-p220"]
out["p100_feasible_by_T"] = dict(Counter(r["T_i0_keV"] for r in p100 if b(r["feasible"])))
out["p100_feasible_by_a"] = dict(Counter(r["a"] for r in p100 if b(r["feasible"])))
out["p100_burn_violated_by_a"] = dict(Counter(r["a"] for r in p100 if r["burn_hold_ok"] == "violated"))
out["p100_burn_violated_by_T"] = dict(Counter(r["T_i0_keV"] for r in p100 if r["burn_hold_ok"] == "violated"))
out["p100_cheapest_feasible_by_T"] = cheapest_by(p100, lambda r: float(r["T_i0_keV"]))
out["p100_cheapest_feasible_by_a"] = cheapest_by(p100, lambda r: float(r["a"]))
out["p220_cheapest_feasible_by_T"] = cheapest_by(p220, lambda r: float(r["T_i0_keV"]))

# --- the design column (R 12.7, a 1.3) at each level ---
def design_col(rows, wp):
    return [r for r in rows if abs(float(r["R"]) - 12.7) < 1e-9 and abs(float(r["a"]) - 1.3) < 1e-9 and abs(float(r["p_wallplug_heat_MW"]) - wp) < 1e-9]
for wp in (100.0, 220.0):
    col = design_col(pts, wp)
    out[f"design_column_{int(wp)}"] = {"points": len(col), "feasible_ten": sum(b(r["feasible"]) for r in col), "feasible_driven": sum(b(r["feasible_driven"]) for r in col),
                                       "feasible_nine": sum(b(r["feasible_nine"]) for r in col), "ignited": sum(b(r["ignited"]) for r in col),
                                       "burn_hold_violated": sum(r["burn_hold_ok"] == "violated" for r in col),
                                       "feasible_points": [{k: r[k] for k in ("case_id", "arm_id", "I_coil_A", "T_i0_keV", "n_e0", "eta_source_heat", "lcoe", "p_aux_required_MW_oracle", "wall_load_peak", "branch_oracle", "dpaux_dT_MW_per_keV_oracle", "is_baseline_point")} for r in col if b(r["feasible"])],
                                       "committed_feasible_driven": sum(b(r["committed_feasible_driven"]) for r in col if r["class_vs_committed"] == "executed_in_both")}
out["R12.7_100MW_burn_violated_by_a"] = dict(Counter(r["a"] for r in pts if abs(float(r["R"]) - 12.7) < 1e-9 and abs(float(r["p_wallplug_heat_MW"]) - 100.0) < 1e-9 and r["burn_hold_ok"] == "violated"))
out["R12.7_100MW_feasible_by_a"] = dict(Counter(r["a"] for r in pts if abs(float(r["R"]) - 12.7) < 1e-9 and abs(float(r["p_wallplug_heat_MW"]) - 100.0) < 1e-9 and b(r["feasible"])))

# --- the committed headline points here ---
for cid, tag in (("c2823", "committed cheapest driven 100 MW"), ("c6466", "committed cheapest driven 220 MW"), ("c2132", "the 20260904 headline c1721 (ignited at the rule)"), ("c2835", "the probe's P1"), ("c3694", "the pinned baseline"), ("c7625", "committed cheapest driven design column 220 MW")):
    r = next((p for p in both if p["committed_case_id"].endswith(":" + cid)), None)
    out[f"committed_{cid}"] = ({"tag": tag, **{k: r[k] for k in ("case_id", "R", "a", "I_coil_A", "T_i0_keV", "n_e0", "eta_source_heat", "lcoe", "committed_lcoe", "p_aux_required_MW_oracle", "committed_p_aux_required_MW", "burn_hold_ok", "sustainment_ok", "feasible", "feasible_driven", "committed_feasible_driven", "state_here", "state_committed", "branch_oracle", "dpaux_dT_MW_per_keV_oracle")}} if r else {"tag": tag, "missing": True})

# --- the re-read arm and the transect arm ---
rr = [p for p in pts if p["arm_id"] == "arm-reread-p220"]
out["reread"] = {"feasible_ten_by_eta": dict(Counter(p["eta_source_heat"] for p in rr if b(p["feasible"]))), "driven_by_eta": dict(Counter(p["eta_source_heat"] for p in rr if b(p["feasible_driven"]))),
                 "committed_driven_by_eta": dict(Counter(p["eta_source_heat"] for p in rr if b(p["committed_feasible_driven"]))), "burn_hold_violated": sum(p["burn_hold_ok"] == "violated" for p in rr),
                 "cheapest_feasible_ten": cheapest(rr)}
tr = sorted([p for p in pts if p["arm_id"] == "arm-transect-ash"], key=lambda p: (float(p["p_wallplug_heat_MW"]), float(p["R"]), float(p["a"]), float(p["tau_ratio_ash"])))
out["transect"] = [{k: p[k] for k in ("R", "a", "I_coil_A", "T_i0_keV", "n_e0", "p_wallplug_heat_MW", "tau_ratio_ash", "wall_load_ok", "sustainment_ok", "burn_hold_ok", "feasible", "p_aux_required_MW_oracle", "committed_p_aux_required_MW", "branch_oracle", "lcoe")} for p in tr]

# --- the excluded set beside the committed 164 ---
out["excluded_by_arm"] = dict(Counter(e["arm_id"] for e in exc))
out["excluded_in_both"] = sum(e["class_vs_committed"] == "excluded_in_both" for e in exc)
out["committed_executed_now_excluded"] = sum(e["class_vs_committed"] == "committed_executed_now_excluded" for e in exc)
out["committed_excluded_now_executed"] = sum(p["class_vs_committed"] == "committed_excluded_now_executed" for p in pts)

print(json.dumps(out, indent=1, default=str))
