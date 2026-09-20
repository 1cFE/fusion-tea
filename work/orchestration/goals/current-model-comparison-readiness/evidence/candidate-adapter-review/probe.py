"""Bounded reviewer probes. Uses synthetic data and existing admitted baseline only."""
import copy
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
HERE = ROOT / '.project/active/aries-comparison-preparation/current-readiness/candidate'
OUT = Path(__file__).parent
sys.path.insert(0, str(HERE))
from candidate_common import exclusive_document, validate_rules
from execute_frozen import select_inputs
from build_freeze import safe_name

rules = json.loads((HERE / 'input-rules.json').read_text())
receipt = {}
key = rules['prefix'] + 'plasma__n_e0'
declared = next(r for r in rules['independent_reference_inputs'] if r['key'] == key)
request = {'run_kind': 'conditioned', 'conditioned_seam': 'table5_geometry_field',
           'values': {key: {'value': declared['default'], 'unit': declared['unit'],
                            'source': 'synthetic reviewer fixture', 'definition': 'declared field', 'resolution': 'matched'}}}
point, classified = select_inputs(rules, request)
receipt['table5_nonempty_independent_values_accepted'] = classified['supplied_input_keys']

bad = copy.deepcopy(rules)
bad['conditioned_seams'] = []
bad['forward_overrides'][rules['prefix'] + 'discount_rate'] = 0.02
point, _ = select_inputs(bad, {'run_kind': 'verification', 'values': {}})
receipt['undeclared_fixed_override_accepted'] = {k: point[k] for k in point if k not in rules['forward_overrides']}

temp = Path(tempfile.mkdtemp(prefix='candidate-adapter-review-'))
path = temp / 'existing.json'
path.write_bytes(b'original')
try:
    exclusive_document(path, lambda: {'state': 'should not run'})
except FileExistsError:
    receipt['existing_document_after_refusal'] = {'bytes': path.read_text(), 'files': sorted(p.name for p in temp.iterdir())}

# Path strings only: no barred source is opened.
names = ['knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/example.txt',
         'exploration/concept_analysis/analyses/09-qi-stellarator-hts/example.txt',
         'knowledge/sources/aries_cost_account_documentation/example.txt',
         'knowledge/research/pending/20260912-115614_stellaris-structural-behavioral-modeling.md']
receipt['barred_path_strings_accepted'] = [str(safe_name(name)) for name in names]

from check_accounting import check
baseline = json.loads((ROOT / 'work/orchestration/goals/current-model-comparison-readiness/evidence/entering-validation/baseline/baseline_result.json').read_text())
adapted = {'state': 'completed', 'effective_inputs': rules['default_values'] | baseline['point'],
           'outputs': baseline['channels'], 'verdicts': {r['constraint_id']: r['status'] for r in baseline['verdicts']}}
native_path = temp / 'adapted-baseline.json'
native_path.write_text(json.dumps(adapted))
receipt['baseline_accounting'] = check(ROOT, native_path)

# Accounting should assert the enumerated child inventory, even for zero contributions.
extra = rules['prefix'] + 'buildings__not_a_declared_facility__civil__cost_2025'
adapted['outputs'][extra] = 0.0
native_path = temp / 'extra-facility-child.json'
native_path.write_text(json.dumps(adapted))
receipt['extra_zero_facility_child_accounting_status'] = check(ROOT, native_path)['status']
from candidate_common import schema_declarations, digest
contract = json.loads((ROOT / rules['package_path'] / 'contracts/model_contract.json').read_text())
declarations = schema_declarations(ROOT / rules['package_path'], contract['parameters'])
assert declarations == rules['input_types']
receipt['actual_schema_declaration_count'] = len(declarations)
adapted['outputs'].pop(extra)
adapted['requested_overrides'] = baseline['point']
native_path = temp / 'baseline-selected-check.json'
native_path.write_text(json.dumps(adapted))
from check_selected_mode import check as check_selected
receipt['baseline_selected_check'] = check_selected(ROOT, native_path)
receipt['reviewed_hashes'] = {str((HERE / name).relative_to(ROOT)): digest(HERE / name) for name in (
    'candidate_common.py', 'execute_frozen.py', 'refresh_contract.py', 'check_lineage.py',
    'export_model_values.py', 'check_accounting.py', 'check_selected_mode.py', 'build_freeze.py',
    'input-rules.json', 'manifest.json', 'constraint-inventory.json')}
receipt['reviewed_hashes']['tests/test_current_comparison_candidate.py'] = digest(ROOT / 'tests/test_current_comparison_candidate.py')

# Synthetic native result tests error custody; it executes no physical model.
import os
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))
from exploration.stellarator_e2e.studies import study_route
from execute_frozen import execute
import check_lineage
bad_outputs = dict(baseline['channels'])
bad_outputs[next(iter(bad_outputs))] = float('nan')
case = SimpleNamespace(state='completed', candidate_id='synthetic', executable_fingerprint='synthetic',
                       outputs=bad_outputs, verdicts=adapted['verdicts'])
run_dir = temp / 'synthetic-nonfinite-native'
with patch.object(check_lineage, 'check', return_value={'status': 'synthetic_identity_stub'}), \
     patch.object(study_route, 'run_points', return_value=([case], run_dir / 'native/study.sqlite3')), \
     patch.object(study_route, 'short_verdicts', return_value={}):
    try:
        execute(ROOT, HERE / 'input-rules.json', {'run_kind': 'verification', 'values': {}}, run_dir)
    except Exception as error:
        receipt['nonfinite_native_serialization_failure'] = {
            'error': f'{type(error).__name__}: {error}',
            'result_bytes': (run_dir / 'native-result.json').read_text(),
            'identity_receipt_exists': run_dir.with_name(run_dir.name + '.identity.json').exists(),
            'native_execution': 'stubbed; no physical model run'}
(OUT / 'probe.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: (v['status'] if k in ('baseline_accounting', 'baseline_selected_check') else v) for k, v in receipt.items() if k != 'reviewed_hashes'}, indent=2))
