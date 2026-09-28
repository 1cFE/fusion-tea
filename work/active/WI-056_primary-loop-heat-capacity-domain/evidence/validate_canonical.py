"""Comparable canonical all-level evidence using the entering audit's scope."""
import json
from pathlib import Path
from agentic_mbse.validation.runner import QUALITY_CHECKS
HERE=Path(__file__).resolve().parent
rows=[]
for _,check in QUALITY_CHECKS:
 r=check('models');rows.append({k:getattr(r,k) for k in ('level','success','issues','warnings','metrics')})
(HERE/'canonical-validation.json').write_text(json.dumps(rows,indent=2)+'\n')
print([(r['level'],r['success']) for r in rows])
raise SystemExit(0 if all(r['success'] for r in rows) else 1)
