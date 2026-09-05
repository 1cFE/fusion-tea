"""Basis A -- the model as implemented, with the stored thermal energy forced to the paper's printed value.

Oracle-side diagnostic (NOT package evidence). Drives the package-owned oracle
(`exploration/stellarator_e2e/verify_stellaris.py` through `studies/oracle_entry.py`)
with ONE change: inside `_sustainment.state()` the line

    W_th = 1.5 * p_avg * V * 1e-6

becomes `... * W_SCALE`, where W_SCALE = 504.65 / W_th(baseline, unmodified). Everything
else -- the ash fixed point, ISS04 tau_E, the composed radiation, the alpha heating, the
fences and the cost chain -- is the oracle's own code, untouched on disk. The patch is
applied to the function's SOURCE at import (asserting the line occurs exactly once) and
bound into the module, so `verify_stellaris.py` is never edited.

Assumption stated plainly: a constant scale factor treats the profile-shape error as
multiplicative and geometry-independent. Nothing here says that is true; it is the
cheapest counterfactual and the record says so.

Modes:
  baseline   -- the reference point unmodified, then scaled; prints both sustainment states.
  window     -- every committed point of 20260904-wall-and-heating (results/points.csv),
                re-evaluated with the scale; verdict flips counted against the record.
  parity N   -- N committed points re-evaluated UNMODIFIED against the record (a check
                that this script's point construction reproduces the committed verdicts).
"""
from __future__ import annotations
import csv, inspect, json, sys, textwrap
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
E2E = REPO / "exploration" / "stellarator_e2e"
STUDIES = E2E / "studies"
STUDY = STUDIES / "20260904-wall-and-heating"
for p in (str(E2E), str(STUDIES)):
    if p not in sys.path:
        sys.path.insert(0, p)
import verify_stellaris as vs  # noqa: E402
import oracle_entry as oe      # noqa: E402

P = oe.P
W_PRINTED_MJ = 504.65   # Stellaris Table 5, point A, "Total plasma energy [MJ]" (page_009_table_0.png)
LINE = "W_th = 1.5 * p_avg * V * 1e-6"

# --- the one-line source patch -------------------------------------------------------
_src = textwrap.dedent(inspect.getsource(vs._sustainment))
assert _src.count(LINE) == 1, f"expected exactly one W_th line in _sustainment, found {_src.count(LINE)}"
_patched_src = _src.replace(LINE, LINE + " * W_SCALE")
_ns = dict(vs.__dict__)
_ns["W_SCALE"] = 1.0
exec(compile(_patched_src, "<patched _sustainment>", "exec"), _ns)
_patched = _ns["_sustainment"]


def set_scale(s: float) -> None:
    _ns["W_SCALE"] = float(s)
    vs._sustainment = _patched if s != 1.0 else vs.__dict__.get("_sustainment_orig", vs._sustainment)


vs._sustainment_orig = vs._sustainment

# --- bounds and verdicts, exactly as the committed study's scan read them ---------------
def bounds():
    plant = json.loads((E2E / "generated" / "inputs" / "stellarator_plant_params.json").read_text())
    mfe = json.loads((E2E / "generated" / "inputs" / "mfe_plant_params.json").read_text())
    return {"B_max": plant[f"{P}magnet__B_max"], "sigma_allow": plant[f"{P}magnet__sigma_allow"],
            "eps_cond_allow": plant[f"{P}magnet__eps_cond_allow"], "beta_limit": plant[f"{P}beta_limit"],
            "wall_load_limit": plant[f"{P}wall_load_limit"], "recirc_threshold": mfe[f"{P}recirc_ok__threshold"]}


VERDICTS = ("beta_ok", "cond_strain_ok", "net_positive", "peak_field_ok", "recirc_ok",
            "sustainment_ok", "wall_load_ok", "wp_stress_ok")   # tbr_ok is held-vs-held, always satisfied


def verdicts(ch, B):
    """The nine executing constraints' predicates (mfe_viability.sysml), on the oracle's channels."""
    v = {
        "beta_ok": ch[f"{P}beta_calc__beta"] <= B["beta_limit"],
        "cond_strain_ok": ch[f"{P}cond_strain__eps_cond"] <= B["eps_cond_allow"],
        "net_positive": ch[f"{P}pb__p_net"] > 0.0,
        "peak_field_ok": ch[f"{P}peak_field_calc__B_peak"] <= B["B_max"],
        "recirc_ok": ch[f"{P}pb__rec_frac"] <= B["recirc_threshold"],
        "sustainment_ok": ch[f"{P}sustain__p_aux_required"] <= ch[f"{P}heat__p_coupled"],
        "wall_load_ok": ch[f"{P}wall_peak_calc__wall_load_peak"] <= B["wall_load_limit"],
        "wp_stress_ok": ch[f"{P}wp_stress__sigma_wp"] <= B["sigma_allow"],
    }
    return {k: ("satisfied" if ok else "violated") for k, ok in v.items()}


