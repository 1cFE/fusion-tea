"""Recount of the restating study's results (goal stored-energy-basis round 2, T-003), from the
record's own `results/points.csv` and `results/excluded_points.csv` only -- the numbers the record's
sections 3-6, 12 and 15 state, derived in one place so a reader (or the fresh administrator and the
checkpoint) can reproduce every one. Usage:
    python round2_T-003_recount.py <record_dir>
Every count carries its basis: "rule" = this record (the WI-042 profile family, executed);
"committed" = the committed record's own columns joined per point (the WI-037 family, pin c1b0f0d1);
"cf0915" / "cf0940" = the two constant-scale counterfactuals (oracle-side, the WI-037 family times a
constant with the closure live, pin c1b0f0d1). Comparisons are over the `executed_in_both` class only.
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
VERD = ["beta_ok", "cond_strain_ok", "net_positive", "peak_field_ok", "recirc_ok", "sustainment_ok", "tbr_ok", "wall_load_ok", "wp_stress_ok"]

# --- classes and denominators ---
out["classes"] = dict(Counter(p["class_vs_committed"] for p in pts))
out["excluded_classes"] = dict(Counter(e["class_vs_committed"] for e in exc))
both = [p for p in pts if p["class_vs_committed"] == "executed_in_both"]
newrows = [p for p in pts if p["class_vs_committed"] == "not_proposed_by_committed"]
out["executed_in_both"] = len(both); out["not_proposed_by_committed"] = len(newrows)

# --- per-arm counts at the rule (all executed points) and beside the committed reading (both-class) ---
def counts(rows):
    return {"evaluated": len(rows), "feasible": sum(b(r["feasible"]) for r in rows),
            "ignited": sum(b(r["ignited"]) for r in rows),
            "feasible_ignited": sum(b(r["feasible"]) and b(r["ignited"]) for r in rows),
            "feasible_driven": sum(b(r["feasible_driven"]) for r in rows)}
out["per_arm_rule_all"] = {a: counts([p for p in pts if p["arm_id"] == a]) for a in arms}
out["per_arm_rule_both"] = {a: counts([p for p in both if p["arm_id"] == a]) for a in arms}
out["per_arm_rule_newrows"] = {a: counts([p for p in newrows if p["arm_id"] == a]) for a in arms if any(p["arm_id"] == a for p in newrows)}
def ccounts(rows):
    return {"evaluated": len(rows), "feasible": sum(b(r["committed_feasible"]) for r in rows),
            "ignited": sum(b(r["committed_ignited"]) for r in rows),
            "feasible_driven": sum(b(r["committed_feasible_driven"]) for r in rows)}
out["per_arm_committed_both"] = {a: ccounts([p for p in both if p["arm_id"] == a]) for a in arms}
for tag in ("cf0915", "cf0940"):
    out[f"per_arm_{tag}_both"] = {a: {"comparable": sum(p[f"{tag}_p_aux_required_MW"] not in ("", None) for p in both if p["arm_id"] == a),
                                      "feasible_driven": sum(b(p[f"{tag}_feasible_driven"]) for p in both if p["arm_id"] == a),
                                      "ignited": sum(b(p[f"{tag}_ignited"]) for p in both if p["arm_id"] == a)} for a in arms}

# --- verdict flips per constraint (both-class) ---
flips = {}
for v in VERD:
    c = p_key = f"committed_{v}"
    if c not in pts[0]: continue
    tr = Counter((p[c], p[v]) for p in both)
    flips[v] = {f"{a}->{b_}": n for (a, b_), n in tr.items() if a != b_}
out["verdict_flips_both"] = flips
out["violated_per_constraint_rule_all"] = {v: sum(p[v] == "violated" for p in pts) for v in VERD}

# --- transitions (both-class) ---
out["transitions_both"] = dict(Counter(p["transition_vs_committed"] for p in both))
out["transitions_both_per_arm"] = {a: dict(Counter(p["transition_vs_committed"] for p in both if p["arm_id"] == a)) for a in arms}

# --- rule vs the two scales on the requirement (both-class, comparable rows) ---
out["rule_vs_scales_both"] = dict(Counter(p["rule_vs_scales"] for p in both))
out["rule_vs_scales_per_arm"] = {a: dict(Counter(p["rule_vs_scales"] for p in both if p["arm_id"] == a)) for a in arms}

# --- the cheapest driven points per arm at the rule, and the committed ones ---
def cheapest(rows, key="lcoe", cond="feasible_driven"):
    cand = [r for r in rows if b(r[cond]) and f(r[key]) is not None]
    if not cand: return None
    r = min(cand, key=lambda r: f(r[key]))
    return {k: r[k] for k in ("case_id", "arm_id", "R", "a", "I_coil_A", "T_i0_keV", "n_e0", "eta_source_heat", "tau_ratio_ash", "lcoe", "wall_load_peak", "p_aux_required_MW_oracle", "W_th_MJ_oracle", "alpha_He_eff_oracle", "He_over_ne_oracle", "class_vs_committed", "committed_case_id", "committed_lcoe", "committed_feasible_driven")}
out["cheapest_driven_rule_per_arm"] = {a: cheapest([p for p in pts if p["arm_id"] == a]) for a in arms}
out["cheapest_driven_rule_per_arm_both_only"] = {a: cheapest([p for p in both if p["arm_id"] == a]) for a in arms}
out["cheapest_feasible_any_rule_per_arm"] = {a: cheapest([p for p in pts if p["arm_id"] == a], cond="feasible") for a in arms}
out["cheapest_driven_per_arm_by_T"] = {a: {T: (cheapest([p for p in pts if p["arm_id"] == a and abs(float(p["T_i0_keV"]) - T) < 1e-6]) or {}).get("lcoe") for T in (13.0, 14.63, 16.0, 17.0, 18.0)} for a in arms}

# --- the design column (R 12.7, a 1.3) at each level: driven points, the baseline ---
def design_col(rows, wp):
    return [r for r in rows if abs(float(r["R"]) - 12.7) < 1e-9 and abs(float(r["a"]) - 1.3) < 1e-9 and abs(float(r["p_wallplug_heat_MW"]) - wp) < 1e-9]
for wp in (100.0, 220.0):
    col = design_col(pts, wp)
    out[f"design_column_{int(wp)}"] = {"points": len(col), "feasible_driven": sum(b(r["feasible_driven"]) for r in col),
                                       "feasible": sum(b(r["feasible"]) for r in col), "ignited": sum(b(r["ignited"]) for r in col),
                                       "driven_points": [{k: r[k] for k in ("case_id", "arm_id", "I_coil_A", "T_i0_keV", "n_e0", "eta_source_heat", "lcoe", "p_aux_required_MW_oracle", "wall_load_peak", "is_baseline_point")} for r in col if b(r["feasible_driven"])],
                                       "committed_feasible_driven": sum(b(r["committed_feasible_driven"]) for r in col if r["class_vs_committed"] == "executed_in_both"),
                                       "cf0915_feasible_driven": sum(b(r["cf0915_feasible_driven"]) for r in col), "cf0940_feasible_driven": sum(b(r["cf0940_feasible_driven"]) for r in col)}
base = [r for r in pts if b(r["is_baseline_point"])]
out["baseline_row"] = ({k: base[0][k] for k in ("case_id", "lcoe", "p_aux_required_MW_oracle", "wall_load_peak", "W_th_MJ_oracle", "W_th_MJ_store", "beta", "alpha_He_eff_oracle", "alpha_n_e_eff_oracle", "committed_lcoe", "committed_p_aux_required_MW", "cf0915_p_aux_required_MW", "cf0940_p_aux_required_MW", "sustainment_ok", "wall_load_ok")} if base else None)

# --- the W correction and the ash shape across the window (all executed points with a committed W) ---
ratios = [f(p["W_ratio_vs_committed"]) for p in both if f(p["W_ratio_vs_committed"])]
out["W_ratio_vs_committed"] = {"n": len(ratios), "min": min(ratios), "max": max(ratios), "mean": sum(ratios) / len(ratios)} if ratios else None
byT = defaultdict(list)
for p in pts: byT[float(p["T_i0_keV"])].append(f(p["alpha_He_eff_oracle"]))
out["alpha_He_eff_by_T"] = {T: {"min": min(v), "max": max(v), "n": len(v)} for T, v in sorted(byT.items())}
bins = defaultdict(list)
for p in both:
    he = f(p["He_over_ne_oracle"]); w = f(p["W_ratio_vs_committed"])
    if he is not None and w is not None: bins[round(he, 2)].append(w)
out["W_ratio_by_He_over_ne_bin"] = {k: {"n": len(v), "mean": sum(v)/len(v), "min": min(v), "max": max(v)} for k, v in sorted(bins.items())}
byRa = defaultdict(list)
for p in both:
    w = f(p["W_ratio_vs_committed"])
    if w is not None: byRa[(float(p["R"]), float(p["a"]))].append(w)
out["W_ratio_by_R_a"] = {f"R{R}_a{a}": {"n": len(v), "mean": sum(v)/len(v), "min": min(v), "max": max(v)} for (R, a), v in sorted(byRa.items())}
wdev = [f(p["W_store_vs_oracle_reldev"]) for p in pts if f(p["W_store_vs_oracle_reldev"]) is not None]
out["W_store_vs_oracle_worst_reldev"] = max(wdev) if wdev else None

# --- the excluded set beside the committed 65 ---
out["excluded_reasons"] = dict(Counter((e["reason"].split(":")[0] if ":" in e["reason"] else e["reason"][:40]) for e in exc))
out["excluded_by_arm"] = dict(Counter(e["arm_id"] for e in exc))
out["committed_excluded_now_executed"] = sum(p["class_vs_committed"] == "committed_excluded_now_executed" for p in pts)
out["committed_executed_now_excluded"] = sum(e["class_vs_committed"] == "committed_executed_now_excluded" for e in exc)
out["excluded_in_both"] = sum(e["class_vs_committed"] == "excluded_in_both" for e in exc)

print(json.dumps(out, indent=1, default=str))
