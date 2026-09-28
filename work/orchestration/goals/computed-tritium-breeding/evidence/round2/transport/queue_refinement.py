"""Start one refinement only after the frozen initial queue has a spare slot."""
import json
import subprocess
import time
from pathlib import Path
h=Path(__file__).resolve().parent
root=h.parents[6]
runtime=root/'.codex-test/breeding-transport/plant'
cases=json.loads((h/'table-execution-plan.json').read_text())['cases']
while True:
    all_started=all((runtime/c['name']).exists() for c in cases)
    complete=sum((runtime/c['name']/'result.json').exists() for c in cases)
    if all_started and complete>=len(cases)-3:
        break
    time.sleep(2)
print('Initial queue has no unstarted cases and at most3active; launch one refinement',flush=True)
subprocess.run([str(h.parent/'runtime/run'),str(h/'run_batch.py'),str(h/'precision-refinement-plan.json'),'--workers','1'],cwd=root,check=True)
