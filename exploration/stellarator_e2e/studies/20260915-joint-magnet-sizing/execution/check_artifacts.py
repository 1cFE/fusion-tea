"""Check native store joins and every frozen artifact without evaluating a model."""
import hashlib
import json
import sqlite3
from pathlib import Path

H = Path(__file__).resolve().parents[1]
read = lambda path: json.loads(path.read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
native = {row['candidate_id']: row for row in read(H / 'results/native-cases.json')}
catalog = read(H / 'results/predicate-catalog.json')
report = {'outcome': 'pass', 'stores': [], 'snapshot_artifacts_checked': 0}
for db in sorted((H / 'results').rglob('*.db')):
    connection = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    stored = connection.execute('select candidate_id,state,inputs_json,evidence_digest from cases').fetchall()
    joined = 0
    for cid, state, inputs, digest in stored:
        assert state == 'completed'
        path = db.parent / 'artifacts' / (digest + '.json')
        assert path.is_file(), path
        assert sha(path) == digest
        evidence = read(path)
        verdicts = {key: value for key, value in evidence['responses'].items() if key in catalog}
        assert len(verdicts) == 20
        assert {row['constraint_id']: row['status'] for row in evidence['report']['results']} == verdicts
        if cid in native:
            row = native[cid]
            assert json.loads(inputs) == row['inputs']
            assert evidence['outputs'] == row['outputs']
            assert verdicts == row['verdicts']
            joined += 1
        assert evidence['report']['coverage']['coverage_state'] == 'complete'
    proposals = connection.execute('select raw_json,valid,candidate_id from proposals').fetchall()
    if joined:
        assert joined == len(native)
        assert len(proposals) == len(native)
        for raw, valid, cid in proposals:
            assert valid == 1
            assert json.loads(raw) == native[cid]['inputs']
    connection.close()
    report['stores'].append({'path': str(db.relative_to(H)), 'sha256': sha(db),
                             'cases': len(stored), 'export_joins': joined,
                             'content_addressed_evidence_checked': len(stored)})
snapshot = H / 'snapshot.json'
if snapshot.exists():
    snap = read(snapshot)
    report['snapshot_sha256'] = sha(snapshot)
    artifacts = []
    for name in ('preparation_artifacts', 'review_artifacts', 'execution_artifacts', 'definition_artifacts'):
        artifacts.extend(snap[name])
    for arm in snap['arms']:
        artifacts.extend(arm['artifacts'])
    for item in artifacts:
        path = H / item['path']
        assert path.is_file(), path
        assert sha(path) == item['sha256'], path
    report['snapshot_artifacts_checked'] = len(artifacts)
    for store in snap['stores']:
        assert (H / store['path']).is_file()
    assert set(snap['manifest']['content_used']['fingerprint_names']) <= set(snap['fingerprints'])
    for item in snap['fingerprints']['indicator_inputs']['files']:
        assert set(item) == {'path', 'sha256'}
    # Explicit list for the coordinator; only named frozen/evidence artifacts,
    # never runtime caches, package symlinks or transient SQLite sidecars.
    files = {H / item['path'] for item in artifacts}
    files.update([snapshot, H / 'record.md', H / 'synthesis.md', H / 'axes.json', H / 'indicators.json'])
    files.update(path for path in (H / 'reviews').iterdir() if path.is_file())
    files.update([H / 'reviews/artifact-check.json', H / 'reviews/required-files.txt'])
    root = H.parents[3]
    report['required_retained_files'] = len(files)
    (H / 'reviews/required-files.txt').write_text(''.join(str(path.relative_to(root)) + '\n' for path in sorted(files)))
destination = H / ('reviews/artifact-check.json' if snapshot.exists() else 'results/native-store-check.json')
destination.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report | {'required_retained_files': report.get('required_retained_files')}, indent=2))
