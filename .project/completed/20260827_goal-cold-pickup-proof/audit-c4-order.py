"""Auditor's independent check of Criterion 4's ordering claim.

Prints, in transcript order, every tool call in run 08b that (a) writes the
T-001 start line to the trail, or (b) mints WI-032 through the modelling PM.
Then counts `add-item` invocations in the resumer's transcript.
"""
import json

def tool_calls(path):
    out = []
    for lineno, line in enumerate(open(path), 1):
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue

        def walk(o):
            if isinstance(o, dict):
                if o.get("type") == "tool_use":
                    out.append((lineno, o.get("name"),
                                json.dumps(o.get("input", {}))))
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(ev)
    return out

base = ".project/active/goal-cold-pickup-proof/sessions"

print("=== run 08b (round agent): start-line writes vs WI-032 mint ===")
for lineno, name, inp in tool_calls(f"{base}/08-round-agent/transcript.jsonl"):
    is_start = "T-001 start" in inp
    is_mint = "add-item" in inp or "WI-032" in inp
    if is_start or is_mint:
        kind = "START-LINE" if is_start else "MINT/WI-032"
        print(f"  line {lineno:>4}  {kind:<11} tool={name}")
        print(f"      {inp[:260]}")

print("\n=== run 09 (resumer): add-item calls ===")
n = 0
for lineno, name, inp in tool_calls(f"{base}/09-resumer/transcript.jsonl"):
    if "add-item" in inp:
        n += 1
        print(f"  line {lineno} tool={name}: {inp[:300]}")
print(f"  add-item tool inputs in resumer: {n}")

print("\n=== run 10/11 add-item calls (for context) ===")
for sess in ("10-continuation", "11-gate-ruling"):
    m = sum(1 for _, _, inp in tool_calls(f"{base}/{sess}/transcript.jsonl")
            if "add-item" in inp)
    print(f"  {sess}: {m}")
