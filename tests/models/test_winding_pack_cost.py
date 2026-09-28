from tests.models.current_mfe_regressions import (CURRENT_PREDICATES, historical_point, assert_historical_native, assert_current_predicates, PARTITIONS)
"""WI-040: independent inventory identities, deliberate domains and public accounting seams."""
import importlib
import math
import os
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
P = 'stellarator_09__stellaris__'
INVENTORY = dict(volume_in=40., f_copper=.35, f_solder=.12, f_steel=.36,
                 f_helium=.08, rho_copper=8940., rho_solder=8390., rho_steel=8000.,
                 price_copper=11., price_solder=29.23/.45359237, price_steel=6.,
                 price_helium=88.1604045, helium_pressure=1.5e6,
                 temperature=20., helium_gas_constant=2077.2644)
PROCUREMENT = dict(n_coils=48., reference_turns=308., f_set=.5, c_coil=43.5,
                   tape_volume_in=3.6, tape_width=.006, tape_thickness=.000056, tape_price_per_m=20., winding_rate_1990=480.,
                   cost_escalation=334.4/130.7, nonplanar_factor=1.9,
                   material_cost_in=2e6)
INVENTORY_OUTPUTS = ('mass_copper', 'mass_solder', 'mass_steel', 'mass_helium',
                     'cost_copper', 'cost_solder', 'cost_steel', 'cost_helium',
                     'material_cost', 'helium_density', 'tape_volume')
PROCUREMENT_OUTPUTS = ('tape_length', 'tape_cost', 'conductor_length', 'winding_fabrication_cost', 'cost')


@pytest.fixture(scope='module')
def runtime_paths():
    paths = [str(ROOT / 'exploration/stellarator_e2e/pkg'),
             str(ROOT / 'exploration/stellarator_e2e/studies')]
    if os.environ.get('STOP_PARSER_TEAX_ROOT'):
        paths.append(str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))
    for path in paths:
        sys.path.insert(0, path)
    yield
    for path in paths:
        sys.path.remove(path)


@pytest.fixture(scope='module')
def calculations(runtime_paths):
    result = {}
    for slug, title, outputs in (
        ('winding_pack_material_inventory', 'Winding_Pack_Material_Inventory', INVENTORY_OUTPUTS),
        ('winding_pack_procurement_cost', 'Winding_Pack_Procurement_Cost', PROCUREMENT_OUTPUTS),
    ):
        module = importlib.import_module('stellarator_tea.modules.mfe_winding_pack_cost.' + slug)
        implementation = importlib.import_module('stellarator_tea.handwritten.mfe_winding_pack_cost.' + slug + '_impl')
        assert Path(module.__file__).resolve().is_relative_to(ROOT / 'exploration/stellarator_e2e/generated')
        assert implementation.AUTO_IMPLEMENTED is False
        input_type = getattr(module, title + 'Input')
        output_type = getattr(module, title + 'Output')
        wrapper = getattr(module, title + 'Module')()
        function = getattr(implementation, 'run_' + slug)
        fields = tuple(output_type.model_fields)
        assert set(fields) == set(outputs)

        def run(values, input_type=input_type, function=function, fields=fields, wrapper=wrapper):
            # Positional ABI belongs to the generated schema, not source declaration order.
            typed = input_type(**values)
            direct = dict(zip(fields, function(typed), strict=True))
            public = wrapper.run(**values).data.model_dump()
            assert direct == public
            return public

        result[slug] = run
    return result['winding_pack_material_inventory'], result['winding_pack_procurement_cost']


@pytest.mark.parametrize('volume', [0., 1., 40., 173.])
def test_material_mass_and_additive_cost_identities(calculations, volume):
    row = calculations[0](INVENTORY | {'volume_in': volume})
    for material in ('copper', 'solder', 'steel', 'helium'):
        density = row['helium_density'] if material == 'helium' else INVENTORY['rho_' + material]
        assert row['mass_' + material] / density == pytest.approx(volume * INVENTORY['f_' + material])
        assert row['cost_' + material] == pytest.approx(row['mass_' + material] * INVENTORY['price_' + material])
    assert row['material_cost'] == sum(row['cost_' + m] for m in ('copper', 'solder', 'steel', 'helium'))
    assert row['tape_volume'] == pytest.approx(.09 * volume)


@pytest.mark.parametrize('material', ['copper', 'solder', 'steel', 'helium'])
def test_material_price_is_its_own_procurement_only(calculations, material):
    before = calculations[0](INVENTORY)
    after = calculations[0](INVENTORY | {'price_' + material: 2 * INVENTORY['price_' + material]})
    changed = {'cost_' + material, 'material_cost'}
    assert after['cost_' + material] == 2 * before['cost_' + material]
    assert after['material_cost'] - before['material_cost'] == pytest.approx(before['cost_' + material])
    assert {k: v for k, v in after.items() if k not in changed} == {k: v for k, v in before.items() if k not in changed}


