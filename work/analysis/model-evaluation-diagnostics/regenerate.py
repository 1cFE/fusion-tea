"""Fresh native regeneration of two diagnostic-only normative completions."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
PACKAGE = ROOT / 'exploration/stellarator_e2e/generated'
PRIOR = ROOT / 'work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration/candidate-seeds.json'
CHANGED = {'handwritten/mfe_primary_loop/primary_coolant_loop_impl.py', 'handwritten/mfe_conductor_current/rebco_conductor_current_impl.py'}
spec = importlib.util.spec_from_file_location('native_seed_recipe', ROOT / 'work/completed/20260914_WI-040_winding-pack-mass-cost/evidence/regenerate.py')
recipe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recipe)
recipe.SEEDS = HERE / 'candidate-seeds.json'
old = json.loads(PRIOR.read_text())
current = recipe.inventory(PACKAGE)
assert all(current[n] == h for n,h in old.items() if n not in CHANGED)
seeds = {n: current[n] for n in old}
recipe.SEEDS.write_text(json.dumps(seeds, indent=2)+'\n')
(HERE/'seed-delta.json').write_text(json.dumps({n: {'before':old[n], 'after':current[n]} for n in sorted(CHANGED)},indent=2)+'\n')
with tempfile.TemporaryDirectory(prefix='domain-diagnostics-regen-') as tmp:
    fresh = recipe.seed_and_generate(Path(tmp)/'fresh', PACKAGE, models_path=ROOT/'exploration/stellarator_e2e/models')
    expected = recipe.inventory(fresh)
    assert not set(current)-set(expected)
    for n,h in expected.items():
        if current.get(n) != h:
            dst=PACKAGE/n; dst.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(fresh/n,dst)
    assert recipe.inventory(PACKAGE)==expected
    again=recipe.seed_and_generate(Path(tmp)/'again',PACKAGE,models_path=ROOT/'exploration/stellarator_e2e/models')
    assert recipe.inventory(again)==expected
(HERE/'package-hashes.json').write_text(json.dumps(expected,indent=2)+'\n')
(HERE/'generation-changes.json').write_text(json.dumps({n:{'before':current.get(n),'after':h} for n,h in expected.items() if current.get(n)!=h},indent=2)+'\n')
print('PASS: two fresh native generations identical;',len(seeds),'normative manual bodies')
