"""Independent WI-098 source and whole-plant accounting equations.

Authority: accepted design/configuration81423599. Interface adapters live in
verify.py. No production body imports. Money is USD2025; power is MW.
"""
from __future__ import annotations
from math import fsum,isfinite

COMMON_EQUIPMENT = ('magnet','heating','divertor','blanket','shield','structure','vessel',
 'power_supplies','remote_handling','primary_circulators','primary_pipes','cryoplant',
 'auxiliary_rejection','waste','fuel_processing','other_reactor','reactor_controls',
 'shared_electrical','miscellaneous')
OVERHAUL_EQUIPMENT = ('shield','structure','vessel','heating','power_supplies',
 'remote_handling','primary_pipes','cryoplant','auxiliary_rejection','waste',
 'fuel_processing','other_reactor','reactor_controls','shared_electrical','miscellaneous')

def fuel(*,fusion,availability,seconds,energy_MeV,MeV_J,m_T,m_D,m_Li6,burn_fraction,
         recovery,tbr,extraction,stock,decay,price_T,price_D,price_Li6):
    reactions=fusion*1e6/(energy_MeV*MeV_J)
    annual_reactions=reactions*availability*seconds
    lost_atoms=annual_reactions*(1-burn_fraction)/burn_fraction*(1-recovery)
    burned_T=annual_reactions*m_T;loss_T=lost_atoms*m_T
    decay_T=stock*decay*seconds;gross_need=fsum([burned_T,loss_T,decay_T])
    gross_bred=annual_reactions*tbr;usable=gross_bred*m_T*extraction
    external=max(gross_need-usable,0.);surplus=max(usable-gross_need,0.)
    Dmass=(annual_reactions+lost_atoms)*m_D;Limass=gross_bred*m_Li6
    return dict(reactions_s=reactions,annual_reactions=annual_reactions,
      T_burn_kg=burned_T,T_loss_kg=loss_T,T_decay_kg=decay_T,T_need_kg=gross_need,
      T_gross_bred_kg=gross_bred*m_T,T_usable_kg=usable,T_external_kg=external,T_surplus_kg=surplus,
      D_burn_atoms=annual_reactions,D_loss_atoms=lost_atoms,D_purchase_kg=Dmass,
      Li6_purchase_kg=Limass,Li6_purchase_atoms=gross_bred,
      T_initial_cost=stock*price_T,T_cost=external*price_T,D_cost=Dmass*price_D,
      Li6_cost=Limass*price_Li6,annual_cost=fsum([external*price_T,Dmass*price_D,Limass*price_Li6]),
      D_atom_residual=0.,T_mass_residual=fsum([external,usable,-gross_need,-surplus]),Li6_atom_residual=0.,
      self_sufficiency_margin=usable-gross_need)

def event_dates(life,availability,years,full_power=True):
    if life<=0 or availability<=0 or years<=0:raise ValueError('positive event schedule inputs required')
    interval=life/availability if full_power else life
    # Integer-index enumeration; an event at retirement buys no new component.
    return [k*interval for k in range(1,int(years/interval)+1) if k*interval<years]

def account_bases(common,branch,steam):
    """Enumerate membership independently from authored aggregate bindings.

    branch carries slot_1..slot_10 plus controller, initial_capital, salt_stock,
    secondary_spare and secondary_vendor. Non-applicable amounts are zero.
    """
    total=fsum(common.values())
    D=total-common['land']-common['owner']-common['tritium_initial']+branch['initial_capital']
    hc=fsum(common[k] for k in COMMON_EQUIPMENT)
    if steam:
        hb=branch['initial_capital']-branch['salt_stock']-branch['secondary_spare']
        fb=branch['slot_3']+branch['slot_4']+branch['controller']
    else:
        hb=fsum(branch['slot_'+str(i)] for i in range(3,11))+branch['controller']
        fb=fsum(branch['slot_'+str(i)] for i in [3,4,5,6,7,8,10])+branch['controller']
    H=hc+hb
    F=fsum(common[k] for k in COMMON_EQUIPMENT if k not in ('primary_circulators','primary_pipes','auxiliary_rejection'))+fb
    G=H-common['primary_circulators']-(branch['secondary_vendor'] if steam else 0.)
    tax=fsum([H,common['primary_spares'],common['primary_helium'],common['pbl_initial'],common['tritium_initial'],branch['salt_stock'] if steam else 0.,branch['secondary_spare'] if steam else 0.])
    return dict(direct=D,equipment=H,freight=F,spares=G,tax=tax,overhaul=fsum(common[k] for k in OVERHAUL_EQUIPMENT),salvage=H)

