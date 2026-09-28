"""Independent evidence author: YAML bindings + contract IR, no study-tool imports.

Run with .codex-test/run python <this file>. Writes only beside this file.
The traversal uses a bipartite vertex graph and a queue, not the indicator API.
"""
import collections
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent
PACKAGE = ROOT / 'exploration/stellarator_e2e/pkg/stellarator_tea'
PIPELINE = PACKAGE / 'pipelines/pipeline.yaml'
CONTRACT = PACKAGE / 'contracts/model_contract.json'
MANIFEST = ROOT / 'exploration/stellarator_e2e/studies/manifest.json'
AXES = ROOT / 'tests/study/data/axes.known_answers.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    contract = json.loads(CONTRACT.read_text())
    manifest = json.loads(MANIFEST.read_text())
    raw = yaml.safe_load(PIPELINE.read_text())['modules']
    entries = [m for m in raw.values() if m['module_type'] == 'EntryPoint']
    assert len(entries) == 1
    entry = entries[0]['inputs']
    parameters = {p['qualified_name']: p for p in contract['parameters']}
    files = [(PIPELINE.parent / v.split(maxsplit=1)[1]).resolve() for v in entry.values()]
    inputs = {}
    for path in files:
        for key, value in json.loads(path.read_text()).items():
            assert key not in inputs or inputs[key] == value
            inputs[key] = value

    def reference(declaration):
        _, token = declaration.split(maxsplit=1)
        if '.' in token and token.split('.', 1)[0] in entry:
            group, key = token.split('.', 1)
            assert key in inputs and key in parameters
            assert parameters[key]['param_group'] == group
            return 'bound', key
        token = token.removesuffix('.root')
        assert '.' not in token, token
        return 'computed', token

    modules = {}
    producers = {}
    consumers = collections.defaultdict(list)
    for name, module in raw.items():
        if module['module_type'] in ('EntryPoint', 'ExitPoint'):
            continue
        outputs = {port: value.split(maxsplit=1)[1] for port, value in module.get('outputs', {}).items()}
        bindings = {}
        for port, declaration in module.get('inputs', {}).items():
            kind, ref = reference(declaration)
            bindings[port] = {'class': kind, 'ref': ref, 'declaration': declaration}
            consumers[ref].append((name, port))
        modules[name] = {'module_type': module['module_type'], 'inputs': bindings, 'outputs': outputs}
        for channel in outputs.values():
            assert channel not in producers
            producers[channel] = name
    for module in modules.values():
        for binding in module['inputs'].values():
            assert binding['ref'] in (inputs if binding['class'] == 'bound' else producers), binding
    objectives = {row['name']: row['channel'] for row in manifest['objective_catalog']}
    assert all(channel in producers for channel in objectives.values())
    catalog = sorted(contract['constraint_catalog']['concrete_entries'], key=lambda e: e['constraint_id'])
    axes = json.loads(AXES.read_text())['groups']
    for name in ('p_wallplug_heat', 'eta_source_heat', 'eta_couple_heat'):
        axes.append({'axis': name, 'keys': [{'key': 'stellarator_09__stellaris__heating__' + name, 'provenance': 'fan_out'}]})
    groups = []
    traces = {}
    for axis in axes:
        keys = {row['key'] for row in axis['keys']}
        assert keys <= inputs.keys()
        reached = set(keys)
        todo = collections.deque(sorted(keys))
        fired = set()
        witnesses = {}
        while todo:
            ref = todo.popleft()
            for name, port in consumers[ref]:
                if name in fired:
                    continue
                fired.add(name)
                witnesses[name] = {'input_port': port, 'ref': ref}
                for channel in modules[name]['outputs'].values():
                    if channel not in reached:
                        reached.add(channel)
                        todo.append(channel)
        tainted = reached - keys

        bounds = []
        for constraint in catalog:
            name = constraint['constraint_id']
            ir = json.loads(constraint['predicate_ir'])
            operands = []

            def visit(node):
                if node['kind'] == 'operator':
                    for child in node['operands']:
                        visit(child)
                elif node['kind'] == 'literal':
                    operands.append({'operand': '<literal>', 'class': 'literal', 'reached': False, 'value': node['literal']['value']})
                elif node['kind'] == 'feature_ref':
                    assert not node['reference']['chain_segments']
                    port = node['reference']['source_name']
                    binding = modules[name]['inputs'][port]
                    ref = binding['ref']
                    row = {'operand': port, 'class': binding['class'], 'ref': ref, 'reached': ref in reached}
                    if binding['class'] == 'bound':
                        row['entry_type'] = parameters[ref]['entry_type']
                    operands.append(row)
                else:
                    raise AssertionError(node['kind'])

            visit(ir)
            classes = sorted({o['class'] for o in operands if o['class'] != 'literal'})
            bounds.append({k: constraint[k] for k in ('constraint_id', 'definition_qualified_name', 'source_local_identity')} | {
                'operator': ir['operator'], 'operand_classes': classes,
                'bound_vs_bound': classes == ['bound'], 'operands': operands})
        yes = [row for row in bounds if any(o['reached'] for o in row['operands'])]
        no = [row for row in bounds if not any(o['reached'] for o in row['operands'])]
        suffixes = {key.rsplit('__', 1)[-1] for key in keys}
        siblings = sorted(key for key in inputs if key not in keys and key.rsplit('__', 1)[-1] in suffixes)
        assert not siblings, siblings
        group = {'axis': axis['axis'], 'declared_keys': [row | {'entry_type': parameters[row['key']]['entry_type']} for row in axis['keys']],
                 'group_valid': True, 'no_constraint_response': not yes,
                 'constraints_reachable': yes, 'constraints_unreachable': no, 'bounds': bounds,
                 'objectives_reachable': sorted(name for name, channel in objectives.items() if channel in tainted),
                 'objectives_unreachable': sorted(name for name, channel in objectives.items() if channel not in tainted),
                 'sibling_candidates': [], 'trace_size': {'modules_fired': len(fired), 'channels_tainted': len(tainted)},
                 'warnings': [], 'not_derivable': {
                     'statements': ['monotonicity or sign of any response', 'same-quantity identity across differing key names', 'intra-module operand dependency (the trace is module-level)'],
                     'positive_reading': 'A reachable constraint or objective means a possible path exists in the module graph. It never means the axis responds.'}}
        groups.append(group)
        traces[axis['axis']] = {'fired_modules': sorted(fired), 'tainted_channels': sorted(tainted),
            'first_witness_per_module': witnesses,
            'reached_input_edges': [{'module': name, 'input_port': port, 'ref': binding['ref'], 'class': binding['class']}
                for name in sorted(fired) for port, binding in sorted(modules[name]['inputs'].items()) if binding['ref'] in reached]}
    sources = [PIPELINE, CONTRACT, MANIFEST, AXES, *files]
    historical = {str(p.relative_to(ROOT)): digest(p) for p in sorted((ROOT/'tests/study/data').glob('*.expected.json'))}
    metadata = {'authority': 'AGENT independent derivation; requires fresh review',
                'method': 'Queue traversal of authored YAML bipartite graph; predicate leaves from published IR; no indicator imports or calls',
                'derived_against_semantic_fingerprint': contract['semantic_fingerprint'],
                'sources_sha256': {str(p.relative_to(ROOT)): digest(p) for p in sources},
                'historical_fixture_sha256': historical}
    for filename, content in [('current.expected.json', metadata | {'groups': groups}),
                              ('graph-ledger.json', metadata | {'modules': modules, 'objective_channels': objectives,
                                  'predicate_ir': {e['constraint_id']: json.loads(e['predicate_ir']) for e in catalog}, 'traces': traces})]:
        (OUT/filename).write_text(json.dumps(content, indent=2, sort_keys=True)+'\n')
    for g in groups:
        print(g['axis'], g['trace_size'], [c['source_local_identity'] for c in g['constraints_reachable']], g['objectives_reachable'])


if __name__ == '__main__':
    main()
