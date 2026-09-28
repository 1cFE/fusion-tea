"""Ideal_Gas_CompressorModule Module Wrapper

TEAx module for Ideal_Gas_Compressor calculation.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. pout=pin*r; Tout=Tin*(1+(r^((gamma-1)/gamma)-1)/eta); shaft=mdot*cp*(Tout-Tin)/1e6. NASA compressor thermodynamics, retained authority pointer in knowledge/research/pending/20260907-163520_primary-loop-cycle-closure-prework.md section D. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

Inputs:
    - gamma_in: gamma_in parameter
    - cp_in: cp_in parameter
    - ratio_in: ratio_in parameter
    - temperature_in: temperature_in parameter
    - efficiency_in: efficiency_in parameter
    - flow_in: flow_in parameter
    - pressure_in: pressure_in parameter

Outputs:
    - pressure_out: pressure_out result
    - shaft_demand: shaft_demand result
    - temperature_out: temperature_out result

SysML Source: root-0/ideal_gas_brayton_components.sysml:3

SysML Source: root-0/ideal_gas_brayton_components.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/ideal_gas_brayton_components/ideal_gas_compressor_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.primitives import Float
from exchanger_architecture_thermal_tea.schemas.ideal_gas_compressor_output import Ideal_Gas_CompressorOutput


class Ideal_Gas_CompressorInput(BaseModel):
    """Input model for Ideal_Gas_CompressorModule.

    Attributes:
        gamma_in: gamma_in input
        cp_in: cp_in input
        ratio_in: ratio_in input
        temperature_in: temperature_in input
        efficiency_in: efficiency_in input
        flow_in: flow_in input
        pressure_in: pressure_in input
    """
    gamma_in: float = Field(..., description="gamma_in input")
    cp_in: float = Field(..., description="cp_in input")
    ratio_in: float = Field(..., description="ratio_in input")
    temperature_in: float = Field(..., description="temperature_in input")
    efficiency_in: float = Field(..., description="efficiency_in input")
    flow_in: float = Field(..., description="flow_in input")
    pressure_in: float = Field(..., description="pressure_in input")


class Ideal_Gas_CompressorModule(ModuleBase[Ideal_Gas_CompressorInput, Ideal_Gas_CompressorOutput]):
    """TEAx module for Ideal_Gas_Compressor calculation.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. pout=pin*r; Tout=Tin*(1+(r^((gamma-1)/gamma)-1)/eta); shaft=mdot*cp*(Tout-Tin)/1e6. NASA compressor thermodynamics, retained authority pointer in knowledge/research/pending/20260907-163520_primary-loop-cycle-closure-prework.md section D. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

Inputs:
    - gamma_in: gamma_in parameter
    - cp_in: cp_in parameter
    - ratio_in: ratio_in parameter
    - temperature_in: temperature_in parameter
    - efficiency_in: efficiency_in parameter
    - flow_in: flow_in parameter
    - pressure_in: pressure_in parameter

Outputs:
    - pressure_out: pressure_out result
    - shaft_demand: shaft_demand result
    - temperature_out: temperature_out result

SysML Source: root-0/ideal_gas_brayton_components.sysml:3

    SysML Source: root-0/ideal_gas_brayton_components.sysml:3

    Calculation Specification:
        See documentation:
Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. pout=pin*r; Tout=Tin*(1+(r^((gamma-1)/gamma)-1)/eta); shaft=mdot*cp*(Tout-Tin)/1e6. NASA compressor thermodynamics, retained authority pointer in knowledge/research/pending/20260907-163520_primary-loop-cycle-closure-prework.md section D. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

    IMPLEMENTATION: See exchanger_architecture_thermal_tea.handwritten.ideal_gas_brayton_components.ideal_gas_compressor_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts pressure_out, shaft_demand, temperature_out fields to separate channels.
    """

    name: str = "Ideal_Gas_CompressorModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, gamma_in: float, cp_in: float, ratio_in: float, temperature_in: float, efficiency_in: float, flow_in: float, pressure_in: float    ) -> Ideal_Gas_CompressorInput:
        """Validate inputs and fill defaults.

        Args:
            gamma_in: gamma_in input
            cp_in: cp_in input
            ratio_in: ratio_in input
            temperature_in: temperature_in input
            efficiency_in: efficiency_in input
            flow_in: flow_in input
            pressure_in: pressure_in input

        Returns:
            Validated input model
        """
        return Ideal_Gas_CompressorInput(gamma_in=gamma_in, cp_in=cp_in, ratio_in=ratio_in, temperature_in=temperature_in, efficiency_in=efficiency_in, flow_in=flow_in, pressure_in=pressure_in)

    def run(
        self, gamma_in: float, cp_in: float, ratio_in: float, temperature_in: float, efficiency_in: float, flow_in: float, pressure_in: float    ) -> ModuleResult[Ideal_Gas_CompressorOutput]:
        """Execute calculation.

        Args:
            gamma_in: gamma_in input
            cp_in: cp_in input
            ratio_in: ratio_in input
            temperature_in: temperature_in input
            efficiency_in: efficiency_in input
            flow_in: flow_in input
            pressure_in: pressure_in input

        Returns:
            Module result with Ideal_Gas_CompressorOutput (pressure_out, shaft_demand, temperature_out)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(gamma_in, cp_in, ratio_in, temperature_in, efficiency_in, flow_in, pressure_in)

        # Import handwritten implementation
        from exchanger_architecture_thermal_tea.handwritten.ideal_gas_brayton_components.ideal_gas_compressor_impl import (
            run_ideal_gas_compressor,
        )

        # Execute implementation - returns tuple of values
        pressure_out, shaft_demand, temperature_out = run_ideal_gas_compressor(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Ideal_Gas_CompressorOutput(
                pressure_out=pressure_out,
                shaft_demand=shaft_demand,
                temperature_out=temperature_out,
            )
        )
