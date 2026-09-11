"""Reproduce shipped package regeneration and all diagnostic identities."""
from pathlib import Path
from collections import Counter
from dataclasses import replace
import hashlib
import inspect
import json
from sysml_codegen.cli import GenerationConfig, run_codegen
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
root = Path(__file__).resolve().parent
package = Path('exploration/ife_e2e/generated').resolve()
config = GenerationConfig(models_path=Path('exploration/ife_e2e/models'), output_path=package,
                          package_name='ife_tea', overwrite=True)
def tree():
    return {p.relative_to(package).as_posix():p.read_bytes() for p in package.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts}
before = tree()
records=[]
for smart in (False, True):
    assert run_codegen(replace(config, preserve_handwritten=True, smart_regen=smart))
    assert tree() == before
    evaluator = PreparedEvaluator(ProvisionalPackageLoader(package, 'ife_tea', root/'native-link'),
                                  package/'pipelines/pipeline.yaml', expects_constraint_report=True)
    result = evaluator.evaluate(CandidateBridge(evaluator.entry_models).build({}))
    records.append(dict(smart_regen=smart, byte_identical=True,
                        outputs=dict(result.outputs), responses=dict(result.responses)))
from ife_tea.handwritten.ife_lcoe.ife_present_value_factors_impl import run_ife_present_value_factors
from ife_tea.handwritten.ife_lcoe.generating_electricity_price_impl import run_generating_electricity_price
(root/'native-regeneration.json').write_text(json.dumps(dict(
    files=len(before), sha256={k:hashlib.sha256(v).hexdigest() for k,v in before.items()},
    factor_signature=str(inspect.signature(run_ife_present_value_factors)),
    price_signature=str(inspect.signature(run_generating_electricity_price)),
    routes=records), indent=2)+'\n')
a=json.loads((root/'l6-before.json').read_text()); b=json.loads((root/'l6-after.json').read_text())
def key(issue):
    return tuple(issue[k] for k in ('code','element_name','message'))+(issue['location'].rsplit(':',1)[0],)
assert Counter(map(key,a))==Counter(map(key,b))
rows=[]
for n,issue in enumerate(a,1):
    match=next(x for x in b if key(x)==key(issue))
    rows.append(dict(identity=n,status='retained',rule=issue['code'],element=issue['element_name'],
                     message=issue['message'],before=issue['location'],after=match['location']))
(root/'l6-attribution.json').write_text(json.dumps(rows,indent=2)+'\n')
print(f'PASS {len(before)} package files identical under both routes; {len(rows)} retained L6 identities, zero new/resolved.')
