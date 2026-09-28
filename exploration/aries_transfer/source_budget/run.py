"""Native partial source-budget accounting, not a full-plant LCOE calculation."""
import json
import math
from decimal import Decimal, localcontext
from pathlib import Path
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
EVIDENCE=ROOT/'work/active/WI-088_aries-source-budget-cost-contribution/evidence'
package=HERE/'budget_tea';runtime=HERE/'runtime';runtime.mkdir(exist_ok=True)
module,fingerprint=ProvisionalPackageLoader(package_dir=package,package_name='budget_tea',link_root=runtime/'link').load()
registry=module.create_budget_tea_registry();base=json.loads((package/'inputs/source_budget_params.json').read_text());P='aries_source_budget__';B=P+'budget_period__period__';C=P+'capital_budget__total__';Q=P+'partial_cost__cost_per_energy__lcoe'
from budget_tea.schemas.source_budget_params import SourceBudgetParams
assert not any('excluded_annual_channel' in k or 'module_count' in k for k in base)
assert not any('excluded_annual_channel' in k or 'module_count' in k for k in SourceBudgetParams.model_fields)
# Reference source completion, changing only the import namespace required in isolation.
original=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/n_1cfe_form_lcoe_impl.py'
namespace={};exec(compile(original.read_text().replace('from stellarator_tea.','from budget_tea.'),str(original),'exec'),namespace)
from budget_tea.modules.mfe_account_costs.n_1cfe_form_lcoe import n_1cfe_Form_LCOEInput

