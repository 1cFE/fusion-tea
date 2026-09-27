"""Meaningful equation/domain regressions; complete native replay is in run.py."""
import importlib.util
import math
from pathlib import Path

import pytest

BODY = Path(__file__).resolve().parents[1]/'bodies/controlled_exchanger_closure/controlled_network_heat_driven_closure_impl.py'
spec = importlib.util.spec_from_file_location('controlled_body_test', BODY)
body = importlib.util.module_from_spec(spec)
spec.loader.exec_module(body)


class Inputs:
    def __init__(self, values):
        self.values = values

    def model_dump(self):
        return {k+'_in':v for k,v in self.values.items()}


def point(**changes):
    load = 1835.4512830147435
    v = dict(cold_temperature=371.0942082486433,flow=1300.,cp=5193.,gamma=5/3,
             turbine_efficiency=.93,turbine_pressure=14.325,return_pressure=30/7,
             recuperator_effectiveness=.8,control_mode=1.,return_tolerance=1e-6,
             network_mode=0.,pbli_split=.85)
    for b,q,flow,cp,ua,target,cap in (
        ('he',.41164*load+141,3261.,5193.,18.,659.15,729.15),
        ('pbli',.56636*load,26860.,190.,18.,724.15,1011.15),
        ('divertor',.15*load+29,500.,5193.,2.,846.15,973.15)):
        v.update({b+'_available':q,b+'_flow':flow,b+'_cp':cp,b+'_ua':ua,b+'_required_return':target,
                  b+'_limit':cap,b+'_hot_approach':30.,b+'_cold_approach':30.,b+'_max_bypass':1.})
    return Inputs(v | changes)


def test_known_equal_capacity_and_bypass():
    # Active Ch=Cs=4, UA=4 => epsilon=1/2, Q=400MW, both gaps100K.
    result = body.bypass_stage(400.,4.,8.,4.,600.,400.)
    assert result['bypass_fraction'] == .5
    assert result['hx_return'] == 500.
    assert result['mixed_return'] == 550.
    assert result['hot_terminal_difference'] == result['cold_terminal_difference'] == 100.
    assert result['transferred'] == 4.*100.
    for delta in (-1e-8,0.,1e-8):
        assert body.conductance(4.,4.+delta,4.) == pytest.approx(2.,abs=1e-8)


def test_no_bypass_exact_fixture():
    result = body.bypass_stage(400.,4.,4.,4.,600.,400.)
    assert result['bypass_fraction'] == 0.
    assert result['hx_return'] == result['mixed_return'] == 500.


@pytest.mark.parametrize('mode,flow,split',[(0.,1300.,.85),(1.,1260.,.75)])
def test_matched_offered_inventory_full_duty(mode,flow,split):
    inputs = point(network_mode=mode,flow=flow,pbli_split=split)
    result = body.calculate(inputs)
    assert result['unmet_heat'] < 1e-7
    assert abs(result['closure_residual']) <= 1e-6
    for b in ('he','pbli','divertor'):
        for field in ('required_hot_margin','hot_bound_margin','hot_approach_margin','cold_approach_margin','control_margin'):
            assert result[b+'_'+field] >= 0, (b,field,result[b+'_'+field])
        assert result[b+'_return_residual_magnitude'] < 1e-6
        assert result[b+'_state_defined'] == 1.
        q = result[b+'_transferred']
        cap = result[b+'_active_flow']*inputs.values[b+'_cp']/1e6
        assert cap*(result[b+'_hot']-result[b+'_hx_return']) == pytest.approx(q,abs=1e-8)
        f = result[b+'_bypass_fraction']
        assert f*result[b+'_hot']+(1-f)*result[b+'_hx_return'] == pytest.approx(result[b+'_mixed_return'],abs=1e-9)


def test_partial_transfer_changes_cycle_and_exposes_return_error():
    full = body.calculate(point())
    failed = body.calculate(point(pbli_ua=.05))
    assert failed['pbli_unmet'] > 100.
    assert failed['turbine_temperature'] < full['turbine_temperature']
    assert abs(failed['closure_residual']) <= 1e-6
    assert failed['pbli_return_residual'] == pytest.approx(failed['pbli_unmet']/(26860*190/1e6),abs=1e-8)
    assert failed['pbli_required_hot'] == full['pbli_required_hot']


def test_source_cap_and_bypass_limit_do_not_rewrite_states():
    base = body.calculate(point())
    failed = body.calculate(point(divertor_limit=900.,he_max_bypass=.01))
    assert failed['divertor_hot_bound_margin'] < 0.
    assert failed['he_control_margin'] < 0.
    assert failed['accepted_heat'] == base['accepted_heat']
    assert failed['divertor_hot'] == base['divertor_hot']
    assert failed['he_bypass_fraction'] == base['he_bypass_fraction']


@pytest.mark.parametrize('q,ua,hot,tin',[(0.,50.,700.,400.),(100.,0.,700.,400.),(100.,50.,400.,500.)])
def test_inactive_states_are_explicit(q,ua,hot,tin):
    result = body.bypass_stage(q,ua,2.,4.,hot,tin)
    assert result['transferred'] == 0.
    assert result['state_defined'] == 0.
    assert result['unmet'] == q
    assert all(math.isfinite(x) for x in result.values())


def test_original_ua_saturated_terminal_remains_finite_transfer():
    # Reviewer-identified finite-duty original-inventory example.
    q = 276.5
    hot = 846.15+q/(500*5193/1e6)
    tin = hot-229.78786290651692-q/(1100*5193/1e6)
    result = body.bypass_stage(q,50.,500*5193/1e6,1100*5193/1e6,hot,tin)
    assert result['transferred'] == q
    assert result['state_defined'] == 1.
    assert result['bypass_fraction'] == pytest.approx(.6172088525331203,abs=1e-11)
    assert abs(result['cold_terminal_difference']) < 1e-8
    assert result['cold_terminal_difference'] < 30.


@pytest.mark.parametrize('changes',[{'pbli_split':0.},{'pbli_split':1.},{'network_mode':2.},
                                     {'control_mode':2.},{'he_ua':-1.},{'he_max_bypass':1.1},
                                     {'flow':float('nan')},{'he_required_return':0.}])
def test_invalid_inputs_refuse(changes):
    with pytest.raises(ValueError):
        body.calculate(point(**changes))
