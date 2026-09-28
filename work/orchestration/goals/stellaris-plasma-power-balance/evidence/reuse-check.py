"""Content-only custody checks; no source substitution or model evaluation."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from scripts.study import identity
H=ROOT/'exploration/stellarator_e2e/studies/20260916-stellaris-reference-reconciliation'
D=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((H/'snapshot.json').read_text()); artifacts=[]
for k in ('preparation_artifacts','review_artifacts','execution_artifacts','definition_artifacts'): artifacts+=s[k]
for arm in s['arms']: artifacts+=arm['artifacts']
errors=[]
for a in artifacts:
 p=H/a['path']
 if not p.is_file() or sha(p)!=a['sha256']:errors.append(a['path'])
pkg=ROOT/'exploration/stellarator_e2e/generated'
current=identity.build_sealed(package_name='stellarator_tea',package_root=pkg)
prior=json.loads((H/'results/package_identity.json').read_text())
if current['identity']['digest']!=prior['identity']['digest']:errors.append('executable identity')
for a in s['fingerprints']['indicator_inputs']['files']:
 if sha(pkg/a['path'])!=a['sha256']:errors.append('indicator:'+a['path'])
paths=['models','exploration/stellarator_e2e/models','exploration/stellarator_e2e/generated','exploration/stellarator_e2e/verify_stellaris.py','exploration/stellarator_e2e/studies/oracle_entry.py','exploration/stellarator_e2e/studies/manifest.json']
changed=subprocess.check_output(['git','diff','--name-only','22e563392520142246c6883af7674473f973ae4b','--',*paths],cwd=ROOT,text=True).splitlines()
errors+=changed
freeze=ROOT/'.project/active/aries-comparison-preparation/package/freeze/r1/comparison-freeze.tar.gz'
fsha=sha(freeze)
if fsha!='fdf6e14572f10c9254df1e297394f9eccb0060e3947283ea0f8cf569fc63f533':errors.append('historical freeze')
out={'outcome':'fail' if errors else 'pass','snapshot_sha256':sha(H/'snapshot.json'),'artifacts_checked':len(artifacts),'indicator_files_checked':len(s['fingerprints']['indicator_inputs']['files']),'current_package_identity':current,'unchanged_production_scopes':paths,'changed_production_paths':changed,'historical_freeze_sha256':fsha,'errors':errors,'limitation':'Custody and identity reuse, not a new native evaluation or independent physics validation.'}
(D/'reuse-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='current_package_identity'},indent=2))
assert not errors
