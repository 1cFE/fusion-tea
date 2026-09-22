"""Heat_Driven_ClosureModule Module Wrapper

TEAx module for Heat_Driven_Closure calculation.

*Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic heat driven closure. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

Inputs:
    - pbli_cp_in: pbli_cp_in parameter
    - divertor_available_in: divertor_available_in parameter
    - pbli_ua_in: pbli_ua_in parameter
    - cp_in: cp_in parameter
    - pbli_limit_in: pbli_limit_in parameter
    - divertor_flow_in: divertor_flow_in parameter
    - gamma_in: gamma_in parameter
    - turbine_pressure_in: turbine_pressure_in parameter
    - cold_temperature_in: cold_temperature_in parameter
    - divertor_cp_in: divertor_cp_in parameter
    - return_pressure_in: return_pressure_in parameter
    - he_limit_in: he_limit_in parameter
    - pbli_flow_in: pbli_flow_in parameter
    - turbine_efficiency_in: turbine_efficiency_in parameter
    - pbli_available_in: pbli_available_in parameter
    - he_available_in: he_available_in parameter
    - divertor_limit_in: divertor_limit_in parameter
    - recuperator_effectiveness_in: recuperator_effectiveness_in parameter
    - flow_in: flow_in parameter
    - he_ua_in: he_ua_in parameter
    - he_cp_in: he_cp_in parameter
    - divertor_ua_in: divertor_ua_in parameter
    - he_flow_in: he_flow_in parameter

Outputs:
    - he_return: he_return result
    - he_unmet: he_unmet result
    - turbine_temperature: turbine_temperature result
    - he_hot: he_hot result
    - accepted_heat: accepted_heat result
    - divertor_return: divertor_return result
    - divertor_transferred: divertor_transferred result
    - he_secondary_in: he_secondary_in result
    - divertor_unmet: divertor_unmet result
    - he_state_defined: he_state_defined result
    - divertor_hot_terminal_difference: divertor_hot_terminal_difference result
    - pbli_hot: pbli_hot result
    - he_capability: he_capability result
    - divertor_cold_terminal_difference: divertor_cold_terminal_difference result
    - unmet_heat: unmet_heat result
    - iterations: iterations result
    - he_secondary_out: he_secondary_out result
    - pbli_return: pbli_return result
    - pbli_capability: pbli_capability result
    - pbli_unmet: pbli_unmet result
    - divertor_secondary_in: divertor_secondary_in result
    - divertor_hot_bound_margin: divertor_hot_bound_margin result
    - pbli_secondary_out: pbli_secondary_out result
    - divertor_state_defined: divertor_state_defined result
    - pbli_transferred: pbli_transferred result
    - he_hot_bound_margin: he_hot_bound_margin result
    - divertor_capability: divertor_capability result
    - pbli_secondary_in: pbli_secondary_in result
    - heater_inlet: heater_inlet result
    - closure_residual: closure_residual result
    - he_hot_terminal_difference: he_hot_terminal_difference result
    - pbli_hot_bound_margin: pbli_hot_bound_margin result
    - pbli_hot_terminal_difference: pbli_hot_terminal_difference result
    - divertor_hot: divertor_hot result
    - pbli_state_defined: pbli_state_defined result
    - divertor_secondary_out: divertor_secondary_out result
    - he_transferred: he_transferred result
    - pbli_cold_terminal_difference: pbli_cold_terminal_difference result
    - he_cold_terminal_difference: he_cold_terminal_difference result
    - expansion_factor: expansion_factor result

SysML Source: root-0/integrated_heat_electricity.sysml:46

SysML Source: root-0/integrated_heat_electricity.sysml:46

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_heat_electricity/heat_driven_closure_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.primitives import Float
from aries_integrated.schemas.heat_driven_closure_output import Heat_Driven_ClosureOutput


class Heat_Driven_ClosureInput(BaseModel):
    """Input model for Heat_Driven_ClosureModule.

    Attributes:
        pbli_cp_in: pbli_cp_in input
        divertor_available_in: divertor_available_in input
        pbli_ua_in: pbli_ua_in input
        cp_in: cp_in input
        pbli_limit_in: pbli_limit_in input
        divertor_flow_in: divertor_flow_in input
        gamma_in: gamma_in input
        turbine_pressure_in: turbine_pressure_in input
        cold_temperature_in: cold_temperature_in input
        divertor_cp_in: divertor_cp_in input
        return_pressure_in: return_pressure_in input
        he_limit_in: he_limit_in input
        pbli_flow_in: pbli_flow_in input
        turbine_efficiency_in: turbine_efficiency_in input
        pbli_available_in: pbli_available_in input
        he_available_in: he_available_in input
        divertor_limit_in: divertor_limit_in input
        recuperator_effectiveness_in: recuperator_effectiveness_in input
        flow_in: flow_in input
        he_ua_in: he_ua_in input
        he_cp_in: he_cp_in input
        divertor_ua_in: divertor_ua_in input
        he_flow_in: he_flow_in input
    """
    pbli_cp_in: float = Field(..., description="pbli_cp_in input")
    divertor_available_in: float = Field(..., description="divertor_available_in input")
    pbli_ua_in: float = Field(..., description="pbli_ua_in input")
    cp_in: float = Field(..., description="cp_in input")
    pbli_limit_in: float = Field(..., description="pbli_limit_in input")
    divertor_flow_in: float = Field(..., description="divertor_flow_in input")
    gamma_in: float = Field(..., description="gamma_in input")
    turbine_pressure_in: float = Field(..., description="turbine_pressure_in input")
    cold_temperature_in: float = Field(..., description="cold_temperature_in input")
    divertor_cp_in: float = Field(..., description="divertor_cp_in input")
    return_pressure_in: float = Field(..., description="return_pressure_in input")
    he_limit_in: float = Field(..., description="he_limit_in input")
    pbli_flow_in: float = Field(..., description="pbli_flow_in input")
    turbine_efficiency_in: float = Field(..., description="turbine_efficiency_in input")
    pbli_available_in: float = Field(..., description="pbli_available_in input")
    he_available_in: float = Field(..., description="he_available_in input")
    divertor_limit_in: float = Field(..., description="divertor_limit_in input")
    recuperator_effectiveness_in: float = Field(..., description="recuperator_effectiveness_in input")
    flow_in: float = Field(..., description="flow_in input")
    he_ua_in: float = Field(..., description="he_ua_in input")
    he_cp_in: float = Field(..., description="he_cp_in input")
    divertor_ua_in: float = Field(..., description="divertor_ua_in input")
    he_flow_in: float = Field(..., description="he_flow_in input")


class Heat_Driven_ClosureModule(ModuleBase[Heat_Driven_ClosureInput, Heat_Driven_ClosureOutput]):
    """TEAx module for Heat_Driven_Closure calculation.

*Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic heat driven closure. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

Inputs:
    - pbli_cp_in: pbli_cp_in parameter
    - divertor_available_in: divertor_available_in parameter
    - pbli_ua_in: pbli_ua_in parameter
    - cp_in: cp_in parameter
    - pbli_limit_in: pbli_limit_in parameter
    - divertor_flow_in: divertor_flow_in parameter
    - gamma_in: gamma_in parameter
    - turbine_pressure_in: turbine_pressure_in parameter
    - cold_temperature_in: cold_temperature_in parameter
    - divertor_cp_in: divertor_cp_in parameter
    - return_pressure_in: return_pressure_in parameter
    - he_limit_in: he_limit_in parameter
    - pbli_flow_in: pbli_flow_in parameter
    - turbine_efficiency_in: turbine_efficiency_in parameter
    - pbli_available_in: pbli_available_in parameter
    - he_available_in: he_available_in parameter
    - divertor_limit_in: divertor_limit_in parameter
    - recuperator_effectiveness_in: recuperator_effectiveness_in parameter
    - flow_in: flow_in parameter
    - he_ua_in: he_ua_in parameter
    - he_cp_in: he_cp_in parameter
    - divertor_ua_in: divertor_ua_in parameter
    - he_flow_in: he_flow_in parameter

