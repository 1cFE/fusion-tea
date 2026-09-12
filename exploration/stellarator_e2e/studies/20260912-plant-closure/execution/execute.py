"""Execute the frozen list through the stock lifecycle and export complete evidence."""
import csv,json,math,sys,time
from pathlib import Path
from collections import Counter
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study import preflight,verify
from simkit.study.store import StudyStore
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H));import study
R=H/'results'
def write(p,data):p.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def key(p):return json.dumps(dict(p),sort_keys=True,separators=(',',':'))
assert json.loads((H/'reviews/pre-execution-approval.json').read_text())['approved']
assert json.loads((R/'preflight.json').read_text())['outcome']=='pass'
start=time.time();print('Starting native lifecycle',len(study.proposals()),'unique proposals',flush=True)
cases,db=study.run()
print('Native lifecycle returned',len(cases),'cases in',time.time()-start,'seconds',flush=True)
failures=[{'candidate_id':c.candidate_id,'state':c.state,'inputs':dict(c.inputs)} for c in cases if c.state!='completed']
write(R/'execution-summary.json',{'cases':len(cases),'states':dict(Counter(c.state for c in cases)),'elapsed_seconds':time.time()-start,'failures':failures})
assert len(cases)==len(study.proposals())
if failures:raise RuntimeError('Native cases failed; store retained, publication stopped')
channels=study.channels();catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR)
fieldnames=['candidate_id',*channels,*catalog,'full_satisfied']
with (R/'native-points.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fieldnames,lineterminator='\n');w.writeheader()
 for c in cases:
  values=route.required_outputs(c,channels)
  assert set(c.verdicts)==set(catalog)
  w.writerow({'candidate_id':c.candidate_id,**values,**c.verdicts,'full_satisfied':all(v=='satisfied' for v in c.verdicts.values())})
write(R/'case-inputs.json',[{'candidate_id':c.candidate_id,'inputs':dict(c.inputs),'state':c.state} for c in cases])
by_key={key(c.inputs):c.candidate_id for c in cases}
correlation=json.loads((H/'preparation/correlation.json').read_text())
for row in correlation:
 if row['scan_status']=='eligible':row['candidate_id']=by_key[row['proposal_key']]
write(R/'correlation.json',correlation)
with (R/'native-points.csv').open() as f:
 exported={row['candidate_id']:row for row in csv.DictReader(f)}
with (R/'points.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['arm_id','label',*fieldnames],lineterminator='\n');w.writeheader()
 for row in correlation:
  if row['scan_status']=='eligible':w.writerow({'arm_id':row['arm_id'],'label':row['label'],**exported[row['candidate_id']]})
store=StudyStore(db)
try:write(R/'store-compatibility.json',verify.compatibility_digest(store)[1])
finally:store.close()
clean=preflight.run_clean(route.PACKAGE_DIR);write(R/'post-run-clean.json',clean);assert clean['outcome']=='pass'
write(R/'native-store-path.json',{'path':str(db.relative_to(H))})
print('Exported all 158 numeric channels and 18 qualified verdicts, one store.',flush=True)
