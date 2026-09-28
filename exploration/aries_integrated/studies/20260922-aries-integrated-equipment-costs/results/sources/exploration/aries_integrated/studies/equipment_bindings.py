"""Explicit independent WI-090 oracle bindings, reviewed against source ownership.

Financial values use USD2004 (not MUSD). No generated arithmetic is imported.
"""
from exploration.aries_integrated.studies import equipment_oracle as mathcheck
P='aries_integrated_plant__'

QUANTITIES={
    **{b+'_hx':(b+'_hx','selected_area') for b in ('he','pbli','divertor')},
    **{b+'_pump':(b+'_pump','selected_flow_capacity') for b in ('he','pbli','divertor')},
    **{b+'_duty_equipment':(b+'_capacity','selected_rating') for b in ('he','pbli','divertor')},
    **{o:(o,'selected_mass') for o in ('magnet_inventory','blanket_inventory','shield_inventory','primary_support','vacuum_equipment')},
    **{o:(o,'selected_quantity') for o in ('primary_piping','secondary_transport','conversion_services','vf_coils',
       'divertor_inventory','site_land','facilities','heating_equipment','magnet_power_supplies','impurity_control',
       'auxiliary_cooling','waste_equipment','fuel_services','other_reactor_equipment','instrumentation_control',
       'unallocated_source_scope','electrical_equipment','miscellaneous_equipment')},
    'compressor_equipment':('compressor_capacity','selected_rating'),
    'turbine_equipment':('turbine_capacity','selected_rating'),
    'generator_equipment':('generator_capacity','selected_rating'),
    'heat_rejection_equipment':('rejection_capacity','selected_rating'),
    'fuel_processing_equipment':('fuel_capacity','selected_rating'),
}
CORE=['blanket_inventory','shield_inventory','magnet_inventory','vf_coils','divertor_inventory',
      'heating_equipment','primary_support','vacuum_equipment','magnet_power_supplies','impurity_control']
THERMAL=[b+s for s in ('_hx','_pump','_duty_equipment') for b in ('he','pbli','divertor')]+['primary_piping','secondary_transport']
CONVERSION=['compressor_equipment','turbine_equipment','generator_equipment','conversion_services']
FIXED_PACKAGES={owner for owner,(_,field) in QUANTITIES.items() if field=='selected_quantity'}
MASS_COMPONENTS={'magnet_inventory':('selected_winding_mass','selected_structure_mass'),
                 'shield_inventory':('selected_shield_mass','selected_manifold_mass'),
                 'vacuum_equipment':('selected_vessel_mass','selected_cryostat_mass')}


def out(owner,calc,field):
    return f'{P}{owner}__{calc}__{field}'


def thermal_inputs(point):
    """Return computed thermal interfaces independently of generated wiring."""
    get=lambda owner,name:point[P+owner+'__'+name]
    powers={}
    ua={}
    for branch in ('he','pbli','divertor'):
        owner=branch+'_pump'
        mode=get(owner,'pump_mode')
        if mode not in (0,1):raise ValueError('unknown pump mode')
        powers[branch]=(get(owner,'fixed_power') if mode==1 else mathcheck.pump(
            get('heat_exchangers',branch+'_flow'),get(owner,'reference_flow'),get(owner,'reference_power'),
            get(owner,'efficiency'),get(owner,'reference_efficiency')))
        ua[branch]=mathcheck.exchanger(get(branch+'_hx','selected_area'),get(branch+'_hx','assumed_u'))
    return powers,ua


