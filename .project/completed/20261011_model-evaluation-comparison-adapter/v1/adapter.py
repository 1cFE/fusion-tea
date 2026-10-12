"""Synthetic preparation only: exact input meanings, native evaluation, immutable attempts."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PACKAGE = ROOT / 'exploration/stellarator_e2e/generated'
HISTORICAL = ROOT / '.project/active/aries-comparison-preparation/current-readiness/candidate'
P = 'stellarator_09__stellaris__'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def retain(value):
    if isinstance(value, float) and not math.isfinite(value):
        return {'unavailable_nonfinite': repr(value)}
    if isinstance(value, complex):
        return {'unavailable_complex': repr(value)}
    if isinstance(value, dict):
        return {k: retain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [retain(v) for v in value]
    return value


def document(path, value):
    with Path(path).open('x') as stream:
        json.dump(retain(value), stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result

    def invalid(value):
        raise ValueError('nonfinite JSON constant: ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)


def identity_files():
    files = [p for p in PACKAGE.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    files += list((ROOT / 'models').rglob('*.sysml'))
    files += [p for p in HERE.iterdir() if p.suffix in ('.py', '.md', '.json') and p.name != 'identity.json']
    files += list((ROOT / 'scripts/study').glob('*.py'))
    files += [ROOT / 'exploration/stellarator_e2e/studies/study_route.py']
    files += [HISTORICAL / 'manifest.json', HISTORICAL / 'accounting-normalization.md']
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(set(files))}


def pin():
    """Explicit development act; existing versioned pins cannot be overwritten."""
    contract = strict((PACKAGE / 'contracts/package_contract.json').read_bytes())
    document(HERE / 'identity.json', {'schema_version': 'adapter-identity/v1',
             'files': identity_files(), 'executable_fingerprint': contract['executable_fingerprint']})


def verify_identity():
    expected = strict((HERE / 'identity.json').read_bytes())
    actual = identity_files()
    drift = sorted(k for k in actual.keys() | expected['files'].keys()
                   if actual.get(k) != expected['files'].get(k))
    if drift:
        raise ValueError('identity drift: ' + ', '.join(drift))
    for name in ('manifest.json', 'accounting-normalization.md'):
        if sha(HERE / ('historical-' + name)) != sha(HISTORICAL / name):
            raise ValueError('historical contract copy differs: ' + name)
    return expected


def defaults(contract):
    values = {}
    for path in sorted((PACKAGE / 'inputs').glob('*.json')):
        group = strict(path.read_bytes())
        if values.keys() & group.keys():
            raise ValueError('duplicate native input key')
        values.update(group)
    parameters = {p['qualified_name']: p for p in contract['parameters']}
    if set(values) != set(parameters):
        raise ValueError('native input/contract coverage differs')
    for key, parameter in parameters.items():
        value = values[key]
        if parameter['python_type'] == 'bool' and type(value) in (bool, int, float) and value in (0, 1):
            values[key] = bool(value)  # Generator defaults alone admit numeric Booleans.
        elif parameter['python_type'] in ('float', 'int') and type(value) in (int, float) and math.isfinite(value):
            pass
        else:
            raise ValueError('invalid typed native default: ' + key)
    return values


def select(request, base):
    if not isinstance(request, dict) or set(request) != {'schema_version', 'purpose', 'values'}:
        raise ValueError('request requires exactly schema_version, purpose and values')
    if request['schema_version'] != 'adapter-request/v1' or request['purpose'] != 'synthetic_preparation':
        raise ValueError('only versioned synthetic preparation is supported')
    rows = strict((HERE / 'mapping.json').read_bytes())['inputs']
    mapping = {row['key']: row for row in rows}
    supplied = request['values']
    if not isinstance(supplied, dict):
        raise ValueError('values must be an object')
    point = {}
    for key, record in supplied.items():
        if key == P + 'magnet__coil__I_coil':
            raise ValueError('ampere-turns do not select installed reference turns and per-turn operating current')
        if key not in mapping:
            raise ValueError('unknown or retired preparation input: ' + key)
        if not isinstance(record, dict) or set(record) != {'value', 'unit', 'definition', 'resolution', 'source'}:
            raise ValueError('input requires value, unit, definition, resolution and source: ' + key)
        row = mapping[key]
        if record['unit'] != row['unit'] or record['definition'] != row['definition'] or record['resolution'] != 'matched':
            raise ValueError('incompatible or ambiguous quantity definition/unit: ' + key)
        if not isinstance(record['source'], str) or not record['source'].strip():
            raise ValueError('synthetic fixture provenance required: ' + key)
        value = record['value']
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ValueError('finite non-Boolean scalar required: ' + key)
        if key not in base:
            raise ValueError('mapping key absent from current model: ' + key)
        point[key] = float(value)
    missing = sorted(set(mapping) - set(point))
    return point, {'missing_proposed_inputs': missing, 'held_fallback': bool(missing),
                   'fully_specified_preparation_controls': not missing,
                   'fully_reference_specified': False,
                   'effective_inputs': base | point,
                   'input_roles': {k: 'supplied' if k in point else 'held' for k in base}}


def reserve(store, name):
    store = Path(store).resolve()
    store.mkdir(parents=True, exist_ok=True)
    if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', name):
        raise ValueError('invalid attempt name')
    attempt = store / name
    attempt.mkdir(exist_ok=False)
    # A hard-link publishes a fully flushed pointer atomically and never replaces it.
    with tempfile.NamedTemporaryFile(mode='w', prefix='.reservation-', dir=store, delete=False) as stream:
        json.dump({'schema_version': 'first-attempt/v1', 'attempt': name}, stream)
        stream.flush()
        os.fsync(stream.fileno())
        temp = Path(stream.name)
    pointer = store / 'first-attempt.json'
    try:
        try:
            os.link(temp, pointer)
        except FileExistsError:
            pass
    finally:
        temp.unlink()
    first = strict(pointer.read_bytes())  # Corrupt pointer is a refusal, never an absent first.
    if set(first) != {'schema_version', 'attempt'} or first['schema_version'] != 'first-attempt/v1':
        raise ValueError('invalid first-attempt pointer')
    return attempt, first | {'pointer_sha256': sha(pointer)}


def export(native, manifest, contract=None):
    """Current-role overlay; calculated outputs never fall back to parameter defaults."""
    outputs, inputs = native.get('outputs', {}), native.get('effective_inputs', {})
    values = inputs | outputs
    if contract is not None:
        for entry in contract['constraint_catalog']['concrete_entries']:
            verdict = native.get('verdicts', {}).get(entry['constraint_id'])
            if verdict in ('satisfied', 'violated'):
                values[entry['evaluation_channel']] = verdict == 'satisfied'
    overlay = strict((HERE / 'current-overlay.json').read_bytes())
    rows = []
    for q in manifest['quantities']:
        producers = overlay['producer_overrides'].get(q['id'], q['producers'])
        value = None
        status = 'execution_not_completed'
        role = 'calculated'
        if len(producers) == 1 and producers[0] in inputs and producers[0] not in outputs:
            role = native['input_roles'][producers[0]]
        if native['state'] == 'completed':
            status = 'missing_producer'
            if not producers:
                status = 'structural_evidence_required'
            elif all(p in values for p in producers):
                if len(producers) == 1:
                    value = values[producers[0]]
                elif q['calculation'] == 'sum of producers in cumulative radial order':
                    value = sum(values[p] for p in producers)
                elif q['calculation'] == 'producer[0] - producer[1]' and len(producers) == 2:
                    value = values[producers[0]] - values[producers[1]]
                else:
                    raise ValueError('unsupported historical calculation: ' + q['id'])
                status = 'mapped'
        raw = value
        modes = q.get('availability_when', [])
        applicability = 'unknown' if any(c['input'] not in inputs for c in modes) else (
            'active' if all(inputs[c['input']] == c['equals'] for c in modes) else 'inactive')
        if status == 'mapped' and applicability != 'active':
            value, status = None, applicability + '_prediction'
        flags = overlay.get('defined_when', {}).get(q['id'], [])
        definedness = 'unknown' if any(k not in outputs or type(outputs[k]) not in (int, float, bool) or outputs[k] not in (0, 1) for k in flags) else (
            'defined' if all(outputs[k] == 1 for k in flags) else 'undefined')
        if status == 'mapped' and definedness != 'defined':
            value, status = None, definedness + '_prediction'
        rows.append({'id': q['id'], 'unit': q['unit'], 'value': value, 'raw_value': raw,
                     'status': status, 'role': role, 'applicability': applicability,
                     'producers': producers, 'definedness': definedness,
                     'defined_when': {k: outputs.get(k) for k in flags}, 'independent_prediction_credit': False})
    return {'schema_version': 'preparation-export/v1', 'rows': rows,
            'reference_values_loaded': False, 'publication_ready': False,
            'criteria_sha256': sha(HERE / 'historical-manifest.json')}


def native_run(point, attempt, contract):
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))
    from exploration.stellarator_e2e.studies import study_route as route
    channels = {p['channel_name']: p['channel_name'] for p in contract['outputs']
                if p['python_type'] in ('float', 'int', 'bool')}
    cases, db = route.run_points('adapter-preparation-v1', [point], attempt / 'native', PACKAGE,
                                 required_channels=channels)
    if len(cases) != 1:
        raise ValueError('expected exactly one retained native case')
    case = cases[0]
    result = {'state': case.state, 'outputs': dict(case.outputs), 'verdicts': dict(case.verdicts),
              'candidate_id': case.candidate_id, 'executable_fingerprint': case.executable_fingerprint,
              'evidence_digest': case.evidence_digest, 'assessment': case.assessment,
              'store': str(db.relative_to(attempt)), 'headline': case.headline}
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as connection:
        result['native_failure_records'] = [strict(row[0]) for row in connection.execute(
            'SELECT failure_json FROM cases WHERE failure_json IS NOT NULL')]
    document(attempt / 'native-case.json', result)
    if case.state == 'completed':
        route.require_published(case, channels)
        expected = {r['constraint_id'] for r in contract['constraint_catalog']['concrete_entries']}
        if set(case.outputs) != set(channels) or set(case.verdicts) != expected:
            raise ValueError('completed native output or predicate inventory mismatch')
        if any(v not in ('satisfied', 'violated') for v in case.verdicts.values()):
            raise ValueError('incomplete native predicate verdict')
    return result


def execute(request, store, name):
    attempt, first = reserve(store, name)
    result = {'schema_version': 'adapter-result/v1', 'state': 'execution_refused',
              'first_attempt': first, 'attempt': name, 'publication_ready': False,
              'reference_values_loaded': False, 'native_execution_started': False}
    stage = 'request_read'
    contract = None
    try:
        raw = Path(request).read_bytes()
        with (attempt / 'request.raw.json').open('xb') as stream:
            stream.write(raw)
        result['raw_request_sha256'] = sha(attempt / 'request.raw.json')
        stage = 'request_decode'
        parsed = strict(raw)
        stage = 'identity'
        identity = verify_identity()
        result['identity_sha256'] = sha(HERE / 'identity.json')
        result['expected_executable_fingerprint'] = identity['executable_fingerprint']
        contract = strict((PACKAGE / 'contracts/model_contract.json').read_bytes())
        stage = 'selection'
        point, selection = select(parsed, defaults(contract))
        result.update(selection, requested_overrides=point)
        document(attempt / 'selection.json', selection | {'requested_overrides': point})
        stage = 'native_execution'
        result['native_execution_started'] = True
        native = native_run(point, attempt, contract)
        result.update(native)
        stage = 'post_execution_identity'
        verify_identity()
        if result['executable_fingerprint'] != identity['executable_fingerprint']:
            raise ValueError('native executable differs from pinned identity')
        result['runtime'] = {'python': sys.version, 'executable': sys.executable,
                             'packages': {n: importlib.metadata.version(n) for n in ('sysml-codegen', 'agentic-mbse')},
                             'teax_source_files': {str(p): sha(p) for p in sorted((Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit/simkit').rglob('*.py'))}}
    except Exception as error:
        result.update(state='execution_refused', refusal_stage=stage,
                      error=f'{type(error).__name__}: {error}')
        with (attempt / 'exception.txt').open('x') as stream:
            stream.write(traceback.format_exc())
    # A raw retained native case and store remain even if later validation refuses.
    result['all_constraints_satisfied'] = bool(result.get('verdicts')) and result['state'] == 'completed' and all(
        v == 'satisfied' for v in result['verdicts'].values())
    document(attempt / 'result.json', result)
    document(attempt / 'model-export.json', export(result, strict((HERE / 'historical-manifest.json').read_bytes()), contract))
    document(attempt / 'receipt.json', {'first_attempt': first,
             'artifacts': {str(p.relative_to(attempt)): sha(p) for p in sorted(attempt.rglob('*')) if p.is_file()}})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pin', action='store_true')
    parser.add_argument('--request', type=Path)
    parser.add_argument('--store', type=Path)
    parser.add_argument('--attempt')
    args = parser.parse_args()
    if args.pin:
        pin()
        return 0
    if not all((args.request, args.store, args.attempt)):
        parser.error('--request, --store and --attempt are required')
    result = execute(args.request, args.store, args.attempt)
    print(result['state'])
    return 0 if result['state'] == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
