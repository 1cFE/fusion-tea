"""p_net_kwModule Module Wrapper

Computed attribute module.

SysML Expression: p_net_mw * 1000.0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/p_net_kw_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery.primitives import Float


class p_net_kwInput(BaseModel):
    """Input model for p_net_kwModule.

    Attributes:
        p_net_mw: Input p_net_mw
    """
    p_net_mw: float = Field(..., description="Input p_net_mw")


class p_net_kwModule(ModuleBase[p_net_kwInput, Float]):
    """Computed attribute module.

SysML Expression: p_net_mw * 1000.0

    SysML Source: unknown:0

    Calculation Specification:
        p_net_mw * 1000.0

    IMPLEMENTATION: See solar_battery.handwritten.solarbatterydesign.solar_battery_plant.p_net_kw_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "p_net_kwModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_net_mw: float    ) -> p_net_kwInput:
        """Validate inputs and fill defaults.

        Args:
            p_net_mw: Input p_net_mw

        Returns:
            Validated input model
        """
        return p_net_kwInput(p_net_mw=p_net_mw)

    def run(
        self, p_net_mw: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            p_net_mw: Input p_net_mw

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_net_mw)

        # Import handwritten implementation
        from solar_battery.handwritten.solarbatterydesign.solar_battery_plant.p_net_kw_impl import (
            run_solarbatterydesign__solar_battery_plant__p_net_kw,
        )

        # Execute implementation - returns single value
        p_net_kw = run_solarbatterydesign__solar_battery_plant__p_net_kw(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(p_net_kw))
