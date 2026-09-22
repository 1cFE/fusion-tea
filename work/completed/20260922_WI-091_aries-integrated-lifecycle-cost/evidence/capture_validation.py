"""Retain full scoped diagnostic identities omitted by CLI's five-issue display."""
import json,re
from dataclasses import asdict
from pathlib import Path
from collections import Counter
from agentic_mbse.validation import validate_structure,validate_architecture
here=Path(__file__).resolve().parent
results={str(n):asdict(fn('exploration/aries_integrated/input_models')) for n,fn in [(2,validate_structure),(6,validate_architecture)]}
(here/'validation-diagnostics.json').write_text(json.dumps(results,indent=2,default=str)+'\n')
old=json.loads(Path('work/completed/20260922_WI-090_aries-integrated-equipment-and-costs/evidence/validation-diagnostics.json').read_text())
normalize=lambda s:re.sub(r':\d+(?=\D|$)',':LINE',s)
comparison={}
for level in results:
    a=Counter(map(normalize,old[level]['issues']));b=Counter(map(normalize,results[level]['issues']))
    comparison[level]={'prior_count':sum(a.values()),'current_count':sum(b.values()),'added':list((b-a).elements()),'removed':list((a-b).elements()),'metrics':results[level]['metrics']}
(here/'validation-comparison.json').write_text(json.dumps(comparison,indent=2,default=str)+'\n')
