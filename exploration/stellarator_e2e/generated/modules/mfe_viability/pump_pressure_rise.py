"""Pump_Pressure_RiseModule Module Wrapper

TEAx module for Pump_Pressure_Rise calculation.

Required pump pressure rise MPa = outlet minus inlet; inactive returns zero. Finite active arithmetic is guarded. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: MR-7 conditional rating contract. **Last Updated**: 2026-09-20

Inputs:
    - inlet_MPa_in: inlet_MPa_in parameter
    - active_in: active_in parameter
    - outlet_MPa_in: outlet_MPa_in parameter

Outputs:
    - demand: demand result

SysML Source: root-0/analyses/mfe_viability.sysml:92

SysML Source: root-0/analyses/mfe_viability.sysml:92

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_viability/pump_pressure_rise_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Pump_Pressure_RiseInput(BaseModel):
    """Input model for Pump_Pressure_RiseModule.

    Attributes:
        inlet_MPa_in: inlet_MPa_in input
        active_in: active_in input
        outlet_MPa_in: outlet_MPa_in input
    """
    inlet_MPa_in: float = Field(..., description="inlet_MPa_in input")
    active_in: bool = Field(..., description="active_in input")
    outlet_MPa_in: float = Field(..., description="outlet_MPa_in input")


class Pump_Pressure_RiseModule(ModuleBase[Pump_Pressure_RiseInput, Float]):
    """TEAx module for Pump_Pressure_Rise calculation.

Required pump pressure rise MPa = outlet minus inlet; inactive returns zero. Finite active arithmetic is guarded. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: MR-7 conditional rating contract. **Last Updated**: 2026-09-20

Inputs:
    - inlet_MPa_in: inlet_MPa_in parameter
    - active_in: active_in parameter
    - outlet_MPa_in: outlet_MPa_in parameter

Outputs:
    - demand: demand result

SysML Source: root-0/analyses/mfe_viability.sysml:92

    SysML Source: root-0/analyses/mfe_viability.sysml:92

    Calculation Specification:
        See documentation:
Required pump pressure rise MPa = outlet minus inlet; inactive returns zero. Finite active arithmetic is guarded. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: MR-7 conditional rating contract. **Last Updated**: 2026-09-20

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_viability.pump_pressure_rise_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Pump_Pressure_RiseModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, inlet_MPa_in: float, active_in: bool, outlet_MPa_in: float    ) -> Pump_Pressure_RiseInput:
        """Validate inputs and fill defaults.

        Args:
            inlet_MPa_in: inlet_MPa_in input
            active_in: active_in input
            outlet_MPa_in: outlet_MPa_in input

        Returns:
            Validated input model
        """
        return Pump_Pressure_RiseInput(inlet_MPa_in=inlet_MPa_in, active_in=active_in, outlet_MPa_in=outlet_MPa_in)

    def run(
        self, inlet_MPa_in: float, active_in: bool, outlet_MPa_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            inlet_MPa_in: inlet_MPa_in input
            active_in: active_in input
            outlet_MPa_in: outlet_MPa_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(inlet_MPa_in, active_in, outlet_MPa_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_viability.pump_pressure_rise_impl import (
            run_pump_pressure_rise,
        )

        # Execute implementation - returns single value
        demand = run_pump_pressure_rise(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(demand))
