"""Re-key consumer files through a verified ledger: full qualified names, f"{P}<stem>" and P + "<stem>" short forms.
usage: rekey_consumers.py <ledger.json> <file>...   (prints replacements per file)"""
import json, re, sys
from pathlib import Path
L = json.loads(Path(sys.argv[1]).read_text()); P = "stellarator_09__stellaris__"
ren = {k: v for k, v in {**L["parameters"], **L["outputs"]}.items() if k != v}
full = sorted(ren.items(), key=lambda kv: -len(kv[0]))
short = sorted(((k[len(P):], v[len(P):]) for k, v in ren.items() if k.startswith(P)), key=lambda kv: -len(kv[0]))
for f in sys.argv[2:]:
    p = Path(f); s = p.read_text(); n = 0
    for old, new in full:
        s, k = re.subn(r"(?<![\w])" + re.escape(old) + r"(?![\w])", new, s); n += k
    for old, new in short:
        s, k = re.subn(r'(?<=\{P\})' + re.escape(old) + r'(?![\w])', new, s); n += k
        s, k2 = re.subn(r'(?<=P \+ ")' + re.escape(old) + r'(?=")', new, s); n += k2
    if n: p.write_text(s)
    print(f"{f}: {n}")