Outputs:
    - he_return: he_return result
    - he_unmet: he_unmet result
    - turbine_temperature: turbine_temperature result
    - he_hot: he_hot result
    - accepted_heat: accepted_heat result
    - divertor_return: divertor_return result
    - divertor_transferred: divertor_transferred result
    - he_secondary_in: he_secondary_in result
    - divertor_unmet: divertor_unmet result
    - he_state_defined: he_state_defined result
    - divertor_hot_terminal_difference: divertor_hot_terminal_difference result
    - pbli_hot: pbli_hot result
    - he_capability: he_capability result
    - divertor_cold_terminal_difference: divertor_cold_terminal_difference result
    - unmet_heat: unmet_heat result
    - iterations: iterations result
    - he_secondary_out: he_secondary_out result
    - pbli_return: pbli_return result
    - pbli_capability: pbli_capability result
    - pbli_unmet: pbli_unmet result
    - divertor_secondary_in: divertor_secondary_in result
    - divertor_hot_bound_margin: divertor_hot_bound_margin result
    - pbli_secondary_out: pbli_secondary_out result
    - divertor_state_defined: divertor_state_defined result
    - pbli_transferred: pbli_transferred result
    - he_hot_bound_margin: he_hot_bound_margin result
    - divertor_capability: divertor_capability result
    - pbli_secondary_in: pbli_secondary_in result
    - heater_inlet: heater_inlet result
    - closure_residual: closure_residual result
    - he_hot_terminal_difference: he_hot_terminal_difference result
    - pbli_hot_bound_margin: pbli_hot_bound_margin result
    - pbli_hot_terminal_difference: pbli_hot_terminal_difference result
    - divertor_hot: divertor_hot result
    - pbli_state_defined: pbli_state_defined result
    - divertor_secondary_out: divertor_secondary_out result
    - he_transferred: he_transferred result
    - pbli_cold_terminal_difference: pbli_cold_terminal_difference result
    - he_cold_terminal_difference: he_cold_terminal_difference result
    - expansion_factor: expansion_factor result

