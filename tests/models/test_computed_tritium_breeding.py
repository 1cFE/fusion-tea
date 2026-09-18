"""WI-066 released-data custody, independent arithmetic and native dependencies.

These are software/integration checks. Physical method acceptance remains in the
independent benchmark and transport reviews; no synthetic transport table is used.
"""
import hashlib
import importlib
import json
import math
from pathlib import Path
import subprocess

import pytest
import yaml

from tests.models.test_winding_pack_cost import runtime_paths, evaluate, output, P

ROOT = Path(__file__).resolve().parents[2]
ASSET = ROOT / 'models/designs/stellarator_09/breeding_response.json'
GENERATED = ROOT / 'exploration/stellarator_e2e/generated'
GEOMETRY = ('R_in', 'a_in', 'kappa_in', 'vacuum_t_in', 'firstwall_t_in',
            'reflector_t_in', 'ht_shield_t_in', 'structure_t_in', 'gap1_t_in', 'vessel_t_in')
ACCOUNT = dict(tbr_mean_in=1.4, tbr_lower_in=1.37, defined_in=1., tbr_floor_in=1.05,
               tbr_required_in=1.31/.9, burn_rate_in=100., loss_rate_in=19.,
               eta_extract_in=.9, lambda_T_in=.01, I_total_in=1000., G_stock_in=2.,
               burn_fraction_in=.05, t_recycle_in=.99)


@pytest.fixture(scope='module')
def response_asset():
    # Fail if the real released asset is missing; no provisional or dummy data.
    return json.loads(ASSET.read_text())


@pytest.fixture(scope='module')
def modules(runtime_paths):
    return tuple(importlib.import_module('stellarator_tea.modules.mfe_tritium_breeding.' + name)
                 for name in ('blanket_tritium_breeding', 'tritium_breeding_adequacy'))


@pytest.fixture(scope='module')
def response(modules, response_asset):
    wrapper = modules[0].Blanket_Tritium_BreedingModule()
    base = response_asset['fixed_geometry'] | {'blanket_t_in': .8}
    return lambda changes=None: wrapper.run(**(base | (changes or {}))).data.model_dump()


@pytest.fixture(scope='module')
def account(modules):
    wrapper = modules[1].Tritium_Breeding_AdequacyModule()
    return lambda changes=None: wrapper.run(**(ACCOUNT | (changes or {}))).data.model_dump()


def test_released_asset_matches_embedded_implementation_and_twin(runtime_paths, response_asset):
    impl = importlib.import_module('stellarator_tea.handwritten.mfe_tritium_breeding.blanket_tritium_breeding_impl')
    raw = ASSET.read_bytes()
    assert impl.AUTO_IMPLEMENTED is False
    assert impl.RESPONSE_ASSET == response_asset
    assert impl.SOURCE_ASSET_SHA256 == hashlib.sha256(raw).hexdigest()
    assert impl.TABLE == {key: response_asset[key] for key in (
        'fixed_geometry', 'nodes', 'interpolation_allowance', 'statistical_multiplier')}
    twin = ROOT / 'exploration/stellarator_e2e/models/designs/stellarator_09/breeding_response.json'
    assert twin.read_bytes() == raw
    assert set(response_asset['fixed_geometry']) == set(GEOMETRY)


def test_physical_and_withheld_evidence_is_present_and_unchanged(response_asset):
    # This verifies custody and release prerequisites, not predictive accuracy.
    provenance = response_asset['provenance']
    evidence_root = ROOT / provenance['evidence_root']
    for relative, digest in provenance['sha256'].items():
        artifact = evidence_root / relative
        assert hashlib.sha256(artifact.read_bytes()).hexdigest() == digest, relative
    validation = json.loads((evidence_root / 'table-validation.json').read_text())
    assert validation['status'] == 'PASS'
    assert validation['withheld'] and validation['checks']
    training = {row['thickness_m'] for row in response_asset['nodes']}
    withheld = {row['thickness_m'] for row in validation['withheld']}
    assert withheld.isdisjoint(training)
    assert all(row['passes'] for row in validation['checks'])
    assert all(row['precision_pass'] for row in validation['nodes'] + validation['withheld'])
    benchmark = evidence_root.parent / 'benchmark/results.json'
    results = json.loads(benchmark.read_text())
    assert {r['assembly'] for r in results if r['case'] == 'baseline'} == {'Li', 'PbLi'}
    # The adverse reconstruction sensitivity remains part of the record.
    assert any(abs(r['z_diagnostic']) > 2 for r in results)


