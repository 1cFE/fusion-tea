"""Reviewer arithmetic from retained native outputs and generated wiring; no production calculations imported."""
from pathlib import Path
import json,math,yaml,hashlib
B=Path('work/active/WI-073_matched-steam-cycle-for-current-comparison/evidence');HERE=Path(__file__).parent
package=Path('exploration/stellarator_e2e/generated');p=yaml.safe_load((package/'pipelines/pipeline.yaml').read_text());P='stellarator_09__stellaris__'
params={f.stem:json.loads(f.read_text()) for f in (package/'inputs').glob('*.json')}
rows=json.loads((B/'independent-oracle/native-check-results.json').read_text());results=[]
def equal(a,b):assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-8),(a,b)
for r in rows:
 outputs=r['outputs'];changes=r['inputs']
 def resolve(text):
  ref=text.split(' ',1)[1]
  if ref.endswith('.root'):ref=ref[:-5]
  if '.' in ref:
   table,key=ref.split('.',1);return changes.get(key,params[table][key])
  return outputs[ref]
 pb=p['modules'][P+'pb'];x={k:resolve(v) for k,v in pb['inputs'].items()}
 alpha=x['p_nrl']*3.52/17.58;qsource=x['mn_in']*(x['p_nrl']-alpha)+alpha+x['p_input_in'];heat=qsource+x['q_recovered_in'];gross=heat*x['eta_th_in']
 recirc=sum(x[k] for k in ['p_tf_in','p_pf_in','p_pump_total_in','p_trit_in','p_house_in','p_tfcool_in','p_pfcool_in','p_cryo','p_wallplug_in','p_cycle_pumps_in','p_cooling_water_in'])+gross*x['f_sub_in'];net=gross-recirc
 for name,v in [('p_th',heat),('p_the',gross),('p_net',net)]:equal(v,outputs[P+'pb__'+name])
 active=outputs[P+'turbine__matched_cycle__active'];c=lambda k:outputs[P+'turbine__matched_cycle__'+k];w=lambda k:outputs[P+'heat_rejection__cooling_water__'+k]
 if active:
  equal(heat,outputs[P+'heat_transport__equipment__conversion_heat_MW']);equal(gross,c('p_gross_MW'))
  equal(heat+c('p_cycle_pumps_MW'),gross+c('q_rejection_before_cooling_MW'))
  equal(c('q_rejection_before_cooling_MW'),c('q_condenser_MW')+c('q_mechanical_loss_MW')+c('q_generator_loss_MW')+c('q_pump_motor_loss_MW'))
  equal(x['p_cycle_pumps_in'],c('p_condensate_electric_MW')+c('p_feedwater_electric_MW'))
  equal(c('salt_flow_total_kg_s'),c('salt_main_flow_kg_s')+c('salt_reheat_flow_kg_s'))
  if w('active'):equal(w('q_total_rejection_MW'),c('q_rejection_before_cooling_MW')+w('p_cooling_pump_electric_MW'))
 costs={}
 for part,calc,driver in [('turbine','turbine_cost','p_the'),('electric_plant','electric_cost','p_et'),('heat_rejection','heat_rejection_cost','p_th'),('misc_plant','misc_cost','p_et')]:
  m=p['modules'][P+part+'__'+calc];assert m['inputs']['power'].endswith(P+'pb__'+driver)
  v={k:resolve(t) for k,t in m['inputs'].items()};expected=v['power']*v['cost_per_mw']*v['n_mod_in'];actual=resolve(m['outputs']['root']);equal(expected,actual);costs[part]=actual
 results.append({'case':r['label'],'source_heat_MW':qsource,'recovered_heat_MW':x['q_recovered_in'],'gross_MW':gross,'recirculating_MW':recirc,'net_MW':net,'subsystem_allowance_MW':gross*x['f_sub_in'],'cycle_pumps_MW':x['p_cycle_pumps_in'],'cw_pump_MW':x['p_cooling_water_in'],'costs':costs})
out={'scope':'independent heat/gross/net/rejection and CAS23-26 driver arithmetic on retained native cases, not full cost-completeness or physical qualification','native_receipt_sha256':hashlib.sha256((B/'independent-oracle/native-check-results.json').read_bytes()).hexdigest(),'pipeline_sha256':hashlib.sha256((package/'pipelines/pipeline.yaml').read_bytes()).hexdigest(),'cases':results}
(HERE/'account-check.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(results),'cases')
