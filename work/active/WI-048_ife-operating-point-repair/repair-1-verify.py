"""Regenerate WI-048 citation repair and compare all baseline numeric/verdict outputs."""
from pathlib import Path
import hashlib, json, tempfile, subprocess, re
from sysml_codegen.cli import GenerationConfig, run_codegen
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
from tests.model_families import IFE, canonical_path, materialize_canonical_subset
from tests.ife_execution import HANDWRITTEN
from tests.ife_oracle import assert_source_outputs
root=Path.cwd(); item=root/'work/active/WI-048_ife-operating-point-repair'
scratch=Path(tempfile.mkdtemp(prefix='wi048-repair1-')); package=root/'exploration/ife_e2e/generated'
models=materialize_canonical_subset(IFE,scratch/'models')
strip=lambda text: re.sub(r'\s+','',re.sub(r'/\*.*?\*/|//[^\n]*','',text,flags=re.S))
for logical in IFE.owned:
 p=canonical_path(logical)
 old=subprocess.check_output(['git','show',f'243625b4:{p.relative_to(root)}']).decode()
 assert strip(old)==strip(p.read_text()),p
 assert p.read_bytes()==(IFE.twin/logical).read_bytes(),p
before={p.relative_to(package).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in package.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
old_model=json.loads(subprocess.check_output(['git','show','243625b4:exploration/ife_e2e/generated/contracts/model_contract.json']))
old_package=json.loads(subprocess.check_output(['git','show','243625b4:exploration/ife_e2e/generated/contracts/package_contract.json']))
implementation=(package/HANDWRITTEN).read_bytes()
assert run_codegen(GenerationConfig(models_path=models,output_path=package,package_name='ife_tea',overwrite=True,preserve_handwritten=True))
assert (package/HANDWRITTEN).read_bytes()==implementation
loader=ProvisionalPackageLoader(package,'ife_tea',scratch/'link'); _,fingerprint=loader.load()
evaluator=PreparedEvaluator(loader,package/'pipelines/pipeline.yaml',expects_constraint_report=True)
result=evaluator.evaluate(CandidateBridge(evaluator.entry_models).build({}))
assert_source_outputs(result.outputs,{})
prior=json.loads((item/'execution-evidence.json').read_text())['baseline']['outputs']
current={k:v for k,v in result.outputs.items() if isinstance(v,(int,float))}
assert len(current)==30
for k,v in current.items(): assert v==prior[k],(k,v,prior[k])
verdicts={k:v for k,v in result.responses.items() if k!='headline'}
assert len(verdicts)==2
prior_responses=json.loads((item/'execution-evidence.json').read_text())['baseline']['responses']
for k,v in verdicts.items(): assert v==prior_responses[k],(k,v,prior_responses[k])
after={p.relative_to(package).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in package.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
record=dict(baseline_revision='243625b476c6761e6c74dbafa7e9413402eafe90',validation_models=str(models),executable_tokens_unchanged=True,all_family_twins_identical=True,numeric_count=30,verdict_count=2,max_absolute_baseline_residual=0,max_relative_baseline_residual=0,baseline_numeric_outputs=current,baseline_verdicts=verdicts,old_semantic_fingerprint=old_model['semantic_fingerprint'],semantic_fingerprint=json.loads((package/'contracts/model_contract.json').read_text())['semantic_fingerprint'],old_executable_fingerprint=old_package['executable_fingerprint'],loaded_fingerprint=fingerprint,typed_quotient_sha256=hashlib.sha256(implementation).hexdigest(),regeneration_changed_files=[k for k in sorted(before.keys()|after.keys()) if before.get(k)!=after.get(k)],changed_package_files=subprocess.check_output(['git','diff','243625b4','--name-only','--',str(package)]).decode().splitlines())
(item/'repair-1-identity.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if not k.startswith('baseline_')},indent=2))
