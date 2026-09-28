"""Verify every mapped scalar/predicate, preserve controls and quantify requirements."""
import csv,json,math
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parents[1];R=H/'results';P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
def write(n,v):(R/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
def close(a,b):return math.isfinite(a) and math.isfinite(b) and math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-9)
native=read(R/'native-cases.json');byid={r['proposal_id']:r for r in native};scan={r['proposal_id']:r for r in read(R/'oracle-scan.json')['rows']};props={r['proposal_id']:r for r in read(H/'preparation/proposals.json')};cat=read(R/'predicate-catalog.json');defaults=read(H/'preparation/resolved-defaults.json');entering={r['proposal_id']:r for r in read(H/'preparation/entering/native-cases.json')['cases']}
assert len(native)==20 and len(cat)==20
failures=[];ns=np=0;maxabs=maxrel=0.
for pid,row in byid.items():
 expected=scan[pid];assert row['inputs']==expected['point'] and len(expected['channels'])==226
 for k,v in expected['channels'].items():
  got=row['outputs'][k];ns+=1;maxabs=max(maxabs,abs(got-v));maxrel=max(maxrel,abs(got-v)/max(abs(v),abs(got),1e-300))
  if not close(got,v):failures.append({'proposal_id':pid,'channel':k,'native':got,'oracle':v})
 assert set(row['verdicts'])==set(expected['verdicts'])==set(cat)
 for cid,v in expected['verdicts'].items():
  np+=1
  if row['verdicts'][cid]!=v:failures.append({'proposal_id':pid,'constraint_id':cid})
write('oracle-all-points.json',{'outcome':'fail' if failures else 'pass','cases':len(native),'scalar_comparisons':ns,'predicate_comparisons':np,'relative_tolerance':1e-9,'absolute_tolerance':1e-9,'exact_predicates':True,'max_absolute_deviation':maxabs,'max_relative_deviation':maxrel,'failures':failures,'unmapped_native_channels':sorted(set(native[0]['outputs'])-set(scan[native[0]['proposal_id']]['channels']))})
comparisons=[];invariant=[]
for family,old in entering.items():
 base=byid[family+'--loops-14'];diff={k:{'old':v,'new':base['outputs'][k]} for k,v in old['outputs'].items() if v!=base['outputs'][k]};pred={k:v for k,v in old['responses'].items() if k in cat};assert set(pred)==set(cat)
 flips={k:{'old':v,'new':base['verdicts'][k]} for k,v in pred.items() if v!=base['verdicts'][k]}
 comparisons.append({'family':family,'scalar_comparisons':len(old['outputs']),'predicate_comparisons':len(pred),'changed_outputs':diff,'changed_predicates':flips})
 # Full native subsystem outputs, not only selected report values.
 heldkeys=[k for k in base['outputs'] if k.startswith(P+'magnet__') or k.startswith(P+'divertor__divheat__')]
 heldpred=[k for k,e in cat.items() if any(word in e['source_local_identity'] for word in ['magnet','conductor','winding','divertor','field','fit','wp_stress','cond_strain'])]
 for n in [15,16,18]:
  row=byid[family+f'--loops-{n}'];changes=[k for k in heldkeys if row['outputs'][k]!=base['outputs'][k]];flips=[k for k in heldpred if row['verdicts'][k]!=base['verdicts'][k]]
  invariant.append({'proposal_id':row['proposal_id'],'output_comparisons':len(heldkeys),'predicate_ids':heldpred,'changed_outputs':changes,'changed_predicates':flips})
