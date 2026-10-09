"""Cross-case behavioral checks on actual native receipts, separate from arithmetic."""
import argparse,hashlib,json,math
from pathlib import Path
P='whole_plant_conversion__plant__'
p=argparse.ArgumentParser();p.add_argument('receipts',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
rows=json.loads(a.receipts.read_text())['cases'];cases={r['case']:r for r in rows};checks=[]
def check(name,ok):
 assert ok,name
 checks.append(name)
def out(case,owner,field):return cases[case]['outputs'][P+owner+'__evaluate__'+field]
def failed(case,fragment):return any(fragment in k and v=='violated' for k,v in cases[case].get('responses',{}).items())
def close(x,y):return math.isclose(x,y,rel_tol=1e-10,abs_tol=1e-9)
base='whole-baseline2500'
for name in [base,'matched2800']:
 check(name+'_all_predicates',all(v=='satisfied' for v in cases[name]['responses'].values()))
 check(name+'_conditional_source',out(name,'source_basis','source_qualified')==0 and out(name,'supplied_core','nuclear_transport_qualified')==0 and out(name,'supplied_core','global_construction_qualified')==0)
for name,fragment in [('matched3000-failed-source','divertor_margin'),('matched3000-failed-source','pressure_margin'),('cryo-q80','cold_margin'),('cryo-extra13000','cold_margin'),('stock-insufficient','stock_margin'),('processing-insufficient','processing_margin'),('primary-pressure-insufficient','pressure_margin'),('auxiliary-insufficient','auxiliary_margin'),('negative-whole-net','net_export'),('annual-import-dominated','annual_net_grid'),('outage-budget-failure','outage_margin'),('capture-identity-refusal','identity_supported'),('source-path-count-mismatch','inventory_supported')]:check(name+'_'+fragment,failed(name,fragment))
for name in ['cryo-q50','cryo-extra10000','stock-sufficient','processing-sufficient','primary-pressure-sufficient','auxiliary-sufficient','zero-discount']:
 check(name+'_all_predicates',all(v=='satisfied' for v in cases[name]['responses'].values()))
for name in ['negative-cryo-domain','fractional-horizon-refusal']:check(name+'_refused',cases[name]['state']=='failed')
for branch in ['steam','gas']:
 check(branch+'_source_demand_preserves_capital',out(base,branch+'_overheads','initial_capital')==out('demand-only2800',branch+'_overheads','initial_capital'))
 for name in ['cryo-q50','cryo-q80','cryo-extra10000','cryo-extra13000']:
  check(branch+'_'+name+'_fixed_capital',out(base,branch+'_overheads','initial_capital')==out(name,branch+'_overheads','initial_capital'))
  delta=out(name,'cryogenic_demand','refrigeration_MW')-out(base,'cryogenic_demand','refrigeration_MW')
  heat=(out(name,'cryogenic_demand','cold_W')-out(base,'cryogenic_demand','cold_W'))*1e-6
  check(branch+'_'+name+'_net',close(out(base,branch+'_operating','net_export_MW')-out(name,branch+'_operating','net_export_MW'),delta))
  check(branch+'_'+name+'_sink',close(out(name,branch+'_operating','auxiliary_heat_MW')-out(base,branch+'_operating','auxiliary_heat_MW'),delta+heat))
  check(branch+'_'+name+'_standby',close(out(name,branch+'_operating','standby_MW')-out(base,branch+'_operating','standby_MW'),delta))
for name in ['cryo-q50','cryo-q80','cryo-extra10000','cryo-extra13000']:check(name+'_same_fuel',out(name,'fuel_accounts','annual_fuel')==out(base,'fuel_accounts','annual_fuel'))
check('gas_quote_preserves_steam',out('gas-price-only','steam_overheads','initial_capital')==out(base,'steam_overheads','initial_capital'))
check('gas_quote_preserves_common',out('gas-price-only','gas_overheads','common_purchases')==out(base,'gas_overheads','common_purchases'))
check('gas_quote_changes_gas',out('gas-price-only','gas_overheads','initial_capital')>out(base,'gas_overheads','initial_capital'))
check('extraction_leaves_Li6',out('lower-extraction','fuel_accounts','annual_Li6_kg')==out(base,'fuel_accounts','annual_Li6_kg'))
check('extraction_increases_externalT',out('lower-extraction','fuel_accounts','annual_T_external')>out(base,'fuel_accounts','annual_T_external'))
check('recovery_increases_D',out('lower-recovery','fuel_accounts','annual_D_kg')>out(base,'fuel_accounts','annual_D_kg'))
check('zeroTprice_retains_DT_li6_flows',out('zero-T-price','fuel_accounts','annual_T_cost')==0 and out('zero-T-price','fuel_accounts','annual_D_kg')==out(base,'fuel_accounts','annual_D_kg'))
if 'cryoplant-small-offer' in cases:
 check('small_cryoplant_cold_failure',failed('cryoplant-small-offer','cryogenic_demand__cold_margin'))
 check('small_cryoplant_intercept_failure',failed('cryoplant-small-offer','cryogenic_demand__intercept_margin'))
 check('large_cryoplant_all_predicates',all(v=='satisfied' for v in cases['cryoplant-large-offer']['responses'].values()))
 for name in ['cryoplant-small-offer','cryoplant-large-offer']:
  for field in ['cold_W','intercept_W','refrigeration_MW']:
   check(name+'_demand_independent_'+field,out(name,'cryogenic_demand',field)==out(base,'cryogenic_demand',field))
  for branch in ['steam','gas']:
   check(name+'_'+branch+'_same_export',out(name,branch+'_operating','net_export_MW')==out(base,branch+'_operating','net_export_MW'))
 for branch in ['steam','gas']:
  check('selected_cryo_quote_changes_'+branch+'_capital',out('cryoplant-small-offer',branch+'_overheads','initial_capital')<out(base,branch+'_overheads','initial_capital')<out('cryoplant-large-offer',branch+'_overheads','initial_capital'))
if 'actual-exchanger-crossover' in cases:check('actual_exchanger_crossover_excluded',failed('actual-exchanger-crossover','steam_actual_approach__cold_gap'))
if 'water-property-refusal' in cases:check('water_property_excluded',cases['water-property-refusal']['state']=='failed' or any(v=='violated' for v in cases['water-property-refusal']['responses'].values()))
summary={name:{b:{'net_MW':out(name,b+'_operating','net_export_MW'),'lcoe_USD2025_MWh':out(name,b+'_whole','lcoe_USD2025_MWh'),'initial_USD2025':out(name,b+'_overheads','initial_capital'),'outage_margin_years':out(name,b+'_whole','outage_margin')} for b in ['steam','gas']} for name in [base,'matched2800']}
a.out.write_text(json.dumps(dict(status='pass',checks=checks,conditional_common_points=summary,receipts_sha256=hashlib.sha256(a.receipts.read_bytes()).hexdigest()),indent=2)+'\n')
print('pass',len(checks),'native behavioral checks')