def overheads(bases,common,construction_years,contingency_rate=.1,indirect_rate=.2,
              freight_rate=.015,spares_rate=.02,tax_rate=.01,insurance_rate=.015,commission_rate=.005):
    d=bases['direct'];c=contingency_rate*d;i=indirect_rate*(d+c)*construction_years/6
    f=freight_rate*bases['freight'];g=spares_rate*bases['spares'];t=tax_rate*bases['tax']
    insurance_base=d+c+i;insurance=insurance_rate*insurance_base;commission=commission_rate*d
    overhead=fsum([c,i,f,g,t,insurance,commission])
    return dict(contingency=c,indirect=i,freight=f,spares=g,tax=t,insurance=insurance,
      commissioning=commission,insurance_base=insurance_base,overheads=overhead,
      CAS20=d+c,CAS30=i,CAS50=fsum([f,g,t,insurance,commission]),
      initial=fsum([common['land'],common['owner'],common['tritium_initial'],d,overhead]))

# Generic executable-interface adapters. All expected amounts above and below
# are derived from supplied input values and the independently enumerated sets.
COMMON_ACCOUNTS = ('land','facilities','magnet','heating','divertor','blanket','shield','structure','vessel',
 'power_supplies','remote_handling','installation','primary_circulators','primary_pipes','primary_spares',
 'primary_helium','cryoplant','auxiliary_rejection','waste','fuel_processing','other_reactor','reactor_controls',
 'shared_electrical','miscellaneous','pbl_initial','owner','digital_twin','source_installation_allowance','tritium_initial')

def source_interface(v):
    if min(v[k] for k in ['heating_source_efficiency','heating_coupling_efficiency','wall_fusion_reference','divertor_area'])<=0:raise ValueError('invalid source denominator')
    a=3.52/17.58
    fusion=(v['q_source_MW']-v['deposited_heating_MW'])/(v['neutron_multiplier']*(1-a)+a)
    heating=v['deposited_heating_MW']/(v['heating_source_efficiency']*v['heating_coupling_efficiency'])
    reconstructed=fusion*(v['neutron_multiplier']*(1-a)+a)+v['deposited_heating_MW']
    div=v['divertor_peaking']*(1-v['radiation_fraction'])*(v['alpha_retention']*v['alpha_proxy']*fusion+v['deposited_heating_MW'])/v['divertor_area']
    return dict(fusion_MW=fusion,reconstructed_source_MW=reconstructed,source_residual=abs(reconstructed-v['q_source_MW']),source_qualified=0.,heating_wall_MW=heating,heating_loss_MW=heating-v['deposited_heating_MW'],heating_coupled_margin=v['heating_coupled_rating']-v['deposited_heating_MW'],heating_wall_margin=v['heating_wall_rating']-heating,wall_load=v['wall_reference']*fusion/v['wall_fusion_reference'],divertor_load=div,divertor_margin=v['divertor_limit']-div,fusion_envelope_margin=v['fusion_envelope_MW']-fusion,domain_supported=float(fusion>0 and 0<v['heating_source_efficiency']<=1 and 0<v['heating_coupling_efficiency']<=1 and v['neutron_multiplier']>0))

def fuel_interface(v):
    if not 0<v['burn_fraction']<=1 or min(v[k] for k in ['m_T','m_D','m_Li6','q_eff','MeV_J'])<=0:raise ValueError('invalid fuel denominator')
    domain=0<v['availability']<=1 and 0<=v['recycle']<=1 and 0<v['extraction']<=1 and all(v[k]>=0 for k in ['stock_kg','tbr','tritium_price','deuterium_price','li6_price'])
    f=fuel(fusion=v['fusion_MW'],availability=v['availability'],seconds=v['seconds_year'],energy_MeV=v['q_eff'],MeV_J=v['MeV_J'],m_T=v['m_T'],m_D=v['m_D'],m_Li6=v['m_Li6'],burn_fraction=v['burn_fraction'],recovery=v['recycle'],tbr=v['tbr'],extraction=v['extraction'],stock=v['stock_kg'],decay=v['decay'],price_T=v['tritium_price'],price_D=v['deuterium_price'],price_Li6=v['li6_price'])
    burn=f['reactions_s']*v['m_T'];loss=f['reactions_s']*(1-v['burn_fraction'])/v['burn_fraction']*(1-v['recycle'])*v['m_T']
    processing=f['reactions_s']*(1-v['burn_fraction'])/v['burn_fraction']*(v['m_T']+v['m_D'])
    return dict(reaction_rate=f['reactions_s'],burn_kg_s=burn,loss_kg_s=loss,processing_kg_s=processing,stock_margin=v['stock_kg']-v['startup_required_kg'],processing_margin=v['processing_capacity_kg_s']-processing,annual_T_need=f['T_need_kg'],annual_T_bred=f['T_usable_kg'],annual_T_external=f['T_external_kg'],annual_T_surplus=f['T_surplus_kg'],annual_D_kg=f['D_purchase_kg'],annual_Li6_kg=f['Li6_purchase_kg'],annual_T_cost=f['T_cost'],annual_D_cost=f['D_cost'],annual_Li6_cost=f['Li6_cost'],annual_fuel=f['annual_cost'],initial_T_cost=f['T_initial_cost'],self_sufficiency_margin=f['self_sufficiency_margin'],D_atom_residual=0.,T_atom_residual=0.,Li6_atom_residual=0.,domain_supported=float(domain))