assert not any(r['changed_outputs'] or r['changed_predicates'] for r in comparisons+invariant)
write('comparison-entering.json',{'outcome':'pass','exact_equality':True,'cases':comparisons});write('held-subsystems.json',{'outcome':'pass','exact_equality':True,'scope':'All native magnet outputs, divertor heat-account outputs, all six named magnet/divertor predicates; inherited divertor cost is allowed to change with thermal power and is reported separately.','cases':invariant})
loopid=next(k for k,e in cat.items() if e['source_local_identity']=='loop_capacity_ok')
rows=[]
for pid,row in byid.items():
 point=defaults|row['inputs'];v=lambda k:row['outputs'][P+k];i=lambda k:point[P+'heat_transport__'+k];lp=lambda k:v('heat_transport__primary_loop__'+k)
 n=int(i('n_loops'));mdot=lp('mdot');ref=i('mdot_loop_ref');source=v('blanket__source_heat__q_source');w=lp('w_fluid');q=lp('q_ihx');family=props[pid]['family'];base=byid[family+'--loops-14'];energy=8760*v('pb__p_net')*v('calendar__availability');lcoe=v('lcoe_calc__lcoe');headroom=(base['outputs'][P+'lcoe_calc__lcoe']-lcoe)*energy
 quantities={'loops':n,'source_heat_MW':source,'flow_total_kg_s':mdot,'flow_per_loop_kg_s':lp('mdot_loop'),'reference_flow_allowance_per_loop_kg_s':ref,'adopted_total_flow_allowance_kg_s':n*ref,'total_flow_margin_kg_s':n*ref-mdot,'per_loop_margin_kg_s':lp('capacity_margin'),'minimum_representative_integer_count':math.ceil(mdot/ref),'T_in_K':i('loop_T_in'),'T_out_K':lp('T_out'),'deltaT_K':i('loop_dT_blanket'),'dp_loop_Pa':lp('dp_loop'),'fluid_work_MW':w,'electrical_work_MW':lp('p_elec'),'recovered_heat_MW':lp('q_recovered_total'),'IHX_total_MW':q,'IHX_per_loop_MW':q/n,'source_reference_mean_IHX_MW':2231.1/9,'conditional_circulators':2*n,'conditional_IHXs':n,'gross_electric_MW':v('pb__p_et'),'net_electric_MW':v('pb__p_net'),'divertor_inherited_cost_dollars':v('divertor__divertor_cost__cost'),'coolant_inherited_cost_dollars':v('heat_transport__coolant__cost'),'CAS22_dollars':v('cas22_capital__cas22_capital'),'CAS20_dollars':v('cas20_capital__cas20_capital'),'total_capital_dollars':v('total_capital__total_capital'),'availability':v('calendar__availability'),'LCOE_dollars_MWh':lcoe,'annual_net_energy_MWh':energy,'annualized_break_even_headroom_dollars':headroom,'source_heat_residual_MW':source-mdot*i('loop_cp')*i('loop_dT_blanket')/1e6,'IHX_heat_residual_MW':q-source-w,'electric_work_residual_MW':lp('p_elec')-w/i('eta_drive')}
 rows.append({'proposal_id':pid,'family':family,'candidate_id':row['candidate_id'],'quantities':quantities,'loop_screen_satisfied':row['verdicts'][loopid]=='satisfied','all20_satisfied':all(x=='satisfied' for x in row['verdicts'].values()),'violated':[cat[k]['source_local_identity'] for k,x in row['verdicts'].items() if x!='satisfied']})
a={'scope':'Twenty conditional averaged-loop-count sensitivity cases; no engineering qualification or priced equipment accommodation.','cases':rows,'overall':{'cases':20,'loop_screen_passes':sum(r['loop_screen_satisfied'] for r in rows),'all20_passes':sum(r['all20_satisfied'] for r in rows)},'predicate_outcomes':{k:{'source_local_identity':e['source_local_identity'],'counts':dict(Counter(r['verdicts'][k] for r in native))} for k,e in cat.items()},'break_even_equation':'annualized headroom = (LCOE at14 - LCOE at N)*8760*net_MW_N*availability_N. This is extra equivalent annual cost that removes inherited-account LCOE benefit, not installed cost or a capital estimate. Finance, calendar and plant inputs held within each family.','residual_max_abs_MW':{k:max(abs(r['quantities'][k]) for r in rows) for k in ['source_heat_residual_MW','IHX_heat_residual_MW','electric_work_residual_MW']}}
write('analysis.json',a)
flat=[{'proposal_id':r['proposal_id'],'family':r['family'],**r['quantities'],'loop_screen_satisfied':r['loop_screen_satisfied'],'all20_satisfied':r['all20_satisfied'],'violated':';'.join(r['violated'])} for r in rows]
with (R/'case-summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(flat[0]),lineterminator='\n');w.writeheader();w.writerows(flat)
assert not failures
print('Mapped scalars',ns,'predicates',np,'failures',len(failures),a['overall'])
