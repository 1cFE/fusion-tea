"""Verify protected originals and frozen predecessor evidence without mutation."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
manifest = json.loads((Path(__file__).parent / 'entry-preservation.json').read_text())
changed = []
missing = []
for relative, expected in manifest['files'].items():
    path = ROOT / relative
    if not path.is_file():
        missing.append(relative)
    elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        changed.append(relative)
result = {'protected_files': len(manifest['files']), 'changed': changed,
          'missing': missing, 'passed': not changed and not missing}
args.output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
raise SystemExit(0 if result['passed'] else 1)
