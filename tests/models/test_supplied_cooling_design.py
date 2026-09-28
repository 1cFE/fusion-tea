"""WI-078 selected cooling prices/stocks and independent operating diagnostics.

Seed checks precede integration; native checks require the regenerated interface.
They establish represented scalar/stock checks, not machine off-design qualification.
"""
from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
from types import SimpleNamespace
import pytest

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT/'work/active/WI-078_supplied-cooling-design-point-evaluation'
P = 'stellarator_09__stellaris__'
E = P+'heat_transport__equipment__'


def load_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope='module')
def seed():
    return load_file('wi078_cooling_seed', WORK/'seeds/cooling_equipment_impl.py')


@pytest.fixture(scope='module')
def parameters():
    interface = json.loads((ROOT/'work/active/WI-067_installed-cooling-equipment-costs/evidence/equipment-interface.json').read_text())
    values = {i['name']: i['default'] for i in interface['inputs']}
    values.update(json.loads((WORK/'evidence/selected-defaults.json').read_text())['selected_inputs'])
    values.update(enabled=True, stainless_fabrication_usd2017_per_kg=310.)
    return values


FIXED_PRICE = ('primary_vendor','primary_spare','secondary_vendor','secondary_spare',
               'machine_event_purchase','machine_event_installation','machine_event_removal',
               'replacement_annual','helium_inventory_cost','salt_inventory_cost','spares_cost',
               'primary_pipe_purchase','secondary_pipe_purchase','hx_purchase','installed_total')


def test_demand_changes_keep_supplied_design_price(seed, parameters):
    base = seed.calculate(parameters)
    changed = seed.calculate(parameters | dict(q_ihx_MW=parameters['q_ihx_MW']*1.1,
        primary_shaft_MW=parameters['primary_shaft_MW']*1.1,
        primary_electric_MW=parameters['primary_electric_MW']*1.1,
        mdot_loop=parameters['mdot_loop']*1.1,dp_loop=parameters['dp_loop']*1.1))
    for key in FIXED_PRICE:
        assert changed[key] == base[key], key
    assert changed['salt_flow'] > base['salt_flow']
    assert changed['circulator_shaft_MW'] > base['circulator_shaft_MW']
    assert changed['ihx_required_area'] > base['ihx_required_area']
    assert not changed['machine_off_design_performance_qualified']


@pytest.mark.parametrize('key', ['helium_design_shaft_MW','helium_design_suction_Pa',
    'salt_design_flow_kg_s','salt_design_head_m'])
def test_selected_price_point_changes_only_design_price(seed, parameters, key):
    base = seed.calculate(parameters)
    changed = seed.calculate(parameters | {key:parameters[key]*1.1})
    account = 'primary_vendor' if key.startswith('helium') else 'secondary_vendor'
    assert changed[account] != base[account]
    for name in ('salt_flow','salt_shaft_MW','salt_electric_MW','conversion_heat_MW',
                 'circulator_shaft_MW','circulator_flow','ihx_required_area'):
        assert changed[name] == base[name]
    assert not changed['machine_off_design_performance_qualified']


@pytest.mark.parametrize('fraction', [0., .5, 1., 1.2])
def test_stock_coverage_is_supplied_minus_represented_fill(seed, parameters, fraction):
    base = seed.calculate(parameters)
    chosen = {f'{gas}_purchased_mass_kg':base[f'{gas}_required_fill_mass_kg']*fraction
              for gas in ('helium','salt')}
    row = seed.calculate(parameters | chosen)
    for gas in ('helium','salt'):
        assert row[f'{gas}_inventory_mass'] == chosen[f'{gas}_purchased_mass_kg']
        assert row[f'{gas}_represented_fill_margin_kg'] == pytest.approx(
            chosen[f'{gas}_purchased_mass_kg']-base[f'{gas}_required_fill_mass_kg'])
        assert row[f'{gas}_inventory_cost'] == pytest.approx(base[f'{gas}_inventory_cost']*
            chosen[f'{gas}_purchased_mass_kg']/base[f'{gas}_inventory_mass'])
    assert row['represented_fill_defined'] == 1
    assert row['represented_fill_ok'] is (fraction >= 1)
    assert not row['inventory_complete']


