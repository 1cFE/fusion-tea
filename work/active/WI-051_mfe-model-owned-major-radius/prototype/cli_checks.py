"""Baseline-only CLI refuses unsupported arguments instead of ignoring them."""
import json, subprocess
from pathlib import Path
H=Path(__file__).resolve().parent; P='stellarator_09__stellaris__'
rows=[]
for args in [[],[P+'magnet__R0=14'],[P+'R=14',P+'magnet__R0=14'],[P+'R=14',P+'magnet__R0=12.7']]:
    cmd=['.codex-test/run','python',str(H/'direct-prototype/run_stellaris_single.py'),*args]
    r=subprocess.run(cmd,capture_output=True,text=True)
    (H/f'cli-{len(rows)}.log').write_text(r.stdout+r.stderr)
    rows.append({'command':cmd,'exit':r.returncode})
    assert r.returncode==(1 if args else 0)
    if args: assert P+'magnet__R0' in r.stderr
(H/'cli-checks.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS baseline CLI and retired-key argument refusal (alone/equal/conflicting)')