def evaluate(point, power, exhaust, net):
    get=lambda owner,name:point[P+owner+'__'+name]
    literal=lambda owner,calc,name:point[out(owner,calc,name)]
    result={}
    def emit(owner,calc,**fields):
        result.update({out(owner,calc,k):float(v) for k,v in fields.items()})
    def screen(owner,margin):
        applicable=literal(owner,'screen','applicable_in')>=1
        supported=literal(owner,'screen','conditions_supported_in')>=1
        available=literal(owner,'screen','demand_available_in')>=1
        emit(owner,'screen',margin=margin if applicable else 0,evaluation_defined=applicable and supported and available)
    # Generated zero-padding inputs are held inert in this declared study. Reject
    # rather than silently ignore a new nonzero contribution outside this scope.
    for name,value in point.items():
        if '__evaluate__amount' in name and name.endswith('_in') and value!=0 and not name.startswith(P+'source_'):
            raise ValueError(f'oracle only covers declared zero account padding: {name}')
    powers,ua=thermal_inputs(point)
    for b in powers:
        emit(b+'_hx','evaluate',ua=ua[b],area=get(b+'_hx','selected_area'))
        flow=get('heat_exchangers',b+'_flow')
        emit(b+'_pump','evaluate',electric=powers[b],operating_flow=flow,hydraulic_supported=0,mode=get(b+'_pump','pump_mode'))
        screen(b+'_pump',get(b+'_pump','selected_flow_capacity')-flow)
    fixed=get('cost_accounts','estimate_mode')
    if fixed not in (0,1):raise ValueError('unknown cost estimate mode')
    selected={o:get(*ref) for o,ref in QUANTITIES.items() if o not in MASS_COMPONENTS}
    for owner,fields in MASS_COMPONENTS.items():
        selected[owner]=sum(get(owner,field) for field in fields)
        emit(owner,'inventory',total=selected[owner])
    selected['lipb_inventory']=get('lipb_inventory','selected_core_mass')*get('lipb_inventory','external_mass_factor')
    emit('lipb_inventory','inventory',amount=selected['lipb_inventory'])
    capital={}
    for owner,quantity in selected.items():
        if owner in FIXED_PACKAGES:
            if quantity!=1:raise ValueError(f'fixed one-package domain required: {owner}')
            cost=get(owner,'reference_cost')*get(owner,'price_factor')
            capital[owner]=cost
            emit(owner,'estimate',amount=cost)
            emit(owner,'purchase',cost=cost)
            continue
        reference=get(owner,'reference_quantity')
        cost=mathcheck.purchase(quantity,reference,get(owner,'reference_cost'),get(owner,'price_factor'),bool(fixed))
        capital[owner]=cost
        emit(owner,'purchase',capital=cost,purchased_quantity=quantity,quantity_ratio=quantity/reference,
             source_budget=get(owner,'reference_cost'),extrapolated=float(not .5<=quantity/reference<=1.5))
    burn=power*1e6/(get('fuel','reaction_energy_mev')*get('fuel','mev_joules'))
    loss=(1-get('fuel','exhaust_recovery'))*exhaust
    stock=mathcheck.fuel(burn,loss,exhaust,get('fuel','tritium_atom_kg'),get('fuel','seconds_per_year'),
        get('cost_schedule','availability'),get('fuel_inventory','selected_tritium_kg'),get('fuel_inventory','process_residence_s'),
        get('fuel','decay_constant_s'),get('fuel_inventory','annual_recovery_kg'),get('fuel_inventory','tritium_price'))
    emit('fuel_inventory','atoms',atoms=stock['selected_atoms'],stock_kg=get('fuel_inventory','selected_tritium_kg'))
    emit('fuel_inventory','purchase',amount=stock['initial_stock_cost'])
    emit('fuel_inventory','annual',annual_burn=stock['annual_burn_kg'],annual_loss=stock['annual_loss_kg'],
         annual_decay=stock['annual_decay_kg'],annual_external=stock['annual_external_kg'],
         annual_recovery=get('fuel_inventory','annual_recovery_kg'),annual_cost=stock['annual_external_cost'],
         required_stock=stock['required_kg'],breeding_supported=0)
    screen('fuel_inventory',stock['margin_kg'])
    tbr=(burn+loss+get('fuel','decay_constant_s')*stock['selected_atoms']+get('fuel','dormant_stock_growth_atoms_s'))/(get('fuel','assumed_extraction')*burn)
    emit('fuel','evaluate',burn_rate=burn,loss_rate=loss,tbr_required=tbr)
    deuterium=(burn+loss)*get('fuel_inventory','deuterium_atom_kg')*get('fuel_inventory','deuterium_price')*31536000*get('cost_schedule','availability')*get('cost_accounts','one_module')
    emit('fuel_inventory','deuterium',annual_fuel=deuterium)
    sums={}
    def total(owner,leaves):
        value=sum(capital[x] if x in capital else sums[x] for x in leaves)
        sums[owner]=value
        emit(owner,'evaluate',total=value)
        return value
    total('core_first',CORE[:8]);total('core_cost',CORE)
    total('primary_heat_cost',[b+s for s in ('_hx','_pump') for b in ('he','pbli','divertor')]+['primary_piping'])
    total('heat_transport_cost',THERMAL)
    total('fuel_equipment',['fuel_processing_equipment','fuel_services'])
    total('reactor_cost',['core_cost','heat_transport_cost','auxiliary_cooling','waste_equipment','fuel_equipment',
                         'other_reactor_equipment','instrumentation_control','unallocated_source_scope'])
    total('conversion_equipment',CONVERSION)
    direct_source=total('direct_source_scope',['site_land','facilities','reactor_cost','conversion_equipment',
                                               'electrical_equipment','miscellaneous_equipment','lipb_inventory','heat_rejection_equipment'])
    direct=direct_source+stock['initial_stock_cost']
    emit('direct_cost','evaluate',total=direct)
    indirect=direct*get('indirect_cost','fraction')*literal('indirect_cost','evaluate','construction_time')/literal('indirect_cost','evaluate','reference_construction_time')
    contingency=(direct+indirect)*get('contingency','fraction')
    owner_allowance=direct*get('owner_commissioning','fraction')
    emit('indirect_cost','evaluate',cost=indirect)
    emit('contingency_basis','evaluate',total=direct+indirect)
    emit('contingency','evaluate',cost=contingency)
    emit('owner_commissioning','evaluate',amount=owner_allowance)
    om=get('annual_om','selected_amount')+literal('annual_om','evaluate','om_ref')*(
        literal('annual_om','evaluate','p_net')*literal('annual_om','evaluate','n_mod_in')/literal('annual_om','evaluate','ref_net_power'))**literal('annual_om','evaluate','alpha')
    emit('annual_om','evaluate',annual_om=om)
    makeup=capital['lipb_inventory']*get('cost_schedule','lipb_makeup_fraction')
    scope=capital['blanket_inventory']+capital['divertor_inventory']+makeup
    event=scope*get('cost_schedule','replacement_factor')
    scheduled=mathcheck.schedule(get('cost_schedule','replacement_life_fpy'),get('cost_schedule','availability'),get('cost_schedule','plant_years'),event)
    emit('replacement_lipb','evaluate',amount=makeup)
    emit('replacement_scope','evaluate',total=scope)
    emit('replacement_price','evaluate',amount=event)
    emit('replacement','evaluate',event_cost=event,interval_years=scheduled['interval'],event_count=scheduled['count'],
         lifetime_total=scheduled['lifetime_total'],annual_reserve=scheduled['reserve'],
         first_event_year=scheduled['event_times'][0] if scheduled['count'] else 0,
         last_event_year=scheduled['event_times'][-1] if scheduled['count'] else 0)
    source=sum(get('source_budget',f'account_{i}') for i in range(1,9))
    source_inclusive=source*get('source_budget','inclusive_multiplier')
    emit('source_budget','evaluate',direct_total=source,inclusive_capital=source_inclusive)
    source_children={}
    for owner in ('source_reactor_children','source_core_children_first','source_coil_children','source_fuel_children'):
        # Shared parent source facts occupy graph bindings, not duplicated entries.
        shared=({1:get('source_reconciliation','core_parent'),5:get('source_reconciliation','fuel_parent')}
                if owner=='source_reactor_children' else {3:get('source_reconciliation','coil_parent')}
                if owner=='source_core_children_first' else {})
        source_children[owner]=sum(shared[i] if i in shared else literal(owner,'evaluate',f'amount{i}_in') for i in range(1,9))
        emit(owner,'evaluate',total=source_children[owner])
    gaps={'reactor_gap':get('source_budget','account_3')-source_children['source_reactor_children'],
          'core_excess':source_children['source_core_children_first']-get('source_reconciliation','core_parent'),
          'coil_excess':source_children['source_coil_children']-get('source_reconciliation','coil_parent'),
          'fuel_gap':get('source_reconciliation','fuel_parent')-source_children['source_fuel_children']}
    for name,value in gaps.items():emit('source_reconciliation',name+'_calc',difference=value)
    known_mass=sum(selected[owner] for owner in ('magnet_inventory','blanket_inventory','shield_inventory','vacuum_equipment','primary_support'))
    emit('known_dry_inventory','evaluate',total=known_mass)
    emit('inventory_comparison','evaluate',difference=known_mass-get('inventory_comparison','source_dry_core_mass'))
    emit('inventory_comparison','support',amount=get('inventory_comparison','vf_mass_available')*literal('inventory_comparison','support','factor_in'))
    lipb_price=selected['lipb_inventory']*get('lipb_comparison','source_unit_rate')
    emit('lipb_comparison','price',amount=lipb_price)
    emit('lipb_comparison','evaluate',difference=lipb_price-get('source_budget','account_7'))
    source_replacement=get('source_replacement_comparison','event_cost')*get('source_replacement_comparison','events')
    emit('source_replacement_comparison','cost',amount=source_replacement)
    emit('source_replacement_comparison','mass',amount=get('source_replacement_comparison','event_mass')*get('source_replacement_comparison','events'))
    emit('source_replacement_comparison','evaluate',difference=source_replacement-get('source_replacement_comparison','printed_lifetime_cost'))
    imported=max(-net,0)*8760*get('cost_schedule','availability')
    import_cost=imported*get('cost_ledger','import_price')
    emit('cost_ledger','evaluate',direct=direct,source_direct=source,source_inclusive=source_inclusive,
         direct_difference=direct-source,overnight=direct+indirect+contingency+owner_allowance,
         annual_operating=om+stock['annual_external_cost']+deuterium+get('cost_ledger','consumables')+import_cost,
         annual_replacement_reserve=scheduled['reserve'],lifetime_replacement=scheduled['lifetime_total'],
         annual_export_mwh=max(net,0)*8760*get('cost_schedule','availability'),annual_import_mwh=imported,
         annual_import_cost=import_cost,source_reactor_gap=gaps['reactor_gap'],
         source_core_excess=gaps['core_excess'],source_coil_excess=gaps['coil_excess'],
         currency_year=literal('cost_ledger','evaluate','currency_year_in'))
    return result


