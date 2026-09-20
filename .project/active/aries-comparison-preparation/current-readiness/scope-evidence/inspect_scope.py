"""Read-only contract/identity inspection; writes only adjacent diagnostic receipts."""
from pathlib import Path
import json, hashlib, subprocess, tarfile, importlib.util, sys
ROOT=Path.cwd(); OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from scripts.study import indicators, manifest
P=ROOT/'exploration/stellarator_e2e/generated'; C=ROOT/'.project/active/aries-comparison-preparation/package'
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args): return subprocess.check_output(['git',*args],text=True).strip()
def save(name,d): (OUT/name).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
m=read(P/'contracts/model_contract.json'); pc=read(P/'contracts/package_contract.json'); loaded=manifest.load(ROOT/'exploration/stellarator_e2e/studies/manifest.json'); fp=manifest.indicator_input_fingerprint(P)
parsed=indicators.read_pipelines(P); paths=parsed.artifact_paths+[P/'contracts/model_contract.json']; manifest.assert_package_identity(loaded,P); manifest.assert_pin_matches(loaded,fp)
coverage={}
for group,pp in [('all_actual_reads',paths),('input_files',parsed.input_files)]:
 try: manifest.assert_read_set_covered(pp,P,loaded);coverage[group]={'status':'pass','count':len(pp)}
 except Exception as e: coverage[group]={'status':'fail','error':str(e)}
coverage['reads']=[{'path':p.relative_to(P).as_posix(),'sha256':sha(p)} for p in paths]
coverage['negative_guards']={}
for p in [P/'uncovered-input.json',ROOT/'outside-package-input.json']:
 try: manifest.assert_read_set_covered([p],P,loaded); coverage['negative_guards'][str(p)]='ACCEPTED'
 except manifest.ManifestError as e: coverage['negative_guards'][str(p)]=str(e)
spec=importlib.util.spec_from_file_location('scope_verify',P/'contracts/verify.py'); v=importlib.util.module_from_spec(spec);sys.modules[spec.name]=v;spec.loader.exec_module(v);seal=v.verify_package(P,'stellarator_tea',runtime_version='2.0.0',strict=True)
models=['models','exploration/stellarator_e2e/models']; surfaces=models+['exploration/stellarator_e2e/generated','exploration/stellarator_e2e/verify_stellaris.py','exploration/stellarator_e2e/studies/oracle_entry.py']
identity={'head':git('rev-parse','HEAD'),'latest_model_commit':git('log','-1','--format=%H','--',*models),'latest_package_commit':git('log','-1','--format=%H','--','exploration/stellarator_e2e/generated'),'status':git('status','--short','--',*surfaces),'candidate_diff':git('diff','--name-only','fe7205533b191fb538ade6a6ed89d59d04545b82','--',*surfaces),'semantic':m['semantic_fingerprint'],'executable':pc['executable_fingerprint'],'indicator':fp['digest'],'seal_ok':seal.ok,'seal_diagnostics':str(seal.diagnostics),'sealed_artifacts':len(pc['artifact_hashes']),'all_inputs':{p.name:read(p) for p in parsed.input_files}}
save('identity.json',identity);save('read-set.json',coverage)
a=C/'freeze/r2/comparison-freeze.tar.gz';ar={'sha256_before':sha(a),'bytes':a.stat().st_size,'matching':[],'different':[],'missing_current':[]}
with tarfile.open(a,'r:gz') as t:
 for member in t.getmembers():
  name=member.name
  if member.isfile() and any(name==s or name.startswith(s+'/') for s in surfaces):
   old=hashlib.sha256(t.extractfile(member).read()).hexdigest();cur=ROOT/name
   if not cur.is_file(): ar['missing_current'].append(name)
   elif old==sha(cur): ar['matching'].append(name)
   else: ar['different'].append({'path':name,'saved_sha256':old,'current_sha256':sha(cur)})