def test_one_short_stock_fails_even_with_other_surplus(seed, parameters):
    base = seed.calculate(parameters)
    for short in ('helium','salt'):
        row = seed.calculate(parameters | {f'{gas}_purchased_mass_kg':
            base[f'{gas}_required_fill_mass_kg']*(.5 if gas==short else 2.) for gas in ('helium','salt')})
        assert not row['represented_fill_ok']


def test_reserve_and_operating_density_do_not_buy_stock(seed, parameters):
    base=seed.calculate(parameters)
    reserve=seed.calculate(parameters | dict(inventory_reserve=2.))
    density=seed.calculate(parameters | dict(helium_hot_K=parameters['helium_hot_K']+5.))
    assert reserve['helium_inventory_target_mass_kg'] > base['helium_inventory_target_mass_kg']
    assert density['helium_required_fill_mass_kg'] != base['helium_required_fill_mass_kg']
    for row in (reserve,density):
        for name in FIXED_PRICE:
            assert row[name] == base[name]


def test_ihx_fixed_geometry_retains_failure(seed, parameters):
    base=seed.calculate(parameters)
    duty_at_limit=parameters['q_ihx_MW']*base['ihx_installed_area']/base['ihx_required_area']
    for ratio in (.9,1.1):
        row=seed.calculate(parameters | dict(q_ihx_MW=duty_at_limit*ratio))
        assert row['ihx_capacity_ok'] is (ratio<1)
        assert row['ihx_installed_area'] == base['ihx_installed_area']
        assert row['hx_purchase'] == base['hx_purchase']


def test_price_domain_and_dormancy_are_separate(seed, parameters):
    base=seed.calculate(parameters)
    row=seed.calculate(parameters | dict(salt_design_flow_kg_s=10000.))
    assert not row['design_pump_type_ok']
    assert row['pump_type_ok'] == base['pump_type_ok']
    assert row['salt_flow'] == base['salt_flow']
    assert not row['machine_off_design_performance_qualified']
    dormant=seed.calculate({'enabled':False})
    assert dormant['represented_fill_defined']==0
    assert not dormant['represented_fill_ok']


@pytest.mark.parametrize('key,value', [('helium_purchased_mass_kg',-1.),
    ('salt_purchased_mass_kg',-1.),('salt_design_eta_p',0.),('salt_design_eta_motor',1.1),
    ('helium_design_shaft_MW',float('nan'))])
def test_bad_selected_design_refuses(seed, parameters, key, value):
    with pytest.raises(ValueError): seed.calculate(parameters | {key:value})


def test_independent_oracle_all_new_outputs(seed, parameters):
    oracle=load_file('wi078_cooling_oracle', ROOT/'exploration/stellarator_e2e/oracle_cooling.py')
    names=set(seed.OUTPUT_NAMES)&set(oracle.NUMERIC_OUTPUTS+oracle.BOOLEAN_OUTPUTS)
    for delta in ({},{'q_ihx_MW':parameters['q_ihx_MW']*.9},
                  {'helium_purchased_mass_kg':0.}, {'salt_design_head_m':50.}):
        args=parameters|delta
        a=seed.calculate(args); b=oracle.calculate(args|{'fabrication_rate_2017':args['stainless_fabrication_usd2017_per_kg']})
        for key in names:
            if isinstance(a[key],bool): assert a[key] == b[key], key
            else: assert a[key] == pytest.approx(b[key],rel=2e-9,abs=2e-7),key


@pytest.fixture(scope='module')
def native(tmp_path_factory):
    # Explicit skip until the coordinator regenerates; a skip is not acceptance.
    params=json.loads((ROOT/'exploration/stellarator_e2e/generated/inputs/stellarator_plant_params.json').read_text())
    if P+'heat_transport__equipment_helium_design_shaft_MW' not in params:
        pytest.skip('WI-078 native integration not yet generated')
    import sys
    paths=[ROOT/'exploration/stellarator_e2e/pkg',ROOT/'exploration/stellarator_e2e/studies']
    if os.environ.get('STOP_PARSER_TEAX_ROOT'):
        paths.append(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit')
    for path in paths:
        sys.path.insert(0,str(path))
    import study_route
    from simkit.study.bridge import CandidateBridge
    engine=study_route.prepare(ROOT/'exploration/stellarator_e2e/generated',tmp_path_factory.mktemp('wi078-native'))
    bridge=CandidateBridge(engine.entry_models)
    catalog=json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())['constraint_catalog']['concrete_entries']
    predicates={e['source_local_identity']:e['constraint_id'] for e in catalog}
    def run(**changes):
        row=engine.evaluate(bridge.build({P+k:v for k,v in changes.items()}))
        assert row.outputs,row
        return row
    run.predicates=predicates
    return run


