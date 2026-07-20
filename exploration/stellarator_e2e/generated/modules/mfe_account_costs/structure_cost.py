"""Structure_CostModule Module Wrapper

TEAx module for Structure_Cost calculation.

CAS22.1.5 Primary structure (gravity supports, thermal shields,
inter-coil structure, machine base) cost. Volume x gross-electric
scaling:

  cost = unit_cost * structure_vol * (p_et/p_et_ref)^alpha

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:501 (c220105), cas22.py:224 (P_ET_REF=ref_gross_power_mwe)
*Basis**: Volume-based structure cost with gross-electric power law

Inputs:
    - unit_cost: unit_cost parameter
    - structure_vol: structure_vol parameter
    - p_et: p_et parameter
    - p_et_ref: p_et_ref parameter
    - alpha: alpha parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:81

SysML Source: root-0/analyses/mfe_account_costs.sysml:81

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/structure_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Structure_CostInput(BaseModel):
    """Input model for Structure_CostModule.

    Attributes:
        unit_cost: unit_cost input
        structure_vol: structure_vol input
        p_et: p_et input
        p_et_ref: p_et_ref input
        alpha: alpha input
    """
    unit_cost: float = Field(..., description="unit_cost input")
    structure_vol: float = Field(..., description="structure_vol input")
    p_et: float = Field(..., description="p_et input")
    p_et_ref: float = Field(..., description="p_et_ref input")
    alpha: float = Field(..., description="alpha input")


class Structure_CostModule(ModuleBase[Structure_CostInput, Float]):
    """TEAx module for Structure_Cost calculation.

CAS22.1.5 Primary structure (gravity supports, thermal shields,
inter-coil structure, machine base) cost. Volume x gross-electric
scaling:

  cost = unit_cost * structure_vol * (p_et/p_et_ref)^alpha

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:501 (c220105), cas22.py:224 (P_ET_REF=ref_gross_power_mwe)
*Basis**: Volume-based structure cost with gross-electric power law

Inputs:
    - unit_cost: unit_cost parameter
    - structure_vol: structure_vol parameter
    - p_et: p_et parameter
    - p_et_ref: p_et_ref parameter
    - alpha: alpha parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:81

    SysML Source: root-0/analyses/mfe_account_costs.sysml:81

    Calculation Specification:
        p_et_ref = 1100.0
        alpha = 0.5
        cost = unit_cost * structure_vol * (p_et / p_et_ref) ** alpha
        
Documentation:
CAS22.1.5 Primary structure (gravity supports, thermal shields,
inter-coil structure, machine base) cost. Volume x gross-electric
scaling:

  cost = unit_cost * structure_vol * (p_et/p_et_ref)^alpha

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:501 (c220105), cas22.py:224 (P_ET_REF=ref_gross_power_mwe)
*Basis**: Volume-based structure cost with gross-electric power law

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.structure_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Structure_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, unit_cost: float, structure_vol: float, p_et: float, p_et_ref: float, alpha: float    ) -> Structure_CostInput:
        """Validate inputs and fill defaults.

        Args:
            unit_cost: unit_cost input
            structure_vol: structure_vol input
            p_et: p_et input
            p_et_ref: p_et_ref input
            alpha: alpha input

        Returns:
            Validated input model
        """
        return Structure_CostInput(unit_cost=unit_cost, structure_vol=structure_vol, p_et=p_et, p_et_ref=p_et_ref, alpha=alpha)

    def run(
        self, unit_cost: float, structure_vol: float, p_et: float, p_et_ref: float, alpha: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            unit_cost: unit_cost input
            structure_vol: structure_vol input
            p_et: p_et input
            p_et_ref: p_et_ref input
            alpha: alpha input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(unit_cost, structure_vol, p_et, p_et_ref, alpha)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.structure_cost_impl import (
            run_structure_cost,
        )

        # Execute implementation - returns single value
        cost = run_structure_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
