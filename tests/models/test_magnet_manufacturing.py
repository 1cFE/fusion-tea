"""WI-063 direct native inventory geometry, account boundaries and finite domains."""
import importlib
import math
from pathlib import Path

import pytest
from tests.models.test_winding_pack_cost import runtime_paths, PROCUREMENT

SIDES = (.36, .36, .34, .34, .32, .30)
BASE = dict(volume_in=8*25*sum(s*s for s in SIDES), wp_side=.36,
            aspect_ratio=1., internal_fraction_x=0., internal_fraction_y=.025,
            ground_thickness=.003, n_coils=48., c_coil=25.,
            f_perimeter=sum(SIDES)/(6*.36), sheet_thickness=.0005,
            sheet_price=5.73/(12*.0254)**2)
SUPPORT = dict(m_support=2e6, legacy_casing_fraction=0., n_coils=48.,
               m_casing=15000., steel_price=6., f_steel_fab=3.)


@pytest.fixture(scope='module')
def native(runtime_paths):
    def get(package, slug, title):
        module = importlib.import_module(f'stellarator_tea.modules.{package}.{slug}')
        impl = importlib.import_module(f'stellarator_tea.handwritten.{package}.{slug}_impl')
        assert '/generated/' in str(Path(module.__file__).resolve())
        assert impl.AUTO_IMPLEMENTED is False
        input_type = getattr(module, title+'Input')
        fields = tuple(getattr(module, title+'Output').model_fields)
        wrapper = getattr(module, title+'Module')()
        function = getattr(impl, 'run_'+slug)
        def run(values):
            direct = dict(zip(fields, function(input_type(**values)), strict=True))
            public = wrapper.run(**values).data.model_dump()
            assert public == direct
            return public
        return run
    return dict(inventory=get('mfe_winding_pack_cost','winding_pack_insulation_inventory','Winding_Pack_Insulation_Inventory'),
                support=get('mfe_magnet_cost','magnet_structure_cost','Magnet_Structure_Cost'),
                winding=get('mfe_winding_pack_cost','winding_pack_procurement_cost','Winding_Pack_Procurement_Cost'))


@pytest.mark.parametrize('scale,aspect,fx,fy',[(1.,1.,0.,.025),(1.4,2.3,.04,.025),(.7,.4,.025,0.)])
def test_six_distinct_sections_hand_sum(native,scale,aspect,fx,fy):
    # Independent coil-by-coil rectangles; eight copies of each Table 8 section.
    values=BASE | dict(wp_side=.36*scale, volume_in=BASE['volume_in']*scale**2,
                       aspect_ratio=aspect, internal_fraction_x=fx,internal_fraction_y=fy)
    internal=ground=0.
    for side in SIDES:
        x=side*scale*math.sqrt(aspect); y=side*scale/math.sqrt(aspect)
        pack_x=x*(1+fx); pack_y=y*(1+fy); t=values['ground_thickness']
        internal += 8*25*(pack_x*pack_y-x*y)
        ground += 8*25*((pack_x+2*t)*(pack_y+2*t)-pack_x*pack_y)
    row=native['inventory'](values)
    assert row['internal_volume']==pytest.approx(internal,rel=1e-12)
    assert row['ground_volume']==pytest.approx(ground,rel=1e-12)
    assert row['sheet_area']==pytest.approx(internal/.0005,rel=1e-12)
    assert row['stock_cost']==pytest.approx(internal/.0005*BASE['sheet_price'],rel=1e-12)
    if scale==1:
        assert row['internal_volume']==pytest.approx(3.414)
        assert row['sheet_area']==pytest.approx(6828.)
        assert row['stock_cost']==pytest.approx(421131.9672641492)
        assert row['ground_volume']==pytest.approx(4.9518)


def test_dimensions_and_independent_price_thickness(native):
    initial=native['inventory'](BASE); k=3.
    scaled=native['inventory'](BASE | dict(volume_in=BASE['volume_in']*k**3,
        wp_side=BASE['wp_side']*k,c_coil=BASE['c_coil']*k,
        ground_thickness=BASE['ground_thickness']*k,sheet_thickness=BASE['sheet_thickness']*k))
    for key in ('internal_volume','ground_volume'):assert scaled[key]==pytest.approx(initial[key]*k**3)
    for key in ('sheet_area','stock_cost'):assert scaled[key]==pytest.approx(initial[key]*k**2)
    for factor in (0.,2.):
        row=native['inventory'](BASE | dict(sheet_price=BASE['sheet_price']*factor))
        for key in ('internal_volume','ground_volume','sheet_area'):assert row[key]==initial[key]
        assert row['stock_cost']==initial['stock_cost']*factor
    thick=native['inventory'](BASE | dict(sheet_thickness=BASE['sheet_thickness']*2))
    assert thick['stock_cost']==initial['stock_cost']/2
    assert thick['internal_volume']==initial['internal_volume']
    assert thick['ground_volume']==initial['ground_volume']


