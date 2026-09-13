"""Join the native candidate's failure identities to current regression results."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
original = json.loads((ROOT / 'work/active/WI-053_magnet-and-cryogenic-input-domains/evidence/regression-attribution.json').read_text())
root = ET.parse(HERE / 'regressions-models-final.xml').getroot()
current = {}
for case in root.iter('testcase'):
    key = case.attrib['classname'] + '::' + case.attrib['name']
    status = next((kind for kind in ('failure', 'error', 'skipped') if case.find(kind) is not None), 'passed')
    current[key] = status

rows = []
for grade, identities in [('new', original['new_failures']), ('inherited', original['inherited_failure_ids'])]:
    for old in identities:
        new = old.replace('test_peak_component_preserves_open_f07', 'test_peak_component_preserves_valid_and_rejects_invalid_domains')
        assert current.get(new) == 'passed', (old, new, current.get(new))
        if 'test_binding_documentation' in old:
            repair = 'Preserve all source bytes outside the two authorized calculation definitions; retain family twins.'
        elif 'test_current_contract_edges' in old:
            repair = 'Check current package against immutable WI-053 candidate receipt; retain original WI-051 receipts.'
        elif 'test_mfe_major_radius' in old:
            repair = 'Adapt temporary radius drivers to deliberate domain errors while retaining frozen valid/finance and independent assertions.'
        else:
            repair = 'Use WI-053 ten-seed checked generation for current fresh packages.'
        rows.append({'original_identity': old, 'original_grade': grade, 'current_identity': new, 'status': current[new], 'repair': repair})
remaining = {key: status for key, status in current.items() if status != 'passed'}
assert all(status == 'skipped' and original['baseline'].get(key, {}).get('kind') == 'skipped' for key, status in remaining.items()), remaining
output = {'native_basis': '3d9711e2', 'resolved_new': sum(r['original_grade'] == 'new' for r in rows),
          'resolved_inherited': sum(r['original_grade'] == 'inherited' for r in rows),
          'counts': {status: sum(value == status for value in current.values()) for status in ('passed', 'failure', 'error', 'skipped')},
          'dispositions': rows, 'remaining_inherited_skips': remaining}
(HERE / 'regressions-final-attribution.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps({key: output[key] for key in ('resolved_new', 'resolved_inherited', 'counts')}))
