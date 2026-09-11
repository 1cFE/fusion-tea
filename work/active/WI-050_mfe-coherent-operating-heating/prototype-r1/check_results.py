"""Independent identities/response assertions over retained native execution evidence."""
import json,math
import yaml
from pathlib import Path
h=Path(__file__).resolve().parent; root=Path.cwd(); p='stellarator_09__stellaris__'
r=json.loads((h/'results.json').read_text()); scratch=Path((h/'scratch.txt').read_text().strip()); inputs={}
for f in (scratch/'generated/inputs').glob('*.json'): inputs.update(json.loads(f.read_text()))
def equal(a,b): assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-9),(a,b)
def get(case,k): return r[case]['outputs'][p+k]
for case in ['baseline','reserve','demand','efficiency','availability']:
 o=r[case]['outputs']; d=o[p+'sustain__p_aux_required']; couple=.8 if case=='efficiency' else 1.0
 equal(o[p+'operating_heat__p_coupled'],d); equal(o[p+'operating_heat__p_delivered']*couple,d); equal(o[p+'operating_heat__p_wallplug']*.5*couple,d)
 f=o[p+'fusion__p_fus']; alpha=f*3.52/17.58
 q=inputs[p+'mn']*(f-alpha)+alpha+d
 equal(o[p+'source_heat__q_source'],q); equal(o[p+'pb__p_th'],q+o[p+'primary_loop__q_recovered_total']); equal(o[p+'pb__p_et'],o[p+'pb__p_th']*o[p+'cycle__eta_th'])
 # Net conservation: independently sum each online parasitic category.
 gross=o[p+'pb__p_et']; loads=sum(inputs[p+k] for k in ['p_tf','p_pf','p_tfcool','p_pfcool','p_trit','p_house'])+inputs[p+'f_sub']*gross+o[p+'cryo_elec__p_elec']+o[p+'primary_loop__p_pump_total']+d/(.5*couple)
 equal(o[p+'pb__p_net'],gross-loads)
 absorbed=o[p+'sustain__p_alpha_heat']+d; equal(o[p+'divheat__p_heat_abs'],absorbed); equal(o[p+'divheat__p_target_nonrad'],absorbed*(1-inputs[p+'f_rad_total']))
 equal(o[p+'divheat__q_target_peak'],o[p+'divheat__p_target_nonrad']*inputs[p+'q_target_ref']/inputs[p+'p_nonrad_ref'])
for k in ['operating_heat__p_coupled','operating_heat__p_delivered','operating_heat__p_wallplug','source_heat__q_source','primary_loop__mdot','primary_loop__p_pump_total','primary_loop__q_recovered_total','pb__p_et','pb__p_net','divheat__p_heat_abs','calendar__cas72_annual','cas71_calc__levelized','cas80_calc__levelized','calendar__availability']:
 assert get('baseline',k)==get('reserve',k),k
for k in ['operating_heat__p_coupled','operating_heat__p_wallplug','pb__p_net']:
 assert get('baseline',k)==get('availability',k),k
assert get('baseline','heating_cost__cost')==264145000.; assert get('reserve','heating_cost__cost')==316974000.; assert get('demand','heating_cost__cost')==264145000.
assert get('demand','fusion__p_fus')==get('baseline','fusion__p_fus')
assert get('demand','divheat__p_heat_abs')==get('baseline','divheat__p_heat_abs')
for case in ['negative_efficiency','overunit_efficiency']:
 assert any('heating_source_' in k and v=='violated' for k,v in r[case]['responses'].items())
assert r['zero_efficiency']['error']=='EvaluationFailed'
old=json.loads((root/'work/analysis/20260911-190758_mfe-operating-state-evidence/baseline/all_outputs.json').read_text()); b=r['baseline']['outputs']
changes={k.removeprefix(p):{'before':old[k],'after':v,'delta':v-old[k]} for k,v in b.items() if k in old and isinstance(old[k],(int,float)) and v!=old[k]}
# Financial decomposition holds original financial conventions; numerator and energy separated.
def bridge(before,after,lcoe):
 oldenergy=8760*before[p+'pb__p_net']*before[p+'calendar__availability']; newenergy=8760*after[p+'pb__p_net']*after[p+'calendar__availability']
 oldnum=before[p+lcoe]*oldenergy; newnum=after[p+lcoe]*newenergy
 capdelta=(after[p+'total_capital__total_capital']-before[p+'total_capital__total_capital'])
 ann=after[p+'cas70_calc__annual_total']-before[p+'cas70_calc__annual_total']
 capcharge=(newnum-oldnum)-ann
 parts={'capital_delta_dollars':capdelta,'annual_capital_charge_delta':capcharge,'annual_cost_delta':ann,'energy_delta_mwh':newenergy-oldenergy,'capital_effect_per_mwh':capcharge/oldenergy,'annual_effect_per_mwh':ann/oldenergy,'energy_effect_per_mwh':newnum/newenergy-newnum/oldenergy}
 equal(sum(parts[k] for k in ['capital_effect_per_mwh','annual_effect_per_mwh','energy_effect_per_mwh']),after[p+lcoe]-before[p+lcoe]);return parts
contract=json.loads((scratch/'generated/contracts/model_contract.json').read_text()); assert len(contract['parameters'])==247; assert not any('p_operating_coupled_heat' in str(x) for x in contract['parameters'])
pipeline=yaml.safe_load((scratch/'generated/pipelines/pipeline.yaml').read_text())
watched_modules={k:v.get('inputs',{}) for k,v in pipeline['modules'].items() if k in {p+n for n in ['operating_heat','source_heat','pb','divheat','heating_cost']}}
summary={'generated_operating_bindings':watched_modules,'passed':'conversion, thermal/electric/divertor conservation, reserve invariance/procurement, physical-demand alpha compensation, availability invariance, efficiency rejection, no demand entry','entry_count':247,'semantic_fingerprint':contract['semantic_fingerprint'],'changed_baseline_scalars':changes,'reserve_changed_scalars':{k.removeprefix(p):{'before':v,'after':r['reserve']['outputs'][k]} for k,v in b.items() if v!=r['reserve']['outputs'][k]},'baseline_financial_bridge':{name:bridge(old,b,name) for name in ['lcoe_calc__lcoe','lcoe_1cfe_calc__lcoe']}}
(h/'checks.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary['passed']);print('changed baseline scalars',len(changes));print(json.dumps(summary['baseline_financial_bridge'],indent=2))
