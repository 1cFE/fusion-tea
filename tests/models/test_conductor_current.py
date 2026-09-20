from tests.models.current_mfe_regressions import (CURRENT_PREDICATES, historical_point, assert_historical_native, assert_current_predicates, PARTITIONS)
"""WI-062 analytic current capacity, domains and physical inventory propagation."""
import importlib
import json
from pathlib import Path
import pytest
from tests.models.test_winding_pack_cost import runtime_paths, evaluate, output, P

BASE = dict(B_peak=20., temperature=20., tape_width=.004, tape_thickness=56e-6,
            tape_length=100., conductor_length=10., f_set=1., f_wp_vol=1., turn_current=1600.,
            reference_tape_current=200., material_factor=1., orientation_factor=1.,
            cabling_factor=1., degradation_factor=1., sharing_factor=1., allowable_fraction=.8,
            allow_field_extrapolation=0.)

@pytest.fixture(scope='module')
def current(runtime_paths):
    module=importlib.import_module('stellarator_tea.modules.mfe_conductor_current.rebco_conductor_current')
    wrapper=module.REBCO_Conductor_CurrentModule()
    return lambda changes={}: wrapper.run(**(BASE | changes)).data.model_dump()

@pytest.mark.parametrize('turn,margin',[(1600.,0.),(1500.,100.),(1700.,-100.)])
def test_analytic_boundary_and_native_predicate(current,turn,margin):
    row=current({'turn_current':turn})
    assert row['parallel_tapes_reference']==10
    assert row['critical_current_reference']==2000
    assert row['margin_current']==margin
    module=importlib.import_module('stellarator_tea.modules.stellarator_09.stellarisreferenceconductorcurrentokconstraintmodule')
    verdict=module.StellarisReferenceConductorCurrentOkConstraintModule().run(margin_fraction_in=row['margin_fraction']).data.evaluation
    assert verdict.status==('satisfied' if margin>=0 else 'violated')

@pytest.mark.parametrize('key',BASE)
@pytest.mark.parametrize('bad',[float('nan'),float('inf'),-1.])
def test_nonfinite_negative(current,key,bad):
    with pytest.raises(ValueError,match=key):current({key:bad})

@pytest.mark.parametrize('change',[
 {'temperature':19.},{'tape_thickness':60e-6},{'tape_width':.0039},{'tape_width':.0061},
 {'B_peak':19.9,'allow_field_extrapolation':1.},{'B_peak':32.1,'allow_field_extrapolation':1.},
 {'B_peak':24.1},{'allow_field_extrapolation':.5},{'allowable_fraction':0.},{'allowable_fraction':1.01},
 {'cabling_factor':1.1},{'degradation_factor':1.1},{'sharing_factor':1.1},
 {'tape_length':1e308,'conductor_length':1e-308},{'tape_length':1e-308,'conductor_length':1e308},
 {'reference_tape_current':1e308,'material_factor':1e308},
 {'reference_tape_current':1e-308,'degradation_factor':1e-308},
])
def test_unsupported_and_arithmetic(current,change):
    with pytest.raises(ValueError):current(change)

@pytest.mark.parametrize('field,flag',[(20.,0.),(24.,0.),(24.1,1.),(32.,1.)])
def test_field_domain(current,field,flag):
    row=current({'B_peak':field,'allow_field_extrapolation':flag})
    assert row['field_extrapolated']==float(field>24)
    assert row['tape_critical_current']==pytest.approx(200*(field/20)**-.6)


def test_retention_allowance_and_distribution_are_distinct(current):
    original=current(); derated=current({'degradation_factor':.5}); allowance=current({'allowable_fraction':.4})
    assert derated['critical_current_reference']==original['critical_current_reference']/2
    assert allowance['critical_current_reference']==original['critical_current_reference']
    assert derated['allowable_current']==allowance['allowable_current']
    row=current({'f_set':.8,'f_wp_vol':.5})
    assert row['parallel_tapes_set']==10
    assert row['parallel_tapes_reference']==16

@pytest.mark.codegen_available
@pytest.mark.parametrize('changes',[{}, {'magnet__coil__turn_current':25000.},
 {'magnet__coil__I_coil':15.4e6*1.05},{'magnet__winding_pack__B_max':30.},
 {'magnet__winding_pack__j_wp':150.},{'magnet__winding_pack__tape_width':.004},
 {'magnet__winding_pack__degradation_factor':.8},{'magnet__winding_pack__allowable_fraction':.6}])
def test_public_native_oracle(evaluate,changes):
    import oracle_entry
    row=evaluate(changes); expected=oracle_entry.evaluate({P+k:v for k,v in changes.items()})
    for key,value in expected.items():assert row.outputs[key]==pytest.approx(value,rel=1e-10,abs=1e-9),key
    assert set(row.responses) == CURRENT_PREDICATES | {'headline'}
    assert output(row,'magnet__conductor_current__parallel_tapes_set')==pytest.approx(output(row,'magnet__winding_procurement__tape_length')/output(row,'magnet__winding_procurement__conductor_length'))

@pytest.mark.codegen_available
def test_series_turn_repartition(evaluate):
    a=evaluate();b=evaluate({'magnet__coil__turn_current':25000.})
    for scope in ['reference','set']:
        assert output(b,'magnet__conductor_current__parallel_tapes_'+scope)==pytest.approx(output(a,'magnet__conductor_current__parallel_tapes_'+scope)/2)
        assert output(b,'magnet__conductor_current__operating_fraction_'+scope)==pytest.approx(output(a,'magnet__conductor_current__operating_fraction_'+scope))

@pytest.mark.codegen_available
def test_prior_native_reference_preserved(evaluate):
    old=json.loads(Path('work/orchestration/goals/absolute-conductor-current-margin/evidence/entering/native-reference.json').read_text())
    point=historical_point({P+'magnet__winding_pack__insulation_sheet_price':0.})
    row=evaluate({k.removeprefix(P):v for k,v in point.items()})
    assert_historical_native('conductor-current', row, old['outputs'], old['responses'], point)

@pytest.mark.codegen_available
def test_selected_field_predicate_independent(evaluate):
    weak=evaluate({'magnet__winding_pack__B_max':30.,'magnet__winding_pack__material_factor':.5})
    strong=evaluate({'magnet__winding_pack__B_max':24.,'magnet__winding_pack__orientation_factor':3.})
    for row,field_ok,current_ok in [(weak,'satisfied','violated'),(strong,'violated','satisfied')]:
        for key,status in [('peak_field_ok',field_ok),('reference_conductor_current_ok',current_ok)]:
            value=next(v for k,v in row.responses.items() if key+'__' in k)
            assert value==status
