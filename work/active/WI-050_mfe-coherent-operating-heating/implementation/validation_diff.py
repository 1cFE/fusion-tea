import json, sys, tempfile, subprocess
sys.path.insert(0, str(__import__("pathlib").Path.cwd()))
from tests.model_families import MFE, materialize_canonical_subset
from pathlib import Path
from collections import Counter
from agentic_mbse.validation.level6_architecture import validate_architecture
from agentic_mbse.validation.level2_structure import validate_structure
h=Path(__file__).resolve().parent
before=materialize_canonical_subset(MFE, Path(tempfile.mkdtemp(prefix='wi050-r1-entering-'))/'models'); after=Path((h/'scratch.txt').read_text().strip())/'models'
for logical in MFE.owned:
 from tests.model_families import canonical_path
 path=canonical_path(logical).relative_to(Path.cwd())
 (before/logical).write_bytes(subprocess.check_output(['git','show','546218a5:'+str(path)]))
(h/'entering-models.txt').write_text(str(before)+'\n')
def keys(result):
 return Counter(str(x.message if hasattr(x,'message') else x).split(' at file:')[0] for x in result.issues)
out={}
for name,fn in [('L2',validate_structure),('L6',validate_architecture)]:
 a,b=keys(fn(str(before))),keys(fn(str(after)))
 out[name]={'before_count':sum(a.values()),'after_count':sum(b.values()),'added':list((b-a).elements()),'removed':list((a-b).elements())}
(h/'validation-diff.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))

expected=json.loads((h.parent/'prototype-r1/validation-diff.json').read_text());assert out==expected,(out,expected)
