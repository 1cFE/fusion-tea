"""Coolant_Branch_HeatModule Module Wrapper

TEAx module for Coolant_Branch_Heat calculation.

delivered_heat = deposited_heat_in + received_exchange_in - exported_exchange_in + recovered_friction_in. All quantities are MW. Source: work/active/WI-086_aries-dual-blanket-heat-accounting/spec.md. Ref: conservation on a supplied coolant-branch boundary; topology evidence Raffray Fig12 retained in that item's evidence/raffray-p736.png. Basis: generic steady energy accounting, not flow, hydraulic or exchanger performance prediction. Typed native completion rejects nonfinite/negative supplied heat, negative delivered heat and overflow; zero heat is valid. Last Updated: 2026-09-21.

Inputs:
    - received_exchange_in: received_exchange_in parameter
    - exported_exchange_in: exported_exchange_in parameter
    - deposited_heat_in: deposited_heat_in parameter
    - recovered_friction_in: recovered_friction_in parameter

Outputs:
    - delivered_heat: delivered_heat result

SysML Source: root-0/dual_circuit_heat_accounting.sysml:4

SysML Source: root-0/dual_circuit_heat_accounting.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/dual_circuit_heat_accounting/coolant_branch_heat_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.primitives import Float


class Coolant_Branch_HeatInput(BaseModel):
    """Input model for Coolant_Branch_HeatModule.

    Attributes:
        received_exchange_in: received_exchange_in input
        exported_exchange_in: exported_exchange_in input
        deposited_heat_in: deposited_heat_in input
        recovered_friction_in: recovered_friction_in input
    """
    received_exchange_in: float = Field(..., description="received_exchange_in input")
    exported_exchange_in: float = Field(..., description="exported_exchange_in input")
    deposited_heat_in: float = Field(..., description="deposited_heat_in input")
    recovered_friction_in: float = Field(..., description="recovered_friction_in input")


class Coolant_Branch_HeatModule(ModuleBase[Coolant_Branch_HeatInput, Float]):
    """TEAx module for Coolant_Branch_Heat calculation.

delivered_heat = deposited_heat_in + received_exchange_in - exported_exchange_in + recovered_friction_in. All quantities are MW. Source: work/active/WI-086_aries-dual-blanket-heat-accounting/spec.md. Ref: conservation on a supplied coolant-branch boundary; topology evidence Raffray Fig12 retained in that item's evidence/raffray-p736.png. Basis: generic steady energy accounting, not flow, hydraulic or exchanger performance prediction. Typed native completion rejects nonfinite/negative supplied heat, negative delivered heat and overflow; zero heat is valid. Last Updated: 2026-09-21.

Inputs:
    - received_exchange_in: received_exchange_in parameter
    - exported_exchange_in: exported_exchange_in parameter
    - deposited_heat_in: deposited_heat_in parameter
    - recovered_friction_in: recovered_friction_in parameter

Outputs:
    - delivered_heat: delivered_heat result

SysML Source: root-0/dual_circuit_heat_accounting.sysml:4

    SysML Source: root-0/dual_circuit_heat_accounting.sysml:4

    Calculation Specification:
        See documentation:
delivered_heat = deposited_heat_in + received_exchange_in - exported_exchange_in + recovered_friction_in. All quantities are MW. Source: work/active/WI-086_aries-dual-blanket-heat-accounting/spec.md. Ref: conservation on a supplied coolant-branch boundary; topology evidence Raffray Fig12 retained in that item's evidence/raffray-p736.png. Basis: generic steady energy accounting, not flow, hydraulic or exchanger performance prediction. Typed native completion rejects nonfinite/negative supplied heat, negative delivered heat and overflow; zero heat is valid. Last Updated: 2026-09-21.

    IMPLEMENTATION: See combinations_tea.handwritten.dual_circuit_heat_accounting.coolant_branch_heat_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Coolant_Branch_HeatModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, received_exchange_in: float, exported_exchange_in: float, deposited_heat_in: float, recovered_friction_in: float    ) -> Coolant_Branch_HeatInput:
        """Validate inputs and fill defaults.

        Args:
            received_exchange_in: received_exchange_in input
            exported_exchange_in: exported_exchange_in input
            deposited_heat_in: deposited_heat_in input
            recovered_friction_in: recovered_friction_in input

        Returns:
            Validated input model
        """
        return Coolant_Branch_HeatInput(received_exchange_in=received_exchange_in, exported_exchange_in=exported_exchange_in, deposited_heat_in=deposited_heat_in, recovered_friction_in=recovered_friction_in)

    def run(
        self, received_exchange_in: float, exported_exchange_in: float, deposited_heat_in: float, recovered_friction_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            received_exchange_in: received_exchange_in input
            exported_exchange_in: exported_exchange_in input
            deposited_heat_in: deposited_heat_in input
            recovered_friction_in: recovered_friction_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(received_exchange_in, exported_exchange_in, deposited_heat_in, recovered_friction_in)

        # Import handwritten implementation
        from combinations_tea.handwritten.dual_circuit_heat_accounting.coolant_branch_heat_impl import (
            run_coolant_branch_heat,
        )

        # Execute implementation - returns single value
        delivered_heat = run_coolant_branch_heat(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(delivered_heat))
