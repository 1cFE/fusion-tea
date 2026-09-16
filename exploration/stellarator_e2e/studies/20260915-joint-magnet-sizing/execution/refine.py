"""Retained second-stage scan on declared physical choices, no evaluator solve."""
import json,sys
from pathlib import Path
from itertools import product
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'execution'))
from scan import evaluate
P='stellarator_09__stellaris__';old=json.loads((H/'results/initial-oracle-scan.json').read_text())['rows']
anchor=next(r for r in old if r['id']=='reference-sized')['point']
rows=[]
for R,a,I in product([12.7,13.1,13.5],[1.15,1.25,1.35,1.45],[14.6e6,15e6,15.4e6,15.8e6,16.2e6]):
    point=anchor|{P+'plasma__R':R,P+'plasma__a':a,P+'magnet__coil__I_coil':I,P+'magnet__coil__coil_t':.65,P+'magnet__casing__interior_y':.65}
    row={'id':f'r-{R}-{a}-{I:g}','family':'default-refinement','arm':'default-refinement','point':point,'original_point':point}
    rows.append(evaluate(row))
    if len(rows)%15==0:print('refined',len(rows),flush=True)
(H/'results/refinement-oracle-scan.json').write_text(json.dumps({'basis':'No coarse default passes; refine narrow heating/burn/field transitions. R12.7–13.5, a1.15–1.45, NI14.6–16.2MA, independently declared0.65m radial and0.65m transverse allocation. Lower a/current extend the initial window by11.5%/5.2%, inside prior broad geometry model applicability; no acceptance limits change.','rows':rows},indent=2,allow_nan=False)+'\n')
print('refinement passes',[(r['id'],r['channels'][P+'lcoe_calc__lcoe']) for r in rows if r['full_satisfied']],flush=True)
