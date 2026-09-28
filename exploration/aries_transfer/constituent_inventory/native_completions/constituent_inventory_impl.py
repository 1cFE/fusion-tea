"""Guarded native completion of the corresponding SysML inventory identity."""
from inventory_tea.handwritten.sector_constituent_inventory.inventory_support import numeric, fraction, checked
AUTO_IMPLEMENTED = False

def calculate(inputs):
    x = numeric(inputs)
    fraction(x, 'fraction')
    if x['density'] <= 0:
        raise ValueError('density must be positive')
    volume = x['region_volume'] * x['fraction']
    mass = volume * x['density']
    return checked({'constituent_volume': volume, 'known_mass': mass, 'source_price_subtotal': mass * x['unit_price']})

def run_constituent_inventory(inputs):
    from inventory_tea.schemas.constituent_inventory_output import Constituent_InventoryOutput
    result = calculate(inputs)
    return tuple(result[name] for name in Constituent_InventoryOutput.model_fields)

