"""WI-040: fresh stock generation with a checked normative completion inventory."""
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PACKAGE = ROOT / 'exploration/stellarator_e2e/generated'
SEEDS = HERE / 'candidate-seeds.json'


def inventory(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path(path).rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}


def seed_and_generate(path, source=PACKAGE, *, generator=None, **kwargs):
    from sysml_codegen.cli import GenerationConfig, run_codegen
    path, source = Path(path), Path(source)
    if path.is_symlink() or path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise FileExistsError(f'Nonfresh destination: {path}')
    expected = json.loads(SEEDS.read_text())
    found = {str(p.relative_to(source)) for p in (source / 'handwritten').rglob('*.py')
             if p.name == 'financial_factors.py' or re.search(r'^AUTO_IMPLEMENTED = False$', p.read_text(), re.M)}
    if found != set(expected):
        raise ValueError(f'Unexpected normative seed inventory: {found ^ set(expected)}')
    path.mkdir(exist_ok=True)
    for name, digest in expected.items():
        original = source / name
        if original.is_symlink() or hashlib.sha256(original.read_bytes()).hexdigest() != digest:
            raise ValueError('Missing, symlink or mismatched seed: ' + name)
        target = path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original, target)
    assert (generator or run_codegen)(GenerationConfig(
        output_path=path, package_name='stellarator_tea', overwrite=True,
        preserve_handwritten=True, smart_regen=True, **kwargs))
    actual = inventory(path)
    assert all(actual[name] == digest for name, digest in expected.items())
    return path


def initialize_seeds():
    """Preserve thirteen entering bodies and add the two reviewed WI-040 bodies."""
    old = json.loads((ROOT / 'work/active/WI-056_primary-loop-heat-capacity-domain/evidence/corrected-candidate-seeds.json').read_text())
    assert len(old) == 13
    assert all(inventory(PACKAGE)[name] == digest for name, digest in old.items())
    added = {}
    for original in sorted((HERE.parent / 'seeds').glob('*_impl.py')):
        name = 'handwritten/mfe_winding_pack_cost/' + original.name
        target = PACKAGE / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original, target)
        added[name] = hashlib.sha256(original.read_bytes()).hexdigest()
    assert len(added) == 2, added
    expected = old | added
    if SEEDS.exists():
        assert json.loads(SEEDS.read_text()) == expected, 'Reviewed seed inventory drift'
    else:
        SEEDS.write_text(json.dumps(expected, indent=2) + '\n')


def generate():
    initialize_seeds()
    before = inventory(PACKAGE)
    with tempfile.TemporaryDirectory(prefix='wi040-fresh-') as tmp:
        fresh = seed_and_generate(Path(tmp) / 'fresh', models_path=ROOT / 'exploration/stellarator_e2e/models')
        expected = inventory(fresh)
        removed = set(before) - set(expected)
        # Exact obsolete paths from the rejected static-expression generation.
        obsolete = {f'{kind}/stellarator_09/stellaris/magnet/{name}'
                    for kind in ('modules', 'handwritten')
                    for name in ('__init__.py', 'winding_pack/__init__.py')}
        obsolete |= {f'{kind}/stellarator_09/stellaris/magnet/winding_pack/{name}{suffix}.py'
                     for kind, suffix in (('modules', ''), ('handwritten', '_impl'))
                     for name in ('price_solder', 'price_helium', 'cost_escalation')}
        assert removed <= obsolete, f'Unexpected obsolete package paths: {removed - obsolete}'
        for name in removed:
            archive = HERE / 'rejected-first-generation/obsolete' / name
            archive.parent.mkdir(parents=True, exist_ok=True)
            assert not archive.exists(), f'Already archived obsolete path: {archive}'
            shutil.move(PACKAGE / name, archive)
        for name in expected:
            target = PACKAGE / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if before.get(name) != expected[name]:
                shutil.copyfile(fresh / name, target)
        assert inventory(PACKAGE) == expected
        again = seed_and_generate(Path(tmp) / 'again', models_path=ROOT / 'exploration/stellarator_e2e/models')
        assert inventory(again) == expected, 'Fresh generation is not exact'
    changes = {name: {'before': before.get(name), 'after': digest}
               for name, digest in expected.items() if before.get(name) != digest}
    (HERE / 'package-hashes.json').write_text(json.dumps(expected, indent=2) + '\n')
    (HERE / 'generation-changes.json').write_text(json.dumps(changes, indent=2) + '\n')
    model_names = ('analyses/mfe_winding_pack_cost.sysml', 'analyses/mfe_magnet_field.sysml',
                   'cost_structure/mfe_power_core.sysml', 'structure/mfe_magnet_parts.sysml',
                   'designs/generic_mfe/mfe_plant.sysml', 'designs/stellarator_09/stellarator_plant.sysml')
    model_root = ROOT / 'exploration/stellarator_e2e/models'
    model_hashes = {name: hashlib.sha256((model_root / name).read_bytes()).hexdigest() for name in model_names}
    (HERE / 'model-hashes.json').write_text(json.dumps(model_hashes, indent=2) + '\n')
    print('PASS exact fresh package equality; thirteen preserved and two new normative seeds')


if __name__ == '__main__':
    generate()
