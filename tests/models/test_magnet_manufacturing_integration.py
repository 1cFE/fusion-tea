from tests.models.current_mfe_regressions import (CURRENT_PREDICATES, historical_point, assert_historical_native, assert_current_predicates, PARTITIONS)
"""WI-063 full-route accounting identities, not a design-space study."""
import json
from pathlib import Path

import pytest
from tests.models.test_winding_pack_cost import runtime_paths, evaluate, output, P


@pytest.mark.codegen_available
@pytest.mark.parametrize('changes', [{},
    {'magnet__winding_pack__insulation_sheet_price':0.},
    {'magnet__winding_pack__insulation_sheet_price':123.35441337549342},
    {'magnet__winding_pack__internal_build_y':0.},
    {'magnet__winding_pack__ground_insulation':.006},
    {'magnet__casing__assembly_clearance':.004},
    {'magnet__winding_pack__nonplanar_factor':1.},
    {'magnet__casing__steel_price':12.},
    {'magnet__coil__I_coil':16e6},
    {'plasma__a':1.7},
    {'magnet__winding_pack__fit_aspect_ratio':1.25}])
def test_native_independent_oracle_and_subtotals(evaluate, changes):
    import oracle_entry
    row=evaluate(changes)
    expected=oracle_entry.evaluate({P+k:v for k,v in changes.items()})
    for key,value in expected.items():
        assert row.outputs[key] == pytest.approx(value,rel=1e-10,abs=1e-8),key
    get=lambda key: output(row,'magnet__'+key)
    materials=sum(get('material_inventory__cost_'+m) for m in ('copper','solder','steel','helium'))
    pack=get('winding_procurement__tape_cost')+materials+get('winding_procurement__winding_fabrication_cost')
    assert get('winding_procurement__cost') == pytest.approx(pack)
    assert get('magnet_capital_rollup__capital_cost') == pytest.approx(
        pack+get('insulation_inventory__stock_cost')+get('magnet_structure_cost__cost'))
    assert get('magnet_structure_cost__effective_all_in_rate') == (36. if 'magnet__casing__steel_price' in changes else 18.)


@pytest.mark.codegen_available
def test_zero_charge_preserves_every_entering_output_and_predicate(evaluate):
    old=json.loads(Path('work/active/WI-062_absolute-conductor-current-margin/evidence/baseline.json').read_text())
    point=historical_point({P+'magnet__winding_pack__insulation_sheet_price':0.})
    row=evaluate({k.removeprefix(P):v for k,v in point.items()})
    assert_historical_native('manufacturing', row, old['outputs'], old['responses'], point)
    assert output(row,'magnet__insulation_inventory__internal_volume') > 0
    assert output(row,'magnet__wp_fit__minimum_margin') < 0
    assert output(row,'magnet__conductor_current__margin_current') < 0


@pytest.mark.codegen_available
def test_sheet_price_and_winding_rate_are_separate_from_physical_quantities(evaluate):
    before=evaluate()
    sheet=evaluate({'magnet__winding_pack__insulation_sheet_price':0.})
    winding=evaluate({'magnet__winding_pack__nonplanar_factor':1.})
    for key in before.outputs:
        if any(group in key for group in ('__material_inventory__','__conductor_current__',
                '__wp_fit__','__wp_sizing__','__wp_volume__','__support_mass__')):
            assert sheet.outputs[key]==before.outputs[key]==winding.outputs[key],key
    assert sheet.responses==before.responses==winding.responses
    assert output(winding,'magnet__insulation_inventory__stock_cost')==output(before,'magnet__insulation_inventory__stock_cost')
    assert output(sheet,'magnet__winding_procurement__winding_fabrication_cost')==output(before,'magnet__winding_procurement__winding_fabrication_cost')
