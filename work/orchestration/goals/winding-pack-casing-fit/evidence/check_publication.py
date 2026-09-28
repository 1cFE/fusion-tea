"""Check a frozen study's native artifact digests and Git retention, without mutation."""
import argparse,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('record',type=Path);a=p.parse_args()
root=Path.cwd().resolve();home=a.record.resolve();snapshot=json.loads((home/'snapshot.json').read_text())
entries=[]
for key in ('preparation_artifacts','review_artifacts','execution_artifacts','definition_artifacts'):
    entries.extend(snapshot.get(key,[]))
for arm in snapshot['arms']:
    entries.extend(arm['artifacts'])
tracked=set(subprocess.check_output(['git','ls-files','-z','--',str(home.relative_to(root))],text=True).split('\0'))
errors=[]
for entry in entries:
    target=(home/entry['path']).resolve()
    if not target.is_relative_to(home):
        errors.append(f"outside record: {entry['path']}");continue
    if not target.is_file():
        errors.append(f"missing: {entry['path']}");continue
    if hashlib.sha256(target.read_bytes()).hexdigest()!=entry['sha256']:
        errors.append(f"hash mismatch: {entry['path']}")
    if str(target.relative_to(root)) not in tracked:
        errors.append(f"not retained in Git: {entry['path']}")
for store in snapshot['stores']:
    if not any(e['path']==store['path'] for e in entries):
        errors.append(f"store not hashed: {store['path']}")
for name in ('record.md','snapshot.json','indicators.json'):
    if str((home/name).relative_to(root)) not in tracked:
        errors.append(f"record contract untracked: {name}")
result={'outcome':'pass' if not errors else 'fail','study':snapshot['study_id'],'artifact_entries':len(entries),'unique_artifact_paths':len({e['path'] for e in entries}),'stores':len(snapshot['stores']),'snapshot_sha256':hashlib.sha256((home/'snapshot.json').read_bytes()).hexdigest(),'errors':errors}
print(json.dumps(result,indent=2));raise SystemExit(bool(errors))
