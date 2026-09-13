"""Capture entering controls, then apply the approved two logical changes."""
import difflib
import json
import shutil
import subprocess
import sys
from common import H, ROOT, ITEM, FROZEN, PRODUCTION, dump, hashes, sha
sys.path.insert(0, str(ROOT))
from tests.model_families import MFE, canonical_path, materialize_canonical_subset

CHANGED = ['designs/generic_mfe/mfe_plant.sysml', 'designs/stellarator_09/stellarator_plant.sysml']


def protected():
    # Enumerate tracked paths without reading quarantined contents. Capture all excluded
    # implementation/study/history/source surfaces; parent-owned state is not ours.
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    result = {}
    for name in names:
        if not name or name.startswith(('knowledge/holdout/', '.project/')):
            continue
        path = ROOT / name
        allowed = (name in [str(canonical_path(p).relative_to(ROOT)) for p in CHANGED]
                   or name in ['exploration/stellarator_e2e/models/' + p for p in CHANGED]
                   or name.startswith('exploration/stellarator_e2e/generated/')
                   or name in ['exploration/stellarator_e2e/' + p for p in ['run_stellaris.py', 'run_stellaris_single.py', 'stellarator.snapshot.json']]
                   or name in ['tests/models/data/mfe_census.json', 'tests/models/test_model_family_spines.py', 'data/traceability_matrix.csv', 'modeling_project/VALIDATION_MATRIX.md', str((ITEM/'plan.md').relative_to(ROOT))])
        if not allowed:
            if path.is_symlink(): result[name] = {'symlink': str(path.readlink())}
            elif path.is_file(): result[name] = {'sha256': sha(path)}
    return result


def capture():
    assert not (H/'entering.json').exists(), 'Entering capture is immutable'
    dump('protected-before.json', protected())
    (H/'entering-status.txt').write_bytes(subprocess.check_output(['git','status','--short'],cwd=ROOT))
    materialize_canonical_subset(MFE, H/'entering-models')
    shutil.copytree(PRODUCTION, H/'entering-package', ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    entering_paths = [ROOT/'exploration/stellarator_e2e'/n for n in ['run_stellaris.py','run_stellaris_single.py','stellarator.snapshot.json']]
    entering_paths += [ROOT/'tests/models/data/mfe_census.json']
    for path in entering_paths:
        dest=H/'entering-files'/path.relative_to(ROOT); dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(path,dest)
    frozen = {}
    for local, original in [('frozen-results.json','results.json'),('frozen-inventory.json','inventory.json'),('frozen-checks.json','checks.json'),('frozen-source-meaning.md','source-meaning.md')]:
        data=subprocess.check_output(['git','show','2f8856b7:work/analysis/20260911-230953_radius-ownership-evidence/'+original],cwd=ROOT)
        assert data==(FROZEN/local).read_bytes()
        frozen[local]=sha(FROZEN/local)
    assert sha(FROZEN/'expectations.json')==json.loads((FROZEN/'execution-start.json').read_text())['expectations_sha256']
    frozen['expectations.json']=sha(FROZEN/'expectations.json')
    frozen['direct-entering.json']=sha(FROZEN/'direct-entering.json')
    dump('entering.json', {'package':hashes(PRODUCTION),'family':hashes(H/'entering-models'),'frozen':frozen,'files':{str(p.relative_to(ROOT)):sha(p) for p in entering_paths}})
    print('Captured entering family, complete package, frozen git comparators and protected files')


def apply():
    entering=json.loads((H/'entering.json').read_text())
    assert hashes(PRODUCTION)==entering['package']
    patches=[]
    for logical in MFE.owned:
        canonical=canonical_path(logical); twin=MFE.twin/logical
        assert canonical.read_bytes()==twin.read_bytes()==(H/'entering-models'/logical).read_bytes()
        revised=ITEM/'design-revision/models'/logical
        if logical in CHANGED:
            patches.extend(difflib.unified_diff(canonical.read_text().splitlines(True),revised.read_text().splitlines(True),fromfile='a/'+logical,tofile='b/'+logical))
            canonical.write_bytes(revised.read_bytes()); twin.write_bytes(revised.read_bytes())
        else: assert canonical.read_bytes()==revised.read_bytes()
    (H/'applied.patch').write_text(''.join(patches))
    assert (H/'applied.patch').read_bytes()==(ITEM/'design-revision/proposed.patch').read_bytes()
    materialize_canonical_subset(MFE,H/'models')
    dump('source-hashes.json',hashes(H/'models'))
    assert protected()==json.loads((H/'protected-before.json').read_text())
    print('Applied exact revised patch to canonical and twins; other 21 logical files unchanged')

if __name__=='__main__':
    capture() if sys.argv[1:] == ['capture'] else apply()
