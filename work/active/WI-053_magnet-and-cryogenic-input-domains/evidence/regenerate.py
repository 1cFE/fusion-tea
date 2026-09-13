"""WI-053 explicit package-only preservation and native regeneration."""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PACKAGE = ROOT / 'exploration/stellarator_e2e/generated'
SEEDS = ('mfe_account_costs/financial_factors.py', 'mfe_account_costs/idc_closed_form_cost_impl.py', 'mfe_account_costs/levelized_annual_cost_impl.py', 'mfe_lcoe_dcf/lcoe_dcf_impl.py', 'mfe_lifecycle/lifecycle_calendar_impl.py', 'mfe_plasma_scaling/dt_fusion_power_impl.py', 'mfe_plasma_sustainment/plasma_sustainment_impl.py', 'mfe_power_cycle/power_cycle_efficiency_impl.py')
NEW = ('mfe_plasma_scaling/conductor_peak_field_impl.py', 'mfe_cryo_plant/cryoplant_electrical_power_impl.py')

def inventory(package):
    return {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(package.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}

def capture():
    found = {str(p.relative_to(PACKAGE / 'handwritten')) for p in (PACKAGE / 'handwritten').rglob('*.py') if p.name == 'financial_factors.py' or re.search(r'^AUTO_IMPLEMENTED = False$', p.read_text(), re.M)}
    assert found == set(SEEDS), found
    before = inventory(PACKAGE)
    (HERE / 'entering-package-hashes.json').write_text(json.dumps(before, indent=2)+'\n')
    (HERE / 'manual-seeds.json').write_text(json.dumps({n: before['handwritten/'+n] for n in SEEDS}, indent=2)+'\n')
    for name in SEEDS + NEW:
        target = HERE / 'original-bodies' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PACKAGE / 'handwritten' / name, target)

def generate():
    sys.path.insert(0, str(ROOT))
    from tests.model_families import MFE, materialize_canonical_subset
    from sysml_codegen.cli import GenerationConfig, run_codegen
    models = materialize_canonical_subset(MFE, HERE / 'candidate-models')
    expected = json.loads((HERE / 'manual-seeds.json').read_text())
    assert all(hashlib.sha256((PACKAGE/'handwritten'/n).read_bytes()).hexdigest() == digest for n,digest in expected.items())
    for smart in (False, True):
        before = inventory(PACKAGE)
        assert run_codegen(GenerationConfig(models_path=models, output_path=PACKAGE, package_name='stellarator_tea', overwrite=True, preserve_handwritten=True, smart_regen=smart))
        after = inventory(PACKAGE)
        assert all(after['handwritten/'+n] == digest for n,digest in expected.items())
        assert all(after['handwritten/'+n] == before['handwritten/'+n] for n in NEW)
        if smart: assert after == before, 'Second regeneration drift'
    (HERE / 'candidate-package-hashes.json').write_text(json.dumps(after, indent=2)+'\n')
    entering = json.loads((HERE / 'entering-package-hashes.json').read_text())
    (HERE / 'package-changes.json').write_text(json.dumps({n: {'before':entering.get(n),'after':after.get(n)} for n in sorted(set(entering)|set(after)) if entering.get(n)!=after.get(n)}, indent=2)+'\n')
    print('PASS eight entering seeds and two new manual bodies preserved; repeated generation byte-stable')

def seed_and_generate(path, source=PACKAGE, *, generator=None, **kwargs):
    """Complete a fresh current package using ten explicit normative seeds."""
    from sysml_codegen.cli import GenerationConfig, run_codegen
    path, source = Path(path), Path(source)
    if path.is_symlink() or path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise FileExistsError(f'Nonfresh destination: {path}')
    names = {'handwritten/'+name for name in SEEDS+NEW}
    found = {str(p.relative_to(source)) for p in (source/'handwritten').rglob('*.py') if p.name == 'financial_factors.py' or re.search(r'^AUTO_IMPLEMENTED = False$', p.read_text(), re.M)}
    if found != names:
        raise ValueError('Unexpected normative seed inventory')
    expected = json.loads((HERE/'candidate-package-hashes.json').read_text())
    path.mkdir(exist_ok=True)
    for name in sorted(names):
        original = source/name
        if original.is_symlink() or hashlib.sha256(original.read_bytes()).hexdigest() != expected[name]:
            raise ValueError('Missing, symlink or mismatched seed: '+name)
        target = path/name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original,target)
    assert (generator or run_codegen)(GenerationConfig(output_path=path,package_name='stellarator_tea',overwrite=True,preserve_handwritten=True,**kwargs))
    actual=inventory(path)
    assert all(actual[name] == expected[name] for name in names)
    return path

if __name__ == '__main__':
    {'capture':capture, 'generate':generate}[sys.argv[1]]()
