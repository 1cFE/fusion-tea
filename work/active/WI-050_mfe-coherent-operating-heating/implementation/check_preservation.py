from pathlib import Path
import subprocess,json,hashlib
root=Path.cwd();h=root/'work/active/WI-050_mfe-coherent-operating-heating/implementation'
paths=['work/active/WI-050_mfe-coherent-operating-heating/prototype','work/active/WI-050_mfe-coherent-operating-heating/prototype-r1','work/active/WI-050_mfe-coherent-operating-heating/review.md','work/active/WI-050_mfe-coherent-operating-heating/review-r1.md','work/orchestration/goals','work/analysis','exploration/stellarator_e2e/studies','tests/study','models/designs/hif_ife','exploration/hif_ife_e2e/models']
summary={}
for path in paths:
 diff=subprocess.check_output(['git','diff','--name-only','HEAD','--',path],text=True)
 assert not diff,(path,diff);summary[path]='unchanged against entering production HEAD'
# Same exact tracked identity list and hashes for all family/shared sources outside five owned edits.
import sys;sys.path.insert(0,str(root))
from tests.model_families import FAMILIES,canonical_path
edited={'analyses/mfe_heating_chain.sysml','analyses/mfe_divertor_heat.sysml','analyses/mfe_power_balance.sysml','designs/generic_mfe/mfe_plant.sysml','designs/stellarator_09/stellarator_plant.sysml'}
for family in FAMILIES.values():
 for logical in family.owned:
  if logical in edited:continue
  for path in [canonical_path(logical),family.twin/logical]:
   rel=path.relative_to(root);before=subprocess.check_output(['git','show','546218a5:'+str(rel)])
   assert path.read_bytes()==before,rel
summary['family_isolation']='Every canonical and twin file outside the exact five MFE edits equals revision546218a5; no ownership mapping change.'
summary['study_consumer_checks']='Four named current study consumer modules intentionally deferred to separately certified package migration.'
(h/'preservation.json').write_text(json.dumps(summary,indent=2)+'\n')
print('PASS historical, IFE/shared and study source preservation')