@pytest.mark.parametrize('pressure,nist_density', [(1.5e6, 36.138), (2e6, 47.458)])
def test_helium_inventory_against_nist_20k_reference(calculations, pressure, nist_density):
    # Registered NIST isotherm: 20 K, 15 and 20 bar. This is not a continuous accuracy bound.
    row = calculations[0](INVENTORY | {'helium_pressure': pressure})
    assert row['helium_density'] == pytest.approx(nist_density, rel=.015)
    assert row['helium_density'] * INVENTORY['helium_gas_constant'] * 20 == pytest.approx(pressure)


@pytest.mark.parametrize('key', list(INVENTORY))
@pytest.mark.parametrize('value', [math.nan, math.inf, -math.inf])
def test_inventory_refuses_every_nonfinite_input(calculations, key, value):
    with pytest.raises(ValueError, match='Winding Pack Material Inventory:.*' + key):
        calculations[0](INVENTORY | {key: value})


@pytest.mark.parametrize('key,value', [
    ('volume_in', -1.),
    *[(k, v) for k in ('f_copper', 'f_solder', 'f_steel', 'f_helium') for v in (-.01, 1.)],
    *[(k, v) for k in ('rho_copper', 'rho_solder', 'rho_steel', 'helium_pressure', 'temperature', 'helium_gas_constant') for v in (0., -1.)],
    *[(k, -1.) for k in ('price_copper', 'price_solder', 'price_steel', 'price_helium')],
])
def test_inventory_refuses_nonphysical_inputs(calculations, key, value):
    with pytest.raises(ValueError, match='Winding Pack Material Inventory:.*' + key):
        calculations[0](INVENTORY | {key: value})


@pytest.mark.parametrize('fraction', [.44, .5])
def test_composition_requires_positive_residual_tape(calculations, fraction):
    with pytest.raises(ValueError, match='fraction|sum|composition'):
        calculations[0](INVENTORY | {'f_copper': fraction})


def test_finite_inputs_cannot_silently_overflow(calculations):
    with pytest.raises(ValueError):
        calculations[0](INVENTORY | {'volume_in': 1e308})
    with pytest.raises(ValueError):
        calculations[1](PROCUREMENT | {'reference_turns': 1e308})
    with pytest.raises(ValueError):
        calculations[0](INVENTORY | {'temperature': 1e-300, 'helium_gas_constant': 1e-300})


def test_tape_length_and_fabrication_are_separate(calculations):
    before = calculations[1](PROCUREMENT)
    # Recover ampere-metres independently from metres times current per turn.
    assert before['conductor_length'] * 50000 == pytest.approx(48 * 15.4e6 * .5 * 43.5)
    assert before['tape_length'] * .006 * .000056 == pytest.approx(3.6)
    assert before['tape_cost'] / 20 == before['tape_length']
    assert before['cost'] == before['tape_cost'] + 2e6 + before['winding_fabrication_cost']
    expensive = calculations[1](PROCUREMENT | {'tape_price_per_m': 40.})
    assert expensive['tape_cost'] == 2 * before['tape_cost']
    assert expensive['winding_fabrication_cost'] == before['winding_fabrication_cost']
    more_turns = calculations[1](PROCUREMENT | {'reference_turns': 616.})
    assert more_turns['conductor_length'] == 2 * before['conductor_length']
    assert more_turns['winding_fabrication_cost'] == 2 * before['winding_fabrication_cost']
    assert more_turns['tape_cost'] == before['tape_cost']


@pytest.mark.parametrize('key', list(PROCUREMENT))
@pytest.mark.parametrize('value', [math.nan, math.inf, -math.inf])
def test_procurement_refuses_every_nonfinite_input(calculations, key, value):
    with pytest.raises(ValueError, match='Winding Pack Procurement Cost:.*' + key):
        calculations[1](PROCUREMENT | {key: value})


@pytest.mark.parametrize('key,value', [
    *[(k, v) for k in ('n_coils', 'reference_turns', 'c_coil', 'tape_width', 'tape_thickness', 'cost_escalation', 'nonplanar_factor') for v in (0., -1.)],
    *[(k, -1.) for k in ('tape_volume_in', 'tape_price_per_m', 'winding_rate_1990', 'material_cost_in')],
    ('f_set', 0.), ('f_set', -1.), ('f_set', 1.01),
])
def test_procurement_refuses_nonphysical_inputs(calculations, key, value):
    with pytest.raises(ValueError, match='Winding Pack Procurement Cost:.*' + key):
        calculations[1](PROCUREMENT | {key: value})


