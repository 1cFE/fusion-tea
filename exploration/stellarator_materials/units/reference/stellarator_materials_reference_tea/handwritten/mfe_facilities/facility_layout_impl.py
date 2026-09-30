"""WI-068 reviewed conceptual facilities: dated resource schedule and civil solids.

Authority: WI-076 reviewed facilities-binding-plan.md; retained WI-068 civil identities. Mechanical, shielding,
contamination and cooling-outage qualification remain explicitly unresolved.
"""
from __future__ import annotations
import math
from stellarator_materials_reference_tea.handwritten.mfe_lifecycle.lifecycle_calendar_impl import lifecycle_calendar_live
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_materials_reference_tea.modules.mfe_facilities.facility_layout import Facility_LayoutInput
AUTO_IMPLEMENTED = False
DAYS = 365.25


def peak(intervals):
    """Half-open occupancy; release precedes receipt at a coincident endpoint."""
    events = [(a, 1) for a,b in intervals if b>a]+[(b,-1) for a,b in intervals if b>a]
    n=answer=0
    for _,delta in sorted(events):
        n+=delta; answer=max(answer,n)
    return answer


def union_measure(rectangles):
    """Exact orthogonal union area and exposed perimeter by coordinate cells."""
    xs=sorted({r[i] for r in rectangles for i in (0,2)})
    ys=sorted({r[i] for r in rectangles for i in (1,3)})
    cells=set()
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            x=(xs[i]+xs[i+1])/2; y=(ys[j]+ys[j+1])/2
            if any(a<x<c and b<y<d for a,b,c,d in rectangles):cells.add((i,j))
    area=perimeter=0.
    for i,j in cells:
        dx=xs[i+1]-xs[i];dy=ys[j+1]-ys[j];area+=dx*dy
        perimeter+=dy*((i-1,j) not in cells)+dy*((i+1,j) not in cells)
        perimeter+=dx*((i,j-1) not in cells)+dx*((i,j+1) not in cells)
    return area,perimeter


def civil(L,W,H,t,f,r,rho,partitions=(),doors=(),open_ends=False):
    """Inside-shell bounds; doors=(clear width,height) in represented walls."""
    ring=[(-t,-t,0,W+t),(L,-t,L+t,W+t)] if not open_ends else []
    ring += [(0,-t,L,0),(0,W,L,W+t)]
    # Open links have side walls only, and attach without overlapping end caps.
    extL=L if open_ends else L+2*t;extW=W+2*t
    whole=ring+list(partitions);solid,face=union_measure(whole)
    internal,_=union_measure(list(partitions)) if partitions else (0.,0.)
    aperture=sum(w*h for w,h in doors);reveals=sum(t*(2*h+w) for w,h in doors)
    wall=solid*H-aperture*t;clear=L*W-internal;gross=extL*extW
    if min(wall,clear)<0:raise ValueError('doors exceed civil wall or partition area')
    values=dict(clear_length=L,clear_width=W,clear_height=H,clear_area=clear,gross_area=gross,air_volume=clear*H,
                sub_concrete=gross*f,super_concrete=wall+gross*r,
                sub_formwork=2*(extL+extW)*f,super_formwork=face*H-2*aperture+reveals+clear+2*(extL+extW)*r)
    values.update(sub_rebar=values['sub_concrete']*rho,super_rebar=values['super_concrete']*rho)
    return values,dict(wall_rectangles=whole,openings=[dict(width=w,height=h) for w,h in doors],wall_footprint=solid,wall_exposed_perimeter=face)


def vessel_schedule(x,dates):
    if x["waste_package_yield"] < 1:raise ValueError("waste package yield must be at least one; reduction credit is unsupported")
    count=int(x['selected_blanket_packages_per_sector'])+int(x['divertor_packages_per_sector'])
    team=[0.]*int(x['sector_service_teams']);transport=x['cooldown_days']+x['sector_split_days'];schedule=[]
    for j in range(4):
        transport+=x['sector_transport_days'];k=min(range(len(team)),key=team.__getitem__)
        start=max(transport,team[k]);end=start+count*(x['component_remove_days']+x['component_install_days'])+x['sector_clean_days']+x['sector_test_days'];team[k]=end
        schedule.append(dict(sector=j,start=start,end=end,team=k))
    for row in sorted(schedule,key=lambda z:z['end']):
        transport=max(transport,row['end'])+x['sector_transport_days'];row['return']=transport
    required=transport+x['sector_join_days']+x['recommission_days']
    ready_initial=x['initial_sector_start_days']-(-x['initial_receipt_lead_days']+count*x['component_prepare_days'])
    initial_finish=x['initial_sector_start_days']+math.ceil(4/len(team))*(count*x['component_install_days']+x['sector_test_days'])+4*x['sector_transport_days']+x['sector_join_days']+x['recommission_days']
    ready_initial=min(ready_initial,-initial_finish)
    ready=x['calendar_years']*DAYS; wings=[]
    for s in schedule:
        process=-math.inf;prepared=-x['initial_receipt_lead_days']+count*x['component_prepare_days']
        clean=[(-x['initial_receipt_lead_days'],max(prepared,x['initial_sector_start_days']+(j+1)*x['component_install_days'])) for j in range(count)]
        queue=[];store=[];jobs=[]
        for date in dates:
            base=date*DAYS;receipt=base-x['component_receipt_lead_days'];prepared=max(prepared,receipt)+count*x['component_prepare_days']
            deadline=base+s['start']+count*x['component_remove_days']+x['sector_clean_days'];ready=min(ready,base-prepared)
            for j in range(count):
                arrival=base+s['start']+(j+1)*x['component_remove_days'];start=max(arrival,process);process=start+x['component_process_days']
                queue.append((arrival,start));store.append((process,process+x['component_hold_days']))
                clean.append((receipt,max(prepared,deadline+(j+1)*x['component_install_days'])))
                jobs.append(dict(receipt=arrival,processing_start=start,processing_end=process,release=process+x['component_hold_days']))
        wings.append(dict(clean=peak(clean),buffer=peak(queue),stored=math.ceil(peak(store)*x['waste_package_yield']),jobs=jobs,clean_intervals=clean))
    return dict(packages=count,blanket=count-int(x['divertor_packages_per_sector']),outage=required,initial_margin=ready_initial,ready_margin=ready,schedule=schedule,wings=wings)


