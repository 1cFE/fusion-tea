"""Complete the current MFE family using an explicit, hash-checked seed inventory."""
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
PRODUCTION=ROOT/'exploration/stellarator_e2e/generated'
sys.path.insert(0,str(ROOT))
from tests.model_families import MFE,materialize_canonical_subset
NAMES={'handwritten/mfe_account_costs/'+name for name in ('financial_factors.py','idc_closed_form_cost_impl.py','levelized_annual_cost_impl.py')}|{'handwritten/'+name for name in ('mfe_lcoe_dcf/lcoe_dcf_impl.py','mfe_lifecycle/lifecycle_calendar_impl.py','mfe_plasma_scaling/dt_fusion_power_impl.py','mfe_plasma_sustainment/plasma_sustainment_impl.py','mfe_power_cycle/power_cycle_efficiency_impl.py')}

def hashes(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}

def seed_inventory():return json.loads((HERE/'manual-seeds.json').read_text())

def fresh_directory(path):
    path=Path(path)
    if path.is_symlink() or path.exists() and (not path.is_dir() or any(path.iterdir())):raise FileExistsError(f'Nonfresh destination: {path}')
    path.mkdir(exist_ok=True)

def seed_and_generate(path,source=PRODUCTION,*,generator=None,**kwargs):
    from sysml_codegen.cli import GenerationConfig,run_codegen
    path,source=Path(path),Path(source)
    fresh_directory(path)
    expected=seed_inventory()
    if set(expected)!=NAMES:raise ValueError('Unexpected normative seed names')
    # Enumerate only handwritten Python; never walk source/research or study trees.
    if any((source/name).is_symlink() for name in NAMES):raise ValueError('Symlink normative seed')
    found={str(p.relative_to(source)) for p in (source/'handwritten').rglob('*.py') if p.name=='financial_factors.py' or re.search(r'^AUTO_IMPLEMENTED = False',p.read_text(),re.M)}
    if found!=NAMES:raise ValueError('Missing or extra normative source seed')
    for name,digest in expected.items():
        p=source/name
        if p.is_symlink() or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise ValueError('Missing, symlink or mismatched normative seed: '+name)
    for name in expected:
        target=path/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/name,target)
    if hashes(path)!=expected:raise ValueError('Extra or mismatched copied seed')
    assert (generator or run_codegen)(GenerationConfig(output_path=path,package_name='stellarator_tea',overwrite=True,preserve_handwritten=True,**kwargs))
    assert all(hashes(path).get(k)==v for k,v in expected.items())
    return path

def regenerate(destination=None):
    from sysml_codegen.cli import GenerationConfig,run_codegen
    from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot
    destination=Path(destination) if destination else Path(tempfile.mkdtemp(prefix='wi052-regeneration-'))
    models=materialize_canonical_subset(MFE,destination/'models')
    package=seed_and_generate(destination/'generated',models_path=models)
    before=hashes(package)
    records=[]
    for smart in (False,True):
        assert run_codegen(GenerationConfig(models_path=models,output_path=package,package_name='stellarator_tea',overwrite=True,preserve_handwritten=True,smart_regen=smart))
        assert hashes(package)==before
        records.append({'smart_regen':smart,'all_package_bytes_equal':True})
    snapshot=destination/'stellarator.snapshot.json'
    capture_instance_graph_snapshot([models],snapshot)
    other=seed_and_generate(destination/'snapshot-generated',from_snapshot=snapshot)
    assert hashes(other)==before
    (HERE/'regeneration.json').write_text(json.dumps({'destination':str(destination),'inventory':before,'repeats':records,'source_equals_snapshot':True},indent=2)+'\n')
    print('PASS normal/smart preservation and source/snapshot equality:',destination)
    return destination

if __name__=='__main__':regenerate(Path(sys.argv[1]) if sys.argv[1:] else None)
