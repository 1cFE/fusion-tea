"""Throwaway conceptual layout/capacity probe; no production implementation or cost model."""
import json, math, os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/pkg'))
sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from stellarator_tea.handwritten.mfe_lifecycle.lifecycle_calendar_impl import lifecycle_calendar_live
replay=json.loads((ROOT/'work/orchestration/goals/layout-based-facilities/evidence/entering-replay.json').read_text())
o=replay['cases'][0]['outputs']; prefix='stellarator_09__stellaris__'
def v(s): return o[prefix+s]
calendar=lifecycle_calendar_live(cost_per_event=v('replacement_cost_per_event__replacement_cost_per_event'),q_n=v('blanket__first_wall__wall_peak_calc__wall_load_peak'),fluence_limit=18,interest_rate=.07,operational_years=30,outage_years=7/12,unplanned_fraction=0,coil_life_fpy=10)
assert math.isclose(calendar['availability'],v('calendar__availability'),abs_tol=1e-14)

def peak(intervals):
    intervals=[(a,b) for a,b in intervals if b>a]
    events=sorted([(a,1) for a,b in intervals]+[(b,-1) for a,b in intervals])
    n=p=0
    for _,d in events:n+=d;p=max(p,n)
    return p

def run(step=.5,teams=2,hold=365.25,volume_factor=1,events=None,initial_lead=180):
    events=calendar["events"] if events is None else events
    # Four equal batch groups. Blanket packing and segmentation are assumptions.
    blank=math.ceil(v('rb__blanket_vol')*volume_factor/(4*.5*4*2*2))
    count=blank+4 # extra divertor packages per sector: assumed, not sourced
    service=count*2*step+14
    team=[0.]*teams; transport=37.; schedule=[]
    for j in range(4):
        transport+=2; k=min(range(teams),key=lambda t:team[t]); start=max(transport,team[k]); end=start+service;team[k]=end
        schedule.append(dict(sector=j,start=start,end=end,team=k))
    for s in sorted(schedule,key=lambda s:s['end']):transport=max(transport,s['end'])+2;s['return']=transport
    duration=transport+7+30
    pending=[]; storage=[]; station=[]; last_by_wing=[-math.inf]*4
    for date in events:
        for s in schedule:
            last=last_by_wing[s['sector']]
            for j in range(count):
                arrival=date*365.25+s['start']+(j+1)*step
                start=max(arrival,last);last=start+1
                pending.append((arrival,start));station.append((start,last));storage.append((last,last+hold))
            last_by_wing[s['sector']]=last
    # Per-wing capacity; no pooling of dirty routes/resources across wings.
    wing0=schedule[0]; pend0=[];store0=[]
    last=-math.inf;clean_last=-initial_lead+count;clean_inventory=[(-initial_lead,max(-120+(j+1)*step,clean_last)) for j in range(count)];clean_ready=clean_last<=-120
    initial_ready=clean_ready and (-120+math.ceil(4/teams)*(count*step+7)+8+37<=0)
    for date in events:
        receipt=date*365.25-90
        clean_last=max(clean_last,receipt)+count
        clean_ready=clean_ready and clean_last<=date*365.25+wing0['start']+count*step+7
        for j in range(count):
            arrival=date*365.25+wing0['start']+(j+1)*step;start=max(arrival,last);last=start+1
            if start>arrival:pend0.append((arrival,start))
            store0.append((last,last+hold))
            clean_inventory.append((receipt,date*365.25+wing0['start']+count*step+7+(j+1)*step))
    return dict(packages_per_sector=count,blanket_packages_per_sector=blank,service_days=service,sector_schedule=schedule,outage_required_days=duration,outage_offered_days=365.25*7/12,outage_ok=duration<=365.25*7/12,peak_buffer_per_wing=peak(pend0),peak_storage_per_wing=peak(store0),peak_storage_total=peak(storage),peak_clean_per_wing=peak(clean_inventory),initial_ready=initial_ready,clean_ready=clean_ready,calendar_event_years=events,availability_unchanged=calendar['availability'])