SysML Source: root-0/integrated_heat_electricity.sysml:46

    SysML Source: root-0/integrated_heat_electricity.sysml:46

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic heat driven closure. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See aries_integrated.handwritten.integrated_heat_electricity.heat_driven_closure_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts he_return, he_unmet, turbine_temperature, he_hot, accepted_heat, divertor_return, divertor_transferred, he_secondary_in, divertor_unmet, he_state_defined, divertor_hot_terminal_difference, pbli_hot, he_capability, divertor_cold_terminal_difference, unmet_heat, iterations, he_secondary_out, pbli_return, pbli_capability, pbli_unmet, divertor_secondary_in, divertor_hot_bound_margin, pbli_secondary_out, divertor_state_defined, pbli_transferred, he_hot_bound_margin, divertor_capability, pbli_secondary_in, heater_inlet, closure_residual, he_hot_terminal_difference, pbli_hot_bound_margin, pbli_hot_terminal_difference, divertor_hot, pbli_state_defined, divertor_secondary_out, he_transferred, pbli_cold_terminal_difference, he_cold_terminal_difference, expansion_factor fields to separate channels.
    """

    name: str = "Heat_Driven_ClosureModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, pbli_cp_in: float, divertor_available_in: float, pbli_ua_in: float, cp_in: float, pbli_limit_in: float, divertor_flow_in: float, gamma_in: float, turbine_pressure_in: float, cold_temperature_in: float, divertor_cp_in: float, return_pressure_in: float, he_limit_in: float, pbli_flow_in: float, turbine_efficiency_in: float, pbli_available_in: float, he_available_in: float, divertor_limit_in: float, recuperator_effectiveness_in: float, flow_in: float, he_ua_in: float, he_cp_in: float, divertor_ua_in: float, he_flow_in: float    ) -> Heat_Driven_ClosureInput:
        """Validate inputs and fill defaults.

        Args:
            pbli_cp_in: pbli_cp_in input
            divertor_available_in: divertor_available_in input
            pbli_ua_in: pbli_ua_in input
            cp_in: cp_in input
            pbli_limit_in: pbli_limit_in input
            divertor_flow_in: divertor_flow_in input
            gamma_in: gamma_in input
            turbine_pressure_in: turbine_pressure_in input
            cold_temperature_in: cold_temperature_in input
            divertor_cp_in: divertor_cp_in input
            return_pressure_in: return_pressure_in input
            he_limit_in: he_limit_in input
            pbli_flow_in: pbli_flow_in input
            turbine_efficiency_in: turbine_efficiency_in input
            pbli_available_in: pbli_available_in input
            he_available_in: he_available_in input
            divertor_limit_in: divertor_limit_in input
            recuperator_effectiveness_in: recuperator_effectiveness_in input
            flow_in: flow_in input
            he_ua_in: he_ua_in input
            he_cp_in: he_cp_in input
            divertor_ua_in: divertor_ua_in input
            he_flow_in: he_flow_in input

        Returns:
            Validated input model
        """
        return Heat_Driven_ClosureInput(pbli_cp_in=pbli_cp_in, divertor_available_in=divertor_available_in, pbli_ua_in=pbli_ua_in, cp_in=cp_in, pbli_limit_in=pbli_limit_in, divertor_flow_in=divertor_flow_in, gamma_in=gamma_in, turbine_pressure_in=turbine_pressure_in, cold_temperature_in=cold_temperature_in, divertor_cp_in=divertor_cp_in, return_pressure_in=return_pressure_in, he_limit_in=he_limit_in, pbli_flow_in=pbli_flow_in, turbine_efficiency_in=turbine_efficiency_in, pbli_available_in=pbli_available_in, he_available_in=he_available_in, divertor_limit_in=divertor_limit_in, recuperator_effectiveness_in=recuperator_effectiveness_in, flow_in=flow_in, he_ua_in=he_ua_in, he_cp_in=he_cp_in, divertor_ua_in=divertor_ua_in, he_flow_in=he_flow_in)

    def run(
        self, pbli_cp_in: float, divertor_available_in: float, pbli_ua_in: float, cp_in: float, pbli_limit_in: float, divertor_flow_in: float, gamma_in: float, turbine_pressure_in: float, cold_temperature_in: float, divertor_cp_in: float, return_pressure_in: float, he_limit_in: float, pbli_flow_in: float, turbine_efficiency_in: float, pbli_available_in: float, he_available_in: float, divertor_limit_in: float, recuperator_effectiveness_in: float, flow_in: float, he_ua_in: float, he_cp_in: float, divertor_ua_in: float, he_flow_in: float    ) -> ModuleResult[Heat_Driven_ClosureOutput]:
        """Execute calculation.

        Args:
            pbli_cp_in: pbli_cp_in input
            divertor_available_in: divertor_available_in input
            pbli_ua_in: pbli_ua_in input
            cp_in: cp_in input
            pbli_limit_in: pbli_limit_in input
            divertor_flow_in: divertor_flow_in input
            gamma_in: gamma_in input
            turbine_pressure_in: turbine_pressure_in input
            cold_temperature_in: cold_temperature_in input
            divertor_cp_in: divertor_cp_in input
            return_pressure_in: return_pressure_in input
            he_limit_in: he_limit_in input
            pbli_flow_in: pbli_flow_in input
            turbine_efficiency_in: turbine_efficiency_in input
            pbli_available_in: pbli_available_in input
            he_available_in: he_available_in input
            divertor_limit_in: divertor_limit_in input
            recuperator_effectiveness_in: recuperator_effectiveness_in input
            flow_in: flow_in input
            he_ua_in: he_ua_in input
            he_cp_in: he_cp_in input
            divertor_ua_in: divertor_ua_in input
            he_flow_in: he_flow_in input

        Returns:
            Module result with Heat_Driven_ClosureOutput (he_return, he_unmet, turbine_temperature, he_hot, accepted_heat, divertor_return, divertor_transferred, he_secondary_in, divertor_unmet, he_state_defined, divertor_hot_terminal_difference, pbli_hot, he_capability, divertor_cold_terminal_difference, unmet_heat, iterations, he_secondary_out, pbli_return, pbli_capability, pbli_unmet, divertor_secondary_in, divertor_hot_bound_margin, pbli_secondary_out, divertor_state_defined, pbli_transferred, he_hot_bound_margin, divertor_capability, pbli_secondary_in, heater_inlet, closure_residual, he_hot_terminal_difference, pbli_hot_bound_margin, pbli_hot_terminal_difference, divertor_hot, pbli_state_defined, divertor_secondary_out, he_transferred, pbli_cold_terminal_difference, he_cold_terminal_difference, expansion_factor)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(pbli_cp_in, divertor_available_in, pbli_ua_in, cp_in, pbli_limit_in, divertor_flow_in, gamma_in, turbine_pressure_in, cold_temperature_in, divertor_cp_in, return_pressure_in, he_limit_in, pbli_flow_in, turbine_efficiency_in, pbli_available_in, he_available_in, divertor_limit_in, recuperator_effectiveness_in, flow_in, he_ua_in, he_cp_in, divertor_ua_in, he_flow_in)

        # Import handwritten implementation
        from aries_integrated.handwritten.integrated_heat_electricity.heat_driven_closure_impl import (
            run_heat_driven_closure,
        )

        # Execute implementation - returns tuple of values
        he_return, he_unmet, turbine_temperature, he_hot, accepted_heat, divertor_return, divertor_transferred, he_secondary_in, divertor_unmet, he_state_defined, divertor_hot_terminal_difference, pbli_hot, he_capability, divertor_cold_terminal_difference, unmet_heat, iterations, he_secondary_out, pbli_return, pbli_capability, pbli_unmet, divertor_secondary_in, divertor_hot_bound_margin, pbli_secondary_out, divertor_state_defined, pbli_transferred, he_hot_bound_margin, divertor_capability, pbli_secondary_in, heater_inlet, closure_residual, he_hot_terminal_difference, pbli_hot_bound_margin, pbli_hot_terminal_difference, divertor_hot, pbli_state_defined, divertor_secondary_out, he_transferred, pbli_cold_terminal_difference, he_cold_terminal_difference, expansion_factor = run_heat_driven_closure(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Heat_Driven_ClosureOutput(
                he_return=he_return,
                he_unmet=he_unmet,
                turbine_temperature=turbine_temperature,
                he_hot=he_hot,
                accepted_heat=accepted_heat,
                divertor_return=divertor_return,
                divertor_transferred=divertor_transferred,
                he_secondary_in=he_secondary_in,
                divertor_unmet=divertor_unmet,
                he_state_defined=he_state_defined,
                divertor_hot_terminal_difference=divertor_hot_terminal_difference,
                pbli_hot=pbli_hot,
                he_capability=he_capability,
                divertor_cold_terminal_difference=divertor_cold_terminal_difference,
                unmet_heat=unmet_heat,
                iterations=iterations,
                he_secondary_out=he_secondary_out,
                pbli_return=pbli_return,
                pbli_capability=pbli_capability,
                pbli_unmet=pbli_unmet,
                divertor_secondary_in=divertor_secondary_in,
                divertor_hot_bound_margin=divertor_hot_bound_margin,
                pbli_secondary_out=pbli_secondary_out,
                divertor_state_defined=divertor_state_defined,
                pbli_transferred=pbli_transferred,
                he_hot_bound_margin=he_hot_bound_margin,
                divertor_capability=divertor_capability,
                pbli_secondary_in=pbli_secondary_in,
                heater_inlet=heater_inlet,
                closure_residual=closure_residual,
                he_hot_terminal_difference=he_hot_terminal_difference,
                pbli_hot_bound_margin=pbli_hot_bound_margin,
                pbli_hot_terminal_difference=pbli_hot_terminal_difference,
                divertor_hot=divertor_hot,
                pbli_state_defined=pbli_state_defined,
                divertor_secondary_out=divertor_secondary_out,
                he_transferred=he_transferred,
                pbli_cold_terminal_difference=pbli_cold_terminal_difference,
                he_cold_terminal_difference=he_cold_terminal_difference,
                expansion_factor=expansion_factor,
            )
        )
