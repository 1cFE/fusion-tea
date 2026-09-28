"""Write the study interface record and the manifest for costed_loop_brayton_tea from the discovered inventory and one
stored development receipt (the starting point on the re-selected inventory); no native evaluation here.

The pattern is the ARIES `prepare_network_metadata.py`: the interface constant carries the executable and semantic
fingerprints, every entry key, every numeric output channel of the receipt and every emitted constraint id; the manifest
pins the indicator-input fingerprint, declares the baseline point (the receipt's effective inputs), its headline (the
LCOE) and expected verdicts (all satisfied), the oracle block and the absolute tolerance classes the comparison contract
declares (goal design-study-parameters, evidence/comparison-contract.md section 9).

Two phases, because the manifest's objective catalog is the oracle's comparison catalog (the verifier requires an independent
value for every catalogued channel) and the oracle needs the interface record first:
  --phase interface  writes interface_data.py from the inventory and the receipt;
  --phase manifest   writes manifest.json, with the objective catalog read from oracle_entry.comparison_catalog() and every
                     operand-binding channel checked against the published channels.

Run: .codex-test/run python exploration/costed_loop_brayton/studies/prepare_interface.py --phase interface --receipt <receipt>
     .codex-test/run python exploration/costed_loop_brayton/studies/prepare_interface.py --phase manifest --receipt <receipt>
"""
from __future__ import annotations
import argparse
import importlib
import json
import pprint
from pathlib import Path

from scripts.study import common, manifest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKAGE_DIR = HERE.parent / 'costed_loop_brayton_tea'
P = 'costed_loop_brayton__plant__'
HEADLINE = P + 'lifecycle_price__evaluate__lcoe'
ABSOLUTE_TOLERANCES = [
    {'channel': P + 'heat_exchangers__evaluate__closure_residual', 'value': 1e-07, 'units': 'MW',
     'basis': 'The ARIES manifest class for the same closure body (native root termination 1e-8 MW plus roundoff); declared before execution, comparison-contract.md section 9.'},
    {'channel': P + 'lifecycle_accounts__evaluate__idc', 'value': 1.9073486328125e-06, 'units': 'USD2004',
     'basis': 'Two ULP of the capital magnitude for the subtractive IDC diagnostic; the ARIES class for the same lifecycle body; declared before execution.'},
    {'channel': P + 'lifecycle_accounts__evaluate__curtailed_feed', 'value': 1e-09, 'units': 'kg/year', 'basis': 'The ARIES exact-zero difference class (economics goal L-004); declared before execution.'},
    {'channel': P + 'lifecycle_accounts__evaluate__external_shortfall', 'value': 1e-09, 'units': 'kg/year', 'basis': 'As above.'},
    {'channel': P + 'fuel_inventory__annual__annual_external', 'value': 1e-09, 'units': 'kg/year', 'basis': 'As above.'},
    {'channel': P + 'fuel_inventory__annual__annual_recovery', 'value': 1e-09, 'units': 'kg/year', 'basis': 'As above.'},
    # Owner ruling G-001 (2026-09-26): a verification tolerance on calculated temperature margins, never permission to accept a
    # physical constraint violation (work/orchestration/goals/design-study-parameters/evidence/owner-ruling-g001.md).
    {'channel': P + 'heat_exchangers__evaluate__he_hot_bound_margin', 'value': 1e-06, 'units': 'K',
     'basis': 'Two temperatures of order 700 K fixed by the closure root solve (1e-8 MW; the oracle root differs by about 3e-10 K) subtracted to a margin that can be arbitrarily small near the bound; owner ruling G-001; a verification tolerance only, the verdict is re-derived exactly from the operands.'},
    {'channel': P + 'heat_exchangers__evaluate__pbli_hot_bound_margin', 'value': 1e-06, 'units': 'K', 'basis': 'As above (G-001).'},
    {'channel': P + 'heat_exchangers__evaluate__divertor_hot_bound_margin', 'value': 1e-06, 'units': 'K', 'basis': 'As above (G-001).'},
    # WI-095 'Primary Bypass Control': declared before any study on the new identity executes.
    {'channel': P + 'return_control__evaluate__bypass_fraction', 'value': 1e-09, 'units': '1',
     'basis': 'The bypass fraction is a bisection root to |capability - duty| <= 1e-9 MW; two independent solves (package and oracle) agree to about 1e-12 in f, but a relative rule cannot pass a root near zero (the f = 0 family targets 1e-6); an absolute class at the solve resolution, declared before execution.'},
    {'channel': P + 'return_control__evaluate__return_residual', 'value': 1e-08, 'units': 'K',
     'basis': 'The root-solve closure (duty - capability(f)) / C_h, of order 1e-11 K when feasible (two solves within 1e-9 MW each give at most about 1e-10 K difference); a numerical class two orders below the check tolerance 1e-6 K, declared before execution; infeasible cases carry a physical deficit far above it and are compared relatively.'},
    {'channel': P + 'return_control__evaluate__return_residual_magnitude', 'value': 1e-08, 'units': 'K', 'basis': 'As above.'},
]


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
    parser.add_argument('--phase', choices=('interface', 'manifest'), required=True)
    args = parser.parse_args()
    common.assert_tree_clean(PACKAGE_DIR)
    inventory = discover(PACKAGE_DIR)
    receipt = json.loads(args.receipt.read_text())
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
    recorded = importlib.import_module('exploration.costed_loop_brayton.studies.interface_data').INTERFACE
    assert recorded == interface, 'interface_data.py is stale against the package; rerun --phase interface'
    oracle = importlib.import_module('exploration.costed_loop_brayton.studies.oracle_entry')
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
        'oracle': {'kind': 'python_callable', 'module': 'exploration.costed_loop_brayton.studies.oracle_entry', 'callable': 'evaluate', 'sys_path': '.'},
        'absolute_tolerances': ABSOLUTE_TOLERANCES,
    }
    manifest.validate(document)
    common.write_document(document, HERE / 'manifest.json')
    print(json.dumps({'phase': 'manifest', 'entry_keys': len(inventory['entry_keys']), 'channels': len(channels), 'catalog': len(catalog), 'constraints': len(constraints), 'headline': document['baseline']['headline'], **fingerprint}))


if __name__ == '__main__':
    main()
