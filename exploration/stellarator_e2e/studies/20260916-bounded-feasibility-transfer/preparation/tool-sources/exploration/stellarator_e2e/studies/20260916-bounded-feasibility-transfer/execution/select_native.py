import json
from pathlib import Path
H=Path('exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer');read=lambda p:json.loads(p.read_text());P='stellarator_09__stellaris__'
allrows=[]
for stage in ['initial','refine1','refine2','final']:allrows+=read(H/f'results/{stage}-oracle-scan.json')['rows']
# Correct metadata label only; no values or verdicts recomputed.
for r in allrows:
 if 'operands' in r:r['resolved_operand_counts']=r.pop('operands')
ranked=read(H/'results/ranked.json');chosen=[];seen=set()
def add(r):
 key=json.dumps(r['point'],sort_keys=True)
 if key not in seen and r['outcome']=='evaluated':seen.add(key);chosen.append(r)
for r in allrows:
 if r['family'] in ['control','transfer-reference','transfer-coupled','transfer-single-input','loop-accommodation','transverse-accommodation','final-local','allocation-refinement']:add(r)
for r in ranked[:12]:add(r)
for rid in ['lhs-03','lhs-57','lhs-22']:
 add(next(r for r in allrows if r['id']==rid))
for radius in [11,11.5,12,12.5,13,13.5]:
 candidates=[r for r in ranked if r['family']=='boundary-refinement' and r['point'][P+'plasma__R']==radius]
 add(candidates[0])
# Retain representative observed rejection combinations for native stratification.
patterns={tuple(sorted(r.get('violated',[]))) for r in chosen}
for r in ranked:
 pat=tuple(sorted(r['violated']))
 if pat not in patterns and len(chosen)<74:add(r);patterns.add(pat)
props=[]
for r in chosen:
 pid=r['id'];props.append({'id':pid,'proposal_id':pid,'canonical_proposal_id':pid,'family':r['family'],'arm':'arm-native','point':r['point']})
assert len(props)<=79
for name in ['proposals.json','unique-proposals.json']:(H/'preparation'/name).write_text(json.dumps(props,indent=2)+'\n')
(H/'results/oracle-scan.json').write_text(json.dumps({'rows':allrows,'calls':len(allrows),'unique_coordinates':len({json.dumps(r['point'],sort_keys=True) for r in allrows}),'evaluated':sum(r['outcome']=='evaluated' for r in allrows),'refused':sum(r['outcome']=='refused' for r in allrows),'full_satisfied':sum(r['full_satisfied'] for r in allrows)},indent=2)+'\n')
print('native cases',len(props),'families',sorted({r['family'] for r in props}))
print('oracle calls',len(allrows),'unique',len({json.dumps(r['point'],sort_keys=True) for r in allrows}))
