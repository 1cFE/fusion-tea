"""WI-044 MR-WI044-8: execute P1-P3 through the study route, compare to the predictions,
to the WI-043 pin's values at the same coordinates, and to the oracle seam."""
import csv, json, shutil, sys
from pathlib import Path
sys.path.insert(0, "exploration/stellarator_e2e/studies"); sys.path.insert(0, "exploration/stellarator_e2e")
import study_route as sr, oracle_entry as oe
P = "stellarator_09__stellaris__"
HELD = {"availability": 0.85, "discount_rate": 0.07, "j_wp": 118.8271604938272, "eta_source_heat": 0.50,
        "eta_couple_heat": 1.0, "p_delivered_direct_heat": 0.0, "p_coupled_direct_heat": 0.0, "tau_ratio_ash": 8.0}
def point(R, a, I, ne, T, wallplug):
    return {f"{P}R": R, f"{P}magnet__R0": R, f"{P}a": a, f"{P}availability": HELD["availability"],
            f"{P}discount_rate": HELD["discount_rate"], f"{P}magnet__j_wp": HELD["j_wp"], f"{P}T_i0": T,
            f"{P}magnet__I_coil": I, f"{P}n_e0": ne, f"{P}p_wallplug_heat": wallplug,
            f"{P}eta_source_heat": HELD["eta_source_heat"], f"{P}eta_couple_heat": HELD["eta_couple_heat"],
            f"{P}p_delivered_direct_heat": HELD["p_delivered_direct_heat"],
            f"{P}p_coupled_direct_heat": HELD["p_coupled_direct_heat"], f"{P}tau_ratio_ash": HELD["tau_ratio_ash"]}
PTS = {"P1_design_a1.4": point(12.7, 1.4, 15.4e6, 5.06e20, 14.63, 100.0),
       "P2_design_a2.2": point(12.7, 2.2, 15.4e6, 5.06e20, 14.63, 100.0),
       "P3_c2823": point(15.7, 2.2, 13.0e6, 5.06e20, 13.0, 100.0)}
E = Path("work/active/WI-044_magnet-chain-sees-coil-bore/evidence"); out = E / "offdesign_points"
pred = json.loads((E.parent / "prototype/proto_results.json").read_text())["points"]
cases, db = sr.run_points("wi044-offdesign-v1", list(PTS.values()), out / "_work")
cases = sr._completed(cases, "off-design points")
MAG = {"B_peak": "peak_field_calc__B_peak", "sigma_wp": "wp_stress__sigma_wp", "eps_cond": "cond_strain__eps_cond",
       "W_mag": "stored_energy__W_mag", "m_casing": "casing_mass__m_casing", "structure_cost": "magnet_structure_cost__cost",
       "aspect_ratio": "geom__A", "a_coil": "rb__r_coil_centre"}
OC = oe.ORACLE_OUTPUT_TO_CHANNEL
PHYS = {"lcoe": OC["lcoe"][len(P):], "p_fus": OC["p_fus"][len(P):], "wall_load_peak": OC["wall_load_peak"][len(P):],
        "beta": OC["beta"][len(P):], "B_axis": OC["B_axis"][len(P):], "total_capital": OC["total_capital"][len(P):],
        "cas72": OC["cas72_annual"][len(P):], "magnet_capital": OC["magnet_capital_rollup"][len(P):],
        "plasma_volume": OC["V"][len(P):], "vol_cold": None, "heating_capital": OC["heating"][len(P):]}
# reference values at the WI-043 pin: the probe (design column) and the committed record (c2823)
probe = {r["a"]: r for r in csv.DictReader(open("work/orchestration/goals/minor-radius/evidence/grounding_probe/probe_a_results.csv")) if r["column"] == "baseline_100MW"}
com = None
for r in csv.DictReader(open("exploration/stellarator_e2e/studies/20260907-burn-control/results/points.csv")):
    if r["case_id"] == "c2823" or (abs(float(r["R"]) - 15.7) < 1e-9 and abs(float(r["a"]) - 2.2) < 1e-9 and abs(float(r["I_coil_A"]) - 13e6) < 1 and abs(float(r["T_i0_keV"]) - 13.0) < 1e-9 and abs(float(r["n_e0"]) - 5.06e20) < 1e12 and float(r["p_wallplug_heat_MW"]) == 100.0 and float(r["eta_source_heat"]) == 0.5):
        com = r; break
