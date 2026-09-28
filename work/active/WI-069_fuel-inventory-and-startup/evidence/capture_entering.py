"""Read-only entering model diagnostics and executable identities for WI-069."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

from agentic_mbse.validation.level2_structure import validate_structure
from agentic_mbse.validation.level6_architecture import validate_architecture

ROOT = Path.cwd()
HERE = Path(__file__).resolve().parent
MODEL = ROOT / 'exploration/stellarator_e2e/models'
PACKAGE = ROOT / 'exploration/stellarator_e2e/generated'

def inventory(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()
            and '__pycache__' not in p.parts and p.suffix != '.pyc'}

report = {'revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
          'model_hashes': inventory(MODEL), 'package_hashes': inventory(PACKAGE)}
seeds = json.loads((ROOT / 'work/active/WI-068_layout-based-facilities/evidence/candidate-seeds.json').read_text())
found = {str(p.relative_to(PACKAGE)) for p in (PACKAGE / 'handwritten').rglob('*.py')
         if p.name == 'financial_factors.py' or re.search(r'^AUTO_IMPLEMENTED = False$', p.read_text(), re.M)}
report['seed_inventory_exact'] = found == set(seeds)
report['seed_hashes_exact'] = all(report['package_hashes'].get(p) == h for p, h in seeds.items())
report['seed_count'] = len(seeds)
for level, function in [('2', validate_structure), ('6', validate_architecture)]:
    result = function(str(MODEL))
    report[level] = {'success': result.success, 'metrics': result.metrics, 'issues': result.issues}
(HERE / 'entering-static-identities.json').write_text(json.dumps(report, indent=2, default=str) + '\n')
print(json.dumps({k: {'success': report[k]['success'], 'issue_count': len(report[k]['issues'])} for k in ('2', '6')}))
print('Seed inventory:', report['seed_count'], report['seed_inventory_exact'], report['seed_hashes_exact'])
