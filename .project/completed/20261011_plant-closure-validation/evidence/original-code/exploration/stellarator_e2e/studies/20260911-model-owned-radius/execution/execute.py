"""Run one native study; export complete evidence before verification."""
import json,sys,dataclasses
from pathlib import Path
from collections.abc import Mapping
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H))
import study
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study import preflight,verify
from simkit.study.store import StudyStore
from simkit.study.bridge import CandidateBridge
R=H/'results'
def write(p,x):p.write_text(json.dumps(x,indent=2,default=lambda x:dict(x) if isinstance(x,Mapping) else str(x))+'\n')
assert json.loads((R/'preflight.json').read_text())['outcome']=='pass'
assert (H/'preparation/window-freeze.json').exists()
cases,db=study.run()
write(R/'cases.json',[dataclasses.asdict(c) for c in cases])
write(R/'native-store-path.json',{'path':str(db.relative_to(H))})
assert len(cases)==len(study.proposals()) and all(c.state=='completed' for c in cases), 'Native execution failure: stop, retain store; do not publish successful points'
prepared=route.prepare(route.PACKAGE_DIR,R/'runtime-links')
bridge=CandidateBridge(prepared.entry_models)
write(R/'effective-inputs.json',[{'candidate_id':c.candidate_id,'proposal':dict(c.inputs),'groups':{k:v.model_dump(mode='json') for k,v in bridge.build(c.inputs).items()}} for c in cases])
rows=[]
for c in cases:
    values=route.required_outputs(c,study.channels())
    assert len(c.verdicts)==18
    rows.append({'arm_id':'radius','candidate_id':c.candidate_id,'R':c.inputs[route.P+'R'],**values,**route.short_verdicts(c),'feasible':all(s=='satisfied' for s in c.verdicts.values())})
route.write_csv(rows,R/'points.csv')
store=StudyStore(db)
try: write(R/'store-compatibility.json',verify.compatibility_digest(store)[1])
finally:store.close()
clean=preflight.run_clean(route.PACKAGE_DIR);write(R/'post-run-clean.json',clean);assert clean['outcome']=='pass'
print('Completed and exported',len(cases),'native cases; all 158 scalars and 18 authored verdicts; one store.')
