"""WI-057 swap demonstration (design D9): materialize a scratch copy of the committed model twin and package,
add the variant magnet definition and its formula, retype the instance, regenerate, execute at two markups.
usage: swap_demo.py <scratch_dir> <out_dir>   (run from the repo root with the seam environment exported)"""
import json, re, shutil, subprocess, sys
from pathlib import Path
REPO = Path("/home/reid/1cfe/fusion-tea"); scratch = Path(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
if scratch.exists(): shutil.rmtree(scratch)
(scratch / "pkg").mkdir(parents=True)
shutil.copytree(REPO / "exploration/stellarator_e2e/models", scratch / "models")
shutil.copytree(REPO / "exploration/stellarator_e2e/generated", scratch / "pkg/stellarator_tea", ignore=shutil.ignore_patterns("__pycache__"))
models = scratch / "models"
(models / "analyses/mfe_magnet_cost_variants.sysml").write_text("""package mfe_magnet_cost_variants {
    private import ScalarValues::*;
    // WI-057 swap demonstration only: a formula stand-in, not a sourced cost model.
    calc def 'Magnet Structure Cost NI' {
        in n_coils : Real;
        in m_casing : Real;
        in steel_price : Real;
        in f_steel_fab : Real;
        in f_ins : Real;
        return cost : Real = n_coils * m_casing * steel_price * f_steel_fab * (1.0 + f_ins);
    }
}
""")
core = models / "cost_structure/mfe_power_core.sysml"; s = core.read_text()
s = s.replace("    private import mfe_magnet_cost::*;\n", "    private import mfe_magnet_cost::*;\n    private import mfe_magnet_cost_variants::*;\n", 1)
variant = """    // WI-057 swap demonstration: a non-insulated HTS variant of the magnet system. Same interface,
    // one added coil-set fact, its own casing-cost formula bound to the structure_cost seam.
    part def 'NI HTS Magnet System' :> 'Magnet System' {
        attribute t_charge_h : Real;
        attribute f_ins_markup : Real default 0.0;
        calc magnet_structure_cost_ni : 'Magnet Structure Cost NI' {
            in n_coils = coil.n_coils;
            in m_casing = casing.m_casing;
            in steel_price = casing.steel_price;
            in f_steel_fab = casing.f_steel_fab;
            in f_ins = f_ins_markup;
        }
        :>> structure_cost = magnet_structure_cost_ni.cost;
    }
"""
anchor = "    part def 'Heating and CD'"; assert anchor in s; core.write_text(s.replace(anchor, variant + anchor, 1))
inst = models / "designs/stellarator_09/stellarator_plant.sysml"; t = inst.read_text()
if "private import mfe_power_core::*;" not in t: t = t.replace("    private import mfe_plant::*;\n", "    private import mfe_plant::*;\n    private import mfe_power_core::*;\n", 1)
assert t.count("        part :>> magnet {\n") == 1
t = t.replace("        part :>> magnet {\n", "        part :>> magnet : 'NI HTS Magnet System' {\n            :>> t_charge_h = 600.0;   // the source's 25-day charge (swap demonstration; no calc reads it)\n            :>> f_ins_markup = 0.0;\n", 1)
inst.write_text(t)
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "exploration/stellarator_e2e/studies"))
def run(markup):
    tt = inst.read_text(); tt = re.sub(r":>> f_ins_markup = [0-9.]+;", f":>> f_ins_markup = {markup};", tt); inst.write_text(tt)
    done = subprocess.run(["uv", "run", "sysml-codegen", "generate", "--models", str(models), "--output", str(scratch / "pkg/stellarator_tea"), "--package-name", "stellarator_tea", "--overwrite", "--smart-regen", "--preserve-handwritten"], capture_output=True, text=True, cwd=str(REPO))
    assert done.returncode == 0, done.stderr[-2000:]
    # each markup executes in its own process: the generated schema modules carry the parameter
    # defaults as Python constants and stay cached in sys.modules otherwise
    import study_route as sr
    pt = sr._baseline_point(REPO / "exploration/stellarator_e2e/studies/manifest.json")
    work = scratch / f"work_{markup}"; shutil.rmtree(work, ignore_errors=True)
    (scratch / "point.json").write_text(json.dumps(pt)); result_path = scratch / f"result_{markup}.json"
    ex = subprocess.run([sys.executable, str(REPO / "work/active/WI-057_stellaris-structural-decomposition/prototype/scripts/proto_baseline.py"), str(scratch / "pkg/stellarator_tea"), str(work), str(scratch / "point.json"), str(result_path)], capture_output=True, text=True, cwd=str(REPO))
    assert ex.returncode == 0, ex.stderr[-2000:]
    r = json.loads(result_path.read_text())
    res = {"markup": markup, "channels": r["channels"], "verdicts": r["verdicts"], "executable_fingerprint": r["executable_fingerprint"],
           "stencils": re.search(r"Stencils - (.*)", done.stdout + done.stderr).group(1) if re.search(r"Stencils - (.*)", done.stdout + done.stderr) else None}
    (out / f"result_markup_{markup}.json").write_text(json.dumps(res, indent=1)); return res
r0 = run("0.0"); r1 = run("0.1")
P = "stellarator_09__stellaris__"
# optional argv[3], argv[4]: the entering baseline and the ledger to compare against (2026-09-13 re-application: evidence/merge_onto_demo_maturation/)
base = json.loads(Path(sys.argv[3] if len(sys.argv) > 3 else REPO / "work/active/WI-057_stellaris-structural-decomposition/evidence/baseline_before/baseline_result.json").read_text())["channels"]
L = json.loads(Path(sys.argv[4] if len(sys.argv) > 4 else REPO / "work/active/WI-057_stellaris-structural-decomposition/evidence/commit_B/ledger.json").read_text())["outputs"]
base_mapped = {L.get(k, k): v for k, v in base.items()}
eq0 = [k for k in base_mapped if k in r0["channels"] and base_mapped[k] != r0["channels"][k]]
summary = {"markup_0_channels_differing_from_entering_pin": eq0, "markup_0_verdicts": r0["verdicts"], "channels_moving_at_0.1": sorted(k for k in r0["channels"] if r0["channels"][k] != r1["channels"].get(k)),
           "structure_cost_ni": (r0["channels"].get(P + "magnet__magnet_structure_cost_ni__cost"), r1["channels"].get(P + "magnet__magnet_structure_cost_ni__cost")),
           "structure_cost_base_dormant": (r0["channels"].get(P + "magnet__magnet_structure_cost__cost"), r1["channels"].get(P + "magnet__magnet_structure_cost__cost")),
           "magnet_capital": (r0["channels"].get(P + "magnet__magnet_capital_rollup__capital_cost"), r1["channels"].get(P + "magnet__magnet_capital_rollup__capital_cost")),
           "lcoe": (r0["channels"].get(P + "lcoe_calc__lcoe"), r1["channels"].get(P + "lcoe_calc__lcoe")), "stencils": r0["stencils"]}
(out / "summary.json").write_text(json.dumps(summary, indent=1)); print(json.dumps(summary, indent=1)[:1500])