@pytest.mark.parametrize('fraction',[0.,.5,1.2])
def test_native_supplied_stocks_preserved(native, fraction):
    base=native().outputs
    changes={f'heat_transport__equipment_{gas}_purchased_mass_kg':
             base[E+f'{gas}_required_fill_mass_kg']*fraction for gas in ('helium','salt')}
    result=native(**changes)
    assert result.responses[native.predicates['represented_coolant_fill_ok']] == ('satisfied' if fraction>=1 else 'violated')
    row=result.outputs
    for gas in ('helium','salt'):
        chosen=changes[f'heat_transport__equipment_{gas}_purchased_mass_kg']
        assert row[E+f'{gas}_inventory_mass']==chosen
        assert row[E+f'{gas}_inventory_cost']==pytest.approx(base[E+f'{gas}_inventory_cost']*chosen/base[E+f'{gas}_inventory_mass'])
        assert (row[E+f'{gas}_represented_fill_margin_kg']>=0) is (fraction>=1)
    assert row[E+'represented_fill_defined']==1
    assert not row[E+'inventory_complete']


def test_native_flow_ceiling_separate_from_hydraulics(native):
    base=native().outputs
    demand=base[P+'heat_transport__primary_loop__mdot_loop']
    for ratio in (.8,1.2):
        result=native(heat_transport__mdot_loop_rated=demand*ratio)
        assert result.responses[native.predicates['loop_capacity_ok']] == ('satisfied' if ratio>=1 else 'violated')
        row=result.outputs
        assert (row[P+'heat_transport__primary_loop__capacity_margin']>=0) is (ratio>=1)
        for suffix in ('dp_loop','w_fluid','mdot_loop'):
            assert row[P+'heat_transport__primary_loop__'+suffix]==base[P+'heat_transport__primary_loop__'+suffix]
        assert row[E+'installed_total']==base[E+'installed_total']


def test_primary_seed_ceiling_changes_no_hydraulics():
    loop=load_file('wi078_primary_seed',WORK/'seeds/primary_coolant_loop_impl.py')
    args=dict(cp_in=5193.,dT_blanket_in=200.,gamma_in=5/3,q_source_in=2700.,n_loops_in=14.,
              f_loss_in=1.,dp_loop_ref_in=329187.1856931558,mdot_loop_ref_in=225.07777777777778,
              mdot_loop_rated_in=225.07777777777778,p_loop_in=8e6,T_in_in=573.15,
              eta_is_in=.772796639536644,eta_drive_in=1.,loop_live_in=1.,
              eta_p_direct_in=0.,p_pump_direct_in=0.)
    base=loop.calculate(SimpleNamespace(**args))
    for offered in (100.,300.):
        row=loop.calculate(SimpleNamespace(**(args|{'mdot_loop_rated_in':offered})))
        for name,value in row.items():
            if name=='capacity_margin': assert value==offered-base['mdot_loop']
            else: assert value==base[name]


def test_native_demand_does_not_reprice_design(native):
    base=native().outputs
    row=native(heat_transport__loop_dT_blanket=202.).outputs
    assert row[P+'heat_transport__primary_loop__mdot_loop'] != base[P+'heat_transport__primary_loop__mdot_loop']
    for name in FIXED_PRICE:
        assert row[E+name]==base[E+name],name
    assert not row[E+'machine_off_design_performance_qualified']


def test_native_selected_price_does_not_change_demand(native):
    base=native().outputs
    row=native(heat_transport__equipment_helium_design_shaft_MW=7.).outputs
    assert row[E+'primary_vendor'] != base[E+'primary_vendor']
    for name in ('salt_flow','salt_shaft_MW','circulator_shaft_MW','ihx_required_area'):
        assert row[E+name]==base[E+name]
