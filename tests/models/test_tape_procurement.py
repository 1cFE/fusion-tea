"""WI-060 physical tape inventory, independent geometry and public accounting."""
import math
import pytest

from tests.models.test_winding_pack_cost import (
    calculations, runtime_paths, evaluate, output, PROCUREMENT, P,
)


@pytest.mark.parametrize('overrides,quantity', [
    ({'tape_width': 1e308, 'tape_thickness': 1e308}, 'tape_area'),
    ({'tape_width': 1e-308, 'tape_thickness': 1e-308}, 'tape_area'),
    ({'tape_volume_in': 1e308}, 'tape_length'),
    ({'tape_volume_in': 1e-308, 'tape_width': 1e150, 'tape_thickness': 1e150}, 'tape_length'),
    ({'tape_price_per_m': 1e308}, 'tape_cost'),
    ({'tape_volume_in': 1e-308, 'tape_width': 1., 'tape_thickness': 1., 'tape_price_per_m': 1e-308}, 'tape_cost'),
])
def test_positive_inventory_extremes_are_deliberate(calculations, overrides, quantity):
    with pytest.raises(ValueError, match=quantity):
        calculations[1](PROCUREMENT | overrides)


@pytest.mark.parametrize('key', ['tape_volume_in', 'tape_price_per_m'])
def test_explicit_zero_volume_or_price_is_valid(calculations, key):
    result = calculations[1](PROCUREMENT | {key: 0.})
    assert result['tape_cost'] == 0.
    assert result['conductor_length'] > 0.
    assert result['tape_length'] == (0. if key == 'tape_volume_in' else pytest.approx(3.6 / 3.36e-7))


@pytest.mark.codegen_available
@pytest.mark.parametrize('overrides,tape_ratio,conductor_ratio', [
    ({'magnet__winding_pack__j_wp': 118.8271604938272 * .8}, 1/.8, 1.),
    ({'magnet__winding_pack__j_wp': 118.8271604938272 * 1.2}, 1/1.2, 1.),
    ({'magnet__winding_pack__j_wp': 118.8271604938272 * .8,
      'magnet__winding_pack__B_max': 30.}, (30/24.9)**.6/.8, 1.),
    ({'magnet__coil__f_set': .8701298701298701 * .8}, 1., .8),
    ({'magnet__winding_pack__f_wp_vol': .8780864197530865 * .8}, .8, 1.),
    ({'magnet__coil__n_coils': 48. * 1.1}, 1.1, 1.1),
    ({'magnet__coil__I_coil': 15400000. * 1.01}, 1.01, 1.01),
])
def test_native_quantity_scaling_and_expanded_oracle(evaluate, overrides, tape_ratio, conductor_ratio):
    import oracle_entry
    baseline, changed = evaluate(), evaluate(overrides)
    before = output(baseline, 'magnet__winding_procurement__tape_length')
    after = output(changed, 'magnet__winding_procurement__tape_length')
    assert before == pytest.approx(36578571.42857143, rel=1e-12)
    assert after / before == pytest.approx(tape_ratio, rel=1e-12)
    assert output(changed, 'magnet__winding_procurement__tape_cost') == after * 20.
    assert output(changed, 'magnet__winding_procurement__conductor_length') / output(baseline, 'magnet__winding_procurement__conductor_length') == pytest.approx(conductor_ratio, rel=1e-12)
    independent = oracle_entry.evaluate({P + k: v for k, v in overrides.items()})
    for key in ('tape_length', 'tape_procurement_cost', 'winding_pack', 'conductor_length'):
        channel = oracle_entry.ORACLE_OUTPUT_TO_CHANNEL[key]
        assert changed.outputs[channel] == pytest.approx(independent[channel], rel=1e-12)


@pytest.mark.codegen_available
@pytest.mark.parametrize('price', [0., 10., 40.])
def test_tape_price_preserves_quantity_and_all_predicates(evaluate, price):
    baseline = evaluate()
    changed = evaluate({'magnet__winding_pack__tape_price_per_m': price})
    for suffix in ('tape_length', 'conductor_length', 'winding_fabrication_cost'):
        assert output(changed, 'magnet__winding_procurement__' + suffix) == output(baseline, 'magnet__winding_procurement__' + suffix)
    assert output(changed, 'magnet__winding_procurement__tape_cost') == pytest.approx(output(baseline, 'magnet__winding_procurement__tape_cost') * price / 20)
    assert len([k for k in baseline.responses if k != 'headline']) == 20
    assert baseline.responses == changed.responses


@pytest.mark.codegen_available
def test_legacy_rate_changes_only_legacy_accounts(evaluate):
    baseline = evaluate()
    changed = evaluate({'magnet__coil__cost_per_kAm': 100.})
    for suffix in ('winding_procurement__cost', 'winding_procurement__tape_length', 'magnet_capital_rollup__capital_cost'):
        assert output(changed, 'magnet__' + suffix) == output(baseline, 'magnet__' + suffix)
    for suffix in ('winding_pack_cost__cost', 'magnet_cost__capital_cost'):
        assert output(changed, 'magnet__' + suffix) == 2 * output(baseline, 'magnet__' + suffix)


@pytest.mark.parametrize('key,value', [('tape_width', .012), ('tape_thickness', .000112)])
def test_procurement_construction_scaling_at_component_boundary(calculations, key, value):
    # The generic procurement law still scales with area; WI-062's public REBCO
    # analysis deliberately refuses these unsupported material constructions.
    baseline = calculations[1](PROCUREMENT)
    changed = calculations[1](PROCUREMENT | {key: value})
    assert changed['tape_length'] == pytest.approx(.5 * baseline['tape_length'])
    assert changed['conductor_length'] == baseline['conductor_length']
    assert changed['tape_cost'] == pytest.approx(.5 * baseline['tape_cost'])


@pytest.mark.codegen_available
@pytest.mark.parametrize('key,value', [('tape_width', .012), ('tape_thickness', .000112)])
def test_public_current_analysis_refuses_unsupported_construction(evaluate, key, value):
    with pytest.raises(Exception, match=key):
        evaluate({'magnet__winding_pack__' + key: value})
