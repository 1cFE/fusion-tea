"""WI-073 name/graph disposition; no current numerical output is an expectation."""
import collections,hashlib,json,sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[6]
HERE=Path(__file__).parent
CANDIDATE=HERE.parents[1]/'candidate'
PACKAGE=ROOT/'exploration/stellarator_e2e/generated'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 for name in ('input-rules.json','manifest.json','constraint-inventory.json'):
  saved=HERE/('entering-'+name)
  if not saved.exists():saved.write_bytes((CANDIDATE/name).read_bytes())
 old=json.loads((HERE.parent/'partitions.json').read_text());old_rules=json.loads((HERE/'entering-input-rules.json').read_text())
 contract=json.loads((PACKAGE/'contracts/model_contract.json').read_text());parameters={p['qualified_name']:p for p in contract['parameters']}
 numeric={p['channel_name']:p for p in contract['outputs'] if p['python_type'] in ('float','int','bool')};structured={p['channel_name'] for p in contract['outputs'] if p['python_type'] not in ('float','int','bool')}
 predicates={e['constraint_id']:e for e in contract['constraint_catalog']['concrete_entries']}
 added=set(numeric)-set(old['current_numeric_channels']);added_parameters=set(parameters)-set(old_rules['input_types'])
 assert set(old['current_numeric_channels'])<=numeric.keys() and set(old_rules['input_types'])<=parameters.keys()
 assert set(old['current_predicates'])<=predicates.keys()
 for folder in ('exploration/stellarator_e2e','exploration/stellarator_e2e/studies'):sys.path.insert(0,str(ROOT/folder))
 import oracle_entry
 assert added<=set(oracle_entry.ORACLE_OUTPUT_TO_CHANNEL.values())
 local={k:v for k,v in oracle_entry.ORACLE_OUTPUT_TO_CHANNEL.items() if v in added}
 # Conservative module fanout starts at the five changed existing PB outputs.
 prefix='stellarator_09__stellaris__';roots={prefix+'pb__'+s for s in ('p_the','p_et','p_net','q_eng','rec_frac')}
 modules=yaml.safe_load((PACKAGE/'pipelines/pipeline.yaml').read_text())['modules'];consumers=collections.defaultdict(list)
 for name,module in modules.items():
  if module['module_type'] in ('EntryPoint','ExitPoint'):continue
  for declaration in module.get('inputs',{}).values():consumers[declaration.split(maxsplit=1)[1].removesuffix('.root')].append(name)
 reached=set(roots);todo=collections.deque(roots);fired=set()
 while todo:
  for name in consumers[todo.popleft()]:
   if name in fired:continue
   fired.add(name)
   for declaration in modules[name].get('outputs',{}).values():
    channel=declaration.split(maxsplit=1)[1]
    if channel not in reached:reached.add(channel);todo.append(channel)
 old_numeric=set(old['current_numeric_channels'])
 result={'authority':'Released WI-073 design and exact generated contract/mappings. Current selected-mode partition is conservative source dependency reachability, never observed output snapshots. Historical both-off branch preserves all entering scalar equations and policies.',
 'source_sha256':{str(p.relative_to(ROOT)):digest(p) for p in [PACKAGE/'contracts/model_contract.json',PACKAGE/'pipelines/pipeline.yaml',ROOT/'models/library/analyses/mfe_power_balance.sysml',ROOT/'models/library/analyses/mfe_matched_steam_cycle.sysml']},
 'old_numeric_count':len(old_numeric),'current_numeric_channels':sorted(numeric),'current_structured_channels':sorted(structured),'current_predicates':sorted(predicates),'current_parameters':sorted(parameters),
 'added_parameters':{k:parameters[k] for k in sorted(added_parameters)},'added_channels':{k:numeric[k]['python_type'] for k in sorted(added)},'added_locals':local,'added_input_bindings':{k:oracle_entry.ENTRY_KEY_TO_ORACLE_INPUT[k] for k in sorted(added_parameters)},'added_predicates':{k:predicates[k] for k in sorted(set(predicates)-set(old['current_predicates']))},
 'historical_controls':{prefix+'turbine__matched_cycle_enabled':0.,prefix+'heat_rejection__cooling_water_enabled':0.},'historical_local_controls':{'matched_cycle_enabled':0.,'cooling_water_enabled':0.},
 'historical_existing_unaffected_channels':sorted(old_numeric),'historical_existing_changed_channels':[],
 'selected_mode_changed_roots':sorted(roots),'selected_mode_potentially_changed_existing_channels':sorted(reached&old_numeric),'selected_mode_unaffected_existing_channels':sorted(old_numeric-reached),
 'new_rate_invariant_channels':sorted(added),'rate_invariance_basis':'Matched state solver, cycle selection and cooling-water equations consume no interest/inflation input; upstream physical heat/flow inputs are rate invariant. Existing 16 financial channels remain independently calculated.'}
 (HERE/'contract-delta.json').write_text(json.dumps(result,indent=2)+'\n')
 print({k:len(result[k]) for k in ['current_numeric_channels','current_structured_channels','current_predicates','current_parameters','added_channels','added_parameters','selected_mode_potentially_changed_existing_channels','selected_mode_unaffected_existing_channels']})
if __name__=='__main__':main()
