from tests.models.current_mfe_regressions import assert_current_predicates
"""Current supplied-design divertor conservation at retained plasma scenarios.

The old automatic magnet selection is explicitly replaced by the current supplied
pack and fixed reference turns. These are new evaluations, not frozen replays.
"""
import json
from pathlib import Path

import pytest
from tests.models.test_winding_pack_cost import runtime_paths, evaluate, output, P

ENTERING = Path('work/orchestration/goals/divertor-peak-heat-load/evidence/entering/native-cases.json')
CASES = json.loads(ENTERING.read_text())['cases']


def selected_point(old):
    """Retain plasma/excitation controls, explicitly choose current fixed hardware."""
    defaults=json.loads(Path('exploration/stellarator_e2e/generated/inputs/stellarator_plant_params.json').read_text())
    point=dict(old)
    for key in ('magnet__winding_pack__sizing_mode','magnet__winding_pack__inventory_multiplier',
                'magnet__winding_pack__j_wp'):
        point.pop(P+key,None)
    turns=defaults[P+'magnet__coil__reference_turns']
    point[P+'magnet__coil__reference_turns']=turns
    point[P+'magnet__winding_pack__wp_side']=defaults[P+'magnet__winding_pack__wp_side']
    excitation=point.pop(P+'magnet__coil__I_coil',None)
    if excitation is not None:
        point[P+'magnet__coil__turn_current']=excitation/turns
    return point


@pytest.mark.codegen_available
@pytest.mark.parametrize('case', CASES, ids=lambda case: case['proposal_id'])
def test_retained_plasma_scenarios_evaluate_supplied_design(evaluate, case):
    import oracle_entry
    point=selected_point(case['point'])
    row=evaluate({k.removeprefix(P):v for k,v in point.items()})
    expected=oracle_entry.evaluate(point)
    for key,value in expected.items():
        assert row.outputs[key]==pytest.approx(value,rel=1e-9,abs=1e-9),key
    assert_current_predicates(row,point,expected)


@pytest.mark.codegen_available
@pytest.mark.parametrize('index', [0, 1, 2])
@pytest.mark.parametrize('profile', [{}, {'divertor__q_target_ref': 5., 'divertor__target_capture_fraction': .97}])
def test_coupled_account_and_independent_oracle(evaluate, index, profile):
    import oracle_entry
    overrides = {key.removeprefix(P): value for key, value in selected_point(CASES[index]['point']).items()} | profile
    row = evaluate(overrides)
    expected = oracle_entry.evaluate({P + key: value for key, value in overrides.items()})
    for key, value in expected.items():
        assert row.outputs[key] == pytest.approx(value, rel=1e-9, abs=1e-9), key
    d = lambda name: output(row, 'divertor__divheat__' + name)
    core = d('p_heat_abs') - d('p_sep')
    assert d('p_heat_abs') == pytest.approx(core + d('p_rad_edge') + d('p_target_deposited') + d('p_nonrad_uncaptured'), rel=1e-12)
    assert d('p_sep') == pytest.approx(d('p_rad_edge') + d('p_target_nonrad'), rel=1e-12)
    assert d('q_target_peak') == pytest.approx(d('p_target_deposited') / d('peak_equivalent_area'), rel=1e-12)
    assert d('power_account_valid') == d('f_rad_edge_defined') == d('peak_equivalent_area_defined') == 1.


@pytest.mark.codegen_available
def test_paired_transport_does_not_create_or_remove_plant_heat(evaluate):
    base = {key.removeprefix(P): value for key, value in selected_point(CASES[2]['point']).items()}
    high = evaluate(base)
    low = evaluate(base | {'divertor__q_target_ref': 5., 'divertor__target_capture_fraction': .97})
    for key, value in high.outputs.items():
        if '__divertor__' not in key:
            assert low.outputs[key] == value, key
    for suffix in ('divertor__divertor_cost__cost', 'divertor__divheat__p_heat_abs', 'divertor__divheat__p_target_nonrad'):
        assert output(low, suffix) == output(high, suffix)
    assert output(low, 'divertor__divheat__p_nonrad_uncaptured') > output(high, 'divertor__divheat__p_nonrad_uncaptured')
    assert output(low, 'divertor__divheat__q_target_peak') / output(high, 'divertor__divheat__q_target_peak') == pytest.approx(5/9.5)
    # Only the non-radiated divertor screen may change. Primary-loop failure survives.
    for key, verdict in high.responses.items():
        if 'divertor_heat_ok' not in key:
            assert low.responses[key] == verdict


@pytest.mark.codegen_available
@pytest.mark.parametrize('pack_side',[.5,.65])
def test_signed_burn_failures_preserve_heat_equations(evaluate, pack_side):
    import oracle_entry
    point=selected_point({P+'plasma__R':13.5,P+'plasma__a':1.5,P+'magnet__coil__I_coil':16e6})
    point[P+'magnet__winding_pack__wp_side']=pack_side
    native=evaluate({k.removeprefix(P):v for k,v in point.items()})
    now=oracle_entry.evaluate(point)
    for channel,value in now.items():
        assert native.outputs[channel]==pytest.approx(value,rel=1e-9,abs=1e-9),channel
    assert output(native,'divertor__divheat__power_account_valid')==0.
    assert_current_predicates(native,point,now)
    assert native.responses['headline']=='violated'
    # The sustainment failure remains exact; pack selection does not repair burn.
    catalog=json.loads(Path('exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())['constraint_catalog']['concrete_entries']
    burn=next(e['constraint_id'] for e in catalog if e['source_local_identity']=='burn_hold_ok')
    assert native.responses[burn]=='violated'
