"""Native development evidence; dated oracle is verification only, not production."""
import sys,json,math,tempfile,hashlib
from pathlib import Path
from decimal import Decimal,localcontext
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'exploration/aries_integrated'))
from run import load_runtime,execute_case,PREFIX as P,SCENARIOS

def near(a,b,rel=1e-10,absolute=1e-8):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=absolute),(a,b,a-b)

def val(row,owner,key,calc='evaluate'):
    return row['outputs'][P+owner+'__'+calc+'__'+key]

def input_(row,key):return row['effective_inputs'][P+key]

def oracle(row,source=False):
    """Explicit yearly/event cashflows, 60-digit Decimal, distinct from annuitized core."""
    with localcontext() as ctx:
        ctx.prec=60
        d=lambda x:Decimal(str(x))
        i=lambda x:d(input_(row,x))
        v=lambda owner,key,calc='evaluate':d(val(row,owner,key,calc))
        n=int(i('cost_schedule__plant_years'));r=i('finance__discount_rate');a=i('cost_schedule__availability')
        capital=v('source_budget','inclusive_capital') if source else v('cost_ledger','overnight')
        power=i('source_finance__net_power') if source else v('plant_ledger','net_electric')
        t=Decimal(0) if source else i('finance__construction_years')
        discount=lambda y:(1+r)**(-d(y))
        energy=power*8760*a
        epv=sum(energy*discount(year) for year in range(1,n+1))
        money=capital/discount(t/2)
        expenses={k:Decimal(0) for k in ('capital','om','tritium','deuterium','consumables','imports','supply','replacement','other_overhaul','terminal','salvage')}
        expenses['capital']=money
        annual={'om':v('annual_om','annual_om'),'tritium':v('fuel_inventory','annual_cost','annual'),'deuterium':v('fuel_inventory','annual_fuel','deuterium'),'consumables':i('cost_ledger__consumables'),'imports':v('cost_ledger','annual_import_cost'),'supply':i('finance__supply_service_annual')}
        for year in range(1,n+1):
            for key,amount in annual.items():expenses[key]+=amount*discount(year)
        interval=i('cost_schedule__replacement_life_fpy')/a
        k=1
        while k*interval<n:
            expenses['replacement']+=v('replacement','event_cost')*discount(k*interval);k+=1
        year=i('finance__other_overhaul_year')
        if year<n:expenses['other_overhaul']=capital*i('finance__other_overhaul_fraction')*discount(year)
        expenses['terminal']=capital*i('finance__terminal_fraction')*discount(n)
        expenses['salvage']=-capital*i('finance__salvage_fraction')*discount(n)
        return dict(lcoe=float(sum(expenses.values())/epv),pv_energy=float(epv),contributions={k:float(x/epv) for k,x in expenses.items()})

def verify(row):
    assert row['status']=='evaluated',row.get('error')
    for source in (False,True):
        prefix='source_lifecycle' if source else 'lifecycle';expected=oracle(row,source)
        near(val(row,prefix+'_price','lcoe'),expected['lcoe'])
        near(val(row,prefix+'_accounts','lcoe_sum'),expected['lcoe'])
        near(val(row,prefix+'_accounts','pv_energy'),expected['pv_energy'])
        for key,x in expected['contributions'].items():near(val(row,prefix+'_accounts',key+'_lcoe'),x)
        near(val(row,prefix+'_accounts','new_feed'),input_(row,'fuel_inventory__annual_recovery_kg'))
        assert val(row,prefix+'_accounts','breeding_supported')==val(row,prefix+'_accounts','supply_supported')==0
    return {'integrated':oracle(row),'source_comparison':oracle(row,True)}

