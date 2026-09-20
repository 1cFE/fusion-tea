"""Join entering and current public interfaces to explicit semantic review contracts."""
from pathlib import Path
import csv,hashlib,json,yaml
ROOT=Path(__file__).resolve().parents[3]
WI=Path(__file__).resolve().parent
GOAL=ROOT/'work/orchestration/goals/preserve-model-design-choices/evidence'
PACKAGE=ROOT/'exploration/stellarator_e2e/generated'
entering=json.loads((GOAL/'generated-binding-census.json').read_text())
contract_path=PACKAGE/'contracts/model_contract.json';pipeline_path=PACKAGE/'pipelines/pipeline.yaml'
contract=json.loads(contract_path.read_text());pipeline=yaml.safe_load(pipeline_path.read_text())
consumer={}
for module,value in pipeline['modules'].items():
 for port,binding in (value.get('inputs') or {}).items():consumer.setdefault(binding.split(' ',1)[-1],[]).append({'module':module,'input':port})
current={p['qualified_name']:p|{'consumers':consumer.get(p['param_group']+'.'+p['qualified_name'],[])} for p in contract['parameters']}
initial={p['qualified_name']:p for p in entering['parameters']}
C={
'R01':('chosen geometry / identity','compliant-limited','models/library/analyses/mfe_plasma_scaling.sysml:4;models/library/analyses/mfe_plasma_scaling.sysml:52','Torus shape and layer identities; no automatic adequacy; hybrid price separate'),
'R02':('chosen operating state / calculated balance','compliant-limited','models/library/analyses/mfe_plasma_sustainment.sysml;models/library/structure/mfe_plasma.sysml','Specified-state analysis; no inverse operating closure or guaranteed ignition'),
'R03':('calibration or adequacy criterion','compliant-limited','models/library/analyses/mfe_plasma_scaling.sysml:237;models/library/analyses/mfe_tritium_breeding.sysml','Supported source domains and conditional breeding definedness remain separate'),
'R04':('fixed-profile heat ledger input','compliant-limited','models/library/analyses/mfe_divertor_heat.sysml:4','Equivalent area is diagnostic; no independent installed target area or lifetime'),
'R05':('exhaust-boundary assumption / gas balance','compliant-limited','models/library/analyses/mfe_vacuum.sysml:4','Required effective speed only; no selected pumps or conductance/cost evaluation'),
'R06':('maintained nominal stock policy','compliant-limited','models/library/analyses/mfe_fuel_cycle.sysml:94;models/library/structure/mfe_plant_systems.sysml','Explicit stream-times-residence/coverage scenario; no active offered stock/tank evaluation'),
'R07':('fuel reaction/throughput/startup requirement','compliant-limited','models/library/analyses/mfe_fuel_cycle.sysml;models/designs/generic_mfe/mfe_plant.sysml','No external initial supply assurance/procurement cost; undefined breeding stays undefined'),
'R08':('explicit replace-at-limit/availability policy','compliant-limited','models/library/analyses/mfe_lifecycle.sysml:14;models/designs/generic_mfe/mfe_plant.sysml','Physical fluence life distinct from chosen bundled replacement rule; no arbitrary schedules'),
'R09':('demand-matched or hybrid capital/annual cost proxy','unverified-consumer-disclosure','models/library/analyses/mfe_account_costs.sysml;models/designs/generic_mfe/mfe_subsystems.sysml','No independently rated equipment capacity; verify explicit model/report disclosure before acceptance'),
'R10':('legacy/dormant demand-matched allowance','unverified-consumer-disclosure','models/library/analyses/mfe_account_costs.sysml:310;models/library/structure/mfe_plant_systems.sysml','Compatibility cost path; no installed capacity. Account mode must be explicit'),
'R11':('specified-state thermal operating closure','compliant-limited','models/library/analyses/mfe_power_cycle.sysml;models/library/analyses/mfe_matched_steam_cycle.sysml','Required steam/water work and flow; no independently installed equipment rating'),
'R12':('chosen thermal scenario / operating heat balance','compliant-limited','models/library/analyses/mfe_cryo_inventory.sysml;models/library/analyses/mfe_cryo_plant.sysml','Dependent on supplied WI075 geometry/masses; no refrigerator rating or structural qualification'),
'R13':('chosen installed heating / efficiency / price','compliant-limited','models/library/analyses/mfe_heating_chain.sysml;models/library/cost_structure/mfe_power_core.sysml','Stellarator zero-direct-term contract; generic direct-power consistency unverified'),
'R14':('financial/accounting policy or scalar allowance','compliant-limited','models/library/analyses/mfe_account_costs.sysml;models/library/analyses/mfe_lcoe_dcf.sysml;models/designs/generic_mfe/mfe_plant.sysml','Accounting identity/policy only; power-scaled account portion classified separately'),
'R15':('chosen constant / criterion / load assumption','compliant-limited','models/library/analyses/mfe_viability.sysml;models/designs/generic_mfe/mfe_plant.sysml;models/designs/stellarator_09/stellarator_plant.sysml','Comparison or declared assumption; no whole-equipment qualification'),
'M75':('magnet supplied design / operating / price / domain parameter','unverified-integrated-repair','work/orchestration/goals/preserve-model-design-choices/evidence/magnet-binding-plan.md;work/active/WI-075_supplied-magnet-design-evaluation/spec.md','Entering mandatory pack/turn/mass choices violated; approved repair requires native independent acceptance'),
'F76':('facility supplied geometry / requirements / policy / price parameter','unverified-integrated-repair','work/orchestration/goals/preserve-model-design-choices/evidence/facilities-binding-plan.md;work/active/WI-076_supplied-facility-design-evaluation/spec.md','Entering geometry/parcel/packages/positions violated; approved repair requires native independent acceptance'),
'F77':('processor supplied rating / price-source parameter','unverified-integrated-repair','work/active/WI-077_supplied-fuel-processing-capacity-evaluation/spec.md;models/library/analyses/mfe_fuel_cycle.sysml:258','Entering demand-times-margin rating violated; source applicability separate from capacity adequacy'),
'C78':('cooling operating / selected design point / procurement / source parameter','unverified-integrated-repair','work/orchestration/goals/preserve-model-design-choices/evidence/cooling-binding-plan.md;work/active/WI-078_supplied-cooling-design-point-evaluation/spec.md','Entering operating-point prices/purchased stock violated; off-design machine performance remains unavailable'),
}
def group(q):
 parts=q.split('__')[2:];owner=parts[0];name=parts[-1]
 if owner=='magnet':return 'M75'
 if owner=='buildings':return 'R10' if 'buildings_cost' in parts or name.startswith('bldg_') else 'F76'
 if owner=='fuel_cycle':
  if name.startswith('processing_'):return 'F77'
  if 'fuel_handling' in parts or name=='fuel_handling_base':return 'R10'
  if name.startswith('tau_') or name in ('held_inventory','inventory_enabled','reserve_fraction','G_stock'):return 'R06'
  if name=='p_trit':return 'R15'
  return 'R07'
 if owner=='heat_transport':return 'R10' if 'coolant' in parts or name.startswith('coolant_') else 'C78'
 if owner=='cryoplant':return 'R09' if 'aux_cooling' in parts or name=='aux_cryo_base' else 'R12'
 if owner=='heating':return 'R13'
 if owner=='plasma':return 'R01' if name in ('R','a','kappa','pi') else 'R02'
 if owner=='blanket':
  if name=='fluence_limit':return 'R08'
  if name in ('blanket_t','firstwall_t','vacuum_t','reflector_t'):return 'R01'
  if 'first_wall' in parts or name=='mn':return 'R03'
  return 'R09'
 if owner in ('shield','vessel','structure'):return 'R01' if name.endswith('_t') else 'R09'
 if owner=='divertor':return 'R09' if 'divertor_cost' in parts or name=='divertor_base' else 'R04'
 if owner=='vacuum_pumping':return 'R05'
 if owner in ('turbine','heat_rejection'):return 'R09' if name=='cost_per_mw' else 'R11'
 if owner in ('electric_plant','misc_plant','power_supplies'):return 'R15' if name in ('p_pf','p_tf') else 'R09'
 if owner=='rb':return 'R01'
 if owner in ('availability_direct','outage_years','unplanned_fraction','operational_years'):return 'R08'
 if owner in ('n_mod','recirc_ok','beta_limit','wall_load_limit','tbr_floor','p_house','f_sub'):return 'R15'
 if owner=='precon_cost':return 'R10'
 if owner in ('om_cost','other_rpe','owner','inc_cost','remote_handling','waste') or owner in ('om_annual_ref','other_rpe_base','owner_base','inc_base','remote_handling_base','waste_base','aux_per_mw'):return 'R09'
 return 'R14'
