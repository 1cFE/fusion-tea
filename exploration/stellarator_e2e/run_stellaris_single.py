"""Single-pass stellarator runner (Item 10 cutover) — NO bridge, NO two-pass rollup glue.

The cross-part capital rollup (powercore/bop/direct/total_capital) is now compiled by codegen
as instance-scoped aggregation producers, so a single teax-simkit pass computes it in the graph.
glue-1 (patch_bop_wiring) is kept; glue-2 (the Python rollup + placeholder overwrite) is retired
with bridge_v11_generate.py. special_materials_capital (CAS27 pass-through, a declared plain
design input) is harness-supplied. Anchors verified bit-exact vs oracle (rel<1e-9); five verdicts
all satisfied.
"""
import sys, json
from pathlib import Path
sys.path.insert(0, "/home/reid/1cfe/teax/packages/teax-simkit")
sys.path.insert(0, ".")
import run_stellaris as rs
from verify_stellaris import compute as oracle_compute
from simkit.core.pipeline import execute_pipeline
from simkit.io.output_router import WriteHandler, create_output_router_with_json_schemas
from stellarator_tea import CUSTOM_SCHEMA_TYPES, create_stellarator_tea_registry

rs.patch_bop_wiring()  # glue-1 (kept); NO rollup glue-2, single pass
o = oracle_compute()
special = o["special_materials"]
# Inject the leaf design inputs surfaced as per-module entry points (WI-028: the
# rebuilt overnight assembly consumes special_materials_capital in both
# cas2x_pre_contingency and cas23_to_28_capital, and cas28_capital likewise;
# each surfaces as its own module-scoped entry point). CAS27 special materials is
# the harness-supplied pass-through; CAS28 digital twin is the 5.0 M$ constant.
CAS28_CAPITAL = 5_000_000.0  # costing_constants.yaml:229 (digital_twin 5.0 M$) x 1e6
for f in Path("generated/inputs").glob("*.json"):
    d = json.loads(f.read_text())
    changed = False
    for k in list(d):
        if k.endswith("__special_materials_capital"): d[k] = special; changed = True
        elif k.endswith("__cas28_capital"): d[k] = CAS28_CAPITAL; changed = True
    if changed:
        f.write_text(json.dumps(d, indent=2)); print(f"[inject] special_materials={special:,.2f}, cas28={CAS28_CAPITAL:,.2f} into {f.name}")

# CONSTRAINT-EXEC (WI-027 adapter 1): the generated CUSTOM_SCHEMA_TYPES already carry
# ConstraintEvaluation + ConstraintReport, so registering write handlers for every
# CUSTOM_SCHEMA_TYPES name registers the constraint exit-point handlers generically —
# no per-type hand wiring. Without them PipelineValidator would reject the constraint run.
schema_names = dict.fromkeys(["RootModel[float]"] + [t.__name__ for t in CUSTOM_SCHEMA_TYPES])
router = create_output_router_with_json_schemas(list(schema_names))
router.register_handler("float", WriteHandler(fn=lambda v,p: Path(p).write_text(json.dumps(v)), extension=".json"))
result = execute_pipeline(rs.PIPELINE, output_dir=rs.E2E/"outputs"/"single",
    registry=create_stellarator_tea_registry(), output_router=router, custom_schema_types=CUSTOM_SCHEMA_TYPES)
out = result.outputs
# CONSTRAINT-EXEC (WI-027 adapter 2): oracle-comparison map keeps ONLY scalar channels;
# the two non-scalar verdict channels (ConstraintEvaluation/ConstraintReport) are skipped,
# so MR-5.1 bit-exactness on numeric channels is exactly as it was — verdicts are not numbers.
b = {c:(float(v.root) if hasattr(v,'root') else float(v)) for c,v in out.items() if hasattr(v,'root') or isinstance(v,(int,float))}
P, CH = rs.P, rs.CH
total = b[f"{P}total_capital__total_capital"]; magnet = b[CH["magnet"]]
# WI-028 re-baseline (MR-WI028-9): total_capital/LCOE/magnet-share MOVE as the
# CAS22 tail + CAS40 + CAS50 accounts enter the overnight assembly; p_net/q_eng
# (physics spine) UNCHANGED. Authoritative gate is bit-exact vs oracle below.
anchors = [("total capital $",total,16_145_706_216.04),("LCOE $/MWh",b[CH["lcoe"]],258.013640),
    ("p_net MW",b[CH["p_net"]],915.081088),("q_eng",b[CH["q_eng"]],6.606662),
    ("rec_frac",b[CH["rec_frac"]],0.151362),("magnet %",magnet/total*100,39.165025)]
