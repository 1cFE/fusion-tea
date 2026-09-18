"""Package numerically accepted nodes for independent review, without production edits."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
validation=json.loads((HERE/'table-validation.json').read_text())
if validation['status']!='PASS':
    raise RuntimeError('Numerical validation/precision incomplete')
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
records={}
for row in validation['nodes']+validation['withheld']:
    for rel in row['run_paths']:
        p=HERE/rel
        records[rel]=digest(p)
        records[str(p.with_name('manifest.json').relative_to(HERE))]=digest(p.with_name('manifest.json'))
for name in ['table-plan.json','table-freeze.md','table-validation.json','material-cards.json','data-manifest-extra.json','source-verification.json','geometry-verification.json','opening-verification.json','inventory-verification.json','tally-verification.json']:
    records[name]=digest(HERE/name)
for p in sorted(HERE.glob('*refinement*plan*.json')):
    records[p.name]=digest(p)
records['../runtime/data-manifest.json']=digest(HERE.parent/'runtime/data-manifest.json')
records['../runtime/package-manifest.json']=digest(HERE.parent/'runtime/package-manifest.json')
data_records=json.loads((HERE.parent/'runtime/data-manifest.json').read_text())+json.loads((HERE/'data-manifest-extra.json').read_text())
data_digest=hashlib.sha256(json.dumps(sorted(data_records,key=lambda x:x['nuclide']),sort_keys=True,separators=(',',':')).encode()).hexdigest()
response={
 'status':'Numerical release candidate; independent review and physical acceptance are separate',
 'fixed_geometry':{'R_in':12.7,'a_in':1.3,'kappa_in':1.,'vacuum_t_in':.1,'firstwall_t_in':.05,'reflector_t_in':.2,'ht_shield_t_in':.2,'structure_t_in':.15,'gap1_t_in':.1,'vessel_t_in':.1},
 'nodes':[{k:row[k] for k in ['thickness_m','tbr_li6','tbr_li7','std_error']} for row in validation['nodes']],
 'interpolation_allowance':.01,'statistical_multiplier':2.,
 'domain':{'breeder_thickness_m':[.6,1.],'li6_atom_fraction':.7,'extrapolation':False,'interpolation':'piecewise linear','statistical_variance':'sum of squared interpolation weights times independent node variances'},
 'scenario':{'id':'hcll-toroidal-single-window-uniform-773K-endfb8',
   'lithium_atom_fraction_in_PbLi':.158,'li6_atom_fraction_within_lithium':.7,
   'source':{'energy_eV':14.06e6,'spatial':'uniform per physical plasma volume with exact toroidal Jacobian','angular':'isotropic'},
   'opening':{'type':'one contiguous toroidal window','angle_degrees':10.8,'removed_volume_fraction':.03,'voided_layers':['breeder','reflector','ht_shield'],'retained_layers':['firstwall','structure','vessel'],'qualification':'declared conceptual opening; not actual port/divertor reconstruction'},
   'materials':json.loads((HERE/'material-cards.json').read_text()),
   'cross_section_temperature_method':'OpenMC interpolation between bracketing available temperatures at 773.15 K',
   'geometry':'concentric circular-average finite tori; transmitting outer vessel, exterior void, enclosing 20 m vacuum sphere',
   'recoverability':'Li6+Li7 tritium production in breeder only; structural production excluded',
   'cost_convention':'unchanged full-shell cost volumes include the 3% voided inventory; conservative inventory-cost scenario if retained by consumer'},
 'provenance':{'openmc_version':'0.15.2','nuclear_data':'ENDF/B-VIII.0 NNDC processed HDF5','data_repository_commit':'466ab3042f70e60b693fbbd3f6f15f30dba7cd1d','data_set_sha256':data_digest,'data_digest_encoding':'SHA256 of JSON concatenated manifests sorted by nuclide, sorted object keys, compact separators','evidence_root':str(HERE.relative_to(HERE.parents[6])),'sha256':records,'node_aggregation':validation['nodes'],'withheld_checks':validation['checks']},
 'limits':['Numerical lower estimate is not a physical confidence bound.','Material/source/opening alternatives can change adequacy.','Shaped-stellarator geometry and actual outer-component backscatter are not validated.','Experimental benchmark acceptance is recorded independently.']}
(HERE/'response-candidate.json').write_text(json.dumps(response,indent=2)+'\n')
print('Wrote',HERE/'response-candidate.json')
