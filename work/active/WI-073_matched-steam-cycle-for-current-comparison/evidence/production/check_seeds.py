"""Focused author evidence; independent oracle/native integration are separate."""
from pathlib import Path
from types import SimpleNamespace
import hashlib, json, math, sys, tempfile
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).parent
sys.path.insert(0,str(HERE.parents[1]/'seeds'))
import matched_steam_cycle_impl as steam
import cooling_water_rejection_impl as cooling
import cycle_mode_selection_impl as selection
BASE=json.loads((HERE/'baseline-working.json').read_text())['input']
BASE |= {'source_heat_MW':BASE['heat_available_MW'],'selected_recovered_MW':0.0}
CW=dict(enabled=1.,cycle_active=1.,q_rejection_before_cooling_MW=2096.5978893200615,condenser_temperature_C=42.,water_inlet_C=25.,water_outlet_C=35.,head_m=20.,eta_pump=.8,eta_motor=.95)
checks=[]
def record(name,**data): checks.append({'name':name,'passed':True,**data})
def near(actual,expected,name,relative=1e-9,absolute=1e-6):
 assert math.isclose(actual,expected,rel_tol=relative,abs_tol=absolute),(name,actual,expected)
 record(name,actual=actual,expected=expected,relative_tolerance=relative,absolute_tolerance=absolute)
def refuses(fn,values,fragment,label):
 try:fn(values)
 except ValueError as error:
  assert fragment in str(error),(label,str(error),fragment)
  record(label,error=str(error));return
 raise AssertionError('Expected refusal: '+label)
def changed_boundary(**changes):
 p=BASE|changes
 p['salt_flow_per_circuit']=p['heat_available_MW']*1000/(p['salt_cp_kJ_kgK']*(p['salt_hot_C']-p['salt_return_C'])*p['salt_circuit_count'])
 return p

