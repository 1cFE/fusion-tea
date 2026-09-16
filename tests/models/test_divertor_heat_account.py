"""WI-065 independent heat-account identities, source profiles and runtime domains."""
import importlib
import math

import pytest
from tests.models.test_winding_pack_cost import runtime_paths

BASE = dict(p_alpha_heat_in=400., p_coupled_in=100., p_aux_required_in=100.,
            p_installed_coupled_in=120., p_rad_core_in=300., f_rad_total_in=.9,
            target_capture_fraction_in=.99, q_target_ref_in=9.5,
            p_nonrad_ref_in=50., q_target_limit_in=10., R_in=13., R_ref_in=13.)
NAMES = ('peak_equivalent_area', 'q_target_peak_area_scaled', 'f_rad_edge_defined',
         'peak_equivalent_area_defined', 'p_heat_abs', 'f_rad_edge_in_range',
         'q_target_margin', 'p_rad_total', 'p_target_nonrad', 'p_nonrad_uncaptured',
         'f_rad_edge', 'p_target_deposited', 'p_rad_edge',
         'p_heat_operating_minus_installed', 'power_account_valid', 'p_sep', 'q_target_peak')
FLAGS = ('f_rad_edge_defined', 'peak_equivalent_area_defined', 'power_account_valid')


@pytest.fixture(scope='module', params=['wrapper', 'completion'])
def ledger(runtime_paths, request):
    module = importlib.import_module('stellarator_tea.modules.mfe_divertor_heat.divertor_heat_ledger')
    impl = importlib.import_module('stellarator_tea.handwritten.mfe_divertor_heat.divertor_heat_ledger_impl')
    assert tuple(module.Divertor_Heat_LedgerOutput.model_fields) == NAMES
    assert impl.AUTO_IMPLEMENTED is False
    if request.param == 'wrapper':
        return lambda changes={}: module.Divertor_Heat_LedgerModule().run(**(BASE | changes)).data.model_dump()
    return lambda changes={}: dict(zip(NAMES, impl.run_divertor_heat_ledger(module.Divertor_Heat_LedgerInput(**(BASE | changes))), strict=True))


@pytest.mark.parametrize('capture,peak,deposit,area', [(.99,9.5,49.5,49.5/9.5), (.97,5.,48.5,9.7)])
def test_paired_source_cases(ledger, capture, peak, deposit, area):
    r = ledger({'target_capture_fraction_in':capture, 'q_target_ref_in':peak})
    assert r['p_rad_total'] == 450.
    assert r['p_rad_edge'] == 150.
    assert r['p_target_nonrad'] == 50.
    assert r['p_target_deposited'] == deposit
    assert r['p_nonrad_uncaptured'] == 50-deposit
    assert r['q_target_peak'] == peak
    assert r['peak_equivalent_area'] == pytest.approx(area)
    assert r['p_target_deposited']/r['peak_equivalent_area'] == pytest.approx(peak)
    assert all(r[f] == 1 for f in FLAGS)


@pytest.mark.parametrize('radiation', [0.,.3,.6,.9,1.])
@pytest.mark.parametrize('capture', [.01,.97,.99,1.])
def test_destinations_conserve_absorbed_heat(ledger, radiation, capture):
    r=ledger({'f_rad_total_in':radiation,'target_capture_fraction_in':capture})
    assert 300+r['p_rad_edge']+r['p_target_deposited']+r['p_nonrad_uncaptured'] == pytest.approx(500.)
    assert r['p_rad_edge']+r['p_target_nonrad'] == pytest.approx(r['p_sep'])
    assert r['p_rad_total'] == 300+r['p_rad_edge']
    assert r['p_target_deposited']/r['peak_equivalent_area'] == pytest.approx(r['q_target_peak'])
    assert r['power_account_valid'] == float(radiation >= .6)
    assert all(math.isfinite(v) for v in r.values())
    assert all(r[f] in (0.,1.) for f in FLAGS)


def test_fixed_profile_load_linearity(ledger):
    r=ledger(); twice=ledger({'p_alpha_heat_in':800.,'p_coupled_in':200.,'p_rad_core_in':600.})
    for key in ('p_target_nonrad','p_target_deposited','p_nonrad_uncaptured','q_target_peak','p_rad_total','p_rad_edge'):
        assert twice[key] == 2*r[key]
    assert twice['peak_equivalent_area'] == r['peak_equivalent_area']
    assert twice['q_target_margin'] < 0


def test_capture_metadata_changes_deposition_and_implied_area_together(ledger):
    a=ledger(); b=ledger({'target_capture_fraction_in':.5})
    assert b['q_target_peak'] == a['q_target_peak']
    assert b['p_target_deposited'] / a['p_target_deposited'] == pytest.approx(b['peak_equivalent_area'] / a['peak_equivalent_area'])
    assert b['p_nonrad_uncaptured'] > a['p_nonrad_uncaptured']


def test_radius_is_shadow_only_at_fixed_inputs(ledger):
    a=ledger(); b=ledger({'R_in':26.})
    assert b['q_target_peak_area_scaled'] == a['q_target_peak_area_scaled']/2
    assert {k:v for k,v in a.items() if k!='q_target_peak_area_scaled'} == {k:v for k,v in b.items() if k!='q_target_peak_area_scaled'}


