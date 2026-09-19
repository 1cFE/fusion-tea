"""Verify narrow WI-068 geometry exposures preserve every earlier cooling result."""
import hashlib
import json
from pathlib import Path
import runpy
import subprocess

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
RELATIVE = 'exploration/stellarator_e2e/generated/handwritten/mfe_cooling_equipment/cooling_equipment_impl.py'
ENTERING = '1e7fd0d7'
old = {}
source = subprocess.check_output(['git', '-C', str(ROOT), 'show', ENTERING + ':' + RELATIVE], text=True)
exec(compile(source, RELATIVE, 'exec'), old)
new = runpy.run_path(str(ROOT / RELATIVE))
interface = json.loads((ROOT / 'work/active/WI-067_installed-cooling-equipment-costs/evidence/equipment-interface.json').read_text())
base = {i['name']: i['default'] for i in interface['inputs']} | {'enabled': True}
rows = []
for name, change in [('default18', {}), ('circuits14', {'n_loops': 14}),
                     ('shell_wall', {'shell_wall': .3}), ('tube_wall', {'tube_wall': .002}),
                     ('dormant', {'enabled': False})]:
    before, after = old['calculate'](base | change), new['calculate'](base | change)
    assert all(after[k] == v for k, v in before.items()), name
    rows.append({'case': name, 'unchanged_output_count': len(before),
                 'new_geometry': {k: after[k] for k in ('hx_shell_bore', 'hx_shell_wall', 'hx_shell_length', 'hx_tube_length')}})
(HERE / 'cooling-exposure-parity.json').write_text(json.dumps({
    'entering_revision': ENTERING,
    'candidate_file_sha256': hashlib.sha256((ROOT / RELATIVE).read_bytes()).hexdigest(),
    'comparison': 'Every prior calculate output is bit-identical; new geometry fields expose the actual pricing operands. Generated wrapper ABI is checked separately.',
    'cases': rows}, indent=2) + '\n')
print('PASS', len(rows), 'cases; all prior cooling calculate outputs exactly preserved')
