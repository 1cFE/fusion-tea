"""Prepare finite coordinates only. No physics evaluation or optimization."""
import json
from pathlib import Path
import numpy as np
H=Path(__file__).resolve().parents[1];P='stellarator_09__stellaris__'
write=lambda n,x:(H/'preparation'/n).write_text(json.dumps(x,indent=2)+'\n')
rules=json.loads(Path('.project/active/aries-comparison-preparation/package/input-rules.json').read_text())
keys=['plasma__R','plasma__a','magnet__coil__I_coil','plasma__n_e0','plasma__T_i0','magnet__coil__coil_t','magnet__casing__interior_y','heat_transport__n_loops','magnet__winding_pack__inventory_multiplier']
base={P+k:rules['default_values'][P+k] for k in keys}|rules['forward_overrides']
def row(i,point,family):return {'id':i,'proposal_id':i,'canonical_proposal_id':i,'family':family,'arm':'arm-native','point':point}
control=[row('r2-forward',base,'control'),row('r2-table5',base|next(s['keys'] for s in rules['conditioned_seams'] if s['id']=='table5_geometry_field'),'control'),row('r2-forward-reserve',base|{P+'magnet__winding_pack__inventory_multiplier':1.01},'control')]
accom=base|{P+'magnet__winding_pack__inventory_multiplier':1.01,P+'magnet__coil__coil_t':.65,P+'magnet__casing__interior_y':.65,P+'heat_transport__n_loops':18.}
control.append(row('reference-accommodated',accom,'control'))
write('controls.json',control)
bounds=[(10.5,15),(1.1,1.7),(12e6,18e6),(4e20,6e20),(12,18)];rng=np.random.default_rng(20260917);n=512
# Latin hypercube of five genuine levers; generated and retained before oracle use.
a=np.column_stack([(rng.permutation(n)+rng.random(n))/n for _ in bounds])
rows=control+[row(f'lhs-{i:04d}',accom|{P+k:float(lo+v*(hi-lo)) for k,(lo,hi),v in zip(keys[:5],bounds,vs)},'initial-search') for i,vs in enumerate(a)]
write('scan-proposals.json',rows)
print('Prepared',len(rows),'screening calls, seed20260917. No point evaluated.')