ar['sha256_after']=sha(a);save('r2-bytes.json',ar)
r=read(C/'input-rules.json');current=read(P/'inputs/stellarator_plant_params.json');old=r['default_values'];selected={**old,**r['forward_overrides']}
save('controls.json',{'current_count':len(current),'r2_count':len(old),'new_current_keys':{k:current[k] for k in current.keys()-old.keys()},'removed_current_keys':sorted(old.keys()-current.keys()),'changed_defaults':{k:{'r2_default':old[k],'current_default':current[k],'r2_selected':selected[k]} for k in old.keys()&current.keys() if old[k]!=current[k] or selected[k]!=current[k]},'r2_defaults_hash':r['defaults_sha256'],'current_defaults_hash':sha(P/'inputs/stellarator_plant_params.json'),'forward_overrides':r['forward_overrides'],'independent_inputs':r['independent_reference_inputs'],'conditioned_seams':r['conditioned_seams']})
b=read(ROOT/'work/analysis/20260919-201643_stellarator-integrated-depth-reassessment.evidence/baseline_result.json');mm=read(C/'manifest.json');known={x['channel_name'] for x in m['outputs']}; quantities=mm['quantities']; entries=m['constraint_catalog']['concrete_entries']
verification=read(ROOT/'exploration/stellarator_e2e/studies/20260919-cost-estimate-maturity-and-uncertainty/results/verification_summary.json')
save('mapping.json',{'manifest_rows':len(quantities),'accounting_equations':mm['accounting'],'missing_producers':[{'id':q['id'],'producers':q['producers'],'missing':[p for p in q['producers'] if p not in known]} for q in quantities if any(p not in known for p in q['producers'])],'empty_producers':[q['id'] for q in quantities if not q['producers']],'predicates':entries,'baseline_verdicts':b['verdicts'],'engineering_diagnostic_channels':{k:v for k,v in b['channels'].items() if any(w in k for w in ['cycle_interface','coil_life','margin','_ok'])},'not_independently_verified':verification['not_independently_verified'],'quantity_inventory':quantities})
print(json.dumps({'identity':{k:v for k,v in identity.items() if k!='all_inputs'},'read_set':{k:v for k,v in coverage.items() if k!='reads'},'r2':{'hash':ar['sha256_after'],'same':len(ar['matching']),'different':len(ar['different'])},'inputs':{'current':len(current),'old':len(old)},'mapping':{'rows':len(quantities),'constraints':len(entries)}}))
# Distinguish entry parameters and verdict channels from numeric outputs when mapping.
from exploration.stellarator_e2e.studies import oracle_entry
known.update(x['qualified_name'] for x in m['parameters']);known.update(x['evaluation_channel'] for x in entries)
mp=read(OUT/'mapping.json');mp['missing_producers']=[{'id':q['id'],'missing':[p for p in q['producers'] if p not in known]} for q in quantities if any(p not in known for p in q['producers'])]
mp['unmapped_numeric_outputs']=sorted(set(b['channels'])-set(oracle_entry.ORACLE_OUTPUT_TO_CHANNEL.values()))
mp['oracle_mapping_count']=len(set(b['channels'])&set(oracle_entry.ORACLE_OUTPUT_TO_CHANNEL.values()))
mp['not_independently_verified_field_caution']='The generic verifier field is empty but does not enumerate unmapped native outputs; the explicit set difference does.'
spec=importlib.util.spec_from_file_location('scope_export',C/'export_model_values.py');export=importlib.util.module_from_spec(spec);spec.loader.exec_module(export)
native={'state':'completed','run_kind':'diagnostic','outputs':b['channels'],'requested_overrides':b['point'],'verdicts':{q['constraint_id']:q['status'] for q in b['verdicts']}}
ex=export.extract(mm,m,native);save('current-baseline-export.json',ex)
mp['current_export_statuses']={k:sum(q['status']==k for q in ex['quantities']) for k in set(q['status'] for q in ex['quantities'])}
vals={q['id']:q['model_value'] for q in ex['quantities']};eq=[]
for e in mm['accounting']:
 pv=vals.get(e['parent']);cv=[vals.get(k) for k in e['children']];eq.append({'id':e['id'],'parent':e['parent'],'residual':None if pv is None or None in cv else pv-sum(cv)})
mp['r2_equations_on_retained_current_baseline']=eq
save('mapping.json',mp)
print(json.dumps({'missing_producers':mp['missing_producers'],'unmapped_count':len(mp['unmapped_numeric_outputs']),'mapped_count':mp['oracle_mapping_count'],'export_statuses':mp['current_export_statuses'],'equations':eq}))
