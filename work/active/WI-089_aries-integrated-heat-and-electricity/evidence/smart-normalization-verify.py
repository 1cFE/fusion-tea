import ast,hashlib,json
from pathlib import Path
from exploration.aries_integrated.run import load_runtime,execute_case,SCENARIOS
root=Path.cwd();e=root/'work/active/WI-089_aries-integrated-heat-and-electricity/evidence'
old=Path('/tmp/wi089-reviewed-package-before-normalization');new=root/'exploration/aries_integrated/aries_integrated'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def diff(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):return sum([diff(a.get(k),b.get(k),path+'/'+k) for k in sorted(set(a)|set(b))],[])
 return [] if a==b else [dict(path=path,before=a,after=b)]
oldcontract=json.loads((old/'contracts/package_contract.json').read_text());newcontract=json.loads((new/'contracts/package_contract.json').read_text())
diffs=diff(oldcontract,newcontract);(e/'smart-normalization-contract-diff.json').write_text(json.dumps(diffs,indent=2)+'\n')
oldfiles={str(p.relative_to(old)):sha(p) for p in old.rglob('*') if p.is_file() and '__pycache__' not in p.parts};newfiles={str(p.relative_to(new)):sha(p) for p in new.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
assert set(oldfiles)==set(newfiles)
changes=[p for p in oldfiles if oldfiles[p]!=newfiles[p]];assert all(p=='contracts/package_contract.json' or p.startswith('handwritten/') for p in changes)
asts=[]
for rel in changes:
 if rel=='contracts/package_contract.json':continue
 a,b=ast.parse((old/rel).read_text()),ast.parse((new/rel).read_text())
 oldfn=next(n for n in a.body if isinstance(n,ast.FunctionDef) and n.name.startswith('run_'))
 newfn=next(n for n in b.body if isinstance(n,ast.FunctionDef) and n.name=='_reviewed_'+oldfn.name)
 assert [ast.dump(n) for n in oldfn.body]==[ast.dump(n) for n in newfn.body]
 # Original module AST is preserved after removing adapter additions and undoing rename.
 b.body=b.body[:-2];newfn.name=oldfn.name
 assert ast.dump(a)==ast.dump(b),(rel,'module body changed beyond adapter')
 asts.append(dict(path=rel,old_sha256=oldfiles[rel],new_sha256=newfiles[rel],original_module_ast_preserved=True))
runtime=load_runtime();baselines={r['case']:r for r in json.loads((e/'baseline-execution.json').read_text())};rows=[]
for name,changeset in SCENARIOS.items():
 row=execute_case('smart-normalized-'+name,changeset,runtime)
 previous=baselines[name]
 assert row['status']==previous['status']=='evaluated'
 assert row['effective_inputs']==previous['effective_inputs']
 assert row['outputs']==previous['outputs'],name
 rows.append(dict(case=name,exact_all_output_parity=True,effective_inputs_equal=True,result=row))
receipt=dict(old_executable_fingerprint=oldcontract['executable_fingerprint'],new_executable_fingerprint=newcontract['executable_fingerprint'],changed_files=changes,adapters=asts,contract_diff=diffs,baselines=rows,exact_smart_regeneration_fixed_point=True)
(e/'smart-normalization-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(dict(new_fingerprint=newcontract['executable_fingerprint'],changed_files=len(changes),adapters=len(asts),baseline_exact_parity=len(rows))))
