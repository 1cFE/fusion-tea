import importlib.util,json
from collections import Counter
from pathlib import Path
I=Path('work/active/WI-052_mfe-financial-rate-limits/implementation')
spec=importlib.util.spec_from_file_location('diffs',I/'differentials.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
result={}
for surface in ('canonical','mirror','family'):
    a=json.loads((I/f'entering/issues-{surface}.json').read_text());b=json.loads((I/f'issues-{surface}.json').read_text())
    assert [x['level'] for x in a]==[1,2,3,4,5,6]==[x['level'] for x in b]
    result[surface]=[]
    for x,y in zip(a,b):
        old=Counter(map(m.identity,x['issues']));new=Counter(map(m.identity,y['issues']))
        assert old==new
        assert x['warnings']==y['warnings']
        result[surface].append({'level':x['level'],'matched_issue_count':sum(old.values()),'success':y['success']})
print(json.dumps(result,indent=2))
