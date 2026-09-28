"""WI-075 supplied design integration; optional WI-064 helper units remain separately tested."""
import pytest
from tests.models.test_winding_pack_cost import runtime_paths, evaluate, output, P


@pytest.mark.codegen_available
@pytest.mark.parametrize('changes', [{},
    {'magnet__coil__coil_t': .6, 'magnet__casing__interior_y': .6},
    {'plasma__R': 13.5, 'plasma__a': 1.5, 'magnet__coil__turn_current': 16e6/308.},
    {'magnet__winding_pack__wp_side': .6},
    {'magnet__winding_pack__wp_side': .6, 'magnet__coil__coil_t': .65,
     'magnet__casing__interior_y': .65, 'plasma__R': 13.5, 'plasma__a': 1.5},
    {'magnet__winding_pack__wp_side': .6, 'magnet__winding_pack__material_factor': 1.1,
     'magnet__winding_pack__degradation_factor': .9},
])
def test_native_oracle_agreement(evaluate, changes):
    import oracle_entry
    row = evaluate(changes)
    expected = oracle_entry.evaluate({P+k: v for k,v in changes.items()})
    for key,value in expected.items():
        assert row.outputs[key] == pytest.approx(value, rel=1e-9, abs=1e-9), key
    side = changes.get('magnet__winding_pack__wp_side', .35999999999999993)
    current = output(row, 'magnet__winding_state__I_coil')
    assert output(row, 'magnet__winding_state__j_wp_effective') == pytest.approx(current/(side*side*1e6))
    assert not any('__current_sizing__' in key or '__wp_sizing__' in key for key in row.outputs)


@pytest.mark.codegen_available
def test_supplied_pack_straddles_current_capacity_without_changing_turns(evaluate):
    operating = {'magnet__coil__turn_current': 50000.*22/24.9, 'magnet__winding_pack__allow_field_extrapolation': 0.}
    a,b = [evaluate(operating | {'magnet__winding_pack__wp_side': side}) for side in (.2,.6)]
    assert output(a,'magnet__conductor_current__margin_fraction') < 0 < output(b,'magnet__conductor_current__margin_fraction')
    assert output(b,'magnet__winding_procurement__tape_length')/output(a,'magnet__winding_procurement__tape_length') == pytest.approx(9.)
    assert output(a,'magnet__winding_procurement__conductor_length') == output(b,'magnet__winding_procurement__conductor_length')
    assert output(a,'magnet__wp_fit__minimum_margin') > 0 > output(b,'magnet__wp_fit__minimum_margin')


@pytest.mark.codegen_available
def test_excitation_preserves_supplied_winding_and_structural_inventory(evaluate):
    a,b = [evaluate({'magnet__coil__turn_current':50000.*field/24.9}) for field in (21.,23.)]
    for name in ('winding_procurement__tape_length','winding_procurement__conductor_length',
                 'winding_procurement__cost','magnet_structure_cost__cost','magnet_capital_rollup__capital_cost'):
        assert output(a,'magnet__'+name) == output(b,'magnet__'+name), name
    assert output(a,'cryoplant__cold_load__q_structure_nuclear') == output(b,'cryoplant__cold_load__q_structure_nuclear')
    assert output(a,'magnet__peak_field_calc__B_peak') < output(b,'magnet__peak_field_calc__B_peak')
    assert output(a,'magnet__conductor_current__margin_fraction') > output(b,'magnet__conductor_current__margin_fraction')
