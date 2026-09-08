"""Recount of the coil-bore re-read (goal minor-radius round 1, T-003), from the record's own
`results/points.csv` and `results/excluded_points.csv` only -- the numbers record.md sections 3-6, 11 and 15
state, derived in one place so a reader (the fresh administrator, the checkpoint, the round review) can
reproduce every one. Usage:
    uv run python T-003_recount.py <record_dir>
Bases: "here" = this record (the WI-044 pin; ten verdicts); "committed" = the 20260907-burn-control record's own
columns joined per point (the WI-043 pin; ten verdicts). Both at the WI-042 profile family, the held coupling 1.00
and the same executor. Comparisons are over the `executed_in_both` class only; the transect arm's 35 new points
carry no committed row.
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

# --- the identities WI-044 predicted: physics unchanged; the magnet move = the bore factor ---
def worst(rows, col):
    v = [f(r[col]) for r in rows if f(r[col]) is not None]
    return {"n": len(v), "max": max(v) if v else None}
out["physics_identity"] = {"max_physics_reldev_vs_committed": worst(both, "max_physics_reldev_vs_committed"),
                           "channels_named_at_max": dict(Counter(p["max_physics_reldev_name"] for p in both if f(p["max_physics_reldev_vs_committed"]) and f(p["max_physics_reldev_vs_committed"]) > 1e-12)),
                           "p_aux_absdev_MW_vs_committed": worst(both, "p_aux_absdev_MW_vs_committed"),
                           "ignited_equals_committed": {"true": sum(b(p["ignited_equals_committed"]) for p in both), "false": sum(p["ignited_equals_committed"] == "False" for p in both)}}
out["bore_norm_residual"] = {"max_abs": max(abs(f(p["B_peak_ratio_minus_bore_norm"]) or 0.0) for p in both) if both else None}
out["W_store_vs_oracle_worst_reldev"] = worst(pts, "W_store_vs_oracle_reldev")["max"]
out["bore_norm_range"] = {"min": min(f(p["bore_norm"]) for p in pts), "max": max(f(p["bore_norm"]) for p in pts)}
out["points_with_bore_norm_below_1"] = sum(1 for p in pts if f(p["bore_norm"]) < 1.0 - 1e-12)

# --- per-arm counts here and committed at the joined points ---
def counts(rows):
    return {"evaluated": len(rows), "feasible": sum(b(r["feasible"]) for r in rows), "ignited": sum(b(r["ignited"]) for r in rows)}
out["per_arm_here_all"] = {a: counts([p for p in pts if p["arm_id"] == a]) for a in arms}
out["per_arm_here_both"] = {a: counts([p for p in both if p["arm_id"] == a]) for a in arms}
out["per_arm_committed_both"] = {a: {"evaluated": len([p for p in both if p["arm_id"] == a]), "feasible": sum(b(p["committed_feasible"]) for p in both if p["arm_id"] == a)} for a in arms}
out["totals_here"] = counts(pts); out["totals_committed_both"] = {"feasible": sum(b(p["committed_feasible"]) for p in both)}

# --- verdict flips (both-class), per constraint and direction; per arm; per (R, a) ---
flips = {}
for v in VERD:
    tr = Counter((p[f"committed_{v}"], p[v]) for p in both)
    flips[v] = {f"{a_}->{b_}": n for (a_, b_), n in tr.items() if a_ != b_}
out["verdict_flips_both"] = flips
out["points_with_any_flip"] = sum(1 for p in both if p["n_flips"] not in ("", "0", "None"))
out["flips_per_arm"] = {a: dict(Counter(p[f"flip_{v}"] for p in both if p["arm_id"] == a for v in VERD if p[f"flip_{v}"] not in ("", "None"))) for a in arms}
by_Ra = defaultdict(Counter)
for p in both:
    for v in VERD:
        if p[f"flip_{v}"] not in ("", "None"):
            by_Ra[(p["R"], p["a"])][f"{v}:{p[f'flip_{v}']}"] += 1
out["flips_by_R_a"] = {f"R{k[0]}_a{k[1]}": dict(c) for k, c in sorted(by_Ra.items(), key=lambda kv: (float(kv[0][0]), float(kv[0][1])))}
out["feasible_transitions_both"] = dict(Counter(p["feasible_transition"] for p in both))
out["feasible_transitions_per_arm"] = {a: dict(Counter(p["feasible_transition"] for p in both if p["arm_id"] == a)) for a in arms}
out["violated_per_constraint_per_arm"] = {v: {a: sum(p[v] == "violated" for p in pts if p["arm_id"] == a) for a in arms} for v in VERD}
out["violated_alone_per_arm"] = {v: {a: sum(p[v] == "violated" and all(p[w] == "satisfied" for w in VERD if w != v) for p in pts if p["arm_id"] == a) for a in arms} for v in VERD}
out["flips_per_arm_per_verdict"] = {v: {a: sum(1 for p in both if p["arm_id"] == a and p[f"flip_{v}"] not in ("", "None")) for a in arms} for v in ("peak_field_ok", "wp_stress_ok")}
out["violated_per_constraint_here_all"] = {v: sum(p[v] == "violated" for p in pts) for v in VERD}
out["violated_alone_here_all"] = {v: sum(p[v] == "violated" and all(p[w] == "satisfied" for w in VERD if w != v) for p in pts) for v in VERD}

# --- the cost move ---
def stats(vals):
    vals = [x for x in vals if x is not None]
    return {"n": len(vals), "min": min(vals), "max": max(vals), "mean": sum(vals) / len(vals)} if vals else None
out["lcoe_delta_vs_committed"] = stats([f(p["lcoe_delta_vs_committed"]) for p in both])
out["lcoe_delta_feasible_both"] = stats([f(p["lcoe_delta_vs_committed"]) for p in both if b(p["feasible"]) and b(p["committed_feasible"])])
out["magnet_structure_frac_range"] = stats([f(p["magnet_structure_frac_of_total"]) for p in pts])
out["m_casing_t_range"] = stats([f(p["m_casing_t"]) for p in pts]); out["W_mag_GJ_range"] = stats([f(p["W_mag_GJ"]) for p in pts])
out["B_peak_range"] = stats([f(p["B_peak"]) for p in pts])

# --- the cheapest feasible machine per level, per arm, per a, per R; the aspect ratio ---
def cheapest(rows):
    rows = [r for r in rows if b(r["feasible"])]
    if not rows: return None
    r = min(rows, key=lambda r: f(r["lcoe"]))
    return {k: r[k] for k in ("case_id", "arm_id", "lcoe", "R", "a", "I_coil_A", "T_i0_keV", "n_e0", "eta_source_heat", "aspect_ratio", "B_peak", "W_mag_GJ", "m_casing_t", "wall_load_peak", "p_aux_required_MW_oracle", "committed_case_id", "committed_lcoe", "lcoe_delta_vs_committed")}
def ccheapest(rows):
    rows = [r for r in rows if b(r["committed_feasible"])]
    if not rows: return None
    r = min(rows, key=lambda r: f(r["committed_lcoe"]))
    return {k: r[k] for k in ("committed_case_id", "case_id", "committed_lcoe", "R", "a", "I_coil_A", "T_i0_keV", "n_e0", "feasible", "lcoe")}
for lvl in ("100.0", "220.0"):
    rows = [p for p in pts if p["p_wallplug_heat_MW"] == lvl]
    out[f"cheapest_feasible_{lvl}"] = cheapest(rows)
    out[f"cheapest_feasible_{lvl}_grid_arms_only"] = cheapest([p for p in rows if p["arm_id"] in ("arm-fence-p100", "arm-search-p220", "arm-reread-p220")])
    out[f"committed_cheapest_feasible_{lvl}_both"] = ccheapest([p for p in both if p["p_wallplug_heat_MW"] == lvl])
    out[f"feasible_by_a_{lvl}"] = {a: sum(b(p["feasible"]) for p in rows if p["a"] == a and p["arm_id"] in ("arm-fence-p100", "arm-search-p220")) for a in sorted({p["a"] for p in rows}, key=float)}
    out[f"committed_feasible_by_a_{lvl}"] = {a: sum(b(p["committed_feasible"]) for p in both if p["p_wallplug_heat_MW"] == lvl and p["a"] == a and p["arm_id"] in ("arm-fence-p100", "arm-search-p220")) for a in sorted({p["a"] for p in rows}, key=float)}
    out[f"cheapest_feasible_by_a_{lvl}"] = {a: (cheapest([p for p in rows if p["a"] == a]) or {}).get("lcoe") for a in sorted({p["a"] for p in rows}, key=float)}
    out[f"cheapest_feasible_by_R_{lvl}"] = {Rv: (cheapest([p for p in rows if p["R"] == Rv]) or {}).get("lcoe") for Rv in sorted({p["R"] for p in rows}, key=float)}
    out[f"feasible_by_R_{lvl}"] = {Rv: sum(b(p["feasible"]) for p in rows if p["R"] == Rv) for Rv in sorted({p["R"] for p in rows}, key=float)}
    out[f"aspect_ratio_of_feasible_{lvl}"] = stats([f(p["aspect_ratio"]) for p in rows if b(p["feasible"])])
    near = [p for p in rows if b(p["feasible"]) and f(p["a"]) <= f(p["R"]) / 9.8 + 0.1]
    out[f"feasible_near_A9.8_{lvl}"] = {"n": len(near), "cheapest": cheapest(near)}

# --- the transect arm ---
tr = [p for p in pts if p["arm_id"] == "arm-transect-a"]
out["transect_a"] = {}
for (Rv, lvl) in sorted({(p["R"], p["p_wallplug_heat_MW"]) for p in tr}, key=lambda t: (float(t[0]), float(t[1]))):
    col = [p for p in pts if p["p_wallplug_heat_MW"] == lvl and p["R"] == Rv and ((Rv == "12.7" and f(p["I_coil_A"]) == 15.4e6 and f(p["T_i0_keV"]) == 14.63 and abs(f(p["n_e0"]) - 5.06e20) < 1e12) or (Rv in ("15.7", "14.2") and f(p["I_coil_A"]) == 13.0e6 and f(p["T_i0_keV"]) == 13.0 and abs(f(p["n_e0"]) - 5.06e20) < 1e12)) and f(p["eta_source_heat"]) == 0.5 and f(p["tau_ratio_ash"]) == 8.0]
    out["transect_a"][f"R{Rv}_{lvl}MW"] = [{"a": p["a"], "arm": p["arm_id"], "lcoe": round(f(p["lcoe"]), 3), "committed_lcoe": (round(f(p["committed_lcoe"]), 3) if f(p["committed_lcoe"]) is not None else None), "B_peak": round(f(p["B_peak"]), 3), "m_casing_t": round(f(p["m_casing_t"]), 2), "W_mag_GJ": round(f(p["W_mag_GJ"]), 1), "A": round(f(p["aspect_ratio"]), 2), "feasible": b(p["feasible"]), "violated": [v for v in VERD if p[v] == "violated"]} for p in sorted(col, key=lambda p: f(p["a"]))]

# --- the design column and the shadow ---
dc = [p for p in pts if p["R"] == "12.7" and p["a"] == "1.3"]
out["design_column"] = {lvl: {"feasible": sum(b(p["feasible"]) for p in dc if p["p_wallplug_heat_MW"] == lvl), "cheapest": cheapest([p for p in dc if p["p_wallplug_heat_MW"] == lvl])} for lvl in ("100.0", "220.0")}
out["baseline_row"] = next(({k: p[k] for k in ("case_id", "lcoe", "B_peak", "W_mag_GJ", "m_casing_t", "aspect_ratio", "feasible", "committed_lcoe", "lcoe_delta_vs_committed")} for p in pts if b(p["is_baseline_point"])), None)
out["shadow"] = {lvl: {"feasible": sum(b(p["feasible"]) for p in pts if p["p_wallplug_heat_MW"] == lvl), "survive_lo": sum(b(p["feasible_shadow_lo"]) for p in pts if p["p_wallplug_heat_MW"] == lvl), "survive_hi": sum(b(p["feasible_shadow_hi"]) for p in pts if p["p_wallplug_heat_MW"] == lvl)} for lvl in ("100.0", "220.0")}
print(json.dumps(out, indent=1, default=str))
