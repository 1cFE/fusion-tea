"""Invoke the native integration seam for the recorded WI-091 package checkpoint."""
import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[5]
parser = argparse.ArgumentParser()
parser.add_argument('--out-dir', type=Path, required=True)
parser.add_argument('--audited-work', required=True, help='Accepted native item path@commit')
args = parser.parse_args()
base = Path('exploration/aries_integrated')
command = [str(ROOT / '.codex-test/run'), 'python', 'scripts/integrate.py',
    '--audited-work', args.audited_work,
    '--models-root', str(base / 'input_models'), '--package', str(base / 'aries_integrated'),
    '--manifest', str(base / 'studies/manifest.json'), '--groups', str(base / 'studies/axes.json'),
    '--census-file', str(base / 'census.json'),
    '--expected-semantic-fingerprint', '419e6e3d7ba46320a1f88b5f478d36abb5ead85d2ecb6fcdb7aff5fcb2c1e131',
    '--expected-executable-fingerprint', 'd13f4153accc48a3d6533a2d29a8e8b6b7cecd86644c322bb64f59fa402e419b',
    '--expected-teax-revision', '8d877460ac4f6f264561d916e40c1708adb13397',
    '--route-sys-path', str(base / 'studies'), '--route-module', 'study_route',
    '--route-callable', 'execute_baseline', '--out-dir', str(args.out_dir)]
raise SystemExit(subprocess.run(command, cwd=ROOT).returncode)
