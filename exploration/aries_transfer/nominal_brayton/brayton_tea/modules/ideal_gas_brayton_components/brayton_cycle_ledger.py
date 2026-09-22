"""Brayton_Cycle_LedgerModule Module Wrapper

TEAx module for Brayton_Cycle_Ledger calculation.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. compressor_demand=W1+W2+W3; rejected_heat=-(Qic1+Qic2+Qpre); net_shaft=Wt-compressor_demand; shaft_efficiency=net_shaft/Qheater; energy_residual=Qheater-rejected_heat-net_shaft; total_pressure_ratio=pdischarge/pin. Cooling heats<=0, heater>0, shaft magnitudes>=0; signed net and residual preserved. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

Inputs:
    - compressor_3_in: compressor_3_in parameter
    - turbine_work_in: turbine_work_in parameter
    - inlet_pressure_in: inlet_pressure_in parameter
    - intercooler_2_in: intercooler_2_in parameter
    - intercooler_1_in: intercooler_1_in parameter
    - discharge_pressure_in: discharge_pressure_in parameter
    - compressor_2_in: compressor_2_in parameter
    - heater_in: heater_in parameter
    - precooler_in: precooler_in parameter
    - compressor_1_in: compressor_1_in parameter

Outputs:
    - shaft_efficiency: shaft_efficiency result
    - net_shaft: net_shaft result
    - compressor_demand: compressor_demand result
    - rejected_heat: rejected_heat result
    - energy_residual: energy_residual result
    - total_pressure_ratio: total_pressure_ratio result

SysML Source: root-0/ideal_gas_brayton_components.sysml:58

SysML Source: root-0/ideal_gas_brayton_components.sysml:58

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/ideal_gas_brayton_components/brayton_cycle_ledger_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from brayton_tea.primitives import Float
from brayton_tea.schemas.brayton_cycle_ledger_output import Brayton_Cycle_LedgerOutput


class Brayton_Cycle_LedgerInput(BaseModel):
    """Input model for Brayton_Cycle_LedgerModule.

    Attributes:
        compressor_3_in: compressor_3_in input
        turbine_work_in: turbine_work_in input
        inlet_pressure_in: inlet_pressure_in input
        intercooler_2_in: intercooler_2_in input
        intercooler_1_in: intercooler_1_in input
        discharge_pressure_in: discharge_pressure_in input
        compressor_2_in: compressor_2_in input
        heater_in: heater_in input
        precooler_in: precooler_in input
        compressor_1_in: compressor_1_in input
    """
    compressor_3_in: float = Field(..., description="compressor_3_in input")
    turbine_work_in: float = Field(..., description="turbine_work_in input")
    inlet_pressure_in: float = Field(..., description="inlet_pressure_in input")
    intercooler_2_in: float = Field(..., description="intercooler_2_in input")
    intercooler_1_in: float = Field(..., description="intercooler_1_in input")
    discharge_pressure_in: float = Field(..., description="discharge_pressure_in input")
    compressor_2_in: float = Field(..., description="compressor_2_in input")
    heater_in: float = Field(..., description="heater_in input")
    precooler_in: float = Field(..., description="precooler_in input")
    compressor_1_in: float = Field(..., description="compressor_1_in input")


class Brayton_Cycle_LedgerModule(ModuleBase[Brayton_Cycle_LedgerInput, Brayton_Cycle_LedgerOutput]):
    """TEAx module for Brayton_Cycle_Ledger calculation.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. compressor_demand=W1+W2+W3; rejected_heat=-(Qic1+Qic2+Qpre); net_shaft=Wt-compressor_demand; shaft_efficiency=net_shaft/Qheater; energy_residual=Qheater-rejected_heat-net_shaft; total_pressure_ratio=pdischarge/pin. Cooling heats<=0, heater>0, shaft magnitudes>=0; signed net and residual preserved. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

Inputs:
    - compressor_3_in: compressor_3_in parameter
    - turbine_work_in: turbine_work_in parameter
    - inlet_pressure_in: inlet_pressure_in parameter
    - intercooler_2_in: intercooler_2_in parameter
    - intercooler_1_in: intercooler_1_in parameter
    - discharge_pressure_in: discharge_pressure_in parameter
    - compressor_2_in: compressor_2_in parameter
    - heater_in: heater_in parameter
    - precooler_in: precooler_in parameter
    - compressor_1_in: compressor_1_in parameter

