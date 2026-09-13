"""Independently compare same-scope diagnostics and original failed test identity."""
from collections import Counter
import json,re,xml.etree.ElementTree as ET
from pathlib import Path
R=Path.cwd();E=R/'work/active/WI-056_primary-loop-heat-capacity-domain/evidence';O=Path(__file__).parent
old=json.loads((R/'work/active/WI-055_winding-pack-input-domain/evidence/candidate-validation.json').read_text());new=json.loads((E/'canonical-validation.json').read_text())
rows=[]
for a,b in zip(old,new,strict=True):
 assert a['level']==b['level'] and a['success']==b['success']
 for key in ('issues','warnings'):
  norm=lambda v:Counter(re.sub(r'\.sysml:\d+', '.sysml:<line>',str(s)) for s in v)
  assert norm(a[key])==norm(b[key])
 rows.append({'level':b['level'],'success':b['success'],'issues':len(b['issues'])})
def nodes(p):
 return {n.attrib['classname']+'::'+n.attrib['name']: 'failed' if n.find('failure') is not None or n.find('error') is not None else 'skipped' if n.find('skipped') is not None else 'passed' for n in ET.parse(p).iter('testcase')}
a=nodes(R/'work/active/WI-055_winding-pack-input-domain/evidence/candidate-models.xml');b=nodes(E/'models.xml')
changed={k:(a[k],b.get(k)) for k in a if a[k]!=b.get(k)}
assert changed=={'tests.models.test_mfe_operating_heating::test_operating_heat_complete_cost_operand_classification':('passed','failed')},changed
assert {k for k,v in a.items() if v=='skipped'}=={k for k,v in b.items() if v=='skipped'}
retry=nodes(R/'.project/active/primary-loop-current-consumers/implementation/heating-source-retry.xml')
assert all(retry.get(k)=='passed' for k in changed)
(O/'attribution.json').write_text(json.dumps({'same_scope_canonical_levels':rows,'original_model_suite':dict(Counter(b.values())),'changed_existing_nodes':changed,'targeted_retry':retry,'inherited_skips':13},indent=2)+'\n')
print('PASS exact same-scope diagnostics and original failure to targeted retry attribution')
