import json,re
from pathlib import Path
from collections import Counter
from agentic_mbse.validation.level2_structure import validate_structure
from agentic_mbse.validation.level6_architecture import validate_architecture
here=Path(__file__).parent
old=json.loads(Path('work/active/WI-071_shared-fabrication-rate-for-estimate-uncertainty/evidence/static-delta.json').read_text())
norm=lambda s:re.sub(r' at file:.*$', '',s)
out={}
for k,fn in [('2',validate_structure),('6',validate_architecture)]:
 r=fn(str(Path('exploration/stellarator_e2e/models').resolve()));before=Counter(map(norm,old[k]['issues']));after=Counter(map(norm,r.issues))
 out[k]={'success':r.success,'metrics':r.metrics,'issues':r.issues,'added':list((after-before).elements()),'removed':list((before-after).elements())}
(here/'static-delta.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print({k:{'success':v['success'],'total':len(v['issues']),'added':len(v['added']),'removed':len(v['removed'])} for k,v in out.items()})
