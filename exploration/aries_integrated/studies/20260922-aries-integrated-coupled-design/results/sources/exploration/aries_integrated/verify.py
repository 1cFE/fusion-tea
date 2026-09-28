"""Native MR-7, conservation, adverse-state and domain evidence for WI-090.

Independent checks use energy/state identities, not a second plant implementation.
"""
import json
import math
from decimal import Decimal
from pathlib import Path
from run import HERE, EVIDENCE, PREFIX as P, SCENARIOS, load_runtime, execute_case

PLASMA='aries_cs_plasma_integration__plasma__'


def value(row,owner,name):
    return row['outputs'][P+owner+'__evaluate__'+name]


def close(a,b,tol=1e-6):
    assert abs(a-b)<=tol,(a,b,a-b,tol)


def status(row,owner,gate):
    result=next(x for x in row['outputs']['constraint_report']['results'] if x['constraint_id'].startswith(P+owner+'__'+gate+'__'))
    return result['status']


def check_energy(row):
    assert row['status']=='evaluated',row.get('error')
    f=lambda owner,key:value(row,owner,key)
    inp=row['effective_inputs'];dec=lambda x:Decimal(str(x))
    c=dec(inp[P+'cycle__selected_flow'])*dec(inp[P+'cycle__cp'])/Decimal('1e6')
    # Check actual heater mixing from temperatures independently of closure's residual.
    observed=float(c*(dec(f('heat_exchangers','turbine_temperature'))-dec(f('recuperator','cold_out'))))
    close(observed,f('heat_exchangers','accepted_heat'))
    # Recompute electric boundary solely from separately owned work/load outputs.
    net=f('generator_auxiliaries','gross_electric')-f('generator_auxiliaries','shaft_import')
    net-=sum(f('generator_auxiliaries',k) for k in ('primary_pump_electric','heating_electric','cryo_electric','fuel_electric','control_electric','other_electric_demand'))
    close(net,f('plant_ledger','net_electric'))
    close(f('generator_auxiliaries','fuel_electric'),f('generator_auxiliaries','fuel_base_electric')+f('generator_auxiliaries','fuel_variable_electric'))
    # Heat transfer on both sides; counterflow terminal ordering and fixed hot bounds.
    for b in ('he','divertor','pbli'):
        q=f('heat_exchangers',b+'_transferred')
        close(q,float(c*(dec(f('heat_exchangers',b+'_secondary_out'))-dec(f('heat_exchangers',b+'_secondary_in')))))
        close(f(b+'_coolant','delivered_heat'),q+f('heat_exchangers',b+'_unmet'))
        if f('heat_exchangers',b+'_state_defined'):
            ch=dec(inp[P+'heat_exchangers__'+b+'_flow'])*dec(inp[P+'heat_exchangers__'+b+'_cp'])/Decimal('1e6')
            close(q,float(ch*(dec(f('heat_exchangers',b+'_hot'))-dec(f('heat_exchangers',b+'_return')))))
            assert f('heat_exchangers',b+'_hot_bound_margin')>=-1e-9
            assert f('heat_exchangers',b+'_hot_terminal_difference')>=-1e-9
            assert f('heat_exchangers',b+'_cold_terminal_difference')>=-1e-9
        else:
            assert q==0
            assert f('heat_exchangers',b+'_hot')==f('heat_exchangers',b+'_return')==0
    close(f('plant_ledger','branch_residual'),0)
    close(f('plant_ledger','cycle_residual'),0)
    close(f('plant_ledger','electrical_residual'),0)
    close(f('plant_ledger','turbine_state_residual'),0,1e-10)
    close(f('plant_ledger','recuperator_state_residual'),0,1e-10)
    close(f('plant_ledger','plant_residual'),-f('plant_ledger','source_energy_residual'))
    assert 1<=f('heat_exchangers','iterations')<=100
    assert f('plant_ledger','conditional_net_result')==1
    assert f('plant_ledger','net_result_producer_mode')==f('source','selected_mode')
    for key in ('supported_magnet','supported_breeding','supported_deposition','supported_hydraulics','supported_materials','supported_machine_map'):
        assert f('plant_ledger',key)==0
    # Energy per D-T reaction is a separate source-independent dimensional identity.
    expected_burn=float(dec(f('source','selected_power'))*Decimal('1e6')/(Decimal('17.58')*Decimal('1.6021766339999998e-13')))
    assert math.isclose(f('fuel','burn_rate'),expected_burn,rel_tol=3e-15)
    assert math.isclose(f('fuel','inject_rate'),f('fuel','burn_rate')+f('fuel','exhaust_rate'),rel_tol=3e-15)


