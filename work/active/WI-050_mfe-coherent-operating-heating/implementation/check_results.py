"""Independent conservation and unchanged financial-formula acceptance checks."""
import json
import math
from pathlib import Path
P='stellarator_09__stellaris__'

def equal(a,b):
    assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-9),(a,b)

def finance(o,i):
    get=lambda key:o[P+key]
    d,N,Yc,g=(i[P+k] for k in ['discount_rate','operational_years','construction_years','inflation_rate'])
    crf=d/(1-(1+d)**(-N))
    overnight=get('total_capital__total_capital')
    idc=overnight*(((1+d)**Yc-1)/(d*Yc)-1)
    headline=overnight*(1+d)**(Yc/2)*crf
    comparison=(overnight+idc)*crf
    energy=8760*get('pb__p_net')*get('calendar__availability')
    annual=get('cas71_calc__levelized')+get('calendar__cas72_annual')+get('cas80_calc__levelized')
    return dict(crf=crf,idc=idc,headline=headline,comparison=comparison,energy=energy,annual=annual,
                headline_lcoe=(headline+annual)/energy,
                comparison_lcoe=(comparison+annual)/(energy*i[P+'n_mod']))

def check_case(o,i):
    get=lambda key:o[P+key]
    val=lambda key:i[P+key]
    d=get('sustain__p_aux_required');se=val('eta_source_heat');ce=val('eta_couple_heat')
    equal(get('operating_heat__p_coupled'),d)
    equal(get('operating_heat__p_delivered'),d/ce)
    equal(get('operating_heat__p_wallplug'),d/(se*ce))
    fusion=get('fusion__p_fus');alpha=fusion*3.52/17.58
    q=val('mn')*(fusion-alpha)+alpha+d
    equal(get('source_heat__q_source'),q)
    mdot=q*1e6/(val('loop_cp')*val('loop_dT_blanket'))
    perloop=mdot/val('n_loops');dp=val('f_loss')*val('dp_loop_ref')*(perloop/val('mdot_loop_ref'))**2
    ratio=val('loop_p')/(val('loop_p')-dp)
    tin=val('loop_T_in')/(1+(ratio**((val('loop_gamma')-1)/val('loop_gamma'))-1)/val('eta_is'))
    work=mdot*val('loop_cp')*(val('loop_T_in')-tin)/1e6
    recovered=val('loop_live')*work+val('eta_p_direct')*val('p_pump_direct')
    pump=val('loop_live')*work/val('eta_drive')+val('p_pump_direct')
    for key,expected in {'mdot':mdot,'mdot_loop':perloop,'dp_loop':dp,'T_comp_in':tin,'w_fluid':work,'p_pump_total':pump,'q_recovered_total':recovered,'q_ihx':q+work}.items():
        equal(get('primary_loop__'+key),expected)
    thermal=q+recovered;gross=thermal*get('cycle__eta_th')
    loads=sum(val(k) for k in ['p_tf','p_pf','p_tfcool','p_pfcool','p_trit','p_house'])+val('f_sub')*gross+get('cryo_elec__p_elec')+pump+d/(se*ce)
    equal(get('pb__p_th'),thermal);equal(get('pb__p_et'),gross);equal(get('pb__p_net'),gross-loads)
    absorbed=get('sustain__p_alpha_heat')+d
    equal(get('divheat__p_heat_abs'),absorbed)
    equal(get('divheat__p_target_nonrad'),absorbed*(1-val('f_rad_total')))
    equal(get('divheat__q_target_peak'),absorbed*(1-val('f_rad_total'))*val('q_target_ref')/val('p_nonrad_ref'))
    equal(get('divheat__p_heat_operating_minus_installed'),d-get('heat__p_coupled'))
    f=finance(o,i)
    equal(get('lcoe_calc__lcoe'),f['headline_lcoe']);equal(get('lcoe_1cfe_calc__lcoe'),f['comparison_lcoe'])
    equal(get('cas90_1cfe_calc__cas90'),f['comparison'])
    equal(get('cas71_calc__crf'),f['crf'])
    d,N,Yc,g=(val(k) for k in ['discount_rate','operational_years','construction_years','inflation_rate'])
    for leaf,raw in [('cas71_calc__levelized','om_cost__annual_om'),('cas80_calc__levelized','fuel_calc__annual_fuel')]:
        expected=f['crf']*get(raw)*(1+g)**Yc*(1-((1+g)/(1+d))**N)/(d-g)
        equal(get(leaf),expected)
    event=(get('blanket_cost__cost')+get('divertor_cost__cost'))*val('n_mod')
    equal(get('replacement_cost_per_event__replacement_cost_per_event'),event)
    life=val('fluence_limit')/get('wall_peak_calc__wall_load_peak')
    b=1-val('unplanned_fraction');outage=val('outage_years')
    dates=[];k=1
    while k*life/b+(k-1)*outage+outage<N:
        dates.append(k*life/b+(k-1)*outage);k+=1
    pv=event*sum((1+d)**(-t) for t in dates)
    equal(get('calendar__replacement_pv'),pv)
    equal(get('calendar__cas72_annual'),pv*f['crf'])
    assert len(dates)==get('calendar__n_replacements')
    equal(get('calendar__productive_fpy'),get('calendar__availability')*N)
    equal(sum(get('calendar__'+k) for k in ['productive_fpy','planned_downtime_yr','terminal_downtime_yr','unplanned_downtime_yr']),N)
    return f

