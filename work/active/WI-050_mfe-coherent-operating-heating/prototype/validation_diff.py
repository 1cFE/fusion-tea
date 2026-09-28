import json
from pathlib import Path
from collections import Counter
from agentic_mbse.validation.level6_architecture import validate_architecture
from agentic_mbse.validation.level2_structure import validate_structure
h=Path(__file__).resolve().parent
before=Path('/tmp/wi050-entering-models'); after=Path((h/'scratch.txt').read_text().strip())/'models'
def keys(result):
 return Counter(str(x.message if hasattr(x,'message') else x).split(' at file:')[0] for x in result.issues)
out={}
for name,fn in [('L2',validate_structure),('L6',validate_architecture)]:
 a,b=keys(fn(str(before))),keys(fn(str(after)))
 out[name]={'before_count':sum(a.values()),'after_count':sum(b.values()),'added':list((b-a).elements()),'removed':list((a-b).elements())}
(h/'validation-diff.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
