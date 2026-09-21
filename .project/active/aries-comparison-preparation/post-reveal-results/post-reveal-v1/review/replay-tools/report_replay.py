"""Pure reporting replay from original evidence; no physical evaluation."""
import collections,hashlib,json,pathlib,sys
root=pathlib.Path('/home/reid/1cfe/fusion-tea'); reg=root/'.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=read(reg/'review/replay-receipt.json')
sys.path.insert(0,str(pathlib.Path(r['restored_root'])/'.project/active/aries-comparison-preparation/post-reveal-preparation/tools'))
import adapter as a, report
original=reg/'reports/first-forward'
assert all(sha(original/p)==h for p,h in read(original/'receipt.json')['artifacts'].items())
assert sha(reg/'observations.json')==sha(original/'observations.raw.json')=='e4305c2dafef62f5e0d0151dd11eb3c82b3d530ba50fe108632b5c9fd30a958e'
expected=read(original/'report.json')
replayed=report.report(reg/'attempts/first-forward',original/'observations.raw.json',reg/'replay-verification/reports','independent-replay')
assert replayed['state']=='reported'
differences={k:{'original':expected.get(k),'replay':replayed.get(k)} for k in expected.keys()|replayed.keys() if expected.get(k)!=replayed.get(k)}
assert set(differences)<= {'first_report_attempt'}
assert expected['numerical_comparison']==replayed['numerical_comparison']
assert expected['current_predicates']==replayed['current_predicates']=={}
assert expected['attempt_artifacts']==r['original_artifact_hashes']
assert all(sha(reg/'attempts/first-forward'/p)==h for p,h in r['original_artifact_hashes'].items())
rows=replayed['numerical_comparison']['rows']; assert len(rows)==276
r.update(report_replay='passed',original_report_sha256=sha(original/'report.json'),original_report_receipt_verified=True,replayed_report_sha256=sha(reg/'replay-verification/reports/independent-replay/report.json'),observations_sha256=sha(original/'observations.raw.json'),report_differences=differences,scientific_comparison_exact=True,current_predicates_exact=True,input_evidence_identity_exact=True,original_attempt_unchanged_after_report=True,report_status_counts=dict(collections.Counter(x['status'] for x in rows)))
(reg/'review/replay-receipt.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps({'differences':differences,'status_counts':r['report_status_counts'],'numerical_keys':list(replayed['numerical_comparison'])},indent=2))
