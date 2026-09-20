"""Record exact native default-case deltas; overlap hypotheses are diagnostic only."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
old=json.loads((ROOT/'work/active/WI-071_shared-fabrication-rate-for-estimate-uncertainty/evidence/baseline.json').read_text())['outputs']
new=json.loads((HERE/'baseline.json').read_text())['outputs']
P='stellarator_09__stellaris__'
keys=['pb__p_th','pb__p_et','pb__p_net','pb__rec_frac','heat_transport__primary_loop__p_pump_total','overnight_capital__overnight_capital','lcoe_calc__lcoe','lcoe_1cfe_calc__lcoe']
result={key:{'before':old[P+key],'after':new[P+key],'delta':new[P+key]-old[P+key]} for key in keys}
result['gross_efficiency']={'before':old[P+'turbine__cycle__eta_th'],'after':new[P+'turbine__matched_cycle__eta_gross']}
loads=new[P+'turbine__matched_cycle__p_cycle_pumps_MW']+new[P+'heat_rejection__cooling_water__p_cooling_pump_electric_MW']
result['new_explicit_pumps_MW']=loads
result['unchanged_subsystem_fraction']=.03
result['subsystem_allowance_MW']={'before':old[P+'pb__p_et']*.03,'after':new[P+'pb__p_et']*.03}
result['overlap_hypotheses']=[{'assumed_overlap_fraction':f,'assumed_overlap_MW':f*loads,'hypothetical_net_MW':new[P+'pb__p_net']+f*loads,'fixed_cost_model_lcoe_USD_MWh':new[P+'lcoe_calc__lcoe']*new[P+'pb__p_net']/(new[P+'pb__p_net']+f*loads)} for f in [0,.5,1]]
result['overlap_caveat']='Diagnostic hypotheses, not qualified uncertainty or adopted corrections. Costs and other loads fixed; main model retains full 3% allowance plus explicit pumps. Unknown scope overlap remains.'
result['scope']='Raw default plant; unchanged source heat and helium/salt conditions. Lower gross power changes retained gross-scaled capital drivers. Steam generator/reheater/cooling capacity and installed cost remain unqualified.'
(HERE/'result-delta.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
