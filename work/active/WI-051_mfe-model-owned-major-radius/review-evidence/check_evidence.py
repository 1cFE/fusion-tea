"""Independent record/contract check after isolated native execution replays."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

import yaml

ROOT = Path.cwd()
HERE = Path(__file__).resolve().parent
PROTOTYPE = HERE.parent / 'prototype'
REPLAY = Path(sys.argv[1])
PREFIX = 'stellarator_09__stellaris__'
OLD = ROOT / 'exploration/stellarator_e2e/generated'
NEW = PROTOTYPE / 'generated'

def read(path):
    return json.loads(path.read_text())

def digest(data):
    return hashlib.sha256(data).hexdigest()

frozen_hashes = {}
for name in ['results.json', 'inventory.json', 'checks.json', 'source-meaning.md']:
    committed = subprocess.check_output(['git', 'show', '2f8856b7:work/analysis/20260911-230953_radius-ownership-evidence/' + name])
    assert (PROTOTYPE / ('frozen-' + name)).read_bytes() == committed
    frozen_hashes[name] = digest(committed)
expectations = read(PROTOTYPE / 'expectations.json')
assert expectations['source_sha256'] == frozen_hashes
assert digest((PROTOTYPE / 'expectations.json').read_bytes()) == read(PROTOTYPE / 'execution-start.json')['expectations_sha256']
assert expectations['frozen_at'] < read(PROTOTYPE / 'execution-start.json')['utc']

old_records, new_records = [{(p['param_group'], p['qualified_name']): p for p in read(pkg / 'contracts/model_contract.json')['parameters']} for pkg in [OLD, NEW]]
retired = ('stellarator_plant_params', PREFIX + 'magnet__R0')
assert old_records.keys() - new_records.keys() == {retired}
assert not new_records.keys() - old_records.keys()
assert all(old_records[k] == v for k, v in new_records.items())
old_inputs, new_inputs = [{(p.stem, k): v for p in (pkg / 'inputs').glob('*.json') for k, v in read(p).items()} for pkg in [OLD, NEW]]
assert old_inputs.keys() - new_inputs.keys() == {retired}
assert not new_inputs.keys() - old_inputs.keys()
assert all(old_inputs[k] == v for k, v in new_inputs.items())
old_edges, new_edges = [{(m, f): v for m, row in yaml.safe_load((pkg / 'pipelines/pipeline.yaml').read_text())['modules'].items() for f, v in row.get('inputs', {}).items()} for pkg in [OLD, NEW]]
assert old_edges.keys() == new_edges.keys()
pairs = [('rb', 'R_in'), ('geom', 'R_in'), ('sustain', 'R_in'), ('divheat', 'R_in'), ('coil_length', 'R0'), ('field_calc', 'R0'), ('peak_field_calc', 'R_in'), ('magnet_cost', 'R0'), ('stored_energy', 'R0')]
for module, formal in pairs:
    assert new_edges[PREFIX + module, formal] == 'float stellarator_plant_params.' + PREFIX + 'R'
assert {k for k in old_edges if old_edges[k] != new_edges[k]} == {(PREFIX + m, f) for m, f in pairs[4:]}

frozen = read(PROTOTYPE / 'frozen-results.json')
actual = read(REPLAY / 'results.json')
comparison = {}
for case, old_case in [('baseline', 'baseline'), ('R14', 'tied_R14')]:
    expected = frozen['cases'][old_case]['native']
    row = actual[case]
    assert row['outputs'].keys() == expected['outputs'].keys()
    assert row['responses'] == expected['responses']
    comparison[case] = {}
    for channel, value in expected['outputs'].items():
        observed = row['outputs'][channel]
        assert observed == value if case == 'baseline' else math.isclose(observed, value, rel_tol=1e-9, abs_tol=1e-9)
        comparison[case][channel] = {'expected': value, 'actual': observed}
    assert row['report'] == expected['report']
    assert row == read(PROTOTYPE / 'results.json')[case]

ratios = {}
for channel, expected in {'geom__V': 14 / 12.7, 'coil_length__c_coil': 14 / 12.7, 'field_calc__B_axis': 12.7 / 14, 'stored_energy__W_mag': 12.7 / 14, 'peak_field_calc__B_peak': (12.7 - 3.1500000000000004) / (14 - 3.1500000000000004), 'magnet_cost__capital_cost': 1.0}.items():
    ratio = actual['R14']['outputs'][PREFIX + channel] / actual['baseline']['outputs'][PREFIX + channel]
    assert math.isclose(ratio, expected, rel_tol=1e-9, abs_tol=1e-9)
    ratios[channel] = {'expected': expected, 'actual': ratio}
for name, filename in [('source', 'source-hashes.json'), ('package', 'generated-hashes.json')]:
    base = PROTOTYPE / ('models' if name == 'source' else 'generated')
    for path, expected in read(PROTOTYPE / filename).items():
        assert digest((base / path).read_bytes()) == expected, path
for path, expected in read(PROTOTYPE / 'manual-preservation.json').items():
    assert digest((OLD / path).read_bytes()) == digest((NEW / path).read_bytes()) == expected

summary = {'frozen_source_hashes': frozen_hashes, 'old_count': len(old_records), 'new_count': len(new_records), 'removed': [retired], 'added': [], 'nine_pairs': pairs, 'baseline_and_R14_full_reports_exact': True, 'independent_ratios': ratios, 'complete_numeric_comparisons': comparison, 'prototype_source_package_hashes_verified': True, 'four_manual_hashes_verified': True}
(HERE / 'independent-checks.json').write_text(json.dumps(summary, indent=2) + '\n')
print('PASS immutable comparator hashes, pre-generation freeze, exact complete input delta, nine edges, every scalar/report, independent ratios, source/package and manual hashes')
