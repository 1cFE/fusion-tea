import json
from pathlib import Path
H=Path('exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer');P='stellarator_09__stellaris__'
rows=json.loads((H/'results/initial-ranked.json').read_text()); byid={r['id']:r for r in rows};out=[]
for anchor in ['lhs-03','lhs-57','lhs-22']:
 base=byid[anchor]['point']
 for di in [-.06,-.04,-.02,0,.02]:
  for da in [-.03,0,.03]:
   if di==0 and da==0:continue
   out.append({'id':f'{anchor}-i{di:+.2f}-a{da:+.2f}','family':'refinement-1','anchor':anchor,'point':base|{P+'magnet__coil__I_coil':base[P+'magnet__coil__I_coil']*(1+di),P+'plasma__a':base[P+'plasma__a']+da}})
# Inspect independent allocation near the best field-only case without crediting free dimensions.
for t in [.58,.59,.62,.65]:
 for di in [-.04,-.02,0]:
  base=byid['lhs-03']['point'];out.append({'id':f'fit-t{t}-i{di}','family':'allocation-refinement','point':base|{P+'magnet__coil__coil_t':t,P+'magnet__coil__I_coil':base[P+'magnet__coil__I_coil']*(1+di)}})
(H/'preparation/refine1-proposals.json').write_text(json.dumps(out,indent=2)+'\n')
print(len(out))
