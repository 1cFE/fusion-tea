"""Design inventory only: exact names and provenance, never current-output expectations."""
import importlib.util,json,sys,hashlib
from pathlib import Path
sys.path[:0]=[str(Path.cwd()),'exploration/stellarator_e2e/studies']
import oracle_entry as o
from tests.models import current_mfe_regressions as r
P=o.P
contract=json.loads(Path('exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
channels={x['channel_name'] for x in contract['outputs'] if x['python_type'] in ('float','int','bool')}
structured_channels={x['channel_name'] for x in contract['outputs'] if x['python_type'] not in ('float','int','bool')}
local_aliases={'cas30_capital':'indirect_capital','fuel_handling':'processing_cost'}
channel_for=lambda k:o.ORACLE_OUTPUT_TO_CHANNEL.get(local_aliases.get(k,k))
# Exact declared new producer identities; names are not substring exclusion patterns.
new={
'WI-066': ['blanket__breeding','breeding_adequacy'],
'WI-067': ['heat_transport__equipment','heat_transport__cooling_guard','heat_transport__cooling_selection','heat_transport__cooling_energy','cooling_annual'],
'WI-068': ['buildings__layout','buildings__facility_accounts','buildings__facility_land','buildings__civil_rollup','buildings__site_allowance','buildings__ventilation','buildings__initial_sector_start_days','buildings__cooling_initial_handoff_days','facility_preconstruction','facility_shipping','shipping_scope']+[f'buildings__{child}__civil' for child in o.vs.facilities_oracle.CHILDREN],
'WI-069':['fuel_cycle__inventory'],
'WI-070':['fuel_cycle__processing_cost'],
}
source={
'WI-066':'work/active/WI-066_computed-tritium-breeding/design.md',
'WI-067':'work/active/WI-067_installed-cooling-equipment-costs/combined-design.md',
'WI-068':'work/active/WI-068_layout-based-facilities/layout-capacity-design.md',
'WI-069':'work/active/WI-069_fuel-inventory-and-startup/evidence/proposed-abi.md',
'WI-070':'work/active/WI-070_throughput-based-fuel-processing-costs/evidence/proposed-abi.md',
}
result={'force':'[INFERRED] Proposed exact name inventory for review; no numeric current values are expected-value authority. Generated census is observation; reviewed authored/independent declarations are authority.', 'groups':{}}
result['current_numeric_channels']=sorted(channels)
result['current_structured_channels']=sorted(structured_channels)
result['local_alias_equalities']=local_aliases
for item,producers in new.items():
 keys=sorted(k for k in channels if k.removeprefix(P).rsplit('__',1)[0] in producers)
 result['groups'][item]={'source':source[item],'producer_names':sorted(producers),'channels':keys}
for item in ['WI040','WI038','WI059','WI060','WI061','WI062','WI063','WI064','WI065']:
 names=getattr(r,item+'_CHANNELS',set())
 result['groups'][item]={'source':'tests/models/current_mfe_regressions.py::'+item+'_CHANNELS; corresponding item design remains authority','channels':sorted(names),'producer_names':sorted({n.removeprefix(P).rsplit('__',1)[0] for n in names})}
result['current_predicates']=[x['constraint_id'] for x in contract['constraint_catalog']['concrete_entries']]
result['changed_predicates']={'WI-066':[r.WI066_PREDICATE],'signed_boundary_arithmetic':[r.WI062_PREDICATE]}
result['added_predicates']={'WI-061':[r.WI061_PREDICATE],'WI-062':[r.WI062_PREDICATE],'WI-068':[P+x for x in ['facility_capacity_ok__8acbe7a714e6a4d9','facility_outage_ok__9b00e5bd8ea45722','facility_routes_ok__a3dca4061c7bcc9b','facility_replacement_ready__00706bc8dbdf6938','facility_initial_ready__d3a5b04c428ef75f']]}
result['irreducible_breeding_scalar_channels']=[P+'fuel_cycle__fuel__tbr_margin']
result['computed_inventory_scalar_channels']=[P+'fuel_cycle__fuel__tbr_required']
result['earlier_cost_changed_locals']=list(r.WI040_CHANGED_ECONOMICS)+['winding_pack','tape_procurement_cost','conductor_cost_per_kAm_effective','cas30_capital']
controls={P+'heat_transport__equipment_enabled':False,P+'heat_transport__equipment_cost_mode':0.,P+'heat_transport__secondary_energy_mode':0.,P+'buildings__facilities_enabled':False,P+'buildings__facilities_cost_mode':0.,P+'buildings__facilities_capacity_mode':0.,P+'fuel_cycle__inventory_enabled':False,P+'fuel_cycle__held_inventory':0.,P+'fuel_cycle__processing_enabled':False}
result['post_WI065_historical_controls']=controls
path=Path('work/orchestration/goals/divertor-peak-heat-load/evidence/entering/verify_stellaris.py')
spec=importlib.util.spec_from_file_location('old_partition',path);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
result['historical_inventory_authority']={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'local':'I_total','value':old.IN['I_total']}
result['signed_arithmetic_changes']={}
for sized in [False,True]:
 point={P+'plasma__R':13.5,P+'plasma__a':1.5,P+'magnet__coil__I_coil':16e6}
 if sized:point.update({P+'magnet__winding_pack__sizing_mode':1.,P+'magnet__coil__coil_t':.65,P+'magnet__casing__interior_y':.65})
 old.IN.update(o._oracle_overrides(point));before=old.compute();after=o._compute(o._oracle_overrides(controls|point))
 changed=sorted(k for k in before.keys()&after.keys() if before[k]!=after[k] and k!='fuel_tbr_margin')
 result['signed_arithmetic_changes'][str(sized)]={'point':point,'exact_local_names':changed,'exact_channels':{k:channel_for(k) for k in changed},'authority':'Current authored tape-volume/current-sizing sequence versus entering frozen oracle sequence; verify_stellaris.py compute tape_volume_direct and _current_driven_sizing. This observed difference inventory is not permission for a generic tolerance.'}
result['structured_changed_channels']=['constraint_report']+[k+'__evaluation' for vals in result['changed_predicates'].values() for k in vals]
Path('.project/active/aries-comparison-preparation/current-readiness/regression-evidence/partitions.json').write_text(json.dumps(result,indent=2)+'\n')
print('groups',len(result['groups']),'predicates',len(result['current_predicates']),'signed changed',{k:len(v['exact_local_names']) for k,v in result['signed_arithmetic_changes'].items()})
from tests.study.structure_ledger import renamed_keys
# Enumerate fixture partitions as names, never copying current output numbers.
fixtures={
'conductor-current':('work/orchestration/goals/absolute-conductor-current-margin/evidence/entering/native-reference.json','outputs',False),
'conductor-grade':('work/completed/20260914_WI-038_conductor-grade-lever/baseline-before.json','channels',True),
'current-sizing':('work/orchestration/goals/joint-magnet-sizing-feasibility/evidence/entering/native-reference.json','outputs',False),
'manufacturing':('work/active/WI-062_absolute-conductor-current-margin/evidence/baseline.json','outputs',False),
'winding-fit':('work/active/WI-060_tape-procurement-quantity-basis/evidence/baseline.json','outputs',False),
}
result['fixture_partitions']={}
economic={channel_for(k) for k in result['earlier_cost_changed_locals'] if channel_for(k) is not None}
for name,(path,field,early) in fixtures.items():
 d=json.loads(Path(path).read_text());oldkeys=set(renamed_keys(d[field]));changed=set(result['irreducible_breeding_scalar_channels'])&oldkeys
 if early:changed|=economic&oldkeys
 result['fixture_partitions'][name]={'source':path,'changed_current_equation_channels':sorted(changed),'unaffected_exact_channels':sorted(oldkeys-changed),'added_channels':sorted(channels-oldkeys),'extra_declared_cost_changes':early}
for group,path in [('divertor','work/orchestration/goals/divertor-peak-heat-load/evidence/entering/native-cases.json'),('signed','work/orchestration/goals/divertor-peak-heat-load/evidence/entering/negative-native-cases.json')]:
 for case in json.loads(Path(path).read_text())['cases']:
  name=group+'-'+str(case.get('proposal_id',case.get('sized')));oldkeys=set(case['outputs']);changed=set(result['irreducible_breeding_scalar_channels'])&oldkeys
  # Native historical scalar preservation remains exact; changed ORACLE arithmetic is a separate partition.
  result['fixture_partitions'][name]={'source':path,'point':case['point'],'changed_current_equation_channels':sorted(changed),'unaffected_exact_channels':sorted(oldkeys-changed),'added_channels':sorted(channels-oldkeys)}
for name in result['signed_arithmetic_changes']:
 result['signed_arithmetic_changes'][name]['source_commit']='450f4eab1'
# Correct shared producer provenance at individual channel level.
result['groups']['WI-070']['channels'].append(P+'shipping_scope__fuel_installation_exclusion')
result['groups']['WI-068']['channels'].remove(P+'shipping_scope__fuel_installation_exclusion')
result['groups']['WI-068']['channels'].append(P+'rb__outer_radius')
result['groups']['WI-068']['producer_names'].append('rb (outer_radius addition only)')
Path('.project/active/aries-comparison-preparation/current-readiness/regression-evidence/partitions.json').write_text(json.dumps(result,indent=2)+'\n')
print('fixture partitions',len(result['fixture_partitions']))
# Earlier radius and local-oracle replays keep separately named dialects.
path='work/active/WI-051_mfe-model-owned-major-radius/prototype/frozen-results.json'
frozen=json.loads(Path(path).read_text())
for name,case in frozen['cases'].items():
 if name not in ('baseline','tied_R14'):continue
 oldkeys=set(renamed_keys(case['native']['outputs']));changed=(economic|set(result['irreducible_breeding_scalar_channels']))&oldkeys
 result['fixture_partitions']['radius-'+name]={'source':path,'changed_current_equation_channels':sorted(changed),'unaffected_exact_channels':sorted(oldkeys-changed),'added_channels':sorted(channels-oldkeys)}
for label,path in [('winding-local','.project/active/winding-pack-current-consumers/implementation/oracle-before.json'),('coil-thermal-local','work/active/WI-059_coil-thermal-and-total-support-inventory/evidence/entering_oracle.json')]:
 doc=json.loads(Path(path).read_text());controls=doc.get('controls',[doc])
 for index,row in enumerate(controls):
  keys=set(row['outputs']);changed=(set(result['earlier_cost_changed_locals'])|{'fuel_tbr_margin'})&keys
  result['fixture_partitions'][f'{label}-{index}']={'source':path,'dialect':'oracle local names','changed_current_equation_locals':sorted(changed),'unaffected_exact_locals':sorted(keys-changed),'added_local_names':sorted(set(o.vs.compute())-keys)}
result['arithmetic_change_provenance']={'commit':'450f4eab1','lines':['exploration/stellarator_e2e/verify_stellaris.py:846','exploration/stellarator_e2e/verify_stellaris.py:1103'],'basis':'git blame proves both reordered sizing and selection of authored inventory tape volume entered at this commit; current independent output snapshots are not expected-value authority.'}
Path('.project/active/aries-comparison-preparation/current-readiness/regression-evidence/partitions.json').write_text(json.dumps(result,indent=2)+'\n')
print('complete fixture partitions',len(result['fixture_partitions']))
