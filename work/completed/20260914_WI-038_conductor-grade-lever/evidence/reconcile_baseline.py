"""Execute the unchanged reference point, then check WI-038 neutrality and oracle parity."""
import json
import math
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / 'exploration/stellarator_e2e/studies'),
                str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit')]
import oracle_entry
import study_route as route

before = json.loads((HERE.parent / 'baseline-before.json').read_text())
with tempfile.TemporaryDirectory(prefix='wi038-baseline-') as tmp:
    cases, _ = route.run_points('wi038-native-reference', [before['point']], Path(tmp))
    assert len(cases) == 1 and cases[0].state == 'completed'
    case = cases[0]
    after = {'channels': {k: float(v) for k, v in sorted(case.outputs.items())},
             'executable_fingerprint': case.executable_fingerprint,
             'point': before['point'], 'verdicts': route.short_verdicts(case)}
(HERE.parent / 'baseline-after.json').write_text(json.dumps(after, indent=1) + '\n')
a, b = before['channels'], after['channels']
new = {route.P + 'magnet__conductor_grade__' + name for name in
       ('quantity_factor', 'j_wp_effective', 'cost_per_kAm_effective')}
changed = {k: {'before': v, 'after': b.get(k)} for k, v in a.items() if b.get(k) != v}
oracle = oracle_entry.evaluate(before['point'])
mismatches = {k: {'oracle': v, 'native': b.get(k)} for k, v in oracle.items()
              if k not in b or not math.isclose(v, b[k], rel_tol=1e-9, abs_tol=1e-9)}
report = {'before_fingerprint': before['executable_fingerprint'],
          'after_fingerprint': after['executable_fingerprint'],
          'unchanged_existing_channels_exact': len(a) - len(changed),
          'changed_existing_channels': changed, 'new_channels': {k: b.get(k) for k in sorted(new)},
          'oracle_channels_checked': len(oracle), 'oracle_mismatches': mismatches,
          'all_verdicts_unchanged': before['verdicts'] == after['verdicts'],
          'verdicts': after['verdicts']}
(HERE / 'baseline-reconciliation.json').write_text(json.dumps(report, indent=2) + '\n')
assert len(a) == 174 and not changed, changed
assert set(b) - set(a) == new and len(b) == 177
assert report['all_verdicts_unchanged'] and len(after['verdicts']) == 18
assert len(oracle) == 161 and not mismatches, mismatches
print('PASS 174 exact unchanged channels, three new channels, 161 oracle matches, eighteen unchanged verdicts')
