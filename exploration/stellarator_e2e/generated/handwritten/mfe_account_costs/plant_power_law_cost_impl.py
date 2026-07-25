"""Auto-generated implementation for Plant_Power_Law_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:434

SysML Expressions:
    n_mod = 1.0
    cost = base * (n_mod * power / ref_power) ** alpha
    
Documentation:
Generic plant power-law account:

  cost = base * (n_mod * power / ref_power) ** alpha

Plant-wide account, linear-or-power-law in plant-total driving power.
Covers C220400 waste (base 1.96, ref 1000, a=1.0), C220500 fuel
handling (fuel base, ref 1000, a=0.7), C220600 other (11.5, ref 1000,
a=0.8), C220700 I&C (85.0, ref 3500, a=0.65), and CAS40 owner (owner
base, ref 1000, a=0.5). base/ref_power/alpha are per-account concept
inputs (MR-3, bound at the instance).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:702 (waste), :718 (fuel), :724 (other), :731 (I&C); costs.py:256 (CAS40 owner)
*Basis**: Plant-total power-law account cost
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.plant_power_law_cost import Plant_Power_Law_CostInput


def run_plant_power_law_cost(inputs: Plant_Power_Law_CostInput) -> float:
    """Execute Plant_Power_Law_Cost calculation.

Generic plant power-law account:

  cost = base * (n_mod * power / ref_power) ** alpha

Plant-wide account, linear-or-power-law in plant-total driving power.
Covers C220400 waste (base 1.96, ref 1000, a=1.0), C220500 fuel
handling (fuel base, ref 1000, a=0.7), C220600 other (11.5, ref 1000,
a=0.8), C220700 I&C (85.0, ref 3500, a=0.65), and CAS40 owner (owner
base, ref 1000, a=0.5). base/ref_power/alpha are per-account concept
inputs (MR-3, bound at the instance).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:702 (waste), :718 (fuel), :724 (other), :731 (I&C); costs.py:256 (CAS40 owner)
*Basis**: Plant-total power-law account cost

SysML Source: root-0/analyses/mfe_account_costs.sysml:434

SysML Expressions:
    n_mod = 1.0
    cost = base * (n_mod * power / ref_power) ** alpha
    
Documentation:
Generic plant power-law account:

  cost = base * (n_mod * power / ref_power) ** alpha

Plant-wide account, linear-or-power-law in plant-total driving power.
Covers C220400 waste (base 1.96, ref 1000, a=1.0), C220500 fuel
handling (fuel base, ref 1000, a=0.7), C220600 other (11.5, ref 1000,
a=0.8), C220700 I&C (85.0, ref 3500, a=0.65), and CAS40 owner (owner
base, ref 1000, a=0.5). base/ref_power/alpha are per-account concept
inputs (MR-3, bound at the instance).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:702 (waste), :718 (fuel), :724 (other), :731 (I&C); costs.py:256 (CAS40 owner)
*Basis**: Plant-total power-law account cost

Args:
    inputs: Input parameters validated against Plant_Power_Law_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Plant_Power_Law_CostInput(...)
    >>> result = run_plant_power_law_cost(inputs)
    """
    return (inputs.base * (((inputs.n_mod * inputs.power) / inputs.ref_power) ** inputs.alpha))
