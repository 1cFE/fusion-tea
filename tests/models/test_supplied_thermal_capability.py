"""WI-080 seed evidence for the existing conditional IHX area screen."""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks'


def load_seed(path):
    spec = importlib.util.spec_from_file_location('cooling_seed_' + path.parent.parent.name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope='module')
def seed():
    return load_seed(WORK / 'seeds/cooling_equipment_impl.py')


@pytest.fixture(scope='module')
def parameters():
    interface = json.loads((ROOT / 'work/active/WI-067_installed-cooling-equipment-costs/evidence/equipment-interface.json').read_text())
    values = {item['name']: item['default'] for item in interface['inputs']}
    selected = ROOT / 'work/active/WI-078_supplied-cooling-design-point-evaluation/evidence/selected-defaults.json'
    values.update(json.loads(selected.read_text())['selected_inputs'])
    return values | {'enabled': True, 'stainless_fabrication_usd2017_per_kg': 310.0}


def test_fixed_hardware_load_crosses_area_limit_without_repricing(seed, parameters):
    base = seed.calculate(parameters)
    limit = parameters['q_ihx_MW'] * base['ihx_installed_area'] / base['ihx_required_area']
    low = seed.calculate(parameters | {'q_ihx_MW': limit * 0.9})
    high = seed.calculate(parameters | {'q_ihx_MW': limit * 1.1})
    for row, sufficient in ((low, True), (high, False)):
        assert row['ihx_capacity_defined'] == 1.0
        assert (row['ihx_capacity_margin_m2'] >= 0.0) is sufficient
        assert row['ihx_capacity_ok'] is sufficient
        assert row['ihx_capacity_margin_m2'] == row['ihx_installed_area'] - row['ihx_required_area']
        for name in ('ihx_installed_area', 'hx_mass', 'hx_purchase', 'installed_total', 'replacement_annual'):
            assert row[name] == base[name], name
        assert not row['pressure_qualified']


def test_supplied_circuit_count_changes_exchanger_inventory_and_capacity(seed, parameters):
    base = seed.calculate(parameters)
    required_count = parameters['n_loops'] * base['ihx_required_area'] / base['ihx_installed_area']
    insufficient_count = max(1, math.floor(required_count * 0.7))
    sufficient_count = math.ceil(required_count * 1.3)
    low = seed.calculate(parameters | {'n_loops': insufficient_count})
    high = seed.calculate(parameters | {'n_loops': sufficient_count})
    assert low['ihx_capacity_margin_m2'] < 0.0 < high['ihx_capacity_margin_m2']
    assert low['ihx_count'] == insufficient_count
    assert high['ihx_count'] == sufficient_count
    assert low['ihx_installed_area'] == high['ihx_installed_area']
    assert high['hx_purchase'] / low['hx_purchase'] == pytest.approx(sufficient_count / insufficient_count)
    assert high['installed_total'] > low['installed_total']


def test_dormant_carriers_are_explicitly_undefined(seed):
    row = seed.calculate({'enabled': False})
    assert row['ihx_capacity_defined'] == 0.0
    assert row['ihx_capacity_margin_m2'] == 0.0
    assert not row['ihx_capacity_ok']


@pytest.mark.parametrize('change', [{'helium_hot_K': 738.15}, {'helium_suction_K': 543.15}, {'q_ihx_MW': float('nan')}])
def test_invalid_thermal_domain_still_refuses(seed, parameters, change):
    with pytest.raises(ValueError):
        seed.calculate(parameters | change)


def test_all_existing_outputs_preserved(seed, parameters):
    old = load_seed(ROOT / 'work/active/WI-078_supplied-cooling-design-point-evaluation/seeds/cooling_equipment_impl.py')
    for change in ({}, {'q_ihx_MW': parameters['q_ihx_MW'] * 1.1}, {'n_loops': 14}):
        prior = old.calculate(parameters | change)
        current = seed.calculate(parameters | change)
        assert {key: current[key] for key in prior} == prior
        assert set(current) - set(prior) == {'ihx_capacity_margin_m2', 'ihx_capacity_defined'}


def test_near_boundary_preserves_raw_negative_margin(seed, parameters):
    base = seed.calculate(parameters)
    duty = parameters['q_ihx_MW'] * base['ihx_installed_area'] / base['ihx_required_area']
    # Walk representable heat values to either side of the actual arithmetic boundary.
    for direction, positive in ((0.0, True), (math.inf, False)):
        trial = duty
        for _ in range(32):
            row = seed.calculate(parameters | {'q_ihx_MW': trial})
            margin = row['ihx_capacity_margin_m2']
            if (margin > 0.0 if positive else margin < 0.0):
                assert abs(margin) < 1e-8
                assert row['ihx_capacity_ok'] is positive
                break
            trial = math.nextafter(trial, direction)
        else:
            pytest.fail('Did not cross the raw area boundary within 32 adjacent heat values')


