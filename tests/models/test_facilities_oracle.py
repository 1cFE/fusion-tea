"""Independent source/solid/resource identities; no production facility imports."""
import math

import pytest

from exploration.stellarator_e2e import oracle_facilities as f


def test_source_components_and_original_unit_conversions():
    r=f.rates()
    assert r['floor_concrete']==pytest.approx((358772.036+354136.3796)/(2100*.764554857984))
    assert r['upper_form']==pytest.approx((14196509.53+1403236.116)/(234300*.09290304))
    assert f.rates(1000)['upper_rebar']/r['upper_rebar']==pytest.approx(907.18474/1000)


def test_partition_solid_and_face_counting_independent_identity():
    # Review's three equal4m strips: exterior14x20, occupied bearing width16.
    q=f.shell(10,16,5,2,1,1,partition_length=20,inner_attachment_area=40,
              ceiling_area=120)
    assert q['upper_concrete']-q['footprint']==pytest.approx((14*20-3*10*4)*5)
    faces=2*(14+20)*5 + 3*2*(10+4)*5
    assert faces==760
    assert q['upper_form']==faces+120+2*(14+20)


def test_door_faces_reveals_and_ground_supported_slab():
    whole=f.shell(10,8,5,1,.5,.25)
    door=f.shell(10,8,5,1,.5,.25,openings=[(3,4)])
    assert whole['upper_concrete']-door['upper_concrete']==12
    assert door['upper_form']-whole['upper_form']==-24+11
    assert door['floor_form']==2*(12+10)*.5


def test_equal_time_departures_and_retained_stock():
    assert f.occupancy([(0,1,2),(1,2,3)])==3
    assert f.occupancy([(0,None,1),(1,2,2)],at=30)==1


def test_no_recurring_events_preserve_initial_sector_inventory():
    x=f.sector_inventory([],36)
    assert x['clean_peak']==36 and x['storage_peak']==0 and x['queue_peak']==0
    assert x['initial_finish']==-25
    assert x['initial_ready']
    late=f.sector_inventory([],36,initial_lead=20)
    assert not late['initial_ready'] and late['clean_peak']==36


def test_sector_crew_and_throughput_counterexamples():
    assert f.sector_schedule(36,teams=1)[1]==278
    assert f.sector_schedule(36,remove=.75,install=.75)[1]==216
    x=f.sector_inventory([5],36,remove=.25,install=.25)
    assert x['queue_peak']==27


@pytest.mark.parametrize('kwargs,dirty,unfinished',[
    ({},(28,28,14),0),
    ({'lives':(15,15,15)},(28,28,14),0),
    ({'hold':16*365.25},(56,56,14),0),
    ({'machine_process':200,'bundle_process':400},(28,50,12),40),
])
def test_persistent_cooling_carrier_and_stations(kwargs,dirty,unfinished):
    x=f.cooling_inventory(**kwargs)
    assert x['clean']==(29,29,14) and x['dirty']==dirty
    assert x['unfinished']==unfinished
    intervals=x['movements']
    assert all(a[1]<=b[0] for a,b in zip(intervals,intervals[1:]))
    for u in x['units']:
        if not u['initial']:
            assert u['arrival']<=u['entered']<u['processed']<u['released']
    for station in range(4):
        uses=sorted((u['entered'],u['released']) for u in x['units'] if u.get('station')==station)
        assert all(a[1]<=b[0] for a,b in zip(uses,uses[1:]))


def test_late_initial_cooling_is_not_lost_and_one_spare_remains():
    x=f.cooling_inventory(lives=(30,30,30),initial_lead=1)
    assert x['clean']==(29,29,14) and x['dirty']==(0,0,0)
    assert not x['initial_ready'] and len(x['movements'])==70
    assert x['final_release']==0


def test_zero_resource_is_domain_failure():
    with pytest.raises(ValueError):
        f.cooling_inventory(machine_stations=0)


def _layout(*,events=(5.,10.,15.,20.,25.),**overrides):
    physical=dict(n_mod=1,major_radius=21.4,minor_outer_radius=2.05235,
                  blanket_volume=1000,calendar_mode=0,calendar_years=30,calendar_outage=.5,
                  cooling_helium_count=28,cooling_salt_count=28,cooling_bundle_count=14,
                  cooling_circuits=14,cooling_machine_life=10,cooling_bundle_life=15,
                  hx_tube_length=11.6,hx_shell_bore=3.2,hx_shell_wall=.2,hx_shell_length=13.)
    p=dict(f.DEFAULTS)
    for key,value in overrides.items():
        (physical if key in physical else p)[key]=value
    return f.layout(p,physical,events)


