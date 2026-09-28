"""Reconstruct four frozen arithmetic kernels; never execute a plant/reference run."""
from __future__ import annotations
import ast, hashlib, json, math, tarfile
from pathlib import Path
from types import SimpleNamespace
import yaml
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
PREP=ROOT/'.project/active/aries-comparison-preparation/post-reveal-preparation'
RUN=ROOT/'.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1'
P='stellarator_09__stellaris__'
G='exploration/stellarator_e2e/generated/'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(p):return json.loads(p.read_text())
freeze=load(PREP/'package/freeze-record.json');archive=PREP/'package'/freeze['archive']
assert sha(archive.read_bytes())==freeze['sha256']
result=load(RUN/'attempts/first-forward/result.json');v=result['effective_inputs'];roles=result['input_roles']
assert result['outputs']=={} and result['verdicts']=={}
assert len(v)==704 and len(result['requested_overrides'])==3
with tarfile.open(archive) as t:
 def read(path):return t.extractfile(path).read()
 identity=json.loads(read(str(PREP.relative_to(ROOT)/'tools/identity.json')))
 files=[G+'pipelines/pipeline.yaml',G+'handwritten/mfe_magnet_field/winding_operating_state_impl.py',G+'handwritten/mfe_magnet_field/coil_set_axis_field_impl.py',G+'handwritten/mfe_plasma_scaling/mfe_radial_build_impl.py',G+'handwritten/mfe_plasma_scaling/conductor_peak_field_impl.py','models/library/analyses/mfe_magnet_field.sysml','models/library/analyses/mfe_plasma_scaling.sysml','models/library/cost_structure/mfe_power_core.sysml','models/designs/generic_mfe/mfe_plant.sysml']
 blobs={p:read(p) for p in files}
 for p,b in blobs.items():assert sha(b)==identity['files'][p] and sha((ROOT/p).read_bytes())==sha(b),p
 nodes=yaml.safe_load(blobs[G+'pipelines/pipeline.yaml'])['modules']
 def kernel(path,name):
  # Only the named arithmetic function is compiled; imports and pipeline execution are excluded.
  function=next(n for n in ast.parse(blobs[G+'handwritten/'+path]).body if isinstance(n,ast.FunctionDef) and n.name==name)
  function.returns=None
  for arg in function.args.args:arg.annotation=None
  tree=ast.Module(body=[function],type_ignores=[]);namespace={'math':math};exec(compile(tree,path,'exec'),namespace);return namespace[name]
 bindings={}
 def inputs(node,upstream={}):
  bound={}
  for formal,ref in nodes[P+node]['inputs'].items():
   key=ref.split(' ',1)[1]
   if key.endswith('.root'):key=key[:-5]
   if key.startswith(P):bound[formal]=upstream[key]
   else:bound[formal]=v[key.split('.',1)[1]]
   bindings[node+'.'+formal]={'binding':ref,'value':bound[formal]}
  return bound
 winding=kernel('mfe_magnet_field/winding_operating_state_impl.py','calculate')(inputs('magnet__winding_state'))
 up={P+'magnet__winding_state__I_coil':winding['I_coil']}
 axis_inputs=inputs('magnet__field_calc',up);axis=kernel('mfe_magnet_field/coil_set_axis_field_impl.py','run_coil_set_axis_field')(SimpleNamespace(**axis_inputs))
 radial_inputs=inputs('rb');radial=kernel('mfe_plasma_scaling/mfe_radial_build_impl.py','run_mfe_radial_build')(SimpleNamespace(**radial_inputs));coil_radius=radial[3]
 up.update({P+'magnet__field_calc__B_axis':axis,P+'rb__r_coil_centre':coil_radius})
 peak_inputs=inputs('magnet__peak_field_calc',up);peak_kernel=kernel('mfe_plasma_scaling/conductor_peak_field_impl.py','run_conductor_peak_field');peak=peak_kernel(SimpleNamespace(**peak_inputs))
 layers=[];radius=radial_inputs['a_in']
 for key in ('vacuum_t_in','firstwall_t_in','blanket_t_in','reflector_t_in','ht_shield_t_in','structure_t_in','gap1_t_in','vessel_t_in'):
  radius+=radial_inputs[key];layers.append({'layer':key,'thickness_m':radial_inputs[key],'outer_radius_m':radius})
 R=peak_inputs['R_in'];Rref=peak_inputs['R_ref_in'];aref=peak_inputs['a_coil_ref_in'];ratio=peak_inputs['peak_ratio_in']
 bore=R/(R-coil_radius);bore_ref=Rref/(Rref-aref)
 independent_peak=(axis*ratio)*(bore/bore_ref);assert peak==independent_peak==56.61785714285713
 assert str(peak) in json.dumps(result['native_failure_records'])
 # Reduced identity independent of evaluated axis multiplication ordering.
 reduced=24.9*(Rref-aref)/(R-coil_radius);assert math.isclose(reduced,peak,rel_tol=1e-15)
 ref_ratio=(coil_radius/R)/(aref/Rref)
 # Algebra only: the missing full Eq39 bracket is not fitted or assigned.
 wp=v[P+'magnet__winding_pack__wp_side'];pack_area=wp*wp
 paths=set()
 for record in bindings.values():
  key=record['binding'].split(' ',1)[1]
  if not key.startswith(P):paths.add(key.split('.',1)[1])
 relevant={k:{'value':v[k],'role':roles[k]} for k in sorted(paths)}
 receipt={'kind':'isolated frozen arithmetic diagnostic; not native plant outputs','archive_sha256':freeze['sha256'],'attempt_result_sha256':sha((RUN/'attempts/first-forward/result.json').read_bytes()),'source_files_sha256':{p:sha(b) for p,b in blobs.items()},'native_outputs_remain_empty':True,'native_verdicts_remain_empty':True,'inputs':relevant,'bindings':bindings,'layers':layers,'intermediates':{'reference_turns':v[P+'magnet__coil__reference_turns'],'turn_current_A':v[P+'magnet__coil__turn_current'],'I_coil_Aturn':winding['I_coil'],'pack_side_m':wp,'pack_area_m2':pack_area,'j_wp_effective_A_per_mm2':winding['j_wp_effective'],'n_coils':axis_inputs['n_coils'],'B_axis_T':axis,'a_coil_m':coil_radius,'R_m':R,'live_clearance_m':R-coil_radius,'reference_clearance_m':Rref-aref,'bore_factor':bore,'reference_bore_factor':bore_ref,'normalized_bore_factor':bore/bore_ref,'peak_ratio_reference':ratio,'peak_over_axis_effective':ratio*bore/bore_ref,'B_peak_T':peak,'reduced_identity_T':reduced,'R_over_Rref':R/Rref,'coil_radius_over_reference':coil_radius/aref,'coil_aspect_change_factor':ref_ratio,'plasma_aspect':R/v[P+'plasma__a'],'plasma_aspect_reference':12.7/1.3,'R_over_pack_side':R/wp,'Rref_over_pack_side':Rref/wp},'checks':{'exact_reported_value_reconstructed':True,'frozen_and_live_files_identical':True,'independent_reduced_identity_relative_tolerance':1e-15,'peak_kernel_has_no_pack_area_input':'wp_side' not in peak_inputs and 'A_wp' not in peak_inputs},'unidentified_eq39_factor':'(1-lambda)+lambda*(R/R_ref)*(sqrt(A_wp_ref)/sqrt(A_wp)); lambda unknown; assumes same C, itself unestablished','scientific_status':'axis and peak field unqualified at changed geometry; retained values are implementation diagnostics, not validated predictions'}
(HERE/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt['intermediates'],indent=2))
