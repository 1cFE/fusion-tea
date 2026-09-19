"""Invoke the native integration seam for the audited WI-069 candidate."""
import json
import os
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
pkg = ROOT / 'exploration/stellarator_e2e/generated'
model = json.loads((pkg / 'contracts/model_contract.json').read_text())
exe = json.loads((pkg / 'contracts/package_contract.json').read_text())
revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
teax = subprocess.check_output(['git', '-C', os.environ['STOP_PARSER_TEAX_ROOT'], 'rev-parse', 'HEAD'], text=True).strip()
args = [sys.executable, str(ROOT / 'scripts/integrate.py'),
        '--audited-work', 'work/active/WI-069_fuel-inventory-and-startup@' + revision,
        '--models-root', 'exploration/stellarator_e2e/models',
        '--package', str(pkg), '--manifest', 'exploration/stellarator_e2e/studies/manifest.json',
        '--groups', 'tests/study/data/axes.known_answers.json',
        '--census-file', 'tests/models/data/mfe_census.json',
        '--expected-semantic-fingerprint', model['semantic_fingerprint'],
        '--expected-executable-fingerprint', exe['executable_fingerprint'],
        '--expected-teax-revision', teax,
        '--route-sys-path', 'exploration/stellarator_e2e/studies',
        '--route-module', 'study_route', '--route-callable', 'execute_baseline',
        '--out-dir', str(HERE / 'integration')]
(HERE / 'integration-command.json').write_text(json.dumps(args, indent=2) + '\n')
raise SystemExit(subprocess.run(args, cwd=ROOT).returncode)
