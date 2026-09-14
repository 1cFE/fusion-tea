"""price_heliumModule Module Wrapper

TEAx module for price_helium calculation.

Outputs:
    - price_helium: price_helium result

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:322

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:322

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/stellarator_09/stellaris/magnet/winding_pack/price_helium_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class price_heliumInput(BaseModel):
    """Input model for price_heliumModule.

    Attributes:
    """


class price_heliumModule(ModuleBase[price_heliumInput, Float]):
    """TEAx module for price_helium calculation.

Outputs:
    - price_helium: price_helium result

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:322

    SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:322

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.stellarator_09.stellaris.magnet.winding_pack.price_helium_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "price_heliumModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self,     ) -> price_heliumInput:
        """Validate inputs and fill defaults.

        Args:

        Returns:
            Validated input model
        """
        return price_heliumInput()

    def run(
        self,     ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default()

        # Import handwritten implementation
        from stellarator_tea.handwritten.stellarator_09.stellaris.magnet.winding_pack.price_helium_impl import (
            run_price_helium,
        )

        # Execute implementation - returns single value
        price_helium = run_price_helium(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(price_helium))
