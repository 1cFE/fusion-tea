"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from combinations_tea.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def _reviewed_run_selected_inventory_purchase(inputs):
    v = values(inputs)
    require(v['quantity'] >= 0 and v['reference_quantity'] > 0 and v['reference_cost'] >= 0 and v['price_factor'] > 0, 'invalid selected inventory purchase')
    require(v['mode'] in (0,1), 'purchase mode must be 0 scaled or 1 fixed')
    r = v['quantity']/v['reference_quantity']
    result = dict(purchased_quantity=v['quantity'], quantity_ratio=r, capital=v['reference_cost']*v['price_factor']*(r if v['mode']==0 else 1), source_budget=v['reference_cost'], extrapolated=float(r<.5 or r>1.5))
    return finish('selected_inventory_purchase', result)


from combinations_tea.modules.integrated_equipment_costs.selected_inventory_purchase import Selected_Inventory_PurchaseInput


def run_selected_inventory_purchase(inputs: Selected_Inventory_PurchaseInput) -> tuple[float, float, float, float, float]:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_selected_inventory_purchase(inputs)
