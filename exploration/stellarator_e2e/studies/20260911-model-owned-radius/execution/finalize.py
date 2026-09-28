"""Finish record metadata/registration; never execute or alter numeric case evidence."""
import json,hashlib,os,re
from pathlib import Path
H=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def artifacts(directory):
 out=[]
 for root,dirs,files in os.walk(directory,followlinks=False):
  dirs[:]=[d for d in dirs if d not in ['runtime-links','pkg_link','__pycache__','pytest-cache'] and not (Path(root)/d).is_symlink()]
  for name in sorted(files):
   p=Path(root)/name
   if p.is_symlink() or name.endswith(('.db-wal','.db-shm','.pyc')):continue
   out.append({'path':str(p.relative_to(H)),'sha256':sha(p)})
 return sorted(out,key=lambda x:x['path'])
p=H/'record.md';s=p.read_text()
s=s.replace('All seven analytic ratio checks use held inputs and the baseline','All six analytic ratios pass at all seven points using held inputs and the baseline')
producer=H/'execution/report.py';t=producer.read_text().replace('All seven analytic ratio checks use held inputs and the baseline','All six analytic ratios pass at all seven points using held inputs and the baseline');producer.write_text(t)
s=s.replace('complete numerical results, fresh final review pending','finalized executor record; parent freeze commit pending')
s=s.replace('| Fresh final correctness, honesty and readability | Pending | A new no-history reviewer must assess this complete record before final handback. |','| Fresh final correctness, honesty and readability | Correctness POSITIVE; honesty POSITIVE; readability POSITIVE with minor F1 | Corrected ratio count to six at seven points (42 comparisons); no numerical rerun needed. Original review: reviews/final-review.md; disposition: reviews/final-disposition.md. |')
s=s.replace('Native first-sighting rows for this record will be appended before handback; goal dispositions and residual acceptance remain separate.','The native executor appended first-sighting rows for this record before handback; goal dispositions and residual acceptance remain separate.')
findings=read(H/'preparation/findings.json')
extras=[['4','process','Pre-execution critique required populated record arguments and truthful preparatory-baseline identity/coverage.','Resolved before points: explicit nil provenance under native schema, exact 18-response catalog check and populated framing; original conditional review retained.','reviews/pre-execution-disposition.md'],['5','process','Initial report-builder invocation omitted the repository import path and failed before report execution.','Corrected launcher configuration only; original failed log retained, no model rerun or numerical change.','execution/commands.md'],['6','process','Final review found the prose counted seven analytic checks instead of six ratios at seven points.','Corrected wording to six ratios and 42 comparisons; evidence unchanged and objective correction directly checked.','reviews/final-disposition.md']]
for row in extras:
 if row[0] not in {x[0] for x in findings}:findings.append(row)
write(H/'preparation/findings.json',findings)
start=s.index('## 15. Findings');end=s.index('## 16. Snapshot')
s=s[:start]+'## 15. Findings\n\n| Id | Kind | Finding | Disposition | Home |\n|---|---|---|---|---|\n'+'\n'.join(f'| `{H.name}#{n}` | {k} | {f} | {d} | {home} |' for n,k,f,d,home in findings)+'\n\nFindings #2 and #3 are current-study sightings of inherited limitations, not claims of first-ever discovery. The native executor appended all six first-sighting rows before handback. No goal disposition or residual acceptance is executed.\n\n'+s[end:]
log=H.parent/'DISCOVERY_LOG.md'
# Append only; never rewrite prior or concurrently added rows.
existing=log.read_text();added=[]
for n,k,f,d,home in findings:
 identifier=H.name+'#'+n
 if '| `'+identifier+'` |' not in existing:
  added.append(f'| 2026-09-11 | `{k}` | `{identifier}` | {f} | {d} | `{H.name}/{home}` |' if home.startswith(('reviews/','execution/')) else f'| 2026-09-11 | `{k}` | `{identifier}` | {f} | {d} | {home} |')
if added:
 with log.open('a') as f:f.write(('' if existing.endswith('\n') else '\n')+'\n'.join(added)+'\n')
s=s.replace('Resolved numerical evidence, store identity, copied basis and source provenance are present. Fresh final review and record-only publication checks remain pending. Parent owns the freeze commit.','Resolved numerical evidence, native store identity, copied basis/source provenance, fresh review dispositions and publication checks are present. Snapshot values are finalized for the parent-owned freeze commit. Native record validation is recorded in execution/native-record-tests.log; full artifact validation in execution/record-validation.log.')
snap=read(H/'snapshot.json');snap['status']='Finalized executor evidence; reviews dispositioned; six findings registered; parent owns freeze commit'
for field,directory in [('result_artifacts','results'),('context_artifacts','context'),('preparation_artifacts','preparation'),('execution_artifacts','execution'),('review_artifacts','reviews'),('diagnostic_artifacts','diagnostics')]:snap[field]=artifacts(H/directory)
snap['arms'][0]['artifacts']=snap['result_artifacts']
snap['findings_registration']={'ids':[H.name+'#'+r[0] for r in findings],'writer':'native T-026 executor','status':'six first sightings appended; no goal dispositions','date':'2026-09-11'}
snap['gaps']=[g.replace('No administrator synthesis or parent freeze commit yet.','Administrator synthesis and parent freeze commit are separate subsequent actions.') for g in snap['gaps']]
snap['support_artifacts']=[{'path':p,'sha256':sha(H/p)} for p in ['study.py','axes.json','.gitignore']]
write(H/'snapshot.json',snap)
s=re.sub(r'(- \*\*sha256:\*\* )[0-9a-f]{64}',lambda m:m.group(1)+sha(H/'snapshot.json'),s)
assert '<' not in s
p.write_text(s)
print('Record finalized; six discovery IDs registered; snapshot refreshed; no numerical evidence rerun')
