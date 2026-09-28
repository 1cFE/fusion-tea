"""Read-only final artifact and registration checks; prints a stable outcome."""
import json,hashlib,re,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parents[1]
snap=json.loads((H/'snapshot.json').read_text());record=(H/'record.md').read_text()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
count=0
for key in ['result_artifacts','context_artifacts','execution_artifacts','preparation_artifacts','record_support_artifacts']:
 for a in snap[key]:
  assert sha(H/a['path'])==a['sha256'],a['path'];count+=1
assert snap['fingerprints']['indicator_inputs']['digest']
for name in snap['manifest']['content_used']['fingerprint_names']:assert name in snap['fingerprints']
for store in snap['stores']:assert sha(H/store['path'])==store['sha256']
assert sha(H/'snapshot.json') in record
assert len(re.findall(r'^## \d+\.',record,re.M))==17 and '<' not in record
assert all(not any('/'+d+'/' in a['path'] for d in ['_work','_study','_runtime']) for a in snap['result_artifacts'])
spec=importlib.util.spec_from_file_location('native_record_checks','tests/study/test_records.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
t.test_record_is_closed(H);t.test_arms_share_one_store_when_fingerprints_agree(H);t.test_findings_join_the_discovery_log(H)
assert len(snap['findings_registration']['ids'])==6
print('PASS: final published artifact digests, store hash, snapshot hash, native closure/one-store/findings join, six IDs, complete fingerprints, seventeen sections, local runtime separation')
