"""Verify the full input-record and pipeline-binding delta, beyond the key census."""
import json
from pathlib import Path
import yaml
H=Path(__file__).resolve().parent; ROOT=Path.cwd(); P='stellarator_09__stellaris__'
before=ROOT/'exploration/stellarator_e2e/generated'; after=H/'generated'
def records(pkg):
    return {(x['param_group'],x['qualified_name']):x for x in json.loads((pkg/'contracts/model_contract.json').read_text())['parameters']}
a,b=records(before),records(after); retired=('stellarator_plant_params',P+'magnet__R0')
assert set(a)-set(b)=={retired} and not set(b)-set(a)
assert all(a[k]==b[k] for k in b)
def inputs(pkg): return {(f.stem,k):v for f in (pkg/'inputs').glob('*.json') for k,v in json.loads(f.read_text()).items()}
ai,bi=inputs(before),inputs(after)
assert set(ai)-set(bi)=={retired} and not set(bi)-set(ai)
assert all(ai[k]==bi[k] for k in bi)
def bindings(pkg):
    p=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text())
    return {(name,formal):value for name,m in p['modules'].items() for formal,value in m.get('inputs',{}).items()}
ap,bp=bindings(before),bindings(after); assert set(ap)==set(bp)
changed={k:(ap[k],bp[k]) for k in ap if ap[k]!=bp[k]}
assert set(changed)=={(P+m,f) for m,f in [('coil_length','R0'),('field_calc','R0'),('peak_field_calc','R_in'),('magnet_cost','R0'),('stored_energy','R0')]}
for old,new in changed.values(): assert old=='float stellarator_plant_params.'+P+'magnet__R0' and new=='float stellarator_plant_params.'+P+'R'
anchors=json.loads((H/'expectations.json').read_text())['anchors']
anchor_edges=[{'module':k[0],'formal':k[1],'binding':v} for k,v in bp.items() if any('stellarator_plant_params.'+P+x==v.split(' ',1)[-1] for x in anchors)]
assert all(ap[(x['module'],x['formal'])]==x['binding'] for x in anchor_edges)
(H/'contract-checks.json').write_text(json.dumps({'remaining_parameter_records_exact':len(b),'remaining_input_values_exact':len(bi),'changed_bindings':[{'module':k[0],'formal':k[1],'old':v[0],'new':v[1]} for k,v in changed.items()],'fixed_anchor_bindings':anchor_edges},indent=2)+'\n')
print('PASS all 246 surviving parameter records/default values exact; only five binding operands change; fixed anchor edges exact')
