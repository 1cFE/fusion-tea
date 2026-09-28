"""Guarded native completion of the corresponding SysML inventory identity."""
from inventory_tea.handwritten.sector_constituent_inventory.inventory_support import numeric, fraction, checked
AUTO_IMPLEMENTED = False

def calculate(inputs):
    x = numeric(inputs)
    fraction(x, 'coverage')
    return checked({'volume': x['area_basis'] * x['coverage'] * x['thickness']})

def run_covered_layer_volume(inputs):
    return calculate(inputs)['volume']
