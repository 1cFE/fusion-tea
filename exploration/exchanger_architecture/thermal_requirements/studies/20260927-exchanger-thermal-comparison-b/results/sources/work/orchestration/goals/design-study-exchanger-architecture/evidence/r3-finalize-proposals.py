"""Complete final oracle-scoped proposals before native execution, no model edits."""
import hashlib
import json
from pathlib import Path
import runpy
import shutil

m=runpy.run_path(str(Path(__file__).with_name('r3-prepare-study.py')))
Scout=m['Scout'];record=m['RECORD'];read=m['read'];write=m['write'];key=m['key'];branches=m['BRANCHES']
assert not (record/'results').exists() and not (record/'snapshot.json').exists()
s=Scout();scan=read(record/'oracle-scan.json');s.rows=scan['cases'];s.selected=read(record/'oracle-selection.json')['selected']
s.cache={tuple(sorted((s.base|r['changes']).items())):r for r in s.rows}
proposed=read(record/'proposed-points.json');s.aliases=proposed['aliases'];s.proposals={tuple(sorted(r['point'].items())):r for r in proposed['cases']}
start=len(s.rows);before=len(s.proposals)
assert all(r.get('stability_pass',True) for r in s.selected),'refinement still unresolved'
assert all(not r['edge_passes'] for r in s.selected),'sampled passing edge needs disposition'
for selection in s.selected:
    if selection['best_scan_id'] is None:
        candidates=[r for r in s.rows if r['status']=='evaluated' and r['net']>0 and all(r['metadata'].get(k)==selection[k] for k in ('load','offer','mode','scenario'))]
        if candidates:
            best=min(candidates,key=lambda r:(len(r['failed']),-r['net']))
            s.propose(best,'no-passing-sample-failure-witness')
        s.propose(s.get(selection['load'],selection['offer'],selection['mode'],1400.,.7 if selection['mode'] else .85,selection['scenario']),'no-passing-sample-standard-control')
        continue
    if selection['scenario']!='main':continue
    parent=s.rows[selection['best_scan_id']]
    for scenario,factor in (('zero-tritium',0.),('price-half',.5),('price-double',2.),('linear-area-price',1.)):
        p=s.base|parent['changes'];meta=parent['metadata']|{'scenario':scenario,'parent_scan_id':parent['scan_id']}
        if scenario=='zero-tritium':p[key('fuel_inventory','tritium_price')]=0.
        else:
            for b in branches:p[key(b+'_hx','price_factor')]=1. if scenario=='linear-area-price' else p[key(b+'_hx','price_factor')]*factor
        s.propose(s.evaluate(p,meta),'final-selection-financial-sensitivity')
for scenario,source_mode in (('legacy-calculated',1.),('legacy-supplied',0.)):
    p=dict(s.base);p[key('source','producer_mode')]=source_mode
    if not source_mode:p[key('source','reference_fusion_mw')]=m['LOADS'][1]
    meta=dict(load=m['LOADS'][1],offer='original',mode=0,flow=p[key('cycle','selected_flow')],split=p[key('heat_exchangers','pbli_split_fraction')],scenario=scenario)
    s.propose(s.evaluate(p,meta),'legacy-replay-control')
shutil.copyfile(record/'proposed-points.json',record/'proposed-points-refined.json')
def replace(name,value):
    path=record/name;temp=path.with_suffix(path.suffix+'.next');write(temp,value);temp.replace(path)
replace('oracle-scan.json',scan|{'cases':s.rows})
replace('proposed-points.json',{'cases':list(s.proposals.values()),'aliases':s.aliases})
ledger=[]
for row in s.rows:
    ident=tuple(sorted((s.base|row['changes']).items()))
    native=s.proposals.get(ident)
    if row['status']=='refused':status='oracle-refused';reason=row['error']
    elif row['net']<=0:status='excluded-from-native-lcoe';reason='nonpositive net electricity outside inherited lifecycle domain'
    elif native:status='native-proposal';reason=native['classification']
    else:status='oracle-scan-only';reason='retained window/scouting evidence; not a native result'
    ledger.append({'scan_id':row['scan_id'],'metadata':row['metadata'],'status':status,'reason':reason,'native_case':native['case'] if native else None,'oracle_pass':row['pass'],'oracle_failed':row.get('failed',[])})
write(record/'candidate-ledger.json',{'cases':ledger,'scan_count':len(s.rows),'native_count':len(s.proposals)})
write(record/'proposal-finalization.json',{'new_oracle_points':len(s.rows)-start,'new_native_proposals':len(s.proposals)-before,'final_scan_count':len(s.rows),'final_native_count':len(s.proposals),'all_selected_stability_targets_pass':True,'sampled_competitive_edges_open':False,'scope':'Sampled components; no global absence proof. Native failure witnesses added for no-pass groups; all final main winners receive executed financial endpoints.'})
print(json.dumps({'scan_count':len(s.rows),'native_count':len(s.proposals)}))
