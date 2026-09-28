"""Recheck all failed-record native points; retain the eight expected failures."""
from pathlib import Path
import importlib.util,json
HERE=Path(__file__).resolve().parent
source=HERE.parent/'verification-failure-r1/scan_discrepancies.py'
spec=importlib.util.spec_from_file_location('unchanged_forensic_checks',source)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.HERE=HERE/'original2496';module.HERE.mkdir(exist_ok=False)
module.run()
result=json.loads((module.HERE/'discrepancies.json').read_text());s=result['summary']
assert s['cases']==s['evaluated']==2496
assert s['off_tolerance_comparisons']==8 and s['off_tolerance_cases']==4
assert s['predicate_mismatches']==s['evaluation_errors']==0 and s['inputs_unchanged']
assert {r['channel'].rsplit('__',1)[-1] for r in result['scalar_failures']}=={'cold_margin_W','extra_cold_capacity_W'}
assert all(r['case'].startswith('cryo-capacity-') for r in result['scalar_failures'])
print('PASS: 2492 unchanged points pass; exactly eight original cryogenic scalar failures retained')
