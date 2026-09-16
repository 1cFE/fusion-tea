"""Scan exactly the candidate diagnostic sample with the independent current oracle."""
import json
from pathlib import Path
from collections import Counter
from exploration.stellarator_e2e.studies import oracle_entry as oe, study_route as route
from scripts.study.verify import derive_verdict, package_input_values

H=Path(__file__).resolve().parents[1]
R=H/'results'
read=lambda p:json.loads(p.read_text())
assert read(R/'preflight_results.json')['outcome']=='pass'
assert read(H/'preparation/execution-release.json')['authorized_by']=='coordinator'
params=package_input_values(route.PACKAGE_DIR)
catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR)
bindings=oe.operand_bindings()
rows=[]
for row in read(H/'preparation/scan-proposals.json'):
    point=row['point']
    try:
        channels=oe.evaluate(point)
        verdicts={cid:'satisfied' if derive_verdict(cid,e,bindings,point,params,channels)[0] else 'violated' for cid,e in catalog.items()}
        rows.append(row|{'outcome':'evaluated','channels':channels,'verdicts':verdicts,'violated':[catalog[c]['source_local_identity'] for c,v in verdicts.items() if v!='satisfied'],'full_satisfied':all(v=='satisfied' for v in verdicts.values())})
    except Exception as error:
        rows.append(row|{'outcome':'refused','error':repr(error),'full_satisfied':False,'interpretation':'Retained evaluation refusal; requires coordinator review before refinement.'})
result={'rows':rows,'states':dict(Counter(r['outcome'] for r in rows)),'all_predicate_passes':sum(r['full_satisfied'] for r in rows),'window_status':'Scanned diagnostic candidates, no search boundary or feasibility-bracket claim.'}
(R/'oracle-scan.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print('Scan:',result['states'],'all-predicate passes',result['all_predicate_passes'])
assert all(r['outcome']=='evaluated' for r in rows), 'Refusals retained; review before points'