def comparison_catalog():
    catalog=[]
    def add(owner,calc,fields):catalog.extend(out(owner,calc,name) for name in fields.split())
    for branch in ('he','pbli','divertor'):
        add(branch+'_hx','evaluate','ua area')
        add(branch+'_pump','evaluate','electric operating_flow hydraulic_supported mode')
        add(branch+'_pump','screen','margin evaluation_defined')
    for owner in (*QUANTITIES,'lipb_inventory'):
        if owner in FIXED_PACKAGES:
            add(owner,'purchase','cost')
            add(owner,'estimate','amount')
        else:
            add(owner,'purchase','capital purchased_quantity quantity_ratio source_budget extrapolated')
    for owner in MASS_COMPONENTS:add(owner,'inventory','total')
    add('lipb_inventory','inventory','amount')
    add('fuel_inventory','atoms','atoms stock_kg')
    add('fuel_inventory','purchase','amount')
    add('fuel_inventory','annual','annual_burn annual_loss annual_decay annual_external annual_recovery annual_cost required_stock breeding_supported')
    add('fuel_inventory','screen','margin evaluation_defined')
    add('fuel_inventory','deuterium','annual_fuel')
    add('fuel','evaluate','burn_rate loss_rate tbr_required')
    for owner in ('core_first','core_cost','primary_heat_cost','heat_transport_cost','fuel_equipment','reactor_cost',
                  'conversion_equipment','direct_source_scope','direct_cost','contingency_basis','replacement_scope'):
        add(owner,'evaluate','total')
    for owner in ('indirect_cost','contingency'):add(owner,'evaluate','cost')
    for owner in ('owner_commissioning','replacement_lipb','replacement_price'):add(owner,'evaluate','amount')
    add('annual_om','evaluate','annual_om')
    add('replacement','evaluate','event_cost interval_years event_count lifetime_total annual_reserve first_event_year last_event_year')
    add('source_budget','evaluate','direct_total inclusive_capital')
    for owner in ('source_reactor_children','source_core_children_first','source_coil_children','source_fuel_children','known_dry_inventory'):
        add(owner,'evaluate','total')
    for name in ('reactor_gap','core_excess','coil_excess','fuel_gap'):add('source_reconciliation',name+'_calc','difference')
    add('inventory_comparison','evaluate','difference')
    add('inventory_comparison','support','amount')
    add('lipb_comparison','price','amount')
    add('lipb_comparison','evaluate','difference')
    add('source_replacement_comparison','cost','amount')
    add('source_replacement_comparison','mass','amount')
    add('source_replacement_comparison','evaluate','difference')
    add('cost_ledger','evaluate','direct source_direct source_inclusive direct_difference overnight annual_operating annual_replacement_reserve lifetime_replacement annual_export_mwh annual_import_mwh annual_import_cost source_reactor_gap source_core_excess source_coil_excess currency_year')
    return catalog
