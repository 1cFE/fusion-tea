"""WI-048 source fidelity and public physical/economic acceptance."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def test_library_output_contract_and_strict_generation():
    lcoe = (ROOT / 'models/library/analyses/ife_lcoe.sysml').read_text()
    for name in ('fusion_power', 'thermal_power', 'thermal_power_gw', 'gross_electric_power',
                 'driver_electric_power', 'other_parasitic_power', 'net_electric_power',
                 'net_electric_power_gw', 'driver_recirculating_fraction',
                 'total_recirculating_fraction', 'discounted_cost', 'discounted_energy',
                 'price', 'generating'):
        assert f'out attribute {name} : Real' in lcoe
    assert 'out attribute lcoe :' not in lcoe
    assert 'out attribute generating : Boolean' not in lcoe
    assert len(re.findall(r'in attribute \w+ : Real;', lcoe.split("calc def 'Generating")[0])) == 14
    cycle = (ROOT / 'models/library/analyses/fusion_cycle.sysml').read_text()
    assert "constraint def 'Positive Net Generation'" in cycle
    assert 'net_power > 0.0' in cycle
    assert 'net_power >= 0.0' not in cycle
    economics = (ROOT / 'models/library/analyses/hif_economics.sysml').read_text()
    assert 'out attribute bank_energy_joules : Real' in economics
    assert economics.count('beam_energy_mj_in * 1.0e6 / driver_efficiency') == 1


def test_osiris_exact_source_facts_and_computed_bindings():
    plant = (ROOT / 'models/designs/hif_ife/hif_plant.sysml').read_text()
    expected = {'beam_energy_mj':5.0, 'gain':87.0, 'yield_mj':432.0,
                'frequency_hz':4.6, 'driver_efficiency_percent':28.0,
                'fusion_power_mw':1987.0, 'thermal_power_mw':2504.0,
                'thermal_efficiency_percent':45.0, 'gross_electric_power_mw':1127.0,
                'driver_electric_power_mw':82.0, 'auxiliary_electric_power_mw':45.0,
                'net_electric_power_mw':1000.0, 'coe_1992_cents_kwh':5.6}
    actual = {name:float(value) for name,value in re.findall(
        r'attribute osiris_reference_(\w+) : Real = ([\d.]+);', plant)}
    assert actual == expected
    for binding in (':>> frequency = 4.6', ':>> gain = 87.0', ':>> thermal_efficiency = 0.45',
                    ':>> pulse_rate_ref = frequency;',
                    'thermal_power_gw : Real = lcoe_calc.thermal_power_gw;',
                    'net_electric_power_gw : Real = lcoe_calc.net_electric_power_gw;'):
        assert binding in plant
    assert 'images/page_007_table_0.png' in plant
    assert not re.search(r'in \w+ = osiris_reference_', plant)
    driver = (ROOT / 'models/designs/hif_ife/hif_driver.sysml').read_text()
    assert ':>> efficiency = 0.28;' in driver
    assert ':>> energy = meier_cost.bank_energy_joules;' in driver
    generic = (ROOT / 'models/designs/generic_ife/ife_plant.sysml').read_text()
    assert "assert constraint net_positive : 'Positive Net Generation'" in generic
    assert 'in net_power = net_electric_power;' in generic
    assert 'in net_power = lcoe_calc.net_electric_power;' in generic


import os
import sys
import math
import pytest
from tests.ife_oracle import PREFIX, NET_GATE, HEURISTIC, MUTATIONS, BOUNDARIES, assert_source_outputs


@pytest.fixture(scope='module')
def executed_ife(tmp_path_factory):
    pytest.importorskip('sysml_codegen', reason='codegen pipeline unavailable')
    teax = os.environ.get('STOP_PARSER_TEAX_ROOT')
    if teax:
        sys.path.insert(0, str(Path(teax) / 'packages/teax-simkit'))
    if os.environ.get('STUDY_REQUIRE_TEAX'):
        import simkit
    else:
        pytest.importorskip('simkit', reason='TEAx pipeline unavailable')
    from simkit.evaluation.evaluator import PreparedEvaluator
    from simkit.evaluation.package_load import ProvisionalPackageLoader
    from simkit.study.bridge import CandidateBridge
    from sysml_codegen.cli import GenerationConfig, run_codegen
    from tests.model_families import IFE, materialize_canonical_subset
    from tests.ife_execution import complete_ife_package

    root = tmp_path_factory.mktemp('wi048-acceptance')
    models = materialize_canonical_subset(IFE, root / 'models')
    package = root / 'wi048_acceptance'
    config = GenerationConfig(models_path=models, output_path=package, package_name=package.name, overwrite=True)
    assert run_codegen(config)
    complete_ife_package(config)
    evaluator = PreparedEvaluator(ProvisionalPackageLoader(package, package.name, root / 'link'),
                                  package / 'pipelines/pipeline.yaml', expects_constraint_report=True)
    bridge = CandidateBridge(evaluator.entry_models)
    return {name:evaluator.evaluate(bridge.build({PREFIX+k:v for k,v in values.items()}))
            for name,values in (MUTATIONS | BOUNDARIES).items()}


@pytest.mark.codegen_available
@pytest.mark.parametrize('name', list(MUTATIONS))
def test_sv073_sv074_independent_source_and_cashflow_execution(executed_ife, name):
    result = executed_ife[name]
    assert_source_outputs(result.outputs, MUTATIONS[name])
    assert result.responses[NET_GATE] == 'satisfied'
    o = result.outputs
    bank = o[PREFIX+'driver__meier_cost__bank_energy_joules']
    assert o[PREFIX+'driver__meier_cost__gamma'] * bank == pytest.approx(
        o[PREFIX+'driver__meier_cost__cost_billions']*1e9, rel=1e-9)


@pytest.mark.codegen_available
def test_sv074_mutation_identities(executed_ife):
    base, beam, efficiency, rate = [executed_ife[name].outputs for name in MUTATIONS]
    d, p = PREFIX+'driver__meier_cost__', PREFIX+'lcoe_calc__'
    for field in ('bank_energy_joules',):
        assert beam[d+field] / base[d+field] == pytest.approx(2, rel=1e-9)
    assert beam[p+'fusion_energy_per_shot'] / base[p+'fusion_energy_per_shot'] == pytest.approx(2, rel=1e-9)
    assert beam[d+'cost_billions'] / base[d+'cost_billions'] == pytest.approx(1.5789473684210527, rel=1e-9)
    assert efficiency[d+'bank_energy_joules'] / base[d+'bank_energy_joules'] == pytest.approx(0.28/0.35, rel=1e-9)
    assert efficiency[p+'energy_on_target'] == pytest.approx(base[p+'energy_on_target'], rel=1e-9)
    assert efficiency[p+'fusion_energy_per_shot'] == pytest.approx(base[p+'fusion_energy_per_shot'], rel=1e-9)
    for field in ('fusion_power', 'thermal_power', 'gross_electric_power', 'driver_electric_power',
                  'other_parasitic_power', 'net_electric_power', 'shots_per_year'):
        assert rate[p+field] / base[p+field] == pytest.approx(5/4.6, rel=1e-9)
    assert rate[p+'driver_lifetime_years'] / base[p+'driver_lifetime_years'] == pytest.approx(4.6/5, rel=1e-9)
    assert rate[d+'cost_billions'] / base[d+'cost_billions'] == pytest.approx(1/(1+0.0088*(4.6-5)), rel=1e-9)


@pytest.mark.codegen_available
@pytest.mark.parametrize('name', list(BOUNDARIES))
def test_sv075_strict_boundary_and_named_net_verdict(executed_ife, name):
    result = executed_ife[name]
    o = result.outputs
    net = o[PREFIX+'lcoe_calc__net_electric_power']
    expected = {'zero':0.0, 'negative_neighbor':-2.5, 'positive_neighbor':2.5,
                'roundoff_positive':5.960464477539063e-8}
    if name in expected:
        assert net == expected[name]
    else:
        assert net == pytest.approx(-0.2*o[PREFIX+'lcoe_calc__driver_electric_power'], rel=1e-9, abs=1e-6)
    assert result.responses[HEURISTIC] == 'satisfied'
    assert result.responses[NET_GATE] == ('satisfied' if net > 0 else 'violated')
    for channel in ('hawker_price', 'meier_price'):
        assert o[PREFIX+channel+'__generating'] == float(net > 0)
        price = o[PREFIX+channel+'__price']
        assert math.isfinite(price)
        assert price > 0 if net > 0 else price == 0
    gross, driver, other = [o[PREFIX+'lcoe_calc__'+field] for field in (
        'gross_electric_power','driver_electric_power','other_parasitic_power')]
    assert net == pytest.approx(gross-driver-other, rel=1e-9, abs=1e-6)
    assert o[PREFIX+'lcoe_calc__driver_recirculating_fraction'] == pytest.approx(driver/gross, rel=1e-9)
    assert o[PREFIX+'lcoe_calc__total_recirculating_fraction'] == pytest.approx((driver+other)/gross, rel=1e-9)
