"""Narrow follow-up when initial oracle resolution misses a declared stability target.

Preserves initial proposal/selection documents and their hashes. Reconstructs
initial full scan exactly from its retained prefix. No native execution here.
"""
import hashlib
import json
from pathlib import Path
import runpy
import shutil

module=runpy.run_path(str(Path(__file__).with_name('r3-prepare-study.py')))
Scout=module['Scout'];record=module['RECORD'];read=module['read'];write=module['write']
assert not (record/'snapshot.json').exists(),'never alter a sealed study'
scan_path=record/'oracle-scan.json';old_bytes=scan_path.read_bytes();scan=read(scan_path)
s=Scout();s.rows=scan['cases'];s.selected=read(record/'oracle-selection.json')['selected']
s.cache={tuple(sorted((s.base|r['changes']).items())):r for r in s.rows}
proposed=read(record/'proposed-points.json');s.aliases=proposed['aliases']
s.proposals={tuple(sorted(r['point'].items())):r for r in proposed['cases']}
initial_count=len(s.rows);updates=[]
for selection in s.selected:
    if selection.get('stability_pass',True):continue
    best=s.rows[selection['best_scan_id']];m=best['metadata'];prior=best;rounds=[]
    for spacing in (.00025,.000125,.0000625):
        center=best['metadata']['split'];options=[best]
        for j in range(-4,5):
            split=round(center+j*spacing,10)
            if not .001<=split<=.999:continue
            r=s.line(m['load'],m['offer'],m['mode'],split,m['scenario'])
            if r:
                s.propose(r,'additional-resolution-refinement');options.append(r)
        best=max(options,key=lambda r:r['net'])
        change={'split_spacing':spacing,'before_scan_id':prior['scan_id'],'after_scan_id':best['scan_id'],'delta_net':best['net']-prior['net'],'delta_lcoe':best['lcoe']-prior['lcoe']}
        rounds.append(change)
        stable=abs(change['delta_net'])<=.2 and abs(change['delta_lcoe'])<=.1
        prior=best
        if stable:break
    f=best['metadata']['flow'];split=best['metadata']['split'];before=best
    for df in (-.0125,-.00625,0,.00625,.0125):
        r=s.get(m['load'],m['offer'],m['mode'],f+df,split,m['scenario'])
        s.propose(r,'additional-resolution-final-flow')
        if r['pass'] and r['net']>best['net']:best=r
    selection.update(best_scan_id=best['scan_id'],additional_refinement=rounds,stability_pass=stable and abs(best['net']-before['net'])<=.2 and abs(best['lcoe']-before['lcoe'])<=.1)
    updates.append({'load':m['load'],'offer':m['offer'],'mode':m['mode'],'scenario':m['scenario'],'rounds':rounds,'best_scan_id':best['scan_id'],'stability_pass':selection['stability_pass']})
# Fine negative search for no-series main cases: a sampled absence remains a
# sampled absence, but cannot be attributed solely to the initial 50 kg/s mesh.
negative=[]
for selection in s.selected:
    if selection['scenario']!='main' or selection['mode']!=0 or selection['best_scan_id'] is not None:continue
    rows=[s.get(selection['load'],selection['offer'],0,float(f),.85,'main') for f in range(1000,1751)]
    passing=[r for r in rows if r['pass']]
    if passing:raise RuntimeError('Finer negative check discovered passing series window; retain evidence and refine it before native execution.')
    negative.append({'load':selection['load'],'offer':selection['offer'],'mode':0,'flow_range':[1000,1750,1],'count':len(rows),'passing':0,'scan_ids':[r['scan_id'] for r in rows]})
for name in ('oracle-selection.json','proposed-points.json'):
    shutil.copyfile(record/name,record/(name[:-5]+'-initial.json'))
write(record/'oracle-refinement-receipt.json',{'initial_scan_sha256':hashlib.sha256(old_bytes).hexdigest(),'initial_count':initial_count,'initial_reconstruction':'oracle-scan.json with cases truncated to initial_count and compact JSON separators plus terminal newline','added_count':len(s.rows)-initial_count,'updates':updates,'negative_checks':negative})
def replace(name,value):
    path=record/name;temp=path.with_suffix(path.suffix+'.next');write(temp,value);temp.replace(path)
replace('oracle-scan.json',scan|{'cases':s.rows})
replace('oracle-selection.json',{'selected':s.selected,'scope':'Best tested passing operations; sampled components, no global optimum proof.'})
replace('proposed-points.json',{'cases':list(s.proposals.values()),'aliases':s.aliases})
print(json.dumps({'additional_points':len(s.rows)-initial_count,'updates':updates,'negative_checks':[{k:v for k,v in r.items() if k!='scan_ids'} for r in negative],'native_proposals':len(s.proposals)}))
