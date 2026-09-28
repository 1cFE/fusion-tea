import json,sys,math
from pathlib import Path
ROOT=Path('/home/reid/1cfe/fusion-tea');sys.path.insert(0,str(ROOT))
from exploration.aries_integrated.studies import study_route as route
P='aries_integrated_plant__'
r=ROOT/'exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture'
base=json.loads((r/'baseline-control.json').read_text())['inputs']
variants=[('baseline',base)]
for branch in ('he','pbli','divertor'):
 variants.append((branch+'-25000',base|{P+branch+'_hx__selected_area':25000.}))
for area in (5000.,10000.,20000.,30000.):
 variants.append(('all-'+str(int(area)),base|{P+b+'_hx__selected_area':area for b in ('he','pbli','divertor')}))
cases,db=route.run_points('r3-cost-boundary-probe',[p for _,p in variants],Path('/tmp/r3-cost-boundary-probe'))
lookup={tuple(sorted(c.inputs.items())):c for c in cases}
b=lookup[tuple(sorted(base.items()))].outputs
get=lambda o,owner,calc,field:o[P+owner+'__'+calc+'__'+field]
rows=[]
for name,p in variants:
 c=lookup[tuple(sorted(p.items()))]
 if c.state!='completed':raise RuntimeError(name+' '+str(c.state))
 o=c.outputs
 d=sum((p[P+br+'_hx__selected_area']-base[P+br+'_hx__selected_area'])*58325700/50000 for br in ('he','pbli','divertor'))
 channels={}
 for owner,calc,field,expected in [('direct_cost','evaluate','total',d),('cost_ledger','evaluate','overnight',1.49*d),('indirect_cost','evaluate','cost',.2*d),('contingency','evaluate','cost',.24*d),('owner_commissioning','evaluate','amount',.05*d),('lifecycle_accounts','evaluate','financed_capital',1.49*1.05**3*d),('lifecycle_accounts','evaluate','other_overhaul_cost',1.49*.05*d),('lifecycle_accounts','evaluate','gross_terminal',1.49*.1*d),('lifecycle_accounts','evaluate','salvage',1.49*.02*d),('replacement','evaluate','event_cost',0),('cost_ledger','evaluate','annual_operating',0)]:
  actual=get(o,owner,calc,field)-get(b,owner,calc,field)
  assert math.isclose(actual,expected,abs_tol=1e-5,rel_tol=1e-12),(name,owner,field,actual,expected)
  channels[owner+'.'+field]=actual
 rows.append({'case':name,'direct_delta':d,'validated_deltas':channels,'area':{br:p[P+br+'_hx__selected_area'] for br in ('he','pbli','divertor')},'cost':{br:get(o,br+'_hx','purchase','capital') for br in ('he','pbli','divertor')},'extrapolated':{br:get(o,br+'_hx','purchase','extrapolated') for br in ('he','pbli','divertor')},'native_engineering_failures':[k for k,v in c.verdicts.items() if v!='satisfied'],'net':get(o,'plant_ledger','evaluate','net_electric')})
print(json.dumps({'outcome':'pass','count':len(rows),'store':str(db),'rows':rows},indent=2))
