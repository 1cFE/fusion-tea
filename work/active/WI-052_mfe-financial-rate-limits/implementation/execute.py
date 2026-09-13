"""SV-092 native attribution with independent factors and full scalar/edge ledger."""
import json
import math
import subprocess
from decimal import Decimal as D,localcontext
from pathlib import Path
import yaml
from reference_finance import crf,annuity_pv,idc,dcf_components,dated_pv
from capture import ROOT,HERE,logged
P='stellarator_09__stellaris__'
FINANCE={P+x for x in ('cas71_calc__crf','cas71_calc__levelized','cas80_calc__crf','cas80_calc__levelized','idc__cost','calendar__replacement_pv','calendar__cas72_annual','calendar__dated_energy_ratio','cas70_calc__cas70','cas70_calc__annual_total','cas90_1cfe_calc__cas90','lcoe_calc__lcoe','lcoe_1cfe_calc__lcoe')}

def check(actual,expected):
    with localcontext() as ctx:
        ctx.prec=100
        error=abs(D(actual)-expected)
        if expected:error/=abs(expected)
        assert error<=D('1e-9'),(actual,str(expected),str(error))
        return str(error)

def run():
    package=ROOT/'exploration/stellarator_e2e/generated'
    assert logged('candidate-native',['python',str(HERE/'native_probe.py'),str(package),str(HERE/'native-results.json')],HERE)==0
    old=json.loads((HERE/'entering/native.json').read_text());new=json.loads((HERE/'native-results.json').read_text())
    assert old['inputs']==new['inputs']
    modules=yaml.safe_load((package/'pipelines/pipeline.yaml').read_text())['modules']
    entering=yaml.safe_load((HERE/'entering/package/pipelines/pipeline.yaml').read_text())['modules']
    assert modules==entering,'Public graph or output order changed'
    producers={v.split()[-1]:name for name,m in modules.items() for v in m.get('outputs',{}).values()}
    consumers={key:[{'module':name,'formal':formal} for name,m in modules.items() for formal,v in m.get('inputs',{}).items() if v.split()[-1].removesuffix('.root')==key] for key in new['cases']['live_ordinary']['outputs']}
    ledger={};independent={}
    for name,row in new['cases'].items():
        assert 'error' not in row,(name,row)
        baseline=old['cases'][name.split('_')[0]+'_ordinary']
        assert row['responses']==baseline['responses'] and row['report']==baseline['report']
        assert list(row['outputs'])==list(baseline['outputs'])
        same=old['cases'][name]
        inputs=dict(new['inputs'],**row['overrides']);o=row['outputs']
        def arguments(module):
            values={}
            for formal,binding in modules[P+module]['inputs'].items():
                key=binding.split()[-1].removesuffix('.root')
                values[formal]=o[key] if key in o else inputs[key.split('.',1)[1]]
            return values
        refs={}
        with localcontext() as ctx:
            ctx.prec=100
            for module in ('cas71_calc','cas80_calc'):
                x=arguments(module);c=crf(x['interest_rate'],x['operational_years_in']);pv=annuity_pv(x['annual_cost'],x['interest_rate'],x['inflation_rate_in'],x['operational_years_in'],x['project_time'])
                refs[P+module+'__crf']=c;refs[P+module+'__levelized']=c*pv
                independent[name+'_'+module+'_internal_pv']=str(pv)
            from tests.models.test_mfe_financial_calendar import independent_schedule,energy_reference
            x=arguments('calendar');dates,segments,branch=independent_schedule(x)
            pv=dated_pv(x['cost_per_event'],x['interest_rate'],dates)
            refs[P+'calendar__replacement_pv']=pv
            refs[P+'calendar__cas72_annual']=pv*crf(x['interest_rate'],x['operational_years_in'])
            if x['availability_direct_in']:refs[P+'calendar__dated_energy_ratio']=D(1)
            else:
                num,den,ratio=energy_reference(segments,1-x['unplanned_fraction_in'],x['operational_years_in'],x['interest_rate'],o[P+'calendar__productive_fpy'])
                refs[P+'calendar__dated_energy_ratio']=ratio
                independent[name+'_calendar_energy']={'numerator':str(num),'denominator':str(den)}
            independent[name+'_calendar_dates']=dates
            x=arguments('idc');factor=idc(x['interest_rate'],x['construction_years_in']);refs[P+'idc__cost']=D(x['overnight_cost'])*factor
            independent[name+'_idc_factor']=str(factor)
            x=arguments('lcoe_calc');parts=dcf_components(x['total_capital_in'],x['annual_om_in'],x['discount_rate_in'],x['operational_years_in'],x['construction_years_in'],x['net_electric_mw'],x['availability_in'])
            refs[P+'lcoe_calc__lcoe']=parts['lcoe']
            independent[name+'_dcf_components']={k:str(v) for k,v in parts.items()}
            x=arguments('cas70_calc');refs[P+'cas70_calc__cas70']=D(x['cas71'])+D(x['cas72']);refs[P+'cas70_calc__annual_total']=D(x['cas71'])+D(x['cas72'])+D(x['cas80'])
            x=arguments('cas90_1cfe_calc');refs[P+'cas90_1cfe_calc__cas90']=D(x['crf'])*(D(x['overnight_cost'])+D(x['idc_cost']))
            x=arguments('lcoe_1cfe_calc');refs[P+'lcoe_1cfe_calc__lcoe']=(D(x['cas70'])+D(x['cas80'])+D(x['cas90']))/(D(8760)*D(x['n_mod_in'])*D(x['net_electric_mw'])*D(x['availability_in']))
        independent[name+'_references']={k:{'expected':str(v),'relative_or_zero_absolute_error':check(o[k],v)} for k,v in refs.items()}
        rows=[]
        for key,value in o.items():
            before=same.get('outputs',{}).get(key)
            financial=key in FINANCE
            if not financial:assert value==baseline['outputs'][key],(name,key,value,baseline['outputs'][key])
            if before is not None and financial:check(value,D(before))
            coverage='independent factor/charge' if key in refs else 'independent calendar reference (SV-091)' if key.startswith(P+'calendar__') and financial else 'exact entering physical/other'
            rows.append({'name':key,'entering':before,'candidate':value,'delta':None if before is None else value-before,'relative_delta':None if before in (None,0) else abs((value-before)/before),'producer':producers.get(key),'consumers':consumers[key],'classification':'changed finance' if financial and before!=value else 'unchanged physical/other','coverage':coverage,'entering_error':same.get('error')})
        ledger[name]=rows
    (HERE/'scalar-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
    (HERE/'independent-native.json').write_text(json.dumps(independent,indent=2)+'\n')
    print('PASS ten native cases, 158 named scalars each, exact physical/response/report preservation, unchanged graph and independent finance')
if __name__=='__main__':run()
