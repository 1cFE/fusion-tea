"""Independent targeted receipt checks for the corrected WI-090 graph."""
import hashlib
import json
import math
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[5]
E=ROOT/'work/active/WI-090_aries-integrated-equipment-and-costs/evidence'
v=json.loads((E/'verification.json').read_text())
rows={r['case']:r for r in v['cases']}
P='aries_integrated_plant__'
b=rows['nominal-calculated']
checks=[]
def value(case,owner,calc,field):
    return rows[case]['outputs'][P+owner+'__'+calc+'__'+field]
def check(label,actual,expected,tol=.01):
    assert math.isclose(actual,expected,rel_tol=0,abs_tol=tol),(label,actual,expected)
    checks.append(dict(label=label,actual=actual,expected=expected))
def f(owner,calc,field):return value('nominal-calculated',owner,calc,field)
expected={
 ('source_reconciliation','reactor_gap_calc','difference'):28396000.,
 ('source_reconciliation','core_excess_calc','difference'):31000.,
 ('source_reconciliation','coil_excess_calc','difference'):5287000.,
 ('source_reconciliation','fuel_gap_calc','difference'):1000.,
 ('known_dry_inventory','evaluate','total'):sum([627200,3465000,662500,3280000,1305000,1440000,1333000,2909000]),
 ('inventory_comparison','evaluate','difference'):1333700.,
 ('lipb_comparison','evaluate','difference'):3532000*2.5*17.1-151327000,
 ('source_replacement_comparison','evaluate','difference'):75e6*13-966e6,
 ('source_replacement_comparison','mass','amount'):842000*13,
 ('cost_ledger','evaluate','direct'):2619572000+31000+10*30e6,
 ('cost_ledger','evaluate','overnight'):(2619572000+31000+10*30e6)*1.49,
}
for key,amount in expected.items():check('__'.join(key),f(*key),amount)
for case in ('density_lower','density_higher'):
    for key,val in b['outputs'].items():
        if '__purchase__' in key:
            assert rows[case]['outputs'][key]==val,(case,key)
    assert value(case,'fuel_inventory','annual','annual_burn')!=f('fuel_inventory','annual','annual_burn')
for case in ('u_low','u_high'):
    check(case+' purchase',value(case,'he_hx','purchase','capital'),f('he_hx','purchase','capital'))
for case,ratio in [('area_low',.1),('area_high',1.5)]:
    check(case+' purchase',value(case,'he_hx','purchase','capital'),f('he_hx','purchase','capital')*ratio)
    check(case+' UA',value(case,'he_hx','evaluate','ua'),50*ratio)
for case,q,status in [('stock_low',.01,'violated'),('stock_high',1.,'satisfied')]:
    check(case+' quantity',value(case,'fuel_inventory','atoms','stock_kg'),q,1e-15)
    check(case+' cost',value(case,'fuel_inventory','purchase','amount'),q*30e6)
    check(case+' requirement',value(case,'fuel_inventory','annual','required_stock'),f('fuel_inventory','annual','required_stock'),1e-15)
    report=rows[case]['outputs']['constraint_report']['results']
    target=[x for x in report if x['constraint_id'].startswith(P+'fuel_inventory__capacity_ok__')]
    assert len(target)==1 and target[0]['status']==status
    check(case+' no heat change',value(case,'plant_ledger','evaluate','net_electric'),f('plant_ledger','evaluate','net_electric'),0)
check('source parent propagation',value('source_parent_change','cost_ledger','evaluate','source_reactor_gap'),38396000)
check('source parent leaves selected purchases',value('source_parent_change','cost_ledger','evaluate','direct'),f('cost_ledger','evaluate','direct'))
pipe=ROOT/'exploration/aries_integrated/aries_integrated/pipelines/pipeline.yaml'
modules=yaml.safe_load(pipe.read_text())['modules']
bindings=[]
for owner,calc,arg,channel in [
 ('fuel','evaluate','I_total_in',P+'fuel_inventory__atoms__atoms'),
 ('fuel_inventory','annual','stock_kg_in','plant_params.'+P+'fuel_inventory__selected_tritium_kg'),
 ('fuel_inventory','annual','decay_in','plant_params.'+P+'fuel__decay_constant_s'),
 ('he_hx','purchase','quantity_in','plant_params.'+P+'he_hx__selected_area'),
 ('he_hx','evaluate','area_in','plant_params.'+P+'he_hx__selected_area'),
 ('he_pump','purchase','quantity_in','plant_params.'+P+'he_pump__selected_flow_capacity'),
 ('he_pump','evaluate','flow_in','plant_params.'+P+'heat_exchangers__he_flow'),
 ('cost_ledger','evaluate','source_reactor_gap_in',P+'source_reconciliation__reactor_gap_calc__difference.root')]:
    actual=modules[P+owner+'__'+calc]['inputs'][arg].split(' ',1)[1]
    assert actual==channel,(owner,arg,actual,channel)
    bindings.append(dict(owner=owner,calc=calc,input=arg,channel=channel))
receipt=dict(passed=True,checkpoint='56a83338',fingerprint=v['fingerprint'],cases=v['case_count'],
 checks=checks,bindings=bindings,verification_sha256=hashlib.sha256((E/'verification.json').read_bytes()).hexdigest(),
 pipeline_sha256=hashlib.sha256(pipe.read_bytes()).hexdigest())
Path(__file__).with_suffix('.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(dict(passed=True,checks=len(checks),bindings=len(bindings),cases=v['case_count'])))
