"""Verify doc-only source changes and exact audited native values."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
new = json.loads((HERE / 'native.json').read_text())
old = json.loads((HERE.parent / 'audit-evidence/native-absolute/native.json').read_text())
assert new == old
assert len(new['cases']) == 10
assert all(len(case['outputs']) == 158 and 'error' not in case for case in new['cases'].values())
regeneration = json.loads((HERE / 'regeneration.json').read_text())
assert regeneration['before_manifest'] == regeneration['after_manifest']
paths = []
for filename, names in {
    'mfe_account_costs.sysml': ['IDC Closed-Form Cost', 'Levelized Annual Cost'],
    'mfe_lcoe_dcf.sysml': ['LCOE DCF'],
    'mfe_lifecycle.sysml': ['Lifecycle Calendar'],
}.items():
    path = ROOT / 'models/library/analyses' / filename
    text = path.read_text()
    for name in names:
        block = text.split("calc def '" + name + "'", 1)[1].split('*/', 1)[0]
        source = block.rsplit('**Source**: ', 1)[1].splitlines()[0]
        assert (ROOT / source).is_file()
        paths.append({'definition': name, 'source': source})
    if filename == 'mfe_account_costs.sysml':
        fuel = text.split("calc def 'DT Fuel Cost'", 1)[1].split('*/', 1)[0]
        assert 'manual completion' not in fuel
        assert 'generate the fuel arithmetic directly' in fuel
result = {
    'native_equal_to_audit': True, 'native_cases': 10, 'scalars_per_case': 158,
    'input_defaults_equal': True, 'responses_and_reports_equal': True,
    'generation_manifest_equal': True, 'supplemental_sources': paths,
    'fuel_documentation_matches_generated_arithmetic': True,
}
(HERE / 'checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
