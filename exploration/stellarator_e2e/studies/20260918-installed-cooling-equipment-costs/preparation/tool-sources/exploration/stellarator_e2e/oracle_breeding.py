"""Independent WI-066 interpolation and normalized fuel-account oracle.

Reads the design-owned released response asset, never generated implementations.
The source table is shared physical evidence; interpolation and fuel conservation
are independently evaluated here. Undefined carriers require defined_flag=0.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

RESPONSE_PATH = Path(__file__).resolve().parents[2] / 'models/designs/stellarator_09/breeding_response.json'
RESPONSE_FIELDS = ('tbr_li6', 'tbr_li7', 'tbr_mean', 'tbr_std_error',
                   'interpolation_allowance', 'tbr_lower', 'defined_flag')
ADEQUACY_FIELDS = ('required_tbr', 'design_margin', 'fuel_margin', 'numerical_margin',
                   'production_rate', 'extracted_supply_rate', 'extraction_loss_rate',
                   'recycle_loss_rate', 'decay_rate', 'stock_growth_rate',
                   'balance_rate', 'defined_flag')
GEOMETRY_FIELDS = ('R', 'a', 'kappa', 'vacuum_t', 'firstwall_t', 'reflector_t',
                   'ht_shield_t', 'structure_t', 'gap1_t', 'vessel_t')


def response(plant: dict[str, float]) -> dict[str, float]:
    """Barycentric interpolation; independent node errors combine in quadrature.

    A missing/malformed release asset is a mechanical error, never a zero-TBR
    fallback. Unsupported plant inputs instead produce explicit invalid carriers.
    Hash custody belongs to the release/package integration checks.
    """
    table = json.loads(RESPONSE_PATH.read_text())
    fixed = table['fixed_geometry']
    if set(fixed) != {name + '_in' for name in GEOMETRY_FIELDS}:
        raise ValueError('breeding oracle: incomplete fixed-geometry manifest')
    nodes = table['nodes']
    if len(nodes) < 2:
        raise ValueError('breeding oracle: fewer than two response nodes')
    quantities = [table['interpolation_allowance'], table['statistical_multiplier'],
                  *fixed.values(), *(node[key] for node in nodes
                  for key in ('thickness_m', 'tbr_li6', 'tbr_li7', 'std_error'))]
    if any(not math.isfinite(v) or v < 0 for v in quantities):
        raise ValueError('breeding oracle: invalid response asset value')
    if any(right['thickness_m'] <= left['thickness_m'] for left, right in zip(nodes, nodes[1:])):
        raise ValueError('breeding oracle: response nodes not strictly increasing')
    invalid = dict.fromkeys(RESPONSE_FIELDS, 0.0)
    thickness = plant['blanket_t']
    if any(not math.isfinite(plant[name]) for name in (*GEOMETRY_FIELDS, 'blanket_t')):
        return invalid
    if any(plant[name] != fixed[name + '_in'] for name in GEOMETRY_FIELDS):
        return invalid
    if not nodes[0]['thickness_m'] <= thickness <= nodes[-1]['thickness_m']:
        return invalid
    for left, right in zip(nodes, nodes[1:]):
        if left['thickness_m'] <= thickness <= right['thickness_m']:
            break
    span = right['thickness_m'] - left['thickness_m']
    weights = ((right['thickness_m'] - thickness) / span,
               (thickness - left['thickness_m']) / span)
    li6 = sum(w * node['tbr_li6'] for w, node in zip(weights, (left, right)))
    li7 = sum(w * node['tbr_li7'] for w, node in zip(weights, (left, right)))
    mean = li6 + li7
    sigma = math.hypot(*(w * node['std_error'] for w, node in zip(weights, (left, right))))
    allowance = table['interpolation_allowance']
    lower = mean - table['statistical_multiplier'] * sigma - allowance
    result = dict(tbr_li6=li6, tbr_li7=li7, tbr_mean=mean, tbr_std_error=sigma,
                  interpolation_allowance=allowance, tbr_lower=lower, defined_flag=1.0)
    return result if all(math.isfinite(v) for v in result.values()) else invalid


def adequacy(*, mean: float, lower: float, defined: float, floor: float,
             required: float, burn: float, loss: float, extraction: float,
             decay_constant: float, inventory: float, growth: float,
             burn_fraction: float, recycle: float) -> dict[str, float]:
    """Check conservation per burned atom before returning dimensional rates.

    The normalized demand is 1 + lost/burned + decayed/burned + reserve/burned.
    This separately checks the inherited required-TBR account and prevents
    accepting inconsistent or malformed supplied requirements.
    """
    invalid = dict.fromkeys(ADEQUACY_FIELDS, 0.0)
    if any(not math.isfinite(v) for v in locals().copy().values() if isinstance(v, (float, int))):
        return invalid
    if (defined not in (0, 1) or min(burn, floor, required) <= 0
            or not 0 < burn_fraction <= 1 or not 0 < extraction <= 1
            or not 0 <= recycle <= 1 or min(loss, decay_constant, inventory, growth) < 0):
        return invalid
    decay = decay_constant * inventory
    injected_rate = burn / burn_fraction
    demand_rate = sum((burn, loss, decay, growth))
    effective_burn = extraction * burn
    if not all(math.isfinite(v) for v in (decay, demand_rate, effective_burn, injected_rate)) or effective_burn <= 0:
        return invalid
    lost_per_burn = loss / burn
    expected_lost_per_burn = (1 - recycle) * (1 / burn_fraction - 1)
    demand_per_burn = 1 + lost_per_burn + decay / burn + growth / burn
    reconstructed_required = demand_per_burn / extraction
    if not (math.isfinite(reconstructed_required)
            and math.isclose(lost_per_burn, expected_lost_per_burn, rel_tol=1e-12, abs_tol=0)
            and math.isclose(required, reconstructed_required, rel_tol=1e-12, abs_tol=0)):
        return invalid
    result = invalid | dict(required_tbr=max(floor, required), recycle_loss_rate=loss,
                            decay_rate=decay, stock_growth_rate=growth)
    if defined == 0:
        return result
    if mean < 0 or lower > mean:
        return invalid
    production = mean * burn
    supplied = extraction * production
    # Conservation is checked in normalized form above, then reported as streams.
    balance = supplied - burn - loss - decay - growth
    result.update(design_margin=mean-floor, fuel_margin=mean-required,
                  numerical_margin=lower-result['required_tbr'], production_rate=production,
                  extracted_supply_rate=supplied, extraction_loss_rate=(1-extraction)*production,
                  balance_rate=balance, defined_flag=1.0)
    return result if all(math.isfinite(v) for v in result.values()) else invalid
