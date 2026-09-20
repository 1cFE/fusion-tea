from tests.models.current_mfe_regressions import (CURRENT_PREDICATES, historical_point, assert_historical_native, assert_current_predicates, PARTITIONS)
"""WI-065: native/oracle conservation and exact entering-case preservation."""
import json
from pathlib import Path

import pytest
from tests.models.test_winding_pack_cost import runtime_paths, evaluate, output, P

ENTERING = Path('work/orchestration/goals/divertor-peak-heat-load/evidence/entering/native-cases.json')
CASES = json.loads(ENTERING.read_text())['cases']


@pytest.mark.codegen_available
@pytest.mark.parametrize('case', CASES, ids=lambda case: case['proposal_id'])
def test_entering_values_and_predicates_preserved(evaluate, case):
    point=historical_point(case['point'])
    row=evaluate({k.removeprefix(P):v for k,v in point.items()})
    assert_historical_native('divertor-'+case['proposal_id'], row, case['outputs'], case['responses'], point)


@pytest.mark.codegen_available
@pytest.mark.parametrize('index', [0, 1, 2])
@pytest.mark.parametrize('profile', [{}, {'divertor__q_target_ref': 5., 'divertor__target_capture_fraction': .97}])
def test_coupled_account_and_independent_oracle(evaluate, index, profile):
    import oracle_entry
    overrides = {key.removeprefix(P): value for key, value in CASES[index]['point'].items()} | profile
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
    base = {key.removeprefix(P): value for key, value in CASES[2]['point'].items()}
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
@pytest.mark.parametrize('sized', [False, True])
def test_signed_burn_failures_keep_entering_equations_and_predicates(evaluate, sized):
    import importlib.util
    import oracle_entry
    entering_file = ENTERING.with_name('verify_stellaris.py')
    spec = importlib.util.spec_from_file_location('wi065_frozen_entering', entering_file)
    entering = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(entering)
    changes = {'plasma__R': 13.5, 'plasma__a': 1.5, 'magnet__coil__I_coil': 16e6}
    if sized:
        changes |= {'magnet__winding_pack__sizing_mode': 1., 'magnet__coil__coil_t': .65, 'magnet__casing__interior_y': .65}
    import math
    point = historical_point({P+key: value for key, value in changes.items()})
    # The historical oracle has no later subsystem switches; current native/oracle
    # receive the same qualified historical scenario through the declared seam.
    entering.IN.update(oracle_entry._oracle_overrides({P+k:v for k,v in changes.items()}))
    old = entering.compute()
    native = evaluate({k.removeprefix(P):v for k,v in point.items()})
    now = oracle_entry.evaluate(point)
    arithmetic = PARTITIONS['signed_arithmetic_changes'][str(sized)]
    changed = set(arithmetic['exact_local_names']) | {'fuel_tbr_margin'}
    for local, channel in oracle_entry.ORACLE_OUTPUT_TO_CHANNEL.items():
        if local in old:
            if local not in changed:
                assert now[channel] == old[local], local
            assert native.outputs[channel] == pytest.approx(now[channel], rel=1e-9, abs=1e-9), local
    area = 'sizing_required_conductor_area'
    channel=oracle_entry.ORACLE_OUTPUT_TO_CHANNEL[area]
    assert math.isclose(now[channel],old[area],rel_tol=0,abs_tol=4*max(math.ulp(now[channel]), math.ulp(old[area])))
    if sized:
        assert oracle_entry.vs.IN['magnet_turn_current'] == 50000.
        for local,scale in [('conductor_margin_current',50000.),('conductor_margin_fraction',1.)]:
            channel=oracle_entry.ORACLE_OUTPUT_TO_CHANNEL[local]
            assert now[channel] < 0 and native.outputs[channel] < 0
            assert math.isclose(now[channel],old[local],rel_tol=0,abs_tol=8*math.ulp(scale))
    assert output(native, 'divertor__divheat__power_account_valid') == 0.
    assert_current_predicates(native, point)
    for suffix in ('reference_conductor_current_ok','burn_hold_ok'):
        cid=next(cid for cid in CURRENT_PREDICATES if cid.split('__')[2]==suffix)
        assert native.responses[cid] == 'violated'
    assert native.responses['headline'] == 'violated'
    controls = json.loads(ENTERING.with_name('negative-native-cases.json').read_text())['cases']
    old_native = next(case for case in controls if case['sized'] == sized)
    assert_historical_native('signed-'+str(sized), native, old_native['outputs'], old_native['responses'], point)
