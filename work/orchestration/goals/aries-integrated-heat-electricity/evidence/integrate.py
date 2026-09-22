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
    '--audited-work', 'work/active/WI-089_aries-integrated-heat-and-electricity@71b2867a',
    '--models-root', str(base / 'input_models'), '--package', str(package),
    '--manifest', str(base / 'studies/manifest.json'), '--groups', str(base / 'studies/axes.json'),
    '--census-file', str(base / 'census.json'),
    '--expected-semantic-fingerprint', '35c6023027b2a842b3a681ae44bb782485394c60a5dd18dde382bc3b3f269c97',
    '--expected-executable-fingerprint', '469191fd32c624ccf70e0b4ebc1065b34920df8174c37a09e8f45ecfb241a7d7',
    '--expected-teax-revision', '8d877460ac4f6f264561d916e40c1708adb13397',
    '--route-sys-path', str(base / 'studies'), '--route-module', 'study_route',
    '--route-callable', 'execute_baseline', '--out-dir', str(args.out_dir)]
raise SystemExit(subprocess.run(command, cwd=ROOT).returncode)
