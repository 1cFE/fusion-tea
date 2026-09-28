"""Invoke native proof on unchanged entering model and audited lineage."""
import json, subprocess, sys
from pathlib import Path
prior=Path('work/orchestration/goals/divertor-peak-heat-load/evidence/T-003_integration/integration_return.json')
cmd=json.loads(prior.read_text())['command']
cmd[cmd.index('--out-dir')+1]='work/orchestration/goals/primary-loop-sizing/evidence/T-002_integration'
raise SystemExit(subprocess.call([sys.executable,*cmd]))
