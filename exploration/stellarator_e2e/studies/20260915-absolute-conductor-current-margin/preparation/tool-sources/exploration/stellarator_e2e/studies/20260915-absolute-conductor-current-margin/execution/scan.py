"""Scan every released candidate and endpoints with the independent package oracle."""
import json,sys
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as oe,study_route as route
from scripts.study.verify import derive_verdict,package_input_values
H=Path(__file__).resolve().parents[1];R=H/'results'
def read(p):return json.loads(p.read_text())
def write(n,x):(R/n).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
release=read(H/'preparation/scan-release.json');assert release['authorized_by']=='coordinator'
for key in ['executable_fingerprint','semantic_fingerprint']:assert read(route.MANIFEST_PATH)['fingerprints']['recorded_provenance'][key]==release[key]
params=package_input_values(route.PACKAGE_DIR);catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR);bindings=oe.operand_bindings()
current=next(cid for cid,r in catalog.items() if r['source_local_identity']=='reference_conductor_current_ok')
def evaluate(point):
 channels=oe.evaluate(point)
 verdicts={cid:'satisfied' if derive_verdict(cid,e,bindings,point,params,channels)[0] else 'violated' for cid,e in catalog.items()}
 return {'channels':channels,'verdicts':verdicts,'feasible_19':all(v=='satisfied' for cid,v in verdicts.items() if cid!=current),'current_satisfied':verdicts[current]=='satisfied','full_satisfied':all(v=='satisfied' for v in verdicts.values())}
rows=read(H/'preparation/unique-proposals.json')
if '--edges-only' in sys.argv:
 out=read(R/'oracle-scan.json')['rows'];assert [(r['proposal_id'],r['point']) for r in out]==[(r['proposal_id'],r['point']) for r in rows]
else:
 out=[r|evaluate(r['point']) for r in rows]
if '--edges-only' not in sys.argv:write('oracle-scan.json',{'scope':'Final independent candidate oracle scan, not native execution','rows':out,'feasible_19':sum(r['feasible_19'] for r in out),'feasible_20':sum(r['full_satisfied'] for r in out)})
feasible=[r for r in out if r['full_satisfied']]
anchor=feasible[0] if feasible else out[0]
edges=[]
for g in read(H/'axes.json')['groups']:
 keys=[r['key'] for r in g['keys']];assert len(keys)==1
 key=keys[0];values=sorted({r['point'][key] for r in rows})
 for edge,value in [('low',values[0]),('high',values[-1])]:
  point=anchor['point']|{key:value}
  try:result=evaluate(point)
  except ValueError as error:
   if str(error)!='oracle conductor current: unsupported field':raise
   trace=error.__traceback__;fields=[]
   while trace is not None:
    if 'B_peak' in trace.tb_frame.f_locals:fields.append(trace.tb_frame.f_locals['B_peak'])
    trace=trace.tb_next
   assert fields and all(v==fields[0] for v in fields)
   edges.append({'axis':g['axis'],'edge':edge,'value':value,'point':point,'caught':None,'violated':[],'outcome':'unsupported_field_domain','actual_peak_field_T':fields[0],'supported_field_domain_T':[20,32],'error':str(error)});continue
  violated=[catalog[cid]['source_local_identity'] for cid,v in result['verdicts'].items() if v!='satisfied']
  edges.append({'axis':g['axis'],'edge':edge,'value':value,'point':point,'caught':bool(violated),'violated':violated,**result})
print('Endpoint unsupported-domain refusals',sum(e.get('outcome')=='unsupported_field_domain' for e in edges),flush=True)
write('edge-scan.json',{'anchor_proposal_id':anchor['proposal_id'],'anchor_point':anchor['point'],'anchor_feasible_20':anchor['full_satisfied'],'edges':edges,'interpretation':'Engineered sensitivity endpoints; caught denotes any violated predicate. No continuous boundary is located. Conditional orientation anchor, if feasible, does not establish nominal performance.'})
print('Scanned',len(out),'unique candidates;',len(feasible),'conditional all20 passes; anchor',anchor['proposal_id'])
