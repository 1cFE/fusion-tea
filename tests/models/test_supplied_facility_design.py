"""WI-076 selected facilities: arithmetic checks plus actual generated/native execution."""
import importlib.util
import json
import os
import sys
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[2]
WI=ROOT/'work/active/WI-076_supplied-facility-design-evaluation'
PREFIX='stellarator_09__stellaris__buildings__'

@pytest.fixture(scope='module',autouse=True)
def runtime():
    paths=[str(ROOT/'exploration/stellarator_e2e/pkg'),str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit')]
    for p in paths:sys.path.insert(0,p)
    yield
    for p in paths:sys.path.remove(p)

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

@pytest.fixture(scope='module')
def calc(runtime):
    return load(WI/'seeds/facility_layout_impl.py','wi076_seed')

@pytest.fixture
def inputs():
    r=json.loads((WI/'evidence/selected-design-migration.json').read_text())
    x=r['entering_inputs']|r['selected_inputs']
    for k in ('facilities_capacity_mode','occupancy_aspect_ratio'):x.pop(k)
    return x

def geometry_only(out):
    return {k:v for k,v in out.items() if k.endswith(('_clear_length','_clear_width','_clear_height','_clear_area','_gross_area','_air_volume','_concrete','_formwork','_rebar')) or k in ('parcel_area','controlled_air_volume')}

def test_entering_design_replay(calc,inputs):
    old=json.loads((WI/'evidence/selected-design-migration.json').read_text())['entering_outputs']
    out=calc.calculate(inputs)
    for k,v in old.items():
        if k!='capacity_mode':assert out[k]==pytest.approx(v,rel=1e-11,abs=1e-9),k
    for r in calc.ROOMS:
        for axis in ('length','width','height'):assert out[r+'_clear_'+axis]==inputs['selected_'+r+'_'+axis]
    # Preserve the real finite-precision residual, including its failed predicate.
    assert out['occupancy_area_margin_m2']<0

@pytest.mark.parametrize('key,value',[('major_radius',15.),('blanket_volume',2000.),('component_hold_days',3652.5),('cooling_circuits',18.),('hx_shell_bore',4.),('turbine_length',80.),('administration_occupants',300.)])
def test_demand_does_not_purchase_geometry(calc,inputs,key,value):
    base=calc.calculate(inputs);other=calc.calculate(inputs|{key:value})
    assert geometry_only(base)==geometry_only(other)
    assert other!=base

def test_package_shortfall_and_zero_preserved(calc,inputs):
    need=calc.calculate(inputs)['blanket_packages_required_per_sector']
    for count in (0.,need-1,need):
        out=calc.calculate(inputs|{'selected_blanket_packages_per_sector':count})
        assert out['blanket_packages_per_sector']==count
        assert (out['unused_material_capacity']>=0)==(count>=need)
        assert out['packages_per_sector']==count+inputs['divertor_packages_per_sector']
    empty=calc.calculate(inputs|{'selected_blanket_packages_per_sector':0.,'divertor_packages_per_sector':0.})
    assert empty['initial_clean_required']==0

OFFERS=('clean_positions','dirty_buffer_positions','dirty_store_positions')+tuple('cooling_'+z+'_'+k+'_positions' for z in ('clean','dirty') for k in ('helium','salt','bundle'))
@pytest.mark.parametrize('key',OFFERS)
def test_supplied_slots_do_not_expand_room(calc,inputs,key):
    base=calc.calculate(inputs)
    out=calc.calculate(inputs|{key:0.})
    name=key.replace('_positions','_allocated') if key.startswith('cooling_') else key+'_allocated'
    assert out[name]==0
    assert out['capacity_margin_units']<0
    assert geometry_only(out)==geometry_only(base)

@pytest.mark.parametrize('key',('selected_sector_wing_east_length','selected_cooling_hall_length','selected_turbine_hall_length'))
def test_constructible_insufficient_room(calc,inputs,key):
    base=calc.calculate(inputs);out=calc.calculate(inputs|{key:inputs[key]-1})
    assert out['geometry_fit_margin_m']<0
    room=key.removeprefix('selected_').removesuffix('_length')
    assert out[room+'_clear_length']==inputs[key]-1
    assert out[room+'_sub_concrete']<base[room+'_sub_concrete']
    assert out['parcel_area']==base['parcel_area']

def test_unequal_wing_controls_served_volume(calc,inputs):
    base=calc.calculate(inputs);out=calc.calculate(inputs|{'selected_sector_wing_east_length':inputs['selected_sector_wing_east_length']+1})
    lane=inputs['selected_sector_wing_east_width']-56-2*inputs['nuclear_wall']
    assert out['controlled_air_volume']-base['controlled_air_volume']==pytest.approx((lane+28)*inputs['selected_sector_wing_east_height'])
    for direction in ('north','west','south'):
        for key,value in base.items():
            if key.startswith('sector_wing_'+direction+'_') and 'required' not in key:assert out[key]==value

def test_independent_parcel_and_occupancy(calc,inputs):
    base=calc.calculate(inputs)
    for delta in (-1.,1.):
        out=calc.calculate(inputs|{'selected_parcel_length':inputs['selected_parcel_length']+delta})
        assert (out['parcel_fit_margin_m']>=0)==(delta>0)
        assert out['parcel_area']==(inputs['selected_parcel_length']+delta)*inputs['selected_parcel_width']
        assert out['reactor_hall_sub_concrete']==base['reactor_hall_sub_concrete']
    out=calc.calculate(inputs|{f'selected_{r}_length':inputs[f'selected_{r}_length']+1 for r in ('administration','control','security')})
    assert out['occupancy_area_margin_m2']>0

@pytest.mark.parametrize('changes',[{'selected_cooling_annex_north_depth':1.},{'selected_blanket_packages_per_sector':1.5},{'selected_reactor_hall_length':float('nan')},{'sector_count':3.}])
def test_unsupported_geometry_or_topology(calc,inputs,changes):
    with pytest.raises(ValueError):calc.calculate(inputs|changes)

@pytest.mark.parametrize('changes',[{}, {'selected_sector_wing_east_length':155.}, {'major_radius':15.}, {'selected_blanket_packages_per_sector':0.}, {'selected_parcel_length':800.}, {'cooling_circuits':18.}, {'cooling_hold_days':500.}])
def test_independent_oracle(calc,inputs,changes):
    oracle=load(ROOT/'exploration/stellarator_e2e/oracle_facilities.py','wi076_oracle')
    x=inputs|changes;diag=calc.diagnostics(x);actual=diag['outputs']
    params=oracle.DEFAULTS|{k:v for k,v in x.items() if k not in calc.UPSTREAM}
    physical={k:x[k] for k in calc.UPSTREAM}
    expected=oracle.layout(params,physical,diag['calendar']['events'])
    assert set(actual)<=set(expected)
    for k,v in actual.items():assert expected[k]==pytest.approx(v,rel=1e-10,abs=1e-8),k

@pytest.fixture(scope='module')
def native(tmp_path_factory,runtime):
    contract=json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
    if not any('selected_parcel_length' in p['qualified_name'] for p in contract['parameters']):
        pytest.skip('WI-076 current package regeneration pending; native acceptance unverified')
    import importlib
    path=str(ROOT/'exploration/stellarator_e2e/studies');sys.path.insert(0,path)
    route=importlib.import_module('study_route')
    from simkit.study.bridge import CandidateBridge
    engine=route.prepare(ROOT/'exploration/stellarator_e2e/generated',tmp_path_factory.mktemp('supplied-facility-native'))
    yield engine,CandidateBridge(engine.entry_models),contract['constraint_catalog']['concrete_entries']
    sys.path.remove(path)

@pytest.mark.parametrize('changes,predicate,failed',[
    ({'selected_blanket_packages_per_sector':0.},'facility_material_capacity_ok',True),
    ({'selected_blanket_packages_per_sector':32.},'facility_material_capacity_ok',False),
    ({'clean_positions':0.},'facility_capacity_ok',True),
    ({'selected_turbine_hall_length':63.},'facility_geometry_ok',True),
    ({'selected_parcel_length':800.},'facility_parcel_ok',True),
    ({'selected_parcel_length':900.},'facility_parcel_ok',False),
    ({'selected_administration_length':80.,'selected_control_length':35.,'selected_security_length':20.},'facility_occupancy_ok',False),
])
def test_native_supplied_failure_and_sufficiency(native,changes,predicate,failed):
    engine,bridge,catalog=native
    row=engine.evaluate(bridge.build({PREFIX+k:v for k,v in changes.items()}))
    assert row.outputs
    entry=next(e for e in catalog if predicate in e['source_local_identity'])
    assert row.responses[entry['constraint_id']] == ('violated' if failed else 'satisfied')
    for key,value in changes.items():
        if key.startswith('selected_') and key.endswith(('_length','_width','_height')) and not key.startswith('selected_parcel'):
            output=PREFIX+'layout__'+key.removeprefix('selected_').rsplit('_',1)[0]+'_clear_'+key.rsplit('_',1)[1]
            assert row.outputs[output]==value

@pytest.mark.parametrize('change', [{'turbine_length':80.},{'component_hold_days':3652.5},{'selected_blanket_packages_per_sector':0.}])
def test_native_fixed_design_cost_propagation(native,change):
    engine,bridge,catalog=native
    base=engine.evaluate(bridge.build({}));other=engine.evaluate(bridge.build({PREFIX+k:v for k,v in change.items()}))
    keys=[k for k in base.outputs if k.startswith(PREFIX) and (k.endswith(('_sub_concrete','_super_concrete','_sub_formwork','_super_formwork','_sub_rebar','_super_rebar','_clear_length','_clear_width','_clear_height','__civil_capital','__cost_2025')) or '__facility_land__' in k or '__ventilation__' in k)]
    assert keys
    for key in keys:assert other.outputs[key]==base.outputs[key],key


def test_native_selected_parcel_price(native,inputs):
    engine,bridge,catalog=native
    base=engine.evaluate(bridge.build({}));length=inputs['selected_parcel_length']+10
    other=engine.evaluate(bridge.build({PREFIX+'selected_parcel_length':length}))
    assert other.outputs[PREFIX+'layout__parcel_area']==length*inputs['selected_parcel_width']
    land=PREFIX+'facility_land__cost'
    assert other.outputs[land]/base.outputs[land]==pytest.approx(length/inputs['selected_parcel_length'])
    assert other.outputs[PREFIX+'civil_rollup__civil_capital']==base.outputs[PREFIX+'civil_rollup__civil_capital']


def test_native_selected_room_price(native):
    engine,bridge,catalog=native
    base=engine.evaluate(bridge.build({}));other=engine.evaluate(bridge.build({PREFIX+'selected_turbine_hall_length':65.}))
    assert other.outputs[PREFIX+'layout__turbine_hall_clear_length']==65.
    assert other.outputs[PREFIX+'civil_rollup__civil_capital']>base.outputs[PREFIX+'civil_rollup__civil_capital']
    assert other.outputs[PREFIX+'facility_land__cost']==base.outputs[PREFIX+'facility_land__cost']

@pytest.mark.parametrize('axis', ['x','y'])
@pytest.mark.parametrize('shift', [-10.,10.])
def test_native_signed_parcel_translation(native,inputs,axis,shift):
    engine,bridge,catalog=native
    base=engine.evaluate(bridge.build({}))
    other=engine.evaluate(bridge.build({PREFIX+f'parcel_origin_{axis}_offset':shift}))
    absolute=PREFIX+f'selected_parcel_{axis}_min__selected_parcel_{axis}_min'
    assert other.outputs[absolute]==inputs[f'selected_parcel_{axis}_min']+shift
    assert other.outputs[PREFIX+'layout__parcel_fit_margin_m']==pytest.approx(-abs(shift))
    for key,value in base.outputs.items():
        if key.startswith(PREFIX) and (key.endswith(('_concrete','_formwork','_rebar','_clear_length','_clear_width','_clear_height','__civil_capital')) or '__facility_land__' in key or '__ventilation__' in key):
            assert other.outputs[key]==value,key
    assert other.outputs[PREFIX+'layout__parcel_area']==base.outputs[PREFIX+'layout__parcel_area']