REF = {"P1_design_a1.4": probe["1.4"], "P2_design_a2.2": probe["2.2"], "P3_c2823": com}
REFKEYS = {"P1_design_a1.4": dict(lcoe="lcoe", p_fus="p_fus", wall_load_peak="wall_load_peak", beta="beta", B_axis="B_axis", total_capital="total_capital", cas72="cas72", magnet_capital="magnet_capital", plasma_volume="plasma_volume", vol_cold="vol_cold", heating_capital="heating_capital", B_peak="B_peak", sigma_wp="sigma_wp", eps_cond="eps_cond")}
REFKEYS["P2_design_a2.2"] = REFKEYS["P1_design_a1.4"]
REFKEYS["P3_c2823"] = dict(lcoe="lcoe", p_fus="p_fus", wall_load_peak="wall_load_peak", beta="beta", B_axis="B_axis", total_capital="total_capital", cas72="cas72", magnet_capital="magnet_capital", plasma_volume="plasma_volume", vol_cold="vol_cold", heating_capital="heating_capital", B_peak="B_peak", sigma_wp="sigma_wp", eps_cond="eps_cond")
def rel(a, b): return abs(a - b) / max(abs(b), 1e-300)
results = {}
for case in cases:
    inp = case.inputs; name = next(k for k, v in PTS.items() if all(abs(inp[kk] - vv) < 1e-9 * max(1, abs(vv)) for kk, vv in v.items()))
    ch = {k: float(v) for k, v in case.outputs.items()}
    verdicts = sr.short_verdicts(case)
    mag = {k: ch[P + v] for k, v in MAG.items()}
    pr = pred[name]
    pred_cmp = {k: {"executed": mag[k], "predicted": pr[k], "reldev": rel(mag[k], pr[k])} for k in ("B_peak", "sigma_wp", "eps_cond", "W_mag", "m_casing", "structure_cost", "aspect_ratio", "a_coil")}
    PHYS["vol_cold"] = next(k for k in ch if k.endswith("vol_cold_total"))[len(P):]
    ref = REF[name]; refcmp = {}
    for k, rk in REFKEYS[name].items():
        if ref is not None and rk in ref and ref[rk] not in ("", None):
            refcmp[k] = {"executed": ch[P + PHYS.get(k, MAG.get(k))], "pin": float(ref[rk]), "reldev": rel(ch[P + PHYS.get(k, MAG.get(k))], float(ref[rk]))}
    # oracle seam
    oc = oe.evaluate(PTS[name]); ocmp = {}
    for k, key in (("B_peak", MAG["B_peak"]), ("W_mag", MAG["W_mag"]), ("m_casing", MAG["m_casing"]), ("magnet_structure", MAG["structure_cost"]), ("sigma_wp", MAG["sigma_wp"]), ("eps_cond", MAG["eps_cond"]), ("A", MAG["aspect_ratio"]), ("r_coil_centre", MAG["a_coil"]), ("lcoe", PHYS["lcoe"])):
        ocmp[k] = {"package": ch[P + key], "oracle": oc[P + key], "reldev": rel(ch[P + key], oc[P + key])}
    fences = {"peak_field_ok": "satisfied" if oc[P + MAG["B_peak"]] <= 24.9 else "violated",
              "wp_stress_ok": "satisfied" if oc[P + MAG["sigma_wp"]] <= 8.0e8 else "violated",
              "cond_strain_ok": "satisfied" if oc[P + MAG["eps_cond"]] <= 0.004 else "violated"}
    results[name] = {"case_id": case.candidate_id, "inputs": PTS[name], "verdicts": verdicts, "magnet_channels": mag,
                     "vs_prediction": pred_cmp, "vs_pin_reference": refcmp, "vs_oracle": ocmp,
                     "fences_rederived_from_oracle": fences, "fences_agree": all(verdicts[k] == v for k, v in fences.items()),
                     "all_channels": ch}
    print(name, case.candidate_id, "verdicts:", {k: v for k, v in verdicts.items() if v != "satisfied"} or "all satisfied")
    print("  pred max reldev", max(v["reldev"] for v in pred_cmp.values()), "| oracle max reldev", max(v["reldev"] for v in ocmp.values()), "| fences agree", results[name]["fences_agree"])
    for k, v in refcmp.items():
        flag = "SAME" if v["reldev"] < 1e-12 else f"moved {v['reldev']:.3e}"
        print(f"  {k:16s} exec={v['executed']:.10g} pin={v['pin']:.10g} {flag}")
(out / "results.json").write_text(json.dumps(results, indent=2, default=str))
shutil.rmtree(out / "_work", ignore_errors=True)
print("deposited", out / "results.json")
