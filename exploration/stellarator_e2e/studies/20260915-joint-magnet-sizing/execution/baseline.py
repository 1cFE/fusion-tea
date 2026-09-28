"""Run the exact pinned baseline and all native preflight gates after release."""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study import preflight

H = Path(__file__).resolve().parents[1]
R = H / 'results'
release = json.loads((H / 'preparation/execution-release.json').read_text())
candidate = json.loads((H / 'preparation/integration-return.json').read_text())
assert release['candidate_pin'] == candidate['candidate']['pin']
assert (H / 'reviews/preexecution-check.md').exists()
route.execute_baseline(R)
result = preflight.run_gates(route.PACKAGE_DIR, route.MANIFEST_PATH, H / 'axes.json',
                             R / 'package_identity.json', R / 'baseline_result.json')
(R / 'preflight_results.json').write_text(json.dumps(result, indent=2) + '\n')
assert result['outcome'] == 'pass', result
identity = json.loads((R / 'package_identity.json').read_text())
assert identity['identity']['digest'] == candidate['candidate']['executable_fingerprint']
print('Exact baseline and all preflight gates passed.')
