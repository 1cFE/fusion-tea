from pathlib import Path
from collections import Counter
from dataclasses import asdict
import json
from agentic_mbse.validation.level6_architecture import validate_architecture
root=Path(__file__).resolve().parent
result=validate_architecture('exploration/ife_e2e/models')
rows=[{k:str(getattr(x,k)) if k=="location" else getattr(x,k) for k in ("code","element_name","message","location")} for x in result.structured_issues]
(root/'l6-current.json').write_text(json.dumps(rows,indent=2,default=str)+'\n')
before=json.loads(Path('work/active/WI-049_ife-zero-discount-repair/implementation/l6-before.json').read_text())
def key(x): return (x['code'],x['element_name'],x['message'],str(x['location']).rsplit(':',1)[0])
a=Counter(map(key,before)); b=Counter(map(key,rows))
assert a==b
print('L6 matched by file, element, rule, message:',len(rows),'retained; 0 new; 0 resolved')
