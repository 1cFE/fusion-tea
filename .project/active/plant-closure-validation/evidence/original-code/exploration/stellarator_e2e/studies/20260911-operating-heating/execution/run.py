import importlib.util,json,sqlite3,dataclasses
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study import preflight
from simkit.study.identity import mint_proposal_id
H=Path(__file__).resolve().parents[1];R=H/'results'
def write(name,x): (R/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
assert (R/'window-freeze.json').exists()
spec=importlib.util.spec_from_file_location('local_study',H/'study.py'); study=importlib.util.module_from_spec(spec);spec.loader.exec_module(study)
assert len(study.labelled_proposals())==15
cases,db=study.run_all(R/'_study')
write('raw-cases.json',[dataclasses.asdict(c) for c in cases])
assert all(c.state=='completed' for c in cases), 'Native failure preserved in raw cases/store; stop'
byid={c.candidate_id:c for c in cases}; catalog=route._export_catalog(route.PACKAGE_DIR)
conn=sqlite3.connect(db);conn.row_factory=sqlite3.Row
props={p['proposal_id']:dict(p) for p in conn.execute('select * from proposals')}
compat=dict(conn.execute('select * from compatibility').fetchone());conn.close()
rows=[]
for i,label in enumerate(study.labelled_proposals()):
 pid=mint_proposal_id(study.PROPOSAL['study_id'],i); persisted=props[pid]
 assert json.loads(persisted['raw_json'])==label['point']
 c=byid[persisted['candidate_id']]
 assert dict(c.inputs)==label['point'], (i,c.inputs,label['point'])
 values=route.required_outputs(c,study.CHANNELS)
 short=route._short_verdicts(c,catalog)
 rows.append({'proposal_index':i,'proposal_id':pid,'candidate_id':c.candidate_id,'arm_id':label['arm_id'],'label':label['label'],'inputs':dict(c.inputs),'values':values,'verdicts':dict(c.verdicts),'verdicts_by_local_identity':short,'feasible':all(v=='satisfied' for v in short.values())})
write('cases.json',rows);write('store-compatibility.json',compat);write('constraint-catalog.json',catalog)
route.write_csv([{'proposal_index':r['proposal_index'],'candidate_id':r['candidate_id'],'arm_id':r['arm_id'],'label':r['label'],**r['values'],**r['verdicts'],'feasible':r['feasible']} for r in rows],R/'points.csv')
clean=preflight.run_clean(route.PACKAGE_DIR);write('post-run-clean.json',clean);assert clean['outcome']=='pass'
print(json.dumps({'proposals':len(rows),'native_cases':len(cases),'feasible':sum(r['feasible'] for r in rows),'store':str(db)},indent=2))
