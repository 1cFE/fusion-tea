"""Independent preparation checks; no reference request is executed."""
import hashlib,json,sys
from pathlib import Path
repo=Path.cwd(); prep=repo/'.project/active/aries-comparison-preparation/post-reveal-preparation'
restoration=json.loads((prep/'evidence/review/final-restoration.json').read_text()); scratch=Path(restoration['scratch']); tools=Path(restoration['restored_tools']);sys.path.insert(0,str(tools))
import adapter as a, observations as o, report as r
n=a.strict((scratch/'executions/baseline/result.json').read_bytes());report=a.strict((scratch/'reports/baseline/report.json').read_bytes())
assert n['state']=='completed' and len(n['outputs'])==1352 and len(n['verdicts'])==67 and len(n['effective_inputs'])==704
assert sum(v=='violated' for v in n['verdicts'].values())==6
assert report['state']=='reported' and len(report['numerical_comparison']['rows'])==276
assert not any(row['independent_credit'] for row in report['numerical_comparison']['rows'])
author=prep/'package/restoration-receipt.json';author_receipt=a.strict(author.read_bytes())
assert author_receipt['archive_sha256']==restoration['archive_sha256']
for key,digest in author_receipt['evidence'].items():assert a.sha(prep/'package'/key)==digest,key
other=a.strict((prep/'package/restoration-evidence/attempts/baseline/result.json').read_bytes());assert n['outputs']==other['outputs'] and n['verdicts']==other['verdicts']
checks=[]
for index,payload in enumerate(['{','{"state":"completed"}']):
 attempt,_=a.reserve(scratch/f'partial-{index}','first');(attempt/'result.json').write_text(payload)
 obs=scratch/f'partial-{index}.json';a.document(obs,o.template(attempt));out=r.report(attempt,obs,scratch/f'partial-reports-{index}','first')
 assert out['state']=='reported' and out['interrupted'] and len(out['numerical_comparison']['rows'])==276
 assert all(row['status']=='blocked' for row in out['numerical_comparison']['rows']);checks.append('partial terminal '+str(index)+' suppressed')
bad=scratch/'malformed.json';bad.write_text('{');native=a.execute(bad,scratch/'malformed-attempts','first');assert native['state']=='execution_refused' and not native['native_execution_started']
obs=scratch/'malformed-observations.json';a.document(obs,o.template(scratch/'malformed-attempts/first'));out=r.report(scratch/'malformed-attempts/first',obs,scratch/'malformed-reports','first');assert out['state']=='reported' and len(out['numerical_comparison']['rows'])==276;checks.append('pre-identity decode refusal reported')
extra=tools/'unexpected-review-probe.txt';extra.write_text('unexpected')
try:
 try:a.verify_identity()
 except ValueError:checks.append('unindexed tool file refused')
 else:raise AssertionError('unindexed file accepted')
finally:extra.unlink()
a.verify_identity()
protected=a.strict((prep/'evidence/preservation-before.json').read_bytes())['preserved_files'];drift=[k for k,v in protected.items() if a.sha(repo/k)!=v];assert not drift,drift
result={'archive_sha256':restoration['archive_sha256'],'identity_sha256':restoration['identity_sha256'],'native_outputs':1352,'predicates':67,'violated_predicates':6,'held_inputs':704,'report_rows':276,'focused_tests':9,'independent_negative_checks':checks,'author_evidence_artifacts_checked':len(author_receipt['evidence']),'author_native_values_identical':True,'preserved_file_count':len(protected),'protected_drift':drift,'reference_request_executed':False,'report_sha256':a.sha(scratch/'reports/baseline/report.json')}
(prep/'evidence/review/final-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
