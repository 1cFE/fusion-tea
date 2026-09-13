"""Attribute full-suite statuses; retain the original new consumer failure."""
import collections,json,xml.etree.ElementTree as ET
from pathlib import Path
HERE=Path(__file__).resolve().parent

def records(p):
 return {n.attrib['classname']+'::'+n.attrib['name']:('skipped' if n.find('skipped') is not None else 'failed' if n.find('failure') is not None or n.find('error') is not None else 'passed') for n in ET.parse(p).iter('testcase')}
old=records(HERE.parents[1]/'WI-055_winding-pack-input-domain/evidence/candidate-models.xml');new=records(HERE/'models.xml')
oldbad={k:v for k,v in old.items() if v!='passed'};newbad={k:v for k,v in new.items() if v!='passed'}
changed={k:{'before':old.get(k),'after':v} for k,v in new.items() if k in old and old[k]!=v}
assert len(changed)==1 and next(iter(changed)).endswith('test_operating_heat_complete_cost_operand_classification'),changed
assert {k:v for k,v in newbad.items() if k not in changed}==oldbad
added={k:v for k,v in new.items() if k not in old};assert len(added)==61 and all(v=='passed' for v in added.values())
assert not set(old)-set(new)
out={'before':dict(collections.Counter(old.values())),'full_suite':dict(collections.Counter(new.values())),'new_nodes':added,'inherited_nonpass':oldbad,'changed_existing_nodes':changed,'disposition':'Existing current-source freeze assertion requires separately owned T-046 migration; retain this failed run and join its focused correction evidence.'}
(HERE/'regression-attribution.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
