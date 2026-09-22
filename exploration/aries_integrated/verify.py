"""Native MR-7, conservation, adverse-state and domain evidence for WI-089.

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
              ('negative_ua',{P+'heat_exchangers__he_ua':-1.},'nonnegative'),
              ('negative_flow',{P+'cycle__selected_flow':-1.},'positive'),
              ('invalid_recuperator',{P+'cycle__recuperator_effectiveness':1.1},'[0,1]'),
              ('invalid_heating_efficiency',{P+'generator_auxiliaries__heating_efficiency':0.},'(0,1]'),
              ('invalid_plasma_temperature',{PLASMA+'temperature_edge':.023},'domain')]
    for owner in ('he_capacity','pbli_capacity','divertor_capacity','compressor_capacity','turbine_capacity','rejection_capacity','generator_capacity','fuel_capacity'):
        cases += [(owner+'_low',{**base,P+owner+'__selected_rating':1e20 if owner=='fuel_capacity' else 1.},None),
                  (owner+'_high',{**base,P+owner+'__selected_rating':1e24 if owner=='fuel_capacity' else 10000.},None)]
    # Explicit native nonfinite test is retained as a refusal, never a study point.
    cases += [('nonfinite_ua',{P+'heat_exchangers__he_ua':float('nan')},'finite')]
    for name,changes,error in cases:
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
    summary=dict(passed=True,case_count=len(rows),evaluated=sum(r['status']=='evaluated' for r in rows),
                 refused=sum(r['status']=='refused' for r in rows),fingerprint=runtime[2],
                 zero_heat_ledger='undefined efficiency and nonclosing energy reported; not a valid operating point',cases=rows)
    (EVIDENCE/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='cases'}))


if __name__=='__main__':main()
