"""Select retained screen evidence and prepare finite refinements before evaluating."""
import json,itertools
from pathlib import Path
import numpy as np
H=Path(__file__).resolve().parents[1];P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text());write=lambda n,x:(H/'preparation'/n).write_text(json.dumps(x,indent=2)+'\n')
rows=read(H/'results/ranked.json');eligible=[r for r in rows if r['family']=='initial-search' and r['full_satisfied'] and r['channels'][P+'divertor__divheat__power_account_valid']==1]
# Rank only variable engineering margins: fixed current reserve and fixed literals cannot distinguish anchors.
active=['peak_field_ok','divertor_heat_ok','sustainment_ok','burn_hold_ok','wp_fit_ok','loop_capacity_ok','wall_load_ok','beta_ok','wp_stress_ok','cond_strain_ok','recirc_ok']
def score(r):
 m=r['margins'];vals=[m[k]['normalized'] for k in active if k not in ['burn_hold_ok','sustainment_ok']]
 vals.extend([m[k]['margin']/50 for k in ['burn_hold_ok','sustainment_ok']]);return min(vals)
anchor=max(eligible or [r for r in rows if r['family']=='initial-search'],key=score);base=anchor['point'];out=[]
def add(pid,pt,family):out.append({'id':pid,'proposal_id':pid,'canonical_proposal_id':pid,'family':family,'arm':'arm-native','point':pt})
keys=['plasma__R','plasma__a','magnet__coil__I_coil','plasma__n_e0','plasma__T_i0','magnet__coil__coil_t','magnet__casing__interior_y'];bounds=[(10.5,15),(1.1,1.7),(12e6,18e6),(4e20,6e20),(12,18),(.55,.75),(.55,.75)]
add('anchor',base,'anchor')
for k,(lo,hi) in zip(keys,bounds):
 for delta in [-.02,-.01,.01,.02]:
  value=base[P+k]*(1+delta)
  if lo<=value<=hi:add(f'neighbor-{k}-{delta:+g}',base|{P+k:value},'axis-neighbor')
for delta in [-1,1]:add(f'neighbor-loops-{delta:+d}',base|{P+'heat_transport__n_loops':base[P+'heat_transport__n_loops']+delta},'integer-neighbor')
rng=np.random.default_rng(1709)
for i in range(16):
 signs=rng.choice([-1,1],7);pt=base|{P+k:float(base[P+k]*(1+.005*s)) for k,s in zip(keys,signs)}
 assert all(lo<=pt[P+k]<=hi for k,(lo,hi) in zip(keys,bounds))
 add(f'combined-{i:02d}',pt|{P+'heat_transport__n_loops':float(base[P+'heat_transport__n_loops']+(-1 if i%2 else 1))},'combined-neighbor')
ref=read(H/'preparation/controls.json')[0]['point']
for k in keys[:5]:add('restore-'+k,base|{P+k:ref[P+k]},'matched-contrast')
add('restore-both-peaks',base|{P+k:ref[P+k] for k in keys[3:5]},'matched-contrast')
add('anchor-inventory1',base|{P+'magnet__winding_pack__inventory_multiplier':1.0},'inventory-contrast')
for n in [14,16,20,22]:add(f'anchor-loops-{n}',base|{P+'heat_transport__n_loops':float(n)},'loop-contrast')
for k in keys[5:]:
 for value in [.55,.6,.7,.75]:add(f'accommodation-{k}-{value}',base|{P+k:value},'accommodation-contrast')
# A declared local R-current lattice. All other parameters are literally identical.
Rs=sorted(set([float(x) for x in np.linspace(max(10.5,base[P+keys[0]]*.92),min(15,base[P+keys[0]]*1.08),15)]+[base[P+keys[0]]]))
Is=sorted(set([float(x) for x in np.linspace(max(12e6,base[P+keys[2]]*.92),min(18e6,base[P+keys[2]]*1.08),15)]+[base[P+keys[2]]]))
for i,(r,c) in enumerate(itertools.product(Rs,Is)):add(f'map-{i:03d}',base|{P+keys[0]:r,P+keys[2]:c},'map')
write('refinement-selection.json',{'anchor':anchor,'variable_margin_score':score(anchor),'initial_valid_passes':len(eligible),'ranking':'maximum minimum normalized variable engineering margin, with heating normalized by50MW; no cost ranking','bounds_unchanged':True,'map_R_values':Rs,'map_I_values':Is,'scope':'Fixed-configuration local lattice, no hidden optimization. Neighbor amplitudes declared here before evaluation.'})
write('refine-proposals.json',out)
print('anchor',anchor['id'],'score',score(anchor),'passes initially',len(eligible),'refinement calls',len(out));print(base)
