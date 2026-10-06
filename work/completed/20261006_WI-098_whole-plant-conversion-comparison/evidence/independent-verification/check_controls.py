"""Incremental independent verification of immutable completed replay batches."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from exploration.whole_plant_conversion import verify
IN=HERE.parent/'conversion-controls/native';OUT=HERE/'controls';OUT.mkdir(exist_ok=True)
files=[*sorted((ROOT/'exploration/whole_plant_conversion').glob('oracle*')),ROOT/'exploration/whole_plant_conversion/verify.py',ROOT/'models/designs/whole_plant_conversion/plant.sysml',verify.PACKAGE/'pipelines/pipeline.yaml']
identity=hashlib.sha256(b''.join(p.read_bytes() for p in files if p.is_file())).hexdigest()
counts={};failures=[]
for path in sorted(IN.glob('batch-*/cases.json')):
 batch=path.parent.name;rows=json.loads(path.read_text())['cases'];wanted=23 if batch=='batch-19' else 25
 if len(rows)!=wanted:continue
 sha=hashlib.sha256(path.read_bytes()).hexdigest();out=OUT/(batch+'.json')
 prior=json.loads(out.read_text()) if out.exists() else {}
 if prior.get('receipts_sha256')==sha and prior.get('oracle_identity')==identity:
  record=prior
 else:
  results={}
  for row in rows:
   try:
    r=verify.verify_row(row)
    if r['status']=='refused':
     try:verify.evaluate(row['inputs'])
     except (ValueError,ZeroDivisionError) as e:r.update(status='consistent_refusal',oracle_error=str(e))
     else:r.update(status='fail',reason='unexplained native refusal')
   except Exception as e:r=dict(status='verification_refused',error=repr(e))
   results[row['case']]=r
  assert len(results)==len(rows),'duplicate case names'
  record=dict(receipts=str(path),receipts_sha256=sha,oracle_identity=identity,results=results)
  out.write_text(json.dumps(record,indent=2)+'\n')
 for name,r in record['results'].items():
  counts[r['status']]=counts.get(r['status'],0)+1
  if r['status'] not in ['pass','consistent_refusal']:failures.append(dict(case=name,batch=batch,result=r))
 print(batch,len(record['results']),flush=True)
summary=dict(status='pass' if sum(counts.values())==498 and not failures else 'incomplete' if not failures else 'fail',counts=counts,checked_cases=sum(counts.values()),failures=failures,oracle_identity=identity)
(HERE/'controls-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
raise SystemExit(bool(failures))
