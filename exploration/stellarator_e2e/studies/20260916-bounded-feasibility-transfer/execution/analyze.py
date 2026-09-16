"""All-point oracle comparison and signed authored-predicate residuals."""
import csv,json,math
from collections import Counter
from pathlib import Path
from scripts.study.verify import evaluate_operand
from exploration.stellarator_e2e.studies.oracle_entry import operand_bindings
H=Path(__file__).resolve().parents[1];R=H/'results';P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
def write(n,x):(R/n).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def pid(r):return r.get('proposal_id',r.get('id'))
def pointkey(p):return json.dumps({k:float(v) for k,v in p.items()},sort_keys=True)
native=read(R/'native-cases.json');scan={pointkey(r['point']):r for r in read(R/'oracle-scan.json')['rows'] if r['outcome']=='evaluated'};props={pid(r):r for r in read(H/'preparation/proposals.json')};cat=read(R/'predicate-catalog.json');defaults=read(H/'preparation/resolved-defaults.json');bindings=operand_bindings()
assert 0<len(native)<=79 and len(cat)==20
failures=[];ns=np=0;maxabs=maxrel=0.;rows=[]
for row in native:
 expected=scan[pointkey(row['inputs'])];assert len(expected['channels'])==226 and len(row['outputs'])==242
 for k,v in expected['channels'].items():
  got=row['outputs'][k];ns+=1;maxabs=max(maxabs,abs(got-v));maxrel=max(maxrel,abs(got-v)/max(abs(v),abs(got),1e-300))
  if not math.isfinite(got) or not math.isclose(got,v,rel_tol=1e-9,abs_tol=1e-9):failures.append({'proposal_id':row['proposal_id'],'channel':k,'native':got,'oracle':v})
 assert set(row['verdicts'])==set(expected['verdicts'])==set(cat)
 for cid,v in expected['verdicts'].items():
  np+=1
  if row['verdicts'][cid]!=v:failures.append({'proposal_id':row['proposal_id'],'constraint_id':cid})
 margins={}
 for cid,e in cat.items():
  ir=json.loads(e['predicate_ir']);left,right=[evaluate_operand(cid,o,bindings,row['inputs'],defaults,row['outputs'])[0] for o in ir['operands']]
  op=ir['operator'];assert op in ('>','>=','<','<=') and not e.get('is_negated')
  margins[e['source_local_identity']]=left-right if op in ('>','>=') else right-left
 point=defaults|row['inputs'];v=lambda k:row['outputs'][P+k];i=lambda k:point[P+k];n=int(i('heat_transport__n_loops'));meta=props.get(row['proposal_id'],expected)
 quantities={'R_m':i('plasma__R'),'a_m':i('plasma__a'),'current_MAturn':i('magnet__coil__I_coil')/1e6,'radial_exterior_m':i('magnet__coil__coil_t'),'transverse_cavity_m':i('magnet__casing__interior_y'),'loops':n,'power_account_valid':bool(v('divertor__divheat__power_account_valid')),'auxiliary_required_MW':v('plasma__sustain__p_aux_required'),'divertor_peak_MW_m2':v('divertor__divheat__q_target_peak'),'flow_total_kg_s':v('heat_transport__primary_loop__mdot'),'flow_per_loop_kg_s':v('heat_transport__primary_loop__mdot_loop'),'minimum_representative_integer_count':math.ceil(v('heat_transport__primary_loop__mdot')/i('heat_transport__mdot_loop_ref')),'pump_electric_MW':v('heat_transport__primary_loop__p_elec'),'IHX_total_MW':v('heat_transport__primary_loop__q_ihx'),'IHX_per_loop_MW':v('heat_transport__primary_loop__q_ihx')/n,'conditional_circulators':2*n,'conditional_IHXs':n,'net_electric_MW':v('pb__p_net'),'availability':v('calendar__availability'),'LCOE_dollars_MWh':v('lcoe_calc__lcoe'),'CAS22_dollars':v('cas22_capital__cas22_capital'),'total_capital_dollars':v('total_capital__total_capital')}
 rows.append({'proposal_id':row['proposal_id'],'family':meta['family'],'candidate_id':row['candidate_id'],'quantities':quantities,'signed_margins':margins,'all20_satisfied':all(v=='satisfied' for v in row['verdicts'].values()),'verdicts':row['verdicts'],'violated':[cat[c]['source_local_identity'] for c,v in row['verdicts'].items() if v!='satisfied']})
write('oracle-all-points.json',{'outcome':'fail' if failures else 'pass','cases':len(native),'scalar_comparisons':ns,'predicate_comparisons':np,'relative_tolerance':1e-9,'absolute_tolerance':1e-9,'exact_predicates':True,'max_absolute_deviation':maxabs,'max_relative_deviation':maxrel,'failures':failures,'unmapped_native_channels':sorted(set(native[0]['outputs'])-set(next(iter(scan.values()))['channels']))})
# Only exact matched coordinates, excluding loop count, support inherited headroom algebra.
matched={};loopkey=P+'heat_transport__n_loops'
for r in native:matched.setdefault(pointkey({k:v for k,v in r['inputs'].items() if k!=loopkey}),[]).append(r)
headroom=[]
for group in matched.values():
 if len(group)<2:continue
 group.sort(key=lambda r:(defaults|r['inputs'])[loopkey]);base=group[0]
 for r in group[1:]:
  v=r['outputs'];energy=8760*v[P+'pb__p_net']*v[P+'calendar__availability'];headroom.append({'base_id':base['proposal_id'],'case_id':r['proposal_id'],'annualized_break_even_headroom_dollars':(base['outputs'][P+'lcoe_calc__lcoe']-v[P+'lcoe_calc__lcoe'])*energy})
a={'scope':'Bounded engineered physical-screen search; conditional inherited costs, no economic optimum.','cases':rows,'overall':{'cases':len(rows),'all20_passes':sum(r['all20_satisfied'] for r in rows),'valid_account_combined_passes':sum(r['all20_satisfied'] and r['quantities']['power_account_valid'] for r in rows),'invalid_power_accounts':sum(not r['quantities']['power_account_valid'] for r in rows)},'predicate_outcomes':{c:{'source_local_identity':e['source_local_identity'],'counts':dict(Counter(r['verdicts'][c] for r in rows))} for c,e in cat.items()},'signed_margin_definition':'Authored predicate lhs-rhs for >= or >; rhs-lhs for <= or <. Positive means inside the authored comparison. Units are the authored operands; equality needs exact operator verdict.','matched_loop_headroom':headroom,'break_even_equation':'(LCOE_base-LCOE_N)*8760*net_MW_N*availability_N; exact matched input pairs only. Equivalent annual omitted-cost budget, never an installed quote.'}
write('analysis.json',a)
flat=[{'proposal_id':r['proposal_id'],'family':r['family'],**r['quantities'],**{'margin_'+k:v for k,v in r['signed_margins'].items()},'all20_satisfied':r['all20_satisfied'],**r['verdicts'],'violated':';'.join(r['violated'])} for r in rows]
with (R/'case-summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(flat[0]),lineterminator='\n');w.writeheader();w.writerows(flat)
assert not failures
print('Mapped scalars',ns,'predicates',np,'failures',len(failures),a['overall'])
