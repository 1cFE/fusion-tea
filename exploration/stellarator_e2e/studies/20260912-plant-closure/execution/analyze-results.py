"""Derive comparison tables from native exports, retaining every correlation."""
import csv,json,itertools
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parents[1];R=H/'results';P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def main():
 assert read(R/'all-channel-verification.json')['outcome']=='pass'
 channelmap=read(H/'preparation/required-channels.json');cat=read(R/'constraint-catalog.json');corr=read(R/'correlation.json');defaults=read(R/'package-inputs.json')
 points={}
 with (R/'native-points.csv').open() as f:
  for row in csv.DictReader(f):points[row['candidate_id']]={'candidate_id':row['candidate_id'],**{a:float(row[a]) for a in channelmap},'verdicts':{cid:row[cid] for cid in cat},'full_satisfied':row['full_satisfied']=='True'}
 ledger={r['candidate_id']:r for r in read(R/'finance-ledgers.json')};inputs={r['candidate_id']:r['inputs'] for r in read(R/'case-inputs.json')}
 predicates=read(H/'preparation/predicate-correlation.json');sets={era:[r['current_id'] for r in predicates if r['era']==era] for era in {r['era'] for r in predicates}};sets['current-eighteen']=list(cat)
 def view(c):return {'candidate_id':c['candidate_id'],'inputs':inputs[c['candidate_id']],'lcoe':c['lcoe'],'lcoe_1cfe':c['lcoe_1cfe'],'satisfied_sets':{era:all(c['verdicts'][k]=='satisfied' for k in keys) for era,keys in sets.items()},'violations':[cat[k]['source_local_identity'] for k,v in c['verdicts'].items() if v=='violated']}
 arms=[]
 for arm in sorted({r['arm_id'] for r in corr}):
  rows=[r for r in corr if r['arm_id']==arm];ids={r['candidate_id'] for r in rows if r['scan_status']=='eligible'};cs=[points[i] for i in ids];full=[c for c in cs if c['full_satisfied']]
  arms.append({'arm_id':arm,'correlation_status_counts':dict(Counter(r['scan_status'] for r in rows)),'unique_cases':len(cs),'fully_satisfied_unique_cases':len(full),'satisfaction_counts':{era:sum(all(c['verdicts'][k]=='satisfied' for k in keys) for c in cs) for era,keys in sets.items()},'best_full_current_sample':view(min(full,key=lambda c:c['lcoe'])) if full else None,'lcoe_extrema_all_diagnostics':[min(c['lcoe'] for c in cs),max(c['lcoe'] for c in cs)] if cs else None})
 summary={'unique_cases':len(points),'fully_satisfied':sum(c['full_satisfied'] for c in points.values()),'constraint_counts':{cid:{'source_local_identity':e['source_local_identity'],**dict(Counter(c['verdicts'][cid] for c in points.values()))} for cid,e in cat.items()},'arms':arms}
 write(R/'report-summary.json',summary)
 factorial=[];bridges=[]
 for anchor in sorted({r['anchor'] for r in corr if r['arm_id']=='arm-closure-factorial'}):
  rows=[r for r in corr if r['arm_id']=='arm-closure-factorial' and r['anchor']==anchor];missing=[r for r in rows if r['scan_status']!='eligible'];item={'anchor':anchor,'complete_factorial':len(rows)==8 and not missing,'corners':[{'modes':r['modes'],'status':r['scan_status'],**(view(points[r['candidate_id']]) if r['scan_status']=='eligible' else {'exclusion_reason':r['exclusion_reason']})} for r in rows]}
  if item['complete_factorial']:
   cs={tuple(r['modes']):points[r['candidate_id']] for r in rows};item['effects']={}
   for objective,capkey in [('lcoe','C'),('lcoe_1cfe','C_1cfe')]:
    base=cs[(0,0,0)][objective];alllive=cs[(1,1,1)][objective];single=[cs[m][objective]-base for m in [(1,0,0),(0,1,0),(0,0,1)]]
    path=[(0,0,0),(1,0,0),(1,1,0),(1,1,1)];deltas=[cs[b][objective]-cs[a][objective] for a,b in zip(path,path[1:])]
    # Full inclusion-exclusion coefficients reveal pair and triple interactions.
    interactions={}
    for mask in [(1,1,0),(1,0,1),(0,1,1),(1,1,1)]:
     bits=[j for j in range(3) if mask[j]];coefficient=0.
     for n in range(len(bits)+1):
      for subset in itertools.combinations(bits,n):coefficient+=(-1)**(len(bits)-n)*cs[tuple(int(j in subset) for j in range(3))][objective]
     interactions[''.join(map(str,mask))]=coefficient
    item['effects'][objective]={'single_effects_L_C_A_from_all_held':single,'loop_then_cycle_then_calendar':deltas,'all_live_minus_all_held':alllive-base,'interaction_residual':alllive-base-sum(single),'inclusion_exclusion_interactions':interactions}
    for a,b in zip(path,path[1:]):
     x=ledger[cs[a]['candidate_id']];y=ledger[cs[b]['candidate_id']];terms=[(y[capkey]-x[capkey])/x['E_MWh'],(y['A']-x['A'])/x['E_MWh'],(y[capkey]+y['A'])*(1/y['E_MWh']-1/x['E_MWh'])];delta=y[objective]-x[objective];residual=sum(terms)-delta
     assert abs(residual)<=1e-9+1e-9*abs(delta)
     bridges.append({'anchor':anchor,'objective':objective,'from_modes':a,'to_modes':b,'from_candidate':x['candidate_id'],'to_candidate':y['candidate_id'],'capital_term':terms[0],'annual_term':terms[1],'energy_term':terms[2],'direct_delta':delta,'residual':residual})
  factorial.append(item)
 write(R/'closure-factorial.json',factorial);write(R/'lcoe-bridges.json',bridges)
 historical={r['case_id']:r for r in csv.DictReader((H/'context/historical-points.csv').open())};comparison=[]
 for r in corr:
  if not r['arm_id'].startswith('arm-window'):continue
  old=historical.get(r['historical_id']);item={'arm_id':r['arm_id'],'historical_id':r['historical_id'],'historical_arm':r['historical_arm'],'historical_excluded':r['historical_excluded'],'current_status':r['scan_status']}
  if old:item.update(historical_lcoe=float(old['lcoe']),historical_lcoe_1cfe=float(old['lcoe_1cfe']),historical_feasible=old['feasible']=='True',historical_verdicts={r['source_local_identity']:old[r['source_local_identity']] for r in predicates if r['era']=='old-ten'})
  if r['scan_status']=='eligible':
   c=points[r['candidate_id']];item.update(view(c))
   if old:item.update(cross_revision_lcoe_delta=c['lcoe']-float(old['lcoe']),cross_revision_lcoe_1cfe_delta=c['lcoe_1cfe']-float(old['lcoe_1cfe']))
  else:item['reason']=r['exclusion_reason']
  comparison.append(item)
 write(R/'historical-comparison.json',{'meaning':'Historical actual ten-predicate execution versus current views of identical predicates; upstream model changes are intentional. Cross-revision deltas are not closure-only attribution.','rows':comparison})
 # Full per-axis observed values and violations; correlated variation implies no causal slope.
 accounts=[]
 for group in read(H/'axes.json')['groups']:
  k=group['keys'][0]['key'];bins={}
  for cid,c in points.items():bins.setdefault(inputs[cid].get(k,defaults[k]),[]).append(c)
  accounts.append({'axis':group['axis'],'entry_key':k,'framing':'sensitivity','boundary_claim':False,'confounding_note':'These aggregate bins include coordinated changes; causal effects only in explicitly paired families.','values':[{'value':v,'cases':len(cs),'full_satisfied':sum(c['full_satisfied'] for c in cs),'lcoe_range':[min(c['lcoe'] for c in cs),max(c['lcoe'] for c in cs)],'violated_counts':{cat[q]['source_local_identity']:sum(c['verdicts'][q]=='violated' for c in cs) for q in cat}} for v,cs in sorted(bins.items())]})
 write(R/'axis-accounts.json',accounts)
 # Every native point on the inherited minor-radius transect is kept, including event-step neighbors.
 transect=[]
 for r in corr:
  if r.get('historical_arm')=='arm-transect-a' and r['scan_status']=='eligible':
   c=points[r['candidate_id']];transect.append({'arm_id':r['arm_id'],'historical_id':r.get('historical_id'),'inputs':inputs[c['candidate_id']],**view(c),**{k:c[k] for k in ['calendar_n_replacements','calendar_terminal_downtime_yr','calendar_availability','cas72_annual','wall_load_peak','calendar_physical_life_fpy']}})
 write(R/'calendar-transect.json',transect)
 groups={}
 for row in transect:
  effective={**defaults,**row['inputs']};held={k:v for k,v in effective.items() if k!=P+'a' and not (row['arm_id']=='arm-window-sized' and k==P+'n_loops')}
  signature=(row['arm_id'],json.dumps(held,sort_keys=True));groups.setdefault(signature,[]).append(row)
 steps=[]
 for (arm,held),rows in groups.items():
  rows.sort(key=lambda r:r['inputs'].get(P+'a',defaults[P+'a']))
  for a,b in zip(rows,rows[1:]):
   if a['calendar_n_replacements']==b['calendar_n_replacements']:continue
   steps.append({'arm_id':arm,'held_inputs':json.loads(held),'lower_a':a['inputs'].get(P+'a',defaults[P+'a']),'upper_a':b['inputs'].get(P+'a',defaults[P+'a']),'lower_candidate':a['candidate_id'],'upper_candidate':b['candidate_id'],'replacement_counts':[a['calendar_n_replacements'],b['calendar_n_replacements']],'availability':[a['calendar_availability'],b['calendar_availability']],'cas72_annual':[a['cas72_annual'],b['cas72_annual']],'lcoe':[a['lcoe'],b['lcoe']],'meaning':'Adjacent retained same-input transect samples except a and the explicitly sized loop count; sampled count transition, not a continuous boundary.'})
 write(R/'calendar-steps.json',steps)
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
