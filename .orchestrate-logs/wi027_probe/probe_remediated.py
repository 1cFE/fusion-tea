"""WI-027 remediation probe (2026-07-20): at the lifecycle-remediation candidate,
does the UN-MODIFIED staged stellarator tree (Phase-1 un-strips, ORIGINAL
literal-actual asserts, no D7 passthroughs, no bridge pre-fill) capture cleanly
with constraint lowering enabled, carrying all five constraint facts?

Expected if Items 2 (Gate A: literal actuals resolve, no passthrough) and
3 (Gate B: extension-time whole-graph coverage check deleted) hold on this tree:
capture SUCCEEDS, constraint_lowering_mode == "applied", five usages carried
(net_positive, recirc_ok, beta_ok, wall_load_ok, tbr_ok).

Old behavior for the record: Gate A abort ("unresolved actual 'beta'") without
D7; Gate B abort (uncovered capital-rollup params) with D7.
"""
import json
import shutil
import subprocess
from pathlib import Path

from sysml_codegen.snapshot.capture import capture_snapshot

WORKTREE = Path("/home/reid/1cfe/fusion-tea-stellarator-mbse-demo")
SRC = WORKTREE / "exploration/stellarator_e2e/models"
TREE = Path("/tmp/wi027_probe_remediated_models")
OUT = WORKTREE / ".orchestrate-logs/wi027_probe/probe_remediated.snapshot.json"

EXPECTED = {"net_positive", "recirc_ok", "beta_ok", "wall_load_ok", "tbr_ok"}

# Record the candidate commits the probe runs against.
for repo in ("sysml-codegen", "agentic-mbse", "teax"):
    h = subprocess.run(
        ["git", "-C", str(Path.home() / "1cfe" / repo), "log", "-1", "--format=%h %s"],
        capture_output=True, text=True,
    ).stdout.strip()
    print(f"candidate {repo}: {h}")

if TREE.exists():
    shutil.rmtree(TREE)
shutil.copytree(SRC, TREE)
print(f"tree: unmodified copy of {SRC}")

print("=== capture (constraint lowering enabled, default) ===")
try:
    out = capture_snapshot([TREE], OUT)
    print("capture SUCCEEDED ->", out)
    snap = json.loads(OUT.read_text())
    mode = snap.get("constraint_lowering_mode")
    cf = snap.get("constraint_facts")
    usages = cf.get("usages") if isinstance(cf, dict) else None
    print("constraint_lowering_mode:", mode)
    names = set()
    if usages is not None:
        print("num usages carried:", len(usages))
        for u in usages:
            nm = u.get("usage_name") or u.get("name") or str(u)[:80]
            # keep the short local name for the expected-set check
            names.add(str(nm).rsplit(".", 1)[-1].rsplit("__", 1)[-1])
            print("   usage:", nm)
    else:
        print("constraint_facts (raw, truncated):", json.dumps(cf)[:400])
    missing = EXPECTED - names
    extra = names - EXPECTED
    print("VERDICT:", "PASS — all five facts carried" if not missing else f"PARTIAL — missing {sorted(missing)}")
    if extra:
        print("extra (informational):", sorted(extra))
except Exception as e:
    print("capture FAILED:", type(e).__name__)
    print(str(e)[:800])
    print("VERDICT: FAIL")