Outputs:
    - shaft_efficiency: shaft_efficiency result
    - net_shaft: net_shaft result
    - compressor_demand: compressor_demand result
    - rejected_heat: rejected_heat result
    - energy_residual: energy_residual result
    - total_pressure_ratio: total_pressure_ratio result

SysML Source: root-0/ideal_gas_brayton_components.sysml:58

    SysML Source: root-0/ideal_gas_brayton_components.sysml:58

    Calculation Specification:
        See documentation:
Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. compressor_demand=W1+W2+W3; rejected_heat=-(Qic1+Qic2+Qpre); net_shaft=Wt-compressor_demand; shaft_efficiency=net_shaft/Qheater; energy_residual=Qheater-rejected_heat-net_shaft; total_pressure_ratio=pdischarge/pin. Cooling heats<=0, heater>0, shaft magnitudes>=0; signed net and residual preserved. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

    IMPLEMENTATION: See brayton_tea.handwritten.ideal_gas_brayton_components.brayton_cycle_ledger_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts shaft_efficiency, net_shaft, compressor_demand, rejected_heat, energy_residual, total_pressure_ratio fields to separate channels.
    """

    name: str = "Brayton_Cycle_LedgerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, compressor_3_in: float, turbine_work_in: float, inlet_pressure_in: float, intercooler_2_in: float, intercooler_1_in: float, discharge_pressure_in: float, compressor_2_in: float, heater_in: float, precooler_in: float, compressor_1_in: float    ) -> Brayton_Cycle_LedgerInput:
        """Validate inputs and fill defaults.

        Args:
            compressor_3_in: compressor_3_in input
            turbine_work_in: turbine_work_in input
            inlet_pressure_in: inlet_pressure_in input
            intercooler_2_in: intercooler_2_in input
            intercooler_1_in: intercooler_1_in input
            discharge_pressure_in: discharge_pressure_in input
            compressor_2_in: compressor_2_in input
            heater_in: heater_in input
            precooler_in: precooler_in input
            compressor_1_in: compressor_1_in input

        Returns:
            Validated input model
        """
        return Brayton_Cycle_LedgerInput(compressor_3_in=compressor_3_in, turbine_work_in=turbine_work_in, inlet_pressure_in=inlet_pressure_in, intercooler_2_in=intercooler_2_in, intercooler_1_in=intercooler_1_in, discharge_pressure_in=discharge_pressure_in, compressor_2_in=compressor_2_in, heater_in=heater_in, precooler_in=precooler_in, compressor_1_in=compressor_1_in)

    def run(
        self, compressor_3_in: float, turbine_work_in: float, inlet_pressure_in: float, intercooler_2_in: float, intercooler_1_in: float, discharge_pressure_in: float, compressor_2_in: float, heater_in: float, precooler_in: float, compressor_1_in: float    ) -> ModuleResult[Brayton_Cycle_LedgerOutput]:
        """Execute calculation.

        Args:
            compressor_3_in: compressor_3_in input
            turbine_work_in: turbine_work_in input
            inlet_pressure_in: inlet_pressure_in input
            intercooler_2_in: intercooler_2_in input
            intercooler_1_in: intercooler_1_in input
            discharge_pressure_in: discharge_pressure_in input
            compressor_2_in: compressor_2_in input
            heater_in: heater_in input
            precooler_in: precooler_in input
            compressor_1_in: compressor_1_in input

        Returns:
            Module result with Brayton_Cycle_LedgerOutput (shaft_efficiency, net_shaft, compressor_demand, rejected_heat, energy_residual, total_pressure_ratio)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(compressor_3_in, turbine_work_in, inlet_pressure_in, intercooler_2_in, intercooler_1_in, discharge_pressure_in, compressor_2_in, heater_in, precooler_in, compressor_1_in)

        # Import handwritten implementation
        from brayton_tea.handwritten.ideal_gas_brayton_components.brayton_cycle_ledger_impl import (
            run_brayton_cycle_ledger,
        )

        # Execute implementation - returns tuple of values
        shaft_efficiency, net_shaft, compressor_demand, rejected_heat, energy_residual, total_pressure_ratio = run_brayton_cycle_ledger(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Brayton_Cycle_LedgerOutput(
                shaft_efficiency=shaft_efficiency,
                net_shaft=net_shaft,
                compressor_demand=compressor_demand,
                rejected_heat=rejected_heat,
                energy_residual=energy_residual,
                total_pressure_ratio=total_pressure_ratio,
            )
        )
