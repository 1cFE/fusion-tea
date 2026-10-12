"""Reproduce current manifest and known answers from the unchanged native package.

Run from the repository root with the documented TEAx runtime; use a fresh work dir.
This prepares metadata identities. It does not invoke integration or promote a pin.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
STUDIES = ROOT / 'exploration/stellarator_e2e/studies'
sys.path[:0] = [str(ROOT), str(STUDIES)]
from scripts.study import manifest
from tests.study.conftest import DATA_DIR, run_tool
import study_route

parser = argparse.ArgumentParser()
parser.add_argument('work_dir', type=Path)
args = parser.parse_args()
path = STUDIES / 'manifest.json'
data = json.loads(path.read_text())
package = study_route.PACKAGE_DIR
pin = manifest.indicator_input_fingerprint(package)
data['fingerprints'] = {
    'indicator_inputs': {**pin, 'files': [f['path'] for f in pin['files']]},
    'recorded_provenance': {
        'executable_fingerprint': manifest.read_executable_fingerprint(package),
        'semantic_fingerprint': manifest.read_semantic_fingerprint(package),
    },
}
# These are published operating outputs and therefore required oracle comparisons.
for name, suffix in [('operating_heat_coupled', 'p_coupled'), ('operating_heat_delivered', 'p_delivered'), ('operating_heat_wallplug', 'p_wallplug')]:
    if not any(obj['name'] == name for obj in data['objective_catalog']):
        data['objective_catalog'].append({'name': name, 'channel': f'{study_route.P}operating_heat__{suffix}', 'note': 'WI-050 signed operating demand at held source/coupling efficiencies.'})
manifest.validate(data)
path.write_text(json.dumps(data, indent=1) + '\n')
result_paths = study_route.execute_baseline(args.work_dir)
result = json.loads(result_paths['baseline_result'].read_text())
data['baseline']['headline']['value'] = result['channels'][data['baseline']['headline']['channel']]
data['baseline']['verdicts'] = sorted([
    {'source_local_identity': v['source_local_identity'], 'expected': v['status']}
    for v in result['verdicts']
], key=lambda v: v['source_local_identity'])
manifest.validate(data)
path.write_text(json.dumps(data, indent=1) + '\n')
report = run_tool(package, path, DATA_DIR / 'axes.known_answers.json')
for group in report['groups']:
    fixture = {'derived_against_semantic_fingerprint': manifest.read_semantic_fingerprint(package), 'group': group}
    (DATA_DIR / f"{group['axis']}.expected.json").write_text(json.dumps(fixture, indent=1) + '\n')
(args.work_dir / 'known-answers.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'fingerprints': data['fingerprints'], 'baseline': data['baseline']}, indent=2))
