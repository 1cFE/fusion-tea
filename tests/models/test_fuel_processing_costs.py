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
            capacity_margin=1., price_multiplier=1., reference_flow=2.08e-5,
            exponent=.3, target_cpi=321.9)
for row, (capital, installation, cpi) in zip(ROWS, RAW):
    CASE.update({row + '_capital': capital, row + '_installation': installation, row + '_cpi': cpi})


@pytest.fixture(scope='module', params=('oracle', 'production'))
def calculate(request):
    if request.param == 'oracle':
        return oracle.calculate
    path = ROOT / 'work/active/WI-070_throughput-based-fuel-processing-costs/seeds/fuel_processing_cost_impl.py'
    spec = importlib.util.spec_from_file_location('processing_seed_under_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.calculate


def decimal_reference(case):
    """Evaluate the written row equations at 60 decimal digits, no model imports."""
    with localcontext() as context:
        context.prec = 60
        d = {key: Decimal(str(value)) for key, value in case.items() if type(value) is not bool}
        capacity = d['flow'] * d['capacity_margin']
        ratio = capacity / d['reference_flow']
        scale = ratio ** d['exponent']
        values = dict(flow_kg_s=d['flow'], capacity_kg_s=capacity,
                      plant_capacity_kg_s=capacity * d['n_mod'], flow_ratio=ratio,
                      scaling_factor=scale, defined_flag=Decimal(int(case['source_conditions'])))
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
    {'capacity_margin': 1.5}, {'source_conditions': False},
    {'n_mod': 3., 'price_multiplier': 2., 'capacity_margin': 1.25},
])
def test_every_output_against_high_precision_source_equations(calculate, changes):
    case = CASE | changes
    actual, expected = calculate(case), decimal_reference(case)
    assert len(actual) == 27
    assert set(actual) == set(expected)
    for name, value in expected.items():
        assert actual[name] == pytest.approx(value, rel=2e-13, abs=1e-18), name


def test_reviewed_current_flow_and_expenditure_date_anchors(calculate):
    current = calculate(CASE)
    assert current['equipment_total'] == pytest.approx(20443419.583268173, rel=0, abs=1e-7)
    assert current['installation_total'] == pytest.approx(2342809.8205252266, rel=0, abs=1e-7)
    assert current['cost'] == pytest.approx(22786229.4037934, rel=0, abs=1e-7)
    for cpi, total in ((65.2, 23180989.577015813), (96.5, 22567582.023116916)):
        changed = calculate(CASE | {'containment_cpi': cpi})
        assert changed['cost'] == pytest.approx(total, rel=0, abs=1e-7)
        for row in ROWS[:-1]:
            for field in ('capital', 'installation', 'reference_capital', 'reference_installation'):
                assert changed[row + '_' + field] == current[row + '_' + field]


def test_reference_rows_recover_raw_expenditures_in_each_original_year(calculate):
    for row, (capital, installation, cpi) in zip(ROWS, RAW):
        result = calculate(CASE | {'flow': CASE['reference_flow'], 'target_cpi': cpi})
        assert result[row + '_capital'] == pytest.approx(capital, rel=1e-14)
        assert result[row + '_installation'] == pytest.approx(installation, rel=1e-14)


def test_zero_exhaust_has_zero_actual_price_but_retains_reference_anchors(calculate):
    zero = calculate(CASE | {'flow': 0.})
    reference = calculate(CASE)
    for name, value in zero.items():
        if '_reference_' in name:
            assert value == reference[name] > 0
        elif name == 'defined_flag':
            assert value == 1.
        else:
            assert value == 0.


def test_identical_modules_price_and_margin_are_distinct_scalings(calculate):
    one = calculate(CASE)
    two = calculate(CASE | {'n_mod': 2.})
    expensive = calculate(CASE | {'price_multiplier': 2.})
    margin = calculate(CASE | {'capacity_margin': 1.5})
    assert two['flow_kg_s'] == two['capacity_kg_s'] == one['flow_kg_s']
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
    {'capacity_margin': .99}, {'price_multiplier': 0.}, {'reference_flow': 0.},
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
    {'flow': 1e308, 'capacity_margin': 2.},
    {'flow': 1e200, 'exponent': 20.},
    {'price_multiplier': 1e308},
    {'transfer_capital': 1e308, 'target_cpi': 1e308},
])
def test_overflow_is_a_domain_error_not_a_plausible_price(calculate, changes):
    with pytest.raises(ValueError):
        calculate(CASE | changes)
