"""Resolve final record metadata; never rerun or rewrite numeric result evidence."""
import json,hashlib,re
from pathlib import Path
H=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
record=H/'record.md';s=record.read_text()
s=s.replace('execute; results and draft report ready for fresh final review. Final registration and commit remain pending.','execute; final review dispositioned, findings registered, evidence finalized for parent commit.')
s=s.replace('on sealed candidate','on sealed executable fingerprint')
s=s.replace('| Fresh correctness, honesty and readability review | Pending | Parent will arrange a fresh non-author review before registration and final freeze. |','| Fresh correctness, honesty and readability review | FINDINGS; correctness, honesty and readability PASS within stated scope | Minor F1 corrected: executable fingerprint is accurately labeled. Parent accepted direct verification without rerun; original review preserved in execution/final-review.md and disposition in execution/finalization.md. |')
s=s.replace('failed script/results retained and fresh final review required.','failed script/results retained; fresh final review passed its stated numerical and honesty scope.')
s=s.replace('These are proposed first-sighting rows for final review. Discovery-log registration and the final commit are pending parent authorization; no goal disposition is executed by this draft.','All six first-sighting IDs were registered by the native executor in the append-only discovery log before finalization. Proposed modeling dispositions remain subject to the later goal review. No goal disposition is executed by this record.')
s=s.replace('Draft snapshot resolved from present artifacts. Parent will refresh after fresh review and before final registration/freeze. All result and copied-context artifacts carry digests; study arms reference one complete compatibility tuple.','Final snapshot resolved after fresh review, disposition and findings registration. Committed-facing result, preparation, execution and copied-context artifacts carry digests; local runtime artifacts are separately labeled. Study arms reference one complete compatibility tuple. Parent owns the final commit.')
s=s.replace('There is no fresh final review, discovery-log registration, final record commit, administrator synthesis or goal disposition yet.','Administrator synthesis and goal dispositions are separate later work. Parent commits this finalized executor record.')
# Idempotent first-sighting append, preserving all historical rows.
log=H.parent/'DISCOVERY_LOG.md';previous=log.read_text();new=[]
for line in s.splitlines():
 if line.startswith('| `'+H.name+'#'):
  cells=[c.strip() for c in line.strip('|').split('|')];identifier,kind,finding,disposition,home=cells
  if identifier not in previous:new.append(f'| 2026-09-11 | `{kind}` | {identifier} | {finding} | {disposition} | {home} |')
if new:log.write_text(previous.rstrip()+'\n'+'\n'.join(new)+'\n')
snap=json.loads((H/'snapshot.json').read_text());snap['status']='Finalized executor evidence; final review dispositioned and findings registered; parent owns commit'
local=[];published=[]
for a in snap['result_artifacts']:
 if any(a['path'].startswith('results/'+d+'/') for d in ['_work','_study','_runtime']):local.append({**a,'availability':'local runtime only; excluded from version control'})
 else:published.append(a)
if local:snap['local_runtime_artifacts']=local
snap['result_artifacts']=published
for arm in snap['arms']:arm['artifacts']=published
for key,directory in [('context_artifacts','context'),('execution_artifacts','execution'),('preparation_artifacts','preparation')]:
 snap[key]=[{'path':str(p.relative_to(H)),'sha256':sha(p)} for p in sorted((H/directory).glob('*')) if p.is_file()]
snap['record_support_artifacts']=[{'path':str(p.relative_to(H)),'sha256':sha(p)} for p in [H/'.gitignore',H/'study.py',H/'axes.json',H/'indicators.json']]
snap['baseline_store_note']='Native runtime stores, evidence bodies and sidecars are excluded by record-local .gitignore and labeled local_runtime_artifacts. Complete exported numerical evidence and inputs are in committed-facing result_artifacts. The baseline preparation store is not a comparison arm.'
snap['findings_registration']={'ids':[H.name+'#'+str(i) for i in range(1,7)],'writer':'native T-019 executor','date':'2026-09-11','status':'first sightings appended before final commit','goal_dispositions':'not executed'}
(H/'snapshot.json').write_text(json.dumps(snap,indent=2)+'\n')
s=re.sub(r'(- \*\*sha256:\*\* )[0-9a-f]{64}',lambda m:m.group(1)+sha(H/'snapshot.json'),s)
assert '<' not in s
record.write_text(s)
print('Final metadata resolved; numerical results unchanged')
