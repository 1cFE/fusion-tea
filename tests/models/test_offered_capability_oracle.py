"""Independent arithmetic evidence for WI-080, without native calculators."""
import importlib
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'exploration/stellarator_e2e'))
oracle = importlib.import_module('oracle_capability')


@pytest.fixture(scope='module')
def reference():
    verifier = importlib.import_module('verify_stellaris')
    parameters = dict(verifier.IN) | oracle.DEFAULTS
    result = verifier.compute()
    return parameters, result


@pytest.mark.parametrize('name', oracle.SCREENS)
def test_every_screen_strict_boundary_and_zero(name):
    # Each dimension shares a reviewed scalar rule; no epsilon or tolerance snapping.
    for rating, passing in [(math.nextafter(17., 0.), False), (17., True),
                            (math.nextafter(17., math.inf), True)]:
        row = oracle.screen(rating, 17.)
        assert row['capacity_ok'] is passing, name
        assert row['margin'] == rating - 17.
    assert oracle.screen(0., 0.)['capacity_ok']


@pytest.mark.parametrize('field', ['rating', 'demand'])
@pytest.mark.parametrize('invalid', [-1., math.inf, -math.inf, math.nan])
def test_invalid_active_values_refuse(field, invalid):
    with pytest.raises(ValueError):
        oracle.screen(**({'rating': 10., 'demand': 5.} | {field: invalid}))


def test_unsupported_and_inactive_are_distinct():
    unsupported = oracle.screen(10., 5., supported=False)
    inactive = oracle.screen(10., math.nan, applicable=False)
    assert unsupported['margin'] == 5. and unsupported['applicable']
    assert inactive['margin'] == 0. and not inactive['applicable']
    assert not unsupported['capacity_ok'] and not inactive['capacity_ok']
    assert unsupported['defined'] == inactive['defined'] == 0.
    assert not oracle.screen(10., 0., available=False)['capacity_ok']


def test_default_condition_and_result_mapping(reference):
    parameters, results = reference
    row = oracle.evaluate(parameters, results)
    assert set(row) == set(oracle.OUTPUT_MAP)
    assert len(row) == 179
    assert all(row[f'capability_{name}_state_supported'] for name in oracle.STATES)
    assert row['capability_cold_stage_margin'] == parameters['capability_cryoplant__rated_cold_W'] - results['p_cold'] * 1e6
    assert row['capability_direct_electric_capacity_ok']
    assert row['capability_magnet_pf_electric_capacity_ok']


@pytest.mark.parametrize('name', oracle.SCREENS)
def test_each_binding_independently_crosses_capacity(reference, name):
    parameters, results = reference
    owner, group, rating_ref, demand_ref, available = oracle.SCREENS[name]
    # Change the offer only. The independent demand/state calculation stays fixed.
    initial = oracle.evaluate(parameters, results)
    scope, key = rating_ref.split(':', 1)
    rated = (parameters if scope == 'p' else results)[key]
    demand = rated - initial[f'capability_{name}_margin']
    for value, passing in [(max(0., demand * .5), demand == 0), (demand * 1.5, True)]:
        p, r = dict(parameters), dict(results)
        (p if scope == 'p' else r)[key] = value
        row = oracle.evaluate(p, r)
        assert row[f'capability_{name}_capacity_ok'] is passing
        assert row[f'capability_{name}_margin'] == value - demand


@pytest.mark.parametrize('group', oracle.STATES)
def test_changed_point_conditions_cannot_pass(reference, group):
    parameters, results = reference
    _, _, _, pairs = oracle.STATES[group]
    _, rated = pairs[0]
    changed = parameters[rated]
    for _ in range(9):
        changed = math.nextafter(changed, math.inf)
    parameters = parameters | {rated: changed}
    row = oracle.evaluate(parameters, results)
    assert not row[f'capability_{group}_state_supported']
    for name, (_, screen_group, *_) in oracle.SCREENS.items():
        if screen_group == group:
            assert not row[f'capability_{name}_capacity_ok']
            assert row[f'capability_{name}_defined'] == 0.


