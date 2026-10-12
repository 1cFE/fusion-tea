import json, runpy, sys
from pathlib import Path
from unittest.mock import patch
root = Path.cwd()
out = root / '.project/active/mfe-major-radius-study-package/audit-evidence'
helper = root / '.project/active/mfe-major-radius-study-package/implementation/protect.py'
reads=[]; writes={}
metadata={'knowledge/holdout/fake.txt':'old','safe.txt':'old'}
def read_bytes(p):
    assert 'knowledge/holdout' not in str(p), str(p)
    reads.append(str(p)); return b'safe'
def read_text(p,*a,**k):
    assert p.name == 'protected-before.json'
    return json.dumps(metadata)
code=compile(helper.read_text(),str(helper),'exec')
with patch('subprocess.check_output',return_value=b'knowledge/holdout/fake.txt\0safe.txt\0'), patch.object(Path,'rglob',return_value=iter([])), patch.object(Path,'is_file',return_value=True), patch.object(Path,'read_bytes',read_bytes), patch.object(Path,'read_text',read_text), patch.object(Path,'write_text',lambda p,s: writes.update({p.name:s})), patch.object(sys,'argv',['protect.py','after']):
    try: exec(code,{'__file__':str(out/'protect.py')})
    except AssertionError as e:
        assert str(e).startswith("{'safe.txt':"), str(e)
assert reads == [str(root/'safe.txt')]
assert 'knowledge/holdout' not in writes['protected-after.json']
assert 'knowledge/holdout' not in writes['protected-delta.json']
(out/'guard-check.json').write_text(json.dumps({'synthetic_quarantined_paths':1,'quarantine_byte_reads':0,'allowed_reads':reads,'filter_before_read':True,'old_metadata_filtered':True},indent=2)+'\n')
print('PASS: corrected helper excludes quarantine before byte reads and comparison; synthetic execution, no broad files read')
