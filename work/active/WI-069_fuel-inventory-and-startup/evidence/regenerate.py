"""WI-069 stock fresh generation from hash-checked normative manual bodies."""
import hashlib
import importlib.util
import json
import re
import shutil
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PACKAGE = ROOT / 'exploration/stellarator_e2e/generated'
PRODUCTION = PACKAGE
SEEDS = HERE / 'candidate-seeds.json'
PRIOR = ROOT / 'work/completed/20260914_WI-040_winding-pack-mass-cost/evidence/regenerate.py'
ADDED = {'handwritten/mfe_fuel_cycle/fuel_inventory_impl.py'}



def recipe():
    spec = importlib.util.spec_from_file_location('wi069_seed_protocol', PRIOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.SEEDS = SEEDS
    return module


def inventory(path):
    return recipe().inventory(path)


hashes = inventory


def seed_and_generate(path, source=PACKAGE, *, generator=None, **kwargs):
    return recipe().seed_and_generate(path, source, generator=generator, **kwargs)


def record_reviewed_inventory():
    from tests.model_families import MFE, canonical_path
    prior = json.loads((ROOT / 'work/active/WI-068_layout-based-facilities/evidence/candidate-seeds.json').read_text())
    for name in ADDED:
        target = PACKAGE / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(HERE.parent / 'seeds' / target.name, target)
    current = inventory(PACKAGE)
    assert len(prior) == 34
    assert all(current[name] == digest for name, digest in prior.items()), 'Preserved manual body changed'
    found = {str(p.relative_to(PACKAGE)) for p in (PACKAGE / 'handwritten').rglob('*.py')
             if p.name == 'financial_factors.py' or re.search(r'^AUTO_IMPLEMENTED = False$', p.read_text(), re.M)}
    assert found == set(prior) | ADDED, found ^ (set(prior) | ADDED)
    seeds = {name: current[name] for name in sorted(found)}
    if SEEDS.exists():
        assert json.loads(SEEDS.read_text()) == seeds, 'Reviewed seed drift'
    else:
        SEEDS.write_text(json.dumps(seeds, indent=2) + '\n')
    models = {}
    for name in MFE.owned:
        original = canonical_path(name)
        assert original.read_bytes() == (MFE.twin / name).read_bytes(), name
        models[name] = hashlib.sha256(original.read_bytes()).hexdigest()
    (HERE / 'model-hashes.json').write_text(json.dumps(models, indent=2) + '\n')
    (HERE / 'changed-seeds.json').write_text(json.dumps({name: {'before': prior.get(name), 'after': current[name]} for name in ADDED}, indent=2) + '\n')


def generate():
    record_reviewed_inventory()
    before = inventory(PACKAGE)
    with tempfile.TemporaryDirectory(prefix='wi069-fresh-') as tmp:
        fresh = seed_and_generate(Path(tmp) / 'fresh', models_path=ROOT / 'exploration/stellarator_e2e/models')
        expected = inventory(fresh)
        assert not set(before) - set(expected), f'Unexpected obsolete package paths: {set(before) - set(expected)}'
        for name, digest in expected.items():
            if before.get(name) != digest:
                target = PACKAGE / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(fresh / name, target)
        assert inventory(PACKAGE) == expected
        again = seed_and_generate(Path(tmp) / 'again', models_path=ROOT / 'exploration/stellarator_e2e/models')
        assert inventory(again) == expected, 'Fresh generation is not exact'
    (HERE / 'package-hashes.json').write_text(json.dumps(expected, indent=2) + '\n')
    (HERE / 'generation-changes.json').write_text(json.dumps({name: {'before': before.get(name), 'after': digest} for name, digest in expected.items() if before.get(name) != digest}, indent=2) + '\n')
    print('PASS exact fresh package equality; 34 unchanged, one new normative fuel inventory seed')


if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(ROOT))
    generate()
