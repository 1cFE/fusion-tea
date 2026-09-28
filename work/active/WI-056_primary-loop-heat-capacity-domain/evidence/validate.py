"""Run all six checks on the changed MFE model package; retain failure status."""
import dataclasses,json
from pathlib import Path
from agentic_mbse.validation.runner import QUALITY_CHECKS
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
results=[dataclasses.asdict(check(str(ROOT/'exploration/stellarator_e2e/models'))) for _,check in QUALITY_CHECKS]
(HERE/'candidate-validation.json').write_text(json.dumps(results,indent=2,default=str)+'\n')
print([(r['level'],r['success']) for r in results])
raise SystemExit(0 if all(r['success'] for r in results) else 1)
