import json,sys
from pathlib import Path
from unittest.mock import patch
root=Path.cwd(); audit=root/'.project/active/mfe-major-radius-study-package/audit-evidence'; impl=audit.parent/'implementation'; out=audit/'guard-real'; out.mkdir()
(out/'protected-before.json').write_bytes((impl/'protected-before.json').read_bytes())
source=(impl/'protect.py').read_text(); code=compile(source,str(impl/'protect.py'),'exec'); original=Path.read_bytes; calls=[]; refused=[]
def read(p):
    if p.resolve().is_relative_to((root/'knowledge/holdout').resolve()):
        refused.append(str(p)); raise RuntimeError('quarantine read blocked')
    calls.append(str(p)); return original(p)
with patch.object(Path,'read_bytes',read),patch.object(sys,'argv',['protect.py','after']):
    try: exec(code,{'__file__':str(out/'protect.py')})
    except AssertionError:
        delta=json.loads((out/'protected-delta.json').read_text())
        assert set(delta)=={'.project/CURRENT_WORK.md'}, delta
assert len(calls)==14363 and not refused
(out/'guard-result.json').write_text(json.dumps({'permitted_reads':len(calls),'quarantine_attempts':len(refused),'delta':json.loads((out/'protected-delta.json').read_text()),'delta_disposition':'CURRENT_WORK was already modified at audit entry; preserved, not reset'},indent=2)+'\n')
print('PASS actual corrected helper: 14363 allowed reads, 0 quarantine attempts; sole CURRENT_WORK delta retained')
