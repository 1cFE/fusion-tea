"""Independent receipt/body/fresh-generation checks; never mutates production."""
import ast, hashlib, importlib.util, json, subprocess, tempfile
from pathlib import Path
ROOT=Path.cwd(); E=ROOT/'work/active/WI-056_primary-loop-heat-capacity-domain/evidence'; OUT=Path(__file__).resolve().parent
P=ROOT/'exploration/stellarator_e2e/generated'
def hashes(root):
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
def function(s):return next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef))
old=subprocess.check_output(['git','show','cea6bc1a:exploration/stellarator_e2e/generated/handwritten/mfe_primary_loop/primary_coolant_loop_impl.py'],text=True)
new=(P/'handwritten/mfe_primary_loop/primary_coolant_loop_impl.py').read_text()
assert [ast.dump(n) for n in function(old).body[1:]]==[ast.dump(n) for n in function(new).body[3:]]
assert len(function(new).body[-1].value.elts)==13
enter=json.loads(subprocess.check_output(['git','show','cea6bc1a:work/active/WI-055_winding-pack-input-domain/evidence/candidate-seeds.json']))
seeds=json.loads((E/'candidate-seeds.json').read_text()); assert len(enter)==12 and len(seeds)==13
assert all(seeds[k]==v for k,v in enter.items())
receipt=json.loads((E/'candidate-package-hashes.json').read_text()); assert hashes(P)==receipt
spec=importlib.util.spec_from_file_location('audit_generate',E/'regenerate.py'); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory(prefix='independent-wi056-') as td:
 fresh=m.seed_and_generate(Path(td)/'fresh',models_path=ROOT/'exploration/stellarator_e2e/models')
 assert hashes(fresh)==receipt
assert hashes(P)==receipt
assert (ROOT/'models/library/analyses/mfe_primary_loop.sysml').read_bytes()==(ROOT/'exploration/stellarator_e2e/models/analyses/mfe_primary_loop.sysml').read_bytes()
# Exact historical namespaces only; no source/quarantine or broad preservation traversal.
historical=[f'work/active/{name}' for name in ['WI-050_mfe-coherent-operating-heating','WI-051_mfe-model-owned-major-radius','WI-052_mfe-financial-rate-limits','WI-053_magnet-and-cryogenic-input-domains','WI-054_faithful-model-equations-and-citations','WI-055_winding-pack-input-domain']]
assert all((ROOT/p).is_dir() for p in historical)
changed=subprocess.check_output(['git','diff','--name-only','cea6bc1a','--',*historical,'models/designs/generic_ife','models/library/analyses/ife_power_balance.sysml'],text=True).splitlines()
assert not changed,changed
result={'ordered_valid_body_equal':True,'output_tuple_count':13,'prior_seeds_preserved':12,'seeds':13,'exact_fresh_receipt_files':len(receipt),'production_unchanged_by_audit':True,'source_twins_equal':True,'checked_historical_paths':historical,'historical_diff':changed}
(OUT/'checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
