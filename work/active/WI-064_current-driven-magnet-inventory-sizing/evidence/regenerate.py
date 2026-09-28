"""WI-064 fresh generation from the explicit reviewed manual implementation set."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(ROOT))
PACKAGE = ROOT / 'exploration/stellarator_e2e/generated'
PRODUCTION = PACKAGE
SEEDS = HERE / 'candidate-seeds.json'
PRIOR = ROOT / 'work/completed/20260914_WI-040_winding-pack-mass-cost/evidence/regenerate.py'


def recipe():
    spec = importlib.util.spec_from_file_location('wi064_seed_protocol', PRIOR)
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
    """Verify twenty-five preserved bodies and one new sizing body before receipts."""
    import hashlib
    import re
    from tests.model_families import MFE, canonical_path
    prior = json.loads((ROOT / 'work/active/WI-063_magnet-manufacturing-account-completeness/evidence/candidate-seeds.json').read_text())
    added = 'handwritten/mfe_conductor_current/current_driven_pack_sizing_impl.py'
    assert len(prior) == 25
    found = {str(p.relative_to(PACKAGE)) for p in (PACKAGE / 'handwritten').rglob('*.py')
             if p.name == 'financial_factors.py' or re.search(r'^AUTO_IMPLEMENTED = False$', p.read_text(), re.M)}
    assert found == set(prior) | {added}, found ^ set(prior)
    current = inventory(PACKAGE)
    assert all(current[name] == digest for name, digest in prior.items()), 'Preserved body changed'
    (HERE / 'changed-seeds.json').write_text(json.dumps({added: {'before': None, 'after': current[added]}}, indent=2) + '\n')
    seeds = {name: current[name] for name in sorted(found)}
    if SEEDS.exists():
        assert json.loads(SEEDS.read_text()) == seeds, 'Reviewed seed inventory changed'
    else:
        SEEDS.write_text(json.dumps(seeds, indent=2) + '\n')
    models = {}
    for name in MFE.owned:
        original = canonical_path(name)
        assert original.read_bytes() == (MFE.twin / name).read_bytes(), name
        models[name] = hashlib.sha256(original.read_bytes()).hexdigest()
    (HERE / 'model-hashes.json').write_text(json.dumps(models, indent=2) + '\n')
    (HERE / 'package-hashes.json').write_text(json.dumps(current, indent=2) + '\n')
    return seeds


def generate():
    """Regenerate from reviewed seeds and prove exact repeatability before sealing."""
    import shutil
    import tempfile
    record_reviewed_inventory()
    before = inventory(PACKAGE)
    with tempfile.TemporaryDirectory(prefix='wi064-fresh-') as tmp:
        fresh = seed_and_generate(Path(tmp) / 'fresh', models_path=ROOT / 'exploration/stellarator_e2e/models')
        expected = inventory(fresh)
        assert not set(before) - set(expected), 'Unexpected obsolete package paths'
        for name, digest in expected.items():
            if before.get(name) != digest:
                target = PACKAGE / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(fresh / name, target)
        assert inventory(PACKAGE) == expected
        again = seed_and_generate(Path(tmp) / 'again', models_path=ROOT / 'exploration/stellarator_e2e/models')
        assert inventory(again) == expected, 'Fresh generation is not exact'
    record_reviewed_inventory()
    (HERE / 'generation-changes.json').write_text(json.dumps({
        name: {'before': before.get(name), 'after': digest}
        for name, digest in expected.items() if before.get(name) != digest
    }, indent=2) + '\n')
    print('PASS exact fresh package equality; twenty-five preserved and one new sizing manual body')


if __name__ == '__main__':
    generate()
