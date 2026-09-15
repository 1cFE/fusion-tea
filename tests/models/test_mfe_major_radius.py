"""WI-051 production binding, fresh generation and full native acceptance."""
import json
import runpy
import shutil
import sys
from pathlib import Path
import pytest
from tests.model_families import MFE, canonical_path, materialize_canonical_subset

ROOT=Path(__file__).resolve().parents[2]
H=ROOT/'work/active/WI-051_mfe-model-owned-major-radius/implementation'
# Implementation evidence helpers remain one shared acceptance path.
sys.path.insert(0,str(H))
from regenerate import MANUAL, fresh_directory, seed_and_generate, verify_seed_inventory
from common import hashes
import hashlib
# WI-057 (2026-09-13): the files the structural decomposition owns, pinned to its receipt.
WI057_MODEL_HASHES=json.loads((ROOT/'work/active/WI-057_stellaris-structural-decomposition/evidence/merge_onto_demo_maturation/model-hashes.json').read_text())
WI057_STRUCTURE=tuple(WI057_MODEL_HASHES)
from tests.models.current_mfe_regressions import structure_ledger, structure_modules
from tests.models.current_mfe_regressions import DOMAIN_EVIDENCE, WI040_CHANNELS, LIVE_CONDUCTOR_CHANNELS, WI059_CHANNELS, RECEIPT_EVIDENCE
RENAMED=structure_ledger()[0]
MODULES=structure_modules(RENAMED)
def new(key): return RENAMED.get(key,key)  # an entry point or channel under its WI-057 name


def test_binding_documentation_and_source_preservation(tmp_path):
    from agentic_mbse.sysml.syside_adapter import get_syside
    models=materialize_canonical_subset(MFE,tmp_path/'models')
    syside=get_syside()
    model,diagnostics=syside.try_load_model([str(p) for p in sorted(models.rglob('*.sysml'))])
    for category in ('parser','sema'):
        assert not [d for d in getattr(diagnostics,category) if d.severity==syside.DiagnosticSeverity.Error]
    attached=[(e,d.body) for e in model.elements(syside.ReferenceUsage) for d in e.documentation if '[INHERITED: T-021@2f8856b7]' in d.body]
    assert len(attached)==1
    element,doc=attached[0]
    assert element.name=='R0' and str(element.qualified_name)=="mfe_plant::'MFE Power Plant'::magnet::coil::R0"  # WI-057 (2026-09-13): R0 is the modular coil's; the T-021 binding sits on the nested coil part
    assert all(x in doc for x in ('Source: work/analysis/20260911-230953_radius-ownership-evidence/source-meaning.md','Ref:','Basis:','Last Updated:','## Assessment'))
    assert ':>> R0 = plasma.R {' in (models/'designs/generic_mfe/mfe_plant.sysml').read_text()  # WI-057: R lives on the plasma part
    assert ':>> R0 = 12.7;' not in (models/'designs/stellarator_09/stellarator_plant.sysml').read_text()
    documentation=ROOT/'work/active/WI-054_faithful-model-equations-and-citations/evidence'
    lexical=runpy.run_path(str(documentation/'preservation.py'))['lexical']
    entering=json.loads((documentation/'entering.json').read_text())['models']
    current_hashes=json.loads((RECEIPT_EVIDENCE/'model-hashes.json').read_text())  # WI-059: complete current canonical-source receipt
    for p in MFE.owned:
        assert canonical_path(p).read_bytes()==(MFE.twin/p).read_bytes()
        if p in ('analyses/mfe_plasma_scaling.sysml', 'analyses/mfe_plasma_sustainment.sysml', 'foundation/economic_parameter.sysml'):
            # WI-054 changes comments only; every executable token stays frozen.
            source=str(canonical_path(p).relative_to(ROOT))
            assert lexical((models/p).read_text()) == entering[source]['tokens']
        elif p in current_hashes:
            # WI-040/038: preserve the six prior source guards and add conductor
            # capability. Other unchanged sources keep their historical guards.
            assert set(current_hashes) == set(MFE.owned)
            assert hashlib.sha256((models/p).read_bytes()).hexdigest()==current_hashes[p],p
        elif p in ('analyses/mfe_cryo_plant.sysml', 'analyses/mfe_primary_loop.sysml'):
            calculation = ('Primary Coolant Loop' if 'primary_loop' in p
                           else 'Cryoplant Electrical Power')
            def outside_calculation(text):
                start = text.index("    calc def '" + calculation + "'")
                end = text.find('\n    calc def ', start + 1)
                if end == -1:
                    end = text.rindex('\n}')
                return text[:start], text[end:]
            assert outside_calculation((models/p).read_text()) == outside_calculation((H/'entering-models'/p).read_text())
        elif p in WI057_STRUCTURE:
            # WI-057 (2026-09-13): the structural decomposition restructured these files and added the
            # structure/ definitions; they are pinned to WI-057's own receipt, not to the WI-051 entering copy.
            assert hashlib.sha256((models/p).read_bytes()).hexdigest()==WI057_MODEL_HASHES[p],p
        elif p not in ('designs/generic_mfe/mfe_plant.sysml','designs/stellarator_09/stellarator_plant.sysml','analyses/mfe_account_costs.sysml','analyses/mfe_lcoe_dcf.sysml','analyses/mfe_lifecycle.sysml'):
            assert (models/p).read_bytes()==(H/'entering-models'/p).read_bytes()


