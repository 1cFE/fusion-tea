"""WI-056: primary-loop heating domain and independent heat-flow checks."""
import importlib
import math
import os
from pathlib import Path
import sys
import pytest
ROOT=Path(__file__).resolve().parents[2]
BASE=dict(q_source_in=2101.7,T_in_in=573.15,dT_blanket_in=200.,cp_in=5193.,gamma_in=1.6667,p_loop_in=8e6,n_loops_in=9.,mdot_loop_ref_in=2025.7/9,mdot_loop_rated_in=2025.7/9,dp_loop_ref_in=550000.,f_loss_in=1.,eta_is_in=.9,eta_drive_in=.95,loop_live_in=1.,p_pump_direct_in=3.,eta_p_direct_in=.5)

@pytest.fixture(scope='module')
def module():
    paths=[str(ROOT/'exploration/stellarator_e2e/pkg')]
    if os.environ.get('STOP_PARSER_TEAX_ROOT'):
        paths.append(str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
    for path in paths:sys.path.insert(0,path)
    m=importlib.import_module('stellarator_tea.modules.mfe_primary_loop.primary_coolant_loop')
    assert Path(m.__file__).resolve().is_relative_to(ROOT/'exploration/stellarator_e2e/generated')
    yield m.Primary_Coolant_LoopModule()
    for path in paths:sys.path.remove(path)

@pytest.mark.parametrize('live',[0.,1.])
@pytest.mark.parametrize('heat',[0.,2101.7])
@pytest.mark.parametrize('field',['cp_in','dT_blanket_in'])
@pytest.mark.parametrize('bad',[0.,-0.,-1.,math.nan,math.inf,-math.inf])
def test_independent_heating_domains(module,live,heat,field,bad):
    with pytest.raises(ValueError,match='Primary Coolant Loop: '+field+' must be finite and positive'):
        module.run(**(BASE|{'loop_live_in':live,'q_source_in':heat,field:bad}))

@pytest.mark.parametrize('live',[0.,1.])
def test_negative_pair_is_not_admissible(module,live):
    with pytest.raises(ValueError,match='Primary Coolant Loop: cp_in'):
        module.run(**(BASE|{'loop_live_in':live,'cp_in':-5193.,'dT_blanket_in':-200.}))

@pytest.mark.parametrize('cp,rise',[(5193.,200.),(10386.,200.),(5193.,400.),(5000.,150.)])
def test_heat_units_and_work_conservation(module,cp,rise):
    r=module.run(**(BASE|{'cp_in':cp,'dT_blanket_in':rise})).data
    assert r.mdot*cp*rise/1e6==pytest.approx(BASE['q_source_in'],rel=1e-12)
    assert r.mdot_loop*BASE['n_loops_in']==pytest.approx(r.mdot,rel=1e-12)
    assert r.T_out-BASE['T_in_in']==pytest.approx(rise,rel=1e-12)
    assert r.q_ihx-BASE['q_source_in']==pytest.approx(r.w_fluid,rel=1e-12)
    assert r.p_elec*BASE['eta_drive_in']==pytest.approx(r.w_fluid,rel=1e-12)
    assert r.q_recovered_total==pytest.approx(r.w_fluid+1.5,rel=1e-12)
    assert r.p_pump_total==pytest.approx(r.p_elec+3.,rel=1e-12)

@pytest.mark.parametrize('field',['cp_in','dT_blanket_in'])
def test_inverse_flow_and_square_loss_scaling(module,field):
    a=module.run(**BASE).data
    b=module.run(**(BASE|{field:2*BASE[field]})).data
    assert b.mdot==pytest.approx(a.mdot/2,rel=1e-12)
    assert b.dp_loop==pytest.approx(a.dp_loop/4,rel=1e-12)
    assert b.p_elec<a.p_elec

@pytest.mark.parametrize('heat',[0.,2101.7])
def test_dormant_still_evaluates_flow_but_retains_direct_power(module,heat):
    active=module.run(**(BASE|{'q_source_in':heat})).data
    dormant=module.run(**(BASE|{'q_source_in':heat,'loop_live_in':0.})).data
    assert dormant.mdot==active.mdot
    assert dormant.w_fluid==active.w_fluid
    assert dormant.p_pump_total==3.
    assert dormant.q_recovered_total==1.5
    if heat==0.:
        assert dormant.mdot==dormant.w_fluid==dormant.p_elec==0.

def test_moscato_printed_anchor(module):
    # Section 2.1.1 prints 2101.7 MW and 2025.7 kg/s over 300→500°C.
    # Their rounded effective cp supplies an independent printed-flow control.
    implied_cp=2101.7e6/(2025.7*200.)
    result=module.run(**(BASE|{'cp_in':implied_cp})).data
    assert result.mdot==pytest.approx(2025.7,rel=1e-12)
    assert abs(implied_cp-5193.)/5193.<.0011
