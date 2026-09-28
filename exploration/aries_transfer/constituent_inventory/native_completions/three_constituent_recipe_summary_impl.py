"""Guarded native completion of the corresponding SysML inventory identity."""
from inventory_tea.handwritten.sector_constituent_inventory.inventory_support import numeric, fraction, checked
AUTO_IMPLEMENTED = False

def calculate(inputs):
    x = numeric(inputs)
    for name in ('fraction_1', 'fraction_2', 'fraction_3', 'unquantified_fraction'):
        fraction(x, name)
    represented = x['fraction_1'] + x['fraction_2'] + x['fraction_3']
    if abs(represented + x['unquantified_fraction'] - 1.0) > 1e-12:
        raise ValueError('recipe fractions must sum to one within 1e-12')
    return checked({'represented_fraction': represented, 'unquantified_volume': x['region_volume'] * x['unquantified_fraction'], 'known_mass': x['mass_1'] + x['mass_2'] + x['mass_3'], 'source_price_subtotal': x['price_1'] + x['price_2'] + x['price_3']})

def run_three_constituent_recipe_summary(inputs):
    from inventory_tea.schemas.three_constituent_recipe_summary_output import Three_Constituent_Recipe_SummaryOutput
    result = calculate(inputs)
    return tuple(result[name] for name in Three_Constituent_Recipe_SummaryOutput.model_fields)