def main():
    runtime=load_runtime(); rows=[]; expected={}
    base={P+'source__producer_mode':1.}
    cases=[(n,c,None) for n,c in SCENARIOS.items()]
    cases += [('density_lower',{**base,PLASMA+'amplitude':4.75e20},None),('density_higher',{**base,PLASMA+'amplitude':5.25e20},None),
              ('one_ratio',{**base,P+'compressor_1__selected_ratio':1.6},None),
              ('cycle_flow',{**base,P+'cycle__selected_flow':1500.},None),
              ('low_he_ua',{**base,P+'heat_exchangers__he_ua':.1},None),
              ('high_he_ua',{**base,P+'heat_exchangers__he_ua':100.},None),
              ('bypass_motor',{P+'source__reference_fusion_mw':600.},None),
              ('unsupported_capacity',{**base,P+'he_capacity__assumed_supported':False},None),
              ('zero_he_ua',{**base,P+'heat_exchangers__he_ua':0.},None),
              ('low_he_hot_bound',{**base,P+'heat_exchangers__he_limit':300.},None),
              ('zero_all_ua',{**base,**{P+'heat_exchangers__'+b+'_ua':0. for b in ('he','pbli','divertor')}},'cooler'),
              ('zero_selected_power',{P+'source__producer_mode':1.,PLASMA+'deuterium_fraction':0.},'strictly positive'),
              ('invalid_mode',{P+'source__producer_mode':2.},'mode'),
              ('invalid_fraction',{P+'deposition__radiation_fraction':1.1},'[0,1]'),
              ('negative_ua',{P+'heat_exchangers__he_ua':-1.},'invalid'),
              ('negative_flow',{P+'cycle__selected_flow':-1.},'positive'),
              ('invalid_recuperator',{P+'cycle__recuperator_effectiveness':1.1},'[0,1]'),
              ('invalid_heating_efficiency',{P+'generator_auxiliaries__heating_efficiency':0.},'(0,1]'),
              ('invalid_plasma_temperature',{PLASMA+'temperature_edge':.023},'domain')]
    for owner in ('he_capacity','pbli_capacity','divertor_capacity','compressor_capacity','turbine_capacity','rejection_capacity','generator_capacity','fuel_capacity'):
        cases += [(owner+'_low',{**base,P+owner+'__selected_rating':1e20 if owner=='fuel_capacity' else 1.},None),
                  (owner+'_high',{**base,P+owner+'__selected_rating':1e24 if owner=='fuel_capacity' else 10000.},None)]
    # Explicit native nonfinite test is retained as a refusal, never a study point.
    cases += [('nonfinite_ua',{P+'heat_exchangers__he_ua':float('nan')},'finite')]
    cases += equipment_cases(base)
    for name,changes,error in cases:
        changes = {((P+k[len(P+'heat_exchangers__'):-3]+'_hx__selected_area') if k.startswith(P+'heat_exchangers__') and k.endswith('_ua') else k): (v*1000 if k.startswith(P+'heat_exchangers__') and k.endswith('_ua') else v) for k,v in changes.items()}
        row=execute_case(name,changes,runtime);rows.append(row)
        (EVIDENCE/'verification-attempt.json').write_text(json.dumps(rows,indent=2)+'\n')
        if error:
            assert row['status']=='refused',(name,row['status'])
            assert error.lower() in row['error'].lower(),(name,row['error'])
        else:
            check_energy(row)
        print(name,row['status'])
    by={r['case']:r for r in rows}; baseline=by['nominal-calculated']
    assert status(baseline,'plant_ledger','heat_removal_ok')=='satisfied'
    assert status(baseline,'plant_ledger','balances_ok')=='satisfied'
    assert value(baseline,'plant_ledger','net_electric')>0
    assert status(by['nominal-source-assumed'],'plant_ledger','heat_removal_ok')=='violated'
    assert status(by['literal-Lyon-source-input'],'plant_ledger','heat_removal_ok')=='violated'
    assert status(by['literal-Raffray-accounting'],'plant_ledger','balances_ok')=='violated'
    close(value(by['literal-Raffray-accounting'],'plant_ledger','comparison_blanket_deposition_difference'),-1.)
    for owner in ('he_capacity','pbli_capacity','divertor_capacity','compressor_capacity','turbine_capacity','rejection_capacity','generator_capacity','fuel_capacity'):
        low,high=by[owner+'_low'],by[owner+'_high']
        assert status(low,owner,'capacity_ok')=='violated'
        assert status(high,owner,'capacity_ok')=='satisfied'
        assert value(low,'plant_ledger','net_electric')==value(high,'plant_ledger','net_electric')==value(baseline,'plant_ledger','net_electric')
        # Only the named rating changes; all demand-producing inputs remain fixed.
        assert {k:v for k,v in low['effective_inputs'].items() if k!=P+owner+'__selected_rating'}=={k:v for k,v in baseline['effective_inputs'].items() if k!=P+owner+'__selected_rating'}
    for name,multiplier in [('density_lower',.95),('density_higher',1.05)]:
        row=by[name]
        assert math.isclose(value(row,'source','selected_power'),value(baseline,'source','selected_power')*multiplier**2,rel_tol=3e-14)
        assert math.isclose(value(row,'fuel','exhaust_rate'),value(baseline,'fuel','exhaust_rate')*multiplier**2,rel_tol=3e-14)
        assert {k:v for k,v in row['effective_inputs'].items() if k!=PLASMA+'amplitude'}=={k:v for k,v in baseline['effective_inputs'].items() if k!=PLASMA+'amplitude'}
    assert value(by['density_lower'],'plant_ledger','net_electric')<value(baseline,'plant_ledger','net_electric')<value(by['density_higher'],'plant_ledger','net_electric')
    assert value(by['low_he_ua'],'heat_exchangers','unmet_heat')>0
    assert value(by['bypass_motor'],'recuperator','bypass_active')==1
    assert value(by['bypass_motor'],'generator_auxiliaries','shaft_import')>0
    assert value(by['bypass_motor'],'plant_ledger','net_electric')<0
    assert value(by['unsupported_capacity'],'he_capacity','evaluation_defined')==0
    assert status(by['unsupported_capacity'],'he_capacity','capacity_ok')=='violated'
    for name in ('zero_he_ua','low_he_hot_bound'):
        assert value(by[name],'heat_exchangers','he_state_defined')==0
    # Probe generic ledger's zero-heat denominator handling using actual resolved inputs.
    import yaml
    from aries_integrated.modules.integrated_heat_electricity.integrated_plant_ledger import Integrated_Plant_LedgerInput
    from aries_integrated.schemas.integrated_plant_ledger_output import Integrated_Plant_LedgerOutput
    from aries_integrated.handwritten.integrated_heat_electricity.integrated_plant_ledger_impl import run_integrated_plant_ledger
    pipe=yaml.safe_load((HERE/'aries_integrated/pipelines/pipeline.yaml').read_text())
    resolved={}
    for key,entry in pipe['modules'][P+'plant_ledger__evaluate']['inputs'].items():
        channel=entry.split(' ',1)[1].removesuffix('.root')
        resolved[key]=baseline['effective_inputs'][channel.split('.',1)[1]] if '.' in channel else baseline['outputs'][channel]
    resolved['accepted_heat_in']=0.
    outputs=dict(zip(Integrated_Plant_LedgerOutput.model_fields,run_integrated_plant_ledger(Integrated_Plant_LedgerInput(**resolved))))
    assert outputs['efficiency_defined']==0 and outputs['thermal_efficiency']==0
    assert outputs['residual_magnitude']>outputs['energy_tolerance']
    check_equipment(by)
    summary=dict(passed=True,case_count=len(rows),evaluated=sum(r['status']=='evaluated' for r in rows),
                 refused=sum(r['status']=='refused' for r in rows),fingerprint=runtime[2],
                 zero_heat_ledger='undefined efficiency and nonclosing energy reported; not a valid operating point',cases=rows)
    (EVIDENCE/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='cases'}))


