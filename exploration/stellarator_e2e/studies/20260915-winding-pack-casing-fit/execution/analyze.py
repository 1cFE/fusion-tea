"""Verify mapped numerics, old predicates and entering attribution; summarize fit."""
import json
import math
from pathlib import Path

H = Path(__file__).resolve().parents[1]
R = H / 'results'
P = 'stellarator_09__stellaris__'
read = lambda path: json.loads(path.read_text())


def write(name, value):
    (R / name).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def close(a, b):
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)


rows = read(R / 'native-cases.json')
byid = {row['proposal_id']: row for row in rows}
scan = {row['proposal_id']: row for row in read(R / 'oracle-scan.json')['rows']}
catalog = read(R / 'predicate-catalog.json')
params = read(H / 'preparation/resolved-defaults.json')
props = {row['id']: row for row in read(H / 'preparation/proposals.json')}
fit = next(cid for cid, entry in catalog.items() if entry['source_local_identity'] == 'wp_fit_ok')
oldcatalog = {entry['constraint_id']: entry for entry in read(H / 'preparation/entering/generated/contracts/model_contract.json')['constraint_catalog']['concrete_entries']}
assert len(oldcatalog) == 18
assert oldcatalog == {cid: entry for cid, entry in catalog.items() if cid != fit}
failures, scalars, predicates, worst = [], 0, 0, 0.0
for row in rows:
    want = scan[row['proposal_id']]
    assert row['inputs'] == want['point']
    assert len(want['channels']) == 196
    for key, value in want['channels'].items():
        got = row['outputs'][key]
        scalars += 1
        worst = max(worst, abs(got - value) / max(abs(got), abs(value), 1e-100))
        if not close(got, value):
            failures.append({'proposal_id': row['proposal_id'], 'channel': key, 'native': got, 'oracle': value})
    assert set(row['verdicts']) == set(want['verdicts']) == set(catalog)
    for cid, value in want['verdicts'].items():
        predicates += 1
        if row['verdicts'][cid] != value:
            failures.append({'proposal_id': row['proposal_id'], 'constraint_id': cid})
write('oracle-all-points.json', {'outcome': 'pass' if not failures else 'fail',
      'cases': len(rows), 'mapped_channels_per_case': 196, 'scalar_comparisons': scalars,
      'predicate_comparisons': predicates, 'max_relative_deviation': worst, 'failures': failures,
      'unmapped_native_channels': sorted(set(rows[0]['outputs']) - set(next(iter(scan.values()))['channels']))})
assert not failures, failures[:5]

comparisons, unchanged, verdict_checks = [], 0, 0
for filename in ('comparison.json', 'allocation-comparison.json'):
    entering = read(H / 'preparation/entering' / filename)
    for before in entering['rows']:
        proposal = props[before['id']]
        row = byid[proposal['canonical_proposal_id']]
        assert proposal['original_point'] == before['point']
        changes, flips = {}, {}
        for key, value in before['channels'].items():
            assert key in row['outputs']
            if close(row['outputs'][key], value):
                unchanged += 1
            else:
                changes[key] = {'before': value, 'after': row['outputs'][key]}
        for cid, entry in oldcatalog.items():
            verdict_checks += 1
            value = before['verdicts'][entry['source_local_identity']]
            if row['verdicts'][cid] != value:
                flips[cid] = {'before': value, 'after': row['verdicts'][cid]}
        comparisons.append({'proposal_id': before['id'], 'source_file': filename,
                            'candidate_id': row['candidate_id'], 'entering_point': before['point'],
                            'resolved_candidate_point': row['inputs'], 'scalar_comparisons': len(before['channels']),
                            'changed_channels': changes, 'old_verdict_flips': flips,
                            'fit_verdict': row['verdicts'][fit]})
write('comparison-entering.json', {'scope': 'Matched entering independent-oracle captures, not native execution of the old package',
      'entering_revision': entering['revision'], 'matched_cases': len(comparisons),
      'original_nominal_cases': sum(row['source_file'] == 'comparison.json' for row in comparisons),
      'allocation_cases': sum(row['source_file'] == 'allocation-comparison.json' for row in comparisons),
      'unchanged_scalar_comparisons': unchanged, 'old_predicate_comparisons': verdict_checks,
      'old_predicate_catalog_exact_equal': True, 'new_predicate': fit,
      'cases': comparisons, 'outcome': 'pass' if all(not row['changed_channels'] and not row['old_verdict_flips'] for row in comparisons) else 'fail'})
assert len(comparisons) == 72
assert all(not row['changed_channels'] and not row['old_verdict_flips'] for row in comparisons)


def val(row, suffix):
    return row['outputs'][P + suffix]


