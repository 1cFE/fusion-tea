"""Verify retained history and final adapter bytes without interpreting observations."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
entry = json.loads((HERE / 'entering-custody.json').read_text())
changed = [r['path'] for r in entry['protected_files']
           if hashlib.sha256((ROOT / r['path']).read_bytes()).hexdigest() != r['sha256']]
assert not changed, changed
adapter = ROOT / '.project/active/model-evaluation-comparison-adapter/v1/identity.json'
identity = json.loads(adapter.read_text())
drift = [p for p, h in identity['files'].items()
         if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h]
assert not drift, drift
result = {'protected_inventory': 'entering-custody.json',
          'checked_files': len(entry['protected_files']), 'changed_files': changed,
          'adapter_identity_sha256': hashlib.sha256(adapter.read_bytes()).hexdigest(),
          'adapter_indexed_files': len(identity['files']), 'adapter_drift': drift,
          'branch': subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip(),
          'checked_checkpoint': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
          'scope': 'Byte preservation and adapter identity only; no reference observations interpreted.'}
(HERE / 'final-protected-custody.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS', result['checked_files'], 'protected files;', result['adapter_indexed_files'], 'adapter indexed files')