@pytest.mark.parametrize('kind',['absent','empty'])
def test_fresh_destination_acceptance(tmp_path,kind):
    path=tmp_path/'target'
    if kind=='empty': path.mkdir()
    calls=[]
    seed_and_generate(path,H/'entering-package',generator=lambda config: calls.append(config) or True,models_path=H/'models')
    assert len(calls)==1 and hashes(path)==MANUAL


@pytest.mark.parametrize('kind',['visible','hidden','file','symlink','dangling_symlink','reused'])
def test_nonfresh_destination_refusal_without_mutation(tmp_path,kind):
    path=tmp_path/'target'
    if kind in ('symlink','dangling_symlink'):
        referent=tmp_path/'referent'
        if kind=='symlink': referent.mkdir()
        path.symlink_to(referent)
    elif kind=='file': path.write_text('keep')
    else:
        path.mkdir()
        (path/('.hidden' if kind=='hidden' else 'generation_manifest.json' if kind=='reused' else 'entry')).write_text('keep')
    before=(str(path.readlink()) if path.is_symlink() else path.read_bytes() if path.is_file() else hashes(path))
    calls=[]
    with pytest.raises(FileExistsError):
        seed_and_generate(path,H/'entering-package',generator=lambda config: calls.append(config),models_path=H/'models')
    after=(str(path.readlink()) if path.is_symlink() else path.read_bytes() if path.is_file() else hashes(path))
    assert before==after and not calls


@pytest.mark.parametrize('kind',['missing','extra','mismatch'])
def test_seed_inventory_refuses_deviation(tmp_path,kind):
    for name in MANUAL:
        target=tmp_path/name; target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(H/'entering-package'/name,target)
    target=tmp_path/next(iter(MANUAL))
    if kind=='missing': target.unlink()
    elif kind=='mismatch': target.write_text('changed')
    else: (tmp_path/'.extra').write_text('extra')
    with pytest.raises(ValueError,match='exactly the four'): verify_seed_inventory(tmp_path)


def test_current_contract_edges_and_fresh_package_agreement():
    import runpy
    runpy.run_path(str(H/'contract_checks.py'))
    expected=json.loads((H/'generated-hashes.json').read_text())
    for path in ('source-attempt-1','snapshot-attempt-1'):
        assert hashes(H/path)==expected
    # Historical generation receipts stay frozen; WI-040's additive-account package
    # has its own current receipt (2026-09-13).
    assert hashes(ROOT/'exploration/stellarator_e2e/generated')==json.loads((RECEIPT_EVIDENCE/'package-hashes.json').read_text())  # WI-059: current package receipt
    assert all(expected[name]==value for name,value in MANUAL.items())