CONTRACT = json.loads((WORK / 'evidence/capability-contract.json').read_text())


@pytest.fixture(scope='module')
def screen_seed():
    return load_seed(WORK / 'seeds/offered_capacity_screen_impl.py')


@pytest.mark.parametrize('rating,expected', [(0.0, False), (math.nextafter(10.0, 0.0), False), (10.0, True), (math.nextafter(10.0, math.inf), True), (20.0, True)])
def test_scalar_screen_strict_rating_boundary(screen_seed, rating, expected):
    result = screen_seed.calculate(dict(rating=rating, demand=10.0, applicable=True, conditions_supported=True, demand_available=True))
    assert result['capacity_ok'] is expected
    assert result['margin'] == rating - 10.0
    assert result['evaluation_defined'] == 1.0


@pytest.mark.parametrize('field', ['applicable', 'conditions_supported', 'demand_available'])
def test_absent_or_unsupported_screen_never_gets_capacity_credit(screen_seed, field):
    args = dict(rating=20.0, demand=10.0, applicable=True, conditions_supported=True, demand_available=True)
    result = screen_seed.calculate(args | {field: False})
    assert not result['capacity_ok']
    assert result['evaluation_defined'] == 0.0
    assert result['applicable'] is (field != 'applicable')


@pytest.mark.parametrize('rating', [-1.0, float('nan'), float('inf'), True])
def test_bad_offered_rating_is_rejected_even_if_inactive(screen_seed, rating):
    with pytest.raises(ValueError):
        screen_seed.calculate(dict(rating=rating, demand=0.0, applicable=False, conditions_supported=False, demand_available=False))


@pytest.mark.parametrize('state', CONTRACT['state_conditions'], ids=lambda s: s['group'])
def test_each_point_condition_is_checked_from_values(state):
    seed = load_seed(WORK / 'seeds' / (state['definition'].lower().replace(' ', '_') + '_impl.py'))
    values = {'enabled': True}
    if 'mode_binding' in state:
        values['mode'] = 1.0
    for pair in state['pairs']:
        values['actual_' + pair['name']] = 100.0
        values['rated_' + pair['name']] = 100.0
    assert seed.calculate(values)['evaluation_defined'] == 1.0
    for pair in state['pairs']:
        key = 'actual_' + pair['name']
        row = seed.calculate(values | {key: 100.0 + 9 * math.ulp(100.0)})
        assert row['applicable'] and not row['supported']
        assert row['evaluation_defined'] == 0.0
        with pytest.raises(ValueError):
            seed.calculate(values | {key: float('nan')})
    assert seed.calculate({'enabled': False, **({'mode': 1.0} if 'mode_binding' in state else {})}) == dict(applicable=False, supported=False, evaluation_defined=0.0)
    if 'mode_binding' in state:
        assert not seed.calculate(values | {'mode': 0.0})['applicable']
        for mode in (-1.0, 0.5, 2.0, float('nan'), True):
            with pytest.raises(ValueError): seed.calculate(values | {'mode': mode})


def test_dormant_conversion_does_not_divide_by_zero():
    seed = load_seed(WORK / 'seeds/salt_machine_electric_impl.py')
    assert seed.calculate({'active': False}) == {'demand': 0.0}
    with pytest.raises(ValueError):
        seed.calculate(dict(active=True, total_MW=1.0, count=0.0))


