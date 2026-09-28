"""Execute exact baseline, gate it, then run the fixed list through stock native lifecycle."""
import csv,json,sys,time,subprocess
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study import preflight,verify
from simkit.study.store import StudyStore
H=Path(__file__).resolve().parents[1];R=H/'results';sys.path.insert(0,str(H));import study
read=lambda p:json.loads(p.read_text())
def write(n,x):(R/n).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def key(p):return json.dumps(dict(p),sort_keys=True)
assert (H/'reviews/preexecution-check.md').exists()
assert read(R/'oracle-scan.json')['rows']
contract=read(H/'preparation/package-contracts/model_contract.json')
required=sorted(o['channel_name'] for o in contract['outputs'] if o['python_type'] in ('float','int'))
(H/'preparation/required-channels.json').write_text(json.dumps(required,indent=2)+'\n')
print('required native numeric channels',len(required),flush=True)
route.execute_baseline(R)
pre=preflight.run_gates(route.PACKAGE_DIR,route.MANIFEST_PATH,H/'axes.json',R/'package_identity.json',R/'baseline_result.json');write('preflight_results.json',pre);assert pre['outcome']=='pass',pre
release=read(H/'preparation/integration-return.json')['candidate']; identity=read(R/'package_identity.json');assert identity['identity']['digest']==release['executable_fingerprint']
write('execution-clean-before.json',preflight.run_clean(route.PACKAGE_DIR))
started=datetime.now(timezone.utc).isoformat();t=time.monotonic()
print('baseline/preflight passed; beginning',len(study.proposals()),'native cases',flush=True)
cases,db=study.run();assert all(c.state=='completed' for c in cases)
write('execution-summary.json',{'started_at_utc':started,'finished_at_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'cases':len(cases),'states':dict(Counter(c.state for c in cases)),'store':str(db.relative_to(H)),'repo_revision':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()})
bykey={key(c.inputs):c for c in cases}; ur=read(H/'preparation/unique-proposals.json'); byid={r['proposal_id']:bykey[key(r['point'])] for r in ur};catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR)
complete=[]
for r in ur:
 c=byid[r['proposal_id']]; assert set(c.verdicts)==set(catalog); values=route.required_outputs(c,study.channels())
 complete.append({'proposal_id':r['proposal_id'],'candidate_id':c.candidate_id,'inputs':dict(c.inputs),'outputs':dict(c.outputs),'verdicts':dict(c.verdicts),'headline':c.headline,'state':c.state})
write('native-cases.json',complete);write('predicate-catalog.json',catalog)
rows=[]
for p in read(H/'preparation/proposals.json'):
 c=byid[p['canonical_proposal_id']]; row={'arm_id':'arm-native','block':p['arm'],'proposal_id':p['id'],'canonical_proposal_id':p['canonical_proposal_id'],'candidate_id':c.candidate_id,'point_json':key(p['point']),**route.required_outputs(c,study.channels()),**dict(c.verdicts),'full_satisfied':all(v=='satisfied' for v in c.verdicts.values())}; rows.append(row)
with (R/'points.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
s=StudyStore(db)
try:write('store-compatibility.json',verify.compatibility_digest(s)[1])
finally:s.close()
# Retain the complete entry-model map as the actual stock loader uses it.
prepared=route.prepare(route.PACKAGE_DIR,R/'entry-model-inspection')
write('entry-models.json',{k:{'module':v.__module__,'qualname':v.__qualname__,'schema':v.model_json_schema()} for k,v in prepared.entry_models.items()})
post=preflight.run_clean(route.PACKAGE_DIR);write('post-run-clean.json',post);assert post['outcome']=='pass'
print('EXECUTE COMPLETE',len(cases),'native cases;',len(rows),'coordinate-joined report rows',flush=True)
