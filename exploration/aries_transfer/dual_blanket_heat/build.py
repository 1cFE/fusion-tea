"""Generate and seal the isolated dual-blanket accounting package."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'work/active/WI-086_aries-dual-blanket-heat-accounting/evidence'
SOURCES = [ROOT / 'models/library/analyses/dual_circuit_heat_accounting.sysml', ROOT / 'models/library/analyses/mfe_viability.sysml', ROOT / 'models/designs/aries_cs_transfer/dual_blanket_heat.sysml']
staging = HERE / 'input_models'
staging.mkdir(exist_ok=True)
for source in SOURCES:
    shutil.copy2(source, staging / source.name)
command = [str(ROOT / '.codex-test/run'), 'sysml-codegen', 'generate', '--models', str(staging), '--output', str(HERE / 'heat_tea'), '--package-name', 'heat_tea', '--overwrite']
with (EVIDENCE / 'generation.log').open('w') as log:
    subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT)
target = HERE / 'heat_tea/handwritten/dual_circuit_heat_accounting'
for source in (HERE / 'native_completions').glob('*.py'):
    shutil.copy2(source, target / source.name)
relative = Path('handwritten/mfe_viability/offered_capacity_screen_impl.py')
original = ROOT / 'exploration/stellarator_e2e/generated' / relative
capacity = HERE / 'heat_tea' / relative
capacity.write_text(original.read_text().replace('from stellarator_tea.', 'from heat_tea.'))
with (EVIDENCE / 'completion-generation.log').open('w') as log:
    subprocess.run(command + ['--preserve-handwritten'], check=True, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
receipt = {'source_hashes': {str(p.relative_to(ROOT)): sha(p) for p in SOURCES}, 'staged_hashes': {str(p.relative_to(ROOT)): sha(staging / p.name) for p in SOURCES}, 'completion_hashes': {p.name: sha(p) for p in (HERE / 'native_completions').glob('*.py')}, 'capacity_original': sha(original), 'capacity_copied': sha(capacity), 'capacity_prefix_only': capacity.read_text().replace('from heat_tea.', 'from stellarator_tea.') == original.read_text()}
assert receipt['source_hashes'] == receipt['staged_hashes']
assert receipt['capacity_prefix_only']
for name, digest in receipt['completion_hashes'].items():
    assert sha(target / name) == digest
(EVIDENCE / 'build-hashes.json').write_text(json.dumps(receipt, indent=2) + '\n')
