"""Current candidate contract and immutable first-attempt behavior."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'.project/active/aries-comparison-preparation/current-readiness/candidate'
sys.path.insert(0,str(HERE))
from candidate_common import typed, strict_json, validate_rules, exclusive_document
from execute_frozen import execute, select_inputs


def test_runtime_identity_allows_relocation_but_rejects_changed_content():
    import copy
    from runtime_identity import verify
    expected=json.loads((HERE/'runtime-requirements.json').read_text())
    relocated=copy.deepcopy(expected)
    relocated['interpreter']='/restored/python'
    relocated['teax']['root']='/restored/teax'
    for module in relocated['modules'].values(): module['import_path']='/restored/module'
    assert verify(expected,relocated)['status']=='pass'
    for section,name,field in [('modules','syside','module_file_sha256'),
                               ('sealed_wheels','codegen','sha256')]:
        changed=copy.deepcopy(relocated);changed[section][name][field]='changed'
        with pytest.raises(ValueError,match='runtime identity mismatch'): verify(expected,changed)
    for field,value in [('commit','changed'),('runtime_python_files',{}),('runtime_dirty_status',' M runtime.py')]:
        changed=copy.deepcopy(relocated);changed['teax'][field]=value
        with pytest.raises(ValueError,match='runtime identity mismatch'): verify(expected,changed)


@pytest.mark.parametrize('channel,failure',[
    ('heat_transport__equipment__salt_electric_MW','total_pump_electric_once'),
    ('pb__p_net','net_electric_balance'),
    ('pb__p_th','thermal_balance'),
])
@pytest.mark.parametrize('scenario',['historical-disabled','matched'])
def test_power_account_rejects_inconsistent_retained_output(tmp_path,channel,failure,scenario):
    from check_accounting import check
    source=ROOT/'work/orchestration/goals/current-model-comparison-readiness/evidence/entering-validation/baseline/baseline_result.json'
    baseline=json.loads(source.read_text())
    rules=json.loads((HERE/'input-rules.json').read_text())
    if scenario=='historical-disabled':
        delta=json.loads((HERE.parent/'regression-evidence/cycle-migration/contract-delta.json').read_text())
        additions={key:False if kind=='bool' else 0. for key,kind in delta['added_channels'].items()}
        prefix='stellarator_09__stellaris__'
        additions.update({prefix+'turbine__cycle_selection__eta_selected':baseline['channels'][prefix+'turbine__cycle__eta_th'],
            prefix+'turbine__cycle_selection__legacy_domain_applicable':True})
        native={'state':'completed','effective_inputs':rules['default_values']|baseline['point']|delta['historical_controls'],
            'outputs':baseline['channels']|additions,'verdicts':{r['constraint_id']:r['status'] for r in baseline['verdicts']}}
    else:
        cases=json.loads((ROOT/'work/active/WI-073_matched-steam-cycle-for-current-comparison/evidence/independent-oracle/native-check-results.json').read_text())
        case=next(row for row in cases if row['label']=='baseline')
        contract=json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
        assert case['semantic_fingerprint']==contract['semantic_fingerprint']
        native={'state':'completed','effective_inputs':rules['default_values']|case['inputs'],
            'outputs':case['outputs'],'verdicts':{row['id']:row['actual'] for row in case['predicates']}}
    path=tmp_path/'native.json';path.write_text(json.dumps(native))
    assert check(ROOT,path)['status']=='pass'
    native['outputs']['stellarator_09__stellaris__'+channel]+=1.0
    path.write_text(json.dumps(native))
    result=check(ROOT,path)
    assert result['status']=='fail'
    assert not next(r for r in result['checks'] if r['name']==failure)['passed']


@pytest.mark.parametrize('value',[False,True])
def test_all_declared_boolean_defaults(value):
    rules=json.loads((HERE/'input-rules.json').read_text())
    keys=[key for key,kind in rules['input_types'].items() if kind=='bool']
    assert len(keys)==6
    for key in keys:
        changed=rules|{'default_values':rules['default_values']|{key:value}}
        assert validate_rules(changed)[key] is value
        changed['default_values'][key]=int(value)
        assert validate_rules(changed)[key] is value
        with pytest.raises(ValueError): typed(int(value),'bool',key)


@pytest.mark.parametrize('value',[2,-1,'true','1',None,[],{},float('nan'),float('inf')])
def test_boolean_coercion_refused(value):
    with pytest.raises(ValueError): typed(value,'bool','switch',stored=True)


@pytest.mark.parametrize('value',[True,False,'1',None,float('nan'),float('inf')])
def test_numeric_coercion_refused(value):
    with pytest.raises(ValueError): typed(value,'float','number')


def test_integer_type_and_unknown_declaration():
    with pytest.raises(ValueError): typed(1.0,'int','count')
    with pytest.raises(ValueError): typed(1,'invented','count')


@pytest.mark.parametrize('raw',[b'{',b'{"values":{},"values":{}}',b'{"values":NaN}',b'[]'])
def test_bad_raw_request_retained_before_identity(tmp_path,monkeypatch,raw):
    import check_lineage
    def forbidden(*args): raise AssertionError('identity must not be read')
    monkeypatch.setattr(check_lineage,'check',forbidden)
    request=tmp_path/'bad.json'; request.write_bytes(raw)
    out=tmp_path/'attempt'
    result=execute(ROOT,HERE/'input-rules.json',request,out)
    assert result['state']=='execution_refused'
    assert result['native_execution_started'] is False
    assert result['refusal_stage']=='request_decode'
    assert (out/'request.raw.json').read_bytes()==raw
    assert out.with_name(out.name+'.identity.json').exists()


def test_attempt_cannot_overwrite_first_result(tmp_path):
    out=tmp_path/'attempt';out.mkdir();(out/'sentinel').write_bytes(b'original')
    result=execute(ROOT,HERE/'input-rules.json',tmp_path/'missing.json',out)
    assert result['refusal_stage']=='attempt_creation'
    assert {p.name:p.read_bytes() for p in out.iterdir()}=={'sentinel':b'original'}
    assert len(list(tmp_path.glob('attempt.overwrite-refused-*/native-result.json')))==1


def test_missing_request_retained(tmp_path):
    result=execute(ROOT,HERE/'input-rules.json',tmp_path/'missing.json',tmp_path/'attempt')
    assert result['refusal_stage']=='request' and not result['native_execution_started']
    assert result['request_source'].endswith('missing.json')


def test_exclusive_report_retains_failure_and_refuses_overwrite(tmp_path):
    path=tmp_path/'report.json'
    def fail(): raise ValueError('named invalid producer')
    receipt,ok=exclusive_document(path,fail)
    original=path.read_bytes()
    assert not ok and 'named invalid producer' in receipt['error']
    with pytest.raises(FileExistsError): exclusive_document(path,lambda:{'pass':True})
    assert path.read_bytes()==original


def test_selected_forward_preserves_r2_selection():
    rules=json.loads((HERE/'input-rules.json').read_text())
    old=json.loads((HERE.parents[1]/'package/input-rules.json').read_text())
    assert rules['forward_overrides']==old['forward_overrides']
    assert rules['independent_reference_inputs']==old['independent_reference_inputs']
    point,classification=select_inputs(rules,{'run_kind':'verification','values':{}})
    assert point==old['forward_overrides'] and classification['run_kind']=='verification'


def test_held_calendar_passthrough_is_supplied_even_when_execution_refused():
    from export_model_values import extract
    rules=json.loads((HERE/'input-rules.json').read_text())
    validate_rules(rules)
    _, classification=select_inputs(rules,{'run_kind':'conditioned','values':{},
        'conditioned_seam':'held_calendar',
        'conditioned_values':{'stellarator_09__stellaris__availability_direct':0.8}})
    manifest=json.loads((HERE/'manifest.json').read_text())
    contract=json.loads((ROOT/manifest['package_path']/'contracts/model_contract.json').read_text())
    exported=extract(manifest,contract,classification|{'state':'execution_refused'})
    row=next(row for row in exported['quantities'] if row['id']=='availability')
    assert row['role_at_this_point']=='supplied'
    assert row['status']=='execution_not_completed' and row['model_value'] is None
    assert row['independent_prediction_credit'] is False


def test_manifest_keeps_formal_criteria_and_has_all_predicates():
    from scripts.compare_fixed_point import validate_manifest
    current=json.loads((HERE/'manifest.json').read_text())
    old=json.loads((HERE.parents[1]/'package/manifest.json').read_text())
    validate_manifest(current)
    formal=lambda m:{row['id']:(row['axis'],row['unit']) for row in m['quantities'] if row['formal']}
    assert formal(current)==formal(old)
    contract=json.loads((ROOT/current['package_path']/'contracts/model_contract.json').read_text())
    assert set(current['required_constraints'])=={row['constraint_id'] for row in contract['constraint_catalog']['concrete_entries']}
    assert all(row['reference_value'] is None for row in current['quantities'])


def test_draft_archive_is_deterministic_and_detects_changed_payload(tmp_path):
    import io
    import tarfile
    from build_freeze import build, verify
    here=tmp_path/'candidate';here.mkdir()
    (tmp_path/'payload.txt').write_text('original\n')
    (here/'candidate-identity.json').write_text(json.dumps({'status':'draft_candidate','base_revision':'fixture'}))
    (here/'archive-members.json').write_text(json.dumps(['payload.txt']))
    first=build(tmp_path,here,tmp_path/'a');second=build(tmp_path,here,tmp_path/'b')
    assert first['archive_sha256']==second['archive_sha256']
    original=tmp_path/'a/comparison-freeze.tar.gz'
    assert verify(original)['files']==1
    tampered=tmp_path/'tampered.tar.gz'
    with tarfile.open(original,'r:gz') as src, tarfile.open(tampered,'w:gz') as dst:
        for member in src.getmembers():
            payload=src.extractfile(member).read()
            if member.name=='payload.txt': payload=b'changed!\n'
            member.size=len(payload);dst.addfile(member,io.BytesIO(payload))
    with pytest.raises(ValueError,match='content mismatch'): verify(tampered)


@pytest.mark.parametrize('name',['../outside','/absolute','a/../b','.env','knowledge/holdout/aries-cs/paper.pdf',
                                 '.project/concepts/stellarator-mbse-demo.md','x/pkg_link/file','x/__pycache__/file.pyc'])
def test_archive_forbids_barred_or_unsafe_members(name):
    from build_freeze import safe_name
    with pytest.raises(ValueError): safe_name(name)


def test_archive_rejects_symlink_parent_and_live_database(tmp_path):
    from build_freeze import read_members
    directory=tmp_path/'actual';directory.mkdir();(directory/'data').write_text('data')
    (tmp_path/'link').symlink_to(directory,target_is_directory=True)
    members=tmp_path/'members.json';members.write_text(json.dumps(['link/data']))
    with pytest.raises(ValueError,match='symlink'): read_members(tmp_path,members)
    (tmp_path/'study.sqlite3').write_bytes(b'database');(tmp_path/'study.sqlite3-wal').write_bytes(b'pending')
    members.write_text(json.dumps(['study.sqlite3']))
    with pytest.raises(ValueError,match='not quiescent'): read_members(tmp_path,members)


def test_entry_schema_declarations_match_and_conflicts_refuse(tmp_path):
    from candidate_common import schema_declarations
    schemas=tmp_path/'schemas';schemas.mkdir()
    (schemas/'first.py').write_text('class First:\n    key: bool\n')
    rows=[{'qualified_name':'key','param_group':'first','python_type':'bool'}]
    assert schema_declarations(tmp_path,rows)=={'key':'bool'}
    with pytest.raises(ValueError,match='declarations differ'):
        schema_declarations(tmp_path,[rows[0]|{'python_type':'float'}])
    (schemas/'second.py').write_text('class Second:\n    key: float\n')
    with pytest.raises(ValueError,match='conflicting declared types'):
        schema_declarations(tmp_path,rows+[{'qualified_name':'key','param_group':'second','python_type':'float'}])


def test_engineering_report_keeps_unlisted_failures_and_source_limits_visible():
    from compare_candidate import engineering_evidence
    inventory={'diagnostics':[
        {'id':'heat','channel':'heat','kind':'physical_screen','interpretation':'equal_one','active_input':None},
        {'id':'price','channel':'price','kind':'source_domain','interpretation':'equal_one','active_input':None}],
        'unresolved_essential_evidence':['Unmatched conversion cycle']}
    report=engineering_evidence({'state':'completed','outputs':{'heat':0.,'price':0.},'verdicts':{'authored': 'satisfied'}},inventory)
    assert report['engineering_acceptance_withheld']
    assert report['adverse_or_missing_diagnostics']==['heat','price']
    assert [r['kind'] for r in report['diagnostics']]==['physical_screen','source_domain']
    assert report['authored_violations_or_unknowns']==[]


def test_reported_coil_lifetime_margin_is_not_promoted_to_fence():
    from compare_candidate import engineering_evidence
    inventory={'diagnostics':[{'id':'coil','channel':'coil','kind':'lifecycle_diagnostic','interpretation':'report_only','active_input':None}],
               'unresolved_essential_evidence':[]}
    report=engineering_evidence({'state':'completed','outputs':{'coil':-17.},'verdicts':{'authored':'satisfied'}},inventory,['authored'])
    assert report['diagnostics'][0]['value']==-17.
    assert report['diagnostics'][0]['status']=='reported'
    assert not report['engineering_acceptance_withheld']


def test_missing_engineering_diagnostic_is_explicit():
    from compare_candidate import engineering_evidence
    inventory={'diagnostics':[{'id':'heat','channel':'heat','kind':'physical_screen','interpretation':'equal_one','active_input':None}],
               'unresolved_essential_evidence':[]}
    report=engineering_evidence({'state':'completed','outputs':{},'verdicts':{}},inventory)
    assert report['diagnostics'][0]['status']=='missing_or_invalid'
    assert report['engineering_acceptance_withheld']


@pytest.mark.parametrize('change',['fixed_override','duplicate_independent','duplicate_seam'])
def test_rule_selection_policy_cannot_expand(change):
    rules=json.loads((HERE/'input-rules.json').read_text())
    if change=='fixed_override': rules['forward_overrides']['stellarator_09__stellaris__discount_rate']=.02
    elif change=='duplicate_independent': rules['independent_reference_inputs'].append(rules['independent_reference_inputs'][0])
    else: rules['conditioned_seams'].append(rules['conditioned_seams'][0])
    with pytest.raises(ValueError,match='selection policy'): validate_rules(rules)


def test_wrong_sibling_rules_are_retained_and_refused(tmp_path,monkeypatch):
    import check_lineage
    monkeypatch.setattr(check_lineage,'check',lambda *args:pytest.fail('must refuse before identity'))
    wrong=tmp_path/'alternative.json';wrong.write_bytes((HERE/'input-rules.json').read_bytes())
    result=execute(ROOT,wrong,{'run_kind':'verification','values':{}},tmp_path/'attempt')
    assert result['refusal_stage']=='rules' and not result['native_execution_started']
    assert 'canonical' in result['error']


def test_table5_is_fixed_empty_control():
    rules=json.loads((HERE/'input-rules.json').read_text())
    row=next(row for row in rules['independent_reference_inputs'] if row['key'].endswith('n_e0'))
    record={'value':rules['default_values'][row['key']],'unit':row['unit'],'source':'synthetic','definition':'synthetic','resolution':'matched'}
    request={'run_kind':'conditioned','conditioned_seam':'table5_geometry_field','values':{row['key']:record},'conditioned_values':{}}
    with pytest.raises(ValueError,match='fixed Table5'): select_inputs(rules,request)
    with pytest.raises(ValueError,match='must be an object'): select_inputs(rules,request|{'values':{},'conditioned_values':[]})


@pytest.mark.parametrize('bad',[float('nan'),float('inf'),-float('inf')])
def test_nonfinite_native_result_has_raw_and_canonical_failure_receipts(tmp_path,monkeypatch,bad):
    from types import SimpleNamespace
    import check_lineage
    from exploration.stellarator_e2e.studies import study_route
    contract=json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
    outputs={r['channel_name']:0. for r in contract['outputs'] if r['python_type'] in ('float','int','bool')}
    bad_key=next(iter(outputs));outputs[bad_key]=bad
    verdicts={r['constraint_id']:'satisfied' for r in contract['constraint_catalog']['concrete_entries']}
    case=SimpleNamespace(state='completed',candidate_id='synthetic',executable_fingerprint='synthetic',outputs=outputs,verdicts=verdicts)
    out=tmp_path/'attempt'
    monkeypatch.setattr(check_lineage,'check',lambda *args:{'status':'synthetic identity stub'})
    monkeypatch.setattr(study_route,'run_points',lambda *args,**kwargs:([case],out/'native/study.sqlite3'))
    monkeypatch.setattr(study_route,'short_verdicts',lambda *args:{})
    result=execute(ROOT,HERE/'input-rules.json',{'run_kind':'verification','values':{}},out)
    assert result['state']=='invalid_native_result' and result['native_execution_started']
    assert result['outputs'][bad_key]=={'nonfinite_value':repr(bad)}
    assert (out/'native-result.raw.json').exists()
    assert strict_json((out/'native-result.json').read_text())['refusal_stage']=='result_validation'
    assert out.with_name(out.name+'.identity.json').exists()


def test_failure_after_native_start_is_retained(tmp_path,monkeypatch):
    import check_lineage
    from exploration.stellarator_e2e.studies import study_route
    monkeypatch.setattr(check_lineage,'check',lambda *args:{'status':'synthetic identity stub'})
    def fail(*args,**kwargs): raise ZeroDivisionError('synthetic invalid calculation')
    monkeypatch.setattr(study_route,'run_points',fail)
    result=execute(ROOT,HERE/'input-rules.json',{'run_kind':'verification','values':{}},tmp_path/'attempt')
    assert result['native_execution_started'] and result['refusal_stage']=='native_execution'
    assert 'synthetic invalid calculation' in result['error']


def test_document_retains_raw_malformed_input_and_overwrite_refusal(tmp_path):
    source=tmp_path/'malformed.json';source.write_bytes(b'{')
    output=tmp_path/'report.json'
    result,ok=exclusive_document(output,lambda:strict_json(source.read_text()),inputs=[source])
    assert not ok
    attempt=next(tmp_path.glob('report.json.attempt-*'))
    if attempt.is_file(): attempt=next(p for p in tmp_path.glob('report.json.attempt-*') if p.is_dir())
    assert (attempt/'input-0.raw').read_bytes()==b'{'
    assert json.loads((attempt/'receipt.json').read_text())['inputs'][0]['sha256']
    with pytest.raises(FileExistsError): exclusive_document(output,lambda:pytest.fail('producer must not run'),inputs=[source])
    assert len(list(tmp_path.glob('report.json.overwrite-refused-*/receipt.json')))==1


@pytest.mark.parametrize('name',[
    'exploration/concept_analysis/analyses/09-qi-stellarator-hts/artificial',
    'knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/aries-cs-compact-stellarator-study.md',
    'knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/aries-cs-systems-optimization/artificial',
    'knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/helios-stellarator-comparison.md',
    'knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/artificial',
    'knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/academia-144327326-the-aries-cs-compact-stellarator-fusion-artificial',
    'knowledge/sources/aries_cost_account_documentation/artificial',
    'knowledge/sources/tea_dt_mfe_cost_analysis/artificial',
    'knowledge/research/pending/20260912-115614_stellaris-structural-behavioral-modeling.md',
    'work/active/WI-009_mfe-cost-structure-library/design.md'])
def test_complete_protocol_named_exclusions_without_opening_content(name):
    from build_freeze import safe_name
    with pytest.raises(ValueError,match='protocol-barred'): safe_name(name)


def test_facility_children_reject_extra_zero_and_missing_members():
    from check_accounting import facility_children
    inventory=json.loads((HERE/'account-inventory.json').read_text())
    outputs={key:0. for key in inventory['facility_civil_children']}
    prefix='stellarator_09__stellaris__'
    assert len(facility_children(outputs,inventory,prefix))==25
    extra=outputs|{prefix+'buildings__invented__civil__cost_2025':0.}
    with pytest.raises(ValueError,match='inventory differs'): facility_children(extra,inventory,prefix)
    del outputs[next(iter(outputs))]
    with pytest.raises(ValueError,match='inventory differs'): facility_children(outputs,inventory,prefix)


def test_missing_predicates_withhold_engineering_acceptance_even_without_other_limits():
    from compare_candidate import engineering_evidence
    report=engineering_evidence({'state':'completed','outputs':{},'verdicts':{}},
        {'diagnostics':[],'unresolved_essential_evidence':[]},['required'])
    assert report['engineering_acceptance_withheld']
    assert report['missing_predicates']==['required']
    assert not report['predicate_inventory_complete']


def test_comparison_preserves_fallback_and_original_forward_identity(tmp_path):
    from compare_candidate import compare
    from candidate_common import digest
    manifest=json.loads((HERE/'manifest.json').read_text())
    verdicts={key:'satisfied' for key in manifest['required_constraints']}
    native={'run_kind':'blind','state':'completed','outputs':{},'verdicts':verdicts,
            'held_fallback':True,'missing_independent_inputs':['synthetic_missing'],
            'supplied_input_keys':[],'candidate_id':'synthetic-forward','executable_fingerprint':'synthetic-executable'}
    observation={'schema_version':1,'run_kind':'blind','execution_status':'completed',
                 'constraints':{key:True for key in verdicts},'extrapolations':[],'quantities':{}}
    first=tmp_path/'first.json';first.write_text(json.dumps(native))
    obs=tmp_path/'observations.json';obs.write_text(json.dumps(observation))
    report=compare(ROOT,first,obs)
    assert report['input_selection']['held_fallback'] is True
    assert report['input_selection']['missing_independent_inputs']==['synthetic_missing']
    assert report['original_forward']['native_result_sha256']==digest(first)
    assert not report['numerical_comparison']['numerical_comparison_pass']
    later=tmp_path/'conditioned.json';later.write_text(json.dumps(native|{'run_kind':'conditioned','candidate_id':'synthetic-conditioned'}))
    obs.write_text(json.dumps(observation|{'run_kind':'conditioned'}))
    with pytest.raises(ValueError,match='original forward'): compare(ROOT,later,obs)
    report=compare(ROOT,later,obs,original_forward=first)
    assert report['original_forward']['native_result_sha256']==digest(first)
    assert report['original_forward']['relationship']=='conditioned follow-up'
    wrong=tmp_path/'wrong.json';wrong.write_text(json.dumps(native|{'executable_fingerprint':'different'}))
    with pytest.raises(ValueError,match='identities differ'): compare(ROOT,later,obs,original_forward=wrong)


def test_held_efficiency_disables_both_new_modules_and_labels_dependents():
    rules=json.loads((HERE/'input-rules.json').read_text())
    p='stellarator_09__stellaris__'
    point,classification=select_inputs(rules,{'run_kind':'conditioned','conditioned_seam':'held_cycle','values':{},'conditioned_values':{p+'turbine__eta_th_direct':.333}})
    assert point[p+'turbine__cycle_live']==point[p+'turbine__matched_cycle_enabled']==point[p+'heat_rejection__cooling_water_enabled']==0.
    assert point[p+'turbine__eta_th_direct']==.333
    assert classification['conditioned_output_roles'][p+'turbine__cycle_selection__eta_selected']=='supplied'
    for key in ('pb__p_et','pb__p_net','lcoe_calc__lcoe'):
        assert classification['conditioned_output_roles'][p+key]=='derived_from_supplied_efficiency'
    broken=json.loads(json.dumps(rules))
    next(s for s in broken['conditioned_seams'] if s['id']=='held_cycle')['keys'].pop(p+'heat_rejection__cooling_water_enabled')
    with pytest.raises(ValueError,match='selection policy'):select_inputs(broken,{'run_kind':'verification','values':{}})


def test_inactive_cycle_placeholders_are_unavailable_export_predictions():
    from export_model_values import extract
    q={'id':'steam_state','axis':'diagnostic','producers':['enthalpy'],'calculation':None,'role':'derived','unit':'kJ/kg','applicability':'conditional','availability_when':[{'input':'matched','equals':1}]}
    contract={'parameters':[],'constraint_catalog':{'concrete_entries':[]}}
    native={'state':'completed','effective_inputs':{'matched':0.},'outputs':{'enthalpy':0.}}
    row=extract({'quantities':[q]},contract,native)['quantities'][0]
    assert row['status']=='inactive_prediction' and row['model_value'] is None and row['raw_model_value']==0.
    row=extract({'quantities':[q]},contract,native|{'effective_inputs':{}})['quantities'][0]
    assert row['status']=='unknown_applicability' and row['model_value'] is None


@pytest.mark.parametrize('mode',[0.,1.,None,.5])
def test_raw_legacy_failure_retained_with_exact_mode_applicability(mode):
    from compare_candidate import engineering_evidence
    inventory={'diagnostics':[],'unresolved_essential_evidence':[],
        'predicate_applicability':{'legacy':[{'input':'matched','equals':0}]}}
    native={'state':'completed','effective_inputs':{} if mode is None else {'matched':mode},'outputs':{},'verdicts':{'legacy':'violated','current':'satisfied'}}
    report=engineering_evidence(native,inventory,['legacy','current'])
    assert report['authored_violations_or_unknowns']==['legacy']
    if mode==1.:
        assert report['inactive_predicates']==['legacy'] and not report['engineering_acceptance_withheld']
    else:assert report['engineering_acceptance_withheld']
    if mode in (None,.5):assert report['unknown_predicate_applicability']==['legacy']


@pytest.mark.parametrize('declared,expected', [('bool',False),('bool',0.),('float',False)])
@pytest.mark.parametrize('native,passed', [(0.,True),(1e-12,False),(1.,False)])
def test_selected_mode_status_requires_exact_boolean_value(tmp_path,monkeypatch,declared,expected,native,passed):
    from check_selected_mode import check
    from exploration.stellarator_e2e.studies import oracle_entry
    from scripts.study import verify
    package=tmp_path/'exploration/stellarator_e2e/generated'
    (package/'contracts').mkdir(parents=True)
    contract={'outputs':[{'channel_name':'status','python_type':declared},
                         {'channel_name':'scalar','python_type':'float'}],
              'constraint_catalog':{'concrete_entries':[]}}
    (package/'contracts/model_contract.json').write_text(json.dumps(contract))
    monkeypatch.setattr(oracle_entry,'evaluate',lambda _: {'status':expected,'scalar':0.})
    monkeypatch.setattr(oracle_entry,'operand_bindings',lambda: {})
    monkeypatch.setattr(verify,'package_input_values',lambda _: {})
    path=tmp_path/'native.json'
    path.write_text(json.dumps({'state':'completed','requested_overrides':{},
        'outputs':{'status':native,'scalar':1e-12},'verdicts':{}}))
    result=check(tmp_path,path)
    assert (result['status']=='pass') is passed
    assert [r['channel'] for r in result['numeric_discrepancies']]==([] if passed else ['status'])
