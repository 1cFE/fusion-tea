import json
from pathlib import Path
H=Path('exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer');P='stellarator_09__stellaris__';base=json.loads((H/'preparation/search-base.json').read_text());rows=json.loads((H/'results/ranked.json').read_text());original=next(r for r in rows if r['id']=='lhs-03')['point'];out=[]
for dr in [-.1,0,.1]:
 for di in [-.03,-.025,-.015,-.01]:
  out.append({'id':f'fine-R{dr:+g}-I{di:+g}','family':'final-local','point':original|{P+'plasma__R':original[P+'plasma__R']+dr,P+'magnet__coil__I_coil':original[P+'magnet__coil__I_coil']*(1+di),P+'magnet__coil__coil_t':.58}})
for scale,name in [(12.3/12.7,'smaller'),(13.1/12.7,'larger')]:
 out.append({'id':'transfer-'+name,'family':'transfer-coupled','point':base|{P+'plasma__R':12.7*scale,P+'plasma__a':1.3*scale,P+'magnet__coil__I_coil':15.4e6*scale}})
 for k in ['plasma__R','plasma__a','magnet__coil__I_coil']:
  out.append({'id':f'transfer-{name}-{k}','family':'transfer-single-input','point':base|{P+k:base[P+k]*scale}})
near=rows[0]['point']
for n in [12,14,15,18]:out.append({'id':f'near-loops-{n}','family':'loop-accommodation','point':near|{P+'heat_transport__n_loops':n}})
for n in [14,18]:out.append({'id':f'reference-loops-{n}','family':'loop-accommodation','point':base|{P+'heat_transport__n_loops':n}})
for y in [.55,.58,.70]:out.append({'id':f'near-y-{y}','family':'transverse-accommodation','point':near|{P+'magnet__casing__interior_y':y}})
(H/'preparation/final-proposals.json').write_text(json.dumps(out,indent=2)+'\n');print(len(out))
