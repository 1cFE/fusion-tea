"""Check unchanged protected evidence and retain exact repair provenance; fresh --out only."""
import argparse,difflib,hashlib,json,os,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[4];E=Path(__file__).resolve().parent;H=R/'exploration/component_alternatives';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if a.out.exists():raise FileExistsError(a.out)
 before=json.loads((E/'preservation-before.json').read_text());differences=[]
 for name,old in before['protected'].items():
  p=R/name
  if old['kind']=='file':new=dict(kind='file',sha256=sha(p)) if p.is_file() else None
  else:new=dict(kind='symlink',sha256=hashlib.sha256(os.readlink(p).encode()).hexdigest()) if p.is_symlink() else None
  if new!=old:differences.append(dict(path=name,before=old,after=new))
 oldbuild=json.loads((E.parent/'evidence/build-hashes.json').read_text());newbuild=json.loads((E/'build/build-hashes.json').read_text())
 assert oldbuild['sources']==newbuild['sources']
 changed=[k for k,v in before['package_files'].items() if sha(H/'component_alternatives_tea'/k)!=v['live']]
 expected=['contracts/package_contract.json','handwritten/component_alternatives_thermal/finite_water_cooler_impl.py','handwritten/integrated_heat_electricity/network_heat_driven_closure_impl.py','handwritten/loop_return_control/primary_bypass_control_impl.py']
 assert sorted(changed)==sorted(expected),changed
 contract='exploration/component_alternatives/component_alternatives_tea/contracts/package_contract.json'
 old_contract=json.loads(subprocess.check_output(['git','show','49c20e69:'+contract],cwd=R,text=True));new_contract=json.loads((R/contract).read_text())
 for key in old_contract:
  if key not in ('executable_fingerprint','artifact_hashes'):
   assert old_contract[key]==new_contract[key],key
 origins={'integrated_heat_electricity/network_heat_driven_closure_impl.py':R/'exploration/aries_integrated/aries_integrated/handwritten/integrated_heat_electricity/network_heat_driven_closure_impl.py',
 'loop_return_control/primary_bypass_control_impl.py':R/'exploration/costed_loop_brayton/bodies/loop_return_control/primary_bypass_control_impl.py'}
 provenance=[]
 for rel,origin in origins.items():
  variant=H/'bodies'/rel
  retained=next(r for r in oldbuild['completions'] if r['source']==str(origin.relative_to(R)))
  assert sha(origin)==retained['source_sha256']
  provenance.append(dict(original=str(origin.relative_to(R)),original_sha256=sha(origin),variant=str(variant.relative_to(R)),variant_sha256=sha(variant),diff=''.join(difflib.unified_diff(origin.read_text().splitlines(True),variant.read_text().splitlines(True),fromfile=str(origin.relative_to(R)),tofile=str(variant.relative_to(R))))))
 cooler='exploration/component_alternatives/bodies/component_alternatives_thermal/finite_water_cooler_impl.py';old=subprocess.check_output(['git','show','49c20e69:'+cooler],cwd=R,text=True)
 provenance.append(dict(original='git:49c20e69:'+cooler,original_sha256=hashlib.sha256(old.encode()).hexdigest(),variant=cooler,variant_sha256=sha(R/cooler),diff=''.join(difflib.unified_diff(old.splitlines(True),(R/cooler).read_text().splitlines(True),fromfile='49c20e69:'+cooler,tofile=cooler))))
 result=dict(protected_entries=len(before['protected']),protected_differences=differences,original_package_files=len(before['package_files']),changed_package_files=changed,unchanged_model_sources=len(newbuild['sources']),old_study_snapshot_unchanged=sha(H/'studies/20260926-design-study-component-alternatives/snapshot.json')==before['old_snapshot_sha256'],provenance=provenance)
 a.out.write_text(json.dumps(result,indent=2)+'\n');assert not differences,differences
 print(json.dumps({k:v for k,v in result.items() if k!='provenance'}))
if __name__=='__main__':main()
