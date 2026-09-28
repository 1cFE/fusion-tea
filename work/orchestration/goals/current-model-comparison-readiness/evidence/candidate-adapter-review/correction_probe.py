"""Reviewer correction checks; preserve the original failure probes and receipts."""
import copy
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
HERE = ROOT / '.project/active/aries-comparison-preparation/current-readiness/candidate'
sys.path.insert(0, str(HERE))
from candidate_common import digest, exclusive_document, validate_rules
from execute_frozen import select_inputs
from build_freeze import safe_name
from check_accounting import check
from check_lineage import check as lineage

prior = json.loads(Path(__file__).with_name('probe.json').read_text())
rules = json.loads((HERE / 'input-rules.json').read_text())
receipt = {'refusals': {}, 'reviewed_hashes': {}}
def refuses(name, fn):
    try:
        fn()
    except (ValueError, AssertionError, FileExistsError) as error:
        receipt['refusals'][name] = f'{type(error).__name__}: {error}'
    else:
        raise AssertionError('unexpected acceptance: ' + name)

for name in prior['barred_path_strings_accepted']:
    refuses(name, lambda name=name: safe_name(name))
bad = copy.deepcopy(rules)
bad['forward_overrides'][rules['prefix'] + 'discount_rate'] = .02
refuses('extra_fixed_override', lambda: validate_rules(bad))
row = next(r for r in rules['independent_reference_inputs'] if r['key'].endswith('n_e0'))
request = {'run_kind': 'conditioned', 'conditioned_seam': 'table5_geometry_field',
           'values': {row['key']: {'value': row['default'], 'unit': row['unit'],
                       'source': 'synthetic', 'definition': 'synthetic', 'resolution': 'matched'}}}
refuses('table5_extra_input', lambda: select_inputs(rules, request))

temp = Path(tempfile.mkdtemp(prefix='candidate-correction-review-'))
path = temp / 'report.json'
path.write_bytes(b'original')
refuses('overwrite', lambda: exclusive_document(path, lambda: None))
assert path.read_bytes() == b'original'
sidecars = list(temp.glob('report.json.overwrite-refused-*/receipt.json'))
assert len(sidecars) == 1
receipt['overwrite_receipt'] = json.loads(sidecars[0].read_text())

candidate = temp / 'candidate'
candidate.mkdir()
(candidate / 'input-rules.json').write_text(json.dumps(rules))
(candidate / 'candidate-identity.json').write_text(json.dumps({'input_rules_sha256': 'bad-hash'}))
refuses('selected_rules_identity_hash', lambda: lineage(ROOT, candidate))

baseline = json.loads((ROOT / 'work/orchestration/goals/current-model-comparison-readiness/evidence/entering-validation/baseline/baseline_result.json').read_text())
adapted = {'state': 'completed', 'effective_inputs': rules['default_values'] | baseline['point'],
           'outputs': baseline['channels'], 'verdicts': {r['constraint_id']: r['status'] for r in baseline['verdicts']}}
native_path = temp / 'baseline.json'
native_path.write_text(json.dumps(adapted))
receipt['baseline_accounting'] = check(ROOT, native_path)
assert receipt['baseline_accounting']['status'] == 'pass'
adapted['outputs'][rules['prefix'] + 'buildings__not_declared__civil__cost_2025'] = 0.
native_path = temp / 'extra.json'
native_path.write_text(json.dumps(adapted))
refuses('extra_zero_facility_child', lambda: check(ROOT, native_path))

paths = list(prior['reviewed_hashes']) + [str((HERE / name).relative_to(ROOT)) for name in ('selection-policy.json', 'account-inventory.json')]
receipt['reviewed_hashes'] = {path: digest(ROOT / path) for path in paths}
Path(__file__).with_name('correction-probe.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'refusal_count': len(receipt['refusals']), 'baseline_accounting': receipt['baseline_accounting']['status']}, indent=2))
