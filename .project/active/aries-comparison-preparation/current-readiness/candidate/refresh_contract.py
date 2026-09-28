"""Capture the current executable contract; never select new comparison controls.

This is a preparation command. Its output must be reviewed before freezing.
"""
import copy
import json
import sys
from pathlib import Path
from candidate_common import digest, typed, schema_declarations

PREFIX = 'stellarator_09__stellaris__'


def refresh(root, here):
    root, here = Path(root).resolve(), Path(here).resolve()
    sys.path.insert(0, str(root))
    from scripts.study.indicators import read_pipelines
    rules = json.loads((here/'input-rules.json').read_text())
    package = root/rules['package_path']
    contract = json.loads((package/'contracts/model_contract.json').read_text())
    schema_declarations(package, contract['parameters'])
    declarations, origins = {}, {}
    for row in contract['parameters']:
        key, kind = row['qualified_name'], row['python_type']
        if key in declarations and declarations[key] != kind:
            raise ValueError('conflicting declarations: '+key)
        declarations[key] = kind
        origins.setdefault(key, []).append(row['param_group'])
    files, defaults, normalized = [], {}, {}
    for path in read_pipelines(package).input_files:
        name = path.resolve().relative_to(package).as_posix()
        values = json.loads(path.read_text())
        for key, value in values.items():
            canonical = typed(value, declarations[key], key, stored=True)
            if key in normalized and normalized[key] != canonical:
                raise ValueError('conflicting defaults: '+key)
            defaults[key], normalized[key] = value, canonical
        files.append({'path':name, 'sha256':digest(path), 'keys':sorted(values)})
    if set(defaults) != set(declarations):
        raise ValueError('input and declaration key sets differ')
    rules.update(default_values=defaults, input_types=declarations,
                 input_origins=origins, input_files=files,
                 defaults_source='All pipeline input files listed in input_files; original bytes remain authoritative',
                 preparation_status='draft; physical connection unresolved')
    rules.pop('defaults_sha256',None)
    for key, value in rules['forward_overrides'].items():
        typed(value,declarations[key],key)
    (here/'input-rules.json').write_text(json.dumps(rules,indent=2)+'\n')

    manifest = json.loads((here/'manifest.json').read_text())
    mapping = {'achieved_tbr':'blanket__breeding__tbr_mean',
               'coolant':'heat_transport__cooling_selection__cost',
               'fuel_handling':'fuel_cycle__processing_cost__cost',
               'CAS21':'buildings__facility_accounts__cost',
               'CAS10':'facility_preconstruction__cost',
               'CAS72':'cooling_annual__cas72_total'}
    for row in manifest['quantities']:
        if row['id'] in mapping:
            row['producers'] = [PREFIX+mapping[row['id']]]
        if row['id']=='achieved_tbr':
            row.update(role='derived',meaning='Computed mean tritium breeding ratio; adequacy uses the lower bound separately')
            row.pop('role_input',None)
            row['role_basis']='Calculated reduced transport estimate; retain uncertainty and lower-bound engineering check.'
        if row['id']=='CAS23':
            limitation='Steam-generator cost inclusion is unverified; installed scope is incomplete or uncertain.'
            if limitation not in row['validity_limits']: row['validity_limits'].append(limitation)
    catalog = contract['constraint_catalog']['concrete_entries']
    manifest['required_constraints'] = [row['constraint_id'] for row in catalog]
    manifest['semantic_fingerprint'] = contract['semantic_fingerprint']
    existing = {p for row in manifest['quantities'] for p in row['producers']}
    template = next(row for row in manifest['quantities'] if row['axis']=='diagnostic')
    for constraint in catalog:
        if constraint['evaluation_channel'] in existing: continue
        row = copy.deepcopy(template)
        row.update(id=constraint['source_local_identity'],axis='diagnostic',formal=False,
                   meaning=constraint['definition_qualified_name'],unit='1',
                   producers=[constraint['evaluation_channel']],calculation=None,role='derived',
                   depends_on=[],included_scope=['Authored engineering predicate'],excluded_scope=[],
                   reference_value=None,conversion={'basis':'single_module_current_model','allowed_basis_conversions':[],'allowed_units':['1']})
        row.pop('role_input',None)
        row.pop('price_basis',None)
        manifest['quantities'].append(row)
    for equation in manifest['accounting']:
        equation['meaning']=equation['parent']+' is the sum of its disjoint child accounts'
    refresh_matched_cycle(root, here, manifest, contract, rules)
    (here/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (here/'constraint-inventory.json').write_text(json.dumps(catalog,indent=2)+'\n')
    return {'inputs':len(defaults),'input_files':len(files),'predicates':len(catalog),
            'quantities':len(manifest['quantities']),'status':'draft contract; not a freeze or readiness verdict'}


def refresh_matched_cycle(root, here, manifest, contract, rules):
    """Apply only the released WI-073 interface and conditioned-mode migration."""
    delta=json.loads((here.parent/'regression-evidence/cycle-migration/contract-delta.json').read_text())
    matched=PREFIX+'turbine__matched_cycle_enabled'
    cooling=PREFIX+'heat_rejection__cooling_water_enabled'
    assert set(delta['current_parameters'])==set(rules['input_types'])
    seam=next(row for row in rules['conditioned_seams'] if row['id']=='held_cycle')
    seam['keys'].update({matched:0.,cooling:0.})
    seam['reason']='Supply gross efficiency with matched states and cooling water disabled together; historical auxiliary boundary, no matched pump/state prediction.'
    seam['output_roles']={key:'derived_from_supplied_efficiency' for key in delta['selected_mode_potentially_changed_existing_channels']}
    seam['output_roles'].update({PREFIX+'turbine__cycle_selection__eta_selected':'supplied',PREFIX+'turbine__cycle__eta_th':'supplied'})
    rules['selected_modes'].update({matched:1.,cooling:1.})
    rules['preparation_status']='draft WI-073 contract; independent integrated science and candidate lineage remain required'
    policy=json.loads((here/'selection-policy.json').read_text())
    policy['conditioned_seams']=rules['conditioned_seams']
    (here/'selection-policy.json').write_text(json.dumps(policy,indent=2)+'\n')
    (here/'input-rules.json').write_text(json.dumps(rules,indent=2)+'\n')
    template=next(row for row in manifest['quantities'] if row['axis']=='diagnostic')
    existing={row['id']:row for row in manifest['quantities']}
    def unit(name):
        for suffix,value in (('_kJ_kgK','kJ/(kg K)'),('_kJ_kg','kJ/kg'),('_kg_s','kg/s'),('_UA_MW_K','MW/K'),('_MPa','MPa'),('_MW','MW'),('_K','K'),('_C','degC')):
            if name.endswith(suffix):return value
        return '1'
    for channel in delta['added_channels']:
        suffix=channel.removeprefix(PREFIX);name=suffix.split('__')[-1]
        row=existing.get(suffix,copy.deepcopy(template))
        row.update(id=suffix,axis='diagnostic',formal=False,meaning='WI-073 '+suffix.replace('__',' / '),unit=unit(name),
            producers=[channel],calculation=None,role='derived',depends_on=[],included_scope=['Bounded WI-073 matched-cycle scenario'],excluded_scope=[],
            reference_value=None,conversion={'basis':'single_module_current_model','allowed_basis_conversions':[],'allowed_units':[unit(name)]},
            validity_limits=['Fixed supported pressure/property domains; component assumptions remain conditional.','Required UA is not installed capacity or price; turbine and site qualification remain unresolved.'])
        row.pop('role_input',None);row.pop('price_basis',None)
        enabled=matched if '__matched_cycle__' in channel else cooling if '__cooling_water__' in channel else None
        if enabled and name!='active':row['availability_when']=[{'input':enabled,'equals':1}]
        if suffix not in existing:manifest['quantities'].append(row)
    meanings={'p_th':'Total heat admitted at the power-balance boundary','p_the':'Gross thermal-generator electricity before plant recirculation',
        'p_et':'Gross electricity; equals thermal-generator electricity in this no-direct-conversion plant',
        'p_net':'Export electricity after all represented recirculating loads',
        'recirculating_power':'Gross minus exported electricity, including selected steam and cooling-water pumps once'}
    for row in manifest['quantities']:
        if row['id'] in meanings:row['meaning']=meanings[row['id']]
    inventory=json.loads((here/'diagnostic-inventory.json').read_text())
    for row in inventory['diagnostics']:
        if row['id']=='cycle_interface_ok' or row['channel'].startswith(PREFIX+'turbine__cycle__'):
            row['active_when']=[{'input':matched,'equals':0}]
            row['meaning']+=' (raw historical-fit diagnostic; applicable only with matched cycle disabled)' if '(raw historical-fit' not in row['meaning'] else ''
    inventory['predicate_applicability']={}
    for entry in contract['constraint_catalog']['concrete_entries']:
        local=entry['source_local_identity']
        if local=='cycle_domain_ok':conditions=[{'input':matched,'equals':0}]
        elif local in ('matched_main_heat_direction','matched_reheat_heat_direction'):conditions=[{'input':matched,'equals':1}]
        elif local=='cooling_water_heat_direction':conditions=[{'input':cooling,'equals':1}]
        else:continue
        inventory['predicate_applicability'][entry['constraint_id']]=conditions
    ids={row['id'] for row in inventory['diagnostics']}
    for channel in delta['added_channels']:
        suffix=channel.removeprefix(PREFIX);name=suffix.split('__')[-1]
        if suffix in ids:continue
        enabled=matched if '__matched_cycle__' in channel else cooling if '__cooling_water__' in channel else None
        interpretation='equal_one' if name in ('main_admission_ok','reheat_admission_ok','cooling_approach_ok') else 'report_only'
        inventory['diagnostics'].append({'id':suffix,'channel':channel,'unit':unit(name),
            'kind':'physical_screen' if interpretation=='equal_one' else 'qualification' if name.endswith('_qualified') else 'cycle_diagnostic',
            'meaning':'Raw WI-073 '+suffix.replace('__',' / '),'interpretation':interpretation,
            'active_input':enabled if name!='active' else None,'source':'models/library/analyses/mfe_matched_steam_cycle.sysml',
            'affects':['net_power','lcoe']})
    inventory['unresolved_essential_evidence']=[value for value in inventory['unresolved_essential_evidence'] if value!='Cooling-to-electricity performance lacks a matched cycle basis.']
    for value in ('Matched-cycle integrated source/state/heat/work verification remains a prerequisite for adoption.','Turbine equipment and cooling-water site qualification remain unresolved.','The full historical 3% allowance plus explicit pumps retains unresolved auxiliary overlap.'):
        if value not in inventory['unresolved_essential_evidence']:inventory['unresolved_essential_evidence'].append(value)
    inventory['status']='WI-073 draft applicability and diagnostics; raw legacy results retained'
    (here/'diagnostic-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')


if __name__=='__main__':
    print(json.dumps(refresh(Path.cwd(),Path(__file__).parent),indent=2))
