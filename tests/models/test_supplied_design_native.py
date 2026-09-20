"""MR-7: actual public entry inputs, generated execution and downstream prices."""
import importlib
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
P = 'stellarator_09__stellaris__'

@pytest.fixture(scope='module')
def native(tmp_path_factory):
    paths = [str(ROOT/'exploration/stellarator_e2e/studies'), str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit')]
    for path in paths:
        sys.path.insert(0, path)
    from simkit.study.bridge import CandidateBridge
    route = importlib.import_module('study_route')
    engine = route.prepare(ROOT/'exploration/stellarator_e2e/generated', tmp_path_factory.mktemp('mr7-native'))
    bridge = CandidateBridge(engine.entry_models)
    catalog = json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())['constraint_catalog']['concrete_entries']
    def execute(changes, require_outputs=True):
        row = engine.evaluate(bridge.build({P+k:v for k,v in changes.items()}))
        if require_outputs:
            assert row.outputs, row
        return row
    yield execute, {e['source_local_identity']:e['constraint_id'] for e in catalog}
    for path in paths:
        sys.path.remove(path)

@pytest.mark.parametrize('capacity,verdict', [(0.00005,'violated'), (0.0003,'satisfied')])
def test_supplied_processor_capacity_is_evaluated(native,capacity,verdict):
    execute, predicates = native
    row = execute({'fuel_cycle__processing_capacity_kg_s': capacity})
    q = P+'fuel_cycle__processing_cost__'
    assert row.outputs[q+'capacity_kg_s'] == capacity
    assert row.responses[predicates['fuel_processing_capacity_ok']] == verdict
    assert row.outputs[q+'cost'] > 0


def test_processor_price_follows_rating_not_operating_demand(native):
    execute,_ = native
    fixed = {'fuel_cycle__processing_capacity_kg_s':0.0003}
    a = execute(fixed | {'fuel_cycle__burn_fraction':0.01})
    b = execute(fixed | {'fuel_cycle__burn_fraction':0.02})
    q = P+'fuel_cycle__processing_cost__'
    assert a.outputs[q+'flow_kg_s'] != b.outputs[q+'flow_kg_s']
    assert a.outputs[q+'capacity_margin_kg_s'] != b.outputs[q+'capacity_margin_kg_s']
    for name in ('capacity_kg_s','plant_capacity_kg_s','cost','equipment_total','installation_total'):
        assert a.outputs[q+name] == b.outputs[q+name]


def test_processor_price_domain_is_distinct_from_capacity(native):
    execute,predicates = native
    row = execute({'fuel_cycle__processing_capacity_kg_s':0.0003,'fuel_cycle__processing_source_conditions':False})
    q = P+'fuel_cycle__processing_cost__'
    assert row.outputs[q+'defined_flag'] == 0
    assert row.outputs[q+'cost'] > 0  # diagnostic price, explicitly undefined
    assert row.responses[predicates['fuel_processing_capacity_ok']] == 'satisfied'


@pytest.mark.parametrize('side,verdict',[(0.20,'violated'),(0.60,'satisfied')])
def test_native_supplied_pack_current_capacity(native,side,verdict):
    execute,predicates=native
    row=execute({'magnet__winding_pack__wp_side':side,'magnet__coil__turn_current':50000*22/24.9,'magnet__winding_pack__allow_field_extrapolation':0.})
    assert row.responses[predicates['reference_conductor_current_ok']] == verdict
    assert row.outputs[P+'magnet__winding_state__j_wp_effective'] == pytest.approx(308*50000*22/24.9/(side*side*1e6))
    assert row.outputs[P+'magnet__winding_procurement__cost'] > 0
    # The independently supplied larger pack can pass current yet fail geometric fit.
    assert row.responses[predicates['wp_fit_ok']] == ('satisfied' if side == .20 else 'violated')


