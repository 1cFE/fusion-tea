"""Summarize retained native evidence and independently reconcile account identities."""
import csv
import json
import math
from pathlib import Path
import sys

H=Path(__file__).resolve().parents[1];ROOT=H.parents[3];R=H/'results'
sys.path.insert(0,str(ROOT))
P='stellarator_09__stellaris__';E='heat_transport__equipment__'
read=lambda p:json.loads(p.read_text())
def write(p,data):p.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def key(point):return json.dumps({k:float(v) for k,v in point.items()},sort_keys=True)
assert read(R/'oracle-all-points.json')['outcome']=='pass'
props=read(H/'preparation/proposals.json');by_point={key(c['inputs']):c for c in read(R/'native-cases.json')}
by={p['id']:by_point[key(p['point'])] for p in props};base=by['reference']
catalog=read(R/'predicate-catalog.json');defaults=read(H/'preparation/resolved-defaults.json')
accounts=read(H/'preparation/references/account-extraction.json')['direct_accounts']
rows=[];checks=[]
def equal(name,actual,expected,absolute=1e-4):
 checks.append({'check':name,'actual':actual,'expected':expected,'error':actual-expected,'outcome':'pass' if math.isclose(actual,expected,rel_tol=1e-12,abs_tol=absolute) else 'fail'})
def same(name,ident,channels,predicates=False):
 case=by[ident]
 differences=[k for k in channels if case['outputs'][k]!=base['outputs'][k]]
 verdicts_equal=case['verdicts']==base['verdicts']
 checks.append({'check':name,'case':ident,'channel_count':len(channels),'differences':differences,'verdicts_equal':verdicts_equal,'require_verdict_equality':predicates,'outcome':'pass' if not differences and (verdicts_equal or not predicates) else 'fail'})