base=run();r=3.55;e=2.;outside=12.7+r+e;sl=outside;sw=math.sqrt(2)*outside;sh=2*(r+e);c=2.;bayw=sw+2*(2+c)
cleanw=dirtyw=28.
cleanl=math.ceil((base['packages_per_sector']+2)/4)*6+6
dirtyl=math.ceil((base['peak_buffer_per_wing']+base['peak_storage_per_wing']+4)/4)*6+6
wingl=max(sl+2*(2+c),cleanl,dirtyl);wingw=bayw+cleanw+dirtyw
hallside=2*max(outside+sl+c,wingw/2+c)
# Two banks of cells, draw each exchanger axially into its own unobstructed pull zone.
cellL=13+4+11.6+4+12; cellW=9.;circuits=14
coolL=2*cellL+5;coolW=math.ceil(circuits/2)*cellW
def store(k,l,w):return (math.ceil(k/2)*(l+2)+6,2*(w+2)+6)
cleanstores=[store(2*circuits+1,6,3),store(2*circuits+1,3,2),store(circuits,11.6,3.2)]
dirtystores=[store(2*circuits,6,3),store(2*circuits,3,2),store(circuits,11.6,3.2)]
annexL=max(s[0] for s in cleanstores+dirtystores)
annexW=sum(s[1] for s in cleanstores+dirtystores)+20.4
rooms={}
for name,L,W,H in [('turbine',60,20,15),('cryo_coldbox',20,12,10),('cryo_compressors',30,12,8),('fuel',30,20,8),('reactor_aux',30,20,10),('power_supply',20,10,8),('onsite_ac',16,8,6),('service_water',20,15,8),('conventional_shop',20,15,8),('site_services',20,10,6)]:rooms[name]=dict(L=L+4,W=W+4,H=H+3,provisional=True)
for name,A in [('administration',3120),('control',585),('security',156)]:rooms[name]=dict(L=math.sqrt(2*A),W=math.sqrt(A/2),H=4,provisional=True)
# Campus strip beyond the south wing; cooling hall + annex east beyond the east wing.
h=hallside/2
campusy=-(h+wingl+10)
x=-h;rects={}
for name,d in rooms.items():
    rects[name]=[x,campusy-d['W'],x+d['L'],campusy];x+=d['L']+10
rects['heat_rejection_plot']=[x,campusy-60,x+100,campusy]
rects['cooling_hall']=[h+wingl+10,-coolW/2,h+wingl+10+coolL,coolW/2]
rects['cooling_annex']=[h+wingl+10+coolL+10,-annexW/2,h+wingl+10+coolL+10+annexL,annexW/2]
parcel=[min(-h-wingl,min(r[0] for r in rects.values()))-12,min(-h-wingl,min(r[1] for r in rects.values()))-12,max(h+wingl,max(r[2] for r in rects.values()))+12,max(h+wingl,max(r[3] for r in rects.values()))+12]
for i,(name,a) in enumerate(rects.items()):
    for name2,b in list(rects.items())[i+1:]:assert a[2]<=b[0] or b[2]<=a[0] or a[3]<=b[1] or b[3]<=a[1],(name,name2)