print("\n=== SIX ANCHORS (single-pass, graph rollup, no bridge) ===")
allok=True
for name,val,exp in anchors:
    # Recorded anchors are truncated to their printed precision; the authoritative
    # gate is BIT-EXACT vs oracle below. Here compare at the recorded precision.
    ok = (abs(val-exp)<0.01) if name=="magnet %" else (abs(round(val,6)-exp)<=1e-6 or abs(val-exp)/abs(exp)<1e-6)
    allok &= ok
    print(f"  {name:16s} exec={val:20.6f}  expect={exp:<18}  {'OK' if ok else '*** DEVIATION'}")
print(f"  magnet capital $ = {magnet:,.2f}")
# CONSTRAINT-EXEC (WI-027 adapter 3): harvest the generated ConstraintReport into the run
# report and assert verdict PARITY against the static expected set (design §Decision 6).
# This is a string-equality regression check on the model's own reported status — NOT a
# physics comparison: no operand-vs-bound test appears here (MR-WI027-2). The verdict source
# is the generated ConstraintReport; a non-satisfied verdict is a demo finding to surface
# (MR-WI027-4), never tuned away.
EXPECTED_VERDICTS = {  # design-point actuals table — all five satisfied, none on a boundary
    "beta_ok": "satisfied", "net_positive": "satisfied", "recirc_ok": "satisfied",
    "tbr_ok": "satisfied", "wall_load_ok": "satisfied",
}
report = out["constraint_report"]
print("=== FIVE VERDICTS (generated ConstraintReport) ===")
verdicts = {}
for c,v in out.items():
    if c.endswith('__evaluation') and hasattr(v,'status'):
        name = c.split("__")[2]
        verdicts[name] = v.status
        print(f"  {name:14s} {v.status}")
assert report.headline == "all_satisfied", f"headline {report.headline!r} != all_satisfied"
assert report.assessed_count == 5, f"assessed_count {report.assessed_count} != 5"
for name, exp in EXPECTED_VERDICTS.items():
    got = verdicts.get(name)
    assert got == exp, f"VERDICT PARITY FAIL: {name} = {got!r}, expected {exp!r} (surface per MR-WI027-4)"
print(f"VERDICT PARITY: PASS — headline={report.headline}, assessed_count={report.assessed_count}, all five == satisfied")
print("ANCHORS", "GREEN" if allok else "*** STOP — DEVIATION ***")

# --- Bit-exact oracle comparison (WI-027 standard: rel dev < 1e-9) ---
print("\n=== BIT-EXACT vs ORACLE (rel<1e-9) ===")
omap = {"total_capital":total, "lcoe":b[CH["lcoe"]], "p_net":b[CH["p_net"]],
        "q_eng":b[CH["q_eng"]], "rec_frac":b[CH["rec_frac"]],
        "cas20_capital":b[f"{P}cas20_capital__cas20_capital"],
        "overnight_capital":b[f"{P}overnight_capital__overnight_capital"]}
bit=True
for k,val in omap.items():
    exp=o[k]; rd=abs(val-exp)/(abs(exp) or 1); ok=rd<1e-9; bit&=ok
    print(f"  {k:16s} exec={val:20.9f} oracle={exp:20.9f} reldev={rd:.2e} {'OK' if ok else 'FAIL'}")
print("BIT-EXACT vs oracle:", "PASS" if bit else "*** FAIL ***")
