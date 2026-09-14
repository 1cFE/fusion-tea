"""WI-038 fresh generation: preserve fifteen reviewed bodies and add field capability."""
import hashlib
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PACKAGE = ROOT / 'exploration/stellarator_e2e/generated'
PRIOR = ROOT / 'work/completed/20260914_WI-040_winding-pack-mass-cost/evidence'
SEEDS = HERE / 'candidate-seeds.json'
NEW_SEED = 'handwritten/mfe_conductor_grade/conductor_field_capability_impl.py'


def prior_recipe():
    spec = importlib.util.spec_from_file_location('wi038_prior_seed_protocol', PRIOR / 'regenerate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.SEEDS = SEEDS
    return module


def inventory(path):
    return prior_recipe().inventory(path)


def seed_and_generate(path, source=PACKAGE, *, generator=None, **kwargs):
    # Reuse the checked exact-inventory protocol, not the prior item's frozen inventory.
    return prior_recipe().seed_and_generate(path, source, generator=generator, **kwargs)


def initialize_seeds():
    old = json.loads((PRIOR / 'candidate-seeds.json').read_text())
    assert len(old) == 15
    current = inventory(PACKAGE)
    assert all(current[name] == digest for name, digest in old.items())
    original = HERE.parent / 'seeds/conductor_field_capability_impl.py'
    target = PACKAGE / NEW_SEED
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(original, target)
    expected = old | {NEW_SEED: hashlib.sha256(original.read_bytes()).hexdigest()}
    if SEEDS.exists():
        assert json.loads(SEEDS.read_text()) == expected, 'Reviewed seed inventory drift'
    else:
        SEEDS.write_text(json.dumps(expected, indent=2) + '\n')


def generate():
    initialize_seeds()
    before = inventory(PACKAGE)
    with tempfile.TemporaryDirectory(prefix='wi038-fresh-') as tmp:
        fresh = seed_and_generate(Path(tmp) / 'fresh', models_path=ROOT / 'exploration/stellarator_e2e/models')
        expected = inventory(fresh)
        assert set(before) <= set(expected), 'Unexpected obsolete package paths'
        for name, digest in expected.items():
            target = PACKAGE / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if before.get(name) != digest:
                shutil.copyfile(fresh / name, target)
        assert inventory(PACKAGE) == expected
        again = seed_and_generate(Path(tmp) / 'again', models_path=ROOT / 'exploration/stellarator_e2e/models')
        assert inventory(again) == expected, 'Fresh generation is not exact'
    changes = {name: {'before': before.get(name), 'after': digest}
               for name, digest in expected.items() if before.get(name) != digest}
    (HERE / 'package-hashes.json').write_text(json.dumps(expected, indent=2) + '\n')
    (HERE / 'generation-changes.json').write_text(json.dumps(changes, indent=2) + '\n')
    write_model_hashes()
    print('PASS exact fresh package equality; fifteen preserved and one new normative seed')


def write_model_hashes():
    # Carry the prior changed-source guards forward as well as this increment.
    prior_hashes = json.loads((PRIOR / 'model-hashes.json').read_text())
    model_names = sorted(set(prior_hashes) | {'analyses/mfe_conductor_grade.sysml'})
    model_root = ROOT / 'exploration/stellarator_e2e/models'
    hashes = {name: hashlib.sha256((model_root / name).read_bytes()).hexdigest() for name in model_names}
    (HERE / 'model-hashes.json').write_text(json.dumps(hashes, indent=2) + '\n')


if __name__ == '__main__':
    generate()
