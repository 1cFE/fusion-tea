from tests.models.current_mfe_regressions import (CURRENT_PREDICATES, historical_point, assert_historical_native, assert_current_predicates, PARTITIONS)
"""WI-064 independent inversion and full-route inventory/field/cost closure."""
import json
import math
from pathlib import Path

import pytest
from tests.models.test_winding_pack_cost import runtime_paths, evaluate, output, P


@pytest.mark.codegen_available
@pytest.mark.parametrize('changes', [{},
    {'magnet__coil__coil_t': .6, 'magnet__casing__interior_y': .6},
    {'plasma__R': 13.5, 'plasma__a': 1.5, 'magnet__coil__I_coil': 16e6},
    {'magnet__winding_pack__sizing_mode': 1., 'magnet__winding_pack__inventory_multiplier': 1.01},
    {'magnet__winding_pack__sizing_mode': 1., 'magnet__coil__coil_t': .65,
     'magnet__casing__interior_y': .65, 'plasma__R': 13.5, 'plasma__a': 1.5},
    {'magnet__winding_pack__sizing_mode': 1., 'magnet__winding_pack__material_factor': 1.1,
     'magnet__winding_pack__degradation_factor': .9},
])
def test_native_oracle_agreement(evaluate, changes):
    import oracle_entry
    row = evaluate(changes)
    expected = oracle_entry.evaluate({P+k: v for k,v in changes.items()})
    for key,value in expected.items():
        assert row.outputs[key] == pytest.approx(value, rel=1e-9, abs=1e-9), key
    if changes.get('magnet__winding_pack__sizing_mode'):
        multiple = changes.get('magnet__winding_pack__inventory_multiplier', 1.)
        assert output(row, 'magnet__conductor_current__operating_fraction_reference') == pytest.approx(.8/multiple)
        assert output(row, 'magnet__conductor_current__parallel_tapes_reference') == pytest.approx(
            multiple*output(row, 'magnet__current_sizing__required_tapes'))
        assert output(row, 'magnet__wp_sizing__wp_side')**2 == pytest.approx(
            multiple*output(row, 'magnet__current_sizing__required_pack_area'))


@pytest.mark.codegen_available
def test_every_entering_native_output_and_predicate_preserved(evaluate):
    before = json.loads(Path('work/orchestration/goals/joint-magnet-sizing-feasibility/evidence/entering/native-reference.json').read_text())
    point = historical_point()
    row = evaluate({k.removeprefix(P):v for k,v in point.items()})
    assert_historical_native('current-sizing', row, before['outputs'], before['responses'], point)


@pytest.mark.codegen_available
def test_grade_is_not_applied_twice_and_multiplier_is_physical(evaluate):
    active = {'magnet__winding_pack__sizing_mode': 1., 'magnet__winding_pack__inventory_multiplier': 1.01}
    base = evaluate(active)
    envelope = evaluate(active | {'magnet__winding_pack__B_max': 30.})
    excess = evaluate(active | {'magnet__winding_pack__inventory_multiplier': 1.1})
    for name in ('winding_procurement__tape_length', 'wp_sizing__wp_side',
                 'conductor_current__operating_fraction_reference', 'magnet_capital_rollup__capital_cost'):
        assert output(base, 'magnet__'+name) == output(envelope, 'magnet__'+name)
    assert output(excess, 'magnet__winding_procurement__tape_length')/output(base,'magnet__winding_procurement__tape_length') == pytest.approx(1.1/1.01)
    assert output(excess,'magnet__conductor_current__operating_fraction_reference') == pytest.approx(.8/1.1)


@pytest.mark.codegen_available
def test_radial_allocation_propagates_existing_feedback(evaluate):
    fixed = {'magnet__winding_pack__sizing_mode': 1., 'magnet__winding_pack__inventory_multiplier': 1.01}
    a,b = evaluate(fixed), evaluate(fixed | {'magnet__coil__coil_t': .65})
    for name in ('peak_field_calc__B_peak','current_sizing__required_tapes',
                 'winding_procurement__tape_length','winding_procurement__conductor_length',
                 'magnet_capital_rollup__capital_cost'):
        assert output(b,'magnet__'+name) > output(a,'magnet__'+name), name