def point_from_row(r):
    return {f"{P}R": float(r["R"]), f"{P}magnet__R0": float(r["R"]), f"{P}a": float(r["a"]),
            f"{P}availability": float(r["availability"]), f"{P}discount_rate": float(r["discount_rate"]),
            f"{P}magnet__I_coil": float(r["I_coil_A"]), f"{P}n_e0": float(r["n_e0"]),
            f"{P}T_i0": float(r["T_i0_keV"]), f"{P}magnet__j_wp": float(r["j_wp"]),
            f"{P}p_wallplug_heat": float(r["p_wallplug_heat_MW"]),
            f"{P}eta_source_heat": float(r["eta_source_heat"]),
            f"{P}eta_couple_heat": float(r["eta_couple_heat"]),
            f"{P}tau_ratio_ash": float(r["tau_ratio_ash"]),
            f"{P}p_delivered_direct_heat": 0.0, f"{P}p_coupled_direct_heat": 0.0}


BASELINE_POINT = {f"{P}p_wallplug_heat": 100.0}   # the oracle's IN is the design point; the lever explicit


def sustain_state(ch):
    return {k: ch[f"{P}sustain__{k}"] for k in ("W_th", "tau_E", "p_rad", "p_alpha_heat", "p_aux_required", "n_He0")} | {
        "p_coupled": ch[f"{P}heat__p_coupled"], "beta": ch[f"{P}beta_calc__beta"], "p_fus": ch[f"{P}fusion__p_fus"],
        "lcoe": ch[f"{P}lcoe_calc__lcoe"], "wall_load_peak": ch[f"{P}wall_peak_calc__wall_load_peak"]}


def baseline_scale():
    set_scale(1.0)
    ch0 = oe.evaluate(BASELINE_POINT)
    return W_PRINTED_MJ / ch0[f"{P}sustain__W_th"], ch0


def run_baseline():
    B = bounds()
    s, ch0 = baseline_scale()
    set_scale(s); ch1 = oe.evaluate(BASELINE_POINT); set_scale(1.0)
    out = {"W_printed_MJ": W_PRINTED_MJ, "W_scale": s,
           "unmodified": sustain_state(ch0) | {"verdicts": verdicts(ch0, B)},
           "W_forced": sustain_state(ch1) | {"verdicts": verdicts(ch1, B)}}
    # the two-term decomposition of the required-heating move: W/tau_E and everything else
    for k, ch in (("unmodified", ch0), ("W_forced", ch1)):
        out[k]["W_over_tau_E"] = ch[f"{P}sustain__W_th"] / ch[f"{P}sustain__tau_E"]
    (HERE / "baseline_counterfactual.json").write_text(json.dumps(out, indent=1) + "\n")
    for k in ("unmodified", "W_forced"):
        o = out[k]
        print(f"{k:11s} W_th {o['W_th']:8.3f} MJ  tau_E {o['tau_E']:.4f} s  W/tau_E {o['W_over_tau_E']:7.2f} MW  p_rad {o['p_rad']:7.2f}  "
              f"p_alpha_heat {o['p_alpha_heat']:7.2f}  p_aux_required {o['p_aux_required']:7.2f} MW vs coupled {o['p_coupled']:.1f}  "
              f"-> sustainment_ok {o['verdicts']['sustainment_ok']}  n_He0 {o['n_He0']:.3e}  p_fus {o['p_fus']:.1f}  beta {o['beta']:.5f}  "
              f"peak {o['wall_load_peak']:.3f}  lcoe {o['lcoe']:.3f}")
    print(f"scale {s:.6f}")
    return s


# --- window pass ----------------------------------------------------------------------
_B = None
_scale = None


def _init(scale):
    global _B, _scale
    _B = bounds(); _scale = scale
    set_scale(scale)


def _eval_row(r):
    try:
        ch = oe.evaluate(point_from_row(r))
    except Exception as exc:  # the closure's validity edge (record § 15 #8)
        return {"case_id": r["case_id"], "error": f"{type(exc).__name__}: {exc}"}
    v = verdicts(ch, _B)
    st = sustain_state(ch)
    return {"case_id": r["case_id"], **v, "p_aux_required": st["p_aux_required"], "W_th": st["W_th"],
            "tau_E": st["tau_E"], "lcoe": st["lcoe"], "wall_load_peak": st["wall_load_peak"], "beta": st["beta"],
            "p_fus": st["p_fus"], "feasible": all(x == "satisfied" for x in v.values()),
            "ignited": st["p_aux_required"] < 0.0}


