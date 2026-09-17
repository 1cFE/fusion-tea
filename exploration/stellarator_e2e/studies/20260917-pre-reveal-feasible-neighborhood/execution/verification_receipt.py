"""Record the generic verifier's actual early refusal and all-point check separately."""
import json
from pathlib import Path
from scripts.study import verify,common
from simkit.study.store import StudyStore
from simkit.study.query import StudyQuery
from exploration.stellarator_e2e.studies import study_route as route
H=Path(__file__).resolve().parents[1];R=H/'results';read=lambda p:json.loads(p.read_text())
db=H/read(R/'execution-summary.json')['store'];s=StudyStore(db)
try:
 digest,fields=verify.compatibility_digest(s);cases=StudyQuery(s,route.PACKAGE_DIR.resolve()).cases()
finally:s.close()
seed=verify.derive_seed(fields['study_id'],digest);sample,strata=verify.stratified_sample(cases,40,seed);ids=[c.candidate_id for c in sample];failure=H.name+':c0000';attempted=ids[:ids.index(failure)+1]
message=(R/'generic-verification.log').read_text().strip();assert failure in message and 'margin_fraction' in message and 'channel off tolerance' in message
command=['scripts/study/verify.py','--package',str(route.PACKAGE_DIR.relative_to(H.parents[3])),'--manifest',str(route.MANIFEST_PATH.relative_to(H.parents[3])),'--identity',str((R/'package_identity.json').relative_to(H.parents[3])),'--store',str(db.relative_to(H.parents[3])),'--sample-size','40','--out',str((R/'verification_summary.json').relative_to(H.parents[3]))]
receipt={'schema_version':'study-local-generic-verification-refusal/v1','author':'coordinator receipt of original stderr; not an emitted verifier summary','outcome':'refused-known-exact-boundary','command':command,'tool':{'path':'scripts/study/verify.py','source_digest':common.tool_source_digest(verify.TOOL_SOURCE_FILES)},'message':message,'official_summary_emitted':False,'stores':[{'path':str(db.relative_to(H)),'sampling':{'planned_sampled_case_ids':ids,'sampled_case_ids':attempted,'sampled_rows':len(attempted),'strata_observed':strata,'seed':hex(seed),'count_basis':'Reconstructed deterministic sample order and first thrown error; check_case calls oracle once, loop aborts on first error.'}}]}
(R/'generic-verification-refusal.json').write_text(json.dumps(receipt,indent=2)+'\n')
a=read(R/'oracle-all-points.json');assert not a['failures'];assert len(a['boundary_exceptions'])==3
assert all('conductor_current__margin_' in x['channel'] for x in a['strict_relative_misses'])
summary=a|{'schema_version':'study-local-all-point-verification/v1','tool':{'path':str((H/'execution/analyze.py').relative_to(H.parents[3])),'source_digest':common.tool_source_digest((str((H/'execution/analyze.py').relative_to(H.parents[3])),))},'command':['execution/analyze.py'],'generic_verifier':'generic-verification-refusal.json','scope':'All mapped native scalars and all20 independently derived predicates; exact boundary exceptions preserved. Generic strict-relative verifier did not pass.'}
(R/'verification_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Generic oracle calls before refusal',len(attempted),'; all-point summary',a['outcome'])
