"""Bounded documentation regeneration; retained implementation evidence is read-only."""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('wi052_generation', HERE.parent / 'implementation/regenerate.py')
generation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generation)
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot

production = ROOT / 'exploration/stellarator_e2e/generated'
before = generation.hashes(production)
old_manifest = json.loads((production / 'contracts/generation_manifest.json').read_text())
for filename in ('mfe_account_costs.sysml', 'mfe_lcoe_dcf.sysml', 'mfe_lifecycle.sysml'):
    canonical = ROOT / 'models/library/analyses' / filename
    twin = ROOT / 'exploration/stellarator_e2e/models/analyses' / filename
    assert canonical.read_bytes() == twin.read_bytes()
    # Compare SysML outside documentation against the entering commit.
    import re
    old = subprocess.check_output(['git', 'show', '59b1ff97:' + str(canonical.relative_to(ROOT))], cwd=ROOT, text=True)
    strip = lambda text: re.sub(r'doc /\*.*?\*/', '', text, flags=re.S)
    assert strip(old) == strip(canonical.read_text())

scratch = Path(tempfile.mkdtemp(prefix='wi052-doc-repair-'))
models = generation.materialize_canonical_subset(generation.MFE, scratch / 'models')
package = generation.seed_and_generate(scratch / 'generated', models_path=models)
snapshot = scratch / 'stellarator.snapshot.json'
capture_instance_graph_snapshot([models], snapshot)
other = generation.seed_and_generate(scratch / 'snapshot-generated', from_snapshot=snapshot)
after = generation.hashes(package)
assert generation.hashes(other) == after
assert before.keys() == after.keys()
changed = [name for name in before if before[name] != after[name]]
# Reject any executable Python change outside module documentation.
import ast
for name in changed:
    if name.endswith('.py'):
        def executable(path):
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                    node.body.pop(0)
            return ast.dump(tree)
        assert executable(production / name) == executable(package / name), name
assert all(before[name] == after[name] for name in generation.NAMES)
assert generation.hashes(production) == before
for name in changed:
    shutil.copyfile(package / name, production / name)
shutil.copyfile(snapshot, ROOT / 'exploration/stellarator_e2e/stellarator.snapshot.json')
result = {
    'entering_commit': '59b1ff97', 'scratch': str(scratch),
    'canonical_twin_equal': True, 'non_doc_sysml_equal': True,
    'source_snapshot_package_equal': True, 'all_python_executable_asts_equal': True,
    'eight_manual_seed_bytes_equal': True, 'changed_package_files': changed,
    'before_manifest': old_manifest,
    'after_manifest': json.loads((production / 'contracts/generation_manifest.json').read_text()),
    'before_inventory': before, 'after_inventory': after,
}
(HERE / 'regeneration.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS', json.dumps({k: v for k, v in result.items() if not k.endswith(('manifest', 'inventory'))}, indent=2))
