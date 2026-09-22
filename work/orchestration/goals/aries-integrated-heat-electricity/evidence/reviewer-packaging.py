"""Bounded review of typed adapter normalization against reviewed Git package."""
import ast,hashlib,importlib.util,json,subprocess,tempfile
from pathlib import Path
ROOT=Path.cwd();E=ROOT/'work/orchestration/goals/aries-integrated-heat-electricity/evidence'
BASE='exploration/aries_integrated/aries_integrated';package=ROOT/BASE
receipt=json.loads((ROOT/'work/active/WI-089_aries-integrated-heat-and-electricity/evidence/smart-normalization-verification.json').read_text())
changed=subprocess.check_output(['git','diff','--name-only','71b2867a','--',BASE],text=True).splitlines()
assert {str(Path(p).relative_to(BASE)) for p in changed}==set(receipt['changed_files'])
for entry in receipt['adapters']:
 rel=entry['path'];before=subprocess.check_output(['git','show','71b2867a:'+BASE+'/'+rel],text=True);after=(package/rel).read_text()
 assert hashlib.sha256(before.encode()).hexdigest()==entry['old_sha256']
 assert hashlib.sha256(after.encode()).hexdigest()==entry['new_sha256']
 a=ast.parse(before);b=ast.parse(after)
 original=next(n for n in a.body if isinstance(n,ast.FunctionDef) and n.name.startswith('run_'))
 adapter=b.body[-1];added_import=b.body[-2]
 assert isinstance(added_import,ast.ImportFrom) and added_import.module.startswith('aries_integrated.modules.')
 assert isinstance(adapter,ast.FunctionDef) and adapter.name==original.name
 assert len(adapter.body)==2 and isinstance(adapter.body[0],ast.Expr) and isinstance(adapter.body[1],ast.Return)
 call=adapter.body[1].value
 assert isinstance(call,ast.Call) and call.func.id=='_reviewed_'+original.name and len(call.args)==1 and call.args[0].id=='inputs' and not call.keywords
 assert adapter.args.args[0].annotation is not None and adapter.returns is not None
 b.body=b.body[:-2]
 renamed=next(n for n in b.body if isinstance(n,ast.FunctionDef) and n.name=='_reviewed_'+original.name)
 renamed.name=original.name
 assert ast.dump(a)==ast.dump(b),rel
old=json.loads(subprocess.check_output(['git','show','71b2867a:'+BASE+'/contracts/package_contract.json'],text=True))
new=json.loads((package/'contracts/package_contract.json').read_text())
for field in set(old)|set(new):
 if field not in ('artifact_hashes','executable_fingerprint'):assert old[field]==new[field],field
changed_hashes={k for k in old['artifact_hashes'] if old['artifact_hashes'][k]!=new['artifact_hashes'][k]}
assert changed_hashes=={r['path'] for r in receipt['adapters']}
assert len(changed_hashes)==13
spec=importlib.util.spec_from_file_location('review_run',ROOT/'exploration/aries_integrated/run.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
from simkit.evaluation.package_load import ProvisionalPackageLoader
scratch=Path(tempfile.mkdtemp(prefix='reviewer-aries-adapter-'))
module,fp=ProvisionalPackageLoader(package_dir=package,package_name='aries_integrated',link_root=scratch/'links').load()
runtime=(module,module.create_aries_integrated_registry(),str(fp))
case=r.execute_case('reviewer-adapted-calculated',{r.PREFIX+'source__producer_mode':1.},runtime,scratch)
original=json.loads((E/'reviewer-native.json').read_text())['rows'][0]
assert case['status']=='evaluated'
assert case['outputs']==original['outputs'] and case['effective_inputs']==original['effective_inputs']
refusal=r.execute_case('reviewer-adapted-zero-power',{r.PREFIX+'source__producer_mode':1.,'aries_cs_plasma_integration__plasma__deuterium_fraction':0.},runtime,scratch)
assert refusal['status']=='refused' and 'strictly positive' in refusal['error']
result={'passed':True,'old_commit':'71b2867a','old_fingerprint':old['executable_fingerprint'],'new_fingerprint':str(fp),'adapter_count':13,'exact_changed_files':receipt['changed_files'],'whole_original_module_ast_preserved':True,'public_adapters_only_forward_same_input':True,'other_contract_fields_unchanged':True,'calculated_baseline_all_outputs_and_inputs_exact':True,'zero_selected_power_refusal_preserved':True,'scratch':str(scratch)}
(E/'reviewer-packaging.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
