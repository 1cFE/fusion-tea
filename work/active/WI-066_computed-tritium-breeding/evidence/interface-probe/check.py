"""Read-only checks on native generation products; no scientific implementation claim."""
import json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
old=yaml.safe_load((HERE/'entering-pipeline.yaml').read_text())['modules']
new=yaml.safe_load((HERE/'production-pipeline.yaml').read_text())['modules']
probe=yaml.safe_load((HERE/'subtype-pipeline.yaml').read_text())['modules']
assert 'probe__held__blanket__breeding' not in probe
assert probe['probe__held__fuel_cycle__fuel']['inputs']['achieved']=='float probe_params.probe__held__blanket__tbr'
assert probe['probe__stellaris__fuel_cycle__fuel']['inputs']['achieved']=='float probe__stellaris__blanket__breeding__total'
P='stellarator_09__stellaris__'
breeding=new[P+'blanket__breeding']
expected={'blanket_t_in':'blanket__blanket_t','R_in':'plasma__R','a_in':'plasma__a','kappa_in':'plasma__kappa','vacuum_t_in':'blanket__first_wall__vacuum_t','firstwall_t_in':'blanket__first_wall__firstwall_t','reflector_t_in':'blanket__reflector_t','ht_shield_t_in':'shield__ht_shield_t','structure_t_in':'structure__structure_t','gap1_t_in':'vessel__gap1_t','vessel_t_in':'vessel__vessel_t'}
for k,v in expected.items():
    assert breeding['inputs'][k]=='float stellarator_plant_params.'+P+v,(k,breeding['inputs'][k])
assert new[P+'fuel_cycle__fuel']['inputs']['tbr_available_in']=='float '+P+'blanket__breeding__tbr_mean'
key=P+'tbr_ok__2cd198f674d413e4'
assert key in old and key in new
assert new[key]['inputs']=={'defined_in':'float '+P+'breeding_adequacy__defined_flag','numerical_margin_in':'float '+P+'breeding_adequacy__numerical_margin'}
old_constraints=[k for k,v in old.items() if v.get('module_type','').endswith('ConstraintModule')]
new_constraints=[k for k,v in new.items() if v.get('module_type','').endswith('ConstraintModule')]
assert set(old_constraints)==set(new_constraints)
# Definitions and wires must remain byte-identical across canonical and exploration copies.
pairs=[('library/analyses/mfe_tritium_breeding.sysml','analyses/mfe_tritium_breeding.sysml'),('library/structure/mfe_plant_systems.sysml','structure/mfe_plant_systems.sysml'),('designs/generic_mfe/mfe_subsystems.sysml','designs/generic_mfe/mfe_subsystems.sysml'),('designs/stellarator_09/stellarator_plant.sysml','designs/stellarator_09/stellarator_plant.sysml')]
for canonical,twin in pairs:
    assert (ROOT/'models'/canonical).read_bytes()==(ROOT/'exploration/stellarator_e2e/models'/twin).read_bytes(),canonical
report={'generic_held_input_preserved':True,'no_phantom_held_breeding_occurrence':True,'geometry_bindings':expected,'fuel_uses_computed_tbr':True,'constraint_identity':key,'constraint_count_before':len(old_constraints),'constraint_count_after':len(new_constraints),'new_modules':sorted(set(new)-set(old)),'twins_identical':True,'numerical_implementation_executed':False}
Path(__file__).with_name('checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
