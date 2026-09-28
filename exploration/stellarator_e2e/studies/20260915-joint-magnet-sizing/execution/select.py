"""Fix one prepared native cohort after retained staged oracle scans."""
import json,sys
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parents[1];R=H/'results';PREP=H/'preparation';sys.path.insert(0,str(H/'execution'))
from scan import evaluate
P='stellarator_09__stellaris__';read=lambda p:json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
base=read(R/'initial-oracle-scan.json')['rows'];fine=read(R/'refinement-oracle-scan.json')['rows'];allrows=base+fine
pool=[r for r in allrows if r['family'].startswith('default') and r['outcome']=='evaluated']
passes=[r for r in pool if r['full_satisfied']]
best=min(passes,key=lambda r:r['channels'][P+'lcoe_calc__lcoe']) if passes else min(pool,key=lambda r:(len(r['violated']),r['channels'][P+'lcoe_calc__lcoe']))
near=min([r for r in pool if 'peak_field_ok' not in r['violated']],key=lambda r:(len(r['violated']),r['channels'][P+'lcoe_calc__lcoe']))
ref=next(r for r in base if r['id']=='reference-sized')
accommodated=next(r for r in base if r['id']=='reference-accommodated')
anchors={r['id']:r for r in [ref,accommodated,best,near]}
scenarios=[('material-1.10',{'material_factor':1.1}),('material-1.35',{'material_factor':1.35}),('orientation-2',{'orientation_factor':2.}),('retentions-0.9',{'cabling_factor':.9,'degradation_factor':.9,'sharing_factor':.9})]
extras=[]
for aid,a in anchors.items():
 for name,over in scenarios:
  point=a['point']|{P+'magnet__winding_pack__'+k:v for k,v in over.items()}
  extras.append(evaluate(dict(id=aid+'--'+name,family='performance-sensitivity',arm='performance-sensitivity',scenario=name,anchor_id=aid,point=point,original_point=point)))
# Shape is a local fit diagnostic only: missing physical couplings exclude economic ranking.
for ratio in [.8,1.25]:
 point=near['point']|{P+'magnet__winding_pack__fit_aspect_ratio':ratio}
 extras.append(evaluate(dict(id=near['id']+f'--shape-{ratio}',family='shape-sensitivity',arm='shape-sensitivity',scenario='local-shape-only',anchor_id=near['id'],point=point,original_point=point)))
# Independently vary each available dimension from an anchor; no required-space feedback.
for leaf,values in [('magnet__coil__coil_t',[.5,.55,.6,.65,.7]),('magnet__casing__interior_y',[.45,.5,.55,.6,.65])]:
 for value in values:
  point=best['point']|{P+leaf:value}
  extras.append(evaluate(dict(id=best['id']+'--'+leaf+f'-{value}',family='allocation-bracket',arm='allocation-bracket',anchor_id=best['id'],point=point,original_point=point)))
write(R/'sensitivity-oracle-scan.json',{'anchor_ids':list(anchors),'rows':extras})
allrows+=extras
# Retain exact diagnostic separately: floating sign mismatch is disclosed, no predicate altered.
selected=[r for r in allrows if r['outcome']=='evaluated' and r['family']!='exact-boundary']
unique=[];seen={};props=[];scans=[]
for r in selected:
 sig=json.dumps(r['point'],sort_keys=True)
 if sig not in seen:
  seen[sig]=r['id'];unique.append({'proposal_id':r['id'],'point':r['point']});scans.append(r|{'proposal_id':r['id']})
 props.append({k:v for k,v in r.items() if k not in ['channels','verdicts','violated','full_satisfied','outcome']}|{'canonical_proposal_id':seen[sig]})
assert len(unique)<=400
write(PREP/'unique-proposals.json',unique);write(PREP/'proposals.json',props)
write(R/'oracle-scan.json',{'rows':scans,'scope':'Unchanged candidate independent oracle; reuses retained initial/refinement evaluations and adds separate sensitivities.'})
write(PREP/'final-selection.json',{'unique_native_cases':len(unique),'report_rows':len(props),'initial_rows':len(base),'refinement_rows':len(fine),'extra_rows':len(extras),'all_scan_rows':len(allrows),'unsupported':[r for r in allrows if r['outcome']!='evaluated'],'separate_exact_boundary':['reference-exact'],'default_initial_passes':sum(r['full_satisfied'] for r in base if r['family']=='default-grid'),'default_refinement_passes':sum(r['full_satisfied'] for r in fine),'scenario_anchor_ids':list(anchors),'best_scan_anchor':best['id'],'field_passing_anchor':near['id']})
# Endpoint diagnostics keep uncaught and unsupported edges explicitly; no native adaptive search.
anchor=min([r for r in scans if r['full_satisfied'] and r['family'].startswith('default')],key=lambda r:r['channels'][P+'lcoe_calc__lcoe']) if passes else near
edges=[]
for g in read(H/'axes.json')['groups']:
 key=g['keys'][0]['key'];values=sorted({r['point'][key] for r in unique})
 for label,value in [('low',values[0]),('high',values[-1])]:
  row=evaluate({'id':g['axis']+'-'+label,'point':anchor['point']|{key:value}})
  edges.append(row|{'axis':g['axis'],'edge':label,'value':value,'caught':bool(row['violated']) if row['outcome']=='evaluated' else None})
write(R/'edge-scan.json',{'anchor_id':anchor['id'],'anchor_full_satisfied':anchor['full_satisfied'],'interpretation':'From feasible default anchor if present; otherwise nearest field-passing rejected anchor, so caught does not bracket a feasible region. No continuous boundary claim.','edges':edges})
print('SELECTED',len(unique),'native cases;',len(props),'aliases; default passes',len(passes),'best',best['id'],flush=True)
