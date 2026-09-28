"""Compare the entering native baseline, current native baseline and independent oracle."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'exploration/stellarator_e2e/studies'))
import oracle_entry
from tests.models.current_mfe_regressions import WI040_CHANGED_ECONOMICS, WI040_CHANNELS

before = json.loads((HERE.parent / 'baseline-before.json').read_text())
after = json.loads((HERE.parent / 'baseline-after.json').read_text())
a, b = before['channels'], after['channels']
changed = {k for k in a if b.get(k) != a[k]}
allowed = {oracle_entry.ORACLE_OUTPUT_TO_CHANNEL[k] for k in WI040_CHANGED_ECONOMICS}
assert changed == allowed, (changed - allowed, allowed - changed)
assert set(b) - set(a) == WI040_CHANNELS
assert set(a) <= set(b)
assert before['verdicts'] == after['verdicts']
oracle = oracle_entry.evaluate(after['point'])
assert oracle.keys() <= b.keys()
assert all(math.isclose(value, b[k], rel_tol=1e-9, abs_tol=1e-9) for k, value in oracle.items())
report = {'before_fingerprint': before['executable_fingerprint'],
          'after_fingerprint': after['executable_fingerprint'],
          'unchanged_existing_channels_exact': len(a) - len(changed),
          'changed_existing_channels': {k: {'before': a[k], 'after': b[k], 'oracle': oracle[k]} for k in sorted(changed)},
          'new_channels': {k: b[k] for k in sorted(WI040_CHANNELS)},
          'oracle_channels_checked': len(oracle), 'oracle_relative_tolerance': 1e-9,
          'all_verdicts_unchanged': True, 'verdicts': after['verdicts']}
(HERE / 'baseline-reconciliation.json').write_text(json.dumps(report, indent=2) + '\n')
print(f'PASS {len(a)-len(changed)} exact unchanged channels; {len(changed)} explained economic changes; {len(oracle)} oracle matches; {len(after["verdicts"])} unchanged verdicts')
