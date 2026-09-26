"""Isolated replay of the documented fixed-design Stellaris diagnostic baseline at goal entry (adapted from the reconciled-economics goal's stellaris-regression-entry.py)."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import traceback

ROOT = Path.cwd()
HERE = ROOT / 'work/orchestration/goals/design-space-combinations/evidence'
PREFIX = HERE / 'entry-stellaris-regression'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'exploration/stellarator_e2e/studies'))
sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def preservation():
    entry = json.loads((HERE / 'preservation-entry.json').read_text())['files']
    changes = []
    for name, expected in entry.items():
        path = ROOT / name
        actual = digest(path) if path.is_file() else None
        if actual != expected:
            changes.append({'path': name, 'expected': expected, 'actual': actual})
    return {'checked_files': len(entry), 'changes': changes, 'passed': not changes}

def package_hashes(package):
    return {str(p.relative_to(package)): digest(p) for p in sorted(package.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}

receipt = {'source_baseline': 'work/analysis/model-evaluation-diagnostics/baseline.json', 'replay_reference': 'work/analysis/model-evaluation-diagnostics/check_and_pin.py', 'proposal': {}, 'preservation_before': preservation()}
original = ROOT / 'exploration/stellarator_e2e/generated'
receipt['source_baseline_sha256'] = digest(ROOT / receipt['source_baseline'])
for name in ['model_contract', 'package_contract']:
    contract = json.loads((original / 'contracts' / (name + '.json')).read_text())
    receipt[name + '_fingerprint'] = contract.get('semantic_fingerprint', contract.get('executable_fingerprint'))
before = package_hashes(original)
scratch = Path(tempfile.mkdtemp(prefix='stellaris-regression-'))
receipt['scratch'] = str(scratch)
package = scratch / 'stellarator_tea'
shutil.copytree(original, package, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
receipt['copied_package_exact'] = before == package_hashes(package)
try:
    from simkit.study.bridge import CandidateBridge
    import study_route
    evaluator = study_route.prepare(package, scratch / 'evaluation')
    row = evaluator.evaluate(CandidateBridge(evaluator.entry_models).build({}))
    actual = {'outputs': dict(row.outputs), 'responses': dict(row.responses)}
    Path(str(PREFIX) + '-actual.json').write_text(json.dumps(actual, indent=2) + '\n')
    expected = json.loads((ROOT / receipt['source_baseline']).read_text())
    differences = {section: [key for key in set(actual[section]) | set(expected[section]) if actual[section].get(key) != expected[section].get(key)] for section in actual}
    receipt['behavior'] = {'executed': True, 'exact_match': not any(differences.values()), 'differences': differences, 'output_count': len(actual['outputs']), 'response_count': len(actual['responses'])}
except Exception as exc:
    receipt['behavior'] = {'executed': False, 'exception_type': type(exc).__name__, 'message': str(exc), 'traceback': traceback.format_exc()}
receipt['original_package_preserved'] = before == package_hashes(original)
receipt['preservation_after'] = preservation()
Path(str(PREFIX) + '-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