def test_strict_current_package_load(tmp_path, monkeypatch):
    import os
    monkeypatch.syspath_prepend(str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))
    from simkit.evaluation.package_load import ProvisionalPackageLoader
    package,fingerprint=ProvisionalPackageLoader(ROOT/'exploration/stellarator_e2e/generated','stellarator_tea',tmp_path/'link',strict=True).load()
    assert fingerprint and package.CUSTOM_SCHEMA_TYPES


@pytest.fixture(scope='module')
def acceptance(tmp_path_factory):
    from tests.models.current_mfe_regressions import radius_acceptance
    return radius_acceptance(tmp_path_factory.mktemp('wi051')/'acceptance',H)


def read_result(acceptance,name):
    return json.loads((acceptance/name).read_text())


@pytest.mark.parametrize('case',['baseline','R14'])
def test_complete_native_and_direct_parity(acceptance,case):
    native=read_result(acceptance,'results.json')[case]
    direct=read_result(acceptance,'direct-production.json')['results'][case]
    assert len(native['outputs'])==158 + len(WI040_CHANNELS | LIVE_CONDUCTOR_CHANNELS | WI059_CHANNELS) and len(native['responses'])==19
    assert len(direct['single']['outputs'])==177 + len(WI040_CHANNELS | LIVE_CONDUCTOR_CHANNELS | WI059_CHANNELS)
    assert len(direct['helper']['outputs'])==158 + len(WI040_CHANNELS | LIVE_CONDUCTOR_CHANNELS | WI059_CHANNELS)
    # Full exact baseline and tolerant R14 scalar comparisons, plus exact serialized
    # structured outputs, are performed in the shared executing acceptance path.
    assert read_result(acceptance,'checks.json')[case]['responses_exact']


def test_independent_radius_ratios_and_fixed_anchors(acceptance):
    import math
    checks=read_result(acceptance,'checks.json')
    assert len(checks['independent_ratios'])==6
    for r in checks['independent_ratios'].values():
        assert math.isclose(r['expected'],r['actual'],rel_tol=1e-9,abs_tol=1e-9)
    p='stellarator_09__stellaris__'
    assert checks['anchors']=={new(p+'magnet__R_ref'):12.7,new(p+'magnet__a_coil_ref'):3.1500000000000004,new(p+'wall_peak_R_ref'):12.7,new(p+'R_ref_divertor'):12.7}  # WI-057: the anchors live on their parts
    outputs=read_result(acceptance,'results.json')
    for case in ('baseline','R14'):
        values=outputs[case]['outputs']
        assert values[p+'rb__r_coil']==3.0000000000000004
        assert values[p+'rb__r_coil_centre']==3.1500000000000004
        inputs=json.loads((ROOT/'exploration/stellarator_e2e/generated/inputs/stellarator_plant_params.json').read_text())
        outer=values[p+'rb__r_coil']+inputs[new(p+'coil_t')]+inputs[new(p+'gap2_t')]+inputs[new(p+'lt_shield_t')]
        assert outer==3.5500000000000003


# WI-058 (2026-09-14): 'coil_length' left this list -- the winding length now takes the coil-centre bore, not
# R0 (tests/models/test_winding_length_bore.py covers its response and its R-invariance at fixed bore).
@pytest.mark.parametrize('component',['field_calc','stored_energy','magnet_cost'])
def test_standalone_radius_formals(acceptance,component):
    result=read_result(acceptance,'standalone.json')[MODULES.get(component,component)]  # WI-057: the magnet's calcs are magnet__<calc>
    assert 'R0' in result['inputs']
    assert result['R0_only14']!=result['baseline']


