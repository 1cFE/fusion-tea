"""Build only the isolated sector constituent inventory package."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'work/active/WI-084_aries-sector-constituent-inventory/evidence'
SOURCES = [ROOT / 'models/library/analyses/sector_constituent_inventory.sysml', ROOT / 'models/designs/aries_cs_transfer/constituent_inventory.sysml']
staging = HERE / 'input_models'
staging.mkdir(exist_ok=True)
for source in SOURCES:
    shutil.copy2(source, staging / source.name)
command = [str(ROOT / '.codex-test/run'), 'sysml-codegen', 'generate', '--models', str(staging), '--output', str(HERE / 'inventory_tea'), '--package-name', 'inventory_tea', '--overwrite']
with (EVIDENCE / 'generation.log').open('w') as log:
    subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT)
target = HERE / 'inventory_tea/handwritten/sector_constituent_inventory'
for source in (HERE / 'native_completions').glob('*.py'):
    shutil.copy2(source, target / source.name)
with (EVIDENCE / 'completion-generation.log').open('w') as log:
    subprocess.run(command + ['--preserve-handwritten'], check=True, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
receipt = {'source_hashes': {str(p.relative_to(ROOT)): sha(p) for p in SOURCES}, 'staged_hashes': {str(p.relative_to(ROOT)): sha(staging / p.name) for p in SOURCES}, 'completion_hashes': {p.name: sha(p) for p in (HERE / 'native_completions').glob('*.py')}}
assert receipt['source_hashes'] == receipt['staged_hashes']
for name, digest in receipt['completion_hashes'].items():
    assert sha(target / name) == digest
(EVIDENCE / 'build-hashes.json').write_text(json.dumps(receipt, indent=2) + '\n')
