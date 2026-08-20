"""Does a deferred-lowering capture (lower_constraints_enabled=False) succeed AND
carry the five constraint facts? If yes, a bridge-force-lower flow is possible:
capture facts unlowered -> bridge fills the 3 capital-rollup placeholders ->
lower. If capture still fails, or facts are dropped, no in-scope flow exists.

Also re-run the default (True) capture on candidate A to capture the exact
error object for the record.
"""
import json
from pathlib import Path
from sysml_codegen.snapshot.capture import capture_snapshot

TREE = Path("/tmp/wi027_probeA_models")
OUT_DEFER = Path(".orchestrate-logs/wi027_probe/probeA_deferred.snapshot.json")

print("=== capture A with lower_constraints_enabled=False (deferred) ===")
try:
    out = capture_snapshot([TREE], OUT_DEFER, lower_constraints_enabled=False)
    print("capture SUCCEEDED ->", out)
    snap = json.loads(OUT_DEFER.read_text())
    cf = snap.get("constraint_facts")
    mode = snap.get("constraint_lowering_mode")
    # constraint_facts may serialize as dict with 'usages'
    usages = None
    if isinstance(cf, dict):
        usages = cf.get("usages")
    print("constraint_lowering_mode:", mode)
    print("constraint_facts type:", type(cf).__name__)
    if usages is not None:
        print("num usages carried:", len(usages))
        for u in usages:
            nm = u.get("usage_name") or u.get("name") or u
            print("   usage:", nm)
    else:
        print("constraint_facts (raw, truncated):", json.dumps(cf)[:400])
except Exception as e:
    print("capture FAILED:", type(e).__name__)
    print(str(e)[:600])
