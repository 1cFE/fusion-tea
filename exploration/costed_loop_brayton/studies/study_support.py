"""Study support for costed_loop_brayton_tea (goal design-study-parameters): compose declared full input points on the
manifest baseline, scan them with the package-owned oracle, execute the pinned baseline through the route, and run the
declared list through the stock executor after an integration CANDIDATE exists. No plant arithmetic here.

A study configuration (config.json) declares its axes (each an entry-key group with metadata) and its designs; each design
names a base (the manifest baseline, or another design) and axis values; every case is a complete input map composed on
that base, so nothing is optimized and no rating is changed from demand. The proposal composer is the ARIES reconciliation
composer's rule set, restated here without its sealed-base branch (this package has no sealed studies yet).

Run (from the repository root, through the launcher):
  study_support.py prepare  --record <record> --config <record>/config.json
  study_support.py scan     --record <record>
  study_support.py baseline --record <record>
  study_support.py execute  --record <record> --integration-return <integration_return.json>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from scripts.study import common, manifest
from exploration.costed_loop_brayton.studies import study_route as route

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ROLES = {'operating', 'equipment', 'assumption', 'price', 'convention'}


def write_new(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def proposals(config, baseline, entry_keys):
    axes = {a['axis']: a for a in config['axes']}
    if not axes or len(axes) != len(config['axes']):
        raise ValueError('nonempty unique axis declarations required')
    all_keys = set()
    for axis in axes.values():
        keys = [k['key'] for k in axis['keys']]
        if not keys or len(keys) != len(set(keys)) or not set(keys) <= set(entry_keys):
            raise ValueError('invalid entry group: ' + axis['axis'])
        if all_keys.intersection(keys):
            raise ValueError('overlapping groups: ' + axis['axis'])
        all_keys.update(keys)
        for field in ('units', 'role', 'framing', 'window_provenance', 'basis', 'missing_response'):
            if not axis.get(field):
                raise ValueError('missing axis metadata: ' + field)
        if axis['framing'] not in ('search', 'sensitivity') or axis['role'] not in ROLES:
            raise ValueError('axes carry a framing and a declared role: ' + axis['axis'])
    if set(baseline) != set(entry_keys):
        raise ValueError('incomplete baseline input map')
    rows, seen, points = [], set(), {}
    for design in config['designs']:
        name = design['name']
        if name in points:
            raise ValueError('duplicate design name: ' + name)
        base = points[design['base_design']] if 'base_design' in design else baseline
        changes = {}
        for axis_name, value in design.get('values', {}).items():
            axis = axes[axis_name]
            if axis.get('declined', False):
                raise ValueError('declined axis cannot be varied: ' + axis_name)
            if isinstance(value, bool) or not math.isfinite(float(value)):
                raise ValueError('axis requires a finite numeric value: ' + axis_name)
            changes.update({k['key']: float(value) for k in axis['keys']})
        point = {k: float(v) for k, v in base.items()} | changes
        key = tuple(sorted(point.items()))
        if key in seen:
            raise ValueError('duplicate full point: ' + name)
        seen.add(key)
        points[name] = point
        rows.append({'case': name, 'design': name, 'classification': design.get('classification', 'declared point'),
                     'arm': design.get('arm', 'main'), 'base': design.get('base_design', 'manifest-baseline'),
                     'axis_values': design.get('values', {}), 'changes': changes, 'point': point})
    return {'study_id': config['study_id'], 'cases': rows}


def prepare(record, config_path):
    config = common.read_json(config_path, 'audited study configuration')
    if record.name != config['study_id']:
        raise ValueError('record name and study_id differ')
    common.assert_tree_clean(route.PACKAGE_DIR)
    loaded = manifest.load(route.MANIFEST_PATH)
    manifest.assert_pin_matches(loaded, manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    proposal = proposals(config, loaded.data['baseline']['point'], route.interface()['entry_keys'])
    groups = {'schema_version': 'study-axis-declaration/v1', 'groups': [
        {'axis': a['axis'], 'keys': a['keys'], 'note': a['basis']} for a in config['axes']]}
    record.mkdir(parents=True, exist_ok=True)
    paths = ['proposed-points.json', 'axes.json', 'axis-plan.json', 'preparation-provenance.json', 'manifest.json']
    if any((record / p).exists() for p in paths):
        raise ValueError('preparation exists; preserve it')
    for name, value in zip(paths, [proposal, groups, config, {
        'manifest_sha256': hashlib.sha256(route.MANIFEST_PATH.read_bytes()).hexdigest(),
        'fingerprints': loaded.data['fingerprints'], 'native_evaluations': 0,
        'composition': 'Every case is a complete input map composed on the manifest baseline (or a named design) by the declared axis values; nothing is optimized.'}, loaded.data]):
        write_new(record / name, value)
    return {'cases': len(proposal['cases']), 'record': str(record)}


def scan(record):
    from exploration.costed_loop_brayton.studies import oracle_entry
    loaded = manifest.load(record / 'manifest.json')
    manifest.assert_pin_matches(loaded, manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    common.assert_tree_clean(route.PACKAGE_DIR)
    rows = []
    for row in common.read_json(record / 'proposed-points.json', 'proposals')['cases']:
        try:
            rows.append({'case': row['case'], 'status': 'evaluated', 'values': oracle_entry.evaluate(row['point'])})
        except Exception as error:
            rows.append({'case': row['case'], 'status': 'refused', 'error': str(error)})
    write_new(record / 'oracle-window-scan.json', {'kind': 'independent-oracle-only', 'fingerprints': loaded.data['fingerprints'], 'cases': rows})
    return {'scanned': len(rows), 'refused': sum(r['status'] == 'refused' for r in rows)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'scan', 'baseline', 'execute'])
    parser.add_argument('--record', type=Path, required=True)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--integration-return', type=Path)
    args = parser.parse_args()
    record = args.record.resolve()
    if args.command == 'prepare':
        if args.config is None:
            parser.error('prepare requires --config')
        result = prepare(record, args.config)
    elif args.command == 'scan':
        result = scan(record)
    elif args.command == 'baseline':
        out = record / 'preparation'
        out.mkdir(exist_ok=True)
        paths = route.execute_baseline(out, manifest_path=(record / 'manifest.json').resolve())
        result = {k: str(v) for k, v in paths.items()}
    else:
        if args.integration_return is None:
            parser.error('execute requires --integration-return')
        route.MANIFEST_PATH = (record / 'manifest.json').resolve()
        from exploration.costed_loop_brayton.studies.execute_study import execute
        result = execute(record, args.integration_return)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
