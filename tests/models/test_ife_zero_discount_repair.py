"""WI-049: independent present-value channels and strict generation evidence."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_factor_and_shared_real_duration_structure():
    library = (ROOT / 'models/library/analyses/ife_lcoe.sysml').read_text()
    plant = (ROOT / 'models/designs/generic_ife/ife_plant.sysml').read_text()
    assert "calc def 'IFE Present Value Factors'" in library
    for name in ('discount_rate_in', 'construction_years_in', 'operational_years_in'):
        assert f'in attribute {name} : Real;' in library
    for name, value in [('construction_duration', '5.0'), ('operational_duration', '40.0')]:
        assert f'attribute {name} : Real = {value}' in plant
    for binding in ('in construction_years_in = construction_duration;',
                    'in operational_years_in = operational_duration;',
                    'in construction_years = construction_duration;',
                    'in operational_years = operational_duration;',
                    'in pvf_construction = pv_factors.construction_factor;',
                    'in pvf_operation = pv_factors.operation_factor;',
                    'in net_power = lcoe_calc.net_electric_power;'):
        assert binding in plant
    assert 'annual_capital_cost * pvf_construction' in library
    assert 'annual_energy * pvf_operation' in library
    assert 'calc def' not in plant
    for relative, canonical in [('analyses/ife_lcoe.sysml', 'library/analyses/ife_lcoe.sysml'),
                                ('designs/generic_ife/ife_plant.sysml', 'designs/generic_ife/ife_plant.sysml')]:
        assert (ROOT/'exploration/ife_e2e/models'/relative).read_bytes() == (ROOT/'models'/canonical).read_bytes()


import json
import math
import os
import sys
from dataclasses import replace
from decimal import Decimal, localcontext

import pytest

from exploration.ife_e2e.eligibility import price_eligible, require_price
from tests.ife_oracle import (
    BASE, BOUNDARIES, HEURISTIC, NET_GATE, PREFIX,
    assert_source_outputs, decimal_present_value_reference,
)

RATES = [0.08, 0.0] + [sign * 10.0 ** -power
                       for power in (4, 8, 12, 14, 16, 18) for sign in (1, -1)]
DURATIONS = [(5.0, 40.0), (5.5, 40.5), (0.25, 0.5),
             (1.0, 1.0), (20.0, 100.0), (50.5, 200.5)]
POINTS = {'baseline': {}, 'zero': BOUNDARIES['zero'],
          'negative': BOUNDARIES['counterexample']}
CASES = [(name, construction, operation, rate)
         for construction, operation in DURATIONS for name in POINTS
         for rate in RATES + ([0.5, -0.5] if name == 'baseline' else [])]
FACTOR_CHANNELS = {PREFIX + 'pv_factors__' + name
                   for name in ('construction_factor', 'operation_factor')}
BASELINE = ROOT / 'work/active/WI-049_ife-zero-discount-repair/entry-baseline/baseline_result.json'


@pytest.fixture(scope='module')
def native_package(tmp_path_factory):
    # In the required sealed environment, missing dependencies are failures.
    if os.environ.get('STUDY_REQUIRE_TEAX'):
        import sysml_codegen
    else:
        pytest.importorskip('sysml_codegen', reason='codegen pipeline unavailable')
    teax = os.environ.get('STOP_PARSER_TEAX_ROOT')
    if teax:
        sys.path.insert(0, str(Path(teax) / 'packages/teax-simkit'))
    if os.environ.get('STUDY_REQUIRE_TEAX'):
        import simkit
    else:
        pytest.importorskip('simkit', reason='TEAx pipeline unavailable')
    from sysml_codegen.cli import GenerationConfig, run_codegen
    from tests.model_families import IFE, materialize_canonical_subset
    from tests.ife_execution import complete_ife_package

    root = tmp_path_factory.mktemp('wi049-acceptance')
    models = materialize_canonical_subset(IFE, root / 'models')
    package = root / 'wi049_acceptance'
    config = GenerationConfig(models_path=models, output_path=package,
                              package_name=package.name, overwrite=True)
    assert run_codegen(config)
    complete_ife_package(config)
    entries = {}
    for path in (package / 'inputs').glob('*.json'):
        entries.update(json.loads(path.read_text()))
    assert entries == {PREFIX + key: value for key, value in (BASE | {'viability__threshold': 10.0}).items()}
    assert len(entries) == 19
    return config, root


def public_evaluator(config, root, link='link'):
    from simkit.evaluation.evaluator import PreparedEvaluator
    from simkit.evaluation.package_load import ProvisionalPackageLoader
    from simkit.study.bridge import CandidateBridge

    evaluator = PreparedEvaluator(
        ProvisionalPackageLoader(config.output_path, config.package_name, root / link),
        Path(config.output_path) / 'pipelines/pipeline.yaml', expects_constraint_report=True)
    return evaluator, CandidateBridge(evaluator.entry_models)


@pytest.fixture(scope='module')
def evaluate(native_package):
    evaluator, bridge = public_evaluator(*native_package)

    def run(overrides=None):
        return evaluator.evaluate(bridge.build({PREFIX + key: value
                                               for key, value in (overrides or {}).items()}))
    return run


def assert_strict_channel(actual, expected, name):
    """No absolute floor may hide a small nonzero channel's relative error."""
    assert math.isfinite(actual), (name, actual)
    with localcontext() as context:
        context.prec = 80
        expected = Decimal(str(expected))
        error = abs(Decimal.from_float(float(actual)) - expected)
        limit = Decimal('1e-9') * abs(expected) if expected else Decimal('1e-9')
        assert error <= limit, (name, actual, expected, error, limit)