def execute(name,overrides):
    case=runtime/name;case.mkdir(exist_ok=True);values={**base,**{P+k:v for k,v in overrides.items()}}
    inputs=case/'inputs.json';inputs.write_text(json.dumps(values,indent=2)+'\n')
    pipeline=yaml.safe_load((package/'pipelines/pipeline.yaml').read_text())
    pipeline['modules']['entry_fusion']['inputs']['source_budget_params']='SourceBudgetParams '+str(inputs)
    target=case/'pipeline.yaml';target.write_text(yaml.safe_dump(pipeline,sort_keys=False))
    result=execute_pipeline(target,case/'outputs',registry=registry,custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
    return values,{k:v.model_dump(mode='json') if hasattr(v,'model_dump') else v for k,v in result.outputs.items()}

cases=[('literal_expression',{}),('inferred_fpy_calendar',{'budget_period__selected_mode':1.}),('land_cost_plus_one_million',{'land__selected_cost_usd2004':13929000.}),('literal_availability_070',{'budget_period__selected_availability':.7}),('inferred_availability_070',{'budget_period__selected_mode':1.,'budget_period__selected_availability':.7}),('rounded_replacement_975M',{'replacement_budget__selected_lifetime_cost_usd2004':975000000.}),('supplied_net_power_900MW',{'budget_period__selected_net_power':900.}),('capital_only_boundary',{'replacement_budget__selected_lifetime_cost_usd2004':0.})]
records=[]
for name,overrides in cases:
    values,out=execute(name,overrides)
    with localcontext() as ctx:
        ctx.prec=50;d=lambda key:Decimal(str(values[P+key]))
        direct=sum(Decimal(str(v)) for k,v in values.items() if k.endswith('__selected_cost_usd2004'))
        cap=direct*d('capital_budget__inclusive_multiplier');rep=d('replacement_budget__selected_lifetime_cost_usd2004');avail=d('budget_period__selected_availability');power=d('budget_period__selected_net_power');period=d('budget_period__selected_period')
        if d('budget_period__selected_mode')==1:period/=avail
        energy=Decimal(8760)*power*avail;capital_annual=cap/period;replacement_annual=rep/period
        checks={C+'direct_total':direct,C+'inclusive_capital':cap,C+'inclusive_addition':cap-direct,B+'annual_capital':capital_annual,B+'annual_replacement':replacement_annual,B+'partial_annual_cost':capital_annual+replacement_annual,B+'comparison_period':period,B+'annual_energy':energy,B+'lifetime_energy':energy*period,B+'validated_net_power':power,B+'validated_availability':avail,B+'module_count':Decimal(1),B+'excluded_annual_channel':Decimal(0),Q:(cap+rep)/(period*energy)}
        for key,value in checks.items():assert math.isclose(out[key],float(value),rel_tol=3e-15,abs_tol=1e-9),(name,key,out[key],value)
    ref=namespace['run_n_1cfe_form_lcoe'](n_1cfe_Form_LCOEInput(cas90=out[B+'annual_capital'],cas70=out[B+'annual_replacement'],cas80=out[B+'excluded_annual_channel'],net_electric_mw=out[B+'validated_net_power'],n_mod_in=out[B+'module_count'],availability_in=out[B+'validated_availability']))
    assert out[Q]==ref
    for key,value in base.items():assert values[key]==overrides.get(key[len(P):],value)
    records.append(dict(case=name,effective_inputs=values,outputs=out,independent_comparisons=len(checks),reused_formula_exact=True,capital_only_cost_per_mwh=out[B+'annual_capital']/out[B+'annual_energy']))
assert math.isclose(records[1]['outputs'][Q],records[0]['outputs'][Q]*.85,rel_tol=2e-15)
assert math.isclose(records[4]['outputs'][Q],records[1]['outputs'][Q],rel_tol=2e-15)
assert math.isclose(records[3]['outputs'][Q],records[0]['outputs'][Q]*.85/.7,rel_tol=2e-15)
assert math.isclose(records[2]['outputs'][C+'inclusive_capital']-records[0]['outputs'][C+'inclusive_capital'],1930000.,abs_tol=1e-6)
assert records[7]['outputs'][Q]==records[7]['capital_only_cost_per_mwh']
invalids=[('negative_account',{'land__selected_cost_usd2004':-1.},'nonnegative'),('nonfinite_account',{'structures__selected_cost_usd2004':float('inf')},'finite'),('negative_replacement',{'replacement_budget__selected_lifetime_cost_usd2004':-1.},'nonnegative'),('nan_replacement',{'replacement_budget__selected_lifetime_cost_usd2004':float('nan')},'finite'),('zero_multiplier',{'capital_budget__inclusive_multiplier':0.},'positive'),('infinite_multiplier',{'capital_budget__inclusive_multiplier':float('inf')},'finite'),('zero_period',{'budget_period__selected_period':0.},'positive'),('nan_period',{'budget_period__selected_period':float('nan')},'finite'),('invalid_mode',{'budget_period__selected_mode':.5},'mode'),('zero_power',{'budget_period__selected_net_power':0.},'positive'),('nonfinite_power',{'budget_period__selected_net_power':float('inf')},'finite'),('zero_availability',{'budget_period__selected_availability':0.},'availability'),('availability_above_one',{'budget_period__selected_availability':1.01},'availability'),('nonfinite_availability',{'budget_period__selected_availability':float('nan')},'finite'),('budget_overflow',{'land__selected_cost_usd2004':1e308},'nonfinite'),('period_overflow',{'budget_period__selected_mode':1.,'budget_period__selected_period':1e308,'budget_period__selected_availability':1e-308},'nonfinite'),('zero_energy_underflow',{'budget_period__selected_net_power':5e-324,'budget_period__selected_availability':5e-324},'energy must be positive'),('quotient_overflow',{'land__selected_cost_usd2004':1e300,'budget_period__selected_net_power':1e-300},'quotient'),('excluded_channel_override',{'budget_period__excluded_annual_channel':1.},'Extra inputs'),('module_count_override',{'budget_period__module_count':2.},'Extra inputs')]
refusals=[]
for name,overrides,message in invalids:
    try:execute(name,overrides)
    except Exception as exc:
        assert message in str(exc),(name,type(exc).__name__,str(exc))
        refusals.append(dict(case=name,overrides={k:str(v) if not math.isfinite(v) else v for k,v in overrides.items()},exception=type(exc).__name__,message=str(exc)))
    else:raise AssertionError('invalid case returned: '+name)
payload=dict(claim='Partial supplied capital and operating-replacement cost contribution under explicit period conventions; not plant LCOE or reconciliation.',fingerprint=str(fingerprint),cases=records,refusals=refusals,source_diagnostics=dict(published_total_cost_per_mwh=77.6,published_approximate_capital_share=.82,share_implied_capital_cost_per_mwh=77.6*.82,literal_capital_contribution=records[0]['capital_only_cost_per_mwh'],table_vii_replacement_USD2004=966000000.,rounded_75M_times13_USD2004=975000000.,replacement_difference_USD2004=9000000.),all_checks_passed=True)
(EVIDENCE/'results.json').write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
summary=[dict(case=r['case'],partial_annual_cost_USD2004=r['outputs'][B+'partial_annual_cost'],comparison_period=r['outputs'][B+'comparison_period'],lifetime_energy_MWh=r['outputs'][B+'lifetime_energy'],partial_contribution_USD2004_per_MWh=r['outputs'][Q]) for r in records]
print(json.dumps(dict(cases=summary,independent_comparisons=sum(r['independent_comparisons'] for r in records),exact_reuse_comparisons=len(records),native_refusals=len(refusals),all_checks_passed=True),indent=2))
