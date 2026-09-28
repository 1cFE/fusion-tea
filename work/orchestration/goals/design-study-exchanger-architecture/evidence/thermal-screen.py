import json, sys
from pathlib import Path
ROOT=Path('/home/reid/1cfe/fusion-tea')
sys.path.insert(0,str(ROOT))
from exploration.aries_integrated.studies import study_route as route
src=ROOT/'exploration/aries_integrated/studies/20260926-aries-design-choice-interactions/results/cases.json'
rows=json.loads(src.read_text())['cases']
base=next(r for r in rows if r['case']=='b3-N-amp5.00e20-hol0.66-net0') if any(r['case']=='b3-N-amp5.00e20-hol0.66-net0' for r in rows) else None
if base is None:
 config=json.loads((src.parent.parent/'config.json').read_text())
 name=config['aliases']['b3-N-amp5.00e20-hol0.66-net0']
 base=next(r for r in rows if r['case']==name)
P='aries_integrated_plant__'
point=base['inputs']
amp=next(k for k in point if k.endswith('__amplitude'))
proposals=[]; names=[]
for density in (5.0,5.5,5.6,5.75):
 for mode,split in [(0,.85)]+[(1,s) for s in (.55,.65,.75,.80,.85,.90,.95)]:
  proposals.append(point|{amp:density*1e20,P+'heat_exchangers__network_mode':mode,P+'heat_exchangers__pbli_split_fraction':split})
  names.append(f'n{density}-m{mode}-s{split}')
work=Path('/tmp/thermal-screen-run')
cases,db=route.run_points('thermal-screen-audit-v1',proposals,work)
# Query order is not the proposal order: join by full input maps.
by_point={tuple(sorted(c.inputs.items())):c for c in cases}
result=[]
for name,p in zip(names,proposals):
 c=by_point[tuple(sorted(p.items()))]
 o=c.outputs
 def out(part,k):return o.get(P+part+'__evaluate__'+k)
 r={'case':name,'state':c.state,'fus':out('source','selected_power'),'net':out('plant_ledger','net_electric'),'unmet':out('heat_exchangers','unmet_heat'),'tt':out('heat_exchangers','turbine_temperature'),'violated':[k for k,v in c.verdicts.items() if v!='satisfied']}
 for b in ('he','pbli','divertor'):
  for k in ('unmet','hot','return','hot_terminal_difference','cold_terminal_difference'):
   r[b+'_'+k]=out('heat_exchangers',b+'_'+k)
 result.append(r)
print(json.dumps({'baseline_case':base['case'],'baseline_inputs':{k:v for k,v in point.items() if any(s in k for s in ('plasma__','heat_exchangers__','cycle__','compressor_','deposition__auxiliary','selected_area','coefficient','capacity__selected_rating'))},'baseline_outputs':{k:v for k,v in base['outputs'].items() if any(s in k for s in ('plant_ledger__evaluate__','coolant__evaluate__','pump__evaluate__electric','hx__conductance'))},'results':result},indent=2))
(work/'summary.json').write_text(json.dumps(result,indent=2))
