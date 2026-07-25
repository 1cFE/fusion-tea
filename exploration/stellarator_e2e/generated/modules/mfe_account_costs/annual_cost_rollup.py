"""Annual_Cost_RollupModule Module Wrapper

TEAx module for Annual_Cost_Rollup calculation.

CAS70 = CAS71 + CAS72, and the total levelized annual cost the LCOE
numerator carries (CAS70 + CAS80). Pure addition — it introduces no new
economics, it makes the two sums producer channels the DCF core and the
1cfe-form comparison channel can read.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/model.py (pin 0254385)
*Ref**: model.py:1483-1605 (c70 = c71 + c72; lcoe numerator c90 + c70 + c80);
economics.py:88-92 (compute_lcoe)
*Basis**: 1costingFE CAS70 composition and LCOE annual-cost numerator

Inputs:
    - cas71: cas71 parameter
    - cas72: cas72 parameter
    - cas80: cas80 parameter

Outputs:
    - cas70: cas70 result
    - annual_total: annual_total result

SysML Source: root-0/analyses/mfe_account_costs.sysml:853

SysML Source: root-0/analyses/mfe_account_costs.sysml:853

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/annual_cost_rollup_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.annual_cost_rollup_output import Annual_Cost_RollupOutput


class Annual_Cost_RollupInput(BaseModel):
    """Input model for Annual_Cost_RollupModule.

    Attributes:
        cas71: cas71 input
        cas72: cas72 input
        cas80: cas80 input
    """
    cas71: float = Field(..., description="cas71 input")
    cas72: float = Field(..., description="cas72 input")
    cas80: float = Field(..., description="cas80 input")


class Annual_Cost_RollupModule(ModuleBase[Annual_Cost_RollupInput, Annual_Cost_RollupOutput]):
    """TEAx module for Annual_Cost_Rollup calculation.

CAS70 = CAS71 + CAS72, and the total levelized annual cost the LCOE
numerator carries (CAS70 + CAS80). Pure addition — it introduces no new
economics, it makes the two sums producer channels the DCF core and the
1cfe-form comparison channel can read.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/model.py (pin 0254385)
*Ref**: model.py:1483-1605 (c70 = c71 + c72; lcoe numerator c90 + c70 + c80);
economics.py:88-92 (compute_lcoe)
*Basis**: 1costingFE CAS70 composition and LCOE annual-cost numerator

Inputs:
    - cas71: cas71 parameter
    - cas72: cas72 parameter
    - cas80: cas80 parameter

Outputs:
    - cas70: cas70 result
    - annual_total: annual_total result

SysML Source: root-0/analyses/mfe_account_costs.sysml:853

    SysML Source: root-0/analyses/mfe_account_costs.sysml:853

    Calculation Specification:
        cas70 = cas71 + cas72
        annual_total = cas71 + cas72 + cas80
        
Documentation:
CAS70 = CAS71 + CAS72, and the total levelized annual cost the LCOE
numerator carries (CAS70 + CAS80). Pure addition — it introduces no new
economics, it makes the two sums producer channels the DCF core and the
1cfe-form comparison channel can read.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/model.py (pin 0254385)
*Ref**: model.py:1483-1605 (c70 = c71 + c72; lcoe numerator c90 + c70 + c80);
economics.py:88-92 (compute_lcoe)
*Basis**: 1costingFE CAS70 composition and LCOE annual-cost numerator

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.annual_cost_rollup_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts cas70, annual_total fields to separate channels.
    """

    name: str = "Annual_Cost_RollupModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, cas71: float, cas72: float, cas80: float    ) -> Annual_Cost_RollupInput:
        """Validate inputs and fill defaults.

        Args:
            cas71: cas71 input
            cas72: cas72 input
            cas80: cas80 input

        Returns:
            Validated input model
        """
        return Annual_Cost_RollupInput(cas71=cas71, cas72=cas72, cas80=cas80)

    def run(
        self, cas71: float, cas72: float, cas80: float    ) -> ModuleResult[Annual_Cost_RollupOutput]:
        """Execute calculation.

        Args:
            cas71: cas71 input
            cas72: cas72 input
            cas80: cas80 input

        Returns:
            Module result with Annual_Cost_RollupOutput (cas70, annual_total)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(cas71, cas72, cas80)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.annual_cost_rollup_impl import (
            run_annual_cost_rollup,
        )

        # Execute implementation - returns tuple of values
        cas70, annual_total = run_annual_cost_rollup(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Annual_Cost_RollupOutput(
                cas70=cas70,
                annual_total=annual_total,
            )
        )