def test_native_magnet_hardware_fixed_as_excitation_changes(native):
    execute,_=native
    rows=[execute({'magnet__coil__turn_current':50000*b/24.9,'magnet__winding_pack__allow_field_extrapolation':0.}).outputs for b in (21.,23.)]
    for suffix in ('magnet__winding_procurement__tape_length','magnet__winding_procurement__conductor_length','magnet__winding_procurement__cost','magnet__magnet_structure_cost__cost','magnet__magnet_capital_rollup__capital_cost','cryoplant__inventory__area_cold'):
        assert rows[0][P+suffix] == rows[1][P+suffix],suffix
    for suffix in ('magnet__peak_field_calc__B_peak','magnet__wp_stress__sigma_wp','magnet__stored_energy__W_mag','cryoplant__inventory__q_lead_cold','magnet__conductor_current__margin_fraction'):
        assert rows[0][P+suffix] != rows[1][P+suffix],suffix


@pytest.mark.parametrize('field',[19.,33.])
def test_native_conductor_outside_domain_is_not_infeasibility(native,field):
    execute,_=native
    from simkit.evaluation.evaluator import EvaluationFailed
    with pytest.raises(EvaluationFailed,match='B_peak outside 20..32 T'):
        execute({'magnet__coil__turn_current':50000*field/24.9},require_outputs=False)


def test_native_supplied_support_mass_reaches_price_and_cold_load(native):
    execute,_=native
    rows=[execute({'magnet__m_support':mass,'cryoplant__q_nuc_structure':10.}).outputs for mass in (100000.,200000.)]
    for suffix in ('cryoplant__cold_load__q_structure_nuclear','magnet__magnet_structure_cost__cost'):
        assert rows[1][P+suffix] == pytest.approx(2*rows[0][P+suffix])
    assert rows[0][P+'magnet__winding_procurement__tape_length'] == rows[1][P+'magnet__winding_procurement__tape_length']


def test_native_selected_pack_area_sets_procurement(native):
    execute,_=native
    rows=[execute({'magnet__winding_pack__wp_side':side,'magnet__coil__turn_current':50000*22/24.9,'magnet__winding_pack__allow_field_extrapolation':0.}).outputs for side in (.20,.60)]
    q=P+'magnet__winding_procurement__'
    assert rows[1][q+'tape_length']/rows[0][q+'tape_length'] == pytest.approx(9.)
    assert rows[1][q+'conductor_length'] == rows[0][q+'conductor_length']
    assert rows[1][q+'cost'] > rows[0][q+'cost']


def test_native_selected_casing_mass_reaches_inventory_and_price(native):
    execute,_=native
    rows=[execute({'magnet__casing__m_casing':mass,'magnet__legacy_casing_fraction':1.}).outputs for mass in (1000.,2000.)]
    q=P+'magnet__magnet_structure_cost__cost'
    assert rows[1][q]-rows[0][q] == pytest.approx(48*1000*18)
    assert rows[0][P+'magnet__winding_procurement__tape_length'] == rows[1][P+'magnet__winding_procurement__tape_length']


@pytest.mark.parametrize('shortfall',[1e-12,1e-10])
def test_native_current_margin_keeps_tiny_negative_verdict(native,shortfall):
    # Test-only construction supplies the resulting side as a fixed design.
    import math
    import oracle_entry
    execute,predicates=native
    point={'magnet__winding_pack__wp_side':.36,'magnet__coil__turn_current':50000*22/24.9,'magnet__winding_pack__allow_field_extrapolation':0.}
    q=P+'magnet__conductor_current__'
    reference=oracle_entry.evaluate({P+k:v for k,v in point.items()})
    critical=reference[q+'critical_current_reference']
    point['magnet__winding_pack__wp_side']=.36*math.sqrt(point['magnet__coil__turn_current']/(.8+shortfall)/critical)
    expected=oracle_entry.evaluate({P+k:v for k,v in point.items()})
    row=execute(point)
    assert -1e-8 < expected[q+'margin_fraction'] < 0
    assert -1e-8 < row.outputs[q+'margin_fraction'] < 0
    assert row.responses[predicates['reference_conductor_current_ok']] == 'violated'
