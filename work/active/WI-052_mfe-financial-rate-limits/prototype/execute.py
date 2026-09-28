from pathlib import Path
from decimal import Decimal as D, localcontext
import json
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge

root=Path(__file__).resolve().parent
ev=PreparedEvaluator(ProvisionalPackageLoader(root/'generated','wi052_probe',root/'link'),root/'generated/pipelines/pipeline.yaml',expects_constraint_report=True)
bridge=CandidateBridge(ev.entry_models)
prefix='stellarator_09__stellaris__'
rows=[]
for mode in (0.,.85):
    for rate in (0.,.02,.08,1e-18,-1e-18):
        result=ev.evaluate(bridge.build({prefix+'availability_direct':mode,prefix+'discount_rate':rate,prefix+'inflation_rate':rate}))
        rows.append(dict(mode=mode,rate=rate,outputs=dict(result.outputs)))
from wi052_probe.modules.mfe_account_costs.levelized_annual_cost import Levelized_Annual_CostModule
from wi052_probe.modules.mfe_account_costs.idc_closed_form_cost import IDC_Closed_Form_CostModule
from wi052_probe.modules.mfe_lcoe_dcf.lcoe_dcf import LCOE_DCFModule
from wi052_probe.modules.mfe_lifecycle.lifecycle_calendar import Lifecycle_CalendarModule
with localcontext() as ctx:
    ctx.prec=90
    i=D(.02); n=D(30); t=D(8)
    expected=D('1e6')*(1+i)**t*n/(1+i)*i/(1-(1+i)**(-n))
    out=Levelized_Annual_CostModule().run(annual_cost=1e6,interest_rate=.02,inflation_rate_in=.02,operational_years_in=30.,project_time=8.).data
    assert abs(D(out.levelized)-expected)/abs(expected)<D('1e-9')
    dcf=LCOE_DCFModule().run(discount_rate_in=0.,availability_in=.85,construction_years_in=8.,net_electric_mw=1000.,annual_om_in=1e7,operational_years_in=30.,total_capital_in=1e9).data.root
    expected=(D('1e9')/30+D('1e7'))/(D(8760)*1000*D(.85))
    assert abs(D(dcf)-expected)/abs(expected)<D('1e-9')
    cost=IDC_Closed_Form_CostModule().run(overnight_cost=1e9,interest_rate=0.,construction_years_in=8.).data.root
    assert cost==0.
    calendar_cases=0
    for mode in (0.,.85):
        for q in (0.,1.,10.):
            for horizon in (30.,30.5):
                previous=None
                for rate in (0.,.08,1e-8,-1e-8,1e-18,-1e-18):
                    inputs=dict(interest_rate=rate,q_n_in=q,operational_years_in=horizon,outage_years_in=.5,fluence_limit_in=5.,unplanned_fraction_in=.1,cost_per_event=1e6,availability_direct_in=mode,coil_life_fpy_in=100.)
                    output=Lifecycle_CalendarModule().run(**inputs).data.model_dump()
                    # Independently reconstruct event dates with Decimal operations.
                    N=D(horizon)
                    if mode:
                        life=min(max(D(5)/max(D(q),D(1e-6)),D(.5)),N*D(mode))
                        interval=life/D(mode)
                        import math
                        dates=[D(k)*interval for k in range(1,max(0,math.ceil(N/interval)-1)+1)]
                    else:
                        interval=None if not q else D(5)/D(q)/(1-D(.1))
                        dates=[]; time=D(0)
                        while interval is not None and time+interval+D(.5)<N:
                            time+=interval; dates.append(time); time+=D(.5)
                    pv=sum((D('1e6')/(1+D(rate))**date for date in dates),D(0))
                    c=1/N if not rate else D(rate)/(1-(1+D(rate))**(-N))
                    for key,expected in [('replacement_pv',pv),('cas72_annual',pv*c)]:
                        error=abs(D(output[key])-expected)/abs(expected) if expected else abs(D(output[key]))
                        assert error<D('1e-9'),(inputs,key,error)
                    physical={k:v for k,v in output.items() if k not in ('replacement_pv','cas72_annual','dated_energy_ratio')}
                    if previous is not None:
                        assert physical==previous
                    previous=physical; calendar_cases+=1
(root/'execution.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS 10 sealed native evaluations in live/held modes; direct public annuity, DCF and IDC counterexamples;',calendar_cases,'public calendar checks against independently dated sums and unchanged physical fields')
