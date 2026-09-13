"""Identity attribution against the unchanged audited WI-054 all-level evidence."""
import collections,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
before=json.loads((HERE.parents[1]/'WI-054_faithful-model-equations-and-citations/evidence/validation.json').read_text())
after=json.loads((HERE/'candidate-validation.json').read_text())
rows=[]
for old,new in zip(before,after,strict=True):
 row={'level':new['level'],'before_success':old['success'],'after_success':new['success']}
 for key in ('issues','warnings'):
  normalize=lambda xs:collections.Counter(re.sub(r'(\.sysml):\d+',r'\1:<line>',v) for v in xs)
  a,b=normalize(old[key]),normalize(new[key])
  row['new_'+key]=list((b-a).elements());row['removed_'+key]=list((a-b).elements());row['count_'+key]=sum(b.values())
  assert a==b,(new['level'],key,row)
 rows.append(row)
(HERE/'validation-attribution.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows)