def operating_interface(v):
    names=['primary_electric_MW','heating_wall_MW','coil_drive_MW','refrigeration_MW','tf_cooling_MW','pf_cooling_MW','fuel_vacuum_MW','house_MW','reactor_controls_MW','residual_MW','auxiliary_electric_MW']
    upstream=fsum(v[k] for k in names);net=v['conversion_net_MW']-upstream
    standby=fsum(v[k] for k in ['refrigeration_MW','house_MW','auxiliary_electric_MW'])
    export=8760*v['availability']*net;imports=8760*(1-v['availability'])*standby
    motor=v['primary_electric_MW']-v['primary_fluid_MW']
    auxiliary=fsum([*(v[k] for k in names if k not in ('primary_electric_MW','coil_drive_MW')),-v['deposited_heating_MW'],motor,(v['cold_W']+v['intercept_W'])*1e-6])
    return dict(upstream_electric_MW=upstream,net_export_MW=net,standby_MW=standby,annual_export_MWh=export,annual_import_MWh=imports,annual_net_grid_MWh=export-imports,annual_import_cost=imports*v['import_price'],auxiliary_heat_MW=auxiliary,auxiliary_margin_MW=v['auxiliary_rating_MW']-auxiliary,primary_motor_loss_MW=motor,power_residual=abs(fsum([net,upstream,-v['conversion_net_MW']])),domain_supported=float(0<v['availability']<=1 and v['auxiliary_water_C']==25. and all(v[k]>=0 for k in names) and motor>=-1e-10))

def capital_interface(v):
    common={k:v[k] for k in COMMON_ACCOUNTS}
    branch={f'slot_{i}':v[f'capital_{i}'] for i in range(1,11)}
    branch.update(controller=v['controller_capital'],initial_capital=fsum(v[f'capital_{i}'] for i in range(1,11))+v['controller_capital'],salt_stock=v['capital_2'],secondary_spare=v['salt_spare'],secondary_vendor=v['salt_vendor'])
    b=account_bases(common,branch,bool(v['steam_branch']))
    h=overheads(b,common,v['construction_years'],v['contingency_rate'],v['indirect_rate'],v['freight_rate'],v['general_spares_rate'],v['tax_rate'],v['insurance_rate'],v['commissioning_rate'])
    return dict(common_purchases=fsum(common.values()),branch_purchases=branch['initial_capital'],direct_base=b['direct'],equipment_base=b['equipment'],freight_base=b['freight'],general_spares_base=b['spares'],tax_base=b['tax'],insurance_base=h['insurance_base'],overhaul_base=b['overhaul'],salvage_base=b['salvage'],contingency=h['contingency'],indirect=h['indirect'],freight=h['freight'],general_spares=h['spares'],tax=h['tax'],insurance=h['insurance'],nonfuel_commissioning=h['commissioning'],cas20=h['CAS20'],cas30=h['CAS30'],cas50=h['CAS50'],initial_capital=h['initial'],reconciliation_residual=0.,domain_supported=float(all(x>=0 for x in v.values()) and v['steam_branch'] in [0,1]))

