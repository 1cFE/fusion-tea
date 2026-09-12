import json,csv,sqlite3,shutil,importlib.util,hashlib
from pathlib import Path
S=Path('exploration/stellarator_e2e/studies/20260912-plant-closure');T=Path('/tmp/plant-prefix-verification');(T/'results').mkdir(parents=True,exist_ok=True);(T/'preparation').mkdir(exist_ok=True)
for name in ['package-inputs.json','constraint-catalog.json','baseline-native-evidence.json']:shutil.copyfile(S/'results'/name,T/'results'/name)
for name in ['required-channels.json','oracle-scan.json']:shutil.copyfile(S/'preparation'/name,T/'preparation'/name)
channels=json.loads((S/'preparation/required-channels.json').read_text());catalog=json.loads((T/'results/constraint-catalog.json').read_text())
db=S/'results/store'/f'{S.name}.db'
with sqlite3.connect('file:'+str(db)+'?mode=ro',uri=True) as c:cases=c.execute("select candidate_id,inputs_json,evidence_digest from cases where state='completed' order by commit_order").fetchall()
rows=[];inputs=[]
for cid,point,digest in cases:
 p=S/'results/store/artifacts'/f'{digest}.json';b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==digest;e=json.loads(b)
 rows.append({'candidate_id':cid,**{a:e['outputs'][k] for a,k in channels.items()},**{k:e['responses'][k] for k in catalog},'full_satisfied':all(e['responses'][k]=='satisfied' for k in catalog)})
 inputs.append({'candidate_id':cid,'inputs':json.loads(point)})
with (T/'results/native-points.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(T/'results/case-inputs.json').write_text(json.dumps(inputs))
spec=importlib.util.spec_from_file_location('v',str(S/'execution/verify-all.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.H=T;m.R=T/'results';m.main()
print('Read-only native prefix checked:',len(cases),'cases; final all-case verification remains required')