def cooling_schedule(x):
    counts={'helium':int(x['cooling_helium_count']),'salt':int(x['cooling_salt_count']),'bundle':int(x['cooling_bundle_count'])}
    batches=[];N=x['calendar_years']*DAYS
    for kind,count in counts.items():
        life=x['cooling_bundle_life'] if kind=='bundle' else x['cooling_machine_life']
        dates=[x['cooling_initial_handoff_days']]+[k*life*DAYS for k in range(1,math.ceil(x['calendar_years']/life)) if k*life<x['calendar_years']]
        for date in dates:batches.append((date,kind,count,date==x['cooling_initial_handoff_days']))
    lead=x['cooling_initial_receipt_lead_days'];prep=[-lead]*int(x['cooling_prepare_stations']);spares=[]
    for kind in ('helium','salt'):
        k=min(range(len(prep)),key=prep.__getitem__);prep[k]+=x['cooling_prepare_machine_days'];spares.append(dict(kind=kind,receipt=-lead,prepared=prep[k],release=None))
    rows=[];initial_margin=min(x['cooling_initial_handoff_days']-s['prepared'] for s in spares);ready_margin=N
    for date,kind,count,initial in sorted(batches):
        receipt=-lead if initial else date-x['cooling_receipt_lead_days']
        for j in range(count):
            k=min(range(len(prep)),key=prep.__getitem__);prep[k]=max(prep[k],receipt)+x['cooling_prepare_bundle_days' if kind=='bundle' else 'cooling_prepare_machine_days']
            rows.append(dict(kind=kind,initial=initial,campaign=date,index=j,receipt=receipt,prepared=prep[k]))
            if initial:initial_margin=min(initial_margin,date-prep[k])
            else:ready_margin=min(ready_margin,date-prep[k])
    tasks=[dict(stage='field',due=max(r['campaign'],r['prepared']),row=j) for j,r in enumerate(rows)]
    free={'machine':[-math.inf]*int(x['cooling_machine_stations']),'bundle':[-math.inf]*int(x['cooling_bundle_stations'])};carrier=-math.inf;route=[]
    rank={'from_service':0,'to_service':1,'field':2}
    while tasks:
        choices=[]
        for k,task in enumerate(tasks):
            row=rows[task['row']];pool='bundle' if row['kind']=='bundle' else 'machine';slot=None;start=max(carrier,task['due'])
            if task['stage']=='to_service':
                slot=min(range(len(free[pool])),key=free[pool].__getitem__);start=max(start,free[pool][slot])
            if math.isfinite(start):choices.append((start,rank[task['stage']],task['row'],k,pool,slot))
        if not choices:raise ValueError('cooling resource deadlock')
        start,_,_,k,pool,slot=min(choices);task=tasks.pop(k);row=rows[task['row']];stage=task['stage']
        carrier=start+x['cooling_field_cycle_days' if stage=='field' else 'cooling_internal_move_days'];route.append(dict(stage=stage,row=task['row'],start=start,end=carrier))
        if stage=='field':
            row.update(withdraw=start,field_handoff=start+x['cooling_field_cycle_days']/2,return_arrival=carrier)
            if not row['initial']:tasks.append(dict(stage='to_service',due=carrier,row=task['row']))
        elif stage=='to_service':
            end=carrier+x['cooling_bundle_process_days' if pool=='bundle' else 'cooling_machine_process_days']
            row.update(service_pickup=start,service_start=carrier,service_end=end,station=pool+str(slot),station_pool=pool,station_slot=slot);free[pool][slot]=math.inf
            tasks.append(dict(stage='from_service',due=end,row=task['row']))
        else:
            row.update(station_release=carrier,storage_arrival=carrier,release=carrier+x['cooling_hold_days']);free[row['station_pool']][row['station_slot']]=carrier
    # Preparation must precede day-30 dispatch; every initial carrier return must
    # precede commissioning at day0, without shifting the plant calendar.
    initial_margin=min(initial_margin,-max(r['return_arrival'] for r in rows if r['initial']))
    capacity={}
    for kind in counts:
        rr=[r for r in rows if r['kind']==kind];dirty=[r for r in rr if not r['initial']]
        queue=[(r['return_arrival'],r['service_pickup']) for r in dirty];stored=[(r['storage_arrival'],r['release']) for r in dirty]
        capacity[kind]=dict(clean=peak([(r['receipt'],r['withdraw']) for r in rr])+(kind!='bundle'),queue=peak(queue),stored=peak(stored),dirty=peak(queue+stored))
    return dict(capacity=capacity,initial_margin=initial_margin,ready_margin=ready_margin,jobs=rows,carrier_jobs=route,spares=spares,
                jobs_after_shutdown=sum(r.get('service_end',0)>N for r in rows),last_release=max((r['release']/DAYS for r in rows if not r['initial']),default=0.))


DIRECTIONS = ('east', 'north', 'west', 'south')
ROOM_ENVELOPES = {'turbine_hall':'turbine','cryo_coldbox':'cryo_coldbox','cryo_compressors':'cryo_compressors','fuel_building':'fuel','reactor_auxiliaries':'reactor_aux','power_supply_building':'power_supply','electrical_building':'onsite_ac','service_water_building':'service_water','maintenance_shop':'conventional_shop','site_services_building':'site_services'}
ROOMS = ('reactor_hall',) + tuple('sector_wing_'+d for d in DIRECTIONS) + tuple('sector_link_'+d for d in DIRECTIONS) + ('cooling_hall','cooling_annex','cooling_link') + tuple(ROOM_ENVELOPES) + ('administration','control','security')
SELECTED = tuple('selected_'+r+'_'+d for r in ROOMS for d in ('length','width','height')) + tuple('selected_cooling_'+k+'_store_width' for k in ('helium','salt','bundle')) + ('selected_cooling_annex_north_depth','selected_blanket_packages_per_sector','selected_parcel_x_min','selected_parcel_y_min','selected_parcel_length','selected_parcel_width')
NEW_OUTPUTS = ('geometry_fit_margin_m','occupancy_area_margin_m2','parcel_fit_margin_m','blanket_packages_required_per_sector','required_parcel_x_min','required_parcel_y_min','required_parcel_x_max','required_parcel_y_max') + tuple(r+'_required_'+d for r in ROOMS if r not in ('administration','control','security') for d in ('length','width','height')) + tuple(r+'_required_'+d for r in ('administration','control','security') for d in ('area','height'))