def check(results,inputs):
    controls={'baseline':{},'reserve':{'p_wallplug_heat':120},'demand':{'f_alpha_fast':.96},'efficiency':{'eta_couple_heat':.8},'availability':{'unplanned_fraction':.10}}
    financial={}
    for case,changes in controls.items():
        financial[case]=check_case(results[case]['outputs'],dict(inputs,**{P+k:v for k,v in changes.items()}))
    b=results['baseline']['outputs'];r=results['reserve']['outputs']
    invariants=['operating_heat__','source_heat__','primary_loop__','pb__','calendar__','cas71_calc__','cas80_calc__']
    for key,value in b.items():
        if any(key.removeprefix(P).startswith(prefix) for prefix in invariants) or (key.startswith(P+'divheat__') and not key.endswith('p_heat_operating_minus_installed')):
            assert value==r[key],key
    assert b[P+'heating_cost__cost']==264145000
    assert r[P+'heating_cost__cost']==316974000
    assert results['demand']['outputs'][P+'heating_cost__cost']==264145000
    assert results['demand']['outputs'][P+'divheat__p_heat_abs']==b[P+'divheat__p_heat_abs']
    assert results['demand']['outputs'][P+'fusion__p_fus']==b[P+'fusion__p_fus']
    for k in ['operating_heat__p_coupled','operating_heat__p_wallplug','pb__p_net']:
        assert b[P+k]==results['availability']['outputs'][P+k]
    for case in controls:
        responses=results[case]['responses'];individual={k:v for k,v in responses.items() if k!='headline'}
        assert len(individual)==18
        violated=[k for k,v in individual.items() if v=='violated']
        assert len(violated)==(2 if case=='efficiency' else 1)
        assert any('divertor_heat_ok' in k for k in violated)
    assert results['zero_efficiency']['error']=='EvaluationFailed'
    return financial

if __name__=='__main__':
    h=Path(__file__).resolve().parent
    r=json.loads((h/'results.json').read_text());i=json.loads((h/'inputs.json').read_text())
    f=check(r,i)
    old=json.loads(Path('work/analysis/20260911-190758_mfe-operating-state-evidence/baseline/all_outputs.json').read_text())
    b=r['baseline']['outputs'];oldfin=finance(old,i);newfin=f['baseline']
    bridges={}
    for form,output in [('headline','lcoe_calc__lcoe'),('comparison','lcoe_1cfe_calc__lcoe')]:
        equal(old[P+output],oldfin[form+'_lcoe'])
        capital=(newfin[form]-oldfin[form])/oldfin['energy']
        annual=(newfin['annual']-oldfin['annual'])/oldfin['energy']
        energy=(newfin[form]+newfin['annual'])*(1/newfin['energy']-1/oldfin['energy'])
        delta=b[P+output]-old[P+output];equal(capital+annual+energy,delta)
        bridges[form]=dict(capital=capital,annual=annual,energy=energy,delta=delta,residual=delta-capital-annual-energy)
    compared={k.removeprefix(P):{'before':v,'after':b[k],'delta':b[k]-v} for k,v in old.items() if k in b and isinstance(v,(int,float)) and isinstance(b[k],(int,float))}
    report={'independent_finance':f,'financial_bridge':bridges,'all_compared_scalars':compared,'new_channels':{k:v for k,v in b.items() if k not in old},'changed_count':sum(v['delta']!=0 for v in compared.values())}
    (h/'baseline-attribution.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS independent conservation, loop, finance, calendar and both LCOE attribution; changed scalars',report['changed_count'])
