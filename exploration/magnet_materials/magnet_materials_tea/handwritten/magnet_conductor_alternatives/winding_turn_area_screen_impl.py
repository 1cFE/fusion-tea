"""WI-099 'Winding Turn Area Screen' (design section 2.3).

Sums the supplied per-turn component areas (mm2) and compares the gross area with the envelope, and
computes the allowance-rule copper and steel requirements at the evaluated duty for comparison with the
supplied areas. Nothing is resized. Inputs are keyed by the design names without the generated `_in`
suffix; invalid inputs raise ValueError.
"""
import math

AUTO_IMPLEMENTED = False
INPUTS = dict(turn_current=0., B_peak=0., available_area=0., element_area=0., element_copper_area=0., cabling_factor=1.,
              cable_void=0., cu_space=0., steel_area=0., misc_area=0., solder_area=0., ins_fraction=0., J_cu_rule=0.,
              cu_void=0., cu_per_kA_rule=0., steel_per_kA_rule=0., B_steel_ref=1., steel_B_scaling=0.)
OUTPUTS = ['cable_area', 'net_area', 'gross_area', 'fit_margin', 'fit_margin_fraction', 'required_envelope_J', 'cu_required',
           'cu_margin', 'steel_required', 'steel_margin', 'fit_pass', 'cu_pass', 'steel_pass']
NAME = 'Winding Turn Area Screen'


def _check(x):
    missing = sorted(set(INPUTS) - set(x))
    if missing:
        raise ValueError(f'{NAME}: missing inputs {missing}')
    for key in INPUTS:
        value = x[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f'{NAME}: nonfinite or non-numeric input {key}={value!r}')
    for key in ('turn_current', 'B_peak', 'available_area', 'cabling_factor', 'B_steel_ref'):
        if x[key] <= 0:
            raise ValueError(f'{NAME}: {key} must be positive, got {x[key]}')
    for key in ('element_area', 'element_copper_area', 'cu_space', 'steel_area', 'misc_area', 'solder_area', 'J_cu_rule',
                'cu_per_kA_rule', 'steel_per_kA_rule'):
        if x[key] < 0:
            raise ValueError(f'{NAME}: {key} must be nonnegative, got {x[key]}')
    for key in ('cable_void', 'ins_fraction', 'cu_void'):
        if not 0 <= x[key] < 1:
            raise ValueError(f'{NAME}: {key} must lie in [0, 1)')
    if x['steel_B_scaling'] not in (0, 1):
        raise ValueError(f'{NAME}: steel_B_scaling must be 0 or 1')


def calculate(x):
    _check(x)
    I, B = x['turn_current'], x['B_peak']
    cable = x['element_area'] / x['cabling_factor'] / (1 - x['cable_void'])
    net = cable + x['cu_space'] + x['steel_area'] + x['misc_area'] + x['solder_area']
    gross = net / (1 - x['ins_fraction'])
    fit_margin = x['available_area'] - gross
    if x['J_cu_rule'] > 0:
        cu_required = max(0.0, I / x['J_cu_rule'] - x['element_copper_area']) / (1 - x['cu_void'])
    else:
        cu_required = x['cu_per_kA_rule'] * I / 1000
    field_factor = B / x['B_steel_ref'] if x['steel_B_scaling'] == 1 else 1.0
    steel_required = x['steel_per_kA_rule'] * (I / 1000) * field_factor
    cu_margin = x['cu_space'] - cu_required
    steel_margin = x['steel_area'] - steel_required
    return dict(cable_area=cable, net_area=net, gross_area=gross, fit_margin=fit_margin,
                fit_margin_fraction=fit_margin / x['available_area'],
                required_envelope_J=I / gross if gross > 0 else math.inf, cu_required=cu_required, cu_margin=cu_margin,
                steel_required=steel_required, steel_margin=steel_margin, fit_pass=1.0 if fit_margin >= 0 else 0.0,
                cu_pass=1.0 if cu_margin >= 0 else 0.0, steel_pass=1.0 if steel_margin >= 0 else 0.0)


from magnet_materials_tea.modules.magnet_conductor_alternatives.winding_turn_area_screen import Winding_Turn_Area_ScreenInput


def _native_result(inputs):
    """Typed native adapter: strip the generated `_in` suffix, delegate to calculate, return schema order."""
    result = calculate({k.removesuffix('_in'): v for k, v in inputs.model_dump().items()})
    return tuple(result[k] for k in ['net_area', 'fit_margin', 'steel_margin', 'fit_margin_fraction', 'steel_pass', 'cu_required', 'cu_pass', 'steel_required', 'gross_area', 'cable_area', 'cu_margin', 'required_envelope_J', 'fit_pass'])


def run_winding_turn_area_screen(inputs: Winding_Turn_Area_ScreenInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float]:
    return _native_result(inputs)
