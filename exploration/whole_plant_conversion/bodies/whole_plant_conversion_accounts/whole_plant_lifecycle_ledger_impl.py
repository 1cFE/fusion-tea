"""End-year cashflows, exact finite replacement dates and initial finance only."""
import math
AUTO_IMPLEMENTED=False
INPUTS=dict(initial_capital=0.,salvage_base=0.,overhaul_base=0.,magnet_capital=0.,blanket_capital=0.,divertor_capital=0.,pbl_capital=0.,helium_capital=0.,wall_load=1.,annual_export_MWh=0.,annual_net_grid_MWh=0.,annual_import_cost=0.,annual_fuel=0.,conversion_annual_service=0.,conversion_annual_makeup=0.,conversion_replacement_pv=0.,rate=.05,years=30.,availability=.8,construction_years=8.,routine_om=50617243.276030459,routine_fraction=.8,wall_life=18.,magnet_life=10.,blanket_outage=7/12,magnet_outage=1.,other_outage=.5,blanket_removal_fraction=.1,magnet_removal_fraction=.1,pbl_refill_fraction=1.,primary_event=546492750.266880,primary_life=10.,helium_makeup_fraction=.001,overhaul_fraction=.05,overhaul_year=20.,dismantle_fraction=.1,salvage_fraction=.02)
OUTPUTS='initial_financed_capital annual_source_service annual_service annual_makeup annual_expense blanket_life_years magnet_life_years blanket_events magnet_events primary_events blanket_replacement_pv magnet_replacement_pv primary_replacement_pv overhaul_pv source_replacement_pv conversion_replacement_pv terminal_pv annual_expense_pv total_cost_pv energy_pv lcoe_USD2025_MWh outage_years outage_margin domain_supported economic_defined cost_residual'.split()
def calculate(x):
    n=x['years'];r=x['rate'];a=x['availability']
    if not(n>0 and n==int(n) and r>=0 and 0<a<=1 and min(x['wall_load'],x['wall_life'],x['magnet_life'],x['primary_life'])>0):raise ValueError('whole lifecycle domain: integer years and positive lives required')
    def events(life,amount):
        dates=[k*life for k in range(1,math.ceil(n/life)) if k*life<n]
        return len(dates),math.fsum(amount/(1+r)**t for t in dates)
    bl=x['wall_life']/x['wall_load']/a;ml=x['magnet_life']/a
    bc,bpv=events(bl,(x['blanket_capital']+x['divertor_capital'])*(1+x['blanket_removal_fraction'])+x['pbl_capital']*x['pbl_refill_fraction'])
    mc,mpv=events(ml,x['magnet_capital']*(1+x['magnet_removal_fraction']))
    pc,ppv=events(x['primary_life'],x['primary_event'])
    opv=x['overhaul_fraction']*x['overhaul_base']/(1+r)**x['overhaul_year'] if 0<x['overhaul_year']<n else 0.
    spv=bpv+mpv+ppv+opv;fin=x['initial_capital']*(1+r)**(x['construction_years']/2)
    service=x['routine_om']*x['routine_fraction'];makeup=x['helium_capital']*x['helium_makeup_fraction']+x['conversion_annual_makeup']
    annual=service+x['conversion_annual_service']+makeup+x['annual_fuel']+x['annual_import_cost']
    ann=math.fsum((1+r)**(-y) for y in range(1,int(n)+1));apv=annual*ann;epv=x['annual_export_MWh']*ann
    terminal=(x['dismantle_fraction']*x['initial_capital']-x['salvage_fraction']*x['salvage_base'])/(1+r)**n
    total=math.fsum([fin,spv,x['conversion_replacement_pv'],apv,terminal]);outage=bc*x['blanket_outage']+mc*x['magnet_outage']+x['other_outage']
    valid=epv>0 and x['annual_net_grid_MWh']>0
    return dict(initial_financed_capital=fin,annual_source_service=service,annual_service=service+x['conversion_annual_service'],annual_makeup=makeup,annual_expense=annual,blanket_life_years=bl,magnet_life_years=ml,blanket_events=float(bc),magnet_events=float(mc),primary_events=float(pc),blanket_replacement_pv=bpv,magnet_replacement_pv=mpv,primary_replacement_pv=ppv,overhaul_pv=opv,source_replacement_pv=spv,conversion_replacement_pv=x['conversion_replacement_pv'],terminal_pv=terminal,annual_expense_pv=apv,total_cost_pv=total,energy_pv=epv,lcoe_USD2025_MWh=total/epv if valid else 0.,outage_years=outage,outage_margin=n*(1-a)-outage,domain_supported=float(x['construction_years']>=0 and min(x['initial_capital'],x['routine_fraction'],x['dismantle_fraction'],x['salvage_fraction'])>=0),economic_defined=float(valid),cost_residual=total-fin-spv-x['conversion_replacement_pv']-apv-terminal)
