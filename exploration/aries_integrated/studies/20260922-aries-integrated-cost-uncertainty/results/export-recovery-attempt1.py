"""Recover exports only: exact numeric matching after native float normalization."""
import csv,json,hashlib
from pathlib import Path
from simkit.study.query import StudyQuery
from simkit.study.store import StudyStore
from exploration.aries_integrated.studies import study_route as route
R=Path(__file__).resolve().parent
results=R/'results'; db=results/'native'/f'{R.name}.db'
protected=[p for p in results.rglob('*') if p.is_file() and 'pkg_link' not in p.parts]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={str(p.relative_to(R)):sha(p) for p in protected}
assert not (results/'cases.json').exists()
proposals=json.loads((R/'proposed-points.json').read_text())['cases']
store=StudyStore(db)
try: cases=StudyQuery(store,route.PACKAGE_DIR.resolve()).cases()
finally: store.close()
rows=[]; proof=[]
for case in cases:
    inputs=dict(case.inputs)
    matches=[p for p in proposals if p['point']==inputs]
    assert len(matches)==1
    proposal=matches[0]
    assert route.validate_proposal(proposal['point'])==inputs
    route.require_published(case,route.interface()['channels'])
    route.short_verdicts(case)
    proof.append({'case':proposal['case'],'candidate_id':case.candidate_id,'full_numeric_map_equal':True,'representation_changes':{k:{'declared_type':type(v).__name__,'stored_type':type(inputs[k]).__name__,'value':v} for k,v in proposal['point'].items() if type(v)!=type(inputs[k])}})
    rows.append({'case':proposal['case'],'candidate_id':case.candidate_id,'state':case.state,'inputs':inputs,'outputs':dict(case.outputs),'verdicts':dict(case.verdicts),'executable_fingerprint':case.executable_fingerprint,'evidence_digest':case.evidence_digest,'headline':case.headline,'disposition':case.disposition})
assert len(rows)==113 and len({r['case'] for r in rows})==113
assert all(r['state']=='completed' for r in rows)
assert all(sha(R/p)==digest for p,digest in before.items())
(results/'cases.json').write_text(json.dumps({'store':str(db.relative_to(route.REPO_ROOT)),'cases':rows},indent=2)+'\n')
columns=['case','candidate_id','state',*sorted(route.interface()['channels']),*sorted(route.interface()['constraints'])]
with (results/'cases.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader()
    for row in rows: writer.writerow({k:row[k] for k in ('case','candidate_id','state')}|{k:row['outputs'][v] for k,v in route.interface()['channels'].items()}|row['verdicts'])
(results/'export-recovery-proof.json').write_text(json.dumps({'scope':'Read-only export of original queried evidence; zero native evaluations; exact numeric equality, no tolerance.','source_hashes_unchanged':before,'cases':proof},indent=2)+'\n')
print(json.dumps({'exported':len(rows),'completed':len(rows),'native_evaluations':0,'original_receipts_unchanged':True}))
