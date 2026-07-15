"""Power_Supplies_CostModule Module Wrapper

TEAx module for Power_Supplies_Cost calculation.

CAS22.1.7 Power supplies (steady-state: high-current DC for SC magnets,
switchgear). Power-law in gross electric:

  cost = base * (p_et/p_et_ref)^alpha

`base` is the account cost at the calibration power (power_supplies_base,
M$ at 1 GWe in the source) — a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:554 (c220107 steady-state), cas22.py:224 (P_ET_REF)
*Basis**: Power-scaled power-supply cost

Inputs:
    - base: base parameter
    - p_et: p_et parameter
    - p_et_ref: p_et_ref parameter
    - alpha: alpha parameter

Outputs:
    - cost: cost result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:140

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:140

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/power_supplies_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Power_Supplies_CostInput(BaseModel):
    """Input model for Power_Supplies_CostModule.

    Attributes:
        base: base input
        p_et: p_et input
        p_et_ref: p_et_ref input
        alpha: alpha input
    """
    base: float = Field(..., description="base input")
    p_et: float = Field(..., description="p_et input")
    p_et_ref: float = Field(..., description="p_et_ref input")
    alpha: float = Field(..., description="alpha input")


class Power_Supplies_CostModule(ModuleBase[Power_Supplies_CostInput, Float]):
    """TEAx module for Power_Supplies_Cost calculation.

CAS22.1.7 Power supplies (steady-state: high-current DC for SC magnets,
switchgear). Power-law in gross electric:

  cost = base * (p_et/p_et_ref)^alpha

`base` is the account cost at the calibration power (power_supplies_base,
M$ at 1 GWe in the source) — a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:554 (c220107 steady-state), cas22.py:224 (P_ET_REF)
*Basis**: Power-scaled power-supply cost

Inputs:
    - base: base parameter
    - p_et: p_et parameter
    - p_et_ref: p_et_ref parameter
    - alpha: alpha parameter

Outputs:
    - cost: cost result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:140

    SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:140

    Calculation Specification:
        p_et_ref = 1100.0
        alpha = 0.7
        cost = base * (p_et / p_et_ref) ** alpha
        
Documentation:
CAS22.1.7 Power supplies (steady-state: high-current DC for SC magnets,
switchgear). Power-law in gross electric:

  cost = base * (p_et/p_et_ref)^alpha

`base` is the account cost at the calibration power (power_supplies_base,
M$ at 1 GWe in the source) — a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:554 (c220107 steady-state), cas22.py:224 (P_ET_REF)
*Basis**: Power-scaled power-supply cost

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.power_supplies_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Power_Supplies_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, base: float, p_et: float, p_et_ref: float, alpha: float    ) -> Power_Supplies_CostInput:
        """Validate inputs and fill defaults.

        Args:
            base: base input
            p_et: p_et input
            p_et_ref: p_et_ref input
            alpha: alpha input

        Returns:
            Validated input model
        """
        return Power_Supplies_CostInput(base=base, p_et=p_et, p_et_ref=p_et_ref, alpha=alpha)

    def run(
        self, base: float, p_et: float, p_et_ref: float, alpha: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            base: base input
            p_et: p_et input
            p_et_ref: p_et_ref input
            alpha: alpha input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(base, p_et, p_et_ref, alpha)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.power_supplies_cost_impl import (
            run_power_supplies_cost,
        )

        # Execute implementation - returns single value
        cost = run_power_supplies_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