@pytest.fixture(scope='module')
def native_capability(tmp_path_factory):
    import importlib
    import os
    import sys
    paths = [ROOT / 'exploration/stellarator_e2e/pkg', ROOT / 'exploration/stellarator_e2e/studies', Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit']
    for path in paths:
        sys.path.insert(0, str(path))
    from simkit.study.bridge import CandidateBridge
    route = importlib.import_module('study_route')
    package = ROOT / 'exploration/stellarator_e2e/generated'
    engine = route.prepare(package, tmp_path_factory.mktemp('wi080-native-capability'))
    bridge = CandidateBridge(engine.entry_models)
    catalog = json.loads((package / 'contracts/model_contract.json').read_text())['constraint_catalog']['concrete_entries']
    predicates = {e['source_local_identity']: e['constraint_id'] for e in catalog}
    public = json.loads((package / 'inputs/stellarator_plant_params.json').read_text())
    prefix = 'stellarator_09__stellaris__'
    # Missing regeneration is a failure, never a skipped acceptance case.
    for entry in CONTRACT['public_inputs']:
        assert prefix + entry['public_suffix'] in public
    for screen in CONTRACT['screens']:
        assert screen['assertion'] in predicates
    assert 'ihx_capacity_ok' in predicates
    def execute(changes=None):
        row = engine.evaluate(bridge.build({prefix + k: v for k, v in (changes or {}).items()}))
        assert row.outputs, row
        return row
    yield execute, predicates, public
    for path in paths:
        sys.path.remove(str(path))


@pytest.mark.parametrize('screen', CONTRACT['screens'], ids=lambda s: s['name'])
def test_native_each_offered_dimension_changes_strict_capacity(native_capability, screen):
    execute, predicates, public = native_capability
    prefix = 'stellarator_09__stellaris__'
    base = execute()
    assert base.outputs[screen['defined_output']] == 1.0, screen['name']
    rating_path = screen['owner'] + '__' + screen['rating_binding'].replace('.', '__')
    if '.salt_design_' in screen['rating_binding']:
        # Purchased shaft/electric ratings derive from the independently selected pump design.
        selected_key = 'heat_transport__equipment_salt_design_flow_kg_s'
        rating = base.outputs[prefix + rating_path]
        selected = public[prefix + selected_key]
    else:
        selected_key = rating_path
        selected = rating = public[prefix + selected_key]
    demand = rating - base.outputs[screen['margin_output']]
    offers = (0.0, max(1.0, demand * 2.0)) if demand > 0 else (0.0, 1.0)
    for offered in offers:
        supplied = offered * selected / rating if '.salt_design_' in screen['rating_binding'] else offered
        # Existing selected machine price points have a strictly positive source domain.
        if selected_key in ('heat_transport__mdot_loop_rated', 'heat_transport__equipment_helium_design_shaft_MW', 'heat_transport__equipment_salt_design_flow_kg_s', 'heat_transport__equipment_salt_design_head_m') and supplied == 0:
            supplied = selected * 0.1
        row = execute({selected_key: supplied})
        assert row.outputs[screen['defined_output']] == 1.0
        margin = row.outputs[screen['margin_output']]
        expected = 'satisfied' if margin >= 0.0 else 'violated'
        assert row.responses[predicates[screen['assertion']]] == expected
        if demand > 0:
            assert (margin >= 0) is (offered > 0)


@pytest.mark.parametrize('state', CONTRACT['state_conditions'], ids=lambda s: s['group'])
def test_native_changed_offered_state_is_unsupported(native_capability, state):
    execute, predicates, _ = native_capability
    first = state['pairs'][0]
    suffix = state['owner'] + '__' + first['rated_binding']
    entry = next(x for x in CONTRACT['public_inputs'] if x['public_suffix'] == suffix)
    row = execute({suffix: entry['default'] + 1.0})
    for screen in CONTRACT['screens']:
        if screen['group'] == state['group']:
            assert row.outputs[screen['defined_output']] == 0.0
            assert row.responses[predicates[screen['assertion']]] == 'violated'


@pytest.mark.parametrize('state', CONTRACT['state_conditions'], ids=lambda s: s['group'])
def test_point_state_binary_identity_boundary(state):
    seed = load_seed(WORK / 'seeds' / (state['definition'].lower().replace(' ', '_') + '_impl.py'))
    for a in (0.0, -100.0, 562.0, 8e6):
        assert seed.same_state(a, a)
        assert seed.same_state(a, math.nextafter(a, math.inf))
        assert seed.same_state(a, a + 8 * math.ulp(a))
        assert not seed.same_state(a, a + 9 * math.ulp(a))
        assert not seed.same_state(a, a + 1.0)
    for bad in (float('nan'), float('inf'), -float('inf')):
        assert not seed.same_state(bad, bad)
        assert not seed.same_state(100.0, bad)


def test_capability_bindings_pass_semantic_type_check():
    import syside
    files = sorted((ROOT / 'exploration/stellarator_e2e/models').rglob('*.sysml'))
    _, diagnostics = syside.try_load_model([str(path) for path in files])
    errors = [str(item) for category in ('parser', 'sema')
              for item in getattr(diagnostics, category)
              if item.severity == syside.DiagnosticSeverity.Error]
    assert not errors, errors


def test_native_ihx_selected_circuit_inventory_crosses_area_capacity(native_capability):
    execute, predicates, public = native_capability
    prefix = 'stellarator_09__stellaris__'
    count_key = 'heat_transport__n_loops'
    count = public[prefix + count_key]
    low_count = count - 2
    low, high = execute({count_key: low_count}), execute({count_key: count})
    equipment = prefix + 'heat_transport__equipment__'
    for row, expected in ((low, 'violated'), (high, 'satisfied')):
        assert row.outputs[equipment + 'ihx_capacity_defined'] == 1.0
        assert row.responses[predicates['ihx_capacity_ok']] == expected
        assert row.outputs[equipment + 'ihx_capacity_margin_m2'] == row.outputs[equipment + 'ihx_installed_area'] - row.outputs[equipment + 'ihx_required_area']
    assert low.outputs[equipment + 'ihx_installed_area'] == high.outputs[equipment + 'ihx_installed_area']
    assert high.outputs[equipment + 'ihx_count'] / low.outputs[equipment + 'ihx_count'] == pytest.approx(count / low_count)
    assert high.outputs[equipment + 'hx_purchase'] / low.outputs[equipment + 'hx_purchase'] == pytest.approx(count / low_count)
