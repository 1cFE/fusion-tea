"""Independent source-price, domain and capacity-basis checks for WI-070.

Raw rows and monetary years: goal evidence/proposed-cost-scope.md and independent
proposed-price-review.md. Decimal arithmetic here imports neither calculator body.
"""
from decimal import Decimal, localcontext
import importlib.util
from pathlib import Path

import pytest

from exploration.stellarator_e2e import oracle_fuel_processing as oracle

ROOT = Path(__file__).resolve().parents[2]
ROWS = ('transfer', 'cleanup', 'distiller', 'containment')
RAW = ((111000, 112000, 60.6), (1000000, 70000, 82.4),
       (1237000, 63000, 65.2), (182000, 30000, 82.4))
CASE = dict(enabled=True, source_conditions=True, inventory_enabled=True,
            flow=12.911794045007683 / 86400, n_mod=1., legacy_cost=120746472.201428,
            capacity=0.00015, price_multiplier=1., reference_flow=2.08e-5,
            exponent=.3, target_cpi=321.9)
for row, (capital, installation, cpi) in zip(ROWS, RAW):
    CASE.update({row + '_capital': capital, row + '_installation': installation, row + '_cpi': cpi})


@pytest.fixture(scope='module', params=('oracle', 'production'))
def calculate(request):
    if request.param == 'oracle':
        return oracle.calculate
    path = ROOT / 'work/active/WI-077_supplied-fuel-processing-capacity-evaluation/seeds/fuel_processing_cost_impl.py'
    spec = importlib.util.spec_from_file_location('processing_seed_under_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.calculate


def decimal_reference(case):
    """Evaluate the written row equations at 60 decimal digits, no model imports."""
    with localcontext() as context:
        context.prec = 60
        d = {key: Decimal(str(value)) for key, value in case.items() if type(value) is not bool}
        capacity = d['capacity']
        ratio = capacity / d['reference_flow']
        scale = ratio ** d['exponent']
        values = dict(flow_kg_s=d['flow'], capacity_kg_s=capacity,
                      plant_capacity_kg_s=capacity * d['n_mod'], flow_ratio=ratio,
                      scaling_factor=scale, defined_flag=Decimal(int(case['source_conditions'])),
                      plant_demand_kg_s=d['flow'] * d['n_mod'],
                      capacity_margin_kg_s=(capacity - d['flow']) * d['n_mod'],
                      capacity_evaluation_defined=Decimal(1))
        for row in ROWS:
            for field in ('capital', 'installation'):
                reference = d[row + '_' + field] * d['target_cpi'] / d[row + '_cpi']
                values[row + '_reference_' + field] = reference
                values[row + '_' + field] = reference * scale * d['price_multiplier'] * d['n_mod']
        values['equipment_total'] = sum(values[row + '_capital'] for row in ROWS)
        values['installation_total'] = sum(values[row + '_installation'] for row in ROWS)
        values['new_total'] = values['equipment_total'] + values['installation_total']
        values['module_total'] = values['new_total'] / d['n_mod']
        values['cost'] = values['new_total']
        return {key: float(value) for key, value in values.items()}


@pytest.mark.parametrize('changes', [
    {}, {'flow': 2.08e-5}, {'flow': 0.}, {'containment_cpi': 65.2},
    {'containment_cpi': 96.5}, {'n_mod': 2.}, {'price_multiplier': .5},
    {'capacity': 0.000225}, {'source_conditions': False},
    {'n_mod': 3., 'price_multiplier': 2., 'capacity': 0.0001875},
])
def test_every_output_against_high_precision_source_equations(calculate, changes):
    case = CASE | changes
    actual, expected = calculate(case), decimal_reference(case)
    assert len(actual) == 30
    assert set(actual) == set(expected)
    for name, value in expected.items():
        assert actual[name] == pytest.approx(value, rel=2e-13, abs=1e-18), name


def test_supplied_capacity_and_expenditure_date_anchors(calculate):
    for changes in ({}, {'containment_cpi': 65.2}, {'containment_cpi': 96.5}):
        x = CASE | changes
        actual = calculate(x)
        expected = decimal_reference(x)
        for field in ('equipment_total', 'installation_total', 'cost'):
            assert actual[field] == pytest.approx(expected[field], rel=2e-13)


def test_reference_rows_recover_raw_expenditures_in_each_original_year(calculate):
    for row, (capital, installation, cpi) in zip(ROWS, RAW):
        result = calculate(CASE | {'capacity': CASE['reference_flow'], 'target_cpi': cpi})
        assert result[row + '_capital'] == pytest.approx(capital, rel=1e-14)
        assert result[row + '_installation'] == pytest.approx(installation, rel=1e-14)


def test_zero_exhaust_keeps_selected_hardware_and_price(calculate):
    zero = calculate(CASE | {'flow': 0.})
    reference = calculate(CASE)
    for name in ('capacity_kg_s', 'cost', 'equipment_total', 'installation_total'):
        assert zero[name] == reference[name] > 0
    assert zero['plant_demand_kg_s'] == 0
    assert zero['capacity_margin_kg_s'] == zero['plant_capacity_kg_s']


def test_identical_modules_price_and_margin_are_distinct_scalings(calculate):
    one = calculate(CASE)
    two = calculate(CASE | {'n_mod': 2.})
    expensive = calculate(CASE | {'price_multiplier': 2.})
    margin = calculate(CASE | {'capacity': 0.000225})
    assert two['flow_kg_s'] == one['flow_kg_s']
    assert two['capacity_kg_s'] == one['capacity_kg_s']
    assert two['module_total'] == one['module_total']
    assert two['plant_capacity_kg_s'] == 2 * one['capacity_kg_s']
    assert two['cost'] == pytest.approx(2 * one['cost'])
    assert expensive['cost'] == pytest.approx(2 * one['cost'])
    assert expensive['capacity_kg_s'] == one['capacity_kg_s']
    assert margin['flow_kg_s'] == one['flow_kg_s']
    assert margin['cost'] / one['cost'] == pytest.approx(1.5 ** .3)
    for row in ROWS:
        assert expensive[row + '_reference_capital'] == margin[row + '_reference_capital'] == one[row + '_reference_capital']


def test_source_condition_false_is_diagnostic_not_a_zero_price(calculate):
    active = calculate(CASE)
    diagnostic = calculate(CASE | {'source_conditions': False})
    assert diagnostic['defined_flag'] == 0
    assert {k: v for k, v in diagnostic.items() if k != 'defined_flag'} == {k: v for k, v in active.items() if k != 'defined_flag'}


def test_disabled_mode_preserves_exact_legacy_and_accepts_zero_source_placeholders(calculate):
    dormant = {key: 0. for key, value in CASE.items() if type(value) is not bool}
    dormant.update(enabled=False, inventory_enabled=False, source_conditions=False, legacy_cost=123456789.01234567)
    result = calculate(dormant)
    assert result['cost'] == dormant['legacy_cost']
    assert all(value == 0. for name, value in result.items() if name != 'cost')


@pytest.mark.parametrize('changes', [
    {'inventory_enabled': False}, {'flow': -1e-9}, {'n_mod': 0}, {'n_mod': 1.5},
    {'capacity': 0.}, {'price_multiplier': 0.}, {'reference_flow': 0.},
    {'exponent': 0.}, {'target_cpi': 0.},
    *({row + '_cpi': 0.} for row in ROWS),
    *({row + '_' + field: -1.} for row in ROWS for field in ('capital', 'installation')),
])
def test_refuses_unphysical_or_undefined_active_domains(calculate, changes):
    with pytest.raises(ValueError):
        calculate(CASE | changes)


@pytest.mark.parametrize('key', tuple(key for key, value in CASE.items() if type(value) is not bool))
def test_nonfinite_inputs_refused_even_for_dormant_legacy(calculate, key):
    for value in (float('nan'), float('inf'), -float('inf')):
        for enabled in (True, False):
            with pytest.raises(ValueError):
                calculate(CASE | {key: value, 'enabled': enabled})


@pytest.mark.parametrize('key', tuple(key for key, value in CASE.items() if type(value) is not bool))
def test_boolean_is_not_an_amount_or_source_quantity(calculate, key):
    for value in (False, True):
        for enabled in (True, False):
            with pytest.raises(ValueError):
                calculate(CASE | {key: value, 'enabled': enabled})


@pytest.mark.parametrize('enabled', (True, False))
def test_negative_legacy_account_refused_even_when_not_selected(calculate, enabled):
    with pytest.raises(ValueError):
        calculate(CASE | {'legacy_cost': -1., 'enabled': enabled})


@pytest.mark.parametrize('key', ('enabled', 'inventory_enabled', 'source_conditions'))
def test_flags_require_exact_boolean_declarations(calculate, key):
    for value in (0., 1., None, 'true'):
        with pytest.raises(ValueError):
            calculate(CASE | {key: value})


@pytest.mark.parametrize('changes', [
    {'flow': 1e308, 'n_mod': 2.},
    {'capacity': 1e200, 'exponent': 20.},
    {'price_multiplier': 1e308},
    {'transfer_capital': 1e308, 'target_cpi': 1e308},
])
def test_overflow_is_a_domain_error_not_a_plausible_price(calculate, changes):
    with pytest.raises(ValueError):
        calculate(CASE | changes)
