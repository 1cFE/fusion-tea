"""Compare strict-runner receipts with every independent scalar and predicate."""
from pathlib import Path
import argparse,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from exploration.whole_plant_conversion import verify
p=argparse.ArgumentParser();p.add_argument('receipts',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
data=json.loads(a.receipts.read_text());rows=data['cases'] if isinstance(data,dict) else data
result={}
for row in rows:
 name=row.get('case',row.get('candidate_id','unnamed'))
 try:
  r=verify.verify_row(row)
  if r['status']=='refused':
   try:verify.evaluate(row.get('inputs',row.get('effective_inputs',{})))
   except (ValueError,ZeroDivisionError) as e:r.update(status='consistent_refusal',oracle_error=str(e))
   else:r.update(status='fail',reason='native refused inputs for which independent equations evaluated',native_error=r['reason'])
 except Exception as e:r=dict(status='verification_refused',error=repr(e))
 result[name]=r
 print(name,r['status'],r.get('comparisons',0),r.get('predicates',0),r.get('differences',r.get('error','')))
record=dict(receipts=str(a.receipts),receipts_sha256=hashlib.sha256(a.receipts.read_bytes()).hexdigest(),results=result)
a.out.write_text(json.dumps(record,indent=2)+'\n')
raise SystemExit(any(r['status'] not in ('pass','consistent_refusal') for r in result.values()))
