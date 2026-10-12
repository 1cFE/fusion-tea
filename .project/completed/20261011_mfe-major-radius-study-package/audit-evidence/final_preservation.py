import hashlib,json,subprocess
from pathlib import Path
root=Path.cwd(); item=root/'.project/active/mfe-major-radius-study-package'; out=item/'audit-evidence'
start=json.loads((out/'audit-start-hashes.json').read_text())
def digest(p):
    assert not p.resolve().is_relative_to((root/'knowledge/holdout').resolve())
    return hashlib.sha256(p.read_bytes()).hexdigest()
delta={p:[v,digest(root/p)] for p,v in start.items() if digest(root/p)!=v}
assert set(delta)=={'.project/active/mfe-major-radius-study-package/spec.md','.project/active/mfe-major-radius-study-package/plan.md'},delta
package=root/'exploration/stellarator_e2e/generated'; expected=json.loads((root/'work/active/WI-051_mfe-model-owned-major-radius/implementation/final-identities.json').read_text())['package_files']
actual={str(p.relative_to(package)):digest(p) for p in package.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
assert actual==expected and len(actual)==246
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(); assert head=='f5737119a65ef8dd9306589e499260c127e97bb7'
(out/'final-preservation.json').write_text(json.dumps({'tracked_file_delta':delta,'only_verified_item_checkboxes_changed':True,'package_files_exact':246,'CURRENT_WORK_unchanged_since_audit_entry':digest(root/'.project/CURRENT_WORK.md')==start['.project/CURRENT_WORK.md'],'head':head},indent=2)+'\n')
print('PASS: only item checkbox files changed; 246 package files exact; CURRENT_WORK and protected tracked bytes preserved')
