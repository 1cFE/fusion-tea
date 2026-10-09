"""Blanket_CostModule Module Wrapper

TEAx module for Blanket_Cost calculation.

CAS22.1.1 First-wall + blanket + neutron-multiplier cost. Hybrid
volume x thermal-power scaling:

  cost = unit_cost * structure_factor * blanket_vol * (p_th/p_th_ref)^alpha

`unit_cost` is the fuel- and fill-chemistry-effective blanket unit cost
(fuel-keyed table with a Li2O override in the source); `structure_factor`
is the blanket-form multiplier. Both are concept inputs (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:252-254 (c220101), cas22.py:223 (P_TH_REF=2500)
*Basis**: Volume-based blanket cost with thermal-intensity power law

Inputs:
    - blanket_vol: blanket_vol parameter
    - p_th_in: p_th_in parameter
    - p_th_ref: p_th_ref parameter
    - structure_factor: structure_factor parameter
    - alpha: alpha parameter
    - unit_cost: unit_cost parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:72

SysML Source: root-0/analyses/mfe_account_costs.sysml:72

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/blanket_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float


class Blanket_CostInput(BaseModel):
    """Input model for Blanket_CostModule.

    Attributes:
        blanket_vol: blanket_vol input
        p_th_in: p_th_in input
        p_th_ref: p_th_ref input
        structure_factor: structure_factor input
        alpha: alpha input
        unit_cost: unit_cost input
    """
    blanket_vol: float = Field(..., description="blanket_vol input")
    p_th_in: float = Field(..., description="p_th_in input")
    p_th_ref: float = Field(..., description="p_th_ref input")
    structure_factor: float = Field(..., description="structure_factor input")
    alpha: float = Field(..., description="alpha input")
    unit_cost: float = Field(..., description="unit_cost input")


class Blanket_CostModule(ModuleBase[Blanket_CostInput, Float]):
    """TEAx module for Blanket_Cost calculation.

CAS22.1.1 First-wall + blanket + neutron-multiplier cost. Hybrid
volume x thermal-power scaling:

  cost = unit_cost * structure_factor * blanket_vol * (p_th/p_th_ref)^alpha

`unit_cost` is the fuel- and fill-chemistry-effective blanket unit cost
(fuel-keyed table with a Li2O override in the source); `structure_factor`
is the blanket-form multiplier. Both are concept inputs (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:252-254 (c220101), cas22.py:223 (P_TH_REF=2500)
*Basis**: Volume-based blanket cost with thermal-intensity power law

Inputs:
    - blanket_vol: blanket_vol parameter
    - p_th_in: p_th_in parameter
    - p_th_ref: p_th_ref parameter
    - structure_factor: structure_factor parameter
    - alpha: alpha parameter
    - unit_cost: unit_cost parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:72

    SysML Source: root-0/analyses/mfe_account_costs.sysml:72

    Calculation Specification:
        p_th_ref = 2500.0
        alpha = 0.6
        cost = unit_cost * structure_factor * blanket_vol * (p_th_in / p_th_ref) ** alpha
        
Documentation:
CAS22.1.1 First-wall + blanket + neutron-multiplier cost. Hybrid
volume x thermal-power scaling:

  cost = unit_cost * structure_factor * blanket_vol * (p_th/p_th_ref)^alpha

`unit_cost` is the fuel- and fill-chemistry-effective blanket unit cost
(fuel-keyed table with a Li2O override in the source); `structure_factor`
is the blanket-form multiplier. Both are concept inputs (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:252-254 (c220101), cas22.py:223 (P_TH_REF=2500)
*Basis**: Volume-based blanket cost with thermal-intensity power law

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_account_costs.blanket_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Blanket_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, blanket_vol: float, p_th_in: float, p_th_ref: float, structure_factor: float, alpha: float, unit_cost: float    ) -> Blanket_CostInput:
        """Validate inputs and fill defaults.

        Args:
            blanket_vol: blanket_vol input
            p_th_in: p_th_in input
            p_th_ref: p_th_ref input
            structure_factor: structure_factor input
            alpha: alpha input
            unit_cost: unit_cost input

        Returns:
            Validated input model
        """
        return Blanket_CostInput(blanket_vol=blanket_vol, p_th_in=p_th_in, p_th_ref=p_th_ref, structure_factor=structure_factor, alpha=alpha, unit_cost=unit_cost)

    def run(
        self, blanket_vol: float, p_th_in: float, p_th_ref: float, structure_factor: float, alpha: float, unit_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            blanket_vol: blanket_vol input
            p_th_in: p_th_in input
            p_th_ref: p_th_ref input
            structure_factor: structure_factor input
            alpha: alpha input
            unit_cost: unit_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(blanket_vol, p_th_in, p_th_ref, structure_factor, alpha, unit_cost)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_account_costs.blanket_cost_impl import (
            run_blanket_cost,
        )

        # Execute implementation - returns single value
        cost = run_blanket_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
