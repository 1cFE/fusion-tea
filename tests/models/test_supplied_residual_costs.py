"""WI-079 supplied purchase contracts, source capture and independent demand tests."""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ITEM = ROOT / 'work/active/WI-079_supplied-equipment-design-bases-for-residual-costs'


def seed(name):
    spec = importlib.util.spec_from_file_location(name, ITEM/'seeds'/f'{name}_impl.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.calculate


purchase = seed('supplied_purchase_cost')
auxiliary = seed('supplied_auxiliary_cooling_cost')


@pytest.mark.parametrize('amount', [0., 1., 109109123.15593052, 2e9])
def test_entered_purchase_amount_is_preserved(amount):
    assert purchase(amount, 1.) == amount
    assert auxiliary(0., 0., amount, 1.) == (0., amount, amount)


@pytest.mark.parametrize('bad', [-1., float('nan'), float('inf'), True, '100'])
def test_invalid_purchase_amount_is_refused(bad):
    with pytest.raises(ValueError):
        purchase(bad, 1.)
    with pytest.raises(ValueError):
        auxiliary(1100., 3300., bad, 1.)


@pytest.mark.parametrize('modules', [0., .5, 2., True, float('nan')])
def test_unverified_module_scope_is_refused(modules):
    with pytest.raises(ValueError):
        purchase(100., modules)
    with pytest.raises(ValueError):
        auxiliary(1100., 3300., 100., modules)


def test_auxiliary_allowance_and_cryo_package_are_separate_accounts():
    a = auxiliary(1100., 3000., 31e6, 1.)
    b = auxiliary(1100., 4000., 31e6, 1.)
    c = auxiliary(1100., 3000., 40e6, 1.)
    assert b[0] - a[0] == 1100. * 1000.
    assert b[1] == a[1]
    assert c[0] == a[0]
    assert c[2] - a[2] == 9e6


@pytest.mark.parametrize('index', [0, 1])
@pytest.mark.parametrize('bad', [-1., float('nan'), float('inf'), True])
def test_invalid_auxiliary_class_or_rate_is_refused(index, bad):
    values = [1100., 3300., 31e6, 1.]
    values[index] = bad
    with pytest.raises(ValueError):
        auxiliary(*values)


def test_auxiliary_product_overflow_is_not_a_finite_price():
    with pytest.raises(ValueError, match='Nonfinite'):
        auxiliary(1e308, 1e308, 1., 1.)


def test_every_default_is_an_exact_native_capture_and_independently_checked():
    record = json.loads((ITEM/'evidence/public-defaults.json').read_text())
    native = json.loads((ROOT/record['native_capture']).read_text())['outputs']
    independent = json.loads((ROOT/record['independent_capture']).read_text())['outputs']
    assert len(record['inputs']) == 27
    for row in record['inputs'].values():
        assert row['default'] == native[row['native_channel']]
        assert row['default'] == pytest.approx(independent[row['entering_oracle_key']], rel=1e-10)


def test_independent_oracle_retains_prices_under_changed_operating_demand(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "exploration/stellarator_e2e"))
    import verify_stellaris as oracle
    a = oracle.compute()
    monkeypatch.setattr(oracle, "IN", oracle.IN | {"n_e0": oracle.IN["n_e0"] * .95})
    b = oracle.compute()
    for key in ('blanket', 'shield', 'structure', 'vessel', 'power_supplies', 'divertor',
                'turbine', 'electric', 'heat_rejection', 'misc', 'remote_handling',
                'aux_cost', 'cryo_cost', 'waste', 'other_rpe', 'inc', 'owner',
                'supplementary', 'annual_om_unlevelized'):
        assert a[key] == b[key], key
    assert a['p_fus'] != b['p_fus']
    assert a['p_net'] != b['p_net']


@pytest.mark.parametrize('value', [0., 850.0653006674999, 3306.8890988488924])
def test_selected_class_guard_preserves_design_choice(value):
    assert seed('supplied_cost_class')(value) == value


@pytest.mark.parametrize('value', [-1., float('nan'), float('inf'), True, '3300'])
def test_selected_class_guard_rejects_invalid_procurement(value):
    with pytest.raises(ValueError):
        seed('supplied_cost_class')(value)


# Reuse the existing supported native evaluator; root's integration test owns
# demand-only fixed-package invariance. These tests cover replacement offers.
from tests.models.test_winding_pack_cost import evaluate, runtime_paths  # noqa: E402,F401

P = 'stellarator_09__stellaris__'


