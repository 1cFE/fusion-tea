"""Native fixed-point integration using a separately reviewed candidate identity."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--audited-revision', required=True)
parser.add_argument('--semantic', required=True)
parser.add_argument('--executable', required=True)
parser.add_argument('--out-dir', required=True)
args = parser.parse_args()
root = Path('exploration/stellarator_e2e')
assert json.loads((root/'generated/contracts/model_contract.json').read_text())['semantic_fingerprint'] == args.semantic
assert json.loads((root/'generated/contracts/package_contract.json').read_text())['executable_fingerprint'] == args.executable
command = [sys.executable, 'scripts/integrate.py',
    '--audited-work', f'work/active/WI-062_absolute-conductor-current-margin@{args.audited_revision}',
    '--models-root', str(root/'models'), '--package', str(root/'pkg/stellarator_tea'),
    '--manifest', str(root/'studies/manifest.json'), '--groups', 'tests/study/data/axes.known_answers.json',
    '--census-file', 'tests/models/data/mfe_census.json',
    '--expected-semantic-fingerprint', args.semantic,
    '--expected-executable-fingerprint', args.executable,
    '--expected-teax-revision', '8d877460ac4f6f264561d916e40c1708adb13397',
    '--route-sys-path', str(root/'studies'), '--route-module', 'study_route',
    '--route-callable', 'execute_baseline', '--out-dir', args.out_dir]
raise SystemExit(subprocess.call(command))
