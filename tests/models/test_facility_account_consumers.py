"""WI-068 checks at the actual supplementary and whole-plant consumers."""
import importlib
import json
import os
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
P = 'stellarator_09__stellaris__'
CIVIL_BUILDINGS = (
    'reactor_hall', 'sector_wing_east', 'sector_wing_north',
    'sector_wing_west', 'sector_wing_south', 'sector_link_east',
    'sector_link_north', 'sector_link_west', 'sector_link_south',
    'cooling_hall', 'cooling_annex', 'cooling_link', 'turbine_hall',
    'cryo_coldbox', 'cryo_compressors', 'fuel_building', 'reactor_auxiliaries',
    'power_supply_building', 'electrical_building', 'service_water_building',
    'maintenance_shop', 'site_services_building', 'administration', 'control',
    'security')


@pytest.fixture(scope='module')
def runtime():
    paths = [ROOT / 'exploration/stellarator_e2e/pkg',
             ROOT / 'exploration/stellarator_e2e/studies',
             ROOT / 'exploration/stellarator_e2e']
    if os.environ.get('STOP_PARSER_TEAX_ROOT'):
        paths.append(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit')
    for path in paths:
        sys.path.insert(0, str(path))
    yield
    for path in paths:
        sys.path.remove(str(path))


@pytest.mark.parametrize('plant_contingency', [0., .1, .3])
@pytest.mark.parametrize('supplementary_contingency', [0., .2])
def test_installed_facility_shipping_exclusion_preserves_other_charges(
        runtime, plant_contingency, supplementary_contingency):
    # Civil costs already contain site labor. Remove their entire loaded
    # contribution to shipping while retaining the old raw cooling subtraction.
    facility = 200e6
    other_direct = 800e6
    cooling_delivered = 100e6
    cas20 = (1 + plant_contingency) * (facility + other_direct)
    facility_exclusion = (1 + plant_contingency) * facility
    module = importlib.import_module(
        'stellarator_tea.modules.mfe_account_costs.supplementary_cost'
    ).Supplementary_CostModule()
    inputs = dict(
        spares_frac=.04, cas23_to_28=80e6, ref_net_power=1000.,
        cas30=50e6, shipping_frac=.015, p_net=600., tax_frac=.01,
        decom_base=20e6, cas20=cas20, n_mod_in=1.,
        delivered_shipping_exclusion_in=cooling_delivered,
        facility_exclusion_in=facility_exclusion, fuel_installation_exclusion_in=0.,
        insurance_frac=.015, startup_fuel_base=10e6,
        contingency_rate_in=supplementary_contingency)
    actual = module.run(**inputs).data.root
    # Independent remaining-scope calculation: no facility amount remains
    # in freight, but its full loaded amount remains taxable and insured.
    remaining_shipping = (1 + plant_contingency) * other_direct - cooling_delivered
    expected = (.015 * remaining_shipping + .04 * 80e6 + .01 * cas20
                + .015 * (cas20 + 50e6) + .6 * 30e6)
    assert actual == pytest.approx(expected * (1 + supplementary_contingency))
    before = module.run(**(inputs | {
        'facility_exclusion_in': 0.})).data.root
    assert before - actual == pytest.approx(
        .015 * facility_exclusion * (1 + supplementary_contingency))


@pytest.fixture(scope='module')
def evaluate(runtime, tmp_path_factory):
    from simkit.study.bridge import CandidateBridge
    import study_route
    engine = study_route.prepare(ROOT / 'exploration/stellarator_e2e/generated',
                                 tmp_path_factory.mktemp('facilities-accounts'))
    bridge = CandidateBridge(engine.entry_models)

    def run(point):
        row = engine.evaluate(bridge.build(point))
        assert row.outputs, row
        return row

    return run


@pytest.mark.parametrize('case_index', [0, 1], ids=['default14', 'selected18'])
@pytest.mark.parametrize('contingency', [0., .1, .3])
def test_native_facility_children_reconcile_to_total_without_calendar_change(
        evaluate, case_index, contingency):
    entering = json.loads((ROOT / 'work/orchestration/goals/layout-based-facilities'
                          '/evidence/entering-replay.json').read_text())['cases'][case_index]
    # Frozen WI-068 monetary anchor predates throughput costing; replay its legacy selection.
    from tests.models.current_mfe_regressions import WI073_REPLAY
    point = entering['inputs'] | WI073_REPLAY | {P + 'contingency_rate': contingency, P + 'fuel_cycle__processing_enabled': False}
    old_case = evaluate(point | {P + 'buildings__facilities_cost_mode': 0.})
    new_case = evaluate(point | {P + 'buildings__facilities_cost_mode': 1.})
    old, new = old_case.outputs, new_case.outputs

    # Actual child consumers, not a detached facility total or an oracle result.
    civil = sum(new[P + f'buildings__{name}__civil__cost_2025']
                for name in CIVIL_BUILDINGS)
    served_volume = new[P + 'buildings__layout__controlled_air_volume']
    ventilation = 1000. * served_volume ** .8 * (321.9 / 130.7)
    installed_facilities = civil + ventilation
    legacy_buildings = old[P + 'buildings__buildings_cost__cost']
    delta_direct = installed_facilities + 85e6 - legacy_buildings
    delta_cas20 = (1 + contingency) * delta_direct
    delta_indirect = (.2 * 8 / 6) * delta_cas20
    delta_supplementary = (
        .015 * (delta_cas20 - (1 + contingency) * installed_facilities)
        + .01 * delta_cas20 + .015 * (delta_cas20 + delta_indirect))
    new_land = new[P + 'buildings__layout__parcel_area'] / 4046.8564224 * 10000.
    old_land = old[P + 'precon_cost__cost'] - 16e6
    expected_capital_change = (new_land - old_land + delta_cas20
                               + delta_indirect + delta_supplementary)
    for name, expected in (
            ('cas2x_pre_contingency__cas2x_pre_contingency', delta_direct),
            ('cas20_capital__cas20_capital', delta_cas20),
            ('indirect__cost', delta_indirect),
            ('supplementary__cost', delta_supplementary),
            ('total_capital__total_capital', expected_capital_change)):
        assert new[P + name] - old[P + name] == pytest.approx(
            expected, rel=2e-11, abs=1e-5), name

    physical_prefixes = tuple(P + stem for stem in (
        'plasma__', 'radial_build__', 'pb__', 'calendar__',
        'heat_transport__primary_loop__', 'heat_transport__equipment__',
        'blanket__breeding__', 'divertor__divheat__'))
    checked = [key for key in old if key.startswith(physical_prefixes)]
    assert len(checked) > 50
    for key in checked:
        assert new[key] == old[key], key
    assert new_case.responses == old_case.responses
    assert (new[P + 'lcoe_calc__lcoe'] - old[P + 'lcoe_calc__lcoe']) * expected_capital_change > 0
    if contingency == .1:
        assert old[P + 'total_capital__total_capital'] == pytest.approx(
            entering['outputs'][P + 'total_capital__total_capital'], rel=1e-12)
