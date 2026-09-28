"""Read explicit native metadata and test key translation, without plant execution."""
from pathlib import Path
import json,sys
ROOT=Path('/home/reid/1cfe/fusion-tea-codex-test')
sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/studies'))
import oracle_entry as oracle
E=ROOT/'work/orchestration/goals/plant-closure/evidence/T-011_candidate-assessment'
P=oracle.P
contract=json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
params={x['qualified_name']:x for x in contract['parameters']}
scalars={x['channel_name'] for x in contract['outputs'] if x['python_type'] in ('float','int')}
families={
'closure-factorial':['loop_live','cycle_live','availability_direct','p_pump_direct','eta_p_direct','eta_th_direct'],
'inherited-window':['R','a','magnet__I_coil','n_e0','T_i0','p_wallplug_heat'],
'fixed-loop':['n_loops'], 'sized-loop':['n_loops'],
'loop-loss':['f_loss','loop_dT_blanket'],
'cycle':['loop_T_in','loop_dT_blanket','dT_approach','a_fit','b_fit','T_offset_fit','T2_min','T2_max','delta_eta'],
'calendar':['outage_years','unplanned_fraction'], 'fuel':['burn_fraction'],
'divertor-transport':['q_target_ref'], 'divertor-radiation':['f_rad_total'],
'reserve':['p_wallplug_heat'], 'vacuum':[], 'area-shadow':[], 'baseline':[]}
fixed_directs={'p_pump_direct','eta_p_direct','eta_th_direct'}
axes=sorted(set(sum(families.values(),[]))-fixed_directs)
groups={'schema_version':'study-axis-declaration/v1','groups':[{'axis':k,'note':'AGENT proposed sensitivity/control input for plant comparison; not an approved execution ruling. Complete native entry for this plant attribute.','keys':[{'key':P+k,'provenance':'fan_out'}]} for k in axes]}
(E/'axes.json').write_text(json.dumps(groups,indent=2)+'\n')
provisional=json.loads((ROOT/'work/orchestration/goals/plant-closure/evidence/round2_preparation/required-channels.provisional.json').read_text())
rows=[]
for family,keys in families.items():
 point={P+k:params[P+k]['default_value'] for k in keys if P+k in params}
 try:
  translated=oracle._oracle_overrides(point)
  result='accepted translation only; no numerical execution'
 except Exception as exc: translated={};result=repr(exc)
 rows.append({'family':family,'keys':keys,'missing_native':[k for k in keys if P+k not in params],'missing_oracle':[k for k in keys if P+k not in oracle.ENTRY_KEY_TO_ORACLE_INPUT],'translation_result':result})
retired={}
try:oracle._oracle_overrides({P+'magnet__R0':12.7})
except oracle.OracleSeamError as exc:retired={'refused':True,'message':str(exc)}
expanded=dict(provisional)
for c in sorted(scalars-set(expanded.values())):expanded[c.removeprefix(P)]=c
(E/'required-channels.json').write_text(json.dumps(expanded,indent=2)+'\n')
bindings=oracle.operand_bindings()
result={'scope':'metadata and adapter translation only; no evaluate/compute calls','native_inputs':len(params),'mapped_inputs':len(oracle.ENTRY_KEY_TO_ORACLE_INPUT),'candidate_axes':len(axes),'families':rows,'native_scalars':len(scalars),'provisional_columns':len(provisional),'missing_provisional_channels':sorted(set(provisional.values())-scalars),'native_scalars_missing_from_provisional':sorted(scalars-set(provisional.values())),'expanded_columns':len(expanded),'oracle_channels':len(oracle.ORACLE_OUTPUT_TO_CHANNEL),'independent_omissions':sorted(scalars-set(oracle.ORACLE_OUTPUT_TO_CHANNEL.values())),'expanded_missing_oracle':sorted(set(expanded.values())-set(oracle.ORACLE_OUTPUT_TO_CHANNEL.values())),'constraints':len(contract['constraint_catalog']['concrete_entries']),'unbound_constraints':sorted({x['constraint_id'] for x in contract['constraint_catalog']['concrete_entries']}-set(bindings)),'retired_key':retired}
(E/'coverage.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('families','independent_omissions','native_scalars_missing_from_provisional','expanded_missing_oracle')},indent=2))