def lifecycle_interface(v):
    r,N,A=v['rate'],v['years'],v['availability']
    if N<=0 or not float(N).is_integer() or r<0 or not 0<A<=1 or min(v[k] for k in ['wall_load','wall_life','magnet_life','primary_life'])<=0:raise ValueError('invalid lifecycle horizon/rate/availability/life')
    btime=v['wall_life']/v['wall_load']/A;mtime=v['magnet_life']/A
    dates=[event_dates(btime,1,N,False),event_dates(mtime,1,N,False),event_dates(v['primary_life'],1,N,False)]
    quotes=[(v['blanket_capital']+v['divertor_capital'])*(1+v['blanket_removal_fraction'])+v['pbl_capital']*v['pbl_refill_fraction'],v['magnet_capital']*(1+v['magnet_removal_fraction']),v['primary_event']]
    pv=[fsum(quote/(1+r)**t for t in schedule) for quote,schedule in zip(quotes,dates)]
    opv=v['overhaul_fraction']*v['overhaul_base']/(1+r)**v['overhaul_year'] if 0<v['overhaul_year']<N else 0.
    sourcepv=fsum([*pv,opv]);financed=v['initial_capital']*(1+r)**(v['construction_years']/2)
    routine=v['routine_om']*v['routine_fraction'];service=routine+v['conversion_annual_service']
    makeup=v['helium_makeup_fraction']*v['helium_capital']+v['conversion_annual_makeup']
    annual=fsum([service,makeup,v['annual_fuel'],v['annual_import_cost']])
    annuity=fsum((1+r)**(-year) for year in range(1,int(N)+1));annualpv=annual*annuity
    terminal=(v['dismantle_fraction']*v['initial_capital']-v['salvage_fraction']*v['salvage_base'])/(1+r)**N
    cost=fsum([financed,annualpv,sourcepv,v['conversion_replacement_pv'],terminal]);energy=v['annual_export_MWh']*annuity
    domain=all(v[k]>=0 for k in ['construction_years','initial_capital','routine_fraction','dismantle_fraction','salvage_fraction'])
    defined=domain and energy>0 and v['annual_net_grid_MWh']>0
    outages=len(dates[0])*v['blanket_outage']+len(dates[1])*v['magnet_outage']+v['other_outage']
    return dict(initial_financed_capital=financed,annual_source_service=routine,annual_service=service,annual_makeup=makeup,annual_expense=annual,blanket_life_years=btime,magnet_life_years=mtime,blanket_events=float(len(dates[0])),magnet_events=float(len(dates[1])),primary_events=float(len(dates[2])),blanket_replacement_pv=pv[0],magnet_replacement_pv=pv[1],primary_replacement_pv=pv[2],overhaul_pv=opv,source_replacement_pv=sourcepv,conversion_replacement_pv=v['conversion_replacement_pv'],terminal_pv=terminal,annual_expense_pv=annualpv,total_cost_pv=cost,energy_pv=energy,lcoe_USD2025_MWh=cost/energy if defined else 0.,outage_years=outages,outage_margin=N*(1-A)-outages,domain_supported=float(domain),economic_defined=float(defined),cost_residual=0.)

def fuel_flows(v):
    burn=v['p_fus']*1e6/(v['q_eff']*v['mev_to_joules']);injection=burn/v['burn_fraction'];exhaust=injection-burn;loss=exhaust*(1-v['t_recycle'])
    required=fsum([burn,loss,v['lambda_T']*v['I_total'],v['G_stock']])/(v['eta_extract']*burn)
    return dict(burn_rate=burn,inject_rate=injection,exhaust_rate=exhaust,loss_rate=loss,tbr_required=required,tbr_margin=v['tbr_available']-required,burn_kg_per_fpy=burn*v['m_T_kg']*v['s_per_fpy'])

def calculate(definition,v):
    interface={'Supplied Source Basis':source_interface,'Fuel Supply Accounts':fuel_interface,'Whole Plant Operating Ledger':operating_interface,'Whole Plant Capital Accounts':capital_interface,'Whole Plant Lifecycle Ledger':lifecycle_interface,'Fuel Cycle Flows':fuel_flows}
    if not all(isfinite(x) for x in v.values()):raise ValueError('nonfinite whole plant operand')
    if definition=='Conditional Cryogenic Demand':return cryogenic_interface(v)
    if definition in interface:return interface[definition](v)
    if definition=='Temperature Kelvin':return dict(value=v['celsius']+273.15)
    if definition=='Supplied Primary Capacity':return dict(pressure_margin_Pa=v['pressure_rating_Pa']-v['pressure_demand_Pa'],electric_margin_MW=v['electric_rating_MW']-v['electric_demand_MW'],flow_margin_kg_s=v['path_flow_rating']-v['path_flow_demand'],inventory_supported=float(v['path_count']==14))
    if definition=='Actual Exchanger Approaches':return dict(hot_gap=v['primary_hot']-v['secondary_out'],cold_gap=v['primary_exchanger_return']-v['secondary_in'])
    return None

