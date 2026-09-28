"""WI-047 phase 3: P3 / P4 / the low case / E (the loop-domain declared invalid) through the
route, the seam at each point, the verdict re-derived through OPERAND_BINDINGS, the source
case reconstructed by the oracle. Modelled on WI-045's evidence/run_phase3_points.py."""
import json, shutil, sys
from pathlib import Path

REPO = Path("/home/reid/1cfe/fusion-tea")
sys.path.insert(0, str(REPO / "exploration/stellarator_e2e/studies"))
sys.path.insert(0, str(REPO / "exploration/stellarator_e2e"))
import study_route as route  # noqa: E402
import oracle_entry as oe  # noqa: E402
import verify_stellaris as vs  # noqa: E402

P = route.P
WI = REPO / "work/active/WI-047_fuel-divertor-vacuum-flows"
NEW = [f"{P}fuel__{o}" for o in ("burn_rate", "inject_rate", "exhaust_rate", "loss_rate", "tbr_required", "tbr_margin", "burn_kg_per_fpy")] + \
      [f"{P}divheat__{o}" for o in ("p_heat_abs", "p_sep", "f_rad_edge", "f_rad_edge_in_range", "p_target_nonrad", "q_target_peak", "q_target_peak_area_scaled", "q_target_margin", "p_heat_operating_minus_installed")] + \
      [f"{P}vacuum__{o}" for o in ("n_molecules", "Q_total", "S_eff_required")]
REQ = dict(route.CHANNELS)
for k in NEW:
    REQ[k.split("__", 2)[2]] = k
base = route._baseline_point(route.MANIFEST_PATH)
DIV_ID = f"{P}divertor_heat_ok__26b4658f9fdfd7b7"


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


def pt(**over):
    d = dict(base); d.update(over); return d

P3 = pt(**{f"{P}R": 15.7, f"{P}magnet__R0": 15.7, f"{P}a": 2.2, f"{P}magnet__I_coil": 13.0e6, f"{P}T_i0": 13.0, f"{P}n_e0": 5.06e20})
P4 = pt(**{f"{P}R": 17.2, f"{P}magnet__R0": 17.2, f"{P}a": 2.2, f"{P}magnet__I_coil": 14.0e6, f"{P}T_i0": 13.0, f"{P}n_e0": 5.06e20})
LOW = pt(**{f"{P}q_target_ref": 5.0})
E = pt(**{f"{P}R": 17.2, f"{P}magnet__R0": 17.2, f"{P}a": 1.8, f"{P}magnet__I_coil": 13.0e6, f"{P}T_i0": 18.0, f"{P}n_e0": 5.06e20})
E7 = dict(E, **{f"{P}n_loops": 7.0})  # the loop's own domain: per-path loss > 8 MPa
names = ["P3_c2823_14loops", "P4_c3598_14loops", "P0_low_case_q_ref_5", "E_c3343_14loops_negative_net", "E7_c3343_7loops_loop_domain"]
res = run("wi047-offdesign", [P3, P4, LOW, E, E7], WI / "evidence/offdesign_points")
pred = json.load(open(WI / "prototype/proto_results.json"))
bindings = oe.operand_bindings()[DIV_ID]


import glob
PKG_DEFAULTS = {}
for fn in glob.glob(str(REPO / "exploration/stellarator_e2e/generated/inputs/*.json")):
    d = json.load(open(fn))
    def _walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, (int, float)) and k.startswith(P):
                    PKG_DEFAULTS[k] = float(v)
                elif isinstance(v, dict) and ("value" in v or "default_value" in v) and k.startswith(P):
                    PKG_DEFAULTS[k] = v.get("value", v.get("default_value"))
                _walk(v)
    _walk(d)


def rederive(inputs, outputs):
    """The verdict from the published bindings: a channel from the case's outputs, an
    input from the proposal or -- when the proposal did not set it -- the package's own
    parameter default (the WI-045 note: a threshold that is not a study lever)."""
    def val(b):
        if b["kind"] == "channel":
            return outputs[b["key"]]
        return inputs[b["key"]] if b["key"] in inputs else PKG_DEFAULTS[b["key"]]
    return "satisfied" if val(bindings["q_target_peak_in"]) <= val(bindings["q_target_limit_in"]) else "violated"