def summarize(row):
    full = params | row['inputs']
    return {'proposal_id': row['proposal_id'], 'candidate_id': row['candidate_id'],
            'inputs': row['inputs'], 'lcoe': val(row, 'lcoe_calc__lcoe'),
            'allocation_m': full[P + 'magnet__coil__coil_t'],
            'density_ratio': full[P + 'magnet__winding_pack__j_wp'] / params[P + 'magnet__winding_pack__j_wp'],
            'feasible_18': all(row['verdicts'][cid] == 'satisfied' for cid in oldcatalog),
            'fit_satisfied': row['verdicts'][fit] == 'satisfied',
            'feasible_19': all(value == 'satisfied' for value in row['verdicts'].values()),
            'violated': [catalog[cid]['source_local_identity'] for cid, value in row['verdicts'].items() if value != 'satisfied'],
            'fit_dimensions_m': {key.removeprefix(P + 'magnet__wp_fit__'): value for key, value in row['outputs'].items() if key.startswith(P + 'magnet__wp_fit__')},
            'tape_length_m': val(row, 'magnet__winding_procurement__tape_length'),
            'tape_cost': val(row, 'magnet__winding_procurement__tape_cost'),
            'refrigeration_MW': val(row, 'cryoplant__refrigeration_sum__total'),
            'support_mass_kg': val(row, 'magnet__support_mass__m_support')}


summaries = {row['proposal_id']: summarize(row) for row in rows}


def family_summary(ids):
    selected = [summaries[key] for key in sorted(set(ids))]
    passed18 = [row for row in selected if row['feasible_18']]
    passed19 = [row for row in selected if row['feasible_19']]
    cheapest18 = min(passed18, key=lambda row: row['lcoe']) if passed18 else None
    cheapest19 = min(passed19, key=lambda row: row['lcoe']) if passed19 else None
    return {'unique_cases': len(selected), 'feasible_18': len(passed18), 'feasible_19': len(passed19),
            'fit_passes': sum(row['fit_satisfied'] for row in selected),
            'lost_feasibility': [row for row in selected if row['feasible_18'] and not row['feasible_19']],
            'feasible_19_cases': passed19, 'cheapest_without_fit': cheapest18, 'cheapest_with_fit': cheapest19,
            'cheapest_lcoe_shift': cheapest19['lcoe'] - cheapest18['lcoe'] if cheapest18 and cheapest19 else None,
            'lcoe_range': [min(row['lcoe'] for row in selected), max(row['lcoe'] for row in selected)],
            'margin_x_range_m': [min(row['fit_dimensions_m']['margin_x'] for row in selected), max(row['fit_dimensions_m']['margin_x'] for row in selected)],
            'margin_y_range_m': [min(row['fit_dimensions_m']['margin_y'] for row in selected), max(row['fit_dimensions_m']['margin_y'] for row in selected)]}


families = {family: family_summary([row['canonical_proposal_id'] for row in props.values() if row['family'] == family])
            for family in sorted({row['family'] for row in props.values()})}
geometry_checks = []
old_outputs = {row['channel_name'] for row in read(H / 'preparation/entering/generated/contracts/model_contract.json')['outputs'] if row['python_type'] in ('float', 'int')}
for proposal in props.values():
    if 'anchor_id' not in proposal:
        continue
    row = byid[proposal['canonical_proposal_id']]
    anchor = byid[props[proposal['anchor_id']]['canonical_proposal_id']]
    changes = [key for key in old_outputs if not close(row['outputs'][key], anchor['outputs'][key])]
    flips = [cid for cid in oldcatalog if row['verdicts'][cid] != anchor['verdicts'][cid]]
    assert not changes and not flips
    geometry_checks.append({'proposal_id': proposal['id'], 'anchor_id': proposal['anchor_id'],
                            'old_scalar_comparisons': len(old_outputs), 'old_predicate_comparisons': len(oldcatalog),
                            'changed_old_channels': changes, 'old_verdict_flips': flips})
write('geometry-isolation.json', {'outcome': 'pass', 'scope': 'New geometry controls compared with native allocation anchor; numerical isolation, not independent validation of unchanged old quantities',
                                'cases': geometry_checks, 'scalar_comparisons': len(old_outputs) * len(geometry_checks),
                                'predicate_comparisons': len(oldcatalog) * len(geometry_checks)})

responses = {}
for group in read(H / 'axes.json')['groups']:
    keys = [entry['key'] for entry in group['keys']]
    grouped = {}
    for row in rows:
        inputs = params | row['inputs']
        signature = json.dumps({key: value for key, value in inputs.items() if key not in keys}, sort_keys=True)
        grouped.setdefault(signature, []).append(row)
    blocks = []
    for members in grouped.values():
        if len(members) > 1:
            blocks.append({'points': [summaries[row['proposal_id']] | {'axis_value': row['inputs'][keys[0]]}
                                     for row in sorted(members, key=lambda row: row['inputs'][keys[0]])]})
    responses[group['axis']] = blocks
write('axis-responses.json', responses)
base = summaries[props['baseline']['canonical_proposal_id']]
write('analysis.json', {'baseline': base, 'unique_cases': len(rows), 'report_rows': len(props),
      'overall': family_summary(byid), 'families': families,
      'allocation_by_value': {str(value): family_summary([row['canonical_proposal_id'] for row in props.values()
                             if row['family'] == 'allocation-nominal-geometry' and row['point'][P + 'magnet__coil__coil_t'] == value]) for value in (0.4, 0.5, 0.6)},
      'violation_counts': {cid: sum(row['verdicts'][cid] != 'satisfied' for row in rows) for cid in catalog},
      'cases': list(summaries.values())})
print('PASS', scalars, 'mapped scalar and', predicates, 'predicate comparisons;', unchanged, 'entering scalars and', verdict_checks, 'entering old verdicts')
for name, family in families.items():
    print(name, family['unique_cases'], 'cases; old/new passes', family['feasible_18'], family['feasible_19'])
