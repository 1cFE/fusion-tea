"""WI-061 independent geometric witnesses and public fit behavior."""
import importlib
import math
import pytest
from tests.models.test_winding_pack_cost import runtime_paths, evaluate, output, P

BASE = dict(wp_side=.25, aspect_ratio=1., internal_fraction_x=0., internal_fraction_y=0.,
            ground_insulation=0., radial_allocation=.375, interior_y=.25,
            wall_thickness=.0625, assembly_clearance=0.)
FIT_ID = P + 'wp_fit_ok__a25ca6a0161f6339'

@pytest.fixture(scope='module')
def fit(runtime_paths):
    module = importlib.import_module('stellarator_tea.modules.mfe_winding_pack_fit.winding_pack_casing_fit')
    wrapper = module.Winding_Pack_Casing_FitModule()
    return lambda changes={}: wrapper.run(**(BASE | changes)).data.model_dump()

@pytest.mark.parametrize('change,margins', [({}, (0.,0.)),
    ({'radial_allocation':.34375},(-.03125,0.)),
    ({'interior_y':.21875},(0.,-.03125)),
    ({'radial_allocation':.40625,'interior_y':.28125},(.03125,.03125))])
def test_exact_boundary_and_each_axis(fit, change, margins):
    row=fit(change)
    assert (row['margin_x'],row['margin_y']) == margins
    assert row['nominal_x']*row['nominal_y'] == .0625


def test_allowances_count_once_and_orientation(fit):
    row=fit(dict(aspect_ratio=4., internal_fraction_x=.25, internal_fraction_y=.5,
                 ground_insulation=.015625, assembly_clearance=.0078125))
    assert row['nominal_x']==.5 and row['nominal_y']==.125
    assert row['internal_x']==.125 and row['internal_y']==.0625
    assert row['pack_x']==.625 and row['pack_y']==.1875
    assert row['required_x']==.671875 and row['required_y']==.234375
    assert row['exterior_x']==.375 and row['exterior_y']==.375

@pytest.mark.parametrize('key', BASE)
@pytest.mark.parametrize('bad', [float('nan'),float('inf'),-float('inf'),-1.])
def test_invalid_inputs_deliberately_refused(fit,key,bad):
    with pytest.raises(ValueError,match=key): fit({key:bad})

@pytest.mark.parametrize('change,diagnosis', [
    ({'wp_side':0.},'wp_side'), ({'aspect_ratio':0.},'aspect_ratio'),
    ({'wall_thickness':.25},'cavity_x'), ({'wall_thickness':1e308},'two_walls'),
    ({'interior_y':1e308,'wall_thickness':5e307,'radial_allocation':1.5e308},'exterior_y'),
    ({'wp_side':1e308,'aspect_ratio':1e308},'nominal_x'),
    ({'wp_side':1e-308,'aspect_ratio':1e308},'nominal_y'),
    ({'internal_fraction_y':1e308,'wp_side':4.},'internal_y'),
    ({'internal_fraction_x':1e-308,'wp_side':1e-308},'internal_x'),
    ({'ground_insulation':1e308},'two_ground_faces'),
    ({'assembly_clearance':1e308},'two_clearance_faces'),
])
def test_arithmetic_domain(fit,change,diagnosis):
    with pytest.raises(ValueError,match=diagnosis): fit(change)

@pytest.mark.codegen_available
@pytest.mark.parametrize('changes', [
    {}, {'magnet__winding_pack__j_wp':118.8271604938272*.8},
    {'magnet__coil__I_coil':15.4e6*1.1}, {'magnet__winding_pack__B_max':30.},
    {'magnet__winding_pack__internal_build_y':0.},
    {'magnet__winding_pack__fit_aspect_ratio':1.25},
    {'magnet__casing__wall_thickness':.035},
    {'magnet__casing__interior_y':.35}, {'magnet__coil__coil_t':.5},
])
def test_public_native_oracle_and_existing_predicates(evaluate,changes):
    import oracle_entry
    row=evaluate(changes)
    expected=oracle_entry.evaluate({P+k:v for k,v in changes.items()})
    for key,value in expected.items():
        assert row.outputs[key]==pytest.approx(value,rel=1e-10,abs=1e-9),key
    assert len([k for k in row.responses if k!='headline'])==19
    assert row.outputs[P+'magnet__wp_fit__cavity_x']==pytest.approx(changes.get('magnet__coil__coil_t',.3)-2*changes.get('magnet__casing__wall_thickness',.025))
    if not changes:
        assert output(row,'magnet__wp_fit__margin_x')==pytest.approx(-.120)
        assert output(row,'magnet__wp_fit__margin_y')==pytest.approx(.021)

@pytest.mark.codegen_available
def test_local_geometry_has_no_existing_physical_cost_effect(evaluate):
    before=evaluate(); after=evaluate({'magnet__winding_pack__fit_aspect_ratio':1.25,'magnet__casing__interior_y':.5})
    for key,value in before.outputs.items():
        if '__wp_fit__' not in key and 'wp_fit_ok' not in key and key!='constraint_report':
            assert after.outputs[key]==value,key
    for key,value in before.responses.items():
        if 'wp_fit_ok' not in key:
            assert after.responses[key]==value,key

@pytest.mark.parametrize('change', [{}, {'radial_allocation':.34375}, {'interior_y':.21875},
    {'radial_allocation':.40625,'interior_y':.28125}])
def test_native_predicate_equivalent_to_two_axis_check(fit, change):
    row=fit(change)
    module=importlib.import_module('stellarator_tea.modules.stellarator_09.stellariswpfitokconstraintmodule')
    verdict=module.StellarisWpFitOkConstraintModule().run(minimum_margin_in=row['minimum_margin']).data.evaluation
    assert row['minimum_margin']==min(row['margin_x'],row['margin_y'])
    expected='satisfied' if row['margin_x']>=0 and row['margin_y']>=0 else 'violated'
    assert verdict.status==expected

@pytest.mark.codegen_available
def test_entering_baseline_scalars_preserved(evaluate):
    import json
    from pathlib import Path
    entering=json.loads(Path('work/orchestration/goals/winding-pack-casing-fit/evidence/entering/comparison.json').read_text())['baseline']
    row=evaluate()
    assert len(entering)==179
    previous=json.loads(Path('work/active/WI-060_tape-procurement-quantity-basis/evidence/baseline.json').read_text())
    for key,value in previous['outputs'].items():
        if isinstance(value,(int,float)):
            assert row.outputs[key] == value,key
    assert {k: v for k, v in row.responses.items() if 'wp_fit_ok' not in k} == previous['responses']
    for key,value in entering.items():
        assert row.outputs[key]==pytest.approx(value,rel=1e-10,abs=1e-9),key

@pytest.mark.parametrize('key', ['fit_aspect_ratio','fit_wall','fit_interior_y','coil_t',
    'fit_internal_x','fit_internal_y','fit_ground','fit_clearance'])
@pytest.mark.parametrize('bad', [float('nan'),float('inf'),-1.])
def test_independent_oracle_geometry_domains(runtime_paths,key,bad):
    import verify_stellaris as vs
    with pytest.raises(ValueError,match=key):
        vs._winding_fit(vs.IN | {key:bad})

@pytest.mark.codegen_available
def test_zero_cavity_is_native_refusal(evaluate):
    with pytest.raises(Exception,match='cavity_x'):
        evaluate({'magnet__casing__wall_thickness':.15})
