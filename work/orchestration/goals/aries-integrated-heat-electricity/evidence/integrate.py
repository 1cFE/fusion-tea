"""Replay the native integration seam against the accepted WI-089 checkpoint."""
import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[5]
parser = argparse.ArgumentParser()
parser.add_argument('--out-dir', type=Path, required=True)
args = parser.parse_args()
base = Path('exploration/aries_integrated')
package = base / 'aries_integrated'
command = [str(ROOT / '.codex-test/run'), 'python', 'scripts/integrate.py',
    '--audited-work', 'work/active/WI-089_aries-integrated-heat-and-electricity@143a556c',
    '--models-root', str(base / 'input_models'), '--package', str(package),
    '--manifest', str(base / 'studies/manifest.json'), '--groups', str(base / 'studies/axes.json'),
    '--census-file', str(base / 'census.json'),
    '--expected-semantic-fingerprint', '35c6023027b2a842b3a681ae44bb782485394c60a5dd18dde382bc3b3f269c97',
    '--expected-executable-fingerprint', 'cebe17fd3ca0dae4c5102365b384cc40635406b3c470c29dd7f55c086b9657bd',
    '--expected-teax-revision', '8d877460ac4f6f264561d916e40c1708adb13397',
    '--route-sys-path', str(base / 'studies'), '--route-module', 'study_route',
    '--route-callable', 'execute_baseline', '--out-dir', str(args.out_dir)]
raise SystemExit(subprocess.run(command, cwd=ROOT).returncode)
