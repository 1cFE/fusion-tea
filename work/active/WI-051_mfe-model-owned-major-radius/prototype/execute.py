"""Strict native execution, using only frozen pre-repair expectations."""
import importlib, json, math, sys
from types import SimpleNamespace
from collections.abc import Mapping
from pathlib import Path
import yaml
H=Path(__file__).resolve().parent; ROOT=Path.cwd(); P='stellarator_09__stellaris__'
sys.path.insert(0,str(ROOT))
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
def dump(name,v): (H/name).write_text(json.dumps(v,indent=2,default=lambda x:dict(x) if isinstance(x,Mapping) else str(x))+'\n')
pkg=H/'generated'; e=json.loads((H/'expectations.json').read_text()); old=json.loads((H/'frozen-results.json').read_text())
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
contract=json.loads((pkg/'contracts/model_contract.json').read_text()); prior=json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
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
component={}
for name,row in e['component_cases'].items():
    try: component[name]={'B_peak':module.run_conductor_peak_field(SimpleNamespace(**row['inputs']))}
    except Exception as exc: component[name]={'error':type(exc).__name__,'message':str(exc)}
    assert component[name].get('B_peak',component[name].get('error'))==row.get('B_peak',row.get('error'))
checks['component']=component
dump('checks.json',checks)
print('PASS frozen numeric coverage, verdicts, independent ratios, nine exact edges, anchors and adverse components')
