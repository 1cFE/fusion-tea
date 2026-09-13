"""Fresh public sealed baseline check against retained pre-repair audit identity."""
import json
from pathlib import Path
import tempfile
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
package = Path('exploration/ife_e2e/generated').resolve()
with tempfile.TemporaryDirectory(prefix='wi049-reaudit-') as temporary:
    evaluator = PreparedEvaluator(ProvisionalPackageLoader(package, 'ife_tea', Path(temporary)/'link'), package/'pipelines/pipeline.yaml', expects_constraint_report=True)
    result = evaluator.evaluate(CandidateBridge(evaluator.entry_models).build({}))
    current = dict(outputs=dict(result.outputs), responses=dict(result.responses))
expected = json.loads(Path('work/active/WI-049_ife-zero-discount-repair/repair-1-evidence/results.json').read_text())['before_baseline']
assert current == expected
Path(__file__).with_name('baseline.json').write_text(json.dumps(current,indent=2)+'\n')
print(f'PASS: sealed baseline executes; {len(current["outputs"])} outputs and {len(current["responses"])} responses exactly reproduce retained repair baseline.')
