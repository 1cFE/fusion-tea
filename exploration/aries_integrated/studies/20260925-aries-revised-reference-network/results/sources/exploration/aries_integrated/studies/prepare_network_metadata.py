"""Re-pin the live study interface and manifest after WI-092; no native evaluation here.

Reads the WI-092 development receipt for the canonical mode-0 replay of the baseline point,
regenerates interface_data.py from the discovered inventory, and rewrites manifest.json with
the migrated baseline point (two new keys at defaults), the unchanged headline and verdicts,
and the new fingerprints. Frozen records are untouched.
"""
from __future__ import annotations
import importlib, json, pprint
from pathlib import Path
from scripts.study import common, manifest
from exploration.aries_integrated.studies import prepare_metadata, study_route as route

HERE = Path(__file__).resolve().parent
RECEIPT = HERE.parents[2] / 'work/active/WI-092_aries-parallel-exchanger-network/evidence/development-cases.json'
NEW_KEYS = {'aries_integrated_plant__heat_exchangers__network_mode': 0.0, 'aries_integrated_plant__heat_exchangers__pbli_split_fraction': 0.85}


def main():
    common.assert_tree_clean(route.PACKAGE_DIR)
    inventory = prepare_metadata.discover(route.PACKAGE_DIR)
    rows = json.loads(RECEIPT.read_text())
    nominal = next(r for r in rows if r['case'] == 'replay-nominal-calculated')
    if nominal['status'] != 'evaluated':
        raise ValueError('baseline replay must evaluate')
    fingerprint = inventory['fingerprints']['recorded_provenance']
    if nominal['fingerprint'] != fingerprint['executable_fingerprint']:
        raise ValueError('receipt does not describe the rebuilt executable')
    channels = {k: k for k, v in nominal['outputs'].items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
    constraints = {e['constraint_id']: e['source_local_identity'] for e in inventory['constraint_catalog']['concrete_entries']}
    interface = fingerprint | {'entry_keys': inventory['entry_keys'], 'channels': channels, 'constraints': constraints}
    (HERE / 'interface_data.py').write_text('"""Generated-artifact metadata; no physical arithmetic."""\nINTERFACE = ' + pprint.pformat(interface, sort_dicts=True) + '\n')
    importlib.invalidate_caches(); importlib.reload(importlib.import_module(route.INTERFACE_MODULE))
    from exploration.aries_integrated.studies import oracle_entry
    oracle_entry.operand_bindings()
    missing = set(oracle_entry.comparison_catalog()) - set(channels)
    if missing:
        raise ValueError(f'oracle catalog not published by model: {sorted(missing)}')
    old = json.loads((HERE / 'manifest.json').read_text())
    point = dict(old['baseline']['point']) | NEW_KEYS
    if set(point) != set(inventory['entry_keys']):
        raise ValueError('migrated baseline point does not match the entry keys: ' + str(set(point) ^ set(inventory['entry_keys'])))
    if point != nominal['effective_inputs']:
        raise ValueError('receipt baseline differs from the migrated manifest baseline')
    headline = old['baseline']['headline']
    if abs(nominal['outputs'][headline['channel']] - headline['value']) > 1e-9 * abs(headline['value']):
        raise ValueError('baseline headline changed; do not silently repin')
    fingerprints = inventory['fingerprints']
    fingerprints['indicator_inputs']['files'] = [x['path'] for x in fingerprints['indicator_inputs']['files']]
    document = old | {'fingerprints': fingerprints, 'baseline': old['baseline'] | {'point': point}}
    manifest.validate(document)
    common.write_document(document, HERE / 'manifest.json')
    print(json.dumps({'entry_keys': len(inventory['entry_keys']), 'channels': len(channels), **fingerprint}))


if __name__ == '__main__':
    main()
