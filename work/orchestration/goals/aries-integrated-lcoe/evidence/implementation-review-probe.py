"""Independent native probes and dated-cashflow checks; no production outputs filled."""
import json
import math
import sys
from decimal import Decimal, localcontext
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'exploration/aries_integrated'))
from run import load_runtime, execute_case, PREFIX as P

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-8), (a, b)

def check(row):
    assert row['status'] == 'evaluated', row.get('error')
    inp = row['effective_inputs']; out = row['outputs']
    v = lambda owner, key, calc='evaluate': out[P + owner + '__' + calc + '__' + key]
    i = lambda key: inp[P + key]
    result = {}
    with localcontext() as ctx:
        ctx.prec = 65
        d = lambda x: Decimal(str(x))
        rate = d(i('finance__discount_rate')); years = int(i('cost_schedule__plant_years'))
        w = lambda t: (1 + rate) ** -d(t)
        for source in (False, True):
            prefix = 'source_lifecycle' if source else 'lifecycle'
            capital = d(v('source_budget', 'inclusive_capital') if source else v('cost_ledger', 'overnight'))
            power = d(i('source_finance__net_power') if source else v('plant_ledger', 'net_electric'))
            energy = power * 8760 * d(i('cost_schedule__availability'))
            annuity = sum(w(t) for t in range(1, years + 1))
            epv = energy * annuity
            construction = 0 if source else i('finance__construction_years')
            pv = {'capital': capital / w(d(construction)/2)}
            annual = {'om': v('annual_om', 'annual_om'), 'tritium': v('fuel_inventory', 'annual_cost', 'annual'), 'deuterium': v('fuel_inventory', 'annual_fuel', 'deuterium'), 'consumables': i('cost_ledger__consumables'), 'imports': v('cost_ledger', 'annual_import_cost'), 'supply': i('finance__supply_service_annual')}
            pv.update({k: d(x)*annuity for k, x in annual.items()})
            tau = d(i('cost_schedule__replacement_life_fpy')) / d(i('cost_schedule__availability'))
            dates = []; k = 1
            while k*tau < years:
                dates.append(k*tau); k += 1
            pv['replacement'] = sum(d(v('replacement', 'event_cost'))*w(t) for t in dates)
            t = d(i('finance__other_overhaul_year'))
            pv['other_overhaul'] = capital*d(i('finance__other_overhaul_fraction'))*w(t) if t < years else Decimal(0)
            pv['terminal'] = capital*d(i('finance__terminal_fraction'))*w(years)
            pv['salvage'] = -capital*d(i('finance__salvage_fraction'))*w(years)
            expected = float(sum(pv.values())/epv)
            close(v(prefix+'_price', 'lcoe'), expected)
            close(v(prefix+'_accounts', 'lcoe_sum'), expected)
            close(v(prefix+'_accounts', 'pv_energy'), float(epv))
            for key, amount in pv.items(): close(v(prefix+'_accounts', key+'_lcoe'), float(amount/epv))
            assert v(prefix+'_accounts', 'supply_supported') == v(prefix+'_accounts', 'breeding_supported') == 0
            result[prefix] = {'native_lcoe':v(prefix+'_price','lcoe'), 'dated_oracle_lcoe':expected,'event_count':len(dates)}
        assert v('source_lifecycle_accounts','idc') == 0
    return result

def main():
    pipeline = yaml.safe_load((ROOT/'exploration/aries_integrated/aries_integrated/pipelines/pipeline.yaml').read_text())
    modules = pipeline['modules']; boundary = 'float '+P+'source_finance__boundary__years.root'
    for owner in ('source_lifecycle_accounts','source_lifecycle_price'):
        assert modules[P+owner+'__evaluate']['inputs']['construction_years_in'] == boundary
    for owner in ('lifecycle_accounts','source_lifecycle_accounts','lifecycle_price','source_lifecycle_price'):
        assert not any('reserve' in x for x in modules[P+owner+'__evaluate']['inputs'].values())
    runtime = load_runtime()
    assert runtime[2] == 'd13f4153accc48a3d6533a2d29a8e8b6b7cecd86644c322bb64f59fa402e419b'
    base = {P+'source__producer_mode':1.,P+'fuel_inventory__annual_recovery_kg':73.,P+'finance__supply_service_annual':42000000.,P+'finance__discount_rate':.073,P+'finance__construction_years':7.5,P+'cost_schedule__plant_years':31.,P+'cost_schedule__availability':.78,P+'finance__terminal_fraction':.15,P+'finance__salvage_fraction':.01,P+'finance__other_overhaul_fraction':.07,P+'finance__other_overhaul_year':17.}
    configs = [('off_default',base),('fixed_hardware_demand',{**base,'aries_cs_plasma_integration__plasma__amplitude':5.13e20}),('tiny_rate',{**base,P+'finance__discount_rate':1e-12}),('tiny_nonzero_source_duration',{**base,P+'source_finance__construction_years':1e-15})]
    rows=[]; checks={}
    for name, changes in configs:
        row=execute_case(name,changes,runtime,root=HERE/'implementation-review-native')
        rows.append(row)
        if name=='tiny_nonzero_source_duration':
            assert row['status']=='refused' and 'already-financed' in row['error']
            checks[name]={'native_refusal':row['error']}
        else: checks[name]=check(row)
    assert rows[0]['outputs'][P+'cost_ledger__evaluate__overnight']==rows[1]['outputs'][P+'cost_ledger__evaluate__overnight']
    for key,x in rows[0]['effective_inputs'].items():
        if key!='aries_cs_plasma_integration__plasma__amplitude': assert rows[1]['effective_inputs'][key]==x
    for key in ('plant_ledger__evaluate__net_electric','fuel_inventory__annual__annual_external','lifecycle_price__evaluate__lcoe'):
        assert rows[0]['outputs'][P+key]!=rows[1]['outputs'][P+key]
    development=json.loads((ROOT/'work/active/WI-091_aries-integrated-lifecycle-cost/evidence/development-cases.json').read_text())
    checks['retained_development_oracle']={row['case']:check(row) for row in development if row['status']=='evaluated'}
    (HERE/'implementation-review-probe.json').write_text(json.dumps({'passed':True,'fingerprint':runtime[2],'checks':checks,'native_rows':rows},indent=2)+'\n')
    print(json.dumps({'passed':True,'new_native_cases':4,'retained_cases_checked':len(checks['retained_development_oracle']),'checks':{k:v for k,v in checks.items() if k!='retained_development_oracle'}},indent=2))

if __name__=='__main__': main()
