"""Real native Brayton execution with independent Decimal state/energy checks."""
import json
import math
from decimal import Decimal, localcontext
from pathlib import Path
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
EVIDENCE=ROOT/'work/active/WI-087_aries-nominal-brayton-component-cycle/evidence'
package=HERE/'brayton_tea'
runtime=HERE/'runtime';runtime.mkdir(exist_ok=True)
module,fingerprint=ProvisionalPackageLoader(package_dir=package,package_name='brayton_tea',link_root=runtime/'link').load()
registry=module.create_brayton_tea_registry()
base=json.loads((package/'inputs/nominal_brayton_params.json').read_text())
P='aries_nominal_brayton__'

def execute(name,overrides):
    case=runtime/name;case.mkdir(exist_ok=True)
    values={**base,**{P+k:v for k,v in overrides.items()}}
    for key in values:
        if key.endswith(('__assumed_supported','__scenario_applicable','__demand_available')):values[key]=bool(values[key])
    inputs=case/'inputs.json';inputs.write_text(json.dumps(values,indent=2)+'\n')
    pipeline=yaml.safe_load((package/'pipelines/pipeline.yaml').read_text())
    pipeline['modules']['entry_fusion']['inputs']['nominal_brayton_params']='NominalBraytonParams '+str(inputs)
    target=case/'pipeline.yaml';target.write_text(yaml.safe_dump(pipeline,sort_keys=False))
    result=execute_pipeline(target,case/'outputs',registry=registry,custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
    return values,{k:v.model_dump(mode='json') if hasattr(v,'model_dump') else v for k,v in result.outputs.items()}

def oracle(values):
    with localcontext() as ctx:
        ctx.prec=50
        d=lambda key:Decimal(str(values[P+key]))
        m=d('operating_point__selected_flow');cp=d('operating_point__cp');a=1-1/d('operating_point__gamma');million=Decimal(1000000)
        p=d('operating_point__return_pressure');t=d('operating_point__low_temperature');checks={};works=[];cools=[]
        def put(part,calc,**fields):
            checks.update({P+part+'__'+calc+'__'+key:value for key,value in fields.items()})
        for i in range(1,4):
            ratio=d(f'compressor_{i}__selected_ratio');eta=d(f'compressor_{i}__efficiency')
            tout=t*(1+(ratio**a-1)/eta);p=p*ratio;work=m*cp*(tout-t)/million;works.append(work)
            put(f'compressor_{i}','performance',temperature_out=tout,pressure_out=p,shaft_demand=work)
            if i<3:
                t=d(f'intercooler_{i}__target_temperature');q=m*cp*(t-tout)/million;cools.append(q)
                put(f'intercooler_{i}','conditioning',temperature_out=t,pressure_out=p,heat_into_fluid=q)
        final_compressor_t=tout;discharge=p
        turbine_pin=p*(1-d('hot_side_loss__loss_fraction'));put('hot_side_loss','loss',pressure_out=turbine_pin)
        lowp=d('operating_point__return_pressure');turbine_tin=d('operating_point__turbine_temperature')
        turbine_tout=turbine_tin*(1-d('equivalent_turbine__efficiency')*(1-(lowp/turbine_pin)**a));wt=m*cp*(turbine_tin-turbine_tout)/million
        put('equivalent_turbine','performance',temperature_out=turbine_tout,pressure_out=lowp,shaft_produced=wt)
        exchange=d('recuperator__effectiveness')*(turbine_tout-final_compressor_t)
        coldout=final_compressor_t+exchange;hotout=turbine_tout-exchange
        put('recuperator','exchange',cold_temperature_out=coldout,hot_temperature_out=hotout,transferred_heat=m*cp*exchange/million)
        heat=m*cp*(turbine_tin-coldout)/million;lowt=d('operating_point__low_temperature');pre=m*cp*(lowt-hotout)/million
        put('heater','conditioning',temperature_out=turbine_tin,pressure_out=turbine_pin,heat_into_fluid=heat)
        put('precooler','conditioning',temperature_out=lowt,pressure_out=lowp,heat_into_fluid=pre)
        demand=sum(works);rejection=-sum(cools)-pre;net=wt-demand
        put('cycle_ledger','balance',compressor_demand=demand,rejected_heat=rejection,net_shaft=net,shaft_efficiency=net/heat,energy_residual=Decimal(0),total_pressure_ratio=discharge/lowp)
        return checks

scenarios=[('nominal',{}),('higher_flow_fixed_hardware',{'operating_point__selected_flow':1200.}),('smaller_compressor_rating',{'compressor_capacity__offered_rating':900.}),('smaller_heater_rating',{'heater_capacity__offered_rating':1800.}),('smaller_rejection_rating',{'rejection_capacity__offered_rating':1000.}),('one_stage_ratio_changed',{'compressor_2__selected_ratio':1.6}),('higher_turbine_temperature',{'operating_point__turbine_temperature':1030.15}),('unsupported_heater',{'heater_capacity__assumed_supported':False}),('negative_net_shaft',{'equivalent_turbine__efficiency':0.15})]
records=[]
for name,overrides in scenarios:
    values,out=execute(name,overrides);expected=oracle(values)
    for key,value in expected.items():
        assert math.isclose(out[key],float(value),rel_tol=8e-14,abs_tol=5e-10),(name,key,out[key],value)
    demands={'compressor':out[P+'cycle_ledger__balance__compressor_demand'],'heater':out[P+'heater__conditioning__heat_into_fluid'],'rejection':out[P+'cycle_ledger__balance__rejected_heat']}
    verdicts={}
    for kind,demand in demands.items():
        prefix=P+kind+'_capacity__';rating=values[prefix+'offered_rating'];supported=values[prefix+'assumed_supported']
        ok=supported and rating>=demand;verdicts[kind]=ok
        assert out[prefix+'screen__capacity_ok'] is ok
        assert out[prefix+'screen__supported'] is supported
        assert out[prefix+'screen__evaluation_defined']==float(supported)
        assert out[prefix+'screen__margin']==rating-demand
        assert rating==overrides.get(kind+'_capacity__offered_rating',base[prefix+'offered_rating'])
    report=out['constraint_report'];assert report['assessed_entry_count']==3
    for result in report['results']:
        kind=next(k for k in demands if '__'+k+'_capacity__' in result['constraint_id'])
        assert result['status']==('satisfied' if verdicts[kind] else 'violated')
    records.append(dict(case=name,effective_inputs=values,outputs=out,independent_comparisons=len(expected),capacity_ok=verdicts,source_comparison=dict(heater_inlet_C_difference=out[P+'recuperator__exchange__cold_temperature_out']-273.15-355.,shaft_vs_published_gross_difference=out[P+'cycle_ledger__balance__shaft_efficiency']-.43,maximum_pressure_MPa_difference=out[P+'compressor_3__performance__pressure_out']-15.,compression_ratio_difference=out[P+'cycle_ledger__balance__total_pressure_ratio']-3.5)))
nominal=records[0]['outputs'];higher=records[1]['outputs'];ledger=P+'cycle_ledger__balance__'
for key in ('compressor_demand','rejected_heat','net_shaft'):assert math.isclose(higher[ledger+key],1.2*nominal[ledger+key],rel_tol=2e-14)
assert math.isclose(higher[ledger+'shaft_efficiency'],nominal[ledger+'shaft_efficiency'],rel_tol=2e-14)
assert all(records[0]['capacity_ok'].values()) and not any(records[1]['capacity_ok'].values())
for index,kind in enumerate(('compressor','heater','rejection'),2):assert records[index]['capacity_ok'][kind] is False
for index in (5,6):
    assert records[index]['outputs'][ledger+'net_shaft']!=nominal[ledger+'net_shaft']
for i in (1,3):assert records[5]['effective_inputs'][P+f'compressor_{i}__selected_ratio']==base[P+f'compressor_{i}__selected_ratio']
assert records[5]['outputs'][P+'compressor_3__performance__pressure_out']!=nominal[P+'compressor_3__performance__pressure_out']
assert records[8]['outputs'][ledger+'net_shaft']<0

invalids=[('zero_flow',{'operating_point__selected_flow':0.},'positive'),('zero_cp',{'operating_point__cp':0.},'positive'),('bad_gamma',{'operating_point__gamma':1.},'gamma'),('zero_temperature',{'operating_point__low_temperature':0.},'positive'),('zero_pressure',{'operating_point__return_pressure':0.},'positive'),('bad_ratio',{'compressor_1__selected_ratio':.9},'ratio'),('zero_compressor_efficiency',{'compressor_1__efficiency':0.},'efficiency'),('high_turbine_efficiency',{'equivalent_turbine__efficiency':1.1},'efficiency'),('bad_effectiveness',{'recuperator__effectiveness':1.1},'effectiveness'),('bad_loss',{'hot_side_loss__loss_fraction':1.},'fraction'),('no_expansion',{'hot_side_loss__loss_fraction':.8},'expansion'),('heater_as_cooler',{'heater__heating_role':0.},'cooler'),('cooler_as_heater',{'intercooler_1__heating_role':1.},'heater'),('bad_role',{'precooler__heating_role':.5},'role'),('hot_cooler_target',{'intercooler_1__target_temperature':500.},'cooler'),('reversed_recuperator',{'operating_point__turbine_temperature':400.},'recuperator'),('nan_flow',{'operating_point__selected_flow':float('nan')},'finite'),('infinite_ratio',{'compressor_2__selected_ratio':float('inf')},'finite'),('negative_rating',{'heater_capacity__offered_rating':-1.},'rating'),('infinite_rating',{'heater_capacity__offered_rating':float('inf')},'rating'),('overflow_flow',{'operating_point__selected_flow':1e308},'nonfinite')]
refusals=[]
for name,overrides,message in invalids:
    try:execute(name,overrides)
    except Exception as exc:
        assert message in str(exc),(name,type(exc).__name__,str(exc))
        refusals.append(dict(case=name,overrides={k:str(v) if not math.isfinite(v) else v for k,v in overrides.items()},exception=type(exc).__name__,message=str(exc)))
    else:raise AssertionError('invalid case returned: '+name)
# Generated ledger wrapper preserves signed diagnostic residuals and negative work.
from brayton_tea.modules.ideal_gas_brayton_components.brayton_cycle_ledger import Brayton_Cycle_LedgerModule
signed=[]
for heat in (8.,10.):
    result=Brayton_Cycle_LedgerModule().run(compressor_1_in=1.,compressor_2_in=1.,compressor_3_in=1.,turbine_work_in=9.,intercooler_1_in=-1.,intercooler_2_in=-1.,precooler_in=-1.,heater_in=heat,inlet_pressure_in=1.,discharge_pressure_in=3.)
    assert result.data.energy_residual==heat-9.;signed.append(result.data.energy_residual)
payload=dict(claim='Reduced nominal ideal-gas component cycle; shaft work, not electrical output or qualified off-design equipment.',fingerprint=str(fingerprint),cases=records,refusals=refusals,generated_wrapper_signed_residuals=signed,all_checks_passed=True)
(EVIDENCE/'results.json').write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
summary=[dict(case=r['case'],net_shaft_MW=r['outputs'][ledger+'net_shaft'],heater_MW=r['outputs'][P+'heater__conditioning__heat_into_fluid'],shaft_efficiency=r['outputs'][ledger+'shaft_efficiency'],energy_residual_MW=r['outputs'][ledger+'energy_residual'],capacity_ok=r['capacity_ok']) for r in records]
print(json.dumps(dict(cases=summary,independent_comparisons=sum(r['independent_comparisons'] for r in records),native_refusals=len(refusals),signed_residuals=signed,all_checks_passed=True),indent=2))
