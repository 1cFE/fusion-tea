"""Actual baseline CLI gates and exact unsupported argument refusal."""
import json
import subprocess
import sys
from pathlib import Path
H=Path(sys.argv[1]).resolve(); CODE=Path(__file__).resolve().parent
P='stellarator_09__stellaris__'
rows=[]
for args in [[],[P+'magnet__R0=14'],[P+'R=14',P+'magnet__R0=14'],[P+'R=14',P+'magnet__R0=12.7'],[P+'magnet__R0=0']]:
    cmd=['.codex-test/run','python',str(CODE/'cli_entry.py'),str(H/f'cli-output-{len(rows)}'),*args]
    r=subprocess.run(cmd,capture_output=True,text=True)
    (H/f'cli-{len(rows)}.log').write_text(r.stdout+r.stderr)
    rows.append({'command':cmd,'exit':r.returncode,'arguments':args})
    assert r.returncode==(1 if args else 0)
    if args: assert 'Unsupported command-line arguments: '+' '.join(args) in r.stderr
(H/'cli-checks.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS actual CLI baseline and exact old-key alone/equal/conflicting/zero refusal')
