"""Diagnostic replay of retained inputs on the entering executable; not a new parameter study."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
if os.environ.get('STOP_PARSER_TEAX_ROOT'):
    sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study import identity

HERE = Path(__file__).resolve().parent
source = json.loads((HERE / 'starting-cases.json').read_text())
rows = source['cases']
cases, db = route.run_points('cooling-entering-replay', [row['inputs'] for row in rows], HERE / 'entering-replay')
by_inputs = {json.dumps(dict(case.inputs), sort_keys=True): case for case in cases}
result = {'purpose': __doc__, 'revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(), 'database': str(db.relative_to(ROOT)), 'cases': []}
for row in rows:
    case = by_inputs[json.dumps(row['inputs'], sort_keys=True)]
    old = row['native_channels']
    common = {key: {'historical': value, 'current': case.outputs.get(key)} for key, value in old.items()}
    result['cases'].append({'historical_proposal_id': row['proposal_id'], 'state': case.state, 'inputs': dict(case.inputs), 'outputs': dict(case.outputs), 'verdicts': route.short_verdicts(case), 'historical_common_channels': common})
(HERE / 'entering-replay.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
for row in result['cases']:
    print(row['historical_proposal_id'], row['state'], [key for key, value in row['verdicts'].items() if value != 'satisfied'])
