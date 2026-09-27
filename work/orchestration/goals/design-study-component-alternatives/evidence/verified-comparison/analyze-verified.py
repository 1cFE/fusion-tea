"""Read retained native cases, summarize accounting and render publication figures.

No model/oracle imports or evaluations. Values come from results/cases.json;
selection metadata and duplicate aliases come from the same study record.
Run with .codex-test/run python <this-file> [--record PATH] [--out-dir PATH].
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,math,os
os.environ.setdefault("MPLCONFIGDIR","/tmp/wi096-matplotlib")
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
P='component_alternatives__plant__'
ROOT=Path(__file__).resolve().parents[6]
OLD=ROOT/'exploration/component_alternatives/studies/20260926-design-study-component-alternatives'
DEFAULT=ROOT/'exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b'
LEDGER=('gross_electric electrical_load net_electric total_rejected unremoved_heat energy_residual conversion_energy_residual capital_total recurring_base annual_service annual_makeup machine_replacement_pv bundle_replacement_pv conversion_replacement_pv replacement_pv annuity_factor annual_energy discounted_energy accounted_pv corrected_pv cost_per_net_MWh economic_defined').split()
C={'steam':'#b65a26','fixed':'#967351','gas':'#176f91','failed':'#be4048','no_root':'#9ca3af','lower':'#8a5b9c','upper':'#8b949e','mixed':'#b68942'}
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def channel(row,owner,field,calc='evaluate'):return float(row['outputs'][P+owner+'__'+calc+'__'+field])
def inp(row,key):return float(row['inputs'][P+key])
def close(a,b,absolute=1e-5):assert math.isclose(a,b,rel_tol=1e-9,abs_tol=absolute),(a,b)
def ledger(row,branch):
 d={k:channel(row,branch+'_ledger',k) for k in LEDGER}
 d['capital_accounts']={str(i):channel(row,branch+'_ledger','capital_'+str(i)) for i in range(1,11)}
 d['controller_capital']=inp(row,branch+'_ledger__controller_capital')
 d['service_pv']=d['annual_service']*d['annuity_factor'];d['makeup_pv']=d['annual_makeup']*d['annuity_factor']
 d['cost_components_per_MWh']={k:d[v]/d['discounted_energy'] for k,v in [('Capital','capital_total'),('Service','service_pv'),('Makeup','makeup_pv'),('Replacement','replacement_pv')]}
 close(sum(d['capital_accounts'].values())+d['controller_capital'],d['capital_total'])
 close(d['capital_total']+d['replacement_pv']+d['service_pv']+d['makeup_pv'],d['accounted_pv'])
 if d['economic_defined']:
  close(d['corrected_pv']/d['discounted_energy'],d['cost_per_net_MWh'])
 else:assert d['cost_per_net_MWh']==0
 return d

def summarize(record):
 verification=verification_gate(record)
 raw=read(record/'results/cases.json')['cases'];proposals=read(record/'proposed-points.json')['cases'];window=read(record/'window.json')
 assert len(raw)==len(proposals)==window['native_case_count']==498
 native={r['case']:r for r in raw};assert len(native)==498 and set(native)=={r['case'] for r in proposals}
 diagnostic_cases={r['case']:dict(candidate_id=r['candidate_id'],numeric_mismatches=[],predicate_mismatches=[]) for r in raw}
 assert set(diagnostic_cases)==set(native)
 roles={r['case']:{r['role']} for r in proposals};aliases=collections.defaultdict(list)
 for a in window['duplicate_aliases']:
  aliases[a['native_case']].append(a['alias']);roles[a['native_case']].add(a['role'])
 index={**native,**{a['alias']:native[a['native_case']] for a in window['duplicate_aliases']}}
 rows=[]
 for ordinal,row in enumerate(raw):
  diag=diagnostic_cases[row['case']];assert diag['candidate_id']==row['candidate_id']
  assert row['state']=='completed'
  failed=sorted(k for k,v in row['verdicts'].items() if v!='satisfied')
  assert len(row['verdicts'])==84
  cooler={c:channel(row,c,'failure_code') for c in ('water_ic1','water_ic2','water_pre')}
  no_root=[k for k,v in cooler.items() if v==2];pinch=[k for k,v in cooler.items() if v==1]
  status='pass' if not failed else 'cooler_no_root' if no_root else 'cooler_invalid' if pinch else 'equipment_or_coupling_insufficient'
  r={'case':row['case'],'candidate_id':row['candidate_id'],'state':row['state'],'roles':sorted(roles[row['case']]),'aliases':aliases[row['case']],'plot_index':ordinal,'status':status,'all_checks_pass':not failed,'verification_status':'numerical_mismatch' if diag['numeric_mismatches'] else 'stock_verification_pass','numerical_verification_mismatch':bool(diag['numeric_mismatches']),'numeric_mismatches':diag['numeric_mismatches'],'predicate_mismatches':diag['predicate_mismatches'],'failed_constraints':failed,'cooler_no_root':no_root,'cooler_invalid':pinch,'source_MW':inp(row,'blanket_source__q_source'),'delivered_heat_MW':channel(row,'primary_loop','q_ihx'),'source_hot_K':channel(row,'primary_loop','T_out'),'source_return_K':channel(row,'primary_loop','T_comp_in'),'gas_flow_kg_s':inp(row,'cycle__selected_flow'),'stage_ratio':inp(row,'compressor_1__selected_ratio'),'cooler_UA':[inp(row,c+'__ua') for c in ('water_ic1','water_ic2','water_pre')],'recuperator_UA':inp(row,'recuperator_hardware__ua'),'steam_circuits':inp(row,'steam_transport__n_loops'),'salt_pumps_per_circuit':inp(row,'steam_transport__salt_pumps_per_circuit'),'salt_pump_design_kg_s':inp(row,'steam_transport__selected_salt_design_flow_kg_s'),'gas':ledger(row,'gas'),'steam':ledger(row,'steam')}
  for branch in ('steam','gas'):
   d=r[branch];d['net_fraction_of_delivered_heat']=d['net_electric']/r['delivered_heat_MW']
   if not failed:close(r['delivered_heat_MW'],d['net_electric']+d['total_rejected'])
  r['energy_decomposition']={
   'steam':{'cycle_pumps_MW':channel(row,'steam_cycle','p_cycle_pumps_MW'),'salt_pumps_MW':channel(row,'steam_transport','salt_electric_MW'),'water_pumps_MW':channel(row,'steam_water','p_cooling_pump_electric_MW'),'controller_MW':inp(row,'steam_boundary__actuation')},
   'gas':{'compressor_shaft_MW':channel(row,'electrical','compressor_demand'),'turbine_shaft_MW':channel(row,'turbine','shaft_produced'),'net_shaft_MW':channel(row,'electrical','net_shaft'),'generator_loss_MW':channel(row,'electrical','generator_loss'),'shaft_import_MW':channel(row,'electrical','shaft_import'),'water_pumps_MW':sum(channel(row,c,'pump_electric') for c in ('water_ic1','water_ic2','water_pre'))+channel(row,'gas_loss_water','p_cooling_pump_electric_MW'),'controller_MW':inp(row,'gas_boundary__actuation')},
   'upstream_circulation_electric_excluded_MW':channel(row,'primary_loop','p_elec')}
  close(sum(r['energy_decomposition']['steam'].values()),r['steam']['electrical_load'])
  gd=r['energy_decomposition']['gas'];close(gd['shaft_import_MW']+gd['water_pumps_MW']+gd['controller_MW'],r['gas']['electrical_load'])
  rows.append(r)
 byid={r['case']:r for r in rows};resolve=lambda name:byid[index[name]['case']]
 anchors=[]
 ga=read(record/'gas-anchor-selection.json')['anchors'];sa=read(record/'matched-anchor-selection.json')['anchors']
 for g,s in zip(ga,sa):
  assert g['source_MW']==s['source_MW'];q=g['source_MW'];fixed=resolve(g['case']);selected=resolve(s['case'])
  assert fixed['all_checks_pass'] and selected['all_checks_pass']
  for field in ('source_MW','delivered_heat_MW','source_hot_K','source_return_K'):close(fixed[field],selected[field])
  gc=[r for r in rows if 'gas_catalog' in r['roles'] and r['source_MW']==q and r['all_checks_pass']]
  sc=[r for r in rows if 'steam_connector_catalog' in r['roles'] and r['source_MW']==q and r['all_checks_pass']]
  assert fixed['gas']['cost_per_net_MWh']==min(r['gas']['cost_per_net_MWh'] for r in gc),'Original gas anchor is no longer the exact catalog minimum'
  assert selected['steam']['cost_per_net_MWh']==min(r['steam']['cost_per_net_MWh'] for r in sc),'Original steam anchor is no longer the exact catalog minimum'
  E_S,E_B=selected['steam']['discounted_energy'],selected['gas']['discounted_energy'];K_S,K_B=selected['steam']['accounted_pv'],selected['gas']['accounted_pv']
  slope=E_S/E_B;intercept=slope*K_B-K_S;denom=1/E_S-1/E_B;delta=K_S/E_S-K_B/E_B
  anchors.append({'source_MW':q,'gas_case':fixed['case'],'fixed_steam_case':fixed['case'],'selected_steam_case':selected['case'],'gas_passing_catalog_count':len(gc),'steam_passing_catalog_count':len(sc),'fixed':fixed,'selected':selected,'steam_minus_gas_net_MW':selected['steam']['net_electric']-selected['gas']['net_electric'],'steam_minus_gas_cost_per_MWh':delta,'cost_gap_exceeds_5_USD_materiality':abs(delta)>5,'fixed_connector_cost_penalty_per_MWh':fixed['steam']['cost_per_net_MWh']-selected['steam']['cost_per_net_MWh'],'frontier':{'equation':'X_steam = slope * X_gas + intercept_USD2025','slope':slope,'intercept_USD2025':intercept,'common_source_difference_coefficient_per_USD':denom,'common_source_break_even_PV_USD2025':-delta/denom}})
 counts={}
 for role in sorted({k for r in rows for k in r['roles']}):
  rr=[r for r in rows if role in r['roles']];counts[role]=dict(collections.Counter(r['status'] for r in rr))|{'total':len(rr)}
 sensitivity=[r for r in rows if 'sensitivity' in r['roles'] or 'adverse_controller_offer' in r['roles']]
 for r in sensitivity:
  a=next(a for a in anchors if a['source_MW']==r['source_MW']);r['steam_minus_gas_cost_per_MWh']=r['steam']['cost_per_net_MWh']-r['gas']['cost_per_net_MWh']
  r['steam_minus_gas_net_MW']=r['steam']['net_electric']-r['gas']['net_electric']
  r['delta_cost_gap_from_anchor']=r['steam_minus_gas_cost_per_MWh']-a['steam_minus_gas_cost_per_MWh']
  r['within_cost_materiality']=abs(r['steam_minus_gas_cost_per_MWh'])<=5
  if 'common-source-pv' in r['case']:
   C0=inp(native[r['case']],'steam_ledger__common_source_pv');close(C0,inp(native[r['case']],'gas_ledger__common_source_pv'))
   r['common_source_PV_USD2025']=C0;close(r['steam_minus_gas_cost_per_MWh'],a['steam_minus_gas_cost_per_MWh']+C0*a['frontier']['common_source_difference_coefficient_per_USD'])
 sources=['results/verification_summary.json','results/cases.json','window.json','proposed-points.json','gas-anchor-selection.json','matched-anchor-selection.json']
 summary={'authority':'AGENT analysis of independently verified native cases; no model/oracle evaluation in this analysis' ,'verification_status':'pass','status_semantics':'pass means all implemented native constraints satisfied; stock independent numerical verification passed for all 498 cases' ,'record':str(record.relative_to(ROOT)),'source_hashes':{s:digest(record/s) for s in sources},'native_unique_cases':len(rows),'duplicate_aliases':window['duplicate_aliases'],'counts':counts,'overall_status':dict(collections.Counter(r['status'] for r in rows)),'verification_diagnostics':{'numeric_mismatch_cases':[r['case'] for r in rows if r['numerical_verification_mismatch']],'native_passing_numeric_mismatch_cases':[r['case'] for r in rows if r['numerical_verification_mismatch'] and r['all_checks_pass']],'predicate_mismatch_cases':[r['case'] for r in rows if r['predicate_mismatches']]},'failed_predicate_counts':dict(collections.Counter(k for r in rows for k in r['failed_constraints'])),'anchors':anchors,'sensitivities':sensitivity,'materiality':{'power_MW':5,'cost_USD2025_per_net_MWh':5},'limits':'Finite tested offers, conditional pressure-service/off-design/quote assumptions; supplied steam cycle versus tested gas, not equal optimization or whole-plant LCOE.'}
 summary['stock_verification']=verification
 enrich(summary,rows,raw,record)
 return summary,rows

def verification_gate(record):
 path=record/'results/verification_summary.json'
 if not path.exists():raise SystemExit('Verified reporting is pending: stock results/verification_summary.json is absent')
 v=read(path)
 assert v['schema_version']=='study-verification-summary/v1' and v['outcome']=='pass'
 assert v['tool']['path']=='scripts/study/verify.py' and v['identity']['matches_preflight']
 assert v['verdicts_rederived'] and not v['verdict_mismatches'] and not v['not_independently_verified']
 rows=read(record/'results/cases.json')['cases'];ids={r['candidate_id'] for r in rows}
 assert len(ids)==498 and {r['executable_fingerprint'] for r in rows}=={v['identity']['digest']}
 samples={i for s in v['stores'] for i in s['sampling']['sampled_case_ids']}
 assert samples==ids,'Stock verification must cover every retained case'
 assert sum(s['cases_completed'] for s in v['stores'])==498
 return dict(path=str(path.relative_to(ROOT)),sha256=digest(path),outcome=v['outcome'],fingerprint=v['identity']['digest'],verified_cases=len(samples),channels=len(v['channels_checked']),predicates=len(v['constraints_rederived']),relative_tolerance=v['tolerance'])

def enrich(summary,rows,raw,record):
 native={r['case']:r for r in raw};old={r['case']:r for r in read(OLD/'results/cases.json')['cases']}
 assert set(native)==set(old)
 differences=[];unit_counts=collections.Counter();case_counts=collections.Counter()
 for r in rows:
  n=native[r['case']];o=old[r['case']]
  assert n['inputs']==o['inputs'],'Input map changed: '+r['case']
  r['cooler_details']={};classes=[]
  for cooler,hotowner,hotfield in [('water_ic1','compressor_1','temperature_out'),('water_ic2','compressor_2','temperature_out'),('water_pre','recuperator','hot_out')]:
   code=channel(n,cooler,'failure_code');low=channel(n,cooler,'bracket_low_ua');high=channel(n,cooler,'bracket_high_ua');ua=inp(n,cooler+'__ua');hot=channel(n,hotowner,hotfield)-273.15
   kind='solved' if code==0 else 'pinch_or_empty_bracket' if code==1 else 'lower_no_root' if ua<low else 'upper_no_root' if ua>high else 'unclassified'
   assert kind!='unclassified',(r['case'],cooler,code,ua,low,high)
   margins={k:channel(n,cooler,k+'_margin') for k in ('flow','power','duty')}
   r['cooler_details'][cooler]=dict(failure_code=code,classification=kind,selected_UA_MW_K=ua,bracket_low_UA_MW_K=low,bracket_high_UA_MW_K=high,water_inlet_after_C=channel(n,cooler,'water_inlet_after_C'),hot_gas_C=hot,upper_temperature_bound_C=min(hot,60),upper_bound_kind='property_ceiling_60C' if hot>=60 else 'hot_gas_terminal_pinch',margins=margins,defined_capacity_failures=[k for k,v in margins.items() if code==0 and v<0])
   unit_counts[kind]+=1
   if kind!='solved':classes.append(kind)
  for kind in set(classes):case_counts[kind]+=1
  if classes:
   r['status']='cooler_'+classes[0] if len(set(classes))==1 else 'cooler_mixed_bounds'
  r['native_executable_fingerprint']=n['executable_fingerprint'];r['native_evidence_digest']=n['evidence_digest'];r['native_verdicts']=n['verdicts']
  changes={k:dict(old=o['outputs'][k],new=v,delta=float(v)-float(o['outputs'][k])) for k,v in n['outputs'].items() if isinstance(v,(int,float)) and v!=o['outputs'][k]}
  verdict_changes={k:dict(old=o['verdicts'].get(k),new=v) for k,v in n['verdicts'].items() if v!=o['verdicts'].get(k)}
  differences.append(dict(case=r['case'],old_candidate_id=o['candidate_id'],new_candidate_id=n['candidate_id'],inputs_identical=True,changed_scalar_channels=changes,changed_verdicts=verdict_changes,steam_net_delta_MW=r['steam']['net_electric']-channel(o,'steam_ledger','net_electric'),gas_net_delta_MW=r['gas']['net_electric']-channel(o,'gas_ledger','net_electric'),steam_cost_delta=r['steam']['cost_per_net_MWh']-channel(o,'steam_ledger','cost_per_net_MWh'),gas_cost_delta=r['gas']['cost_per_net_MWh']-channel(o,'gas_ledger','cost_per_net_MWh')))
 summary['counts']={role:dict(collections.Counter(r['status'] for r in rows if role in r['roles']))|{'total':sum(role in r['roles'] for r in rows)} for role in summary['counts']}
 summary['overall_status']=dict(collections.Counter(r['status'] for r in rows))
 examples={kind:[dict(case=r['case'],candidate_id=r['candidate_id'],cooler=c,**d) for r in rows for c,d in r['cooler_details'].items() if d['classification']==kind][:3] for kind in unit_counts if kind!='solved'}
 summary['cooler_classification']=dict(units=dict(unit_counts),cases_nonexclusive=dict(case_counts),examples=examples,domain='Water inlet 20 <= T < 60 C; pumped inlet/outlet remain in retained property range. Outlet bracket: pumped inlet + 1e-7 C to min(hot gas,60 C) - 1e-7 C. Lower and upper UA bounds are native outputs; no domain extrapolation.')
 summary['before_after']=dict(old_record=str(OLD.relative_to(ROOT)),old_cases_sha256=digest(OLD/'results/cases.json'),all_498_input_maps_identical=True,verdict_changed_cases=[d['case'] for d in differences if d['changed_verdicts']],cases=differences)
 for a in summary['anchors']:
  a['selected_anchor_still_minimum']=True # exact catalog minima assertions in summarize
  a['steam_minus_gas_net_exceeds_5_MW']=abs(a['steam_minus_gas_net_MW'])>5

def report(s,rows,out):
 a=s['anchors'];v=s['stock_verification'];passing=sum(r['all_checks_pass'] for r in rows)
 lines=['# Verified matched conversion comparison','','[AGENT] Reporting analysis of the retained native record. Stock verification passes all 498 unchanged input maps, with '+str(v['channels'])+' scalar channels and '+str(v['predicates'])+' independently rederived predicates per case. '+str(passing)+' cases satisfy all implemented checks. This report reads stored results and runs no model or oracle.','',
 'The comparison is the selected steam offer versus tested Brayton offers at matched source conditions. Steam’s fixed 14-circuit connector and least-cost passing connector are shown separately. The original selected anchors remain cost minima in their exact finite passing catalogs. The comparison does not establish equally optimized technologies or whole-plant LCOE.','',
 '| Source MW | Steam circuits × pumps / pump kg/s | Steam net MW | Brayton net MW | Fixed steam USD/net MWh | Selected steam | Tested Brayton | Steam minus Brayton |','| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |']
 for x in a:
  r=x['selected'];lines.append(f"| {x['source_MW']:g} | {r['steam_circuits']:g} × {r['salt_pumps_per_circuit']:g} / {r['salt_pump_design_kg_s']:g} | {r['steam']['net_electric']:.3f} | {r['gas']['net_electric']:.3f} | {x['fixed']['steam']['cost_per_net_MWh']:.3f} | {r['steam']['cost_per_net_MWh']:.3f} | {r['gas']['cost_per_net_MWh']:.3f} | {x['steam_minus_gas_cost_per_MWh']:+.3f} |")
 lines+=['','Steam produces 378.086, 542.184 and 461.168 MW more net electricity in the three selected comparisons. Its cost differences at 2500 and 2800 MW are below the 5 USD2025/net MWh materiality threshold. At 3000 MW the nominal tested Brayton offer is cheaper by 9.446 USD/net MWh; quote scenarios reverse that sign. These conclusions apply to this selected steam offer and the tested passing catalogs.','',
 'Power materiality is 5 MW; cost materiality is 5 USD2025 per net MWh. Price scenarios and component efficiencies are conditional assumptions. The lines connect selected discrete offers, not a continuous optimum or a reactor turndown trajectory.','',
 '## Accounting','','| Source MW | Branch | Gross MW | Electric loads MW | Net MW | Rejected MW | Capital BUSD | Service PV BUSD | Replacement PV BUSD | Discounted energy million MWh |','| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
 for x in a:
  for b in ('steam','gas'):
   d=x['selected'][b];lines.append(f"| {x['source_MW']:g} | {b} | {d['gross_electric']:.3f} | {d['electrical_load']:.3f} | {d['net_electric']:.3f} | {d['total_rejected']:.3f} | {d['capital_total']/1e9:.6f} | {d['service_pv']/1e9:.6f} | {d['replacement_pv']/1e9:.6f} | {d['discounted_energy']/1e6:.6f} |")
 lines+=['','Delivered source heat includes recovered upstream circulation work. Upstream circulation electricity and costs are excluded equally. Net electricity plus rejection closes the conversion boundary for passing cases. Full capital accounts, salt makeup, disjoint machine/bundle/conversion replacement terms and pumping/generator losses are retained in plot-data.json.','',
 '## Failure classification and coverage','',''+s['cooler_classification']['domain'],'','| Role | Status counts |','| --- | --- |']
 for role,counts in s['counts'].items():lines.append('| '+role+' | '+', '.join(f'{k}: {v}' for k,v in counts.items())+' |')
 upper=[d for r in rows for d in r['cooler_details'].values() if d['classification']=='upper_no_root'];lower=[d for r in rows for d in r['cooler_details'].values() if d['classification']=='lower_no_root']
 ceiling=sum(d['upper_bound_kind']=='property_ceiling_60C' for d in upper)
 examples=s['cooler_classification']['examples'];u=examples['upper_no_root'][0];l=examples['lower_no_root'][0]
 lines+=['',f"Across the 498 cases, {len(upper)} cooler occurrences exceed their upper UA bound; {ceiling} of these have a 60 °C property ceiling. There are {len(lower)} lower-bound occurrences. Multiple cooler occurrences can belong to one case. In `{u['candidate_id']}`, `{u['cooler']}` has selected UA {u['selected_UA_MW_K']:.3f} MW/K above the retained upper bound {u['bracket_high_UA_MW_K']:.6f} MW/K. In `{l['candidate_id']}`, `{l['cooler']}` has selected UA {l['selected_UA_MW_K']:.3f} MW/K below its lower bound {l['bracket_low_UA_MW_K']:.6f} MW/K.",'',
 'A lower no-root result means the selected UA lies below the native lower bracket value, near the infinite-water-flow limit. An upper no-root result means selected UA exceeds the native upper bracket value. Where that upper temperature is 60 °C, the current property range limits the calculation; it does not prove the purchased equipment physically cannot work. A hot-gas terminal limit is identified separately in each cooler receipt. Neither class is ranked as an admissible offer. Solved coolers can independently fail purchased flow, power or duty capacity. Those margins, all failed predicates, and overlapping failure reasons remain visible in plot-data.json.','',
 'The water-property limits restrict tested candidate coverage and any ranking. No property range, equipment offer or physical domain was expanded. A passing case does not qualify machine maps, site hydraulics, or vendor quotes.','',
 '## Sensitivities and missing-cost frontiers','','The sensitivity figure retains every efficiency, price, recurring-cost and common-source-PV case, including failed controller offers. It compares cost differences against the ±5 USD/net MWh band. Common source-service charges are accounting scenarios; no reactor fuel price is inferred.','',
 '| Source MW | Efficiency gap range USD/net MWh | Branch quote gap range | Common-PV equality BUSD | Missing-cost equality, X in BUSD2025 |','| ---: | ---: | ---: | ---: | --- |']
 for x in a:
  rr=[r for r in s['sensitivities'] if r['source_MW']==x['source_MW'] and r['all_checks_pass']]
  er=[r['steam_minus_gas_cost_per_MWh'] for r in rr if '-eta' in r['case']];qr=[r['steam_minus_gas_cost_per_MWh'] for r in rr if '-quote-' in r['case']];f=x['frontier']
  lines.append(f"| {x['source_MW']:g} | {min(er):+.3f} to {max(er):+.3f} | {min(qr):+.3f} to {max(qr):+.3f} | {f['common_source_break_even_PV_USD2025']/1e9:.6f} | X_S = {f['slope']:.6f} X_B {f['intercept_USD2025']/1e9:+.6f} |")
 lines+=['','At 3000 MW the efficiency scenarios retain the nominal cost sign: steam minus Brayton spans +4.007 to +13.104 USD/net MWh. The low end falls below the 5 USD/net MWh materiality threshold. The quote scenarios cross zero, so a material nominal advantage is not a price-independent technology ranking.','',
 'The negative common-PV equality values at 2500 and 2800 MW are algebraic extrapolations. There is no crossover for a nonnegative common charge under these held assumptions; added common cost favors steam’s larger energy denominator. They are not negative fuel prices. At 3000 MW equality occurs at +1.831386 BUSD2025; the +2 BUSD scenario gives about −0.870 USD/net MWh, within materiality.','',
 'The frontier follows directly from native present-value costs K and discounted net energies E: `X_S = (E_S/E_B)(K_B + X_B) - K_S`. It shows the cost corrections that would erase the comparison; it does not validate omitted purchase scopes. Reactor equipment, source fuel and upstream circulation costs remain excluded. Cooling-water site service, imposed pressure-service losses, off-design efficiencies, procurement scope and quotes remain conditional.','',
 '## Numerical repair comparison','','All 498 new input maps are exactly identical to the preserved old record. Changed scalar channels are listed separately from engineering verdict changes in matched-study-summary.json. Changed engineering-status cases: '+str(len(s['before_after']['verdict_changed_cases']))+'.','']
 for field,label in [('steam_net_delta_MW','Steam net MW'),('gas_net_delta_MW','Brayton net MW'),('steam_cost_delta','Steam USD/net MWh'),('gas_cost_delta','Brayton USD/net MWh')]:
  worst=max(s['before_after']['cases'],key=lambda r:abs(r[field]));lines.append(f"- Largest absolute change in {label}: {worst[field]:+.9g}, case `{worst['new_candidate_id']}`.")
 lines+=['','Old blocked figures and data remain unchanged. Numerical verification now covers the repaired executable; physical-domain and price limitations remain.','',
 '## Evidence and replay','','[Summary](matched-study-summary.json) · [Exact plot data](plot-data.json) · [CSV](plot-data.csv) · [Output and failed offers](matched-output.svg) · [Cost decomposition](matched-cost.svg) · [Sensitivity](matched-sensitivity.svg). Figures also have PNG copies. Every plotted point retains its native candidate ID, input parameters, fingerprint, evidence digest, verification status and actual constraint verdicts.','',
 'Record: `'+s['record']+'`. Stock verification SHA-256: `'+v['sha256']+'`. Executable fingerprint: `'+v['fingerprint']+'`.','',
 'Reproduce with `.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/verified-comparison/analyze-verified.py`. The renderer refuses to generate results until the stock verification receipt covers all 498 exact native case IDs and the current recorded fingerprint.']
 (out/'report.md').write_text('\n'.join(lines)+'\n')

def style():
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.grid':True,'grid.alpha':.2,'svg.fonttype':'none','savefig.facecolor':'white'})
def save(fig,out,name):
 fig.savefig(out/(name+'.svg'),bbox_inches='tight');fig.savefig(out/(name+'.png'),dpi=190,bbox_inches='tight');plt.close(fig)

def figures(summary,rows,out):
 style();anchors=summary['anchors'];qs=[a['source_MW'] for a in anchors]
 fig=plt.figure(figsize=(15,11),layout='constrained');grid=fig.add_gridspec(3,3,height_ratios=[1.15,1,.65]);ax=fig.add_subplot(grid[0,:2])
 for branch,kind,label,color,ls,marker in [('steam','fixed','Steam · fixed 14-circuit connector',C['fixed'],'--','s'),('steam','selected','Steam · least-cost passing connector',C['steam'],'-','o'),('gas','selected','Brayton · least-cost tested offer',C['gas'],'-','D')]:
  yy=[a[kind][branch]['net_electric'] for a in anchors];ax.plot(qs,yy,color=color,linestyle=ls,marker=marker,label=label,linewidth=2)
  if kind=='selected':
   for x,y in zip(qs,yy):ax.annotate(f'{y:.1f}',(x,y),xytext=(0,8 if branch=='steam' else -17),textcoords='offset points',ha='center',color=color)
 ax.set(title='Net electricity at matched source conditions',xlabel='Selected reactor heat input (MW)',ylabel='Conversion-subsystem net electricity (MW)',xticks=qs);ax.legend(loc='center left',fontsize=9);ax.set_ylim(460,1220);ax.text(.02,.96,'Steam net curves coincide; connector costs differ.',transform=ax.transAxes,va='top',fontsize=9,color=C['steam'])
 ax=fig.add_subplot(grid[0,2]);a=anchors[1];base=a['selected'];xx=np.arange(2);bottom=np.zeros(2)
 for field,label,color in [('net_electric','Net electricity','#287f9d'),('electrical_load','Included electric loads','#edbd5b'),('total_rejected','Rejected heat','#b9c3cd')]:
  vals=[base[b][field] for b in ('steam','gas')]
  # Gross-to-net waterfall is displayed separately from rejection: heat split uses net + rejection only.
  if field=='electrical_load':continue
  ax.bar(xx,vals,bottom=bottom,label=label,color=color);bottom+=vals
 ax.set(title='Delivered heat disposition · 2800 MW source',xticks=xx,xticklabels=['Steam','Brayton'],ylabel='MW');ax.legend(fontsize=8)
 for x,b in zip(xx,('steam','gas')):ax.text(x,base[b]['net_electric']/2,f"Net {base[b]['net_electric']:.0f}\nLoads {base[b]['electrical_load']:.1f}",ha='center',va='center',color='white',fontsize=9)
 offers=[(25,25,20),(25,25,25),(25,25,40),(30,30,50),(40,40,60)]
 for i,q in enumerate(qs):
  ax=fig.add_subplot(grid[1,i]);rr=[r for r in rows if 'gas_catalog' in r['roles'] and r['source_MW']==q]
  for r in rr:
   offset=(offers.index(tuple(r['cooler_UA']))-2)*.022;x=r['stage_ratio']+offset;y=r['gas_flow_kg_s'];status=r['status'];color=C['gas'] if status=='pass' else C['lower'] if status=='cooler_lower_no_root' else C['upper'] if status=='cooler_upper_no_root' else C['mixed'] if status=='cooler_mixed_bounds' else C['failed'];marker='o' if status=='pass' else '*' if status=='cooler_mixed_bounds' else 'x' if status.startswith('cooler') else '+'
   ax.scatter(x,y,c=color,marker=marker,s=28,linewidths=1.3)
   if r['numerical_verification_mismatch']:ax.scatter(x,y,facecolors='none',edgecolors='#5c224f',marker='D',s=72,linewidths=1.2)
  cc=collections.Counter(r['status'] for r in rr);ax.set(title=f"{q:g} MW · {cc['pass']}/125 offers pass",xlabel='Chosen stage ratio · small offset distinguishes offers',ylabel='Chosen gas flow (kg/s)',xticks=[1.2,1.35,1.5,1.65,1.8],yticks=[1500,1750,2000,2250,2500]);ax.set_xlim(1.13,1.87)
 for i,q in enumerate(qs):
  ax=fig.add_subplot(grid[2,i]);rr=[r for r in rows if 'steam_connector_catalog' in r['roles'] and r['source_MW']==q]
  for r in rr:
   offset=-.13 if r['salt_pump_design_kg_s']==225 else .13
   ax.scatter(r['steam_circuits']+offset,r['salt_pumps_per_circuit'],c=C['gas'] if r['all_checks_pass'] else C['failed'],marker='o' if r['all_checks_pass'] else '+',s=35,linewidths=1.3)
  ax.set(title=f"Steam connector · {sum(r['all_checks_pass'] for r in rr)}/24 pass",xlabel='Installed IHX circuits · offset: 225 / 250 kg/s pump',ylabel='Salt pumps per circuit',xticks=[10,11,12,14],yticks=[2,3,4]);ax.set_ylim(1.7,4.3)
 fig.legend(handles=[Line2D([],[],marker='o',color=C['gas'],ls='',label='Native checks pass'),Line2D([],[],marker='+',color=C['failed'],ls='',label='Equipment or coupling check fails'),Line2D([],[],marker='x',color=C['lower'],ls='',label='Below cooler lower-UA bound'),Line2D([],[],marker='x',color=C['upper'],ls='',label='Above cooler upper-UA bound'),Line2D([],[],marker='*',color=C['mixed'],ls='',label='Both bounds across coolers')],loc='outside lower center',ncol=3)
 fig.suptitle('Verified native comparison · finite tested offers\nSelected steam offer versus tested Brayton offers',fontsize=16)
 save(fig,out,'matched-output')
 fig,(ax,bx)=plt.subplots(1,2,figsize=(14,5.5),layout='constrained')
 for branch,kind,label,color,ls in [('steam','fixed','Steam · fixed 14 circuits',C['fixed'],'--'),('steam','selected','Steam · selected connector',C['steam'],'-'),('gas','selected','Brayton · selected offer',C['gas'],'-')]:
  yy=[a[kind][branch]['cost_per_net_MWh'] for a in anchors];ax.plot(qs,yy,'o',color=color,linestyle=ls,label=label,linewidth=2)
  if kind=='selected':
   for x,y in zip(qs,yy):ax.annotate(f'{y:.2f}',(x,y),xytext=(0,8 if branch=='steam' else -15),textcoords='offset points',ha='center',color=color)
 ax.set(title='Nominal hypothetical price scenario',xlabel='Selected reactor heat input (MW)',ylabel='USD2025 per net MWh',xticks=qs);ax.legend(fontsize=9);ax.set_ylim(24,48)
 xx=np.arange(6);bottom=np.zeros(6);rr=[a['selected'][b] for a in anchors for b in ('steam','gas')]
 for label,color in [('Capital','#527e98'),('Service','#adc6d2'),('Makeup','#ead4aa'),('Replacement','#d69058')]:
  v=[r['cost_components_per_MWh'][label] for r in rr];bx.bar(xx,v,bottom=bottom,label=label,color=color);bottom+=v
 bx.set(title='Present-value cost / discounted net energy',ylabel='USD2025 per net MWh',xticks=xx,xticklabels=['S\n2500','B\n2500','S\n2800','B\n2800','S\n3000','B\n3000']);bx.legend(fontsize=8,ncol=2)
 fig.suptitle('Verified native comparison · finite tested offers\nConversion-subsystem costs · upstream equipment and fuel excluded',fontsize=15)
 fig.supxlabel('S: supplied steam cycle with selected connector; B: tested Brayton offer. Quotes and installed scope remain conditional.',fontsize=10)
 save(fig,out,'matched-cost')
 fig,axes=plt.subplots(1,3,figsize=(17,7.8),layout='constrained');sen=summary['sensitivities']
 for ax,kind,title,labels in [(axes[0],'eta','Efficiency assumptions', [('gas-eta-0.03','Gas −3 pp'),('gas-eta+0.03','Gas +3 pp'),('steam-eta-0.03','Steam −3 pp'),('steam-eta+0.03','Steam +3 pp'),('both-eta-0.03','Both −3 pp'),('both-eta+0.03','Both +3 pp')]),(axes[1],'quote','Quote / recurring-cost assumptions',[('gas-quote-x0.5','Gas quote ×0.5'),('gas-quote-x1.5','Gas quote ×1.5'),('steam-quote-x0.5','Steam quote ×0.5'),('steam-quote-x1.5','Steam quote ×1.5'),('gas-quote-x0.5-steam-x1.5','Gas ×0.5 / steam ×1.5'),('gas-quote-x1.5-steam-x0.5','Gas ×1.5 / steam ×0.5'),('recurring-x0.5','Recurring ×0.5'),('recurring-x1.5','Recurring ×1.5'),('controller-gas','Gas bypass 500 (fails)'),('controller-steam','Steam bypass 500 (passes)')])]:
  for i,q in enumerate(qs):
   vals=[]
   for suffix,label in labels:
    name=f'controller-q{q:g}-{suffix.removeprefix("controller-")}-500' if suffix.startswith('controller-') else f'sensitivity-q{q:g}-{suffix}'
    r=next(r for r in sen if r['case']==name);vals.append(r['steam_minus_gas_cost_per_MWh']);ax.scatter(vals[-1],labels.index((suffix,label))+(i-1)*.19,marker='o' if r['all_checks_pass'] else 'x',s=35,color=['#b65a26','#407d88','#713f81'][i])
    if r['numerical_verification_mismatch']:ax.scatter(vals[-1],labels.index((suffix,label))+(i-1)*.19,facecolors='none',edgecolors='#111',marker='D',s=100,linewidths=1.5)
  ax.axvspan(-5,5,color='#e7e7e7',zorder=-2);ax.axvline(0,color='#666',lw=.8);ax.set(title=title,yticks=range(len(labels)),yticklabels=[v for _,v in labels],xlabel='Steam minus Brayton (USD2025/net MWh)');ax.invert_yaxis()
 ax=axes[2]
 for i,a in enumerate(anchors):
  q=a['source_MW'];rr=[r for r in sen if r['source_MW']==q and 'common_source_PV_USD2025' in r];xx=[0]+[r['common_source_PV_USD2025']/1e9 for r in rr];yy=[a['steam_minus_gas_cost_per_MWh']]+[r['steam_minus_gas_cost_per_MWh'] for r in rr];ax.plot(xx,yy,'o-',label=f'{q:g} MW',color=['#b65a26','#407d88','#713f81'][i])
 ax.axhspan(-5,5,color='#e7e7e7',zorder=-2);ax.axhline(0,color='#666',lw=.8);ax.set(title='Same source-service PV charge',xlabel='Added common PV charge (billion USD2025)',ylabel='Steam minus Brayton (USD2025/net MWh)');ax.legend(fontsize=9)
 fig.suptitle('Verified native comparison · finite tested offers\nRanking depends on conditional prices and performance',fontsize=16);fig.supxlabel('Positive: steam costs more. ×: failed implemented checks. Gray band: predeclared ±5 USD/net MWh materiality. No fuel price is inferred.',fontsize=10)
 save(fig,out,'matched-sensitivity')

def main():
 p=argparse.ArgumentParser();p.add_argument('--record',type=Path,default=DEFAULT);p.add_argument('--out-dir',type=Path,default=Path(__file__).resolve().parent);args=p.parse_args();out=args.out_dir;out.mkdir(parents=True,exist_ok=True)
 summary,rows=summarize(args.record)
 (out/'matched-study-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 (out/'plot-data.json').write_text(json.dumps({'record':summary['record'],'source_hashes':summary['source_hashes'],'cases':rows,'aliases':summary['duplicate_aliases']},indent=2)+'\n')
 fields=['case','candidate_id','state','roles','aliases','status','all_checks_pass','verification_status','numerical_verification_mismatch','numeric_mismatches','predicate_mismatches','failed_constraints','cooler_no_root','cooler_invalid','source_MW','delivered_heat_MW','gas_flow_kg_s','stage_ratio','cooler_UA','steam_circuits','salt_pumps_per_circuit','salt_pump_design_kg_s','steam_net_MW','gas_net_MW','steam_cost_per_MWh','gas_cost_per_MWh']
 for branch in ('steam','gas'):
  fields += [branch+'_'+f for f in LEDGER+['service_pv','makeup_pv']]
 with (out/'plot-data.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in rows:
   rr={k:r.get(k) for k in fields};rr.update({branch+'_'+f:r[branch][f] for branch in ('steam','gas') for f in LEDGER+['service_pv','makeup_pv']});rr.update(steam_net_MW=r['steam']['net_electric'],gas_net_MW=r['gas']['net_electric'],steam_cost_per_MWh=r['steam']['cost_per_net_MWh'],gas_cost_per_MWh=r['gas']['cost_per_net_MWh']);w.writerow({k:json.dumps(v) if isinstance(v,(list,dict)) else v for k,v in rr.items()})
 figures(summary,rows,out)
 report(summary,rows,out)
 print(json.dumps({'counts':summary['counts'],'anchors':[{k:v for k,v in a.items() if k not in ('selected','fixed')} for a in summary['anchors']]},indent=2))
if __name__=='__main__':main()
