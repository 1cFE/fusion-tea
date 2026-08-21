"""IDC_Closed_Form_CostModule Module Wrapper

TEAx module for IDC_Closed_Form_Cost calculation.

CAS60 interest-during-construction line (closed form, uniform spend):

  f_idc = ((1 + interest_rate) ** construction_years - 1)
          / (interest_rate * construction_years) - 1
  cost  = f_idc * overnight_cost

Variable real exponent construction_years — the idc_factor precedent
(mfe_lcoe_dcf.sysml:47) proves the codegen envelope handles it. WI-028
Option C (owner-ruled): this line is A-2-checked and reported but
EXCLUDED from total_capital; the DCF idc_factor is untouched.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:286-297 (cas60_idc)
*Basis**: Uniform-spend closed-form interest during construction

Inputs:
    - interest_rate: interest_rate parameter
    - construction_years: construction_years parameter
    - overnight_cost: overnight_cost parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:601

SysML Source: root-0/analyses/mfe_account_costs.sysml:601

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/idc_closed_form_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class IDC_Closed_Form_CostInput(BaseModel):
    """Input model for IDC_Closed_Form_CostModule.

    Attributes:
        interest_rate: interest_rate input
        construction_years: construction_years input
        overnight_cost: overnight_cost input
    """
    interest_rate: float = Field(..., description="interest_rate input")
    construction_years: float = Field(..., description="construction_years input")
    overnight_cost: float = Field(..., description="overnight_cost input")


class IDC_Closed_Form_CostModule(ModuleBase[IDC_Closed_Form_CostInput, Float]):
    """TEAx module for IDC_Closed_Form_Cost calculation.

CAS60 interest-during-construction line (closed form, uniform spend):

  f_idc = ((1 + interest_rate) ** construction_years - 1)
          / (interest_rate * construction_years) - 1
  cost  = f_idc * overnight_cost

Variable real exponent construction_years — the idc_factor precedent
(mfe_lcoe_dcf.sysml:47) proves the codegen envelope handles it. WI-028
Option C (owner-ruled): this line is A-2-checked and reported but
EXCLUDED from total_capital; the DCF idc_factor is untouched.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:286-297 (cas60_idc)
*Basis**: Uniform-spend closed-form interest during construction

Inputs:
    - interest_rate: interest_rate parameter
    - construction_years: construction_years parameter
    - overnight_cost: overnight_cost parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:601

    SysML Source: root-0/analyses/mfe_account_costs.sysml:601

    Calculation Specification:
        f_idc = ((1.0 + interest_rate) ** construction_years - 1.0) / (interest_rate * construction_years) - 1.0
        cost = f_idc * overnight_cost
        
Documentation:
CAS60 interest-during-construction line (closed form, uniform spend):

  f_idc = ((1 + interest_rate) ** construction_years - 1)
          / (interest_rate * construction_years) - 1
  cost  = f_idc * overnight_cost

Variable real exponent construction_years — the idc_factor precedent
(mfe_lcoe_dcf.sysml:47) proves the codegen envelope handles it. WI-028
Option C (owner-ruled): this line is A-2-checked and reported but
EXCLUDED from total_capital; the DCF idc_factor is untouched.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:286-297 (cas60_idc)
*Basis**: Uniform-spend closed-form interest during construction

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.idc_closed_form_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "IDC_Closed_Form_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, interest_rate: float, construction_years: float, overnight_cost: float    ) -> IDC_Closed_Form_CostInput:
        """Validate inputs and fill defaults.

        Args:
            interest_rate: interest_rate input
            construction_years: construction_years input
            overnight_cost: overnight_cost input

        Returns:
            Validated input model
        """
        return IDC_Closed_Form_CostInput(interest_rate=interest_rate, construction_years=construction_years, overnight_cost=overnight_cost)

    def run(
        self, interest_rate: float, construction_years: float, overnight_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            interest_rate: interest_rate input
            construction_years: construction_years input
            overnight_cost: overnight_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(interest_rate, construction_years, overnight_cost)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.idc_closed_form_cost_impl import (
            run_idc_closed_form_cost,
        )

        # Execute implementation - returns single value
        cost = run_idc_closed_form_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
