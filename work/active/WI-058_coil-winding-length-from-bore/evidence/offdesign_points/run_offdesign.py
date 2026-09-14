"""WI-058 MR-WI058-5: execute P1-P5 through the study route, compare the winding chain to the
predictions of record (prototype/proto_results.json), check the R-invariance to the double, and
compare every listed channel to the oracle seam."""
import json, shutil, sys
from pathlib import Path
sys.path.insert(0, "exploration/stellarator_e2e/studies"); sys.path.insert(0, "exploration/stellarator_e2e")
import study_route as sr, oracle_entry as oe
P = "stellarator_09__stellaris__"
E = Path("work/active/WI-058_coil-winding-length-from-bore"); out = E / "evidence/offdesign_points"
pred = json.loads((E / "prototype/proto_results.json").read_text())
PTS = {"P0_design": (12.7, 1.3), "P1_a1.4": (12.7, 1.4), "P2_a2.2": (12.7, 2.2), "P3_R15.7_a1.3": (15.7, 1.3),
       "P4_R15.7_a2.2": (15.7, 2.2), "P5_R11.43_a1.3": (11.43, 1.3)}
props = {k: sr.proposal_for(R, a, 0.0) for k, (R, a) in PTS.items()}
cases, db = sr.run_points("wi058-offdesign-v1", list(props.values()), out / "_work")
cases = sr._completed(cases, "off-design points")
CHAIN = ["magnet__coil_length__c_coil", "magnet__wp_volume__vol_winding_pack", "magnet__wp_volume__vol_cold_total",
         "magnet__winding_procurement__conductor_length", "magnet__winding_procurement__tape_cost",
         "magnet__winding_procurement__winding_fabrication_cost", "magnet__material_inventory__material_cost",
         "magnet__winding_procurement__cost", "magnet__winding_pack_cost__cost", "magnet__magnet_capital_rollup__capital_cost",
         "cryoplant__cryo_elec__p_elec", "cryoplant__aux_cooling__cryo_cost", "pb__p_net", "pb__rec_frac", "lcoe_calc__lcoe",
         "total_capital__total_capital"]
UNMOVED = ["magnet__peak_field_calc__B_peak", "magnet__wp_stress__sigma_wp", "magnet__cond_strain__eps_cond",
           "magnet__stored_energy__W_mag", "magnet__casing_mass__m_casing", "pb__p_th", "rb__r_coil_centre"]
def rel(a, b): return abs(a - b) / max(abs(b), 1e-300)
results = {}; byname = {}
for case in cases:
    inp = case.inputs
    name = next(k for k, v in props.items() if all(abs(inp[kk] - vv) < 1e-12 * max(1, abs(vv)) for kk, vv in v.items()))
    ch = {k: float(v) for k, v in case.outputs.items()}; byname[name] = ch
    verdicts = sr.short_verdicts(case)
    pr = pred[name]
    pred_cmp = {}
    for k in CHAIN + UNMOVED:
        if k in pr and isinstance(pr[k], dict) and "new" in pr[k]:
            pred_cmp[k] = {"executed": ch[P + k], "predicted": pr[k]["new"], "reldev": rel(ch[P + k], pr[k]["new"])}
    oc = oe.evaluate(props[name]); ocmp = {}
    for k in CHAIN + UNMOVED:
        if P + k in oc:
            ocmp[k] = {"package": ch[P + k], "oracle": oc[P + k], "reldev": rel(ch[P + k], oc[P + k])}
    results[name] = {"case_id": case.candidate_id, "inputs": props[name], "verdicts": verdicts,
                     "vs_prediction": pred_cmp, "vs_oracle": ocmp, "all_channels": ch}
    print(name, case.candidate_id, "| violated:", [k for k, v in verdicts.items() if v != "satisfied"] or "none")
    print("   pred max reldev %.3e (%d ch) | oracle max reldev %.3e (%d ch) | c_coil %r | procurement %r | p_cryo %r | lcoe %r" % (
        max(v["reldev"] for v in pred_cmp.values()), len(pred_cmp), max(v["reldev"] for v in ocmp.values()), len(ocmp),
        ch[P + "magnet__coil_length__c_coil"], ch[P + "magnet__winding_procurement__cost"], ch[P + "cryoplant__cryo_elec__p_elec"], ch[P + "lcoe_calc__lcoe"]))
# R-invariance to the double: P3 and P5 equal P0 on the winding chain
inv = {}
for nm in ("P3_R15.7_a1.3", "P5_R11.43_a1.3"):
    inv[nm] = {k: (byname["P0_design"][P + k] == byname[nm][P + k]) for k in CHAIN[:9]}
    print(nm, "R-invariance on the winding chain:", all(inv[nm].values()), {k: v for k, v in inv[nm].items() if not v})
results["_R_invariance"] = inv
(out / "results.json").write_text(json.dumps(results, indent=2, default=str))
shutil.rmtree(out / "_work", ignore_errors=True); print("deposited", out / "results.json")
