"""Independent read-only production identity and execution checks for WI-048 r1."""
from pathlib import Path
import hashlib,json,re,subprocess,tempfile
from tests.model_families import IFE,canonical_path,materialize_canonical_subset
from tests.ife_execution import HANDWRITTEN
from tests.ife_oracle import assert_source_outputs
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
root=Path.cwd(); evidence=root/'work/analysis/wi048-r1-audit-evidence'
old='243625b4'; head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
strip=lambda s: re.sub(r'\s+','',re.sub(r'/\*.*?\*/|//[^\n]*','',s,flags=re.S))
for logical in IFE.owned:
    p=canonical_path(logical)
    before=subprocess.check_output(['git','show',f'{old}:{p.relative_to(root)}'],text=True)
    assert strip(before)==strip(p.read_text()),p
    assert p.read_bytes()==(IFE.twin/logical).read_bytes(),p
oldmatrix=subprocess.check_output(['git','show',f'{old}:data/traceability_matrix.csv'])
assert (root/'data/traceability_matrix.csv').read_bytes().startswith(oldmatrix)
scratch=Path(tempfile.mkdtemp(prefix='wi048-r1-audit-'))
models=materialize_canonical_subset(IFE,scratch/'models')
package=root/'exploration/ife_e2e/generated'
loader=ProvisionalPackageLoader(package,'ife_tea',scratch/'link'); _,fingerprint=loader.load()
evaluator=PreparedEvaluator(loader,package/'pipelines/pipeline.yaml',expects_constraint_report=True)
result=evaluator.evaluate(CandidateBridge(evaluator.entry_models).build({}))
assert_source_outputs(result.outputs,{})
prior=json.loads((root/'work/active/WI-048_ife-operating-point-repair/execution-evidence.json').read_text())['baseline']
nums={k:v for k,v in result.outputs.items() if isinstance(v,(int,float))}
responses={k:v for k,v in result.responses.items() if k!='headline'}
assert len(nums)==30 and len(responses)==2
assert all(v==prior['outputs'][k] for k,v in nums.items())
assert all(v==prior['responses'][k] for k,v in responses.items())
semantic=json.loads((package/'contracts/model_contract.json').read_text())['semantic_fingerprint']
assert semantic==json.loads(subprocess.check_output(['git','show',f'{old}:exploration/ife_e2e/generated/contracts/model_contract.json']))['semantic_fingerprint']
record=dict(head=head,canonical_file_count=len(IFE.owned),tokens_equal=True,twins_equal=True,matrix_add_only=True,models=str(models),semantic_fingerprint=semantic,loaded_fingerprint=fingerprint,guard_sha256=hashlib.sha256((package/HANDWRITTEN).read_bytes()).hexdigest(),numeric_count=len(nums),verdict_count=len(responses),max_absolute_residual=0,max_relative_residual=0,outputs=nums,responses=responses)
(evidence/'identity.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ('outputs','responses')},indent=2))
validation=subprocess.run([str(root/'.codex-test/run'),'agentic-mbse','validate','--complete',str(models)],capture_output=True,text=True)
(evidence/'validation.txt').write_text(validation.stdout+validation.stderr+f'\nExit code: {validation.returncode}\n')
print('Validation exit code:',validation.returncode)
