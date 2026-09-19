"""WI-070 public native processing, accounting and physical-preservation checks."""
import importlib
import json
import math
from pathlib import Path
import pytest
from tests.models.test_winding_pack_cost import runtime_paths, evaluate, output, P

CASES = [({},'base'),({'fuel_cycle__burn_fraction':.025},'burn'),
 ({'plasma__T_i0':16.},'power'),({'fuel_cycle__processing_price_multiplier':1.7},'price'),
 ({'fuel_cycle__processing_capacity_margin':1.4},'margin'),
 ({'fuel_cycle__processing_containment_cpi':65.2},'date'),
 ({'fuel_cycle__processing_source_conditions':False},'undeclared'),
 ({'fuel_cycle__processing_enabled':False},'legacy'),
 ({'fuel_cycle__processing_enabled':False,'fuel_cycle__inventory_enabled':False},'dormant'),
 ({'unplanned_fraction':.2},'calendar')]

@pytest.mark.codegen_available
@pytest.mark.parametrize('changes,label',CASES,ids=[x[1] for x in CASES])
def test_all_mapped_native_outputs_at_public_cases(evaluate,changes,label):
    import oracle_entry as entry
    row=evaluate(changes)
    expected=entry.evaluate({P+k:v for k,v in changes.items()})
    for key,value in expected.items():
        assert row.outputs[key] == pytest.approx(value,rel=1e-9,abs=1e-18 if '__inventory__' in key else 1e-6),(label,key)
    if label=='base':
        assert output(row,'fuel_cycle__processing_cost__cost')==pytest.approx(22786229.4037934,abs=1e-6)
    if label=='undeclared':
        assert output(row,'fuel_cycle__processing_cost__defined_flag')==0
        assert output(row,'fuel_cycle__processing_cost__cost')>0
    if label in ('legacy','dormant'):
        assert output(row,'fuel_cycle__processing_cost__cost')==output(row,'fuel_cycle__fuel_handling__cost')
        assert output(row,'shipping_scope__fuel_installation_exclusion')==0

@pytest.mark.codegen_available
@pytest.mark.parametrize('change',[{'fuel_cycle__processing_price_multiplier':2.}, {'fuel_cycle__processing_containment_cpi':96.5},{'fuel_cycle__processing_capacity_margin':1.5}])
def test_cost_controls_preserve_every_other_physical_output_and_verdict(evaluate,change):
    import oracle_entry as entry
    a=evaluate();b=evaluate(change)
    # Exact identity for every output outside the declared processing/financial fan-out.
    financial=('fuel_cycle__processing_cost__','shipping_scope__','cas22_','cas2x_','contingency__','cas20_','indirect__','supplementary__','overnight_','idc__','total_capital__','cas90_1cfe_calc__','lcoe')
    ignored={key for key in a.outputs if any(t in key for t in financial)}
    # Some generated finance channels are named by their established consumers.
    economic_names=('cas30_capital','cas50_capital','capital_annualized','annual_capital_charge','capital_cost','coe','cost_of_electricity')
    ignored|={key for key in a.outputs if any(t in key for t in economic_names)}
    differing={key for key in a.outputs if a.outputs[key]!=b.outputs[key]}
    assert differing<=ignored,differing-ignored
    assert a.responses==b.responses
    assert output(a,'fuel_cycle__inventory__dt_processor_kg_s')==output(b,'fuel_cycle__inventory__dt_processor_kg_s')

@pytest.mark.codegen_available
@pytest.mark.parametrize('c',[0.,.1])
def test_native_old_to_new_account_identity(evaluate,c):
    a=evaluate({'fuel_cycle__processing_enabled':False,'contingency_rate':c})
    b=evaluate({'contingency_rate':c})
    import verify_stellaris as vs
    p=vs.IN;k=p['indirect_fraction']*p['construction_years']/p['reference_construction_time']
    d=output(b,'fuel_cycle__processing_cost__cost')-output(a,'fuel_cycle__processing_cost__cost')
    labor=output(b,'fuel_cycle__processing_cost__installation_total')
    ds=(1+p['supp_contingency_rate'])*(p['supp_shipping_frac']*(1+c)*(d-labor)+p['supp_tax_frac']*(1+c)*d+p['supp_insurance_frac']*(1+k)*(1+c)*d)
    assert output(b,'supplementary__cost')-output(a,'supplementary__cost')==pytest.approx(ds,abs=1e-6)
    assert output(b,'total_capital__total_capital')-output(a,'total_capital__total_capital')==pytest.approx((1+k)*(1+c)*d+ds,abs=1e-5)

