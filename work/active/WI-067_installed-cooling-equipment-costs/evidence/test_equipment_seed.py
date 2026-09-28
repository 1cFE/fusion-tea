"""Author checks: independent source reconstruction, guards, and account invariants."""
import importlib.util
import json
import math
from pathlib import Path
import pytest
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('equipment_seed',HERE/'seeds/cooling_equipment_impl.py')
seed=importlib.util.module_from_spec(spec)
spec.loader.exec_module(seed)
CONTRACT=json.loads((HERE/'equipment-interface.json').read_text())
BASE={x['name']:x['default'] for x in CONTRACT['inputs']} | {'enabled':True}

def run(**changes): return seed.calculate(BASE | changes)

def test_source_geometry_reconstruction():
    # EU DEMO Table2: 2passes*7426*11.6m*19.05mm outside surface.
    r=run()
    assert r['ihx_installed_area']==pytest.approx(10310.691255459016)
    # Independent annular tube count/length equation, not area*wall expression.
    expected=8000*math.pi/4*(.01905**2-.01605**2)*14852*11.6
    assert r['tube_mass']==pytest.approx(expected)

def test_bnl_source_anchor_and_motor_boundary():
    # 735psia suction and50shaft hp reproduce550000 source machine +110000supply.
    r=run(n_loops=1,primary_shaft_MW=2*50*745.6998715822702/1e6,primary_electric_MW=1,helium_discharge_Pa=735*6894.757293168+BASE['dp_loop'])
    assert r['primary_vendor']==pytest.approx(2*660000*321.9/65.2)
    assert run(primary_electric_MW=2*BASE['primary_electric_MW'])['primary_vendor']==run()['primary_vendor']

def test_account_identities_and_delivered_exclusion():
    r=run()
    children=['primary_circulators_cost','primary_piping_cost','exchangers_cost','secondary_pumps_cost','secondary_piping_cost','inventory_cost','spares_cost']
    assert sum(r[k] for k in children)==pytest.approx(r['installed_total'])
    assert r['purchased_total']+r['installation_total']==pytest.approx(r['installed_total'])
    assert r['delivered_total']==pytest.approx(sum(r[k] for k in ['primary_vendor','primary_spare','hx_purchase','primary_pipe_purchase','secondary_pipe_purchase']))
    assert r['salt_pump_flow']*r['salt_pump_count']==pytest.approx(r['salt_flow']*BASE['n_loops'])
    assert r['salt_pump_shaft_MW']*r['salt_pump_count']==pytest.approx(r['salt_shaft_MW'])

def test_lifecycle_horizon_and_zero_discount():
    r=run(discount=0)
    assert (r['machine_events'],r['bundle_events'])==(2,1)
    assert r['replacement_annual']==pytest.approx((2*sum(r[k] for k in ['machine_event_purchase','machine_event_installation','machine_event_removal'])+sum(r[k] for k in ['bundle_event_purchase','bundle_event_installation','bundle_event_removal']))/30)
    assert run(machine_life=30,bundle_life=30)['replacement_annual']==0
    assert run(makeup_fraction=0)['consumables_annual']==0

def test_dormant_precedes_active_guards():
    r=run(enabled=False,n_mod=4,n_loops=0,helium_cp=float('nan'),tube_wall=-1)
    assert all(v==0 for v in r.values())

@pytest.mark.parametrize('changes',[{'n_mod':2},{'n_loops':14.5},{'tube_wall':.01},{'helium_cp':float('nan')},{'eta_motor':1.1},{'q_ihx_MW':0},{'helium_hot_K':730},{'accessory_mass':1e9}])
def test_invalid_active_inputs(changes):
    with pytest.raises(ValueError): run(**changes)

def test_preserved_failures_and_sensitivity():
    r=run()
    assert r['cycle_temperature_gap']==15 and not r['cycle_interface_ok']
    assert not r['inventory_source_volume_ok'] and not r['salt_bulk_scale_ok']
    assert not run(n_loops=14)['pump_type_ok']
    assert run(costscale=2)['installed_total']==pytest.approx(2*r['installed_total'])
    assert run(layout_multiplier=2)['salt_straight_loss']==pytest.approx(2*r['salt_straight_loss'])
    assert run(saltprice_source_choice=1)['salt_unit_price']==pytest.approx(2.53*321.9/271)

def test_native_tuple_abi_matches_saved_generated_order():
    from types import SimpleNamespace
    native=json.loads((HERE/'equipment-generated-abi.json').read_text())['output_order']
    typed_shape=SimpleNamespace(**{k+'_in':v for k,v in BASE.items()})
    values=seed.run_cooling_equipment(typed_shape)
    assert len(values)==109
    assert dict(zip(native,values,strict=True))==run()
