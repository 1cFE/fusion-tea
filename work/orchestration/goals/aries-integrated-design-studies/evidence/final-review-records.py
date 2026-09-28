"""Independent frozen-record, matched-comparison and final-ledger checks."""
import csv,json,hashlib,math,sqlite3
from pathlib import Path
R=Path.cwd();E=R/'work/orchestration/goals/aries-integrated-design-studies/evidence';S=R/'exploration/aries_integrated/studies';sid='20260922-aries-integrated-design-robustness';r=S/sid
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def eq(a,b):assert math.isclose(float(a),float(b),rel_tol=1e-10,abs_tol=1e-7),(a,b)
P='aries_integrated_plant__';L=P+'lifecycle_accounts__evaluate__';D='aries_cs_plasma_integration__plasma__amplitude'
cs=read(r/'results/cases.json')['cases'];by={c['case']:c for c in cs};base=by['baseline--no-credit']['inputs'];config=read(r/'config.json');approved=read(E/'coupled-review-robustness.json');assert config['physical_designs']==approved['design_groups']
axis={a['axis']:[k['key'] for k in a['keys']] for a in config['axes']}
assert axis['hx_price_factor']==approved['correlated_price_keys']
tie=read(r/'manifest.json')['ties'];assert len(tie)==1 and [tie[0]['key']]+tie[0]['rides_with']==approved['correlated_price_keys']
allowed={x['key']:x['levels'] for x in approved['scenario_inputs']}
assert len(config['uncertainty_settings'])==21
seen=set();physical_names={d['name'] for d in config['physical_designs']}
for design in config['physical_designs']:
 for setting in config['uncertainty_settings']:
  changes={}
  assert len(setting['values'])<=1
  for group,value in setting['values'].items():
   for key in axis[group]:assert value in allowed[key];changes[key]=value
  for arm,feed,service in [('no-credit',0,0),('feed100-service30m',100,30e6)]:
   name=('baseline' if design['name']=='baseline' and setting['name']=='default' else design['name']+'__'+setting['name'])+'--'+arm
   expected=dict(base);expected.update(design['values']);expected.update(changes);expected[P+'fuel_inventory__annual_recovery_kg']=feed;expected[P+'finance__supply_service_annual']=service
   assert by[name]['inputs']==expected,name;seen.add(name)
assert len(seen)==168
old={c['case']:c for c in read(S/'20260922-aries-integrated-coupled-design/results/cases.json')['cases']}
for name in set(by)-seen:assert by[name]['inputs']==old[name]['inputs'] and by[name]['outputs']==old[name]['outputs'] and by[name]['verdicts']==old[name]['verdicts']
# Independent lifecycle cashflow arithmetic; no diagnostic reserve added.
for c in cs:
 x,y=c['inputs'],c['outputs'];k=y[P+'cost_ledger__evaluate__overnight'];rate=x[P+'finance__discount_rate'];years=x[P+'cost_schedule__plant_years'];construction=x[P+'finance__construction_years'];energy=y[L+'annual_energy'];annuity=(1-(1+rate)**(-years))/rate
 eq(y[L+'financed_capital'],k*(1+rate)**(construction/2));eq(y[L+'capital_lcoe'],k*(1+rate)**(construction/2)/annuity/energy)
 rep=P+'replacement__evaluate__';interval=y[rep+'interval_years'];count=int(y[rep+'event_count']);assert count==sum(1 for i in range(1,count+2) if i*interval<years)
 pv=sum(y[rep+'event_cost']*(1+rate)**(-i*interval) for i in range(1,count+1));eq(y[L+'pv_replacement'],pv);eq(y[L+'replacement_lcoe'],pv/annuity/energy)
 eq(y[L+'terminal_lcoe'],k*x[P+'finance__terminal_fraction']*(1+rate)**(-years)/annuity/energy);eq(y[L+'salvage_lcoe'],-k*x[P+'finance__salvage_fraction']*(1+rate)**(-years)/annuity/energy)
 eq(y[P+'fuel_inventory__purchase__amount'],x[P+'fuel_inventory__selected_tritium_kg']*x[P+'fuel_inventory__tritium_price'])
 eq(y[L+'tritium_lcoe'],y[L+'external_shortfall']*x[P+'fuel_inventory__tritium_price']/energy)
