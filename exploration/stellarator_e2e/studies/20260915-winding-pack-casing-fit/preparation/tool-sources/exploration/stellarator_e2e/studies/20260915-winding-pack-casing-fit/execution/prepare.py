"""After explicit release, capture candidate evidence and resolve proposal coordinates."""
import json
import shutil
from pathlib import Path

H = Path(__file__).resolve().parents[1]
ROOT = H.parents[3]
PREP = H / 'preparation'


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def main():
    release = read(PREP / 'execution-release.json')
    candidate = read(PREP / 'integration-return.json')
    assert release['authorized_by'] == 'coordinator'
    assert candidate['class'] == 'CANDIDATE'
    assert all(gate['status'] == 'pass' for gate in candidate['gates'])
    assert release['candidate_pin'] == candidate['candidate']['pin']
    from exploration.stellarator_e2e.studies import study_route as route
    from scripts.study.verify import package_input_values
    from scripts.study.common import assert_tree_clean
    assert_tree_clean(route.PACKAGE_DIR)
    for name in ('manifest.json', 'oracle_entry.py', 'ANNEX.md', 'study_route.py'):
        shutil.copy2(H.parent / name, PREP / name)
    for name in ('verify_stellaris.py', 'oracle_finance.py'):
        shutil.copy2(H.parent.parent / name, PREP / name)
    for name in ('contracts', 'inputs', 'pipelines', 'schemas'):
        shutil.copytree(route.PACKAGE_DIR / name, PREP / ('package-' + name), dirs_exist_ok=True)
    manifest = read(PREP / 'manifest.json')
    assert manifest['fingerprints']['recorded_provenance']['executable_fingerprint'] == candidate['candidate']['executable_fingerprint']
    assert manifest['fingerprints']['recorded_provenance']['semantic_fingerprint'] == candidate['candidate']['semantic_fingerprint']
    params = package_input_values(route.PACKAGE_DIR)
    write(PREP / 'resolved-defaults.json', params)
    contract = read(PREP / 'package-contracts/model_contract.json')
    required = sorted(row['channel_name'] for row in contract['outputs']
                      if row['python_type'] in ('float', 'int'))
    write(PREP / 'required-channels.json', required)
    expected = read(PREP / 'expected-fit-interface.json')
    assert set(expected['outputs']) <= set(required)
    assert len(params) == expected['expected_public_inputs']
    assert len(required) == expected['expected_native_numeric_outputs']
    catalog = contract['constraint_catalog']['concrete_entries']
    assert len(catalog) == expected['expected_total_predicates']
    matches = [row for row in catalog if row['constraint_id'] == expected['predicate_constraint_id']]
    assert len(matches) == 1
    assert matches[0]['source_local_identity'] == expected['predicate_source_local_identity']
    assert all(params[key] == value for key, value in expected['inputs'].items())
    axes = read(H / 'axes.json')['groups']
    keys = [entry['key'] for group in axes for entry in group['keys']]
    assert set(keys) <= set(params)
    rows = read(PREP / 'proposals-draft.json')
    unique, seen = [], {}
    for row in rows:
        original = manifest['baseline']['point'] if row.pop('use_exact_manifest_baseline', False) else row['point']
        row['original_point'] = original
        row['point'] = {key: params[key] for key in keys} | original
        signature = json.dumps(params | row['point'], sort_keys=True)
        if signature not in seen:
            seen[signature] = row['id']
            unique.append({'proposal_id': row['id'], 'point': row['point']})
        row['canonical_proposal_id'] = seen[signature]
    assert 0 < len(unique) <= 150
    write(PREP / 'proposals.json', rows)
    write(PREP / 'unique-proposals.json', unique)
    print(f'Resolved {len(rows)} report rows, {len(unique)} native proposals; no point evaluation.')


if __name__ == '__main__':
    main()
