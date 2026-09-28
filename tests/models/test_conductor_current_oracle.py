"""Independent WI-062 oracle arithmetic and domain checks."""
import importlib.util
import sys
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    'conductor_oracle', Path(__file__).parents[2] / 'exploration/stellarator_e2e/verify_stellaris.py'
)
vs = importlib.util.module_from_spec(_SPEC)
sys.path.insert(0, str(Path(_SPEC.origin).parent))
_SPEC.loader.exec_module(vs)
sys.path.pop(0)


def evaluate(**overrides):
    p = dict(vs.IN, magnet_tape_width=0.004, magnet_f_set=0.5,
             magnet_f_wp_vol=1, magnet_turn_current=800)
    p.update(overrides)
    return vs._conductor_current(p, 20, 100, 10)


def test_analytic_inventory_and_exact_boundary():
    result = evaluate()
    assert result['parallel_tapes_set'] == 10
    assert result['parallel_tapes_reference'] == 5
    assert result['tape_critical_current'] == 200
    assert result['critical_current_reference'] == 1000
    assert result['critical_current_set'] == 2000
    assert result['margin_fraction'] == result['margin_current'] == 0
    assert evaluate(magnet_turn_current=799)['margin_current'] > 0
    assert evaluate(magnet_turn_current=801)['margin_current'] < 0


def test_allowance_and_retention_have_distinct_roles():
    base = evaluate()
    allowance = evaluate(magnet_allowable_fraction=0.5)
    retention = evaluate(magnet_degradation_factor=0.5)
    assert allowance['critical_current_reference'] == base['critical_current_reference']
    assert retention['critical_current_reference'] == 0.5 * base['critical_current_reference']
    assert allowance['parallel_tapes_reference'] == retention['parallel_tapes_reference']


@pytest.mark.parametrize('key,value', [
    ('T_cold_cryo', 21), ('magnet_tape_thickness', 0.00006),
    ('magnet_tape_width', 0.007), ('magnet_allow_field_extrapolation', 0.5),
    ('magnet_cabling_factor', 1.1), ('magnet_degradation_factor', 0),
    ('magnet_sharing_factor', -1), ('magnet_allowable_fraction', 1.1),
    ('magnet_material_factor', float('nan')), ('magnet_orientation_factor', float('inf')),
    ('magnet_reference_tape_current', 1e308),
])
def test_invalid_inputs_refused(key, value):
    with pytest.raises(ValueError):
        evaluate(**{key: value})


def test_field_domain_and_opt_in():
    p = dict(vs.IN)
    for field in (19.9, 32.1):
        with pytest.raises(ValueError):
            vs._conductor_current(p, field, 100, 10)
    p['magnet_allow_field_extrapolation'] = 0
    assert vs._conductor_current(p, 24, 100, 10)['field_extrapolated'] == 0
    with pytest.raises(ValueError):
        vs._conductor_current(p, 25, 100, 10)
    p['magnet_allow_field_extrapolation'] = 1
    assert vs._conductor_current(p, 25, 100, 10)['field_extrapolated'] == 1
    assert vs._conductor_current(p, 32, 100, 10)['tape_critical_current'] < vs._conductor_current(p, 25, 100, 10)['tape_critical_current']
