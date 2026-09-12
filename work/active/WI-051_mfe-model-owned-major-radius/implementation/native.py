"""Strict native execution, using only frozen pre-repair expectations."""
import importlib, json, math, sys
from types import SimpleNamespace
from collections.abc import Mapping
from pathlib import Path
import yaml
H=Path(sys.argv[1]).resolve(); ROOT=Path.cwd(); FROZEN=Path(__file__).resolve().parent.parent/'prototype'; P='stellarator_09__stellaris__'
sys.path.insert(0,str(ROOT))
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
def dump(name,v): (H/name).write_text(json.dumps(v,indent=2,default=lambda x:dict(x) if isinstance(x,Mapping) else str(x))+'\n')
pkg=ROOT/'exploration/stellarator_e2e/generated'; e=json.loads((FROZEN/'expectations.json').read_text()); old=json.loads((FROZEN/'frozen-results.json').read_text())
ev=PreparedEvaluator(ProvisionalPackageLoader(pkg,'stellarator_tea',H/'link',strict=True),pkg/'pipelines/pipeline.yaml',expects_constraint_report=True)
bridge=CandidateBridge(ev.entry_models)
out={}
for name,change in [('baseline',{}),('R14',{P+'R':14.0})]+[(f'invalid_{i}',{P+'R':v}) for i,v in enumerate(e['invalid_R'])]+[(f'retired_{i}',v) for i,v in enumerate(e['retired_key_cases'])]:
    try:
        r=ev.evaluate(bridge.build(change)); out[name]={'outputs':dict(r.outputs),'responses':dict(r.responses),'report':r.report}
    except Exception as exc: out[name]={'error':type(exc).__name__,'message':str(exc)}
    print(name,out[name].get('error','executed'),flush=True)
dump('results.json',out)
out=json.loads((H/'results.json').read_text())
checks={}
for name,ref in [('baseline','baseline'),('R14','tied_R14')]:
    a=out[name]; b=old['cases'][ref]['native']; assert set(a['outputs'])==set(e['channels'])==set(b['outputs'])
    for k,v in b['outputs'].items():
        assert (a['outputs'][k]==v if name=='baseline' else math.isclose(a['outputs'][k],v,rel_tol=1e-9,abs_tol=1e-9)),(name,k,a['outputs'][k],v)
    assert a['responses']==b['responses'],(name,'responses')
    if name=='baseline': assert a['report']==b['report']
    checks[name]={'channels':len(b['outputs']),'responses_exact':True,'report_exact':a['report']==b['report']}
ratios={}
for k,v in e['ratios'].items():
    actual=out['R14']['outputs'][P+k]/out['baseline']['outputs'][P+k]
    assert math.isclose(actual,v,rel_tol=1e-9,abs_tol=1e-9)
    ratios[k]={'expected':v,'actual':actual}
checks['independent_ratios']=ratios
for i in range(5): assert out[f'invalid_{i}'].get('error')=='EvaluationFailed'
for i in range(4): assert 'error' in out[f'retired_{i}'] and P+'magnet__R0' in out[f'retired_{i}']['message']
contract=json.loads((pkg/'contracts/model_contract.json').read_text()); prior=json.loads((Path(__file__).resolve().parent/'entering-package/contracts/model_contract.json').read_text())
def census(c): return sorted((x['param_group'],x['qualified_name']) for x in c['parameters'])
before,after=census(prior),census(contract)
delta={'removed':sorted(set(before)-set(after)),'added':sorted(set(after)-set(before))}
assert [list(x) for x in delta['removed']]==e['contract_delta']['remove'] and delta['added']==[]
dump('contract-delta.json',{'old_count':len(before),'new_count':len(after),'old':before,'new':after,**delta,'semantic_fingerprint':contract['semantic_fingerprint'],'executable_fingerprint':ev.fingerprint})
pipeline=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text()); edges={}
for suffix,formal in e['edges'].items():
    binding=pipeline['modules'][P+suffix]['inputs'][formal]
    assert binding=='float stellarator_plant_params.'+P+'R',(suffix,formal,binding)
    edges[P+suffix+'.'+formal]=binding
dump('edges.json',edges)
inputs={}
for f in (pkg/'inputs').glob('*.json'): inputs.update(json.loads(f.read_text()))
checks['anchors']={P+k:inputs[P+k] for k in e['anchors']}
assert all(inputs[P+k]==old['inputs'][P+k] for k in e['anchors'])
module=importlib.import_module('stellarator_tea.handwritten.mfe_plasma_scaling.conductor_peak_field_impl')
schema=getattr(importlib.import_module('stellarator_tea.modules.mfe_plasma_scaling.conductor_peak_field'),'Conductor_Peak_FieldInput')
assert 'R_in' in schema.model_fields
component={}
for name,row in e['component_cases'].items():
    try: component[name]={'B_peak':module.run_conductor_peak_field(schema(**row['inputs']))}
    except Exception as exc: component[name]={'error':type(exc).__name__,'message':str(exc)}
    if 'B_peak' in component[name]:
        component[name]['upper_bound_24_9_satisfied']=component[name]['B_peak']<=24.9
        assert component[name]['upper_bound_24_9_satisfied']==row['upper_bound_24_9_satisfied']
    assert component[name].get('B_peak',component[name].get('error'))==row.get('B_peak',row.get('error'))
checks['component']=component
dump('checks.json',checks)
print('PASS frozen numeric coverage, verdicts, independent ratios, nine exact edges, anchors and adverse components')

import pydantic
from simkit.evaluation.package_load import ProvisionalPackageLoader
package,_=ProvisionalPackageLoader(pkg,'stellarator_tea',H/'schema-link',strict=True).load()
entry=json.loads((pkg/'inputs/stellarator_plant_params.json').read_text())
schema=next(c for c in package.CUSTOM_SCHEMA_TYPES if P+'R' in c.model_fields)
assert schema.model_config.get('extra')=='forbid'
schema_refusals={}
for i,change in enumerate(e['retired_key_cases']):
    try: schema(**(entry|change))
    except pydantic.ValidationError as exc:
        assert P+'magnet__R0' in str(exc)
        schema_refusals[str(i)]={'error':type(exc).__name__,'message':str(exc)}
    else: raise AssertionError('Retired key accepted')
dump('schema-refusals.json',schema_refusals)