rows=[]
for q in sorted(initial.keys()|current.keys()):
 p=current.get(q,initial.get(q));g=group(q);role,status,evidence,limit=C[g]
 if g in ('R09','R10'):
  status='compliant-disclosed-proxy'
  evidence+=';models/designs/generic_mfe/mfe_plant.sysml;exploration/stellarator_e2e/studies/study_route.py:26'
  limit='Explicit demand-matched cost estimate; independently supplied installed capacity and qualification absent'
 state='retained' if q in initial and q in current else ('retired' if q not in current else 'introduced')
 if state=='retired':status='retired-entering-interface';limit+='; no current parameter/consumer; reject old key in new package'
 rows.append(dict(parameter=q,entry_type=p['entry_type'],direct_consumer_count=len(p.get('consumers',[])) if q in current else 0,role_review_home='../../../../active/WI-074_design-choice-inventory-and-evaluation-contract/residual-dispositions.md',compliance=status,contract=g,role=role,interface_status=state,entering_consumer_count=len(initial.get(q,{}).get('consumers',[])),direct_consumers=';'.join(v['module']+'.'+v['input'] for v in current.get(q,{}).get('consumers',[])),source_evidence=evidence,limitation=limit,review_status='independently approved limited disposition; implementation-review.md' if g.startswith('R') else 'binding design approved; native integrated review pending'))
with (GOAL/'public-parameter-coverage.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (contract_path,pipeline_path)}
semantic_files=sorted(set(part.split(':',1)[0] for family in C.values() for part in family[2].split(';'))|{'exploration/stellarator_e2e/studies/study_route.py'})
semantic_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in semantic_files}
record={'source_hashes':source_hashes,'semantic_source_hashes':semantic_hashes,'entering_parameter_count':len(initial),'current_parameter_count':len(current),'coverage_rows':len(rows),'retired':[q for q in initial if q not in current],'introduced':[q for q in current if q not in initial],'unconsumed_current':[q for q,p in current.items() if not p['consumers']],'current_parameters':list(current.values()),'contract_counts':{k:sum(r['contract']==k and r['interface_status']!='retired' for r in rows) for k in C}}
(WI/'evidence/current-interface-coverage.json').write_text(json.dumps(record,indent=2)+'\n')
print({k:v for k,v in record.items() if k not in ('current_parameters','retired','introduced')})