def assert_finance(result, overrides):
    expected, reference_kind = decimal_present_value_reference(overrides)
    for name in ('discounted_cost', 'discounted_energy'):
        assert_strict_channel(result.outputs[PREFIX + 'lcoe_calc__' + name], expected[name], name)
    assert_strict_channel(result.outputs[PREFIX + 'hawker_price__price'], expected['price'], 'price')
    for name in ('construction_factor', 'operation_factor'):
        assert_strict_channel(result.outputs[PREFIX + 'pv_factors__' + name], expected[name], name)
    durations = BASE | overrides
    integral = all(durations[key].is_integer() for key in ('construction_duration', 'operational_duration'))
    assert reference_kind == ('dated_integer_sums' if integral else 'fractional_power_extension')


def assert_eligibility(result, generating):
    outputs = result.outputs
    assert result.responses[NET_GATE] == ('satisfied' if generating else 'violated')
    assert result.responses[HEURISTIC] == 'satisfied'
    net = outputs[PREFIX + 'lcoe_calc__net_electric_power']
    assert (net > 0) == generating
    for method in ('hawker_price', 'meier_price'):
        price = outputs[PREFIX + method + '__price']
        flag = outputs[PREFIX + method + '__generating']
        assert flag == float(generating)
        assert math.isfinite(price)
        assert price_eligible(price, flag, result.responses[NET_GATE]) == generating
        if generating:
            assert price > 0
            assert require_price(price, flag, result.responses[NET_GATE]) == price
        else:
            assert price == 0.0
            with pytest.raises(ValueError, match='ineligible'):
                require_price(price, flag, result.responses[NET_GATE])


@pytest.mark.codegen_available
@pytest.mark.parametrize('name,construction,operation,rate', CASES)
def test_sv076_sv077_sv078_full_design_window(evaluate, name, construction, operation, rate):
    assert len(CASES) == 264
    overrides = POINTS[name] | {'construction_duration': construction,
                              'operational_duration': operation, 'discount_rate': rate}
    result = evaluate(overrides)
    assert_finance(result, overrides)
    assert_eligibility(result, name == 'baseline')
    energy = result.outputs[PREFIX + 'lcoe_calc__discounted_energy']
    if name == 'zero':
        assert energy == 0.0
        assert result.outputs[PREFIX + 'lcoe_calc__net_electric_power'] == 0.0
    elif name == 'negative':
        assert energy < 0
    else:
        assert energy > 0


@pytest.mark.codegen_available
@pytest.mark.parametrize('rate', [0.0, 1e-12, -1e-12, 0.08])
def test_sv078_positive_neighbor_remains_eligible(evaluate, rate):
    overrides = BOUNDARIES['positive_neighbor'] | {'discount_rate': rate}
    result = evaluate(overrides)
    assert result.outputs[PREFIX + 'lcoe_calc__net_electric_power'] == 2.5
    assert_finance(result, overrides)
    assert_eligibility(result, True)


