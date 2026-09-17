"""Map retained native outputs to every frozen quantity without reference data."""
import argparse
import json
from pathlib import Path


def extract(manifest, contract, native):
    values = {p['qualified_name']: p['default_value'] for p in contract['parameters']}
    values.update(native.get('effective_inputs', {}))
    values.update(native.get('requested_overrides', {}))
    values.update(native.get('outputs', {}))
    # Native stores publish predicate verdicts separately from numeric outputs.
    for entry in contract['constraint_catalog']['concrete_entries']:
        verdict = native.get('verdicts', {}).get(entry['constraint_id'])
        if verdict in ('satisfied', 'violated'):
            values[entry['evaluation_channel']] = 1 if verdict == 'satisfied' else 0
    rows = []
    for q in manifest['quantities']:
        producers = q['producers']
        value, status = None, 'not_produced'
        if native.get('state') != 'completed':
            status = 'execution_not_completed'
        elif not producers:
            status = 'structural_evidence_required' if q['axis'] == 'structural' else 'not_produced'
        elif any(p not in values for p in producers):
            status = 'missing_producer'
        elif len(producers) == 1:
            value, status = values[producers[0]], 'mapped'
        elif q['calculation'] == 'sum of producers in cumulative radial order':
            value, status = sum(values[p] for p in producers), 'mapped'
        elif q['calculation'] == 'producer[0] - producer[1]' and len(producers) == 2:
            value, status = values[producers[0]]-values[producers[1]], 'mapped'
        else:
            raise ValueError(f"Unsupported frozen calculation for {q['id']}")
        role = q['role']
        role_input = q.get('role_input', producers[0] if len(producers) == 1 else None)
        if role_input in native.get('supplied_input_keys', []):
            role = 'supplied'
        elif role_input is not None and q['role'] in ('held', 'supplied'):
            role = 'held'
        rows.append({'id': q['id'], 'model_value': value, 'unit': q['unit'], 'status': status,
                     'role_at_this_point': role, 'producers': producers, 'reference_value': None,
                     'applicability': q['applicability']})
    return {'run_kind': native.get('run_kind'), 'candidate_id': native.get('candidate_id'),
            'execution_status': native.get('state'), 'quantities': rows,
            'held_fallback': native.get('held_fallback'),
            'missing_independent_inputs': native.get('missing_independent_inputs', []),
            'constraints': native.get('verdicts', {}), 'reference_values_loaded': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--native-result', type=Path, required=True)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    contract = json.loads((args.root / manifest['package_path'] / 'contracts/model_contract.json').read_text())
    result = extract(manifest, contract, json.loads(args.native_result.read_text()))
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False)+'\n')


if __name__ == '__main__':
    main()