def test_unavailable_exchanger_and_intercept_receive_no_credit(reference):
    p, r = reference
    row = oracle.evaluate(p | {'cryo_inventory_enabled': False},
                          r | {'matched_main_UA_available': False, 'matched_main_UA_MW_K': 0.})
    for name in ('main_UA', 'intercept_stage'):
        assert row[f'capability_{name}_defined'] == 0
        assert not row[f'capability_{name}_capacity_ok']


def test_legacy_cycle_gross_check_survives_inactive_steam(reference):
    p, r = reference
    row = oracle.evaluate(p, r | {'matched_active': False, 'cw_active': False})
    assert not row['capability_hp_flow_applicable']
    assert not row['capability_water_flow_capacity_ok']
    assert row['capability_turbine_gross_defined'] == 1


def test_fixed_ratings_preserve_choice_as_demand_changes(reference):
    p, r = reference
    before = dict(p)
    low = oracle.evaluate(p, r | {'p_cold': r['p_cold'] * .5})
    high = oracle.evaluate(p, r | {'p_cold': r['p_cold'] * 1.5})
    assert p == before
    assert low['capability_cold_stage_capacity_ok']
    assert not high['capability_cold_stage_capacity_ok']


@pytest.mark.parametrize('actual', [0., 1.5, 300., -300.])
def test_point_state_eight_ulp_boundary(actual):
    inside = actual
    for _ in range(8):
        inside = math.nextafter(inside, math.inf)
    outside = math.nextafter(inside, math.inf)
    assert oracle.same_state(actual, actual)
    assert oracle.same_state(actual, inside)
    assert not oracle.same_state(actual, outside)
    # The state identity allowance never affects physical adequacy.
    assert not oracle.screen(math.nextafter(17., 0.), 17.)['capacity_ok']


@pytest.mark.parametrize('value', [math.nan, math.inf, -math.inf])
def test_point_state_rejects_nonfinite(value):
    with pytest.raises(ValueError):
        oracle.same_state(value, value)


@pytest.mark.parametrize('group,mode', [('helium', 'loop_live'), ('salt', 'cooling_energy_mode')])
def test_unselected_hydraulic_mode_gets_no_capacity_credit(reference, group, mode):
    p, r = reference
    row = oracle.evaluate(p | {mode: 0}, r)
    assert not row[f'capability_{group}_state_applicable']
    for name, (_, screen_group, *_) in oracle.SCREENS.items():
        if screen_group == group:
            assert not row[f'capability_{name}_capacity_ok']
            assert row[f'capability_{name}_margin'] == 0


@pytest.mark.parametrize('mode', ['loop_live', 'cooling_energy_mode'])
@pytest.mark.parametrize('invalid', [-1., .5, 2., math.nan, math.inf])
def test_mode_guard_applies_when_equipment_disabled(reference, mode, invalid):
    p, r = reference
    with pytest.raises(ValueError):
        oracle.evaluate(p | {'cooling_enabled': False, mode: invalid}, r)


@pytest.mark.parametrize('suffix', oracle.FLAG_DEFAULTS)
def test_public_administrative_flags_only_withhold_credit(reference, suffix):
    p, r = reference
    key, _ = oracle.FLAG_DEFAULTS[suffix]
    row = oracle.evaluate(p | {key: False}, r)
    if suffix == oracle.CRYO_ENABLED_SUFFIX:
        names = ['cold_stage', 'intercept_stage']
        assert not row['capability_cryogenic_state_applicable']
    else:
        names = [suffix.split('__')[1].removesuffix('_capability')]
    for name in names:
        assert row[f'capability_{name}_defined'] == 0
        assert not row[f'capability_{name}_supported']
        assert not row[f'capability_{name}_capacity_ok']
    assert len(oracle.PUBLIC_DEFAULTS) == 49
    assert len(oracle.FLAG_DEFAULTS) == 40


def test_disabled_salt_mode_skips_conversion_division(reference):
    p, r = reference
    row = oracle.evaluate(p | {'cooling_energy_mode': 0}, r | {'cooling_salt_pump_count': 0.})
    assert row['capability_salt_electric_converted_demand'] == 0.
