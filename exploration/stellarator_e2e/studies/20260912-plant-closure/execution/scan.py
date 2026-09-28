"""Prepare explicit cases using oracle screening; never execute the native study here."""
import csv, json, math, sys, time, traceback
from pathlib import Path
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from exploration.stellarator_e2e.studies import oracle_entry as oracle, study_route as route
from scripts.study import verify
H=Path(__file__).resolve().parents[1]; P=route.P
D=verify.package_input_values(route.PACKAGE_DIR)
CAT={e['constraint_id']:e for e in json.loads((H/'context/model_contract.json').read_text())['constraint_catalog']['concrete_entries']}
B=oracle.operand_bindings()
FIELDS={'R':'R','a':'a','I_coil_A':'magnet__I_coil','n_e0':'n_e0','T_i0_keV':'T_i0','p_wallplug_heat_MW':'p_wallplug_heat','eta_source_heat':'eta_source_heat','eta_couple_heat':'eta_couple_heat','tau_ratio_ash':'tau_ratio_ash'}
def write(p,data):p.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def canonical(point): return {k:float(v) for k,v in sorted(point.items()) if float(v)!=float(D[k])}
def key(point):return json.dumps(canonical(point),sort_keys=True,separators=(',',':'))
def from_row(row):
 point={}
 for field,name in FIELDS.items():
  if row.get(field):point[P+name]=float(row[field])
 return canonical(point)
def eligibility(point):
 p={**D,**point};v=lambda n:float(p[P+n])
 if not all(math.isfinite(float(x)) for x in point.values()):return 'nonfinite input'
 if v('R')<=v('a')+2.25:return 'derived radial-stack clearance R <= a + 2.25'
 if v('magnet__R_ref')<=v('magnet__a_coil_ref'):return 'nonpositive reference inboard bore'
 if v('n_mod')!=1:return 'outside single-module experiment'
 for n in ['R','a','magnet__j_wp','loop_cp','loop_dT_blanket','loop_p','n_loops','operational_years']:
  if v(n)<=0:return 'nonpositive '+n
 for n in ['eta_source_heat','eta_couple_heat','eta_is','eta_drive']:
  if not 0<v(n)<=1:return 'efficiency outside (0,1]: '+n
 if v('discount_rate')==0 or v('discount_rate')==v('inflation_rate'):return 'unrepaired financial denominator'
 return None
CACHE={}; SIZING=[]
def evaluate(point):
 point=canonical(point);k=key(point)
 if k in CACHE:return CACHE[k]
 try:
  reason=eligibility(point)
  if reason:raise ValueError(reason)
  channels=oracle.evaluate(point)
  if not all(math.isfinite(x) for x in channels.values()):raise ValueError('nonfinite oracle output')
  verdicts={cid:'satisfied' if verify.derive_verdict(cid,e,B,point,D,channels)[0] else 'violated' for cid,e in CAT.items()}
  result={'status':'eligible','channels':channels,'verdicts':verdicts}
 except Exception as exc:result={'status':'excluded','reason':type(exc).__name__+': '+str(exc),'traceback':traceback.format_exc()}
 CACHE[k]=result
 return result
def evaluate_pair(point):
 return key(point),evaluate(point)

def precompute(points,stage):
 unique={key(p):canonical(p) for p in points if key(p) not in CACHE}
 print('Parallel',stage,':',len(unique),'independent oracle evaluations',flush=True)
 # Separate processes isolate the oracle's saved/restored module-global IN.
 with ProcessPoolExecutor(max_workers=8,mp_context=multiprocessing.get_context('spawn')) as pool:
  for i,(k,result) in enumerate(pool.map(evaluate_pair,unique.values(),chunksize=4)):
   CACHE[k]=result
   if i%100==0:print(stage,i,'/',len(unique),flush=True)


