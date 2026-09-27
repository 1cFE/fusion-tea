"""Recuperator_Installed_CapabilityModule Module Wrapper

TEAx module for Recuperator_Installed_Capability calculation.

*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/recuperator_installed_capability_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

Inputs:
    - ua_in: ua_in parameter
    - flow_in: flow_in parameter
    - cp_in: cp_in parameter

Outputs:
    - capacity_rate: capacity_rate result
    - effectiveness: effectiveness result

SysML Source: root-0/component_alternatives_thermal.sysml:116

SysML Source: root-0/component_alternatives_thermal.sysml:116

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/component_alternatives_thermal/recuperator_installed_capability_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.primitives import Float
from component_alternatives_tea.schemas.recuperator_installed_capability_output import Recuperator_Installed_CapabilityOutput


class Recuperator_Installed_CapabilityInput(BaseModel):
    """Input model for Recuperator_Installed_CapabilityModule.

    Attributes:
        ua_in: ua_in input
        flow_in: flow_in input
        cp_in: cp_in input
    """
    ua_in: float = Field(..., description="ua_in input")
    flow_in: float = Field(..., description="flow_in input")
    cp_in: float = Field(..., description="cp_in input")


class Recuperator_Installed_CapabilityModule(ModuleBase[Recuperator_Installed_CapabilityInput, Recuperator_Installed_CapabilityOutput]):
    """TEAx module for Recuperator_Installed_Capability calculation.

*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/recuperator_installed_capability_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

Inputs:
    - ua_in: ua_in parameter
    - flow_in: flow_in parameter
    - cp_in: cp_in parameter

Outputs:
    - capacity_rate: capacity_rate result
    - effectiveness: effectiveness result

SysML Source: root-0/component_alternatives_thermal.sysml:116

    SysML Source: root-0/component_alternatives_thermal.sysml:116

    Calculation Specification:
        ua_in = 60.0
        flow_in = 2000.0
        cp_in = 5193.0
        
Documentation:
*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/recuperator_installed_capability_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

    IMPLEMENTATION: See component_alternatives_tea.handwritten.component_alternatives_thermal.recuperator_installed_capability_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts capacity_rate, effectiveness fields to separate channels.
    """

    name: str = "Recuperator_Installed_CapabilityModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, ua_in: float, flow_in: float, cp_in: float    ) -> Recuperator_Installed_CapabilityInput:
        """Validate inputs and fill defaults.

        Args:
            ua_in: ua_in input
            flow_in: flow_in input
            cp_in: cp_in input

        Returns:
            Validated input model
        """
        return Recuperator_Installed_CapabilityInput(ua_in=ua_in, flow_in=flow_in, cp_in=cp_in)

    def run(
        self, ua_in: float, flow_in: float, cp_in: float    ) -> ModuleResult[Recuperator_Installed_CapabilityOutput]:
        """Execute calculation.

        Args:
            ua_in: ua_in input
            flow_in: flow_in input
            cp_in: cp_in input

        Returns:
            Module result with Recuperator_Installed_CapabilityOutput (capacity_rate, effectiveness)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(ua_in, flow_in, cp_in)

        # Import handwritten implementation
        from component_alternatives_tea.handwritten.component_alternatives_thermal.recuperator_installed_capability_impl import (
            run_recuperator_installed_capability,
        )

        # Execute implementation - returns tuple of values
        capacity_rate, effectiveness = run_recuperator_installed_capability(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Recuperator_Installed_CapabilityOutput(
                capacity_rate=capacity_rate,
                effectiveness=effectiveness,
            )
        )
