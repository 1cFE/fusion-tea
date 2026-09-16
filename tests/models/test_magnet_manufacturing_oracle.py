"""WI-063 independent section sum and deliberately separate cost/geometry controls."""
import importlib.util
import math
from pathlib import Path
import sys

import pytest

_SPEC = importlib.util.spec_from_file_location('manufacturing_oracle',
    Path(__file__).parents[2] / 'exploration/stellarator_e2e/verify_stellaris.py')
vs = importlib.util.module_from_spec(_SPEC)
sys.path.insert(0, str(Path(_SPEC.origin).parent))
_SPEC.loader.exec_module(vs)
sys.path.pop(0)


def evaluate(**overrides):
    p = dict(vs.IN)
    p.update(overrides)
    return vs._insulation_inventory(p, 25., .36, 136.56)


def test_original_six_section_geometry_and_catalog_area_conversion():
    # Eight occurrences of each section, no current-distribution factor in perimeter.
    sides = (.36, .36, .34, .34, .32, .30)
    sheets = sum(8 * 25 * side**2 * .025 for side in sides)
    ground = sum(8 * 25 * ((side+.006)*(side*1.025+.006)-side**2*1.025)
                 for side in sides)
    row = evaluate()
    assert row['internal_volume'] == pytest.approx(sheets, abs=1e-12)
    assert row['ground_volume'] == pytest.approx(ground, abs=1e-12)
    assert row['sheet_area'] == pytest.approx(6828.)
    assert row['stock_cost'] == pytest.approx(6828 * 5.73 / (.3048**2))


def test_zero_charge_is_not_zero_physical_insulation():
    base = evaluate()
    free_increment = evaluate(magnet_insulation_sheet_price=0.)
    assert free_increment['stock_cost'] == 0
    assert {k:v for k,v in free_increment.items() if k != 'stock_cost'} == {
        k:v for k,v in base.items() if k != 'stock_cost'}
    included = evaluate(fit_internal_y=0.)
    assert included['sheet_area'] == included['stock_cost'] == 0
    assert included['ground_volume'] < base['ground_volume']


def test_clearance_is_never_purchased_and_ground_never_prices_as_sheet():
    base = evaluate()
    assert evaluate(fit_clearance=.25, fit_wall=.2, fit_interior_y=20.) == base
    ground = evaluate(fit_ground=.006)
    assert ground['ground_volume'] > 2 * base['ground_volume']  # corner term is quadratic
    assert ground['stock_cost'] == base['stock_cost']


def test_price_changes_neither_material_quantity_nor_ground():
    base = evaluate()
    changed = evaluate(magnet_insulation_sheet_price=2*vs.IN['magnet_insulation_sheet_price'])
    assert changed['stock_cost'] == 2*base['stock_cost']
    assert {k:v for k,v in changed.items() if k != 'stock_cost'} == {
        k:v for k,v in base.items() if k != 'stock_cost'}


def test_perimeter_scale_is_distinct_from_area_scale():
    p = dict(vs.IN, fit_aspect_ratio=4.)
    result = vs._insulation_inventory(p, 50., .72, 8*136.56)
    assert result['internal_volume'] == pytest.approx(8*3.414)
    expected = sum(8*50*((2*side*2+.006)*(2*side/2*1.025+.006)
                         -(2*side*2)*(2*side/2*1.025))
                   for side in (.36,.36,.34,.34,.32,.30))
    assert result['ground_volume'] == pytest.approx(expected)


@pytest.mark.parametrize('key,value', [('magnet_insulation_sheet_thickness',0.),
    ('magnet_f_wp_perimeter',0.), ('magnet_f_wp_perimeter',1.01), ('magnet_insulation_sheet_price',-1.),
    ('fit_internal_y',-1.), ('fit_ground',math.inf),
    ('magnet_insulation_sheet_price',math.nan), ('magnet_insulation_sheet_price',1e308)])
def test_invalid_or_nonfinite_cost_is_refused(key,value):
    with pytest.raises(ValueError, match='oracle insulation'):
        evaluate(**{key:value})