def load_rows():
    return list(csv.DictReader((STUDY / "results" / "points.csv").open()))


def run_window(scale, workers=10):
    rows = load_rows()
    with Pool(workers, initializer=_init, initargs=(scale,)) as pool:
        res = pool.map(_eval_row, rows, chunksize=25)
    by_id = {x["case_id"]: x for x in res}
    out_rows = []
    flips = Counter(); flips_arm = Counter(); errs = 0
    for r in rows:
        x = by_id[r["case_id"]]
        if "error" in x:
            errs += 1; out_rows.append({**{k: r[k] for k in ("case_id", "arm_id")}, "error": x["error"]}); continue
        row = {k: r[k] for k in ("case_id", "arm_id", "p_wallplug_heat_MW", "R", "a", "I_coil_A", "n_e0", "T_i0_keV",
                                  "eta_source_heat", "tau_ratio_ash", "is_baseline_point")}
        for k in VERDICTS:
            row[f"{k}_record"] = r[k]; row[f"{k}_forced"] = x[k]
            if r[k] != x[k]:
                flips[(k, r[k], x[k])] += 1; flips_arm[(r["arm_id"], k, r[k], x[k])] += 1
        x["feasible_driven"] = x["feasible"] and not x["ignited"]
        for k in ("p_aux_required", "W_th", "tau_E", "lcoe", "wall_load_peak", "beta", "p_fus"):
            row[f"{k}_forced"] = x[k]
        row["p_aux_required_record"] = r["p_aux_required_MW_oracle"]; row["lcoe_record"] = r["lcoe"]
        for k in ("feasible", "ignited", "feasible_driven"):
            row[f"{k}_record"] = r[k]; row[f"{k}_forced"] = x[k]
        out_rows.append(row)
    keys = list(out_rows[0].keys())
    for o in out_rows:
        for k in o:
            if k not in keys: keys.append(k)
    with (HERE / "window_counterfactual.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(out_rows)
    summary = {"W_scale": scale, "points": len(rows), "oracle_errors": errs, "flips": {f"{k}:{a}->{b}": n for (k, a, b), n in sorted(flips.items())},
               "flips_by_arm": {f"{arm}|{k}:{a}->{b}": n for (arm, k, a, b), n in sorted(flips_arm.items())}, "arms": {}}
    ok_rows = [o for o in out_rows if "error" not in o]
    for arm in sorted(set(o["arm_id"] for o in ok_rows)):
        sub = [o for o in ok_rows if o["arm_id"] == arm]
        rec = {k: sum(o[f"{k}_record"] == "True" for o in sub) for k in ("feasible", "ignited", "feasible_driven")}
        frc = {k: sum(bool(o[f"{k}_forced"]) for o in sub) for k in ("feasible", "ignited", "feasible_driven")}
        drv = [o for o in sub if o["feasible_driven_forced"]]
        best = min(drv, key=lambda o: o["lcoe_forced"]) if drv else None
        col = [o for o in drv if float(o["R"]) == 12.7 and float(o["a"]) == 1.3]
        summary["arms"][arm] = {"n": len(sub), "record": rec, "forced": frc,
                                "cheapest_driven_forced": None if best is None else {k: best[k] for k in ("case_id", "R", "a", "I_coil_A", "n_e0", "T_i0_keV", "lcoe_forced", "p_aux_required_forced", "wall_load_peak_forced")},
                                "driven_on_design_geometry_forced": len(col),
                                "driven_a_values_forced": sorted(set(float(o["a"]) for o in drv))}
    (HERE / "window_summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1))


def run_parity(n):
    rows = load_rows()[:n]
    set_scale(1.0); B = bounds(); bad = 0
    for r in rows:
        ch = oe.evaluate(point_from_row(r)); v = verdicts(ch, B)
        dv = [k for k in VERDICTS if v[k] != r[k]]
        dp = abs(ch[f"{P}sustain__p_aux_required"] - float(r["p_aux_required_MW_oracle"]))
        dl = abs(ch[f"{P}lcoe_calc__lcoe"] - float(r["lcoe"])) / float(r["lcoe"])
        if dv or dp > 1e-6 or dl > 1e-9:
            bad += 1; print("MISMATCH", r["case_id"], dv, dp, dl)
    print(f"parity: {n} committed points re-evaluated unmodified, {bad} mismatches")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "baseline"
    if mode == "baseline":
        run_baseline()
    elif mode == "parity":
        run_parity(int(sys.argv[2]) if len(sys.argv) > 2 else 40)
    elif mode == "window":
        s = run_baseline()
        run_window(s, workers=int(sys.argv[2]) if len(sys.argv) > 2 else 10)
    else:
        raise SystemExit(f"unknown mode {mode}")
