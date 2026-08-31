"""Magnet_CapitalModule Module Wrapper

TEAx module for Magnet_Capital calculation.

CAS22.1.3 magnet account rollup (WI-035 D6): the decomposed magnet
capital is the sum of the separately sized sub-accounts. Kept as a
calc def so the plant's magnet.capital_cost redefinition stays a
reference binding (the codegen-proven WI-021 pattern), not an
arithmetic redefinition expression (dropped by the pinned codegen,
WI-030).

*Source**: work/active/WI-035_magnet-closure/design.md
*Ref**: design D6 (rollup + comparison channel); design Risk 1
(redefinition envelope)
*Basis**: sum of winding-pack and magnet-structure sub-accounts

Inputs:
    - structure_cost_in: structure_cost_in parameter
    - winding_cost: winding_cost parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:137

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:137

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_cost/magnet_capital_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Magnet_CapitalInput(BaseModel):
    """Input model for Magnet_CapitalModule.

    Attributes:
        structure_cost_in: structure_cost_in input
        winding_cost: winding_cost input
    """
    structure_cost_in: float = Field(..., description="structure_cost_in input")
    winding_cost: float = Field(..., description="winding_cost input")


class Magnet_CapitalModule(ModuleBase[Magnet_CapitalInput, Float]):
    """TEAx module for Magnet_Capital calculation.

CAS22.1.3 magnet account rollup (WI-035 D6): the decomposed magnet
capital is the sum of the separately sized sub-accounts. Kept as a
calc def so the plant's magnet.capital_cost redefinition stays a
reference binding (the codegen-proven WI-021 pattern), not an
arithmetic redefinition expression (dropped by the pinned codegen,
WI-030).

*Source**: work/active/WI-035_magnet-closure/design.md
*Ref**: design D6 (rollup + comparison channel); design Risk 1
(redefinition envelope)
*Basis**: sum of winding-pack and magnet-structure sub-accounts

Inputs:
    - structure_cost_in: structure_cost_in parameter
    - winding_cost: winding_cost parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:137

    SysML Source: root-0/analyses/mfe_magnet_cost.sysml:137

    Calculation Specification:
        capital_cost = winding_cost + structure_cost_in
        
Documentation:
CAS22.1.3 magnet account rollup (WI-035 D6): the decomposed magnet
capital is the sum of the separately sized sub-accounts. Kept as a
calc def so the plant's magnet.capital_cost redefinition stays a
reference binding (the codegen-proven WI-021 pattern), not an
arithmetic redefinition expression (dropped by the pinned codegen,
WI-030).

*Source**: work/active/WI-035_magnet-closure/design.md
*Ref**: design D6 (rollup + comparison channel); design Risk 1
(redefinition envelope)
*Basis**: sum of winding-pack and magnet-structure sub-accounts

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_cost.magnet_capital_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Magnet_CapitalModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, structure_cost_in: float, winding_cost: float    ) -> Magnet_CapitalInput:
        """Validate inputs and fill defaults.

        Args:
            structure_cost_in: structure_cost_in input
            winding_cost: winding_cost input

        Returns:
            Validated input model
        """
        return Magnet_CapitalInput(structure_cost_in=structure_cost_in, winding_cost=winding_cost)

    def run(
        self, structure_cost_in: float, winding_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            structure_cost_in: structure_cost_in input
            winding_cost: winding_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(structure_cost_in, winding_cost)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_cost.magnet_capital_impl import (
            run_magnet_capital,
        )

        # Execute implementation - returns single value
        capital_cost = run_magnet_capital(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(capital_cost))
