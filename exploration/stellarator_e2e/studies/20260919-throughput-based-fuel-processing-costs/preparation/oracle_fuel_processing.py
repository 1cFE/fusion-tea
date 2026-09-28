"""Independent WI-070 limited exhaust-processing price arithmetic.

Authority: WI-070/design.md, proposed-abi.md and reviewed four-row price evidence.
No production implementation or defaults are imported. All costs express the
caller-declared target CPI purchasing power; applicability is conditional.
"""
import math

ROWS = ('transfer', 'cleanup', 'distiller', 'containment')
FLAGS = ('enabled', 'inventory_enabled', 'source_conditions')
NUMERIC_INPUTS = (
    'flow', 'n_mod', 'legacy_cost', 'capacity_margin', 'price_multiplier',
    'reference_flow', 'exponent', 'target_cpi',
    *(f'{row}_{field}' for row in ROWS for field in ('cpi', 'capital', 'installation')),
)
OUTPUTS = (
    'flow_kg_s', 'capacity_kg_s', 'plant_capacity_kg_s', 'flow_ratio', 'scaling_factor',
    *(f'{row}_{field}' for row in ROWS for field in
      ('reference_capital', 'reference_installation', 'capital', 'installation')),
    'equipment_total', 'installation_total', 'module_total', 'new_total', 'cost', 'defined_flag',
)


def calculate(x: dict) -> dict:
    """Price independent identical module trains, with explicit dormant behavior."""
    for name in FLAGS:
        if type(x[name]) is not bool:
            raise ValueError(f'processing oracle: {name} must be Boolean')
    for name in NUMERIC_INPUTS:
        if isinstance(x[name], bool):
            raise ValueError(f'processing oracle: {name} must be numeric, not Boolean')
        try:
            finite = math.isfinite(x[name])
        except (TypeError, OverflowError) as error:
            raise ValueError(f'processing oracle: invalid {name}') from error
        if not finite:
            raise ValueError(f'processing oracle: nonfinite {name}')
    if x['legacy_cost'] < 0:
        raise ValueError('processing oracle: negative legacy account')
    result = dict.fromkeys(OUTPUTS, 0.0)
    if not x['enabled']:
        result['cost'] = x['legacy_cost']
        return result
    if not x['inventory_enabled']:
        raise ValueError('processing oracle: active pricing requires active inventory')
    if x['flow'] < 0 or x['capacity_margin'] < 1:
        raise ValueError('processing oracle: invalid flow or capacity margin')
    n = x['n_mod']
    if isinstance(n, bool) or n < 1 or int(n) != n:
        raise ValueError('processing oracle: modules must be a positive integer')
    for name in ('price_multiplier', 'reference_flow', 'exponent', 'target_cpi',
                 *(f'{row}_cpi' for row in ROWS)):
        if x[name] <= 0:
            raise ValueError(f'processing oracle: {name} must be positive')
    for row in ROWS:
        if x[row + '_capital'] < 0 or x[row + '_installation'] < 0:
            raise ValueError(f'processing oracle: negative {row} expenditure')

    def finite(value):
        if not math.isfinite(value):
            raise ValueError('processing oracle: nonfinite arithmetic')
        return value

    try:
        capacity = finite(x['flow'] * x['capacity_margin'])
        ratio = finite(capacity / x['reference_flow'])
        scale = finite(math.pow(ratio, x['exponent']))
        per_module_factor = finite(x['price_multiplier'] * scale)
        plant_factor = finite(n * per_module_factor)
        result.update(flow_kg_s=x['flow'], capacity_kg_s=capacity,
                      plant_capacity_kg_s=finite(n * capacity), flow_ratio=ratio,
                      scaling_factor=scale, defined_flag=float(x['source_conditions']))
        for row in ROWS:
            escalation = finite(x['target_cpi'] / x[row + '_cpi'])
            for field in ('capital', 'installation'):
                reference = finite(x[row + '_' + field] * escalation)
                result[row + '_reference_' + field] = reference
                result[row + '_' + field] = finite(reference * plant_factor)
        result['equipment_total'] = finite(math.fsum(result[row + '_capital'] for row in ROWS))
        result['installation_total'] = finite(math.fsum(result[row + '_installation'] for row in ROWS))
        reference_total = finite(math.fsum(result[row + '_reference_' + field]
                                          for row in ROWS for field in ('capital', 'installation')))
        result['module_total'] = finite(reference_total * per_module_factor)
        result['new_total'] = finite(result['equipment_total'] + result['installation_total'])
        result['cost'] = result['new_total']
    except (OverflowError, ZeroDivisionError) as error:
        raise ValueError('processing oracle: arithmetic outside finite domain') from error
    return result