def run():
 # Exact interface membership is derived from the reviewed document, not results.
 import re
 interface=(HERE.parents[1]/'interface-inventory.md').read_text()
 scalars=re.search(r'Other Real outputs are exactly: (.+?)\.',interface).group(1)
 booleans=re.search(r'Boolean outputs are exactly: (.+?)\.',interface).group(1)
 states=('feed','main','hp','reheat','lp','condensate','condensate_pumped','heater')
 expected={f'{prefix}_{state}_{unit}' for state in states for prefix,unit in [('p','MPa'),('h','kJ_kg'),('mdot','kg_s')]}
 expected|={f'{prefix}_{state}_{unit}' for state in states if state!='condensate_pumped' for prefix,unit in [('t','C'),('s','kJ_kgK')]}
 expected|=set(re.findall('`([^`]+)`',scalars+booleans))
 assert set(steam.REAL_OUTPUTS+steam.BOOL_OUTPUTS)==expected and len(expected)==78
 record('exact released steam output membership',count=len(expected))
 cw_section=interface.split('## Cooling Water Rejection')[1].split('## Cycle Mode Selection')[0]
 cw_real=re.search(r'Real outputs are exactly (.+?)\.',cw_section).group(1)
 cw_bool=re.search(r'Boolean outputs are (.+?)\.',cw_section).group(1)
 assert set(cooling.REAL_OUTPUTS+cooling.BOOL_OUTPUTS)==set(re.findall('`([^`]+)`',cw_real+cw_bool))
 assert set(selection.GENERATED_OUTPUT_ORDER)=={'eta_selected','legacy_domain_applicable','matched_domain_applicable'}
 record('exact released cooling and selection output membership',cooling_count=13,selection_count=3)
 asset=ROOT/'models/library/data/matched_steam_properties.json';steam.verify_source_asset(asset)
 data=json.loads(asset.read_text())
 assert asset.read_bytes()==steam.SOURCE_ASSET_JSON.encode()
 for table in data['tables'].values():
  source=ROOT/table['source_path'];assert hashlib.sha256(source.read_bytes()).hexdigest()==table['source_sha256']
  assert table['reference_state']=='DEF'
  for row in table['rows']:
   assert row['source_cells'][-1]==row['phase']
   for i,key in enumerate(('T','P','rho','v','u','h','s')):assert float(row['source_cells'][i])==row[key]
   # Propagate half of each source cell's last printed digit; no fitted allowance.
   pressure,volume,u,h=[Decimal(row['source_cells'][i]) for i in (1,3,4,5)]
   dp,dv,du,dh=[Decimal(1).scaleb(v.as_tuple().exponent)/2 for v in (pressure,volume,u,h)]
   bound=dh+du+1000*(abs(pressure)*dv+abs(volume)*dp+dp*dv)
   assert abs(h-u-1000*pressure*volume)<=bound
 record('canonical embedded and original row identities',sha256=steam.SOURCE_ASSET_SHA256,rows=sum(t['row_count'] for t in data['tables'].values()))
 prototype=json.loads((ROOT/'work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-results.json').read_text())
 outputs={}
 for reference in prototype['cases']:
  if not reference['reheat']:continue
  p=BASE|{'steam_temperature_C':reference['steam_C'],'reheat_temperature_C':reference['steam_C'],'condenser_temperature_C':reference['condenser_C']}
  result=steam.calculate(p);cw=cooling.calculate(CW|{'condenser_temperature_C':p['condenser_temperature_C'],'q_rejection_before_cooling_MW':result['q_rejection_before_cooling_MW']})
  outputs[reference['name']]={'inputs':p,'steam':result,'cooling_water':cw}
  for key,original in {'p_gross_MW':'gross_MW','eta_gross':'gross_efficiency','p_cycle_pumps_MW':'feed_and_condensate_pump_MW','bleed_fraction':'bleed_fraction','lp_quality':'LP_quality','t_feed_C':'feedwater_C','q_condenser_MW':'condenser_MW','q_main_MW':'main_duty_MW','q_reheat_MW':'reheater_duty_MW','q_rejection_before_cooling_MW':'rejection_before_cw_pump_MW'}.items():
   near(result[key],reference[original],reference['name']+': '+key)
  for key,original in {'p_cooling_pump_electric_MW':'cooling_water_pump_MW','water_flow_kg_s':'cooling_water_kg_s','water_pump_rise_K':'cooling_water_pump_temperature_rise_K'}.items():near(cw[key],reference[original],reference['name']+': '+key)
  near(result['p_cycle_net_before_cooling_MW']-cw['p_cooling_pump_electric_MW'],reference['cycle_net_MW'],reference['name']+': net after cooling')
  for branch,ref in [('main','main'),('reheat','reheater')]:
   near(result[branch+'_min_gap_K'],reference[ref]['min_gap_K'],reference['name']+': '+branch+' gap',relative=0,absolute=1e-12)
   near(result[branch+'_UA_MW_K'],reference[ref]['UA_MW_K'],reference['name']+': analytic versus author quadrature '+branch,relative=1e-6,absolute=0)
  for name in ('salt_heat_residual_MW','heater_mass_residual_kg_s','heater_energy_residual_MW','cycle_shaft_residual_MW','cycle_electric_residual_MW'):assert abs(result[name])<1e-8
  assert result['active'] and result['main_admission_ok'] and result['reheat_admission_ok']
  assert result['turbine_equipment_qualified'] is False and result['installed_sg_capacity_qualified'] is False and cw['site_qualified'] is False
  record(reference['name']+': raw balances and qualification statuses')
 # Branch must return before any property work, even with invalid unused inputs.
 original=steam.property_tables;original_cooling=cooling.property_tables
 def forbidden():raise AssertionError('inactive property access')
 steam.property_tables=forbidden;cooling.property_tables=forbidden
 try:
  assert all(v in (0.,False) for v in steam.calculate({'enabled':0.}).values())
  assert all(v in (0.,False) for v in cooling.calculate({'enabled':0.}).values())
  for module,func in [(steam,steam.run_matched_steam_cycle),(cooling,cooling.run_cooling_water_rejection)]:
   p={name+'_in':float('nan') for name in module.INPUT_NAMES};p['enabled_in']=0.
   assert all(v in (0.,False) for v in func(SimpleNamespace(**p)))
 finally:steam.property_tables=original;cooling.property_tables=original_cooling
 record('disabled modes and wrappers perform zero property lookups with invalid unused facts')
 for module,base,wrapper in [(steam,BASE,steam.run_matched_steam_cycle),(cooling,CW,cooling.run_cooling_water_rejection),(selection,dict(matched_enabled=1.,legacy_eta=.333,matched_eta=.37,legacy_domain_product=-1.),selection.run_cycle_mode_selection)]:
  expected_result=module.calculate(base)
  assert wrapper(SimpleNamespace(**{k+'_in':v for k,v in base.items()}))==tuple(expected_result[k] for k in module.GENERATED_OUTPUT_ORDER)
 record('seed wrappers follow explicitly designated output order; generated order still pending')
 for key,value,fragment in [('main_pressure_MPa',6.3,'pressure domain'),('extraction_pressure_MPa',.9,'pressure domain'),('steam_temperature_C',455.00001,'main steam'),('steam_temperature_C',277.73289,'main steam'),('reheat_temperature_C',170.40649,'reheat steam'),('condenser_temperature_C',19.999,'condenser'),('condenser_temperature_C',60.001,'condenser'),('eta_hp',0.,'efficiency'),('eta_lp',1.01,'efficiency'),('salt_flow_per_circuit',0.,'positive'),('heat_available_MW',-1.,'positive'),('salt_circuit_count',0.,'positive'),('heat_available_MW',BASE['heat_available_MW']+1.,'salt input heat join'),('salt_circuit_count',28.,'salt input heat join')]:
  case=BASE|{key:value}
  if key=='heat_available_MW' and value>0:
   # Preserve the salt-closure test: independently keep the new plant-heat prerequisite coherent.
   case['source_heat_MW']=value
  refuses(steam.calculate,case,fragment,'steam refusal '+key+' '+str(value))
 for key in steam.INPUT_NAMES:
  refuses(steam.calculate,BASE|{key:float('nan')},'finite real','nonfinite steam '+key)
 for value in (-1.,.5,2.,float('inf')):
  fragment='finite real' if not math.isfinite(value) else 'mode must'
  refuses(steam.calculate,BASE|{'enabled':value},fragment,'invalid steam mode '+str(value))
  refuses(cooling.calculate,CW|{'enabled':value},fragment,'invalid cooling mode '+str(value))
 for key,value,fragment in [('cycle_active',0.,'requires matched'),('cycle_active',.5,'mode must'),('head_m',-1.,'nonnegative'),('head_m',1e7,'denominator'),('water_inlet_C',35.,'require 20'),('water_outlet_C',60.1,'require 20'),('eta_pump',0.,'efficiency'),('eta_motor',1.1,'efficiency'),('q_rejection_before_cooling_MW',0.,'positive')]:
  refuses(cooling.calculate,CW|{key:value},fragment,'cooling refusal '+key+' '+str(value))
 for key in cooling.INPUT_NAMES:refuses(cooling.calculate,CW|{key:float('nan')},'finite real','nonfinite cooling '+key)
 for hot in (445.,444.,455.):
  result=steam.calculate(changed_boundary(salt_hot_C=hot))
  if hot<=445:
   assert result['main_min_gap_K']<=0 and result['reheat_min_gap_K']<=0
   assert not result['main_admission_ok'] and not result['reheat_admission_ok']
   assert not result['main_UA_available'] and result['main_UA_MW_K']==0
   assert not result['reheat_UA_available'] and result['reheat_UA_MW_K']==0
  else:assert result['main_min_gap_K']==10 and result['main_admission_ok']
  record('finite adverse/10 K historical-screen distinction '+str(hot),main_gap=result['main_min_gap_K'],reheat_gap=result['reheat_min_gap_K'],UA_available=result['main_UA_available'])
 for outlet in (42.,43.):
  result=cooling.calculate(CW|{'water_outlet_C':outlet})
  assert result['active'] and not result['cooling_approach_ok'] and result['condenser_water_gap_K']<=0
  record('adverse finite cooling approach '+str(outlet),raw_gap=result['condenser_water_gap_K'])
 baseline=steam.calculate(BASE)
 for count in (10.,18.):
  p=BASE|{'salt_circuit_count':count,'heat_available_MW':BASE['heat_available_MW']*count/14}
  p['source_heat_MW']=p['heat_available_MW']
  r=steam.calculate(p)
  near(r['salt_flow_total_kg_s'],BASE['salt_flow_per_circuit']*count,'nondefault circuit flow '+str(count))
  near(r['q_main_MW']+r['q_reheat_MW'],p['heat_available_MW'],'nondefault circuit heat '+str(count))
  near(r['p_gross_MW'],baseline['p_gross_MW']*count/14,'nondefault circuit gross '+str(count))
 for name in ('main','extraction'):
  rows=steam.property_tables()[name];liquid,vapor=steam.saturation_endpoints(rows)
  for key in ('h','s'):
   for endpoint in (liquid,vapor):assert steam.state_at(rows,key,endpoint[key])['h']==endpoint['h']
   middle=steam.state_at(rows,key,(liquid[key]+vapor[key])/2)
   near(middle['T'],liquid['T'],'phase plateau '+name+' '+key,relative=0,absolute=1e-10)
   for direction,bound in [('low',min(r[key] for r in rows)),('high',max(r[key] for r in rows))]:
    value=math.nextafter(bound,-math.inf if direction=='low' else math.inf)
    refuses(lambda p:steam.state_at(rows,key,p['value']),{'value':value},'property domain','no extrapolation '+name+' '+key+' '+direction)
 record('both saturation endpoints and closed inversion domains')
 # Analytic constant-gap limit and a nearby segment, using actual original knots.
 rows=steam.property_tables()['main'];a,b=rows[:2];duty=3.
 for delta in (0.,1e-10):
  gap,ua,available=steam.heat_profile(rows,a['h'],b['h'],b['T']+20+delta,a['T']+20,duty,inlet_temperature=a['T'],outlet_temperature=b['T'])
  assert available and gap==20.
  near(ua,duty/20,'constant/near-constant gap limit '+str(delta),relative=1e-11,absolute=0)
 # Exact supplied endpoint and its neighbors retain their signs, without tolerance.
 for hot in (math.nextafter(445.,-math.inf),445.,math.nextafter(445.,math.inf)):
  r=steam.calculate(changed_boundary(salt_hot_C=hot))
  for branch in ('main','reheat'):
   assert r[branch+'_min_gap_K']==hot-445.
   assert r[branch+'_admission_ok'] is (hot>445.)
  record('strict representable endpoint '+repr(hot),gap=r['reheat_min_gap_K'])
 for key in ('eta_hp','eta_lp','eta_condensate_pump','eta_feedwater_pump','eta_pump_motor','eta_mechanical','eta_generator'):
  r=steam.calculate(BASE|{key:1.})
  assert r['active']
  record('efficiency upper endpoint '+key)
 r=steam.calculate(BASE|{'condenser_temperature_C':20.})
 assert r['active']
 record('condenser lower table endpoint')
 refuses(steam.calculate,BASE|{'condenser_temperature_C':60.},'LP actual endpoint','temperature support does not imply LP phase support')
 zero_head=cooling.calculate(CW|{'head_m':0.})
 assert zero_head['p_cooling_pump_electric_MW']==zero_head['p_cooling_pump_shaft_MW']==zero_head['water_pump_rise_K']==0.
 record('zero cooling head exact zero work')
 # Cached production helper is explicitly cleared for this adverse identity probe.
 original_text=steam.SOURCE_ASSET_JSON
 steam.property_tables.cache_clear()
 try:
  steam.SOURCE_ASSET_JSON=original_text+' '
  refuses(steam.calculate,BASE,'embedded property asset identity mismatch','tampered embedded asset')
 finally:
  steam.SOURCE_ASSET_JSON=original_text;steam.property_tables.cache_clear()
 for value in (0.,1.):
  r=selection.calculate(dict(matched_enabled=value,legacy_eta=.333,matched_eta=.37,legacy_domain_product=-5.))
  assert r['eta_selected']==(.37 if value else .333)
  assert r['legacy_domain_applicable'] is (not bool(value))
 record('selection retains negative raw historical domain without green substitute')
 refuses(selection.calculate,dict(matched_enabled=.5,legacy_eta=.333,matched_eta=.37,legacy_domain_product=1.),'mode must','selection mixed mode')
 with tempfile.TemporaryDirectory() as td:
  p=Path(td)/'asset.json';p.write_bytes(asset.read_bytes()+b' ')
  refuses(lambda _:steam.verify_source_asset(p),{},'identity mismatch','tampered staged asset')
  try:steam.verify_source_asset(Path(td)/'missing.json')
  except FileNotFoundError:record('missing staged asset refuses')
  else:raise AssertionError('missing asset accepted')
 (HERE/'author-results.json').write_text(json.dumps({'status':'author checks pass; independent verification and native generation pending','checks':checks,'cases':outputs,'source_asset_sha256':steam.SOURCE_ASSET_SHA256,'seed_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.parents[1]/'seeds').glob('*.py')},'non_reheat_cases':'The two retained prototype references remain unchanged; production has no no-reheat selector.'},indent=2,allow_nan=False)+'\n')
 print(f'{len(checks)} author checks passed; four reviewed reheat cases; exact 78/13/3 output inventories')
if __name__=='__main__':run()
