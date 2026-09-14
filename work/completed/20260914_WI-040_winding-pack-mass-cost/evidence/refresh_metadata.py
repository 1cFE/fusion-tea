"""Re-derive WI-040's current snapshot, census, manifest pin and graph fixtures."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from scripts.study import indicators, manifest
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot


def main():
    package = ROOT / 'exploration/stellarator_e2e/generated'
    capture_instance_graph_snapshot([ROOT / 'exploration/stellarator_e2e/models'], ROOT / 'exploration/stellarator_e2e/stellarator.snapshot.json')
    contract = json.loads((package / 'contracts/model_contract.json').read_text())
    by_type = {}
    for row in contract['parameters']:
        by_type.setdefault(row['entry_type'], []).append(row['qualified_name'])
    census = {'derived_against_semantic_fingerprint': contract['semantic_fingerprint'],
              'entry_points': len(contract['parameters']),
              'by_entry_type': {k: sorted(v) for k, v in by_type.items()}}
    census_path = ROOT / 'tests/models/data/mfe_census.json'
    old_census = json.loads(census_path.read_text())
    census_path.write_text(json.dumps(census, indent=2) + '\n')
    path = ROOT / 'exploration/stellarator_e2e/studies/manifest.json'
    data = json.loads(path.read_text())
    old = data['fingerprints']
    pin = manifest.indicator_input_fingerprint(package)
    data['fingerprints'] = {'indicator_inputs': {**pin, 'files': [r['path'] for r in pin['files']]},
                            'recorded_provenance': {'executable_fingerprint': manifest.read_executable_fingerprint(package),
                                                    'semantic_fingerprint': manifest.read_semantic_fingerprint(package)}}
    # The native baseline is evaluated separately before this value is adopted.
    baseline = HERE.parent / 'baseline-after.json'
    if baseline.exists():
        evaluated = json.loads(baseline.read_text())
        assert evaluated['executable_fingerprint'] == data['fingerprints']['recorded_provenance']['executable_fingerprint']
        headline = data['baseline']['headline']
        headline['value'] = evaluated['channels'][headline['channel']]
    path.write_text(json.dumps(manifest.validate(data), indent=1) + '\n')
    loaded = manifest.load(path)
    manifest.assert_package_identity(loaded, package)
    manifest.assert_pin_matches(loaded, pin)
    axes = ROOT / 'tests/study/data/axes.known_answers.json'
    report = indicators.build_report(package, loaded, indicators.read_axis_declaration(axes), [])
    contracts = {}
    for group in report['groups']:
        axis = group['axis']
        payload = {'derived_against_semantic_fingerprint': contract['semantic_fingerprint'], 'group': group}
        (axes.parent / f'{axis}.expected.json').write_text(json.dumps(payload, indent=1) + '\n')
        contracts[axis] = [group['no_constraint_response'],
                           sorted(c['source_local_identity'] for c in group['constraints_reachable']),
                           group['objectives_reachable'], group['trace_size']['modules_fired'], group['trace_size']['channels_tainted']]
    (HERE / 'derived-fixture-contract.json').write_text(json.dumps(contracts, indent=2) + '\n')
    (HERE / 'metadata-refresh.json').write_text(json.dumps({'before': old, 'after': data['fingerprints'],
        'census_before': old_census['entry_points'], 'census_after': census['entry_points']}, indent=2) + '\n')
    print(json.dumps({'semantic': contract['semantic_fingerprint'], 'census': census['entry_points'],
                      'trace_counts': {k: v[-2:] for k, v in contracts.items()}}, indent=2))


if __name__ == '__main__':
    main()
