"""Study support for costed_loop_brayton_tea (goal design-study-parameters): compose declared full input points on the
manifest baseline, scan them with the package-owned oracle, choose the declared sensitivity anchors from that scan, execute
the pinned baseline through the route, and run the declared list through the stock executor after an integration CANDIDATE
exists. No plant arithmetic here.

A study configuration (`flow_ratio_config.py` writes config.json) declares its axes (entry-key groups with metadata), the
flow x ratio grid, the inventories and the sensitivity levels; every case is a complete input map composed on the manifest
baseline by declared axis values, so nothing is optimized and no rating is changed from a demand. The proposal composer is
the ARIES reconciliation composer's rule set (`exploration/aries_integrated/studies/reconciliation_support.py`) restated
without its sealed-base branch and with the search framing admitted for the two swept axes.

Run (from the repository root, through the launcher):
  study_support.py prepare  --record <record> --config <record>/config.json
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
P = 'costed_loop_brayton__plant__'
NET = P + 'electrical__evaluate__net_electric'
UNMET = P + 'heat_exchangers__evaluate__unmet_heat'
TOLERANCE = P + 'checks__energy_tolerance'
LCOE = P + 'lifecycle_price__evaluate__lcoe'
BYPASS = P + 'return_control__evaluate__bypass_fraction'
FEASIBLE = P + 'return_control__evaluate__feasible'
MARGINS = {name: P + key for name, key in (
    ('compressor', 'compressor_capacity__evaluate__margin'), ('turbine', 'turbine_capacity__evaluate__margin'),
    ('generator', 'generator_capacity__evaluate__margin'), ('rejection', 'rejection_capacity__evaluate__margin'),
    ('he_duty', 'he_capacity__evaluate__margin'), ('loop', 'primary_loop__evaluate__capacity_margin'),
    ('fuel_stock', 'fuel_inventory__screen__margin'))}


def write_new(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def case_name(prefix, flow, ratio):
    return f'{prefix}-f{flow:g}-r{ratio:.4f}'


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
                     'arm': design.get('arm', 'main'), 'sensitivity': design.get('sensitivity'), 'anchor': design.get('anchor'),
                     'base': design.get('base_design', 'manifest-baseline'),
                     'axis_values': design.get('values', {}), 'changes': changes, 'point': point})
    return {'study_id': config['study_id'], 'cases': rows}


def boundary_designs(config, baseline, entry_keys):
    """Arrangement A's consistent settings: for each declared flow, the ratio at which the bypass fraction just exceeds a
    tiny target (the exchanger exactly matched, the heat-removal boundary), found by bisection on the oracle within a
    declared bracket; the found ratio becomes the case's chosen input. A flow whose bracket's lower end is already
    feasible (the boundary lies outside the window) is recorded as such and not solved."""
    from exploration.costed_loop_brayton.studies import oracle_entry
    b = config['boundary']
    grid = config['grid_axes']
    inventory = config['inventories'][b['inventory']]['values']
    target = float(b['target_bypass_fraction'])
    designs, log = [], []

    def probe(flow, ratio):
        design = {'name': 'probe', 'values': {grid['flow_axis']: flow, grid['ratio_axis']: ratio} | inventory}
        point = proposals(config | {'designs': [design]}, baseline, entry_keys)['cases'][0]['point']
        try:
            v = oracle_entry.evaluate(point)
        except Exception as error:
            return None, str(error)
        return (v[FEASIBLE] >= 1.0, v[BYPASS], v[NET]), None

    for flow, (lo, hi) in ((float(f), tuple(map(float, b['brackets'][str(int(f))]))) for f in b['flows']):
        plo, elo = probe(flow, lo)
        phi, ehi = probe(flow, hi)
        entry = {'flow': flow, 'bracket': [lo, hi], 'target_bypass_fraction': target}
        if plo is None or phi is None:
            entry['outcome'] = 'refused at a bracket end: ' + str(elo or ehi)
        elif plo[0] and plo[1] > target:
            entry['outcome'] = 'boundary below the bracket (window edge); lower end already feasible with f=%.3e' % plo[1]
        elif not phi[0]:
            entry['outcome'] = 'upper end infeasible; no boundary in the bracket'
        else:
            a, c = lo, hi
            for _ in range(200):
                m = 0.5 * (a + c)
                pm, _ = probe(flow, m)
                if pm is None:
                    entry['outcome'] = 'refused inside the bracket'; break
                if pm[0] and pm[1] > target:
                    c = m
                else:
                    a = m
                if c - a < 1e-10:
                    break
            pc, _ = probe(flow, c)
            entry.update({'outcome': 'solved', 'ratio': c, 'bypass_fraction_by_oracle': pc[1], 'net_by_oracle': pc[2], 'iterations_interval': c - a})
            designs.append({'name': f"ir-boundary-f{flow:g}", 'arm': 'boundary', 'classification': 'arrangement A: the exchanger exactly matched at this flow (bypass fraction at the target), ratio solved on the oracle',
                            'values': {grid['flow_axis']: flow, grid['ratio_axis']: c} | inventory})
        log.append(entry)
    return designs, log


def grid_designs(config):
    grid = config['grid']
    designs = []
    for arm, inventory in config['inventories'].items():
        for flow in grid['flows']:
            for ratio in grid['ratios']:
                designs.append({'name': case_name(arm, flow, ratio), 'arm': arm, 'classification': inventory['label'],
                                'values': {grid['flow_axis']: flow, grid['ratio_axis']: ratio} | inventory['values']})
    return designs


def passing(point, values):
    """Every check satisfied, read from the oracle's own operands: net positive, unmet heat within the energy tolerance,
    every rating and stock margin nonnegative, the loop flow within its rated ceiling."""
    return values[NET] > 0 and values[UNMET] <= point[TOLERANCE] and all(values[key] >= 0 for key in MARGINS.values())


def scan_rows(rows):
    from exploration.costed_loop_brayton.studies import oracle_entry
    scanned = {}
    for row in rows:
        try:
            values = oracle_entry.evaluate(row['point'])
        except Exception as error:  # the bodies' own guards, mirrored by the oracle
            scanned[row['case']] = {'status': 'refused', 'error': str(error)}
            continue
        scanned[row['case']] = {'status': 'evaluated', 'passing': passing(row['point'], values), 'net': values[NET],
                                'unmet': values[UNMET], 'lcoe': values[LCOE], 'bypass_fraction': values.get(BYPASS), 'feasible': values.get(FEASIBLE),
                                'margins': {name: values[key] for name, key in MARGINS.items()}}
    return scanned


def choose_anchors(config, grid, scanned):
    sens = config['sensitivities']
    flows, ratios = sorted(config['grid']['flows']), sorted(config['grid']['ratios'])
    start = (float(sens['starting_point']['cycle_flow']), float(sens['starting_point']['stage_ratio']))
    best = None
    for design in grid:
        row = scanned[design['name']]
        if design['arm'] != 'ir' or row['status'] != 'evaluated' or not row['passing']:
            continue
        flow, ratio = design['values'][config['grid']['flow_axis']], design['values'][config['grid']['ratio_axis']]
        if best is None or row['net'] > best[0]:
            best = (row['net'], flow, ratio)
    if best is None:
        raise ValueError("no all-checks-passing I-R point on the grid: the contract's fallback question applies")
    net, flow, ratio = best
    points = {'starting-point': start, 'best-passing': (flow, ratio)}
    if ratios.index(ratio) > 0:
        points['ratio-step-lower'] = (flow, ratios[ratios.index(ratio) - 1])
    if flows.index(flow) + 1 < len(flows):
        points['flow-step-higher'] = (flows[flows.index(flow) + 1], ratio)
    for extra in sens.get('extra_anchors', []):
        points[extra['label']] = (float(extra['cycle_flow']), float(extra['stage_ratio']))
    return {'rule': sens['anchor_rule'], 'best_passing_net_by_oracle': net, 'points': {k: list(v) for k, v in points.items()}}


def sensitivity_designs(config, anchors, baseline):
    axes = {a['axis']: a for a in config['axes']}
    grid = config['grid']

    def resolve(level):
        values = dict(level.get('values', {}))
        for axis_name, scale in level.get('scales', {}).items():
            values[axis_name] = baseline[axes[axis_name]['keys'][0]['key']] * float(scale)
        return values

    designs = {}

    def add(level, flow, ratio, anchor):
        name = case_name(level['id'], flow, ratio)
        if name not in designs:
            designs[name] = {'name': name, 'arm': 'sensitivity', 'sensitivity': level['sensitivity'], 'anchor': anchor,
                             'classification': f"{level['sensitivity']} {level['id']} at {anchor} on I-R",
                             'values': {grid['flow_axis']: flow, grid['ratio_axis']: ratio} | resolve(level)}

    for level in config['sensitivities']['levels']:
        for label, (flow, ratio) in anchors['points'].items():
            add(level, flow, ratio, label)
    levels = {level['id']: level for level in config['sensitivities']['levels']}
    for column in config['sensitivities'].get('columns', []):
        for ratio in column['ratios']:
            add(levels[column['level']], float(column['flow']), float(ratio), 'column')
    return list(designs.values())


def prepare(record, config_path):
    config = common.read_json(config_path, 'audited study configuration')
    if record.name != config['study_id']:
        raise ValueError('record name and study_id differ')
    common.assert_tree_clean(route.PACKAGE_DIR)
    loaded = manifest.load(route.MANIFEST_PATH)
    manifest.assert_pin_matches(loaded, manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    baseline, entry_keys = loaded.data['baseline']['point'], route.interface()['entry_keys']
    grid = (grid_designs(config) if 'grid' in config else []) + list(config.get('designs', []))
    grid_rows = proposals(config | {'designs': grid}, baseline, entry_keys)['cases']
    scanned = scan_rows(grid_rows)
    anchors = choose_anchors(config, grid, scanned) if 'sensitivities' in config else {'rule': 'none', 'points': {}}
    sens = sensitivity_designs(config, anchors, baseline) if 'sensitivities' in config else []
    boundary_log = []
    if 'boundary' in config:
        boundary, boundary_log = boundary_designs(config, baseline, entry_keys)
        sens = sens + boundary
    rows = proposals(config | {'designs': grid + sens}, baseline, entry_keys)['cases']
    scanned.update(scan_rows(rows[len(grid_rows):]))
    kept = [row for row in rows if scanned[row['case']]['status'] == 'evaluated']
    refused = {row['case']: scanned[row['case']]['error'] for row in rows if scanned[row['case']]['status'] == 'refused'}
    groups = {'schema_version': 'study-axis-declaration/v1', 'groups': [
        {'axis': a['axis'], 'keys': a['keys'], 'note': a['basis']} for a in config['axes']]}
    record.mkdir(parents=True, exist_ok=True)
    paths = ['proposed-points.json', 'axes.json', 'axis-plan.json', 'oracle-window-scan.json', 'preparation-provenance.json', 'manifest.json']
    if any((record / p).exists() for p in paths):
        raise ValueError('preparation exists; preserve it')
    documents = [
        {'study_id': config['study_id'], 'cases': kept},
        groups,
        config | {'expanded_designs': grid + sens, 'anchors': anchors, 'boundary_solve': boundary_log, 'refused_by_oracle_scan': refused},
        {'kind': 'independent-oracle-only', 'fingerprints': loaded.data['fingerprints'], 'anchors': anchors,
         'cases': [{'case': row['case'], 'arm': row['arm'], 'axis_values': row['axis_values']} | scanned[row['case']] for row in rows]},
        {'manifest_sha256': hashlib.sha256(route.MANIFEST_PATH.read_bytes()).hexdigest(),
         'config_sha256': hashlib.sha256(Path(config_path).read_bytes()).hexdigest(),
         'fingerprints': loaded.data['fingerprints'], 'native_evaluations': 0,
         'composition': 'Every case is a complete input map composed on the manifest baseline by declared axis values; the '
                        'sensitivity anchors are chosen from the oracle scan by the declared rule; cases the oracle refuses are '
                        'excluded from the executed list and reported as the scanned edge; nothing is optimized.'},
        loaded.data]
    for name, value in zip(paths, documents):
        write_new(record / name, value)
    return {'record': str(record), 'composed': len(rows), 'executed_list': len(kept), 'refused': len(refused), 'anchors': anchors['points']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'baseline', 'execute'])
    parser.add_argument('--record', type=Path, required=True)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--integration-return', type=Path)
    args = parser.parse_args()
    record = args.record.resolve()
    if args.command == 'prepare':
        if args.config is None:
            parser.error('prepare requires --config')
        print(json.dumps(prepare(record, args.config), indent=2))
    elif args.command == 'baseline':
        out = record / 'preparation'
        out.mkdir(exist_ok=True)
        print(json.dumps({k: str(v) for k, v in route.execute_baseline(out, manifest_path=(record / 'manifest.json').resolve()).items()}, indent=2))
    else:
        if args.integration_return is None:
            parser.error('execute requires --integration-return')
        route.MANIFEST_PATH = (record / 'manifest.json').resolve()
        from exploration.costed_loop_brayton.studies.execute_study import execute
        execute(record, args.integration_return)


if __name__ == '__main__':
    main()
