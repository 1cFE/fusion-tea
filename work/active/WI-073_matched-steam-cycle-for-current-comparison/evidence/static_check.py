"""Compare issue identities to audited WI-070, retaining full native diagnostics."""
import json,re
from collections import Counter
from pathlib import Path
from agentic_mbse.validation.level2_structure import validate_structure
from agentic_mbse.validation.level6_architecture import validate_architecture
HERE=Path(__file__).resolve().parent
prior=json.loads((HERE.parents[1]/'WI-071_shared-fabrication-rate-for-estimate-uncertainty/evidence/static-delta.json').read_text())
normalize=lambda x:re.sub(r' at file:.*$', '',x)
report={}
for level,fn in [('2',validate_structure),('6',validate_architecture)]:
 r=fn(str(Path.cwd()/'exploration/stellarator_e2e/models'))
 before=Counter(map(normalize,prior[level]['issues']));after=Counter(map(normalize,r.issues))
 report[level]=dict(success=r.success,metrics=r.metrics,issues=r.issues,added=list((after-before).elements()),removed=list((before-after).elements()))
(HERE/'static-delta.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
print({k:{'success':v['success'],'total':len(v['issues']),'added':v['added'],'removed':v['removed']} for k,v in report.items()})
