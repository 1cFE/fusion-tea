"""Scoped native trace additions; existing declaration rows remain historical facts."""
import subprocess
from pathlib import Path
h=Path(__file__).resolve().parent
entries=[
('Divertor Heat Ledger.p_installed_coupled_in','models/library/analyses/mfe_divertor_heat.sysml','attribute','models/library/analyses/mfe_heating_chain.sysml:4','Installed ceiling separated from operating heat; MR-WI050-3/9.'),
('MFE Power Plant.operating_heat','models/designs/generic_mfe/mfe_plant.sysml','calc','models/library/analyses/mfe_heating_chain.sysml:83','One signed operating producer for source heat, loop, power balance and divertor; MR-WI050-1/3/7/9.'),
('stellaris.p_operating_coupled_heat','models/designs/stellarator_09/stellarator_plant.sysml','attribute','models/library/analyses/mfe_plasma_sustainment.sysml:4','Pure exposure of signed sustained demand; no new public demand parameter; MR-WI050-1/2/7.'),
('MFE Power Plant.operating_heat_consumers','models/designs/generic_mfe/mfe_plant.sysml','binding','models/library/analyses/mfe_power_balance.sysml:4','Operating source, loop and thermal/electrical balances; installed delivered procurement preserved; MR-WI050-3/4/6.')]
with (h/'trace-commands.log').open('w') as log:
 for element,file,kind,loc,assumptions in entries:
  cmd=['.codex-test/run','agentic-mbse','pm','trace-element','--element',element,'--file',file,'--type',kind,'--source-type','model','--source-doc','Existing MFE heating and sustainment definitions','--source-location',loc,'--confidence','Medium','--assumptions',assumptions]
  log.write(repr(cmd)+'\n');log.flush()
  subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