names={
 'direct':'cas2x_pre_contingency__cas2x_pre_contingency','contingency':'contingency__cost',
 'CAS20':'cas20_capital__cas20_capital','indirect':'indirect__cost','supplementary':'supplementary__cost',
 'overnight':'total_capital__total_capital','idc':'idc__cost','comparison_annual_capital':'cas90_1cfe_calc__cas90',
 'routine_raw':'om_cost__annual_om','routine_levelized':'cas71_calc__levelized',
 'replacement_total':'cooling_annual__cas72_total','cooling_replacement':E+'replacement_annual',
 'annual_expense':'cas70_calc__annual_total','fuel_raw':'fuel_cycle__fuel_calc__annual_fuel','fuel_levelized':'cas80_calc__levelized',
 'net_MW':'pb__p_net','availability':'calendar__availability','LCOE':'lcoe_calc__lcoe','LCOE_comparison':'lcoe_1cfe_calc__lcoe',
 'cooling':'heat_transport__cooling_selection__cost','facilities':'buildings__facility_accounts__cost',
 'magnet':'magnet__magnet_capital_rollup__capital_cost','fuel_processing':'fuel_cycle__processing_cost__cost',
 'hx_supply':E+'hx_purchase','primary_pipe_supply':E+'primary_pipe_purchase','secondary_pipe_supply':E+'secondary_pipe_purchase',
 'bundle_purchase':E+'bundle_event_purchase','bundle_installation':E+'bundle_event_installation','bundle_removal':E+'bundle_event_removal',
 'delivered':E+'delivered_total','shipping_base':'shipping_scope__remaining_shipping_base',
 'cycle_interface':E+'cycle_interface_ok','salt_pump_equation_range':E+'pump_size_ok',
}
for proposal in props:
 ident=proposal['id'];case=by[ident];v=lambda k:case['outputs'][P+k];inputs=defaults|case['inputs']
 row={'id':ident,'family':proposal['family'],'candidate_id':case['candidate_id']}
 row.update({n:v(k) for n,k in names.items()})
 for k,value in proposal['point'].items():row[k.removeprefix(P)]=value
 row['energy_MWh']=8760*row['net_MW']*row['availability']
 row['headline_annual_capital']=row['overnight']*(1+inputs[P+'discount_rate'])**(inputs[P+'construction_years']/2)*v('cas71_calc__crf')
 row['financed_comparison_capital']=row['overnight']+row['idc']
 row['in_vessel_replacement']=row['replacement_total']-row['cooling_replacement']
 row['failed']=';'.join(catalog[cid]['source_local_identity'] for cid,status in case['verdicts'].items() if status!='satisfied')
 rows.append(row)
 direct=sum(inputs[P+a['channel'][1:]] if a['channel'].startswith('@') else v(a['channel']) for a in accounts)
 equal(ident+':direct_accounts',direct,row['direct'])
 equal(ident+':CAS29',row['contingency'],inputs[P+'contingency_rate']*direct)
 equal(ident+':CAS20',row['CAS20'],direct+row['contingency'])
 equal(ident+':overnight',row['overnight'],sum(v(k) for k in ['facility_preconstruction__cost','cas20_capital__cas20_capital','indirect__cost','owner__cost','supplementary__cost']))
 equal(ident+':cooling_children',row['cooling'],sum(v(E+k) for k in ['primary_circulators_cost','primary_piping_cost','exchangers_cost','secondary_pumps_cost','secondary_piping_cost','inventory_cost','spares_cost']))
 equal(ident+':CAS70',v('cas70_calc__cas70'),row['routine_levelized']+row['replacement_total'])
 equal(ident+':annual_expense',row['annual_expense'],v('cas70_calc__cas70')+row['fuel_levelized'])
 equal(ident+':headline_LCOE',row['LCOE'],(row['headline_annual_capital']+row['annual_expense'])/row['energy_MWh'],1e-9)
 equal(ident+':comparison_LCOE',row['LCOE_comparison'],(row['comparison_annual_capital']+row['annual_expense'])/row['energy_MWh'],1e-9)
 # Independently derive all three supply bills from unchanged physical mass and the shared raw source rate.
 rate=inputs[P+'heat_transport__equipment_stainless_fabrication_usd2017_per_kg'];conv=321.9/245.1
 equal(ident+':source_rate_HX',v(E+'hx_purchase'),v(E+'hx_mass')*v(E+'ihx_count')*rate*conv)
 equal(ident+':source_rate_primary_pipe',v(E+'primary_pipe_purchase'),v(E+'primary_pipe_mass')*rate*conv)
 equal(ident+':source_rate_secondary_pipe',v(E+'secondary_pipe_purchase'),v(E+'secondary_pipe_mass')*rate*conv)
 equal(ident+':source_rate_bundle',v(E+'bundle_event_purchase'),v(E+'bundle_mass')*v(E+'ihx_count')*rate*conv)
 equal(ident+':HX_installation',v(E+'hx_installation'),.026*v(E+'hx_purchase'))
 equal(ident+':primary_pipe_installation',v(E+'primary_pipe_installation'),.5*v(E+'primary_pipe_purchase'))
 equal(ident+':secondary_pipe_installation',v(E+'secondary_pipe_installation'),.5*v(E+'secondary_pipe_purchase'))
 # Exact coordinated rate response holds at fixed physical design, even in the separate downtime stress.
 factor=rate/310.
 for suffix in ['bundle_event_purchase','bundle_event_installation','bundle_event_removal','hx_purchase','hx_installation','primary_pipe_purchase','primary_pipe_installation','secondary_pipe_purchase','secondary_pipe_installation']:
  equal(ident+':shared_rate:'+suffix,v(E+suffix),base['outputs'][P+E+suffix]*factor)
 # Supplied fabrication is removed from initial freight once; no future replacement enters it.
 supply_delta=sum(v(E+k)-base['outputs'][P+E+k] for k in ['hx_purchase','primary_pipe_purchase','secondary_pipe_purchase'])
 equal(ident+':initial_delivered_response',v(E+'delivered_total'),base['outputs'][P+E+'delivered_total']+supply_delta)
 # Source chronology applies jointly to equipment and direct installation for the one containment row.
 date_ratio=82.4/inputs[P+'fuel_cycle__processing_containment_cpi']
 for suffix in ['containment_capital','containment_installation']:
  equal(ident+':containment_shared_date:'+suffix,v('fuel_cycle__processing_cost__'+suffix),base['outputs'][P+'fuel_cycle__processing_cost__'+suffix]*date_ratio)
 for suffix in ['cleanup_capital','cleanup_installation','distiller_capital','distiller_installation','transfer_capital','transfer_installation']:
  equal(ident+':other_fuel_rows_fixed:'+suffix,v('fuel_cycle__processing_cost__'+suffix),base['outputs'][P+'fuel_cycle__processing_cost__'+suffix])
 equal(ident+':sheet_stock_charge',v('magnet__insulation_inventory__stock_cost'),v('magnet__insulation_inventory__sheet_area')*inputs[P+'magnet__winding_pack__insulation_sheet_price'])
 same('Physical insulation unchanged',ident,[P+'magnet__insulation_inventory__'+k for k in ['ground_volume','internal_volume','sheet_area']])
 # No unrelated cooling purchases are changed by any cost interpretation.
 same('Machines/inventory unchanged',ident,[P+E+k for k in ['primary_vendor','primary_design','secondary_vendor','inventory_cost','spares_cost','primary_circulators_cost','secondary_pumps_cost']])
 if proposal['family']!='downtime-stress':
  physical=[k for k in case['outputs'] if any(k.startswith(P+prefix) for prefix in ['plasma__','calendar__','pb__','sustain__','operating_heat__','fuel_cycle__inventory__'])]
  physical += [P+E+k for k in ['primary_pipe_mass','secondary_pipe_mass','hx_mass','bundle_mass','ihx_count','ihx_duty_MW','ihx_required_area','primary_pipe_volume','salt_pipe_volume','salt_flow','salt_electric_MW','helium_inventory_mass','salt_inventory_mass']]
  physical += [P+k for k in ['magnet__winding_procurement__winding_fabrication_cost']]
  same('Physical generation/calendar/stock-demand unchanged',ident,physical,True)
 # Stock's unit-price interpretation must not change winding operations or tape.
 same('Winding and tape unchanged',ident,[P+'magnet__winding_procurement__'+k for k in ['winding_fabrication_cost','tape_cost']])
