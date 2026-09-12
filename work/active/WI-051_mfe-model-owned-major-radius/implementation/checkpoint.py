"""Retain native checkpoint exits and full diagnostic multisets."""
import sys
from collections import Counter
from common import H, dump, run_logged

def differential():
    from agentic_mbse.validation.level2_structure import validate_structure
    from agentic_mbse.validation.level6_architecture import validate_architecture
    diffs={}
    for level,fn in [('L2',validate_structure),('L6',validate_architecture)]:
        def issues(root):
            result=fn(str(root))
            # Native messages include qualified affected element; only file location
            # trailers (root and shifted line offsets) are excluded, as in the reviewed probe.
            return Counter(str(x.message if hasattr(x,'message') else x).split(' at file:')[0] for x in result.issues)
        a,b=issues(H/'entering-models'),issues(H/'models')
        diffs[level]={'before':sum(a.values()),'after':sum(b.values()),'added':list((b-a).elements()),'removed':list((a-b).elements()),'inherited':dict(a&b)}
    dump('validation-diff.json',diffs)
    assert all(not x['added'] and not x['removed'] for x in diffs.values())
    print({k:{n:v for n,v in x.items() if n!='inherited'} for k,x in diffs.items()})

if __name__=='__main__':
    phase=sys.argv[1]
    for level in (1,2,3):
        code=run_logged(f'{phase}-L{level}',['agentic-mbse','validate',str(H/'models'),f'--level={level}'])
        assert code==(1 if level==2 else 0)
    differential()