def test_zero_magnitudes_and_zero_prices_are_allowed_locally(calculations):
    row = calculations[0](INVENTORY | {k: 0. for k in INVENTORY if k.startswith('price_')})
    assert row['material_cost'] == 0.
    row = calculations[1](PROCUREMENT | {'winding_rate_1990': 0., 'tape_volume_in': 0., 'material_cost_in': 0.})
    assert row['cost'] == row['tape_length'] == row['winding_fabrication_cost'] == 0.
    assert row['conductor_length'] > 0.
    assert calculations[1](PROCUREMENT | {'f_set': 1.})['cost'] > 0.


@pytest.fixture(scope='module')
def evaluate(runtime_paths, tmp_path_factory):
    from simkit.study.bridge import CandidateBridge
    import study_route
    evaluator = study_route.prepare(ROOT / 'exploration/stellarator_e2e/generated', tmp_path_factory.mktemp('wi040-public'))
    bridge = CandidateBridge(evaluator.entry_models)

    def run(overrides=None):
        result = evaluator.evaluate(bridge.build({P + k: v for k, v in (overrides or {}).items()}))
        assert result.outputs, result
        return result

    return run


def output(row, suffix):
    return row.outputs[P + suffix]


@pytest.mark.codegen_available
def test_extra_cold_volume_does_not_purchase_winding_material(evaluate):
    baseline = evaluate()
    changed = evaluate({'magnet__vol_cold_cryo': 100.})
    for suffix in INVENTORY_OUTPUTS:
        assert output(changed, 'magnet__material_inventory__' + suffix) == output(baseline, 'magnet__material_inventory__' + suffix)
    assert output(changed, 'magnet__winding_procurement__cost') == output(baseline, 'magnet__winding_procurement__cost')
    assert output(changed, 'magnet__wp_volume__vol_cold_total') != output(baseline, 'magnet__wp_volume__vol_cold_total')


@pytest.mark.codegen_available
@pytest.mark.parametrize('key,value,component,factor', [
    ('magnet__winding_pack__price_copper', 22., 'material_inventory__cost_copper', 2.),
    ('magnet__winding_pack__tape_price_per_m', 40., 'winding_procurement__tape_cost', 2.),
])
def test_accounting_levers_preserve_physics_and_operating_verdicts(evaluate, key, value, component, factor):
    # Procurement prices change no supplied hardware or operating state.
    before, after = evaluate(), evaluate({key: value})
    assert output(after, 'magnet__' + component) == pytest.approx(factor * output(before, 'magnet__' + component))
    unchanged = ['material_inventory__mass_' + material for material in ('copper', 'solder', 'steel', 'helium')]
    if key.endswith('price_copper'):
        unchanged += ['winding_procurement__' + suffix for suffix in ('tape_cost', 'conductor_length', 'winding_fabrication_cost')]
        unchanged += ['material_inventory__cost_' + material for material in ('solder', 'steel', 'helium')]
    elif key.endswith('tape_price_per_m'):
        unchanged += ['winding_procurement__conductor_length', 'winding_procurement__winding_fabrication_cost', 'material_inventory__material_cost']
    else:
        unchanged += ['winding_procurement__tape_cost', 'material_inventory__material_cost']
    for suffix in unchanged:
        assert output(after, 'magnet__' + suffix) == output(before, 'magnet__' + suffix)
    assert set(before.responses) == CURRENT_PREDICATES | {'headline'}
    assert before.responses == after.responses
    # Explicit physical owners/calculations, not all channels with an economic name filtered out.
    physical = ('plasma__', 'magnet__field_calc__', 'magnet__peak_field_calc__',
                'magnet__winding_state__', 'magnet__wp_stress__', 'magnet__wp_volume__',
                'cryoplant__', 'primary_loop__', 'operating_heat__')
    keys = [k for k in before.outputs if k.startswith(tuple(P + prefix for prefix in physical))]
    assert len(keys) > 20
    assert {k: before.outputs[k] for k in keys} == {k: after.outputs[k] for k in keys}
    assert output(after, 'total_capital__total_capital') > output(before, 'total_capital__total_capital')


@pytest.mark.codegen_available
def test_public_pack_volume_scales_all_materials_including_tape(evaluate):
    before = evaluate()
    after = evaluate({'magnet__winding_pack__f_wp_vol': 2 * .8780864197530865})
    assert output(after, 'magnet__wp_volume__vol_winding_pack') == pytest.approx(2 * output(before, 'magnet__wp_volume__vol_winding_pack'))
    for suffix in INVENTORY_OUTPUTS:
        factor = 1 if suffix == 'helium_density' else 2
        assert output(after, 'magnet__material_inventory__' + suffix) == pytest.approx(factor * output(before, 'magnet__material_inventory__' + suffix))
    assert output(after, 'magnet__winding_procurement__tape_cost') == pytest.approx(2 * output(before, 'magnet__winding_procurement__tape_cost'))
    for suffix in ('conductor_length', 'winding_fabrication_cost'):
        assert output(after, 'magnet__winding_procurement__' + suffix) == output(before, 'magnet__winding_procurement__' + suffix)
