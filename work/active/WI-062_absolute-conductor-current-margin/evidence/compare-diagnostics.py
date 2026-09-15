from pathlib import Path
from collections import Counter
import json,re
from agentic_mbse.validation.level6_architecture import validate_architecture
HERE=Path(__file__).resolve().parent
rows={}
for name,path in [('entering','/tmp/wi062-entering-models'),('candidate','exploration/stellarator_e2e/models')]:
 result=validate_architecture(path)
 rows[name]={'success':result.success,'metrics':result.metrics,'issues':result.issues}
 (HERE/('L6-'+name+'.json')).write_text(json.dumps(rows[name],indent=2)+'\n')
def normalized(row):
 return Counter(re.sub(r' at file:.*','',x) for x in row['issues'])
a,b=map(normalized,(rows['entering'],rows['candidate']))
out={'added':list((b-a).elements()),'removed':list((a-b).elements()),'normalization':'compare diagnostic text excluding path and line suffix; preserve full raw issues separately'}
(HERE/'L6-delta.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
