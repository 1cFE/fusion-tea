"""Auto-generated implementation for Supplementary_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:555

SysML Expressions:
    shipping_frac = 0.015
    tax_frac = 0.01
    insurance_frac = 0.015
    contingency_rate = 0.0
    n_mod = 1.0
    ref_net_power = 1000.0
    cost = (shipping_frac * cas20 + spares_frac * cas23_to_28 + tax_frac * cas20 + insurance_frac * (cas20 + cas30) + startup_fuel_base * (n_mod * p_net / ref_net_power) + decom_base * (n_mod * p_net / ref_net_power)) * (1.0 + contingency_rate)
    
Documentation:
CAS50 supplementary account:

  cost = (shipping*cas20 + spares*cas23_to_28 + tax*cas20
          + insurance*(cas20+cas30)
          + startup*(n_mod*p_net/ref) + decom*(n_mod*p_net/ref))
(1 + contingency_rate)

cas20 is CAS20 WITH contingency; cas23_to_28 is c23+c24+c25+c26+c27+c28
(1cfe's param is misnamed cas22_to_28 but model.py:1492 feeds c23..c28 —
WI-028 finding F-1). c59 internal contingency applies to the CAS50
subtotal (NOAK 0).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:259-283 (cas50_supplementary); model.py:1492 (spares base = c23..c28)
*Basis**: Fraction-of-aggregate supplementary cost with internal contingency
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.supplementary_cost import Supplementary_CostInput


def run_supplementary_cost(inputs: Supplementary_CostInput) -> float:
    """Execute Supplementary_Cost calculation.

CAS50 supplementary account:

  cost = (shipping*cas20 + spares*cas23_to_28 + tax*cas20
          + insurance*(cas20+cas30)
          + startup*(n_mod*p_net/ref) + decom*(n_mod*p_net/ref))
(1 + contingency_rate)

cas20 is CAS20 WITH contingency; cas23_to_28 is c23+c24+c25+c26+c27+c28
(1cfe's param is misnamed cas22_to_28 but model.py:1492 feeds c23..c28 —
WI-028 finding F-1). c59 internal contingency applies to the CAS50
subtotal (NOAK 0).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:259-283 (cas50_supplementary); model.py:1492 (spares base = c23..c28)
*Basis**: Fraction-of-aggregate supplementary cost with internal contingency

SysML Source: root-0/analyses/mfe_account_costs.sysml:555

SysML Expressions:
    shipping_frac = 0.015
    tax_frac = 0.01
    insurance_frac = 0.015
    contingency_rate = 0.0
    n_mod = 1.0
    ref_net_power = 1000.0
    cost = (shipping_frac * cas20 + spares_frac * cas23_to_28 + tax_frac * cas20 + insurance_frac * (cas20 + cas30) + startup_fuel_base * (n_mod * p_net / ref_net_power) + decom_base * (n_mod * p_net / ref_net_power)) * (1.0 + contingency_rate)
    
Documentation:
CAS50 supplementary account:

  cost = (shipping*cas20 + spares*cas23_to_28 + tax*cas20
          + insurance*(cas20+cas30)
          + startup*(n_mod*p_net/ref) + decom*(n_mod*p_net/ref))
(1 + contingency_rate)

cas20 is CAS20 WITH contingency; cas23_to_28 is c23+c24+c25+c26+c27+c28
(1cfe's param is misnamed cas22_to_28 but model.py:1492 feeds c23..c28 —
WI-028 finding F-1). c59 internal contingency applies to the CAS50
subtotal (NOAK 0).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:259-283 (cas50_supplementary); model.py:1492 (spares base = c23..c28)
*Basis**: Fraction-of-aggregate supplementary cost with internal contingency

Args:
    inputs: Input parameters validated against Supplementary_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Supplementary_CostInput(...)
    >>> result = run_supplementary_cost(inputs)
    """
    return (((((((inputs.shipping_frac * inputs.cas20) + (inputs.spares_frac * inputs.cas23_to_28)) + (inputs.tax_frac * inputs.cas20)) + (inputs.insurance_frac * (inputs.cas20 + inputs.cas30))) + (inputs.startup_fuel_base * ((inputs.n_mod * inputs.p_net) / inputs.ref_net_power))) + (inputs.decom_base * ((inputs.n_mod * inputs.p_net) / inputs.ref_net_power))) * (1.0 + inputs.contingency_rate))
