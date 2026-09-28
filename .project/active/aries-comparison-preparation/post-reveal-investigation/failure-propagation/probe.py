"""Synthetic fault injection into the native executor; no reference request or continuation."""
import hashlib,json,os,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from exploration.stellarator_e2e.studies import study_route as route
from simkit.study.bridge import CandidateBridge
from simkit.evaluation.failure import EvaluationFailed
from simkit.evaluation.projection import _numeric_output
prepared=route.prepare(route.PACKAGE_DIR,Path(tempfile.mkdtemp()))
graph=prepared._graph
failure=next(k for k,v in graph.spec.modules.items() if v.module_type=='mfe_conductor_current.REBCO_Conductor_CurrentModule')
descendants=set();pending=[failure]
while pending:
    node=pending.pop()
    for dependent in graph.adjacency[node]:
        if dependent not in descendants:descendants.add(dependent);pending.append(dependent)
exit_node=next(v for v in graph.spec.modules.values() if v.is_exit)
contract=json.loads((route.PACKAGE_DIR/'contracts/model_contract.json').read_text())
outputs={key:{'channel':b.channel_name,'producer':graph.channel_providers[b.channel_name],'depends_on_failed_module':graph.channel_providers[b.channel_name] in descendants|{failure}} for key,b in exit_node.outputs.items()}
original=prepared._executor._execute_module
seen=[];captured={}
def injection(key,spec,context):
    captured['context']=context
    if key==failure:raise ValueError('Synthetic conductor fault injection; no reference inputs')
    original(key,spec,context);seen.append(key)
prepared._executor._execute_module=injection
try:prepared.evaluate(CandidateBridge(prepared.entry_models).build({}))
except EvaluationFailed as exc:error=exc.failure.model_dump(mode='json')
context=captured['context'];numbers={k:_numeric_output(v) for k,v in context.channels.items() if _numeric_output(v) is not None}
result={'purpose':'synthetic failure-capture only; no continuation or reference execution','failed_node':failure,'native_failure':error,'module_count':len(graph.spec.modules),'completed_module_count':len(seen),'in_memory_channel_count':len(context.channels),'in_memory_numeric_count':len(numbers),'descendant_modules':sorted(descendants),'outputs':outputs,'completed_modules':seen,'in_memory_numbers':numbers,'constraint_catalog':contract['constraint_catalog']['concrete_entries']}
Path(__file__).with_name('probe-results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('outputs','completed_modules','in_memory_numbers','constraint_catalog')},indent=2))
