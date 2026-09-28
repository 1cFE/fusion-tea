"""Native generation of the shipped model package after isolated acceptance."""
import json
from pathlib import Path
from run_acceptance import ROOT,HERE,hashes,dump,evaluator,execute
from check_results import check
from sysml_codegen.cli import GenerationConfig,run_codegen
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot
h=HERE; scratch=Path((h/'scratch.txt').read_text().strip());models=scratch/'models'
check(json.loads((h/'results.json').read_text()),json.loads((h/'inputs.json').read_text()))
package=ROOT/'exploration/stellarator_e2e/generated'
before=hashes(package);dump(h/'shipped-before-hashes.json',before)
manual=json.loads((h/'normative-handwritten.json').read_text())
body=package/'handwritten/mfe_divertor_heat/divertor_heat_ledger_impl.py'
assert 'AUTO_IMPLEMENTED = True' in body.read_text().split('SysML Source:')[0]
body.unlink()
config=GenerationConfig(models_path=models,output_path=package,package_name='stellarator_tea',overwrite=True,preserve_handwritten=True)
assert run_codegen(config)
after=hashes(package)
assert all(after[k]==v for k,v in manual.items())
assert after==hashes(scratch/'generated')
ev,bridge=evaluator(package,'stellarator_tea',scratch/'shipped-link')
r=execute(ev,bridge,{})
assert r['outputs']==json.loads((h/'results.json').read_text())['baseline']['outputs']
assert run_codegen(config)
assert hashes(package)==after
capture_instance_graph_snapshot([models],h/'instance_graph_snapshot.json')
dump(h/'shipped-after-hashes.json',after)
contract=json.loads((package/'contracts/model_contract.json').read_text());by_type={}
for parameter in contract['parameters']: by_type.setdefault(parameter['entry_type'],[]).append(parameter['qualified_name'])
census={'derived_against_semantic_fingerprint':contract['semantic_fingerprint'],'entry_points':len(contract['parameters']),'by_entry_type':{k:sorted(v) for k,v in by_type.items()}}
(ROOT/'tests/models/data/mfe_census.json').write_text(json.dumps(census,indent=1)+'\n')
dump(h/'shipped-verification.json',{'isolated_equals_shipped':True,'regeneration_fixed_point':True,'normative_implementations_unchanged':manual,'semantic_fingerprint':contract['semantic_fingerprint'],'entry_points':len(contract['parameters']),'responses':r['responses']})
print('PASS native shipped package, isolated parity, regeneration fixed point, normative preservation and census')
