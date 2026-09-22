"""Generate and seal the isolated source-budget partial accounting package."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'work/active/WI-088_aries-source-budget-cost-contribution/evidence'
SOURCES = [ROOT / 'models/library/analyses/source_budget_accounting.sysml', ROOT / 'models/library/analyses/mfe_account_costs.sysml', ROOT / 'models/designs/aries_cs_transfer/source_budget.sysml']
staging = HERE / 'input_models'
staging.mkdir(exist_ok=True)
for source in SOURCES:
    shutil.copy2(source, staging / source.name)
command = [str(ROOT / '.codex-test/run'), 'sysml-codegen', 'generate', '--models', str(staging), '--output', str(HERE / 'budget_tea'), '--package-name', 'budget_tea', '--overwrite']
with (EVIDENCE / 'generation.log').open('w') as log:
    subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT)
target = HERE / 'budget_tea/handwritten/source_budget_accounting'
for source in (HERE / 'native_completions').glob('*.py'):
    shutil.copy2(source, target / source.name)
relative = Path('handwritten/mfe_account_costs/n_1cfe_form_lcoe_impl.py')
original = ROOT / 'exploration/stellarator_e2e/generated' / relative
reused_formula = HERE / 'budget_tea' / relative
reused_formula.write_text(original.read_text().replace('from stellarator_tea.', 'from budget_tea.'))
with (EVIDENCE / 'completion-generation.log').open('w') as log:
    subprocess.run(command + ['--preserve-handwritten'], check=True, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
receipt = {'source_hashes': {str(p.relative_to(ROOT)): sha(p) for p in SOURCES}, 'staged_hashes': {str(p.relative_to(ROOT)): sha(staging / p.name) for p in SOURCES}, 'completion_hashes': {p.name: sha(p) for p in (HERE / 'native_completions').glob('*.py')}, 'reused_formula_original': sha(original), 'reused_formula_copied': sha(reused_formula), 'reused_formula_prefix_only': reused_formula.read_text().replace('from budget_tea.', 'from stellarator_tea.') == original.read_text()}
assert receipt['source_hashes'] == receipt['staged_hashes']
assert receipt['reused_formula_prefix_only']
for name, digest in receipt['completion_hashes'].items():
    assert sha(target / name) == digest
(EVIDENCE / 'build-hashes.json').write_text(json.dumps(receipt, indent=2) + '\n')
