import hashlib,json,subprocess,sys
from pathlib import Path
root=Path.cwd(); out=root/'.project/active/mfe-major-radius-study-package/audit-evidence'; impl=out.parent/'implementation'
quarantine=(root/'knowledge/holdout').resolve()
def digest(p):
    p=Path(p)
    assert not p.resolve().is_relative_to(quarantine), str(p)
    return hashlib.sha256(p.read_bytes()).hexdigest()
baseline=json.loads((impl/'protected-before.json').read_text())
permitted={p:v for p,v in baseline.items() if not p.startswith('knowledge/holdout/')}
actual={p:digest(root/p) for p in permitted}
delta={p:[v,actual[p]] for p,v in permitted.items() if v!=actual[p]}
wi=root/'work/active/WI-051_mfe-model-owned-major-radius/implementation/final-identities.json'
assert wi.read_bytes()==subprocess.check_output(['git','show','641c1051:'+str(wi.relative_to(root))])
expected=json.loads(wi.read_text())['package_files']; package=root/'exploration/stellarator_e2e/generated'
package_actual={str(p.relative_to(package)):digest(p) for p in package.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
assert package_actual==expected and len(expected)==246
frozen={}
for p,info in json.loads((impl/'frozen-integrity.json').read_text()).items():
    value=digest(root/p)
    assert value==info['sha256']
    assert (root/p).read_bytes()==subprocess.check_output(['git','show','f07015bb:'+p])
    frozen[p]=value
# Freeze current permitted bytes for the audit's after comparison.
audit_start={p:digest(root/p) for p in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if p and not p.startswith('knowledge/holdout/') and not p.startswith('.project/active/mfe-major-radius-study-package/audit-evidence/')}
(out/'audit-start-hashes.json').write_text(json.dumps(audit_start,indent=2)+'\n')
(out/'preservation.json').write_text(json.dumps({'quarantine_entries_metadata_only':len(baseline)-len(permitted),'permitted_count':len(actual),'implementation_baseline_delta':delta,'audited_package_files':len(expected),'package_exact':True,'frozen_controls':frozen},indent=2)+'\n')
print(json.dumps({'permitted_count':len(actual),'baseline_delta':delta,'package_files_exact':len(expected),'frozen_files_exact':len(frozen)}))
