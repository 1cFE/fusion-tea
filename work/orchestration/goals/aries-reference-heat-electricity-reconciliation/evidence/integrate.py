"""Replay the native integration seam against the WI-092 checkpoint (parallel exchanger network)."""
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
    '--audited-work', 'work/active/WI-092_aries-parallel-exchanger-network@6828df18',
    '--models-root', str(base / 'input_models'), '--package', str(package),
    '--manifest', str(base / 'studies/manifest.json'), '--groups', str(base / 'studies/axes.json'),
    '--census-file', str(base / 'census.json'),
    '--expected-semantic-fingerprint', '78dd23bf4c4a2d431ce8223d973db08e955e6f378175623ced8b976db4231f93',
    '--expected-executable-fingerprint', 'f739dbce67699b7adfae7c1adf5599ab7c30e85987caad53e0f8affd9b880ce4',
    '--expected-teax-revision', '8d877460ac4f6f264561d916e40c1708adb13397',
    '--route-sys-path', str(base / 'studies'), '--route-module', 'study_route',
    '--route-callable', 'execute_baseline', '--out-dir', str(args.out_dir)]
raise SystemExit(subprocess.run(command, cwd=ROOT).returncode)
