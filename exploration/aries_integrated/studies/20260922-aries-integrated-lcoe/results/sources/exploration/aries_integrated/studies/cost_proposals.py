"""Bounded accounting sensitivities on the accepted thermal baseline; no evaluator."""
from .equipment_proposals import key

STUDY_ID = '20260922-aries-integrated-cost-uncertainty'

def axes(entry_keys):
    rows=[]
    def add(name, k, values, units, gap):
        if k not in entry_keys: raise ValueError(f'missing public input {k}')
        rows.append(dict(axis=name, keys=[k], values=values, units=units, role='assumed', framing='sensitivity', window_provenance='engineered', missing_response=gap))
    prices=sorted(k for k in entry_keys if k.endswith('__price_factor'))
    if len(prices)!=38: raise ValueError('expected exactly 38 price owners')
    for k in prices:
        owner=k.split('__')[1]
        add(owner+'_price', k, [.5, 2. if owner=='unallocated_source_scope' else 1.5], 'dimensionless', 'Supplied price uncertainty has no market calibration or purchased quality response.')
    for owner,field,lo,hi,units in [
        ('fuel_inventory','tritium_price',1e7,1e8,'USD2004/kg'),
        ('fuel_inventory','selected_tritium_kg',1.,30.,'kg'),
        ('fuel_inventory','deuterium_price',100.,10000.,'USD2004/kg'),
        ('annual_om','selected_amount',35e6,140e6,'USD2004/year'),
        ('cost_ledger','consumables',1e6,15e6,'USD2004/year'),
        ('indirect_cost','fraction',.1,.3,'dimensionless'),
        ('contingency','fraction',.1,.4,'dimensionless'),
        ('owner_commissioning','fraction',.02,.1,'dimensionless'),
        ('cost_schedule','replacement_life_fpy',2.,8.,'full-power years'),
        ('cost_schedule','replacement_factor',.5,2.,'dimensionless'),
        ('cost_schedule','lipb_makeup_fraction',0.,.2,'dimensionless'),
        ('cost_schedule','availability',.7,.95,'dimensionless')]:
        add(owner+'_'+field,key(owner,field),[lo,hi],units,'Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only.')
    add('supplied_recovery',key('fuel_inventory','annual_recovery_kg'),[0.,200.],'kg/year','Independently supplied recovery is not a calculated breeding capability; support remains zero.')
    rows[-1]['scenario_values']=[0.,100.,200.]
    rows[-1]['response_limit']='Supplied recovery has no incremental recovery-cost or qualification law at fixed installed scope; it is a boundary scenario, not purchased-capability optimization.'
    add('purchase_mode',key('cost_accounts','estimate_mode'),[0,1],'enumeration','Fixed budget mode deliberately suppresses selected quantity price response.')
    add('adequate_he_area',key('he_hx','selected_area'),[50000.,75000.],'m2','Previously tested adequate area is not geometry or hydraulic qualification.')
    return rows

def declare_axes(entry_keys):
    return {'schema_version':'study-axis-declaration/v1','groups':[{'axis':a['axis'],'note':a['missing_response'],'keys':[{'key':a['keys'][0],'provenance':'fan_out'}]} for a in axes(entry_keys)]}

def propose(canonical, entry_keys):
    names=('nominal-calculated','nominal-source-assumed','literal-Lyon-source-input','literal-Raffray-accounting')
    if set(canonical)!=set(names): raise ValueError('four canonical maps required')
    if any(set(p)!=set(entry_keys) for p in canonical.values()): raise ValueError('incomplete canonical maps')
    baseline=canonical[names[0]]
    rows=[dict(case=n,arm='canonical',point=canonical[n]) for n in names]
    def append(name, changes, family, axis=None):
        rows.append(dict(case=name,arm=family,axis=axis,changes=changes,point=baseline|changes))
    aa=axes(entry_keys)
    for a in aa[:50]:
        for label,v in zip(('low','high'),a['values']): append(a['axis']+'-'+label,{a['keys'][0]:v},'economic',a['axis'])
    for recovery in (100.,200.): append(f'recovery-{int(recovery)}',{key('fuel_inventory','annual_recovery_kg'):recovery},'recovery','supplied_recovery')
    mode=key('cost_accounts','estimate_mode'); area=key('he_hx','selected_area')
    append('fixed-budget-nominal',{mode:1},'purchase-mode')
    for m in (0,1): append(f'adequate-area-mode-{m}',{area:75000.,mode:m},'purchase-mode')
    for label,index in (('low',0),('high',1)):
        changes={a['keys'][0]:a['values'][index] for a in aa[:50]}
        changes[key('cost_schedule','replacement_life_fpy')]=8. if label=='low' else 2.
        for recovery in (0.,100.): append(f'combined-{label}-recovery-{int(recovery)}',changes|{key('fuel_inventory','annual_recovery_kg'):recovery},'combined')
    assert len(rows)==113 and len({r['case'] for r in rows})==113
    assert len({tuple(sorted(r['point'].items())) for r in rows})==113
    return {'study_id':STUDY_ID,'scenario_covariance':'Combined economic corners vary all first 50 axes together, reversing life endpoints for lower/higher replacement exposure; supplied recovery is independently fixed at 0 or 100 kg/year. Area/mode scenarios jointly choose area and purchase mode. These are declared coordinated scenarios, not physical equality ties or probabilistic bounds.','cases':rows}
