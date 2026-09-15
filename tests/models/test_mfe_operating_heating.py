"""WI-050 native operating-state, independent conservation and consumer regressions."""
from __future__ import annotations
from tests.models.current_mfe_regressions import WI060_PARAMETERS, WI059_PARAMETERS, WI059_CHANNELS, WI059_NATIVE_ONLY_PARAMETERS, WI059_NATIVE_ONLY_VALUES, WI059_REPLAY_LOCAL

from tests.models.current_mfe_regressions import WI061_PARAMETERS, WI061_MAPPED_PARAMETERS, WI061_CHANNELS, WI062_PARAMETERS

import importlib.util
import json
import math
import shutil
import subprocess
from pathlib import Path
import pytest
import yaml

ROOT=Path(__file__).resolve().parents[2]
SUPPORT=ROOT/'work/active/WI-050_mfe-coherent-operating-heating/implementation'
P='stellarator_09__stellaris__'
# WI-057 (2026-09-13): the calcs live on the parts that own them; entry points and channels carry the
# part's path. Keys handed to the package or the verifier use the new names; the frozen drivers'
# results are aliased under both spellings by tests.models.current_mfe_regressions.
LEDGER=json.loads((ROOT/'work/active/WI-057_stellaris-structural-decomposition/evidence/merge_onto_demo_maturation/ledger.json').read_text())
RENAMED={**LEDGER['parameters'],**LEDGER['outputs']}
def renamed(key): return RENAMED.get(key,key)
def renamed_module(module):
    channel=next(k for k in LEDGER['outputs'] if k.startswith(P+module+'__'))
    return renamed(channel).rsplit('__',1)[0]
def renamed_qualified(name):
    """'<group>_params.<key>', '<channel>', or '<channel>.<accessor>' under the new names."""
    head,_,rest=name.partition('.')
    if head.endswith('_params'): return head+'.'+renamed(rest)
    return renamed(head)+('.'+rest if rest else '')
def renamed_ref(ref):
    """A pipeline input reference ('float <name>') under the new names."""
    kind,name=ref.rsplit(' ',1)
    return kind+' '+renamed_qualified(name)

