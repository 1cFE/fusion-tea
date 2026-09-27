"""Prepare the WI-097 controlled-exchanger study interface from a native receipt.

No native evaluation occurs here. The generated inventory and an evaluated receipt
must share the executable fingerprint. The legacy replay baseline preserves the
old outputs/verdicts and records its actual new thermal failures; it is not a
passing controlled-design baseline. The objective catalog includes only channels
independently calculated by this package's oracle. Numerical classes below follow
WI-097's reviewed design and retain all inherited ARIES absolute classes.

Run with --receipt <native-controls.json> --case replay-nominal-calculated and
--phase interface, then --phase manifest, after the generated package is committed.
"""
from __future__ import annotations
import argparse
import importlib
import json
import pprint
from pathlib import Path

from scripts.study import common, manifest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PACKAGE_DIR = HERE.parent / 'exchanger_architecture_thermal_tea'
P = 'aries_integrated_plant__'
HEADLINE = P + 'lifecycle_price__evaluate__lcoe'
# Inherited classes are retained verbatim; their channel names are unchanged.
ABSOLUTE_TOLERANCES = json.loads((ROOT / 'exploration/aries_integrated/studies/manifest.json').read_text())['absolute_tolerances']
ABSOLUTE_TOLERANCES += [
    {'channel': P+'heat_exchangers__evaluate__closure_residual', 'value': 1e-7, 'units': 'MW',
     'basis': 'Native root termination 1e-8 MW plus roundoff; independent Brent root 1e-11 K. Numerical comparison only, below 1e-6 MW engineering solve contract.'},
]
for branch in ('he', 'pbli', 'divertor'):
    for field in ('hot_bound_margin', 'required_hot_margin', 'hot_terminal_difference', 'cold_terminal_difference',
                  'hot_approach_margin', 'cold_approach_margin', 'return_residual', 'return_residual_magnitude'):
        ABSOLUTE_TOLERANCES.append({'channel': P+'heat_exchangers__evaluate__'+branch+'_'+field,
            'value': 1e-7, 'units': 'K',
            'basis': 'Difference of order-1000 K temperatures from native 1e-8 MW cycle and 1e-10 MW control solves; allows float cancellation in saturated terminal gaps. Numerical agreement only; exact margin signs determine physical verdicts and 1e-6 K checks numerical return closure.'})
    for field in ('bypass_fraction', 'control_margin'):
        ABSOLUTE_TOLERANCES.append({'channel': P+'heat_exchangers__evaluate__'+branch+'_'+field,
            'value': 1e-9, 'units': '1',
            'basis': 'Control root fraction can approach zero; independent LMTD inverse versus native 1e-10 MW capability solve. Absolute scale below flow/split study resolution; no acceptance relaxation.'})
    ABSOLUTE_TOLERANCES.append({'channel': P+'heat_exchangers__evaluate__'+branch+'_capability_at_solution',
        'value': 1e-7, 'units': 'MW', 'basis': 'Finite transfer can approach zero; native 1e-10 MW controller solve and cycle 1e-8 MW termination. Below inherited heat-removal numerical contract.'})



