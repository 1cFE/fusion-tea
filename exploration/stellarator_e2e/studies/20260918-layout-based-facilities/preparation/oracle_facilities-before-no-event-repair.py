"""Independent facility arithmetic from WI-068's released design and source rows.

No production calculator/model is imported. Shared authority is the released
layout policy and MIT A.215 rows; agreement does not qualify those assumptions.
"""

import math

DAY_YEAR = 365.25
CY_M3 = 0.764554857984
SF_M2 = 0.09290304
SOURCE_ROWS = {
    'floor_form': (3100., 182434.8277, 19191.92427, 'SF'),
    'floor_rebar': (260., 568568.0349, 546291.652, 'TN'),
    'floor_concrete': (2100., 358772.036, 354136.3796, 'CY'),
    'upper_form': (234300., 14196509.53, 1403236.116, 'SF'),
    'upper_rebar': (1700., 4861416.797, 3571906.955, 'TN'),
    'upper_concrete': (11800., 3527928.923, 1989909.18, 'CY'),
}


def rates(ton_kg=907.18474):
    if not math.isfinite(ton_kg) or ton_kg <= 0:
        raise ValueError('positive TN mass required')
    units = {'SF': SF_M2, 'CY': CY_M3, 'TN': ton_kg}
    return {k: (labor + material) / quantity / units[unit]
            for k, (quantity, labor, material, unit) in SOURCE_ROWS.items()}


def occupancy(intervals, at=None):
    """Weighted half-open inventory; departure precedes receipt at an equal time."""
    events = []
    for begin, end, count in intervals:
        if end is not None and end <= begin:
            continue
        events.append((begin, count))
        if end is not None:
            events.append((end, -count))
    current = peak = 0.
    for when, delta in sorted(events, key=lambda item: (item[0], item[1])):
        if at is not None and when > at:
            break
        current += delta
        peak = max(peak, current)
    return current if at is not None else peak


def shell(length, width, height, wall, floor, roof, *,
          openings=(), partition_length=0., partition_openings=(),
          inner_attachment_area=0., ceiling_area=None, link=False):
    """Clear rectangle, actual openings and interior wall lengths in metres.

    Width includes partition bearing footprints; ceiling_area removes them.
    Links are clear between side walls, with no end walls or door holes.
    """
    if min(length, width, height, wall, floor, roof) <= 0:
        raise ValueError('positive shell dimensions required')
    exterior_l = length if link else length + 2 * wall
    exterior_w = width + 2 * wall
    footprint = exterior_l * exterior_w
    perimeter = 2 * (exterior_l + exterior_w)
    hole = sum(w*h for w,h in openings)
    phole = sum(w*h for w,h in partition_openings)
    wall_volume = ((footprint - length*width)*height - wall*hole
                   + wall*(partition_length*height-phole))
    if link:
        wall_faces = 4*length*height + 4*wall*height
    else:
        wall_faces = (perimeter + 2*(length+width))*height
    wall_faces += 2*partition_length*height - inner_attachment_area
    wall_faces -= 2*(hole+phole)
    wall_faces += sum(wall*(w+2*h) for w,h in (*openings,*partition_openings))
    ceiling = length*width if ceiling_area is None else ceiling_area
    floor_volume = footprint * floor
    upper_volume = wall_volume + footprint * roof
    return {'length': exterior_l, 'width': exterior_w, 'height': height+floor+roof,
            'footprint': footprint, 'clear_area': ceiling,
            'air_volume': ceiling*height, 'floor_concrete': floor_volume,
            'upper_concrete': upper_volume, 'floor_form': perimeter*floor,
            'upper_form': wall_faces+ceiling+perimeter*roof,
            'opening_area': hole+phole}


def price_shell(quantities, intensity, ton_kg=907.18474, multiplier=1.):
    unit = rates(ton_kg)
    values = dict(quantities)
    values['floor_rebar'] = intensity*values['floor_concrete']
    values['upper_rebar'] = intensity*values['upper_concrete']
    values['civil_2018'] = multiplier*sum(values[k]*unit[k] for k in unit)
    values['civil_2025'] = values['civil_2018']*321.9/251.1
    return values


def sector_schedule(packages, teams=2, remove=.5, install=.5, *, cooldown=30., split=7., transport=2., cleaning=7., testing=7., joining=7., recommission=30.):
    """Four outbound moves first; deterministic teams; returns in finish order."""
    if int(teams) != teams or teams < 1:
        raise ValueError('positive integer service teams required')
    free = [0.]*int(teams)
    jobs = []
    for sector in range(4):
        arrival = cooldown+split+transport*(sector+1)
        team = min(range(len(free)), key=lambda i:(free[i],i))
        start = max(arrival, free[team])
        done = start + packages*(remove+install)+cleaning+testing
        free[team] = done
        jobs.append({'sector':sector, 'arrival':arrival,'start':start,'done':done})
    carrier = cooldown+split+4*transport
    for job in sorted(jobs, key=lambda j:(j['done'], j['sector'])):
        carrier = max(carrier,job['done'])+transport
        job['returned'] = carrier
    return jobs, carrier+joining+recommission


