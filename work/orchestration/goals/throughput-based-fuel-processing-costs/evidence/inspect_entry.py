"""Read retained upstream evidence and establish unchanged producer files."""
import json, subprocess
from pathlib import Path
root=Path.cwd()
here=Path(__file__).resolve().parent
record=root/'exploration/stellarator_e2e/studies/20260919-fuel-inventory-and-startup/results/baseline_result.json'
base=json.loads(record.read_text())
paths=['models','exploration/stellarator_e2e/models','exploration/stellarator_e2e/generated','exploration/stellarator_e2e/oracle_fuel_inventory.py','exploration/stellarator_e2e/verify_stellaris.py','exploration/stellarator_e2e/studies/oracle_entry.py']
diff=subprocess.run(['git','diff','--exit-code','956444b5','--',*paths],capture_output=True,text=True)
assert diff.returncode==0, diff.stdout
prefix='stellarator_09__stellaris__'
keys=['fuel_cycle__fuel_handling__cost','fuel_cycle__fuel_calc__annual_fuel','fuel_cycle__inventory__exhaust_kg_day','fuel_cycle__inventory__dt_processor_kg_day','fuel_cycle__inventory__production_kg_s','fuel_cycle__inventory__extracted_kg_s','fuel_cycle__inventory__startup_conservative_kg','fuel_cycle__inventory__defined_flag','lcoe_calc__lcoe','lcoe_1cfe_calc__lcoe']
result={'checkout':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'producer_model':'956444b5d440238857911a0406e6d3f51ddcbf2e','producer_paths_unchanged':paths,'retained_native_record':str(record.relative_to(root)),'values':{key:base['channels'][prefix+key] for key in keys},'note':'Retained upstream native results, not a new study. Current producer continuity plus fresh entering-fuel-tests.log verifies reuse.'}
(here/'entering-evidence.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
