"""Preparatory strict direct evaluation; no study/store identity is fabricated."""
import json,os,sys,subprocess
from pathlib import Path
from collections.abc import Mapping
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study import preflight,verify
from simkit.study.bridge import CandidateBridge
from simkit.study.evidence_io import encode_evidence
H=Path(__file__).resolve().parents[1];R=H/'results'
def write(p,x):p.write_text(json.dumps(x,indent=2,default=lambda x:dict(x) if isinstance(x,Mapping) else str(x))+'\n')
assert json.loads((H/'reviews/pre-execution-approval.json').read_text())['approved'] is True
p=route.prepare(route.PACKAGE_DIR,R/'runtime-links')
point=route._baseline_point(route.MANIFEST_PATH)
inputs=CandidateBridge(p.entry_models).build(point)
write(R/'baseline-effective-inputs.json',{k:v.model_dump(mode='json') for k,v in inputs.items()})
write(R/'package-inputs.json',verify.package_input_values(route.PACKAGE_DIR))
write(R/'entry-models.json',{k:{'class':v.__module__+'.'+v.__qualname__,'schema':v.model_json_schema()} for k,v in p.entry_models.items()})
e=p.evaluate(inputs)
write(R/'baseline-native-evidence.json',encode_evidence(e))
cat=route._catalog_by_constraint_id(route.PACKAGE_DIR)
assert set(e.responses) == set(cat) | {'headline'} and len(cat)==18
route.write_identity_document(route.PACKAGE_DIR,R/'package_identity.json')
write(R/'constraint-catalog.json',cat)
write(R/'baseline_result.json',{'schema_version':route.BASELINE_RESULT_SCHEMA_VERSION,'executed_under':{'identity_digest':e.provenance.executable_fingerprint,'store_id':'not-stored:preparatory-direct-api','case_id':'not-a-study-case:preparatory-baseline'},'point':point,'channels':dict(e.outputs),'verdicts':[{'constraint_id':cid,'definition_qualified_name':cat[cid]['definition_qualified_name'],'source_local_identity':cat[cid]['source_local_identity'],'status':status} for cid,status in e.responses.items() if cid!='headline']})
gates=preflight.run_gates(route.PACKAGE_DIR,route.MANIFEST_PATH,H/'axes.json',R/'package_identity.json',R/'baseline_result.json');write(R/'preflight.json',gates)
write(R/'runtime.json',{'python':sys.version,'python_executable':sys.executable,'teax_root':os.environ['STOP_PARSER_TEAX_ROOT'],'teax_revision':subprocess.check_output(['git','-C',os.environ['STOP_PARSER_TEAX_ROOT'],'rev-parse','HEAD'],text=True).strip(),'repo_revision':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'launcher':'.codex-test/run','pythonpath':'$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit','STUDY_REQUIRE_TEAX':'1','era_pin':None})
assert gates['outcome']=='pass',gates
print('Baseline/preflight pass; preparatory baseline has no store; ordinary baseline will execute through StudyRunner.')
