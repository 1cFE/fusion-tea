"""Check unchanged baseline and record revised native package identity."""
import json, os, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/studies'))
sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/pkg'))
sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from scripts.study import manifest as m
from simkit.study.bridge import CandidateBridge
import study_route
pkg=ROOT/'exploration/stellarator_e2e/generated'
with tempfile.TemporaryDirectory(prefix='diagnostic-baseline-') as tmp:
 evaluator=study_route.prepare(pkg,Path(tmp))
 row=evaluator.evaluate(CandidateBridge(evaluator.entry_models).build({}))
 outputs=dict(row.outputs);responses=dict(row.responses)
old=json.loads((ROOT/'work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration/baseline.json').read_text())
assert outputs==old['outputs'], [(k,v,old['outputs'].get(k)) for k,v in outputs.items() if old['outputs'].get(k)!=v]
assert responses==old['responses']
record={'outputs':outputs,'responses':responses,'baseline_exactly_unchanged':True,'numeric_channels':len(outputs),'source_baseline':'work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration/baseline.json','semantic_fingerprint':m.read_semantic_fingerprint(pkg),'executable_fingerprint':m.read_executable_fingerprint(pkg)}
(HERE/'baseline.json').write_text(json.dumps(record,indent=2)+'\n')
p=ROOT/'exploration/stellarator_e2e/studies/manifest.json';d=json.loads(p.read_text())
fp=m.indicator_input_fingerprint(pkg)
d['fingerprints']['indicator_inputs']=fp|{'files':[x['path'] for x in fp['files']]}
d['fingerprints']['recorded_provenance']={'semantic_fingerprint':record['semantic_fingerprint'],'executable_fingerprint':record['executable_fingerprint']}
p.write_text(json.dumps(d,indent=2)+'\n');m.load(p)
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot
snapshot=ROOT/'exploration/stellarator_e2e/stellarator.snapshot.json'
capture_instance_graph_snapshot([ROOT/'exploration/stellarator_e2e/models'],snapshot)
print('PASS baseline exact equality:',len(outputs),'numeric channels and',len(responses),'responses; pin',fp['digest'])
