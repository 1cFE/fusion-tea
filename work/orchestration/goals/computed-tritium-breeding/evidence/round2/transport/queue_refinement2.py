"""Respect the four-job cap across initial and first refinement queues."""
import json
import subprocess
import time
from pathlib import Path
h=Path(__file__).resolve().parent;root=h.parents[6];runtime=root/'.codex-test/breeding-transport/plant'
cases=[]
for plan in ['table-execution-plan.json','precision-refinement-plan.json']:
 cases+=json.loads((h/plan).read_text())['cases']
while True:
 if all((runtime/c['name']).exists() for c in cases) and sum(not (runtime/c['name']/'result.json').exists() for c in cases)<=3:break
 time.sleep(2)
print('Atmost3otherjobs; launch one precision refinement',flush=True)
subprocess.run([str(h.parent/'runtime/run'),str(h/'run_batch.py'),str(h/'precision-refinement2-plan.json'),'--workers','1'],cwd=root,check=True)