summary = {}
for name, r in zip(names, res):
    o = r["outputs"]; row = {"state": r["state"]}
    row.update({k.rsplit("__", 1)[1]: o.get(k) for k in NEW})
    row["lcoe"] = o.get(f"{P}lcoe_calc__lcoe"); row["verdicts"] = r["verdicts"]
    try:
        ev = oe.evaluate(r["inputs"])
        row["oracle_reldev"] = {k.split("__", 2)[2]: abs(ev[k] - o[k]) / (abs(o[k]) or 1.0) for k in NEW if k in ev and o.get(k) is not None}
        row["oracle_reldev_max"] = max(row["oracle_reldev"].values()) if row["oracle_reldev"] else None
        row["oracle_error"] = None
    except Exception as err:  # the declared invalid at E
        row["oracle_reldev"] = None; row["oracle_reldev_max"] = None
        row["oracle_error"] = f"{type(err).__name__}: {err}"
    if r["state"] == "completed":
        row["divertor_heat_ok_rederived"] = rederive(r["inputs"], o)
        pkg = None
        for v in (r["verdicts"] or []):
            ident = v.get("constraint_id", v.get("source_local_identity", "")) if isinstance(v, dict) else (getattr(v, "constraint_id", None) or getattr(v, "source_local_identity", "") or str(v))
            if "divertor_heat_ok" in str(ident):
                pkg = v.get("status") if isinstance(v, dict) else getattr(v, "status", None)
                pkg = getattr(pkg, "value", pkg)
        row["divertor_heat_ok_package"] = str(pkg) if pkg is not None else None
    summary[name] = row
    print(name, r["state"], "q_peak", row.get("q_target_peak"), "shadow", row.get("q_target_peak_area_scaled"), "tbr_req", row.get("tbr_required"), "oracle_max", row.get("oracle_reldev_max"), "oracle_error", row.get("oracle_error"), "rederived", row.get("divertor_heat_ok_rederived"), "pkg", row.get("divertor_heat_ok_package"))

# Hand check at E (c3343, p_fus 11075.912578921578 committed): the loop margin is positive at 14
# loops, so the complex value the seam surfaced is NOT the loop's domain -- it is the CAS10 land
# term's sqrt(p_net) on a negative net power (the pre-existing WI-034 class the study's
# pre-screen already records as "oracle p_net <= 0").
_pf = 11075.912578921578; _pa = (3.52 / 17.58) * _pf; _q = 1.2 * (_pf - _pa) + _pa + 50.0
_md = _q * 1.0e6 / (5193.0 * 200.0)
hand = {}
for nl in (14.0, 7.0):
    _ml = _md / nl; _dp = 329187.1856931558 * (_ml / 225.07777777777778) ** 2
    hand[f"n_loops_{int(nl)}"] = {"q_source_MW": _q, "mdot_loop": _ml, "dp_loop_Pa": _dp, "p_loop_margin_Pa": 8.0e6 - _dp}
print("hand loop margins at E:", hand)
cmp = {"hand_loop_margin_at_E": hand}
for name, key in (("P3_c2823_14loops", "P3_c2823"), ("P4_c3598_14loops", "P4_c3598_highest_heating_feasible")):
    pr = pred[key]; got = summary[name]
    checks = {"p_heat_abs": (got["p_heat_abs"], pr["p_heat_abs"]), "p_target_nonrad": (got["p_target_nonrad"], pr["p_target_nonrad"]),
              "q_target_peak": (got["q_target_peak"], pr["q_target_peak_pessimistic"]), "q_target_peak_area_scaled": (got["q_target_peak_area_scaled"], pr["q_target_peak_area_scaled"]),
              "burn_rate": (got["burn_rate"], pr["fuel"]["burn_rate"]), "inject_rate": (got["inject_rate"], pr["fuel"]["inject_rate"]),
              "tbr_required": (got["tbr_required"], pr["fuel"]["tbr_required"]), "burn_kg_per_fpy": (got["burn_kg_per_fpy"], pr["fuel"]["burn_kg_per_fpy"]),
              "Q_total": (got["Q_total"], pr["vacuum"]["Q_total"]), "S_eff_required": (got["S_eff_required"], pr["vacuum"]["S_eff_required"])}
    cmp[name] = {k: {"executed": a, "predicted": b, "reldev": abs(a - b) / (abs(b) or 1.0)} for k, (a, b) in checks.items()}
    cmp[name]["p_sep_positive"] = got["p_sep"] > 0
    print(name, "max reldev vs prediction", max(x["reldev"] for k, x in cmp[name].items() if isinstance(x, dict)), "p_sep", got["p_sep"], "f_rad_edge", got["f_rad_edge"])
low = summary["P0_low_case_q_ref_5"]
cmp["P0_low_case"] = {"q_target_peak": {"executed": low["q_target_peak"], "predicted": pred["P0_design_point"]["divheat_low_case"]["q_target_peak"]}, "verdict": low.get("divertor_heat_ok_package")}
(WI / "evidence/offdesign_points/summary.json").write_text(json.dumps({"summary": summary, "vs_predictions": cmp}, indent=1, default=str))
# the source case
sc = vs.reconstruct_divertor_source_case()
(WI / "evidence/source_case").mkdir(exist_ok=True)
(WI / "evidence/source_case/results.json").write_text(json.dumps({"oracle": sc, "exact": {"p_target_nonrad": sc["p_target_nonrad"] == 50.0, "q_peak": sc["q_peak"] == 9.5, "q_peak_low": sc["q_peak_low"] == 5.0, "doubled": sc["q_peak_doubled"] == 19.0},
    "t_recycle_threshold": pred["t_recycle_transect"]["threshold"], "identity_1p19": pred["t_recycle_transect"]["identity_1p19"]}, indent=1))
print("source case", sc)
print("done")
