"""Materialize only the MFE family; generate from fresh bodies plus four manual files."""
import difflib, hashlib, json, shutil, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path.cwd(); H=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from tests.model_families import MFE, materialize_canonical_subset, canonical_path
from sysml_codegen.cli import GenerationConfig, run_codegen
def hashes(root):
    return {str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(root.rglob('*')) if f.is_file() and '__pycache__' not in str(f) and f.suffix!='.pyc'}
def dump(name,value): (H/name).write_text(json.dumps(value,indent=2)+'\n')
if __name__=='__main__':
    assert (H/'expectations.json').exists()
    source=ROOT/'exploration/stellarator_e2e/generated'
    dump('execution-start.json',{'utc':datetime.now(timezone.utc).isoformat(),'expectations_sha256':hashlib.sha256((H/'expectations.json').read_bytes()).hexdigest(),'package_before':hashes(source),'family_before':{p:hashlib.sha256(canonical_path(p).read_bytes()).hexdigest() for p in MFE.owned},'twins_equal':{p:canonical_path(p).read_bytes()==(MFE.twin/p).read_bytes() for p in MFE.owned}})
    models=materialize_canonical_subset(MFE,H/'models')
    materialize_canonical_subset(MFE,H/'entering-models')
    original={p:p.read_text() for p in models.rglob('*.sysml')}
    f=models/'designs/generic_mfe/mfe_plant.sysml'
    f.write_text(f.read_text().replace("part magnet : 'Magnet System' {", "part magnet : 'Magnet System' {\n            // Major plasma/axis radius [m], owned by the containing plant.\n            // Source: models/library/cost_structure/mfe_power_core.sysml; R0.\n            // Basis: T-021 source-meaning assessment at 2f8856b7; WI-051.\n            :>> R0 = R;"))
    f=models/'designs/stellarator_09/stellarator_plant.sysml'
    f.write_text(f.read_text().replace('            // Major radius [m]. Source: stellaris-design-details.md Table 2 /\n            //   line 251 (R ~= 12.7 m).\n            :>> R0 = 12.7;\n',''))
    (H/'proposed.patch').write_text(''.join(''.join(difflib.unified_diff(old.splitlines(True),p.read_text().splitlines(True),fromfile=str(p.relative_to(models)),tofile=str(p.relative_to(models)))) for p,old in original.items() if old!=p.read_text()))
    manual=json.loads((ROOT/'work/active/WI-050_mfe-coherent-operating-heating/implementation/normative-handwritten.json').read_text())
    pkg=H/'generated'
    for name,sha in manual.items():
        assert hashlib.sha256((source/name).read_bytes()).hexdigest()==sha
        dest=pkg/name; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(source/name,dest)
    assert run_codegen(GenerationConfig(models_path=models,output_path=pkg,package_name='stellarator_tea',overwrite=True,preserve_handwritten=True))
    after=hashes(pkg)
    assert all(after[n]==v for n,v in manual.items())
    dump('generated-hashes.json',after); dump('manual-preservation.json',manual)
    dump('source-hashes.json',hashes(models))
    print('Native generation complete; manual bodies preserved; all other bodies freshly generated.')
