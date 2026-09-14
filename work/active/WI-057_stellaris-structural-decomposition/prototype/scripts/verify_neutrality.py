"""Compare two baseline executions through a verified ledger: every entering channel must map to an
after-channel with the same value; every verdict equal.
usage: verify_neutrality.py <before_result.json> <after_result.json> <ledger.json> <out.json>
"""
import json, sys
from pathlib import Path
b = json.loads(Path(sys.argv[1]).read_text()); a = json.loads(Path(sys.argv[2]).read_text()); L = json.loads(Path(sys.argv[3]).read_text())
omap = L["outputs"]
bc = {omap.get(k, k): v for k, v in b["channels"].items()}; ac = a["channels"]
missing = sorted(k for k in bc if k not in ac); extra = sorted(k for k in ac if k not in bc)
diffs = [(k, bc[k], ac[k]) for k in bc if k in ac and bc[k] != ac[k]]
vb = b["verdicts"] if isinstance(b["verdicts"], dict) else {v["source_local_identity"]: v["status"] for v in b["verdicts"]}
va = a["verdicts"] if isinstance(a["verdicts"], dict) else {v["source_local_identity"]: v["status"] for v in a["verdicts"]}
res = {"channels_before": len(bc), "channels_after": len(ac), "missing_after": missing, "new_after": extra,
       "differing": [{"channel": k, "before": x, "after": y} for k, x, y in diffs], "verdicts_equal": vb == va,
       "verdict_count": len(va), "lcoe_before": b["channels"].get("stellarator_09__stellaris__lcoe_calc__lcoe"), "lcoe_after": ac.get("stellarator_09__stellaris__lcoe_calc__lcoe")}
Path(sys.argv[4]).write_text(json.dumps(res, indent=1))
print(f"channels {len(bc)} -> {len(ac)}; missing {len(missing)}; new {len(extra)}; differing {len(diffs)}; verdicts equal {vb == va} ({len(va)}); LCOE {res['lcoe_before']} -> {res['lcoe_after']}")
for k, x, y in diffs[:10]: print("  DIFF", k, x, y)
for k in missing[:6]: print("  MISSING", k)
for k in extra[:6]: print("  NEW", k)
sys.exit(1 if (missing or diffs or vb != va) else 0)
