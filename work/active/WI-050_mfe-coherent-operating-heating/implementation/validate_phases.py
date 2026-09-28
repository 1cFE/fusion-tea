"""Retain each required phase's native levels, including accepted failures."""
from pathlib import Path
import subprocess,json
h=Path(__file__).resolve().parent
models=Path((h/'scratch.txt').read_text().strip())/'models'
summary={}
for phase in range(1,6):
 for level in range(1,4):
  cmd=['.codex-test/run','agentic-mbse','validate',str(models),f'--level={level}']
  target=h/f'phase-{phase}-level-{level}.log'
  with target.open('w') as log:
   log.write(repr(cmd)+'\n');log.flush();result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
  summary[f'phase-{phase}-level-{level}']={'command':cmd,'exit':result.returncode}
  assert result.returncode==(1 if level==2 else 0),(phase,level)
with (h/'validation-complete.log').open('w') as log:
 cmd=['.codex-test/run','agentic-mbse','validate',str(models),'--complete'];log.write(repr(cmd)+'\n');log.flush();r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
summary['complete']={'command':cmd,'exit':r.returncode}
assert r.returncode==1
(h/'validation-commands.json').write_text(json.dumps(summary,indent=2)+'\n')
