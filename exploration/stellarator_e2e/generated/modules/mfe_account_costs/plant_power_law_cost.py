"""Plant_Power_Law_CostModule Module Wrapper

TEAx module for Plant_Power_Law_Cost calculation.

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

Inputs:
    - base: base parameter
    - ref_power: ref_power parameter
    - alpha: alpha parameter
    - n_mod_in: n_mod_in parameter
    - power: power parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:449

SysML Source: root-0/analyses/mfe_account_costs.sysml:449

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/plant_power_law_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Plant_Power_Law_CostInput(BaseModel):
    """Input model for Plant_Power_Law_CostModule.

    Attributes:
        base: base input
        ref_power: ref_power input
        alpha: alpha input
        n_mod_in: n_mod_in input
        power: power input
    """
    base: float = Field(..., description="base input")
    ref_power: float = Field(..., description="ref_power input")
    alpha: float = Field(..., description="alpha input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    power: float = Field(..., description="power input")


class Plant_Power_Law_CostModule(ModuleBase[Plant_Power_Law_CostInput, Float]):
    """TEAx module for Plant_Power_Law_Cost calculation.

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

Inputs:
    - base: base parameter
    - ref_power: ref_power parameter
    - alpha: alpha parameter
    - n_mod_in: n_mod_in parameter
    - power: power parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:449

    SysML Source: root-0/analyses/mfe_account_costs.sysml:449

    Calculation Specification:
        n_mod_in = 1.0
        cost = base * (n_mod_in * power / ref_power) ** alpha
        
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.plant_power_law_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Plant_Power_Law_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, base: float, ref_power: float, alpha: float, n_mod_in: float, power: float    ) -> Plant_Power_Law_CostInput:
        """Validate inputs and fill defaults.

        Args:
            base: base input
            ref_power: ref_power input
            alpha: alpha input
            n_mod_in: n_mod_in input
            power: power input

        Returns:
            Validated input model
        """
        return Plant_Power_Law_CostInput(base=base, ref_power=ref_power, alpha=alpha, n_mod_in=n_mod_in, power=power)

    def run(
        self, base: float, ref_power: float, alpha: float, n_mod_in: float, power: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            base: base input
            ref_power: ref_power input
            alpha: alpha input
            n_mod_in: n_mod_in input
            power: power input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(base, ref_power, alpha, n_mod_in, power)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.plant_power_law_cost_impl import (
            run_plant_power_law_cost,
        )

        # Execute implementation - returns single value
        cost = run_plant_power_law_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