def sized(point,label):
 scout={**point,P+'n_loops':1000.0};result=evaluate(scout)
 if result['status']!='eligible':
  SIZING.append({'label':label,'scout_inputs':scout,'status':'failed full oracle scout; upstream duty not determined','failure':result})
  return None,result['reason']
 # The scout's q_source is upstream of pump/loop effects; native graph establishes this.
 c=result['channels'];count=max(1,math.ceil(c[P+'primary_loop__mdot']/float(D[P+'mdot_loop_ref'])))
 SIZING.append({'label':label,'scout_inputs':scout,'status':'scout complete; actual proposal separately screened','scout_n_loops':1000,'q_source':c[P+'source_heat__q_source'],'mdot':c[P+'primary_loop__mdot'],'mdot_loop_ref':D[P+'mdot_loop_ref'],'selected_n_loops':count,'candidate_pin':json.loads((H/'context/candidate.json').read_text())['candidate']['pin']})
 return canonical({**point,P+'n_loops':float(count)}),None

def main():
 assert json.loads((H/'reviews/pre-execution-approval.json').read_text())['approved'] is True
 assert json.loads((H/'results/preflight.json').read_text())['outcome']=='pass'
 historical=list(csv.DictReader((H/'context/historical-points.csv').open()))
 excluded=list(csv.DictReader((H/'context/historical-excluded.csv').open()))
 for field,name in [('j_wp','magnet__j_wp'),('eta_couple_heat','eta_couple_heat'),('discount_rate','discount_rate')]:
  assert all(float(r[field])==float(D[P+name]) for r in historical),(field,D[P+name])
 witnesses=[('baseline',{})]
 for suffix in ['c2823','c3598','c3343','c7752']:
  row=next(r for r in historical if r['case_id'].endswith(':'+suffix));witnesses.append((row['case_id'],from_row(row)))
 # Exact full-result control equality tests the process transport without changing arithmetic.
 controls=[{}, {P+'R':14.0}]
 serial=[evaluate(p) for p in controls]
 with ProcessPoolExecutor(max_workers=2,mp_context=multiprocessing.get_context('spawn')) as pool:
  parallel=list(pool.map(evaluate_pair,controls))
 assert [r for k,r in parallel]==serial
 write(H/'preparation/parallel-control-check.json',{'outcome':'pass','controls':controls,'comparison':'complete outputs/verdicts equal between serial and isolated-process oracle','processes':8})
 precompute([{**from_row(r),P+'n_loops':1000.0} for r in historical+excluded],'sizing-scouts')
 rows=[]
 def add(arm,label,point,**meta):rows.append({'arm_id':arm,'label':label,'inputs':canonical(point),**meta})
 add('arm-baseline','manifest',{})
 for i,row in enumerate(historical+excluded):
  point=from_row(row);oldid=row.get('case_id') or 'historical-excluded-row-'+str(i-len(historical)+1)
  meta={'historical_id':oldid,'historical_arm':row['arm_id'],'historical_excluded':i>=len(historical)}
  add('arm-window-fixed',oldid,{**point,P+'n_loops':14.0},**meta)
  resized,error=sized(point,oldid)
  if error:rows.append({'arm_id':'arm-window-sized','label':oldid,'inputs':point,'sizing_error':error,**meta})
  else:add('arm-window-sized',oldid,resized,**meta)
  if i%250==0: print('Sizing historical tuple',i,'/',len(historical)+len(excluded),flush=True)
 for name,p in witnesses:
  for l in [0,1]:
   for c in [0,1]:
    for a in [0,1]:
     point={**p,P+'loop_live':l,P+'p_pump_direct':0 if l else 195,P+'eta_p_direct':0 if l else .5,P+'cycle_live':c,P+'eta_th_direct':0 if c else .333,P+'availability_direct':0 if a else .85}
     add('arm-closure-factorial',f'{name}:L{l}C{c}A{a}',point,anchor=name,modes=[l,c,a])
  for d in [5,7,10]:
   for u in [0,.05,.10]:add('arm-calendar',f'{name}:d{d}:u{u}',{**p,P+'outage_years':d/12,P+'unplanned_fraction':u},anchor=name)
  for f in [.025,.05,.10]:add('arm-fuel',f'{name}:burn{f}',{**p,P+'burn_fraction':f},anchor=name)
  for q in [9.5,5]:add('arm-divertor-transport',f'{name}:q{q}',{**p,P+'q_target_ref':q},anchor=name)
  for f in [.8,.9,.95]:add('arm-divertor-radiation',f'{name}:radiation{f}',{**p,P+'f_rad_total':f},anchor=name)
  for r in [100,120,220]:add('arm-reserve',f'{name}:reserve{r}',{**p,P+'p_wallplug_heat':r},anchor=name)
 for loss in [.8,1,1.2]:
  for flow in [.8,1,1.2]:add('arm-loop-loss',f'loss{loss}:flow{flow}',{P+'f_loss':loss,P+'loop_dT_blanket':200/flow})
 for t in [383,384,480,642,643]:add('arm-cycle',f'Rankine-T2-{t}',{P+'loop_T_in':t+273.15+20-200})
 add('arm-cycle','sCO2-T2-480',{P+'a_fit':.4347,P+'b_fit':2.5043,P+'T2_min':135,P+'T2_max':750,P+'T_offset_fit':273,P+'delta_eta':0})
 precompute([row['inputs'] for row in rows if not row.get('sizing_error')],'actual-proposals')
 proposals={};out=[];scan=[]
 for i,row in enumerate(rows):
  point=row['inputs'];r={'status':'excluded','reason':row['sizing_error']} if row.get('sizing_error') else evaluate(point)
  row['proposal_key']=key(point);row['scan_status']=r['status']
  if r['status']=='eligible':
   proposals[row['proposal_key']]=point
   row['scan_full_satisfied']=all(x=='satisfied' for x in r['verdicts'].values())
   row['scan_lcoe']=r['channels'][P+'lcoe_calc__lcoe']
   row['scan_violations']=[CAT[k]['source_local_identity'] for k,v in r['verdicts'].items() if v!='satisfied']
  else:
   row['exclusion_reason']=r['reason']
   if 'traceback' in r:row['failure_traceback']=r['traceback']
  out.append(row)
  if i%500==0:print('Classifying proposal',i,'/',len(rows),flush=True)
 # Full oracle values are retained once per proposed native case, not once per correlation row.
 for k,p in proposals.items():scan.append({'proposal_key':k,'inputs':p,**CACHE[k]})
 write(H/'preparation/correlation.json',out);write(H/'preparation/proposals.json',list(proposals.values()))
 for q in SIZING:
  if 'selected_n_loops' not in q:continue
  actual=canonical({**q['scout_inputs'],P+'n_loops':float(q['selected_n_loops'])});r=evaluate(actual)
  if r['status']=='eligible':
   q['source_heat_equal']=math.isclose(q['q_source'],r['channels'][P+'source_heat__q_source'],rel_tol=1e-9,abs_tol=1e-9)
   q['total_flow_equal']=math.isclose(q['mdot'],r['channels'][P+'primary_loop__mdot'],rel_tol=1e-9,abs_tol=1e-9)
   assert q['source_heat_equal'] and q['total_flow_equal']
  else:q['actual_failure']=r['reason']
 write(H/'preparation/oracle-scan.json',scan);write(H/'preparation/sizing-queries.json',SIZING)
 summary={'historical_rows':len(historical),'historical_exclusions_reconsidered':len(excluded),'correlation_rows':len(rows),'unique_eligible_proposals':len(proposals),'excluded_correlations':sum(r['scan_status']=='excluded' for r in out),'fully_satisfied_correlations':sum(r.get('scan_full_satisfied',False) for r in out),'arms':{a:dict(Counter(r['scan_status'] for r in out if r['arm_id']==a)) for a in sorted({r['arm_id'] for r in out})},'status':'scan complete; edge report and freeze still required'}
 write(H/'preparation/scan-summary.json',summary);print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':main()
