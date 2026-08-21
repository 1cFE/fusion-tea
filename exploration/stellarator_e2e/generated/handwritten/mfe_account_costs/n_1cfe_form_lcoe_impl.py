"""Auto-generated implementation for n_1cfe_Form_LCOE.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:898

SysML Expressions:
    n_mod = 1.0
    annual_energy_mwh = 8760.0 * net_electric_mw * n_mod * availability
    lcoe = (cas90 + cas70 + cas80) / annual_energy_mwh
    
Documentation:
LCOE in 1costingFE's form — the comparison channel that pairs with
'1cfe-Form Capital Charge' (WI-029 Option ii):

  lcoe = (cas90 + cas70 + cas80) / (8760 * net_electric_mw * n_mod * availability)

Money-unit transparent: with the cost inputs in $ the result is $/MWh.
This is NOT the design-point headline — 'LCOE DCF' remains the headline
and its convention is untouched. Both channels coexist by design.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: economics.py:88-92 (compute_lcoe)
*Basis**: Annual cost over annual energy sold, 1costingFE denominator form
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.n_1cfe_form_lcoe import n_1cfe_Form_LCOEInput


def run_n_1cfe_form_lcoe(inputs: n_1cfe_Form_LCOEInput) -> float:
    """Execute n_1cfe_Form_LCOE calculation.

LCOE in 1costingFE's form — the comparison channel that pairs with
'1cfe-Form Capital Charge' (WI-029 Option ii):

  lcoe = (cas90 + cas70 + cas80) / (8760 * net_electric_mw * n_mod * availability)

Money-unit transparent: with the cost inputs in $ the result is $/MWh.
This is NOT the design-point headline — 'LCOE DCF' remains the headline
and its convention is untouched. Both channels coexist by design.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: economics.py:88-92 (compute_lcoe)
*Basis**: Annual cost over annual energy sold, 1costingFE denominator form

SysML Source: root-0/analyses/mfe_account_costs.sysml:898

SysML Expressions:
    n_mod = 1.0
    annual_energy_mwh = 8760.0 * net_electric_mw * n_mod * availability
    lcoe = (cas90 + cas70 + cas80) / annual_energy_mwh
    
Documentation:
LCOE in 1costingFE's form — the comparison channel that pairs with
'1cfe-Form Capital Charge' (WI-029 Option ii):

  lcoe = (cas90 + cas70 + cas80) / (8760 * net_electric_mw * n_mod * availability)

Money-unit transparent: with the cost inputs in $ the result is $/MWh.
This is NOT the design-point headline — 'LCOE DCF' remains the headline
and its convention is untouched. Both channels coexist by design.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: economics.py:88-92 (compute_lcoe)
*Basis**: Annual cost over annual energy sold, 1costingFE denominator form

Args:
    inputs: Input parameters validated against n_1cfe_Form_LCOEInput schema

Returns:
    float: lcoe

Example:
    >>> inputs = n_1cfe_Form_LCOEInput(...)
    >>> result = run_n_1cfe_form_lcoe(inputs)
    """
    annual_energy_mwh = (((8760.0 * inputs.net_electric_mw) * inputs.n_mod) * inputs.availability)
    return (((inputs.cas90 + inputs.cas70) + inputs.cas80) / annual_energy_mwh)
