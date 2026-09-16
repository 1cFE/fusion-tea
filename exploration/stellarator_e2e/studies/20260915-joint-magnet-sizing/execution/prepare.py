"""Preserve candidate inputs/contracts and stage the bounded physical-choice scan."""
import json
import shutil
from itertools import product
from pathlib import Path
from scripts.study.verify import package_input_values
from exploration.stellarator_e2e.studies import study_route as route
H=Path(__file__).resolve().parents[1]; ROOT=H.parents[3]; PREP=H/'preparation'; P=route.P
read=lambda p:json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
for name in ['manifest.json','oracle_entry.py','ANNEX.md','study_route.py']:
    shutil.copy2(H.parent/name,PREP/name)
for name in ['verify_stellaris.py','oracle_finance.py']:
    shutil.copy2(H.parent.parent/name,PREP/name)
for name in ['contracts','inputs','pipelines','schemas']:
    shutil.copytree(route.PACKAGE_DIR/name,PREP/('package-'+name),dirs_exist_ok=True)
for name in ['source-design-review.md','coupled-requirements.md','coupled-dependencies.md']:
    shutil.copy2(ROOT/'work/orchestration/goals/joint-magnet-sizing-feasibility/evidence'/name,PREP/name)
shutil.copytree(ROOT/'work/orchestration/goals/joint-magnet-sizing-feasibility/evidence/entering',PREP/'entering',dirs_exist_ok=True)
params=package_input_values(route.PACKAGE_DIR)
write(PREP/'resolved-defaults.json',params)
contract=read(PREP/'package-contracts/model_contract.json')
write(PREP/'required-channels.json',sorted(x['channel_name'] for x in contract['outputs'] if x['python_type'] in ['float','int']))
rows=[]
def add(id,family,point,**extra):
    rows.append(dict(id=id,family=family,arm=family,point={P+k:v for k,v in point.items()},**extra))
add('reference','entering-controls',{})
old=read(H.parent/'20260915-absolute-conductor-current-margin/preparation/proposals.json')
for name in ['alloc-oldpass0.8-0.5','alloc-oldpass1.0-0.5','alloc-oldpass1.2-0.5','alloc-oldpass1.2-0.5--orientation-3']:
    r=next(r for r in old if r['id']==name)
    add(name,'historical-controls',{k.removeprefix(P):v for k,v in r['original_point'].items()})
active={'magnet__winding_pack__sizing_mode':1.,'magnet__winding_pack__inventory_multiplier':1.01}
for r,a,i,(t,y) in product([12.7,13.5,14.25,15.0],[1.3,1.5,1.7,1.9],[15.4e6,16.2e6,17e6,18e6],[(.3,.4),(.45,.55),(.6,.6),(.75,.75)]):
    add(f'g-{r}-{a}-{i:g}-{t}','default-grid',active|{'plasma__R':r,'plasma__a':a,'magnet__coil__I_coil':i,'magnet__coil__coil_t':t,'magnet__casing__interior_y':y})
add('reference-sized','reference-sizing',active)
add('reference-exact','exact-boundary',active|{'magnet__winding_pack__inventory_multiplier':1.})
add('reference-accommodated','reference-sizing',active|{'magnet__coil__coil_t':.6,'magnet__casing__interior_y':.6})
# Proposed/declined controls are declared before evaluation, including planned small sensitivities.
keys=sorted({k for row in rows for k in row['point']}|{P+'magnet__winding_pack__'+k for k in ['material_factor','orientation_factor','cabling_factor','degradation_factor','sharing_factor','fit_aspect_ratio']})
axes={'schema_version':'study-axis-declaration/v1','groups':[{'axis':k.removeprefix(P),'note':'Complete single public attribute group; physical geometry search or separately labeled scenario/control.', 'keys':[{'key':k,'provenance':'fan_out'}]} for k in keys]}
assert set(keys)<=set(params)
for row in rows:
    row['original_point']=row['point'].copy()
    row['point']={k:params[k] for k in keys}|row['point']
write(H/'axes.json',axes);write(PREP/'scan-proposals.json',rows)
(PREP/'ANNEX-correction.md').write_text('# Current study interface\n\nThe preserved ANNEX carries historical interface counts. Current copied contracts and manifest govern: '+str(len(params))+' inputs, '+str(len(read(PREP/'required-channels.json')))+' numeric outputs and20 predicates. Sizing mode0 is entering behavior; mode1 derives physical inventory after actual field. All acceptance limits remain fixed in the main study.\n')
print('Prepared',len(rows),'scan rows and',len(keys),'complete axis groups; no evaluations.')
