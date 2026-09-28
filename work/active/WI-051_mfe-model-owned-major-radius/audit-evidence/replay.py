"""Independent native generation and location-aware validation of committed sources."""
import ast, collections, difflib, hashlib, json, re, shutil, subprocess, sys
from pathlib import Path
ROOT=Path.cwd(); A=Path(__file__).resolve().parent; I=A.parent/'implementation'
sys.path.insert(0,str(ROOT))
from tests.model_families import MFE, materialize_canonical_subset, canonical_path
from sysml_codegen.cli import GenerationConfig, run_codegen
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files(p):return {str(f.relative_to(p)):f.read_bytes() for f in sorted(p.rglob('*')) if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc'}
def dump(n,x):(A/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
models=materialize_canonical_subset(MFE,A/'models')
old=A/'entering-models';old.mkdir()
for name in MFE.owned:
    p=old/name;p.parent.mkdir(parents=True,exist_ok=True)
    relative=str(canonical_path(name).relative_to(ROOT))
    p.write_bytes(subprocess.check_output(['git','show','45003717:'+relative]))
    assert p.read_bytes()==(I/'entering-models'/name).read_bytes()
    assert (models/name).read_bytes()==(MFE.twin/name).read_bytes()
manual={
'handwritten/mfe_lifecycle/lifecycle_calendar_impl.py',
'handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py',
'handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py',
'handwritten/mfe_power_cycle/power_cycle_efficiency_impl.py'}
seeds={n:subprocess.check_output(['git','show','45003717:exploration/stellarator_e2e/generated/'+n]) for n in manual}
for label,kwargs in [('source',{'models_path':models}),('snapshot',{'from_snapshot':A/'fresh.snapshot.json'})]:
    target=A/('generated-'+label);target.mkdir(exist_ok=False)
    for name,content in seeds.items():
        p=target/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
    assert files(target)==seeds
    dump(label+'-seeds.json',{k:hashlib.sha256(v).hexdigest() for k,v in files(target).items()})
    assert run_codegen(GenerationConfig(output_path=target,package_name='stellarator_tea',preserve_handwritten=True,overwrite=True,**kwargs))
    assert all((target/k).read_bytes()==v for k,v in seeds.items())
    if label=='source':capture_instance_graph_snapshot([models],A/'fresh.snapshot.json')
prod=ROOT/'exploration/stellarator_e2e/generated'
fresh=files(A/'generated-source');assert fresh==files(A/'generated-snapshot')==files(prod)
assert (A/'fresh.snapshot.json').read_bytes()==(ROOT/'exploration/stellarator_e2e/stellarator.snapshot.json').read_bytes()
class StripDocs(ast.NodeTransformer):
    def strip(self,node):
        self.generic_visit(node)
        if node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):node.body=node.body[1:]
        return node
    visit_Module=visit_FunctionDef=visit_AsyncFunctionDef=visit_ClassDef=strip
body=[]
for name,data in fresh.items():
    if name.startswith('handwritten/') and name.endswith('_impl.py'):
        prior=subprocess.check_output(['git','show','45003717:exploration/stellarator_e2e/generated/'+name])
        equal=ast.dump(StripDocs().visit(ast.parse(prior)))==ast.dump(StripDocs().visit(ast.parse(data)))
        assert equal,name
        body.append({'path':name,'manual':name in manual,'bytes_equal':prior==data,'executable_ast_without_docstrings_equal':equal})
        if prior!=data:
            d=A/'body-diffs'/name;d.parent.mkdir(parents=True,exist_ok=True)
            d.with_suffix('.diff').write_text(''.join(difflib.unified_diff(prior.decode().splitlines(True),data.decode().splitlines(True),fromfile='entering/'+name,tofile='production/'+name)))
dump('generation.json',{'all_package_bytes_equal':True,'snapshot_bytes_equal':True,'files':{k:hashlib.sha256(v).hexdigest() for k,v in fresh.items()},'bodies':body,'sources':{k:hashlib.sha256(v).hexdigest() for k,v in files(models).items()}})
print('INDEPENDENT GENERATION PASS',flush=True)
# Invoke all six levels through the native CLI, retaining failing levels honestly.
for label,path in [('entering',old),('current',models)]:
    command=['.codex-test/run','agentic-mbse','validate',str(path),'--complete']
    with (A/(label+'-validation.log')).open('x') as out:r=subprocess.run(command,stdout=out,stderr=subprocess.STDOUT,cwd=ROOT)
    dump(label+'-validation-command.json',{'command':command,'exit':r.returncode})
# Compare diagnostics including locations on identical source lines only.
from agentic_mbse.validation.level2_structure import validate_structure
from agentic_mbse.validation.level6_architecture import validate_architecture
maps={}
for name in MFE.owned:
    a=(old/name).read_text().splitlines();b=(models/name).read_text().splitlines()
    maps[name]={block.b+i+1:block.a+i+1 for block in difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_matching_blocks() for i in range(block.size)}
delta={}
for level,fn in [('L2',validate_structure),('L6',validate_architecture)]:
    sides={}
    for side,root in [('entering',old),('current',models)]:
        rows=[]
        for issue in fn(str(root)).issues:
            raw=str(getattr(issue,'message',issue)); msg=raw.replace(str(root)+'/', '')
            m=re.search(r' at file:(.*\.sysml):(\d+)',msg)
            if m:
                name=m[1].lstrip('/');line=int(m[2]);mapped=line if side=='entering' else maps[name].get(line,'CHANGED-'+str(line))
                msg=msg[:m.start()]+f' at file:{name}:{mapped}'+msg[m.end():]
            rows.append({'raw':raw,'normalized':msg})
        sides[side]=rows
    before,after=[collections.Counter(r['normalized'] for r in sides[s]) for s in ('entering','current')]
    delta[level]={'diagnostics':sides,'added':list((after-before).elements()),'removed':list((before-after).elements()),'inherited':dict(before&after)}
dump('diagnostic-delta.json',delta)
assert all(not x['added'] and not x['removed'] for x in delta.values())
print('INDEPENDENT DIAGNOSTIC PRESERVATION PASS',flush=True)
