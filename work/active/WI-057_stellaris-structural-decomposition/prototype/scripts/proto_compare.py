"""Compare a transformed package against the before-state: parameter ledger + channel diff.

usage: proto_compare.py <contract_before.json> <pkg_after_dir> <movemap.json> <before_result.json> <after_result.json> <out_dir>
"""
import json, sys
from pathlib import Path

cb = json.loads(Path(sys.argv[1]).read_text())
pkg = Path(sys.argv[2])
ca = json.loads((pkg / "contracts/model_contract.json").read_text())
movemap = json.loads(Path(sys.argv[3]).read_text())
before = json.loads(Path(sys.argv[4]).read_text())
after = json.loads(Path(sys.argv[5]).read_text())
out = Path(sys.argv[6]); out.mkdir(parents=True, exist_ok=True)

P = "stellarator_09__stellaris__"
def expected_new(old_qn):
    """Apply the move map to a parameter qualified name."""
    rest = old_qn[len(P):]
    segs = rest.split("__")
    name = segs[-1]
    owner = "__".join(segs[:-1])
    # calc-formal parameters (owner is a calc usage) keep their name; design attributes move
    calc_moves = movemap.get("__calcs__", {})
    if segs[0] in calc_moves:
        return P + calc_moves[segs[0]] + "__" + rest
    if name in movemap and (owner == "" or owner == "magnet") and not isinstance(movemap[name], dict):
        return P + movemap[name].replace(".", "__") + "__" + name
    return old_qn

pb = {p["qualified_name"]: p for p in cb["parameters"]}
pa = {p["qualified_name"]: p for p in ca["parameters"]}
ledger, unmatched, value_drift = [], [], []
for old, p in sorted(pb.items()):
    if old.startswith("__"): continue
    new = expected_new(old)
    if new in pa:
        ledger.append({"old": old, "new": new, "moved": new != old,
                       "default_before": p.get("default_value"), "default_after": pa[new].get("default_value")})
        if p.get("default_value") != pa[new].get("default_value"):
            value_drift.append((old, new, p.get("default_value"), pa[new].get("default_value")))
    else:
        unmatched.append(old)
new_only = sorted(set(pa) - {r["new"] for r in ledger})
(out / "ledger.json").write_text(json.dumps(ledger, indent=1))
print(f"parameters before {len(pb)} after {len(pa)}; mapped {len(ledger)} (moved {sum(r['moved'] for r in ledger)}); unmatched old {len(unmatched)}; new-only {len(new_only)}; default drift {len(value_drift)}")
for u in unmatched[:10]: print("  UNMATCHED", u)
for n in new_only[:10]: print("  NEW-ONLY", n)
for v in value_drift[:10]: print("  DRIFT", v)

ob = {expected_new(o["channel_name"]) for o in cb["outputs"]}; oa = {o["channel_name"] for o in ca["outputs"]}
print(f"outputs before {len(ob)} after {len(oa)}; lost {sorted(ob-oa)[:6]}; gained {sorted(oa-ob)[:6]}")

bc = {expected_new(k): v for k, v in before["channels"].items()}
ac = after["channels"]
common = sorted(set(bc) & set(ac))
diffs = [(k, bc[k], ac[k]) for k in common if bc[k] != ac[k]]
print(f"channels before {len(bc)} after {len(ac)} common {len(common)}; differing {len(diffs)}; missing-after {sorted(set(bc)-set(ac))[:6]}")
for k, x, y in diffs[:12]: print("  DIFF", k, x, y, f"rel={abs(y-x)/abs(x) if x else float('nan'):.3e}")
print("verdicts equal:", before["verdicts"] == after["verdicts"])
print("LCOE before/after:", bc.get(P+"lcoe_calc__lcoe"), ac.get(P+"lcoe_calc__lcoe"))
print("semantic fingerprint before/after:", cb["semantic_fingerprint"][:16], ca["semantic_fingerprint"][:16])
(out / "channel_diff.json").write_text(json.dumps({"differing": diffs, "missing_after": sorted(set(bc)-set(ac)), "new_after": sorted(set(ac)-set(bc))}, indent=1))