def test_layout_shell_and_source_sums_are_closed():
    x=_layout()
    assert len(f.CHILDREN)==25
    assert x['reactor_hall_clear_length']==pytest.approx(max(4*(21.4+2.05235+2)+4, x['sector_wing_east_clear_width']+8))
    assert x['cooling_annex_clear_length']==pytest.approx(67.7)
    assert x['cooling_annex_clear_width']==pytest.approx(296.2)
    assert x['civil_capital']==pytest.approx(sum(x[c+'_cost_2025'] for c in f.CHILDREN))
    assert x['total_air_volume']==pytest.approx(sum(x[c+'_air_volume'] for c in f.CHILDREN))
    assert x['ventilation_2025']==pytest.approx(1000*x['controlled_air_volume']**.8*(321.9/130.7))
    assert x['layout_land_cost']==pytest.approx(x['parcel_area']/4046.8564224*10000)


def test_geometry_and_demand_contrasts_preserve_supplied_facilities():
    base=_layout()
    radius=_layout(major_radius=24)
    demand=_layout(blanket_volume=3000)
    assert radius['geometry_fit_margin_m'] < base['geometry_fit_margin_m']
    for row in (radius,demand):
        for key in ('reactor_hall_gross_area','civil_capital','packages_per_sector','sector_wing_east_gross_area'):
            assert row[key] == base[key], key
    # Packaging is independently selected; added material tests its offered capacity.
    assert demand['unused_material_capacity'] < base['unused_material_capacity']


def test_enabled_legacy_costs_keep_physical_diagnostics():
    x=_layout(facilities_cost_mode=0)
    assert x['civil_capital']>0 and x['active']==1 and x['cost_mode']==0
    off=_layout(facilities_enabled=False,facilities_cost_mode=0)
    assert off['civil_capital']==0 and off['initial_margin_days']==1
    with pytest.raises(ValueError):
        _layout(facilities_enabled=False,facilities_cost_mode=1)


def test_recurring_stock_ready_after_campaign_before_installation_fails():
    x=f.sector_inventory([5.],36,lead=10.)
    # Batch finishes26 days after campaign start, before the earliest nominal
    # installation at day64. The campaign deadline remains unchanged.
    assert x['recurring_margin']==pytest.approx(-26.)
    assert not x['ready']


def test_extra_processing_stations_need_physical_room_capacity():
    machine=_layout(cooling_machine_stations=3)
    bundle=_layout(cooling_bundle_stations=3)
    assert machine['capacity_margin_units']==-1
    assert bundle['capacity_margin_units']==-1
    assert machine['cooling_annex_gross_area']>0
    assert bundle['cooling_annex_gross_area']>0


def test_disabled_full_map_preserves_legacy_accounts_and_zeroes_facilities():
    from exploration.stellarator_e2e.studies import oracle_entry as seam

    result=seam._compute({'facility_facilities_enabled':False,
                         'facility_facilities_cost_mode':0.})
    assert set(seam.ORACLE_OUTPUT_TO_CHANNEL)<=result.keys()
    assert result['buildings']==result['buildings_legacy']
    assert result['precon']==result['precon_legacy']
    unit_margins={'initial_margin_days','readiness_margin_days','capacity_margin_units',
                  'route_margin_m','outage_margin_days','unused_material_capacity','geometry_fit_margin_m','occupancy_area_margin_m2','parcel_fit_margin_m'}
    fixed={'facility_initial_sector_start_days':-120.,'facility_cooling_initial_handoff_days':-30.}
    for name,channel in seam.ORACLE_OUTPUT_TO_CHANNEL.items():
        assert math.isfinite(result[name])
        if not name.startswith('facility_'):
            continue
        expected=fixed.get(name,1. if name.removeprefix('facility_') in unit_margins else 0.)
        assert result[name]==expected,(name,channel,result[name])
    assert result['shipping_facility_exclusion']==0
    assert result['shipping_remaining_base']==pytest.approx(
        result['cas20_capital']-result['shipping_cooling_exclusion']-result['shipping_fuel_installation_exclusion'])


@pytest.mark.parametrize('waste_yield',[0.,.5])
def test_waste_packaging_cannot_erase_retired_material(waste_yield):
    with pytest.raises(ValueError,match='yield'):
        f.sector_inventory([5.],36,yield_factor=waste_yield)
    with pytest.raises(ValueError,match='yield'):
        _layout(waste_package_yield=waste_yield)


