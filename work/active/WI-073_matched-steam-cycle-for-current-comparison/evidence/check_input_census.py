"""Check bound cycle states against the actual source-derived entry census."""
import json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
current=json.loads((ROOT/'tests/models/data/mfe_census.json').read_text())
prior=json.loads(subprocess.check_output(['git','show','9e07184f1301ad0d4ebdba5ae9bbe5fa97f1f1ef:tests/models/data/mfe_census.json'],cwd=ROOT))
flatten=lambda c:set().union(*(set(v) for v in c['by_entry_type'].values()))
a,b=flatten(prior),flatten(current)
added=sorted(b-a);removed=sorted(a-b)
assert len(a)==490 and len(b)==511 and len(added)==21 and not removed
suffixes=['heat_transport__salt_hot_C','heat_transport__salt_cp_kJ_kgK','turbine__matched_cycle_enabled','turbine__pump_motor_efficiency','turbine__main_steam_generator__pressure_MPa','turbine__main_steam_generator__outlet_temperature_C','turbine__reheater__outlet_temperature_C','turbine__hp_turbine__efficiency','turbine__lp_turbine__efficiency','turbine__open_feedwater_heater__pressure_MPa','turbine__condenser__temperature_C','turbine__condensate_pump__efficiency','turbine__feedwater_pump__efficiency','turbine__generator__mechanical_efficiency','turbine__generator__generator_efficiency','heat_rejection__cooling_water_enabled','heat_rejection__water_inlet_C','heat_rejection__water_outlet_C','heat_rejection__circulating_water_pump__head_m','heat_rejection__circulating_water_pump__efficiency','heat_rejection__circulating_water_pump__motor_efficiency']
expected={'stellarator_09__stellaris__'+s for s in suffixes}
assert set(added)==expected,(set(added)-expected,expected-set(added))
(HERE/'input-census-check.json').write_text(json.dumps({'prior_commit':'9e07184f1301ad0d4ebdba5ae9bbe5fa97f1f1ef','prior_count':len(a),'current_count':len(b),'added':added,'removed':removed,'exact_designed_input_set':True,'no_calculated_state_or_bound_heat_entry':True,'semantic_fingerprint':current['derived_against_semantic_fingerprint']},indent=2)+'\n')
print('PASS 21 explicit design inputs; no new state or bound heat entries')
