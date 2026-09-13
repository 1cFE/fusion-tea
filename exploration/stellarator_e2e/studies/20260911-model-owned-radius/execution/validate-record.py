"""Record-only integrity checks; no model/runtime execution or source lookups."""
import json,hashlib,os,re
from pathlib import Path
H=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
snap=read(H/'snapshot.json');text=(H/'record.md').read_text()
expected=[x for x in (H/'context/record-template.md').read_text().splitlines() if x.startswith('## ') and x[3:4].isdigit()]
actual=[x for x in text.splitlines() if x.startswith('## ') and x[3:4].isdigit()]
assert actual==expected and len(actual)==17 and '<' not in text
assert sha(H/'snapshot.json') in text
names=snap['manifest']['content_used']['fingerprint_names'];assert set(names)<=set(snap['fingerprints'])
assert snap['indicators']['axis_declaration']['subset'] is False
assert len(snap['stores'])==len(snap['arms'])==1
store=snap['stores'][0];assert snap['arms'][0]['store_id']==store['store_id'];assert sha(H/store['path'])==store['sha256']
assert read(H/'results/store-compatibility.json')==store['compatibility_tuple']
assert store['compatibility_tuple']['evidence_schema_version']=='v3'
paths={};count=0
for field in ['result_artifacts','context_artifacts','preparation_artifacts','execution_artifacts','review_artifacts','diagnostic_artifacts','support_artifacts']:
 for entry in snap[field]:
  p=H/entry['path'];assert p.resolve().is_relative_to(H.resolve()) and not p.is_symlink()
  assert sha(p)==entry['sha256'],entry['path'];paths[entry['path']]=entry['sha256'];count+=1
result_paths=[]
for root,dirs,files in os.walk(H/'results',followlinks=False):
 dirs[:]=[d for d in dirs if d not in ['runtime-links','pkg_link','__pycache__'] and not (Path(root)/d).is_symlink()]
 for name in files:
  p=Path(root)/name
  if p.is_symlink() or name.endswith(('.db-shm','.db-wal','.pyc')):continue
  result_paths.append(str(p.relative_to(H)))
assert set(result_paths)=={a['path'] for a in snap['result_artifacts']}
for row in read(H/'context/provenance.json'):
 assert sha(H/row['path'])==row['sha256']
 assert row['source_path'] and 'knowledge/holdout' not in row['source_path']
 # Installed/untracked copies may have explicit nil revisions; byte digests remain authoritative.
 if row['source_commit']:assert row['source_commit_bytes_match'] is True,row['path']
assert len(read(H/'results/cases.json'))==7
assert not (H/'synthesis.md').exists()
assert len(snap['findings_registration']['ids'])==6
print(f'PASS: 17 headings; fingerprints/one-store identity resolved; {count} artifact digest entries verified; all {len(result_paths)} numerical/result artifacts inventoried; copied provenance consistent; six findings; no synthesis.')
