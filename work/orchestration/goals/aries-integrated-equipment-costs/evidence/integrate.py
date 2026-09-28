"""Invoke the native integration seam for the recorded WI-090 package checkpoint."""
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
    '--expected-semantic-fingerprint', '10ea8ab0c94ef4bd126465b2bf664a86bc3a38fa892b39591aa3057069f13a6f',
    '--expected-executable-fingerprint', '01f8f89c42a98621ff4c6868156d9b7938b7c80102f1c8321b35504ffcc7a021',
    '--expected-teax-revision', '8d877460ac4f6f264561d916e40c1708adb13397',
    '--route-sys-path', str(base / 'studies'), '--route-module', 'study_route',
    '--route-callable', 'execute_baseline', '--out-dir', str(args.out_dir)]
raise SystemExit(subprocess.run(command, cwd=ROOT).returncode)
