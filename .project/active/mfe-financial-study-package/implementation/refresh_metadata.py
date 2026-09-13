"""Prepare current metadata in a fresh destination, without promoting a pin."""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'), str(ROOT), str(ROOT / 'exploration/stellarator_e2e/studies')]
import study_route as route
from scripts.study import manifest, indicators


def prepare(out):
    out.mkdir(parents=True, exist_ok=False)
    data = json.loads(route.MANIFEST_PATH.read_text())
    pin = manifest.indicator_input_fingerprint(route.PACKAGE_DIR)
    data['fingerprints'] = {
        'indicator_inputs': {**pin, 'files': [row['path'] for row in pin['files']]},
        'recorded_provenance': {
            'executable_fingerprint': manifest.read_executable_fingerprint(route.PACKAGE_DIR),
            'semantic_fingerprint': manifest.read_semantic_fingerprint(route.PACKAGE_DIR),
        },
    }
    candidate = out / 'manifest.json'
    candidate.write_text(json.dumps(manifest.validate(data), indent=1) + '\n')
    paths = route.execute_baseline(out / 'baseline', manifest_path=candidate)
    result = json.loads(paths['baseline_result'].read_text())
    data['baseline']['headline']['value'] = result['channels'][data['baseline']['headline']['channel']]
    verdicts = sorted([
        {'source_local_identity': v['source_local_identity'], 'expected': v['status']}
        for v in result['verdicts']
    ], key=lambda v: v['source_local_identity'])
    assert verdicts == data['baseline']['verdicts']
    candidate.write_text(json.dumps(manifest.validate(data), indent=1) + '\n')
    report = indicators.build_report(route.PACKAGE_DIR, manifest.load(candidate), indicators.read_axis_declaration(ROOT / 'tests/study/data/axes.known_answers.json'), [])
    (out / 'known-answers.json').write_text(json.dumps(report, indent=2) + '\n')
    for group in report['groups']:
        fixture = {'derived_against_semantic_fingerprint': manifest.read_semantic_fingerprint(route.PACKAGE_DIR), 'group': group}
        (out / f"{group['axis']}.expected.json").write_text(json.dumps(fixture, indent=1) + '\n')
    return data


if __name__ == '__main__':
    print(json.dumps(prepare(Path(sys.argv[1]))['fingerprints'], indent=2))
