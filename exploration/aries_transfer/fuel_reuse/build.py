"""Generate isolated native fuel package; never mutates shared models/runtime."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'work/active/WI-082_aries-existing-component-transfer-proof/evidence'
SOURCES = [ROOT / 'models/library/analyses/mfe_fuel_cycle.sysml', ROOT / 'models/library/analyses/mfe_viability.sysml', ROOT / 'models/designs/aries_cs_transfer/fuel_reuse.sysml']
staging = HERE / 'input_models'
staging.mkdir(exist_ok=True)
for source in SOURCES:
    shutil.copy2(source, staging / source.name)
command = [str(ROOT / '.codex-test/run'), 'sysml-codegen', 'generate', '--models', str(staging), '--output', str(HERE / 'fuel_tea'), '--package-name', 'fuel_tea', '--overwrite']
with (EVIDENCE / 'generation.log').open('w') as log:
    subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT)
relative = Path('handwritten/mfe_viability/offered_capacity_screen_impl.py')
original = ROOT / 'exploration/stellarator_e2e/generated' / relative
target = HERE / 'fuel_tea' / relative
target.write_text(original.read_text().replace('from stellarator_tea.', 'from fuel_tea.'))
with (EVIDENCE / 'completion-generation.log').open('w') as log:
    subprocess.run(command + ['--preserve-handwritten'], check=True, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
receipt = {'source_hashes': {str(p.relative_to(ROOT)): sha(p) for p in SOURCES}, 'staged_hashes': {str(p.relative_to(ROOT)): sha(staging / p.name) for p in SOURCES}, 'capacity_completion_original': sha(original), 'capacity_completion_copied': sha(target), 'capacity_completion_prefix_only': target.read_text().replace('from fuel_tea.', 'from stellarator_tea.') == original.read_text()}
assert receipt['source_hashes'] == receipt['staged_hashes']
assert receipt['capacity_completion_prefix_only']
(EVIDENCE / 'reuse-hashes.json').write_text(json.dumps(receipt, indent=2) + '\n')