def load(name):
    spec=importlib.util.spec_from_file_location('wi050_'+name,SUPPORT/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

@pytest.fixture(scope='module')
def native(tmp_path_factory):
    destination=tmp_path_factory.mktemp('wi050-evidence')
    harness=load('run_acceptance')
    from tests.models.current_mfe_regressions import operating_acceptance
    scratch,results,inputs=operating_acceptance(destination,harness)
    return scratch,results,inputs,destination

@pytest.fixture(scope='module')
def boundaries(native):
    _,_,_,destination=native
    shutil.copyfile(SUPPORT/'boundaries.py',destination/'boundaries.py')
    result=subprocess.run([str(ROOT/'.codex-test/run'),'python',str(destination/'boundaries.py')],cwd=ROOT,capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    return json.loads((destination/'boundary-results.json').read_text())

def test_operating_heat_signed_demand_bounds(boundaries):
    p='boundary_fixture__test__'
    for case,d in [('positive',12),('equality',37.5),('zero',0),('insufficient',38),('negative',-1)]:
        o=boundaries[case]['outputs'];r=boundaries[case]['responses']
        for key,v in [('p_coupled',d),('p_delivered',d/.75),('p_wallplug',d/(.75*.5))]:
            assert o[p+'operating_heat__'+key]==pytest.approx(v,rel=1e-9,abs=1e-9)
            if d==0: assert o[p+'operating_heat__'+key]==0
        assert o[p+'heat__p_delivered']==50
        for bound,rejected in [('upper',case=='insufficient'),('lower',case=='negative')]:
            assert [v for k,v in r.items() if '__'+bound+'__' in k]==['violated' if rejected else 'satisfied']

def test_generic_heating_default_modes(boundaries):
    o=boundaries['positive']['outputs']
    for name,expected in [('chain',(50,50,37.5,100)),('legacy',(50,40,30,80)),('mixed',(100,90,67.5,180)),('allzero',(0,0,0,0))]:
        p='boundary_fixture__'+name+'__'
        actual=[o[p+k] for k in ['heat__p_delivered','operating_heat__p_delivered','operating_heat__p_coupled','operating_heat__p_wallplug']]
        assert actual==list(expected)

def test_heating_efficiency_scalar_consumers(native,boundaries):
    from scripts.study import indicators,verify
    scratch,_,_,_=native
    entries=json.loads((scratch/'generated/contracts/model_contract.json').read_text())['constraint_catalog']['concrete_entries']
    assert len(entries)==20
    assert sum(len(verify.feature_refs(json.loads(e['predicate_ir']))) for e in entries)==30
    for entry in entries: indicators.predicate_operands(entry)
    new={e['source_local_identity']:e for e in entries if e['source_local_identity'].startswith('heating_')}
    assert set(new)=={'heating_source_positive_ok','heating_source_upper_ok','heating_couple_positive_ok','heating_couple_upper_ok'}
    bindings={e['constraint_id']:{'efficiency':{'kind':'input','key':P+('heating__eta_source_heat' if 'source' in name else 'heating__eta_couple_heat')}} for name,e in new.items()}
    for stage in ['source','couple']:
        for label,value in [('valid_one',1),('negative',-.5),('zero',0),('over_one',1.01)]:
            i={P+'heating__eta_source_heat':.5,P+'heating__eta_couple_heat':.75,P+'heating__eta_'+stage+'_heat':value}
            for name,entry in new.items():
                actual,count=verify.derive_verdict(entry['constraint_id'],entry,bindings,{},i,{})
                expected=(value>0 if 'positive' in name else value<=1) if stage in name else True
                assert actual==expected and count==1
            native_case=boundaries[stage+'_'+label]
            if value==0:
                assert native_case['error']=='EvaluationFailed'
                assert 'ZeroDivisionError' in native_case['message']
            else:
                for bound in ['positive','upper']:
                    expected='satisfied' if (value>0 if bound=='positive' else value<=1) else 'violated'
                    assert [v for k,v in native_case['responses'].items() if '__'+stage+'_'+bound+'__' in k]==[expected]
    entry=next(iter(new.values()))
    with pytest.raises(verify.VerifyError):
        verify.derive_verdict(entry['constraint_id'],entry,{}, {},{}, {})
    # Exercise the actual verifier's mismatch paths with current generated entries.
    # This local case fixture does not prepare or promote a study package.
    from types import SimpleNamespace
    baseline=native[1]['baseline']
    channel=P+'operating_heat__p_coupled'
    entries_by_id={e['constraint_id']:e for e in new.values()}
    case=SimpleNamespace(candidate_id='scalar-consumer-fixture',executable_fingerprint='local-fixture',inputs={},outputs={channel:baseline['outputs'][channel]},verdicts={key:baseline['responses'][key] for key in entries_by_id})
    evaluate=lambda _:dict(case.outputs)
    verify.check_case(case,evaluate,bindings,entries_by_id,{channel},native[2],'local-fixture')
    case.verdicts=dict(case.verdicts,**{entry['constraint_id']:'violated'})
    with pytest.raises(verify.VerifyError,match='verdict mismatch'):
        verify.check_case(case,evaluate,bindings,entries_by_id,{channel},native[2],'local-fixture')
    case.verdicts={key:baseline['responses'][key] for key in entries_by_id}
    with pytest.raises(verify.VerifyError,match='relative deviation'):
        verify.check_case(case,lambda _:{channel:case.outputs[channel]*1.001},bindings,entries_by_id,{channel},native[2],'local-fixture')


def test_stellarator_operating_heat_has_no_public_demand_input(native):
    scratch,results,_,_=native
    contract=json.loads((scratch/'generated/contracts/model_contract.json').read_text())
    assert len(contract['parameters'])==265 + len(WI059_PARAMETERS | WI060_PARAMETERS | WI059_NATIVE_ONLY_PARAMETERS | WI061_PARAMETERS | WI062_PARAMETERS)  # WI-059 adds21public inputs and3native-only literals.
    assert not any('p_operating_coupled_heat' in str(p) for p in contract['parameters'])
    modules=yaml.safe_load((scratch/'generated/pipelines/pipeline.yaml').read_text())['modules']
    expected={'operating_heat':{'p_required_in':'sustain.p_aux_required'},'source_heat':{'p_input_in':'operating_heat.p_coupled'},'pb':{'p_input_in':'operating_heat.p_coupled','p_wallplug_in':'operating_heat.p_wallplug'},'divheat':{'p_coupled_in':'operating_heat.p_coupled','p_installed_coupled_in':'heat.p_coupled'},'primary_loop':{'q_source_in':'source_heat.q_source.root'},'heating_cost':{'p_ecrh_in':'heat.p_delivered'}}
    for module,formals in expected.items():
        for formal,target in formals.items():
            actual=modules[renamed_module(module)]['inputs'][formal]  # WI-057: the module carries its part's path
            producer,output=target.split('.',1)
            assert actual.split()[-1]==renamed_qualified(P+producer+'__'+output),(module,formal,actual)
    assert results['baseline']['responses']['headline']=='violated'

def test_operating_heat_reserve_invariance(native):
    _,results,inputs,_=native
    # Frozen WI-050 checker retains its original eighteen-predicate scope.
    historical = {name: (dict(row, responses={k: v for k, v in row['responses'].items() if 'wp_fit_ok' not in k and 'reference_conductor_current_ok' not in k}) if 'responses' in row else row) for name, row in results.items()}
    load('check_results').check(historical,inputs)
    for case,expected in [('baseline',-.920399212073221),('reserve',-10.920399212073221)]:
        assert results[case]['outputs'][P+'divheat__p_heat_operating_minus_installed']==pytest.approx(expected,rel=1e-9,abs=1e-9)

def test_operating_heat_financial_attribution(native):
    _,results,inputs,_=native
    checker=load('check_results')
    for case,controls in load('run_acceptance').CASES.items():
        if case in ['negative_efficiency','zero_efficiency','overunit_efficiency']:continue
        checker.check_case(results[case]['outputs'],dict(inputs,**{P+k:v for k,v in controls.items()}))

def test_operating_heat_direct_native_parity(native,monkeypatch):
    import sys
    sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e'))
    import verify_stellaris
    _,results,_,_=native
    # Resolve the map without importing run_stellaris's global package loader.
    import ast
    tree=ast.parse((ROOT/'exploration/stellarator_e2e/run_stellaris.py').read_text())
    assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CH' for t in n.targets))
    channels=eval(compile(ast.Expression(assignment.value),'<channel-map>','eval'),{'P':P})
    for case in ['baseline','reserve','demand','efficiency','availability']:
        with monkeypatch.context() as context:
            context.setattr(verify_stellaris,'IN',verify_stellaris.IN | WI059_REPLAY_LOCAL | load('run_acceptance').CASES[case])
            expected=verify_stellaris.compute()
        runner=ast.parse((ROOT/'exploration/stellarator_e2e/run_stellaris_single.py').read_text())
        verdict_assignment=next(n for n in runner.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EXPECTED_VERDICTS' for t in n.targets))
        expected_verdicts=ast.literal_eval(verdict_assignment.value)
        assert len(expected_verdicts)==20
        if case in ['baseline','reserve','demand','availability']:
            actual={key.split('__')[2]:value for key,value in results[case]['responses'].items() if key!='headline'}
            assert actual==expected_verdicts
        gate=next(n for n in runner.body if isinstance(n,ast.FunctionDef) and n.name=='_oracle_gate')
        assignment=next(n for n in gate.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='compared' for t in n.targets))
        values=results[case]['outputs']
        compared=eval(compile(ast.Expression(assignment.value),'<direct-consumer-map>','eval'),{'P':P,'CH':channels,'values':values,'total':values[P+'total_capital__total_capital']})
        for key,value in compared.items():
            assert value==pytest.approx(expected[key],rel=1e-9,abs=1e-9),(case,key)

def test_operating_heat_definition_structure():
    text=(ROOT/'models/library/analyses/mfe_heating_chain.sysml').read_text()
    for name in ['Operating Heating Power','Heating Efficiency Positive','Heating Efficiency Upper']:
        assert text.count("def '"+name+"'")==1
    for path in (ROOT/'models/designs').rglob('*.sysml'):
        import re
        assert not re.search(r'^\s*calc def ',path.read_text(),re.MULTILINE)


def test_operating_heat_complete_cost_operand_classification(native,monkeypatch):
    import sys
    sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e'))
    import verify_stellaris
    scratch,results,_,_=native
    mapping={
        'heating_cost__cost':'heating','blanket_cost__cost':'blanket','shield_cost__cost':'shield',
        'structure_cost__cost':'structure','vessel_cost__cost':'vessel','power_supplies_cost__cost':'power_supplies',
        'divertor_cost__cost':'divertor','turbine_cost__cost':'turbine','electric_cost__cost':'electric',
        'heat_rejection_cost__cost':'heat_rejection','misc_cost__cost':'misc','buildings_cost__cost':'buildings',
        'precon_cost__cost':'precon','om_cost__annual_om':'annual_om_unlevelized',
        'remote_handling__cost':'remote_handling','coolant__cost':'coolant','aux_cooling__cost':'aux_cooling',
        'waste__cost':'waste','fuel_handling__cost':'fuel_handling','other_rpe__cost':'other_rpe',
        'inc_cost__cost':'inc','owner__cost':'owner','supplementary__cost':'supplementary',
        'installation__cost':'installation','powercore_capital__powercore_capital':'powercore_capital',
        'bop_capital__bop_capital':'bop_capital','cas22_capital__cas22_capital':'cas22_capital',
        'special_materials_capital__special_materials_capital':'special_materials',
        'cas23_to_28_capital__cas23_to_28_capital':'cas23_to_28_capital',
        'cas2x_pre_contingency__cas2x_pre_contingency':'cas2x_pre_contingency',
        'contingency__cost':'contingency_capital','cas20_capital__cas20_capital':'cas20_capital',
        'indirect__cost':'indirect_capital','overnight_capital__overnight_capital':'overnight_capital',
        'total_capital__total_capital':'total_capital','idc__cost':'idc_capital'}
    for case in ['baseline','reserve','demand','availability']:
        with monkeypatch.context() as context:
            context.setattr(verify_stellaris,'IN',verify_stellaris.IN | WI059_REPLAY_LOCAL | load('run_acceptance').CASES[case])
            direct=verify_stellaris.compute()
        for channel,key in mapping.items():
            assert results[case]['outputs'][P+channel]==pytest.approx(direct[key],rel=1e-9,abs=1e-9),(case,channel)
    old=yaml.safe_load(subprocess.check_output(['git','show','546218a5:exploration/stellarator_e2e/generated/pipelines/pipeline.yaml'],cwd=ROOT))['modules']
    current=yaml.safe_load((scratch/'generated/pipelines/pipeline.yaml').read_text())['modules']
    # WI-057: compare the historical (flat-named) module inputs through the rename ledger.
    for channel in mapping:
        module=P+channel.rsplit('__',1)[0]
        expected_inputs={k:renamed_ref(v) for k,v in old[module]['inputs'].items()}
        if channel == 'structure_cost__cost':
            expected_inputs['residual_fraction']='float stellarator_plant_params.'+P+'structure__residual_fraction'
        elif channel == 'aux_cooling__cost':
            expected_inputs['p_cryo']='float '+P+'cryoplant__refrigeration_sum__total.root'
        elif channel == 'powercore_capital__powercore_capital':
            expected_inputs['structure_capital_cost']='float '+P+'structure__structure_cost__cost'
        assert current[renamed_module(channel.rsplit('__',1)[0])]['inputs']==expected_inputs,module
    assert current[renamed_module('primary_loop')]['inputs'] == {k:renamed_ref(v) for k,v in old[P+'primary_loop']['inputs'].items()}
    assert current[renamed_module('primary_loop')]['outputs'] == {k:renamed_ref(v) for k,v in old[P+'primary_loop']['outputs'].items()}
    # WI-056 owns only the Primary Coolant Loop definition. Preserve the source
    # outside that exact boundary, alongside the independent cost/operand checks.
    path='models/library/analyses/mfe_primary_loop.sysml'
    def outside_primary_definition(text):
        start = text.index("    calc def 'Primary Coolant Loop'")
        end = text.rindex('\n}')
        return text[:start], text[end:]
    previous = subprocess.check_output(['git','show','546218a5:'+path],cwd=ROOT).decode()
    assert outside_primary_definition((ROOT/path).read_text()) == outside_primary_definition(previous)
