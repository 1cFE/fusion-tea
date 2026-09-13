"""Independent read-only package identity, preservation and graph audit."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path.cwd()
out = root / '.project/active/mfe-operating-heating-study-package/audit-evidence'
implementation = out.parent / 'implementation'
sys.path[:0] = [str(root), str(root / 'exploration/stellarator_e2e/studies')]
from scripts.study import manifest
from tests.study.conftest import run_tool
import study_route

sha = lambda data: hashlib.sha256(data).hexdigest()
preserved = json.loads((implementation / 'preserved-hashes.json').read_text())
for name, expected in preserved.items():
    assert sha((root / name).read_bytes()) == expected, name
historical = json.loads((implementation / 'historical-failures.json').read_text())
for name, expected in historical['historical_sources_and_test_unchanged'].items():
    assert sha((root / name).read_bytes()) == expected, name
    assert sha(subprocess.check_output(['git', 'show', f'6cf3649e:{name}'])) == expected, name
fixed = json.loads((implementation / 'metadata-fixedpoint.json').read_text())['sha256']
for name, expected in fixed.items():
    assert sha((root / name).read_bytes()) == expected, name
current = json.loads(study_route.MANIFEST_PATH.read_text())
for name in ['controls.json', 'package_identity.json']:
    assert json.loads((out / name).read_text()) == json.loads((implementation / name).read_text()), name
controls = json.loads((out / 'controls.json').read_text())
assert current['baseline']['headline']['value'] == controls['baseline']['outputs'][current['baseline']['headline']['channel']]
assert current['baseline']['verdicts'] == sorted([
    {'source_local_identity': name, 'expected': status}
    for name, status in controls['baseline']['verdicts'].items()
], key=lambda row: row['source_local_identity'])
pkg = study_route.PACKAGE_DIR
pin = manifest.indicator_input_fingerprint(pkg)
assert current['fingerprints']['indicator_inputs'] == {**pin, 'files': [f['path'] for f in pin['files']]}
assert current['fingerprints']['recorded_provenance'] == {
    'semantic_fingerprint': manifest.read_semantic_fingerprint(pkg),
    'executable_fingerprint': manifest.read_executable_fingerprint(pkg),
}
report = run_tool(pkg, study_route.MANIFEST_PATH, root / 'tests/study/data/axes.known_answers.json')
for group in report['groups']:
    fixture = {'derived_against_semantic_fingerprint': manifest.read_semantic_fingerprint(pkg), 'group': group}
    name = root / f"tests/study/data/{group['axis']}.expected.json"
    assert name.read_bytes() == (json.dumps(fixture, indent=1) + '\n').encode(), name
axes = {'schema_version': 'study-axis-declaration/v1', 'groups': [
    {'axis': key, 'keys': [{'key': study_route.P + key, 'provenance': 'fan_out'}]}
    for key in ['p_wallplug_heat', 'eta_source_heat', 'eta_couple_heat']
]}
axes_path = out / 'heating-axes.json'
axes_path.write_text(json.dumps(axes, indent=2) + '\n')
heating = run_tool(pkg, study_route.MANIFEST_PATH, axes_path)
retained = json.loads((implementation / 'heating-reachability.json').read_text())
for group in heating['groups']:
    expected = next(g for g in retained['groups'] if g['axis'] == group['axis'])
    # Declarations may carry different prose; compare the graph's entire calculated group.
    assert group == expected, group['axis']
(out / 'heating-reachability.json').write_text(json.dumps(heating, indent=2) + '\n')
result = {'preserved_hashes': len(preserved), 'historical_source_identities': len(historical['historical_sources_and_test_unchanged']), 'metadata_hashes': len(fixed), 'fixtures_rederived_byte_exact': len(report['groups']), 'heating_groups_rederived_exact': len(heating['groups']), 'fingerprints': current['fingerprints']}
(out / 'checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
