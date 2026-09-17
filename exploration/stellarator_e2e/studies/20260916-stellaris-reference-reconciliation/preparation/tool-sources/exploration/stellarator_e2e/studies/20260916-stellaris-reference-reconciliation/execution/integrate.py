"""Invoke native integration after independently audited comment correction."""
import json,subprocess,sys
from pathlib import Path
prior=Path('work/orchestration/goals/primary-loop-sizing/evidence/T-002_integration/integration_return.json')
cmd=json.loads(prior.read_text())['command'];cmd[cmd.index('--out-dir')+1]='work/orchestration/goals/stellaris-reference-reconciliation/evidence/T-007_integration'
cmd.extend(['--audited-work','work/orchestration/goals/stellaris-reference-reconciliation/evidence/model-correction.md@5dd9cbd0','--audited-work','work/orchestration/goals/stellaris-reference-reconciliation/evidence/source-review.md@d86e5b57'])
raise SystemExit(subprocess.call([sys.executable,*cmd]))