result={'basis':'Current-default native q/volume/calendar, agent-selected layout/task assumptions; standalone probe only','calendar':calendar,'baseline':base,'geometry':dict(sector_L=sl,sector_W=sw,sector_H=sh,hall_side=hallside,hall_area=hallside**2,hall_height=sh+3,wing_length=wingl,wing_width=wingw,wing_height=sh+3,clean_annex_area=cleanw*wingl,dirty_annex_area=dirtyw*wingl,sector_lane_area=bayw*wingl,four_wings_area=4*wingl*wingw,cooling_hall_L=coolL,cooling_hall_W=coolW,cooling_hall_area=coolL*coolW,cooling_hall_height=9,cooling_annex_L=annexL,cooling_annex_W=annexW,cooling_annex_area=annexL*annexW), 'provisional_conventional_rooms':rooms,'placement_rectangles':rects,'parcel_bounds':parcel,'parcel_area':(parcel[2]-parcel[0])*(parcel[3]-parcel[1]), 'contrasts':{'one_team':run(teams=1),'slow_tasks':run(step=.75),'double_material':run(volume_factor=2),'six_year_storage':run(hold=6*365.25),'fast_tasks':run(step=.25)}}
def cooling_calendar(machine_life=10,bundle_life=15,hold=365.25,lead=90,machine_days=2,bundle_days=5,stations=2,lead_initial=180):
    if stations<1:raise ValueError('At least one offered machine station is required')
    counts={'helium':28,'salt':28,'bundle':14};batches=[]
    for kind,count in counts.items():
        dates=[-30]+[k*(bundle_life if kind=='bundle' else machine_life)*365.25 for k in range(1,1000) if k*(bundle_life if kind=='bundle' else machine_life)<30]
        for date in dates:batches.append((date,kind,count,date<0))
    prep=[-lead_initial+.5]*2;rows=[];ready=True;initial_ready=True
    # One spare uses each prep station for the first half day; neither is consumed.
    for date,kind,count,initial in sorted(batches):
        receipt=-lead_initial if initial else date-lead
        batch=[]
        for j in range(count):
            k=min(range(2),key=lambda n:prep[n]);prep[k]=max(prep[k],receipt)+(1 if kind=='bundle' else .5)
            row=dict(kind=kind,initial=initial,campaign=date,index=j,receipt=receipt,prepared=prep[k]);rows.append(row);batch.append(row)
        ok=all(r['prepared']<=date for r in batch);ready=ready and ok
        if initial:initial_ready=initial_ready and ok
    # All actual projected movement waits for prepared goods, but required campaign dates do not change.
    tasks=[dict(stage='field',due=max(r['campaign'],r['prepared']),row=j) for j,r in enumerate(rows)]
    free={'machine':[-math.inf]*stations,'bundle':[-math.inf]*2};carrier=-math.inf;route_jobs=[]
    rank={'from_service':0,'to_service':1,'field':2}
    while tasks:
        choices=[]
        for k,task in enumerate(tasks):
            row=rows[task['row']];pool='bundle' if row['kind']=='bundle' else 'machine';slot=None;earliest=max(carrier,task['due'])
            if task['stage']=='to_service':
                slot=min(range(len(free[pool])),key=lambda i:free[pool][i]);earliest=max(earliest,free[pool][slot])
            if math.isfinite(earliest):choices.append((earliest,rank[task['stage']],task['row'],k,pool,slot))
        if not choices:raise RuntimeError('No schedulable task; resource deadlock')
        start,_,_,k,pool,slot=min(choices);task=tasks.pop(k);row=rows[task['row']];stage=task['stage'];carrier=start+(.2 if stage=='field' else .1)
        route_jobs.append(dict(stage=stage,row=task['row'],start=start,end=carrier))
        if stage=='field':
            row.update(withdraw=start,field_handoff=start+.1,return_arrival=carrier)
            if not row['initial']:
                row['removed']=start+.1;tasks.append(dict(stage='to_service',due=carrier,row=task['row']))
        elif stage=='to_service':
            row.update(service_pickup=start,service_start=carrier,service_end=carrier+(bundle_days if pool=='bundle' else machine_days),station=pool+str(slot),station_pool=pool,station_slot=slot)
            free[pool][slot]=math.inf # Occupied through its finished-component transfer.
            tasks.append(dict(stage='from_service',due=row['service_end'],row=task['row']))
        else:
            row.update(station_release=carrier,storage_arrival=carrier,release=carrier+hold)
            free[row['station_pool']][row['station_slot']]=carrier
    capacity={}
    for kind in counts:
        rr=[r for r in rows if r['kind']==kind];dirty=[r for r in rr if not r['initial']]
        capacity[kind]=dict(clean=peak([(r['receipt'],r['withdraw']) for r in rr])+(kind!='bundle'),queue=peak([(r['return_arrival'],r['service_pickup']) for r in dirty]),stored=peak([(r['storage_arrival'],r['release']) for r in dirty]),dirty_bank=peak([(r['return_arrival'],r['service_pickup']) for r in dirty]+[(r['storage_arrival'],r['release']) for r in dirty]))
    for name in set(r['station'] for r in rows if not r['initial']):
        jobs=sorted((r['service_start'],r['station_release']) for r in rows if r.get('station')==name)
        assert all(a[1]<=b[0] for a,b in zip(jobs,jobs[1:]))
    assert all(a['end']<=b['start'] for a,b in zip(route_jobs,route_jobs[1:]))
    return dict(capacity=capacity,all_batches_ready=ready,initial_ready=initial_ready and -lead_initial+.5<=-30,spares={'helium':{'receipt':-lead_initial,'ready':-lead_initial+.5,'release':None},'salt':{'receipt':-lead_initial,'ready':-lead_initial+.5,'release':None}},last_release=max((r['release'] for r in rows if not r['initial']),default=None),transport_busy_until=carrier,cooling_outage_basis_resolved=False,jobs=rows,carrier_jobs=route_jobs)