def equipment_cases(base):
    result = [
        ('u_low',{**base,P+'he_hx__assumed_u':500.},None),
        ('u_high',{**base,P+'he_hx__assumed_u':1500.},None),
        ('area_low',{**base,P+'he_hx__selected_area':5000.},None),
        ('area_high',{**base,P+'he_hx__selected_area':75000.},None),
        ('stock_low',{**base,P+'fuel_inventory__selected_tritium_kg':.01},None),
        ('stock_high',{**base,P+'fuel_inventory__selected_tritium_kg':1.},None),
        ('source_parent_change',{**base,P+'source_budget__account_3':1548817000.},None),
        ('stock_double',{**base,P+'fuel_inventory__selected_tritium_kg':20.},None),
        ('recovery_supplied',{**base,P+'fuel_inventory__annual_recovery_kg':100.},None),
        ('source_budget_mode',{**base,P+'cost_accounts__estimate_mode':1.},None),
        ('fixed_budget_area',{**base,P+'cost_accounts__estimate_mode':1.,P+'he_hx__selected_area':75000.},None),
        ('magnet_price',{**base,P+'magnet_inventory__price_factor':1.5},None),
        ('schedule_at',{**base,P+'cost_schedule__plant_years':10.,P+'cost_schedule__availability':1.,P+'cost_schedule__replacement_life_fpy':5.},None),
        ('schedule_before',{**base,P+'cost_schedule__plant_years':9.999,P+'cost_schedule__availability':1.,P+'cost_schedule__replacement_life_fpy':5.},None),
        ('schedule_after',{**base,P+'cost_schedule__plant_years':10.001,P+'cost_schedule__availability':1.,P+'cost_schedule__replacement_life_fpy':5.},None),
        ('invalid_schedule',{**base,P+'cost_schedule__replacement_life_fpy':0.},'replacement'),
        ('invalid_stock',{**base,P+'fuel_inventory__selected_tritium_kg':-1.},'nonnegative'),
    ]
    for b,m in [('he',3261.),('pbli',26860.),('divertor',500.)]:
        for label,factor in [('low',.5),('high',1.5)]:
            result.append((b+'_pump_capacity_'+label,{**base,P+b+'_pump__selected_flow_capacity':m*factor},None))
        result.append((b+'_flow_low',{**base,P+'heat_exchangers__'+b+'_flow':m*.5},None))
    return result


