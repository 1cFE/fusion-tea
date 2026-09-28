"""Guarded native completion of the corresponding SysML inventory identity."""
from inventory_tea.handwritten.sector_constituent_inventory.inventory_support import numeric, fraction, checked
AUTO_IMPLEMENTED = False

def calculate(inputs):
    x = numeric(inputs)
    for name in ('coverage_1', 'coverage_2', 'coverage_3'):
        fraction(x, name)
    if abs(x['coverage_1'] + x['coverage_2'] + x['coverage_3'] - 1.0) > 1e-12:
        raise ValueError('sector coverages must sum to one within 1e-12')
    return checked({'volume': x['volume_1'] + x['volume_2'] + x['volume_3'], 'known_mass': x['mass_1'] + x['mass_2'] + x['mass_3'], 'source_price_subtotal': x['price_1'] + x['price_2'] + x['price_3'], 'unquantified_volume': x['unquantified_volume_1'] + x['unquantified_volume_2'] + x['unquantified_volume_3']})

def run_three_sector_inventory_sum(inputs):
    from inventory_tea.schemas.three_sector_inventory_sum_output import Three_Sector_Inventory_SumOutput
    result = calculate(inputs)
    return tuple(result[name] for name in Three_Sector_Inventory_SumOutput.model_fields)
