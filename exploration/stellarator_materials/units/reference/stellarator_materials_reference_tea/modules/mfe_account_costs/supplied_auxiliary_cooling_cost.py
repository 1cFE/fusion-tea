"""Supplied_Auxiliary_Cooling_CostModule Module Wrapper

TEAx module for Supplied_Auxiliary_Cooling_Cost calculation.

WI-079 separate chosen auxiliary allowance and cryogenic package price.
aux_cost = aux_per_mw_in * thermal_class_in * n_mod_in;
cryo_cost = purchase_cost_in; cost = aux_cost + cryo_cost.
The class is thermal MW of the selected procurement scenario, never actual
rejected heat or cold-stage W. The cryo amount is dollars for the selected
package; current one-module scope preserves entering aggregation. Native
completion rejects nonfinite/negative inputs and n_mod_in other than one.
*Source**: modeling_project/REQUIREMENTS.md
*Reference**: MR-7; work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/design.md
*Basis**: reviewed selected amount plus independent budget-class allowance
*Last Updated**: 2026-09-20

Inputs:
    - thermal_class_in: thermal_class_in parameter
    - n_mod_in: n_mod_in parameter
    - aux_per_mw_in: aux_per_mw_in parameter
    - purchase_cost_in: purchase_cost_in parameter

Outputs:
    - cost: cost result
    - cryo_cost: cryo_cost result
    - aux_cost: aux_cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:33

SysML Source: root-0/analyses/mfe_account_costs.sysml:33

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/supplied_auxiliary_cooling_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float
from stellarator_materials_reference_tea.schemas.supplied_auxiliary_cooling_cost_output import Supplied_Auxiliary_Cooling_CostOutput


class Supplied_Auxiliary_Cooling_CostInput(BaseModel):
    """Input model for Supplied_Auxiliary_Cooling_CostModule.

    Attributes:
        thermal_class_in: thermal_class_in input
        n_mod_in: n_mod_in input
        aux_per_mw_in: aux_per_mw_in input
        purchase_cost_in: purchase_cost_in input
    """
    thermal_class_in: float = Field(..., description="thermal_class_in input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    aux_per_mw_in: float = Field(..., description="aux_per_mw_in input")
    purchase_cost_in: float = Field(..., description="purchase_cost_in input")


class Supplied_Auxiliary_Cooling_CostModule(ModuleBase[Supplied_Auxiliary_Cooling_CostInput, Supplied_Auxiliary_Cooling_CostOutput]):
    """TEAx module for Supplied_Auxiliary_Cooling_Cost calculation.

WI-079 separate chosen auxiliary allowance and cryogenic package price.
aux_cost = aux_per_mw_in * thermal_class_in * n_mod_in;
cryo_cost = purchase_cost_in; cost = aux_cost + cryo_cost.
The class is thermal MW of the selected procurement scenario, never actual
rejected heat or cold-stage W. The cryo amount is dollars for the selected
package; current one-module scope preserves entering aggregation. Native
completion rejects nonfinite/negative inputs and n_mod_in other than one.
*Source**: modeling_project/REQUIREMENTS.md
*Reference**: MR-7; work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/design.md
*Basis**: reviewed selected amount plus independent budget-class allowance
*Last Updated**: 2026-09-20

Inputs:
    - thermal_class_in: thermal_class_in parameter
    - n_mod_in: n_mod_in parameter
    - aux_per_mw_in: aux_per_mw_in parameter
    - purchase_cost_in: purchase_cost_in parameter

Outputs:
    - cost: cost result
    - cryo_cost: cryo_cost result
    - aux_cost: aux_cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:33

    SysML Source: root-0/analyses/mfe_account_costs.sysml:33

    Calculation Specification:
        See documentation:
WI-079 separate chosen auxiliary allowance and cryogenic package price.
aux_cost = aux_per_mw_in * thermal_class_in * n_mod_in;
cryo_cost = purchase_cost_in; cost = aux_cost + cryo_cost.
The class is thermal MW of the selected procurement scenario, never actual
rejected heat or cold-stage W. The cryo amount is dollars for the selected
package; current one-module scope preserves entering aggregation. Native
completion rejects nonfinite/negative inputs and n_mod_in other than one.
*Source**: modeling_project/REQUIREMENTS.md
*Reference**: MR-7; work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/design.md
*Basis**: reviewed selected amount plus independent budget-class allowance
*Last Updated**: 2026-09-20

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_account_costs.supplied_auxiliary_cooling_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts cost, cryo_cost, aux_cost fields to separate channels.
    """

    name: str = "Supplied_Auxiliary_Cooling_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, thermal_class_in: float, n_mod_in: float, aux_per_mw_in: float, purchase_cost_in: float    ) -> Supplied_Auxiliary_Cooling_CostInput:
        """Validate inputs and fill defaults.

        Args:
            thermal_class_in: thermal_class_in input
            n_mod_in: n_mod_in input
            aux_per_mw_in: aux_per_mw_in input
            purchase_cost_in: purchase_cost_in input

        Returns:
            Validated input model
        """
        return Supplied_Auxiliary_Cooling_CostInput(thermal_class_in=thermal_class_in, n_mod_in=n_mod_in, aux_per_mw_in=aux_per_mw_in, purchase_cost_in=purchase_cost_in)

    def run(
        self, thermal_class_in: float, n_mod_in: float, aux_per_mw_in: float, purchase_cost_in: float    ) -> ModuleResult[Supplied_Auxiliary_Cooling_CostOutput]:
        """Execute calculation.

        Args:
            thermal_class_in: thermal_class_in input
            n_mod_in: n_mod_in input
            aux_per_mw_in: aux_per_mw_in input
            purchase_cost_in: purchase_cost_in input

        Returns:
            Module result with Supplied_Auxiliary_Cooling_CostOutput (cost, cryo_cost, aux_cost)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(thermal_class_in, n_mod_in, aux_per_mw_in, purchase_cost_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_account_costs.supplied_auxiliary_cooling_cost_impl import (
            run_supplied_auxiliary_cooling_cost,
        )

        # Execute implementation - returns tuple of values
        cost, cryo_cost, aux_cost = run_supplied_auxiliary_cooling_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Supplied_Auxiliary_Cooling_CostOutput(
                cost=cost,
                cryo_cost=cryo_cost,
                aux_cost=aux_cost,
            )
        )
