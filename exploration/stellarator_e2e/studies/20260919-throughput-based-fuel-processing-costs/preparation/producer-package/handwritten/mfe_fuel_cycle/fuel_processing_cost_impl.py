"""Normative WI-070 conditional exhaust processing estimate; see released design."""
from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_tea.modules.mfe_fuel_cycle.fuel_processing_cost import Fuel_Processing_CostInput
AUTO_IMPLEMENTED = False
ROWS = ('transfer', 'cleanup', 'distiller', 'containment')
OUTPUTS = ('flow_kg_s', 'capacity_kg_s', 'plant_capacity_kg_s', 'flow_ratio', 'scaling_factor') + tuple(r+'_'+f for r in ROWS for f in ('reference_capital','reference_installation','capital','installation')) + ('equipment_total','installation_total','module_total','new_total','cost','defined_flag')

def calculate(x):
    for key, value in x.items():
        if key in ('enabled','inventory_enabled','source_conditions'):
            if type(value) is not bool: raise ValueError('Processing flags must be Boolean')
        elif isinstance(value, bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
            raise ValueError('Processing inputs must be finite numbers')
    out = dict.fromkeys(OUTPUTS, 0.0)
    if x['legacy_cost'] < 0: raise ValueError('Legacy price must be nonnegative')
    if not x['enabled']:
        out['cost'] = x['legacy_cost']
        return out
    if not x['inventory_enabled']: raise ValueError('Active processing requires active inventory')
    if x['flow'] < 0 or x['capacity_margin'] < 1 or x['n_mod'] < 1 or x['n_mod'] != int(x['n_mod']):
        raise ValueError('Invalid operating flow, capacity margin or module count')
    if any(x[k] <= 0 for k in ('price_multiplier','reference_flow','exponent','target_cpi')+tuple(r+'_cpi' for r in ROWS)):
        raise ValueError('Source references and price multiplier must be positive')
    if any(x[r+'_'+f] < 0 for r in ROWS for f in ('capital','installation')):
        raise ValueError('Source amounts must be nonnegative')
    try:
        out['flow_kg_s'] = x['flow']
        out['capacity_kg_s'] = x['flow'] * x['capacity_margin']
        out['plant_capacity_kg_s'] = x['n_mod'] * out['capacity_kg_s']
        out['flow_ratio'] = out['capacity_kg_s'] / x['reference_flow']
        out['scaling_factor'] = out['flow_ratio'] ** x['exponent']
        scale = x['price_multiplier'] * out['scaling_factor']
        for row in ROWS:
            for field in ('capital','installation'):
                ref = x[row+'_'+field] * x['target_cpi'] / x[row+'_cpi']
                out[row+'_reference_'+field] = ref
                out[row+'_'+field] = x['n_mod'] * scale * ref
        out['equipment_total'] = sum(out[r+'_capital'] for r in ROWS)
        out['installation_total'] = sum(out[r+'_installation'] for r in ROWS)
        out['new_total'] = out['equipment_total'] + out['installation_total']
        out['module_total'] = out['new_total'] / x['n_mod']
        out['cost'] = out['new_total']
        out['defined_flag'] = float(x['source_conditions'])
    except (OverflowError, ZeroDivisionError) as exc:
        raise ValueError('Nonfinite processing result') from exc
    if not all(math.isfinite(v) for v in out.values()): raise ValueError('Nonfinite processing result')
    return out

def run_fuel_processing_cost(inputs: Fuel_Processing_CostInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
    from stellarator_tea.schemas.fuel_processing_cost_output import Fuel_Processing_CostOutput
    out = calculate({k.removesuffix('_in'):getattr(inputs,k) for k in type(inputs).model_fields})
    return tuple(out[k] for k in Fuel_Processing_CostOutput.model_fields)
