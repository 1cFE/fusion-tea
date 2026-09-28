"""Thin single-arm diagnostic-attribution study support for the reconciliation goal.

Named designs compose explicit input changes on a canonical native map or on an earlier
design; no native evaluation happens during preparation or the oracle scan. The route,
executor, manifest schema, indicators, preflight and verifier are the stock ones.
"""
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
ROLES = ('assumed', 'operating', 'purchased', 'accounting', 'source')


def write_new(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def proposals(config, baseline, entry_keys, canonical):
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
        if axis['framing'] != 'sensitivity' or axis['role'] not in ROLES:
            raise ValueError('diagnostic axes are sensitivity-framed with a declared role: ' + axis['axis'])
    if set(baseline) != set(entry_keys):
        raise ValueError('incomplete baseline input map')
    rows, seen, points = [], set(), {}
    for design in config['designs']:
        name = design['name']
        if name in points:
            raise ValueError('duplicate design name: ' + name)
        if 'canonical_base' in design:
            base = canonical[design['canonical_base']]
        elif 'base_design' in design:
            base = points[design['base_design']]
        else:
            base = baseline
        if set(base) != set(entry_keys):
            raise ValueError('incomplete base map for ' + name)
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
        rows.append({'case': name, 'design': name, 'classification': design.get('classification', 'declared diagnostic'),
                     'arm': 'diagnostic', 'base': design.get('canonical_base') or design.get('base_design') or 'manifest-baseline',
                     'axis_values': design.get('values', {}), 'changes': changes, 'point': point})
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
        'canonical_receipt': str(PREDECESSOR.relative_to(HERE.parents[2]) / 'canonical-author-receipt.json'),
        'fingerprints': loaded.data['fingerprints'], 'native_evaluations': 0,
        'source_comparisons': 'Canonical source controls are copied verbatim; every other case composes declared changes on a named base.'}, loaded.data]):
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
    parser.add_argument('command', choices=['prepare', 'scan', 'baseline', 'execute'])
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
    elif args.command == 'baseline':
        out = args.record / 'preparation'
        out.mkdir(exist_ok=True)
        paths = route.execute_baseline(out, manifest_path=(args.record / 'manifest.json').resolve())
        result = {k: str(v) for k, v in paths.items()}
    else:
        if args.integration_return is None:
            parser.error('execute requires --integration-return')
        route.MANIFEST_PATH = (args.record / 'manifest.json').resolve()
        execute = runpy.run_path(str(PREDECESSOR / 'execute_study.py'))['execute']
        result = execute(args.record, args.integration_return)
    if result is not None:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
