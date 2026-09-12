"""Re-read inherited edges and freeze the explicitly correlated native list."""
import json,hashlib
from pathlib import Path
from collections import Counter
import scan
H=Path(__file__).resolve().parents[1];P=scan.P
read=lambda p:json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def main():
 rows=read(H/'preparation/correlation.json');results=read(H/'preparation/oracle-scan.json');by_key={r['proposal_key']:r for r in results}
 scan.CACHE.update({k:{a:v for a,v in r.items() if a not in ['proposal_key','inputs']} for k,r in by_key.items()})
 grouped={}
 for row in rows:
  if row['arm_id'] not in ['arm-window-fixed','arm-window-sized']:continue
  group=(row['arm_id'],row['historical_arm'],row['inputs'].get(P+'p_wallplug_heat',scan.D[P+'p_wallplug_heat']))
  grouped.setdefault(group,[]).append(row)
 edges=[];probes=[]
 for (arm,oldarm,power),group in sorted(grouped.items()):
  feasible=[r for r in group if r.get('scan_full_satisfied')]
  base={'arm_id':arm,'historical_arm':oldarm,'installed_power_MW':power,'fully_satisfied_scan_rows':len(feasible)}
  if not feasible:
   edges.append({**base,'status':'no full-current-predicate feasible anchor; no feasible boundary claim','edges':[]});continue
  anchor=min(feasible,key=lambda r:r['scan_lcoe']);report={**base,'anchor_label':anchor['label'],'anchor_inputs':anchor['inputs'],'edges':[]};edges.append(report)
  for suffix in ['R','a','magnet__I_coil','n_e0','T_i0','eta_source_heat','tau_ratio_ash']:
   k=P+suffix;values=sorted({r['inputs'].get(k,scan.D[k]) for r in group})
   for side,value in [('low',values[0]),('high',values[-1])]:
    point=scan.canonical({**anchor['inputs'],k:value});label=f'{arm}:{oldarm}:{power}:{suffix}:{side}'
    detail={'axis':k,'side':side,'value':value,'label':label,'window_provenance':'engineered inherited actual axis extent'}
    report['edges'].append(detail);probes.append((detail,{'arm_id':'arm-edge-diagnostics','label':label,'inputs':point,'parent_arm':arm,'historical_arm':oldarm}))
 # Complete the declared all-live sized witness where its fixed-loop factorial cannot run.
 anchors={r['anchor']:r for r in rows if r['arm_id']=='arm-closure-factorial' and r['modes']==[1,1,1] and r['scan_status']=='excluded'}
 for name,row in anchors.items():
  point,error=scan.sized(row['inputs'],name+':extra-sized-anchor')
  if error:
   rows.append({'arm_id':'arm-sized-witness','label':name,'inputs':row['inputs'],'scan_status':'excluded','exclusion_reason':error,'proposal_key':scan.key(row['inputs'])});continue
  probes.append(({}, {'arm_id':'arm-sized-witness','label':name,'anchor':name,'inputs':point}))
 sized_edges=[(detail,row) for detail,row in probes if row.get('parent_arm')=='arm-window-sized']
 scan.precompute([{**row['inputs'],P+'n_loops':1000.} for detail,row in sized_edges],'edge-sizing-scouts')
 for detail,row in sized_edges:
  point,error=scan.sized(row['inputs'],row['label'])
  if error:row['sizing_error']=error
  else:row['inputs']=point
 scan.precompute([row['inputs'] for detail,row in probes if not row.get('sizing_error')],'edge-and-sized-witness-proposals')
 for detail,row in probes:
  r={'status':'excluded','reason':row['sizing_error']} if row.get('sizing_error') else scan.evaluate(row['inputs']);k=scan.key(row['inputs']);row.update(proposal_key=k,scan_status=r['status'])
  if r['status']=='eligible':
   satisfied=all(v=='satisfied' for v in r['verdicts'].values());row.update(scan_full_satisfied=satisfied,scan_lcoe=r['channels'][P+'lcoe_calc__lcoe'],scan_violations=[scan.CAT[c]['source_local_identity'] for c,v in r['verdicts'].items() if v!='satisfied'])
   by_key[k]={'proposal_key':k,'inputs':row['inputs'],**r};detail.update(status='not caught at sampled edge' if satisfied else 'caught by current predicate at sampled edge',violations=row['scan_violations'])
  else:
   row.update(exclusion_reason=r['reason'],failure_traceback=r.get('traceback'));detail.update(status='arithmetic/domain exclusion; not a predicate boundary',reason=r['reason'])
  rows.append(row)
 # Every retained historical row remains correlated; no scan exclusion disappears.
 assert sum(r['arm_id']=='arm-window-fixed' for r in rows)==7949
 assert sum(r['arm_id']=='arm-window-sized' for r in rows)==7949
 write(H/'preparation/correlation.json',rows);write(H/'preparation/oracle-scan.json',list(by_key.values()));write(H/'preparation/proposals.json',[r['inputs'] for r in by_key.values()])
 write(H/'preparation/window-edges.json',edges);write(H/'preparation/extra-sizing-queries.json',scan.SIZING)
 digests={name:hashlib.sha256((H/'preparation'/name).read_bytes()).hexdigest() for name in ['correlation.json','oracle-scan.json','proposals.json','window-edges.json']}
 write(H/'preparation/window-freeze.json',{'frozen':True,'provenance':'engineered','unique_native_proposals':len(by_key),'correlation_rows':len(rows),'excluded_correlations':sum(r['scan_status']=='excluded' for r in rows),'arms':{a:dict(Counter(r['scan_status'] for r in rows if r['arm_id']==a)) for a in sorted({r['arm_id'] for r in rows})},'digests':digests,'claims':'Sampled predicate and exclusion evidence only. Uncaught edges remain uncaught; no extrapolated optimum or whole feasible-region claim. Four owner-approved sensitivities make no boundary claims.'})
 print(json.dumps(read(H/'preparation/window-freeze.json'),indent=2))
if __name__=='__main__':main()
