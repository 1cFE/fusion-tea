from pathlib import Path
import json
from tests.model_families import MFE, materialize_canonical_subset
from agentic_mbse.validation.level2_structure import validate_structure

root=Path(__file__).resolve().parent
before=materialize_canonical_subset(MFE,root/'baseline-models')
def issues(path):
    result=validate_structure(str(path))
    return [str(i).replace(str(path),'MODEL') for i in result.issues]
a,b=issues(before),issues(root/'models')
assert a==b,(a,b)
(root/'l2-differential.json').write_text(json.dumps(dict(before=a,after=b,new=[]),indent=2)+'\n')
print('PASS L2 issue identities unchanged:',len(a))
