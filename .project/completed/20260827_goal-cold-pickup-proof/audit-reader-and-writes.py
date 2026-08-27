"""Auditor's checks: (a) run 13's four answers, (b) writes attempted by cold sessions."""
import json, glob, os

def events(path):
    for line in open(path):
        line = line.strip()
        if line:
            try:
                yield json.loads(line)
            except Exception:
                pass

def tool_calls(path):
    out = []
    for ev in events(path):
        def walk(o):
            if isinstance(o, dict):
                if o.get("type") == "tool_use":
                    out.append((o.get("name"), json.dumps(o.get("input", {}))))
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(ev)
    return out

base = ".project/active/goal-cold-pickup-proof/sessions"

print("=== run 13 reader: writes attempted ===")
r13 = tool_calls(f"{base}/13-reader/transcript.jsonl")
writes = [(n, i) for n, i in r13
          if n in ("Write", "Edit", "NotebookEdit")
          or (n == "Bash" and (" > " in i or ">>" in i or "git commit" in i))]
print(f"  write-ish tool calls: {len(writes)}")
for n, i in writes[:5]:
    print(f"   {n}: {i[:200]}")

print("\n=== run 13 reader: final assistant message ===")
last = ""
for ev in events(f"{base}/13-reader/transcript.jsonl"):
    if ev.get("type") == "result" and isinstance(ev.get("result"), str):
        last = ev["result"]
    elif ev.get("type") == "assistant":
        for b in ev.get("message", {}).get("content", []):
            if b.get("type") == "text":
                last = b["text"]
print(last[:5000])

print("\n=== every session dir vs freshness rows ===")
for d in sorted(os.listdir(base)):
    js = sorted(os.path.basename(p) for p in glob.glob(f"{base}/{d}/*.jsonl"))
    print(f"  {d}: {js}")
