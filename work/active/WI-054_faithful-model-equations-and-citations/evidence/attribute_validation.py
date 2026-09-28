"""Compare full issue identities to the audited WI-053 candidate, ignoring only line shifts."""
import collections
import json
import re
from pathlib import Path
HERE=Path(__file__).resolve().parent
before=json.loads((HERE.parents[1]/'WI-053_magnet-and-cryogenic-input-domains/evidence/candidate-validation.json').read_text())
after=json.loads((HERE/'validation.json').read_text())
rows=[]
for old,new in zip(before,after,strict=True):
    result={'level':new['level'],'before_success':old['success'],'after_success':new['success']}
    for key in ('issues','warnings'):
        normalize=lambda values:collections.Counter(re.sub(r'(\.sysml):\d+',r'\1:<line>',v) for v in values)
        a,b=normalize(old[key]),normalize(new[key])
        result['new_'+key]=list((b-a).elements());result['removed_'+key]=list((a-b).elements())
        result['count_'+key]=sum(b.values())
        assert a==b,(new['level'],key,result)
    rows.append(result)
(HERE/'validation-attribution.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows)
