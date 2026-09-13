"""WI-053: domain refusal and independent valid identities through public modules."""
import importlib
import math
import os
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
FIELD = dict(B_axis_in=9., peak_ratio_in=24.9/9., R_in=12.7, a_coil_in=3., R_ref_in=12.7, a_coil_ref_in=3.)
CRYO = dict(q_nuc=0., vol_cold=0., p_fixed=0., f_uplift=1., T_cold=20., T_amb=300., f_carnot=1., p_direct=0.)

@pytest.fixture(scope='module')
def modules():
    paths = [str(ROOT/'exploration/stellarator_e2e/pkg')]
    if os.environ.get('STOP_PARSER_TEAX_ROOT'):
        paths.append(str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
    for path in paths: sys.path.insert(0,path)
    field = importlib.import_module('stellarator_tea.modules.mfe_plasma_scaling.conductor_peak_field')
    cryo = importlib.import_module('stellarator_tea.modules.mfe_cryo_plant.cryoplant_electrical_power')
    assert Path(field.__file__).resolve().is_relative_to(ROOT/'exploration/stellarator_e2e/generated')
    yield field.Conductor_Peak_FieldModule(), cryo.Cryoplant_Electrical_PowerModule()
    for path in paths: sys.path.remove(path)

@pytest.mark.parametrize('side', ['live','reference'])
@pytest.mark.parametrize('clearance', [-.3,0.])
def test_clearance_refusal(modules,side,clearance):
    x = dict(FIELD)
    radius,coil = ('R_in','a_coil_in') if side=='live' else ('R_ref_in','a_coil_ref_in')
    x[coil] = 13.; x[radius] = 13.+clearance
    with pytest.raises(ValueError, match=f'Conductor Peak Field: {side} clearance'):
        modules[0].run(**x)

@pytest.mark.parametrize('cold,ambient', [(0.,300.),(-1.,300.),(300.,300.),(301.,300.),(20.,0.),(20.,-1.),(-2.,-1.),(0.,0.)])
@pytest.mark.parametrize('load', [0.,1.])
def test_temperature_refusal(modules,cold,ambient,load):
    with pytest.raises(ValueError, match='Cryoplant Electrical Power: require 0 < T_cold < T_amb'):
        modules[1].run(**dict(CRYO,T_cold=cold,T_amb=ambient,p_fixed=load))

def test_reference_anchor_and_geometry_scale_invariance(modules):
    run = modules[0].run
    assert run(**FIELD).data.root == FIELD['B_axis_in']*FIELD['peak_ratio_in']
    off = dict(FIELD,R_in=15.)
    value = run(**off).data.root
    scaled = {k: v*2 if k in ('R_in','a_coil_in','R_ref_in','a_coil_ref_in') else v for k,v in off.items()}
    assert run(**scaled).data.root == value
    # Independently cancel the rational factors, preserving the source equation.
    expected = 9*(24.9/9)*15*(12.7-3)/(12.7*(15-3))
    assert value == pytest.approx(expected,rel=1e-12)

def test_field_remains_signed(modules):
    assert modules[0].run(**dict(FIELD,B_axis_in=-9.)).data.root == -modules[0].run(**FIELD).data.root

@pytest.mark.parametrize('cold,ambient', [(20.,300.),(4.5,300.),(100.,200.),(299.,300.)])
def test_refrigeration_energy_identity(modules,cold,ambient):
    x = dict(CRYO,q_nuc=2000.,vol_cold=50.,p_fixed=.03,f_uplift=1.2,f_carnot=.24,p_direct=7.,T_cold=cold,T_amb=ambient)
    electrical = modules[1].run(**x).data.root
    heat = (2000*50*1e-6+.03)*1.2
    # Reversed Carnot first/second-law identity: recovered load matches input.
    recovered = (electrical-7.)*.24*cold/(ambient-cold)
    assert recovered == pytest.approx(heat,rel=1e-12)
    assert math.isfinite(electrical)

def test_dormant_direct_and_signed_controls(modules):
    run = modules[1].run
    assert run(**CRYO).data.root == 0.
    assert run(**dict(CRYO,p_direct=17.)).data.root == 17.
    assert run(**dict(CRYO,p_direct=-17.)).data.root == -17.
    assert run(**dict(CRYO,p_fixed=-1.)).data.root == -run(**dict(CRYO,p_fixed=1.)).data.root
