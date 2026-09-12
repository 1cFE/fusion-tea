"""All-case retained independent oracle and independently expanded scalar identities."""
import csv,json,math
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route as route,oracle_entry as oracle
from scripts.study import common,verify
H=Path(__file__).resolve().parents[1];R=H/'results';P=route.P
read=lambda p:json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def key(p):return json.dumps(p,sort_keys=True,separators=(',',':'))
def main():
 defaults=read(R/'package-inputs.json'); channelmap=read(H/'preparation/required-channels.json')
 expected={x['proposal_key']:x for x in read(H/'preparation/oracle-scan.json')}
 inputs={x['candidate_id']:x['inputs'] for x in read(R/'case-inputs.json')}
 catalog=read(R/'constraint-catalog.json');bindings=oracle.operand_bindings()
 failures=[];summaries=[];events=[];ledgers=[];counts={};maxima={}
 def check(cid,name,actual,want,absolute=False):
  counts[name]=counts.get(name,0)+1
  dev=abs(actual-want) if absolute else common.relative_deviation(actual,want)
  maxima[name]=max(maxima.get(name,0),dev)
  ok=math.isfinite(actual) and (math.isclose(actual,want,rel_tol=1e-9,abs_tol=1e-9) if absolute else dev<1e-9)
  if not ok:failures.append({'candidate_id':cid,'check':name,'native':actual,'expected':want,'deviation':dev})
 with (R/'native-points.csv').open() as f:
  for row in csv.DictReader(f):
   cid=row['candidate_id'];point=inputs[cid];p={**defaults,**point};v=lambda n:float(p[P+n]);y={a:float(row[a]) for a in channelmap}
   e=expected[key(point)];native={channelmap[a]:z for a,z in y.items()}
   assert set(point)<=set(oracle.ENTRY_KEY_TO_ORACLE_INPUT),'Unsupported oracle override'
   for fixed in ['discount_rate','inflation_rate','construction_years','operational_years','n_mod']:
    assert v(fixed)==float(defaults[P+fixed]),fixed
   if not point:
    baseline=read(R/'baseline-native-evidence.json')
    for channel,actual in native.items():
     if actual!=baseline['outputs'][channel]:failures.append({'candidate_id':cid,'exact_baseline_channel':channel,'native':actual,'baseline':baseline['outputs'][channel]})
    for q in catalog:
     if row[q]!=baseline['responses'][q]:failures.append({'candidate_id':cid,'exact_baseline_predicate':q})
   assert set(e['channels'])==set(oracle.ORACLE_OUTPUT_TO_CHANNEL.values())
   for channel,want in e['channels'].items():check(cid,channel,native[channel],want)
   for q,entry in catalog.items():
    derived,resolved=verify.derive_verdict(q,entry,bindings,point,defaults,e['channels'])
    want='satisfied' if derived else 'violated'
    if row[q]!=want:failures.append({'candidate_id':cid,'predicate':q,'actual':row[q],'expected':want})
   i=v('discount_rate');N=int(v('operational_years'));tc=v('construction_years');g=v('inflation_rate')
   crf=1/sum((1+i)**(-t) for t in range(1,N+1));mult=crf*sum((1+g)**(tc+t-1)/(1+i)**t for t in range(1,N+1))
   annual71=y['annual_om_unlevelized']*mult;annual80=y['annual_fuel']*mult
   radius=v('a');edges={};factor=v('kappa')*2*v('rb__pi')**2*v('R')
   for layer in ['vacuum','firstwall','blanket','reflector','ht_shield','structure','gap1','vessel','coil','gap2','lt_shield']:
    inner=radius;radius+=v(layer+'_t');edges[layer]=(inner,radius)
   vol=lambda layer:factor*(edges[layer][1]**2-edges[layer][0]**2)
   length=v('magnet__k_coil')*v('R');side=math.sqrt(v('magnet__I_coil')/v('magnet__j_wp'))/1000
   extra={'cas71_calc__crf':crf,'cas80_calc__crf':crf,'cas71_calc__levelized':annual71,'cas80_calc__levelized':annual80,'cas70_calc__cas70':annual71+y['cas72_annual'],'cas70_calc__annual_total':annual71+y['cas72_annual']+annual80,'coil_length__c_coil':length,'wp_sizing__wp_side':side,'wp_volume__vol_cold_total':v('magnet__f_wp_vol')*v('magnet__n_coils')*side**2*length+v('vol_cold_cryo'),'rb__blanket_vol':sum(vol(s) for s in ['firstwall','blanket','reflector']),'rb__shield_vol':vol('ht_shield')+vol('lt_shield'),'rb__structure_vol':vol('structure'),'rb__vessel_vol':vol('vessel'),'rb__wall_area':v('kappa')*4*v('rb__pi')**2*v('R')*edges['vacuum'][1],'rb__r_coil':edges['vessel'][1],'replacement_cost_per_event__replacement_cost_per_event':(y['blanket']+y['divertor'])*v('n_mod'),'reactor_equipment_subtotal__reactor_equipment_subtotal':y['powercore_capital']+y['remote_handling']}
   for a,want in extra.items():check(cid,a,y[a],want)
   # Closed-form event times; annual energy uses full years minus outage overlap.
   C=extra['replacement_cost_per_event__replacement_cost_per_event'];A=v('availability_direct');d=v('outage_years');u=v('unplanned_fraction');b=1-u
   if A>0:
    life=min(max(v('fluence_limit')/max(y['wall_load_peak'],1e-6),.5),N*A);period=life/A
    dates=[k*period for k in range(1,max(0,math.ceil(N/period)-1)+1)];F=N*A;planned=terminal=0.;unplanned=N-F;ratio=1.
   else:
    life=v('fluence_limit')/y['wall_load_peak'];run=life/b
    dates=[k*run+(k-1)*d for k in range(1,math.ceil(N/(run+d))+1) if k*run+k*d<N]
    next_start=(len(dates)+1)*run+len(dates)*d
    terminal=max(0,N-next_start);planned=len(dates)*d;online=N-planned-terminal;F=b*online;unplanned=u*online
    outages=[(t,t+d) for t in dates]+([(next_start,N)] if terminal else [])
    num=sum(b*(1-sum(max(0,min(end,year)-max(start,year-1)) for start,end in outages))/(1+i)**year for year in range(1,N+1))
    ratio=num/((F/N)*sum((1+i)**(-t) for t in range(1,N+1)))
   pv=sum(C/(1+i)**t for t in dates)
   cal={'calendar_physical_life_fpy':life,'calendar_n_replacements':len(dates),'calendar_productive_fpy':F,'calendar_planned_downtime_yr':planned,'calendar_terminal_downtime_yr':terminal,'calendar_unplanned_downtime_yr':unplanned,'calendar_availability':F/N,'calendar_replacement_pv':pv,'cas72_annual':crf*pv,'calendar_coil_life_margin_fpy':v('coil_life_fpy')-F,'calendar_dated_energy_ratio':ratio}
   for a,want in cal.items():check(cid,'dated-'+a,y[a],want,True)
   check(cid,'calendar-time-balance',y['calendar_productive_fpy']+y['calendar_planned_downtime_yr']+y['calendar_terminal_downtime_yr']+y['calendar_unplanned_downtime_yr'],N,True)
   events.append({'candidate_id':cid,'mode':'held' if A else 'computed','derived_event_dates_years':dates,'derived_terminal_start':N-terminal if terminal else None,'replacement_cost':C,'replacement_pv':pv})
   E=8760*y['p_net']*y['calendar_availability'];annual=annual71+crf*pv+annual80
   cap=y['total_capital']*(1+i)**(tc/2)*crf;cap1=(y['overnight_capital']+y['idc_capital'])*crf
   check(cid,'finite-sum-lcoe',y['lcoe'],(cap+annual)/E);check(cid,'finite-sum-lcoe-1cfe',y['lcoe_1cfe'],(cap1+annual)/E)
   ledgers.append({'candidate_id':cid,'C':cap,'C_1cfe':cap1,'A':annual,'E_MWh':E,'lcoe':y['lcoe'],'lcoe_1cfe':y['lcoe_1cfe']})
   identities={'signed-demand':(y['p_aux_required'],y['p_rad']+y['W_th']/y['tau_E']-y['p_alpha_heat']),'operating-wallplug':(y['operating_heat_wallplug'],y['p_aux_required']/(v('eta_source_heat')*v('eta_couple_heat'))),'source-heat':(y['q_source'],v('mn')*(1-3.52/17.58)*y['p_fus']+3.52/17.58*y['p_fus']+y['p_aux_required']),'loop-flow':(y['loop_mdot'],1e6*y['q_source']/(v('loop_cp')*v('loop_dT_blanket'))),'loop-pressure':(y['loop_dp_loop'],v('f_loss')*v('dp_loop_ref')*(y['loop_mdot']/v('n_loops')/v('mdot_loop_ref'))**2),'loop-compression':(y['loop_r_comp'],v('loop_p')/(v('loop_p')-y['loop_dp_loop'])),'loop-ihx':(y['loop_q_ihx'],y['q_source']+y['loop_w_fluid']),'thermal-power':(y['p_th'],y['q_source']+y['loop_q_recovered_total']),'fuel-balance':(y['fuel_inject_rate'],y['fuel_burn_rate']+y['fuel_exhaust_rate']),'divertor-heat':(y['divheat_p_heat_abs'],y['p_alpha_heat']+y['p_aux_required']),'divertor-separatrix':(y['divheat_p_sep'],y['divheat_p_heat_abs']-y['p_rad']),'divertor-target':(y['divheat_q_target_peak'],y['divheat_p_heat_abs']*(1-v('f_rad_total'))*v('q_target_ref')/v('p_nonrad_ref'))}
   identities.update({
    'loop-work':(y['loop_w_fluid'],y['loop_mdot']*v('loop_cp')*(v('loop_T_in')-y['loop_T_comp_in'])/1e6),
    'loop-electrical':(y['loop_p_elec'],y['loop_w_fluid']/v('eta_drive')),
    'pump-control':(y['loop_p_pump_total'],v('loop_live')*y['loop_p_elec']+v('p_pump_direct')),
    'heat-recovery-control':(y['loop_q_recovered_total'],v('loop_live')*y['loop_w_fluid']+v('eta_p_direct')*v('p_pump_direct')),
    'gross-electric':(y['p_the'],y['cycle_eta_th']*y['p_th']),
    'net-electric-ledger':(y['p_net'],y['p_the']-(v('p_tf')+v('p_pf')+y['loop_p_pump_total']+v('f_sub')*y['p_the']+v('p_trit')+v('p_house')+v('p_tfcool')+v('p_pfcool')+y['p_cryo']+y['operating_heat_wallplug'])),
    'fuel-injection':(y['fuel_inject_rate'],y['fuel_burn_rate']/v('burn_fraction')),
    'fuel-loss':(y['fuel_loss_rate'],(1-v('t_recycle'))*y['fuel_exhaust_rate']),
    'fuel-tbr-requirement':(y['fuel_tbr_required'],(y['fuel_burn_rate']+y['fuel_loss_rate']+v('lambda_T')*v('I_total')+v('G_stock'))/(v('eta_extract')*y['fuel_burn_rate'])),
    'fuel-tbr-margin':(y['fuel_tbr_margin'],v('tbr')-y['fuel_tbr_required']),
    'divertor-area-shadow':(y['divheat_q_target_peak_area_scaled'],y['divheat_q_target_peak']*v('R_ref_divertor')/v('R')),
    'vacuum-throughput':(y['vacuum_Q_total'],(y['fuel_exhaust_rate']+y['fuel_burn_rate'])*v('vacuum__k_B_in')*v('T_gas')),
    'vacuum-conditional-speed':(y['vacuum_S_eff_required'],y['vacuum_Q_total']/v('p_exhaust'))})
   for name,(actual,want) in identities.items():check(cid,name,actual,want,True)
   if len(ledgers)%500==0:print('Verified',len(ledgers),'cases',flush=True)
 write(R/'all-channel-verification.json',{'outcome':'fail' if failures else 'pass','cases':len(inputs),'oracle_channels':141,'extra_scalar_identities':17,'qualified_predicates':18,'comparison_counts':counts,'maximum_deviations':maxima,'failures':failures,'oracle_basis':'Retained preparation/oracle-scan.json, package-owned independent oracle at this candidate; generic verifier independently reruns stratified cases.'})
 write(R/'derived-event-tables.json',{'kind':'study-derived dates, not native model scalar outputs','cases':events});write(R/'finance-ledgers.json',ledgers)
 assert not failures,failures[:10]
if __name__=='__main__':main()