old=read(H/'preparation/references/wi070-baseline-result.json')['channels']
shared=set(old)&set(base['outputs']);deltas=[k for k in shared if old[k]!=base['outputs'][k]]
checks.append({'check':'WI070 nominal exact preservation','channel_count':len(shared),'differences':deltas,'outcome':'pass' if not deltas else 'fail'})
# Constant-rate mass tests above are independent arithmetic; all-point oracle also reconstructs replacement cashflows.
equal('source low endpoint',240.,120.*2,0);equal('source high endpoint',360.,120.*3,0)
write(R/'account-and-dependency-checks.json',{'outcome':'pass' if all(c['outcome']=='pass' for c in checks) else 'fail','checks':checks,'limits':'Source assumptions are shared. Default preservation compares retained native results; it is not independent physical validation.'})
write(R/'interpreted-cases.json',rows)
with (R/'points.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
numeric=read(H/'preparation/required-channels.json')
with (R/'all-native-channels.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['id','candidate_id']+numeric);w.writeheader()
 for ident,case in by.items():w.writerow({'id':ident,'candidate_id':case['candidate_id']}|{k:case['outputs'][k] for k in numeric})
summary={}
for family in ['source-envelope','contingency-diagnostic','downtime-stress']:
 selected=[r for r in rows if r['family']==family]
 summary[family]={'count':len(selected),'whole_plant_passing':sum(not r['failed'] for r in selected),'bounds':{name:{'min':min(r[name] for r in selected),'max':max(r[name] for r in selected)} for name in names if isinstance(selected[0][name],(float,int))}}
write(R/'summary.json',summary)
fail=[c for c in checks if c['outcome']!='pass']
print(json.dumps({'cases':len(rows),'checks':len(checks),'failures':fail},indent=2))
if fail:raise SystemExit('Account/dependency checks failed; inspect retained evidence')
