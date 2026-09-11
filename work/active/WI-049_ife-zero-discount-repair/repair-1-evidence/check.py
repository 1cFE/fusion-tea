"""Bounded A01 citation, package-preservation and baseline verification."""
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from sysml_codegen.cli import GenerationConfig, run_codegen
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
root = Path(__file__).resolve().parent
package = Path('exploration/ife_e2e/generated').resolve()
source = 'knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md'
old = '**Source**: Hawker, A simplified economic model for inertial fusion'
new = '**Source**: ' + source
paths = [Path('models/designs/generic_ife/ife_plant.sysml'), Path('exploration/ife_e2e/models/designs/generic_ife/ife_plant.sysml')]
for path in paths:
    before = subprocess.check_output(['git', 'show', f'HEAD:{path}'], text=True)
    assert before.count(old) == 2
    assert path.read_text() == before.replace(old, new)
assert paths[0].read_bytes() == paths[1].read_bytes()
assert Path(source).is_file()
assert 'construction time to be 5 years and the operational lifetime to be 40 years' in Path(source).read_text().splitlines()[147]
def tree():
    return {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in package.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def identity():
    return dict(semantic=json.loads((package/'contracts/model_contract.json').read_text())['semantic_fingerprint'], executable=json.loads((package/'contracts/package_contract.json').read_text())['executable_fingerprint'])
def execute():
    with tempfile.TemporaryDirectory(prefix='wi049-a01-') as tmp:
        evaluator = PreparedEvaluator(ProvisionalPackageLoader(package, 'ife_tea', Path(tmp)/'link'), package/'pipelines/pipeline.yaml', expects_constraint_report=True)
        result = evaluator.evaluate(CandidateBridge(evaluator.entry_models).build({}))
        return dict(outputs=dict(result.outputs), responses=dict(result.responses))
initial_tree, initial_identity, baseline = tree(), identity(), execute()
records=[]
config=GenerationConfig(models_path=Path('exploration/ife_e2e/models'),output_path=package,package_name='ife_tea',overwrite=True,preserve_handwritten=True)
for smart in (False, False, True):
    previous=tree()
    assert run_codegen(replace(config,smart_regen=smart))
    current=tree()
    result=execute()
    assert result==baseline
    assert identity()==initial_identity
    if records:
        assert current==previous
    records.append(dict(smart_regen=smart,changed_files=[p for p in sorted(set(previous)|set(current)) if previous.get(p)!=current.get(p)],identity=identity(),baseline_equal=True,baseline=result))
report=dict(source_fields_checked=4,source_resolves=True,reference_preserved=True,defaults_equations_preserved=True,canonical_twin_equal=True,before_identity=initial_identity,before_package=initial_tree,before_baseline=baseline,routes=records,after_package=tree())
(root/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: four Source fields resolve, exact citation-only diff, equal twins; unchanged semantic/executable identity and all 32 baseline outputs/two responses through three regeneration passes.')
print('Changed files on first regeneration:', records[0]['changed_files'])
print(json.dumps(initial_identity))
