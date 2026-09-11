import sys,json,tempfile,subprocess
from pathlib import Path
from collections import Counter
root=Path.cwd();sys.path.insert(0,str(root))
from tests.model_families import MFE,materialize_canonical_subset,canonical_path
from agentic_mbse.validation.level2_structure import validate_structure
from agentic_mbse.validation.level6_architecture import validate_architecture
h=Path(__file__).resolve().parent
current=materialize_canonical_subset(MFE,Path(tempfile.mkdtemp(prefix='wi050-audit-current-'))/'models')
before=materialize_canonical_subset(MFE,Path(tempfile.mkdtemp(prefix='wi050-audit-before-'))/'models')
for logical in MFE.owned:
 (before/logical).write_bytes(subprocess.check_output(['git','show','546218a5:'+str(canonical_path(logical).relative_to(root))]))
commands=[]
for level in [1,2,3]:
 cmd=[str(root/'.codex-test/run'),'agentic-mbse','validate',str(current),'--level',str(level)]
 r=subprocess.run(cmd,capture_output=True,text=True);(h/f'level-{level}.log').write_text(r.stdout+r.stderr);commands.append({'command':cmd,'returncode':r.returncode})
cmd=[str(root/'.codex-test/run'),'agentic-mbse','validate',str(current),'--complete']
r=subprocess.run(cmd,capture_output=True,text=True);(h/'complete.log').write_text(r.stdout+r.stderr);commands.append({'command':cmd,'returncode':r.returncode})
(h/'validation-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
def keys(result):return Counter(str(x.message if hasattr(x,'message') else x).split(' at file:')[0] for x in result.issues)
diff={}
for name,fn in [('L2',validate_structure),('L6',validate_architecture)]:
 a,b=keys(fn(str(before))),keys(fn(str(current)));diff[name]={'before_count':sum(a.values()),'after_count':sum(b.values()),'added':list((b-a).elements()),'removed':list((a-b).elements())}
(h/'validation-diff.json').write_text(json.dumps(diff,indent=2)+'\n')
assert diff==json.loads((h.parent/'implementation/validation-diff.json').read_text())
print(json.dumps(diff,indent=2))
