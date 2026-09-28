"""Divertor_CostModule Module Wrapper

TEAx module for Divertor_Cost calculation.

CAS22.1.8 Divertor (W monoblock cassettes on CuCrZr heat sinks) cost,
steady-state MFE. Power-law in thermal power:

  cost = base * (p_th/p_th_ref)^alpha

`base` is the account cost at the 1 GWth calibration point
(divertor_base) -- a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:570 (c220108 steady-state, divertor concepts)
*Basis**: Power-scaled divertor cost; MFE analogue of IFE target factory

Inputs:
    - p_th_ref: p_th_ref parameter
    - alpha: alpha parameter
    - base: base parameter
    - p_th_in: p_th_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:168

SysML Source: root-0/analyses/mfe_account_costs.sysml:168

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/divertor_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Divertor_CostInput(BaseModel):
    """Input model for Divertor_CostModule.

    Attributes:
        p_th_ref: p_th_ref input
        alpha: alpha input
        base: base input
        p_th_in: p_th_in input
    """
    p_th_ref: float = Field(..., description="p_th_ref input")
    alpha: float = Field(..., description="alpha input")
    base: float = Field(..., description="base input")
    p_th_in: float = Field(..., description="p_th_in input")


class Divertor_CostModule(ModuleBase[Divertor_CostInput, Float]):
    """TEAx module for Divertor_Cost calculation.

CAS22.1.8 Divertor (W monoblock cassettes on CuCrZr heat sinks) cost,
steady-state MFE. Power-law in thermal power:

  cost = base * (p_th/p_th_ref)^alpha

`base` is the account cost at the 1 GWth calibration point
(divertor_base) -- a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:570 (c220108 steady-state, divertor concepts)
*Basis**: Power-scaled divertor cost; MFE analogue of IFE target factory

Inputs:
    - p_th_ref: p_th_ref parameter
    - alpha: alpha parameter
    - base: base parameter
    - p_th_in: p_th_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:168

    SysML Source: root-0/analyses/mfe_account_costs.sysml:168

    Calculation Specification:
        p_th_ref = 1000.0
        alpha = 0.5
        cost = base * (p_th_in / p_th_ref) ** alpha
        
Documentation:
CAS22.1.8 Divertor (W monoblock cassettes on CuCrZr heat sinks) cost,
steady-state MFE. Power-law in thermal power:

  cost = base * (p_th/p_th_ref)^alpha

`base` is the account cost at the 1 GWth calibration point
(divertor_base) -- a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:570 (c220108 steady-state, divertor concepts)
*Basis**: Power-scaled divertor cost; MFE analogue of IFE target factory

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.divertor_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Divertor_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_th_ref: float, alpha: float, base: float, p_th_in: float    ) -> Divertor_CostInput:
        """Validate inputs and fill defaults.

        Args:
            p_th_ref: p_th_ref input
            alpha: alpha input
            base: base input
            p_th_in: p_th_in input

        Returns:
            Validated input model
        """
        return Divertor_CostInput(p_th_ref=p_th_ref, alpha=alpha, base=base, p_th_in=p_th_in)

    def run(
        self, p_th_ref: float, alpha: float, base: float, p_th_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            p_th_ref: p_th_ref input
            alpha: alpha input
            base: base input
            p_th_in: p_th_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_th_ref, alpha, base, p_th_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.divertor_cost_impl import (
            run_divertor_cost,
        )

        # Execute implementation - returns single value
        cost = run_divertor_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
