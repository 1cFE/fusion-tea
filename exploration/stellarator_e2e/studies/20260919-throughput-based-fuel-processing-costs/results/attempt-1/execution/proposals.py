"""Resolve the proposed finite list only after the workflow releases the candidate."""
import json

P = 'stellarator_09__stellaris__'
AXES = {
    'burn': 'fuel_cycle__burn_fraction',
    'recovery': 'fuel_cycle__t_recycle',
    'density': 'plasma__n_e0',
    'downtime': 'unplanned_fraction',
    'price': 'fuel_cycle__processing_price_multiplier',
    'margin': 'fuel_cycle__processing_capacity_margin',
    'containment-date': 'fuel_cycle__processing_containment_cpi',
    'account-selection': 'fuel_cycle__processing_enabled',
}


def build(home, defaults):
    missing = {P + suffix for suffix in AXES.values()} - set(defaults)
    if missing:
        raise RuntimeError(f'Proposed ABI differs from released inputs: {sorted(missing)}')
    base = {P + suffix: defaults[P + suffix] for suffix in AXES.values()}
    groups = []
    for name, suffix in AXES.items():
        groups.append({'axis': suffix, 'note': f'{name}: public authored attribute; no tie to a different input. Complete fan-out must be checked against released pipelines before framing release.', 'keys': [{'key': P + suffix, 'provenance': 'fan_out'}]})
    (home / 'axes.json').write_text(json.dumps({'schema_version': 'study-axis-declaration/v1', 'groups': groups}, indent=2) + '\n')
    rows, seen = [], set()

    def add(name, family, values, note):
        point = base | {P + AXES[k]: value for k, value in values.items()}
        signature = json.dumps({k: float(v) for k, v in point.items()}, sort_keys=True)
        if signature not in seen:
            rows.append({'id': name, 'family': family, 'point': point, 'note': note})
            seen.add(signature)

    add('reference', 'reference', {}, 'Released nominal defaults; no feasibility tuning.')
    choices = {
        'burn': [.025, .05, .10],
        'recovery': [.99, .999, 1.0],
        'density': [base[P + AXES['density']] * factor for factor in (.9, 1., 1.1)],
        'downtime': [0., .1, .5],
        'price': [.5, 1., 2.],
        'margin': [1., 1.25, 1.5],
        'containment-date': [65.2, 82.4, 96.5],
    }
    for family, values in choices.items():
        for value in values:
            add(f'{family}-{value:g}', family, {family: value}, 'One-factor sensitivity; reference duplicates execute once. Recurring fuel_recovery remains held.')
    add('legacy-reference', 'legacy-control', {'account-selection': False}, 'Same physical point with old account selected.')
    for family in ('burn', 'density'):
        for value in (choices[family][0], choices[family][-1]):
            add(f'legacy-{family}-{value:g}', 'legacy-control', {family: value, 'account-selection': False}, f'Matched control for {family}-{value:g}; cost-method difference at identical physical inputs.')
    (home / 'preparation/candidate-proposals.json').write_text(json.dumps(rows, indent=2) + '\n')
    (home / 'preparation/proposed-window.json').write_text(json.dumps({'provenance': 'engineered', 'choices': choices, 'unique_candidates': len(rows), 'selection': 'Finite one-factor and matched-account controls; no feasible-boundary claim.'}, indent=2) + '\n')
