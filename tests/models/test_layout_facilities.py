"""WI-068 author tests: failed schedules, initial demand, physical solids and guards."""
import importlib.util
import json
import os
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
BODY=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_facilities'

@pytest.fixture(scope="module", autouse=True)
def runtime():
    paths=[ROOT/"exploration/stellarator_e2e/pkg", Path(os.environ["STOP_PARSER_TEAX_ROOT"])/"packages/teax-simkit"]
    for p in paths:sys.path.insert(0,str(p))
    yield
    for p in paths:sys.path.remove(str(p))


def load(name):
    spec=importlib.util.spec_from_file_location(name,BODY/(name+'_impl.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

@pytest.fixture
def inputs():
    # Direct-helper scenario uses a0.1m HX shell wall. Native cases below use
    # the actual modeled0.2m default through captured entry models.
    m=json.loads((ROOT/'work/active/WI-068_layout-based-facilities/evidence/facility-contract.json').read_text())
    selected=json.loads((ROOT/'work/active/WI-076_supplied-facility-design-evaluation/evidence/selected-design-migration.json').read_text())['selected_inputs']
    parameters={k:v for k,v in m['parameters'].items() if k not in ('facilities_capacity_mode','occupancy_aspect_ratio')}
    return parameters|selected|dict(n_mod=1,major_radius=12.7,minor_outer_radius=3.55,blanket_volume=1013.4060451016529,calendar_q=18/4.5239260339489915,calendar_fluence=18,calendar_years=30,calendar_outage=7/12,calendar_unplanned=0,calendar_mode=0,calendar_life=4.5239260339489915,calendar_count=5,calendar_availability=.9027777777777779,cooling_circuits=14,cooling_helium_count=28,cooling_salt_count=28,cooling_bundle_count=14,cooling_machine_life=10,cooling_bundle_life=15,hx_shell_bore=3.2,hx_shell_wall=.1,hx_shell_length=13,hx_tube_length=11.6)

def test_baseline_persistent_resources(inputs):
    d=load('facility_layout').diagnostics(inputs);o=d['outputs'];assert o['packages_per_sector']==36;assert o['outage_required_days']==180
    assert o['cooling_carrier_moves']==448;assert o['dirty_buffer_required']==18;assert o['dirty_store_required']==36
    assert o['initial_margin_days']==pytest.approx(16);assert o['route_margin_m']>=0;assert not d['geometry']['overlaps']
    jobs=d['cooling']['carrier_jobs'];assert all(a['end']<=b['start'] for a,b in zip(jobs,jobs[1:]))
    rows=d['cooling']['jobs']
    for station in {r['station'] for r in rows if 'station' in r}:
        intervals=sorted((r['service_start'],r['station_release']) for r in rows if r.get('station')==station)
        assert all(a[1]<=b[0] for a,b in zip(intervals,intervals[1:]))

def test_initial_without_replacements_retains_late_stock(inputs):
    f=load('facility_layout');inputs.update(calendar_years=1,calendar_count=0,calendar_availability=1,cooling_machine_life=30,cooling_bundle_life=30,cooling_initial_receipt_lead_days=1,initial_receipt_lead_days=20)
    o=f.calculate(inputs);assert o['initial_margin_days']<0;assert o['initial_clean_required']==36;assert o['dirty_store_required']==0
    assert [o['cooling_clean_'+k+'_required'] for k in ('helium','salt','bundle')]==[29,29,14]
    assert o['calendar_event_count']==0;assert o['cooling_last_release_year']==0

@pytest.mark.parametrize('changes,key', [({'sector_service_teams':1},'outage_margin_days'),({'component_remove_days':.75,'component_install_days':.75},'outage_margin_days'),({'component_hold_days':365.25*6},'capacity_margin_units'),({'cooling_hold_days':365.25*16},'capacity_margin_units'),({'cooling_receipt_lead_days':1},'readiness_margin_days'),({'cooling_aisle_width':5},'route_margin_m'),({'cooling_cross_width':13},'route_margin_m')])
def test_counterexamples_fail_native_operands(inputs,changes,key):
    assert load('facility_layout').calculate(inputs|changes)[key]<0

def test_long_processing_queues_across_campaigns(inputs):
    d=load('facility_layout').diagnostics(inputs|dict(cooling_machine_process_days=200,cooling_bundle_process_days=400));o=d['outputs']
    assert [o['cooling_dirty_'+k+'_required'] for k in ('helium','salt','bundle')]==[28,50,12]
    assert o['cooling_jobs_after_shutdown']==40

def test_half_open_and_zero_occupancy():
    f=load('facility_layout');assert f.peak([(1,1),(1,2),(2,3)])==1
    assert f.union_measure([(0,0,2,1),(1,0,3,1)])==(3,8)

def test_shipping_scope_combined_and_nonfinite():
    f=load('facility_shipping_scope');assert f.calculate(dict(cas20=100,cooling_exclusion=20,facility_exclusion=30))['remaining_shipping_base']==50
    for x in [dict(cas20=100,cooling_exclusion=60,facility_exclusion=50),dict(cas20=float('nan'),cooling_exclusion=0,facility_exclusion=0)]:
        with pytest.raises(ValueError):f.calculate(x)

def test_dormant_returns_before_unused_geometry(inputs):
    inputs.update(facilities_enabled=False,facilities_cost_mode=0,major_radius=float('nan'))
    o=load('facility_layout').calculate(inputs);assert o['active']==0;assert o['reactor_hall_gross_area']==0;assert o['route_margin_m']==1


def test_prepared_after_campaign_before_installation_still_fails(inputs):
    o=load("facility_layout").calculate(inputs|dict(component_receipt_lead_days=30))
    assert o["replacement_ready_margin_days"] == -6
    assert o["readiness_margin_days"] < 0


@pytest.mark.parametrize("key", ["cooling_machine_stations", "cooling_bundle_stations"])
def test_station_requests_cannot_exceed_physical_room_offer(inputs,key):
    o=load("facility_layout").calculate(inputs|{key:3})
    assert o["capacity_margin_units"] == -1

@pytest.fixture(scope='module')
def native(tmp_path_factory,runtime):
    import importlib
    path=str(ROOT/'exploration/stellarator_e2e/studies');sys.path.insert(0,path)
    route=importlib.import_module('study_route')
    from simkit.study.bridge import CandidateBridge
    engine=route.prepare(ROOT/'exploration/stellarator_e2e/generated',tmp_path_factory.mktemp('facility-native'))
    bridge=CandidateBridge(engine.entry_models)
    catalog=json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())['constraint_catalog']['concrete_entries']
    yield engine,bridge,catalog
    sys.path.remove(path)

@pytest.mark.parametrize('change,predicate', [({'initial_receipt_lead_days':20},'facility_initial_ready'),({'component_receipt_lead_days':30},'facility_replacement_ready'),({'sector_service_teams':1},'facility_outage_ok'),({'cooling_machine_stations':3},'facility_capacity_ok'),({'cooling_aisle_width':5},'facility_routes_ok'),({'helium_package_width':8},'facility_routes_ok'),({'salt_package_width':8},'facility_routes_ok'),({'cooling_field_cycle_days':1},'facility_initial_ready')])
def test_actual_native_store_executes_facility_failure(native,change,predicate):
    engine,bridge,catalog=native
    row=engine.evaluate(bridge.build({'stellarator_09__stellaris__buildings__'+k:v for k,v in change.items()}))
    assert row.outputs
    entry=next(e for e in catalog if predicate in e['source_local_identity'])
    assert row.responses[entry['constraint_id']]=='violated'

def test_civil_overflow_cannot_emit_nonfinite_cost():
    m=json.loads((ROOT/'work/active/WI-068_layout-based-facilities/evidence/facility-contract.json').read_text())
    x={k:(True if k=='enabled' else m['rates'].get(k,1e308)) for k in m['civil_inputs']}
    with pytest.raises(ValueError,match='overflow'):
        load('facility_civil_cost').calculate(x)


@pytest.mark.parametrize("changes", [dict(facilities_enabled=False,facilities_cost_mode=1),dict(facilities_enabled=False,facilities_cost_mode=.5)])
def test_dormant_rejects_invalid_selectors_before_unused_geometry(inputs,changes):
    with pytest.raises(ValueError):load("facility_layout").calculate(inputs|changes|dict(major_radius=float("nan")))


@pytest.mark.parametrize('yield_value',[0,.5,.999])
def test_waste_reduction_credit_is_rejected(inputs,yield_value):
    with pytest.raises(ValueError,match='yield'):
        load('facility_layout').calculate(inputs|dict(waste_package_yield=yield_value))

@pytest.mark.parametrize('kind',['helium','salt'])
def test_all_machine_envelopes_reach_routes(inputs,kind):
    d=load('facility_layout').diagnostics(inputs|{kind+'_package_width':8})
    assert d['outputs']['route_margin_m'] == -4
    assert d['geometry']['route_checks'][kind+'_door'] == -4
    assert d['geometry']['route_checks'][kind+'_aisle'] == -4

@pytest.mark.parametrize('kind',['helium','salt'])
def test_machine_lengths_change_requirements_without_resizing_hall(inputs,kind):
    f=load('facility_layout');base=f.diagnostics(inputs);d=f.diagnostics(inputs|{kind+'_package_length':10})
    assert d['outputs']['cooling_hall_clear_width']==base['outputs']['cooling_hall_clear_width']
    assert d['outputs']['cooling_hall_required_width'] > base['outputs']['cooling_hall_required_width']
    assert d['outputs']['geometry_fit_margin_m'] < 0
    assert d['outputs']['cooling_hall_sub_concrete']==base['outputs']['cooling_hall_sub_concrete']


def test_initial_carrier_must_return_before_commissioning(inputs):
    d=load('facility_layout').diagnostics(inputs|dict(cooling_field_cycle_days=1))
    assert max(r['return_arrival'] for r in d['cooling']['jobs'] if r['initial']) == 40
    assert d['outputs']['cooling_initial_ready_margin_days']==-40
    assert d['outputs']['initial_margin_days']==-40
    assert d['outputs']['calendar_event_count']==5


@pytest.mark.parametrize("kind",["helium","salt","bundle"])
@pytest.mark.parametrize("zone",["clean","dirty"])
def test_cooling_position_offers_are_integer_counts(inputs,kind,zone):
    with pytest.raises(ValueError,match="integer"):
        load("facility_layout").calculate(inputs|{"cooling_"+zone+"_"+kind+"_positions":.5})


@pytest.mark.parametrize("aisle",[5,8])
def test_internal_doors_keep_their_declared_width_when_aisle_changes(inputs,aisle):
    d=load("facility_layout").diagnostics(inputs|dict(cooling_aisle_width=aisle))
    holes=d["geometry"]["civil"]["cooling_annex"]["openings"]
    assert len(holes)==16
    assert all(h["width"]==6 for h in holes[2:])
