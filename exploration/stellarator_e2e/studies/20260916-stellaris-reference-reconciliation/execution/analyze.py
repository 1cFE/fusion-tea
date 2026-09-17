"""All-point oracle comparison and complete case/predicate accounting."""
import json,math,csv
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parents[1];R=H/'results';P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
def write(n,v):(R/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
native=read(R/'native-cases.json');scan={r['proposal_id']:r for r in read(R/'oracle-scan.json')['rows']};cat=read(R/'predicate-catalog.json')
assert len(native)==8 and len(cat)==20
failures=[];ns=np=0;maxabs=maxrel=0.
for row in native:
 expected=scan[row['proposal_id']];assert row['inputs']==expected['point']
 for k,v in expected['channels'].items():
  got=row['outputs'][k];ns+=1;maxabs=max(maxabs,abs(got-v));maxrel=max(maxrel,abs(got-v)/max(abs(v),abs(got),1e-300))
  if not math.isclose(got,v,rel_tol=1e-9,abs_tol=1e-9):failures.append({'proposal_id':row['proposal_id'],'channel':k,'native':got,'oracle':v})
 assert set(row['verdicts'])==set(expected['verdicts'])==set(cat)
 for cid,v in expected['verdicts'].items():
  np+=1
  if row['verdicts'][cid]!=v:failures.append({'proposal_id':row['proposal_id'],'constraint_id':cid,'native':row['verdicts'][cid],'oracle':v})
write('oracle-all-points.json',{'outcome':'fail' if failures else 'pass','cases':len(native),'scalar_comparisons':ns,'predicate_comparisons':np,'relative_tolerance':1e-9,'absolute_tolerance':1e-9,'exact_predicates':True,'max_absolute_deviation':maxabs,'max_relative_deviation':maxrel,'failures':failures,'unmapped_native_channels':sorted(set(native[0]['outputs'])-set(scan[native[0]['proposal_id']]['channels']))})
rows=[]
for row in native:
 q={k.removeprefix(P):v for k,v in row['outputs'].items()}
 rows.append({'proposal_id':row['proposal_id'],'candidate_id':row['candidate_id'],'quantities':q,'all20_satisfied':all(x=='satisfied' for x in row['verdicts'].values()),'violated':[cat[k]['source_local_identity'] for k,x in row['verdicts'].items() if x!='satisfied']})
a={'scope':'Eight conditional reconstruction and local sensitivity cases; no engineering qualification or search.','cases':rows,'overall':{'cases':8,'all20_passes':sum(r['all20_satisfied'] for r in rows)},'predicate_outcomes':{k:{'source_local_identity':e['source_local_identity'],'counts':dict(Counter(r['verdicts'][k] for r in native))} for k,e in cat.items()}}
write('analysis.json',a)
flat=[{'proposal_id':r['proposal_id'],**r['quantities'],'all20_satisfied':r['all20_satisfied'],'violated':';'.join(r['violated'])} for r in rows]
with (R/'case-summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(flat[0]),lineterminator='\n');w.writeheader();w.writerows(flat)
assert not failures,failures
print('Mapped scalars',ns,'predicates',np,'failures',len(failures),a['overall'])
app=read(H/'preparation/predicate-applicability.json');amap={r['constraint_id']:r for r in app['predicates']};assert set(amap)==set(cat)
joined=[]
for row in native:
 joined.append({'proposal_id':row['proposal_id'],'raw_all20_satisfied':all(v=='satisfied' for v in row['verdicts'].values()),'published_reference_qualification':'unresolved','predicates':[amap[cid]|{'raw_verdict':v} for cid,v in row['verdicts'].items()]})
write('case-predicate-applicability.json',{'policy':app['policy'],'cases':joined})
contrasts=[];byid={r['proposal_id']:r for r in native}
for old,new,scope in [('legacy-control','selected-reserve-control','Selected inventory mode and reserve joint intervention'),('legacy-control','exact-profiles-legacy','Two exact profile exponents jointly'),('selected-reserve-control','exact-profiles-selected-reserve','Two exact profile exponents jointly'),('exact-profiles-legacy','table5-conditioned-legacy','Coordinated source R, volume shape and current conditioning'),('exact-profiles-selected-reserve','table5-conditioned-selected-reserve','Coordinated source R, volume shape and current conditioning'),('exact-profiles-legacy','offref-R-plus2pct','R alone +2%, fixed shape/current'),('exact-profiles-legacy','offref-a-plus2pct','a alone +2%, fixed shape/current')]:
 a=byid[old];b=byid[new];contrasts.append({'from':old,'to':new,'attribution_scope':scope,'delta_outputs':{k:b['outputs'][k]-v for k,v in a['outputs'].items()},'predicate_changes':[{**amap[k],'from':v,'to':b['verdicts'][k]} for k,v in a['verdicts'].items() if v!=b['verdicts'][k]]})
write('contrasts.json',contrasts)