def test_zero_layers_and_zero_volume(native):
    no_layers=native['inventory'](BASE | dict(internal_fraction_x=0.,internal_fraction_y=0.,ground_thickness=0.))
    assert all(value==0 for value in no_layers.values())
    no_volume=native['inventory'](BASE | dict(volume_in=0.))
    assert no_volume['internal_volume']==no_volume['sheet_area']==no_volume['stock_cost']==0.
    assert no_volume['ground_volume']>0 # Separate prescribed envelope remains defined.
    assert native['inventory'](BASE | dict(ground_thickness=0.))['stock_cost']>0


@pytest.mark.parametrize('key',BASE)
@pytest.mark.parametrize('bad',[float('nan'),float('inf'),-float('inf'),-1.])
def test_inventory_invalid_inputs(native,key,bad):
    with pytest.raises(ValueError,match=key):native['inventory'](BASE | {key:bad})


@pytest.mark.parametrize('key',['wp_side','aspect_ratio','n_coils','c_coil','sheet_thickness','f_perimeter'])
def test_positive_input_zero(native,key):
    with pytest.raises(ValueError,match=key):native['inventory'](BASE | {key:0.})


@pytest.mark.parametrize('change,diagnosis',[
    ({'f_perimeter':1.1},'f_perimeter'),
    ({'volume_in':1e308,'internal_fraction_y':10.},'internal_volume'),
    ({'internal_fraction_x':1e308,'internal_fraction_y':1e308},'fraction_cross_term'),
    ({'internal_fraction_x':1e-300,'internal_fraction_y':1e-300},'fraction_cross_term'),
    ({'volume_in':1e-300,'internal_fraction_y':1e-300},'internal_volume'),
    ({'c_coil':1e308,'n_coils':48.},'coil_path'),
    ({'wp_side':1e308},'integrated_perimeter'),
    ({'wp_side':1e-300,'f_perimeter':1e-300},'integrated_perimeter'),
    ({'ground_thickness':1e308},'ground_shell'),
    ({'ground_thickness':1e-300},'ground_corners'),
    ({'sheet_thickness':1e-308},'sheet_area'),
    ({'volume_in':1e-300,'sheet_thickness':1e308},'sheet_area'),
    ({'sheet_price':1e308},'stock_cost'),
    ({'volume_in':1e-300,'sheet_price':1e-300},'stock_cost'),
])
def test_inventory_arithmetic_refusals(native,change,diagnosis):
    with pytest.raises(ValueError,match=diagnosis):native['inventory'](BASE | change)


@pytest.mark.parametrize('fraction',[0.,.4,1.])
def test_support_historical_order_and_rate(native,fraction):
    values=SUPPORT | dict(legacy_casing_fraction=fraction)
    row=native['support'](values)
    assert row['effective_all_in_rate']==18.
    assert row['cost']==(fraction*48*15000+2e6)*6*3
    quoted=native['support'](values | dict(steel_price=18.,f_steel_fab=1.))
    assert row==quoted
    for key in ('steel_price','f_steel_fab'):
        assert native['support'](values | {key:0.})==dict(cost=0.,effective_all_in_rate=0.)


@pytest.mark.parametrize('key',SUPPORT)
@pytest.mark.parametrize('bad',[float('nan'),float('inf'),-float('inf'),-1.])
def test_support_invalid_inputs(native,key,bad):
    with pytest.raises(ValueError):native['support'](SUPPORT | {key:bad})


@pytest.mark.parametrize('change',[
    {'legacy_casing_fraction':1.1}, {'steel_price':1e308,'f_steel_fab':3.},
    {'steel_price':1e-300,'f_steel_fab':1e-300},
    {'m_support':1e308}, {'m_support':1e-300,'steel_price':1e-300},
    {'legacy_casing_fraction':1.,'n_coils':1e308},
])
def test_support_arithmetic_refusals(native,change):
    with pytest.raises(ValueError):native['support'](SUPPORT | change)


def test_winding_support_and_sheet_rates_are_independent(native):
    sheet=native['inventory'](BASE); support=native['support'](SUPPORT); winding=native['winding'](PROCUREMENT)
    sheet2=native['inventory'](BASE | dict(sheet_price=2*BASE['sheet_price']))
    support2=native['support'](SUPPORT | dict(steel_price=12.))
    winding2=native['winding'](PROCUREMENT | dict(winding_rate_1990=2*PROCUREMENT['winding_rate_1990']))
    assert sheet2['stock_cost']==2*sheet['stock_cost']
    assert support2['cost']==2*support['cost']
    assert winding2['winding_fabrication_cost']==2*winding['winding_fabrication_cost']
    for key in ('tape_cost','tape_length','conductor_length'):assert winding2[key]==winding[key]
    assert winding2['cost']-winding['cost']==pytest.approx(winding['winding_fabrication_cost'])
