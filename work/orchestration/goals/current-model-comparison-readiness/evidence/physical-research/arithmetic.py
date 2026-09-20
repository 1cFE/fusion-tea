"""Research arithmetic only: no plant prediction or model implementation."""
import json,math,pathlib,hashlib
p=pathlib.Path(__file__).parent
eta=lambda t:.1802*math.log(t+273)-.7823
dT_pump=9.80665*40/(.75*1560)
cold=270-dT_pump
qfractions=[.89/4.24,2.67/4.24,.68/4.24]
bounds=[cold,cold+(465-cold)*qfractions[0],465-(465-cold)*qfractions[2],465]
result={'status':'conditional research arithmetic; no steam property solution or native plant evaluation','eta_by_steam_C':{str(t):eta(t) for t in [480,465,455,445,435,427]},'pump_temperature_rise_K':dT_pump,'SG_return_C':cold,'IHX_cold_in_C':270,'SG_salt_span_K':465-cold,'SG_hot_margin_at445_K':20,'IHX_hot_margin_default500_K':35,'IHX_hot_margin_scenario520_K':55,'minimum_economizer_heat_fraction_for_20K_pinch_at62bar':(277.733+20-cold)/(465-cold),'source_duty_fractions':qfractions,'illustrative_salt_breakpoints_C_using_source_fractions':bounds,'illustrative_terminal_gaps_K_at_feed171_sat277733_steam445':[bounds[0]-171,bounds[1]-277.733,bounds[2]-277.733,bounds[3]-445],'warning':'Source heat fractions belong to a conflicting source temperature diagram. Illustrative gaps are NOT a thermodynamically solved or accepted candidate.'}
(p/'arithmetic.json').write_text(json.dumps(result,indent=2)+'\n')
files=['models/library/analyses/mfe_power_cycle.sysml','models/library/analyses/mfe_primary_loop.sysml','models/designs/generic_mfe/mfe_subsystems.sysml','models/designs/generic_mfe/mfe_plant.sysml','models/designs/stellarator_09/stellarator_plant.sysml','exploration/stellarator_e2e/generated/handwritten/mfe_cooling_equipment/cooling_equipment_impl.py','knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md','knowledge/sources/mcdonnell_douglas_1979_small_power_system_volume5/output.md','knowledge/sources/nistir5078_table2_water_saturation_pressure/output.md','work/orchestration/goals/plant-closure/evidence/grounding_sources/kovari2016_p9_table4.png']
files += [str(x) for x in p.glob('*.png')]
(p/'evidence-hashes.json').write_text(json.dumps({f:hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest() for f in files},indent=2)+'\n')
print(json.dumps(result,indent=2))
