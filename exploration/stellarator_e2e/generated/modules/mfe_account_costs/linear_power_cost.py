"""Linear_Power_CostModule Module Wrapper

TEAx module for Linear_Power_Cost calculation.

Generic balance-of-plant account cost linear in plant-total power:

  cost = n_mod * power * cost_per_mw

Reused for the four flat BOP accounts, each with its own driving power
and per-MW unit cost (concept/power-cycle inputs, WI-011):
  - Turbine plant       : power = p_the,  turbine_per_mw
  - Electric plant      : power = p_et,   electric_per_mw
  - Heat rejection      : power = p_th,   heat_rej_per_mw
  - Miscellaneous plant : power = p_et,   misc_per_mw

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:154 (turbine), :162 (electric), :170 (misc), :179 (heat_rej)
*Basis**: Balance-of-plant cost linear in plant-total driving power

Inputs:
    - power: power parameter
    - cost_per_mw: cost_per_mw parameter
    - n_mod: n_mod parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:226

SysML Source: root-0/analyses/mfe_account_costs.sysml:226

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/linear_power_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Linear_Power_CostInput(BaseModel):
    """Input model for Linear_Power_CostModule.

    Attributes:
        power: power input
        cost_per_mw: cost_per_mw input
        n_mod: n_mod input
    """
    power: float = Field(..., description="power input")
    cost_per_mw: float = Field(..., description="cost_per_mw input")
    n_mod: float = Field(..., description="n_mod input")


class Linear_Power_CostModule(ModuleBase[Linear_Power_CostInput, Float]):
    """TEAx module for Linear_Power_Cost calculation.

Generic balance-of-plant account cost linear in plant-total power:

  cost = n_mod * power * cost_per_mw

Reused for the four flat BOP accounts, each with its own driving power
and per-MW unit cost (concept/power-cycle inputs, WI-011):
  - Turbine plant       : power = p_the,  turbine_per_mw
  - Electric plant      : power = p_et,   electric_per_mw
  - Heat rejection      : power = p_th,   heat_rej_per_mw
  - Miscellaneous plant : power = p_et,   misc_per_mw

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:154 (turbine), :162 (electric), :170 (misc), :179 (heat_rej)
*Basis**: Balance-of-plant cost linear in plant-total driving power

Inputs:
    - power: power parameter
    - cost_per_mw: cost_per_mw parameter
    - n_mod: n_mod parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:226

    SysML Source: root-0/analyses/mfe_account_costs.sysml:226

    Calculation Specification:
        n_mod = 1.0
        cost = n_mod * power * cost_per_mw
        
Documentation:
Generic balance-of-plant account cost linear in plant-total power:

  cost = n_mod * power * cost_per_mw

Reused for the four flat BOP accounts, each with its own driving power
and per-MW unit cost (concept/power-cycle inputs, WI-011):
  - Turbine plant       : power = p_the,  turbine_per_mw
  - Electric plant      : power = p_et,   electric_per_mw
  - Heat rejection      : power = p_th,   heat_rej_per_mw
  - Miscellaneous plant : power = p_et,   misc_per_mw

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:154 (turbine), :162 (electric), :170 (misc), :179 (heat_rej)
*Basis**: Balance-of-plant cost linear in plant-total driving power

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.linear_power_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Linear_Power_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, power: float, cost_per_mw: float, n_mod: float    ) -> Linear_Power_CostInput:
        """Validate inputs and fill defaults.

        Args:
            power: power input
            cost_per_mw: cost_per_mw input
            n_mod: n_mod input

        Returns:
            Validated input model
        """
        return Linear_Power_CostInput(power=power, cost_per_mw=cost_per_mw, n_mod=n_mod)

    def run(
        self, power: float, cost_per_mw: float, n_mod: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            power: power input
            cost_per_mw: cost_per_mw input
            n_mod: n_mod input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(power, cost_per_mw, n_mod)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.linear_power_cost_impl import (
            run_linear_power_cost,
        )

        # Execute implementation - returns single value
        cost = run_linear_power_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