cool=cooling_calendar()
result['initial_and_cooling']={'no_in_vessel_replacements':run(events=[]),'late_initial_receipt':run(events=[],initial_lead=20),'baseline':cool,'coincident':cooling_calendar(machine_life=15,bundle_life=15),'late_initial_cooling':cooling_calendar(machine_life=30,bundle_life=30,lead_initial=1),'no_cooling_replacements':cooling_calendar(machine_life=30,bundle_life=30),'long_hold':cooling_calendar(hold=16*365.25),'late_receipt':cooling_calendar(lead=1),'long_processing':cooling_calendar(machine_days=200,bundle_days=400)}
assert result['initial_and_cooling']['no_in_vessel_replacements']['peak_clean_per_wing']==36
assert result['initial_and_cooling']['no_in_vessel_replacements']['peak_storage_per_wing']==0
assert not result['initial_and_cooling']['late_initial_receipt']['initial_ready']
assert not result['initial_and_cooling']['late_receipt']['all_batches_ready']
assert not result['initial_and_cooling']['late_initial_cooling']['initial_ready']
assert [result['initial_and_cooling']['late_initial_cooling']['capacity'][k]['clean'] for k in ('helium','salt','bundle')]==[29,29,14]
# Revised bundle route: unchanged y-axis orientation and lateral-capable carrier, with no rotation credit.
# Clear module coordinates; construction wall/partition thickness is added by final quantity owner.
bundle_transport=[13.6,5.2,4.2] # y-length, x-width, height; explicitly assumed packaging/handling margin
route_clear=6.;cross_clear=17.;cell_w=13.2;cell_l=13+4+11.6+4+16
coolx=math.ceil(circuits/2)*cell_w;cooly=2*cell_l+cross_clear
stores=[];x0=0;door_register=[]
for kind,l,w in [('helium',6,3),('salt',3,2),('bundle',11.6,3.2)]:
    width=2*(w+2)+route_clear
    for zone,sign in [('clean',1),('dirty',-1)]:
        k=cool['capacity'][kind]['clean' if zone=='clean' else 'dirty_bank'];length=math.ceil(k/2)*(l+2)+6
        stores.append(dict(kind=kind,zone=zone,x=[x0,x0+width],y=[sign*25.5,sign*(25.5+length)],aisle_x=x0+width/2,positions=k,pitch=l+2,depth=w+2))
        for yy in [sign*8.5,sign*25.5]:door_register.append(dict(owner='cooling_annex',name=zone+'_'+kind+'_airlock_'+str(yy),center=[x0+width/2,yy],width=6,height=9,wall_axis='x',served_envelope=bundle_transport))
    x0+=width
