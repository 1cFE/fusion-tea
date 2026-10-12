import json,runpy,sys,subprocess
from pathlib import Path
from unittest.mock import patch
root=Path.cwd(); out=root/'.project/active/mfe-major-radius-study-package/audit-evidence/metadata'; out.mkdir()
work=out/'execution'; work.mkdir()
paths=[root/'exploration/stellarator_e2e/studies/manifest.json',root/'tests/study/test_known_answers.py']+list((root/'tests/study/data').glob('*.expected.json'))
redirect={p.resolve():out/'copies'/p.relative_to(root) for p in paths}
read=Path.read_text; write=Path.write_text; check=subprocess.check_output
for p,q in redirect.items(): q.parent.mkdir(parents=True,exist_ok=True); write(q,read(p))
def read_redirect(p,*a,**k): return read(redirect.get(p.resolve(),p),*a,**k)
def write_redirect(p,s,*a,**k):
    q=redirect.get(p.resolve(),p)
    assert q.resolve().is_relative_to(out),str(q)
    return write(q,s,*a,**k)
def child(args,*a,**k):
    assert str(args[0]).endswith('.codex-test/run')
    args=[str(redirect.get(Path(v).resolve(),v)) if isinstance(v,str) else v for v in args]
    return check(args,*a,**k)
with patch.object(Path,'read_text',read_redirect),patch.object(Path,'write_text',write_redirect),patch('subprocess.check_output',child),patch.object(sys,'argv',['refresh_metadata.py',str(work)]):
    runpy.run_path(str(out.parent.parent/'implementation/refresh_metadata.py'),run_name='__main__')
comparison={str(p.relative_to(root)):p.read_bytes()==q.read_bytes() for p,q in redirect.items()}
(out/'reproduction.json').write_text(json.dumps(comparison,indent=2)+'\n')
assert all(comparison.values()),comparison
print('PASS exact native metadata reproduction in isolated outputs')
