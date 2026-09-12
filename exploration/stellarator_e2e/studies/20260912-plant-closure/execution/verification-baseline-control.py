import json,csv,shutil,sys,importlib.util
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as oracle
S=Path('exploration/stellarator_e2e/studies/20260912-plant-closure');T=Path('/tmp/plant-verifier-control');(T/'results').mkdir(parents=True,exist_ok=True);(T/'preparation').mkdir(exist_ok=True)
for name in ['package-inputs.json','constraint-catalog.json']:shutil.copyfile(S/'results'/name,T/'results'/name)
shutil.copyfile(S/'preparation/required-channels.json',T/'preparation/required-channels.json')
e=json.loads((S/'results/baseline-native-evidence.json').read_text());print('baseline evidence keys',list(e))
channels=json.loads((S/'preparation/required-channels.json').read_text());catalog=json.loads((T/'results/constraint-catalog.json').read_text())
print('output keys',list(e.get('outputs',{}))[:3])
row={'candidate_id':'preparatory-control',**{a:e['outputs'][k] for a,k in channels.items()},**{k:e['responses'][k] for k in catalog},'full_satisfied':False}
with (T/'results/native-points.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(row));w.writeheader();w.writerow(row)
(T/'results/case-inputs.json').write_text(json.dumps([{'candidate_id':'preparatory-control','inputs':{}}]))
(T/'preparation/oracle-scan.json').write_text(json.dumps([{'proposal_key':'{}','channels':oracle.evaluate({})}]))
spec=importlib.util.spec_from_file_location('v',str(S/'execution/verify-all.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.H=T;m.R=T/'results';m.main()
print('Preparatory baseline verifier control PASS; no native study case written')
