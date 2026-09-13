"""Independent exact fresh and stock in-place coherence, with all handwritten files."""
import ast,hashlib,importlib.util,json,shutil,subprocess,tempfile
from pathlib import Path
R=Path.cwd();E=R/'work/active/WI-056_primary-loop-heat-capacity-domain/evidence';O=Path(__file__).resolve().parent;P=R/'exploration/stellarator_e2e/generated'
def hashes(p):return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc'}
def func(s):return next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef))
name='handwritten/mfe_primary_loop/primary_coolant_loop_impl.py'
a=func(subprocess.check_output(['git','show','b413838c:exploration/stellarator_e2e/generated/'+name],text=True));b=func((P/name).read_text())
assert ast.dump(a.args)==ast.dump(b.args)
assert [ast.dump(n) for n in a.body]==[ast.dump(n) for n in b.body]
assert ast.dump(b.returns)==ast.dump(ast.parse('tuple['+', '.join(['float']*13)+']',mode='eval').body)
oldseeds=json.loads((E/'candidate-seeds.json').read_text());seeds=json.loads((E/'corrected-candidate-seeds.json').read_text())
assert len(seeds)==13 and set(seeds)==set(oldseeds)
assert {k for k in seeds if seeds[k]!=oldseeds[k]}=={name}
expected=json.loads((E/'corrected-package-hashes.json').read_text());assert hashes(P)==expected
s=importlib.util.spec_from_file_location('corrected_generation',E/'regenerate_corrected.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def stock(path,label):
 command=[str(R/'.codex-test/run'),'sysml-codegen','generate','--models',str(R/'exploration/stellarator_e2e/models'),'--output',str(path),'--package-name','stellarator_tea','--overwrite','--smart-regen','--preserve-handwritten']
 r=subprocess.run(command,text=True,capture_output=True);(O/(label+'.log')).write_text(r.stdout+r.stderr);assert r.returncode==0
 observed=hashes(path);assert observed==expected,{k for k in expected.keys()|observed.keys() if expected.get(k)!=observed.get(k)}
with tempfile.TemporaryDirectory(prefix='wi056-corrected-audit-') as t:
 fresh=m.seed_and_generate(Path(t)/'fresh',models_path=R/'exploration/stellarator_e2e/models');assert hashes(fresh)==expected
 stock(fresh,'stock-after-fresh')
 existing=Path(t)/'existing';shutil.copytree(P,existing,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 stock(existing,'stock-after-existing')
assert hashes(P)==expected
summary={'exact_thirteen_float_annotation':True,'guarded_body_and_arguments_unchanged':True,'twelve_other_seeds_unchanged':True,'fresh_exact_files':len(expected),'stock_inplace_after_fresh_exact':True,'stock_inplace_after_existing_exact':True,'all_handwritten_and_backup_paths_included':True,'production_unchanged_by_audit':True}
(O/'corrected-checks.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