@pytest.mark.parametrize('c,cs',[(0.,0.),(.1,.2),(.3,.1)])
def test_actual_shipping_and_supplementary_consumers(runtime_paths,c,cs):
    scope=importlib.import_module('stellarator_tea.modules.mfe_facilities.facility_shipping_scope').Facility_Shipping_ScopeModule()
    r=scope.run(cas20_in=1e9,cooling_exclusion_in=1e8,facility_exclusion_in=2e8,fuel_installation_in=3e7,contingency_in=c).data.model_dump()
    assert r['fuel_installation_exclusion']==(1+c)*3e7
    assert r['remaining_shipping_base']==1e9-3e8-(1+c)*3e7
    module=importlib.import_module('stellarator_tea.modules.mfe_account_costs.supplementary_cost').Supplementary_CostModule()
    args=dict(ref_net_power=1000.,shipping_frac=.015,tax_frac=.01,insurance_frac=.015,spares_frac=.04,startup_fuel_base=2e7,decom_base=3e7,cas20=1e9,cas23_to_28=1e8,cas30=2e8,p_net=1000.,n_mod_in=1.,delivered_shipping_exclusion_in=1e8,facility_exclusion_in=2e8,contingency_rate_in=cs)
    old=module.run(**args,fuel_installation_exclusion_in=0.).data.root
    new=module.run(**args,fuel_installation_exclusion_in=r['fuel_installation_exclusion']).data.root
    assert new-old==pytest.approx(-.015*(1+cs)*(1+c)*3e7,abs=1e-6)
    with pytest.raises(Exception):scope.run(cas20_in=1.,cooling_exclusion_in=0.,facility_exclusion_in=0.,fuel_installation_in=2.,contingency_in=0.)

@pytest.mark.codegen_available
def test_active_processing_refuses_disabled_inventory(evaluate):
    with pytest.raises(Exception):evaluate({'fuel_cycle__inventory_enabled':False})

@pytest.mark.codegen_available
def test_undefined_breeding_keeps_physical_exhaust_price_and_failure(evaluate):
    row=evaluate({'plasma__R':12.71})
    assert output(row,'blanket__breeding__defined_flag')==0
    assert output(row,'fuel_cycle__inventory__defined_flag')==0
    assert output(row,'fuel_cycle__inventory__dt_processor_kg_s')>0
    assert output(row,'fuel_cycle__processing_cost__defined_flag')==1
    assert output(row,'fuel_cycle__processing_cost__cost')>0
    assert next(v for k,v in row.responses.items() if '__tbr_ok__' in k)=='violated'

@pytest.mark.codegen_available
def test_calendar_does_not_size_running_processor(evaluate):
    a=evaluate();b=evaluate({'unplanned_fraction':.2})
    assert output(a,'fuel_cycle__inventory__dt_processor_kg_s')==output(b,'fuel_cycle__inventory__dt_processor_kg_s')
    assert output(a,'fuel_cycle__processing_cost__cost')==output(b,'fuel_cycle__processing_cost__cost')
    assert output(a,'fuel_cycle__inventory__calendar_processor_kg_s')!=output(b,'fuel_cycle__inventory__calendar_processor_kg_s')

def test_typed_public_calculation_preserves_all_row_outputs_and_modules(runtime_paths):
    from tests.models.test_fuel_processing_costs import CASE,decimal_reference
    module=importlib.import_module('stellarator_tea.modules.mfe_fuel_cycle.fuel_processing_cost').Fuel_Processing_CostModule()
    for changes in ({},{'n_mod':2.},{'flow':0.},{'source_conditions':False}):
        case=CASE|changes
        actual=module.run(**{k+'_in':v for k,v in case.items()}).data.model_dump()
        for key,value in decimal_reference(case).items():assert actual[key]==pytest.approx(value,rel=1e-12,abs=1e-9)