def test_initial_cooling_carrier_finishes_before_fixed_commissioning():
    baseline=f.cooling_inventory()
    late=f.cooling_inventory(field_cycle=1.)
    assert baseline['initial_margin']==pytest.approx(16.)
    assert baseline['initial_ready']
    assert max(u['arrival'] for u in late['units'] if u['initial'])==pytest.approx(40.)
    assert late['initial_margin']==pytest.approx(-40.)
    assert not late['initial_ready']
    layout=_layout(cooling_field_cycle_days=1.)
    assert layout['initial_margin_days']==pytest.approx(-40.)
    assert layout['calendar_event_count']==5


@pytest.mark.parametrize('changes',[
    {'helium_package_width':8.}, {'salt_package_width':8.},
    {'helium_package_length':18.}, {'salt_package_length':18.},
    {'helium_package_height':10.}, {'salt_package_height':10.},
])
def test_every_cooling_carried_envelope_must_fit_common_route(changes):
    x=_layout(**changes)
    assert x['route_margin_m']<0
    assert math.isfinite(x['civil_capital'])


def test_longer_salt_machine_tests_supplied_service_strip():
    baseline=_layout()
    longer=_layout(salt_package_length=10.)
    assert longer['geometry_fit_margin_m'] < baseline['geometry_fit_margin_m']
    assert longer['cooling_hall_clear_width'] == baseline['cooling_hall_clear_width']
    assert longer['cooling_hall_gross_area'] == baseline['cooling_hall_gross_area']


def test_wider_cooling_aisle_does_not_enlarge_internal_doors():
    x=_layout(cooling_aisle_width=10.,helium_package_width=5.)
    assert x['route_margin_m'] <= -1.  # Fixed room geometry can impose a tighter bottleneck than the door.


def test_long_package_must_fit_airlock_even_when_cross_corridor_grows():
    x=_layout(cooling_cross_width=25.,salt_package_length=16.,building_separation=100.)
    assert x['route_margin_m'] <= -1.  # Fixed room geometry can impose a tighter bottleneck than the door.


@pytest.mark.parametrize('bank',['clean','dirty'])
@pytest.mark.parametrize('kind',['helium','salt','bundle'])
def test_fixed_cooling_offers_require_whole_storage_positions(bank,kind):
    with pytest.raises(ValueError,match='integer'):
        _layout(facilities_capacity_mode=0,**{f'cooling_{bank}_{kind}_positions':.5})


@pytest.mark.parametrize('aisle',[5.,6.,8.,10.])
def test_cooling_aisle_changes_do_not_resize_fourteen_internal_door_apertures(aisle):
    x=_layout(cooling_aisle_width=aisle)
    gross=x['cooling_annex_gross_area']
    clear=x['cooling_annex_clear_area']
    height=x['cooling_annex_clear_height']
    # Recover aperture area from solid-wall volume and the separately poured
    # roof. Fourteen6m internal doors plus two17m exterior openings are fixed.
    solid_wall=(gross-clear)*height
    net_wall=x['cooling_annex_super_concrete']-gross*f.DEFAULTS['conventional_roof']
    aperture_area=(solid_wall-net_wall)/f.DEFAULTS['conventional_wall']
    assert aperture_area==pytest.approx((14*6+2*17)*height)


def test_native_fluence_owner_drives_calendar_and_facility_demand():
    from exploration.stellarator_e2e.studies import oracle_entry as seam

    key=seam.P+'blanket__first_wall__fluence_limit'
    defaults=seam._compute({})
    default_point=seam._oracle_overrides({key:18.})
    assert default_point=={'fluence_limit':18.}
    assert seam._compute(default_point)==defaults
    no_replacements=seam._compute(seam._oracle_overrides({key:180.}))
    assert all(math.isfinite(no_replacements[k]) for k in seam.ORACLE_OUTPUT_TO_CHANNEL)
    assert defaults['calendar_n_replacements']>0
    assert no_replacements['calendar_n_replacements']==0
    assert no_replacements['calendar_cas72_annual']==0
    assert no_replacements['facility_calendar_event_count']==0
    assert no_replacements['facility_dirty_store_required']==0
    assert no_replacements['facility_outage_margin_days']==30*365.25
    assert no_replacements['facility_initial_clean_required']>0
    assert no_replacements['facility_initial_margin_days']>0
    assert seam.vs.IN['fluence_limit']==18.


def test_no_sector_events_make_hypothetical_outage_nonbinding():
    with_events=_layout(component_remove_days=20.)
    without_events=_layout(events=(),component_remove_days=20.)
    late_initial=_layout(events=(),component_remove_days=20.,initial_receipt_lead_days=20.)
    assert with_events['outage_margin_days']<0
    assert without_events['outage_required_days']==with_events['outage_required_days']
    assert without_events['outage_margin_days']==30*365.25
    assert without_events['initial_margin_days']>0
    assert late_initial['initial_margin_days']<0
    assert late_initial['outage_margin_days']==30*365.25
