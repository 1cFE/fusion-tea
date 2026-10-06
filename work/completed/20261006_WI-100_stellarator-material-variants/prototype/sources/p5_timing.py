"""Scratch probe P5: per-case wall time of one plant instance through the stock strict loader and StudyRunner."""
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path('/home/reid/1cfe/fusion-tea')
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))
sys.path.insert(0, str(ROOT / 'exploration/stellarator_e2e/studies'))
import study_route as route  # noqa: E402

pkg, name, work, prefix, n = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), sys.argv[4], int(sys.argv[5])
route.PACKAGE_NAME = name
contract = json.loads((pkg / 'contracts/model_contract.json').read_text())
route.BOOLEAN_KEYS = frozenset(p['qualified_name'] for p in contract['parameters'] if p['python_type'] == 'bool')
key = prefix + 'magnet__coil__turn_current'
proposals = [{key: 50000.0 * (1.0 + 0.001 * i)} for i in range(n)]
t0 = time.time()
prepared = route.prepare(pkg, work)
t1 = time.time()
cases, db = route.run_points('p5-timing', proposals, work, pkg, required_channels={'lcoe': prefix + 'lcoe_calc__lcoe'})
t2 = time.time()
states = [c.state for c in cases]
print(json.dumps(dict(package=name, prefix=prefix, cases=n, states=sorted(set(states)), prepare_s=t1 - t0,
                      run_s_including_prepare=t2 - t1, per_case_s=(t2 - t1) / n,
                      lcoe=[c.outputs.get(prefix + 'lcoe_calc__lcoe') for c in cases[:3]],
                      failures=[getattr(c, 'failure', None) for c in cases if c.state != 'completed'][:2]), indent=1, default=str))
