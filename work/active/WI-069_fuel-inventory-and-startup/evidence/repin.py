"""WI-069 metadata derived from the regenerated package and checked native baseline."""
import json
import os
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/studies'))
sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/pkg'))
if os.environ.get('STOP_PARSER_TEAX_ROOT'):
    sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from scripts.study import manifest as m
from scripts.integrate import rederived_census
from simkit.study.bridge import CandidateBridge
import study_route
import oracle_entry
pkg=ROOT/'exploration/stellarator_e2e/generated'
import tempfile
scratch=tempfile.TemporaryDirectory(prefix='wi069-baseline-')
evaluator=study_route.prepare(pkg,Path(scratch.name))
row=evaluator.evaluate(CandidateBridge(evaluator.entry_models).build({}))
assert row.outputs
scratch.cleanup()
expected=oracle_entry.evaluate({})
import math
for key,value in expected.items():
    if isinstance(value,(int,float)):
        assert math.isclose(row.outputs[key],value,rel_tol=1e-10,abs_tol=1e-18 if '__fuel_cycle__inventory__' in key else 1e-9),(key,row.outputs.get(key),value)
headline=row.outputs[oracle_entry.ORACLE_OUTPUT_TO_CHANNEL['lcoe']]
(HERE/'baseline.json').write_text(json.dumps({'outputs':dict(row.outputs),'responses':dict(row.responses),'oracle_mapped_count':len(expected)},indent=2,default=str)+'\n')
p=ROOT/'exploration/stellarator_e2e/studies/manifest.json'
d=json.loads(p.read_text());fp=m.indicator_input_fingerprint(pkg)
d['fingerprints']['indicator_inputs']=fp|{'files':[x['path'] for x in fp['files']]}
semantic=m.read_semantic_fingerprint(pkg)
d['fingerprints']['recorded_provenance']={'semantic_fingerprint':semantic,'executable_fingerprint':m.read_executable_fingerprint(pkg)}
d['baseline']['headline']['value']=headline
catalog=json.loads((pkg/'contracts/model_contract.json').read_text())['constraint_catalog']['concrete_entries']
d['baseline']['verdicts']=sorted([{'source_local_identity': entry['source_local_identity'], 'expected': row.responses[entry['constraint_id']]} for entry in catalog], key=lambda entry: entry['source_local_identity'])
p.write_text(json.dumps(d,indent=2)+'\n');m.load(p)
census={'derived_against_semantic_fingerprint':semantic}|rederived_census(pkg)
(ROOT/'tests/models/data/mfe_census.json').write_text(json.dumps(census,indent=2)+'\n')
print(json.dumps(d['fingerprints'],indent=2));print('native entries',census['entry_points'],'headline',headline)

# The tracked instance graph is a producer prerequisite checked byte-for-byte by integration.
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot
snapshot=ROOT/'exploration/stellarator_e2e/stellarator.snapshot.json'
capture_instance_graph_snapshot([ROOT/'exploration/stellarator_e2e/models'],snapshot)
print('captured tracked structural snapshot',snapshot.relative_to(ROOT))
