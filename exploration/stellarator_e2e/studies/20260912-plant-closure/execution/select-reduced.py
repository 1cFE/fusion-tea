import json,collections
from pathlib import Path
H=Path('/home/reid/1cfe/fusion-tea-codex-test/exploration/stellarator_e2e/studies/20260912-plant-closure')
read=lambda p:json.loads(p.read_text())
rows=read(H/'preparation/correlation.json');oracle=read(H/'preparation/oracle-scan.json');by={r['proposal_key']:r for r in oracle};selected={};P='stellarator_09__stellaris__'
def choose(k,why):selected.setdefault(k,[]).append(why)
for r in rows:
 if r['scan_status']=='eligible' and not r['arm_id'].startswith('arm-window'):choose(r['proposal_key'],'complete declared sensitivity/closure/edge block: '+r['arm_id'])
groups={}
for r in rows:
 if r['scan_status']=='eligible' and r['arm_id'].startswith('arm-window'):
  g=(r['arm_id'],r['historical_arm'],r['inputs'].get(P+'p_wallplug_heat',100))
  groups.setdefault(g,[]).append(r)
for g,rs in groups.items():
 for side,f in [('minimum',min),('maximum',max)]:choose(f(rs,key=lambda r:r['scan_lcoe'])['proposal_key'],f'{side} LCOE in oracle group {g}')
 for r in rs:
  if r.get('scan_full_satisfied'):
   choose(min([x for x in rs if x.get('scan_full_satisfied')],key=lambda x:x['scan_lcoe'])['proposal_key'],'full-18 oracle minimum '+str(g));break
combos={}
for e in oracle:combos.setdefault(tuple(sorted(e['verdicts'].items())),[]).append(e)
for combo,es in combos.items():
 if not any(e['proposal_key'] in selected for e in es):choose(min(es,key=lambda e:e['channels'][P+'lcoe_calc__lcoe'])['proposal_key'],'uncovered oracle verdict combination')
# Preserve every point on the original minor-radius transect for integer calendar steps.
transects=[r for r in rows if r.get('historical_arm')=='arm-transect-a' and r['scan_status']=='eligible']
print('transect rows',len(transects))
for r in transects:choose(r['proposal_key'],'retained minor-radius calendar transect')
print('selected',len(selected),'combos',len(combos),'groups',len(groups))
# Include the exact lowest-cost oracle point for each inherited/current predicate view.
pc=read(H/'preparation/predicate-correlation.json');sets={era:[x['current_id'] for x in pc if x['era']==era] for era in ['old-ten','round1-fourteen']}
for g,rs in groups.items():
 for name,ids in sets.items():
  passing=[r for r in rs if all(by[r['proposal_key']]['verdicts'][cid]=='satisfied' for cid in ids)]
  if passing:choose(min(passing,key=lambda r:r['scan_lcoe'])['proposal_key'],name+' oracle minimum '+str(g))
assert len(selected)<=400
newrows=[{**r,'selection_reasons':selected.get(r['proposal_key'],[])} for r in rows if r['scan_status']=='excluded' or r['proposal_key'] in selected]
write=lambda p,x:p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
write(H/'preparation/reduced-proposals.json',[by[k]['inputs'] for k in selected])
write(H/'preparation/reduced-correlation.json',newrows)
write(H/'preparation/reduced-selection.json',{'authority':'Owner: honestly please reduce the set. stay focused on risk mitigation, not jus tdoing shit for the sake of it','selected_cases':len(selected),'original_eligible_cases':len(by),'oracle_verdict_combinations':len(combos),'complete_nonwindow_blocks':True,'complete_calendar_transect':True,'reasons':selected,'meaning':'Native verification of all declared comparison blocks, 84 edges, every observed oracle verdict combination, calendar transect, extrema and per-set candidate minima. Full historical counts remain oracle-scan results, not exhaustive native results. Completed interrupted-store cases remain separate supporting evidence.'})
import hashlib
names=['reduced-proposals.json','reduced-correlation.json','oracle-scan.json','window-edges.json']
write(H/'preparation/reduced-window-freeze.json',{'frozen':True,'unique_native_proposals':len(selected),'correlation_rows':len(newrows),'excluded_correlations':sum(r['scan_status']=='excluded' for r in newrows),'digests':{n:hashlib.sha256((H/'preparation'/n).read_bytes()).hexdigest() for n in names},'provenance':'engineered risk-selected subset of completed full oracle scan; owner-directed reduction','original_freeze':'preparation/window-freeze.json'})
print('FINAL selected',len(selected),'correlations',len(newrows))