def sector_inventory(events, packages, horizon=30., *, teams=2, remove=.5,
                     install=.5, process=1., prepare=1., lead=90.,
                     initial_lead=180., hold=365.25, yield_factor=1., initial_start=-120., schedule_options=None):
    if not math.isfinite(yield_factor) or yield_factor<1:
        raise ValueError("waste package yield must be at least one")
    opt = schedule_options or {}
    jobs, outage = sector_schedule(packages, teams, remove, install, **opt)
    initial_duration = packages*install+opt.get("testing",7.)
    initial_starts = [initial_start+(i//int(teams))*initial_duration for i in range(4)]
    clean_peaks=[]; queue_peaks=[]; store_peaks=[]
    ready=True; initial_ready=True; final_release=0.; shutdown=0.
    initial_margin=math.inf; recurring_margin=horizon*DAY_YEAR
    for sector, job in enumerate(jobs):
        clean=[]; queue=[]; storage=[]
        prep_free=dirty_free=-math.inf
        for event in [None,*events]:
            receipt = -initial_lead if event is None else event*DAY_YEAR-lead
            start = initial_starts[sector] if event is None else event*DAY_YEAR+job['start']+packages*remove+opt.get('cleaning',7.)
            for unit in range(int(packages)):
                prep_free=max(receipt,prep_free)+prepare
                deadline=initial_start if event is None else event*DAY_YEAR
                if event is None: initial_margin=min(initial_margin,deadline-prep_free)
                else: recurring_margin=min(recurring_margin,deadline-prep_free)
                ready &= prep_free <= deadline
                if event is None:
                    initial_ready &= prep_free <= deadline
                withdrawal=start+unit*install
                clean.append((receipt,max(withdrawal,prep_free),1))
                if event is not None:
                    arrival=event*DAY_YEAR+job['start']+(unit+1)*remove
                    service=max(arrival,dirty_free)
                    dirty_free=service+process
                    queue.append((arrival,service,1))
                    storage.append((dirty_free,dirty_free+hold,yield_factor))
                    final_release=max(final_release,dirty_free+hold)
        clean_peaks.append(occupancy(clean));queue_peaks.append(occupancy(queue))
        store_peaks.append(occupancy(storage));shutdown+=occupancy(storage,horizon*DAY_YEAR)
    return {'sector_jobs':jobs, 'outage_days':outage, 'clean_peak':max(clean_peaks),
            'queue_peak':max(queue_peaks), 'storage_peak':max(store_peaks),
            'ready':ready,'initial_ready':initial_ready,
            'shutdown_stored':shutdown, 'final_release':final_release,
            'initial_finish':max(initial_starts)+initial_duration+4*opt.get('transport',2.)+opt.get('joining',7.)+opt.get('recommission',30.),
            'initial_margin':min(initial_margin,-(max(initial_starts)+initial_duration+4*opt.get('transport',2.)+opt.get('joining',7.)+opt.get('recommission',30.))), 'recurring_margin':recurring_margin}


def cooling_inventory(counts=(28,28,14), lives=(10.,10.,15.), horizon=30., *,
                      lead=90., initial_lead=180., hold=365.25,
                      prepare_stations=2, machine_stations=2, bundle_stations=2,
                      machine_process=2., bundle_process=5., initial_handoff=-30., prepare_machine=.5, prepare_bundle=1., field_cycle=.2, internal_move=.1):
    """Independent discrete-event dispatcher; one carrier and persistent stations."""
    station_counts=(prepare_stations,machine_stations,bundle_stations)
    if any(int(n)!=n or n<1 for n in station_counts):
        raise ValueError('positive integer cooling resources required')
    if min(*lives, horizon, lead,initial_lead,hold,machine_process,bundle_process)<=0:
        raise ValueError('positive cooling durations required')
    prepared=[-initial_lead]*int(prepare_stations)
    clean=[[],[],[]];waiting=[[],[],[]];finished=[[],[],[]]
    # The two perpetually stocked spare machines prepare before initial batches.
    for kind in (0,1):
        s=min(range(len(prepared)),key=lambda i:(prepared[i],i))
        prepared[s]=max(-initial_lead,prepared[s])+prepare_machine
        clean[kind].append((-initial_lead,None,1))
    batches=[]
    for kind,(count,life) in enumerate(zip(counts,lives)):
        batches.append((initial_handoff,kind,int(count),True))
        k=1
        while k*life < horizon:
            batches.append((k*life*DAY_YEAR,kind,int(count),False)); k+=1
    units=[];ready=True;initial_ready=True
    initial_margin=math.inf; recurring_margin=horizon*DAY_YEAR
    for date,kind,count,initial in sorted(batches):
        receipt=-initial_lead if initial else date-lead
        for _ in range(count):
            s=min(range(len(prepared)),key=lambda i:(prepared[i],i))
            prepared[s]=max(prepared[s],receipt)+(prepare_bundle if kind==2 else prepare_machine)
            if initial: initial_margin=min(initial_margin,date-prepared[s])
            else: recurring_margin=min(recurring_margin,date-prepared[s])
            ready &= prepared[s]<=date
            if initial: initial_ready &= prepared[s]<=date
            units.append({'kind':kind,'date':date,'receipt':receipt,'prepared':prepared[s],
                          'initial':initial,'state':'field'})
    station=[None]*(int(machine_stations)+int(bundle_stations))
    carrier=-math.inf; movements=[]
    while any(unit['state']!='done' for unit in units):
        choices=[]
        for j,unit in enumerate(units):
            if unit['state']=='field':
                choices.append((max(carrier,unit['date'],unit['prepared']),2,j,-1))
            elif unit['state']=='waiting':
                compatible=range(int(machine_stations)) if unit['kind']<2 else range(int(machine_stations),len(station))
                for s in compatible:
                    if station[s] is None:
                        choices.append((max(carrier,unit['arrival']),1,j,s))
            elif unit['state']=='processing':
                choices.append((max(carrier,unit['processed']),0,j,unit['station']))
        begin,priority,j,s=min(choices)
        unit=units[j];kind=unit['kind']
        duration=field_cycle if priority==2 else internal_move
        carrier=begin+duration;movements.append((begin,carrier,priority,j))
        if priority==2:
            clean[kind].append((unit['receipt'],begin+field_cycle/2,1))
            unit['arrival']=carrier
            unit['state']='done' if unit['initial'] else 'waiting'
        elif priority==1:
            waiting[kind].append((unit['arrival'],begin,1))
            station[s]=j;unit['station']=s;unit['entered']=carrier
            unit['processed']=carrier+(bundle_process if kind==2 else machine_process)
            unit['state']='processing'
        else:
            station[s]=None;unit['released']=carrier
            finished[kind].append((carrier,carrier+hold,1));unit['state']='done'
    # Preparation must meet the campaign start; the shared carrier must finish
    # every initial delivery and its return before commissioning at day zero.
    initial_return=max((unit['arrival'] for unit in units if unit['initial']),default=0.)
    initial_margin=min(initial_margin,-initial_return)
    initial_ready &= initial_return<=0.
    ready &= initial_return<=0.
    def peaks(banks): return tuple(occupancy(bank) for bank in banks)
    return {'clean':peaks(clean), 'queue':peaks(waiting), 'finished':peaks(finished),
            'dirty':peaks([waiting[k]+finished[k] for k in range(3)]),
            'ready':ready,'initial_ready':initial_ready,'initial_margin':initial_margin,'recurring_margin':recurring_margin,'movements':movements,'units':units,
            'shutdown_stored':sum(occupancy(bank,horizon*DAY_YEAR) for bank in finished),
            'unfinished':sum(not u['initial'] and u['released']>horizon*DAY_YEAR for u in units),
            'final_release':max([0.]+[end for bank in finished for _,end,_ in bank])}

# Explicit public scenario contract, independently transcribed from the released
# facility-contract.md; no reflection from the generated implementation.
DEFAULTS = dict(
    facilities_enabled=True, facilities_cost_mode=1., facilities_capacity_mode=1.,
    sector_count=4., sector_bays=4., sector_service_teams=2.,
    exterior_allowance=2.,sector_route_clearance=6.,sector_headroom=3.,
    component_width=4.,component_height=2.,component_length=2.,
    component_handling_margin=.5,component_material_fraction=.5,
    divertor_packages_per_sector=4.,waste_package_yield=1.,
    component_remove_days=.5,component_install_days=.5,
    sector_clean_days=7.,sector_test_days=7.,sector_split_days=7.,sector_join_days=7.,
    sector_transport_days=2.,cooldown_days=30.,recommission_days=30.,
    initial_receipt_lead_days=180.,initial_sector_start_days=-120.,
    component_receipt_lead_days=90.,component_prepare_days=1.,
    component_process_days=1.,component_hold_days=365.25,
    clean_positions=36.,dirty_buffer_positions=18.,dirty_store_positions=36.,
    cooling_initial_receipt_lead_days=180.,cooling_initial_handoff_days=-30.,
    cooling_receipt_lead_days=90.,cooling_hold_days=365.25,
    cooling_prepare_stations=2.,cooling_machine_stations=2.,cooling_bundle_stations=2.,
    cooling_prepare_machine_days=.5,cooling_prepare_bundle_days=1.,
    cooling_machine_process_days=2.,cooling_bundle_process_days=5.,
    cooling_field_cycle_days=.2,cooling_internal_move_days=.1,
    cooling_clean_helium_positions=29.,cooling_clean_salt_positions=29.,cooling_clean_bundle_positions=14.,
    cooling_dirty_helium_positions=28.,cooling_dirty_salt_positions=28.,cooling_dirty_bundle_positions=14.,
    helium_package_length=6.,helium_package_width=3.,helium_package_height=4.,
    salt_package_length=3.,salt_package_width=2.,salt_package_height=3.,
    hx_end_allowance=2.,cooling_package_margin=1.,cooling_aisle_width=6.,cooling_cross_width=17.,
    cooling_headroom=9.,cooling_airlock_length=17.,
    nuclear_wall=2.,nuclear_floor=1.,nuclear_roof=1.,nuclear_rebar_density=150.,
    conventional_wall=.3,conventional_floor=.3,conventional_roof=.2,conventional_rebar_density=100.,
    building_separation=10.,external_access_width=12.,provisional_envelope_scale=1.,
    administration_occupants=200.,control_occupants=30.,security_occupants=10.,
    administration_area_per_person=12.,control_area_per_person=15.,security_area_per_person=12.,
    occupancy_circulation_factor=1.3,occupancy_height=4.,occupancy_aspect_ratio=2.,
    heat_rejection_length=100.,heat_rejection_width=60.,
    civil_cpi_ratio=321.9/251.1,civil_rate_multiplier=1.,tonne_interpretation_kg=907.18474,
    ventilation_coefficient=1000.,ventilation_exponent=.8,ventilation_cpi_ratio=321.9/130.7,
    land_rate_per_acre=10000.,retained_site_improvements=85e6,
)
ENVELOPES = {'turbine':(60,20,15),'cryo_coldbox':(20,12,10),'cryo_compressors':(30,12,8),
    'fuel':(30,20,8),'reactor_aux':(30,20,10),'power_supply':(20,10,8),'onsite_ac':(16,8,6),
    'service_water':(20,15,8),'conventional_shop':(20,15,8),'site_services':(20,10,6)}
ROOM_NAMES=('turbine_hall','cryo_coldbox','cryo_compressors','fuel_building','reactor_auxiliaries',
    'power_supply_building','electrical_building','service_water_building','maintenance_shop','site_services_building')
for _stem,_dims in ENVELOPES.items():
    DEFAULTS.update({_stem+'_'+dim:float(value) for dim,value in zip(('length','width','height'),_dims)})
_rate=rates()
for _level,_key in [('sub','floor'),('super','upper')]:
    DEFAULTS.update({_level+'_concrete_rate':_rate[_key+'_concrete'],
                    _level+'_formwork_rate':_rate[_key+'_form'],
                    _level+'_rebar_rate':_rate[_key+'_rebar']})
CHILDREN=('reactor_hall',*(f'sector_wing_{x}' for x in ('east','north','west','south')),
    *(f'sector_link_{x}' for x in ('east','north','west','south')),
    'cooling_hall','cooling_annex','cooling_link',*ROOM_NAMES,'administration','control','security')
QUANTITIES=('clear_length','clear_width','clear_height','clear_area','gross_area','air_volume',
            'sub_concrete','super_concrete','sub_formwork','super_formwork','sub_rebar','super_rebar')
SCALARS=('active cost_mode capacity_mode sector_length sector_width sector_height parcel_area '
 'controlled_air_volume total_clear_area total_gross_area total_air_volume '
 'blanket_packages_per_sector packages_per_sector material_capacity_volume unused_material_capacity '
 'initial_clean_required dirty_buffer_required dirty_store_required initial_ready_margin_days '
 'replacement_ready_margin_days outage_required_days outage_allowed_days outage_margin_days '
 'calendar_event_count calendar_first_event_year calendar_last_event_year '
 'cooling_clean_helium_required cooling_clean_salt_required cooling_clean_bundle_required '
 'cooling_dirty_helium_required cooling_dirty_salt_required cooling_dirty_bundle_required '
 'cooling_helium_queue_peak cooling_salt_queue_peak cooling_bundle_queue_peak '
 'cooling_initial_ready_margin_days cooling_replacement_ready_margin_days cooling_jobs_after_shutdown '
 'cooling_last_release_year cooling_carrier_moves clean_positions_allocated dirty_buffer_positions_allocated '
 'dirty_store_positions_allocated cooling_clean_helium_allocated cooling_clean_salt_allocated '
 'cooling_clean_bundle_allocated cooling_dirty_helium_allocated cooling_dirty_salt_allocated '
 'cooling_dirty_bundle_allocated initial_margin_days readiness_margin_days capacity_margin_units route_margin_m '
 'exterior_envelope_qualified sector_load_qualified contamination_procedure_qualified '
 'cooling_outage_basis_resolved provisional_room_count').split()


def rectangle_union(rectangles):
    """Exact area and exposed perimeter by elementary cell adjacency."""
    xs=sorted({x for x0,y0,x1,y1 in rectangles for x in (x0,x1)})
    ys=sorted({y for x0,y0,x1,y1 in rectangles for y in (y0,y1)})
    cells=set()
    for i,(x0,x1) in enumerate(zip(xs,xs[1:])):
        for j,(y0,y1) in enumerate(zip(ys,ys[1:])):
            x=(x0+x1)/2;y=(y0+y1)/2
            if any(a<x<c and b<y<d for a,b,c,d in rectangles):cells.add((i,j))
    area=perimeter=0.
    for i,j in cells:
        dx=xs[i+1]-xs[i];dy=ys[j+1]-ys[j]
        area+=dx*dy
        perimeter+=dy*((i-1,j) not in cells)+dy*((i+1,j) not in cells)
        perimeter+=dx*((i,j-1) not in cells)+dx*((i,j+1) not in cells)
    return area,perimeter


def room_takeoff(length,width,height,t,floor,roof,density,partitions=(),openings=(),link=False):
    # Coordinates: clear rectangle [0,L]x[0,W]; external walls surround it.
    walls=[(-t,-t,length+t,0),(-t,width,length+t,width+t),
           (-t,0,0,width),(length,0,length+t,width)] if not link else [
           (0,-t,length,0),(0,width,length,width+t)]
    walls.extend(partitions)
    wall_area,perimeter=rectangle_union(walls)
    gross=(length+(0 if link else 2*t))*(width+2*t)
    clear=gross-wall_area
    holes=sum(w*h for w,h in openings)
    sub=gross*floor;sup=gross*roof+wall_area*height-t*holes
    edge=2*(length+(0 if link else 2*t)+width+2*t)
    return dict(clear_length=length,clear_width=width,clear_height=height,
        clear_area=clear,gross_area=gross,air_volume=clear*height,
        sub_concrete=sub,super_concrete=sup,sub_formwork=edge*floor,
        super_formwork=perimeter*height-2*holes+sum(t*(w+2*h) for w,h in openings)+clear+edge*roof,
        sub_rebar=sub*density,super_rebar=sup*density)


def layout(p, physical, events):
    """Contract-level independent geometry and logistics; costs joined separately."""
    out={k:0. for k in SCALARS}
    out.update({c+'_'+q:0. for c in CHILDREN for q in QUANTITIES})
    out.update({key:0. for c in CHILDREN for key in (c+'_sub_cost_2018',c+'_super_cost_2018',c+'_cost_2018',c+'_cost_2025')})
    out.update({k:0. for k in ('civil_capital','installed_facility_capital','layout_buildings_capital','layout_land_cost','ventilation_1990','ventilation_2025')})
    if p['facilities_cost_mode'] not in (0,1) or p['facilities_capacity_mode'] not in (0,1):raise ValueError('facility selectors must be binary')
    if not p['facilities_enabled']:
        if p['facilities_cost_mode']:raise ValueError('facility cost requires enabled layout')
        out.update({k:1. for k in ('initial_margin_days','readiness_margin_days','capacity_margin_units','route_margin_m','outage_margin_days')})
        return out
    if physical['n_mod']!=1 or p['sector_count']!=4 or physical['calendar_mode']!=0:raise ValueError('unsupported facility topology/calendar')
    for key,value in p.items():
        if not math.isfinite(value):raise ValueError('nonfinite facility input '+key)
    for key,value in p.items():
        if key not in ('initial_sector_start_days','cooling_initial_handoff_days') and value<0:
            raise ValueError('negative facility input '+key)
    for key in ('component_width','component_height','component_length','component_material_fraction',
                'sector_service_teams','cooling_prepare_stations','cooling_machine_stations','cooling_bundle_stations',
                'nuclear_wall','conventional_wall','occupancy_aspect_ratio','tonne_interpretation_kg'):
        if p[key]<=0:raise ValueError('positive facility input required '+key)
    integer_keys=('sector_count','sector_bays','sector_service_teams','divertor_packages_per_sector',
        'clean_positions','dirty_buffer_positions','dirty_store_positions',
        'cooling_prepare_stations','cooling_machine_stations','cooling_bundle_stations')
    integer_keys+=tuple(k for k in p if k.startswith('cooling_') and k.endswith('_positions'))
    for key in integer_keys:
        if int(p[key])!=p[key]:raise ValueError('integer facility input required '+key)
    if p['component_material_fraction']>1:raise ValueError('material fraction exceeds one')
    if p['waste_package_yield']<1:raise ValueError('waste package yield must be at least one')
    R=physical['major_radius'];r=physical['minor_outer_radius'];V=physical['blanket_volume']
    years=physical['calendar_years'];t=p['nuclear_wall'];tc=p['conventional_wall']
    c=p['sector_route_clearance'];H=2*(r+p['exterior_allowance'])+p['sector_headroom']
    Ls=R+r+p['exterior_allowance'];Ws=math.sqrt(2)*Ls;Wlane=Ws+2*c
    nb=math.ceil(V/(4*p['component_material_fraction']*p['component_width']*p['component_height']*p['component_length']))
    packages=nb+p['divertor_packages_per_sector']
    iv=sector_inventory(events,packages,years,teams=p['sector_service_teams'],remove=p['component_remove_days'],
        install=p['component_install_days'],process=p['component_process_days'],prepare=p['component_prepare_days'],
        lead=p['component_receipt_lead_days'],initial_lead=p['initial_receipt_lead_days'],hold=p['component_hold_days'],
        yield_factor=p['waste_package_yield'],initial_start=p['initial_sector_start_days'],schedule_options=dict(
            cooldown=p['cooldown_days'],split=p['sector_split_days'],transport=p['sector_transport_days'],
            cleaning=p['sector_clean_days'],testing=p['sector_test_days'],joining=p['sector_join_days'],recommission=p['recommission_days']))
    co=cooling_inventory((physical['cooling_helium_count'],physical['cooling_salt_count'],physical['cooling_bundle_count']),
        (physical['cooling_machine_life'],physical['cooling_machine_life'],physical['cooling_bundle_life']),years,
        lead=p['cooling_receipt_lead_days'],initial_lead=p['cooling_initial_receipt_lead_days'],hold=p['cooling_hold_days'],
        prepare_stations=p['cooling_prepare_stations'],machine_stations=p['cooling_machine_stations'],bundle_stations=p['cooling_bundle_stations'],
        machine_process=p['cooling_machine_process_days'],bundle_process=p['cooling_bundle_process_days'],
        initial_handoff=p['cooling_initial_handoff_days'],prepare_machine=p['cooling_prepare_machine_days'],prepare_bundle=p['cooling_prepare_bundle_days'],
        field_cycle=p['cooling_field_cycle_days'],internal_move=p['cooling_internal_move_days'])
    resize=p['facilities_capacity_mode']==1
    ac=iv['clean_peak'] if resize else p['clean_positions']; ab=iv['queue_peak'] if resize else p['dirty_buffer_positions']; ast=iv['storage_peak'] if resize else p['dirty_store_positions']
    cool_alloc={kind:tuple(co[kind][i] if resize else p['cooling_'+kind+'_'+name+'_positions'] for i,name in enumerate(('helium','salt','bundle'))) for kind in ('clean','dirty')}
    out.update(active=1.,cost_mode=p['facilities_cost_mode'],capacity_mode=p['facilities_capacity_mode'],
        sector_length=Ls,sector_width=Ws,sector_height=H-p['sector_headroom'],blanket_packages_per_sector=nb,packages_per_sector=packages,
        material_capacity_volume=4*nb*p['component_material_fraction']*p['component_width']*p['component_height']*p['component_length'],
        initial_clean_required=iv['clean_peak'],dirty_buffer_required=iv['queue_peak'],dirty_store_required=iv['storage_peak'],
        initial_ready_margin_days=iv['initial_margin'],replacement_ready_margin_days=iv['recurring_margin'],
        outage_required_days=iv['outage_days'],outage_allowed_days=physical['calendar_outage']*DAY_YEAR,
        outage_margin_days=physical['calendar_outage']*DAY_YEAR-iv['outage_days'],calendar_event_count=len(events),
        calendar_first_event_year=events[0] if events else 0.,calendar_last_event_year=events[-1] if events else 0.,
        cooling_initial_ready_margin_days=co['initial_margin'],cooling_replacement_ready_margin_days=co['recurring_margin'],
        cooling_jobs_after_shutdown=co['unfinished'],cooling_last_release_year=co['final_release']/DAY_YEAR,cooling_carrier_moves=len(co['movements']),
        clean_positions_allocated=ac,dirty_buffer_positions_allocated=ab,dirty_store_positions_allocated=ast,
        initial_margin_days=min(iv['initial_margin'],co['initial_margin']),readiness_margin_days=min(iv['recurring_margin'],co['recurring_margin']),provisional_room_count=13.)
    out['unused_material_capacity']=out['material_capacity_volume']-V
    margins=[p['sector_bays']-4,ac-iv['clean_peak'],ab-iv['queue_peak'],ast-iv['storage_peak'],
             2-p['cooling_machine_stations'],2-p['cooling_bundle_stations']]
    for i,name in enumerate(('helium','salt','bundle')):
        out['cooling_'+name+'_queue_peak']=co['queue'][i]
        for kind in ('clean','dirty'):
            out['cooling_'+kind+'_'+name+'_required']=co[kind][i]
            out['cooling_'+kind+'_'+name+'_allocated']=cool_alloc[kind][i]
            margins.append(cool_alloc[kind][i]-co[kind][i])
    out['capacity_margin_units']=min(margins)
    buildings={};positions={}
    def add(name,L,W,h,nuclear=False,parts=(),doors=(),link=False):
        prefix='nuclear_' if nuclear else 'conventional_'
        q=room_takeoff(L,W,h,p[prefix+'wall'],p[prefix+'floor'],p[prefix+'roof'],p[prefix+'rebar_density'],parts,doors,link)
        buildings[name]=q
    wingL=max(Ls+2*c,6*math.ceil((ac+2)/4)+12+2*t,6*math.ceil((ab+ast+4)/4)+12+2*t)
    wingW=Wlane+56+2*t
    partitions=[(0,28,wingL,28+t),(0,28+t+Wlane,wingL,28+2*t+Wlane)]
    # Clean lower annex and dirty upper annex each have a U-shaped6m clear airlock.
    partitions.extend([(0,28-6-t,t,28),(t+6,28-6-t,2*t+6,28),(t,28-6-t,t+6,28-6)])
    edge=28+2*t+Wlane
    partitions.extend([(0,edge,t,edge+6+t),(t+6,edge,2*t+6,edge+6+t),(t,edge+6,t+6,edge+6+t)])
    half=max(2*Ls+2, (wingW+2*t)/2+2)
    add('reactor_hall',2*half,2*half,H,True,doors=[(Wlane,H)]*4)
    for direction in ('east','north','west','south'):
        add('sector_wing_'+direction,wingL,wingW,H,True,partitions,[(Wlane,H)]+[(6,6)]*6)
        add('sector_link_'+direction,p['building_separation'],Wlane,H,True,link=True)
    # Cooling cell envelopes follow actual shell/tube geometry and fixed-orientation carrier.
    aisle=p['cooling_aisle_width'];cross=p['cooling_cross_width'];margin=p['cooling_package_margin']
    bundleL=physical['hx_tube_length']+2*margin; bundleW=physical['hx_shell_bore']+2*margin
    shellL=physical['hx_shell_length']+2*p['hx_end_allowance']
    shellW=physical['hx_shell_bore']+2*physical['hx_shell_wall']
    cellW=aisle+2*max(p['helium_package_width']+.6,p['salt_package_width']+.6,shellW)
    machineL=2*(max(p['helium_package_length'],p['salt_package_length'])+2*margin)
    cellL=shellL+bundleL+2+machineL
    hallL=math.ceil(physical['cooling_circuits']/2)*cellW; hallW=2*cellL+cross
    add('cooling_hall',hallL,hallW,p['cooling_headroom'],doors=[(cross,p['cooling_headroom'])])
    widths=(2*(p['helium_package_width']+2*margin)+aisle,
        2*(p['salt_package_width']+2*margin)+aisle,2*(physical['hx_shell_bore']+2*margin)+aisle,
        2*(max(p['helium_package_width']+2*margin,p['salt_package_width']+2*margin,bundleW)+2*margin)+aisle)
    # Fixed source geometry yields widths16,14,16.4,20.4 at baseline.
    pitches=(p['helium_package_length']+2*margin,p['salt_package_length']+2*margin,bundleL)
    reserve=cross/2+p['cooling_airlock_length']+2*tc
    clean_depth=max(math.ceil(cool_alloc['clean'][i]/2)*pitches[i]+aisle for i in range(3))
    dirty_depth=max(max(math.ceil(cool_alloc['dirty'][i]/2)*pitches[i]+aisle for i in range(3)),
                    machineL/2+bundleL+10*margin)
    north=reserve+clean_depth;south=reserve+dirty_depth
    annexL=sum(widths)+3*tc;annexW=north+south
    transverse=[south-cross/2-tc,south+cross/2,south-cross/2-p['cooling_airlock_length']-2*tc,south+cross/2+p['cooling_airlock_length']+tc]
    parts=[(0,y,annexL,y+tc) for y in transverse]
    x=0.
    for w in widths[:-1]:
        x+=w
        parts.extend([(x,0,x+tc,south-cross/2-tc),(x,south+cross/2+tc,x+tc,annexW)])
        x+=tc
    add('cooling_annex',annexL,annexW,p['cooling_headroom'],parts=parts,
        doors=[(6,p['cooling_headroom'])]*14+[(cross,p['cooling_headroom'])]*2)
    add('cooling_link',p['building_separation'],cross,p['cooling_headroom'],link=True)
    for stem,name in zip(ENVELOPES,ROOM_NAMES):
        scale=p['provisional_envelope_scale']
        dims=[p[stem+'_'+d]*scale for d in ('length','width','height')]
        add(name,dims[0]+4,dims[1]+4,dims[2]+3,name=='fuel_building')
    for name in ('administration','control','security'):
        area=p[name+'_occupants']*p[name+'_area_per_person']*p['occupancy_circulation_factor']
        add(name,math.sqrt(area*p['occupancy_aspect_ratio']),math.sqrt(area/p['occupancy_aspect_ratio']),p['occupancy_height'])
    # Placement uses actual outside faces, not clear-room dimensions.
    h=half+t;sep=p['building_separation'];wel=wingL+2*t;wew=wingW+2*t
    positions['reactor_hall']=(-h,-h,h,h)
    base=(h+sep,-wew/2,h+sep+wel,wew/2)
    for turn,direction in enumerate(('east','north','west','south')):
        x0,y0,x1,y1=base
        corners=[(x,y) for x in (x0,x1) for y in (y0,y1)]
        for _ in range(turn):corners=[(-y,x) for x,y in corners]
        positions['sector_wing_'+direction]=(min(x for x,y in corners),min(y for x,y in corners),max(x for x,y in corners),max(y for x,y in corners))
    cw=hallL+2*tc;ch=hallW+2*tc
    x=h+sep+wel+sep
    positions['cooling_hall']=(x,-ch/2,x+cw,ch/2)
    ax=x+cw+sep
    positions['cooling_annex']=(ax,-south-tc,ax+annexL+2*tc,north+tc)
    # Reviewed campus row starts at the reactor hall's west exterior face.
    x=-h;top=-(h+sep+wel)-sep
    for name in (*ROOM_NAMES,'administration','control','security'):
        q=buildings[name];wt=t if name=='fuel_building' else tc
        el=q['clear_length']+2*wt;ew=q['clear_width']+2*wt
        positions[name]=(x,top-ew,x+el,top);x+=el+sep
    positions['heat_rejection_plot']=(x,top-p['heat_rejection_width'],x+p['heat_rejection_length'],top)
    bounds=(min(v[0] for v in positions.values()),min(v[1] for v in positions.values()),max(v[2] for v in positions.values()),max(v[3] for v in positions.values()))
    out['parcel_area']=(bounds[2]-bounds[0]+2*p['external_access_width'])*(bounds[3]-bounds[1]+2*p['external_access_width'])
    for name,q in buildings.items():
        out.update({name+'_'+k:v for k,v in q.items()})
        subtotal={}
        for level in ('sub','super'):
            subtotal[level]=p['civil_rate_multiplier']*(q[level+'_concrete']*p[level+'_concrete_rate']+q[level+'_formwork']*p[level+'_formwork_rate']+q[level+'_rebar']*p[level+'_rebar_rate']*907.18474/p['tonne_interpretation_kg'])
            out[name+'_'+level+'_cost_2018']=subtotal[level]
        out[name+'_cost_2018']=sum(subtotal.values());out[name+'_cost_2025']=sum(subtotal.values())*p['civil_cpi_ratio']
    out['civil_capital']=sum(out[name+'_cost_2025'] for name in CHILDREN)
    out['controlled_air_volume']=buildings['reactor_hall']['air_volume']+4*((Wlane+28)*wingL-(18*t+2*t*t))*H+4*buildings['sector_link_east']['air_volume']+buildings['fuel_building']['air_volume']
    for output,key in [('total_clear_area','clear_area'),('total_gross_area','gross_area'),('total_air_volume','air_volume')]:out[output]=sum(q[key] for q in buildings.values())
    out['ventilation_1990']=p['ventilation_coefficient']*out['controlled_air_volume']**p['ventilation_exponent']
    out['ventilation_2025']=out['ventilation_1990']*p['ventilation_cpi_ratio']
    out['installed_facility_capital']=out['civil_capital']+out['ventilation_2025']
    out['layout_buildings_capital']=out['installed_facility_capital']+p['retained_site_improvements']
    out['layout_land_cost']=out['parcel_area']/4046.8564224*p['land_rate_per_acre']
    envelope_w=p['component_width']+2*p['component_handling_margin'];envelope_l=p['component_length']+2*p['component_handling_margin']
    envelope_h=p['component_height']+2*p['component_handling_margin']
    bundleH=physical['hx_shell_bore']+margin
    machine_side=max(p['helium_package_width']+.6,p['salt_package_width']+.6,shellW)
    out['route_margin_m']=min(5-envelope_w,3-envelope_h,c-math.hypot(envelope_w,envelope_l),
        6-envelope_w,6-envelope_h,c-6,p['sector_headroom'],aisle-bundleW,cross-bundleL,
        p['cooling_airlock_length']-bundleL,
        p['cooling_headroom']-max(bundleH,p['helium_package_height']+margin,p['salt_package_height']+margin),
        machine_side-max(p['helium_package_width'],p['salt_package_width']),
        cellW-shellW,wingL-Ls-2*c)
    carried=((p['helium_package_length']+2*margin,p['helium_package_width']+2*margin,p['helium_package_height']+margin),
             (p['salt_package_length']+2*margin,p['salt_package_width']+2*margin,p['salt_package_height']+margin),
             (bundleL,bundleW,bundleH))
    service_slot_width=(widths[3]-aisle)/2
    for length,width,height in carried:
        out['route_margin_m']=min(out['route_margin_m'],aisle-width,6-width,
            cross-length,p['cooling_airlock_length']-length,p['cooling_headroom']-height,
            service_slot_width-width)
    boxes=list(positions.values())
    for i,a in enumerate(boxes):
        for b in boxes[i+1:]:
            overlap_x=min(a[2],b[2])-max(a[0],b[0]); overlap_y=min(a[3],b[3])-max(a[1],b[1])
            if min(overlap_x,overlap_y)>1e-9:
                out['route_margin_m']=min(out['route_margin_m'],-min(overlap_x,overlap_y))
    return out
