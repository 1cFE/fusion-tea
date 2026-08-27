"""Auditor's independent transcript-fence sweep (Required Invariant 2).

Sweeps tool-call INPUTS (not raw text) in every kept session transcript for
references to the item directory, orchestrator logs, or the external log dir.
"""
import json, glob, re

PATTERNS = [
    r"goal-cold-pickup-proof",
    r"\.orchestrate-logs",
    r"goal-proof-logs",
]
rx = re.compile("|".join(PATTERNS))

files = sorted(glob.glob(
    ".project/active/goal-cold-pickup-proof/sessions/*/*.jsonl"))
hits = 0


def walk(o, f, lineno):
    global hits
    if isinstance(o, dict):
        if o.get("type") == "tool_use":
            s = json.dumps(o.get("input", {}))
            if rx.search(s):
                hits += 1
                print(f"HIT {f}:{lineno} tool={o.get('name')}")
                print("   " + s[:700])
        for v in o.values():
            walk(v, f, lineno)
    elif isinstance(o, list):
        for v in o:
            walk(v, f, lineno)


for f in files:
    for lineno, line in enumerate(open(f), 1):
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        walk(ev, f, lineno)

print(f"\nTOTAL TOOL-INPUT HITS: {hits} across {len(files)} transcripts")