def test_actual_nodes_and_independent_oracle_interpolation(response, response_asset, runtime_paths):
    import oracle_entry  # establishes the existing independent-oracle import path
    import oracle_breeding
    nodes = response_asset['nodes']
    assert [n['thickness_m'] for n in nodes] == sorted({n['thickness_m'] for n in nodes})
    for node in nodes:
        result = response({'blanket_t_in': node['thickness_m']})
        assert result['defined_flag'] == 1
        assert result['tbr_li6'] == node['tbr_li6']
        assert result['tbr_li7'] == node['tbr_li7']
        assert result['tbr_mean'] == node['tbr_li6'] + node['tbr_li7']
        assert result['tbr_std_error'] == pytest.approx(node['std_error'], rel=1e-14)
    samples = [n['thickness_m'] for n in nodes]
    samples += [(a['thickness_m'] + b['thickness_m']) / 2 for a, b in zip(nodes, nodes[1:])]
    plant = {key.removesuffix('_in'): value for key, value in response_asset['fixed_geometry'].items()}
    for thickness in samples:
        native = response({'blanket_t_in': thickness})
        independent = oracle_breeding.response(plant | {'blanket_t': thickness})
        assert native == pytest.approx(independent, rel=1e-12, abs=1e-14)
        assert native['tbr_mean'] == pytest.approx(native['tbr_li6'] + native['tbr_li7'])
        assert native['tbr_lower'] == pytest.approx(native['tbr_mean'] - response_asset['statistical_multiplier'] * native['tbr_std_error'] - response_asset['interpolation_allowance'])


@pytest.mark.parametrize('key', GEOMETRY)
def test_every_fixed_geometry_coordinate_is_guarded_exactly(response, response_asset, key):
    unsupported = math.nextafter(response_asset['fixed_geometry'][key], math.inf)
    result = response({key: unsupported})
    assert set(result.values()) == {0.}


@pytest.mark.parametrize('key', (*GEOMETRY, 'blanket_t_in'))
@pytest.mark.parametrize('value', [math.nan, math.inf, -math.inf])
def test_response_nonfinite_inputs_are_undefined(response, key, value):
    assert set(response({key: value}).values()) == {0.}


def test_domain_edges_accepted_and_extrapolation_refused(response, response_asset):
    lo, hi = (response_asset['nodes'][i]['thickness_m'] for i in (0, -1))
    for thickness in (lo, hi):
        assert response({'blanket_t_in': thickness})['defined_flag'] == 1
    for thickness in (math.nextafter(lo, -math.inf), math.nextafter(hi, math.inf)):
        assert set(response({'blanket_t_in': thickness}).values()) == {0.}


def test_adequacy_conserves_distinct_supply_and_loss_streams(account):
    row = account()
    assert row['defined_flag'] == 1
    assert row['production_rate'] == pytest.approx(140.)
    assert row['production_rate'] == pytest.approx(row['extracted_supply_rate'] + row['extraction_loss_rate'])
    assert row['recycle_loss_rate'] == 19.
    assert row['decay_rate'] == 10.
    assert row['stock_growth_rate'] == 2.
    assert row['balance_rate'] == pytest.approx(126. - 100. - 19. - 10. - 2.)
    assert row['required_tbr'] == pytest.approx(131. / 90.)
    assert row['required_tbr'] == max(ACCOUNT['tbr_floor_in'], ACCOUNT['tbr_required_in'])
    assert row['design_margin'] > 0 and row['fuel_margin'] < 0
    assert row['numerical_margin'] < 0


