"""Finite staged independent-oracle scan. Does not execute native points or solve model equations."""
import json,time,sys
from pathlib import Path
from collections import Counter
from exploration.stellarator_e2e.studies import oracle_entry as oe,study_route as route
from scripts.study.verify import derive_verdict,package_input_values
H=Path(__file__).resolve().parents[1];R=H/'results';P=route.P
read=lambda p:json.loads(p.read_text())
params=package_input_values(route.PACKAGE_DIR);catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR);bindings=oe.operand_bindings()
def evaluate(row):
 try:
  point=row['point'];ch=oe.evaluate(point)
  vd={cid:'satisfied' if derive_verdict(cid,e,bindings,point,params,ch)[0] else 'violated' for cid,e in catalog.items()}
  margins={}
  for cid,e in catalog.items():
   result=derive_verdict(cid,e,bindings,point,params,ch)
   margins[e['source_local_identity']]=result[1]
  return row|{'outcome':'evaluated','channels':ch,'verdicts':vd,'resolved_operand_counts':margins,'violated':[catalog[c]['source_local_identity'] for c,v in vd.items() if v!='satisfied'],'full_satisfied':all(v=='satisfied' for v in vd.values())}
 except Exception as e:return row|{'outcome':'refused','error':repr(e),'full_satisfied':False}
if __name__=='__main__':
 assert read(R/'preflight_results.json')['outcome']=='pass'
 stage=sys.argv[1] if len(sys.argv)>1 else 'initial'
 proposals=H/'preparation'/('scan-proposals.json' if stage=='initial' else stage+'-proposals.json')
 t=time.monotonic();rows=[evaluate(r) for r in read(proposals)]
 (R/(stage+'-oracle-scan.json')).write_text(json.dumps({'rows':rows,'elapsed_seconds':time.monotonic()-t},indent=2,allow_nan=False)+'\n')
 print(stage,len(rows),'states',Counter(r['outcome'] for r in rows),'passes',sum(r['full_satisfied'] for r in rows))
 print('failures',Counter(v for r in rows for v in r.get('violated',[])))
 print('pass ids',[r['id'] for r in rows if r['full_satisfied']])
