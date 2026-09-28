"""WI-098 separate isotope purchase streams; kg/year, USD2025/year; reviewed r2."""
AUTO_IMPLEMENTED=False
INPUTS=dict(fusion_MW=0.,availability=.8,burn_fraction=.05,recycle=.99,tbr=1.1980739195540366,extraction=1.,stock_kg=5.,startup_required_kg=0.,processing_capacity_kg_s=.00015,decay=1.782785958230312e-9,seconds_year=31536000.,m_T=5.008267663228036e-27,m_D=3.3435837768e-27,m_Li6=6.015122795*1.66053906892e-27,q_eff=17.58,MeV_J=1.602176634e-13,tritium_price=30e6*321.9/188.9,deuterium_price=2175.,li6_price=1000.)
OUTPUTS='reaction_rate burn_kg_s loss_kg_s processing_kg_s stock_margin processing_margin annual_T_need annual_T_bred annual_T_external annual_T_surplus annual_D_kg annual_Li6_kg annual_T_cost annual_D_cost annual_Li6_cost annual_fuel initial_T_cost self_sufficiency_margin D_atom_residual T_atom_residual Li6_atom_residual domain_supported'.split()
def calculate(x):
    if not 0<x['burn_fraction']<=1 or min(x['m_T'],x['m_D'],x['m_Li6'],x['q_eff'],x['MeV_J'])<=0:raise ValueError('fuel denominator domain')
    f=x['fusion_MW']*1e6/(x['q_eff']*x['MeV_J']);r=x['availability']*x['seconds_year']*f
    loss=(1-x['burn_fraction'])/x['burn_fraction']*(1-x['recycle'])
    need=r*x['m_T']*(1+loss)+x['stock_kg']*x['decay']*x['seconds_year']
    bred=r*x['tbr']*x['extraction']*x['m_T'];ext=max(need-bred,0.);surplus=max(bred-need,0.)
    d=r*x['m_D']*(1+loss);li=r*x['tbr']*x['m_Li6'];proc=(f/x['burn_fraction']-f)*(x['m_D']+x['m_T'])
    tc=ext*x['tritium_price'];dc=d*x['deuterium_price'];lc=li*x['li6_price']
    return dict(reaction_rate=f,burn_kg_s=f*x['m_T'],loss_kg_s=f*loss*x['m_T'],processing_kg_s=proc,stock_margin=x['stock_kg']-x['startup_required_kg'],processing_margin=x['processing_capacity_kg_s']-proc,annual_T_need=need,annual_T_bred=bred,annual_T_external=ext,annual_T_surplus=surplus,annual_D_kg=d,annual_Li6_kg=li,annual_T_cost=tc,annual_D_cost=dc,annual_Li6_cost=lc,annual_fuel=tc+dc+lc,initial_T_cost=x['stock_kg']*x['tritium_price'],self_sufficiency_margin=bred-need,D_atom_residual=(d/x['m_D']-r-r*loss)/max(r,1.),T_atom_residual=(ext+bred-need-surplus)/max(need,1.),Li6_atom_residual=(li/x['m_Li6']-r*x['tbr'])/max(r,1.),domain_supported=float(0<x['availability']<=1 and 0<=x['recycle']<=1 and 0<x['extraction']<=1 and min(x['stock_kg'],x['tbr'],x['tritium_price'],x['deuterium_price'],x['li6_price'])>=0))
