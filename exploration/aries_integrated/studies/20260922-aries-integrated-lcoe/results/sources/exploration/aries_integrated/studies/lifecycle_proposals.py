"""Predeclared complete-map WI-091 sensitivity points; no evaluator."""
from .equipment_proposals import key, A
STUDY_ID='20260922-aries-integrated-lcoe'


def axes():
    rows=[]
    def add(name,owner,field,values,units,gap,role='assumed'):
        rows.append(dict(axis=name,keys=[key(owner,field)],values=values,units=units,
            role=role,framing='sensitivity',window_provenance='engineered',missing_response=gap))
    finance='Financial assumption lacks financing, liability or service-life evidence; no engineering optimum.'
    for name,field,values,units in [
        ('discount','discount_rate',[0.,1e-12,.03,.05,.08,.1],'real/year'),
        ('construction','construction_years',[0.,4.,6.,10.],'calendar years'),
        ('terminal','terminal_fraction',[.05,.1,.2],'dimensionless'),
        ('salvage','salvage_fraction',[0.,.02,.05],'dimensionless'),
        ('overhaul_fraction','other_overhaul_fraction',[0.,.05,.1],'dimensionless'),
        ('overhaul_date','other_overhaul_year',[15.,20.,30.],'calendar years')]:
        add(name,'finance',field,values,units,finance)
    add('life','cost_schedule','plant_years',[20.,30.,40.,60.],'calendar years',finance)
    add('availability','cost_schedule','availability',[.6,.75,.85,.95],'dimensionless','Supplied availability has no outage/reliability response; no additional downtime charge.')
    for owner,values in [('magnet_inventory',[.5,1.,1.5]),('unallocated_source_scope',[.5,1.,2.])]:
        add(owner+'_price',owner,'price_factor',values,'dimensionless','Supplied price factor has no calibrated market or equipment-quality response.')
    for name,owner,field,values,units in [
        ('tritium_price','fuel_inventory','tritium_price',[1e7,3e7,1e8],'USD2004/kg'),
        ('routine_om','annual_om','selected_amount',[35e6,70e6,140e6],'USD2004/year'),
        ('consumables','cost_ledger','consumables',[1e6,5e6,15e6],'USD2004/year'),
        ('replacement_life','cost_schedule','replacement_life_fpy',[2.,5.,8.],'full-power years'),
        ('replacement_factor','cost_schedule','replacement_factor',[.5,1.,2.],'dimensionless')]:
        add(name,owner,field,values,units,'Supply/lifetime/operating-cost assumption lacks calibrated engineering evidence.')
    add('new_feed','fuel_inventory','annual_recovery_kg',[0.,50.,100.,110.],'kg/calendar year','Net extracted breeder feed has no qualified capability or extraction-cost model; internal exhaust recycling is already accounted.')
    add('supply_service','finance','supply_service_annual',[0.,10e6,30e6,100e6],'USD2004/year','Incremental assumed extraction/service cost has no price-versus-capability relationship.')
    add('density_amplitude','unused','unused',[4.5e20,5e20,5.5e20],'m^-3','Fixed-hardware source-demand change does not qualify confinement.','demand')
    rows[-1]['keys']=[A]
    add('he_hx_area','he_hx','selected_area',[5000.,50000.,75000.],'m2','Selected area has linear provisional price response; hydraulic/geometric qualification absent.','purchased')
    return rows


def declare_axes(entry_keys):
    groups=[]
    for row in axes():
        if not set(row['keys'])<=set(entry_keys):raise ValueError('absent axis: '+row['axis'])
        groups.append({'axis':row['axis'],'note':row['missing_response'],
                       'keys':[{'key':k,'provenance':'fan_out'} for k in row['keys']]})
    return {'schema_version':'study-axis-declaration/v1','groups':groups}


def propose(canonical,entry_keys):
    expected=('no-breeding-credit','assumed-new-tritium-feed-100','nominal-source-assumed','literal-Lyon-source-input','literal-Raffray-accounting')
    if set(canonical)!=set(expected):raise ValueError('five canonical cases required')
    declare_axes(entry_keys)
    canonical={n:{k:float(v) for k,v in p.items()} for n,p in canonical.items()}
    if any(set(p)!=set(entry_keys) for p in canonical.values()):raise ValueError('incomplete canonical map')
    rows=[]
    def add(name,point,arm,changes=None,axis=None):
        point={k:float(v) for k,v in point.items()}
        duplicate=next((r for r in rows if r['point']==point),None)
        if duplicate:
            duplicate.setdefault('aliases',[]).append(name)
            return
        rows.append(dict(case=name,arm=arm,axis=axis,changes=changes or {},point=point))
    for name in expected:add(name,canonical[name],'canonical')
    def case(name,axis,value,feed=False,extra=None):
        row=next(r for r in axes() if r['axis']==axis)
        base=canonical[expected[int(feed)]]
        changes={k:float(value) for k in row['keys']}|(extra or {})
        add(name,base|changes,'named-feed' if feed else 'no-credit',changes,axis)
    for axis in ('discount','construction','life','availability'):
        a=next(r for r in axes() if r['axis']==axis)
        for feed in (False,True):
            for value in a['values']:
                case(f'{axis}-{value}-'+('feed' if feed else 'no-credit'),axis,value,feed)
    for axis in ('magnet_inventory_price','unallocated_source_scope_price','tritium_price','routine_om','consumables',
                 'terminal','salvage','overhaul_fraction','overhaul_date','replacement_life','replacement_factor'):
        a=next(r for r in axes() if r['axis']==axis)
        for value in (a['values'][0],a['values'][-1]):case(f'{axis}-{value}',axis,value)
    for value in (50.,110.):case(f'new-feed-{value}','new_feed',value,True)
    for value in (10e6,100e6):case(f'supply-service-{value}','supply_service',value,True)
    for value in (4.5e20,5.5e20):case(f'density-{value}-fixed-feed','density_amplitude',value,True)
    for value in (5000.,75000.):case(f'he-area-{value}','he_hx_area',value)
    case('zero-rate-zero-construction','discount',0.,extra={key('finance','construction_years'):0.})
    return {'study_id':STUDY_ID,'scenario_covariance':'Named feed fixes100kg/year and30mUSD2004/year service except independent feed/service axes. Availability and demand changes hold feed/service fixed. Zero-rate-zero-construction is a declared joint limit. All other sensitivity rows change one qualified input; source branch is a native controlled comparison.','cases':rows}
