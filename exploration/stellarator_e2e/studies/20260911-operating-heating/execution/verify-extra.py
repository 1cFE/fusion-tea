import json,math
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as oracle,study_route as route
from scripts.study import common
H=Path(__file__).resolve().parents[1];R=H/'results';P=route.P
rows=json.loads((R/'cases.json').read_text()); raws={r['candidate_id']:r for r in json.loads((R/'raw-cases.json').read_text())}; channels=json.loads((H/'preparation/required-channels.json').read_text())
inputs={}
for f in (route.PACKAGE_DIR/'inputs').glob('*.json'):inputs.update(json.loads(f.read_text()))
(R/'package-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
checks=[];parity=[];finance=[]
def check(case,name,actual,expected,exact=False):
 checks.append({'proposal_index':case['proposal_index'],'identity':name,'actual':actual,'expected':expected,'residual':actual-expected,'pass':actual==expected if exact else math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-9)})
for r in rows:
 v=r['values'];o=raws[r['candidate_id']]['outputs']; inp={**inputs,**r['inputs']};p=lambda n:float(inp[P+n])
 expected=oracle.evaluate(r['inputs'])
 for name,ch in channels.items():
  dev=common.relative_deviation(o[ch],expected[ch]);parity.append({'proposal_index':r['proposal_index'],'channel':ch,'relative_deviation':dev,'pass':dev<1e-9})
 D=v['p_aux_required']; s=p('eta_source_heat');c=p('eta_couple_heat'); A=3.52/17.58*v['p_fus']
 equations={'operating_heat_coupled':D,'operating_heat_delivered':D/c,'operating_heat_wallplug':D/(c*s),'heat_delivered':s*p('p_wallplug_heat'),'heat_coupled':c*s*p('p_wallplug_heat'),'divheat_p_heat_operating_minus_installed':D-v['heat_coupled'],'q_source':p('mn')*(v['p_fus']-A)+A+D,'loop_mdot':1e6*v['q_source']/(p('loop_cp')*p('loop_dT_blanket')),'loop_mdot_loop':v['loop_mdot']/p('n_loops'),'loop_dp_loop':p('f_loss')*p('dp_loop_ref')*(v['loop_mdot_loop']/p('mdot_loop_ref'))**2,'loop_r_comp':p('loop_p')/(p('loop_p')-v['loop_dp_loop']),'loop_w_fluid':v['loop_mdot']*p('loop_cp')*(p('loop_T_in')-v['loop_T_comp_in'])/1e6,'loop_p_elec':v['loop_w_fluid']/p('eta_drive'),'loop_q_ihx':v['q_source']+v['loop_w_fluid'],'loop_p_pump_total':p('loop_live')*v['loop_p_elec']+p('p_pump_direct'),'loop_q_recovered_total':p('loop_live')*v['loop_w_fluid']+p('eta_p_direct')*p('p_pump_direct'),'p_th':v['q_source']+v['loop_q_recovered_total'],'p_the':v['cycle_eta_th']*v['p_th'],'divheat_p_heat_abs':v['p_alpha_heat']+D,'divheat_p_sep':v['divheat_p_heat_abs']-v['p_rad'],'divheat_p_target_nonrad':v['divheat_p_heat_abs']*(1-p('f_rad_total')),'divheat_q_target_peak':v['divheat_p_target_nonrad']*p('q_target_ref')/p('p_nonrad_ref'),'heating':v['heat_delivered']*5282900}
 for key,val in equations.items():check(r,key,v[key],val)
 check(r,'p_net',v['p_net'],v['p_the']-(p('p_tf')+p('p_pf')+v['loop_p_pump_total']+p('f_sub')*v['p_the']+p('p_trit')+p('p_house')+p('p_tfcool')+p('p_pfcool')+v['p_cryo']+v['operating_heat_wallplug']))
 check(r,'demand balance',D,v['p_rad']+v['W_th']/v['tau_E']-v['p_alpha_heat'])
 d=p('discount_rate');N=int(p('operational_years'));tc=p('construction_years');g=p('inflation_rate');crf=1/sum((1+d)**(-year) for year in range(1,N+1))
 annual_multiplier=crf*sum((1+g)**(tc+year-1)/(1+d)**year for year in range(1,N+1))
 annual=(o[P+'cas71_calc__levelized']+v['cas72_annual']+o[P+'cas80_calc__levelized'])
 check(r,'annual O&M levelization',o[P+'cas71_calc__levelized'],v['annual_om_unlevelized']*annual_multiplier)
 check(r,'annual fuel levelization',o[P+'cas80_calc__levelized'],v['annual_fuel']*annual_multiplier)
 head=v['total_capital']*(1+d)**(tc/2)*crf; comp=(v['overnight_capital']+v['idc_capital'])*crf;energy=8760*v['p_net']*v['calendar_availability']
 check(r,'headline LCOE',v['lcoe'],(head+annual)/energy);check(r,'comparison LCOE',v['lcoe_1cfe'],(comp+annual)/energy)
 finance.append({'proposal_index':r['proposal_index'],'label':r['label'],'capital_head':head,'capital_comparison':comp,'annual':annual,'energy':energy,'total_capital':v['total_capital'],'overnight_capital':v['overnight_capital'],'idc':v['idc_capital'],'cas71':o[P+'cas71_calc__levelized'],'cas72':v['cas72_annual'],'cas80':o[P+'cas80_calc__levelized'],'crf':crf})
base=rows[2];bf=finance[2]
for r,f in zip(rows,finance):
 for kind,channel in [('head','lcoe'),('comparison','lcoe_1cfe')]:
  capital=(f['capital_'+kind]-bf['capital_'+kind])/bf['energy'];annual=(f['annual']-bf['annual'])/bf['energy'];energy=(f['capital_'+kind]+f['annual'])*(1/f['energy']-1/bf['energy'])
  f['bridge_'+kind]={'capital':capital,'annual':annual,'energy':energy,'sum':capital+annual+energy,'delta':r['values'][channel]-base['values'][channel]};check(r,'bridge '+kind,capital+annual+energy,r['values'][channel]-base['values'][channel])
 for key in ['operating_heat_coupled','operating_heat_delivered','operating_heat_wallplug','q_source','p_net','p_th','p_the','loop_mdot','loop_dp_loop','loop_w_fluid','loop_q_recovered_total','cycle_eta_th','divheat_p_heat_abs','divheat_q_target_peak','annual_fuel','cas72_annual','calendar_availability']:
  if r['arm_id']=='arm-reserve':check(r,'reserve invariant '+key,r['values'][key],base['values'][key],exact=True)
 if r['arm_id']!='arm-reserve':check(r,'installed heating invariant',r['values']['heating'],base['values']['heating'],exact=True)
 if r['arm_id']=='arm-retained-alpha':
  check(r,'alpha compensation',r['values']['divheat_p_heat_abs'],base['values']['divheat_p_heat_abs'])
  check(r,'alpha demand delta',r['values']['p_aux_required']-base['values']['p_aux_required'],-float(inputs[P+'sustain__ash_frac_in'])*base['values']['p_fus']*(r['inputs'][P+'f_alpha_fast']-.95))
result={'identities':checks,'oracle_comparisons':parity,'finance':finance,'outcome':'pass' if all(x['pass'] for x in checks+parity) else 'fail','failed':[x for x in checks+parity if not x['pass']]}
(R/'additional-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'outcome':result['outcome'],'identities':len(checks),'oracle_channels_per_case':len(channels),'failed':result['failed']},indent=2));assert result['outcome']=='pass'