@pytest.mark.codegen_available
def test_native_replacement_turbine_offer_changes_capability_and_purchase(evaluate):
    baseline = evaluate()
    demand = baseline.outputs[P+'pb__p_the']
    old_amount = baseline.outputs[P+'turbine__turbine_cost__cost']
    assert demand > 0 and old_amount > 0
    offers = [(.9 * demand, old_amount), (1.1 * demand, 1.2 * old_amount)]
    rows = [evaluate({'turbine__selected_gross_MWe': rating,
                      'turbine__purchase_cost_per_module': amount})
            for rating, amount in offers]
    catalog = json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())['constraint_catalog']['concrete_entries']
    predicate = next(e['constraint_id'] for e in catalog
                     if e['source_local_identity'] == 'turbine_gross_capacity_ok')
    assert [r.responses[predicate] for r in rows] == ['violated', 'satisfied']
    for row, (rating, amount) in zip(rows, offers, strict=True):
        assert row.outputs[P+'turbine__turbine_cost__cost'] == amount
        assert row.outputs[P+'turbine__turbine_gross_capability__margin'] == pytest.approx(rating-demand)
        assert row.outputs[P+'pb__p_the'] == demand
    assert rows[1].outputs[P+'bop_capital__bop_capital'] - rows[0].outputs[P+'bop_capital__bop_capital'] == pytest.approx(.2 * old_amount)
    assert rows[1].outputs[P+'total_capital__total_capital'] > rows[0].outputs[P+'total_capital__total_capital']
    assert rows[1].outputs[P+'lcoe_calc__lcoe'] > rows[0].outputs[P+'lcoe_calc__lcoe']


@pytest.mark.codegen_available
def test_native_selected_divertor_price_reaches_replacement_without_rescheduling(evaluate):
    baseline = evaluate()
    amount = baseline.outputs[P+'divertor__divertor_cost__cost']
    changed = evaluate({'divertor__purchase_cost_per_module': 1.25 * amount})
    assert changed.outputs[P+'divertor__divertor_cost__cost'] == 1.25 * amount
    event = P+'replacement_cost_per_event__replacement_cost_per_event'
    assert changed.outputs[event] - baseline.outputs[event] == pytest.approx(.25 * amount)
    for name in ('availability', 'n_replacements', 'physical_life_fpy', 'productive_fpy'):
        assert changed.outputs[P+'calendar__'+name] == baseline.outputs[P+'calendar__'+name]
    assert changed.outputs[P+'calendar__replacement_pv'] > baseline.outputs[P+'calendar__replacement_pv']
    assert changed.outputs[P+'total_capital__total_capital'] > baseline.outputs[P+'total_capital__total_capital']


@pytest.mark.codegen_available
def test_native_auxiliary_public_schema_preserves_all_three_named_amounts(runtime_paths):
    from stellarator_tea.modules.mfe_account_costs.supplied_auxiliary_cooling_cost import Supplied_Auxiliary_Cooling_CostModule
    actual = Supplied_Auxiliary_Cooling_CostModule().run(
        aux_per_mw_in=1100., thermal_class_in=3000., purchase_cost_in=31e6, n_mod_in=1.).data
    assert actual.aux_cost == 3.3e6
    assert actual.cryo_cost == 31e6
    assert actual.cost == 34.3e6


@pytest.mark.codegen_available
def test_native_legacy_accounts_keep_selected_costs_under_changed_demand(evaluate):
    import oracle_entry as oracle
    from scripts.study.verify import package_input_values
    defaults = package_input_values(ROOT/'exploration/stellarator_e2e/generated')
    density = next(key for key, name in oracle.ENTRY_KEY_TO_ORACLE_INPUT.items() if name == 'n_e0')
    legacy = {'heat_transport__equipment_cost_mode': 0.,
              'buildings__facilities_cost_mode': 0.,
              'fuel_cycle__processing_enabled': False}
    first = evaluate(legacy)
    second = evaluate(legacy | {density.removeprefix(P): defaults[density] * .95})
    assert first.outputs[P+'pb__p_net'] != second.outputs[P+'pb__p_net']
    for suffix in ('buildings__buildings_cost__cost', 'buildings__facility_accounts__cost',
                   'precon_cost__cost', 'facility_preconstruction__cost',
                   'heat_transport__coolant__cost', 'heat_transport__cooling_selection__cost',
                   'fuel_cycle__fuel_handling__cost', 'fuel_cycle__processing_cost__cost',
                   'om_cost__annual_om', 'total_capital__total_capital'):
        assert first.outputs[P+suffix] == second.outputs[P+suffix], suffix