def geometry(x, allocated):
    """Evaluate supplied civil solids. Requirements never select a room or partition."""
    t=x['nuclear_wall'];tc=x['conventional_wall']; c=x['sector_route_clearance']
    b=x['major_radius']+x['minor_outer_radius']+x['exterior_allowance']
    sw=math.sqrt(2)*b;sh=2*(x['minor_outer_radius']+x['exterior_allowance'])
    q={};ledgers={};rects={};req={};fits={};routes={}
    def size(name):
        return tuple(x['selected_'+name+'_'+a] for a in ('length','width','height'))
    def requirement(name, L, W, H):
        req[name]=(L,W,H)
        for a,offer,need in zip(('length','width','height'),size(name),(L,W,H)):
            fits[name+'_'+a]=offer-need
    def add(name,nuclear=False,partitions=(),holes=(),link=False):
        L,W,H=size(name)
        prefix='nuclear_' if nuclear else 'conventional_'
        wall=x[prefix+'wall']
        if any(not (0<=a<cc<=L and 0<=bb<dd<=W) for a,bb,cc,dd in partitions):
            raise ValueError(name+': partition outside supplied room')
        if any(w<=0 or h<=0 or h>H or w>max(L,W) for w,h in holes):
            raise ValueError(name+': impossible wall aperture')
        vals,ledger=civil(L,W,H,wall,x[prefix+'floor'],x[prefix+'roof'],x[prefix+'rebar_density'],partitions,holes,link)
        if any(v<0 for v in vals.values()):raise ValueError(name+': invalid civil solid')
        q[name]=vals;ledgers[name]=ledger
    # Four selected passages through the hall; their sizes are hardware, not demand.
    hall_holes=[(size('sector_link_'+d)[1],min(size('sector_link_'+d)[2],size('reactor_hall')[2])) for d in DIRECTIONS]
    add('reactor_hall',True,holes=hall_holes)
    requirement('reactor_hall',4*b+4,4*b+4,sh+x['sector_headroom'])
    storage_L=max(math.ceil((allocated['clean_positions_allocated']+2)/4)*6+12+2*t,math.ceil((allocated['dirty_buffer_positions_allocated']+allocated['dirty_store_positions_allocated']+4)/4)*6+12+2*t)
    for d in DIRECTIONS:
        name='sector_wing_'+d;L,W,H=size(name);lane=W-56-2*t
        if lane<=0:raise ValueError(name+': nonpositive installed lane')
        parts=[(0,28,L,28+t),(0,28+t+lane,L,28+2*t+lane)]
        for lo,hi in [(28,28+t),(28+t+lane,28+2*t+lane)]:
            if lo==28:
                near=lo;far=near-6-t;parts.extend([(0,far,t,near),(6+t,far,6+2*t,near),(t,far,6+t,far+t)])
            else:
                near=hi;far=near+6;parts.extend([(0,near,t,far+t),(6+t,near,6+2*t,far+t),(t,far,6+t,far+t)])
        add(name,True,parts,[(lane,H)]+[(6,6)]*6)
        requirement(name,max(b+2*c,storage_L),sw+2*c+56+2*t,sh+x['sector_headroom'])
        link='sector_link_'+d;ll,lw,lh=size(link);add(link,True,link=True)
        requirement(link,0.,sw+2*c,sh+x['sector_headroom'])
        # A wider/taller passage than either receiving room cannot connect.
        hall_side=size('reactor_hall')[1 if d in ('east','west') else 0]
        fits[link+'_hall_opening']=hall_side-lw
        fits[link+'_wing_opening']=lane-lw
        fits[link+'_hall_height']=size('reactor_hall')[2]-lh
        fits[link+'_wing_height']=H-lh
    a=x['cooling_aisle_width'];cross=x['cooling_cross_width'];m=x['cooling_package_margin']
    bl=x['hx_tube_length']+2*m;bw=x['hx_shell_bore']+2*m;bh=x['hx_shell_bore']+m
    ml=max(x['helium_package_length'],x['salt_package_length'])+2*m
    cellw=a+2*(max(x['helium_package_width'],x['salt_package_width'])+.6)
    celll=x['hx_shell_length']+2*x['hx_end_allowance']+bl+2*m+2*ml
    requirement('cooling_hall',math.ceil(x['cooling_circuits']/2)*cellw,2*celll+cross,max(x['cooling_headroom'],bh,x['helium_package_height']+m,x['salt_package_height']+m))
    add('cooling_hall',holes=[(cross,size('cooling_hall')[2])])
    dims={'helium':(x['helium_package_length'],x['helium_package_width'],x['helium_package_height']), 'salt':(x['salt_package_length'],x['salt_package_width'],x['salt_package_height']), 'bundle':(x['hx_tube_length'],x['hx_shell_bore'],x['hx_shell_bore'])}
    al,aw,ah=size('cooling_annex')  # Historical takeoff uses length across strips, width along storage.
    north=x['selected_cooling_annex_north_depth'];south=aw-north
    widths=[x['selected_cooling_'+k+'_store_width'] for k in dims]
    service=al-sum(widths)-3*tc;air=x['cooling_airlock_length'];reserve=cross/2+air+2*tc
    if min(service,north-reserve,south-reserve)<=0:raise ValueError('cooling annex: crossing partitions or nonpositive service region')
    required_widths=[];north_needs=[];south_needs=[];store_routes=[];carried={};xp=0.
    for (kind,(l,w,h)),width in zip(dims.items(),widths):
        required_widths.append(2*(w+2*m)+a)
        clean=math.ceil(allocated['cooling_clean_'+kind+'_allocated']/2)*(l+2*m)+a
        dirty=math.ceil(allocated['cooling_dirty_'+kind+'_allocated']/2)*(l+2*m)+a
        north_needs.append(clean);south_needs.append(dirty)
        fits[kind+'_storage_width']=width-required_widths[-1]
        fits[kind+'_clean_storage_depth']=north-reserve-clean
        fits[kind+'_dirty_storage_depth']=south-reserve-dirty
        carried[kind]=(l+2*m,w+2*m,h+m)
        store_routes.append(dict(kind=kind,center_x=xp+width/2,clear_width=width,pitch=l+2*m,clean_positions=allocated['cooling_clean_'+kind+'_allocated'],dirty_positions=allocated['cooling_dirty_'+kind+'_allocated']))
        xp+=width+tc
    service_need=2*(max(v[1] for v in carried.values())+2*m)+a
    service_depth=ml+bl+10*m
    fits['service_width']=service-service_need;fits['service_depth']=south-reserve-service_depth
    requirement('cooling_annex',sum(required_widths)+service_need+3*tc,2*reserve+max(north_needs)+max(max(south_needs),service_depth),max(x['cooling_headroom'],*(v[2] for v in carried.values())))
    parts=[(0,y+south,al,y+south+tc) for y in (-cross/2-tc,cross/2,-cross/2-air-2*tc,cross/2+air+tc)]
    xp=0.
    for width in widths:
        xp+=width;parts.extend([(xp,0,xp+tc,south-cross/2),(xp,south+cross/2,xp+tc,aw)]);xp+=tc
    add('cooling_annex',partitions=parts,holes=[(cross,ah)]*2+[(6,ah)]*14)
    add('cooling_link',link=True)
    requirement('cooling_link',0.,cross,max(x['cooling_headroom'],*(v[2] for v in carried.values())))
    fits['cooling_link_hall_width']=cross-size('cooling_link')[1]
    fits['cooling_link_annex_width']=cross-size('cooling_link')[1]
    fits['cooling_link_height']=min(size('cooling_hall')[2],ah)-size('cooling_link')[2]
    for name,stem in ROOM_ENVELOPES.items():
        scale=x['provisional_envelope_scale'];requirement(name,x[stem+'_length']*scale+4,x[stem+'_width']*scale+4,x[stem+'_height']*scale+3)
        add(name,name=='fuel_building')
    area_margins={}
    for name in ('administration','control','security'):
        add(name);need=x[name+'_occupants']*x[name+'_area_per_person']*x['occupancy_circulation_factor']
        area_margins[name]=q[name]['clear_area']-need;fits[name+'_height']=size(name)[2]-x['occupancy_height']
    # Fixed attachment/row conventions use supplied outer faces only.
    hx=(size('reactor_hall')[0]+2*t)/2;hy=(size('reactor_hall')[1]+2*t)/2
    rects['reactor_hall']=[-hx,-hy,hx,hy]
    for d in DIRECTIONS:
        L,W,H=size('sector_wing_'+d);ll,lw,lh=size('sector_link_'+d);outerL=L+2*t;outerW=W+2*t
        h=hx if d in ('east','west') else hy
        wing=[h+ll,-outerW/2,h+ll+outerL,outerW/2];link=[h,-lw/2-t,h+ll,lw/2+t]
        turn=DIRECTIONS.index(d)
        for stem,box in [('sector_wing_',wing),('sector_link_',link)]:
            corners=[(xx,yy) for xx in (box[0],box[2]) for yy in (box[1],box[3])]
            for _ in range(turn):corners=[(-yy,xx) for xx,yy in corners]
            rects[stem+d]=[min(xx for xx,yy in corners),min(yy for xx,yy in corners),max(xx for xx,yy in corners),max(yy for xx,yy in corners)]
    gap=x['building_separation'];cx=max(r[2] for r in rects.values())+gap
    cl,cw,ch=size('cooling_hall');ll,lw,lh=size('cooling_link');ax=cx+cl+2*tc+ll
    rects['cooling_hall']=[cx,-cw/2-tc,cx+cl+2*tc,cw/2+tc]
    rects['cooling_link']=[cx+cl+2*tc,-lw/2-tc,ax,lw/2+tc]
    rects['cooling_annex']=[ax,-south-tc,ax+al+2*tc,north+tc]
    campusy=min(rects['reactor_hall'][1],*(rects['sector_wing_'+d][1] for d in DIRECTIONS))-gap;campusx=-hx
    for name in list(ROOM_ENVELOPES)+['administration','control','security']:
        wall=t if name=='fuel_building' else tc;L,W,H=size(name)
        rects[name]=[campusx,campusy-W-2*wall,campusx+L+2*wall,campusy];campusx+=L+2*wall+gap
    rects['heat_rejection_plot']=[campusx,campusy-x['heat_rejection_width'],campusx+x['heat_rejection_length'],campusy]
    access=x['external_access_width'];bounds=[min(r[0] for r in rects.values())-access,min(r[1] for r in rects.values())-access,max(r[2] for r in rects.values())+access,max(r[3] for r in rects.values())+access]
    parcel=[x['selected_parcel_x_min'],x['selected_parcel_y_min'],x['selected_parcel_x_min']+x['selected_parcel_length'],x['selected_parcel_y_min']+x['selected_parcel_width']]
    parcel_margin=min(bounds[0]-parcel[0],bounds[1]-parcel[1],parcel[2]-bounds[2],parcel[3]-bounds[3])
    overlaps=[]
    for i,(name,r) in enumerate(rects.items()):
        for other,s in list(rects.items())[i+1:]:
            dx=min(r[2],s[2])-max(r[0],s[0]);dy=min(r[3],s[3])-max(r[1],s[1])
            if dx>1e-9 and dy>1e-9:
                overlaps.append(dict(first=name,second=other,intrusion=min(dx,dy)));fits[name+'__'+other]=-min(dx,dy)
    pw=x['component_width']+2*x['component_handling_margin'];pl=x['component_length']+2*x['component_handling_margin'];ph=x['component_height']+2*x['component_handling_margin']
    routes.update(component_vessel_width=5-pw,component_vessel_height=3-ph,component_turn=c-math.hypot(pw,pl),component_airlock_width=6-pw,component_airlock_height=6-ph,sector_side=c-6)
    for kind,(length,width,height) in carried.items():
        routes.update({kind+'_aisle':a-width,kind+'_door':6-width,kind+'_cross':cross-length,kind+'_airlock':air-length,kind+'_headroom':min(size('cooling_hall')[2],ah)-height,kind+'_service_slot':(service-a)/2-width})
    controlled=q['reactor_hall']['air_volume']+q['fuel_building']['air_volume']
    for d in DIRECTIONS:
        L,W,H=size('sector_wing_'+d);lane=W-56-2*t
        controlled+=((lane+28)*L-(18*t+2*t*t))*H+q['sector_link_'+d]['air_volume']
    gout=dict(sector_length=b,sector_width=sw,sector_height=sh,parcel_area=x['selected_parcel_length']*x['selected_parcel_width'],controlled_air_volume=controlled,total_clear_area=sum(v['clear_area'] for v in q.values()),total_gross_area=sum(v['gross_area'] for v in q.values()),total_air_volume=sum(v['air_volume'] for v in q.values()),route_margin_m=min(routes.values()),geometry_fit_margin_m=min(fits.values()),occupancy_area_margin_m2=min(area_margins.values()),parcel_fit_margin_m=parcel_margin)
    for name,values in req.items():gout.update({name+'_required_'+axis:value for axis,value in zip(('length','width','height'),values)})
    for name in area_margins:gout.update({name+'_required_area':x[name+'_occupants']*x[name+'_area_per_person']*x['occupancy_circulation_factor'],name+'_required_height':x['occupancy_height']})
    gout.update(zip(('required_parcel_x_min','required_parcel_y_min','required_parcel_x_max','required_parcel_y_max'),bounds))
    return q,dict(civil=ledgers,rectangles=rects,parcel_bounds=parcel,required_parcel_bounds=bounds,cooling_store_routes=store_routes,cooling_carried_envelopes=carried,cooling_service_depth=service_depth,route_checks=routes,fit_checks=fits,occupancy_checks=area_margins,overlaps=overlaps,sector_clear_box=[b,sw,sh]),gout


