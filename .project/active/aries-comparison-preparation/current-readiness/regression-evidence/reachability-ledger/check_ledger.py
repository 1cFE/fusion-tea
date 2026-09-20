"""Cross-check the authored ledger with reverse ancestor searches; no indicator API."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
graph = json.loads((HERE/'graph-ledger.json').read_text())
expected = json.loads((HERE/'current.expected.json').read_text())
modules = graph['modules']
producer = {channel: name for name, module in modules.items() for channel in module['outputs'].values()}


def ancestors_hit(refs, seeds):
    pending = list(refs)
    seen = set()
    while pending:
        ref = pending.pop()
        if ref in seeds:
            return True
        if ref in seen:
            continue
        seen.add(ref)
        if ref in producer:
            pending.extend(row['ref'] for row in modules[producer[ref]]['inputs'].values())
    return False


counts = {}
for group in expected['groups']:
    seeds = {row['key'] for row in group['declared_keys']}
    trace = graph['traces'][group['axis']]
    reverse_modules = {name for name, module in modules.items() if ancestors_hit([row['ref'] for row in module['inputs'].values()], seeds)}
    reverse_channels = {channel for channel in producer if ancestors_hit([channel], seeds)}
    assert reverse_modules == set(trace['fired_modules'])
    assert reverse_channels == set(trace['tainted_channels'])
    assert group['trace_size'] == {'modules_fired': len(reverse_modules), 'channels_tainted': len(reverse_channels)}
    assert len(group['bounds']) == 25
    assert sum(o['class'] != 'literal' for c in group['bounds'] for o in c['operands']) == 35
    assert all(o['reached'] == (o.get('ref') in seeds | reverse_channels) for c in group['bounds'] for o in c['operands'])
    assert group['objectives_reachable'] == sorted(name for name, channel in graph['objective_channels'].items() if channel in reverse_channels)
    counts[group['axis']] = group['trace_size'] | {'constraints_reached': len(group['constraints_reachable']), 'objectives_reached': len(group['objectives_reachable'])}
for path, digest in expected['sources_sha256'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, path
for path, digest in expected['historical_fixture_sha256'].items():
    content = (ROOT/path).read_bytes()
    assert hashlib.sha256(content).hexdigest() == digest, path
    assert json.loads(content)['derived_against_semantic_fingerprint'] == '8ea7a4c353455698deaa1026d3d3d547d572e08c6ceb58c2bb9cfea26c0120e0'
receipt = {'status': 'pass', 'checks': ['reverse ancestor searches agree for every module and channel on all eight axes', '25 predicates and 35 nonliteral operand occurrences per axis', 'all operand reached flags and objective lists agree', 'source hashes unchanged', 'historical five fixture bytes and original fingerprint unchanged'], 'counts': counts,
           'artifact_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('derive.py', 'current.expected.json', 'graph-ledger.json')}}
(HERE/'derivation-check.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
print(json.dumps(receipt, indent=2, sort_keys=True))
