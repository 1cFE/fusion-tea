"""Retained synthetic native checks; never reads reference requests or observations."""
import importlib.util
import json
from pathlib import Path

V1 = Path(__file__).resolve().parent.parent / 'v1'
HERE = Path(__file__).resolve().parent / 'final'
HERE.mkdir(exist_ok=False)
spec = importlib.util.spec_from_file_location('adapter', V1 / 'adapter.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def request(name, values):
    path = HERE / (name + '.request.json')
    a.document(path, {'schema_version': 'adapter-request/v1', 'purpose': 'synthetic_preparation', 'values': values})
    return path


def record(key, value):
    r = next(r for r in a.strict((V1 / 'mapping.json').read_bytes())['inputs'] if r['key'] == key)
    return {'value': value, 'unit': r['unit'], 'definition': r['definition'], 'resolution': 'matched', 'source': 'synthetic fixture from model defaults; no reference observations'}


key = a.P + 'magnet__coil__turn_current'
default = request('default', {})
wrong = record(a.P + 'plasma__n_e0', 5e20)
wrong['definition'] = 'volume_average_density'
incompatible = request('incompatible', {a.P + 'plasma__n_e0': wrong})
missing = request('missing', {key: record(key, 49000)})
domain = request('domain', {key: record(key, 65000)})
results = {}
for name, path in [('incompatible', incompatible), ('default', default), ('missing', missing), ('domain', domain)]:
    results[name] = a.execute(path, HERE / 'attempts', name)
    print(name, results[name]['state'], results[name].get('error', ''), flush=True)
# Simulate an interrupted reservation; completion of a later attempt cannot replace it.
a.reserve(HERE / 'interrupted-store', 'interrupted')
results['after_interruption'] = a.execute(default, HERE / 'interrupted-store', 'later-success')
a.document(HERE / 'native-summary.json', {k: {x: v.get(x) for x in ('state', 'error', 'first_attempt', 'candidate_id', 'executable_fingerprint', 'native_failure_records')} for k, v in results.items()})
assert results['incompatible']['state'] == 'execution_refused'
assert results['default']['state'] == 'completed'
assert results['missing']['state'] == 'completed' and results['missing']['held_fallback']
assert results['domain']['state'] != 'completed'
assert results['domain']['native_execution_started'] and results['domain'].get('native_failure_records')
assert results['default']['first_attempt']['attempt'] == 'incompatible'
assert results['after_interruption']['state'] == 'completed'
assert results['after_interruption']['first_attempt']['attempt'] == 'interrupted'
base = results['default']['effective_inputs']
changed = results['missing']['effective_inputs']
assert {k for k in base if base[k] != changed[k]} == {key}
assert all(r['value'] is None for r in a.strict((HERE / 'attempts/domain/model-export.json').read_bytes())['rows'])
geometry = request('undefined-breeding', {a.P + 'plasma__R': record(a.P + 'plasma__R', 12.6)})
results['undefined_breeding'] = a.execute(geometry, HERE / 'attempts', 'undefined-breeding')
assert results['undefined_breeding']['state'] == 'completed'
exported = {r['id']: r for r in a.strict((HERE / 'attempts/undefined-breeding/model-export.json').read_bytes())['rows']}
assert exported['achieved_tbr']['status'] == 'undefined_prediction'
assert exported['tbr_margin']['value'] is None
assert exported['raw_fuel']['status'] == 'mapped'
a.document(HERE / 'definedness-summary.json', {k: exported[k] for k in ('achieved_tbr', 'required_tbr', 'tbr_margin', 'raw_fuel')})
print('All native synthetic, definedness and custody checks passed.', flush=True)
assert 'conductor' in json.dumps(results['domain']['native_failure_records']).lower()