def diagnostics(inputs):
    x=dict(inputs);out={k:0. for k in OUTPUT_NAMES}
    if not isinstance(x.get('facilities_enabled'),bool):raise ValueError('facilities_enabled must be Boolean')
    if any(isinstance(x[k],bool) or x[k] not in (0,1) for k in ('facilities_cost_mode',)):raise ValueError('facility modes must be binary')
    if not x['facilities_enabled'] and x['facilities_cost_mode']==1:raise ValueError('facility cost mode requires enabled layout')
    if not x['facilities_enabled']:
        out.update(initial_margin_days=1.,readiness_margin_days=1.,outage_margin_days=1.,capacity_margin_units=1.,route_margin_m=1.,geometry_fit_margin_m=1.,occupancy_area_margin_m2=1.,parcel_fit_margin_m=1.,unused_material_capacity=1.)
        return dict(outputs=out,active=False)
    for k,v in x.items():
        if k!='facilities_enabled' and (isinstance(v,bool) or not math.isfinite(v)):raise ValueError(k+' must be finite numeric')
    if x['n_mod']!=1 or x['sector_count']!=4 or x['calendar_mode']!=0:raise ValueError('facilities requires one module, four sectors, live calendar')
    zero_allowed={'facilities_cost_mode','calendar_q','calendar_count','calendar_unplanned','calendar_mode','calendar_outage','divertor_packages_per_sector','waste_package_yield','initial_sector_start_days','cooling_initial_handoff_days','component_remove_days','component_install_days','component_prepare_days','component_process_days','component_hold_days','sector_clean_days','sector_test_days','sector_split_days','sector_join_days','sector_transport_days','cooldown_days','recommission_days','cooling_hold_days','cooling_prepare_machine_days','cooling_prepare_bundle_days','cooling_machine_process_days','cooling_bundle_process_days','cooling_field_cycle_days','cooling_internal_move_days'}
    zero_allowed.update(k for k in PARAMETERS if k.endswith('_positions') or k in ('clean_positions','dirty_buffer_positions','dirty_store_positions','selected_blanket_packages_per_sector'))
    for k in PARAMETERS+UPSTREAM:
        if k in ('selected_parcel_x_min','selected_parcel_y_min'):continue
        if k not in zero_allowed and k!='facilities_enabled' and x[k]<=0:raise ValueError(k+' must be positive')
        if k in zero_allowed and k not in ('initial_sector_start_days','cooling_initial_handoff_days') and x[k]<0:raise ValueError(k+' cannot be negative')
    for k in ('sector_bays','sector_service_teams','cooling_prepare_stations','cooling_machine_stations','cooling_bundle_stations','cooling_circuits','cooling_helium_count','cooling_salt_count','cooling_bundle_count','selected_blanket_packages_per_sector','divertor_packages_per_sector','clean_positions','dirty_buffer_positions','dirty_store_positions','cooling_clean_helium_positions','cooling_clean_salt_positions','cooling_clean_bundle_positions','cooling_dirty_helium_positions','cooling_dirty_salt_positions','cooling_dirty_bundle_positions'):
        if x[k]!=int(x[k]):raise ValueError(k+' must be integer')
    if x['component_material_fraction']>1 or x['initial_sector_start_days']>=0 or x['cooling_initial_handoff_days']>=0:raise ValueError('invalid packing or preoperation deadline')
    cal=lifecycle_calendar_live(cost_per_event=0,q_n=x['calendar_q'],fluence_limit=x['calendar_fluence'],interest_rate=0,operational_years=x['calendar_years'],outage_years=x['calendar_outage'],unplanned_fraction=x['calendar_unplanned'],coil_life_fpy=x['calendar_years'])
    if not math.isclose(cal['n_replacements'],x['calendar_count'],abs_tol=1e-9) or not math.isclose(cal['availability'],x['calendar_availability'],rel_tol=1e-10):raise ValueError('facility calendar owner inputs disagree')
    vessel=vessel_schedule(x,cal['events']);cool=cooling_schedule(x);wings=vessel['wings'];count=vessel['packages']
    required={'clean_positions_allocated':max(w['clean'] for w in wings),'dirty_buffer_positions_allocated':max(w['buffer'] for w in wings),'dirty_store_positions_allocated':max(w['stored'] for w in wings)}
    for kind in ('helium','salt','bundle'):
        for zone in ('clean','dirty'):required['cooling_'+zone+'_'+kind+'_allocated']=cool['capacity'][kind][zone]
    allocated={k:x[k.replace('_allocated','_positions') if k.startswith('cooling_') else k.replace('_allocated','')] for k in required}
    quantities,geo,gout=geometry(x,allocated)
    material=4*vessel['blanket']*x['component_material_fraction']*x['component_width']*x['component_height']*x['component_length']
    out.update(active=1.,cost_mode=x['facilities_cost_mode'],blanket_packages_per_sector=vessel['blanket'],packages_per_sector=count,material_capacity_volume=material,unused_material_capacity=material-x['blanket_volume'],initial_clean_required=required['clean_positions_allocated'],dirty_buffer_required=required['dirty_buffer_positions_allocated'],dirty_store_required=required['dirty_store_positions_allocated'],initial_ready_margin_days=vessel['initial_margin'],replacement_ready_margin_days=vessel['ready_margin'],outage_required_days=vessel['outage'],outage_allowed_days=x['calendar_outage']*DAYS,outage_margin_days=x['calendar_outage']*DAYS-vessel['outage'] if cal['events'] else x['calendar_years']*DAYS,calendar_event_count=len(cal['events']),calendar_first_event_year=cal['events'][0] if cal['events'] else 0.,calendar_last_event_year=cal['events'][-1] if cal['events'] else 0.,cooling_initial_ready_margin_days=cool['initial_margin'],cooling_replacement_ready_margin_days=cool['ready_margin'],cooling_jobs_after_shutdown=cool['jobs_after_shutdown'],cooling_last_release_year=cool['last_release'],cooling_carrier_moves=len(cool['carrier_jobs']),initial_margin_days=min(vessel['initial_margin'],cool['initial_margin']),readiness_margin_days=min(vessel['ready_margin'],cool['ready_margin']),capacity_margin_units=min(x['sector_bays']-4,2-x['cooling_machine_stations'],2-x['cooling_bundle_stations'],*[allocated[k]-v for k,v in required.items()]),provisional_room_count=13.)
    out['blanket_packages_required_per_sector']=math.ceil(x['blanket_volume']/(4*x['component_material_fraction']*x['component_width']*x['component_height']*x['component_length']))
    out.update(allocated);out.update(gout)
    for kind in ('helium','salt','bundle'):
        for zone in ('clean','dirty'):out['cooling_'+zone+'_'+kind+'_required']=cool['capacity'][kind][zone]
        out['cooling_'+kind+'_queue_peak']=cool['capacity'][kind]['queue']
    for name,qty in quantities.items():out.update({name+'_'+k:v for k,v in qty.items()})
    if set(out)!=set(OUTPUT_NAMES) or not all(math.isfinite(v) for v in out.values()):raise ValueError('nonfinite or undeclared facility output')
    return dict(outputs=out,calendar=cal,vessel=vessel,cooling=cool,geometry=geo)


