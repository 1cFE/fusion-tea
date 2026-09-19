"""Retain complete issue identities, comparing entering source to WI-068."""
from pathlib import Path
import json,re,subprocess
from collections import Counter
from agentic_mbse.validation.level6_architecture import validate_architecture
from agentic_mbse.validation.level2_structure import validate_structure
ROOT=Path.cwd(); E=ROOT/'work/active/WI-068_layout-based-facilities/evidence'; old=Path('/tmp/wi068-static-entering')
prefix='exploration/stellarator_e2e/models/'
files=subprocess.check_output(['git','ls-tree','-r','--name-only','1e7fd0d7','--',prefix],text=True).splitlines()
for name in files:
    if name.endswith('.sysml'):
        p=old/name.removeprefix(prefix);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(subprocess.check_output(['git','show',f'1e7fd0d7:{name}']))
def normalized(s):
    return re.sub(r' at file:.*$', '',s)
report={}
for level,fn in [(2,validate_structure),(6,validate_architecture)]:
    rows={}
    for label,path in [('entering',old),('current',ROOT/prefix)]:
        result=fn(str(path));rows[label]={'success':result.success,'metrics':result.metrics,'issues':result.issues}
    before=Counter(map(normalized,rows['entering']['issues']));after=Counter(map(normalized,rows['current']['issues']))
    rows['added']=list((after-before).elements());rows['removed']=list((before-after).elements());report[str(level)]=rows
(E/'static-delta.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
print({k:{'entering':len(v['entering']['issues']),'current':len(v['current']['issues']),'added':len(v['added']),'removed':len(v['removed'])} for k,v in report.items()})
# Classify added reports against the actual owning declarations, not calc formals.
source='\n'.join((ROOT/f).read_text() for f in ['models/designs/generic_mfe/mfe_subsystems.sysml','models/designs/generic_mfe/mfe_plant.sysml','models/library/structure/mfe_plant_systems.sysml'])
added=report['6']['added'];kinds=Counter('dot reference' if "Unsupported operator '.'" in s else 'numeric-default extraction' if 'cannot extract a numeric default' in s else 'OTHER' for s in added)
attrs=sorted(set(re.search(r"attribute '(.*)'(?: has expression|$)",s).group(1).split('::')[-1] for s in added));rows=[]
for name in attrs:
    expressions=re.findall(r'attribute\s+'+re.escape(name)+r'\s*:\s*Real\s*=\s*([^;]+);',source)
    rows.append({'attribute':name,'expressions':expressions,'pure_dotted_references':bool(expressions) and all(re.fullmatch(r'\w+\.\w+',v.strip()) for v in expressions)})
classification={'l2_added':report['2']['added'],'l6_added_kinds':dict(kinds),'attributes':rows,'all_added_are_pure_exposes':all(r['pure_dotted_references'] for r in rows),'limits':'Lexical classification of actual added issue identities; executable generation and oracle tests separately verify the resolved values.'}
(E/'static-delta-classification.json').write_text(json.dumps(classification,indent=2)+'\n')
