"""Retain actual native stored controls, oracle parity and all individual verdicts."""
import json
import sys
from pathlib import Path

root = Path.cwd()
sys.path[:0] = [str(root), str(root / 'exploration/stellarator_e2e/studies')]
import study_route as route
from scripts.study import verify

out = Path(sys.argv[1])
baseline = json.loads(route.MANIFEST_PATH.read_text())['baseline']['point']
controls = {'baseline': baseline, 'reserve': {**baseline, route.P+'p_wallplug_heat':120},
            'demand': {**baseline, route.P+'f_alpha_fast':.96}}
cases, db = route.run_points('operating-controls', list(controls.values()), out / '_work')
assert len(cases) == 3 and all(c.state == 'completed' for c in cases)
identity = route.write_identity_document(route.PACKAGE_DIR, out / 'package_identity.json')
summary = verify.build_summary(route.PACKAGE_DIR, route.MANIFEST_PATH, identity, [db], 3, None, [])
assert summary['worst_channel_rel_dev'] < 1e-9
(out / 'verification_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
results={name: {'inputs': c.inputs, 'outputs': c.outputs, 'verdicts': route.short_verdicts(c)}
         for name,point in controls.items() for c in cases if c.inputs == point}
assert set(results) == set(controls)
(out / 'controls.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'cases':len(cases),'verdicts':len(summary['constraints_rederived']),
                  'worst_channel_rel_dev': summary['worst_channel_rel_dev'],
                  'store':str(db)},indent=2))
