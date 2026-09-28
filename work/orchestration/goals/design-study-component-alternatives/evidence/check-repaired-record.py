"""Check the retained repaired record without model execution or mutation."""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
import sys
sys.path.insert(0, str(ROOT))
from tests.study.test_records import _csv_arms, _ids_in_log, _ids_in_record
RECORD = ROOT / 'exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
snapshot = read(RECORD / 'snapshot.json')
assert snapshot['released'] and snapshot['record_status'] == 'verified'
assert len(snapshot['arms']) == len(snapshot['stores']) == 1
assert snapshot['arms'][0]['store_id'] == snapshot['stores'][0]['store_id']
artifacts = snapshot['arms'][0]['artifacts']
assert all(sha(RECORD / a['path']) == a['sha256'] for a in artifacts)
text = (RECORD / 'record.md').read_text()
assert len(re.findall(r'^## \d+\.', text, re.M)) == 17
assert not re.search(r'<[A-Za-z][^>]*>', text)
assert sha(RECORD / 'snapshot.json') in text
ids = _ids_in_record(text, RECORD.name)
assert ids and ids == _ids_in_log((RECORD.parent / 'DISCOVERY_LOG.md').read_text(), RECORD.name)
with (RECORD / 'results/cases.csv').open() as stream:
    assert _csv_arms(list(csv.DictReader(stream)), snapshot['arms']) == {'arm-matched-offers'}
verification = read(RECORD / 'results/verification_summary.json')
cases = read(RECORD / 'results/cases.json')['cases']
assert verification['outcome'] == 'pass'
assert {c['candidate_id'] for c in cases} == set(verification['stores'][0]['sampling']['sampled_case_ids'])
assert len(cases) == 498 and len(verification['channels_checked']) == 872 and len(verification['constraints_rederived']) == 84
assert not verification['verdict_mismatches'] and not verification['not_independently_verified']
assert not read(RECORD / 'results/replay-comparison.json')['predicate_changes']
missing = []
for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
    if '://' not in target and not target.startswith('#') and not (RECORD / target.split('#')[0]).exists():
        missing.append(target)
assert not missing, missing
print(json.dumps({'outcome':'pass', 'snapshot_sha256':sha(RECORD / 'snapshot.json'), 'artifact_hashes_checked':len(artifacts), 'findings_joined':len(ids), 'cases':len(cases), 'channels':872, 'predicates':84, 'record_links_resolve':True}, indent=2))