def calculate(inputs):
    return diagnostics(inputs)['outputs']

OUTPUT_NAMES = ['active', 'cost_mode', 'sector_length', 'sector_width', 'sector_height', 'parcel_area', 'controlled_air_volume', 'total_clear_area', 'total_gross_area', 'total_air_volume', 'blanket_packages_per_sector', 'packages_per_sector', 'material_capacity_volume', 'unused_material_capacity', 'initial_clean_required', 'dirty_buffer_required', 'dirty_store_required', 'initial_ready_margin_days', 'replacement_ready_margin_days', 'outage_required_days', 'outage_allowed_days', 'outage_margin_days', 'calendar_event_count', 'calendar_first_event_year', 'calendar_last_event_year', 'cooling_clean_helium_required', 'cooling_clean_salt_required', 'cooling_clean_bundle_required', 'cooling_dirty_helium_required', 'cooling_dirty_salt_required', 'cooling_dirty_bundle_required', 'cooling_helium_queue_peak', 'cooling_salt_queue_peak', 'cooling_bundle_queue_peak', 'cooling_initial_ready_margin_days', 'cooling_replacement_ready_margin_days', 'cooling_jobs_after_shutdown', 'cooling_last_release_year', 'cooling_carrier_moves', 'clean_positions_allocated', 'dirty_buffer_positions_allocated', 'dirty_store_positions_allocated', 'cooling_clean_helium_allocated', 'cooling_clean_salt_allocated', 'cooling_clean_bundle_allocated', 'cooling_dirty_helium_allocated', 'cooling_dirty_salt_allocated', 'cooling_dirty_bundle_allocated', 'initial_margin_days', 'readiness_margin_days', 'capacity_margin_units', 'route_margin_m', 'exterior_envelope_qualified', 'sector_load_qualified', 'contamination_procedure_qualified', 'cooling_outage_basis_resolved', 'provisional_room_count', 'reactor_hall_clear_length', 'reactor_hall_clear_width', 'reactor_hall_clear_height', 'reactor_hall_clear_area', 'reactor_hall_gross_area', 'reactor_hall_air_volume', 'reactor_hall_sub_concrete', 'reactor_hall_super_concrete', 'reactor_hall_sub_formwork', 'reactor_hall_super_formwork', 'reactor_hall_sub_rebar', 'reactor_hall_super_rebar', 'sector_wing_east_clear_length', 'sector_wing_east_clear_width', 'sector_wing_east_clear_height', 'sector_wing_east_clear_area', 'sector_wing_east_gross_area', 'sector_wing_east_air_volume', 'sector_wing_east_sub_concrete', 'sector_wing_east_super_concrete', 'sector_wing_east_sub_formwork', 'sector_wing_east_super_formwork', 'sector_wing_east_sub_rebar', 'sector_wing_east_super_rebar', 'sector_wing_north_clear_length', 'sector_wing_north_clear_width', 'sector_wing_north_clear_height', 'sector_wing_north_clear_area', 'sector_wing_north_gross_area', 'sector_wing_north_air_volume', 'sector_wing_north_sub_concrete', 'sector_wing_north_super_concrete', 'sector_wing_north_sub_formwork', 'sector_wing_north_super_formwork', 'sector_wing_north_sub_rebar', 'sector_wing_north_super_rebar', 'sector_wing_west_clear_length', 'sector_wing_west_clear_width', 'sector_wing_west_clear_height', 'sector_wing_west_clear_area', 'sector_wing_west_gross_area', 'sector_wing_west_air_volume', 'sector_wing_west_sub_concrete', 'sector_wing_west_super_concrete', 'sector_wing_west_sub_formwork', 'sector_wing_west_super_formwork', 'sector_wing_west_sub_rebar', 'sector_wing_west_super_rebar', 'sector_wing_south_clear_length', 'sector_wing_south_clear_width', 'sector_wing_south_clear_height', 'sector_wing_south_clear_area', 'sector_wing_south_gross_area', 'sector_wing_south_air_volume', 'sector_wing_south_sub_concrete', 'sector_wing_south_super_concrete', 'sector_wing_south_sub_formwork', 'sector_wing_south_super_formwork', 'sector_wing_south_sub_rebar', 'sector_wing_south_super_rebar', 'sector_link_east_clear_length', 'sector_link_east_clear_width', 'sector_link_east_clear_height', 'sector_link_east_clear_area', 'sector_link_east_gross_area', 'sector_link_east_air_volume', 'sector_link_east_sub_concrete', 'sector_link_east_super_concrete', 'sector_link_east_sub_formwork', 'sector_link_east_super_formwork', 'sector_link_east_sub_rebar', 'sector_link_east_super_rebar', 'sector_link_north_clear_length', 'sector_link_north_clear_width', 'sector_link_north_clear_height', 'sector_link_north_clear_area', 'sector_link_north_gross_area', 'sector_link_north_air_volume', 'sector_link_north_sub_concrete', 'sector_link_north_super_concrete', 'sector_link_north_sub_formwork', 'sector_link_north_super_formwork', 'sector_link_north_sub_rebar', 'sector_link_north_super_rebar', 'sector_link_west_clear_length', 'sector_link_west_clear_width', 'sector_link_west_clear_height', 'sector_link_west_clear_area', 'sector_link_west_gross_area', 'sector_link_west_air_volume', 'sector_link_west_sub_concrete', 'sector_link_west_super_concrete', 'sector_link_west_sub_formwork', 'sector_link_west_super_formwork', 'sector_link_west_sub_rebar', 'sector_link_west_super_rebar', 'sector_link_south_clear_length', 'sector_link_south_clear_width', 'sector_link_south_clear_height', 'sector_link_south_clear_area', 'sector_link_south_gross_area', 'sector_link_south_air_volume', 'sector_link_south_sub_concrete', 'sector_link_south_super_concrete', 'sector_link_south_sub_formwork', 'sector_link_south_super_formwork', 'sector_link_south_sub_rebar', 'sector_link_south_super_rebar', 'cooling_hall_clear_length', 'cooling_hall_clear_width', 'cooling_hall_clear_height', 'cooling_hall_clear_area', 'cooling_hall_gross_area', 'cooling_hall_air_volume', 'cooling_hall_sub_concrete', 'cooling_hall_super_concrete', 'cooling_hall_sub_formwork', 'cooling_hall_super_formwork', 'cooling_hall_sub_rebar', 'cooling_hall_super_rebar', 'cooling_annex_clear_length', 'cooling_annex_clear_width', 'cooling_annex_clear_height', 'cooling_annex_clear_area', 'cooling_annex_gross_area', 'cooling_annex_air_volume', 'cooling_annex_sub_concrete', 'cooling_annex_super_concrete', 'cooling_annex_sub_formwork', 'cooling_annex_super_formwork', 'cooling_annex_sub_rebar', 'cooling_annex_super_rebar', 'cooling_link_clear_length', 'cooling_link_clear_width', 'cooling_link_clear_height', 'cooling_link_clear_area', 'cooling_link_gross_area', 'cooling_link_air_volume', 'cooling_link_sub_concrete', 'cooling_link_super_concrete', 'cooling_link_sub_formwork', 'cooling_link_super_formwork', 'cooling_link_sub_rebar', 'cooling_link_super_rebar', 'turbine_hall_clear_length', 'turbine_hall_clear_width', 'turbine_hall_clear_height', 'turbine_hall_clear_area', 'turbine_hall_gross_area', 'turbine_hall_air_volume', 'turbine_hall_sub_concrete', 'turbine_hall_super_concrete', 'turbine_hall_sub_formwork', 'turbine_hall_super_formwork', 'turbine_hall_sub_rebar', 'turbine_hall_super_rebar', 'cryo_coldbox_clear_length', 'cryo_coldbox_clear_width', 'cryo_coldbox_clear_height', 'cryo_coldbox_clear_area', 'cryo_coldbox_gross_area', 'cryo_coldbox_air_volume', 'cryo_coldbox_sub_concrete', 'cryo_coldbox_super_concrete', 'cryo_coldbox_sub_formwork', 'cryo_coldbox_super_formwork', 'cryo_coldbox_sub_rebar', 'cryo_coldbox_super_rebar', 'cryo_compressors_clear_length', 'cryo_compressors_clear_width', 'cryo_compressors_clear_height', 'cryo_compressors_clear_area', 'cryo_compressors_gross_area', 'cryo_compressors_air_volume', 'cryo_compressors_sub_concrete', 'cryo_compressors_super_concrete', 'cryo_compressors_sub_formwork', 'cryo_compressors_super_formwork', 'cryo_compressors_sub_rebar', 'cryo_compressors_super_rebar', 'fuel_building_clear_length', 'fuel_building_clear_width', 'fuel_building_clear_height', 'fuel_building_clear_area', 'fuel_building_gross_area', 'fuel_building_air_volume', 'fuel_building_sub_concrete', 'fuel_building_super_concrete', 'fuel_building_sub_formwork', 'fuel_building_super_formwork', 'fuel_building_sub_rebar', 'fuel_building_super_rebar', 'reactor_auxiliaries_clear_length', 'reactor_auxiliaries_clear_width', 'reactor_auxiliaries_clear_height', 'reactor_auxiliaries_clear_area', 'reactor_auxiliaries_gross_area', 'reactor_auxiliaries_air_volume', 'reactor_auxiliaries_sub_concrete', 'reactor_auxiliaries_super_concrete', 'reactor_auxiliaries_sub_formwork', 'reactor_auxiliaries_super_formwork', 'reactor_auxiliaries_sub_rebar', 'reactor_auxiliaries_super_rebar', 'power_supply_building_clear_length', 'power_supply_building_clear_width', 'power_supply_building_clear_height', 'power_supply_building_clear_area', 'power_supply_building_gross_area', 'power_supply_building_air_volume', 'power_supply_building_sub_concrete', 'power_supply_building_super_concrete', 'power_supply_building_sub_formwork', 'power_supply_building_super_formwork', 'power_supply_building_sub_rebar', 'power_supply_building_super_rebar', 'electrical_building_clear_length', 'electrical_building_clear_width', 'electrical_building_clear_height', 'electrical_building_clear_area', 'electrical_building_gross_area', 'electrical_building_air_volume', 'electrical_building_sub_concrete', 'electrical_building_super_concrete', 'electrical_building_sub_formwork', 'electrical_building_super_formwork', 'electrical_building_sub_rebar', 'electrical_building_super_rebar', 'service_water_building_clear_length', 'service_water_building_clear_width', 'service_water_building_clear_height', 'service_water_building_clear_area', 'service_water_building_gross_area', 'service_water_building_air_volume', 'service_water_building_sub_concrete', 'service_water_building_super_concrete', 'service_water_building_sub_formwork', 'service_water_building_super_formwork', 'service_water_building_sub_rebar', 'service_water_building_super_rebar', 'maintenance_shop_clear_length', 'maintenance_shop_clear_width', 'maintenance_shop_clear_height', 'maintenance_shop_clear_area', 'maintenance_shop_gross_area', 'maintenance_shop_air_volume', 'maintenance_shop_sub_concrete', 'maintenance_shop_super_concrete', 'maintenance_shop_sub_formwork', 'maintenance_shop_super_formwork', 'maintenance_shop_sub_rebar', 'maintenance_shop_super_rebar', 'site_services_building_clear_length', 'site_services_building_clear_width', 'site_services_building_clear_height', 'site_services_building_clear_area', 'site_services_building_gross_area', 'site_services_building_air_volume', 'site_services_building_sub_concrete', 'site_services_building_super_concrete', 'site_services_building_sub_formwork', 'site_services_building_super_formwork', 'site_services_building_sub_rebar', 'site_services_building_super_rebar', 'administration_clear_length', 'administration_clear_width', 'administration_clear_height', 'administration_clear_area', 'administration_gross_area', 'administration_air_volume', 'administration_sub_concrete', 'administration_super_concrete', 'administration_sub_formwork', 'administration_super_formwork', 'administration_sub_rebar', 'administration_super_rebar', 'control_clear_length', 'control_clear_width', 'control_clear_height', 'control_clear_area', 'control_gross_area', 'control_air_volume', 'control_sub_concrete', 'control_super_concrete', 'control_sub_formwork', 'control_super_formwork', 'control_sub_rebar', 'control_super_rebar', 'security_clear_length', 'security_clear_width', 'security_clear_height', 'security_clear_area', 'security_gross_area', 'security_air_volume', 'security_sub_concrete', 'security_super_concrete', 'security_sub_formwork', 'security_super_formwork', 'security_sub_rebar', 'security_super_rebar', 'geometry_fit_margin_m', 'occupancy_area_margin_m2', 'parcel_fit_margin_m', 'blanket_packages_required_per_sector', 'required_parcel_x_min', 'required_parcel_y_min', 'required_parcel_x_max', 'required_parcel_y_max', 'reactor_hall_required_length', 'reactor_hall_required_width', 'reactor_hall_required_height', 'sector_wing_east_required_length', 'sector_wing_east_required_width', 'sector_wing_east_required_height', 'sector_wing_north_required_length', 'sector_wing_north_required_width', 'sector_wing_north_required_height', 'sector_wing_west_required_length', 'sector_wing_west_required_width', 'sector_wing_west_required_height', 'sector_wing_south_required_length', 'sector_wing_south_required_width', 'sector_wing_south_required_height', 'sector_link_east_required_length', 'sector_link_east_required_width', 'sector_link_east_required_height', 'sector_link_north_required_length', 'sector_link_north_required_width', 'sector_link_north_required_height', 'sector_link_west_required_length', 'sector_link_west_required_width', 'sector_link_west_required_height', 'sector_link_south_required_length', 'sector_link_south_required_width', 'sector_link_south_required_height', 'cooling_hall_required_length', 'cooling_hall_required_width', 'cooling_hall_required_height', 'cooling_annex_required_length', 'cooling_annex_required_width', 'cooling_annex_required_height', 'cooling_link_required_length', 'cooling_link_required_width', 'cooling_link_required_height', 'turbine_hall_required_length', 'turbine_hall_required_width', 'turbine_hall_required_height', 'cryo_coldbox_required_length', 'cryo_coldbox_required_width', 'cryo_coldbox_required_height', 'cryo_compressors_required_length', 'cryo_compressors_required_width', 'cryo_compressors_required_height', 'fuel_building_required_length', 'fuel_building_required_width', 'fuel_building_required_height', 'reactor_auxiliaries_required_length', 'reactor_auxiliaries_required_width', 'reactor_auxiliaries_required_height', 'power_supply_building_required_length', 'power_supply_building_required_width', 'power_supply_building_required_height', 'electrical_building_required_length', 'electrical_building_required_width', 'electrical_building_required_height', 'service_water_building_required_length', 'service_water_building_required_width', 'service_water_building_required_height', 'maintenance_shop_required_length', 'maintenance_shop_required_width', 'maintenance_shop_required_height', 'site_services_building_required_length', 'site_services_building_required_width', 'site_services_building_required_height', 'administration_required_area', 'administration_required_height', 'control_required_area', 'control_required_height', 'security_required_area', 'security_required_height']
PARAMETERS = ['facilities_enabled', 'facilities_cost_mode', 'sector_count', 'sector_bays', 'sector_service_teams', 'exterior_allowance', 'sector_route_clearance', 'sector_headroom', 'component_width', 'component_height', 'component_length', 'component_handling_margin', 'component_material_fraction', 'divertor_packages_per_sector', 'waste_package_yield', 'component_remove_days', 'component_install_days', 'sector_clean_days', 'sector_test_days', 'sector_split_days', 'sector_join_days', 'sector_transport_days', 'cooldown_days', 'recommission_days', 'initial_receipt_lead_days', 'initial_sector_start_days', 'component_receipt_lead_days', 'component_prepare_days', 'component_process_days', 'component_hold_days', 'clean_positions', 'dirty_buffer_positions', 'dirty_store_positions', 'cooling_initial_receipt_lead_days', 'cooling_initial_handoff_days', 'cooling_receipt_lead_days', 'cooling_hold_days', 'cooling_prepare_stations', 'cooling_machine_stations', 'cooling_bundle_stations', 'cooling_prepare_machine_days', 'cooling_prepare_bundle_days', 'cooling_machine_process_days', 'cooling_bundle_process_days', 'cooling_field_cycle_days', 'cooling_internal_move_days', 'cooling_clean_helium_positions', 'cooling_clean_salt_positions', 'cooling_clean_bundle_positions', 'cooling_dirty_helium_positions', 'cooling_dirty_salt_positions', 'cooling_dirty_bundle_positions', 'helium_package_length', 'helium_package_width', 'helium_package_height', 'salt_package_length', 'salt_package_width', 'salt_package_height', 'hx_end_allowance', 'cooling_package_margin', 'cooling_aisle_width', 'cooling_cross_width', 'cooling_headroom', 'cooling_airlock_length', 'nuclear_wall', 'nuclear_floor', 'nuclear_roof', 'nuclear_rebar_density', 'conventional_wall', 'conventional_floor', 'conventional_roof', 'conventional_rebar_density', 'building_separation', 'external_access_width', 'provisional_envelope_scale', 'administration_occupants', 'control_occupants', 'security_occupants', 'administration_area_per_person', 'control_area_per_person', 'security_area_per_person', 'occupancy_circulation_factor', 'occupancy_height', 'heat_rejection_length', 'heat_rejection_width', 'turbine_length', 'turbine_width', 'turbine_height', 'cryo_coldbox_length', 'cryo_coldbox_width', 'cryo_coldbox_height', 'cryo_compressors_length', 'cryo_compressors_width', 'cryo_compressors_height', 'fuel_length', 'fuel_width', 'fuel_height', 'reactor_aux_length', 'reactor_aux_width', 'reactor_aux_height', 'power_supply_length', 'power_supply_width', 'power_supply_height', 'onsite_ac_length', 'onsite_ac_width', 'onsite_ac_height', 'service_water_length', 'service_water_width', 'service_water_height', 'conventional_shop_length', 'conventional_shop_width', 'conventional_shop_height', 'site_services_length', 'site_services_width', 'site_services_height', 'selected_reactor_hall_length', 'selected_reactor_hall_width', 'selected_reactor_hall_height', 'selected_sector_wing_east_length', 'selected_sector_wing_east_width', 'selected_sector_wing_east_height', 'selected_sector_wing_north_length', 'selected_sector_wing_north_width', 'selected_sector_wing_north_height', 'selected_sector_wing_west_length', 'selected_sector_wing_west_width', 'selected_sector_wing_west_height', 'selected_sector_wing_south_length', 'selected_sector_wing_south_width', 'selected_sector_wing_south_height', 'selected_sector_link_east_length', 'selected_sector_link_east_width', 'selected_sector_link_east_height', 'selected_sector_link_north_length', 'selected_sector_link_north_width', 'selected_sector_link_north_height', 'selected_sector_link_west_length', 'selected_sector_link_west_width', 'selected_sector_link_west_height', 'selected_sector_link_south_length', 'selected_sector_link_south_width', 'selected_sector_link_south_height', 'selected_cooling_hall_length', 'selected_cooling_hall_width', 'selected_cooling_hall_height', 'selected_cooling_annex_length', 'selected_cooling_annex_width', 'selected_cooling_annex_height', 'selected_cooling_link_length', 'selected_cooling_link_width', 'selected_cooling_link_height', 'selected_turbine_hall_length', 'selected_turbine_hall_width', 'selected_turbine_hall_height', 'selected_cryo_coldbox_length', 'selected_cryo_coldbox_width', 'selected_cryo_coldbox_height', 'selected_cryo_compressors_length', 'selected_cryo_compressors_width', 'selected_cryo_compressors_height', 'selected_fuel_building_length', 'selected_fuel_building_width', 'selected_fuel_building_height', 'selected_reactor_auxiliaries_length', 'selected_reactor_auxiliaries_width', 'selected_reactor_auxiliaries_height', 'selected_power_supply_building_length', 'selected_power_supply_building_width', 'selected_power_supply_building_height', 'selected_electrical_building_length', 'selected_electrical_building_width', 'selected_electrical_building_height', 'selected_service_water_building_length', 'selected_service_water_building_width', 'selected_service_water_building_height', 'selected_maintenance_shop_length', 'selected_maintenance_shop_width', 'selected_maintenance_shop_height', 'selected_site_services_building_length', 'selected_site_services_building_width', 'selected_site_services_building_height', 'selected_administration_length', 'selected_administration_width', 'selected_administration_height', 'selected_control_length', 'selected_control_width', 'selected_control_height', 'selected_security_length', 'selected_security_width', 'selected_security_height', 'selected_cooling_helium_store_width', 'selected_cooling_salt_store_width', 'selected_cooling_bundle_store_width', 'selected_cooling_annex_north_depth', 'selected_blanket_packages_per_sector', 'selected_parcel_x_min', 'selected_parcel_y_min', 'selected_parcel_length', 'selected_parcel_width']
UPSTREAM = ['n_mod', 'major_radius', 'minor_outer_radius', 'blanket_volume', 'calendar_q', 'calendar_fluence', 'calendar_years', 'calendar_outage', 'calendar_unplanned', 'calendar_mode', 'calendar_life', 'calendar_count', 'calendar_availability', 'cooling_circuits', 'cooling_helium_count', 'cooling_salt_count', 'cooling_bundle_count', 'cooling_machine_life', 'cooling_bundle_life', 'hx_shell_bore', 'hx_shell_wall', 'hx_shell_length', 'hx_tube_length']


def run_facility_layout(inputs: Facility_LayoutInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
    from stellarator_materials_reference_tea.schemas.facility_layout_output import Facility_LayoutOutput
    out=calculate({k.removesuffix('_in'):getattr(inputs,k) for k in type(inputs).model_fields})
    return tuple(out[name] for name in Facility_LayoutOutput.model_fields)
