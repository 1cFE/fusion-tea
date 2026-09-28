"""Second bounded design probe after inspecting explicit UA feasibility intervals."""
import json
import sys
from pathlib import Path
import importlib.util

sys.dont_write_bytecode=True
path=Path(__file__).with_name('development-probe.py')
spec=importlib.util.spec_from_file_location('probe',path)
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
old=json.loads(path.with_suffix('.json').read_text())
p.OFFERS={'matched_small':(12.,12.,2.),'matched_medium':(18.,18.,2.)}
rows=[]
for load in (1650.,1835.4512830147435,1950.,2000.,2200.):
    for offer in p.OFFERS:
        for flow in range(1100,1651,10):
            for mode,splits in ((0,(.85,)),(1,tuple(i/100 for i in range(40,91,5)))):
                for split in splits:
                    row=p.assess(load,flow,mode,split,offer,old['cold_k'],old['expansion_factor'],old['recuperator_effectiveness'])
                    row['retained_budget_offer_usd2004']=3*58325700.
                    rows.append(row)
summary=[]
for load in sorted({r['load_mw'] for r in rows}):
    for offer in p.OFFERS:
        for mode in (0,1):
            rr=[r for r in rows if (r['load_mw'],r['offer'],r['mode'])==(load,offer,mode)]
            passing=[r for r in rr if r['thermal_pass']]
            best=min(passing,key=lambda r:r['cycle_flow_kg_s'],default=None)
            summary.append({'load_mw':load,'offer':offer,'mode':mode,'points':len(rr),'thermal_passes':len(passing),
                            'minimum_passing_flow':best['cycle_flow_kg_s'] if best else None,'example':best})
result={'kind':'development full-duty feasibility only; no native execution or all-equipment qualification',
        'selection_basis':'First probe series failure exposed divertor UA above permissible interval; 2MW/K is a declared second-stage supplied offer.',
        'offers_ua_mw_k':p.OFFERS,'offered_purchase_per_hx_usd2004':58325700.,'rows':rows,'summary':summary}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'points':len(rows),'thermal_passes':sum(r['thermal_pass'] for r in rows),
                  'summary':[{k:v for k,v in r.items() if k!='example'} for r in summary]},indent=2))
