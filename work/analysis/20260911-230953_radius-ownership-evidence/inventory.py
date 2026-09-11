"""Capture current generated contract identities and exact source/input consumers."""
import hashlib,json
from pathlib import Path
import yaml
ROOT=Path.cwd(); HERE=Path(__file__).resolve().parent; pkg=ROOT/'exploration/stellarator_e2e/generated'; P='stellarator_09__stellaris__'
c=json.loads((pkg/'contracts/model_contract.json').read_text()); pc=json.loads((pkg/'contracts/package_contract.json').read_text()); pipe=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text())
rows={}
for key in [P+'R',P+'magnet__R0']:
 needle='float stellarator_plant_params.'+key
 rows[key]=[{'module':n,'formal':f} for n,m in pipe['modules'].items() for f,v in m.get('inputs',{}).items() if v==needle]
paths=['models/designs/generic_mfe/mfe_plant.sysml','models/designs/stellarator_09/stellarator_plant.sysml','models/library/analyses/mfe_plasma_scaling.sysml','models/library/analyses/mfe_magnet_field.sysml','models/library/cost_structure/mfe_power_core.sysml','exploration/stellarator_e2e/verify_stellaris.py','exploration/stellarator_e2e/studies/oracle_entry.py','exploration/stellarator_e2e/studies/study_route.py','exploration/stellarator_e2e/studies/manifest.json','tests/models/data/mfe_census.json']
out={'semantic_fingerprint':c['semantic_fingerprint'],'executable_fingerprint':pc['executable_fingerprint'],'parameter_count':len(c['parameters']),'constraint_count':len(c['constraint_catalog']['concrete_entries']),'exact_consumers':rows,'source_hashes':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'reference_parameters':[p for p in c['parameters'] if any(s in p['qualified_name'] for s in ['__R_ref','__a_coil_ref','__wall_peak_R_ref'])]}
(HERE/'inventory.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
