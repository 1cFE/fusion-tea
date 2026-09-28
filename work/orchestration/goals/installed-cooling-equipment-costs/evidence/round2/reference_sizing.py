"""Conditional conceptual specifications from retained executed requirements; no equipment price."""
import json
import math
from pathlib import Path
H=Path(__file__).resolve().parent
rows=json.loads((H.parent/'starting-cases.json').read_text())['cases']
P='stellarator_09__stellaris__heat_transport__primary_loop__'
cp=5193.0
gamma=5.0/3.0
R=cp*(gamma-1)/gamma
# Image-checked source OB geometry and temperature terminals, per independent review.
A_ref=2*math.pi*0.01905*11.6*7426
lmtd_ref=(35-19.3)/math.log(35/19.3)
UF=267.8e6/(A_ref*lmtd_ref)
result={'status':'proposed conceptual assumptions; not a selected or priced hardware design','assumptions':{'circulators':'two active equally loaded parallel machines per circuit; topology is AGENT assumption','helium':'ideal gas using current cp and gamma, compressor suction pressure p_loop-dp','IHX':'source OB configuration, fixed effective UF and270/465C secondary terminals; transfer is AGENT assumption, not measured off-design law'},'reference':{'OB_area_m2':A_ref,'OB_lmtd_K':lmtd_ref,'OB_effective_UF_W_m2_K':UF},'cases':[]}
for row in rows:
 q=row['quantities'];v=row['native_channels'];N=q['loops'];dp=v[P+'dp_loop'];Tc=v[P+'T_comp_in'];Th=v[P+'T_out'];mdot=q['flow_per_loop_kg_s'];p_suction=8e6-dp
 rho=p_suction/(R*Tc)
 hot_approach=Th-(465+273.15);cold_approach=Tc-(270+273.15)
 valid=min(hot_approach,cold_approach)>0
 lmtd=(hot_approach-cold_approach)/math.log(hot_approach/cold_approach) if valid and hot_approach!=cold_approach else hot_approach if valid else None
 area=q['IHX_per_loop_MW']*1e6/(UF*lmtd) if valid else None
 result['cases'].append({'case':row['proposal_id'],'circuits':N,'circulators':2*N,'circulator_mass_flow_kg_s':mdot/2,'circulator_pressure_rise_Pa':dp,'circulator_suction_pressure_Pa':p_suction,'circulator_suction_temperature_K':Tc,'ideal_suction_density_kg_m3':rho,'circulator_inlet_volume_m3_s':mdot/(2*rho),'circulator_electric_MW':q['pump_electric_MW']/(2*N),'IHX_count':N,'IHX_duty_MW_each':q['IHX_per_loop_MW'],'IHX_hot_approach_K':hot_approach,'IHX_cold_approach_K':cold_approach,'IHX_terminal_approaches_valid':valid,'IHX_LMTD_K':lmtd,'IHX_conditional_area_m2_each':area,'IHX_conditional_area_m2_total':area*N if area else None})
(H/'reference-sizing.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
for r in result['cases']: print(r)
