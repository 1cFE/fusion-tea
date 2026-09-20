"""WI-055: dimensional sizing and independent zero-consumer domains."""
import importlib
import math
import os
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope='module')
def modules(optional_analysis):
    paths = [str(ROOT / 'exploration/stellarator_e2e/pkg')]
    if os.environ.get('STOP_PARSER_TEAX_ROOT'):
        paths.append(str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))
    for path in paths:
        sys.path.insert(0, path)
    result = {}
    for name in ('winding_pack_sizing', 'winding_pack_stress', 'coil_set_axis_field'):
        module = importlib.import_module('optional_magnet_tea.modules.mfe_magnet_field.' + name)
        cls = {'winding_pack_sizing': 'Winding_Pack_SizingModule',
               'winding_pack_stress': 'Winding_Pack_StressModule',
               'coil_set_axis_field': 'Coil_Set_Axis_FieldModule'}[name]
        assert Path(module.__file__).resolve().is_relative_to(optional_analysis)
        result[name] = getattr(module, cls)()
    yield result
    for path in paths:
        sys.path.remove(path)


@pytest.mark.parametrize('current,density,field', [
    (-1., 119., 'I_coil'), (-1., -119., 'I_coil'),
    (1., -119., 'j_wp'), (1., 0., 'j_wp'), (1., -0., 'j_wp'),
    (0., 0., 'j_wp'), (0., -119., 'j_wp'),
    *[(value, 119., 'I_coil') for value in (math.nan, math.inf, -math.inf)],
    *[(1., value, 'j_wp') for value in (math.nan, math.inf, -math.inf)],
])
def test_sizing_refuses_invalid_magnitudes(modules, current, density, field):
    with pytest.raises(ValueError, match='Winding Pack Sizing: ' + field):
        modules['winding_pack_sizing'].run(I_coil=current, j_wp=density)


@pytest.mark.parametrize('zero', [0., -0.])
def test_local_zero_is_retained_and_consumers_own_denominators(modules, zero):
    side = modules['winding_pack_sizing'].run(I_coil=zero, j_wp=119.).data.root
    assert side == 0.
    field = modules['coil_set_axis_field'].run(n_coils=48., I_coil=zero, k_link=.77, R0=12.7, mu0=1.25663706212e-6, two_pi=6.283185307179586).data.root
    assert field == 0.
    with pytest.raises(ValueError, match='Winding Pack Stress: wp_side must be nonzero'):
        modules['winding_pack_stress'].run(I_coil=zero, B_peak_in=field, wp_side=side, k_sigma=.6)


@pytest.mark.parametrize('current,density', [(15.4e6, 118.8271604938272), (1., 1.), (15.4e6, 500.), (2e6, .5)])
def test_area_and_stress_units(modules, current, density):
    side = modules['winding_pack_sizing'].run(I_coil=current, j_wp=density).data.root
    # Recovered current from square metres, A/mm² and the exact mm²/m² conversion.
    assert side * side * 1e6 * density == pytest.approx(current, rel=1e-12)
    sigma = modules['winding_pack_stress'].run(I_coil=current, B_peak_in=24.9, wp_side=side, k_sigma=.61).data.root
    # Independent force/area identity: sigma*d = k*I*B, and unit substitution.
    assert sigma * side == pytest.approx(.61 * current * 24.9, rel=1e-12)
    assert sigma == pytest.approx(1000 * .61 * 24.9 * math.sqrt(current * density), rel=1e-12)


@pytest.mark.parametrize('current,density,side_mm', [
    (15.4e6,119.,360.), (14.6e6,112.,360.), (13.8e6,120.,340.),
    (12.9e6,112.,340.), (12.5e6,122.,320.), (11.2e6,124.,300.),
])
def test_printed_coil_examples(modules, current, density, side_mm):
    # Table 8 integer rounding permits 0.6% current closure, not exact calibration.
    assert density * side_mm**2 == pytest.approx(current, rel=.006)
    side = modules['winding_pack_sizing'].run(I_coil=current,j_wp=density).data.root
    assert side == pytest.approx(side_mm / 1000., rel=.003)


def test_linked_current_scaling(modules):
    rows=[]
    for current in (1e6,4e6):
        side=modules['winding_pack_sizing'].run(I_coil=current,j_wp=100.).data.root
        field=modules['coil_set_axis_field'].run(n_coils=48.,I_coil=current,k_link=.77,R0=12.7,mu0=1.25663706212e-6,two_pi=6.283185307179586).data.root
        stress=modules['winding_pack_stress'].run(I_coil=current,B_peak_in=field,wp_side=side,k_sigma=.61).data.root
        rows.append((side,field,stress))
    assert rows[1][0]/rows[0][0] == pytest.approx(2.)
    assert rows[1][1]/rows[0][1] == pytest.approx(4.)
    assert rows[1][2]/rows[0][2] == pytest.approx(8.)


@pytest.mark.parametrize('zero', [0., -0.])
def test_sustainment_owns_zero_field_denominator(modules, zero):
    import json
    module = importlib.import_module('stellarator_tea.modules.mfe_plasma_sustainment.plasma_sustainment')
    implementation = importlib.import_module('stellarator_tea.handwritten.mfe_plasma_sustainment.plasma_sustainment_impl')
    baseline = json.loads((ROOT / 'work/active/WI-055_winding-pack-input-domain/evidence/baseline-sustain-input.json').read_text())
    with pytest.raises(implementation.SustainmentError, match='Plasma Sustainment: B_in must be nonzero'):
        module.Plasma_SustainmentModule().run(**{**baseline, 'B_in': zero})