# Separate machine/bundle service strip; same fixed orientation, side-sliding from longitudinal aisle.
service_w=20.4;service_center=x0+service_w/2
for yy in [-8.5,-25.5]:door_register.append(dict(owner='cooling_annex',name='service_airlock_'+str(yy),center=[service_center,yy],width=6,height=9,wall_axis='x',served_envelope=bundle_transport))
annex_width=x0+service_w
annex_positive=max(max(s['y']) for s in stores);annex_negative=min(min(s['y']) for s in stores)
for owner,name,center,width,axis in [('cooling_hall','link_exit',[coolx,cooly/2],17,'y'),('cooling_annex','link_entry',[0,0],17,'y'),('cooling_annex','controlled_goods_gateway',[annex_width,0],17,'y')]:door_register.append(dict(owner=owner,name=name,center=center,width=width,height=9,wall_axis=axis,served_envelope=bundle_transport))
result['revised_motion']={'bundle_transport_envelope':bundle_transport,'motion':'Keep longitudinal y orientation. Ground carrier translates laterally in x; no rotation. One paired transfer cycle owns shared corridor at a time.','hall_clear_xy':[coolx,cooly],'hall_cross_corridor_y':[cell_l,cell_l+17],'link_clear_LWH':[10,17,9],'stores':stores,'annex_clear_bounds':[0,annex_negative,annex_width,annex_positive],'service_strip_x':[x0,annex_width],'service_strip_y':[-57.1,-25.5],'door_register':door_register,'cooling_opening_counts':{'hall_exterior':1,'annex_exterior':2,'annex_internal':14},'route_fit':route_clear>=bundle_transport[1] and cross_clear>=bundle_transport[0]}

sector_lane_w=sw+12
sector_doors=[]
for wing in range(4):
    for side,sign in [('clean',-1),('dirty',1)]:
        for vlocal in [0,6]:sector_doors.append(dict(wing=wing,name=side+'_airlock_'+str(vlocal),center=[3,sign*(sector_lane_w/2+vlocal)],clear_width=6,clear_height=6,wall_axis='u'))
    sector_doors.append(dict(wing=wing,name='hall_link_opening',center=[0,0],clear_width=sector_lane_w,clear_height=sh+3,wall_axis='v'))
portu=6+12.7/math.sqrt(2);portv=12.7/math.sqrt(2)
stageu=6+math.sqrt(2)*12.7-sw/2-3
result['revised_sector_routes']={'lane_clear_width':sector_lane_w,'sector_box':[6,-sw/2,6+sl,sw/2],'end_ports':[[portu,-portv],[portu,portv]],'side_staging_centers':[[stageu,-sw/2-3],[stageu,sw/2+3]],'turning_square_side':6,'outer_bypass_strip':[6+sl,-sector_lane_w/2,12+sl,sector_lane_w/2],'inner_bypass_strip':[0,-sector_lane_w/2,6,sector_lane_w/2],'door_register':sector_doors,'opening_counts':{'wing_partition':8,'wing_exterior_link':4,'hall_exterior_link':4,'airlock_end':8},'package_with_carrier':[5,3,3],'rotation_fits':math.hypot(5,3)<=6}
# Register doors by physical face: per wing 2 partition apertures + 2 airlock outer faces.
result['revised_sector_routes']['opening_counts']['wing_partition']=8


for wing in range(4):
    for side,sign in [('clean_receipt',-1),('dirty_outgoing',1)]:
        sector_doors.append(dict(wing=wing,name=side,center=[wingl,sign*(sector_lane_w/2+7)],clear_width=6,clear_height=6,wall_axis='v'))
