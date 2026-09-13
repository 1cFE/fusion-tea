"""Full native outputs in a process isolated from other package imports."""
import json
import os
import sys
from collections.abc import Mapping
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
P='stellarator_09__stellaris__'
CASES={f'{mode}_{name}':{P+'availability_direct':value,**{P+k:v for k,v in rates.items()}} for mode,value in [('live',0.),('held',.85)] for name,rates in [('ordinary',{}),('zero',{'discount_rate':0.}),('equal',{'discount_rate':.02,'inflation_rate':.02}),('tiny_positive',{'discount_rate':1e-18,'inflation_rate':1e-18}),('tiny_negative',{'discount_rate':-1e-18,'inflation_rate':-1e-18})]}
def run(package,destination):
    ev=PreparedEvaluator(ProvisionalPackageLoader(package,'stellarator_tea',destination.parent/'link',strict=True),package/'pipelines/pipeline.yaml',expects_constraint_report=True)
    bridge=CandidateBridge(ev.entry_models)
    rows={}
    for name,overrides in CASES.items():
        try:
            result=ev.evaluate(bridge.build(overrides))
            rows[name]={'overrides':overrides,'outputs':dict(result.outputs),'responses':dict(result.responses),'report':result.report}
        except Exception as exc:rows[name]={'overrides':overrides,'error':type(exc).__name__,'message':str(exc)}
    inputs={}
    for p in sorted((package/'inputs').glob('*.json')):inputs.update(json.loads(p.read_text()))
    destination.write_text(json.dumps({'cases':rows,'inputs':inputs},indent=2,default=lambda v:dict(v) if isinstance(v,Mapping) else str(v))+'\n')
    print({k:r.get('error',len(r['outputs']) if 'outputs' in r else None) for k,r in rows.items()})
if __name__=='__main__':run(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve())
