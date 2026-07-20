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
# Inject the CAS27 pass-through design input (a declared plain attribute, harness-supplied).
for f in Path("generated/inputs").glob("*.json"):
    d = json.loads(f.read_text())
    hit = [k for k in d if k.endswith("direct_capital__special_materials_capital")]
    if hit:
        for k in hit: d[k] = special
        f.write_text(json.dumps(d, indent=2)); print(f"[inject] special_materials_capital={special:,.2f} into {f.name}")

schema_names = dict.fromkeys(["RootModel[float]"] + [t.__name__ for t in CUSTOM_SCHEMA_TYPES])
router = create_output_router_with_json_schemas(list(schema_names))
router.register_handler("float", WriteHandler(fn=lambda v,p: Path(p).write_text(json.dumps(v)), extension=".json"))
result = execute_pipeline(rs.PIPELINE, output_dir=rs.E2E/"outputs"/"single",
    registry=create_stellarator_tea_registry(), output_router=router, custom_schema_types=CUSTOM_SCHEMA_TYPES)
out = result.outputs
b = {c:(float(v.root) if hasattr(v,'root') else float(v)) for c,v in out.items() if hasattr(v,'root') or isinstance(v,(int,float))}
P, CH = rs.P, rs.CH
total = b[f"{P}total_capital__total_capital"]; magnet = b[CH["magnet"]]
anchors = [("total capital $",total,12_638_857_665.74),("LCOE $/MWh",b[CH["lcoe"]],203.647152),
    ("p_net MW",b[CH["p_net"]],915.081088),("q_eng",b[CH["q_eng"]],6.606662),
    ("rec_frac",b[CH["rec_frac"]],0.151362),("magnet %",magnet/total*100,50.03)]
print("\n=== SIX ANCHORS (single-pass, graph rollup, no bridge) ===")
allok=True
for name,val,exp in anchors:
    # Recorded anchors are truncated to their printed precision; the authoritative
    # gate is BIT-EXACT vs oracle below. Here compare at the recorded precision.
    ok = (abs(val-exp)<0.01) if name=="magnet %" else (abs(round(val,6)-exp)<=1e-6 or abs(val-exp)/abs(exp)<1e-6)
    allok &= ok
    print(f"  {name:16s} exec={val:20.6f}  expect={exp:<18}  {'OK' if ok else '*** DEVIATION'}")
print(f"  magnet capital $ = {magnet:,.2f}")
print("=== FIVE VERDICTS ===")
for c,v in out.items():
    if c.endswith('__evaluation') and hasattr(v,'status'):
        print(f"  {c.split('__')[2]:14s} {v.status}")
print("ANCHORS", "GREEN" if allok else "*** STOP — DEVIATION ***")

# --- Bit-exact oracle comparison (WI-027 standard: rel dev < 1e-9) ---
print("\n=== BIT-EXACT vs ORACLE (rel<1e-9) ===")
omap = {"total_capital":total, "lcoe":b[CH["lcoe"]], "p_net":b[CH["p_net"]],
        "q_eng":b[CH["q_eng"]], "rec_frac":b[CH["rec_frac"]], "direct_capital":b[f"{P}direct_capital__direct_capital"]}
bit=True
for k,val in omap.items():
    exp=o[k]; rd=abs(val-exp)/(abs(exp) or 1); ok=rd<1e-9; bit&=ok
    print(f"  {k:16s} exec={val:20.9f} oracle={exp:20.9f} reldev={rd:.2e} {'OK' if ok else 'FAIL'}")
print("BIT-EXACT vs oracle:", "PASS" if bit else "*** FAIL ***")