result['revised_sector_routes']['opening_counts']['wing_exterior_goods']=8
for name,arm in result['initial_and_cooling'].items():
    if 'capacity' not in arm:continue
    arm['offered_positions']=cool['capacity']
    arm['position_capacity_ok']=all(arm['capacity'][kind][zone]<=cool['capacity'][kind][zone] for kind in ('helium','salt','bundle') for zone in ('clean','dirty_bank'))
    deadlines={}
    for row in arm['jobs']:
        if row['initial']:continue
        deadlines.setdefault(row['kind'],[]).append(row)
    arm['processing_clears_before_next_campaign']=all(max(r['service_end'] for r in rr if r['removed']//365.25==year)<min((r['removed'] for r in rr if r['removed']//365.25>year),default=math.inf) for rr in deadlines.values() for year in set(r['removed']//365.25 for r in rr))
    arm['processing_unfinished_at_shutdown']=sum(r.get('service_end',0)>30*365.25 for r in arm['jobs'])
# Wall-expanded external shells and straight links. t=2 is a construction scenario only.
t=2.;tc=.3;airlock_front=12+2*t;newwingclearL=wingl+airlock_front-6;newwingw=sector_lane_w+56+4*t;newwingL=newwingclearL+2*t
newhall=2*max(outside+sl+c,newwingw/2+c);hh=newhall/2+t;near=hh+10
expanded={'hall':[-hh,-hh,hh,hh], 'east_wing':[near,-newwingw/2,near+newwingL,newwingw/2], 'west_wing':[-near-newwingL,-newwingw/2,-near,newwingw/2], 'north_wing':[-newwingw/2,near,newwingw/2,near+newwingL], 'south_wing':[-newwingw/2,-near-newwingL,newwingw/2,-near]}
lw=sector_lane_w/2+t
expanded.update(east_link=[hh,-lw,near,lw],west_link=[-near,-lw,-hh,lw],north_link=[-lw,hh,lw,near],south_link=[-lw,-near,lw,-hh])
hx=near+newwingL+10
expanded['cooling_hall']=[hx,-cooly/2-tc,hx+coolx+2*tc,cooly/2+tc]
ax=hx+coolx+2*tc+10
expanded['cooling_link']=[hx+coolx+2*tc,-8.5-tc,ax,8.5+tc]
expanded['cooling_annex']=[ax,annex_negative-3*tc,ax+annex_width+5*tc,annex_positive+3*tc]
# Campus room shells beyond the actual south wing; include their class thickness and12m exterior access.
campus_y=-near-newwingL-10
campus_x=-hh
for name,d in rooms.items():
    expanded['campus_'+name]=[campus_x,campus_y-d['W']-2*tc,campus_x+d['L']+2*tc,campus_y];campus_x+=d['L']+2*tc+10
expanded['heat_rejection_plot']=[campus_x,campus_y-60,campus_x+100,campus_y]
for i,(name,a) in enumerate(expanded.items()):
    for name2,b in list(expanded.items())[i+1:]:assert a[2]<=b[0] or b[2]<=a[0] or a[3]<=b[1] or b[3]<=a[1],(name,name2)
result['revised_wall_shell_rectangles']=dict(nuclear_t=t,cooling_t=tc,wing_clear_length=newwingclearL,wing_front_reserve=airlock_front,rectangles=expanded,parcel_area=(max(r[2] for r in expanded.values())-min(r[0] for r in expanded.values())+24)*(max(r[3] for r in expanded.values())-min(r[1] for r in expanded.values())+24),warning='Airlock6m clear room plus side walls and6m downstream cross-aisle reserved in wing; cooling register offsets each bank by its partition thickness and each store by2*tc.')

assert result['revised_motion']['route_fit']
result['revised_motion']['counterexamples']={'aisle_5m_fits':5>=bundle_transport[1],'cross_13m_fits':13>=bundle_transport[0]}
assert not any(result['revised_motion']['counterexamples'].values())
assert base['outage_ok'] and not result['contrasts']['one_team']['outage_ok'] and not result['contrasts']['slow_tasks']['outage_ok']
assert result['contrasts']['six_year_storage']['peak_storage_per_wing']>base['peak_storage_per_wing']
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps(result,indent=2))