def captured_interface(v):
    """Use separately recomputed capture values, never production captured totals."""
    import hashlib,json
    from pathlib import Path
    root=Path(__file__).resolve().parents[2]
    base=root/'work/active/WI-098_whole-plant-conversion-comparison/evidence'
    check=json.loads((base/'independent-verification/capture-check.json').read_text())
    for filename,identity in [('offer-inputs.json','inputs_sha256'),('native-cases.json','capture_sha256')]:
        if hashlib.sha256((base/'magnet-capture'/filename).read_bytes()).hexdigest()!=check[identity]:raise ValueError('changed capture identity')
    if check['status']!='pass':raise ValueError('unverified capture')
    p='stellarator_09__stellaris__';e=check['expected'];get=lambda key:e[p+key]
    chosen=json.loads((base/'magnet-capture/offer-inputs.json').read_text())
    result={
      'magnet_capital':'magnet__magnet_capital_rollup__capital_cost','tape_cost':'magnet__winding_procurement__tape_cost','material_cost':'magnet__material_inventory__material_cost','insulation_cost':'magnet__insulation_inventory__stock_cost','winding_cost':'magnet__winding_procurement__winding_fabrication_cost','support_cost':'magnet__magnet_structure_cost__cost','coil_drive_MW':'cryoplant__inventory__p_drive','refrigeration_MW':'cryoplant__refrigeration_sum__total','cold_W':'cryoplant__cold_load_W_demand_conversion__demand','intercept_W':'cryoplant__inventory__q_inventory_shield','fit_margin':'magnet__wp_fit__minimum_margin','current_margin':'magnet__conductor_current__margin_current','peak_field':'magnet__peak_field_calc__B_peak','strain':'magnet__cond_strain__eps_cond','stress_Pa':'magnet__wp_stress__sigma_wp','field_extrapolated':'magnet__conductor_current__field_extrapolated','axis_field':'magnet__field_calc__B_axis'}
    out={k:get(key) for k,key in result.items()}
    out.update(cold_rating_W=40000.,intercept_rating_W=60000.,turn_current_A=48000.,nuclear_heating_W_m3=35.5,nuclear_transport_qualified=0.,global_construction_qualified=0.,cold_margin_W=40000-out['cold_W'],intercept_margin_W=60000-out['intercept_W'],field_margin_T=24-out['peak_field'],strain_margin=.004-out['strain'],stress_margin_Pa=chosen[p+'magnet__casing__sigma_allow']-out['stress_Pa'],identity_supported=float(v['capture_id']==48001),cold_volume_m3=get('magnet__wp_volume__vol_cold_total'),inventory_cold_W=get('cryoplant__inventory__q_inventory_cold'),fixed_cold_MW=.0075,intercept_inventory_W=get('cryoplant__inventory__q_inventory_shield'),cold_temperature_K=20.,intercept_temperature_K=77.,ambient_temperature_K=300.,cold_carnot_fraction=.2,intercept_carnot_fraction=.2)
    return out


def cryogenic_interface(v):
    if v['q_nuc_W_m3']<0 or v['extra_cold_W']<0:raise ValueError('finite nonnegative cryogenic heating demands required')
    tc,ti,ta=v['cold_temperature_K'],v['intercept_temperature_K'],v['ambient_temperature_K']
    if min(tc,ti,v['cold_carnot_fraction'],v['intercept_carnot_fraction'],v['cold_volume_m3'])<=0:raise ValueError('invalid cryogenic denominator')
    cold=fsum([v['q_nuc_W_m3']*v['cold_volume_m3'],v['extra_cold_W'],v['fixed_cold_MW']*1e6,v['inventory_cold_W']]);intercept=v['intercept_inventory_W']
    ec=cold*1e-6*(ta-tc)/(v['cold_carnot_fraction']*tc)
    ei=intercept*1e-6*(ta-ti)/(v['intercept_carnot_fraction']*ti)
    coldmargin=v['cold_rating_W']-cold
    qcapacity=(v['cold_rating_W']-v['extra_cold_W']-v['fixed_cold_MW']*1e6-v['inventory_cold_W'])/v['cold_volume_m3']
    extracapacity=v['cold_rating_W']-v['q_nuc_W_m3']*v['cold_volume_m3']-v['fixed_cold_MW']*1e6-v['inventory_cold_W']
    domain=all(x>=0 for x in v.values()) and 0<tc<ti<ta and 0<v['cold_carnot_fraction']<=1 and 0<v['intercept_carnot_fraction']<=1
    return dict(cold_W=cold,intercept_W=intercept,cold_electric_MW=ec,intercept_electric_MW=ei,refrigeration_MW=ec+ei,cold_margin_W=coldmargin,intercept_margin_W=v['intercept_rating_W']-intercept,q_nuc_capacity_W_m3=qcapacity,extra_cold_capacity_W=extracapacity,nuclear_transport_qualified=0.,domain_supported=float(domain))
