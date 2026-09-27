"""Reviewed r2 exact selected-purchase membership; USD2025 installed-cost proxies."""
import math
AUTO_IMPLEMENTED=False
COMMON='land facilities magnet heating divertor blanket shield structure vessel power_supplies remote_handling installation primary_circulators primary_pipes primary_spares primary_helium cryoplant auxiliary_rejection waste fuel_processing other_reactor reactor_controls shared_electrical miscellaneous pbl_initial owner digital_twin source_installation_allowance tritium_initial'.split()
H='magnet heating divertor blanket shield structure vessel power_supplies remote_handling primary_circulators primary_pipes cryoplant auxiliary_rejection waste fuel_processing other_reactor reactor_controls shared_electrical miscellaneous'.split()
F='magnet heating divertor blanket shield structure vessel power_supplies remote_handling cryoplant waste fuel_processing other_reactor reactor_controls shared_electrical miscellaneous'.split()
O='shield structure vessel heating power_supplies remote_handling primary_pipes cryoplant auxiliary_rejection waste fuel_processing other_reactor reactor_controls shared_electrical miscellaneous'.split()
INPUTS={k:0. for k in COMMON}|{f'capital_{i}':0. for i in range(1,11)}|dict(controller_capital=1e7,salt_spare=0.,salt_vendor=0.,steam_branch=0.,contingency_rate=.1,indirect_rate=.2,freight_rate=.015,general_spares_rate=.02,tax_rate=.01,insurance_rate=.015,commissioning_rate=.005,construction_years=8.)
OUTPUTS='common_purchases branch_purchases direct_base equipment_base freight_base general_spares_base tax_base insurance_base overhaul_base salvage_base contingency indirect freight general_spares tax insurance nonfuel_commissioning cas20 cas30 cas50 initial_capital reconciliation_residual domain_supported'.split()
def calculate(x):
    common=math.fsum(x[k] for k in COMMON);branch=math.fsum(x[f'capital_{i}'] for i in range(1,11))+x['controller_capital'];steam=x['steam_branch']==1.
    direct=common-x['land']-x['owner']-x['tritium_initial']+branch
    hc=math.fsum(x[k] for k in H);hb=branch-x['capital_2']-x['salt_spare'] if steam else branch;h=hc+hb
    freight=math.fsum(x[k] for k in F)+x['controller_capital']+(x['capital_3']+x['capital_4'] if steam else math.fsum(x[f'capital_{i}'] for i in (3,4,5,6,7,8,10)))
    g=h-x['primary_circulators']-(x['salt_vendor'] if steam else 0.)
    taxbase=h+x['primary_spares']+x['primary_helium']+x['pbl_initial']+x['tritium_initial']+(x['capital_2']+x['salt_spare'] if steam else 0.)
    c=x['contingency_rate']*direct;i=x['indirect_rate']*(direct+c)*x['construction_years']/6
    ib=direct+c+i;fr=x['freight_rate']*freight;sp=x['general_spares_rate']*g;tx=x['tax_rate']*taxbase;ins=x['insurance_rate']*ib;comm=x['commissioning_rate']*direct
    supp=fr+sp+tx+ins+comm;total=common+branch+c+i+supp
    return dict(common_purchases=common,branch_purchases=branch,direct_base=direct,equipment_base=h,freight_base=freight,general_spares_base=g,tax_base=taxbase,insurance_base=ib,overhaul_base=math.fsum(x[k] for k in O),salvage_base=h,contingency=c,indirect=i,freight=fr,general_spares=sp,tax=tx,insurance=ins,nonfuel_commissioning=comm,cas20=direct+c,cas30=i,cas50=supp,initial_capital=total,reconciliation_residual=total-(x['land']+x['owner']+x['tritium_initial']+direct+c+i+supp),domain_supported=float(min(x.values())>=0 and x['steam_branch'] in (0.,1.)))
