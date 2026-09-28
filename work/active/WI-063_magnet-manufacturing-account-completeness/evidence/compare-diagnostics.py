from pathlib import Path
from collections import Counter
import json,re
from agentic_mbse.validation.level6_architecture import validate_architecture
HERE=Path(__file__).resolve().parent
enter=Path('work/active/WI-062_absolute-conductor-current-margin/evidence/L6-candidate.json')
a=json.loads(enter.read_text())
result=validate_architecture('exploration/stellarator_e2e/models')
b={'success':result.success,'metrics':result.metrics,'issues':result.issues}
(HERE/'L6-candidate.json').write_text(json.dumps(b,indent=2)+'\n')
def normalized(row): return Counter(re.sub(r' at file:.*','',x) for x in row['issues'])
x,y=normalized(a),normalized(b)
out={'entering_evidence':str(enter),'entering_count':len(a['issues']),'candidate_count':len(b['issues']), 'added':list((y-x).elements()),'removed':list((x-y).elements()),'normalization':'diagnostic identity excludes source line suffix; entering source is the unchanged WI062 production model before this item'}
(HERE/'L6-delta.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