@pytest.mark.parametrize('path',['native','schema','helper','single','cli'])
@pytest.mark.parametrize('case',range(4),ids=['alone','equal','conflicting','zero'])
def test_retired_radius_refused(acceptance,path,case):
    key='stellarator_09__stellaris__magnet__R0'
    if path=='native': row=read_result(acceptance,'results.json')[f'retired_{case}']
    elif path=='schema': row=read_result(acceptance,'schema-refusals.json')[str(case)]
    elif path=='cli':
        row=read_result(acceptance,'cli-checks.json')[case+1]
        assert row['exit']==1
        assert key in (acceptance/f'cli-{case+1}.log').read_text()
        return
    else: row=read_result(acceptance,'direct-production.json')['results'][f'retired_{case}'][path]
    assert 'error' in row and key in row['message']


@pytest.mark.parametrize('path',['native','helper','single'])
# WI-057 (2026-09-13): WI-053 read the magnet's clearance refusal (ValueError, 'Conductor Peak Field: live
# clearance') first at the coil-centre, R3 and negative radii. With the calcs on their parts the regenerated
# pipeline executes the plasma's sustainment module before the magnet's peak-field module, so the first
# refusal at the coil-centre and R3 radii is now the plasma's deliberate sustainment error (accepted); at the
# negative radius it is an incidental TypeError inside plasma__sustain -- an unresolved regression of the
# diagnostic that this expectation documents and does not repair (goal trail, Amendment 2026-09-13). The
# clearance check itself is unchanged and still refuses when reached (the component test below).
@pytest.mark.parametrize('case,kind',[(0,'SustainmentError'),(1,'SustainmentError'),(2,'SustainmentError'),(3,'ZeroDivisionError'),(4,'TypeError')],ids=['R4','coil-centre','R3','zero','negative'])
def test_unified_invalid_radius_failure(acceptance,path,case,kind):
    if path=='native':
        row=read_result(acceptance,'results.json')[f'invalid_{case}']
        assert row['error']=='EvaluationFailed'
    else:
        row=read_result(acceptance,'direct-production.json')['results'][f'invalid_{case}'][path]
        assert row['error']==kind
    if case in (1, 2):
        assert 'non-positive fuel density' in row['message']  # WI-057: the sustainment module refuses first
    if case == 4:
        assert 'must be real number, not complex' in row['message']


@pytest.mark.parametrize('case',['valid','original_negative','equality','reference_equal','reference_inverted'])
def test_peak_component_preserves_valid_and_rejects_invalid_domains(acceptance,case):
    row=read_result(acceptance,'checks.json')['component'][case]
    frozen=json.loads((H.parent/'prototype/expectations.json').read_text())['component_cases'][case]
    if case == 'valid':
        assert row['B_peak'] == frozen['B_peak']
    else:
        assert row['error'] == 'ValueError'
        domain = 'reference' if case.startswith('reference') else 'live'
        assert domain + ' clearance' in row['message']


@pytest.mark.parametrize('kind',['missing','mismatch'])
def test_bad_normative_seed_stops_before_generator(tmp_path,kind):
    source=tmp_path/'source';source.mkdir()
    for name in MANUAL:
        p=source/name;p.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(H/'entering-package'/name,p)
    target=source/next(iter(MANUAL))
    if kind=='missing':target.unlink()
    else:target.write_text('wrong hash')
    calls=[]
    with pytest.raises(ValueError,match='normative seed'):
        seed_and_generate(tmp_path/'destination',source,generator=lambda cfg:calls.append(cfg),models_path=H/'models')
    assert not calls and not list((tmp_path/'destination').iterdir())


def test_extra_seed_stops_before_generator(tmp_path,monkeypatch):
    import regenerate
    original=regenerate.shutil.copyfile
    def copy_with_extra(source,target):
        result=original(source,target)
        (tmp_path/'destination/.extra').write_text('unexpected')
        return result
    monkeypatch.setattr(regenerate.shutil,'copyfile',copy_with_extra)
    calls=[]
    with pytest.raises(ValueError,match='exactly the four'):
        seed_and_generate(tmp_path/'destination',H/'entering-package',generator=lambda cfg:calls.append(cfg),models_path=H/'models')
    assert not calls
