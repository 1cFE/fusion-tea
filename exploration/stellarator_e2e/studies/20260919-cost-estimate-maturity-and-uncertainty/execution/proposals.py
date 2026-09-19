"""Finite proposals; source alternatives, contingency diagnostic and downtime stress."""
from itertools import product
import json

P = 'stellarator_09__stellaris__'
AXES = {
    'fabrication': 'heat_transport__equipment_stainless_fabrication_usd2017_per_kg',
    'tonne': 'buildings__tonne_interpretation_kg',
    'containment': 'fuel_cycle__processing_containment_cpi',
    'sheet': 'magnet__winding_pack__insulation_sheet_price',
    'contingency': 'contingency_rate',
    'downtime': 'unplanned_fraction',
}
NOMINAL = {'fabrication': 310., 'tonne': 907.18474, 'containment': 82.4,
           'sheet': 61.67720668774671, 'contingency': .10, 'downtime': 0.}
CHOICES = {'fabrication': [240., 310., 360.], 'tonne': [907.18474, 1000.],
           'containment': [65.2, 82.4, 96.5], 'sheet': [61.67720668774671, 0.]}


def build(home, defaults):
    keys = {P + suffix for suffix in AXES.values()}
    missing = keys - defaults.keys()
    if missing:
        raise RuntimeError(f'Released ABI missing proposed public inputs: {sorted(missing)}')
    for name, value in NOMINAL.items():
        if defaults[P + AXES[name]] != value:
            raise RuntimeError(f'Unexpected new-candidate default for {name}: {defaults[P + AXES[name]]}')
    groups = [{'axis': suffix, 'note': f'{name}: single public owner input, complete fan-out checked at release; no cross-input tie.',
               'keys': [{'key': P + suffix, 'provenance': 'fan_out'}]} for name, suffix in AXES.items()]
    (home / 'axes.json').write_text(json.dumps({'schema_version': 'study-axis-declaration/v1', 'groups': groups}, indent=2) + '\n')
    base = {P + AXES[name]: value for name, value in NOMINAL.items()}
    rows, seen = [], set()
    for contingency in [.10, 0.]:
        for values in product(*CHOICES.values()):
            changes = dict(zip(CHOICES, values)) | {'contingency': contingency}
            point = base | {P + AXES[name]: value for name, value in changes.items()}
            source_nominal = all(changes[name] == NOMINAL[name] for name in CHOICES)
            source_id = 'reference' if source_nominal else '-'.join(f'{name}{changes[name]:g}' for name in CHOICES)
            identity = source_id if contingency == .10 else 'zero-contingency-' + source_id
            rows.append({'id': identity, 'family': 'source-envelope' if contingency == .10 else 'contingency-diagnostic',
                         'point': point, 'matched_source_id': source_id,
                         'note': 'Finite source-interpretation/model-analogy combination; financial diagnostic is outside headline source envelope.'})
    for value in [.05, .10]:
        rows.append({'id': f'downtime-stress-{value:g}', 'family': 'downtime-stress',
                     'point': base | {P + AXES['downtime']: value}, 'matched_source_id': 'reference',
                     'note': 'Engineered availability stress, not supported reliability bounds; nominal costs/contingency held.'})
    for row in rows:
        signature = json.dumps(row['point'], sort_keys=True)
        if signature in seen:
            raise RuntimeError(f'Unexpected duplicate proposal: {row["id"]}')
        seen.add(signature)
    assert len(rows) == len(seen) == 74
    assert sum(row['family'] == 'source-envelope' for row in rows) == 36
    assert sum(row['family'] == 'contingency-diagnostic' for row in rows) == 36
    assert sum(row['id'] == 'reference' for row in rows) == 1
    (home / 'preparation/candidate-proposals.json').write_text(json.dumps(rows, indent=2) + '\n')
    (home / 'preparation/proposed-window.json').write_text(json.dumps({
        'provenance': 'engineered', 'source_conditioned_axes': CHOICES,
        'contingency_diagnostic': [.10, 0.], 'downtime_stress_only': [.05, .10],
        'unique_candidates': len(rows), 'headline_population': '36 source-envelope cases only',
        'selection': 'Full finite combinations; no sampling, seed, convergence or feasible-boundary claim.'}, indent=2) + '\n')