@pytest.mark.codegen_available
def test_sv078_all_inherited_baseline_outputs_and_verdicts(evaluate):
    baseline = json.loads(BASELINE.read_text())
    result = evaluate()
    assert len(baseline['channels']) == 30
    assert set(result.outputs) == set(baseline['channels']) | FACTOR_CHANNELS
    for name, expected in baseline['channels'].items():
        assert_strict_channel(result.outputs[name], expected, name)
    verdicts = {row['constraint_id']: row['status'] for row in baseline['verdicts']}
    assert len(verdicts) == 2
    assert dict(result.responses) == verdicts | {'headline': 'satisfied'}
    assert_source_outputs(result.outputs)
    assert_finance(result, {})
    assert_eligibility(result, True)


@pytest.mark.codegen_available
@pytest.mark.parametrize('duration,value', [('construction_duration', 5.5), ('operational_duration', 40.5)])
def test_real_duration_mutations_reach_factors_and_cost(evaluate, duration, value):
    baseline = evaluate()
    result = evaluate({duration: value})
    assert_finance(result, {duration: value})
    assert result.outputs[PREFIX + 'lcoe_calc__discounted_cost'] != baseline.outputs[PREFIX + 'lcoe_calc__discounted_cost']
    assert result.outputs[PREFIX + 'pv_factors__operation_factor'] != baseline.outputs[PREFIX + 'pv_factors__operation_factor']
    construction_key = PREFIX + 'pv_factors__construction_factor'
    if duration == 'construction_duration':
        assert result.outputs[construction_key] != baseline.outputs[construction_key]
    else:
        assert result.outputs[construction_key] == baseline.outputs[construction_key]


@pytest.mark.codegen_available
@pytest.mark.parametrize('construction,operation', DURATIONS)
def test_signed_zero_exact_factor_limits(evaluate, construction, operation):
    values = {'construction_duration': construction, 'operational_duration': operation}
    positive = evaluate(values | {'discount_rate': 0.0})
    negative = evaluate(values | {'discount_rate': -0.0})
    assert dict(negative.outputs) == dict(positive.outputs)
    assert negative.outputs[PREFIX + 'pv_factors__construction_factor'] == construction
    assert negative.outputs[PREFIX + 'pv_factors__operation_factor'] == operation
    assert_finance(negative, values | {'discount_rate': -0.0})


@pytest.mark.codegen_available
def test_typed_completions_and_repeat_regeneration(native_package):
    from sysml_codegen.cli import run_codegen

    config, root = native_package
    package = Path(config.output_path)

    def tree():
        return {path.relative_to(package).as_posix(): path.read_bytes()
                for path in package.rglob('*') if path.is_file() and '__pycache__' not in path.parts}

    for filename, input_type in [('ife_present_value_factors_impl.py', 'IFE_Present_Value_FactorsInput'),
                                 ('generating_electricity_price_impl.py', 'Generating_Electricity_PriceInput')]:
        path = Path('handwritten/ife_lcoe') / filename
        shipped = (ROOT / 'exploration/ife_e2e/generated' / path).read_text()
        assert (package / path).read_text() == shipped.replace('from ife_tea.', f'from {config.package_name}.')
        assert input_type in shipped
        assert 'tuple[float, float]' in shipped
    original = tree()
    for smart in (False, True):
        assert run_codegen(replace(config, preserve_handwritten=True, smart_regen=smart))
        assert tree() == original
        evaluator, bridge = public_evaluator(config, root, f'regeneration-{smart}')
        for overrides in ({}, {'discount_rate': 0.0}, {'construction_duration': 5.5, 'operational_duration': 40.5}):
            result = evaluator.evaluate(bridge.build({PREFIX + key: value for key, value in overrides.items()}))
            assert_finance(result, overrides)
            assert_eligibility(result, True)


def test_strict_assertion_rejects_cancellation_and_small_channel_absolute_floor():
    # The assessed 1e-12 defect has roughly 8.89e-5 relative component error.
    with pytest.raises(AssertionError):
        assert_strict_channel(1.0000889, Decimal(1), 'discounted_cost')
    with pytest.raises(AssertionError):
        assert_strict_channel(2e-12, Decimal('1e-12'), 'small_nonzero')
    assert_strict_channel(0.0, Decimal(0), 'true_zero')
