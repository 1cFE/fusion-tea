"""WI-096 disjoint electrical/thermal and common-year conditional DCF ledger.

Finite replacement dates strictly before horizon; source and upstream excluded.
Unknown scope corrections remain public costs, with a separate comparison frontier.
"""
import math
AUTO_IMPLEMENTED=False
INPUTS=dict(available_heat=0.,actual_heat=0.,gross=0.,shaft_import=0.,steam_pumps=0.,salt_pumps=0.,water1=0.,water2=0.,water3=0.,water4=0.,controller_electric=.1,
 rejected1=0.,rejected2=0.,rejected3=0.,rejected4=0.,capital1=0.,capital2=0.,capital3=0.,capital4=0.,capital5=0.,capital6=0.,capital7=0.,capital8=0.,capital9=0.,capital10=0.,currency_factor=1.,controller_capital=1e7,
 separately_replaced_capital=0.,salt_vendor=0.,salt_installation=0.,salt_removal=0.,bundle_event=0.,salt_stock_cost=0.,machine_life=10.,bundle_life=15.,makeup_fraction=.001,
 annual_service_fraction=.02,replacement_fraction=.2,replacement_year=15.,rate=.05,years=30.,availability=.85,scope_correction=0.,common_source_pv=0.)
OUTPUTS='gross_electric electrical_load net_electric total_rejected unremoved_heat energy_residual conversion_energy_residual conversion_energy_residual_magnitude capital_total recurring_base annual_service annual_makeup machine_replacement_pv bundle_replacement_pv conversion_replacement_pv replacement_pv annuity_factor annual_energy discounted_energy accounted_pv corrected_pv cost_per_net_MWh economic_defined energy_tolerance'.split()+['capital_'+str(i) for i in range(1,11)]
def calculate(x):
    if any(not math.isfinite(v) for v in x.values()):raise ValueError('nonfinite ledger input')
    if x['rate']<0 or x['years']<=0 or not 0<x['availability']<=1 or min(x['machine_life'],x['bundle_life'])<=0:
        raise ValueError('ledger finance domain')
    capital={f'capital_{i}':x[f'capital{i}']*x['currency_factor'] for i in range(1,11)}
    cap=math.fsum(capital.values())+x['controller_capital']
    # Exclude purchased salt stock and the initial machine/bundle capital already
    # replaced separately. Salt pipe/shell/spare scope remains in the allowance.
    recurring=cap-capital['capital_2']-x['separately_replaced_capital']
    service=recurring*x['annual_service_fraction'];makeup=x['salt_stock_cost']*x['makeup_fraction']
    r=x['rate'];n=x['years'];ann=n if r==0 else -math.expm1(-n*math.log1p(r))/r
    def events(amount,life):
        return math.fsum(amount*math.exp(-k*life*math.log1p(r)) for k in range(1,math.ceil(n/life)) if k*life<n)
    machine=events(x['salt_vendor']+x['salt_installation']+x['salt_removal'],x['machine_life'])
    bundle=events(x['bundle_event'],x['bundle_life'])
    replacement=recurring*x['replacement_fraction']*math.exp(-x['replacement_year']*math.log1p(r)) if 0<x['replacement_year']<n else 0.
    rp=machine+bundle+replacement
    loads=math.fsum(x[k] for k in ('shaft_import','steam_pumps','salt_pumps','water1','water2','water3','water4','controller_electric'))
    net=x['gross']-loads;rejected=math.fsum(x[f'rejected{i}'] for i in range(1,5))
    annual=8760*net*x['availability'];energy=annual*ann
    accounted=cap+rp+(service+makeup)*ann;corrected=accounted+x['scope_correction']+x['common_source_pv']
    price=0.
    if net>0:
        from types import SimpleNamespace
        from whole_plant_conversion_tea.handwritten.mfe_lcoe_dcf.lcoe_dcf_impl import run_lcoe_dcf
        price=run_lcoe_dcf(SimpleNamespace(total_capital_in=cap+rp+x['scope_correction']+x['common_source_pv'],annual_om_in=service+makeup,net_electric_mw=net,availability_in=x['availability'],discount_rate_in=r,construction_years_in=0.,operational_years_in=n))
    return dict(energy_tolerance=max(1e-6,1e-9*abs(x['available_heat'])),gross_electric=x['gross'],electrical_load=loads,net_electric=net,total_rejected=rejected,
      unremoved_heat=x['available_heat']-x['actual_heat'],energy_residual=x['available_heat']-net-rejected,
      conversion_energy_residual=x['actual_heat']-net-rejected,conversion_energy_residual_magnitude=abs(x['actual_heat']-net-rejected),capital_total=cap,recurring_base=recurring,
      annual_service=service,annual_makeup=makeup,machine_replacement_pv=machine,bundle_replacement_pv=bundle,
      conversion_replacement_pv=replacement,replacement_pv=rp,annuity_factor=ann,annual_energy=annual,
      discounted_energy=energy,accounted_pv=accounted,corrected_pv=corrected,
      cost_per_net_MWh=price,economic_defined=float(net>0),**capital)
