"""Magnet_CapitalModule Module Wrapper

TEAx module for Magnet_Capital calculation.

CAS22.1.3 magnet account rollup (WI-035 D6): the decomposed magnet
capital is the sum of the separately sized sub-accounts. Kept as a
calc def so the plant's magnet.capital_cost redefinition stays a
reference binding (the codegen-proven WI-021 pattern), not an
arithmetic redefinition expression (dropped by the pinned codegen,
WI-030).

*Source**: work/completed/20260901_WI-035_magnet-closure/design.md
*Ref**: design D6 (rollup + comparison channel); design Risk 1
(redefinition envelope)
*Basis**: sum of winding-pack, all-in magnet structure and conditional additional sheet-stock sub-accounts; sheet inclusion in winding remains uncertain (WI-063 design).

Inputs:
    - winding_cost: winding_cost parameter
    - structure_cost_in: structure_cost_in parameter
    - insulation_stock_cost: insulation_stock_cost parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:181

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:181

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_cost/magnet_capital_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Magnet_CapitalInput(BaseModel):
    """Input model for Magnet_CapitalModule.

    Attributes:
        winding_cost: winding_cost input
        structure_cost_in: structure_cost_in input
        insulation_stock_cost: insulation_stock_cost input
    """
    winding_cost: float = Field(..., description="winding_cost input")
    structure_cost_in: float = Field(..., description="structure_cost_in input")
    insulation_stock_cost: float = Field(..., description="insulation_stock_cost input")


class Magnet_CapitalModule(ModuleBase[Magnet_CapitalInput, Float]):
    """TEAx module for Magnet_Capital calculation.

CAS22.1.3 magnet account rollup (WI-035 D6): the decomposed magnet
capital is the sum of the separately sized sub-accounts. Kept as a
calc def so the plant's magnet.capital_cost redefinition stays a
reference binding (the codegen-proven WI-021 pattern), not an
arithmetic redefinition expression (dropped by the pinned codegen,
WI-030).

*Source**: work/completed/20260901_WI-035_magnet-closure/design.md
*Ref**: design D6 (rollup + comparison channel); design Risk 1
(redefinition envelope)
*Basis**: sum of winding-pack, all-in magnet structure and conditional additional sheet-stock sub-accounts; sheet inclusion in winding remains uncertain (WI-063 design).

Inputs:
    - winding_cost: winding_cost parameter
    - structure_cost_in: structure_cost_in parameter
    - insulation_stock_cost: insulation_stock_cost parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:181

    SysML Source: root-0/analyses/mfe_magnet_cost.sysml:181

    Calculation Specification:
        insulation_stock_cost = 0.0
        capital_cost = winding_cost + structure_cost_in + insulation_stock_cost
        
Documentation:
CAS22.1.3 magnet account rollup (WI-035 D6): the decomposed magnet
capital is the sum of the separately sized sub-accounts. Kept as a
calc def so the plant's magnet.capital_cost redefinition stays a
reference binding (the codegen-proven WI-021 pattern), not an
arithmetic redefinition expression (dropped by the pinned codegen,
WI-030).

*Source**: work/completed/20260901_WI-035_magnet-closure/design.md
*Ref**: design D6 (rollup + comparison channel); design Risk 1
(redefinition envelope)
*Basis**: sum of winding-pack, all-in magnet structure and conditional additional sheet-stock sub-accounts; sheet inclusion in winding remains uncertain (WI-063 design).

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_cost.magnet_capital_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Magnet_CapitalModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, winding_cost: float, structure_cost_in: float, insulation_stock_cost: float    ) -> Magnet_CapitalInput:
        """Validate inputs and fill defaults.

        Args:
            winding_cost: winding_cost input
            structure_cost_in: structure_cost_in input
            insulation_stock_cost: insulation_stock_cost input

        Returns:
            Validated input model
        """
        return Magnet_CapitalInput(winding_cost=winding_cost, structure_cost_in=structure_cost_in, insulation_stock_cost=insulation_stock_cost)

    def run(
        self, winding_cost: float, structure_cost_in: float, insulation_stock_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            winding_cost: winding_cost input
            structure_cost_in: structure_cost_in input
            insulation_stock_cost: insulation_stock_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(winding_cost, structure_cost_in, insulation_stock_cost)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_cost.magnet_capital_impl import (
            run_magnet_capital,
        )

        # Execute implementation - returns single value
        capital_cost = run_magnet_capital(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(capital_cost))
