"""Predict (or verify) the WI-057 rename ledger from the entering contract, the attribute home map and the calc host map.

usage: predict_ledger.py <contract_before.json> <attribute_homes.json> <calc_hosts.json> <stage A|B> <out.json> [<contract_after.json>]
With a contract_after, every predicted name is checked against it and every after-name against the prediction.
"""
import json, sys
from pathlib import Path
cb = json.loads(Path(sys.argv[1]).read_text()); homes = json.loads(Path(sys.argv[2]).read_text())
hosts = json.loads(Path(sys.argv[3]).read_text()); stage = sys.argv[4]; out = Path(sys.argv[5])
after = json.loads(Path(sys.argv[6]).read_text()) if len(sys.argv) > 6 else None
P = "stellarator_09__stellaris__"
home_of = {a: (k if not k.startswith("plant") else "") for k, v in homes.items() if not k.startswith("_") for a in v}
# magnet-owned names today live under magnet__; map to their sub-part path
host_of = {c: (k if k != "plant" else "") for k, v in hosts.items() if not k.startswith("_") for c in v}
calc_names = set(host_of)
def predict(qn):
    if not qn.startswith(P): return qn
    rest = qn[len(P):]; segs = rest.split("__")
    if len(segs) == 1:  # plant-level design attribute
        h = home_of.get(segs[0], "")
        return P + (h.replace(".", "__") + "__" if h else "") + segs[0]
    if segs[0] == "magnet" and len(segs) == 2 and segs[1] in home_of:  # magnet attribute -> sub-part
        h = home_of[segs[1]]; return P + h.replace(".", "__") + "__" + segs[1]
    if segs[0] in calc_names and stage == "B":  # calc-formal parameter or calc output channel
        h = host_of[segs[0]]; return P + (h.replace(".", "__") + "__" if h else "") + rest
    return qn
params = {p["qualified_name"]: predict(p["qualified_name"]) for p in cb["parameters"]}
outputs = {o["channel_name"]: predict(o["channel_name"]) for o in cb["outputs"]}
ledger = {"stage": stage, "parameters": params, "outputs": outputs,
          "moved_parameters": sum(1 for k, v in params.items() if k != v), "moved_outputs": sum(1 for k, v in outputs.items() if k != v)}
print(f"stage {stage}: parameters {len(params)} ({ledger['moved_parameters']} renamed); outputs {len(outputs)} ({ledger['moved_outputs']} renamed)")
if after:
    pa = {p["qualified_name"] for p in after["parameters"]}; oa = {o["channel_name"] for o in after["outputs"]}
    miss_p = sorted(v for v in params.values() if v not in pa); new_p = sorted(pa - set(params.values()))
    miss_o = sorted(v for v in outputs.values() if v not in oa); new_o = sorted(oa - set(outputs.values()))
    ledger["verification"] = {"predicted_parameters_missing": miss_p, "parameters_unpredicted": new_p, "predicted_outputs_missing": miss_o, "outputs_unpredicted": new_o}
    print(f"  verification: predicted params missing {len(miss_p)}; unpredicted params {len(new_p)}; predicted outputs missing {len(miss_o)}; unpredicted outputs {len(new_o)}")
    for x in (miss_p[:8] + new_p[:8] + miss_o[:8] + new_o[:8]): print("   ", x)
out.write_text(json.dumps(ledger, indent=1, sort_keys=True))
