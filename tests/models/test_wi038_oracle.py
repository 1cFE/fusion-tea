"""WI-038 relative-grade algebra; priced transfer holds reference density fixed."""

import math
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'exploration/stellarator_e2e/studies'))
import oracle_entry as oracle

BASE = dict(B_design=24.9, B_reference=24.9, field_exponent=.6,
            j_reference=118.8271604938272)


def test_reference_is_exact():
    r = oracle.vs._conductor_field_capability(**BASE)
    assert r == dict(quantity_factor=1., j_wp_effective=BASE['j_reference'])


@pytest.mark.parametrize('field', [20., 24.9, 30.])
def test_relative_quantity_and_reciprocal_density(field):
    r = oracle.vs._conductor_field_capability(**(BASE | {'B_design': field}))
    # Independent logarithmic form checks the power-law implementation.
    q = math.exp(.6 * (math.log(field) - math.log(24.9)))
    assert r['quantity_factor'] == pytest.approx(q, rel=1e-14)
    assert r['j_wp_effective'] * q == pytest.approx(BASE['j_reference'], rel=1e-14)


@pytest.mark.parametrize('name', ['B_design', 'B_reference', 'field_exponent', 'j_reference'])
@pytest.mark.parametrize('value', [0., -1., math.nan, math.inf, -math.inf])
def test_invalid_positive_inputs(name, value):
    with pytest.raises(ValueError, match='Conductor Field Capability: invalid ' + name):
        oracle.vs._conductor_field_capability(**(BASE | {name: value}))


@pytest.mark.parametrize('overrides,quantity', [
    ({'B_design': 1e308, 'B_reference': 1e-308}, 'field_ratio'),
    ({'B_design': 1e-308, 'B_reference': 1e308}, 'field_ratio'),
    ({'B_design': 100., 'B_reference': 1., 'field_exponent': 1000.}, 'quantity_factor'),
    ({'B_design': .01, 'B_reference': 1., 'field_exponent': 1000.}, 'quantity_factor'),
    ({'B_design': 1e-308, 'B_reference': 1., 'field_exponent': 1., 'j_reference': 1e308}, 'j_wp_effective'),
    ({'B_design': 1e308, 'B_reference': 1., 'field_exponent': 1., 'j_reference': 1e-308}, 'j_wp_effective'),
])
def test_invalid_intermediate_or_output_is_deliberate(overrides, quantity):
    with pytest.raises(ValueError, match=quantity):
        oracle.vs._conductor_field_capability(**(BASE | overrides))


@pytest.mark.parametrize('field', [20., 30.])
def test_ceiling_does_not_reselect_supplied_inventory(field):
    before = oracle._compute({})
    after = oracle._compute({'magnet_B_max': field})
    assert before == after


def test_operating_field_and_installed_inventory_are_distinct():
    before = oracle._compute({})
    after = oracle._compute({'magnet_turn_current': oracle.vs.IN['magnet_turn_current'] * 1.01})
    assert after['B_peak'] > before['B_peak']
    for name in ('vol_winding_pack', 'winding_material_cost', 'tape_procurement_cost', 'conductor_length'):
        assert after[name] == before[name]


def test_retired_public_grade_inputs_refuse_and_restore_state():
    saved = dict(oracle.vs.IN)
    for suffix in ('B_grade_ref', 'field_exponent'):
        with pytest.raises(oracle.OracleSeamError, match='retired'):
            oracle.evaluate({oracle.P + 'magnet__winding_pack__' + suffix: 0.})
        assert oracle.vs.IN == saved
