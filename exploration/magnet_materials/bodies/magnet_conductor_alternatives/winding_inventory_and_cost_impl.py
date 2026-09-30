"""WI-099 'Winding Inventory and Cost' (design section 2.4).

Inventory and cost of the supplied winding, never from demand. element_area is the total element area
per turn (mm2). Steel and solder masses carry no void term (only the stabilizer copper space has the
Rutherford void, cu_void). Inputs are keyed by the design names without the generated `_in` suffix;
invalid inputs raise ValueError.
"""
import math

AUTO_IMPLEMENTED = False
INPUTS = dict(n_elements=0., element_area=0., element_density=0., turns=0., coils=0., turn_length=0., turn_current=0.,
              cu_space=0., cu_void=0., steel_area=0., solder_area=0., rho_cu=0., rho_steel=0., rho_solder=0., price_cu=0.,
              price_steel=0., price_solder=0., element_price_per_m=0., manufacturing_per_m=0.)
OUTPUTS = ['conductor_length', 'element_length', 'element_mass', 'cu_mass', 'steel_mass', 'solder_mass', 'sc_cost',
           'materials_cost', 'manufacturing_cost', 'winding_capital', 'ampere_metres']
NAME = 'Winding Inventory and Cost'


def _check(x):
    missing = sorted(set(INPUTS) - set(x))
    if missing:
        raise ValueError(f'{NAME}: missing inputs {missing}')
    for key in INPUTS:
        value = x[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f'{NAME}: nonfinite or non-numeric input {key}={value!r}')
        if key != 'turn_current' and value < 0:
            raise ValueError(f'{NAME}: {key} must be nonnegative, got {value}')
    if not 0 <= x['cu_void'] < 1:
        raise ValueError(f'{NAME}: cu_void must lie in [0, 1)')


def calculate(x):
    _check(x)
    length = x['turns'] * x['coils'] * x['turn_length']
    element_length = x['n_elements'] * length
    element_mass = x['element_area'] * 1e-6 * length * x['element_density']
    cu_mass = x['cu_space'] * (1 - x['cu_void']) * 1e-6 * length * x['rho_cu']
    steel_mass = x['steel_area'] * 1e-6 * length * x['rho_steel']
    solder_mass = x['solder_area'] * 1e-6 * length * x['rho_solder']
    sc_cost = element_length * x['element_price_per_m']
    materials = cu_mass * x['price_cu'] + steel_mass * x['price_steel'] + solder_mass * x['price_solder']
    manufacturing = length * x['manufacturing_per_m']
    return dict(conductor_length=length, element_length=element_length, element_mass=element_mass, cu_mass=cu_mass,
                steel_mass=steel_mass, solder_mass=solder_mass, sc_cost=sc_cost, materials_cost=materials,
                manufacturing_cost=manufacturing, winding_capital=sc_cost + materials + manufacturing,
                ampere_metres=x['turn_current'] * length)