def check_equipment(by):
    base=by['nominal-calculated']; f=lambda r,o,k,c='evaluate':r['outputs'][P+o+'__'+c+'__'+k]
    manifest=json.loads((EVIDENCE/'account-manifest.json').read_text())
    def cost(r,entry):return f(r,entry['owner'],entry.get('cost_output','capital'),'purchase')
    total=sum(cost(base,e) for e in manifest)+f(base,'fuel_inventory','amount','purchase')
    close(total,f(base,'cost_ledger','direct'),.01)
    close(f(base,'cost_ledger','source_direct'),2619572000.,.01)
    close(f(base,'cost_ledger','source_inclusive'),2619572000.*1.93,.01)
    close(f(base,'cost_ledger','direct_difference'),300031000.,.01)
    close(f(base,'cost_ledger','overnight'),total*1.49,.01)
    for name in ['density_lower','density_higher']:
        for e in manifest:assert cost(by[name],e)==cost(base,e),(name,e['owner'])
        assert f(by[name],'fuel_inventory','annual_burn','annual')!=f(base,'fuel_inventory','annual_burn','annual')
    for name in ['u_low','u_high']:
        assert f(by[name],'he_hx','capital','purchase')==f(base,'he_hx','capital','purchase')
        assert f(by[name],'he_hx','ua')!=f(base,'he_hx','ua')
    for name,mult in [('area_low',.1),('area_high',1.5)]:
        close(f(by[name],'he_hx','capital','purchase'),f(base,'he_hx','capital','purchase')*mult,.01)
        close(f(by[name],'he_hx','ua'),50*mult)
    assert status(by['area_low'],'plant_ledger','heat_removal_ok')=='violated'
    assert status(by['area_high'],'plant_ledger','heat_removal_ok')=='satisfied'
    assert f(by['fixed_budget_area'],'he_hx','capital','purchase')==f(base,'he_hx','capital','purchase')
    for owner in ['he','pbli','divertor']:
        lo=by[owner+'_pump_capacity_low'];hi=by[owner+'_pump_capacity_high']
        assert status(lo,owner+'_pump','capacity_ok')=='violated'
        assert status(hi,owner+'_pump','capacity_ok')=='satisfied'
        assert f(lo,owner+'_pump','electric')==f(hi,owner+'_pump','electric')==f(base,owner+'_pump','electric')
        close(f(hi,owner+'_pump','capital','purchase')/f(lo,owner+'_pump','capital','purchase'),3.)
        flow=by[owner+'_flow_low']
        close(f(flow,owner+'_pump','electric'),f(base,owner+'_pump','electric')/8.)
        assert f(flow,owner+'_pump','capital','purchase')==f(base,owner+'_pump','capital','purchase')
    rated={'he':'he_duty_equipment','pbli':'pbli_duty_equipment','divertor':'divertor_duty_equipment','compressor':'compressor_equipment','turbine':'turbine_equipment','generator':'generator_equipment','rejection':'heat_rejection_equipment','fuel':'fuel_processing_equipment'}
    for rating,owner in rated.items():assert f(by[rating+'_capacity_high'],owner,'capital','purchase')>f(by[rating+'_capacity_low'],owner,'capital','purchase')
    assert status(by['stock_low'],'fuel_inventory','capacity_ok')=='violated'
    assert status(by['stock_high'],'fuel_inventory','capacity_ok')=='satisfied'
    assert f(by['stock_low'],'fuel_inventory','required_stock','annual')==f(by['stock_high'],'fuel_inventory','required_stock','annual')
    close(f(base,'source_reconciliation','difference','fuel_gap_calc'),1000.,.01)
    close(f(base,'inventory_comparison','difference'),1333700.,.01)
    close(f(base,'lipb_comparison','difference'),8830000.*17.1-151327000.,.01)
    close(f(base,'source_replacement_comparison','amount','cost'),975000000.,.01)
    close(f(base,'source_replacement_comparison','amount','mass'),10946000.,.01)
    close(f(base,'source_replacement_comparison','difference'),9000000.,.01)
    close(f(by['source_parent_change'],'cost_ledger','source_reactor_gap')-f(base,'cost_ledger','source_reactor_gap'),10000000.,.01)
    assert f(by['source_parent_change'],'cost_ledger','direct')==f(base,'cost_ledger','direct')
    stock=by['stock_double']
    close(f(stock,'fuel_inventory','annual_decay','annual'),2*f(base,'fuel_inventory','annual_decay','annual'))
    close(f(stock,'fuel_inventory','amount','purchase'),2*f(base,'fuel_inventory','amount','purchase'),.01)
    ins=base['effective_inputs'];delta=ins[P+'fuel__decay_constant_s']*(10/ins[P+'fuel__tritium_atom_kg'])/(ins[P+'fuel__assumed_extraction']*f(base,'fuel','burn_rate'))
    close(f(stock,'fuel','tbr_required')-f(base,'fuel','tbr_required'),delta,1e-12)
    for key in ['burn_rate','exhaust_rate','loss_rate']:assert f(stock,'fuel',key)==f(base,'fuel',key)
    assert f(stock,'plant_ledger','net_electric')==f(base,'plant_ledger','net_electric')
    assert f(stock,'fuel_inventory','breeding_supported','annual')==0
    assert f(by['recovery_supplied'],'fuel_inventory','annual_external','annual')<f(base,'fuel_inventory','annual_external','annual')
    for n,count in [('schedule_before',1),('schedule_at',1),('schedule_after',2)]:
        assert f(by[n],'replacement','event_count')==count
        assert f(by[n],'replacement','first_event_year')==5
    assert f(base,'replacement','event_count')==6
    expected=f(base,'blanket_inventory','capital','purchase')+f(base,'divertor_inventory','cost','purchase')+.05*f(base,'lipb_inventory','capital','purchase')
    close(f(base,'replacement','event_cost'),expected,.01)
    imported=by['bypass_motor']
    assert f(imported,'plant_ledger','net_electric')<0
    close(f(imported,'cost_ledger','annual_import_mwh'),-f(imported,'plant_ledger','net_electric')*8760*.85,.0001)
    close(f(imported,'cost_ledger','annual_import_cost'),f(imported,'cost_ledger','annual_import_mwh')*50.,.01)
    assert f(imported,'cost_ledger','annual_export_mwh')==0
    assert f(by['magnet_price'],'plant_ledger','net_electric')==f(base,'plant_ledger','net_electric')
    close(f(by['magnet_price'],'magnet_inventory','capital','purchase'),1.5*f(base,'magnet_inventory','capital','purchase'),.01)


if __name__=='__main__':main()
