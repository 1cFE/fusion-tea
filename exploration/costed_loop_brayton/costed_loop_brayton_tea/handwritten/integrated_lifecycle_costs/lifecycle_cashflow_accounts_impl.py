"""Reviewed WI-091 real cashflow accounts; production native completion, not oracle.
Source: models/library/analyses/integrated_lifecycle_costs.sysml.
Ref: work/active/WI-091_aries-integrated-lifecycle-cost/design.md.
"""
import math
from costed_loop_brayton_tea.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def _reviewed_run_lifecycle_cashflow_accounts(inputs):
    v=values(inputs)
    r=v['discount']; n=v['plant_years']; crf=v['crf']; energy=v['annual_energy']
    require(0 <= r <= 1, 'financial discount must be real in [0,1]')
    require(n>0 and n.is_integer(), 'financial life must be positive integer calendar years')
    require(v['construction_years']>=0 and 0<v['availability']<=1, 'invalid financial construction/availability')
    require(v['net_power']>0 and energy>0, 'LCOE undefined for nonpositive net electricity')
    require(all(v[k]>=0 for k in v if k not in ('net_power',)), 'financial accounts must be nonnegative inputs')
    require(crf>0 and math.isclose(crf,1/n if r==0 else r/-math.expm1(-n*math.log1p(r)),rel_tol=1e-12), 'inconsistent capital recovery factor')
    require(math.isclose(energy,8760*v['net_power']*v['availability'],rel_tol=1e-12), 'inconsistent annual net electricity')
    operating=sum(v[k] for k in ('om','tritium','deuterium','consumables','imports'))
    require(math.isclose(v['annual_operating'],operating,rel_tol=1e-12,abs_tol=1e-7), 'annual accounts do not reconcile')
    tau=v['interval_years']; count=v['event_count']
    require(tau>0 and count.is_integer() and 0<=count<1000000, 'invalid replacement interval/count')
    require(count==max(0,math.ceil(n/tau)-1), 'replacement count inconsistent with horizon')
    require(v['other_overhaul_year']>0, 'other overhaul year must be positive')
    weight=lambda t: math.exp(-t*math.log1p(r))
    capital=v['overnight']; financed=capital/weight(v['construction_years']/2)
    pv_rep=math.fsum(v['event_cost']*weight(k*tau) for k in range(1,int(count)+1))
    occurs=float(v['other_overhaul_year']<n)
    other=capital*v['other_overhaul_fraction']*occurs
    pv_other=other*weight(v['other_overhaul_year'])
    gross=capital*v['terminal_fraction']; salvage=capital*v['salvage_fraction']
    pv_gross=gross*weight(n); pv_salvage=salvage*weight(n)
    pv_operating=operating/crf; pv_supply=v['supply_service']/crf
    pv_energy=energy/crf
    noncapital=operating+v['supply_service']+crf*(pv_rep+pv_other+pv_gross-pv_salvage)
    total=financed+pv_operating+pv_supply+pv_rep+pv_other+pv_gross-pv_salvage
    makeup=sum(v[k] for k in ('annual_burn','annual_loss','annual_decay'))
    shortfall=max(makeup-v['annual_feed'],0.)
    require(math.isclose(v['external_shortfall'],shortfall,rel_tol=1e-12,abs_tol=1e-12),'fuel feed boundary does not reconcile')
    result=dict(noncapital_annual=noncapital,financed_capital=financed,idc=financed-capital,annual_capital=financed*crf,
        annual_energy=energy,lifetime_energy=energy*n,pv_energy=pv_energy,pv_operating=pv_operating,pv_supply=pv_supply,
        pv_replacement=pv_rep,pv_other_overhaul=pv_other,gross_terminal=gross,salvage=salvage,pv_terminal_gross=pv_gross,
        pv_salvage=pv_salvage,pv_terminal_net=pv_gross-pv_salvage,other_overhaul_cost=other,other_overhaul_occurs=occurs,
        pv_total_cost=total,lcoe_sum=total/pv_energy,capital_lcoe=financed/pv_energy,
        supply_lcoe=v['supply_service']/energy,replacement_lcoe=pv_rep/pv_energy,other_overhaul_lcoe=pv_other/pv_energy,
        terminal_lcoe=pv_gross/pv_energy,salvage_lcoe=-pv_salvage/pv_energy,gross_makeup=makeup,new_feed=v['annual_feed'],
        external_shortfall=shortfall,curtailed_feed=max(v['annual_feed']-makeup,0.),supply_supported=0.,breeding_supported=0.,
        financial_defined=1.,currency_year=2004.,real_convention=1.)
    for key in ('om','tritium','deuterium','consumables','imports'):
        result[key+'_lcoe']=v[key]/energy
    return finish('lifecycle_cashflow_accounts',result)


from costed_loop_brayton_tea.modules.integrated_lifecycle_costs.lifecycle_cashflow_accounts import Lifecycle_Cashflow_AccountsInput


def run_lifecycle_cashflow_accounts(inputs: Lifecycle_Cashflow_AccountsInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_lifecycle_cashflow_accounts(inputs)