def test_undefined_breeding_retains_requirement_without_physical_carriers(account):
    row = account({'defined_in': 0., 'tbr_mean_in': 0., 'tbr_lower_in': 0.})
    assert row['defined_flag'] == 0
    assert row['required_tbr'] == max(ACCOUNT['tbr_floor_in'], ACCOUNT['tbr_required_in'])
    assert row['recycle_loss_rate'] == 19 and row['decay_rate'] == 10
    for key in ('production_rate', 'extracted_supply_rate', 'extraction_loss_rate',
                'balance_rate', 'design_margin', 'fuel_margin', 'numerical_margin'):
        assert row[key] == 0, key


@pytest.mark.parametrize('changes', [{}, {'tbr_floor_in': 1.8},
    {'eta_extract_in': 1., 't_recycle_in': 1., 'loss_rate_in': 0.,
     'lambda_T_in': 0., 'I_total_in': 0., 'G_stock_in': 0., 'tbr_required_in': 1.}])
def test_account_matches_independent_normalized_demand(account, runtime_paths, changes):
    import oracle_entry
    import oracle_breeding
    p = ACCOUNT | changes
    independent = oracle_breeding.adequacy(
        mean=p['tbr_mean_in'], lower=p['tbr_lower_in'], defined=p['defined_in'],
        floor=p['tbr_floor_in'], required=p['tbr_required_in'], burn=p['burn_rate_in'],
        loss=p['loss_rate_in'], extraction=p['eta_extract_in'], decay_constant=p['lambda_T_in'],
        inventory=p['I_total_in'], growth=p['G_stock_in'], burn_fraction=p['burn_fraction_in'],
        recycle=p['t_recycle_in'])
    assert account(changes) == pytest.approx(independent, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize('changes', [
    {'defined_in': .5}, {'defined_in': 2.}, {'burn_rate_in': 0.},
    {'burn_fraction_in': 0.}, {'burn_fraction_in': 1.01}, {'eta_extract_in': 0.},
    {'eta_extract_in': 1.01}, {'t_recycle_in': -0.01}, {'t_recycle_in': 1.01},
    {'tbr_floor_in': 0.}, {'tbr_required_in': 0.}, {'tbr_required_in': 1.05},
    {'loss_rate_in': -1.}, {'loss_rate_in': 18.}, {'lambda_T_in': -1.},
    {'I_total_in': -1.}, {'G_stock_in': -1.}, {'tbr_mean_in': -1.},
    {'tbr_lower_in': 1.5}, {'lambda_T_in': 1e308, 'I_total_in': 1e308},
    {'defined_in': 0., 'tbr_floor_in': -1., 'tbr_required_in': -1.},
])
def test_malformed_accounts_cannot_pass(account, changes):
    assert set(account(changes).values()) == {0.}


@pytest.mark.parametrize('key', tuple(ACCOUNT))
@pytest.mark.parametrize('value', [math.nan, math.inf, -math.inf])
def test_account_nonfinite_inputs_cannot_pass(account, key, value):
    assert set(account({key: value}).values()) == {0.}


def test_numerical_threshold_requires_validity_even_at_zero_margin(runtime_paths):
    module = importlib.import_module('stellarator_tea.modules.stellarator_09.stellaristbrokconstraintmodule')
    gate = module.StellarisTbrOkConstraintModule()
    assert gate.run(defined_in=1., numerical_margin_in=0.).data.evaluation.status == 'satisfied'
    assert gate.run(defined_in=1., numerical_margin_in=-1e-12).data.evaluation.status == 'violated'
    assert gate.run(defined_in=0., numerical_margin_in=0.).data.evaluation.status == 'violated'
    assert gate.run(defined_in=0., numerical_margin_in=1.).data.evaluation.status == 'violated'


def test_generated_dependency_graph_has_no_held_achieved_input(runtime_paths):
    pipeline = yaml.safe_load((GENERATED / 'pipelines/pipeline.yaml').read_text())['modules']
    schema = importlib.import_module('stellarator_tea.schemas.stellarator_plant_params')
    assert P + 'blanket__tbr' not in schema.StellaratorPlantParams.model_fields
    producer = P + 'blanket__breeding__tbr_mean'
    assert pipeline[P + 'fuel_cycle__fuel']['inputs']['tbr_available_in'] == 'float ' + producer
    assert pipeline[P + 'breeding_adequacy']['inputs']['tbr_mean_in'] == 'float ' + producer
    assert pipeline[P + 'tbr_ok__2cd198f674d413e4']['inputs'] == {
        'defined_in': 'float ' + P + 'breeding_adequacy__defined_flag',
        'numerical_margin_in': 'float ' + P + 'breeding_adequacy__numerical_margin'}


@pytest.mark.codegen_available
def test_blanket_subtype_does_not_leak_into_a_held_plant(tmp_path):
    fixture = ROOT / 'work/active/WI-066_computed-tritium-breeding/evidence/interface-probe/isolated-subtype.sysml'
    subprocess.run([str(ROOT / '.codex-test/run'), 'sysml-codegen', 'generate',
                    '--models', str(fixture), '--output', str(tmp_path / 'generated'),
                    '--package-name', 'probe_pkg'], cwd=ROOT, check=True, capture_output=True, text=True)
    modules = yaml.safe_load((tmp_path / 'generated/pipelines/pipeline.yaml').read_text())['modules']
    assert 'probe__held__blanket__breeding' not in modules
    assert modules['probe__held__fuel_cycle__fuel']['inputs']['achieved'] == 'float isolated_subtype_params.probe__held__blanket__tbr'
    assert modules['probe__stellaris__fuel_cycle__fuel']['inputs']['achieved'] == 'float probe__stellaris__blanket__breeding__total'


@pytest.mark.codegen_available
def test_native_thickness_changes_breeding_build_and_cost(evaluate):
    rows = [evaluate({'blanket__blanket_t': thickness}) for thickness in (.6, .8, 1.)]
    for suffix in ('rb__blanket_vol', 'rb__r_coil', 'blanket__blanket_cost__cost'):
        values = [output(row, suffix) for row in rows]
        assert values[0] < values[1] < values[2], suffix
    tbr = [output(row, 'blanket__breeding__tbr_mean') for row in rows]
    assert len(set(tbr)) == 3
    for row in rows:
        assert output(row, 'blanket__breeding__defined_flag') == 1
        assert output(row, 'fuel_cycle__fuel__tbr_required') == pytest.approx(1.19)
        assert output(row, 'fuel_cycle__fuel__tbr_margin') == pytest.approx(output(row, 'blanket__breeding__tbr_mean') - output(row, 'fuel_cycle__fuel__tbr_required'))
        assert output(row, 'breeding_adequacy__production_rate') == pytest.approx(output(row, 'blanket__breeding__tbr_mean') * output(row, 'fuel_cycle__fuel__burn_rate'))
        verdict = next(v for k, v in row.responses.items() if '__tbr_ok__' in k)
        numerical_pass = output(row, 'breeding_adequacy__defined_flag') == 1 and output(row, 'breeding_adequacy__numerical_margin') >= 0
        assert verdict == ('satisfied' if numerical_pass else 'violated')


@pytest.mark.codegen_available
def test_unsupported_native_geometry_keeps_cost_diagnostics_but_fails_breeding(evaluate):
    row = evaluate({'plasma__R': 12.71})
    assert output(row, 'rb__blanket_vol') > 0
    assert output(row, 'blanket__blanket_cost__cost') > 0
    assert output(row, 'blanket__breeding__defined_flag') == 0
    assert output(row, 'breeding_adequacy__defined_flag') == 0
    assert next(v for k, v in row.responses.items() if '__tbr_ok__' in k) == 'violated'
