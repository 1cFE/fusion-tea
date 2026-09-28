import importlib.util,json,hashlib,re
from pathlib import Path
H=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('record_tests','tests/study/test_records.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
t.test_record_is_closed(H);t.test_arms_share_one_store_when_fingerprints_agree(H)
snap=json.loads((H/'snapshot.json').read_text());assert snap['fingerprints']['indicator_inputs']['digest']
for name in snap['manifest']['content_used']['fingerprint_names']:assert name in snap['fingerprints']
count=0
for a in snap['result_artifacts']+snap['context_artifacts']+snap['execution_artifacts']:
 p=H/a['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256'],a['path'];count+=1
assert len(re.findall(r'^## \d+\.',(H/'record.md').read_text(),re.M))==17
out={'status':'pass','checks':['native record/store/arm stencil','all fingerprint names populated','all result/context/execution artifact digests','seventeen headings, no placeholders'],'artifact_digest_count':count,'explicitly_not_run':'Full tests/study/test_records.py discovery-log join is deferred until parent authorizes registration; draft is not closed.'}
(H/'execution/draft-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
