"""Independently scan the released candidate before choosing the bounded native list."""
import json
from pathlib import Path
from collections import Counter
from exploration.stellarator_e2e.studies import oracle_entry as oe, study_route as route
from scripts.study.verify import derive_verdict, package_input_values
H=Path(__file__).resolve().parents[1]; R=H/'results'; P=route.P
read=lambda p:json.loads(p.read_text())
def write(n,x):(R/n).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
params=package_input_values(route.PACKAGE_DIR); catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR); bindings=oe.operand_bindings()
rows=read(H/'preparation/unique-proposals.json'); out=[]
def evaluate(p):
 ch=oe.evaluate(p)
 vs={cid:('satisfied' if derive_verdict(cid,e,bindings,p,params,ch)[0] else 'violated') for cid,e in catalog.items()}
 return {'channels':ch,'verdicts':vs,'full_satisfied':all(v=='satisfied' for v in vs.values())}
if (R/'oracle-scan.json').exists():
 out=json.loads((R/'oracle-scan.json').read_text())['rows']
 assert [(r['proposal_id'],r['point']) for r in out]==[(r['proposal_id'],r['point']) for r in rows]
else:
 for row in rows: out.append(row|evaluate(row['point']))
write('oracle-scan.json',{'scope':'Candidate oracle scan only; no native execution','rows':out,'feasible':sum(r['full_satisfied'] for r in out)})
anchor=next(r for r in out if r['full_satisfied'] and r['point'][P+'magnet__winding_pack__j_wp']==params[P+'magnet__winding_pack__j_wp'])
axes=read(H/'axes.json')['groups']; edges=[]
for g in axes:
 k=g['keys'][0]['key']; vals=sorted({r['point'][k] for r in rows})
 for edge,v in [('low',vals[0]),('high',vals[-1])]:
  point=anchor['point']|{k:v}; result=evaluate(point)
  violated=[catalog[c]['source_local_identity'] for c,s in result['verdicts'].items() if s!='satisfied']
  edges.append({'axis':g['axis'],'edge':edge,'value':v,'point':point,'caught':bool(violated),'violated':violated,**result})
write('edge-scan.json',{'anchor_proposal_id':anchor['proposal_id'],'anchor_point':anchor['point'],'anchor_feasible':True,'edges':edges,'interpretation':'Caught means an existing predicate is violated at this sampled edge from a candidate-feasible anchor; not a located continuous boundary. Uncaught edges are retained for bounded sensitivity, not treated as optima.'})
print('scan',len(out),'unique cases;',sum(r['full_satisfied'] for r in out),'oracle-feasible; anchor',anchor['proposal_id'])
for e in edges: print(e['axis'],e['edge'],'caught' if e['caught'] else 'not caught',','.join(e['violated']))
