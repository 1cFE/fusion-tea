"""Exact same-scope diagnostics and regression node attribution."""
import collections,json,re,xml.etree.ElementTree as ET
from pathlib import Path
HERE=Path(__file__).resolve().parent
old=json.loads((HERE.parents[1]/'WI-055_winding-pack-input-domain/evidence/candidate-validation.json').read_text());new=json.loads((HERE/'canonical-validation.json').read_text())
rows=[]
for a,b in zip(old,new,strict=True):
 row={'level':b['level'],'before_success':a['success'],'after_success':b['success']}
 for key in ('issues','warnings'):
  norm=lambda xs:collections.Counter(re.sub(r'(\.sysml):\d+',r'\1:<line>',str(x)) for x in xs)
  aa,bb=norm(a[key]),norm(b[key]);row['new_'+key]=list((bb-aa).elements());row['removed_'+key]=list((aa-bb).elements());row['count_'+key]=sum(bb.values())
  assert aa==bb,(b['level'],key,row)
 rows.append(row)
(HERE/'validation-attribution.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows)