def discover(package_dir: Path) -> dict:
    """Working inventory through the stock readers; loads no generated Python (the ARIES prepare_metadata.discover)."""
    from scripts.study import indicators
    package_dir = Path(package_dir).resolve()
    fingerprint = manifest.indicator_input_fingerprint(package_dir)
    parsed = indicators.read_pipelines(package_dir)
    graph = indicators.build_graph(parsed)
    contract = indicators.read_model_contract(package_dir)
    entries, point = {}, {}
    for module in parsed.modules.values():
        if module.module_type != 'EntryPoint':
            continue
        for group, port in module.inputs.items():
            values = common.read_json((module.file.parent / port.ref).resolve(), 'generated entry defaults')
            for key, value in values.items():
                assert key not in entries, key
                entries[key] = group
                point[key] = value
    assert set(entries) == set(graph.input_keys), 'entry mapping and native graph key set differ'
    return {'fingerprints': {'indicator_inputs': fingerprint, 'recorded_provenance': {
                'executable_fingerprint': manifest.read_executable_fingerprint(package_dir),
                'semantic_fingerprint': contract.semantic_fingerprint}},
            'entry_keys': dict(sorted(entries.items())), 'point': dict(sorted(point.items())),
            'produced_channels': dict(sorted(graph.producer.items())),
            'constraint_catalog': {'concrete_entries': contract.concrete_entries}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--case', help='Row name when receipt is a case list')
    parser.add_argument('--phase', choices=('interface', 'manifest'), required=True)
    args = parser.parse_args()
    common.assert_tree_clean(PACKAGE_DIR)
    inventory = discover(PACKAGE_DIR)
    receipt = json.loads(args.receipt.read_text())
    if isinstance(receipt, list):
        rows = [row for row in receipt if row['case'] == args.case]
        assert len(rows) == 1, '--case must select exactly one receipt row'
        receipt = rows[0]
    assert receipt['status'] == 'evaluated', 'the baseline receipt must evaluate'
    fingerprint = inventory['fingerprints']['recorded_provenance']
    assert receipt['fingerprint'] == fingerprint['executable_fingerprint'], 'receipt does not describe this executable'
    channels = {k: k for k, v in receipt['outputs'].items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
    constraints = {e['constraint_id']: e['source_local_identity'] for e in inventory['constraint_catalog']['concrete_entries']}
    interface = fingerprint | {'entry_keys': inventory['entry_keys'], 'channels': channels, 'constraints': constraints}
    if args.phase == 'interface':
        (HERE / 'interface_data.py').write_text('"""Generated-artifact metadata; no physical arithmetic."""\nINTERFACE = ' + pprint.pformat(interface, sort_dicts=True) + '\n')
        print(json.dumps({'phase': 'interface', 'entry_keys': len(inventory['entry_keys']), 'channels': len(channels), 'constraints': len(constraints), **fingerprint}))
        return
    recorded = importlib.import_module('exploration.exchanger_architecture.thermal_requirements.studies.interface_data').INTERFACE
    assert recorded == interface, 'interface_data.py is stale against the package; rerun --phase interface'
    oracle = importlib.import_module('exploration.exchanger_architecture.thermal_requirements.studies.oracle_entry')
    catalog = sorted(set(oracle.comparison_catalog()))
    missing = set(catalog) - set(channels)
    assert not missing, 'oracle catalog not published by the model: ' + str(sorted(missing))
    for cid, operands in oracle.operand_bindings().items():
        assert cid in constraints, cid
        for formal, binding in operands.items():
            if binding['kind'] == 'channel':
                assert binding['key'] in channels, (cid, formal, binding['key'])
            else:
                assert binding['key'] in inventory['entry_keys'], (cid, formal, binding['key'])
    point = {k: float(v) for k, v in receipt['effective_inputs'].items()}
    assert set(point) == set(inventory['entry_keys']), 'receipt inputs do not cover the entry keys'
    verdicts = [{'source_local_identity': constraints[r['constraint_id']], 'expected': r['status']} for r in receipt['outputs']['constraint_report']['results']]
    seen = set()
    unique = []
    for v in verdicts:  # the manifest names verdicts by local identity; the six capacity screens share one
        if v['source_local_identity'] in seen:
            assert v['expected'] == next(u['expected'] for u in unique if u['source_local_identity'] == v['source_local_identity'])
            continue
        seen.add(v['source_local_identity']); unique.append(v)
    fingerprints = inventory['fingerprints']
    fingerprints['indicator_inputs']['files'] = [x['path'] for x in fingerprints['indicator_inputs']['files']]
    document = {
        'schema_version': manifest.MANIFEST_SCHEMA_VERSION,
        'package': {'name': manifest.read_package_name(PACKAGE_DIR), 'path': manifest.repo_relative_posix(PACKAGE_DIR)},
        'fingerprints': fingerprints,
        'objective_catalog': [{'name': c, 'channel': c} for c in catalog],
        'ties': [],
        'baseline': {'point': point, 'headline': {'channel': HEADLINE, 'value': float(receipt['outputs'][HEADLINE])}, 'verdicts': unique},
        'oracle': {'kind': 'python_callable', 'module': 'exploration.exchanger_architecture.thermal_requirements.studies.oracle_entry', 'callable': 'evaluate', 'sys_path': '.'},
        'absolute_tolerances': ABSOLUTE_TOLERANCES,
    }
    manifest.validate(document)
    common.write_document(document, HERE / 'manifest.json')
    print(json.dumps({'phase': 'manifest', 'entry_keys': len(inventory['entry_keys']), 'channels': len(channels), 'catalog': len(catalog), 'constraints': len(constraints), 'headline': document['baseline']['headline'], **fingerprint}))


if __name__ == '__main__':
    main()
