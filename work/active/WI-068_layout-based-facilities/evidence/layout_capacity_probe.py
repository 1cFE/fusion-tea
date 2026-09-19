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

def run(step=.5,teams=2,hold=365.25,volume_factor=1):
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
    for date in calendar['events']:
        for s in schedule:
            last=last_by_wing[s['sector']]
            for j in range(count):
                arrival=date*365.25+s['start']+(j+1)*step
                start=max(arrival,last);last=start+1
                pending.append((arrival,start));station.append((start,last));storage.append((last,last+hold))
            last_by_wing[s['sector']]=last
    # Per-wing capacity; no pooling of dirty routes/resources across wings.
    wing0=schedule[0]; pend0=[];store0=[]
    last=-math.inf;clean_last=-math.inf;clean_inventory=[];clean_ready=True
    for date in calendar['events']:
        receipt=date*365.25-90
        clean_last=max(clean_last,receipt)+count
        clean_ready=clean_ready and clean_last<=date*365.25+wing0['start']+count*step+7
        for j in range(count):
            arrival=date*365.25+wing0['start']+(j+1)*step;start=max(arrival,last);last=start+1
            if start>arrival:pend0.append((arrival,start))
            store0.append((last,last+hold))
            clean_inventory.append((receipt,date*365.25+wing0['start']+count*step+7+(j+1)*step))
    return dict(packages_per_sector=count,blanket_packages_per_sector=blank,service_days=service,sector_schedule=schedule,outage_required_days=duration,outage_offered_days=365.25*7/12,outage_ok=duration<=365.25*7/12,peak_buffer_per_wing=peak(pend0),peak_storage_per_wing=peak(store0),peak_storage_total=peak(storage),peak_clean_per_wing=peak(clean_inventory),clean_ready=clean_ready,calendar_event_years=calendar['events'],availability_unchanged=calendar['availability'])
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
assert base['outage_ok'] and not result['contrasts']['one_team']['outage_ok'] and not result['contrasts']['slow_tasks']['outage_ok']
assert result['contrasts']['six_year_storage']['peak_storage_per_wing']>base['peak_storage_per_wing']
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps(result,indent=2))
