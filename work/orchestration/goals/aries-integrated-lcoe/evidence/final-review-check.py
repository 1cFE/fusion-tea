"""Read-only all-case native-store/export and immutable artifact review."""
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
R=ROOT/'exploration/aries_integrated/studies/20260922-aries-integrated-lcoe'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
snapshot=read(R/'snapshot.json')
assert sha(R/'snapshot.json')=='6f51f7ad251cdec581c556a6c9ab6655e7132142918efe012af52cd2523742c6'
artifacts=snapshot['arms'][0]['artifacts']
assert len(artifacts)==281
for entry in artifacts: assert sha(R/entry['path'])==entry['sha256'],entry['path']
db=R/'results/native/20260922-aries-integrated-lcoe.db'; before=sha(db)
conn=sqlite3.connect(f'file:{db.resolve()}?mode=ro&immutable=1',uri=True);conn.row_factory=sqlite3.Row
store={row['candidate_id']:dict(row) for row in conn.execute('select * from cases')}
rows=read(R/'results/cases.json')['cases']; proposals=read(R/'proposed-points.json')['cases']
assert len(rows)==len(store)==len(proposals)==64
expected={row['case']:row['point'] for row in proposals}
assert len({json.dumps(r['point'],sort_keys=True) for r in proposals})==64
fp='d13f4153accc48a3d6533a2d29a8e8b6b7cecd86644c322bb64f59fa402e419b'
counts=[tuple(row) for row in conn.execute('select state,count(*),count(distinct attempt_id),max(attempt_number) from attempt_transitions group by state')]
assert len(counts)==2 and all(count==unique==64 and maximum==1 for state,count,unique,maximum in counts),counts
numeric_count=0; predicate_count=0; summaries=[];P='aries_integrated_plant__'
for row in rows:
    native=store[row['candidate_id']]
    assert native['state']==row['state']=='completed'
    assert json.loads(native['inputs_json'])==row['inputs']==expected[row['case']]
    assert native['evidence_digest']==row['evidence_digest']
    artifact=R/'results/native/artifacts'/f"{native['evidence_digest']}.json"
    assert sha(artifact)==native['evidence_digest']
    evidence=read(artifact)
    assert evidence['outputs']==row['outputs']
    assert {k:v for k,v in evidence['responses'].items() if k!='headline'}==row['verdicts']
    assert evidence['responses']['headline']==row['headline']
    assert {'full_satisfaction':'satisfied','violation':'violated'}[evidence['report']['headline']]==row['headline']
    assert evidence['provenance']['executable_fingerprint']==row['executable_fingerprint']==fp
    assert len(row['outputs'])==546 and len(row['verdicts'])==14
    numeric_count+=len(row['outputs']);predicate_count+=len(row['verdicts'])
    v=lambda owner,key:row['outputs'][P+owner+'__evaluate__'+key]
    assert v('source_lifecycle_accounts','idc')==0
    assert v('lifecycle_accounts','supply_supported')==v('lifecycle_accounts','breeding_supported')==0
    assert abs(v('lifecycle_price','lcoe')-v('lifecycle_accounts','lcoe_sum'))<1e-8
    summaries.append({'case':row['case'],'lcoe':v('lifecycle_price','lcoe'),'source_lcoe':v('source_lifecycle_price','lcoe'),'net_power':v('plant_ledger','net_electric'),'violations':[k for k,vv in row['verdicts'].items() if vv!='satisfied']})
assert len([r for r in summaries if r['violations']])==4
conn.close();assert sha(db)==before
verification=read(R/'results/verification_summary.json')
assert verification['outcome']=='pass' and len(verification['channels_checked'])==364
assert {t['channel'] for t in verification['absolute_tolerances']}=={P+'plant_ledger__evaluate__residual_magnitude',P+'lifecycle_accounts__evaluate__idc'}
ids=set(__import__('re').findall(r'20260922-aries-integrated-lcoe#(\d+)',(R/'record.md').read_text()))
assert ids=={str(i) for i in range(1,28)}
result={'passed':True,'snapshot_sha256':sha(R/'snapshot.json'),'artifact_count':len(artifacts),'cases':len(rows),'exported_scalar_values_exactly_matching_store':numeric_count,'exported_predicates_exactly_matching_store':predicate_count,'transition_counts':counts,'store_hash_unchanged':True,'findings':len(ids),'case_summaries':summaries}
(HERE/'final-review-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='case_summaries'},indent=2))
for row in summaries:
    if any(s in row['case'] for s in ['availability','density','new-feed','he-area']): print(json.dumps(row))
