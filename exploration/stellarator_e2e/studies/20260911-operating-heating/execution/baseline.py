import json
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study import preflight
HERE=Path(__file__).resolve().parents[1]
R=HERE/'results'
route.execute_baseline(R)
gates=preflight.run_gates(route.PACKAGE_DIR,route.MANIFEST_PATH,HERE/'axes.json',R/'package_identity.json',R/'baseline_result.json')
(R/'preflight.json').write_text(json.dumps(gates,indent=2)+'\n')
print(preflight.human_summary(gates))
assert gates['outcome']=='pass'
