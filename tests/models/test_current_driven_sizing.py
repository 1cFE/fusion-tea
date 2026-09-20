"""WI-064 analytic inventory sizing and refusal through wrapper and completion."""
import importlib
import pytest
from tests.models.test_winding_pack_cost import runtime_paths

BASE = dict(sizing_mode=1., inventory_multiplier=1., legacy_effective_density=200.,
            I_coil=16000., turn_current=1600., f_copper=.25, f_solder=0., f_steel=.25,
            f_helium=0., tape_width=.004, tape_thickness=56e-6, B_peak=20., temperature=20.,
            reference_tape_current=200., material_factor=1., orientation_factor=1.,
            cabling_factor=1., degradation_factor=1., sharing_factor=1., allowable_fraction=.8,
            allow_field_extrapolation=0.)
NAMES = ('required_tapes', 'required_conductor_area', 'required_pack_area',
         'required_effective_density', 'selected_effective_density', 'tape_available_current')

@pytest.fixture(scope='module', params=['wrapper', 'completion'])
def sizing(runtime_paths, request, optional_analysis):
    module = importlib.import_module('optional_magnet_tea.modules.mfe_conductor_current.current_driven_pack_sizing')
    impl = importlib.import_module('optional_magnet_tea.handwritten.mfe_conductor_current.current_driven_pack_sizing_impl')
    if request.param == 'wrapper':
        return lambda changes={}: module.Current_Driven_Pack_SizingModule().run(**(BASE | changes)).data.model_dump()
    return lambda changes={}: dict(zip(NAMES, impl.run_current_driven_pack_sizing(module.Current_Driven_Pack_SizingInput(**(BASE | changes))), strict=True))


def test_analytic_current_to_inventory(sizing):
    row = sizing()
    assert row == pytest.approx(dict(zip(NAMES, (10., 4.48e-6, 4.48e-5, 16000/44.8, 16000/44.8, 200.))))
    twice = sizing({'I_coil':32000.})
    assert twice['required_pack_area'] == pytest.approx(2*row['required_pack_area'])
    assert twice['required_effective_density'] == row['required_effective_density']
    repartition = sizing({'turn_current':3200.})
    assert repartition['required_tapes'] == 20
    assert repartition['required_pack_area'] == row['required_pack_area']


def test_modes_and_explicit_additional_inventory(sizing):
    a = sizing()
    assert sizing({'legacy_effective_density':900.}) == a
    legacy = sizing({'sizing_mode':0., 'legacy_effective_density':123.456789, 'inventory_multiplier':3.})
    assert legacy['selected_effective_density'] == 123.456789
    more = sizing({'inventory_multiplier':1.01})
    assert more['selected_effective_density'] == a['required_effective_density']/1.01
    for key in NAMES:
        if key != 'selected_effective_density': assert more[key] == a[key]
    assert BASE['I_coil']/(more['selected_effective_density']*1e6) == pytest.approx(a['required_pack_area']*1.01)


@pytest.mark.parametrize('changes',[
    {'degradation_factor':.5}, {'cabling_factor':.5}, {'sharing_factor':.5},
    {'material_factor':.5}, {'orientation_factor':.5}, {'allowable_fraction':.4},
])
def test_capability_and_allowance_act_once(sizing, changes):
    a=sizing(); b=sizing(changes)
    assert b['required_tapes'] == 2*a['required_tapes']
    assert b['required_pack_area'] == 2*a['required_pack_area']
    assert b['required_effective_density'] == a['required_effective_density']/2


@pytest.mark.parametrize('key', BASE)
@pytest.mark.parametrize('bad', [float('nan'), float('inf'), -1.])
def test_nonfinite_and_negative(sizing, key, bad):
    with pytest.raises(ValueError): sizing({key:bad})


@pytest.mark.parametrize('changes',[
    {'sizing_mode':.5}, {'inventory_multiplier':.99}, {'allow_field_extrapolation':.5},
    {'temperature':19.}, {'tape_thickness':60e-6}, {'tape_width':.0039}, {'tape_width':.0061},
    {'B_peak':19.9}, {'B_peak':32.1, 'allow_field_extrapolation':1.}, {'B_peak':24.1},
    {'allowable_fraction':0.}, {'allowable_fraction':1.1}, {'cabling_factor':1.1},
    {'degradation_factor':1.1}, {'sharing_factor':1.1}, {'f_copper':.75}, {'f_copper':.8},
    {'legacy_effective_density':0.}, {'I_coil':0.}, {'turn_current':0.},
    {'reference_tape_current':1e308, 'material_factor':1e308},
    {'reference_tape_current':1e-308, 'degradation_factor':1e-308},
    {'I_coil':1e308, 'turn_current':1e-308},
    {'I_coil':1e-308, 'turn_current':1e308},
    {'reference_tape_current':1e-308},
    {'turn_current':1e-308, 'reference_tape_current':1e308},
    {'inventory_multiplier':1e308, 'reference_tape_current':1e-20},
])
def test_domain_and_arithmetic_refusals(sizing, changes):
    with pytest.raises(ValueError): sizing(changes)


@pytest.mark.parametrize('field,flag', [(20.,0.), (24.,0.), (24.1,1.), (32.,1.)])
def test_domain_boundaries(sizing, field, flag):
    row=sizing({'B_peak':field, 'allow_field_extrapolation':flag})
    assert row['tape_available_current'] == pytest.approx(200*(field/20)**-.6)
    assert sizing({'f_copper':0.,'f_steel':0.})['required_pack_area'] == pytest.approx(2.24e-5)
    wide=sizing({'tape_width':.006})
    assert wide['tape_available_current']==300
    assert wide['required_pack_area']==pytest.approx(sizing()['required_pack_area'])