def test_negative_edge_remains_invalid_diagnostic(ledger):
    r=ledger({'f_rad_total_in':.5})
    assert r['p_rad_edge'] == -50
    assert r['f_rad_edge'] == -.25
    assert r['f_rad_edge_in_range'] < 0
    assert r['power_account_valid'] == 0
    assert r['f_rad_edge_defined'] == 1


def test_zero_power_and_full_radiation(ledger):
    zero=ledger({'p_alpha_heat_in':0.,'p_coupled_in':0.,'p_rad_core_in':0.,'p_aux_required_in':-30.})
    assert zero['p_heat_abs'] == zero['p_sep'] == zero['p_rad_edge'] == zero['p_target_deposited'] == zero['q_target_peak'] == 0
    assert zero['f_rad_edge'] == zero['f_rad_edge_defined'] == 0
    assert zero['power_account_valid'] == zero['peak_equivalent_area_defined'] == 1
    assert zero['p_heat_operating_minus_installed'] == -150.
    full=ledger({'f_rad_total_in':1.})
    assert full['p_target_nonrad'] == full['p_target_deposited'] == full['p_nonrad_uncaptured'] == full['q_target_peak'] == 0
    assert full['f_rad_edge'] == full['power_account_valid'] == 1


@pytest.mark.parametrize('f,valid', [(1.,1.),(.9,0.)])
def test_zero_separatrix_definedness(ledger,f,valid):
    r=ledger({'p_rad_core_in':500.,'f_rad_total_in':f})
    assert r['p_sep'] == r['f_rad_edge'] == r['f_rad_edge_defined'] == 0
    assert r['power_account_valid'] == valid


@pytest.mark.parametrize('capture',[0.,1.])
def test_dormant_reference_is_undefined_area_carrier(ledger,capture):
    r=ledger({'q_target_ref_in':0.,'target_capture_fraction_in':capture})
    assert r['peak_equivalent_area'] == r['peak_equivalent_area_defined'] == r['q_target_peak'] == 0
    assert r['p_target_nonrad'] == 50
    assert r['power_account_valid'] == 1


@pytest.mark.parametrize('key',BASE)
@pytest.mark.parametrize('bad',[float('inf'),float('-inf'),float('nan')])
def test_nonfinite_inputs_refused(ledger,key,bad):
    with pytest.raises(ValueError): ledger({key:bad})


@pytest.mark.parametrize('key',[k for k in BASE if k not in ('p_aux_required_in','p_coupled_in')])
def test_negative_physical_input_refused(ledger,key):
    with pytest.raises(ValueError): ledger({key:-1.})


@pytest.mark.parametrize('changes',[
    {'p_nonrad_ref_in':0.}, {'R_in':0.}, {'R_ref_in':0.},
    {'target_capture_fraction_in':1.01}, {'f_rad_total_in':1.01},
    {'p_rad_core_in':501.}, {'target_capture_fraction_in':0.},
    {'p_coupled_in':-401., 'p_rad_core_in':0.},
])
def test_invalid_domains_refused(ledger,changes):
    with pytest.raises(ValueError): ledger(changes)


@pytest.mark.parametrize('changes',[
    {'p_alpha_heat_in':1e308,'p_coupled_in':1e308},
    {'q_target_ref_in':1e308},
    {'R_ref_in':1e308},
    {'p_aux_required_in':-1e308,'p_installed_coupled_in':1e308},
    {'q_target_ref_in':1e-308,'p_nonrad_ref_in':1e308},
    {'q_target_ref_in':1e308,'p_nonrad_ref_in':1e-300,'f_rad_total_in':1.},
    {'target_capture_fraction_in':1e-300,'p_nonrad_ref_in':1e-300},
    {'q_target_ref_in':1e-300,'p_nonrad_ref_in':1e100},
    {'R_ref_in':1e-300,'R_in':1e100},
    {'p_alpha_heat_in':5e-324,'p_coupled_in':0.,'p_rad_core_in':0.,'f_rad_total_in':.1},
    {'p_alpha_heat_in':5e-324,'p_coupled_in':0.,'p_rad_core_in':0.,'f_rad_total_in':0.,'target_capture_fraction_in':.1},
    {'p_alpha_heat_in':5e-324,'p_coupled_in':0.,'p_rad_core_in':0.,'f_rad_total_in':0.,'target_capture_fraction_in':.99},
])
def test_nonrepresentable_intermediates_refused(ledger,changes):
    with pytest.raises(ValueError): ledger(changes)


@pytest.mark.parametrize('coupled,core', [(-50.,300.), (-400.,0.)])
def test_signed_operating_demand_preserves_burn_hold_diagnostic(ledger,coupled,core):
    r=ledger({'p_coupled_in':coupled,'p_rad_core_in':core,'p_aux_required_in':coupled})
    h=400.+coupled
    nonrad=h-.9*h
    assert r['p_heat_abs'] == h
    assert r['p_target_nonrad'] == nonrad
    assert r['q_target_peak'] == 9.5*nonrad/50.
    assert r['p_heat_operating_minus_installed'] == coupled-120.
    assert r['p_rad_edge'] >= 0
    assert r['power_account_valid'] == 0
    assert core+r['p_rad_edge']+r['p_target_deposited']+r['p_nonrad_uncaptured'] == pytest.approx(h)
    if h==0:
        assert r['f_rad_edge_defined'] == 0
