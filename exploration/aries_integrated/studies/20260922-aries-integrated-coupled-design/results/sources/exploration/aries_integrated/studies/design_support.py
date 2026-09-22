"""Thin paired-study preparation; no native evaluation during preparation or scan."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import runpy

from exploration.aries_integrated.studies import study_route as route
from scripts.study import common, manifest

HERE = Path(__file__).resolve().parent
PREDECESSOR = HERE / '20260922-aries-integrated-lcoe'
P = 'aries_integrated_plant__'
FEED = P + 'fuel_inventory__annual_recovery_kg'
SERVICE = P + 'finance__supply_service_annual'
SCENARIOS = {'no-credit': (0., 0.), 'feed100-service30m': (100., 30e6)}


def write_new(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def proposals(config, baseline, entry_keys, canonical=None):
    """Apply only explicitly declared groups; coordinator supplies audited membership."""
    axes = {a['axis']: a for a in config['axes']}
    if not axes or len(axes) != len(config['axes']):
        raise ValueError('nonempty unique axis declarations required')
    all_keys = set()
    for axis in axes.values():
        keys = [k['key'] for k in axis['keys']]
        if not keys or len(keys) != len(set(keys)) or not set(keys) <= set(entry_keys):
            raise ValueError('invalid entry group: ' + axis['axis'])
        if all_keys.intersection(keys) or {FEED, SERVICE}.intersection(keys):
            raise ValueError('overlapping groups or fixed supply scenario used as axis')
        all_keys.update(keys)
        for field in ('units', 'role', 'framing', 'window_provenance', 'basis', 'missing_response'):
            if not axis.get(field):
                raise ValueError('missing axis metadata: ' + field)
        if axis['framing'] not in ('search', 'sensitivity'):
            raise ValueError('unknown framing')
        if axis['role'] == 'assumed' and axis['framing'] != 'sensitivity':
            raise ValueError('assumptions are sensitivity-only')
    if set(baseline) != set(entry_keys):
        raise ValueError('incomplete baseline input map')
    rows, seen, names = [], set(), set()
    for design in [{'name': 'baseline', 'values': {}, 'classification': 'assumed integrated baseline'}] + config['designs']:
        if design['name'] in names:
            raise ValueError('duplicate design name')
        names.add(design['name'])
        changes = {}
        for name, value in design['values'].items():
            axis = axes[name]
            if axis.get('declined', False):
                raise ValueError('declined axis cannot be varied')
            if isinstance(value, bool) or not math.isfinite(float(value)):
                raise ValueError('axis requires a finite numeric value')
            changes.update({k['key']: float(value) for k in axis['keys']})
        for scenario, (feed, service) in SCENARIOS.items():
            base = (canonical or {})[design['canonical_base']] if 'canonical_base' in design else baseline
            if set(base) != set(entry_keys):
                raise ValueError('incomplete canonical base')
            point = {k: float(v) for k, v in base.items()} | changes | {FEED: feed, SERVICE: service}
            key = tuple(sorted(point.items()))
            if key in seen:
                raise ValueError('duplicate full point; remove redundant declared design')
            seen.add(key)
            rows.append({'case': design['name'] + '--' + scenario, 'design': design['name'],
                         'classification': design.get('classification', 'declared design'),
                         'arm': scenario, 'axis_values': design['values'], 'changes': changes,
                         'point': point})
    return {'study_id': config['study_id'], 'cases': rows}


def prepare(record, config_path):
    config = common.read_json(config_path, 'audited study configuration')
    if record.name != config['study_id']:
        raise ValueError('record name and study_id differ')
    common.assert_tree_clean(route.PACKAGE_DIR)
    loaded = manifest.load(route.MANIFEST_PATH)
    manifest.assert_pin_matches(loaded, manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    receipt = common.read_json(PREDECESSOR / 'canonical-author-receipt.json', 'canonical native receipt')
    if any(r['fingerprint'] != route.interface()['executable_fingerprint'] for r in receipt):
        raise ValueError('canonical receipt executable differs')
    proposal = proposals(config, loaded.data['baseline']['point'], route.interface()['entry_keys'],
                         {r['case']: r['effective_inputs'] for r in receipt})
    groups = {'schema_version': 'study-axis-declaration/v1', 'groups': [
        {'axis': a['axis'], 'keys': a['keys'], 'note': a['basis']} for a in config['axes']]}
    record.mkdir(parents=True, exist_ok=True)
    paths = ['proposed-points.json', 'axes.json', 'axis-plan.json', 'preparation-provenance.json', 'manifest.json']
    if any((record / p).exists() for p in paths):
        raise ValueError('preparation exists; preserve it')
    for name, value in zip(paths, [proposal, groups, config, {
        'manifest_sha256': hashlib.sha256(route.MANIFEST_PATH.read_bytes()).hexdigest(),
        'fingerprints': loaded.data['fingerprints'], 'native_evaluations': 0,
        'source_comparisons': 'Named canonical source controls preserve native inputs and pair the fixed supply scenarios.'}, loaded.data]):
        write_new(record / name, value)
    return {'cases': len(proposal['cases']), 'record': str(record)}


def scan(record):
    from exploration.aries_integrated.studies import oracle_entry
    loaded = manifest.load(record / 'manifest.json')
    manifest.assert_pin_matches(loaded, manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    common.assert_tree_clean(route.PACKAGE_DIR)
    rows = []
    for row in common.read_json(record / 'proposed-points.json', 'proposals')['cases']:
        try:
            rows.append({'case': row['case'], 'status': 'evaluated', 'values': oracle_entry.evaluate(row['point'])})
        except Exception as error:
            rows.append({'case': row['case'], 'status': 'refused', 'error': str(error)})
    write_new(record / 'oracle-window-scan.json', {'kind': 'independent-oracle-only',
              'fingerprints': loaded.data['fingerprints'], 'cases': rows})
    return {'scanned': len(rows), 'refused': sum(r['status'] == 'refused' for r in rows)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'scan', 'execute'])
    parser.add_argument('--record', type=Path, required=True)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--integration-return', type=Path)
    args = parser.parse_args()
    if args.command == 'prepare':
        if args.config is None:
            parser.error('prepare requires --config')
        result = prepare(args.record, args.config)
    elif args.command == 'scan':
        result = scan(args.record)
    else:
        if args.integration_return is None:
            parser.error('execute requires --integration-return')
        # Reuse reviewed full-numeric-map exporter and stock StudyRunner unchanged.
        route.MANIFEST_PATH = (args.record / 'manifest.json').resolve()
        execute = runpy.run_path(str(PREDECESSOR / 'execute_study.py'))['execute']
        result = execute(args.record, args.integration_return)
    if result is not None:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