def main():
    raw=Path(tempfile.mkdtemp(prefix='wi091-development-'))
    (HERE/'raw-execution-location.json').write_text(json.dumps({'root':str(raw),'purpose':'redundant full native files; compact receipts retain all input groups and scalar outputs'},indent=2)+'\n')
    runtime=load_runtime();base={P+'source__producer_mode':1.};feed={**base,P+'fuel_inventory__annual_recovery_kg':100.,P+'finance__supply_service_annual':30000000.}
    cases=[('no-breeding-credit',base,None),('assumed-new-tritium-feed-100',feed,None)]
    cases.extend((name,changes,None) for name,changes in SCENARIOS.items() if name!='nominal-calculated')
    changes=[('zero_discount',{'finance__discount_rate':0.}),('zero_construction',{'finance__construction_years':0.}),('terminal_high',{'finance__terminal_fraction':.2}),('salvage_zero',{'finance__salvage_fraction':0.}),('overhaul_at_end',{'finance__other_overhaul_year':40.}),('overhaul_after_end',{'finance__other_overhaul_year':45.}),('no_replacements',{'cost_schedule__replacement_life_fpy':34.}),('end_replacement_excluded',{'cost_schedule__plant_years':20.,'cost_schedule__replacement_life_fpy':17.}),('oversupply',{'fuel_inventory__annual_recovery_kg':110.}),('internal_recycle',{'fuel__exhaust_recovery':.98}),('supply_cost_high',{'finance__supply_service_annual':100000000.}),('low_availability',{'cost_schedule__availability':.6}),('long_life',{'cost_schedule__plant_years':60.}),('high_discount',{'finance__discount_rate':.1}),('insufficient_he_rating',{'he_capacity__selected_rating':1.}),('sufficient_he_rating',{'he_capacity__selected_rating':3000.}),('other_electric_demand',{'generator_auxiliaries__other_electric':15.})]
    cases.extend((name,{**feed,**{P+k:v for k,v in c.items()}},None) for name,c in changes)
    cases.append(('higher_plasma_demand',{**feed,'aries_cs_plasma_integration__plasma__amplitude':5.25e20},None))
    refusals=[('nonpositive_energy',{'generator_auxiliaries__other_electric':1000.},'nonpositive net electricity'),('negative_discount',{'finance__discount_rate':-.01},'discount'),('unsupported_discount',{'finance__discount_rate':1.1},'discount'),('fractional_life',{'cost_schedule__plant_years':40.5},'integer'),('zero_life',{'cost_schedule__plant_years':0.},None),('invalid_overhaul',{'finance__other_overhaul_year':0.},'overhaul'),('invalid_replacement',{'cost_schedule__replacement_life_fpy':0.},'replacement'),('double_source_financing',{'source_finance__construction_years':1.},'already-financed')]
    cases.extend((name,{**feed,**{P+k:v for k,v in c.items()}},needle or 'REFUSE') for name,c,needle in refusals)
    cases.extend((name,{**feed,P+'source_finance__construction_years':x},'REFUSE') for name,x in [('negative_source_financing',-1.),('nonfinite_source_financing','NaN'),('infinite_source_financing','Infinity')])
    rows=[];checks=[]
    for name,changes,refusal in cases:
        row=execute_case(name,changes,runtime,root=raw)
        if refusal:
            assert row['status']=='refused',(name,row['status'])
            if refusal!='REFUSE':assert refusal.lower() in row['traceback'].lower(),(name,row['traceback'])
            # Capture every retained JSON output from native failure, rather than recomputing upstream state.
            row['retained_native_outputs']={str(p.relative_to(raw/name)):json.loads(p.read_text()) for p in (raw/name/'outputs').rglob('*.json')}
            checks.append({'case':name,'expected_refusal':True,'upstream_files':len(row['retained_native_outputs'])})
        else:
            expected=verify(row);checks.append({'case':name,'expected':expected})
        rows.append(row)
        (HERE/'development-cases.json').write_text(json.dumps(rows,indent=2)+'\n')
        print(name,row['status'],flush=True)
    indexed={x['case']:x for x in rows};a=indexed['no-breeding-credit'];b=indexed['assumed-new-tritium-feed-100']
    near(val(a,'plant_ledger','net_electric'),423.10679410931664,absolute=1e-9)
    near(val(a,'fuel_inventory','annual_external','annual'),104.66770702324638)
    near(val(b,'fuel_inventory','annual_external','annual'),4.66770702324638)
    near(val(a,'plant_ledger','net_electric'),val(b,'plant_ledger','net_electric'))
    near(val(indexed['oversupply'],'lifecycle_accounts','external_shortfall'),0)
    assert val(indexed['oversupply'],'lifecycle_accounts','curtailed_feed')>0
    assert val(indexed['insufficient_he_rating'],'he_capacity','margin')<0
    assert val(indexed['sufficient_he_rating'],'he_capacity','margin')>0
    assert val(indexed['insufficient_he_rating'],'lifecycle_price','lcoe')>0
    for name in ('other_electric_demand','higher_plasma_demand'):
        row=indexed[name]
        for key,x in b['effective_inputs'].items():
            if any(s in key for s in ('selected_rating','selected_area','selected_flow_capacity','selected_mass','selected_tritium_kg')):assert row['effective_inputs'][key]==x,(name,key)
        near(val(row,'cost_ledger','overnight'),val(b,'cost_ledger','overnight'))
        assert val(row,'plant_ledger','net_electric')!=val(b,'plant_ledger','net_electric')
        assert val(row,'lifecycle_price','lcoe')!=val(b,'lifecycle_price','lcoe')
    near(val(indexed['other_electric_demand'],'plant_ledger','net_electric'),val(b,'plant_ledger','net_electric')-10)
    near(val(indexed['end_replacement_excluded'],'replacement','event_count'),0)
    # Source comparison retains recurring costs but scales capital-based allowances.
    ratio=val(b,'source_budget','inclusive_capital')/val(b,'cost_ledger','overnight')
    near(val(b,'source_lifecycle_accounts','gross_terminal'),val(b,'lifecycle_accounts','gross_terminal')*ratio)
    near(val(b,'source_lifecycle_accounts','other_overhaul_cost'),val(b,'lifecycle_accounts','other_overhaul_cost')*ratio)
    near(val(b,'source_lifecycle_accounts','idc'),0)
    (HERE/'verification.json').write_text(json.dumps({'passed':True,'fingerprint':runtime[2],'cases':len(rows),'evaluated':sum(x['status']=='evaluated' for x in rows),'refused':sum(x['status']=='refused' for x in rows),'checks':checks},indent=2)+'\n')
    print(json.dumps({'passed':True,'cases':len(rows),'raw':str(raw)}))
if __name__=='__main__':main()
