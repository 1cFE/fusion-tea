import json
from pathlib import Path
H=Path('exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer');P='stellarator_09__stellaris__';base=json.loads((H/'preparation/search-base.json').read_text());out=[]
for R,I in [(11,12.1e6),(11.5,13e6),(12,13.85e6),(12.5,14.7e6),(13,15.5e6),(13.5,16.2e6)]:
 for a in [1.2,1.375,1.55]:
  for delta in [-.2e6,0,.2e6]:
   if not 12e6<=I+delta<=16.2e6:continue
   out.append({'id':f'boundary-R{R}-a{a}-I{(I+delta)/1e6:g}','family':'boundary-refinement','point':base|{P+'plasma__R':R,P+'plasma__a':a,P+'magnet__coil__I_coil':I+delta}})
(H/'preparation/refine2-proposals.json').write_text(json.dumps(out,indent=2)+'\n');print(len(out))
