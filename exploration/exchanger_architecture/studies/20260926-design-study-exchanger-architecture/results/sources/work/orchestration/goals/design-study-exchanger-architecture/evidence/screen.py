import json,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from exploration.aries_integrated.studies import oracle_entry as o
P='aries_integrated_plant__'
f=Path('exploration/aries_integrated/studies/20260925-aries-revised-reference-network/results/cases.json')
b=next(r['inputs'] for r in json.loads(f.read_text())['cases'] if r['case']=='nominal-calculated')
rows=[]
for load in (1650.,1835.451,2100.,2220.896,2300.,2427.384,2600.):
 for flow in (1400.,1600.):
  for mode,split in [(0,.85)]+[(1,s) for s in (.5,.6,.7,.75,.8,.85,.9,.95)]:
   pt=dict(b);pt.update({P+'source__producer_mode':0.,P+'source__reference_fusion_mw':load,P+'cycle__selected_flow':flow,P+'heat_exchangers__network_mode':mode,P+'heat_exchangers__pbli_split_fraction':split})
   try:
    v=o.evaluate(pt)
    row={'load':load,'flow':flow,'mode':mode,'split':split,'net':v[P+'plant_ledger__evaluate__net_electric'],'unmet':v[P+'heat_exchangers__evaluate__unmet_heat']}
    row['oracle_outputs']=v
    rows.append(row)
   except Exception as e: rows.append({'load':load,'flow':flow,'mode':mode,'split':split,'error':str(e)})
Path('work/orchestration/goals/design-study-exchanger-architecture/evidence/screen.json').write_text(json.dumps(rows,indent=2)+'\n')
for load in sorted({r['load'] for r in rows}):
 for flow in (1400.,1600.):
  rs=[r for r in rows if r['load']==load and r['flow']==flow]
  print(load,flow,[(r['mode'],r['split'],round(r.get('net',0),2),round(r.get('unmet',0),2)) for r in rs if r['mode']==0 or r.get('unmet',999)<1e-6])
print('errors', [r for r in rows if 'error' in r][:2])
