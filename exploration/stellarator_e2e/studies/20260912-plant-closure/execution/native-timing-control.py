import json,time
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route as route
from simkit.study.bridge import CandidateBridge
H=Path('exploration/stellarator_e2e/studies/20260912-plant-closure');t=time.monotonic();p=route.prepare(route.PACKAGE_DIR,Path('/tmp/plant-native-timing-links'));prepared=time.monotonic()-t
i=CandidateBridge(p.entry_models).build(route._baseline_point(route.MANIFEST_PATH));t=time.monotonic();e=p.evaluate(i);elapsed=time.monotonic()-t
old=json.loads((H/'results/baseline-native-evidence.json').read_text());assert dict(e.outputs)==old['outputs'] and dict(e.responses)==old['responses']
print(json.dumps({'kind':'timed repeat of approved unstored baseline, not a study case','preparation_seconds':prepared,'evaluation_seconds':elapsed,'exact_retained_baseline_match':True}))
