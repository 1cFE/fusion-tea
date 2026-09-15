"""Prepare input coordinates only; does not import or execute a model evaluator."""
import json
from pathlib import Path

H = Path(__file__).resolve().parents[1]
P = 'stellarator_09__stellaris__'
FIT = {
    'fit_aspect_ratio': ('magnet__winding_pack__fit_aspect_ratio', 1.0, [0.8, 1.25]),
    'interior_y': ('magnet__casing__interior_y', 0.40, [0.35, 0.45]),
    'wall_thickness': ('magnet__casing__wall_thickness', 0.025, [0.015, 0.035]),
    'ground_insulation': ('magnet__winding_pack__ground_insulation', 0.003, [0.0, 0.005]),
    'assembly_clearance': ('magnet__casing__assembly_clearance', 0.002, [0.0, 0.004]),
    'internal_build_y': ('magnet__winding_pack__internal_build_y', 0.025, [0.0]),
}


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def main():
    axes = read(H / 'preparation/axes-entering-draft.json')
    for name, (suffix, nominal, alternatives) in FIT.items():
        axes['groups'].append({
            'axis': name,
            'note': '[AGENT] Engineered local fit sensitivity at 0.50 m radial allocation; candidate fan-out to be checked after release.',
            'keys': [{'key': P + suffix, 'provenance': 'fan_out'}],
        })
    write(H / 'axes.json', axes)
    rows = read(H / 'preparation/proposals-entering.json')
    for row in rows:
        row['family'] = 'original-nominal'
    rows.append({'id': 'baseline', 'arm': 'baseline', 'family': 'original-nominal',
                 'point': {}, 'use_exact_manifest_baseline': True})
    allocations = read(H / 'preparation/proposals-allocation.json')
    for row in allocations:
        row['family'] = 'allocation-nominal-geometry'
    rows.extend(allocations)
    anchors = [row for row in allocations if row['point'][P + 'magnet__coil__coil_t'] == 0.5]
    for anchor in anchors:
        for name, (suffix, nominal, alternatives) in FIT.items():
            for value in alternatives:
                rows.append({'id': f"geometry-{anchor['id']}-{name}-{value}",
                             'arm': name, 'family': 'geometry-at-allocation-0.5',
                             'anchor_id': anchor['id'],
                             'point': anchor['point'] | {P + suffix: value}})
    assert len(rows) <= 150
    write(H / 'preparation/proposals-draft.json', rows)
    write(H / 'preparation/expected-fit-interface.json', {
        'status': 'Author-supplied interface; validate against released native generation',
        'inputs': {P + suffix: nominal for suffix, nominal, _ in FIT.values()} |
                  {P + 'magnet__winding_pack__internal_build_x': 0.0,
                   P + 'magnet__coil__coil_t': 0.30},
        'outputs': [P + 'magnet__wp_fit__' + quantity + '_' + axis
                    for quantity in ('nominal', 'internal', 'pack', 'insulated',
                                     'required', 'cavity', 'exterior', 'margin')
                    for axis in ('x', 'y')] + [P + 'magnet__wp_fit__minimum_margin'],
        'predicate_source_local_identity': 'wp_fit_ok',
        'predicate_constraint_id': P + 'wp_fit_ok__a25ca6a0161f6339',
        'predicate_operand': 'minimum_margin_in',
        'expected_public_inputs': 299,
        'expected_native_numeric_outputs': 212,
        'expected_oracle_mapped_outputs': 196,
        'expected_total_predicates': 19,
    })
    print(f'Prepared {len(rows)} coordinate rows and {len(axes["groups"])} axis groups; no evaluations.')


if __name__ == '__main__':
    main()