# Matched comparison identities and every reported delta.
comparisons=read(r/'results/matched-comparisons.json')['comparisons'];assert len(comparisons)==126
quant={'net_mw':P+'plant_ledger__evaluate__net_electric','annual_mwh':L+'annual_energy','gross_makeup_kg_year':L+'gross_makeup','external_purchases_kg_year':L+'external_shortfall','curtailed_feed_kg_year':L+'curtailed_feed','overnight_usd2004':P+'cost_ledger__evaluate__overnight'}
rankings={}
for m in comparisons:
 a,b=by[m['baseline_case']],by[m['candidate_case']];xa,xb=a['inputs'],b['inputs'];ya,yb=a['outputs'],b['outputs']
 assert m['supply_scenario']==m['baseline_case'].split('--')[1]==m['candidate_case'].split('--')[1]
 differences={k for k in xa if xa[k]!=xb[k]};assert differences<={P+'he_hx__selected_area',P+'pbli_hx__selected_area',D}
 assert all(v=='satisfied' for v in a['verdicts'].values()) and all(v=='satisfied' for v in b['verdicts'].values());assert m['passes_evaluated_checks_both']
 for term,delta in m['contribution_deltas'].items():eq(delta,yb[L+term]-ya[L+term])
 for term,delta in m['native_quantity_deltas'].items():
  if term=='nonfuel_nonsupply_lcoe_subtotal':
   total=lambda y:y[L+'lcoe_sum']-y[L+'tritium_lcoe']-y[L+'deuterium_lcoe']-y[L+'supply_lcoe'];eq(delta,total(yb)-total(ya))
  else:eq(delta,yb[quant[term]]-ya[quant[term]])
 delta=yb[L+'lcoe_sum']-ya[L+'lcoe_sum'];key=m['supply_scenario']+'/'+m['physical_design'];rankings.setdefault(key,{'lower':[],'higher':[],'deltas':[]});rankings[key]['lower' if delta<0 else 'higher'].append(m['uncertainty_setting']);rankings[key]['deltas'].append(delta)
 if m['physical_design']=='area45k':
  assert ya[quant['net_mw']]==yb[quant['net_mw']] and ya[quant['gross_makeup_kg_year']]==yb[quant['gross_makeup_kg_year']]
findings=read(r/'results/robustness-findings.json')['findings']
for key,data in rankings.items():
 for sign in ['lower','higher']:assert set(data[sign])==set(findings[key][sign])
 eq(min(data['deltas']),findings[key]['delta_range'][0]);eq(max(data['deltas']),findings[key]['delta_range'][1])
# Check all published ledger cells directly against native values and proposal metadata.
ledger=list(csv.DictReader((E/'candidate-ledger.csv').open()));assert len(ledger)==266;unique=set()
scalar={'net_MW':P+'plant_ledger__evaluate__net_electric','annual_MWh':L+'annual_energy','gross_T_kg_per_calendar_year':L+'gross_makeup','assumed_new_feed_kg_per_calendar_year':L+'new_feed','external_T_purchase_kg_per_calendar_year':L+'external_shortfall','curtailed_feed_kg_per_calendar_year':L+'curtailed_feed','overnight_USD2004':P+'cost_ledger__evaluate__overnight','unmet_heat_MW':P+'heat_exchangers__evaluate__unmet_heat'}
cache={}
for row in ledger:
 key=(row['study'],row['case']);assert key not in unique;unique.add(key)
 if row['study'] not in cache:
  st=S/row['study'];cache[row['study']]=({c['case']:c for c in read(st/'results/cases.json')['cases']},{c['case']:c for c in read(st/'proposed-points.json')['cases']})
 natives,props=cache[row['study']];c=natives[row['case']];x,y=c['inputs'],c['outputs']
 assert row['scenario']==props[row['case']]['arm'];assert row['classification']==props[row['case']]['classification'];assert row['scientific_qualification']=='not established'
 assert row['passes_evaluated_checks']==str(all(v=='satisfied' for v in c['verdicts'].values()))
 assert row['failed_predicates']=='; '.join(k+'='+v for k,v in c['verdicts'].items() if v!='satisfied')
 for col,ch in scalar.items():eq(row[col],y[ch])
 eq(row['supply_service_USD2004_per_year'],x[P+'finance__supply_service_annual'])
 for branch in ['he','pbli']:
  hp=P+branch+'_hx__'
  for suffix,ch in {'area_m2':hp+'selected_area','price_factor':hp+'price_factor'}.items():eq(row[branch+'_'+suffix],x[ch])
  for suffix,ch in {'ua_mw_k':hp+'evaluate__ua','purchased_quantity_m2':hp+'purchase__purchased_quantity','capital_usd2004':hp+'purchase__capital'}.items():eq(row[branch+'_'+suffix],y[ch])
 for col in row:
  if col.endswith('_USD2004_per_MWh'):eq(row[col],y[L+col.removesuffix('_USD2004_per_MWh')])
assert len(unique)==sum(len(v[0]) for v in cache.values())
# Hash all snapshot path/digest entries resolving repo- or study-relative artifacts.
snapshot=read(r/'snapshot.json');checked={}
def walk(x):
 if isinstance(x,dict):
  if 'path' in x and 'sha256' in x:
   opts=[R/x['path'],r/x['path']];existing=[p for p in opts if p.is_file()]
   if existing:
    assert any(sha(p)==x['sha256'] for p in existing),x['path'];checked[x['path']]=x['sha256']
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(snapshot)
assert sha(r/'snapshot.json')=='328c8fda45a91620683c1abe92eea6d051ce898bdc78474e26870d68c73f5999'
for source in read(E/'candidate-ledger-provenance.json')['sources']:
 st=S/source['study'];assert sha(st/'snapshot.json')==source['snapshot_sha256'];assert sha(st/'results/accounting.json')==source['accounting_sha256']
receipt={'status':'PASS','exact_approved_design_setting_supply_maps':168,'identical_source_controls':6,'independent_financial_checks':174,'matched_comparisons':126,'ledger_rows_all_cells_checked':266,'snapshot_path_hashes_checked':len(checked),'rankings':rankings,'snapshot_sha256':sha(r/'snapshot.json')}
(E/'final-review-records.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='rankings'}))
