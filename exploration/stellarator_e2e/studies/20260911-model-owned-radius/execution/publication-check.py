"""Check publication gates using copies of this record's actual case; no execution."""
import json,sys,copy,hashlib
from pathlib import Path
from types import SimpleNamespace
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H))
import study
from exploration.stellarator_e2e.studies import study_route as route
R=H/'results'
cases=json.loads((R/'cases.json').read_text());channels=study.channels();cat=json.loads((R/'constraint-catalog.json').read_text());before=hashlib.sha256((R/'points.csv').read_bytes()).hexdigest();checks=[]
def refuse(name,c,fn):
 try:fn(c)
 except route.RouteError as e: checks.append({'check':name,'outcome':'pass','error':str(e)})
 else:raise AssertionError(name+' did not refuse')
# These are synthetic damaged copies, never native proposals or stored cases.
for key in channels.values():
 for condition in ['absent','null','nonfinite']:
  c=SimpleNamespace(**copy.deepcopy(cases[0]))
  if condition=='absent':del c.outputs[key]
  else:c.outputs[key]=None if condition=='null' else float('inf')
  refuse(condition+':'+key,c,lambda c:route.required_outputs(c,channels))
for condition in ['missing','extra']:
 c=SimpleNamespace(**copy.deepcopy(cases[0]))
 if condition=='missing':c.verdicts.pop(next(iter(c.verdicts)))
 else:c.verdicts['not-authored']='satisfied'
 refuse('verdict-'+condition,c,lambda c:route._short_verdicts(c,cat))
c=SimpleNamespace(**copy.deepcopy(cases[0]));c.state='execution_failed'
refuse('execution-failed',c,lambda c:route._completed([c],'publication check'))
c=SimpleNamespace(**copy.deepcopy(cases[0]));c.outputs={k:0.0 for k in c.outputs}
assert set(route.required_outputs(c,channels).values())=={0.0};checks.append({'check':'zero-valued channels publish','outcome':'pass'})
assert before==hashlib.sha256((R/'points.csv').read_bytes()).hexdigest()
(R/'publication-check.json').write_text(json.dumps({'outcome':'pass','evidence_class':'Synthetic damaged copies of actual recorded data; no model execution, no proposal, no store mutation','checks':checks,'count':len(checks),'actual_points_csv_unchanged':True},indent=2)+'\n')
print(len(checks),'publication controls pass; no model/store execution; actual CSV unchanged')
