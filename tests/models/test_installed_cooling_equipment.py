"""Current cooling units/accounts with WI-078 supplied design-point and stock fixtures.

WI-067 historical files stay unchanged; current equipment fixtures explicitly choose
a price point and procurement stocks independently of the operating test point.
"""
import importlib
import json
import math
import os
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
P = 'stellarator_09__stellaris__'
E = 'heat_transport__equipment__'


@pytest.fixture(scope='module')
def runtime():
    paths = [ROOT/'exploration/stellarator_e2e/pkg', ROOT/'exploration/stellarator_e2e/studies', ROOT/'exploration/stellarator_e2e']
    if os.environ.get('STOP_PARSER_TEAX_ROOT'):
        paths.append(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit')
    for path in paths:
        sys.path.insert(0, str(path))
    yield
    for path in paths:
        sys.path.remove(str(path))


@pytest.fixture(scope='module')
def equipment(runtime):
    module = importlib.import_module('stellarator_tea.modules.mfe_cooling_equipment.cooling_equipment')
    assert Path(module.__file__).resolve().is_relative_to(ROOT/'exploration/stellarator_e2e/generated')
    interface = json.loads((ROOT/'work/active/WI-067_installed-cooling-equipment-costs/evidence/equipment-interface.json').read_text())
    defaults = {i['name'] + '_in': i['default'] for i in interface['inputs']}
    selected = json.loads((ROOT/'work/active/WI-078_supplied-cooling-design-point-evaluation/evidence/selected-defaults.json').read_text())['selected_inputs']
    defaults.update({name + '_in': value for name, value in selected.items()})
    defaults['enabled_in'] = True
    defaults['stainless_fabrication_usd2017_per_kg_in'] = 310.0
    return lambda **changes: module.Cooling_EquipmentModule().run(**(defaults | changes)).data.model_dump()


def test_generated_equipment_conservation_and_distinct_accounts(equipment):
    row = equipment()
    names = ['primary_circulators_cost', 'primary_piping_cost', 'exchangers_cost', 'secondary_pumps_cost', 'secondary_piping_cost', 'inventory_cost', 'spares_cost']
    assert sum(row[n] for n in names) == pytest.approx(row['installed_total'], rel=2e-13)
    assert row['purchased_total'] + row['installation_total'] == pytest.approx(row['installed_total'])
    assert row['circulator_count'] == row['salt_pump_count'] == 36
    assert row['ihx_count'] == 18
    assert row['salt_flow'] * 18 * 1560 * 195 / 1e6 == pytest.approx(3013.914942)
    assert row['salt_shaft_MW'] / .95 == pytest.approx(row['salt_electric_MW'])
    assert row['conversion_heat_MW'] == pytest.approx(3013.914942 + row['salt_shaft_MW'])
    assert row['ihx_installed_area'] == pytest.approx(10310.691254572363)
    assert not row['pressure_qualified'] and not row['inventory_complete']
    assert not row['cycle_interface_ok'] and row['cycle_temperature_gap'] == 15


def test_drive_losses_do_not_resize_shaft_based_purchase(equipment):
    base = equipment()
    changed = equipment(primary_electric_MW_in=100.)
    assert changed['primary_vendor'] == base['primary_vendor']
    assert changed['circulator_electric_MW'] > base['circulator_electric_MW']


def test_layout_inventory_and_horizon_sensitivities(equipment):
    base = equipment()
    long = equipment(layout_multiplier_in=2.)
    assert long['primary_pipe_mass'] == pytest.approx(2*base['primary_pipe_mass'])
    assert long['primary_piping_cost'] == pytest.approx(2*base['primary_piping_cost'])
    assert long['salt_straight_loss'] == pytest.approx(2*base['salt_straight_loss'])
    assert long['exchangers_cost'] == base['exchangers_cost']
    for gas in ('helium', 'salt'):
        assert long[f'{gas}_required_fill_mass_kg'] > base[f'{gas}_required_fill_mass_kg']
        assert long[f'{gas}_inventory_mass'] == base[f'{gas}_inventory_mass']
        assert long[f'{gas}_inventory_cost'] == base[f'{gas}_inventory_cost']
    assert not long['represented_fill_ok']
    assert not long['inventory_complete']
    assert equipment(machine_life_in=30., bundle_life_in=30.)['replacement_annual'] == 0
    zero = equipment(discount_in=0.)
    machines = sum(base[n] for n in ('machine_event_purchase','machine_event_installation','machine_event_removal'))
    bundle = sum(base[n] for n in ('bundle_event_purchase','bundle_event_installation','bundle_event_removal'))
    assert zero['replacement_annual'] == pytest.approx((2*machines+bundle)/30)


@pytest.mark.parametrize('change', [{'n_loops_in': 0.}, {'n_loops_in': 14.5}, {'n_mod_in':2.}, {'tube_wall_in':.02}, {'discount_in': math.nan}])
def test_active_invalid_inputs_fail(equipment, change):
    with pytest.raises(ValueError):
        equipment(**change)


def test_disabled_generic_equipment_is_finite(equipment):
    row = equipment(enabled_in=False, n_loops_in=0., q_ihx_MW_in=0.)
    assert all(value == 0 for value in row.values())


@pytest.fixture(scope='module')
def evaluate(runtime, tmp_path_factory):
    from simkit.study.bridge import CandidateBridge
    import study_route
    engine = study_route.prepare(ROOT/'exploration/stellarator_e2e/generated', tmp_path_factory.mktemp('cooling-native'))
    bridge = CandidateBridge(engine.entry_models)
    def run(**changes):
        row = engine.evaluate(bridge.build({P+k:v for k,v in changes.items()}))
        assert row.outputs, row
        return row.outputs
    return run


def test_actual_native_cost_and_energy_selectors(evaluate):
    legacy = evaluate(turbine__matched_cycle_enabled=0., heat_rejection__cooling_water_enabled=0., heat_transport__equipment_cost_mode=0., heat_transport__secondary_energy_mode=0.)
    cost = evaluate(turbine__matched_cycle_enabled=0., heat_rejection__cooling_water_enabled=0., heat_transport__equipment_cost_mode=1., heat_transport__secondary_energy_mode=0.)
    full = evaluate(turbine__matched_cycle_enabled=0., heat_rejection__cooling_water_enabled=0., heat_transport__equipment_cost_mode=1., heat_transport__secondary_energy_mode=1.)
    assert cost[P+'pb__p_net'] == legacy[P+'pb__p_net']
    assert full[P+'pb__p_net'] < cost[P+'pb__p_net']
    new = cost[P+E+'installed_total']
    old = legacy[P+'heat_transport__coolant__cost']
    assert cost[P+'cas22_capital__cas22_capital']-legacy[P+'cas22_capital__cas22_capital'] == pytest.approx(new-old)
    assert full[P+'heat_transport__cooling_energy__electric_total']-cost[P+'heat_transport__cooling_energy__electric_total'] == pytest.approx(full[P+E+'salt_electric_MW'])
    assert full[P+'cooling_annual__cas72_total'] == pytest.approx(full[P+'calendar__cas72_annual'] + full[P+E+'replacement_annual'])
    assert full[P+'cooling_annual__annual_om'] == pytest.approx(full[P+'om_cost__annual_om'] + full[P+E+'consumables_annual'])


def test_native_replacement_reaches_lcoe_without_changing_capital(evaluate):
    # Isolate cooling purchase accounting from the separate facilities account.
    # Supplied facilities geometry also stays fixed under retirement-demand changes.
    base = evaluate(buildings__facilities_cost_mode=0.)
    long = evaluate(buildings__facilities_cost_mode=0.,
                    heat_transport__equipment_machine_life=30.,
                    heat_transport__equipment_bundle_life=30.)
    assert long[P+'total_capital__total_capital'] == base[P+'total_capital__total_capital']
    assert long[P+'pb__p_net'] == base[P+'pb__p_net']
    assert long[P+'lcoe_calc__lcoe'] < base[P+'lcoe_calc__lcoe']


@pytest.mark.parametrize('control_index', range(4))
def test_primary_controls_reach_current_native_comparison(runtime, tmp_path, control_index):
    # Reuse the historical hydraulic perturbations on the current supplied design.
    # This is a new evaluation, not a replay of retired magnet/facility selection.
    import oracle_entry
    import study_route
    historical = json.loads((ROOT/'.project/active/primary-loop-current-consumers/implementation/oracle-before.json').read_text())['controls'][control_index]
    inverse = {v:k for k,v in oracle_entry.ENTRY_KEY_TO_ORACLE_INPUT.items()}
    point = {inverse[k]:v for k,v in historical['overrides'].items()}
    # These controls explicitly exercise direct/legacy primary closure; disable
    # the matched cycle, which requires its distinct live heat-boundary contract.
    point.update({P+'turbine__matched_cycle_enabled':0., P+'heat_rejection__cooling_water_enabled':0.})
    cases, _ = study_route.run_points('cooling-current-primary-control', [point], tmp_path)
    case = cases[0]
    assert case.state == 'completed'
    expected = oracle_entry.evaluate(case.inputs)
    assert set(expected) <= set(case.outputs)
    for key, value in expected.items():
        assert case.outputs[key] == pytest.approx(value, rel=1e-9, abs=1e-9), key
    # Required flow and heat recovery retain their physical balance identities.
    q = P+'heat_transport__primary_loop__'
    assert case.outputs[q+'q_ihx'] == pytest.approx(case.outputs[P+'blanket__source_heat__q_source'] + case.outputs[q+'w_fluid'])
    assert case.outputs[q+'mdot_loop'] == pytest.approx(case.outputs[q+'mdot']/case.outputs[P+E+'ihx_count'])


@pytest.mark.parametrize('proposal_id', ['r2-forward', 'r2-table5'])
def test_retired_current_selection_controls_are_rejected(runtime, tmp_path, proposal_id):
    # Old zero-boundary proposals contain automatic magnet-selection inputs.
    # Preserve them as historical evidence, and require explicit migration.
    import study_route
    records = json.loads((ROOT/'work/orchestration/goals/installed-cooling-equipment-costs/evidence/starting-cases.json').read_text())['cases']
    point = next(row['inputs'] for row in records if row['proposal_id'] == proposal_id)
    with pytest.raises(study_route.RouteError, match='retired magnet entry keys'):
        study_route.run_points('cooling-retired-selection-refusal', [point], tmp_path)


@pytest.mark.parametrize('enabled,cost,energy,valid', [
    (False,0.,0.,True),(True,0.,0.,True),(True,1.,0.,True),(True,1.,1.,True),
    (False,1.,0.,False),(False,0.,1.,False),(True,.5,0.,False),
    (True,1.,-1.,False),(True,math.nan,0.,False)])
def test_scenario_guard_prevents_free_cooling_and_negative_demand(runtime, enabled, cost, energy, valid):
    mod = importlib.import_module('stellarator_tea.modules.mfe_cooling_accounts.cooling_scenario_guard').Cooling_Scenario_GuardModule()
    args = dict(equipment_enabled_in=enabled, cost_mode_in=cost, energy_mode_in=energy)
    if valid:
        result = mod.run(**args).data
        assert result.cost_mode == cost and result.energy_mode == energy
    else:
        with pytest.raises(ValueError, match='Cooling Scenario Guard'):
            mod.run(**args)


def test_matched_direct_delta_and_delivered_shipping_reach_total_capital(evaluate):
    old = evaluate(turbine__matched_cycle_enabled=0., heat_rejection__cooling_water_enabled=0., heat_transport__equipment_cost_mode=0., heat_transport__secondary_energy_mode=0.)
    new = evaluate(turbine__matched_cycle_enabled=0., heat_rejection__cooling_water_enabled=0., heat_transport__equipment_cost_mode=1., heat_transport__secondary_energy_mode=0.)
    direct_change = new[P+E+'installed_total'] - old[P+'heat_transport__coolant__cost']
    # Independent reconciliation using the declared FOAK10%, indirect20% at8/6years,
    # shipping1.5%, tax1%, insurance1.5%. Other equipment and net output are matched.
    cas20_change = 1.1 * direct_change
    cas30_change = (.2 * 8 / 6) * cas20_change
    supplementary_change = (.015*(cas20_change-new[P+E+'delivered_total'])
                            + .01*cas20_change + .015*(cas20_change+cas30_change))
    assert new[P+'total_capital__total_capital'] - old[P+'total_capital__total_capital'] == pytest.approx(cas20_change+cas30_change+supplementary_change, rel=2e-12)
